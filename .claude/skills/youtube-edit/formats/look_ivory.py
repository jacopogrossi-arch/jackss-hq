"""look_ivory.py: the plates-verde look on the OLDER formats (Jacopo, 01/11/2026: "vorrei portare quello stile che abbiamo usato su questa nuova motion plate anche a queste vecchie").

The older formats (compose.py's lists, stats, bars, pipeline, hub, lens, flow, deck, search, dock, pills, chat, tag, equation, wall, pop-out, growth, logo plate...) were built in a
glass look: translucent grey cards, thin white text, neon. The new plates use solid IVORY cards with near-black text, Inter 800 for the words that matter, an italic serif key word
(gold on green, deep green on ivory), mint for structure and state, no neon. This module is that translation, in three parts, all switched on by the preset's style key `look: "ivory"`:

  css()            a stylesheet appended after every older format's own CSS (so it wins at equal specificity)
  GLASS            the glass tween targets (`glassIn` lands on ivory, shadow, no white border)
  swap_literals()  the few fixed 'rgba(255,255,255,0.14)' tween values inside the older formats' JS, repainted to the ivory

compose.py calls them from one place (`swap_legacy_colours`). Without `look: "ivory"` nothing here runs: `--preset none` and `elegante-portfolio` keep their own look.
"""

INK = "#0b0907"
INK2 = "rgba(11,9,7,.62)"
DEEP = "#17613F"          # deep green: the key word and the numbers on ivory
IVORY = "rgba(244,239,230,0.97)"

GLASS = {"bg": IVORY, "border": "rgba(244,239,230,0)", "shadow": "0 30px 60px rgba(0,0,0,0.5)"}


