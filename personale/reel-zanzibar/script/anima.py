"""Prove animate del titolo sull'apertura vera del reel (clip 1 gradata + contrasto, musica): 4, 9 e ibrido 4+9.
uso: python -I anima.py  ->  prova-4.mp4, prova-9.mp4, prova-4+9.mp4"""
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib.util
spec = importlib.util.spec_from_file_location("t", os.path.join(os.path.dirname(os.path.abspath(__file__)), "titoli.py"))
HERE = os.path.dirname(os.path.abspath(__file__))
REEL = os.path.dirname(HERE)

# only the helpers of titoli.py, without running its 20 designs
src = open(os.path.join(HERE, "titoli.py"), encoding="utf-8").read().split("designs = []")[0]
T = {"__file__": os.path.join(HERE, "titoli.py"), "__name__": "t"}
exec(compile(src, "titoli.py", "exec"), T)
font, put, width, layer, IVORY, W, H = T["font"], T["put"], T["width"], T["layer"], T["IVORY"], T["W"], T["H"]
AG, UF = T["AG"], T["UF"]
S = 2 if "--4k" in sys.argv else 1      # 4K: everything drawn at twice the size (sharp text, not an upscale)
W, H = 1920 * S, 1080 * S
T["W"], T["H"] = W, H

FPS, DUR = 25, 5.409
CLIP = os.path.join(REEL, "work", "shots", "01-0008", "grade", "graded.mp4")
GRADE = "scale=%d:%d," % (W, H) + "curves=all='0/0 0.25/0.21 0.5/0.5 0.75/0.79 1/1',eq=saturation=1.12"

# centre veil, computed once (same as titoli.veil 'center', 0.4)
VEIL = Image.new("L", (W, H))
for i in range(H):
    a = 1 - abs(i / H - 0.5) * 2
    VEIL.paste(int(255 * 0.4 * a ** 2), (0, i, W, i + 1))
BLACK = Image.new("RGB", (W, H))


def ease(x):
    x = min(max(x, 0.0), 1.0)
    return 1 - (1 - x) ** 3


def ramp(t, a, b):
    return ease((t - a) / (b - a))


def fade_out(t):
    return 1 - ramp(t, 4.7, 5.3)


def shade(l, r=12, o=0.55):
    a = l.getchannel("A").filter(ImageFilter.GaussianBlur(r * S)).point(lambda v: int(v * o))
    s = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    s.putalpha(a)
    return s


def rising(word, f, cx, base, line_y, t, t0, track, stagger=0.06, dur=0.7, out=1.0):
    """Letters rise from under a line, one after another; nothing is drawn below the line."""
    l = layer()
    x = cx - width(word, f, track) / 2
    hgt = f.getbbox("Z")[3] - f.getbbox("Z")[1]
    for i, c in enumerate(word):
        p = ramp(t, t0 + i * stagger, t0 + i * stagger + dur)
        put(l, c, f, x, base + (1 - p) * (hgt + 20), IVORY, alpha=int(255 * min(1, p * 1.5) * out))
        x += f.getlength(c) + track
    l.paste((0, 0, 0, 0), (0, int(line_y), W, H))
    return l


def line(t, a, b, y, half, out):
    l = layer()
    p = ramp(t, a, b)
    if p > 0:
        ImageDraw.Draw(l).line((W / 2 - half * p, y, W / 2 + half * p, y), fill=IVORY + (int(220 * out),), width=2 * S)
    return l


def v4(t):
    out = fade_out(t)
    l = layer()
    tr = 12 + 8 * ramp(t, 0.3, 2.0)
    put(l, "THE BEAUTY OF", font(UF + "HelveticaNeueLight.otf", 40), W / 2, 450, IVORY, track=tr, anchor="c",
        alpha=int(255 * ramp(t, 0.3, 1.2) * out))
    p = ramp(t, 1.0, 2.6)
    put(l, "ZANZIBAR", font(AG + "AppleGaramond.ttf", 170), W / 2, 640, IVORY, track=60 - 26 * p, anchor="c",
        alpha=int(255 * p * out))
    return [shade(l), l, line(t, 2.3, 3.0, 700, 60, out)]


