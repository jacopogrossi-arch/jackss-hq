# Short #16 «Non ho niente da venderti» (v2, 20/11/2026). Market stall at dawn seen FRONTALLY; the narrator (toy Jacopo) stands on the counter from frame 0.
# Rules after v1 was rejected ("telecamera storta, mai centrata, card sbagliate, pantalone glitchato"):
#  - every camera is on axis with its subject (pos.x == look.x) and level (pos.y == look.y, close-ups max 0.12 m up, SOP numbers); _flush asserts it, and no trims allowed
#  - nothing comes out of the counter: objects appear with t= (fade + 12 cm rise) where nothing is under them, cards hang from the clothesline and leave upwards
#  - every card is a fact said by the voice at that moment, with its source in script.md
import json, math, os, re, shutil, sys
SK = "D:/ClaudeCodeTest/.claude/skills/fashion-3d"
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SK + "/engine"); sys.path.insert(0, HERE)
from world3d import World3D
import room
PI = math.pi
WORDS = json.load(open(HERE + "/words.json", encoding="utf-8"))
JAW = json.load(open(HERE + "/jaw.json"))
norm = lambda s: re.sub(r"[^\w]", "", s.lower().split("'")[-1])


def at(word, n=1, after=0.0):
    k = 0
    for x in WORDS:
        if x["s"] >= after and norm(x["w"]) == norm(word):
            k += 1
            if k == n: return round(x["s"], 2)
    raise KeyError(word)


def end(word, n=1, after=0.0):
    k = 0
    for x in WORDS:
        if x["s"] >= after and norm(x["w"]) == norm(word):
            k += 1
            if k == n: return round(x["e"], 2)
    raise KeyError(word)


DUR = round(WORDS[-1]["e"] + 2.4, 1)
TROUSER = "D:/ClaudeCodeTest/videos/_bench/assets3d/finali/pantalone.glb"
OMINO = os.environ.get("OMINO", "D:/ClaudeCodeTest/videos/_bench/short-16/assets/narratore-perf-smooth.glb")
w = World3D("s", 0.0, DUR, fov=42, w=1080, h=1920, fade=0.4)
w.shutter(0.5)
GESSO, SABBIA, RUGGINE, BOSCO = "#EFE9DD", "#B9AE98", "#8A4B2D", "#2F3A2E"
room.furnish(w)
SX, SZ = room.STALL
Y = room.Y

# ---- the sign on the front of the counter: «IN VENDITA», and on "c'è solo il DOCUMENTO" it becomes «IN CORSO»
T_FLIP = at("documento", 2) - 0.1
SIGNP = (SX, 0.42, SZ + 0.58)
w.card("sign_a", SIGNP, w=1.3, h=0.44, text="*IN VENDITA*", size=120, color="#16120f", ink=GESSO, key="#ff8a5c", flat=True,
       move=[(T_FLIP + 0.6, 0.01, (SIGNP[0], -8.0, SIGNP[2]), "linear")])
w.card("sign_b", (SIGNP[0], SIGNP[1], SIGNP[2] + 0.012), w=1.3, h=0.44, text="*IN CORSO*", size=120, color=GESSO, ink="#16120f", key=RUGGINE, flat=True, t=T_FLIP)

