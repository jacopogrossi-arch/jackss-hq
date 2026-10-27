#!/usr/bin/env python3
"""grade-film.py: the film pipeline of the vacanze-grading preset (27/10/2026), shared by grade-apply, grade-match and grade-ref.

Why it exists: the first pipeline applied the exposure as a gain on the finished Rec.709 picture and the look's contrast as an
S curve on display values. A gain there cannot bring dim highlights up to white without lifting the skin, and it clips
whatever it pushes past 100 %. Colourists work the other way round, and so does this module:

  1. the DJI LUT output is taken back to linear light (code ** 2.4);
  2. exposure and white balance are gains in linear light (one stop = x2, as on the camera);
  3. contrast is a slope in stops around middle grey (0.18), on luminance only, so hues do not shift;
  4. a highlight stretch, measured once per clip, brings that clip's brightest highlights (99.9th percentile) to about 95 %;
     it starts one stop above middle grey ("stretch_from"), so skin and mid-tones stay where the exposure put them:
     white clouds read white, faces do not get paler;
  5. a shoulder in stops rolls everything above it towards white, never past it (no flat clipped patches), and a soft toe
     sets the blacks;
  6. colours that would leave the gamut are pulled towards their own luminance, and the brightest highlights lose a little
     colour, as on film;
  7. back to code values; then the look's colour work (saturation, hue windows, learned colour map, WOW), then the split
     tone (warm highlights, teal shadows) with the water and sky protected by a hue mask, colour density and hue shifts.

Steps 1-7 are a pure colour function of the LUT output, given the clip's measured white, so they are baked into ONE 3D LUT and
ffmpeg applies them in a single pass. The finish (halation, grain, vignette, graduated sky) depends on where a pixel is, so it
is an ffmpeg filter graph after the LUT, built small (quarter-size glow, enlarged grain) and scaled by the frame width:
the same graph runs on a 960 px preview and on the 4K render.

All numbers live in the look ("film" and "finish" keys in presets/vacanze-grading/preset.json); defaults below."""
import importlib.util, os, shutil, subprocess, tempfile

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("grade_looks", os.path.join(HERE, "grade-looks.py"))
gl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gl)
gs = gl.gs

GAMMA = 2.4
GREY = 0.18
WHITE_STOPS = float(np.log2(1.0 / GREY))                 # display white, 2.47 stops above middle grey
FILM = {"contrast": 1.12, "shoulder": 1.5, "white_target": 0.95, "stretch_from": 1.0, "stretch_max": 2.5, "stretch_min": 0.85,
        "black": 0.004, "hl_desat": 0.2, "warm": None, "sat_hue": [], "density": 0.0, "hue": []}
FINISH = {"halation": 0.0, "halation_threshold": 0.8, "halation_radius": 0.006, "halation_color": [1.0, 0.42, 0.16],
          "grain": 0.0, "grain_size": 2.0, "vignette": 0.0, "sky_grad": 0.0}
LOOK_LIGHT_KEYS = ("gamma", "crush", "lift", "gain", "temp", "contrast", "shadows", "highlights")   # the film tone replaces these


def film_params(look):
    f = dict(FILM)
    f.update((look or {}).get("film", {}))
    return f


def finish_params(look):
    f = dict(FINISH)
    f.update((look or {}).get("finish", {}))
    return f


def is_film(look):
    return bool(look) and "film" in look


def to_lin(x):
    return np.clip(x, 0.0, 1.0) ** GAMMA


def from_lin(y):
    return np.clip(y, 0.0, 1.0) ** (1.0 / GAMMA)


def lin_luma(lin):
    return lin[..., 0] * 0.2126 + lin[..., 1] * 0.7152 + lin[..., 2] * 0.0722


def shoulder(d, start, top=WHITE_STOPS):
    """Stops above grey in, stops above grey out: unchanged below `start`, then an exponential roll that approaches `top`
    (display white) and never reaches it. Smooth: same value and slope at `start`."""
    span = max(top - start, 1e-3)
    over = np.maximum(d - start, 0.0)
    return np.where(d > start, start + span * (1.0 - np.exp(-over / span)), d)


