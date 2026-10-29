"""Taglia il pezzo di ogni inquadratura (log, alta qualita'), lo misura con grade-scan, accorda le clip con grade-match
e applica pellicola-oro con grade-apply. Riesegui dopo aver cambiato shots.json: rifa' solo le inquadrature cambiate.
uso: python -I prepara.py [--only 0008,0129]"""
import json, os, subprocess, sys, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
POCKET = os.path.join(HERE, "..", "pocket")
SK = os.path.join(HERE, "..", "..", "..", ".claude", "skills", "youtube-edit", "scripts")
W = os.path.join(HERE, "work", "shots")
cfg = json.load(open(os.path.join(HERE, "shots.json"), encoding="utf-8"))
only = sys.argv[sys.argv.index("--only") + 1].split(",") if "--only" in sys.argv else None
env = dict(os.environ, PYTHONUTF8="1")


def run(cmd, check=True):
    print(">", " ".join(os.path.basename(c) if i == 1 else c for i, c in enumerate(cmd))[:160], flush=True)
    return subprocess.run(cmd, check=check, env=env).returncode


def source(n, kind):
    d = os.path.join(POCKET, kind)
    return os.path.join(d, next(f for f in sorted(os.listdir(d)) if "_%s_" % n in f))


done, recut = [], set()
for i, s in enumerate(cfg["shots"]):
    n = s["id"]
    dur = cfg["cuts"][i + 1] - cfg["cuts"][i] + 0.4
    # "extra" (filters at the edit) and "nota" do not touch the graded file
    key = hashlib.md5(json.dumps([{k: v for k, v in s.items() if k not in ("extra", "nota", "stops")}, round(dur, 3)]).encode()).hexdigest()[:8]
    d = os.path.join(W, "%02d-%s" % (i + 1, n))
    os.makedirs(d, exist_ok=True)
    raw, scan, graded = os.path.join(d, "log.mov"), os.path.join(d, "scan"), os.path.join(d, "grade")
    stamp = os.path.join(d, "key.txt")
    fresh = os.path.exists(stamp) and open(stamp).read() == key
    if (only is None or n in only) and not fresh:
        run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", str(s["start"]), "-i", source(n, s["src"]), "-t", "%.3f" % dur,
             "-map", "0:v:0", "-an", "-c:v", "prores_ks", "-profile:v", "3", "-pix_fmt", "yuv422p10le", raw])
        run([sys.executable, os.path.join(SK, "grade-scan.py"), "--video", raw, "--out", scan, "--profile", s["profile"]])
        open(stamp, "w").write(key)
        recut.add(n)
    done.append((i, n, d, raw, scan, graded))

match = os.path.join(W, "match")
run([sys.executable, os.path.join(SK, "grade-match.py"), "--out", match] +
    sum([["--clip", "%s=%s" % (raw, os.path.join(scan, "report.json"))] for _, _, _, raw, scan, _ in done], []))
for i, n, d, raw, scan, graded in done:
    if n in recut or (only and n in only) or not os.path.exists(os.path.join(graded, "graded.mp4")):
        rc = run([sys.executable, os.path.join(SK, "grade-apply.py"), "--video", raw, "--scan", os.path.join(scan, "report.json"),
             "--out", graded, "--match", os.path.join(match, "match.json"), "--look", "pellicola-oro", "--smooth", str(cfg["shots"][i].get("smooth", 1)),
             "--render", "--encoder", "nvenc"]
                 + (["--stops", str(cfg["shots"][i]["stops"])] if "stops" in cfg["shots"][i] else []), check=False)
        if rc:  # the check after the render failed (e.g. preview vs file on fast water): the file exists, look at it
            print("ATTENZIONE: controllo fallito su", n, flush=True)
print("ok", len(done), "inquadrature")