# ---- the fact cards on the clothesline: (id, x, w, h, t_in, t_out, title, sub, kind)   kind: "no" red cross, "ok" green tick, None neutral
# v2b: never more cards than the frame holds; "ogni strumento, ogni costo, ogni errore" = one card at a time in the centre (each pushes the previous one up)
CZ = room.LINE_Z + 0.02
T_OGNI = at("Ogni")
PX = room.PED_L[0]
CARDS = [
    ("k_corsi", -0.41, 0.74, 0.4, at("corso") - 0.15, at("Economia") - 0.9, "*Corsi*", "zero", "no"),
    ("k_brand", 0.41, 0.74, 0.4, at("aperto") - 0.15, at("Economia") - 0.9, "*Brand*", "non ancora aperto", "no"),
    ("k_studio", 0.0, 0.78, 0.4, at("Economia") + 0.35, at("primo") - 0.6, "*Economia* + *Moda*", "università + accademia", "ok"),
    ("k_drop", PX, 0.62, 0.34, at("primo") - 0.1, at("disegnato") - 0.35, "*Drop 1*", "pieghe doppie · side adjuster", None),
    ("k_3d", PX, 0.62, 0.34, at("disegnato"), at("sbagliato") - 0.35, "disegno → *3D*", "Short del 18/11", None),
    ("k_gonna", PX, 0.62, 0.34, at("sbagliato"), T_OGNI - 0.9, "sembrava *una gonna*", "il primo pantalone · Short #1", "no"),
    ("k_tools", 0.0, 0.78, 0.4, at("strumento") - 0.1, at("costo") - 0.35, "Tripo · *Blender*", "strumenti provati", None),
    ("k_cost", 0.0, 0.78, 0.4, at("costo") - 0.1, at("errore") - 0.35, "*511 crediti*", "la voce di questo Short", None),
    ("k_err", 0.0, 0.78, 0.4, at("errore") - 0.1, at("Il", 2) - 0.2, "*6 versioni*", "Short #3, prima di uscire", "no"),
]
STYLE = {"no": dict(color="#33100e", border="#ff5a47", badge="no"), "ok": dict(color="#0e2b1a", border="#4be08a", badge="ok"), None: dict(color="#16120f", border="#d9b36a")}
for oid, x, cw, ch, t0, t1, title, sub, kind in CARDS:
    cy = room.LINE_Y - ch / 2 - 0.01
    mv = [(t1, 0.55, (x, cy + 3.5, CZ), "in")]
    w.card(oid, (x, cy, CZ), w=cw, h=ch, text=title, sub=sub, size=118, ink=GESSO, key="#ffd98a", flat=True, t=t0, move=mv, **STYLE[kind])
    for s in (-1, 1):                                                                                  # two pegs on the line, they come and go with the card
        w.solid(oid + "_p%d" % s, "box", (x + s * cw * 0.32, room.LINE_Y - 0.01, CZ + 0.012), (0.022, 0.06, 0.02), color="#c9a46a", rough=0.7, t=t0,
                move=[(t1, 0.55, (x + s * cw * 0.32, room.LINE_Y - 0.01 + 3.5, CZ + 0.012), "in")])

# ---- the INVERSO band on the front valance of the awning (below the caption zone), on "...di menswear, INVERSO"
T_INV = at("inverso") - 0.2
T_INV_OUT = at("primo") - 0.5                                # it rolls away before the trouser (the brand is not open yet)...
T_INV2 = at("apro") - 0.2                                   # ...and comes back on "tra un anno APRO il brand"
BAND = (SX, 2.2, SZ + 0.69, 1.2, 0.17)
w.card("fascia", BAND[:3], w=BAND[3], h=BAND[4], img="img/fascia.png", flat=True, color="#000000", t=T_INV, move=[(T_INV_OUT, 0.55, (BAND[0], BAND[1] + 3.5, BAND[2]), "in")])
T_INV2_OUT = at("Fino")                                     # "fino ad allora c'è solo il documento": the band goes, the sign stays
w.card("fascia2", BAND[:3], w=BAND[3], h=BAND[4], img="img/fascia.png", flat=True, color="#000000", t=T_INV2, move=[(T_INV2_OUT, 0.55, (BAND[0], BAND[1] + 3.5, BAND[2]), "in")])

# ---- the trouser appears on the left pedestal (fade + 12 cm rise: it starts above the pedestal, nothing to cross)
T_TR = at("pantalone") - 0.35
w.glb("tr", TROUSER, fit=0.55, pos=(room.PED_L[0], Y + room.PED_H + 0.002, room.PED_L[1]), rot_y=0.0, double=True, t=T_TR)

# ---- NARRATOR on the counter, centre, from frame 0
PN = (SX, Y, SZ - 0.1)
NH = 0.55
w.glb("nar1", OMINO, fit=NH, pos=PN, rot_y=0.0, segs=[[0.0, DUR + 1.0, 0, 0.0, 1.0]], segFade=0.35, clipSpeed=1.0, bob=0, jaw=[60, JAW], jawGain=1.0, recv=False)

# ---- CAMERA
_calls = []


def C(t, d, pos, look, ease="glide"):
    _calls.append([t, d, pos, look, ease])


def _flush():
    _calls.sort(key=lambda c: c[0])
    for i, (t, d, pos, look, ease) in enumerate(_calls):
        assert abs(pos[0] - look[0]) < 1e-6, "camera off axis at %.2f" % t
        assert 0 <= look[1] - pos[1] <= 0.12 + 1e-6, "camera not level at %.2f" % t
        assert d >= 1.1 or ease == "hand", "move too fast at %.2f" % t
        nxt = _calls[i + 1][0] if i + 1 < len(_calls) else 1e9
        assert t + d <= nxt - 0.02, "camera move at %.2f overlaps the next (%.2f)" % (t, nxt)
        w.cam(pos, look, t=t, d=d, ease=ease)


