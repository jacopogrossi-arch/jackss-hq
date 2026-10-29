"""Scrive zanzibar-reel2.edl.json da shots.json: clip gia' gradate (pellicola-oro) + curva a S, tagli netti sugli stacchi
del riferimento, spinta lenta del 5%. Niente testi, niente effetti. Le barre del cinemascope le mette finale.py.
uso: python -I edl.py [--width 3840 --height 2160]"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
cfg = json.load(open(os.path.join(HERE, "shots.json"), encoding="utf-8"))
W = int(sys.argv[sys.argv.index("--width") + 1]) if "--width" in sys.argv else 1920
H = int(sys.argv[sys.argv.index("--height") + 1]) if "--height" in sys.argv else 1080
cuts = cfg["cuts"]
# curva a S come il primo reel (Jacopo 28/10) + sharpening leggero: l'export di DJI Mimo ne mette uno, e senza il reel
# sembrava morbido accanto ai suoi export (29/10). Tarato sul 4K: in 1080 sarebbe il doppio.
GRADE = "curves=all='0/0 0.25/0.21 0.5/0.5 0.75/0.79 1/1',eq=saturation=1.12,unsharp=5:5:0.8:5:5:0"
# --jacopo: le clip col look di Jacopo (prepara_jacopo.py); la curva a S era di pellicola-oro, resta solo lo sharpening
J = "--jacopo" in sys.argv
if J:
    GRADE = "eq=saturation=1.0,unsharp=5:5:0.8:5:5:0"  # eq neutro: il lint di mh-video riconosce un "raw filter" solo cosi'
CLIP = "%s/work/shots-j/%02d-%s/graded.mp4" if J else "%s/work/shots/%02d-%s/grade/graded.mp4"

edl = {
    "version": 1,
    "project": {"name": "zanzibar-reel2", "preset": "youtube-16x9", "width": W, "height": H, "fps": 25,
                "duration": cuts[-1], "music": HERE + "/ref/riferimento.wav",
                "fade_in": 0.0, "fade_out": 1.2, "music_fade_in": 0.0, "music_fade_out": 1.3},
    "beats": {"t0": cuts[1], "period": 0.6},
    "style": {"grade": GRADE, "zoom": 0.05, "drop_flash": False, "end_flare": False, "riser": False, "boom": False, "loudness": -14},
    "shots": [{"clip": CLIP % (HERE, i + 1, s["id"]), "span": [cuts[i], cuts[i + 1]],
               "src_start": 0.0, **({"grade": GRADE + "," + s["extra"]} if s.get("extra") else {})}
              for i, s in enumerate(cfg["shots"])],
}
out = os.path.join(HERE, "zanzibar-reel2.edl.json")
json.dump(edl, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(out)
