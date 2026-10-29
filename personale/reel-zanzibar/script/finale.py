"""Montaggio finale: reel senza titolo (mh-video-editor) + apertura col titolo macchina da scrivere (titoli/anima.py)
+ una light leak leggerissima sul passaggio al tramonto + audio = musica + tasti + ambienti (onde / giungla / onde).
Scrive anche la versione SENZA musica (tasti + ambienti + leak) per usare la canzone dalla libreria di Instagram.
uso: python -I finale.py [--name zanzibar-reel_v5]"""
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
M = "C:/Users/Jacopo Grossi/.claude/skills/mh-video-editor-skill/engine/scripts/mh_video.py"
YE = os.path.join(HERE, "..", "..", "..", ".claude", "skills", "youtube-edit", "assets")
SON = "D:/download/Sonniss GDC 2026/"
K4 = "--4k" in sys.argv               # final: 3840x2160 (title from anima.py --4k)
NAME = sys.argv[sys.argv.index("--name") + 1] if "--name" in sys.argv else ("zanzibar-reel_4k" if K4 else "zanzibar-reel_v5")
TITLE = os.path.join(HERE, "titoli", "prova-4t-4k-muto.mp4" if K4 else "prova-4t-muto.mp4")       # 135 frames = 5,40 s, same graded clip 1
KEYS = os.path.join(HERE, "titoli", "typewriter-sfx.wav")
WAVES = SON + "Just Sound Effects - Rocky Coast of Norway/WATRWave_Soft Waves Cliffs_JSE_RCoN_Stereo.wav"
JUNGLE = SON + "Epic Stock Media - Synthesized Nature Loops and Sounds/AMBTrop_Loop Ambience Jungle Night Humid Birds Bug Chirps 01_ESM_SNLS.wav"
LEAK = os.path.join(YE, "packs", "light-leaks", "Light Leaks (5).mp4")   # the leak Jacopo picked blind on 24/10
# airy wide swoosh (centre ~4 kHz): the low tl2 whoosh (centre 92 Hz) was inaudible on a phone ("manca il sound effect")
WHOOSH = os.path.join(YE, "sfx", "licensed", "es-swoosh-wide.mp3")

WAVES_START, WAVES_DB = 36, -21     # steadiest stretch of the file; about 18 dB under the music ("va bene" 28/10)
JUNGLE_DB = -32                     # the jungle file is 11 dB louder than the waves: same perceived level
WAVES_END, JUNGLE_IN, JUNGLE_OUT, WAVES_BACK = 17.4, 16.6, 26.6, 25.8   # sea -> forest (monkeys..village) -> sea
CUT = 34.046                        # day -> sunset (boat of friends -> flag at sunset): the one transition
LEAK_FROM, LEAK_TO, LEAK_PEAK, LEAK_OPACITY = 1.25, 2.0, 1.6, 0.35       # only the golden streak (from 1,9 s the leak fills the frame with yellow)
WHOOSH_LEAD, WHOOSH_VOL = 0.48, 0.22   # 0,28 era "da abbassare di poco" (Jacopo 28/10): applicato per il render 4K
env = dict(os.environ, PYTHONUTF8="1")


def run(cmd):
    subprocess.run(cmd, check=True, env=env)


run([sys.executable, "-I", os.path.join(HERE, "edl.py"), "--senza-titolo"] + (["--width", "3840", "--height", "2160"] if K4 else []))
run([sys.executable, M, "render", os.path.join(HERE, "zanzibar-reel.edl.json"), "--encoder", "auto",
     "--work", os.path.join(HERE, "work", "render-v1")])
reel = os.path.join(HERE, "zanzibar-reel_v1.mp4")
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", reel],
                           capture_output=True, text=True).stdout)

lstart = CUT - (LEAK_PEAK - LEAK_FROM)
ldur = LEAK_TO - LEAK_FROM
video = ";".join([
    "[1:v]trim=start=5.4,setpts=PTS-STARTPTS[rest]",
    "[0:v]trim=end=5.4,setpts=PTS-STARTPTS[t]",
    "[t][rest]concat=n=2:v=1:a=0,format=gbrp[base]",
    # the leak, faded to black at both ends (screen with black = no change), placed so its middle sits on the cut
    ("[4:v]trim=start=%s:end=%s,setpts=PTS-STARTPTS,fps=25,scale=%s,format=gbrp,"
     "fade=t=in:d=0.5,fade=t=out:st=%.3f:d=0.5,tpad=start_duration=%.3f:stop_duration=%.3f:color=black[lk]"
     % (LEAK_FROM, LEAK_TO, "3840:2160" if K4 else "1920:1080", ldur - 0.5, lstart, dur)),
    "[base][lk]blend=all_mode=screen:all_opacity=%s:shortest=1,format=yuv420p[v]" % LEAK_OPACITY,
])
amb = ";".join([
    "[2:a]aresample=48000,aformat=channel_layouts=stereo,apad[k]",
    "[3:a]atrim=start=%d:duration=%s,asetpts=PTS-STARTPTS,aresample=48000,lowpass=f=6000,volume=%ddB,"
    "afade=t=in:d=1.2,afade=t=out:st=%s:d=1.0[w1]" % (WAVES_START, WAVES_END, WAVES_DB, WAVES_END - 1.0),
    "[3:a]atrim=start=%s:duration=%.3f,asetpts=PTS-STARTPTS,aresample=48000,lowpass=f=6000,volume=%ddB,"
    "afade=t=in:d=1.0,afade=t=out:st=%.3f:d=1.5,adelay=%d:all=1[w2]"
    % (WAVES_START + WAVES_BACK, dur - WAVES_BACK, WAVES_DB, dur - WAVES_BACK - 1.5, WAVES_BACK * 1000),
    "[5:a]atrim=duration=%s,asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,lowpass=f=6000,"
    "volume=%ddB,afade=t=in:d=1.0,afade=t=out:st=%s:d=1.0,adelay=%d:all=1[j]"
    % (JUNGLE_OUT - JUNGLE_IN, JUNGLE_DB, JUNGLE_OUT - JUNGLE_IN - 1.0, JUNGLE_IN * 1000),
    "[6:a]aresample=48000,aformat=channel_layouts=stereo,volume=%s,adelay=%d:all=1[s]" % (WHOOSH_VOL, (CUT - WHOOSH_LEAD) * 1000),
    "[k][w1][w2][j][s]amix=inputs=5:normalize=0:duration=longest,atrim=end=%.3f[fx]" % dur,
])
inputs = ["-i", TITLE, "-i", reel, "-i", KEYS, "-i", WAVES, "-i", LEAK, "-i", JUNGLE, "-i", WHOOSH]
for suffix, audio in (("", "[1:a]aresample=48000[m];[m][fx]amix=inputs=2:normalize=0:duration=first[a]"),
                      ("_senza-musica", "[fx]anull[a]")):
    out = os.path.join(HERE, NAME + suffix + ".mp4")
    run(["ffmpeg", "-v", "error", "-y"] + inputs + ["-filter_complex", ";".join([video, amb, audio]),
         "-map", "[v]", "-map", "[a]", "-c:v", "h264_nvenc", "-preset", "p7", "-cq", "19", "-c:a", "aac", "-b:a", "192k",
         "-t", "%.3f" % dur, out])
    print(out)
