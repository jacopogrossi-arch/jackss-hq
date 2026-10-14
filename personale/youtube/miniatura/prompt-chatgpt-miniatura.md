# Prompt ChatGPT — miniatura YouTube #1

> 14/10/2026. Genera la miniatura in ChatGPT (generazione immagini) partendo dai nostri asset.

## Immagini da caricare (in quest'ordine)
1. **Una tua foto vera** (spalle in su, luce buona, sguardo in camera)
2. `bozza-miniatura-e-mio.jpg` — riferimento di layout
3. `accademia/img-cinque-giacche/giacca2-sahariana-sketch.png` — sketch
4. `accademia/img-cinque-giacche/giacca2-outfit-FINALE.png` — figurino colorato

## Prompt

```
Create a YouTube thumbnail, 16:9 (1280x720).

Use image 2 as the layout reference: keep the same composition.

LEFT SIDE: the young man from image 1, from the shoulders up, looking straight into the camera with a calm, thoughtful expression (not surprised, no exaggerated face). Keep his face exactly as in the photo: same features, same hair, same skin, do not beautify or change him. Soft natural light from the side, slight film grain.

RIGHT SIDE: two fashion illustrations side by side on ivory paper cards with a thin ivory border.
- Left card: the line-art sketch from image 3 (safari jacket, black lines, uncolored).
- Right card: the colored illustration from image 4 (same jacket, beige).
Use the illustrations exactly as they are, do not redraw or change the jacket.
A small amber arrow points from the sketch to the colored version.
Under the cards, small ivory serif labels: "MANO" under the sketch, "AI" under the colored one.

TEXT: bottom left, over the man's chest, large serif text (EB Garamond style) in warm amber color: "È MIO?" — exactly this text, with the accent on the È, nothing else.

STYLE: dark background (almost black, warm brown tones), dark-academia mood: black, amber, warm wood tones, chiaroscuro. Clean and minimal, maximum 3 elements. No other text, no logos, no arrows other than the small one, no emojis.

Keep the bottom right corner empty (YouTube shows the video duration there).
```

## Se il risultato non va
- **Ti ha cambiato la faccia** → "Keep the face identical to image 1, do not modify the facial features."
- **Ha ridisegnato la giacca** → "Use images 3 and 4 as they are, as photos placed on the cards, do not redraw them."
- **Testo sbagliato** (es. "E MIO", lettere strane) → lascia stare, generala senza testo ("no text") e aggiungi "È MIO?" dopo in Canva.

---

## v2 — stile "virale clean" (14/10/2026)

La v1 (fondo scuro, due tavole, serif) è stata scartata da Jacopo: troppo scura e piena, illeggibile in piccolo.
**Allegare:** 1) una foto vera di Jacopo · 2) `giacca2-sahariana-sketch.png` · 3) `giacca2-outfit-FINALE.png`

```
Create a clean, viral-style YouTube thumbnail, 16:9 (1280x720).

COMPOSITION (only 3 elements):
1. LEFT (about 40% of the frame): the young man from image 1, cut out cleanly, from the chest up, big in the frame, slightly turned toward the right, looking into the camera with a skeptical, curious expression (one eyebrow slightly raised, subtle — not exaggerated, no open mouth). Keep his face identical to image 1. Bright, soft studio light on his face, sharp and high detail, thin white outline around him.
2. RIGHT: ONE large fashion illustration of the safari jacket, split vertically down the middle: the left half is the black line-art sketch from image 2, the right half is the colored version from image 3. A clean straight split line. Use the illustrations as they are, do not redraw the jacket. Crop from head to hips so it is big.
3. TEXT: top right, 2 words in a very bold, heavy sans-serif font (like Montserrat Black), white with a thin black outline or on a solid black block: "È MIO?" — exactly this text, accent on the È.

BACKGROUND: clean, light warm off-white / beige (#EFE8DC), plain, with a very soft shadow behind the man. No textures, no objects, no room.

STYLE: bright, high contrast, high saturation, crisp, professional YouTube thumbnail like MKBHD or Ali Abdaal. Must be readable at very small size on a phone. No other text, no arrows, no logos, no emojis.
Keep the bottom right corner empty.
```

Varianti testo: "BARARE?" · "MANO vs AI".

---

## v3 — rigenerazione senza beige e senza testo (14/10/2026)

v2 approvata come impostazione (faccia + figurino split), ma: faccia imbronciata, font Impact brutto, fondo beige da togliere. Font scelto: **EB Garamond** (È corsivo + MIO? tondo), aggiunto dopo da Claude — ChatGPT genera senza testo.
**Allegare:** 1) foto vera di Jacopo · 2) `giacca2-sahariana-sketch.png` · 3) `giacca2-outfit-FINALE.png`

```
Create a clean, viral-style YouTube thumbnail, 16:9 (1280x720).

COMPOSITION (only 2 elements + empty space):
1. LEFT (about 40% of the frame): the young man from image 1, cut out cleanly, from the chest up, big in the frame, slightly turned toward the right. Expression: curious and slightly skeptical, one eyebrow subtly raised, a hint of a smile — friendly, NOT sad, NOT pouting, mouth relaxed. Keep his face identical to image 1, do not change or beautify his features. Bright, soft studio light on his face, sharp and detailed, thin white outline around him.
2. CENTER-RIGHT: ONE large fashion illustration of the safari jacket, split vertically down the middle: the left half is the black line-art sketch from image 2, the right half is the colored version from image 3. Clean straight split line. Use the illustrations as they are, do not redraw the jacket. Crop from head to hips, big in the frame.
3. TOP RIGHT: leave an empty area (about 35% width, top 30% height) for a title that will be added later. NO TEXT anywhere in the image.

BACKGROUND: plain clean light grey-white studio background (#F2F2F0), seamless, with a very soft shadow behind the man. No beige, no textures, no objects, no room.

STYLE: bright, crisp, high contrast, minimal, professional YouTube thumbnail. Must read clearly at very small size on a phone. No text, no arrows, no logos, no emojis.
Keep the bottom right corner empty.
```

Fondi alternativi (sostituire la riga BACKGROUND): bianco puro `#FFFFFF` · oliva scuro `#3F4A2E` (palette capi Inverso, scritta in avorio).
