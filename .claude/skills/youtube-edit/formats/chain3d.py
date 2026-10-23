"""chain3d.py: the 3D card chain (format 27b), a chain of spoken steps as glass cards in 3D space, a slow camera
gliding card to card, soft arrows drawn along the way, one soft swish per travel. Built on the bench A/B of 23/10/2026
(`videos/_bench/ab/processo-glide/`): it beat the `pipeline` (27) on the same 16 s window, the creator chose it for being
"much smoother" and asked for arrows and no pop sounds.

Usage (any build script, or compose.py's "raw_html"/"raw_js"):
    import sys; sys.path.insert(0, "<SK>/formats"); from chain3d import chain3d, write_swish
    out = chain3d(steps=[("Label", "browser", 2.6, "anchor word"), ...], t_in=1.9, t_out=16.3)   # 3 to 5 steps
    storyboard["raw_html"] = out["html"]; storyboard["raw_js"] = out["js"]; write_swish("<project>/public", "<SK>")
steps: (label up to 3 words, icon from compose.py ICONS, time the spoken word lands, anchor word). The last step is magenta.
Spec and numbers: references/formats.md, 27b. Seek-safe: every tween is a fromTo with explicit values.
"""
import math, os, re, subprocess

SK = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
_m = re.search(r"^ICONS = \{.*?^\}", open(os.path.join(SK, "scripts/compose.py"), encoding="utf-8").read(), re.S | re.M)
ICONS = eval(_m.group(0).split("=", 1)[1])
SWISH_SRC = "assets/sfx/mixclap/whoosh-ethereal.mp3"
CW, CH = 560, 340


def write_swish(public, sk=SK):
    """sfx/swish.mp3 in the project: whoosh-ethereal cut to 1.9 s (attack 0.08 s, release 0.5 s from 1.4 s)."""
    os.makedirs(os.path.join(public, "sfx"), exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", os.path.join(sk, SWISH_SRC), "-t", "1.9", "-af",
                    "afade=t=in:d=0.08,afade=t=out:st=1.4:d=0.5", os.path.join(public, "sfx", "swish.mp3")], check=True)


