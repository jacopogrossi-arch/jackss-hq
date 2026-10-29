"""Versione del reel col look di Jacopo (Mimo): per ogni inquadratura
- se Jacopo ha un suo export di quella clip (videos/look-jacopo/coppie.json) si usa quello: e' il suo grading vero;
- altrimenti: pezzo log gia' tagliato da prepara.py -> LUT DJI ufficiale -> ricetta (look-jacopo-ricetta.cube) -> ritocchi
  per clip ("j_extra" in shots.json: filtri ffmpeg, es. "eq=saturation=1.1"). Le clip della Nano non in log saltano la LUT.
Niente grana, alone, vignetta, curva a S. Esce in work/shots-j/NN-id/graded.mp4.
uso: python -I prepara_jacopo.py [--only 0128,0075]"""
import csv, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
LJ = os.path.join(HERE, "..", "..", "look-jacopo")
LUTS = os.path.join(HERE, "..", "..", "..", ".claude", "skills", "youtube-edit", "assets", "luts")
SM = os.path.join(HERE, "..", "..", "..", "personale", "reel-zanzibar", "smistamento")
CUBE = {"D-Log": "DJI-Pocket4P-DLog-to-Rec709-V2.0-size33.cube", "D-Log2": "DJI-Pocket4P-DLog2-to-Rec709-size65.cube",
        "D-Log M": "DJI-OsmoNano-DLogM-to-Rec709-V1.cube"}
cfg = json.load(open(os.path.join(HERE, "shots.json"), encoding="utf-8"))
only = sys.argv[sys.argv.index("--only") + 1].split(",") if "--only" in sys.argv else None
inv = {c: {r["id"].split("_")[2]: r for r in csv.DictReader(open(os.path.join(SM, f), encoding="utf-8"))}
       for c, f in (("p", "inventario-pocket.csv"), ("n", "inventario-nano.csv"))}
exports = {m["clip"]: (e, m["offset"]) for e, m in json.load(open(os.path.join(LJ, "coppie.json"))).items()}
tmp = os.path.join(HERE, "work", "shots-j", "_lut")
os.makedirs(tmp, exist_ok=True)
# lut3d vuole nomi relativi su Windows (un "D:" nel percorso la rompe): copio le LUT accanto e lancio ffmpeg da li'
for k, f in CUBE.items():
    open(os.path.join(tmp, f), "wb").write(open(os.path.join(LUTS, f), "rb").read())
open(os.path.join(tmp, "ricetta.cube"), "wb").write(open(os.path.join(LJ, "look-jacopo-ricetta.cube"), "rb").read())

for i, s in enumerate(cfg["shots"]):
    n = s["id"]
    if only and n not in only:
        continue
    out_dir = os.path.join(HERE, "work", "shots-j", "%02d-%s" % (i + 1, n))
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "graded.mp4")
    dur = cfg["cuts"][i + 1] - cfg["cuts"][i] + 0.4
    extra = ("," + s["j_extra"]) if s.get("j_extra") else ""
    key = s["cam"] + n
    if key in exports and not s.get("j_ricetta"):
        e, off = exports[key]
        src, ss, vf, how = os.path.join(LJ, "export", e), s["start"] - off, "fps=25" + extra, "suo export Mimo"
    else:
        row = inv[s["cam"]][n]
        prof = row["gamma"] if s["cam"] == "p" else (None if row["giorno"] == "23/10" else "D-Log M")
        src, ss = os.path.join(HERE, "work", "shots", "%02d-%s" % (i + 1, n), "log-%s.mov" % n), 0
        vf = ("lut3d=file=%s:interp=tetrahedral,lut3d=file=ricetta.cube:interp=tetrahedral" % CUBE[prof]) if prof \
            else "eq=saturation=1.13:gamma=0.93"  # Nano non in log: i suoi ritocchi su 0190/0191 (-0,04 di luce, saturazione x1,13)
        vf += extra
        how = "ricetta" if prof else "Nano normale"
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", "%.3f" % ss, "-i", src, "-t", "%.3f" % dur, "-an",
                    "-vf", vf + ",format=yuv420p10le", "-c:v", "hevc_nvenc", "-preset", "p6", "-cq", "16", "-pix_fmt", "p010le",
                    "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", out], check=True, cwd=tmp)
    print(i + 1, n, how, flush=True)
print("ok")