def stretch_for(white_lin, f):
    """The highlight factor for a clip: the stretch k (on stops above stretch_from) that lands the clip's measured white at
    white_target after contrast and shoulder. Kept in [stretch_min, stretch_max]: past that it is a different picture."""
    a = f["stretch_from"]
    if white_lin is None or float(np.log2(max(white_lin, 1e-6) / GREY)) * f["contrast"] <= a + 0.05:
        return 1.0
    hw = float(np.log2(white_lin / GREY)) * f["contrast"]
    target = float(np.log2(f["white_target"] ** GAMMA / GREY))
    lo, hi = f["stretch_min"], f["stretch_max"]
    for _ in range(40):                                      # bisection: the shoulder has no closed-form inverse worth keeping
        mid = (lo + hi) / 2
        if float(shoulder(np.array(a + (hw - a) * mid), f["shoulder"])) < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def tone(rgb709, look, stops=0.0, wb=None, white_lin=None):
    """Steps 1-6: LUT output (Rec.709 code values) -> toned code values. Exposure in stops of linear light."""
    f = film_params(look)
    lin = to_lin(rgb709) * (2.0 ** stops)
    if wb:                                                   # the scan measures gains on code values; in linear light the same correction is gain ** 2.4
        lin = lin * np.array([wb[0] ** GAMMA, 1.0, wb[1] ** GAMMA], np.float32)
    y = np.maximum(lin_luma(lin), 1e-7)
    d = np.log2(y / GREY) * f["contrast"]
    k = stretch_for(None if white_lin is None else white_lin * (2.0 ** stops), f)
    a = f["stretch_from"]
    d = np.where(d > a, a + (d - a) * k, d)
    d = shoulder(d, f["shoulder"])
    y2 = GREY * (2.0 ** d)
    b = f["black"]
    y2 = y2 * y2 / (y2 + b) if b > 0 else y2                 # soft toe: about y - b on mid-tones, smooth down to 0
    out = lin * (y2 / y)[..., None]
    yo = lin_luma(out)[..., None]
    mx = out.max(axis=-1, keepdims=True)
    fit = np.where(mx > 1.0, (1.0 - yo) / np.maximum(mx - yo, 1e-6), 1.0)   # out of gamut: towards its own luminance, same brightness
    out = yo + (out - yo) * np.clip(fit, 0.0, 1.0)
    if f["hl_desat"]:
        t = np.clip((yo - 0.55) / 0.45, 0.0, 1.0)
        out = yo + (out - yo) * (1.0 - f["hl_desat"] * t * t)
    return from_lin(out)


def hue_shift(x, shifts):
    """Rotate the hue inside soft windows: [(centre_deg, width_deg, shift_deg), ...]; value and saturation unchanged."""
    h, s = gl.hue_sat(x)
    rot = np.zeros_like(h)
    for c, w, deg in shifts:
        rot += gl.window(h, c / 360.0, w / 360.0) * deg / 360.0
    rot *= np.clip((s - 0.05) / 0.1, 0.0, 1.0)
    mx = x.max(axis=-1)
    h2 = (h + rot) % 1.0
    i = np.floor(h2 * 6.0)
    fr = h2 * 6.0 - i
    p, q, t = mx * (1 - s), mx * (1 - s * fr), mx * (1 - s * (1 - fr))
    i = i.astype(int) % 6
    r = np.choose(i, [mx, q, p, p, t, mx])
    g = np.choose(i, [t, mx, mx, q, p, p])
    b = np.choose(i, [p, p, t, mx, mx, q])
    return np.stack([r, g, b], axis=-1)