def chain3d(steps, t_in, t_out, label_px=56):
    n = len(steps)
    assert 3 <= n <= 5, "3 to 5 steps"
    STEPS = steps
    LABEL_PX = label_px
    T_IN, T_OUT = t_in, t_out
    X = [980 * i for i in range(n)]; Y = [0, -70, 60, -50, 0][:n]; Z = [0, -120, 0, -120, 0][:n]
    RY = [-10, 10, -10, 10, -10][:n]
    LAST = n - 1
    # ---- times
    arr = [None] * n          # moment card i is at rest at the centre
    arr[0] = STEPS[0][2] - 0.1
    trav = [None] * n         # (ts, te) of the travel INTO card i
    for i in range(1, n):
        w = STEPS[i][2]; te = w - 0.1
        ts = max(w - 2.0, arr[i - 1] + 0.6)
        assert te - ts >= 1.4 - 1e-9, (i, te - ts)
        trav[i] = (round(ts, 3), round(te, 3)); arr[i] = te


    cards = ""
    for i, (lab, ic, w, anc) in enumerate(STEPS):
        svg = '<svg viewBox="0 0 64 64"><path class="ic" d="%s"/></svg>' % ICONS[ic]
        cards += ('<div class="glass bc" id="bc%d" data-at="%.3f" data-anchor="%s"><div class="bc-glow" id="bcg%d" style="box-shadow:%s"></div><div class="bc-in" id="bci%d"><div class="bc-num">%02d</div>'
                  '<div class="bc-badge">%s</div><div class="bc-lab" id="bcl%d">%s</div></div></div>\n' % (i, w - 0.1, anc, i, "0 0 46px rgba(205,0,238,0.6)" if i == LAST else "0 0 40px rgba(10,240,240,0.55)", i, i + 1, svg, i, lab))

    css = """
      .bcw { position:absolute; inset:0; perspective:1500px; perspective-origin:50%% 50%%; overflow:hidden; }
      .bcd, .bcc { position:absolute; inset:0; transform-style:preserve-3d; }
      .bc { left:%dpx; top:%dpx; width:%dpx; height:%dpx; border-radius:30px; will-change:transform; }
      .bc-glow { position:absolute; inset:-3px; border-radius:30px; opacity:0; pointer-events:none; }
      .bc-in { position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:26px; opacity:0; }
      .bc-badge { width:96px; height:96px; border-radius:50%%; display:flex; align-items:center; justify-content:center;
        background:rgba(255,255,255,.10); border:3px solid rgba(255,255,255,.5); }
      .bc-badge svg { width:54px; height:54px; overflow:visible; }
      .bc-badge .ic { fill:none; stroke:#fff; stroke-width:4.5; stroke-linecap:round; stroke-linejoin:round; }
      .bc-num { position:absolute; left:26px; top:20px; font-weight:700; font-size:26px; color:rgba(255,255,255,.6); }
      .bc-lab { width:100%%; font-weight:700; font-size:%dpx; line-height:1.05; color:#fff; white-space:nowrap; text-align:center; letter-spacing:-.01em; }
    """ % (960 - CW // 2, 540 - CH // 2, CW, CH, LABEL_PX)

    import math
    ARROWS = []
    arrows_html = ""
    for i in range(n - 1):
        sx, sy, sz = X[i] + CW // 2, Y[i], Z[i]; ex, ey, ez = X[i+1] - CW // 2, Y[i+1], Z[i+1]
        dx, dy, dz = ex - sx, ey - sy, ez - sz
        Ln = math.sqrt(dx*dx + dy*dy + dz*dz)
        ARROWS.append((sx, sy, sz, Ln, math.degrees(math.atan2(dy, dx)), math.degrees(math.atan2(-dz, dx))))
        col = "205,0,238" if i == n - 2 else "10,240,240"
        arrows_html += ('<div class="ar" id="ar%d" style="left:%dpx;top:%dpx;width:%dpx"><div class="ar-l" id="arl%d" style="background:linear-gradient(90deg,rgba(%s,0) 0%%,rgba(%s,.9) 16%%,rgba(%s,.9) 80%%,rgba(%s,0) 100%%)"></div>'
                        '<div class="ar-h" id="arh%d" style="border-left-color:rgba(%s,.85);filter:blur(1px) drop-shadow(0 0 7px rgba(%s,.7))"></div></div>\n' % (i, 960 + sx, 540 + sy - 3, Ln - 36, i, col, col, col, col, i, col, col))
    css += """
      .ar { position:absolute; height:6px; transform-origin:0 50%; }
      .ar-l { position:absolute; left:0; top:0; width:100%; height:6px; border-radius:3px; transform-origin:0 50%; filter:blur(1.6px); box-shadow:0 0 16px rgba(10,240,240,.0); }
      .ar-h { position:absolute; right:-6px; top:-12px; width:0; height:0; border-left:26px solid #fff; border-top:15px solid transparent; border-bottom:15px solid transparent; transform-origin:0 50%; }
    """

    html = ('<style>%s</style>\n<div class="card-host clip" id="host-bc" data-card-id="bc" data-unanchored="1" data-start="%.3f" data-duration="%.3f" data-track-index="3"'
            ' style="left:0;top:0;width:1920px;height:1080px;visibility:hidden;opacity:1;">\n<div class="card"><div class="cut"><div class="gridbg"></div>'
            '<div class="bcw"><div class="bcd" id="bcd"><div class="bcc" id="bcc">\n%s%s</div></div></div></div></div></div>\n'
            % (css, T_IN, T_OUT - T_IN, cards, arrows_html))
    for i in range(1, n):
        html += '    <audio id="sfx-swish-%d" src="sfx/swish.mp3" data-start="%.3f" data-duration="1.9" data-track-index="%d" data-volume="0.25"></audio>' % (i, trav[i][0], 10 + i) + chr(10)


    # ---- js (one timeline, every tween a fromTo with explicit values: seek-safe)
    LOOK = {
     "hidden": "{ backgroundColor:'rgba(255,255,255,0)', borderColor:'rgba(255,255,255,0)' }",
     "cyan":   "{ backgroundColor:'rgba(255,255,255,0.14)', borderColor:'rgba(10,240,240,0.95)' }",
     "magenta": "{ backgroundColor:'rgba(255,255,255,0.14)', borderColor:'rgba(205,0,238,0.95)' }",
     "back":   "{ backgroundColor:'rgba(255,255,255,0.056)', borderColor:'rgba(255,255,255,0.232)' }",
    }
    CONT = {"hidden": 0, "cyan": 1, "magenta": 1, "back": 0.4}
    GL = {'hidden': 0, 'cyan': 1, 'magenta': 1, 'back': 0}
    js = []
    def look(i, a, b, t0, dur, ease):
        js.append("tl.fromTo('#bc%d', %s, Object.assign({}, %s, { duration:%.3f, ease:'%s', immediateRender:false }), %.3f);" % (i, LOOK[a], LOOK[b], dur, ease, t0))
        js.append("tl.fromTo('#bcg%d', { opacity:%s }, { opacity:%s, duration:%.3f, ease:'%s', immediateRender:false }, %.3f);" % (i, GL[a], GL[b], dur, ease, t0))
        js.append("tl.fromTo('#bci%d', { opacity:%s }, { opacity:%s, duration:%.3f, ease:'%s', immediateRender:false }, %.3f);" % (i, CONT[a], CONT[b], dur, ease, t0))
    def last(i): return "magenta" if i == LAST else "cyan"
    # initial poses
    for i in range(n):
        js.append("tl.set('#bc%d', { x:%d, y:%d, z:%d, rotationY:%d, scale:0.92 }, 0);" % (i, X[i], Y[i], Z[i], RY[i]))
        js.append("tl.set('#bc%d', %s, 0);" % (i, LOOK["hidden"]))
        js.append("tl.set('#bci%d', { opacity:0 }, 0);" % i)
        js.append("tl.set('#bcg%d', { opacity:0 }, 0);" % i)
        js.append("tl.set('#bcl%d', { x:0 }, 0);" % i)
    js.append("tl.set('#bcc', { x:0, y:0, z:0 }, 0); tl.set('#bcd', { scale:1 }, 0);")
    # card 1 appears
    js.append("tl.fromTo('#bc0', { scale:0.92, rotationY:%d }, { scale:1, rotationY:0, duration:0.5, ease:'power3.out', immediateRender:false }, 2.0);" % RY[0])
    look(0, "hidden", last(0), 2.0, 0.5, "power3.out")
    DRIFT = 0.006
    def drift(t0, t1):
        js.append("tl.fromTo('#bcd', { scale:1 }, { scale:%.5f, duration:%.3f, ease:'none', immediateRender:false }, %.3f);" % (1 + DRIFT * (t1 - t0), t1 - t0, t0))
    for i in range(1, n):
        ts, te = trav[i]
        drift(arr[i - 1], ts)
        # camera travel (the drift scale eases back to 1 inside it)
        js.append("tl.fromTo('#bcc', { x:%d, y:%d, z:%d }, { x:%d, y:%d, z:%d, duration:%.3f, ease:'sine.inOut', immediateRender:false }, %.3f);"
                  % (-X[i-1], -Y[i-1], -Z[i-1], -X[i], -Y[i], -Z[i], te - ts, ts))
        js.append("tl.fromTo('#bcd', { scale:%.5f }, { scale:1, duration:%.3f, ease:'sine.inOut', immediateRender:false }, %.3f);" % (1 + DRIFT * (ts - arr[i-1]), te - ts, ts))
        # parallax of the titles (60 px faster than the ground, same travel)
        js.append("tl.fromTo('#bcl%d', { x:60 }, { x:0, duration:%.3f, ease:'sine.inOut', immediateRender:false }, %.3f);" % (i, te - ts, ts))
        js.append("tl.fromTo('#bcl%d', { x:0 }, { x:-60, duration:%.3f, ease:'sine.inOut', immediateRender:false }, %.3f);" % (i - 1, te - ts, ts))
        # new card appears in the last second of the travel
        js.append("tl.fromTo('#bc%d', { scale:0.92, rotationY:%d }, { scale:1, rotationY:0, duration:1.0, ease:'power3.out', immediateRender:false }, %.3f);" % (i, RY[i], te - 1.0))
        look(i, "hidden", last(i), te - 1.0, 1.0, "power3.out")
        # old card goes behind
        js.append("tl.fromTo('#bc%d', { rotationY:0, z:%d }, { rotationY:%d, z:%d, duration:1.0, ease:'power2.inOut', immediateRender:false }, %.3f);" % (i - 1, Z[i-1], RY[i-1], Z[i-1] - 160, ts))
        look(i - 1, last(i - 1), "back", ts, 1.0, "power2.inOut")
    drift(arr[LAST], T_OUT)
    for i in range(n - 1):
        sx, sy, sz, Ln, rz, ry = ARROWS[i]; ts = trav[i + 1][0]
        js.append("tl.set('#ar%d', { x:0, y:0, z:%d, rotationZ:%.3f, rotationY:%.3f, opacity:1, transformOrigin:'0%% 50%%' }, 0);" % (i, sz, rz, ry))
        js.append("tl.set('#arl%d', { scaleX:0 }, 0); tl.set('#arh%d', { opacity:0, scale:0.6 }, 0);" % (i, i))
        js.append("tl.fromTo('#arl%d', { scaleX:0 }, { scaleX:1, duration:0.6, ease:'power2.inOut', immediateRender:false }, %.3f);" % (i, ts))
        js.append("tl.fromTo('#arh%d', { opacity:0, scale:0.6 }, { opacity:1, scale:1, duration:0.2, ease:'power2.out', immediateRender:false }, %.3f);" % (i, ts + 0.5))
        if i < n - 2:
            tn = trav[i + 2][0]
            js.append("tl.fromTo('#ar%d', { opacity:1 }, { opacity:0.4, duration:1.0, ease:'power2.inOut', immediateRender:false }, %.3f);" % (i, tn))

    raw_js = "\n        ".join(js)
    return {"html": html, "js": raw_js, "travels": trav, "arrivals": arr}
