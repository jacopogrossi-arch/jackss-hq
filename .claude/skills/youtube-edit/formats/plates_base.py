"""plates_base.py: what the plate formats share (tracker, counter, versus, diagram, uiplane).

A "motion plate" is a full-frame scene (see references/formats.md, Explainers). These five formats were designed on 01/11/2026 from the
teardown of Joseph's video (`personale/youtube/inspo-motion-plates-joseph.md`): every plate has one job, and each element lands ON the word
that names it. They use our own tokens (--k-*, see studio.py) so the preset decides colour, fonts and grid; the defaults of studio.css
(grid_a 0) leave older storyboards untouched.

Contract (same as dotgrid.py / scaletta.py): each format returns {"html": ..., "js": ...} for compose.py's "raw_html"/"raw_js".
All motion is seek-safe: every tween is a fromTo with explicit values and immediateRender:false, hidden start states come from tl.set.

Face PiP (formats.md): the square PiP sits at PIP = (left 1552, top 712, 320 x 320). Nothing of a plate may enter it, plus a 40 px margin:
`safe_right()` / `safe_bottom()` give the limits plates lay out against, and `check_pip()` asserts a box stays clear.
"""
import html as _h

esc = lambda s: _h.escape(str(s), quote=True)

PIP = (1552, 712, 320, 320)
MARGIN = 40
EASE = "power3.out"


def safe_right():
    """x limit for anything below the PiP's top edge: a plate element lower than PIP top keeps its right edge left of this."""
    return PIP[0] - MARGIN


def safe_bottom():
    """y limit for anything to the right of the PiP's left edge."""
    return PIP[1] - MARGIN


def check_pip(x, y, w, h, what=""):
    """Raise if the box (left, top, width, height) overlaps the PiP plus its margin."""
    L, T, W, H = PIP
    if x < L + W + MARGIN and x + w > L - MARGIN and y < T + H + MARGIN and y + h > T - MARGIN:
        raise ValueError("%s box (%d,%d,%d,%d) enters the face PiP corner (left %d, top %d)" % (what or "plate", x, y, w, h, L - MARGIN, T - MARGIN))


CAM_ORIGIN = (1500, 700)   # the camera scales about a point beside the face PiP corner: every plate element moves AWAY from the PiP, never under it
CAM_DRIFT = (1.03, -22, -8)  # a plate's slow push-in: scale, x, y over its whole life (~0.2-0.4 %/s; Joseph's plates: median 0.4 %/s)
GAP = 2.3                    # longest stretch without a camera event (Joseph: a motion burst every ~2 s, never a still run above ~0.3 s at p90)


def plan_kicks(events, t_in, t_out):
    """Camera kicks: a strong one (+1.6 %) on every event time (events closer than 1 s share one), a soft one (+0.8 %) wherever more than GAP s would pass
    with nothing moving. Returns [(t, amplitude)] sorted."""
    ev = sorted(e for e in events if t_in + 0.3 <= e <= t_out - 0.7)
    strong = []
    for e in ev:
        if not strong or e - strong[-1][0] >= 1.0:
            strong.append((e, 0.016))
    out, prev = [], t_in + 0.3
    for t, a in strong + [(t_out - 0.7, 0)]:
        while t - prev > GAP:
            prev += 1.9
            out.append((prev, 0.008))
        if a:
            out.append((t, a)); prev = t
    out = sorted(out)
    keep = []   # a soft filler never crowds a neighbour: at least 1 s from the kick before and the one after (else the two tweens overlap)
    for i, (t, a) in enumerate(out):
        nxt = out[i + 1][0] if i + 1 < len(out) else t_out
        if a < 0.016 and (nxt - t < 1.0 or (keep and t - keep[-1][0] < 1.0)):
            continue
        keep.append((t, a))
    return keep


