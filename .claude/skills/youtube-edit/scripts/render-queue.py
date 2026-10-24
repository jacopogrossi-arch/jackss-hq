#!/usr/bin/env python3
"""render-queue.py: run ONE heavy command at a time. A second render started while the first runs waits in line.

Why: two renders at once (two sessions, or a draft started during a 4K) fight over Chrome, the GPU encoder and the disk,
and stop each other. A lock file makes the second one wait. The command itself is passed through untouched, so every flag
in SKILL.md keeps working.

Usage:  python3 render-queue.py [--lock FILE] [--wait-minutes 240] [--stale-minutes 360] -- <command> [args...]
  e.g.  python3 render-queue.py -- npx hyperframes render "$W/public" --quality draft --resolution 1080p -o "$W/draft.mp4"
The lock defaults to render-queue.lock in the system temp folder (one queue per machine). A lock older than --stale-minutes
(a crashed render) is removed. Exit code = the command's exit code; 3 = gave up waiting.
"""
import argparse, os, shutil, subprocess, sys, tempfile, time

ap = argparse.ArgumentParser()
ap.add_argument("--lock", default=os.path.join(tempfile.gettempdir(), "youtube-edit-render-queue.lock"))
ap.add_argument("--wait-minutes", type=float, default=240.0)
ap.add_argument("--stale-minutes", type=float, default=360.0)
ap.add_argument("--poll", type=float, default=5.0, help="seconds between checks while waiting")
ap.add_argument("cmd", nargs=argparse.REMAINDER)
a = ap.parse_args()
cmd = a.cmd[1:] if a.cmd and a.cmd[0] == "--" else a.cmd
if not cmd:
    ap.error("give the command after --")
# Windows: npx, npm and friends are .cmd files, which subprocess does not find without the full path
exe = shutil.which(cmd[0])
if exe:
    cmd = [exe] + cmd[1:]

deadline = time.time() + a.wait_minutes * 60
told = False
while True:
    try:
        fd = os.open(a.lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.write(fd, ("%d %s\n" % (os.getpid(), " ".join(cmd))).encode("utf-8", "replace")); os.close(fd)
        break
    except FileExistsError:
        try:
            if time.time() - os.stat(a.lock).st_mtime > a.stale_minutes * 60:
                os.remove(a.lock); print("render-queue: removed a stale lock", file=sys.stderr); continue
        except FileNotFoundError:
            continue                                      # released between our two calls: try again at once
        if time.time() > deadline:
            print("render-queue: gave up waiting for the line", file=sys.stderr); sys.exit(3)
        if not told:
            print("render-queue: another render is running, waiting in line...", file=sys.stderr); told = True
        time.sleep(a.poll)

try:
    sys.exit(subprocess.call(cmd))
finally:
    try:
        os.remove(a.lock)
    except FileNotFoundError:
        pass
