"""morph.py: the living shape (format 45), ONE shape that changes into the thing being said: a line with a gold spark, a search
pill typed letter by letter, a globe circle, a logo square, a grid of images, a moodboard page. It never cuts: each change is
0.7 s `power3.inOut` and ends 0.1 s before the spoken word. Won the blind A/B of 26/10/2026 against 27b (the 3D card chain) on the
`processo` bench window (`videos/_bench/ab/processo-morph/`, state sheet `STATE-SHEET.md`).

Usage (any build script, or compose.py's "raw_html"/"raw_js"):
    import sys; sys.path.insert(0, "<SK>/formats"); from morph import morph, write_swish
    out = morph(steps=[{"kind": "pill", "label": "Claude in Chrome", "at": 2.6, "anchor": "Chrome",
                        "text": "Claude in Chrome", "logo": "<SK>/assets/logos/claude.svg", "click": 5.6},
                       {"kind": "circle", "label": "Naviga sul web", "at": 7.395, "anchor": "navigare", "icon": "globe"},
                       {"kind": "square", "label": "Pinterest", "at": 9.56, "anchor": "Pinterest", "logo": "pinterest.svg",
                        "logo_color": "#E60023"},
                       {"kind": "grid", "label": "Sceglie le immagini", "at": 11.8, "anchor": "immagini", "images": [...6 jpg...]},
                       {"kind": "page", "label": "Le impagina da solo", "at": 15.28, "anchor": "impaginate", "images": [...same...],
                        "title": "Royal Humour", "check_at": 15.7}],
                t_in=1.3, t_out=16.3, public="<project>/public")
    storyboard["raw_html"] = out["html"]; storyboard["raw_js"] = out["js"]; write_swish("<project>/public", "<SK>")
    # storyboard "duration" = t_out + 0.2 (the shape fades out in 0.2 s after t_out)
Fonts: Inter and Playfair Display Italic are loaded with @font-face from fonts/ (compose.py stages them from assets/fonts).

Steps: 3 to 6 dicts, each {"kind", "label" (up to 3 words), "at" (time the spoken word lands), "anchor" (the word, for the log), ...}.
  pill   760x120 r60   text (typed 0.04 s a letter, max 22 chars, behind a gold spark), logo (svg/png, optional), click (optional:
                       the cursor enters 0.85 s before and presses the button, 0.12 s down)
  circle 360x360 r180  icon "globe" (meridians; set spin=True to turn them, default False = still, as on the bench) or a name of ICONS in compose.py
  square 420x420 r48   logo (path; svg without its own fill: pass logo_color, e.g. "#E60023", and it is drawn inline in that colour)
  grid   1100x520 r28  images (2 to 6), 3 columns, tiles enter 0.06 s apart (a last short row is centred)
  page   960x540 r18   images (the previous grid's tiles fly into the layout, 0.04 s apart, when the list is the same), title
                       (Playfair Italic), check_at (the emerald check badge, the tick is drawn 0.1 s later)
Numbers: the change k runs [at-0.8, at-0.1]; swish (write_swish, vol .25) at the start of every change after the first; label
(gold number + 44 px name) rides 80 px under the shape and shows on the word; camera drift 1.00 -> 1.05 in every state.
Start: the first state is the line with its spark, drawn in 0.5 s BEFORE the first change (at[0]-1.3). If t_in is later than that
there is no room for line + change, so the card starts early at at[0]-1.3 (on the bench: 1.3 s for at=2.6); if t_in is earlier,
the card starts at t_in (the dark wash and the blobs fade in) and the line is still drawn at at[0]-1.3.
Guards: 3 to 6 steps, "at" increasing, at least 1.2 s between two steps (closer: the shape has no time to rest, use the
pipeline, format 27). Seek-safe: every tween is a fromTo with explicit values.
"""
import html as _html, os, re, shutil, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chain3d import ICONS, SK, write_swish  # noqa: E402,F401  (write_swish re-exported: the 27b swish, same file and volume)

