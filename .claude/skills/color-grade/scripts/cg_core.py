"""Core color grading engine.

Pipeline (mirrors how a colorist works):
  1. balance   - neutralize the source's own color cast
  2. tone      - match the reference's black level, contrast and highlight roll-off (luma curve)
  3. color     - match the color of shadows, mids and highlights separately (zone MKL transfer in Lab)
  4. palette   - hue-specific matching (sliced optimal transport on a color sample set)
  5. recipe    - hand-built look operations (hue curves, split tone, mono, bleach, technicolor, ...)
  6. masks     - skin protection, sky secondary, selective color
  7. finish    - haze, halation, bloom, vignette, grain

Steps 1-5 are per-pixel, so they can also be exported as a .cube LUT (used for video).
Steps 6-7 are spatial and only exist in the full render.
Needs only numpy and opencv-python-headless.
"""
import math
import numpy as np
import cv2

# ---------------------------------------------------------------- io / color

def load(path, max_side=None):
    im = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if im is None:
        raise SystemExit(f"cannot read image: {path}")
    if max_side and max(im.shape[:2]) > max_side:
        s = max_side / max(im.shape[:2])
        im = cv2.resize(im, None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
    return cv2.cvtColor(im, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0

def save(path, rgb, quality=95):
    out = (np.clip(rgb, 0, 1) * 255 + 0.5).astype(np.uint8)
    cv2.imwrite(str(path), cv2.cvtColor(out, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, quality])

def to_lab(rgb):
    return cv2.cvtColor(np.clip(rgb, 0, 1).astype(np.float32), cv2.COLOR_RGB2Lab)

def to_rgb(lab):
    return np.clip(cv2.cvtColor(lab.astype(np.float32), cv2.COLOR_Lab2RGB), 0, 1)

def lab_px(rgb_px_):
    """Nx3 rgb -> Nx3 lab"""
    return to_lab(rgb_px_.reshape(-1, 1, 3)).reshape(-1, 3)

def rgb_px(lab_px_):
    return to_rgb(lab_px_.reshape(-1, 1, 3)).reshape(-1, 3)

def smoothstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)

def luma(rgb):
    return rgb[..., 0] * 0.2126 + rgb[..., 1] * 0.7152 + rgb[..., 2] * 0.0722

# ---------------------------------------------------------------- analysis

PCTS = [0.5, 2, 5, 10, 25, 50, 75, 90, 95, 98, 99.5]

def trim_bars(rgb):
    """Remove letterbox / pillarbox bars."""
    L = luma(rgb)
    rows = np.where((L > 0.025).mean(1) > 0.05)[0]
    cols = np.where((L > 0.025).mean(0) > 0.05)[0]
    if len(rows) < 10 or len(cols) < 10:
        return rgb
    return rgb[rows[0]:rows[-1] + 1, cols[0]:cols[-1] + 1]

def zone_weights(L):
    s = np.clip((48 - L) / 33, 0, 1)
    h = np.clip((L - 52) / 33, 0, 1)
    m = np.clip(1 - s - h, 0, 1)
    return s, m, h

def image_lab_sample(images, per_image=40000, seed=0):
    rng = np.random.default_rng(seed)
    labs = []
    for im in images:
        im = trim_bars(im)
        s = 360 / max(im.shape[:2])
        if s < 1:
            im = cv2.resize(im, None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
        lab = to_lab(im).reshape(-1, 3)
        k = min(len(lab), per_image)
        labs.append(lab[rng.choice(len(lab), k, replace=False)])
    per = min(len(x) for x in labs)
    return np.concatenate([x[rng.choice(len(x), per, replace=False)] for x in labs])

def analyze(images, n_samples=1500, seed=0):
    """Look statistics from one or more images (rgb float arrays). Each image counts equally."""
    return stats_from_lab(image_lab_sample(images, seed=seed), n_samples, np.random.default_rng(seed))

def stats_from_lab(lab, n_samples=1500, rng=None):
    rng = rng or np.random.default_rng(0)
    L, ab = lab[:, 0], lab[:, 1:]
    zones = []
    for w in zone_weights(L):
        ws = w.sum()
        if ws < 50:
            zones.append(None)
            continue
        mu = (ab * w[:, None]).sum(0) / ws
        d = ab - mu
        cov = (d * w[:, None]).T @ d / ws
        zones.append({"w": float(ws / len(L)), "mean": np.round(mu, 3).tolist(), "cov": np.round(cov, 3).tolist()})
    for i in range(3):
        if zones[i] is None:
            nb = [z for z in (zones[1], zones[0], zones[2]) if z is not None][0]
            zones[i] = dict(nb, w=0.0)
    C = np.hypot(ab[:, 0], ab[:, 1])
    idx = rng.choice(len(lab), min(n_samples, len(lab)), replace=False)
    return {
        "lum_pct": np.round(np.percentile(L, PCTS), 3).tolist(),
        "zones": zones,
        "chroma": [round(float(C.mean()), 3), round(float(np.percentile(C, 90)), 3)],
        "samples": np.round(lab[idx], 1).tolist(),
    }

def merge_stats(stats_list, weights=None):
    weights = weights or [1.0] * len(stats_list)
    tw = sum(weights)
    out = {"lum_pct": (sum(np.array(s["lum_pct"]) * w for s, w in zip(stats_list, weights)) / tw).tolist(),
           "chroma": (sum(np.array(s["chroma"]) * w for s, w in zip(stats_list, weights)) / tw).tolist(),
           "zones": [], "samples": []}
    for z in range(3):
        mus = [np.array(s["zones"][z]["mean"]) for s in stats_list]
        covs = [np.array(s["zones"][z]["cov"]) for s in stats_list]
        mu = sum(m * w for m, w in zip(mus, weights)) / tw
        cov = sum((c + np.outer(m - mu, m - mu)) * w for c, m, w in zip(covs, mus, weights)) / tw
        out["zones"].append({"w": float(np.mean([s["zones"][z]["w"] for s in stats_list])),
                             "mean": mu.tolist(), "cov": cov.tolist()})
    for s, w in zip(stats_list, weights):
        k = int(len(s["samples"]) * w / max(weights))
        out["samples"] += s["samples"][:k]
    return out

# ---------------------------------------------------------------- building blocks

def _sqrtm(c):
    d, u = np.linalg.eigh(c)
    d = np.clip(d, 1e-6, None)
    return u @ np.diag(np.sqrt(d)) @ u.T, u @ np.diag(1 / np.sqrt(d)) @ u.T

def mkl(cs, cr, reg=6.0, clip=(0.12, 2.2)):
    """Monge-Kantorovich linear map taking covariance cs to cr (2x2)."""
    cs = np.array(cs) + np.eye(2) * reg
    cr = np.array(cr) + np.eye(2) * reg
    hs, ihs = _sqrtm(cs)
    hc, _ = _sqrtm(hs @ cr @ hs)
    T = ihs @ hc @ ihs
    u, s, vt = np.linalg.svd(T)
    return u @ np.diag(np.clip(s, *clip)) @ vt

def tone_table(src_pct, ref_pct, strength, max_slope=3.0, min_slope=0.25):
    """1001-entry L->L table moving the source luma percentiles toward the reference."""
    sp = np.array(src_pct, float)
    tp = sp + strength * (np.array(ref_pct, float) - sp)
    xs = np.concatenate([[0], sp, [100]])
    end_lo = strength * tp[0] * 0.5 if tp[0] > sp[0] else 0.0
    end_hi = 100 - strength * max(0.0, (sp[-1] - tp[-1])) * 0.5
    ys = np.concatenate([[end_lo], tp, [end_hi]])
    xs = np.maximum.accumulate(xs + np.arange(len(xs)) * 1e-3)
    grid = np.linspace(0, 100, 1001)
    t = np.interp(grid, xs, ys)
    k = cv2.getGaussianKernel(61, 12).ravel()
    t = np.convolve(np.pad(t, 30, mode="edge"), k, mode="valid")
    d = np.clip(np.diff(t), min_slope * 0.1, max_slope * 0.1)
    t = np.concatenate([[t[0]], t[0] + np.cumsum(d)])
    return np.clip(t, 0, 100)

def apply_table(L, table):
    return np.interp(L, np.linspace(0, 100, len(table)), table)

class SlicedOT:
    """Iterative distribution transfer (Pitie et al.) fitted on samples, replayable on any points."""
    def __init__(self, src, ref, iters=14, scale=(0.6, 1.0, 1.0), seed=3):
        rng = np.random.default_rng(seed)
        self.scale = np.array(scale)
        s = src * self.scale
        r = ref * self.scale
        self.steps = []
        q = np.linspace(0, 100, 129)
        for _ in range(iters):
            R, _ = np.linalg.qr(rng.normal(size=(3, 3)))
            ps, pr = s @ R, r @ R
            maps = []
            for k in range(3):
                xs = np.percentile(ps[:, k], q)
                ys = np.percentile(pr[:, k], q)
                xs = np.maximum.accumulate(xs + np.arange(len(xs)) * 1e-6)
                maps.append((xs, ys))
                ps[:, k] = self._map(ps[:, k], xs, ys)
            s = ps @ R.T
            self.steps.append((R, maps))

    @staticmethod
    def _map(v, xs, ys):
        out = np.interp(v, xs, ys)
        lo, hi = v < xs[0], v > xs[-1]
        out[lo] = ys[0] + (v[lo] - xs[0])
        out[hi] = ys[-1] + (v[hi] - xs[-1])
        return out

    def __call__(self, pts):
        p = pts * self.scale
        for R, maps in self.steps:
            pr = p @ R
            for k, (xs, ys) in enumerate(maps):
                pr[:, k] = self._map(pr[:, k], xs, ys)
            p = pr @ R.T
        return p / self.scale

# ---------------------------------------------------------------- default parameters

DEFAULTS = {
    "balance": 0.6,       # remove source color cast (0-1)
    "tone": 0.65,         # luma curve match strength
    "color": 0.85,        # zone color match strength
    "palette": 0.35,      # hue-specific match strength
    "palette_L": 0.0,     # let the palette step move luminance too
    "strength": 1.0,      # global mix of the whole per-pixel grade
    "skin": 0.55,         # skin protection (0 = off)
    "skin_follow": 0.35,  # how much of the look skin still takes when protected
    "sat": 1.0,           # saturation multiplier after matching
    "skin_lum": 0.0,      # keep faces bright in dark looks (0-1)
    # guard rails: keep grades tasteful on any source
    "match_exposure": 0.5,  # pull the graded mid brightness back toward the source's (0 = off)
    "sat_limit": 1.6,       # max mean saturation as a multiple of the source's (0 = off)
    "chroma_knee": 50.0,    # soft roll-off for very saturated colors, Lab chroma (0 = off)
    "max_cast": 20.0,       # max overall color shift in Lab a*/b* units (0 = off)
}

# ---------------------------------------------------------------- the grade

class Grade:
    def __init__(self, src, look_stats, params=None, ops=None):
        """src: an rgb image, or an Nx3 Lab sample (e.g. pooled from video frames)."""
        self.p = dict(DEFAULTS, **(params or {}))
        self.ops = ops or []
        self.look = look_stats
        rng = np.random.default_rng(1)
        lab = src if src.ndim == 2 else to_lab(src).reshape(-1, 3)
        sample = lab[rng.choice(len(lab), min(len(lab), 60000), replace=False)].astype(np.float64)

        # 1 balance: median ab of near-neutral pixels
        abs_ = sample[:, 1:]
        C = np.hypot(abs_[:, 0], abs_[:, 1])
        neutral = (C < 18) & (sample[:, 0] > 15) & (sample[:, 0] < 92)
        self.cast = np.median(abs_[neutral], 0) if neutral.sum() > 500 else np.zeros(2)
        self.cast = np.clip(self.cast, -12, 12)

        s = self._balance(sample.copy())
        # 2 tone
        self.table = tone_table(np.percentile(s[:, 0], PCTS), self.look["lum_pct"], self.p["tone"])
        s[:, 0] = apply_table(s[:, 0], self.table)
        # 3 zone color
        src_stats = stats_from_lab(s, 10)
        self.zone_maps = []
        for z in range(3):
            zs, zr = src_stats["zones"][z], self.look["zones"][z]
            self.zone_maps.append((np.array(zs["mean"]), np.array(zr["mean"]), mkl(zs["cov"], zr["cov"])))
        s = self._zone(s)
        # 4 palette
        self.ot = None
        if self.p["palette"] > 0 and len(self.look["samples"]) > 100:
            ref = np.array(self.look["samples"], float)
            self.ot = SlicedOT(s[rng.choice(len(s), min(len(s), 12000), replace=False)], ref)
        # 5 guard rails (exposure match, saturation ceiling, cast limit)
        self._fit_guard(sample[:10000])

    def _balance(self, lab):
        lab[:, 1:] -= self.cast * self.p["balance"]
        return lab

    def _zone(self, lab):
        L, ab = lab[:, 0], lab[:, 1:]
        out = np.zeros_like(ab)
        for w, (ms, mr, T) in zip(zone_weights(L), self.zone_maps):
            out += w[:, None] * (mr + (ab - ms) @ T.T)
        lab[:, 1:] = ab + self.p["color"] * (out - ab)
        return lab

    def _palette(self, lab):
        if self.ot is None:
            return lab
        m = self.ot(lab.astype(np.float64))
        a = self.p["palette"]
        lab[:, 1:] += a * (m[:, 1:] - lab[:, 1:])
        lab[:, 0] += a * self.p["palette_L"] * (m[:, 0] - lab[:, 0])
        return lab

    def _core(self, rgb):
        lab = self._balance(lab_px(rgb).astype(np.float64))
        lab[:, 0] = apply_table(lab[:, 0], self.table)
        lab = self._zone(lab)
        lab = self._palette(lab)
        if self.p["sat"] != 1.0:
            lab[:, 1:] *= self.p["sat"]
        out = rgb_px(lab.astype(np.float32))
        for op in self.ops:
            fn = PIXEL_OPS.get(op["op"])
            if fn:
                out = fn(out, op)
        return out

    def _fit_guard(self, src_lab):
        """Measure the raw grade on the source sample and derive the guard-rail corrections."""
        self.g_cast, self.g_gamma, self.g_cscale = np.zeros(2), 1.0, 1.0
        out = lab_px(self._core(rgb_px(src_lab.astype(np.float32)))).astype(np.float64)
        mc = self.p["max_cast"]
        d = out[:, 1:].mean(0) - src_lab[:, 1:].mean(0)
        if mc > 0 and np.hypot(*d) > mc:
            self.g_cast = d * (1 - mc / np.hypot(*d))
        k = self.p["match_exposure"]
        mo, ms = np.median(out[:, 0]), np.median(src_lab[:, 0])
        if k > 0 and 3 < mo < 97:
            target = np.clip(mo + k * (ms - mo), 3, 97)
            self.g_gamma = float(np.clip(np.log(target / 100) / np.log(mo / 100), 0.6, 1.6))
        out = self._guard(out, scale=False)
        lim = self.p["sat_limit"]
        if lim > 0:
            co = np.hypot(out[:, 1], out[:, 2]).mean()
            cs = max(np.hypot(src_lab[:, 1], src_lab[:, 2]).mean(), 8.0)
            if co > lim * cs:
                self.g_cscale = float(max(0.72, lim * cs / co))

    def _guard(self, lab, scale=True):
        lab = lab.copy()
        lab[:, 1:] -= self.g_cast
        if self.g_gamma != 1.0:
            lab[:, 0] = 100 * np.clip(lab[:, 0] / 100, 0, 1) ** self.g_gamma
        K = self.p["chroma_knee"]
        if K > 0:
            C = np.hypot(lab[:, 1], lab[:, 2])
            R = K * 0.6
            Cn = np.where(C > K, K + R * np.tanh((C - K) / R), C)
            lab[:, 1:] *= (Cn / np.maximum(C, 1e-6))[:, None]
        if scale and self.g_cscale != 1.0:
            lab[:, 1:] *= self.g_cscale
        return lab

    def pixel(self, rgb):
        """Per-pixel part of the grade, rgb Nx3 -> rgb Nx3. Exportable as a LUT."""
        out = rgb_px(self._guard(lab_px(self._core(rgb)).astype(np.float64)).astype(np.float32))
        st = self.p["strength"]
        return rgb + st * (out - rgb) if st != 1.0 else out

    def lut(self, size=65):
        """Per-pixel grade sampled on a size^3 grid, indexed [b, g, r]."""
        g = np.linspace(0, 1, size, dtype=np.float32)
        b, gg, r = np.meshgrid(g, g, g, indexing="ij")
        pts = np.stack([r.ravel(), gg.ravel(), b.ravel()], 1)
        return np.clip(self.pixel(pts), 0, 1).reshape(size, size, size, 3).astype(np.float32)

    def render(self, rgb, seed=7, skin=None, lut=None):
        """Full grade. Pass lut=self.lut() to speed up repeated renders (video frames)."""
        h, w = rgb.shape[:2]
        if lut is not None:
            graded = apply_lut(lut, rgb)
        else:
            graded = self.pixel(rgb.reshape(-1, 3)).reshape(h, w, 3).astype(np.float32)
        ctx = {"src": rgb, "seed": seed}
        mono = any(o["op"] == "mono" for o in self.ops)
        if self.p["skin"] > 0 or mono:
            ctx["skin"] = skin if skin is not None else skin_mask(rgb)
        if self.p["skin"] > 0 and not mono:
            graded = protect_skin(rgb, graded, ctx["skin"], self.p["skin"], self.p["skin_follow"], self.p["skin_lum"])
        spatial = sorted([o for o in self.ops if o["op"] in SPATIAL_OPS],
                         key=lambda o: SPATIAL_ORDER.index(o["op"]))
        for op in spatial:
            graded = SPATIAL_OPS[op["op"]](graded, op, ctx)
        return np.clip(graded, 0, 1)

    def cube(self, path, size=33, title="color-grade"):
        g = np.linspace(0, 1, size, dtype=np.float32)
        b, gg, r = np.meshgrid(g, g, g, indexing="ij")  # .cube order: red changes fastest
        pts = np.stack([r.ravel(), gg.ravel(), b.ravel()], 1)
        out = np.clip(self.pixel(pts), 0, 1)
        with open(path, "w") as f:
            f.write(f'TITLE "{title}"\nLUT_3D_SIZE {size}\nDOMAIN_MIN 0 0 0\nDOMAIN_MAX 1 1 1\n')
            for v in out:
                f.write(f"{v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n")

def apply_lut(lut, rgb):
    """Trilinear lookup of an [b, g, r] LUT on an HxWx3 rgb image."""
    n = lut.shape[0] - 1
    x = np.clip(rgb, 0, 1) * n
    i0 = np.minimum(x.astype(np.int32), n - 1)
    f = x - i0
    r0, g0, b0 = i0[..., 0], i0[..., 1], i0[..., 2]
    fr, fg, fb = f[..., 0:1], f[..., 1:2], f[..., 2:3]
    out = 0
    for db, wb in ((0, 1 - fb), (1, fb)):
        for dg, wg in ((0, 1 - fg), (1, fg)):
            for dr, wr in ((0, 1 - fr), (1, fr)):
                out = out + lut[b0 + db, g0 + dg, r0 + dr] * (wb * wg * wr)
    return out.astype(np.float32)

# ---------------------------------------------------------------- masks

_FACE = None

def faces(rgb):
    global _FACE
    if _FACE is None:
        try:
            _FACE = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        except AttributeError:  # OpenCV 5 dropped Haar cascades: fall back to the generic skin model
            _FACE = False
    if _FACE is False:
        return []
    g = cv2.cvtColor((np.clip(rgb, 0, 1) * 255).astype(np.uint8), cv2.COLOR_RGB2GRAY)
    s = min(1.0, 900 / max(g.shape))
    small = cv2.resize(g, None, fx=s, fy=s) if s < 1 else g
    f = _FACE.detectMultiScale(small, 1.1, 6, minSize=(24, 24))
    return [(int(x / s), int(y / s), int(w / s), int(h / s)) for x, y, w, h in f]

def skin_mask(rgb):
    """Soft skin mask: color model learned from detected faces, generic skin model as fallback."""
    lab = to_lab(rgb)
    h, w = rgb.shape[:2]
    fs = faces(rgb)
    pix = []
    for x, y, fw, fh in fs:
        c = lab[y + fh // 4: y + fh * 3 // 4, x + fw // 4: x + fw * 3 // 4].reshape(-1, 3)
        if len(c):
            c = c[(c[:, 0] > np.percentile(c[:, 0], 25)) & (c[:, 0] < np.percentile(c[:, 0], 97))]
            pix.append(c)
    if pix and sum(len(p) for p in pix) > 80:
        P = np.concatenate(pix)
        mu = P[:, 1:].mean(0)
        cov = np.cov(P[:, 1:].T) + np.eye(2) * 6
        Lr = (np.percentile(P[:, 0], 2) - 12, np.percentile(P[:, 0], 99) + 8)
    else:
        mu, cov, Lr = np.array([16.0, 20.0]), np.array([[40.0, 10], [10, 50]]), (25, 92)
    d = lab[..., 1:] - mu
    m2 = np.einsum("...i,ij,...j->...", d, np.linalg.inv(cov), d)
    m = np.exp(-0.5 * m2 / 2.5) * smoothstep(Lr[0] - 8, Lr[0], lab[..., 0]) * (1 - smoothstep(Lr[1], Lr[1] + 6, lab[..., 0]))
    prior = np.full((h, w), 0.35, np.float32)
    yy, xx = np.ogrid[:h, :w]
    for x, y, fw, fh in fs:
        e = ((xx - x - fw / 2) / (fw * 0.75)) ** 2 + ((yy - y - fh / 2) / (fh * 0.95)) ** 2
        prior = np.maximum(prior, np.clip(1.6 - e, 0, 1))
    m = (m * prior).astype(np.float32)
    k = max(3, int(max(h, w) * 0.006) | 1)
    return cv2.GaussianBlur(m, (k, k), 0)

def protect_skin(src, graded, mask, amount, follow, lum=0.0):
    """Pull skin color back toward the source. lum > 0 also keeps faces readable in dark looks."""
    ls, lg = to_lab(src), to_lab(graded)
    a = (mask * amount * (1 - follow))[..., None]
    lg[..., 1:] = lg[..., 1:] - a * (lg[..., 1:] - ls[..., 1:])
    if lum > 0:
        target = np.minimum(ls[..., 0], lg[..., 0] * 1.8 + 4)
        lg[..., 0] += mask * lum * np.clip(target - lg[..., 0], 0, None)
    return to_rgb(lg)

def sky_mask(rgb):
    lab = to_lab(rgb)
    h, w = rgb.shape[:2]
    L, b = lab[..., 0], lab[..., 2]
    g = cv2.GaussianBlur(L, (0, 0), 3)
    tex = cv2.GaussianBlur(np.abs(L - g), (0, 0), 6)
    cand = ((L > 45) & (b < 18) & (tex < 3.0)).astype(np.uint8)
    cand[int(h * 0.75):] = 0
    n, lbl = cv2.connectedComponents(cand)
    top = set(np.unique(lbl[: max(2, h // 50)]).tolist()) - {0}
    m = np.isin(lbl, list(top)).astype(np.float32)
    return cv2.GaussianBlur(m, (0, 0), max(2, w * 0.01))

# ---------------------------------------------------------------- pixel ops (LUT-safe)

def _lch(rgb):
    lab = lab_px(rgb).astype(np.float64)
    C = np.hypot(lab[:, 1], lab[:, 2])
    H = np.degrees(np.arctan2(lab[:, 2], lab[:, 1])) % 360
    return lab[:, 0], C, H

def _from_lch(L, C, H):
    r = np.radians(H)
    return rgb_px(np.stack([L, C * np.cos(r), C * np.sin(r)], 1).astype(np.float32))

def op_hue_curves(rgb, op):
    """keys: [{hue, width, shift, sat, lum}] - hue vs hue / sat / lum curves, LCh degrees."""
    L, C, H = _lch(rgb)
    Hn, Cn, Ln = H.copy(), C.copy(), L.copy()
    cw = C / (C + 6)
    for k in op["keys"]:
        dh = (H - k["hue"] + 180) % 360 - 180
        wgt = np.exp(-0.5 * (dh / k.get("width", 30)) ** 2) * cw
        Hn += wgt * k.get("shift", 0)
        Cn *= 1 + wgt * (k.get("sat", 1) - 1)
        Ln += wgt * k.get("lum", 0)
    return _from_lch(Ln, Cn, Hn % 360)

def op_split_tone(rgb, op):
    """Push zones toward ab offsets: {shadows:[a,b], mids:[a,b], highlights:[a,b], amount}"""
    lab = lab_px(rgb).astype(np.float64)
    s, m, h = zone_weights(lab[:, 0])
    a = op.get("amount", 1.0)
    for w, key in ((s, "shadows"), (m, "mids"), (h, "highlights")):
        if key in op:
            lab[:, 1:] += a * w[:, None] * np.array(op[key])
    return rgb_px(lab.astype(np.float32))

def op_curve(rgb, op):
    """Luma curve on L: {points: [[in,out],...] in 0-100, amount}"""
    lab = lab_px(rgb).astype(np.float64)
    pts = np.array(op["points"], float)
    new = np.interp(lab[:, 0], pts[:, 0], pts[:, 1])
    lab[:, 0] += op.get("amount", 1.0) * (new - lab[:, 0])
    return rgb_px(lab.astype(np.float32))

def op_saturation(rgb, op):
    """{amount, vibrance}: vibrance boosts low-chroma colors more than saturated ones."""
    lab = lab_px(rgb).astype(np.float64)
    C = np.hypot(lab[:, 1], lab[:, 2])
    f = op.get("amount", 1.0) * (1 + op.get("vibrance", 0) * np.exp(-C / 25))
    lab[:, 1:] *= f[:, None]
    return rgb_px(lab.astype(np.float32))

def op_mono(rgb, op):
    """Black and white with optional kept hue: {keep:[lo,hi], min_chroma, keep_sat, contrast, tint:[a,b]}"""
    L, C, H = _lch(rgb)
    keep = np.zeros_like(L)
    if "keep" in op:
        lo, hi = op["keep"]
        inside = ((H - lo) % 360) <= ((hi - lo) % 360)
        mc = op.get("min_chroma", 30)
        keep = inside * smoothstep(mc - 8, mc + 8, C)
    c = op.get("contrast", 1.0)
    Lm = np.clip((L - 50) * c + 50, 0, 100)
    tint = np.array(op.get("tint", [0, 0]), float)
    ks = op.get("keep_sat", 1.3)
    a = tint[0] + keep * (C * ks * np.cos(np.radians(H)) - tint[0])
    b = tint[1] + keep * (C * ks * np.sin(np.radians(H)) - tint[1])
    Lo = Lm + keep * (L - Lm) * 0.6
    return rgb_px(np.stack([Lo, a, b], 1).astype(np.float32))

def op_bleach(rgb, op):
    """Bleach bypass: luminance overlay + desaturation. {amount}"""
    a = op.get("amount", 0.6)
    y = luma(rgb)[:, None]
    ov = np.where(y < 0.5, 2 * rgb * y, 1 - 2 * (1 - rgb) * (1 - y))
    ov = ov * 0.5 + y * 0.5
    return rgb + a * (ov - rgb)

def op_technicolor(rgb, op):
    """Three-strip dye separation: pushes primaries apart. {amount}"""
    a = op.get("amount", 0.5)
    r, g, b = rgb[:, 0], rgb[:, 1], rgb[:, 2]
    sep = np.stack([r - (g + b) / 2, g - (r + b) / 2, b - (r + g) / 2], 1)
    return np.clip(rgb + a * sep, 0, 1)

def op_day_for_night(rgb, op):
    """{amount, tint:[a,b], keep_lights, light_from}: darken, cool, desaturate; bright sources survive."""
    a = op.get("amount", 0.8)
    lab = lab_px(rgb).astype(np.float64)
    L = lab[:, 0]
    keep = smoothstep(op.get("light_from", 82), 100, L) * op.get("keep_lights", 0.7)
    Ln = L * (1 - a * 0.62) * (1 - keep) + L * keep
    Ln = 100 * (np.clip(Ln, 0, 100) / 100) ** (1 + a * 0.35)
    ab = lab[:, 1:] * (1 - a * 0.45 * (1 - keep))[:, None]
    ab += a * (1 - keep)[:, None] * np.array(op.get("tint", [-6, -14]))
    return rgb_px(np.stack([Ln, ab[:, 0], ab[:, 1]], 1).astype(np.float32))

def op_mix(rgb, op):
    """Channel mixer: {matrix: 3x3, rows = output r,g,b}"""
    return np.clip(rgb @ np.array(op["matrix"], float).T, 0, 1)

def op_gamma(rgb, op):
    """Exposure / gamma on luminance only. {exposure (stops), gamma}"""
    lab = lab_px(rgb).astype(np.float64)
    L = lab[:, 0] / 100 * 2 ** op.get("exposure", 0)
    lab[:, 0] = 100 * np.clip(L, 0, 1) ** op.get("gamma", 1.0)
    return rgb_px(lab.astype(np.float32))

PIXEL_OPS = {"hue_curves": op_hue_curves, "split_tone": op_split_tone, "curve": op_curve,
             "saturation": op_saturation, "mono": op_mono, "bleach": op_bleach,
             "technicolor": op_technicolor, "day_for_night": op_day_for_night, "mix": op_mix,
             "gamma": op_gamma}

# ---------------------------------------------------------------- spatial ops (full render only)

def _blur(img, frac):
    h, w = img.shape[:2]
    return cv2.GaussianBlur(img, (0, 0), max(1.0, max(h, w) * frac))

def sp_mono(rgb, op, ctx):
    """Mono looks with a kept color: skin never counts as the kept color."""
    if "keep" not in op or "skin" not in ctx:
        return rgb
    lab = to_lab(rgb)
    m = np.clip(ctx["skin"] * 1.6, 0, 1)[..., None]
    t = np.array(op.get("tint", [0, 0]), np.float32)
    lab[..., 1:] = lab[..., 1:] * (1 - m) + t * m
    return to_rgb(lab)

def sp_sky(rgb, op, ctx):
    """Secondary on the sky: {ab:[a,b] target, amount, lum}"""
    m = sky_mask(ctx["src"])[..., None]
    lab = to_lab(rgb)
    lab[..., 1:] += m * op.get("amount", 0.6) * (np.array(op["ab"], np.float32) - lab[..., 1:])
    lab[..., 0] += m[..., 0] * op.get("lum", 0)
    return to_rgb(lab)

def sp_haze(rgb, op, ctx):
    """Atmospheric lift: {color:[r,g,b], amount}"""
    c = np.array(op.get("color", [0.8, 0.6, 0.4]), np.float32)
    y = luma(rgb)[..., None]
    return rgb + (c - rgb) * op.get("amount", 0.2) * (1 - y) ** 0.7

def sp_bloom(rgb, op, ctx):
    """Soft diffusion glow (Pro-Mist like). {amount, radius, threshold}"""
    m = smoothstep(op.get("threshold", 0.6), 1.0, luma(rgb))[..., None]
    glow = _blur(rgb * m, op.get("radius", 0.03))
    return 1 - (1 - rgb) * (1 - op.get("amount", 0.3) * glow)

def sp_halation(rgb, op, ctx):
    """Film halation: red-orange glow bleeding from highlights. {amount, radius, color, threshold}"""
    m = smoothstep(op.get("threshold", 0.72), 1.0, luma(rgb))[..., None]
    glow = _blur(m * np.array(op.get("color", [1.0, 0.35, 0.12]), np.float32), op.get("radius", 0.012))
    return 1 - (1 - rgb) * (1 - op.get("amount", 0.35) * glow)

def sp_soften(rgb, op, ctx):
    """Gentle lens softness. {amount, radius}"""
    return rgb + op.get("amount", 0.3) * (_blur(rgb, op.get("radius", 0.0015)) - rgb)

def sp_sharpen(rgb, op, ctx):
    return rgb + op.get("amount", 0.4) * (rgb - _blur(rgb, op.get("radius", 0.0012)))

def sp_vignette(rgb, op, ctx):
    """{amount, size}"""
    h, w = rgb.shape[:2]
    yy, xx = np.mgrid[:h, :w].astype(np.float32)
    r = np.hypot((xx - w / 2) / (w / 2), (yy - h / 2) / (h / 2)) / math.sqrt(2)
    return rgb * (1 - op.get("amount", 0.3) * smoothstep(op.get("size", 0.45), 1.0, r))[..., None]

def sp_grain(rgb, op, ctx):
    """Film grain, strongest in the mids. {amount, size, chroma}"""
    h, w = rgb.shape[:2]
    rng = np.random.default_rng(ctx.get("seed", 7))
    size = op.get("size", 1.0) * max(h, w) / 1500
    n = rng.normal(0, 1, (h, w)).astype(np.float32)
    if size > 0.5:
        n = cv2.GaussianBlur(n, (0, 0), size * 0.6)
        n /= n.std() + 1e-6
    y = luma(rgb)[..., None]
    amp = op.get("amount", 0.03) * (0.35 + 2.6 * y * (1 - y))
    out = rgb + n[..., None] * amp
    if op.get("chroma", 0) > 0:
        cn = cv2.GaussianBlur(rng.normal(0, 1, (h, w, 3)).astype(np.float32), (0, 0), max(size, 0.8))
        out += cn * op["chroma"] * amp
    return out

SPATIAL_OPS = {"mono": sp_mono, "sky": sp_sky, "haze": sp_haze, "bloom": sp_bloom,
               "halation": sp_halation, "soften": sp_soften, "sharpen": sp_sharpen,
               "vignette": sp_vignette, "grain": sp_grain}
SPATIAL_ORDER = ["mono", "sky", "haze", "bloom", "halation", "soften", "sharpen", "vignette", "grain"]
