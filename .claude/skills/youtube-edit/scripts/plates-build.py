"""plates-build.py: the standard build of a video made of motion plates (the method of Video #3, 03-06/11/2026, as one script).

The planner writes the plan (BRIEF.md, references/plate-plan.md) and one module per block of the plan in <project>/plates/ (b1.py, b2.py, ...).
A block is plain Python on formats/scene.py: its build() makes `Scene(...)` objects on the word times of transcript.json and returns the usual
{"html", "js"}. This script does the rest, the same way for every video:

  1. collects every full-frame Scene (bg=True) of every block; what a block returns besides them (a graphic beside the face made with
     Scene(bg=False), a tracker, hand-built html) goes into the video as it is;
  2. times each plate on its own elements: it starts LEAD s before its first element and ends TAIL s after its last (taste.md 13: a plate starts
     on the word that opens it and does not hold), unless the plan gives its times by hand (`override`);
  3. joins plates closer than GAP s into one run = one digital board (formats/board.py): page to page is a swipe, never a few frames of face;
     inside a page, a wait of HOLE s or more with nothing new brings the face back in the middle;
  4. moves everything onto a new cut when the cut changed after the plates were written (`recut`), instead of retyping the times;
  5. writes <out>/storyboard.json, runs compose.py with the preset, stages the plate sounds, and writes <out>/PLATES.md (every run, page, time,
     hole and warning) for the planner to read before any render.

Usage:  python plates-build.py <project> [--plates DIR] [--plan FILE] [--out DIR] [--video FILE] [--preset plates-verde] [--only b3,b4] [--no-compose]

<plates>/plan.json (every key optional):
  {"id": "video4", "duration": 885.5, "video": "input-video.mp4", "origin": "52% 0%", "blocks": ["b1", "b2"],
   "lead": 0.25, "tail": 1.8, "gap": 2.5, "hole": 6.5,
   "override": {"p12": [177.0, 184.2]},                       plate id -> [start, end] by hand
   "cam": {"p14": [[225.5, 640, 600, 1.55, 2.2]]},            plate id -> camera by hand: [time, x, y, scale, duration] in page pixels
   "nohole": ["p13"], "drop": ["p40"],                        never bring the face back inside / leave this plate out
   "transitions": [25.4, {"at": 173.3, "kind": "burn"}],      light leak by default, at scene changes only
   "recut": [{"insert": 88.3, "dur": 1.0}, {"cut": [206.7, 214.0]}],   changes made to the cut AFTER the times in the blocks were written
   "img": ["../draft/public/img"]}                            folders copied into public/img (also <plates>/img, always)
All times in the blocks and in plan.json are on the cut the blocks were written on; `recut` is applied last, to everything.
"""
import argparse, importlib, json, os, re, shutil, subprocess, sys

SK = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(SK, "formats"))
from scene import Scene  # noqa: E402
from board import Board  # noqa: E402
from plates_base import write_plate_sounds  # noqa: E402

SNAKE = [(0, 0), (1, 0), (2, 0), (2, 1), (1, 1), (0, 1), (0, 2), (1, 2), (2, 2)]     # where the pages of one run sit on the board
DEFAULTS = dict(lead=0.25, tail=1.8, gap=2.5, hole=6.5)
LONG = 12.0      # plate-plan.md rule 9: a plate longer than this needs a split or the face back


def make_T(recut):
    """recut: [{"insert": t, "dur": d}, {"cut": [c0, c1]}] on the old cut -> T(t), the same moment on the new cut."""
    ops = sorted(recut or [], key=lambda o: o["insert"] if "insert" in o else o["cut"][0])

    def T(t):
        shift = 0.0
        for o in ops:
            if "insert" in o:
                if t >= o["insert"]:
                    shift += o["dur"]
            else:
                c0, c1 = o["cut"]
                if t >= c1:
                    shift -= c1 - c0
                elif t > c0:
                    return c0 + shift
        return t + shift
    return T