def v9(t):
    """Messa a fuoco: ZANZIBAR parte grande e sfocato e si stringe a fuoco (atterra a 2,4 s)."""
    out = fade_out(t)
    l = layer()
    put(l, "the beauty of", font(UF + "HelveticaNeueLight.otf", 48), W / 2, 440, IVORY, track=10, anchor="c",
        alpha=int(255 * ramp(t, 0.4, 1.3) * out))
    sm = ramp(t, 0.4, 1.3)
    if sm < 1:
        l = l.filter(ImageFilter.GaussianBlur(8 * (1 - sm)))
    z = layer()
    p = ramp(t, 1.0, 2.4)
    if p > 0:
        put(z, "ZANZIBAR", font(UF + "HelveticaNeueBold.otf", 200), W / 2, 700, IVORY, track=10, anchor="c",
            alpha=int(255 * min(1, p * 1.4) * out))
        k = 1.35 - 0.35 * p
        big = z.resize((int(W * k), int(H * k)), Image.BICUBIC)
        z = big.crop(((big.width - W) // 2, (big.height - H) // 2, (big.width - W) // 2 + W, (big.height - H) // 2 + H))
        if p < 1:
            z = z.filter(ImageFilter.GaussianBlur(22 * (1 - p)))
    return [shade(l), shade(z), l, z]


def v49(t):
    out = fade_out(t)
    l = layer()
    put(l, "THE BEAUTY OF", font(UF + "HelveticaNeueLight.otf", 40), W / 2, 450, IVORY, track=20, anchor="c",
        alpha=int(255 * ramp(t, 0.3, 1.1) * out))
    z = rising("ZANZIBAR", font(AG + "AppleGaramond.ttf", 170), W / 2, 640, 660, t, 1.2, 34, stagger=0.07, dur=0.8, out=out)
    return [shade(l), shade(z), l, z, line(t, 0.8, 1.4, 660, 330, out)]


TOP, ZAN = "THE BEAUTY OF", "ZANZIBAR"
T_TOP, T_ZAN = [0.45 + i * 0.075 for i in range(len(TOP))], [1.75 + i * 0.13 for i in range(len(ZAN))]


def typed(lay, text, times, f, cx, y, track, t, out):
    """Letters appear at their final place when their key is struck; returns x after the last visible letter."""
    x = cx - width(text, f, track) / 2
    for c, tc in zip(text, times):
        if t < tc:
            break
        put(lay, c, f, x, y, IVORY, alpha=int(255 * out))
        x += f.getlength(c) + track
    return x


def v4t(t):
    """Typewriter in the 4 style: THE BEAUTY OF typed fast, ZANZIBAR typed slower, cursor, then the thin rule."""
    out = fade_out(t)
    l = layer()
    f1, f2 = font(UF + "HelveticaNeueLight.otf", 40 * S), font(AG + "AppleGaramond.ttf", 170 * S)
    x1 = typed(l, TOP, T_TOP, f1, W / 2, 450 * S, 20 * S, t, out)
    x2 = typed(l, ZAN, T_ZAN, f2, W / 2, 640 * S, 34 * S, t, out)
    d = ImageDraw.Draw(l)
    blink = int(t * 2.5) % 2 == 0
    if T_TOP[0] <= t < T_ZAN[0] - 0.15 and (t < T_TOP[-1] or blink):
        d.rectangle((x1 + 4 * S, 416 * S, x1 + 6 * S, 456 * S), fill=IVORY + (int(230 * out),))
    elif T_ZAN[0] - 0.15 <= t < T_ZAN[-1] + 0.9 and (t < T_ZAN[-1] or blink):
        d.rectangle((x2 + 6 * S, 520 * S, x2 + 10 * S, 648 * S), fill=IVORY + (int(230 * out),))
    return [shade(l), l, line(t, T_ZAN[-1] + 0.9, T_ZAN[-1] + 1.5, 700 * S, 60 * S, out)]


def typewriter_track():
    """One key strike of a real antique typewriter (Sonniss GDC 2026, 344 Audio) per letter, a softer one per space,
    slightly varied in pitch and level so it does not sound like a loop."""
    import numpy as np, librosa, soundfile as sf
    sr = 48000
    key, _ = librosa.load("D:/download/Sonniss GDC 2026/344 Audio - Antique Typewriter/"
                          "COMType_Typewriter Space Key, Typewriter 05_344 Audio_Antiques - Typewriter.wav", sr=sr, mono=True)
    key = key / (np.abs(key).max() + 1e-9)
    track = np.zeros(int(sr * DUR) + sr)
    rng = np.random.default_rng(7)
    for text, times, level in ((TOP, T_TOP, 0.22), (ZAN, T_ZAN, 0.34)):
        for c, tc in zip(text, times):
            k = librosa.effects.pitch_shift(key, sr=sr, n_steps=float(rng.uniform(-1.2, 1.2)))
            g = level * (0.55 if c == " " else rng.uniform(0.85, 1.1))
            s = int((tc - 0.05) * sr)          # the strike sits 0.05 s into the file
            track[s:s + len(k)] += g * k[:len(track) - s]
    path = os.path.join(HERE, "typewriter-sfx.wav")
    sf.write(path, track[:int(sr * DUR)], sr)
    return path


SFX = os.path.join(REEL, "..", "..", "..", ".claude", "skills", "youtube-edit", "assets", "sfx")
SOUNDS = {
    # 4: eleganza lenta -> soffio etereo che accompagna le lettere che si stringono + luccichio sottile sulla riga
    "4": [("mixclap/whoosh-ethereal.mp3", 0.25, 0.25, 3.0), ("core/sparkle.mp3", 2.3, 0.18, 1.2)],
    # 9: messa a fuoco -> piatto al contrario che sale fino all'atterraggio (2,4 s) + colpo basso morbido quando e' a fuoco
    "9": [("mixclap/reverse-cymbal.mp3", 0.8, 0.36, 1.6), ("core/impact-bass-1.mp3", 2.4, 0.35, 1.4)],
}


def mix(video, name):
    """Music + the version's sounds (delayed, faded), into the final file."""
    ins, chain = ["-i", video, "-i", os.path.join(REEL, "ref", "riferimento.wav")], ["[1:a]atrim=0:%s[m]" % DUR]
    for k, (f, at, vol, keep) in enumerate(SOUNDS[name]):
        ins += ["-i", os.path.join(SFX, f)]
        chain.append("[%d:a]atrim=0:%s,afade=t=out:st=%s:d=0.4,volume=%s,adelay=%d:all=1[s%d]"
                     % (k + 2, keep, max(keep - 0.4, 0), vol, int(at * 1000), k))
    labels = "[m]" + "".join("[s%d]" % k for k in range(len(SOUNDS[name])))
    chain.append("%samix=inputs=%d:normalize=0:duration=first[a]" % (labels, len(SOUNDS[name]) + 1))
    out = video.replace("-muto.mp4", ".mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y"] + ins + ["-filter_complex", ";".join(chain), "-map", "0:v", "-map", "[a]",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", str(DUR), out], check=True)
    return out


SOUNDS["4t"] = [(typewriter_track(), 0.0, 1.0, DUR)]
for name, fn in (("4t", v4t),):
    out = os.path.join(HERE, "prova-%s%s-muto.mp4" % (name, "-4k" if S == 2 else ""))
    # frames are read one at a time: 135 frames of 4K RGB would be 3,4 GB in memory
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", CLIP, "-t", str(DUR), "-vf", GRADE + ",fps=%d" % FPS,
                            "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "%dx%d" % (W, H),
                            "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    n = 0
    while True:
        raw = dec.stdout.read(W * H * 3)
        if len(raw) < W * H * 3:
            break
        t = n / FPS
        n += 1
        bg = Image.frombytes("RGB", (W, H), raw)
        img = Image.composite(BLACK, bg, VEIL).convert("RGBA")
        for lay in fn(t):
            img = Image.alpha_composite(img, lay)
        enc.stdin.write(img.convert("RGB").tobytes())
    enc.stdin.close()
    enc.wait()
    dec.wait()
    print(mix(out, name), n, "fotogrammi")
