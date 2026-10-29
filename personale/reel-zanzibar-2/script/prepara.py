"""Taglia il pezzo di ogni inquadratura (log, ProRes), lo misura con grade-scan, accorda le clip del Pocket con grade-match
e applica pellicola-oro con grade-apply. Come prepara.py del primo reel, piu' la Nano: le clip del 23/10 non sono in log,
quindi passano da una LUT neutra (identita.cube) con esposizione 0 e restano fuori dal match.
Riesegui dopo aver cambiato shots.json: rifa' solo le inquadrature cambiate.
uso: python -I prepara.py [--only 0128,0191]"""
import csv, json, os, subprocess, sys, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
SK = os.path.join(HERE, "..", "..", "..", ".claude", "skills", "youtube-edit", "scripts")
SM = os.path.join(HERE, "..", "..", "..", "personale", "reel-zanzibar", "smistamento")
W = os.path.join(HERE, "work", "shots")
IDENT = os.path.join(HERE, "work", "colore", "identita.cube")
cfg = json.load(open(os.path.join(HERE, "shots.json"), encoding="utf-8"))
only = sys.argv[sys.argv.index("--only") + 1].split(",") if "--only" in sys.argv else None
env = dict(os.environ, PYTHONUTF8="1")
inv = {c: {r["id"].split("_")[2]: r for r in csv.DictReader(open(os.path.join(SM, f), encoding="utf-8"))}
       for c, f in (("p", "inventario-pocket.csv"), ("n", "inventario-nano.csv"))}


def run(cmd, check=True):
    print(">", " ".join(os.path.basename(c) if i == 1 else c for i, c in enumerate(cmd))[:160], flush=True)
    return subprocess.run(cmd, check=check, env=env).returncode


def profile(s):
    row = inv[s["cam"]][s["id"]]
    if s["cam"] == "p":
        return {"D-Log": "dlog", "D-Log2": "dlog2"}[row["gamma"]]
    return None if row["giorno"] == "23/10" else "dlogm"


def source(s):
    d = os.path.join(HERE, "..", "pocket" if s["cam"] == "p" else "nano", "mp4")
    return os.path.join(d, next(f for f in sorted(os.listdir(d)) if "_%s_" % s["id"] in f))


done, recut = [], set()
for i, s in enumerate(cfg["shots"]):
    n, prof = s["id"], profile(s)
    dur = cfg["cuts"][i + 1] - cfg["cuts"][i] + 0.4
    key = hashlib.md5(json.dumps([{k: v for k, v in s.items() if k not in ("cosa", "nota", "stops")}, round(dur, 3)]).encode()).hexdigest()[:8]
    d = os.path.join(W, "%02d-%s" % (i + 1, n))
    os.makedirs(d, exist_ok=True)
    # nome del file unico per clip: grade-match indicizza per nome (bug del 28/10, quando tutte si chiamavano log.mov)
    raw, scan, graded = os.path.join(d, "log-%s.mov" % n), os.path.join(d, "scan"), os.path.join(d, "grade")
    stamp = os.path.join(d, "key.txt")
    fresh = os.path.exists(stamp) and open(stamp).read() == key
    if (only is None or n in only) and not fresh:
        run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", str(s["start"]), "-i", source(s), "-t", "%.3f" % dur,
             "-map", "0:v:0", "-an", "-vf", "fps=25", "-c:v", "prores_ks", "-profile:v", "3", "-pix_fmt", "yuv422p10le", raw])
        run([sys.executable, os.path.join(SK, "grade-scan.py"), "--video", raw, "--out", scan, "--profile", prof or "dlogm"])
        open(stamp, "w").write(key)
        recut.add(n)
    done.append((i, s, prof, d, raw, scan, graded))

match = os.path.join(W, "match")
run([sys.executable, os.path.join(SK, "grade-match.py"), "--out", match] +
    sum([["--clip", "%s=%s" % (raw, os.path.join(scan, "report.json"))] for _, _, prof, _, raw, scan, _ in done if prof], []))
for i, s, prof, d, raw, scan, graded in done:
    n = s["id"]
    if n in recut or (only and n in only) or not os.path.exists(os.path.join(graded, "graded.mp4")):
        extra = ["--log-cube", IDENT, "--stops", "0"] if prof is None else ["--match", os.path.join(match, "match.json")]
        if "stops" in s:
            extra += ["--stops", str(s["stops"])]
        rc = run([sys.executable, os.path.join(SK, "grade-apply.py"), "--video", raw, "--scan", os.path.join(scan, "report.json"),
                  "--out", graded, "--look", "pellicola-oro", "--smooth", str(s.get("smooth", 0)), "--render", "--encoder", "nvenc"] + extra, check=False)
        if rc:
            print("ATTENZIONE: controllo fallito su", n, flush=True)
print("ok", len(done), "inquadrature")
