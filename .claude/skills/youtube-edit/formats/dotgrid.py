"""dotgrid.py: the dot grid (format 31), a count made visible: a grid of empty dots, one row per spoken group, each row
filling with its colour on its word. Built on the bench A/B of 23/10/2026 (`videos/_bench/ab/lista-dotgrid/`), after the
@realskytan reel (100 people as 100 dots): it beat the glass list (3a) on the `lista` window; the creator: "perfect".

Usage (any build script, or compose.py's "raw_html"/"raw_js"):
    import sys; sys.path.insert(0, "<SK>/formats"); from dotgrid import dotgrid
    out = dotgrid(rows=[("Outfit", 7.259, "tre outfit"), ...], title="Tre di ogni cosa", t_in=6.2, t_out=11.5)
    storyboard["raw_html"] = out["html"]; storyboard["raw_js"] = out["js"]
rows: (label, time the group's word lands, anchor phrase), two to five rows; cols: dots per row (the spoken count, 2 to 6).
The grid sits on the free side of the face (default right edge at x 1780, centred on y 540); labels right-aligned to its left.
Colours from the elegante-portfolio preset: gold, emerald, then their light mixes toward ivory. No sound (the creator rejects pops).
Spec and numbers: references/formats.md, 31. Seek-safe: every tween is a fromTo with explicit values.
"""

GOLD, EMER, IVORY = "#d4af5f", "#4aa585", "#f4efe6"


def _mix(h, k=0.45):
    iv = [int(IVORY[i:i + 2], 16) for i in (1, 3, 5)]
    c = [int(h[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % tuple(round(a + (b - a) * k) for a, b in zip(c, iv))


def _rgb(h):
    return "%d,%d,%d" % tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def dotgrid(rows, title, t_in, t_out, cols=3, right=1780, cy=540, exit_s=0.4):
    n = len(rows)
    assert 2 <= n <= 5 and 2 <= cols <= 6, "two to five rows, two to six dots a row"
    COL = ([GOLD, EMER, _mix(GOLD), _mix(EMER), GOLD])[:n]
    D, GAP = 64, 22
    GW, GH = cols * D + (cols - 1) * GAP, n * D + (n - 1) * GAP
    GX, GY = right - GW, cy - GH // 2
    H0, H1 = t_in - 0.2, t_out + exit_s
    T = [r[1] for r in rows]

    css = """
  #host-dg { font-family:"Inter","Segoe UI",system-ui,sans-serif; }
  .dgd { position:absolute; width:%dpx; height:%dpx; box-sizing:border-box; border-radius:50%%; border:2px solid rgba(255,255,255,.35); }
  .dgf { position:absolute; inset:-2px; border-radius:50%%; opacity:0; }
  .dgl { position:absolute; width:560px; height:%dpx; line-height:%dpx; text-align:right; font-weight:600; font-size:32px; color:#f4efe6;
         white-space:nowrap; text-shadow:0 2px 14px rgba(0,0,0,.6); opacity:0; }
  #dgt { position:absolute; width:700px; text-align:right; font-family:"Playfair Display",Georgia,serif; font-style:italic; font-weight:500;
         font-size:44px; line-height:52px; color:#f4efe6; text-shadow:0 2px 16px rgba(0,0,0,.6); opacity:0; }
""" % (D, D, D, D)
    els = '<div id="dgt" style="left:%dpx;top:%dpx">%s</div>\n' % (right - 700, GY - 36 - 52, title)
    for r in range(n):
        for c in range(cols):
            els += ('<div class="dgd" id="d%d%d" style="left:%dpx;top:%dpx"><div class="dgf" id="f%d%d" style="background:%s"></div></div>\n'
                    % (r, c, GX + c * (D + GAP), GY + r * (D + GAP), r, c, COL[r]))
        els += ('<div class="dgl" id="lb%d" data-at="%.3f" data-anchor="%s" style="left:%dpx;top:%dpx">%s</div>\n'
                % (r, T[r], rows[r][2], GX - 28 - 560, GY + r * (D + GAP), rows[r][0]))
    html = ('<style>%s</style>\n<div class="card-host clip" id="host-dg" data-card-id="dg" data-unanchored="1" data-start="%.3f" data-duration="%.3f" data-track-index="3"'
            ' style="left:0;top:0;width:1920px;height:1080px;visibility:hidden;opacity:1;">\n<div id="dgw" style="position:absolute;inset:0">\n%s</div></div>\n'
            % (css, H0, H1 - H0, els))

    js = []
    js.append("tl.set('#dgw', { opacity:1, x:0 }, 0);")
    js.append("tl.set('#dgt', { opacity:0, y:12 }, 0);")
    for r in range(n):
        js.append("tl.set('#lb%d', { opacity:0, x:-14 }, 0);" % r)
        for c in range(cols):
            js.append("tl.set('#d%d%d', { opacity:0, scale:0.8 }, 0);" % (r, c))
            js.append("tl.set('#f%d%d', { opacity:0, scale:0.5, boxShadow:'0 0 0px rgba(%s,0)' }, 0);" % (r, c, _rgb(COL[r])))
    js.append("tl.fromTo('#dgt', { opacity:0, y:12 }, { opacity:1, y:0, duration:0.4, ease:'power3.out', immediateRender:false }, %.3f);" % t_in)
    for k in range(n * cols):   # empty dots appear together, 0.02 s apart
        r, c = divmod(k, cols)
        js.append("tl.fromTo('#d%d%d', { opacity:0, scale:0.8 }, { opacity:1, scale:1, duration:0.4, ease:'power3.out', immediateRender:false }, %.3f);" % (r, c, t_in + k * 0.02))
    for r in range(n):   # a row fills left to right on its word, 0.07 s apart, with a soft glow
        for c in range(cols):
            js.append("tl.fromTo('#f%d%d', { opacity:0, scale:0.5, boxShadow:'0 0 0px rgba(%s,0)' }, { opacity:1, scale:1, boxShadow:'0 0 24px rgba(%s,0.55)', duration:0.3, ease:'power2.out', immediateRender:false }, %.3f);"
                      % (r, c, _rgb(COL[r]), _rgb(COL[r]), T[r] + c * 0.07))
        js.append("tl.fromTo('#lb%d', { opacity:0, x:-14 }, { opacity:1, x:0, duration:0.4, ease:'power3.out', immediateRender:false }, %.3f);" % (r, T[r]))
        if r < n - 1:   # the label drops to .65 once the next group arrives
            js.append("tl.fromTo('#lb%d', { opacity:1.0 }, { opacity:0.65, duration:0.3, ease:'power2.out', immediateRender:false }, %.3f);" % (r, T[r + 1]))
    js.append("tl.fromTo('#dgw', { opacity:1, x:0 }, { opacity:0, x:30, duration:%.3f, ease:'power2.in', immediateRender:false }, %.3f);" % (exit_s, t_out))
    return {"html": html, "js": "\n        ".join(js)}