def wrap(cid, t_in, t_out, css, inner, bg=True, track=3, fade_in=0.3, fade_out=0.3, kicks=(), sound=True, audio=(), track_audio=20):
    """The host: a full-frame card with the wash + grid behind it (bg=True), a fade in/out of the whole plate, a CAMERA (slow push-in + kicks on the events,
    see plan_kicks) and the plate's sound (a soft swish on the way in and out when sound=True; `audio` adds format-specific <audio> tags).
    Returns (html, js_prefix, js_suffix): put the format's own tweens between prefix and suffix."""
    ox, oy = CAM_ORIGIN
    css = css + "\n  .pl-cam, .pl-kick { position:absolute; inset:0; transform-origin:%dpx %dpx; }" % (ox, oy)
    bgd = '<div class="k-wash" id="%s-bg"></div>' % cid if bg else ""
    snd = ""
    if sound:   # sfx/swish.mp3 and sfx/swish-short.mp3 come from write_plate_sounds(public)
        snd += '<audio id="sfx-%s-in" src="sfx/swish.mp3" data-start="%.3f" data-duration="1.9" data-track-index="%d" data-volume="0.25"></audio>\n' % (cid, max(t_in - 0.3, 0), track_audio)
        snd += '<audio id="sfx-%s-out" src="sfx/swish-short.mp3" data-start="%.3f" data-duration="0.9" data-track-index="%d" data-volume="0.18"></audio>\n' % (cid, max(t_out - 0.75, 0), track_audio + 1)
    for k, tag in enumerate(audio):
        snd += tag.replace("@TRACK@", str(track_audio + 2 + k)) + "\n"
    html = ('<style>%s</style>\n<div class="card-host clip" id="host-%s" data-card-id="%s" data-unanchored="1" data-start="%.3f" data-duration="%.3f" data-track-index="%d"'
            ' style="left:0;top:0;width:1920px;height:1080px;visibility:hidden;opacity:1;">\n<div id="%s-root" style="position:absolute;inset:0">%s\n'
            '<div class="pl-cam" id="%s-cam"><div class="pl-kick" id="%s-kick">%s</div></div></div></div>\n%s'
            % (css, cid, cid, t_in, t_out - t_in, track, cid, bgd, cid, cid, inner, snd))
    pre = ["tl.set('#%s-root', { opacity:0 }, 0);" % cid,
           "tl.fromTo('#%s-root', { opacity:0 }, { opacity:1, duration:%.3f, ease:'power2.out', immediateRender:false }, %.3f);" % (cid, fade_in, t_in)]
    if bg:   # parallax: the grid drifts slower than the content (depth) and never stops
        pre.append("tl.fromTo('#%s-bg', { scale:1 }, { scale:1.06, duration:%.3f, ease:'none', immediateRender:false }, %.3f);" % (cid, t_out - t_in, t_in))
    sc, cx, cy = CAM_DRIFT
    pre.append("tl.fromTo('#%s-cam', { scale:1, x:0, y:0 }, { scale:%.3f, x:%d, y:%d, duration:%.3f, ease:'none', immediateRender:false }, %.3f);" % (cid, sc, cx, cy, t_out - t_in, t_in))
    ks = plan_kicks(list(kicks), t_in, t_out)
    pre.append("tl.set('#%s-kick', { scale:1 }, 0);" % cid)
    for i, (t, a) in enumerate(ks):
        nxt = ks[i + 1][0] if i + 1 < len(ks) else t_out
        down = max(min(1.3, nxt - 0.05 - (t + 0.25) - 0.02), 0.3)
        pre.append("tl.fromTo('#%s-kick', { scale:1 }, { scale:%.4f, duration:0.3, ease:'power2.out', immediateRender:false }, %.3f);" % (cid, 1 + a, t - 0.05))
        pre.append("tl.fromTo('#%s-kick', { scale:%.4f }, { scale:1, duration:%.3f, ease:'sine.inOut', immediateRender:false }, %.3f);" % (cid, 1 + a, down, t + 0.25))
    post = ["tl.fromTo('#%s-root', { opacity:1 }, { opacity:0, duration:%.3f, ease:'power2.in', immediateRender:false }, %.3f);" % (cid, fade_out, t_out - fade_out)]
    return html, pre, post


def write_plate_sounds(public, sk=None):
    """sfx/swish.mp3 (whoosh-ethereal 1.9 s), sfx/swish-short.mp3 (0.9 s for the exit), sfx/typing.mp3 and sfx/click.mp3 in the project's public folder."""
    import os, subprocess
    sk = sk or os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    d = os.path.join(public, "sfx"); os.makedirs(d, exist_ok=True)
    src = os.path.join(sk, "assets/sfx/mixclap/whoosh-ethereal.mp3")
    run = lambda *a: subprocess.run(["ffmpeg", "-y", "-v", "error", *a], check=True)
    run("-i", src, "-t", "1.9", "-af", "afade=t=in:d=0.08,afade=t=out:st=1.4:d=0.5", os.path.join(d, "swish.mp3"))
    run("-i", src, "-t", "0.9", "-af", "afade=t=in:d=0.05,afade=t=out:st=0.5:d=0.4", os.path.join(d, "swish-short.mp3"))
    run("-i", os.path.join(sk, "assets/sfx/core/typing.mp3"), "-t", "2.2", "-af", "afade=t=out:st=1.9:d=0.3", os.path.join(d, "typing.mp3"))
    run("-i", os.path.join(sk, "assets/sfx/core/click.mp3"), "-t", "0.34", "-af", "afade=t=out:st=0.2:d=0.14", os.path.join(d, "click.mp3"))


def fromto(sel, a, b, t, d, ease=EASE):
    """One seek-safe tween as a JS line. a and b are JS object literals as strings."""
    return "tl.fromTo('%s', %s, Object.assign({}, %s, { duration:%.3f, ease:'%s', immediateRender:false }), %.3f);" % (sel, a, b, d, ease, t)


def at_attrs(t, anchor):
    """beat-check.py proves each timed element against the words: data-at is its entry time, data-anchor the spoken phrase."""
    return ' data-at="%.3f" data-anchor="%s"' % (t, esc(anchor)) if anchor else ' data-at="%.3f" data-unanchored="1"' % t


def keyword(text):
    """'a *word*' -> the starred word in the italic serif key colour (one per line at most)."""
    parts = str(text).split("*")
    out = []
    for i, p in enumerate(parts):
        out.append('<i class="pl-key">%s</i>' % esc(p) if i % 2 else esc(p))
    return "".join(out)


BASE_CSS = """
  .pl-t { position:absolute; font-family:var(--k-font); font-weight:800; color:var(--k-text); letter-spacing:-.02em; white-space:nowrap; opacity:0; }
  .pl-t .pl-key, .pl-sub .pl-key { font-family:var(--k-serif); font-style:italic; font-weight:500; color:var(--k-accent); letter-spacing:0; }
  .pl-sub { position:absolute; font-family:var(--k-font); font-weight:600; color:var(--k-mute); white-space:nowrap; opacity:0; }
  .pl-card { position:absolute; border-radius:26px; background:rgba(244,239,230,.95); color:#0b0907; box-shadow:0 30px 60px rgba(0,0,0,.5); opacity:0; }
  .pl-ck { position:absolute; width:36px; height:36px; border-radius:50%; background:var(--k-accent2); color:#06140d; opacity:0; }
  .pl-ck svg { position:absolute; inset:0; width:36px; height:36px; }
"""
