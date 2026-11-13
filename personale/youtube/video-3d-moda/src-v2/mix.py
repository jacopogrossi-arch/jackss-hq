# Audio mix of the v2 3D fashion video: voice on its chapters, music ducked under it, and a layer of earned sounds on every whip, label and chapter (retention).
import os, subprocess, sys
sys.argv = [sys.argv[0]]
import build as B
LIC = "D:/ClaudeCodeTest/.claude/skills/youtube-edit/assets"
VO, MUS = LIC + "/sfx/licensed/vo-edward-3d-moda.mp3", LIC + "/music/licensed/steall-waters.mp3"
S = lambda n: LIC + "/sfx/licensed/" + n + ".mp3"
at, DUR = B.at, B.DUR
whips = [11.8, 24.6, 38.9, 33.9, 35.3, 60.7, 63.2]
wh = ["es-whoosh-soft-airy", "es-whoosh-soft-clean", "es-swoosh-wide", "es-whoosh-generic-air", "es-swish-classic-filter", "whoosh-soft-hit", "es-whoosh-soft-resonant"]
cues = []                                                          # (file, video time, dB)
for i, t in enumerate(whips): cues.append((S(wh[i % len(wh)]), t - 0.12, -12 if t in (11.8, 24.6, 38.9) else -17))
for k, t in enumerate([at(19.3), at(20.4), at(21.5), at(24.8), at(30.6), at(31.6), at(32.5), at(38.5), at(42.9), at(46.6)]): cues.append((S("cc-tick" if k % 2 else "al-click"), t, -21))
for t in (13.6, 26.4, 40.35): cues.append((S("cc-riser-corto"), t - 1.5, -19))          # a riser that lands on each chapter's first word
cues += [(S("al-logo-incoming"), 0.2, -17), (S("al-snap"), 14.3, -13), (S("al-snap"), 15.1, -16), (S("cloth-feed"), 27.0, -11), (S("cloth-feed"), 41.9, -12), (S("es-zip-leather"), 50.2, -15),
         (S("cc-knock"), 37.7, -14), (S("es-pops6"), 22.3, -20), (S("cc-impact"), at(65.6), -13), (S("al-logo-incoming"), at(65.6) - 0.1, -12), (S("cloth-feed"), 61.5, -14)]
inputs = ["-i", VO, "-i", MUS] + sum([["-i", f] for f, _, _ in cues], [])
fc = []
for i, ((a, b), s0) in enumerate(zip(B.CHUNKS, B.ABS)):
    ms = int(s0 * 1000)
    fc.append(f"[0:a]aformat=channel_layouts=stereo,atrim=start={a}:end={b + 0.15},asetpts=PTS-STARTPTS,afade=t=in:d=0.04,afade=t=out:st={b - a + 0.15 - 0.12:.2f}:d=0.12,adelay={ms}|{ms}[v{i}]")
fc.append("".join(f"[v{i}]" for i in range(len(B.CHUNKS))) + f"amix=inputs={len(B.CHUNKS)}:normalize=0,highpass=f=70,acompressor=threshold=-20dB:ratio=2.2:attack=15:release=160,volume=3dB,apad=whole_dur={DUR},atrim=0:{DUR},asplit=2[vo][vokey]")
fc.append(f"[1:a]aformat=channel_layouts=stereo,atrim=0:{DUR},asetpts=PTS-STARTPTS,afade=t=in:d=2,afade=t=out:st={DUR - 5}:d=5,volume=-5dB[m]")
fc.append("[m][vokey]sidechaincompress=threshold=0.012:ratio=6:attack=40:release=800:makeup=1[md]")
lab = []
for n, (f, t, g) in enumerate(cues):
    ms = int(max(0, t) * 1000)
    fc.append(f"[{n + 2}:a]aformat=channel_layouts=stereo,volume={g}dB,adelay={ms}|{ms},apad=whole_dur={DUR},atrim=0:{DUR}[s{n}]"); lab.append(f"[s{n}]")
fc.append(f"[vo][md]{''.join(lab)}amix=inputs={2 + len(cues)}:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11,atrim=0:{DUR}[out]")
os.makedirs(os.path.join(B.HERE, "renders"), exist_ok=True)
r = subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(fc), "-map", "[out]", "-ar", "48000", "-ac", "2", os.path.join(B.HERE, "renders", "mix.wav")], capture_output=True, text=True)
print(r.stderr[-1500:] or "mix ok (%d cues)" % len(cues))
