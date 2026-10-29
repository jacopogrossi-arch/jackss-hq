"""Inventario clip DJI: una riga per clip (MP4 se c'è, altrimenti il proxy LRF) + fogli provini per giorno.
uso: python -I inventario.py CARTELLA_POCKET CARTELLA_OUT"""
import json, os, subprocess, sys, csv
from collections import defaultdict
from PIL import Image, ImageDraw, ImageFont

src, out = sys.argv[1], sys.argv[2]
os.makedirs(os.path.join(out, "thumbs"), exist_ok=True)


def probe(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", p],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    j = json.loads(r.stdout or "{}")
    v = next((s for s in j.get("streams", []) if s.get("codec_type") == "video"), {})
    tags = dict(j.get("format", {}).get("tags", {}) or {})
    for s in j.get("streams", []):
        tags.update(s.get("tags", {}) or {})
    fr = v.get("r_frame_rate", "0/1").split("/")
    fps = round(int(fr[0]) / max(int(fr[1]), 1), 2)
    return {"dur": round(float(j.get("format", {}).get("duration", 0) or 0), 1), "w": v.get("width"), "h": v.get("height"),
            "fps": fps, "gamma": str(tags.get("com.dji.camera.ColorGammaSxS", "")).strip(), "transfer": v.get("color_transfer", "")}


clips = {}
for sub in ("lrf", "mp4"):
    d = os.path.join(src, sub)
    for f in sorted(os.listdir(d)) if os.path.isdir(d) else []:
        clips.setdefault(os.path.splitext(f)[0], {})[sub] = os.path.join(d, f)

rows = []
for cid, files in sorted(clips.items()):
    ts = cid.split("_")[1]  # DJI_YYYYMMDDhhmmss_NNNN_D
    row = {"id": cid, "giorno": f"{ts[6:8]}/{ts[4:6]}", "ora": f"{ts[8:10]}:{ts[10:12]}", "mp4": "si" if "mp4" in files else "no"}
    meta_src = files.get("mp4") or files.get("lrf")
    m = probe(meta_src)
    row.update(m)
    if "mp4" not in files:  # dal proxy la risoluzione è quella del proxy, non dell'originale
        row["w"] = row["h"] = ""
    if "lrf" in files:  # fps dell'originale ricavati dall'MP4; dal proxy restano indicativi
        thumbs = []
        for k, frac in enumerate((0.15, 0.5, 0.85)):
            t = os.path.join(out, "thumbs", f"{cid}_{k}.jpg")
            if not os.path.exists(t):
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(max(m["dur"] * frac, 0)), "-i", files["lrf"],
                                "-frames:v", "1", "-vf", "scale=320:-2", t], capture_output=True)
            if os.path.exists(t):
                thumbs.append(t)
        row["thumbs"] = thumbs
    rows.append(row)

with open(os.path.join(out, "inventario.csv"), "w", newline="", encoding="utf-8") as fh:
    keys = ["id", "giorno", "ora", "dur", "w", "h", "fps", "gamma", "transfer", "mp4"]
    wr = csv.DictWriter(fh, keys, extrasaction="ignore")
    wr.writeheader()
    wr.writerows(rows)

# un foglio provini per giorno: una riga per clip, tre fotogrammi + etichetta
font = ImageFont.load_default(size=18)
byday = defaultdict(list)
for r in rows:
    byday[r["giorno"]].append(r)
for day, rs in byday.items():
    for page in range(0, len(rs), 12):
        chunk = rs[page:page + 12]
        W, H = 320 * 3 + 300, 180
        sheet = Image.new("RGB", (W, H * len(chunk)), (20, 20, 20))
        dr = ImageDraw.Draw(sheet)
        for i, r in enumerate(chunk):
            n = r["id"].split("_")[2]
            dr.text((10, i * H + 10), f"#{n}  {r['ora']}\n{r['dur']} s  {r['fps']} fps\n{r['gamma'] or '-'}\nMP4: {r['mp4']}", fill=(230, 230, 230), font=font)
            for k, t in enumerate(r.get("thumbs", [])):
                im = Image.open(t)
                im.thumbnail((320, H - 4))
                sheet.paste(im, (300 + k * 320, i * H + 2))
        sheet.save(os.path.join(out, f"provini_{day.replace('/', '-')}_{page // 12 + 1}.jpg"), quality=82)

print(len(rows), "clip;", sum(r["mp4"] == "si" for r in rows), "con MP4;", round(sum(r["dur"] for r in rows) / 60, 1), "min totali")
for day in sorted(byday, key=lambda d: d[3:] + d[:2]):
    rs = byday[day]
    print(day, len(rs), "clip,", round(sum(r["dur"] for r in rs) / 60, 1), "min, profili:", sorted({r["gamma"] or "-" for r in rs}))
