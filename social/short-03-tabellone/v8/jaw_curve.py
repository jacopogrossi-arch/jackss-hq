"""Mouth opening (0..1, 60 fps) from the voice itself: loudness of the audio in short windows (syllables: loud vowels open, quiet consonants close),
gated by the word timings (closed between words), attack 25 ms / release 70 ms, 2 frames of lead (a mouth that lags reads as dubbed).
Usage: python jaw_curve.py voice.mp3 words.json out.json"""
import json, subprocess, sys, numpy as np
voice, words, out = sys.argv[1:4]
FPS = 60
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", voice, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True).stdout
x = np.frombuffer(raw, dtype="<f4"); n = int(len(x) / 16000 * FPS) + 1
win = 400                                                     # 25 ms
rms = np.array([np.sqrt(np.mean(x[max(0, int(i / FPS * 16000 - win // 2)):int(i / FPS * 16000 + win // 2)] ** 2) + 1e-9) for i in range(n)])
db = 20 * np.log10(rms + 1e-6)
W = json.load(open(words))
gate = np.zeros(n)
for w in W:
    a, b = int(max(0, (w["s"] - 0.03) * FPS)), int(min(n - 1, (w["e"] + 0.04) * FPS))
    gate[a:b + 1] = 1.0
vals = db[gate > 0]; lo, hi = np.percentile(vals, 30), np.percentile(vals, 98)
o = np.clip((db - lo) / (hi - lo), 0, 1) ** 1.1
o = np.where(gate > 0, np.maximum(o, 0.14), 0.0)             # lips part whenever he speaks, closed between words
# attack / release
y = np.zeros(n); ka, kr = 1 - np.exp(-1 / (FPS * 0.025)), 1 - np.exp(-1 / (FPS * 0.070))
for i in range(1, n):
    k = ka if o[i] > y[i - 1] else kr
    y[i] = y[i - 1] + k * (o[i] - y[i - 1])
y = np.concatenate([y[2:], [0, 0]])                           # lead 2 frames
json.dump([round(float(v), 3) for v in y], open(out, "w"))
print("frames", n, "mean open %.2f" % y[gate > 0].mean(), "max %.2f" % y.max())
