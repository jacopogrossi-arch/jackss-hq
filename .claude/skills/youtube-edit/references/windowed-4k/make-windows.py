#!/usr/bin/env python3
"""make-windows.py: divide build/public in finestre di meno di 120 s (window-patch.py della skill), con i tagli fuori da ogni
grafica. Serve perche' HyperFrames 0.9.35 estrae i fotogrammi del video a blocchi di 120 s e su un 4K lungo cade al cambio di blocco:
con finestre piu' corte di 120 s l'estrazione e' sempre un blocco solo. Uscita: final-4k/wNN/public e final-4k/windows.json."""
import re, json, subprocess, sys, os
SK = "D:/ClaudeCodeTest/.claude/skills/youtube-edit"; D = 1261.24; N = 11; MAXW = 118.0
html = open("build/public/index.html", encoding="utf8").read()
iv = []
for m in re.finditer(r'<[a-z]+ [^>]*data-start="([0-9.]+)"[^>]*>', html):
    t = m.group(0)
    if 'id="stage"' in t or 'id="bg-video"' in t or t.startswith("<audio"): continue
    du = re.search(r'data-duration="([0-9.]+)"', t)
    if du: iv.append((float(m.group(1)), float(m.group(1)) + float(du.group(1))))
free = lambda x: all(not (a - 0.6 < x < b + 0.6) for a, b in iv)
cuts = [0.0]
for k in range(1, N):
    ideal = k * D / N; best = None
    for i in range(0, 400):
        for s in (1, -1):
            x = round((ideal + s * i * 0.04) * 25) / 25
            if free(x) and x - cuts[-1] <= MAXW and x > cuts[-1] + 60: best = x; break
        if best is not None: break
    if best is None: raise SystemExit("nessun taglio libero vicino a %.1f" % ideal)
    cuts.append(best)
cuts.append(D)
assert all(b - a <= MAXW + 1e-6 for a, b in zip(cuts, cuts[1:])), cuts
W = []
for i, (a, b) in enumerate(zip(cuts, cuts[1:])):
    out = "final-4k/w%02d" % i
    if not os.path.exists(out + "/public/index.html"):
        subprocess.run([sys.executable, SK + "/scripts/window-patch.py", "--public", "build/public", "--t0", "%.2f" % a, "--t1", "%.2f" % b, "--out", out, "--fps", "25"], check=True)
    W.append({"i": i, "t0": a, "t1": b, "frames50": round((b - a) * 50), "dir": out})
json.dump(W, open("final-4k/windows.json", "w"), indent=1)
print(len(iv), "elementi a tempo;", "tagli:", " ".join("%.2f" % c for c in cuts))
