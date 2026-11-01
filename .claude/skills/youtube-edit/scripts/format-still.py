#!/usr/bin/env python3
"""format-still.py: still frames of a plate format at chosen times, without the whole pipeline (headless Chrome + GSAP seek).

    python3 scripts/format-still.py BUILD.py --times 0.5 1.2 3 --out DIR [--preset plates-verde] [--pip] [--sheet]

BUILD.py defines build() returning {"html": ..., "js": ..., "t_end": seconds (optional)}, exactly what a format in formats/ returns.
--preset picks the style tokens (default: the studio defaults); --pip draws the face PiP square where compose.py will put it, so a
graphic entering that corner is obvious; --sheet also writes sheet.jpg (all times on one page, needs Pillow).
Used on 01/11/2026 to build and check the plate formats; it does NOT replace the real render (no audio, no video underneath).
"""
import argparse, importlib.util, json, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SK = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(SK, "formats"))
import studio  # noqa: E402

CHROMES = [r"C:\Program Files\Google\Chrome\Application\chrome.exe", r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
           r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe", "/usr/bin/google-chrome", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]

PAGE = """<!doctype html><meta charset="utf-8"><style>
  * { box-sizing:border-box; margin:0; } html,body { width:1920px; height:1080px; overflow:hidden; background:#000; position:relative; }
  %(css)s
  #stand { position:absolute; inset:0; background:#2a2622; }
  #pipph { position:absolute; left:1552px; top:712px; width:320px; height:320px; border-radius:28px; border:3px solid %(ring)s; background:linear-gradient(160deg,#4a423a,#1a1612);
           box-shadow:0 0 28px %(ring)s66; z-index:50; display:%(pipd)s; }
</style><body><div id="stand"></div>
%(html)s
<div id="pipph"></div>
<script src="gsap.min.js"></script>
<script>
const tl = gsap.timeline({ paused:true });
%(js)s
function render(t) {
  tl.time(0, false); tl.time(t, false);
  document.querySelectorAll('.card-host').forEach(h => {
    const s = +h.dataset.start, d = +h.dataset.duration;
    h.style.visibility = (t >= s && t <= s + d) ? 'visible' : 'hidden';
  });
}
render(+(location.hash.slice(1) || 0));
</script>"""


def chrome():
    for c in CHROMES:
        if os.path.exists(c):
            return c
    sys.exit("no Chrome/Edge found")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("build"); ap.add_argument("--times", nargs="+", type=float, required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--preset", default=""); ap.add_argument("--pip", action="store_true"); ap.add_argument("--sheet", action="store_true")
    a = ap.parse_args()
    style = {}
    if a.preset:
        style = json.load(open(os.path.join(SK, "presets", a.preset, "preset.json"), encoding="utf-8")).get("style", {})
    spec = importlib.util.spec_from_file_location("lab_build", a.build); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    out = m.build()
    os.makedirs(os.path.join(a.out, "fonts"), exist_ok=True)
    shutil.copy(os.path.join(SK, "assets", "vendor", "gsap.min.js"), a.out)
    for f in os.listdir(os.path.join(SK, "assets", "fonts")):
        shutil.copy(os.path.join(SK, "assets", "fonts", f), os.path.join(a.out, "fonts", f))
    page = PAGE % dict(css=studio.css(style), ring=style.get("ring", "#0AF0F0"), pipd="block" if a.pip else "none", html=out["html"], js=out["js"])
    path = os.path.abspath(os.path.join(a.out, "lab.html"))
    open(path, "w", encoding="utf-8").write(page)
    shots = []
    for t in a.times:
        png = os.path.abspath(os.path.join(a.out, "still-%05.2f.png" % t)); shots.append(png)
        subprocess.run([chrome(), "--headless=new", "--disable-gpu", "--hide-scrollbars", "--window-size=1920,1080", "--virtual-time-budget=3000",
                        "--screenshot=" + png, "file:///" + path.replace("\\", "/") + "#" + repr(t)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print(png)
    if a.sheet:
        from PIL import Image
        ims = [Image.open(p).convert("RGB").resize((640, 360)) for p in shots]
        cols = 3; rows = (len(ims) + cols - 1) // cols
        sh = Image.new("RGB", (640 * cols, 360 * rows), (0, 0, 0))
        for i, im in enumerate(ims):
            sh.paste(im, ((i % cols) * 640, (i // cols) * 360))
        sh.save(os.path.join(a.out, "sheet.jpg"), quality=88); print(os.path.join(a.out, "sheet.jpg"))


if __name__ == "__main__":
    main()
