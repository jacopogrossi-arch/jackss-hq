# Audio of the Short: voice, music ducked under it, and a sound for every whip, label, chapter and the logo (retention). Needs vo.mp3 (the Epidemic voiceover, whole text in one file).
import os, subprocess, sys
sys.argv = [sys.argv[0]]
import build as B
LIC = "D:/ClaudeCodeTest/.claude/skills/youtube-edit/assets"
VO = os.path.join(B.HERE, "vo.mp3"); MUS = LIC + "/music/licensed/steall-waters.mp3"
S = lambda n: LIC + "/sfx/licensed/" + n + ".mp3"
at, DUR = B.at, B.DUR
cues = []
WH = ["es-whoosh-soft-airy", "es-whoosh-soft-clean", "es-swoosh-wide", "es-whoosh-generic-air", "es-swish-classic-filter", "whoosh-soft-hit", "es-whoosh-soft-resonant"]
whips = [t for (t, d, *_ ) in B.CAMS if d <= 1.3]
for i, t in enumerate(sorted(whips)): cues.append((S(WH[i % len(WH)]), t - 0.1, -13))
for k, (t) in enumerate(sorted(l["at"] for l in B.w.labels)): cues.append((S("cc-tick" if k % 2 else "al-click"), t, -20))
cues += [(S("al-logo-incoming"), 0.1, -17), (S("cc-impact"), at("gonna") - 0.05, -14),
         (S("al-snap"), at("cartamodello") + 0.5, -12), (S("al-snap"), at("verso") + 0.3, -14), (S("cloth-feed"), at("cuce"), -12), (S("cc-riser-corto"), at("centodiciassette") - 1.4, -16),
         (S("cc-impact"), at("centodiciassette") + 0.2, -13), (S("es-pops6"), at("meglio"), -17), (S("cloth-feed"), at("tessuto", 2), -13), (S("es-zip-leather"), at("regolatori", 2) + 0.1, -14),
         (S("es-whoosh-medium-transition"), at("Tutto") - 0.95, -12), (S("es-film-advance-wind"), at("Tutto") - 0.35, -15),
         (S("es-scissors-cut-paper"), at("cartamodello") + 0.1, -11), (S("es-scissors-cut-paper"), at("cartamodello") + 2.4, -12),
         (S("cc-impact"), at("inverso"), -12), (S("al-logo-incoming"), at("inverso") - 0.1, -13)]
inputs = ["-i", VO, "-i", MUS] + sum([["-i", f] for f, _, _ in cues], [])
fc = ["[0:a]aformat=channel_layouts=stereo,highpass=f=70,acompressor=threshold=-20dB:ratio=2.2:attack=15:release=160,volume=3dB,apad=whole_dur=%s,atrim=0:%s,asplit=2[vo][vokey]" % (DUR, DUR),
      "[1:a]aformat=channel_layouts=stereo,atrim=0:%s,asetpts=PTS-STARTPTS,afade=t=in:d=1.5,afade=t=out:st=%s:d=4,volume=-5dB[m]" % (DUR, DUR - 4),
      "[m][vokey]sidechaincompress=threshold=0.012:ratio=6:attack=40:release=800:makeup=1[md]"]
lab = []
for n, (f, t, g) in enumerate(cues):
    ms = int(max(0, t) * 1000)
    fc.append(f"[{n + 2}:a]aformat=channel_layouts=stereo,volume={g}dB,adelay={ms}|{ms},apad=whole_dur={DUR},atrim=0:{DUR}[s{n}]"); lab.append(f"[s{n}]")
fc.append(f"[vo][md]{''.join(lab)}amix=inputs={2 + len(cues)}:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11,atrim=0:{DUR}[out]")
os.makedirs(os.path.join(B.HERE, "renders"), exist_ok=True)
r = subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(fc), "-map", "[out]", "-ar", "48000", "-ac", "2", os.path.join(B.HERE, "renders", "mix.wav")], capture_output=True, text=True)
print(r.stderr[-1500:] or "mix ok (%d cues)" % len(cues))