def wide(dist, yc):                                         # frontal, level, centred on the stall
    return (SX, yc, SZ + dist), (SX, yc, SZ)


def close(x=SX):                                            # narrator close-up, SOP numbers: camera 0.62h, look 0.80h, distance 1.2h... widened to 1.5h so the hands stay in frame
    return (x, Y + 0.62 * NH, PN[2] + 1.5 * NH), (x, Y + 0.80 * NH, PN[2])


def trouser(dist, yc=1.62):                                  # pedestal + trouser + its card all inside the frame, card below the captions (solved numerically)
    px, pz = room.PED_L
    return (px, yc, pz + dist), (px, yc, pz)


w.cam(*wide(10.5, 1.45))                                                    # frame 0: the whole stall, the empty counter, the sign, him
C(0.3, 1.3, *wide(4.6, 1.45))                                               # fast push to the stall
C(at("Sono") - 0.35, 1.2, *close())                                         # "sono uno studente": close on him
C(at("studente") + 0.3, 1.2, *wide(3.2, 1.55))                              # back to medium: the card "Economia + Moda" above him
C(at("menswear") - 0.4, 1.2, *wide(4.4, 1.7))                               # a step back: the INVERSO band lands on the awning
C(at("primo") - 0.3, 1.3, *trouser(2.5))                                    # truck left onto the pedestal: the trouser appears
C(at("disegnato") - 0.1, 3.0, *trouser(2.3), ease="hand")                 # slow push while he says how it was made
C(T_OGNI - 0.5, 1.2, *wide(3.9, 1.55))                                      # back to centre: the three fact cards
C(at("Lo", 1, T_OGNI) + 0.1, 1.2, *wide(3.0, 1.5))                          # "lo provo davanti a te": closer
C(at("laboratorio") - 0.45, 1.1, *close())                                  # "il laboratorio, prima del brand": close-up
C(at("Tra") - 0.25, 1.3, *wide(5.0, 1.6))                                   # "tra un anno apro il brand": the whole stall
C(at("Fino") + 0.2, 1.8, *wide(4.0, 1.2), ease="hand")                     # push to the sign: «IN VENDITA» -> «IN CORSO» on "documento"
C(at("Seguimi") - 0.15, 1.2, *close())                               # the CTA: him, the cards, the band
C(end("provi") + 0.1, 1.9, *wide(5.6, 1.5), ease="hand")                    # slow pull back to the end
_flush()


def _layout_check():                                        # every card / the band, at the start and end of every hold: inside the frame and below the captions
    tn = math.tan(math.radians(21)); bad = []
    cams = sorted(_calls, key=lambda c: c[0])
    things = [(c[0], c[1], c[2] - c[2] / 2 if False else room.LINE_Y - 0.01, room.LINE_Y - 0.01 - c[3], c[2], c[4], c[5]) for c in []]
    items = [(oid, x, cw, room.LINE_Y - 0.01, room.LINE_Y - 0.01 - ch, t0 + 0.6, t1) for oid, x, cw, ch, t0, t1, *_ in CARDS]
    for oid, ti, to in (("fascia", T_INV + 0.6, T_INV_OUT), ("fascia2", T_INV2 + 0.6, T_INV2_OUT)):
        items.append((oid, BAND[0], BAND[3], BAND[1] + BAND[4] / 2, BAND[1] - BAND[4] / 2, ti, to))
    for i, (t, d, pos, look, _) in enumerate(cams):
        t_a, t_b = t + d, (cams[i + 1][0] if i + 1 < len(cams) else DUR)
        for tt in (t_a, t_b):
            for oid, x, cw, ytop, ybot, ti, to in items:
                if not (ti <= tt < to): continue
                z = BAND[2] if oid.startswith("fascia") else CZ
                dd = pos[2] - z; hh = tn * dd; ww = hh * 1080 / 1920
                top = 960 - (ytop - pos[1]) / hh * 960; bot = 960 - (ybot - pos[1]) / hh * 960
                lx = 540 + (x - cw / 2 - pos[0]) / ww * 540; rx = 540 + (x + cw / 2 - pos[0]) / ww * 540
                if bot < 0 or top > 1920 or rx < 0 or lx > 1080: continue      # out of frame entirely: fine (e.g. above a close-up)
                if oid.startswith("fascia"):                                     # the band is scenery: it may be cropped, but never under the text on screen
                    z0, z1 = (60, 270) if tt >= T_ENDW else (100, 430)
                    if bot > z0 and top < z1 and rx > 100 and lx < 980: bad.append("%.2f %s top=%d bot=%d" % (tt, oid, top, bot))
                elif top < 430 or lx < 30 or rx > 1050: bad.append("%.2f %s top=%d x=%d..%d" % (tt, oid, top, lx, rx))
    assert not bad, "layout: " + "; ".join(bad)


