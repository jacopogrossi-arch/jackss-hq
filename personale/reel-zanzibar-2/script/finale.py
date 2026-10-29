"""Render del reel 2: edl.py -> mh-video-editor render (16:9) -> ritaglio 4:3 inquadrato clip per clip -> versione per il telefono.
Il ritaglio di ogni clip sta in shots.json ("crop43_x": bordo sinistro su 1920 di larghezza, da 0 a 480; senza = 240, il centro).
Il ritaglio cambia sul FOTOGRAMMA dove avviene davvero lo stacco nel 16:9 (misurato), non sul tempo del taglio: il render
arrotonda lo stacco al fotogramma prima, e col tempo per un fotogramma la clip nuova usciva con l'inquadratura vecchia (29/10).
uso: python -I finale.py [--4k]   -> zanzibar-reel2[_4k].mp4, ..._4x3.mp4, ..._4x3_telefono.mp4"""
import json, os, subprocess, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
M = "C:/Users/Jacopo Grossi/.claude/skills/mh-video-editor-skill/engine/scripts/mh_video.py"
K4 = "--4k" in sys.argv
W, H = (3840, 2160) if K4 else (1920, 1080)
W43 = H * 4 // 3
env = dict(os.environ, PYTHONUTF8="1")
cfg = json.load(open(os.path.join(HERE, "shots.json"), encoding="utf-8"))


def run(cmd):
    print(">", " ".join(cmd)[:200], flush=True)
    subprocess.run(cmd, check=True, env=env)


J = "--jacopo" in sys.argv  # versione col look di Jacopo (prepara_jacopo.py)
name = "zanzibar-reel2" + ("_jacopo" if J else "") + ("_4k" if K4 else "")
master = os.path.join(HERE, name + ".mp4")
run([sys.executable, os.path.join(HERE, "edl.py"), "--width", str(W), "--height", str(H)] + (["--jacopo"] if J else []))
run([sys.executable, M, "render", os.path.join(HERE, "zanzibar-reel2.edl.json"), "--encoder", "auto",
     "--work", os.path.join(HERE, "work", ("render-j" if J else "render") + ("-4k" if K4 else "")), "--out", master])

# fotogrammi reali degli stacchi: differenza fra fotogrammi consecutivi (a 160x90), il massimo vicino al taglio teorico
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", master, "-vf", "scale=160:90,format=gray", "-f", "rawvideo", "-"],
                     capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, 90, 160).astype(np.int16)
diff = np.r_[0, np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2))]
starts = [0]
for t in cfg["cuts"][1:-1]:
    k = round(t * 25)
    starts.append(max(range(k - 3, k + 4), key=lambda j: diff[j]))
print("stacchi (fotogramma):", starts[1:], flush=True)

# x del ritaglio per clip, in pixel del video renderizzato; default = centro
xs = [round(s.get("crop43_x", (1920 - 1440) / 2) * W / 1920) for s in cfg["shots"]]
expr = str(xs[-1])
for n0, x in reversed(list(zip(starts[1:], xs[:-1]))):
    expr = "if(lt(n,%d),%d,%s)" % (n0, x, expr)
out43 = os.path.join(HERE, name + "_4x3.mp4")
run(["ffmpeg", "-v", "error", "-y", "-i", master, "-vf", "crop=%d:%d:'%s':0" % (W43, H, expr),
     "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709",
     "-colorspace", "bt709", "-c:a", "copy", "-movflags", "+faststart", out43])
run(["ffmpeg", "-v", "error", "-y", "-i", out43, "-vf", "scale=-2:960", "-c:v", "libx264", "-crf", "21", "-pix_fmt", "yuv420p",
     "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", os.path.join(HERE, name + "_4x3_telefono.mp4")])
if K4:  # export per Instagram (impostazioni DaVinci di Jacopo, 29/10): H.264 High 25 Mbps due passate, keyframe ogni 2 s, tag BT.709
    ig = os.path.join(HERE, "zanzibar-reel2%s_INSTAGRAM_4x3.mp4" % ("_jacopo" if J else ""))
    common = ["-c:v", "libx264", "-profile:v", "high", "-b:v", "25M", "-maxrate", "30M", "-bufsize", "50M", "-g", "50", "-r", "25",
              "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
              "-passlogfile", os.path.join(HERE, "work", "ig2pass")]
    run(["ffmpeg", "-v", "error", "-y", "-i", out43] + common + ["-pass", "1", "-an", "-f", "null", "NUL"])
    run(["ffmpeg", "-v", "error", "-y", "-i", out43] + common + ["-pass", "2", "-c:a", "aac", "-b:a", "320k", "-movflags", "+faststart", ig])
    print("ok", ig)
print("ok", out43)