def css():
    return """
  /* ================= look ivory: solid ivory cards, near-black text, italic serif key word, mint for state ================= */
  .glass, .glass .inner { color:%(ink)s; }
  .glass, .glass * { text-shadow:none !important; }
  /* key words: the italic serif (gold on the green plate, deep green on ivory) */
  .st-title, .pl-title, .fx-title, .mt-sub, .gr-eye { font-weight:800; }
  .st-title .em, .pl-title .em, .fx-title .em, .mt-sub .em { font-family:var(--k-serif); font-style:italic; font-weight:500; color:var(--k-accent); letter-spacing:0; }
  .chip .inner .em, .lower .w.em { font-family:var(--k-serif); font-style:italic; font-weight:500; }
  /* tag (progress pips) */
  .tag .label { color:%(ink)s; text-shadow:none; font-weight:800; }
  .tag .pip { background:rgba(11,9,7,.22); } .tag .pip.done { background:%(deep)s; }
  .tag .pip.now { background:var(--k-accent2); box-shadow:0 0 0 3px %(deep)s; }
  /* lists, bullets, pop-out */
  .list .eyebrow, .po .ttl { color:%(deep)s; font-family:var(--k-serif); font-style:italic; font-weight:500; }
  .list .item .t, .po .item .t { color:%(ink)s; font-weight:800; }
  .mk .ring { stroke:rgba(11,9,7,.4); } .mk .tick { stroke:%(deep)s; } .list.bad .mk .tick { stroke:#b3261e; }
  .po .item .d { background:%(deep)s; box-shadow:none; }
  /* stat tiles, growth card */
  .st-num { color:%(ink)s; font-weight:800; } .st-tile.em .st-num { color:%(deep)s; } .st-lab { color:%(ink2)s; font-weight:700; }
  .gr-eye { color:%(ink2)s; } .gr-num { color:%(deep)s; font-weight:800; } .gr-sub { color:%(ink2)s; }
  .gr-bar { background:linear-gradient(180deg, rgba(11,9,7,.6), rgba(11,9,7,.14)); box-shadow:none; }
  .gr-bar.last { background:linear-gradient(180deg, %(deep)s, #3f9a78); box-shadow:none; }
  .gr-line { stroke:%(ink)s; filter:none; } .gr-dot { fill:%(deep)s; filter:none; } .gr-area { fill:rgba(23,97,63,.14); } .gr-pt { fill:#fff; stroke:%(ink)s; }
  .gr-badge { background:%(ink)s; color:#f4efe6; }
  /* bars (on the green plate: ivory bars, mint for the one that is ours) */
  .bc-lab { color:rgba(244,239,230,.9); font-weight:800; } .bc-row.hi .bc-lab { color:#f4efe6; }
  .bc-track { background:rgba(244,239,230,.12); } .bc-fill { background:rgba(244,239,230,.55); }
  .bc-row.hi .bc-fill { background:var(--k-accent2); box-shadow:0 0 26px rgba(94,230,168,.45); }
  .bc-val { color:#f4efe6; font-weight:800; } .bc-row.hi .bc-val { color:var(--k-accent2); }
  /* pipeline */
  .pl-lab { color:%(ink)s; font-weight:800; } .pl-sub, .pl-num { color:%(ink2)s; } .pl-node .ic { stroke:%(deep)s; }
  .pl-link { background:rgba(244,239,230,.55); }
  /* hub */
  .hb-c .inner, .hb-pill .inner { color:%(ink)s; font-weight:800; } .hb-spoke { stroke:rgba(244,239,230,.55); }
  /* equation */
  .eq .tk { color:%(ink)s; font-weight:800; } .eq .tk.op { color:%(ink2)s; }
  .eq .tk.em { color:%(deep)s; font-family:var(--k-serif); font-style:italic; font-weight:500; } .eq .tk.pay { color:#8a6a1c; font-family:var(--k-serif); font-style:italic; font-weight:500; }
  /* slot wall */
  .wl-slot { border-color:rgba(11,9,7,.4); } .wl-slot .n { color:%(ink2)s; } .wl-slot .t { color:%(ink)s; font-weight:800; }
  .wl-slot.done { border-color:rgba(11,9,7,.25); background:rgba(11,9,7,.06); }
  .wl-slot .fill { border-color:%(deep)s; background:rgba(23,97,63,.16); box-shadow:none; } .wl-thread { background:%(deep)s; box-shadow:none; }
  /* flow */
  .fl-node .lab { color:%(ink)s; font-weight:800; } .fl-node .dot { background:rgba(11,9,7,.4); }
  .fl-path { stroke:rgba(244,239,230,.22); } .fl-glow { stroke:rgba(94,230,168,.18); }
  /* lens (glass focus) */
  .ln-ttl { color:%(deep)s; font-family:var(--k-serif); font-style:italic; font-weight:500; } .ln-row { color:%(ink)s; font-weight:800; }
  .ln-lens { background:%(ink)s; border:none; box-shadow:0 14px 34px rgba(0,0,0,.4); } .ln-win .ln-row { color:#f4efe6; }
  .ln-sharp .v { color:var(--k-accent2); } .ln-fr, .ln-hl { display:none; }
  /* search */
  .sr-bar .ic { stroke:%(ink)s; } .sr-ph { color:%(ink2)s; } .sr-q, .sr-t { color:%(ink)s; font-weight:800; } .sr-s { color:%(ink2)s; } .sr-caret { background:%(deep)s; }
  /* dock, tooltips */
  .dk-tip { background:%(ink)s; color:#f4efe6; box-shadow:0 10px 30px rgba(0,0,0,.4); } .dk-ic { box-shadow:0 12px 30px rgba(0,0,0,.35); } .dk-svg path { stroke:var(--k-accent2); }
  /* masked title: the eyebrow is an italic serif line, never small spaced capitals */
  .mt-eye { font-family:var(--k-serif); font-style:italic; font-weight:500; font-size:46px; letter-spacing:0; text-transform:none; color:var(--k-accent); }
  .mt-t { font-weight:800; } .mt-rule2 { background:rgba(244,239,230,.25); }
  /* pills (around the head) */
  .pls .t { font-family:var(--k-font); font-style:normal; font-weight:800; color:%(ink)s; letter-spacing:-.01em; } .pls .ic { stroke:%(deep)s; } .pls.cyan .t { color:%(ink)s; } .pls.cyan .ic { stroke:%(deep)s; }
  /* world nodes and the numbered deck: ivory cards, ink text, deep-green icons and numbers; the hex and free text stay light on the plate */
  .wd-card .wd-lab, .wd-orb .wd-lab, .wd-pill .wd-lab, .wd-stat .wd-lab, .dq-card .ttl { color:%(ink)s; font-weight:800; }
  .wd-sub { color:%(ink2)s; } .wd-no, .dq-card .no { color:%(deep)s; font-family:var(--k-serif); font-weight:500; }
  .wd-card .icn, .wd-orb .icn, .wd-pill .icn, .wd-stat .icn, .dq-card .icn, .wd-card .icn *, .wd-orb .icn *, .wd-pill .icn *, .wd-stat .icn *, .dq-card .icn * { stroke:%(deep)s; }
  .wd-stat .v { color:%(deep)s; font-weight:800; } .wd-stat .track { background:rgba(11,9,7,.14); } .wd-stat .fill { background:%(deep)s; box-shadow:none; }
  .wd-hex .wd-lab, .wd-text { font-weight:800; } .wd-hex polygon { stroke:rgba(244,239,230,.8); }
  .dq-head { font-family:var(--k-serif); font-style:italic; font-weight:500; font-size:60px; letter-spacing:0; color:var(--k-accent); }
  /* build (picture, label, value): sentence-case Inter label, the value in the italic serif; never spaced capitals */
  .k-label { text-transform:none; letter-spacing:-.01em; font-weight:800; background:none; color:#f4efe6; -webkit-text-fill-color:currentColor; filter:none; font-size:54px; }
  .k-label::after { display:none; }
  .k-value { font-family:var(--k-serif); font-style:italic; font-weight:500; letter-spacing:0; text-transform:none; font-size:52px; text-shadow:none; }
  /* orbit card, agenda chips, dashboard-zoom card, player */
  .k-or-card { background:rgba(244,239,230,.97); box-shadow:0 40px 90px rgba(0,0,0,.5); }
  .k-or-card .t { color:%(ink)s; font-weight:800; text-transform:none; letter-spacing:-.02em; } .k-or-card .s { color:%(ink2)s; }
  .k-or-cap { text-transform:none; letter-spacing:0; font-weight:800; }
  .k-ag-item { background:rgba(244,239,230,.97) !important; color:%(ink)s !important; text-transform:none; letter-spacing:-.01em; font-weight:800; box-shadow:0 14px 34px rgba(0,0,0,.35); }
  .k-ag-item .n { color:%(deep)s; font-family:var(--k-serif); font-style:italic; font-weight:500; }
  .dz-lab { color:%(ink2)s; } .dz-num { color:%(deep)s; font-weight:800; } .dz-delta { background:%(deep)s; color:#f4efe6; } .dz-spark path { stroke:%(deep)s; }
  .pv .pill, .pv .ttl { color:%(ink)s; } .pv .tm { color:%(ink2)s; } .pv .track { background:rgba(11,9,7,.15); } .pv .fillx { background:%(deep)s; }
  .pv .tri, .pv .ptri { border-color:transparent transparent transparent %(ink)s; }
  /* chat: ivory for them, mint for me (already), ink text */
  .chat-me, .bub.me { color:#06140d; }
""" % {"ink": INK, "ink2": INK2, "deep": DEEP}