T_ENDW = at("Seguimi") - 0.05
_layout_check()
w.dof(0.0, DUR, aperture=0.002)

# ---- pill (a fixed truth: nothing on sale; it changes only with the sign) + text on screen
PILL = [(at("Sono") - 0.1, "in vendita: <i>0</i>"), (T_FLIP, "in vendita: <i>0</i> · in corso: <i>tutto</i>")]
nm = lambda t: t.lower().strip(".,:?!«»")
KEY = {"venderti", "corso", "brand", "studente", "inverso", "pantalone", "errori", "documento", "laboratorio", "anno", "commenti", "provi", "niente", "menswear", "ai", "economia", "moda", "strumento", "costo", "errore"}
chunks, cur = [], []
for i, x in enumerate(WORDS):
    cur.append(x)
    brk = x["w"].endswith((".", ":", "?", "!", ",", "»")) or len(cur) >= 3 or sum(len(c["w"]) for c in cur) > 17
    if brk or i == len(WORDS) - 1:
        nxt = WORDS[i + 1]["s"] if i + 1 < len(WORDS) else cur[-1]["e"] + 1.0
        txt = " ".join(c["w"] for c in cur)
        for c in cur:
            if nm(c["w"]) in KEY:
                bb = c["w"].rstrip(".,:!?»"); txt = txt.replace(c["w"], "*" + bb + "*" + c["w"][len(bb):], 1); break
        chunks.append((cur[0]["s"], min(nxt - 0.02, cur[-1]["e"] + 0.45), txt.rstrip(".,:")))
        cur = []
T_HOOK_END = at("Sono") - 0.1
T_ENDW = at("Seguimi") - 0.05
w.big(-0.3, T_HOOK_END, "Non ho niente|da *venderti*", top=70, size=100)
w.big(T_ENDW, DUR, "Cosa vuoi che *provi*?|scrivilo nei *commenti*", top=70, size=70)
chunks = [c for c in chunks if not (c[0] < T_HOOK_END or c[0] >= T_ENDW)]
w.captions(chunks, top=250, size=92)


def _extra(path):
    p = open(path, encoding="utf-8").read()
    css = ("<style>#cost{position:absolute;left:0;right:0;top:118px;text-align:center;opacity:0;pointer-events:none;z-index:60}"
           "#cost span{display:inline-block;padding:16px 32px;border-radius:999px;background:rgba(22,18,14,.72);color:#fbf7ee;font:600 40px/1.1 Inter,'Segoe UI',sans-serif;letter-spacing:-.01em}"
           "#cost i{font-family:'Playfair Display',Georgia,serif;font-weight:500;color:#ffb48f;font-style:italic}</style></head>")
    js = ("<div id='cost'><span id='costv'></span></div>"
          "<script>(function(){var S=%s,OUT=%.3f;window.addEventListener('hf-seek',function(e){var t=e.detail.time,el=document.getElementById('cost'),v=document.getElementById('costv'),k=-1;"
          "for(var i=0;i<S.length;i++)if(t>=S[i][0])k=i;var a=k<0?0:Math.min(1,(t-S[0][0])/0.25,(OUT-t)/0.25);el.style.opacity=Math.max(0,a);"
          "if(k>=0&&v.innerHTML!==S[k][1]){v.innerHTML=S[k][1];}var p=k>=0?Math.min(1,(t-S[k][0])/0.2):1;el.style.transform='scale('+(1+0.12*Math.sin(Math.PI*p))+')';});})();</script></body>"
          ) % (json.dumps(PILL), T_ENDW - 0.1)
    open(path, "w", encoding="utf-8").write(p.replace("</head>", css, 1).replace("</body>", js, 1))


if __name__ == "__main__":
    out = os.path.join(HERE, "comp")
    print(World3D.page(out, [w], duration=DUR)); os.makedirs(os.path.join(out, "img"), exist_ok=True)
    shutil.copy(os.path.join(HERE, "img", "fascia.png"), os.path.join(out, "img", "fascia.png")); _extra(os.path.join(out, "index.html"))
    print("built, DUR", DUR)
