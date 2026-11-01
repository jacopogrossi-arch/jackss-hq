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


def wrap(cid, t_in, t_out, css, inner, bg=True, track=3, fade_in=0.3, fade_out=0.3):
    """The host: a full-frame card with the wash + grid behind it (bg=True) and a fade in/out of the whole plate.
    Returns (html, js_prefix, js_suffix): put the format's own tweens between prefix and suffix."""
    bgd = '<div class="k-wash" id="%s-bg"></div>' % cid if bg else ""
    html = ('<style>%s</style>\n<div class="card-host clip" id="host-%s" data-card-id="%s" data-unanchored="1" data-start="%.3f" data-duration="%.3f" data-track-index="%d"'
            ' style="left:0;top:0;width:1920px;height:1080px;visibility:hidden;opacity:1;">\n<div id="%s-root" style="position:absolute;inset:0">%s\n%s</div></div>\n'
            % (css, cid, cid, t_in, t_out - t_in, track, cid, bgd, inner))
    pre = ["tl.set('#%s-root', { opacity:0 }, 0);" % cid,
           "tl.fromTo('#%s-root', { opacity:0 }, { opacity:1, duration:%.3f, ease:'power2.out', immediateRender:false }, %.3f);" % (cid, fade_in, t_in)]
    if bg:   # one living thing under every plate (taste.md: no dead frame): the grid drifts 5 % over the plate's whole life
        pre.append("tl.fromTo('#%s-bg', { scale:1 }, { scale:1.05, duration:%.3f, ease:'none', immediateRender:false }, %.3f);" % (cid, t_out - t_in, t_in))
    post = ["tl.fromTo('#%s-root', { opacity:1 }, { opacity:0, duration:%.3f, ease:'power2.in', immediateRender:false }, %.3f);" % (cid, fade_out, t_out - fade_out)]
    return html, pre, post


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
