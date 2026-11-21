#!/usr/bin/env python3
"""Grade a video (mp4/mov) from reference images and/or a built-in look.

The grade is fitted once on frames sampled across the whole clip, so it never flickers.

  python video.py clip.mp4 --look the-matrix                       # fast: LUT through ffmpeg
  python video.py clip.mp4 --ref a.jpg b.jpg --mode full           # full quality: every frame through the engine
  python video.py clip.mp4 --look drive --preview 3.5              # graded still of the frame at 3.5 s

fast  = per-pixel grade as a 3D LUT + vignette + grain in ffmpeg. Quick, no skin protection / glow.
full  = identical to the image grade (skin masks, sky, haze, halation, bloom, grain). Slower.
Needs ffmpeg and ffprobe on PATH. Audio is copied unchanged.
"""
import argparse, json, subprocess, sys, tempfile
from pathlib import Path
import numpy as np, cv2

sys.path.insert(0, str(Path(__file__).parent))
import cg_core as cg
from grade import add_common, build

def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height,r_frame_rate:format=duration", "-of", "json", path],
                         capture_output=True, text=True, check=True).stdout
    d = json.loads(out)
    s = d["streams"][0]
    num, den = s["r_frame_rate"].split("/")
    return int(s["width"]), int(s["height"]), float(num) / float(den), float(d["format"]["duration"])

def frame_at(path, t, w, h):
    """Frame at time t. Steps back toward the start if a seek lands past the last frame (short clips)."""
    for tt in (t, t * 0.75, t * 0.5, 0.0):
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{tt:.3f}", "-i", path, "-frames:v", "1",
                              "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
        if len(raw) >= w * h * 3:
            return np.frombuffer(raw[: w * h * 3], np.uint8).reshape(h, w, 3).astype(np.float32) / 255
    raise SystemExit(f"could not read a frame from {path}")

def has_audio(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index",
                          "-of", "csv=p=0", path], capture_output=True, text=True).stdout
    return bool(out.strip())

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--out")
    ap.add_argument("--mode", choices=["fast", "full"], default="fast")
    ap.add_argument("--frames", type=int, default=12, help="frames sampled to fit the grade")
    ap.add_argument("--preview", type=float, help="only write a graded still at this time (seconds)")
    ap.add_argument("--crf", type=int, default=16)
    add_common(ap)
    a = ap.parse_args()
    w, h, fps, dur = probe(a.video)

    times = np.linspace(dur * 0.04, max(0.0, min(dur * 0.96, dur - 3 / fps)), a.frames)
    frames = [frame_at(a.video, t, w, h) for t in times]
    g = build(a, cg.image_lab_sample(frames))

    if a.preview is not None:
        out = a.out or str(Path(a.video).with_suffix("")) + f"-preview-{a.preview:g}s.jpg"
        cg.save(out, g.render(frame_at(a.video, a.preview, w, h)))
        print("wrote", out)
        return

    out = a.out or str(Path(a.video).with_suffix("")) + "-graded.mp4"
    audio = has_audio(a.video)
    enc = ["-c:v", "libx264", "-preset", "medium", "-crf", str(a.crf), "-pix_fmt", "yuv420p", "-movflags", "+faststart"]
    if a.lut:
        g.cube(a.lut, title=a.look or "reference match")

    if a.mode == "fast":
        with tempfile.TemporaryDirectory() as td:
            cube = Path(td) / "grade.cube"
            g.cube(cube, size=65)
            vf = [f"lut3d=file='{cube}':interp=tetrahedral"]
            for op in g.ops:
                if op["op"] == "vignette":
                    vf.append(f"vignette=angle={0.25 + op.get('amount', 0.3) * 0.9:.3f}")
                if op["op"] == "grain":
                    vf.append(f"noise=alls={max(1, round(op.get('amount', 0.02) * 420))}:allf=t")
            cmd = ["ffmpeg", "-y", "-v", "error", "-i", a.video, "-vf", ",".join(vf)] + enc
            cmd += ["-c:a", "copy"] if audio else []
            subprocess.run(cmd + [out], check=True)
    else:
        dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", a.video, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                               stdout=subprocess.PIPE)
        cmd = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}",
               "-r", f"{fps:.6f}", "-i", "-", "-i", a.video, "-map", "0:v"] + (["-map", "1:a", "-c:a", "copy"] if audio else []) + enc + [out]
        encp = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        n, skin, lut = 0, None, g.lut()
        total = int(dur * fps)
        while True:
            raw = dec.stdout.read(w * h * 3)
            if len(raw) < w * h * 3:
                break
            f = np.frombuffer(raw, np.uint8).reshape(h, w, 3).astype(np.float32) / 255
            if n % 6 == 0 or skin is None:  # skin mask refreshed every 6 frames
                skin = cg.skin_mask(f)
            res = g.render(f, seed=n, skin=skin, lut=lut)
            encp.stdin.write((np.clip(res, 0, 1) * 255 + 0.5).astype(np.uint8).tobytes())
            n += 1
            if n % 50 == 0:
                print(f"  {n}/{total} frames", flush=True)
        encp.stdin.close()
        encp.wait()
        dec.wait()
    print("wrote", out)

if __name__ == "__main__":
    main()
