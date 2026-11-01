#!/usr/bin/env python3
"""studio-lab.py: put a lab in HyperFrames Studio so Jacopo can watch it play and comment on the picture while we work.

    python3 scripts/studio-lab.py LAB_DIR [--name NAME] [--open]

LAB_DIR is a lab folder with a `public/` composition (what compose.py wrote: index.html, the video, fonts, sfx...), e.g. `videos/_bench/plates-verde/ab/lab-B`.
It makes a LIGHT copy under `C:\\Users\\<name>\\HyperFrames\\<NAME>` (the app only sees projects under the home folder: a project on D: "opens" and shows
nothing; and C: is small, so no renders, logs or `.hyperframes` artifacts are copied) and prints the copy's path. With --open it also runs
`npx hyperframes open <copy>`, which starts the desktop app on it and hands it to this session. WITHOUT --open nothing is launched: the rule of
the skill is to PROPOSE Studio at every lab and open it only when Jacopo says yes. Changes made in Studio are read back with
`npx hyperframes catch-up <copy>`; the changed `index.html` is copied back by hand into the lab (see references/hyperframes-app.md).
"""
import argparse, os, shutil, subprocess, sys

SKIP = {".hyperframes", "__pycache__"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("lab"); ap.add_argument("--name", default=""); ap.add_argument("--open", action="store_true")
    a = ap.parse_args()
    lab = os.path.abspath(a.lab)
    pub = os.path.join(lab, "public") if os.path.isdir(os.path.join(lab, "public")) else lab
    if not os.path.exists(os.path.join(pub, "index.html")):
        sys.exit("no index.html in %s (run compose.py first)" % pub)
    name = a.name or os.path.basename(lab.rstrip("\\/"))
    dest = os.path.join(os.path.expanduser("~"), "HyperFrames", name)
    shutil.rmtree(dest, ignore_errors=True)
    shutil.copytree(pub, dest, dirs_exist_ok=True, ignore=lambda d, names: [n for n in names if n in SKIP or n.endswith((".log", ".tmp"))])
    size = sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(dest) for f in fs) / 1e6
    print("copy: %s (%.1f MB)" % (dest, size))
    if a.open:
        r = subprocess.run("npx hyperframes open \"%s\"" % dest, shell=True, capture_output=True, text=True)
        print(r.stdout.strip() or r.stderr.strip())
    else:
        print("not opened: add --open when Jacopo says yes")


if __name__ == "__main__":
    main()
