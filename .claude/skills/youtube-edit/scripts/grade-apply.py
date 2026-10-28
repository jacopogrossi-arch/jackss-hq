#!/usr/bin/env python3
"""grade-apply.py: grade a LOG clip with the official DJI LUT plus the approved exposure, and check the result.

It reads the report that grade-scan.py wrote for the same clip (profile, LUT, proposed exposure). Two steps, on purpose:

  PREVIEW (default)  no video is written. It draws before / after sheets for a few frames: the LOG picture, the picture
                     with the LUT alone, the picture with the LUT and the exposure, zebra on the last one, and its
                     waveform, vectorscope and histogram. This is what you approve.
  --render           encodes the graded clip (4K, 10-bit HEVC by default), then reads the FILE back and checks it:
                     the measured frames must match what the preview predicted, highlights must not clip, skin must
                     sit where the proposal aimed. Writes CHECK.md next to the render. Exit 1 on a FAIL.

The exposure is a gain on the graded Rec.709 signal, in stops of display light (gamma 2.4): code value x 2**(stops / 2.4).
It is applied after the LUT, never on the log signal. Highlights above 100 % clip, so scan's proposal already stops short
of them; --stops overrides the proposal.

Usage:
  python3 grade-apply.py --video clip.MP4 --scan DIR/report.json --out DIR [--stops 0.5] [--frames 3]      # preview
  python3 grade-apply.py --video clip.MP4 --scan DIR/report.json --out DIR --render [--stops 0.5]
                         [--encoder x265|nvenc] [--crf 16]
Writes DIR/preview-NN.png (+ preview-sheet.png); with --render also DIR/graded.mp4 and DIR/CHECK.md."""
import argparse, importlib.util, json, os, shutil, subprocess, sys, tempfile

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("grade_scan", os.path.join(HERE, "grade-scan.py"))
gs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gs)
spec_l = importlib.util.spec_from_file_location("grade_looks", os.path.join(HERE, "grade-looks.py"))
gl = importlib.util.module_from_spec(spec_l)
spec_l.loader.exec_module(gl)
spec_f = importlib.util.spec_from_file_location("grade_film", os.path.join(HERE, "grade-film.py"))
gf = importlib.util.module_from_spec(spec_f)
spec_f.loader.exec_module(gf)

GAMMA = 2.4
TOL_PRED = 0.015         # measured vs predicted luma, mean absolute, 1.5 IRE (compression and 8/10 bit round-trips)
MAX_CLIP, MAX_CRUSH = 0.01, 0.05
MAX_STOPS = gs.CFG["max_stops_apply"]   # ffmpeg's colorchannelmixer takes a gain up to x2 (= 2.4 stops); stay clear of it


def gain(stops):
    return 2.0 ** (stops / GAMMA)


def expose(rgb, stops, wb=None, look=None, white=None):
    """The whole correction after the LUT: exposure, the white-balance gains (red, blue; green = 1) when given, then the look.
    A film look (one with a "film" key) does all of it in linear light instead: see grade-film.py; `white` is the clip's measured white."""
    if gf.is_film(look):
        return gf.apply(rgb, look, stops, wb, white)
    g = gain(stops)
    mul = np.array([g * (wb[0] if wb else 1.0), g, g * (wb[1] if wb else 1.0)], dtype=np.float32)
    out = np.clip(rgb * mul, 0.0, 1.0)
    return gl.apply_look(out, look) if look else out


def bake_look(look_params, path, n=65):
    """Write the look as a .cube (red varies fastest): a look is a pure colour function, so it fits a 3D table; ffmpeg applies it with tetrahedral interpolation."""
    lin = np.linspace(0, 1, n, dtype=np.float32)
    r = np.tile(lin, n * n)
    g = np.tile(np.repeat(lin, n), n)
    b = np.repeat(lin, n * n)
    out = gl.apply_look(np.stack([r, g, b], axis=-1)[:, None, :], look_params)[:, 0, :]
    with open(path, "w") as fh:
        for line in ("LUT_3D_SIZE %d" % n, "DOMAIN_MIN 0 0 0", "DOMAIN_MAX 1 1 1"):
            fh.write(line + "\n")
        np.savetxt(fh, out, fmt="%.6f")


