"""Animatic: ogni inquadratura di shots.json tagliata dall'originale, solo LUT (niente colore finale), cinemascope 2,39:1 in 1280x720,
numero dell'inquadratura nella barra nera, musica vera. Serve a sentire il ritmo e vedere la storia.
uso: python -I animatic.py   -> animatic.mp4"""
import csv, json, os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
Z = os.path.join(HERE, "..")
LUTS = os.path.join(HERE, "..", "..", "..", ".claude", "skills", "youtube-edit", "assets", "luts")
SM = os.path.join(HERE, "..", "..", "..", "personale", "reel-zanzibar", "smistamento")
LUT = {"D-Log": "DJI-Pocket4P-DLog-to-Rec709-V2.0-size33.cube", "D-Log2": "DJI-Pocket4P-DLog2-to-Rec709-size65.cube",
       "D-Log M": "DJI-OsmoNano-DLogM-to-Rec709-V1.cube"}
FONT = "fontfile='C\\:/Windows/Fonts/arial.ttf'"
W, H, SH = 1280, 720, 536  # 1280/2.39 = 536
inv = {c: {r["id"].split("_")[2]: r for r in csv.DictReader(open(os.path.join(SM, f), encoding="utf-8"))}
       for c, f in (("p", "inventario-pocket.csv"), ("n", "inventario-nano.csv"))}
cfg = json.load(open(os.path.join(HERE, "shots.json"), encoding="utf-8"))
tmp = os.path.join(HERE, "work", "animatic")
os.makedirs(tmp, exist_ok=True)
parts = []
for i, s in enumerate(cfg["shots"]):
    cam, n = s["cam"], s["id"]
    row = inv[cam][n]
    prof = row["gamma"] if cam == "p" else (None if row["giorno"] == "23/10" else "D-Log M")
    d = os.path.join(Z, "pocket" if cam == "p" else "nano", "mp4")
    src = os.path.join(d, next(x for x in sorted(os.listdir(d)) if "_%s_" % n in x))
    # durata esatta in fotogrammi a 25 fps, cosi' gli stacchi cadono dove dice shots.json
    f0, f1 = round(cfg["cuts"][i] * 25), round(cfg["cuts"][i + 1] * 25)
    vf = []
    if prof:
        vf.append("lut3d='%s'" % os.path.join(LUTS, LUT[prof]).replace("\\", "/").replace(":", "\\:"))
    vf += ["fps=25", "scale=%d:%d" % (W, H), "crop=%d:%d" % (W, SH), "pad=%d:%d:0:%d:black" % (W, H, (H - SH) // 2),
           "drawtext=%s:text='%d  %s %s':fontsize=22:fontcolor=white@0.55:x=20:y=h-50" % (FONT, i + 1, "Nano" if cam == "n" else "Pocket", n),
           "setsar=1", "format=yuv420p"]
    out = os.path.join(tmp, "%02d.mp4" % (i + 1))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(s["start"]), "-i", src, "-frames:v", str(f1 - f0), "-an", "-vf", ",".join(vf),
                    "-c:v", "libx264", "-crf", "20", "-preset", "fast", out], check=True)
    parts.append(out)
    print(i + 1, n, prof or "normale", f1 - f0, "fotogrammi", flush=True)
lst = os.path.join(tmp, "list.txt")
open(lst, "w").write("".join("file '%s'\n" % p.replace("\\", "/") for p in parts))
end = cfg["cuts"][-1]
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-i", os.path.join(HERE, "ref", "riferimento.wav"),
                "-map", "0:v", "-map", "1:a", "-vf", "fade=t=out:st=%.2f:d=1.2" % (end - 1.2), "-af", "afade=t=out:st=%.2f:d=1.3" % (end - 1.3),
                "-t", "%.3f" % end, "-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                "-movflags", "+faststart", os.path.join(HERE, "animatic.mp4")], check=True)
print("ok animatic.mp4", end, "s")