def css_late():
    """Rules for formats that ship their own <style> inside raw_html (the 3D card chain): appended right before </body> so they come after those styles."""
    return """
  /* look ivory, late: the 3D card chain (27b) */
  .bc-lab { color:%(ink)s; font-weight:800; } .bc-num { color:%(deep)s; font-family:var(--k-serif); font-style:italic; font-weight:500; }
  .bc-badge { background:rgba(23,97,63,.08); border-color:rgba(23,97,63,.45); } .bc-badge .ic { stroke:%(deep)s; }
""" % {"ink": INK, "deep": DEEP}


LITERALS = [   # fixed tween values inside the older formats' JS: (old, new)
    ("backgroundColor: 'rgba(255,255,255,0.14)'", "backgroundColor: '%s'" % IVORY),
    ("backgroundColor: 'rgba(255,255,255,0.16)'", "backgroundColor: '%s'" % IVORY),
    ("backgroundColor: 'rgba(255,255,255,0.18)'", "backgroundColor: '%s'" % IVORY),
    ("backgroundColor: 'rgba(255,255,255,0.07)'", "backgroundColor: 'rgba(244,239,230,0.45)'"),
    ("borderColor: 'rgba(255,255,255,0.58)'", "borderColor: 'rgba(244,239,230,0)'"),
    ("borderColor: 'rgba(255,255,255,0.30)'", "borderColor: 'rgba(244,239,230,0)'"),
    ("boxShadow: '0 24px 80px rgba(0,0,0,0.38)'", "boxShadow: '0 30px 60px rgba(0,0,0,0.5)'"),
]


def swap_literals(html):
    import re
    for old, new in LITERALS:
        html = html.replace(old, new)
    # the same tween values written without the space after the colon (chain3d, others): backgroundColor:'rgba(255,255,255,0.14)'
    html = re.sub(r"backgroundColor:'rgba\(255,255,255,0\.(?:14|16|18)\)'", "backgroundColor:'%s'" % IVORY, html)
    html = re.sub(r"backgroundColor:'rgba\(255,255,255,0\.(?:056|07)\)'", "backgroundColor:'rgba(244,239,230,0.45)'", html)
    html = re.sub(r"borderColor:'rgba\(255,255,255,0\.(?:232|30|58)\)'", "borderColor:'rgba(244,239,230,0)'", html)
    return html