def soften(y, r=3):
    """A luma picture blurred a little: grain and its random pattern average out, the grade itself stays."""
    from PIL import ImageFilter
    return np.asarray(Image.fromarray(gs.to_u8(y)).filter(ImageFilter.GaussianBlur(r))).astype(np.float32) / 255.0


def pick(samples, n):
    if n >= len(samples):
        return list(range(len(samples)))
    return sorted(set(int(round(i * (len(samples) - 1) / (n - 1))) for i in range(n))) if n > 1 else [len(samples) // 2]


def tile(img, w, h, label):
    t = Image.fromarray(gs.to_u8(img) if img.dtype != np.uint8 else img).resize((w, h))
    ImageDraw.Draw(t).text((6, 4), label, fill=(255, 255, 255))
    return t


def sheet(log_rgb, lut_rgb, final_rgb, t, label):
    H, Wd, _ = log_rgb.shape
    tw = 400
    th = int(tw * H / Wd)
    out = Image.new("RGB", (tw * 3 + 16, th + 8 + 256 + 24), (20, 20, 20))
    out.paste(tile(log_rgb, tw, th, "LOG as shot"), (0, 20))
    out.paste(tile(lut_rgb, tw, th, "LUT only"), (tw + 8, 20))
    out.paste(tile(gs.zebra_image(final_rgb), tw, th, label), (tw * 2 + 16, 20))
    wf = gs.waveform_parade(final_rgb, w=tw, h=256)
    hg = gs.histogram_img(final_rgb, w=tw, h=160)
    vs = gs.vectorscope(final_rgb, size=256)
    out.paste(wf, (0, th + 28))
    out.paste(hg, (tw + 8, th + 28))
    out.paste(vs, (tw * 2 + 16, th + 28))
    ImageDraw.Draw(out).text((4, 4), "t=%.1fs   final signal: waveform, histogram, vectorscope (zebra on the right picture)" % t, fill=(220, 220, 220))
    return out


def has_nvenc():
    try:
        enc = subprocess.run(["ffmpeg", "-hide_banner", "-encoders"], capture_output=True, text=True).stdout
        return "hevc_nvenc" in enc and subprocess.run(["nvidia-smi", "-L"], capture_output=True).returncode == 0
    except OSError:
        return False


def encode(video, lut_path, stops, wb, look, out, encoder, crf, meta, smooth=0, white=None, size=None, fps=25):
    tmp = tempfile.mkdtemp(prefix="grade-apply-")
    try:
        shutil.copy(lut_path, os.path.join(tmp, "lut.cube"))       # a relative name: a Windows 'D:' path breaks lut3d
        g = gain(stops)
        denoise = {1: "hqdn3d=1.5:1.5:3:3,", 2: "hqdn3d=3:3:5:5,"}.get(smooth, "")      # before the LUT: the noise is smaller there, the LUT stretches it
        vf = denoise + "format=gbrp10le,lut3d=file=lut.cube:interp=tetrahedral"
        if gf.is_film(look):                                       # DJI LUT, exposure, white balance, tone and colour in ONE table; then the finish graph
            gf.bake(look, os.path.join(tmp, "film.cube"), stops, wb, white, pre=gs.load_cube(lut_path))
            vf = "[0:v]" + denoise + "format=gbrp10le,lut3d=file=film.cube:interp=tetrahedral[in];" + gf.finish_graph(size[0], size[1], look, fps=fps) + ";[out]format=yuv420p10le[v]"
        else:
            if abs(stops) > 1e-6 or wb:
                vf += ",colorchannelmixer=rr=%.6f:gg=%.6f:bb=%.6f" % (g * (wb[0] if wb else 1.0), g, g * (wb[1] if wb else 1.0))
            if look:
                bake_look(look, os.path.join(tmp, "look.cube"))
                vf += ",lut3d=file=look.cube:interp=tetrahedral"
            vf += ",format=yuv420p10le"
        if encoder == "nvenc":
            venc = ["-c:v", "hevc_nvenc", "-preset", "p5", "-rc", "vbr", "-cq", str(crf + 4), "-b:v", "0", "-profile:v", "main10", "-pix_fmt", "p010le"]
        else:
            venc = ["-c:v", "libx265", "-preset", "medium", "-crf", str(crf), "-x265-params", "log-level=error", "-pix_fmt", "yuv420p10le"]
        vsel = ["-filter_complex", vf, "-map", "[v]"] if gf.is_film(look) else ["-map", "0:v:0", "-vf", vf]
        cmd = ["ffmpeg", "-y", "-v", "error", "-i", os.path.abspath(video)] + vsel + ["-map", "0:a:0?"] + venc + [
            "-c:a", "copy", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-color_range", "tv",
            "-tag:v", "hvc1", "-movflags", "+faststart+use_metadata_tags", "-metadata", "comment=" + meta, os.path.abspath(out)]
        p = subprocess.run(cmd, cwd=tmp, capture_output=True, text=True)
        if p.returncode != 0:
            raise RuntimeError(p.stderr[-600:])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--scan", required=True, help="report.json from grade-scan.py for this clip")
    ap.add_argument("--out", required=True)
    ap.add_argument("--stops", type=float, help="exposure in stops; default = the scan's proposal")
    ap.add_argument("--wb", action="store_true", help="also apply the white-balance gains the scan measured on near-neutral objects (only if it found some)")
    ap.add_argument("--wb-gains", help="your own white-balance gains, 'R,B' (green = 1), e.g. 1.03,0.97; wins over --wb")
    ap.add_argument("--smooth", type=int, default=0, choices=[0, 1, 2], help="light (1) or medium (2) noise reduction before the LUT: smoother skin and water, softer detail (Jacopo's own grade is softer than the camera file)")
    ap.add_argument("--look-cube", help="a ready-made creative .cube LUT (made for Rec.709) used as the look; --look-mix says how much (0-1). Third-party LUTs stay local, in assets/looks/external/")
    ap.add_argument("--look-mix", type=float, default=1.0)
    ap.add_argument("--log-cube", help="a ready-made creative .cube LUT that reads the LOG file directly and replaces the technical DJI LUT (e.g. adimology-p4p/adimology-P4P-IndieHaze.cube, built on the Pocket 4P D-Log curve); a bare name is looked up in assets/looks/external/")
    ap.add_argument("--look", help="a look from the preset (see grade-looks.py), applied after the LUT, exposure and white balance, e.g. blockbuster")
    ap.add_argument("--match", help="match.json from grade-match.py: this clip's exposure and white balance come from the shot matching (--stops / --wb-gains still win)")
    ap.add_argument("--frames", type=int, default=3, help="frames in the preview")
    ap.add_argument("--render", action="store_true", help="encode the graded clip and check it (needs your approval of the preview)")
    ap.add_argument("--encoder", default="auto", choices=["auto", "x265", "nvenc"], help="auto = the video card when ffmpeg and the driver offer it (about 4x faster), else the CPU")
    ap.add_argument("--crf", type=int, default=16)
    args = ap.parse_args()

    rep = json.load(open(args.scan, encoding="utf8"))
    prof = rep["profile"]
    if not prof["certain"]:
        print("The scan says the profile is NOT certain (%s). Settle the profile first: rerun grade-scan with --profile." % prof["why"])
        return 1
    lut_path = os.path.join(gs.LUTS, prof["lut"])
    if args.log_cube:
        lut_path = args.log_cube if os.path.isabs(args.log_cube) else os.path.join(os.path.dirname(gs.LUTS), "looks", "external", args.log_cube)
    lut_t = gs.load_cube(lut_path)
    matched = None
    if args.match:
        mt = json.load(open(args.match, encoding="utf8"))["clips"]
        matched = mt.get(os.path.abspath(args.video)) or mt.get(os.path.basename(args.video))
        if not matched:
            print("%s is not in %s (have: %s)" % (os.path.basename(args.video), args.match, ", ".join(mt)))
            return 1
        if args.wb_gains is None and matched.get("wb_gains"):
            args.wb_gains = "%.4f,%.4f" % tuple(matched["wb_gains"])
    stops = (matched["stops"] if matched else rep["proposal"]["exposure_stops"]) if args.stops is None else args.stops
    if abs(stops) > MAX_STOPS:
        print("%+.2f stops is out of range: the limit is +-%.1f (a bigger push is a re-shoot, not a grade)." % (stops, MAX_STOPS))
        return 1
    look = None
    if args.look_cube:
        look = {"cube": args.look_cube, "cube_mix": args.look_mix}
        args.look = "cube:" + os.path.basename(args.look_cube) + ("@%.0f%%" % (args.look_mix * 100) if args.look_mix != 1 else "")
    elif args.look:
        looks = gs.CFG.get("looks", {})
        if args.look not in looks:
            print("unknown look %r (have: %s)" % (args.look, ", ".join(looks)))
            return 1
        look = looks[args.look]["p"]
    wb = None
    if args.wb_gains:
        try:
            wb = [float(x) for x in args.wb_gains.split(",")]
            assert len(wb) == 2
        except (ValueError, AssertionError):
            print("--wb-gains wants two numbers, 'R,B', for example 1.03,0.97")
            return 1
    elif args.wb:
        wb = rep["proposal"].get("wb_gains")
        if not wb:
            print("No white-balance correction: %s" % rep["proposal"].get("wb_gains_why", "the scan found none"))
    lim = gs.CFG["max_wb_gain"]
    if wb and (max(abs(wb[0] - 1), abs(wb[1] - 1)) > lim + 1e-9 or gain(stops) * max(wb) > 2.0):
        print("White-balance gains %s are out of range (limit +-%.0f %%, and exposure times gain must stay under x2)." % (wb, lim * 100))
        return 1
    os.makedirs(args.out, exist_ok=True)

    meta = rep["meta"]
    w = gs.W_STATS
    h = int(round(w * meta["h"] / meta["w"] / 2) * 2)
    samples = rep["samples"]
    fps = meta.get("fps") or "25"
    film = gf.is_film(look)
    white = None
    if film:                                                   # the clip's white, measured once: the highlight stretch is the same on every frame (no flicker)
        white = gf.measure_white([gs.apply_lut(gs.grab(args.video, s["t"], w, h), lut_t) for s in samples])
        print("Film look: clip white %.3f (linear), highlight stretch x%.2f" % (white, gf.stretch_for(white * 2.0 ** stops, gf.film_params(look))))
    idx = pick(samples, args.frames)
    sheets = []
    for k, i in enumerate(idx):
        t = samples[i]["t"]
        f = gs.grab(args.video, t, w, h)
        lut_rgb = gs.apply_lut(f, lut_t)
        fin = expose(lut_rgb, stops, wb, look, white)
        if film:
            fin = gf.finish_image(fin, look, fps)
        s = sheet(f, lut_rgb, fin, t, "LUT %+.2f stops%s%s" % (stops, (" WB R x%.3f B x%.3f" % tuple(wb)) if wb else "", (" + look " + args.look) if look else ""))
        s.save(os.path.join(args.out, "preview-%02d.png" % (k + 1)))
        sheets.append(s)
    big = Image.new("RGB", (sheets[0].width, sum(x.height for x in sheets)), (20, 20, 20))
    y = 0
    for s in sheets:
        big.paste(s, (0, y))
        y += s.height
    big.save(os.path.join(args.out, "preview-sheet.png"))
    print("Profile: %s | LUT: %s | exposure: %+.2f stops (%s) | white balance: %s" % (
        prof["label"], prof["lut"], stops, "your value" if args.stops is not None else ("the shot matching" if matched else "the scan's proposal"),
        ("R x%.3f, B x%.3f" % tuple(wb)) if wb else "untouched") + " | look: %s" % (args.look or "none"))
    print("Preview: %s" % os.path.join(args.out, "preview-sheet.png"))
    if not args.render:
        print("No video written. Look at the preview, then run again with --render (and --stops N if you want another value).")
        return 0

    # ------------------------------------------------------------------ render and check the FILE
    if args.encoder == "auto":
        args.encoder = "nvenc" if has_nvenc() else "x265"
    out_mp4 = os.path.join(args.out, "graded.mp4")
    print("Encoder: %s" % args.encoder)
    note = "graded with %s, exposure %+.2f stops%s%s (grade-apply.py)" % (prof["lut"], stops, (", white balance R x%.3f B x%.3f" % tuple(wb)) if wb else "", (", look %s" % args.look) if look else "")
    print("Rendering %s ..." % out_mp4)
    try:
        encode(args.video, lut_path, stops, wb, look, out_mp4, args.encoder, args.crf, note, args.smooth, white, (meta["w"], meta["h"]), fps)
    except Exception as e:  # noqa
        print("render failed:", e)
        return 1

    fails, lines = [], []
    pred_err, meas = [], []
    for i in range(len(samples)):
        t = samples[i]["t"]
        src = gs.grab(args.video, t, w, h)
        got = gs.grab(out_mp4, t, w, h)
        if src is None or got is None:
            continue
        predicted = expose(gs.apply_lut(src, lut_t), stops, wb, look, white)
        if film:                                               # the finish is in the file too; grain is random, so compare softened pictures
            predicted = gf.finish_image(predicted, look, fps)
            pred_err.append(float(np.abs(soften(gs.luma(predicted)) - soften(gs.luma(got))).mean()))
        else:
            pred_err.append(float(np.abs(gs.luma(predicted) - gs.luma(got)).mean()))
        meas.append(gs.frame_stats(got))
    perr = float(np.mean(pred_err))
    clip = float(np.mean([m["clip"] for m in meas]))
    crush = float(np.mean([m["crush"] for m in meas]))
    p995 = float(np.mean([m["p99.5"] for m in meas]))
    skin = [m["skin_luma"] for m in meas if m["skin_luma"] is not None and m["skin_frac"] >= 0.01]
    before = rep["proposal"]

    def check(ok, text):
        lines.append("- %s %s" % ("PASS" if ok else "FAIL", text))
        if not ok:
            fails.append(text)

    check(perr <= TOL_PRED, "the file matches the preview's prediction: mean luma difference %.1f IRE (limit %.1f)" % (perr * 100, TOL_PRED * 100))
    check(clip <= MAX_CLIP, "clipped highlights %.2f %% of the picture (limit %.0f %%)" % (clip * 100, MAX_CLIP * 100))
    max_crush = gs.CFG.get("look_max_crush", 0.12) if look else MAX_CRUSH      # a look crushes the blacks on purpose
    check(crush <= max_crush, "crushed blacks %.2f %% of the picture (limit %.0f %%)" % (crush * 100, max_crush * 100))
    if look and skin:
        lines.append("- INFO skin at %.0f IRE with the look %s (the look sets its own skin level; the band check is for the exposure-only grade)" % (float(np.median(skin)) * 100, args.look))
    elif skin and before.get("exposure_anchor") == "skin":
        sk = float(np.median(skin)) * 100
        lo, hi = [round(x * 100) for x in before.get("band", gs.CFG["skin_band"])]
        centre = before.get("target", gs.CFG["skin_target"]) * 100
        was = before["exposure_anchor_ire"]
        moved_right = (lo <= sk <= hi) or abs(sk - centre) < abs(was - centre)
        check(moved_right, "skin at %.0f IRE (was %.0f, band %d-%d)" % (sk, was, lo, hi))
        if not lo <= sk <= hi:
            lines.append("- INFO skin is still outside the band: the highlights leave no room to lift the whole picture. "
                         "Lifting the subject alone needs a local adjustment (a mask), which this step does not do.")
    else:
        lines.append("- INFO no skin anchor for this clip; exposure was judged on the median")
    lines.append("- INFO highlights (99.5th percentile) now at %.0f IRE; median %.0f IRE" % (p995 * 100, float(np.mean([m["median"] for m in meas])) * 100))
    md = ["# Check of the graded file", "", "File: `%s`" % out_mp4, "Recipe: " + note, "", "## Result: %s" % ("FAIL" if fails else "PASS"), ""] + lines + [
        "", "The file was read back and measured at the same %d moments as the scan; nothing here is read from the encoder's settings." % len(meas)]
    with open(os.path.join(args.out, "CHECK.md"), "w", encoding="utf8") as fh:
        fh.write("\n".join(md) + "\n")
    print("\n".join(md))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
