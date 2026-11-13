# Audio mix of the 3D fashion video: voice chunks on their chapters, music ducked under the voice, a few earned sounds on the wipes.
import os, subprocess, sys
sys.argv = [sys.argv[0]]
import build as B
LIC = "D:/ClaudeCodeTest/.claude/skills/youtube-edit/assets"
VO, MUS = LIC + "/sfx/licensed/vo-edward-3d-moda.mp3", LIC + "/music/licensed/steall-waters.mp3"
S1, S2, S3 = LIC + "/sfx/licensed/whoosh-soft-airy.mp3", LIC + "/sfx/licensed/whoosh-soft-hit.mp3", LIC + "/sfx/licensed/cloth-feed.mp3"
DUR = B.DUR
at = B.at
# (file index, video time of the sound's start, gain dB)
SFX = [(2, at(10.0) - 0.55, -13), (3, at(23.0) - 1.05, -12), (2, at(37.06) - 1.05, -11),
       (4, at(60.5) - 0.1, -10), (4, at(61.32) - 0.1, -10), (2, 72.1, -15)]
fc = []
for i, ((a, b), s0) in enumerate(zip(B.CHUNKS, B.ABS)):
    ms = int(s0 * 1000)
    fc.append(f"[0:a]aformat=channel_layouts=stereo,atrim=start={a}:end={b + 0.15},asetpts=PTS-STARTPTS,afade=t=in:d=0.04,afade=t=out:st={b - a + 0.15 - 0.12:.2f}:d=0.12,adelay={ms}|{ms}[v{i}]")
fc.append("".join(f"[v{i}]" for i in range(len(B.CHUNKS))) + f"amix=inputs={len(B.CHUNKS)}:normalize=0,highpass=f=70,acompressor=threshold=-20dB:ratio=2.2:attack=15:release=160,volume=3dB,apad=whole_dur={DUR},atrim=0:{DUR},asplit=2[vo][vokey]")
fc.append(f"[1:a]aformat=channel_layouts=stereo,atrim=0:{DUR},asetpts=PTS-STARTPTS,afade=t=in:d=3,afade=t=out:st={DUR - 6}:d=6,volume=-6dB[m]")
fc.append("[m][vokey]sidechaincompress=threshold=0.012:ratio=7:attack=40:release=900:makeup=1[md]")
sfx_labels = []
for n, (idx, t, g) in enumerate(SFX):
    ms = int(max(0, t) * 1000)
    fc.append(f"[{idx}:a]aformat=channel_layouts=stereo,volume={g}dB,adelay={ms}|{ms},apad=whole_dur={DUR},atrim=0:{DUR}[s{n}]")
    sfx_labels.append(f"[s{n}]")
fc.append(f"[vo][md]{''.join(sfx_labels)}amix=inputs={2 + len(SFX)}:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11,atrim=0:{DUR}[out]")
cmd = ["ffmpeg", "-v", "error", "-y", "-i", VO, "-i", MUS, "-i", S1, "-i", S2, "-i", S3, "-filter_complex", ";".join(fc), "-map", "[out]", "-ar", "48000", "-ac", "2", os.path.join(B.HERE, "renders", "mix.wav")]
r = subprocess.run(cmd, capture_output=True, text=True)
print(r.stderr[-1500:] or "mix ok")
