#!/usr/bin/env python3
"""grade-scan.py: measure a LOG clip (D-Log, D-Log2, D-Log M) before grading it, and propose the corrections.

Nothing is changed: this only reads the clip and writes a report to look at. The grade itself is a later step
(grade-apply.py), run only after the proposal is approved.

What it does
  1. Reads the file's metadata for the camera and the log profile. A clip that was re-encoded has lost them.
  2. Takes N frames spread over the clip, decodes them as the camera wrote them (log code values, no conversion).
  3. Applies the official DJI LUT of the profile (assets/luts/) to those frames, in numpy.
  4. Measures the LOG frames and the GRADED frames: percentiles of luma, % of pixels in each zone, zebra at 95 % and
     100 % IRE, crushed blacks, mean chroma (white balance), spread between samples (an exposure change inside the clip).
  5. Writes scopes for each sample: log picture, graded picture with zebra, RGB parade waveform, vectorscope, histogram.
  6. Proposes an exposure correction (in stops, applied on the graded Rec.709 signal) and a white-balance tendency.

If the profile is not in the metadata and not given with --profile, every candidate LUT is tried and ranked by how
sane the result is (few clipped highlights, few crushed blacks, medium level, not over-saturated). That ranking is a
HINT, never a decision: the report says so and the grade waits for a word.

Usage:
  python3 grade-scan.py --video clip.MP4 --out DIR [--profile auto|dlog|dlog2|dlogm] [--samples 12]
Writes DIR/report.json, DIR/REPORT.md, DIR/scopes-NN.png (one per sample) and DIR/scopes-sheet.png.
Exit 0 always, unless the file cannot be read (exit 1)."""
import argparse, json, math, os, re, subprocess, sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
LUTS = os.path.join(os.path.dirname(HERE), "assets", "luts")

# Every tunable value lives in presets/vacanze-grading/preset.json ("grade"); these are the same values, used if the file is missing.
DEFAULTS = {
    "luts": {
        "dlog2": ["D-Log2 (Osmo Pocket 4P)", "DJI-Pocket4P-DLog2-to-Rec709-size65.cube"],
        "dlog": ["D-Log (Osmo Pocket 4P)", "DJI-Pocket4P-DLog-to-Rec709-V2.0-size33.cube"],
        "dlogm": ["D-Log M (Osmo Nano)", "DJI-OsmoNano-DLogM-to-Rec709-V1.cube"],
    },
    "zebra": 0.95, "clip": 0.995, "crush": 0.02,
    "skin_band": [0.50, 0.68], "skin_target": 0.60, "median_band": [0.35, 0.55], "median_target": 0.42,
    "highlight_ceiling": 0.97, "max_stops_scan": 1.5, "max_stops_apply": 2.0, "max_wb_gain": 0.12,
    "wb_neutral_chroma": 0.02, "wb_min_frac": 0.01,     # a pixel counts as neutral under this chroma; a frame needs this share of them (measured 23/10: at 0.06 it took 67 % of a beach)
}


def load_cfg(preset="vacanze-grading"):
    cfg = json.loads(json.dumps(DEFAULTS))
    path = os.path.join(os.path.dirname(HERE), "presets", preset, "preset.json")
    if os.path.exists(path):
        with open(path, encoding="utf8") as fh:
            cfg.update(json.load(fh).get("grade", {}))
    return cfg


CFG = load_cfg()
# profile -> (label, LUT file in assets/luts/). One entry per log curve, not per camera.
PROFILES = {k: tuple(v) for k, v in CFG["luts"].items()}
# camera name found in the metadata -> the profiles it can record
CAMERAS = {"nano": ["dlogm"], "pocket 4p": ["dlog", "dlog2"], "pocket4p": ["dlog", "dlog2"]}

W_STATS = 960            # decode width for the measurements
ZEBRA_HI, ZEBRA_CLIP, CRUSH = CFG["zebra"], CFG["clip"], CFG["crush"]
MAX_STOPS = CFG["max_stops_scan"]
GAMMA_APPLY = 2.4        # exposure is a gain on the graded signal: code x 2**(stops / 2.4), the same law grade-apply.py uses