def retime_html(html, T):
    """data-start / data-duration / data-at of every tag onto the new cut: a host keeps its end on the same moment, a sound keeps its length."""
    def retag(m):
        g = m.group(0)
        st = re.search(r'data-start="([\d.]+)"', g)
        if st:
            a = float(st.group(1))
            d = re.search(r'data-duration="([\d.]+)"', g)
            if d and not g.startswith("<audio"):
                g = g.replace(d.group(0), 'data-duration="%.3f"' % (T(a + float(d.group(1))) - T(a)))
            g = g.replace(st.group(0), 'data-start="%.3f"' % T(a))
        return re.sub(r'data-at="([\d.]+)"', lambda x: 'data-at="%.3f"' % T(float(x.group(1))), g)
    return re.sub(r"<[a-z]+\b[^>]*data-(?:start|at)=[^>]*>", retag, html)


def retime_js(js, T):
    """The position argument of every tl.set / tl.fromTo onto the new cut. Fails when a line does not end the usual way: never retime half a timeline."""
    n_tl = len(re.findall(r"tl\.(?:set|fromTo)\(", js))
    js, n_ok = re.subn(r"(\}\)?, )(\d+(?:\.\d+)?)(\);)", lambda m: "%s%.3f%s" % (m.group(1), T(float(m.group(2))), m.group(3)), js)
    if n_tl != n_ok:
        raise SystemExit("recut: %d timeline calls but %d retimed. A tl.set / tl.fromTo is written in a way the retimer does not read; fix that line." % (n_tl, n_ok))
    return js


def event_times(s):
    return sorted(set(list(s.events) + [t for t in s.when.values() if t]))


def collect(blocks, retime):
    """Runs every block with Scene patched: full-frame scenes are kept aside for the boards, the rest of what a block returns is kept as it is."""
    reg, extra = [], []
    _init, _build = Scene.__init__, Scene.build

    def init(self, cid, t_in, t_out, *a, **k):
        t_in, t_out = retime.get(cid, (t_in, t_out))
        _init(self, cid, t_in, t_out, *a, **k)

    def build(self):
        if not self.bg:
            return _build(self)
        reg.append(self)
        return {"html": "", "js": ""}

    Scene.__init__, Scene.build = init, build
    try:
        for name in blocks:
            m = importlib.reload(sys.modules[name]) if name in sys.modules else importlib.import_module(name)     # a fresh run: track counters start again
            o = m.build()
            if o and (o.get("html") or o.get("js")):
                extra.append(o)
    finally:
        Scene.__init__, Scene.build = _init, _build
    return reg, extra