MD = 0.7                                   # duration of a change
GAP_MIN = 1.2
DIMS = {"pill": (760, 120, 60), "circle": (360, 360, 180), "square": (420, 420, 48), "grid": (1100, 520, 28), "page": (960, 540, 18)}
S0 = (420, 4, 2)                           # the line
# blobs (gold dx,dy, emerald dx,dy) per state, as tuned on the bench
BX = {"line": (140, -60, -140, 60), "pill": (300, -90, -300, 100), "circle": (200, -150, -200, 150),
      "square": (230, -130, -230, 130), "grid": (520, -170, -520, 170), "page": (460, -190, -460, 190)}
LABEL_TOP0 = 500 + 2 + 80                  # 80 px under the bottom edge of the line
PAGE_LAYOUT = {                            # inner box 954x534: (x, y, w, h) per tile
    2: [(28, 70, 441, 440), (485, 70, 441, 440)],
    3: [(28, 66, 420, 460), (462, 66, 464, 224), (462, 302, 464, 224)],
    4: [(28, 66, 442, 213), (484, 66, 442, 213), (28, 293, 442, 213), (484, 293, 442, 213)],
    5: [(28, 66, 420, 460), (462, 66, 226, 214), (700, 66, 226, 214), (462, 292, 226, 234), (700, 292, 226, 234)],
    6: [(28, 66, 420, 460), (462, 66, 226, 214), (700, 66, 226, 214),
        (462, 292, 146.7, 234), (620.7, 292, 146.7, 234), (779.3, 292, 146.7, 234)],
}

CSS = """
  @font-face { font-family:"Inter"; src:url("fonts/Inter.ttf") format("truetype"); font-weight:100 900; font-display:block; }
  @font-face { font-family:"Playfair Display"; src:url("fonts/PlayfairDisplay-Italic.ttf") format("truetype"); font-style:italic; font-weight:400 900; font-display:block; }
  #mroot { font-family:"Inter","Segoe UI",system-ui,sans-serif; }
  #mroot { position:absolute; inset:0; overflow:hidden; }
  #mwash { position:absolute; inset:0; opacity:0; background:
      radial-gradient(1100px 620px at 50% 118%, rgba(212,175,95,.20), transparent 70%),
      radial-gradient(760px 700px at -4% 42%, rgba(74,165,133,.17), transparent 70%), #0b0907; }
  #cam { position:absolute; inset:0; transform-origin:960px 540px; }
  .blob { position:absolute; opacity:0; width:380px; height:380px; left:770px; top:310px; }
  .blob i { display:block; width:380px; height:380px; border-radius:50%; filter:blur(90px); opacity:.55; }
  #shape { position:absolute; left:960px; top:500px; box-sizing:border-box; border:2px solid transparent; border-radius:2px;
    overflow:hidden; --f:rgba(11,9,7,.72);
    background: linear-gradient(var(--f),var(--f)) padding-box, linear-gradient(120deg,#d4af5f,#f4efe6 45%,#4aa585) border-box;
    backdrop-filter: blur(18px); -webkit-backdrop-filter: blur(18px);
    box-shadow: 0 0 40px rgba(212,175,95,.45), 0 0 90px rgba(74,165,133,.25); }
  .sc { position:absolute; inset:0; opacity:0; display:flex; align-items:center; justify-content:center; }
  .sc.pillsc { justify-content:flex-start; padding:0 24px 0 36px; gap:24px; }
  .sc.pillsc img { width:56px; height:56px; flex:none; }
  .typ { flex:1; font-weight:500; font-size:46px; color:#f4efe6; white-space:pre; position:relative; height:60px; line-height:60px; letter-spacing:-.005em; }
  .ch { display:none; }
  .btn { width:72px; height:72px; border-radius:50%; flex:none; display:flex; align-items:center; justify-content:center;
    background:rgba(244,239,230,.10); border:2px solid #d4af5f; box-shadow:0 0 0 rgba(212,175,95,0); }
  .btn svg { width:34px; height:34px; }
  .spark1, #spark0 { position:absolute; width:14px; height:14px; border-radius:50%; background:#d4af5f; opacity:0;
    box-shadow:0 0 14px 6px rgba(212,175,95,.8), 0 0 36px 14px rgba(212,175,95,.35); }
  #spark0 { left:953px; top:493px; }
  .spark1 { left:0; top:23px; }
  .globe { width:230px; height:230px; overflow:visible; }
  .globe * { fill:none; stroke:#f4efe6; stroke-width:3; }
  .icn { width:160px; height:160px; overflow:visible; }
  .icn path { fill:none; stroke:#f4efe6; stroke-width:1.8; stroke-linecap:round; stroke-linejoin:round; }
  .pin { width:150px; height:150px; }
  .tile { position:absolute; left:0; top:0; border-radius:14px; overflow:hidden; opacity:0; background:#1b140d; }
  .tile img { width:100%; height:100%; object-fit:cover; display:block; }
  .ptitle { position:absolute; left:28px; top:12px; font-family:"Playfair Display",Georgia,serif; font-style:italic; font-weight:500;
    font-size:40px; line-height:48px; color:#15100b; opacity:0; white-space:nowrap; }
  .badge { position:absolute; right:18px; top:8px; width:56px; height:56px; border-radius:50%; background:#4aa585; opacity:0;
    display:flex; align-items:center; justify-content:center; box-shadow:0 0 18px rgba(74,165,133,.55); }
  .badge svg { width:30px; height:30px; }
  #lbl { position:absolute; left:0; width:1920px; top:__LT__px; height:100px; }
  .lab { position:absolute; left:0; right:0; top:0; text-align:center; opacity:0; }
  .ln { font-weight:600; font-size:26px; color:#d4af5f; line-height:30px; }
  .lt { font-weight:600; font-size:44px; color:#f4efe6; line-height:54px; margin-top:4px; white-space:nowrap; }
  .cur { position:absolute; left:0; top:0; width:40px; height:40px; opacity:0; transform-origin:0 0; filter:drop-shadow(0 4px 8px rgba(0,0,0,.6)); }
""".replace("__LT__", str(LABEL_TOP0))