def sh(cmd, binary=False):
    p = subprocess.run(cmd, capture_output=True)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.decode("utf8", "replace")[-400:])
    return p.stdout if binary else p.stdout.decode("utf8", "replace")


# ---------------------------------------------------------------- metadata
def probe(path):
    j = json.loads(sh(["ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", path]))
    v = next(s for s in j["streams"] if s["codec_type"] == "video")
    rot = 0
    for sd in v.get("side_data_list", []) or []:
        rot = int(sd.get("rotation", rot) or 0)
    w, h = int(v["width"]), int(v["height"])
    if abs(rot) % 180 == 90:
        w, h = h, w
    tags = {}
    tags.update(j["format"].get("tags", {}) or {})
    for s in j["streams"]:
        for k, val in (s.get("tags", {}) or {}).items():
            tags["%s:%s" % (s["index"], k)] = val
    data_streams = [s.get("codec_tag_string", "") + ":" + s.get("codec_name", "") for s in j["streams"] if s["codec_type"] == "data"]
    return {
        "w": w, "h": h, "duration": float(j["format"]["duration"]), "codec": v.get("codec_name"),
        "pix_fmt": v.get("pix_fmt"), "range": v.get("color_range", "unspecified"), "space": v.get("color_space"),
        "transfer": v.get("color_transfer"), "fps": v.get("r_frame_rate"), "tags": tags, "data_streams": data_streams,
    }


def read_profile_from_metadata(meta):
    """Return (profiles, why). profiles: list of keys; [] = nothing found. Looks only at the text the file carries."""
    gamma = str(meta["tags"].get("com.dji.camera.ColorGammaSxS", "")).strip().lower()   # DJI writes the profile here
    if gamma:
        g = re.sub(r"[^a-z0-9]", "", gamma)
        for key, hit in (("dlogm", "dlogm"), ("dlog2", "dlog2"), ("dlog", "dlog")):
            if g == key:
                return [hit], "the file says so (com.dji.camera.ColorGammaSxS = %s)" % meta["tags"]["com.dji.camera.ColorGammaSxS"].strip()
    blob = " ".join(str(x) for x in meta["tags"].values()).lower() + " " + " ".join(meta["data_streams"]).lower()
    if re.search(r"d-?log\s*-?m\b", blob):
        return ["dlogm"], "metadata names D-Log M"
    if re.search(r"d-?log\s*-?2", blob):
        return ["dlog2"], "metadata names D-Log2"
    if re.search(r"d-?log\b", blob):
        return ["dlog"], "metadata names D-Log"
    for name, profs in CAMERAS.items():
        if name in blob:
            return list(profs), "metadata names the camera (%s), which records %s" % (name, " or ".join(profs))
    return [], "no camera or profile in the metadata (a re-encoded file loses them)"


# ---------------------------------------------------------------- LUT
def load_cube(path):
    n, rows, dmin, dmax = None, [], 0.0, 1.0
    with open(path) as f:
        for line in f:
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            if s.startswith("LUT_3D_SIZE"):
                n = int(s.split()[1])
            elif s.startswith("DOMAIN_MIN"):
                dmin = float(s.split()[1])
            elif s.startswith("DOMAIN_MAX"):
                dmax = float(s.split()[1])
            elif s[0] in "-0123456789.":
                rows.append([float(x) for x in s.split()[:3]])
    lut = np.asarray(rows, dtype=np.float32).reshape(n, n, n, 3)  # [b][g][r] (red varies fastest)
    return lut, dmin, dmax


def apply_lut(rgb, lut_t):
    """rgb: float array (...,3) in 0-1. Trilinear lookup. lut_t = (lut, dmin, dmax)."""
    lut, dmin, dmax = lut_t
    n = lut.shape[0]
    x = (np.clip(rgb, dmin, dmax) - dmin) / (dmax - dmin) * (n - 1)
    i0 = np.minimum(np.floor(x).astype(np.int32), n - 2)
    f = (x - i0).astype(np.float32)
    r0, g0, b0 = i0[..., 0], i0[..., 1], i0[..., 2]
    fr, fg, fb = f[..., 0:1], f[..., 1:2], f[..., 2:3]
    out = 0
    for db in (0, 1):
        for dg in (0, 1):
            for dr in (0, 1):
                wgt = (fr if dr else 1 - fr) * (fg if dg else 1 - fg) * (fb if db else 1 - fb)
                out = out + wgt * lut[b0 + db, g0 + dg, r0 + dr]
    return np.clip(out, 0.0, 1.0)


