"""mix.py: video muto + voce/voce-pause.wav (voce ed effetti) + musica -> video finito.
La musica sta BED dB sotto la voce (misurata, non a occhio), si abbassa ancora sotto il parlato (sidechain),
poi tutto il file prende un guadagno FISSO fino a TARGET LUFS (niente loudnorm dinamico: alzava la musica nelle pause).
Uso: python mix.py <video muto> <uscita> <musica>"""
import subprocess, sys

BED, TARGET = 13.0, -16.0
src, out, music = sys.argv[1:4]
VOICE = "voce/voce-pause.wav"


def lufs(args):
    o = subprocess.run(["ffmpeg", "-v", "info"] + args + ["-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float([l for l in o.splitlines() if "I:" in l][-1].split("I:")[1].split()[0])


v = lufs(["-i", VOICE]); m = lufs(["-i", music])
gain = (v - BED) - m
fc = ("[1:a]aloop=loop=-1:size=2e9,asetpts=PTS-STARTPTS,volume=%.2fdB[bedraw];[bedraw]atrim=0:%.3f,afade=t=in:st=0:d=1.0,afade=t=out:st=%.3f:d=2.5[bed];"
      "[0:a]asplit=2[voice][sc];[bed][sc]sidechaincompress=threshold=0.05:ratio=3:attack=20:release=500[duck];"
      "[voice][duck]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[a]")
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", VOICE], capture_output=True, text=True).stdout)
fc = fc % (gain, dur, dur - 2.5)
tmp = out + ".pre.wav"
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", VOICE, "-i", music, "-filter_complex", fc, "-map", "[a]", "-ar", "48000", tmp], check=True)
g = TARGET - lufs(["-i", tmp])
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src, "-i", tmp, "-map", "0:v:0", "-map", "1:a", "-c:v", "copy", "-af", "volume=%.2fdB,alimiter=limit=0.89:level=disabled" % g,
                "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-shortest", "-movflags", "+faststart", out], check=True)
print("voce %.1f LUFS, musica %.1f -> %+.1f dB (%.0f dB sotto la voce), guadagno finale %+.1f dB" % (v, m, gain, BED, g))
