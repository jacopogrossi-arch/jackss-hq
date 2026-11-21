#!/usr/bin/env python3
"""Download extra film stills of a movie (TMDB backdrops without text) to build a stronger look.

  python fetch_stills.py "Drive" --year 2011 --out stills/drive --n 12

Stills are for the user's own reference only. Do not redistribute them.
"""
import argparse, re, subprocess, time, urllib.parse
from pathlib import Path

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
IMG = re.compile(r'image\.tmdb\.org/t/p/[a-z0-9_]+/([A-Za-z0-9]+\.(?:jpg|png))')

def get(url):
    r = subprocess.run(["curl", "-sL", "--max-time", "40", "-A", UA, url], capture_output=True)
    return r.stdout.decode("utf-8", "ignore")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("title")
    ap.add_argument("--year")
    ap.add_argument("--out", required=True)
    ap.add_argument("--n", type=int, default=12)
    a = ap.parse_args()
    q = a.title + (f" y:{a.year}" if a.year else "")
    page = get("https://www.themoviedb.org/search/movie?query=" + urllib.parse.quote(q))
    ids = re.findall(r'href="/movie/(\d+)[^"]*"', page)
    if not ids:
        raise SystemExit("movie not found on TMDB, try --year or another spelling")
    mid = ids[0]
    title = re.search(r'<title>(.*?)</title>', get(f"https://www.themoviedb.org/movie/{mid}"), re.S)
    print("movie:", title.group(1).strip() if title else mid)
    files = []
    for lang in ("xx", "null"):  # xx = no language, the clean film frames
        for f in IMG.findall(get(f"https://www.themoviedb.org/movie/{mid}/images/backdrops?image_language={lang}")):
            if f not in files:
                files.append(f)
        if len(files) >= a.n:
            break
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    for i, f in enumerate(files[: a.n]):
        subprocess.run(["curl", "-sL", "--max-time", "40", "-A", UA, "-o", str(out / f"still-{i + 1:02d}.jpg"),
                        f"https://image.tmdb.org/t/p/w780/{f}"])
        time.sleep(0.2)
    print(f"saved {min(len(files), a.n)} stills to {out}")

if __name__ == "__main__":
    main()