# ---------------------------------------------------------------- frames
def grab(path, t, w, h):
    raw = sh(["ffmpeg", "-v", "error", "-ss", "%.3f" % t, "-i", path, "-frames:v", "1",
              "-vf", "scale=%d:%d:flags=area,format=rgb48le" % (w, h), "-f", "rawvideo", "-"], binary=True)
    if len(raw) < w * h * 6:
        return None
    return (np.frombuffer(raw[: w * h * 6], dtype="<u2").reshape(h, w, 3).astype(np.float32)) / 65535.0


def to_u8(img):
    """Float 0-1 -> 8-bit with a little noise first (dither): without it a smooth sky shows false bands in the preview PNG that the 10-bit video does not have."""
    rng = np.random.default_rng(7)
    noise = (rng.random(img.shape, dtype=np.float32) + rng.random(img.shape, dtype=np.float32) - 1.0) * 0.5
    return np.clip(np.floor(np.clip(img, 0, 1) * 255 + 0.5 + noise), 0, 255).astype(np.uint8)


def luma(rgb):
    return rgb[..., 0] * 0.2126 + rgb[..., 1] * 0.7152 + rgb[..., 2] * 0.0722


# ---------------------------------------------------------------- measurements
def wb_estimate(rgb):
    """Gains (R, B; green = 1) that would make the near-neutral objects of the frame neutral: clouds, a white boat, a grey wall.
    Returns (gains or None, fraction of the picture used). Pixels: mid-to-light, barely coloured, not clipped."""
    y = luma(rgb)
    cb = (rgb[..., 2] - y) / 1.8556
    cr = (rgb[..., 0] - y) / 1.5748
    m = (y > 0.45) & (y < 0.92) & (np.sqrt(cb ** 2 + cr ** 2) < CFG["wb_neutral_chroma"]) & (rgb.max(axis=2) < 0.97)
    frac = float(m.mean())
    if m.sum() < 200:
        return None, frac
    r, g, b = (float(rgb[..., c][m].mean()) for c in range(3))
    return [g / max(r, 1e-6), g / max(b, 1e-6)], frac


def frame_stats(rgb):
    y = luma(rgb).ravel()
    p = np.percentile(y, [0.5, 1, 5, 25, 50, 75, 95, 99, 99.5])
    cb = (rgb[..., 2] - luma(rgb)) / 1.8556
    cr = (rgb[..., 0] - luma(rgb)) / 1.5748
    ang = np.degrees(np.arctan2(cr, cb)) % 360
    chroma = np.sqrt(cb ** 2 + cr ** 2)
    yy = luma(rgb)
    skin = (ang > 108) & (ang < 138) & (chroma > 0.03) & (chroma < 0.22) & (yy > 0.2) & (yy < 0.92)
    wb, wbf = wb_estimate(rgb)
    return {
        "wb": wb, "wb_frac": wbf,
        "pmax99": float(np.percentile(rgb.max(axis=2), 99)),       # the brightest CHANNEL: sea and sky clip in green or blue before luma gets high
        "skin_frac": float(skin.mean()), "skin_luma": float(np.median(yy[skin])) if skin.sum() > 50 else None,
        "p0.5": float(p[0]), "p1": float(p[1]), "p5": float(p[2]), "p25": float(p[3]), "median": float(p[4]),
        "p75": float(p[5]), "p95": float(p[6]), "p99": float(p[7]), "p99.5": float(p[8]),
        "mean": float(y.mean()),
        "zebra95": float((y >= ZEBRA_HI).mean()), "clip": float((y >= ZEBRA_CLIP).mean()),
        "crush": float((y <= CRUSH).mean()),
        "chroma_mean": float(np.sqrt(cb ** 2 + cr ** 2).mean()),
        "cb_mean": float(cb.mean()), "cr_mean": float(cr.mean()),
        "rgb_mean": [float(rgb[..., c].mean()) for c in range(3)],
    }


