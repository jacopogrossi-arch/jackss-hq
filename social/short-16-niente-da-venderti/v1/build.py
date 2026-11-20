# Short #16 «Non ho niente da venderti» (20/11/2026): market square at dawn. An empty stall; the narrator (toy figure of Jacopo) stands on the counter. Same engine/pipeline as Short «sconosciuti».
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
TOP = room.TOP
Y = TOP + 0.06                                              # surface of the counter top

# ---- the sign on the front of the counter: «IN VENDITA» is turned over -> «IN CORSO»
T_FLIP = at("corso") - 0.15
SIGNP = (SX, 0.42, SZ + 0.58)
w.card("sign_a", SIGNP, w=1.5, h=0.5, text="*IN VENDITA*", size=120, color="#16120f", ink=GESSO, key="#ff8a5c", flat=True,
       move=[(T_FLIP, 0.01, (SIGNP[0], -8.0, SIGNP[2]), "linear")])
w.card("sign_b", (SIGNP[0], -8.0, SIGNP[2]), w=1.5, h=0.5, text="*IN CORSO*", size=120, color=GESSO, ink="#16120f", key=RUGGINE, flat=True,
       move=[(T_FLIP, 0.35, SIGNP, "out")])

# ---- what appears on the counter, one thing at a time, on the word that names it
T_COL, T_TR, T_ERR, T_CST = at("costruendo") - 0.1, at("pantalone") - 0.2, at("errori") - 0.2, at("costo") - 0.3


def pop_card(oid, pos, t, **kw):
    x, y, z = pos
    w.card(oid, (x, -8.0, z), move=[(t, 0.35, pos, "out")], **kw)


for i, c in enumerate((BOSCO, GESSO, RUGGINE, SABBIA)):                                 # colour swatches (moodboard), left
    p = (SX - 1.35 + i * 0.22, Y + 0.14, SZ + 0.28)
    w.solid("sw%d" % i, "box", (p[0], -8.0, p[2]), (0.18, 0.28, 0.03), color=c, rough=0.8, move=[(T_COL + 0.08 * i, 0.35, p, "out")])
pop_card("c_col", (SX - 1.1, Y + 0.95, SZ + 0.18), T_COL + 0.35, w=0.8, h=0.3, text="i *colori*", size=72, color="#16120f", ink=GESSO, key="#d9b36a", flat=True)
w.glb("tr", TROUSER, fit=0.55, pos=(SX - 0.55, -8.0, SZ + 0.3), rot_y=0.15, double=True, move=[(T_TR, 0.4, (SX - 0.55, Y, SZ + 0.3), "out")])   # the toy trouser, Drop 1
pop_card("c_tr", (SX - 0.55, Y + 1.05, SZ + 0.2), T_TR + 0.35, w=0.8, h=0.3, text="*Drop 1*", size=72, color="#16120f", ink=GESSO, key="#d9b36a", flat=True)
nb = (SX + 0.55, Y + 0.02, SZ + 0.3)                                                    # the notebook (the errors)
w.solid("nb", "box", (nb[0], -8.0, nb[2]), (0.42, 0.04, 0.3), color="#e8dfc9", rough=0.8, rot_y=-0.3, move=[(T_ERR, 0.35, nb, "out")])
w.solid("nbc", "box", (nb[0] - 0.19, -8.0, nb[2]), (0.04, 0.045, 0.3), color=RUGGINE, rough=0.8, rot_y=-0.3, move=[(T_ERR, 0.35, (nb[0] - 0.19, nb[1], nb[2]), "out")])
pop_card("c_err", (SX + 0.65, Y + 1.0, SZ + 0.2), T_ERR + 0.35, w=0.9, h=0.3, text="gli *errori*", size=72, color="#16120f", ink=GESSO, key="#ff8a5c", flat=True)
pop_card("c_cst", (SX + 1.3, Y + 0.42, SZ + 0.3), T_CST, w=0.7, h=0.6, text="i *costi*", sub="tutti veri", size=80, color=GESSO, ink="#16120f", key=RUGGINE, flat=True)

# ---- the end sign: INVERSO drops onto the awning at "Tra un anno apro il brand", flips on "documento"
T_SIGN = at("Tra") - 0.2
ENDS = (SX, 2.78, SZ + 0.4)
w.prop("logosign", "totem", (ENDS[0], -6.0, ENDS[2]), (1.0, 0.31), rot_y=0.0, height=0.7, flips=[[at("documento", 2) + 0.1, 1.1, PI]],
       move=[(T_SIGN, 0.01, (ENDS[0], 3.6, ENDS[2]), "linear"), (T_SIGN + 0.02, 0.55, ENDS, "in")])


# ---- NARRATOR on the counter, centre-back
def me(oid, pos, t0, t1, rot=0.0, height=0.55):
    x, y, z = pos
    w.glb(oid, OMINO, fit=height, pos=(x, -8.0, z), rot_y=rot, segs=[[0.0, DUR + 1.0, 0, 0.0, 1.0]], segFade=0.35, clipSpeed=1.0, bob=0, jaw=[60, JAW], jawGain=1.0, recv=False,
          move=[(t0, 0.35, pos, "out"), (t1, 0.01, (x, -8.0, z), "linear")])