def plan_runs(reg, cfg):
    """Plates in time order, joined into runs (one board each) when closer than `gap`."""
    drop = set(cfg.get("drop", []))
    items = sorted((dict(s=s, a=s.t_in, b=s.t_out, cam=[tuple(c) for c in cfg.get("cam", {}).get(s.cid, [])] or None) for s in reg if s.cid not in drop), key=lambda p: p["a"])
    runs = []
    for p in items:
        if runs and p["a"] - runs[-1][-1]["b"] < cfg["gap"]:
            runs[-1][-1]["b"] = p["a"]     # the swipe joins them
            runs[-1].append(p)
        else:
            runs.append([p])
    return runs


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("project")
    ap.add_argument("--plates"); ap.add_argument("--out"); ap.add_argument("--video"); ap.add_argument("--plan", help="plan.json somewhere else than <plates>/plan.json")
    ap.add_argument("--preset", default="plates-verde")
    ap.add_argument("--only", help="comma-separated blocks, for a lab window")
    ap.add_argument("--no-compose", action="store_true", help="stop after storyboard.json and PLATES.md")
    a = ap.parse_args()
    W = os.path.abspath(a.project)
    PL = os.path.abspath(a.plates or os.path.join(W, "plates"))
    OUT = os.path.abspath(a.out or os.path.join(W, "build"))
    PUB = os.path.join(OUT, "public")
    cfg = dict(DEFAULTS)
    pj = os.path.abspath(a.plan) if a.plan else os.path.join(PL, "plan.json")
    if os.path.exists(pj):
        cfg.update(json.load(open(pj, encoding="utf-8")))
    blocks = a.only.split(",") if a.only else cfg.get("blocks") or sorted((f[:-3] for f in os.listdir(PL) if re.fullmatch(r"b\d+\w*\.py", f)), key=lambda n: (int(re.search(r"\d+", n).group()), n))
    if not blocks:
        raise SystemExit("no blocks in %s (b1.py, b2.py, ... each with a build())" % PL)
    sys.path.insert(0, PL)
    os.makedirs(PUB, exist_ok=True)

    # pass 1: where each plate's elements land; pass 2: the plates rebuilt on those times
    reg, _ = collect(blocks, {})
    over = {k: tuple(v) for k, v in cfg.get("override", {}).items()}
    retime, warn = {}, []
    for s in reg:
        ev = event_times(s)
        if s.cid in over:
            retime[s.cid] = over[s.cid]
        elif ev:
            retime[s.cid] = (max(s.t_in, ev[0] - cfg["lead"]), min(s.t_out, ev[-1] + cfg["tail"]))
        else:
            warn.append("%s has no timed element: it keeps %.1f-%.1f as written. A plate with nothing landing on a word is decoration (plate-plan.md)." % (s.cid, s.t_in, s.t_out))
    ids = [s.cid for s in reg]
    for c in sorted(set(c for c in ids if ids.count(c) > 1)):
        raise SystemExit("two plates are called %s: every plate needs its own id" % c)
    reg, extra = collect(blocks, retime)
    runs = plan_runs(reg, cfg)

    html, js, report = [], [], []
    nohole = set(cfg.get("nohole", []))
    for n, run in enumerate(runs):
        B = Board("r%d" % n, track=20 + n, track_audio=500 + 30 * n)
        for k, p in enumerate(run):
            B.page(p["s"], SNAKE[k % len(SNAKE)], p["a"], p["b"], cam=p["cam"])
            ev = [e for e in event_times(p["s"]) if p["a"] <= e <= p["b"]]
            if p["s"].cid not in nohole and not p["cam"]:
                for x, y in zip(ev, ev[1:]):
                    if y - x >= cfg["hole"]:
                        B.away(x + 2.2, y - 0.5)
            held = make_T(cfg.get("recut"))(p["b"]) - make_T(cfg.get("recut"))(p["a"])
            if held > LONG and not p["cam"] and not any(p["a"] <= x <= p["b"] for x, _ in B.holes):
                warn.append("%s stays %.1f s with no face break and no camera of its own: split it, or check it keeps the listener (taste.md 13)." % (p["s"].cid, held))
        o = B.build()
        html.append(o["html"]); js.append(o["js"])
        report.append((n, run, list(B.holes)))
    for o in extra:
        html.append(o.get("html", "")); js.append(o.get("js", ""))

    T = make_T(cfg.get("recut"))
    rawhtml, rawjs = "\n".join(html), re.sub(r"back\.out\([\d.]*\)", "power3.out", "\n".join(js))     # nothing overshoots on a plate (taste.md 13)
    if cfg.get("recut"):
        rawhtml, rawjs = retime_html(rawhtml, T), retime_js(rawjs, T)
    beats = []
    for k, t in enumerate(cfg.get("transitions", [])):
        t = t if isinstance(t, dict) else {"at": t}
        beats.append(dict({"id": "tr%d" % k, "type": "transition", "kind": "lightleak"}, **dict(t, at=T(t["at"]))))

    video = cfg.get("video", "input-video.mp4")
    src = os.path.abspath(a.video) if a.video else os.path.join(W, "public", video)
    dst = os.path.join(PUB, video)
    if os.path.exists(src) and not os.path.exists(dst):
        try:
            os.link(src, dst)        # a hard link: no second copy of the footage on the disk
        except OSError:              # another drive: never copy gigabytes on our own (the small C: trap in traps.md)
            print("NOTE: could not link %s into %s (another drive?). Put --out on the footage's drive, or copy a light proxy there yourself." % (src, PUB))
    duration = cfg.get("duration")
    if duration is None and os.path.exists(dst):
        duration = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", dst], capture_output=True, text=True).stdout.strip() or 0) or None
    if duration is None:
        raise SystemExit('no "duration" in plan.json and no footage at %s to measure' % dst)
    duration = round(T(duration) if cfg.get("duration") is not None else duration, 3)       # a measured file is already the new cut
    for d in [os.path.join(PL, "img")] + [os.path.join(PL, p) for p in cfg.get("img", [])]:
        if os.path.isdir(d):
            shutil.copytree(d, os.path.join(PUB, "img"), dirs_exist_ok=True)
    tj = os.path.join(W, "transcript.json")
    if os.path.exists(tj):
        words = json.load(open(tj, encoding="utf-8"))
        if cfg.get("recut") and isinstance(words, list):
            cuts = [o["cut"] for o in cfg["recut"] if "cut" in o]
            words = [dict(w, start=T(w["start"]), end=T(w["end"])) for w in words if not any(c0 <= w["start"] < c1 for c0, c1 in cuts)]
        json.dump(words, open(os.path.join(OUT, "transcript.json"), "w", encoding="utf-8"), ensure_ascii=False)

    sb = {"id": cfg.get("id", os.path.basename(W)), "duration": duration, "video": video, "origin": cfg.get("origin", "52% 0%"), "preset": a.preset,
          "beats": beats, "camera": [], "raw_html": rawhtml, "raw_js": rawjs}
    json.dump(sb, open(os.path.join(OUT, "storyboard.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    def mmss(t):
        t = round(t, 1)
        return "%d:%04.1f" % (t // 60, t % 60)
    on = sum(T(run[-1]["b"]) - T(run[0]["a"]) for _, run, _ in report)
    md = ["# Plates: %s" % sb["id"], "",
          "%d plates in %d runs (one board each), %.0f s of plates on %.0f s of video (%.0f %%). Blocks: %s. Times on the %s cut." % (
              sum(len(r) for _, r, _ in report), len(report), on, duration, 100 * on / duration, ", ".join(blocks), "new" if cfg.get("recut") else "current"), "",
          "| Run | Plate | In | Out | Seconds | Elements | Camera | Face back inside |", "|---|---|---|---|---|---|---|---|"]
    for n, run, holes in report:
        for p in run:
            hs = ", ".join("%s-%s" % (mmss(T(x)), mmss(T(y))) for x, y in holes if p["a"] <= x <= p["b"]) or "-"
            md.append("| %d | %s | %s | %s | %.1f | %d | %s | %s |" % (n, p["s"].cid, mmss(T(p["a"])), mmss(T(p["b"])), T(p["b"]) - T(p["a"]), len(event_times(p["s"])), "by hand" if p["cam"] else "auto", hs))
    md += ["", "## Warnings", ""] + (["- " + w for w in warn] or ["None."])
    md += ["", "Not checked here: that each element lands on its word (`beat-check.py`), the picture (`snap-beats.py`, `check-frames.py` on a draft) and the sound (nobody listens: `sound-report.py`, then Jacopo's ears)."]
    open(os.path.join(OUT, "PLATES.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print("\n".join(md[2:3] + ["warnings: %d" % len(warn)] + ["  " + w for w in warn]))

    if a.no_compose:
        return
    r = subprocess.run([sys.executable, os.path.join(SK, "scripts", "compose.py"), "--spec", os.path.join(OUT, "storyboard.json"), "--out", PUB, "--preset", a.preset],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    print(r.stdout[-400:], r.stderr[-1200:])
    if r.returncode:
        raise SystemExit("compose.py failed")
    write_plate_sounds(PUB, SK)
    print("built:", PUB)


if __name__ == "__main__":
    main()
