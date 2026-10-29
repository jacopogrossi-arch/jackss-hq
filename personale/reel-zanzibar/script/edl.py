"""Scrive zanzibar-reel.edl.json da shots.json: clip gia' gradate (pellicola-oro), tagli netti sulle battute, titolo.
uso: python -I edl.py [--width 3840 --height 2160]"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
cfg = json.load(open(os.path.join(HERE, "shots.json"), encoding="utf-8"))
W = int(sys.argv[sys.argv.index("--width") + 1]) if "--width" in sys.argv else 1920
H = int(sys.argv[sys.argv.index("--height") + 1]) if "--height" in sys.argv else 1080
cuts = cfg["cuts"]
SANS = "C:/Windows/Fonts/segoeuil.ttf"
SERIF = HERE + "/../../../inverso/assets-jago/carosello-pricing/fonts/AppleGaramond-Light.ttf"


GRADE = "curves=all='0/0 0.25/0.21 0.5/0.5 0.75/0.79 1/1',eq=saturation=1.12"


def word(text, start, x, y, size, font):
    return {"text": text, "start": start, "end": 5.1, "position": "custom", "x": x, "y": y, "size": round(size * H / 1080),
            "font_file": os.path.normpath(font).replace("\\", "/"), "color": "#FFFFFF", "outline_width": 0, "shadow": 1, "style": "subtitle",
            "animation": "fade", "lang": "en"}


edl = {
    "version": 1,
    "project": {"name": "zanzibar-reel_v1", "preset": "youtube-16x9", "width": W, "height": H, "fps": 25,
                "duration": cuts[-1], "music": HERE + "/ref/riferimento.wav",
                "fade_in": 0.0, "fade_out": 0.8, "music_fade_in": 0.0, "music_fade_out": 0.6},
    "beats": {"t0": cuts[1], "period": 0.5024},
    # sopra pellicola-oro: piu' contrasto (scelto da Jacopo 28/10). zoom 0.05 = spinta lenta su ogni clip (nelle v2-v5 per
    # sbaglio, poi confermata: "il push in mi piace"); end_flare (bagliore caldo sul tramonto finale) tolto il 28/10.
    "style": {"grade": GRADE, "zoom": 0.05, "drop_flash": False, "end_flare": False, "riser": False, "boom": False,
              "loudness": -14},
    "shots": [{"clip": "%s/work/shots/%02d-%s/grade/graded.mp4" % (HERE, i + 1, s["id"]), "span": [cuts[i], cuts[i + 1]],
               "src_start": 0.0, **({"grade": GRADE + "," + s["extra"]} if s.get("extra") else {})}
              for i, s in enumerate(cfg["shots"])],
    "texts": [word("The", 0.5, 0.20, 0.50, 50, SANS), word("beauty", 1.0, 0.355, 0.50, 50, SANS),
              word("of", 1.5, 0.50, 0.50, 50, SANS), word("zanzibar", 2.1, 0.335, 0.665, 110, SERIF)],
}
if "--senza-titolo" in sys.argv:  # il titolo vero (macchina da scrivere) lo mette finale.py da titoli/anima.py
    del edl["texts"]
if "--bozza" in sys.argv:  # senza look: clip originali (o proxy) con la sola LUT tecnica DJI, per giudicare clip e tempi
    LUT = HERE + "/../../../.claude/skills/youtube-edit/assets/luts/"
    CUBE = {"dlog": "DJI-Pocket4P-DLog-to-Rec709-V2.0-size33.cube", "dlog2": "DJI-Pocket4P-DLog2-to-Rec709-size65.cube"}
    for shot, s in zip(edl["shots"], cfg["shots"]):
        d = os.path.join(HERE, "..", "pocket", s["src"])
        shot["clip"] = os.path.normpath(os.path.join(d, next(f for f in sorted(os.listdir(d)) if "_%s_" % s["id"] in f))).replace("\\", "/")
        shot["src_start"] = s["start"]
        shot["grade"] = {"lut": os.path.normpath(LUT + CUBE[s["profile"]]).replace("\\", "/")}
    edl["project"]["name"] = "zanzibar-reel_bozza"
out = os.path.join(HERE, "zanzibar-reel%s.edl.json" % ("_bozza" if "--bozza" in sys.argv else ""))
json.dump(edl, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(out)
