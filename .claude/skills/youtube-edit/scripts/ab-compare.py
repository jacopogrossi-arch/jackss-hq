#!/usr/bin/env python3
"""ab-compare.py: a blind A/B between two renders of the SAME bench window, so Jacopo judges the picture, not the label.

The two files are shuffled into 1.mp4 and 2.mp4, joined side by side (side-by-side.mp4: 1 left, 2 right, audio of 1) and one
after the other (in-sequence.mp4: 1, a second of black, 2). Which one is the new version is written only to KEY.md: do not tell
Jacopo before he has picked. Then record the result in references/NOTES_LOG.md and only the winner enters the skill.

Usage: python3 ab-compare.py --a current.mp4 --b candidate.mp4 --out W/ab/<test-name>/ [--labels "current,new"] [--seed N]
"""
import argparse, datetime, os, random, shutil, subprocess

ap = argparse.ArgumentParser()
ap.add_argument("--a", required=True); ap.add_argument("--b", required=True); ap.add_argument("--out", required=True)
ap.add_argument("--labels", default="A,B", help="what --a and --b are, for KEY.md only (e.g. 'sonnet,opus' or 'old list,new list')")
ap.add_argument("--seed", type=int, help="fix the shuffle (tests)")
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)
names = [x.strip() for x in a.labels.split(",")] + ["A", "B"]
pair = [(a.a, names[0]), (a.b, names[1])]
random.Random(a.seed).shuffle(pair)


def ff(*args):
    subprocess.run(["ffmpeg", "-y", "-v", "error", *args], check=True)


one, two = os.path.join(a.out, "1.mp4"), os.path.join(a.out, "2.mp4")
shutil.copyfile(pair[0][0], one); shutil.copyfile(pair[1][0], two)
ff("-i", one, "-i", two, "-filter_complex",
   "[0:v]scale=960:-2,setsar=1[l];[1:v]scale=960:-2,setsar=1[r];[l][r]hstack=inputs=2:shortest=1[v]",
   "-map", "[v]", "-map", "0:a?", "-c:v", "libx264", "-crf", "20", "-preset", "fast", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest",
   os.path.join(a.out, "side-by-side.mp4"))
ff("-i", one, "-i", two, "-f", "lavfi", "-i", "color=c=black:s=1920x1080:r=30:d=1", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo:d=1",
   "-filter_complex",
   "[0:v]scale=1920:1080,setsar=1,fps=30,format=yuv420p[v0];[1:v]scale=1920:1080,setsar=1,fps=30,format=yuv420p[v1];[2:v]format=yuv420p[vb];"
   "[0:a]aresample=48000,aformat=channel_layouts=stereo[a0];[1:a]aresample=48000,aformat=channel_layouts=stereo[a1];"
   "[v0][a0][vb][3:a][v1][a1]concat=n=3:v=1:a=1[v][au]",
   "-map", "[v]", "-map", "[au]", "-c:v", "libx264", "-crf", "20", "-preset", "fast", "-c:a", "aac", os.path.join(a.out, "in-sequence.mp4"))
open(os.path.join(a.out, "KEY.md"), "w", encoding="utf-8").write(
    "# A/B key (do not show before Jacopo picks)\n\n%s\n\n- 1 = %s (`%s`)\n- 2 = %s (`%s`)\n\nJacopo's pick: \nWhy: \n"
    % (datetime.date.today().isoformat(), pair[0][1], pair[0][0], pair[1][1], pair[1][0]))
print("Show Jacopo: %s and %s (or 1.mp4 / 2.mp4). The key is in KEY.md: do not read it out before he picks."
      % (os.path.join(a.out, "side-by-side.mp4"), os.path.join(a.out, "in-sequence.mp4")))
