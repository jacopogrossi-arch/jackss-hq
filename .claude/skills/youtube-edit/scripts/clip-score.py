"""Score a folder of clips for beauty and motion, to pre-select footage.

Aesthetic: the Open-Sora v1.2 scorer (CLIP ViT-L/14 + the LAION
improved-aesthetic-predictor MLP, sac+logos+ava1-l14-linearMSE), 1-10,
mean of N frames. Open-Sora reads 5.5 as fair and 6.5 as high.
Motion: OpenCV Farneback optical flow between frames 0.2 s apart at
320 px, mean magnitude in % of the width per second (Open-Sora uses
UniMatch; Farneback ranks clips the same way at a fraction of the cost).

Needs the D:/tools/video-ai environment (torch + open_clip + opencv):
  D:/tools/video-ai/Scripts/python.exe clip-score.py --dir FOLDER --out scores.csv [--frames 5]

Compare like with like: log clips score a bit lower than graded ones.
Measure MOTION on clips without film grain (raw log or plain Rec.709):
grain reads as flow (27/10/2026: the same lagoon clip gave 1.15 raw and
3.96 with the pellicola-oro grain). Aesthetic is fine on either.
"""
import argparse
import csv
import json
import os
import sys
import urllib.request
from pathlib import Path

import cv2
import numpy as np
import torch
import torch.nn as nn
import open_clip
from PIL import Image

VIDEO_EXT = {".mp4", ".mov", ".mxf", ".m4v", ".mkv", ".avi"}
WEIGHTS_URL = ("https://github.com/christophschuhmann/improved-aesthetic-predictor/"
               "raw/main/sac%2Blogos%2Bava1-l14-linearMSE.pth")
WEIGHTS = Path(os.environ.get("CLIP_SCORE_HOME", "D:/tools/video-ai/models")) / "sac+logos+ava1-l14-linearMSE.pth"


class MLP(nn.Module):  # same layout as Open-Sora tools/scoring/aesthetic
    def __init__(self, input_size=768):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(input_size, 1024), nn.Dropout(0.2),
            nn.Linear(1024, 128), nn.Dropout(0.2),
            nn.Linear(128, 64), nn.Dropout(0.1),
            nn.Linear(64, 16), nn.Linear(16, 1),
        )

    def forward(self, x):
        return self.layers(x)


def load_model(device):
    if not WEIGHTS.exists():
        WEIGHTS.parent.mkdir(parents=True, exist_ok=True)
        print(f"downloading aesthetic weights -> {WEIGHTS}")
        urllib.request.urlretrieve(WEIGHTS_URL, WEIGHTS)
    model, _, preprocess = open_clip.create_model_and_transforms("ViT-L-14", pretrained="openai", device=device)
    model.eval()
    mlp = MLP().to(device)
    mlp.load_state_dict(torch.load(WEIGHTS, map_location=device))
    mlp.eval()
    return model, preprocess, mlp


def grab(cap, t):
    cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
    ok, frame = cap.read()
    return frame if ok else None


def small_gray(frame, width=320):
    h, w = frame.shape[:2]
    return cv2.cvtColor(cv2.resize(frame, (width, int(h * width / w))), cv2.COLOR_BGR2GRAY)


def score_clip(path, n, model, preprocess, mlp, device):
    cap = cv2.VideoCapture(str(path))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    dur = cap.get(cv2.CAP_PROP_FRAME_COUNT) / fps
    points = [dur * (i + 1) / (n + 1) for i in range(n)]
    images, flows = [], []
    gap = 0.2
    for t in points:
        a = grab(cap, t)
        b = grab(cap, min(t + gap, dur - 0.05))
        if a is None:
            continue
        images.append(preprocess(Image.fromarray(cv2.cvtColor(a, cv2.COLOR_BGR2RGB))))
        if b is not None:
            ga, gb = small_gray(a), small_gray(b)
            flow = cv2.calcOpticalFlowFarneback(ga, gb, None, 0.5, 3, 15, 3, 5, 1.2, 0)
            mag = np.linalg.norm(flow, axis=2).mean()
            flows.append(mag / ga.shape[1] * 100 / gap)
    cap.release()
    if not images:
        return None
    with torch.no_grad():
        feats = model.encode_image(torch.stack(images).to(device))
        feats = torch.nn.functional.normalize(feats, p=2, dim=-1).float()
        aes = mlp(feats).squeeze(1).cpu().numpy()
    return {
        "clip": path.name,
        "durata_s": round(dur, 1),
        "estetica": round(float(aes.mean()), 2),
        "estetica_max": round(float(aes.max()), 2),
        "movimento": round(float(np.mean(flows)), 2) if flows else 0.0,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", required=True, help="folder of clips (not recursive)")
    ap.add_argument("--out", required=True, help="CSV path; a .json twin is written next to it")
    ap.add_argument("--frames", type=int, default=5)
    args = ap.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess, mlp = load_model(device)
    clips = sorted(p for p in Path(args.dir).iterdir() if p.suffix.lower() in VIDEO_EXT)
    if not clips:
        sys.exit(f"no clips in {args.dir}")
    rows = []
    for i, p in enumerate(clips, 1):
        r = score_clip(p, args.frames, model, preprocess, mlp, device)
        print(f"[{i}/{len(clips)}] {p.name}: " + (f"estetica {r['estetica']}  movimento {r['movimento']}" if r else "unreadable"))
        if r:
            rows.append(r)
    rows.sort(key=lambda r: r["estetica"], reverse=True)
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    Path(args.out).with_suffix(".json").write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"{len(rows)} clips -> {args.out} (device {device})")


if __name__ == "__main__":
    main()