def colour(x, look):
    """Step 7: the look's colour work on the toned picture, then split tone, density and hue shifts."""
    f = film_params(look)
    p = {k: v for k, v in (look or {}).items() if k not in LOOK_LIGHT_KEYS + ("film", "finish")}
    if p.get("wow"):
        p["wow"] = {k: v for k, v in p["wow"].items() if k not in LOOK_LIGHT_KEYS}
    x = gl.apply_look(x, p)
    if f["warm"]:                                            # warm highlights / teal shadows; water and sky keep their colour
        keep = 1.0 - gl.sea_weight(x)[..., None]
        yy = np.clip(gs.luma(x), 0, 1)[..., None]
        hl, sh = np.array(f["warm"][0], np.float32), np.array(f["warm"][1], np.float32)
        x = np.clip(x + keep * ((yy ** 2) * hl + ((1 - yy) ** 2) * sh), 0, 1)
    if f["sat_hue"]:                                         # saturation per hue, like a colourist's HSL panel: [(centre_deg, width_deg, gain), ...]
        h, s = gl.hue_sat(x)
        gain = np.ones_like(h)
        for c, w, g in f["sat_hue"]:
            gain += gl.window(h, c / 360.0, w / 360.0) * (g - 1.0)
        gain = 1.0 + (gain - 1.0) * np.clip((s - 0.04) / 0.08, 0, 1)     # leave the near-greys alone
        yy = gs.luma(x)[..., None]
        x = np.clip(yy + (x - yy) * gain[..., None], 0, 1)
    if f["density"]:                                         # saturated colours a little darker: rich, not neon
        c = x.max(axis=-1, keepdims=True) - x.min(axis=-1, keepdims=True)
        x = x * (1.0 - f["density"] * c)
    if f["hue"]:
        x = hue_shift(np.clip(x, 0, 1), f["hue"])
    return np.clip(x, 0.0, 1.0)


def apply(rgb709, look, stops=0.0, wb=None, white_lin=None):
    """The whole colour function of a film look: LUT output -> graded code values (no finish)."""
    return colour(tone(rgb709, look, stops, wb, white_lin), look)


def measure_white(lut_frames, pct=99.9):
    """A clip's white: the 99.9th percentile of linear luminance over the sampled frames (LUT applied, no exposure)."""
    ys = np.concatenate([lin_luma(to_lin(f)).ravel() for f in lut_frames])
    return float(np.percentile(ys, pct))


def bake(look, path, stops=0.0, wb=None, white_lin=None, n=65, pre=None):
    """The colour function as a .cube (red fastest). With `pre` (a loaded DJI LUT) the table goes straight from the LOG file:
    DJI LUT and grade in ONE lookup, half the work of two 4K lookups in a row."""
    lin = np.linspace(0, 1, n, dtype=np.float32)
    r = np.tile(lin, n * n)
    g = np.tile(np.repeat(lin, n), n)
    b = np.repeat(lin, n * n)
    grid = np.stack([r, g, b], axis=-1)[:, None, :]
    if pre is not None:
        grid = gs.apply_lut(grid, pre)
    out = apply(grid, look, stops, wb, white_lin)[:, 0, :]
    with open(path, "w") as fh:
        for line in ("LUT_3D_SIZE %d" % n, "DOMAIN_MIN 0 0 0", "DOMAIN_MAX 1 1 1"):
            fh.write(line + "\n")
        np.savetxt(fh, out, fmt="%.6f")


def has_finish(look):
    fin = finish_params(look)
    return any(fin[k] for k in ("halation", "grain", "vignette", "sky_grad"))


