# Short "Ho chiesto a 6 sconosciuti quanto pagherebbero un pantalone fatto bene" (18/11/2026): a Rome street at night. Six comment cards hang from two lamp posts (conferme left, schiaffi right),
# a live counter, the toy trouser in the lit shop window, the narrator in the street. Same engine and pipeline as Short #11 (short-11-pantalone-3d/v1).
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
OMINO = os.environ.get("OMINO", "D:/ClaudeCodeTest/videos/_bench/short-sconosciuti/assets/narratore-perf-smooth.glb")
w = World3D("s", 0.0, DUR, fov=42, w=1080, h=1920, fade=0.4)
w.shutter(0.5)
GESSO, SABBIA, RUGGINE, BOSCO = "#EFE9DD", "#B9AE98", "#8A4B2D", "#2F3A2E"
room.furnish(w, trouser=TROUSER)
LP, RP = room.POLES                                           # (x, z) of the left (conferme) and right (schiaffi) lamp post

# ---- the six comment cards: a pair per beat; the card pops on the first word of its sentence and stays on its post
BEATS = [("conf", "prima", "conferma", "*~200 €*", "se gli sta perfetto"),
         ("schi", "primo", "schiaffo", "*65 $* vs 400", "compro solo quando costa poco"),
         ("conf", "seconda", "conferma", "*toccarlo* di persona", "online: quasi nessuno si fida"),
         ("schi", "secondo", "schiaffo", "*serve tempo*", "da un giovane senza nome: no"),
         ("conf", "terza", "conferma", "*pochi* ma buoni", "meglio che tanti"),
         ("schi", "terzo", "schiaffo", "*400 $* in teoria", "paura di rovinarli")]
YS = {"conf": [2.7, 2.15, 1.6], "schi": [2.7, 2.15, 1.6]}
cnt = {"conf": 0, "schi": 0}
T = []                                                        # [(t_start, side, t_key)] per beat, for the camera and the counter
for kind, w0, w1, text, sub in BEATS:
    ts = at(w0) - 0.05; tk = at(w1, 1, ts) + 0.05
    px, pz = LP if kind == "conf" else RP
    i = cnt[kind]; cnt[kind] += 1
    w.card("c_%s_%d" % (kind, i), (px, YS[kind][i], pz + 0.14), w=0.9, h=0.5, text=text, sub=sub, size=118, rot_y=0.12 if kind == "conf" else -0.12,
           color="#B9D2AA" if kind == "conf" else "#E4AC92", t=ts)
    T.append((ts, kind, tk))

# ---- the logo sign for the end card (drops in with "Tu quanto pagheresti", flips = INVERSO)
T_TU = at("tu", 1, 20.0) if any(x["s"] > 20 for x in WORDS) else at("tu")
ENDS = (-0.55, 0.12, -0.9)
T_SIGN = T_TU - 0.4
w.prop("logosign", "totem", (ENDS[0], -6.0, ENDS[2]), (1.0, 0.31), rot_y=0.0, height=0.78, flips=[[end("commenti") + 0.1, 1.1, PI]],
       move=[(T_SIGN, 0.01, (ENDS[0], 3.6, ENDS[2]), "linear"), (T_SIGN + 0.02, 0.55, ENDS, "in")])

# ---- NARRATOR (speech-driven performance + jaw) in the street between the two posts
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


PN = (0.5, 0.0, 0.5)                                          # narrator spot (in front of the sign, in the middle of the street)
T_HERO = at("erano") - 0.3                                    # "Non erano il mio cliente..." -> "...documento tutto"
E_HERO = end("tutto")
LOOK_L, LOOK_R = (LP[0], 2.45, LP[1]), (RP[0], 2.45, RP[1])
# hook: the lit shop window with the trouser, the camera drifts in, then it looks at the two posts ("ragione" -> left, "schiaffo" -> right)
w.cam((0.5, 1.2, 3.6), (0.5, 2.15, -4.6))
C(0.1, 2.6, (0.5, 1.15, 1.2), (0.5, 1.9, -4.6), "glide")
C(at("ragione") - 0.8, 1.1, (-0.5, 1.5, 3.2), LOOK_L, "glide")
C(at("schiaffo") - 0.6, 1.0, (1.8, 1.5, 3.2), LOOK_R, "glide")
for k, (ts, kind, tk) in enumerate(T):                       # per beat: dive to the post, then a slow push on the card
    look = LOOK_L if kind == "conf" else LOOK_R
    sx = -1 if kind == "conf" else 1
    C(ts - 0.1, 1.0, (look[0] + sx * 0.5, 1.9, 3.6), look, "glide")
    C(ts + 1.4, 2.4, (look[0] + sx * 0.2, 2.0, 2.8), (look[0], look[1] - 0.05, look[2]), "hand")
# narrator + the close-up on the moral
R4 = 0.0
me("nar1", PN, T[0][0] - 0.2, DUR + 1.0, rot=R4, height=0.55)
dd_ = 1.55 * 0.55
look0 = (PN[0], PN[1] + 0.33, PN[2])
C(T_HERO - 0.55, 0.45, (PN[0] + math.sin(R4) * dd_, PN[1] + 0.33, PN[2] + math.cos(R4) * dd_), look0, "glide")
C(T_HERO + 0.9, max(0.5, E_HERO - T_HERO - 1.1), (PN[0], PN[1] + 0.33, PN[2] + dd_ * 0.9), look0, "glide")
T_ENDW = at("tu", 1, T_HERO) - 0.3
C(T_ENDW, 1.8, (0.5, 1.9, 14.2), (0.5, 1.4, -0.5), "glide")                               # the end card: the street, the sign, him, the shop window
C(T_ENDW + 2.0, 2.4, (0.5, 1.8, 13.4), (0.5, 1.4, -0.5), "hand")
_flush()
w.dof(0.0, DUR, aperture=0.003)

# ---- counter (a pill that follows the PHASE) + text on screen
PILL, a, b = [], 0, 0
PILL.append((T[0][0] - 0.1, "conferme <i>0</i> · schiaffi <i>0</i>"))
for ts, kind, tk in T:
    if kind == "conf": a += 1
    else: b += 1
    PILL.append((tk, "conferme <i>%d</i> · schiaffi <i>%d</i>" % (a, b)))
nm = lambda t: t.lower().strip(".,:?!«»")
KEY = {"sconosciuti", "pantalone", "ragione", "schiaffo", "conferma", "vestibilità", "duecento", "fiducia", "toccare", "tempo", "reputazione", "pochi", "quattrocento", "rovinarli", "cliente", "venderti", "studente", "documento", "pagheresti", "commenti"}
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
T_HOOK_END = at("prima") - 0.1
w.big(-0.3, T_HOOK_END, "6 *sconosciuti*|quanto *pagherebbero*|un pantalone?", top=240, size=82)
w.big(T_ENDW, DUR, "Tu quanto *pagheresti*?|scrivilo nei *commenti*", top=215, size=72)
chunks = [c for c in chunks if not (c[0] < T_HOOK_END or c[0] >= T_ENDW - 0.05)]
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
    print(World3D.page(out, [w], duration=DUR)); _extra(os.path.join(out, "index.html"))
    print("built, DUR", DUR)
