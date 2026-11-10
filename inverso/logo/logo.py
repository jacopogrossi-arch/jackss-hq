"""Logo definitivo INVERSO (10/11/2026): disegno del logo di prima (origine.svg),
I romana con linee staccate sopra e sotto, E normale, spazio uniforme 20 tra le lettere.
Uso: python logo.py  -> rigenera inverso-logo.svg in questa cartella."""
import re
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE / "origine.svg"  # logo di prima (render AI vettorializzato)
CREMA = "#EDE6D6"

svg = SRC.read_text(encoding="utf-8")
paths = dict(re.findall(r'<path id="letter-(\w)"[^>]*?d="([^"]+)"', svg))
evenodd = {"r", "o"}
# bordi orizzontali di ogni lettera nel disegno originale
BOX = {"i": (101, 163), "n": (209, 369), "v": (406, 565), "e": (603, 728),
       "r": (771, 912), "s": (948, 1047), "o": (1085, 1242)}
ORDER = "inverso"
TOP, BOT = 288, 435


def letter(k, dx=0, mirror=False):
    fr = ' fill-rule="evenodd"' if k in evenodd else ""
    p = f'<path{fr} d="{paths[k]}"/>'
    if mirror:
        a, b = BOX[k]
        p = f'<g transform="translate({a + b} 0) scale(-1 1)">{p}</g>'
    return f'<g transform="translate({dx} 0)">{p}</g>'


def roman_bars(dx, half, thick, gap=0):
    """Barre del numero romano sulla I: half = mezza larghezza, gap = distacco dalla lettera."""
    cx = (BOX["i"][0] + BOX["i"][1]) / 2 + dx
    x0, w = cx - half, half * 2
    if gap == 0:
        return (f'<rect x="{x0}" y="{TOP}" width="{w}" height="{thick}"/>'
                f'<rect x="{x0}" y="{BOT - thick}" width="{w}" height="{thick}"/>')
    return (f'<rect x="{x0}" y="{TOP - gap - thick}" width="{w}" height="{thick}"/>'
            f'<rect x="{x0}" y="{BOT + gap}" width="{w}" height="{thick}"/>')


def spaced(gap):
    """Spaziatura ottica uniforme: stessa distanza tra tutte le lettere, parola ricentrata."""
    widths = [BOX[k][1] - BOX[k][0] for k in ORDER]
    total = sum(widths) + gap * 6
    x = (1344 - total) / 2
    dxs = {}
    for k, w in zip(ORDER, widths):
        dxs[k] = x - BOX[k][0]
        x += w + gap
    return dxs


def build(name, dxs, bars, stroke=0, note="", mirror_e=True):
    body = "".join(letter(k, dxs.get(k, 0), mirror=(mirror_e and k == "e")) for k in ORDER)
    st = f' stroke="{CREMA}" stroke-width="{stroke}" stroke-linejoin="round"' if stroke else ""
    out = (f'<svg viewBox="0 0 1344 752" width="1344" height="752" xmlns="http://www.w3.org/2000/svg">\n'
           f'  <title>INVERSO — {note}</title>\n  <rect width="1344" height="752" fill="#000"/>\n'
           f'  <g fill="{CREMA}"{st} transform="translate(0 14)">{body}{bars}</g>\n</svg>\n')
    (HERE / f"{name}.svg").write_text(out, encoding="utf-8")


t = spaced(20)
build("inverso-logo", t, roman_bars(t["i"], 38, 5, gap=10), note="logo finale Inverso (10/11/2026)", mirror_e=False)
print("ok")