def _asset(path, public):
    """src for an image/logo: copied to <public>/img/ when public is given; the page always refers to img/<name>."""
    name = os.path.basename(path)
    if public:
        os.makedirs(os.path.join(public, "img"), exist_ok=True)
        dst = os.path.join(public, "img", name)
        if os.path.abspath(path) != os.path.abspath(dst):
            shutil.copy(path, dst)
    return "img/" + name


def _inline_path(path):
    txt = open(path, encoding="utf-8").read()
    vb = re.search(r'viewBox="([^"]+)"', txt)
    return re.search(r'<path d="([^"]+)"', txt).group(1), (vb.group(1) if vb else "0 0 24 24")


def morph(steps, t_in, t_out, public=None):
    n = len(steps)
    assert 3 <= n <= 6, "morph: 3 to 6 steps"
    for i, s in enumerate(steps):
        assert s["kind"] in DIMS, "morph: unknown kind %r (pill, circle, square, grid, page)" % s["kind"]
        assert "label" in s and "at" in s, "morph: each step needs label and at"
        if i:
            assert s["at"] > steps[i - 1]["at"], "morph: 'at' must increase (step %d)" % (i + 1)
            assert s["at"] - steps[i - 1]["at"] >= GAP_MIN - 1e-9, (
                "morph: steps %d and %d are %.2f s apart, less than %.1f s: the shape has no time to rest. Use the pipeline (format 27)"
                % (i, i + 1, s["at"] - steps[i - 1]["at"], GAP_MIN))
        if s["kind"] in ("grid", "page"):
            assert 2 <= len(s.get("images", [])) <= 6, "morph: %s needs 2 to 6 images" % s["kind"]
        if s["kind"] == "pill":
            assert len(s.get("text", "")) <= 22, "morph: pill text up to 22 characters"
    END = [s["at"] - 0.1 for s in steps]
    START = [e - MD for e in END]
    L0 = START[0] - 0.5                       # the line is drawn in 0.5 s before the first change
    T_IN = min(t_in, L0)                      # the card itself starts here
    T_OUT = t_out
    DUR = T_OUT + 0.2
    kinds = [s["kind"] for s in steps]
    pin_dim = [S0] + [DIMS[k] for k in kinds]
    bx = [BX["line"]] + [BX[k] for k in kinds]

    # ---------------- html
    parts, tiles_by_step, reuse = [], {}, {}
    for i, s in enumerate(steps):
        k = s["kind"]
        if k == "pill":
            txt = s.get("text", "")
            chars = "".join('<span class="ch" id="ch%d_%d">%s</span>' % (i, j, "&nbsp;" if c == " " else _html.escape(c)) for j, c in enumerate(txt))
            logo = '<img src="%s">' % _asset(s["logo"], public) if s.get("logo") else ""
            parts.append('<div class="sc pillsc" id="sc%d">%s<div class="typ" id="typ%d">%s<i class="spark1" id="spark1_%d"></i></div>'
                         '<div class="btn" id="btn%d"><svg viewBox="0 0 24 24"><path d="M5 12h13M12 5l7 7-7 7" fill="none" stroke="#f4efe6" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg></div></div>'
                         % (i, logo, i, chars, i, i))
        elif k == "circle":
            ic = s.get("icon", "globe")
            if ic == "globe":
                parts.append('<div class="sc" id="sc%d"><svg class="globe" viewBox="0 0 200 200"><circle cx="100" cy="100" r="80"/>'
                             '<ellipse id="mer%d_0" cx="100" cy="100" rx="80" ry="80"/><ellipse id="mer%d_1" cx="100" cy="100" rx="40" ry="80"/><ellipse id="mer%d_2" cx="100" cy="100" rx="40" ry="80"/>'
                             '<line x1="30.7" y1="60" x2="169.3" y2="60"/><line x1="30.7" y1="140" x2="169.3" y2="140"/></svg></div>' % (i, i, i, i))
            else:
                assert ic in ICONS, "morph: icon %r is not in compose.py ICONS" % ic
                parts.append('<div class="sc" id="sc%d"><svg class="icn" viewBox="0 0 64 64"><path d="%s"/></svg></div>' % (i, ICONS[ic]))
        elif k == "square":
            lg = s["logo"]
            if s.get("logo_color") and lg.lower().endswith(".svg"):
                d, vb = _inline_path(lg)
                parts.append('<div class="sc" id="sc%d"><svg class="pin" viewBox="%s"><path fill="%s" style="fill:%s;stroke:none" d="%s"/></svg></div>'
                             % (i, vb, s["logo_color"], s["logo_color"], d))
            else:
                parts.append('<div class="sc" id="sc%d"><img class="pin" src="%s"></div>' % (i, _asset(lg, public)))
        else:   # grid / page
            if k == "page" and i and kinds[i - 1] == "grid" and list(steps[i - 1]["images"]) == list(s["images"]):
                reuse[i] = i - 1
                tiles_by_step[i] = tiles_by_step[i - 1]
            else:
                tiles_by_step[i] = ["tl%d_%d" % (i, j) for j in range(len(s["images"]))]
                for j, im in enumerate(s["images"]):
                    parts.append('<div class="tile" id="tl%d_%d"><img src="%s"></div>' % (i, j, _asset(im, public)))
            if k == "page":
                if s.get("title"):
                    parts.append('<div class="ptitle" id="ptitle%d">%s</div>' % (i, _html.escape(s["title"])))
                if s.get("check_at") is not None:
                    parts.append('<div class="badge" id="badge%d"><svg viewBox="0 0 24 24"><path id="chk%d" d="M5 12.5l4.5 4.5L19 7.5" fill="none" stroke="#f4efe6" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg></div>' % (i, i))
    labels_html = "".join('<div class="lab" id="lab%d"><div class="ln">%02d</div><div class="lt">%s</div></div>' % (i, i + 1, _html.escape(s["label"])) for i, s in enumerate(steps))
    cursors = "".join('<svg class="cur" id="cur%d" viewBox="0 0 26 38"><path d="M1 1 L1 29 L8.5 22.5 L13.5 35 L19 32.5 L14 20.5 L24 20.5 Z" fill="#fff" stroke="#0b0907" stroke-width="1.6" stroke-linejoin="round"/></svg>' % i
                      for i, s in enumerate(steps) if s["kind"] == "pill" and s.get("click") is not None)
    body = ('<div id="mroot"><div id="mwash"></div><div id="cam">'
            '<div class="blob" id="bg1"><i id="bg1i" style="background:#d4af5f"></i></div>'
            '<div class="blob" id="bg2"><i id="bg2i" style="background:#4aa585"></i></div>'
            '<div id="shape">' + "".join(parts) + '</div>'
            '<div id="lbl">' + labels_html + '</div>'
            '<i id="spark0"></i>' + cursors + '</div></div>')
    html = ('<style>%s</style>\n<div class="card-host clip" id="host-bc" data-card-id="bc" data-unanchored="1" data-start="%.3f" data-duration="%.3f" data-track-index="3"'
            ' style="left:0;top:0;width:1920px;height:1080px;visibility:hidden;opacity:1;">\n<div class="card">%s</div></div>\n' % (CSS, T_IN, DUR - T_IN, body))
    swish = []
    for i in range(1, n):
        swish.append(round(START[i], 3))
        html += '    <audio id="sfx-swish-%d" src="sfx/swish.mp3" data-start="%.3f" data-duration="1.9" data-track-index="%d" data-volume="0.25"></audio>\n' % (i, START[i], 10 + i)

    # ---------------- js: one timeline, every tween a fromTo with explicit values (seek-safe)
    js = []
    def A(s): js.append(s)
    def ft(sel, a, b, dur, ease, t):
        A("tl.fromTo(%s, %s, { %s, duration:%.3f, ease:'%s', immediateRender:false }, %.3f);" % (sel, a, b.strip()[1:-1].strip(), dur, ease, t))
    LAB_Y = lambda h: (h - 4) / 2.0
    A("tl.set('#shape', { xPercent:-50, yPercent:-50, width:0, height:4, borderRadius:2, borderWidth:2, opacity:1 }, 0);")
    A("tl.set('#shape', { '--f':'rgba(11,9,7,.72)' }, 0);")
    A("tl.set('#cam', { scale:1 }, 0);")
    A("tl.set('#spark0', { opacity:0 }, 0);")
    A("tl.set('#bg1', { x:%d, y:%d }, 0); tl.set('#bg2', { x:%d, y:%d }, 0);" % bx[0])
    for i in range(n):
        A("tl.set('#lab%d', { opacity:0, y:12 }, 0);" % i)
        if steps[i]["kind"] in ("pill", "circle", "square"):
            A("tl.set('#sc%d', { opacity:0 }, 0);" % i)
    A("tl.set('#lbl', { y:0 }, 0);")
    for i, s in enumerate(steps):
        if s["kind"] == "pill":
            A("tl.set('#btn%d', { backgroundColor:'rgba(244,239,230,.10)', boxShadow:'0 0 0px rgba(212,175,95,0)' }, 0);" % i)
            if s.get("click") is not None:
                A("tl.set('#cur%d', { opacity:0, x:1500, y:820, scale:1 }, 0);" % i)
        if s["kind"] == "page":
            if s.get("title"): A("tl.set('#ptitle%d', { opacity:0 }, 0);" % i)
            if s.get("check_at") is not None: A("tl.set('#badge%d', { opacity:0, scale:.6 }, 0);" % i)
    # entry: wash, blobs, the line and its spark
    ft("'#mwash'", "{opacity:0}", "{opacity:1}", 0.3, "power2.out", T_IN)
    ft("'#bg1'", "{opacity:0}", "{opacity:1}", 0.5, "power2.out", T_IN)
    ft("'#bg2'", "{opacity:0}", "{opacity:1}", 0.5, "power2.out", T_IN)
    ft("'#shape'", "{width:0}", "{width:420}", 0.5, "power2.out", L0)
    ft("'#spark0'", "{opacity:0, scale:.4}", "{opacity:1, scale:1}", 0.25, "power2.out", L0 + 0.25)
    ft("'#bg1i'", "{x:0, y:0}", "{x:-90, y:50}", DUR - T_IN, "sine.inOut", T_IN)
    ft("'#bg2i'", "{x:0, y:0}", "{x:80, y:-60}", DUR - T_IN, "sine.inOut", T_IN)
    # camera: drift 1.00 -> 1.05 in every state, back to 1.00 inside each change
    for i in range(n):
        b = START[i + 1] if i + 1 < n else T_OUT
        ft("'#cam'", "{scale:1}", "{scale:1.05}", b - END[i], "sine.inOut", END[i])
        if i + 1 < n:
            ft("'#cam'", "{scale:1.05}", "{scale:1}", MD, "sine.inOut", START[i + 1])
    # the changes: shape, label rail, blobs, labels
    for i in range(n):
        w, h, r = pin_dim[i + 1]; pw, ph, pr = pin_dim[i]
        s0, e0 = START[i], END[i]
        ft("'#shape'", "{width:%d, height:%d, borderRadius:%d, borderWidth:%s}" % (pw, ph, pr, "2" if i == 0 else "3"),
           "{width:%d, height:%d, borderRadius:%d, borderWidth:3}" % (w, h, r), MD, "power3.inOut", s0)
        ft("'#lbl'", "{y:%.1f}" % LAB_Y(ph), "{y:%.1f}" % LAB_Y(h), MD, "power3.inOut", s0)
        g, m = bx[i], bx[i + 1]
        ft("'#bg1'", "{x:%d, y:%d}" % (g[0], g[1]), "{x:%d, y:%d}" % (m[0], m[1]), 0.9, "power2.inOut", s0 + 0.12)
        ft("'#bg2'", "{x:%d, y:%d}" % (g[2], g[3]), "{x:%d, y:%d}" % (m[2], m[3]), 0.9, "power2.inOut", s0 + 0.12)
        ft("'#lab%d'" % i, "{opacity:0, y:12}", "{opacity:1, y:0}", 0.4, "power3.out", steps[i]["at"])
        if i >= 1:
            ft("'#lab%d'" % (i - 1), "{opacity:1, y:0}", "{opacity:0, y:-10}", 0.25, "power2.in", steps[i]["at"])
    ft("'#spark0'", "{opacity:1}", "{opacity:0}", 0.2, "power2.in", START[0])
    # page fill: light glass in a page, dark again after it
    for i, s in enumerate(steps):
        if s["kind"] == "page":
            ft("'#shape'", "{'--f':'rgba(11,9,7,.72)'}", "{'--f':'rgba(244,239,230,.8)'}", MD, "power3.inOut", START[i])
        elif i and kinds[i - 1] == "page":
            ft("'#shape'", "{'--f':'rgba(244,239,230,.8)'}", "{'--f':'rgba(11,9,7,.72)'}", MD, "power3.inOut", START[i])
    # content of each state: out when the next change starts, in 0.35 s before the end of its own change
    for i, s in enumerate(steps):
        k = s["kind"]; nxt = START[i + 1] if i + 1 < n else None
        if k in ("pill", "circle", "square"):
            ft("'#sc%d'" % i, "{opacity:0, filter:'blur(6px)'}", "{opacity:1, filter:'blur(0px)'}", 0.35, "power2.out", END[i] - 0.35)
            if nxt is not None:
                ft("'#sc%d'" % i, "{opacity:1, filter:'blur(0px)'}", "{opacity:0, filter:'blur(6px)'}", 0.25, "power2.in", nxt)
    # pill: typing, spark, cursor, click
    for i, s in enumerate(steps):
        if s["kind"] != "pill":
            continue
        txt = s.get("text", ""); nn = len(txt)
        TY0 = END[i] + 0.05
        A("var P%d = { n:0 }; var CH%d = []; for (var i=0;i<%d;i++) CH%d.push(document.getElementById('ch%d_'+i));" % (i, i, nn, i, i))
        A("""function typeUp%d(){ var n=Math.floor(P%d.n+1e-6), last=null; for (var i=0;i<CH%d.length;i++){ var on=i<n; CH%d[i].style.display=on?'inline':'none'; if(on) last=CH%d[i]; }
  var sp=document.getElementById('spark1_%d'); if(last){ sp.style.left=(last.offsetLeft+last.offsetWidth+4)+'px'; } else { sp.style.left='0px'; } }
typeUp%d();""" % (i, i, i, i, i, i, i))
        A("tl.fromTo(P%d, { n:0 }, { n:%d, duration:%.3f, ease:'none', immediateRender:false, onUpdate:typeUp%d, onReverseComplete:typeUp%d }, %.3f);" % (i, nn, nn * 0.04, i, i, TY0))
        ft("'#spark1_%d'" % i, "{opacity:0}", "{opacity:1}", 0.1, "power2.out", TY0)
        ft("'#spark1_%d'" % i, "{opacity:1}", "{opacity:0}", 0.3, "power2.in", TY0 + nn * 0.04 + 0.1)
        c = s.get("click")
        if c is not None:
            assert c - 0.85 >= END[i] - 1e-9 and (i + 1 == n or c + 0.3 <= START[i + 1]), "morph: click %.2f outside the pill's rest %.2f..%.2f" % (c, END[i], START[i + 1] if i + 1 < n else T_OUT)
            ft("'#cur%d'" % i, "{opacity:0, x:1500, y:820}", "{opacity:1, x:1281, y:503}", 0.85, "power2.out", c - 0.85)
            ft("'#cur%d'" % i, "{scale:1}", "{scale:.9}", 0.12, "power2.out", c)
            ft("'#cur%d'" % i, "{scale:.9}", "{scale:1}", 0.12, "power2.out", c + 0.12)
            ft("'#btn%d'" % i, "{backgroundColor:'rgba(244,239,230,.10)', boxShadow:'0 0 0px rgba(212,175,95,0)'}", "{backgroundColor:'rgba(212,175,95,.85)', boxShadow:'0 0 34px rgba(212,175,95,.9)'}", 0.12, "power2.out", c)
            ft("'#btn%d'" % i, "{backgroundColor:'rgba(212,175,95,.85)', boxShadow:'0 0 34px rgba(212,175,95,.9)'}", "{backgroundColor:'rgba(244,239,230,.10)', boxShadow:'0 0 0px rgba(212,175,95,0)'}", 0.18, "power2.inOut", c + 0.12)
            if i + 1 < n:
                ft("'#cur%d'" % i, "{opacity:1}", "{opacity:0}", 0.25, "power2.in", START[i + 1])
    # circle / globe: meridians (still on the bench; spin=True turns them)
    for i, s in enumerate(steps):
        if s["kind"] == "circle" and s.get("icon", "globe") == "globe":
            A("var G%d = { th:0 };" % i)
            A("""function globeUp%d(){ var R=80, th=G%d.th*Math.PI/180; for (var k=0;k<3;k++){ var rx=Math.max(1.5, R*Math.abs(Math.cos(th+k*Math.PI/3))); document.getElementById('mer%d_'+k).setAttribute('rx', rx.toFixed(2)); } }
globeUp%d();""" % (i, i, i, i))
            if s.get("spin"):
                A("tl.fromTo(G%d, { th:0 }, { th:70, duration:3.0, ease:'none', immediateRender:false, onUpdate:globeUp%d, onReverseComplete:globeUp%d }, %.3f);" % (i, i, i, START[i] + 0.2))
            else:
                ft("G%d" % i, "{th:0}", "{th:70}", 3.0, "none", START[i] + 0.2)   # as on the bench: th moves, the drawing stays still
    # grid / page tiles
    GW, GH, PAD, GAP = 1094, 514, 20, 14
    for i, s in enumerate(steps):
        k = s["kind"]
        if k not in ("grid", "page"):
            continue
        ids = tiles_by_step[i]; m = len(ids)
        if k == "page":
            lay = PAGE_LAYOUT[m]
        if k == "grid" or i not in reuse:
            if k == "grid":
                rows = (m + 2) // 3
                tw, th_ = (GW - 2 * PAD - 2 * GAP) / 3.0, (GH - 2 * PAD - GAP * (rows - 1)) / rows
                pos = []
                for j in range(m):
                    c, r = j % 3, j // 3
                    cnt = min(3, m - 3 * r)
                    off = (3 - cnt) * (tw + GAP) / 2.0
                    pos.append((PAD + off + c * (tw + GAP), PAD + r * (th_ + GAP), tw, th_))
            else:
                pos = lay
            for j, tid in enumerate(ids):
                g = pos[j]
                A("tl.set('#%s', { x:%.1f, y:%.1f, width:%.1f, height:%.1f, scale:.9, filter:'blur(6px)' }, 0);" % (tid, g[0], g[1], g[2], g[3]))
                ft("'#%s'" % tid, "{opacity:0, scale:.9, filter:'blur(6px)'}", "{opacity:1, scale:1, filter:'blur(0px)'}", 0.4, "power2.out", END[i] - 0.4 + j * 0.06)
        if i in reuse:
            for j, tid in enumerate(ids):
                g = [None] * 4
                # grid positions of the previous step
                rows = (m + 2) // 3
                tw, th_ = (GW - 2 * PAD - 2 * GAP) / 3.0, (GH - 2 * PAD - GAP * (rows - 1)) / rows
                c, r = j % 3, j // 3
                cnt = min(3, m - 3 * r)
                off = (3 - cnt) * (tw + GAP) / 2.0
                g = (PAD + off + c * (tw + GAP), PAD + r * (th_ + GAP), tw, th_)
                l = lay[j]
                ft("'#%s'" % tid, "{x:%.1f, y:%.1f, width:%.1f, height:%.1f}" % g, "{x:%.1f, y:%.1f, width:%.1f, height:%.1f}" % l, MD, "power3.inOut", START[i] + j * 0.04)
        if k == "page":
            if s.get("title"):
                ft("'#ptitle%d'" % i, "{opacity:0}", "{opacity:1}", 0.35, "power2.out", END[i] - 0.2)
            ca = s.get("check_at")
            if ca is not None:
                ft("'#badge%d'" % i, "{opacity:0, scale:.6}", "{opacity:1, scale:1}", 0.12, "power2.out", ca)
                A("document.getElementById('chk%d').style.strokeDasharray='24';" % i)
                ft("'#chk%d'" % i, "{strokeDashoffset:24}", "{strokeDashoffset:0}", 0.3, "power2.out", ca + 0.1)
        # leaving the state (only when another change follows; the last one fades with the whole card)
        if i + 1 < n:
            nxt = START[i + 1]
            outs = ["'#%s'" % t for t in ids if not (i + 1 in reuse)]
            if k == "page":
                if s.get("title"): outs.append("'#ptitle%d'" % i)
                if s.get("check_at") is not None: outs.append("'#badge%d'" % i)
            for o in outs:
                ft(o, "{opacity:1}", "{opacity:0}", 0.25, "power2.in", nxt)
    # exit
    ft("'#mroot'", "{opacity:1}", "{opacity:0}", 0.2, "power2.in", T_OUT)
    A("tl.set('#mroot', { opacity:1 }, 0);")
    times = {"start": [round(x, 3) for x in START], "end": [round(x, 3) for x in END], "swish": swish,
             "card_start": round(T_IN, 3), "line_at": round(L0, 3), "duration": round(DUR, 3)}
    return {"html": html, "js": "\n        ".join(js), "times": times}