def agg(stats_list, key):
    v = np.array([s[key] for s in stats_list])
    return {"mean": float(v.mean()), "min": float(v.min()), "max": float(v.max())}


def hint_score(stats_list):
    """Lower is saner. Only used to rank candidate LUTs when the profile is unknown."""
    s = 0.0
    for st in stats_list:
        s += 4 * st["clip"] + 2 * st["zebra95"] + 2 * st["crush"]
        s += 0.8 * max(0.0, 0.18 - st["median"]) + 0.8 * max(0.0, st["median"] - 0.65)
        s += 1.5 * max(0.0, st["chroma_mean"] - 0.16)
    return s / max(1, len(stats_list))


def lin(x):
    return np.power(np.clip(x, 1e-6, 1.0), 2.4)


def propose(graded_stats):
    """Exposure is anchored on skin when the frame has some (a beach or a snow field would fool a median);
    otherwise on the median. Inside the band nothing is proposed."""
    skin = [s["skin_luma"] for s in graded_stats if s["skin_luma"] is not None and s["skin_frac"] >= 0.01]
    if len(skin) >= max(2, len(graded_stats) // 3):
        anchor, kind, (lo, hi), centre = float(np.median(skin)), "skin", CFG["skin_band"], CFG["skin_target"]
    else:
        anchor, kind, (lo, hi), centre = float(np.mean([s["median"] for s in graded_stats])), "median", CFG["median_band"], CFG["median_target"]
    if lo <= anchor <= hi:
        stops, why = 0.0, "%s at %.0f IRE, inside the %.0f-%.0f band: no exposure change" % (kind, anchor * 100, lo * 100, hi * 100)
    else:
        stops = math.log2(lin(centre) / lin(anchor))
        why = "%s at %.0f IRE, outside the %.0f-%.0f band: aim at %.0f IRE" % (kind, anchor * 100, lo * 100, hi * 100, centre * 100)
    worst = max(s["pmax99"] for s in graded_stats)          # worst frame, brightest channel: the top 1 % must stay under the highlight ceiling
    room = math.log2(CFG["highlight_ceiling"] / max(worst, 1e-3)) * GAMMA_APPLY
    if stops > room:
        stops = min(stops, room)
        why += "; held back to protect the highlights (in the worst frame the brightest 1 %% of a colour channel reaches %.0f IRE)" % (worst * 100)
    stops = max(-MAX_STOPS, min(MAX_STOPS, stops))
    cb = float(np.mean([s["cb_mean"] for s in graded_stats]))
    cr = float(np.mean([s["cr_mean"] for s in graded_stats]))
    mag = math.hypot(cb, cr)
    tend = "neutral"
    if mag > 0.02:
        warm = cr > 0 and cb < 0
        cool = cb > 0 and cr < 0
        tend = "warm" if warm else "cool" if cool else "tinted (%s%s)" % ("red/magenta " if cr > 0 else "green ", "blue" if cb > 0 else "yellow")
    wbs = [x for x in graded_stats if x.get("wb") and x["wb_frac"] >= CFG["wb_min_frac"]]
    wb_gains, wb_why = None, "no near-neutral objects in enough frames (a scene of sea, skin and sand has none): judge the white by eye"
    if len(wbs) >= max(2, len(graded_stats) // 3):
        gr = float(np.median([x["wb"][0] for x in wbs]))
        gb = float(np.median([x["wb"][1] for x in wbs]))
        spread = max(float(np.std([x["wb"][0] for x in wbs])), float(np.std([x["wb"][1] for x in wbs])))
        dev = max(abs(gr - 1), abs(gb - 1))
        if spread > 0.05:
            wb_why = "the near-neutral objects disagree between frames (spread %.3f): the light changes, no single correction fits" % spread
        elif dev < 0.02:
            wb_why = "near-neutral objects are already neutral (off by %.1f %%)" % (dev * 100)
        else:
            lim = CFG["max_wb_gain"]
            wb_gains = [round(min(1 + lim, max(1 - lim, gr)), 4), round(min(1 + lim, max(1 - lim, gb)), 4)]
            wb_why = "near-neutral objects (%.1f %% of the picture) lean off by %.1f %%; gains red x%.3f, blue x%.3f. A warm sunset or a blue shade is not a cast: apply only if you agree" % (
                100 * float(np.median([x["wb_frac"] for x in wbs])), dev * 100, wb_gains[0], wb_gains[1])
    return {"wb_gains": wb_gains, "wb_gains_why": wb_why, "exposure_stops": round(stops, 2), "exposure_anchor": kind, "exposure_anchor_ire": round(anchor * 100, 1), "band": [lo, hi], "target": centre, "exposure_why": why,
            "wb_tendency": tend, "wb_offset": round(mag, 3),
            "wb_note": "Estimated from the average colour: a scene full of sea, sky or sand leans that way on purpose. "
                       "Judge it by eye and on the vectorscope, never apply it blindly."}


# ---------------------------------------------------------------- scopes (numpy + PIL)
def zebra_image(rgb):
    img = to_u8(rgb).copy()
    y = luma(rgb)
    h, w = y.shape
    yy, xx = np.mgrid[0:h, 0:w]
    stripe = ((xx + yy) // 7) % 2 == 0
    m95 = (y >= ZEBRA_HI) & (y < ZEBRA_CLIP) & stripe
    mclip = (y >= ZEBRA_CLIP) & stripe
    mcr = (y <= CRUSH) & stripe
    img[m95] = (255, 190, 0)
    img[mclip] = (255, 40, 40)
    img[mcr] = (60, 120, 255)
    return img


def waveform_parade(rgb, w=480, h=256):
    img = np.zeros((h, w, 3), np.uint8)
    H, Wd, _ = rgb.shape
    third = w // 3
    cols = np.minimum((np.arange(Wd) * third // Wd), third - 1)
    for c in range(3):
        acc = np.zeros((h, third), np.float32)
        rows = np.clip(((1 - rgb[..., c]) * (h - 1)).astype(np.int32), 0, h - 1)
        for x in range(0, Wd):
            np.add.at(acc[:, cols[x]], rows[:, x], 1.0)
        acc = np.clip(acc / (acc.max() * 0.25 + 1e-6), 0, 1) ** 0.6
        for k in range(3):
            img[:, c * third:(c + 1) * third, k] = (acc * (255 if k == c else 40)).astype(np.uint8)
    d = Image.fromarray(img)
    dr = ImageDraw.Draw(d)
    for ire in (0, 20, 40, 60, 80, 95, 100):
        yv = int((1 - ire / 100) * (h - 1))
        dr.line([(0, yv), (w, yv)], fill=(255, 190, 0) if ire in (95, 100) else (70, 70, 70), width=1)
        dr.text((2, max(0, yv - 10)), str(ire), fill=(180, 180, 180))
    return d


def vectorscope(rgb, size=256):
    y = luma(rgb)
    cb = ((rgb[..., 2] - y) / 1.8556).ravel()
    cr = ((rgb[..., 0] - y) / 1.5748).ravel()
    sc = (size / 2 - 6) / 0.5
    xs = np.clip((size / 2 + cb * sc).astype(np.int32), 0, size - 1)
    ys = np.clip((size / 2 - cr * sc).astype(np.int32), 0, size - 1)
    acc = np.zeros((size, size), np.float32)
    np.add.at(acc, (ys, xs), 1.0)
    acc = np.clip(acc / (np.percentile(acc[acc > 0], 99) + 1e-6), 0, 1) ** 0.5 if (acc > 0).any() else acc
    img = np.zeros((size, size, 3), np.uint8)
    img[..., 0] = img[..., 1] = img[..., 2] = (acc * 230).astype(np.uint8)
    d = Image.fromarray(img)
    dr = ImageDraw.Draw(d)
    c = size // 2
    dr.ellipse([c - 100, c - 100, c + 100, c + 100], outline=(70, 70, 70))
    dr.ellipse([c - 50, c - 50, c + 50, c + 50], outline=(55, 55, 55))
    dr.line([(c, 0), (c, size)], fill=(55, 55, 55))
    dr.line([(0, c), (size, c)], fill=(55, 55, 55))
    # skin-tone line (about 123 degrees from the +Cb axis, towards R/Y), a guide, not a rule
    ang = math.radians(123)
    dr.line([(c, c), (c + math.cos(ang) * 110, c - math.sin(ang) * 110)], fill=(210, 150, 90), width=1)
    dr.text((4, 4), "vectorscope  (skin line)", fill=(180, 180, 180))
    return d


def histogram_img(rgb, w=480, h=160):
    img = Image.new("RGB", (w, h), (12, 12, 12))
    dr = ImageDraw.Draw(img)
    ycc = luma(rgb)
    for data, col in ((ycc, (230, 230, 230)), (rgb[..., 0], (230, 60, 60)), (rgb[..., 1], (60, 200, 60)), (rgb[..., 2], (70, 110, 240))):
        hist, _ = np.histogram(data, bins=w, range=(0, 1))
        hist = np.log1p(hist.astype(np.float32))
        hist = hist / (hist.max() + 1e-6)
        pts = [(i, h - 1 - int(hist[i] * (h - 14))) for i in range(w)]
        dr.line(pts, fill=col, width=1)
    for ire, col in ((CRUSH, (60, 120, 255)), (ZEBRA_HI, (255, 190, 0))):
        x = int(ire * (w - 1))
        dr.line([(x, 0), (x, h)], fill=col, width=1)
    dr.text((4, 2), "histogram (log scale)  white=luma  zebra 95 amber, crush blue", fill=(180, 180, 180))
    return img


def monitor(log_rgb, graded_rgb, label, t):
    H, Wd, _ = log_rgb.shape
    tw = 480
    th = int(tw * H / Wd)
    a = Image.fromarray(to_u8(log_rgb)).resize((tw, th))
    b = Image.fromarray(zebra_image(graded_rgb)).resize((tw, th))
    wf = waveform_parade(graded_rgb)
    vs = vectorscope(graded_rgb)
    hg = histogram_img(graded_rgb)
    sheet = Image.new("RGB", (tw * 2 + 8 + 256, th + 8 + 256 + 8 + 20), (20, 20, 20))
    sheet.paste(a, (0, 20))
    sheet.paste(b, (tw + 4, 20))
    sheet.paste(vs, (tw * 2 + 8, 20))
    sheet.paste(wf, (0, th + 28))
    sheet.paste(hg, (tw + 4, th + 28))
    dr = ImageDraw.Draw(sheet)
    dr.text((4, 4), "t=%.1fs  LOG as shot (left)  |  %s + zebra (centre)" % (t, label), fill=(220, 220, 220))
    return sheet


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--profile", default="auto", choices=["auto"] + list(PROFILES))
    ap.add_argument("--samples", type=int, default=12)
    args = ap.parse_args()
    if not os.path.exists(args.video):
        print("no video at", args.video)
        return 1
    os.makedirs(args.out, exist_ok=True)
    try:
        meta = probe(args.video)
    except Exception as e:  # noqa
        print("cannot read the file:", e)
        return 1

    w = W_STATS
    h = int(round(w * meta["h"] / meta["w"] / 2) * 2)
    n = max(3, args.samples)
    times = [meta["duration"] * (0.03 + 0.94 * i / (n - 1)) for i in range(n)]
    frames, used_t = [], []
    for t in times:
        f = grab(args.video, t, w, h)
        if f is not None:
            frames.append(f)
            used_t.append(t)
    if not frames:
        print("no frames could be decoded")
        return 1

    # which profile(s)?
    if args.profile != "auto":
        cands, why, how = [args.profile], "given with --profile", "given"
    else:
        cands, why = read_profile_from_metadata(meta)
        how = "metadata" if len(cands) == 1 else "metadata-ambiguous" if cands else "none"
        if not cands:
            cands = list(PROFILES)
    luts = {k: load_cube(os.path.join(LUTS, PROFILES[k][1])) for k in cands}
    results = {}
    for k in cands:
        graded = [apply_lut(f, luts[k]) for f in frames]
        results[k] = {"graded": graded, "stats": [frame_stats(g) for g in graded]}
        results[k]["score"] = hint_score(results[k]["stats"])
    ranking = sorted(cands, key=lambda k: results[k]["score"])
    chosen = ranking[0]
    certain = how in ("given", "metadata") and len(cands) == 1
    margin = (results[ranking[1]]["score"] - results[chosen]["score"]) if len(ranking) > 1 else None
    if not certain:
        how = "hint" if how in ("none", "metadata-ambiguous") else how

    log_stats = [frame_stats(f) for f in frames]
    g_stats = results[chosen]["stats"]
    prop = propose(g_stats)

    # scopes
    sheets = []
    for i, (f, t) in enumerate(zip(frames, used_t)):
        m = monitor(f, results[chosen]["graded"][i], PROFILES[chosen][0], t)
        m.save(os.path.join(args.out, "scopes-%02d.png" % (i + 1)))
        sheets.append(m)
    cols = 2
    rows = (len(sheets) + cols - 1) // cols
    sw, sh_ = sheets[0].size
    big = Image.new("RGB", (sw * cols, sh_ * rows), (20, 20, 20))
    for i, m in enumerate(sheets):
        big.paste(m, ((i % cols) * sw, (i // cols) * sh_))
    big.save(os.path.join(args.out, "scopes-sheet.png"))

    spread = max(s["median"] for s in g_stats) - min(s["median"] for s in g_stats)
    # A true log picture is flat and pale: its LUT must add a lot of contrast and colour. If it adds almost none,
    # the clip was probably not shot in log. Thresholds are a first guess, to be calibrated on real log clips.
    lspan = np.mean([s["p99"] - s["p1"] for s in log_stats])
    gspan = np.mean([s["p99"] - s["p1"] for s in g_stats])
    contrast_gain = float(gspan / max(lspan, 1e-6))
    chroma_gain = float(np.mean([s["chroma_mean"] for s in g_stats]) / max(np.mean([s["chroma_mean"] for s in log_stats]), 1e-6))
    # Calibration on real clips (23/10/2026): D-Log x1.76 contrast / x2.11 colour, D-Log2 x2.08 / x3.53, D-Log M (a full-range arena) x1.13 / x1.70.
    # D-Log M is the mildest curve, so the "not log" flag needs BOTH gains low.
    if certain and "names the camera" in why:       # profile guessed from the camera name only: the picture must agree
        if chroma_gain >= 1.25:
            why += "; the picture agrees (the LUT adds colour x%.2f)" % chroma_gain
        else:
            certain = False
            why += "; but the LUT adds almost no colour (x%.2f), so it may not be log" % chroma_gain
    flags = []
    if contrast_gain < 1.25 and chroma_gain < 1.25:
        flags.append("the LUT adds almost no contrast (x%.2f) or colour (x%.2f): this clip may NOT be log (a standard profile, or already graded). "
                     "A log LUT on it gives a wrong picture: check how it was shot before grading" % (contrast_gain, chroma_gain))
    if agg(g_stats, "zebra95")["mean"] > 0.05:
        flags.append("%.0f %% of the graded picture is at 95 IRE or above (zebra): too bright, either over-exposed or the wrong LUT" % (100 * agg(g_stats, "zebra95")["mean"]))
    if agg(g_stats, "clip")["mean"] > 0.01:
        flags.append("highlights clipped on %.1f %% of the picture on average: the log signal is already burnt there, no grade brings it back" % (100 * agg(g_stats, "clip")["mean"]))
    if agg(g_stats, "crush")["mean"] > 0.05:
        flags.append("%.1f %% of the picture sits at or under %.0f IRE after the grade: crushed shadows, lifting them will show noise" % (100 * agg(g_stats, "crush")["mean"], CRUSH * 100))
    if spread > 0.15:
        flags.append("exposure moves a lot inside the clip (median from %.0f to %.0f IRE): one gain cannot fit all of it, grade it in parts" % (100 * min(s["median"] for s in g_stats), 100 * max(s["median"] for s in g_stats)))
    if meta["range"] not in ("tv", "pc"):
        flags.append("the file does not say if it is limited or full range: the black level may be off")

    report = {
        "video": args.video, "meta": {k: v for k, v in meta.items() if k != "tags"}, "tags": meta["tags"],
        "profile": {"chosen": chosen, "label": PROFILES[chosen][0], "lut": PROFILES[chosen][1], "certain": certain,
                    "how": how, "why": why, "scores": {k: round(results[k]["score"], 4) for k in ranking},
                    "margin": None if margin is None else round(margin, 4)},
        "log": {"median": agg(log_stats, "median"), "p1": agg(log_stats, "p1"), "p99.5": agg(log_stats, "p99.5")},
        "graded": {k: agg(g_stats, k) for k in ("median", "p1", "p5", "p95", "p99.5", "zebra95", "clip", "crush", "chroma_mean")},
        "median_spread": round(spread, 3), "contrast_gain": round(contrast_gain, 2), "chroma_gain": round(chroma_gain, 2), "flags": flags, "proposal": prop,
        "samples": [{"t": round(t, 2), "log": ls, "graded": gs} for t, ls, gs in zip(used_t, log_stats, g_stats)],
    }
    with open(os.path.join(args.out, "report.json"), "w") as fh:
        json.dump(report, fh, indent=1)

    g = report["graded"]
    L = []
    L.append("# Grade scan: %s\n" % os.path.basename(args.video))
    L.append("%dx%d, %s, %s, range %s, %.1f s, %d frames measured.\n" % (meta["w"], meta["h"], meta["codec"], meta["pix_fmt"], meta["range"], meta["duration"], len(frames)))
    L.append("## Profile\n")
    if certain:
        L.append("**%s** (%s). LUT: `%s`.\n" % (PROFILES[chosen][0], why, PROFILES[chosen][1]))
    else:
        L.append("**NOT CERTAIN.** %s.\n" % why)
        L.append("Every candidate LUT was tried and ranked by how sane the result is (lower is better):\n")
        for k in ranking:
            L.append("- %s: %.3f%s" % (PROFILES[k][0], results[k]["score"], "  <- best guess" if k == chosen else ""))
        L.append("\nThis ranking is a HINT. Tell me the profile (or look at `scopes-sheet.png`) before any grade is applied. The sheet below uses the best guess.\n")
    L.append("## Measures (graded Rec.709 signal, IRE = %)\n")
    L.append("| | average | lowest sample | highest sample |\n|---|---|---|---|")
    for key, lab in (("median", "median luma"), ("p1", "1st percentile (shadows)"), ("p99.5", "99.5th percentile (highlights)")):
        a = g[key]
        L.append("| %s | %.0f | %.0f | %.0f |" % (lab, a["mean"] * 100, a["min"] * 100, a["max"] * 100))
    for key, lab in (("zebra95", "zebra, 95 IRE and above"), ("clip", "zebra, clipped (99.5 and above)"), ("crush", "crushed (2 IRE and under)")):
        a = g[key]
        L.append("| %s | %.1f %% | %.1f %% | %.1f %% |" % (lab, a["mean"] * 100, a["min"] * 100, a["max"] * 100))
    L.append("")
    L.append("Log as shot: median at %.0f %% of the code range, highlights (99.5th) at %.0f %%.\n" % (report["log"]["median"]["mean"] * 100, report["log"]["p99.5"]["mean"] * 100))
    L.append("## Flags\n")
    L.extend(["- " + x for x in flags] or ["- nothing wrong found"])
    L.append("\n## Proposal (nothing is applied until you approve)\n")
    L.append("- **Exposure:** %+.2f stops on the graded signal. %s." % (prop["exposure_stops"], prop["exposure_why"]))
    L.append("- **White balance:** %s (offset %.3f). %s" % (prop["wb_tendency"], prop["wb_offset"], prop["wb_note"]))
    L.append("- **White balance, measured on near-neutral objects:** %s\n" % prop["wb_gains_why"])
    L.append("## How to read the sheet\n")
    L.append("`scopes-sheet.png`: for each sample, the LOG picture as shot (left), the graded picture with zebra (centre: amber = 95 IRE and above, "
             "red stripes = clipped, blue stripes = crushed), the vectorscope (right, the orange line is the skin-tone direction), the RGB parade waveform "
             "(below left) and the histogram (below centre). Single frames: `scopes-NN.png`. Numbers per frame: `report.json`.")
    with open(os.path.join(args.out, "REPORT.md"), "w", encoding="utf8") as fh:
        fh.write("\n".join(L) + "\n")
    print("\n".join(L))
    return 0


if __name__ == "__main__":
    sys.exit(main())