def finish_graph(w, h, look, inp="in", out="out", fps=25):
    """The finish as an ffmpeg filter_complex fragment, from [inp] (gbrp10le) to [out] (gbrp10le). Sizes scale with the width,
    so a 960 px preview and a 3840 px render look alike. Built cheap: the glow is blurred at a quarter of the size, the grain
    is drawn at 1/grain_size of the size and enlarged (film grain is bigger than a 4K pixel), the vignette is one filter."""
    fin = finish_params(look)
    parts, cur = [], inp
    if fin["halation"]:
        qw, qh = max(16, (w // 4) // 2 * 2), max(16, (h // 4) // 2 * 2)
        r, g, b = fin["halation_color"]
        parts.append("[%s]split=2[hb][hs]" % cur)
        parts.append("[hs]scale=%d:%d:flags=area,curves=all='0/0 %.3f/0 1/1',gblur=sigma=%.2f,"
                     "colorchannelmixer=rr=%.3f:rg=0:rb=0:gr=%.3f:gg=0:gb=0:br=%.3f:bg=0:bb=0,"
                     "scale=%d:%d:flags=bicubic,format=gbrp10le[hg]"
                     % (qw, qh, fin["halation_threshold"], max(0.5, fin["halation_radius"] * w / 4), r, g, b, w, h))
        parts.append("[hb][hg]blend=all_mode=screen:all_opacity=%.3f[h1]" % fin["halation"])
        cur = "h1"
    if fin["sky_grad"]:                                      # a graduated filter: the top of the frame darker, the bright parts (sky) most
        k = fin["sky_grad"]
        ramp = "1023*max(0\\,1-Y/(H*0.45))"                  # 1 at the top edge, 0 from 45 % of the height down
        parts.append("[%s]split=3[sa][sb][sc]" % cur)
        parts.append("[sb]curves=all='0/0 0.5/%.3f 1/%.3f'[sd]" % (0.5 * (1 - k * 0.4), 1 - k))
        # the ramp is drawn on a 2x64 copy of each frame (cheap) and enlarged: it stays in step with the video and ends with it
        # (a per-pixel geq on 4K cost 48 s per second of video; a looped still never ends, maskedmerge has no 'shortest')
        parts.append("[sc]scale=2:64,geq=r='%s':g='%s':b='%s',scale=%d:%d:flags=bilinear[sm]" % (ramp, ramp, ramp, w, h))
        parts.append("[sa][sd][sm]maskedmerge[sg]")
        cur = "sg"
    if fin["vignette"]:
        parts.append("[%s]vignette=angle=%.3f:mode=forward:dither=0[vg]" % (cur, fin["vignette"]))   # dither=1 (default) tripled its cost on 4K
        cur = "vg"
    if fin["grain"]:
        gw, gh = max(16, int(w / fin["grain_size"]) // 2 * 2), max(16, int(h / fin["grain_size"]) // 2 * 2)
        parts.append("color=c=0x808080:s=%dx%d:r=%s,format=gray10le,noise=alls=100:allf=t+u,scale=%d:%d:flags=bicubic,"
                     "format=gbrp10le[gn]" % (gw, gh, fps, w, h))
        parts.append("[%s][gn]blend=all_mode=softlight:all_opacity=%.3f:shortest=1[gr]" % (cur, fin["grain"]))
        cur = "gr"
    if not parts:
        return "[%s]null[%s]" % (inp, out)
    parts.append("[%s]null[%s]" % (cur, out))
    return ";".join(parts)


def finish_image(rgb, look, fps=25):
    """Run the finish graph on one graded frame (float RGB 0-1) through ffmpeg: the preview shows exactly what the render does."""
    if not has_finish(look):
        return rgb
    h, w, _ = rgb.shape
    tmp = tempfile.mkdtemp(prefix="grade-film-")
    try:
        Image.fromarray(gs.to_u8(rgb)).save(os.path.join(tmp, "in.png"))
        fc = "[0:v]format=gbrp10le[in];" + finish_graph(w, h, look, fps=fps) + ";[out]format=rgb24[o]"
        p = subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", "in.png", "-filter_complex", fc, "-map", "[o]", "-frames:v", "1", "out.png"],
                           cwd=tmp, capture_output=True, text=True)
        if p.returncode != 0:
            raise RuntimeError(p.stderr[-600:])
        return np.asarray(Image.open(os.path.join(tmp, "out.png")).convert("RGB")).astype(np.float32) / 255.0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