_calls = []


def C(t, d, pos, look, ease="hand"):
    _calls.append([t, d, pos, look, ease])


def _flush():
    _calls.sort(key=lambda c: c[0])
    for i, c in enumerate(_calls):
        t, d, pos, look, ease = c
        nxt = _calls[i + 1][0] if i + 1 < len(_calls) else 1e9
        dd = min(d, nxt - t - 0.02)
        if dd < 0.25:
            print("  cam skipped %.2f (no room)" % t); continue
        if dd < d - 0.01: print("  cam trim %.2f: %.2f -> %.2f" % (t, d, dd))
        w.cam(pos, look, t=t, d=dd, ease=ease)


T_ENDW = at("Seguimi") - 0.05
PN = (SX, Y, SZ - 0.15)                                       # narrator spot on the counter
me("nar1", PN, 0.4, DUR + 1.0, rot=0.0, height=0.55)
LK = (SX, Y + 0.3, SZ)
w.cam((0.0, 2.4, 13.0), (0.0, 1.0, -2.0))                                                     # starts FAR on the whole square ...
C(0.35, 0.95, (0.0, 1.35, 3.3), (0.0, 0.7, SZ), "glide")                                      # ... fast zoom onto the stall: the empty counter with the sign
C(at("corso") - 1.1, 1.2, (0.0, 1.15, 2.1), (SX, 0.7, SZ + 0.3), "glide")                      # the sign, as it is turned over
C(at("Sono") - 0.2, 1.2, (SX + 0.1, Y + 0.4, SZ + 1.1), LK, "glide")                           # close on the narrator: "sono uno studente"
C(at("Economia") + 0.3, 3.0, (SX + 0.5, Y + 0.45, SZ + 1.35), LK, "hand")
C(T_COL - 0.5, 1.0, (SX - 0.8, Y + 0.6, SZ + 1.8), (SX - 1.0, Y + 0.3, SZ + 0.2), "glide")   # the colours
C(T_TR - 0.7, 1.0, (SX - 0.1, Y + 0.7, SZ + 1.5), (SX - 0.55, Y + 0.35, SZ + 0.3), "glide")     # the trouser, macro push
C(T_TR + 0.9, 1.6, (SX - 0.4, Y + 0.6, SZ + 1.05), (SX - 0.55, Y + 0.32, SZ + 0.3), "hand")
C(T_ERR - 0.7, 1.1, (SX + 1.0, Y + 0.65, SZ + 1.7), (SX + 0.35, Y + 0.3, SZ), "glide")      # the notebook
C(at("Ogni") - 0.3, 1.4, (3.4, 1.7, SZ + 2.4), (SX, 0.9, SZ), "glide")                          # side orbit: all the documents at once
C(at("Lo", 1, at("Ogni")), 3.2, (2.2, 1.5, SZ + 3.4), (SX, 0.95, SZ), "hand")
C(at("Il", 2) - 0.4, 1.0, (SX - 0.1, Y + 0.4, SZ + 1.2), LK, "glide")
C(at("Il", 2) + 1.1, 1.8, (SX - 0.05, Y + 0.38, SZ + 0.95), LK, "hand")                           # "il laboratorio, prima del brand": close on him
C(T_SIGN - 0.3, 1.6, (0.0, 2.0, 9.5), (0.0, 2.1, SZ), "glide")                                   # the end card: the whole stall with the new sign
C(T_SIGN + 1.9, 2.0, (0.0, 1.8, 6.6), (0.0, 2.1, SZ), "hand")
C(T_ENDW - 0.1, 1.2, (SX + 0.1, Y + 0.5, SZ + 1.9), LK, "glide")                              # "seguimi, e dimmi nei commenti": close on him
C(end("commenti") + 0.2, 2.2, (0.0, 1.9, 8.2), (0.0, 2.0, SZ), "glide")                         # pull back to the whole stall
_flush()
w.dof(0.0, DUR, aperture=0.003)

# ---- counter pill (follows the PHASE) + text on screen
PILL = [(at("Sono") - 0.1, "in vendita <i>0</i> · documentato <i>0</i>")]
for k, tt in enumerate((T_COL, T_TR, T_ERR, T_CST)):
    PILL.append((tt, "in vendita <i>0</i> · documentato <i>%d</i>" % (k + 1)))
nm = lambda t: t.lower().strip(".,:?!«»")
KEY = {"venderti", "corso", "brand", "studente", "inverso", "pantalone", "errori", "documento", "laboratorio", "anno", "commenti", "provi", "niente", "menswear", "ai"}
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
w.big(-0.3, T_HOOK_END, "Non ho niente|da *venderti*", top=70, size=100)
w.big(T_ENDW, DUR, "Cosa vuoi che *provi*?|scrivilo nei *commenti*", top=60, size=70)
chunks = [c for c in chunks if not (c[0] < T_HOOK_END or c[0] >= T_ENDW)]
w.captions(chunks, top=340, size=96)


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
    print(World3D.page(out, [w], duration=DUR)); os.makedirs(os.path.join(out, "img"), exist_ok=True); _extra(os.path.join(out, "index.html"))
    print("built, DUR", DUR)
