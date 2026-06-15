# Video #4 — Talking head (scena 16) — mondo Capri

> **Scena 16 — 30–37s (~7s).** Jago MCU frontale, contatto visivo fisso, delivery piatta e stoica.
> **Battuta (lip-sync):** *"Give me one garment and one idea, and in seventy-two hours your brand has a campaign."*
> **Decisione 15/06/2026:** lo sfondo NON è più l'atelier — è il **mondo Capri**, stesso muro bianco intonacato della clip 2 (scena 6), stessa luce dorata vespro. Così la talking head resta dentro la stessa scena cinematografica delle clip Seedance.

**Metodo in 2 passaggi:**
1. **Plate** — genera l'immagine ferma chest-up (Nano Banana Pro + character sheet Jago, sfondo Capri).
2. **Animazione parlata** — anima il plate in Kling 3.0 + applica il lip-sync sulla battuta.

---

## Passaggio 1 — Plate image (Nano Banana Pro)

**Reference da allegare:** `personal-brand/assets/jago-character-sheet.jpeg` (volto/identità). NO Soul ID.

**Prompt immagine — chest-up frontale, sfondo Capri**
```
Photorealistic editorial portrait of the same man from the reference — dark wavy semi-long hair, calm composed face, thin pendant necklace. Chest-up framing, body square to camera, head frontal, eyes direct to lens. He wears a minimal fitted full-black top, nothing else, no color accents.

Setting: he stands close to a smooth whitewashed Mediterranean plaster wall, Capri register — warm pale lime-washed stone, a hard crisp cast shadow of his own silhouette on the wall behind to screen-left. A sliver of magenta bougainvillea and deep blue Tyrrhenian sea sit far out of focus in the right third as negative space, strongly blurred shallow depth of field so the face stays the protagonist.

Light: warm golden late-afternoon Mediterranean sun (the vespro hour) raking from screen-right, low and directional, hard crisp shadows, the warm light glowing on one side of the face, high contrast.

Expression stoic throughout — jaw set, mouth flat, zero upward curve, no raised cheeks, eyes direct and unwavering, effortless and self-possessed, never smiling.

Palette: black top, warm pale stone, golden light, deep blue accent — nothing else enters the frame.

Skin reads true cinematic matte — zero shine on forehead, nose bridge, cheekbones, temples, chin, real peach fuzz at the jaw and hairline, fine even pore texture, light absorbed like true subsurface scattering, warmth preserved, never plastic, never doll-skin, no blemishes. Low-contrast curve, highlights rolled off softly, nothing crushed to black. Vintage 55mm anamorphic character, oval bokeh, fine 35mm film grain, warm golden-hour grade. 9:16 vertical.
```

> Genera 3–4 varianti, tieni quella col volto più fedele al character sheet e l'espressione più stoica. Salva come `talking-head-capri-v1.png` (ecc.) in `video-4/`.

---

## Passaggio 2 — Animazione parlata (Kling 3.0, framework Dan Kieft)

**Reference da allegare:** il plate scelto al passaggio 1 (`talking-head-capri-vX.png`) come primo frame.

**Prompt video — talking head 7s**
```
FORMAT: Single continuous medium close-up talking-head shot, 9:16 vertical, ~7 seconds, locked frontal framing with a slow subtle push-in.

SUBJECT: The same man from the reference image — dark wavy semi-long hair, thin pendant necklace, minimal fitted full-black top. Chest-up, body square to camera, head frontal, eyes locked direct to lens the entire shot.

ENVIRONMENT: He stands against a smooth whitewashed Mediterranean plaster wall, Capri register — warm pale stone, his own hard cast shadow on the wall to screen-left, a strongly blurred sliver of magenta bougainvillea and deep blue sea far out of focus in the right third. The background stays fixed and stable, shallow depth of field, the face the protagonist.

STYLE ANCHOR: Warm golden late-afternoon Mediterranean light raking from screen-right, hard crisp shadows, high contrast, vintage 55mm anamorphic look, fine 35mm film grain, matte cinematic skin with zero specular shine. Expression is stoic throughout — jaw set, mouth flat apart from speech, zero upward curve, no raised cheeks, eyes direct and unwavering.

DELIVERY: He speaks the line in a flat, even, stoic register — calm, self-possessed, unhurried, no warmth, no smile, no eyebrow raises. Natural accurate mouth shapes for the words, minimal head movement, the gaze never leaving the lens.

LOGIC RULE: Expression is STOIC and LOCKED throughout — jaw set, mouth flat, no smile at any point, no pleasant expression, no softening. The background and light stay constant; only the lips, faint breath, and faint hair movement change.

NEGATIVE PROMPT: no smile, no pleasant expression, no exaggerated gestures, no head tilt, no looking away from camera, no background change, no camera shake, no on-screen text, no captions, no rendered typography, no warping of the face or hair.

ACTION: He delivers the line — "Give me one garment and one idea, and in seventy-two hours your brand has a campaign." — with stoic, still delivery, jaw set, mouth flat between words, eyes direct, zero warmth. Faint natural breath, hair lifts almost imperceptibly in the sea breeze, the cast shadow steady on the wall. Slow smooth cinematic push-in across the entire shot, from medium close-up to slightly tighter medium close-up. Stable camera, no shake, no handheld.
```

**Lip-sync:** se Kling non sincronizza bene la battuta, genera il movimento neutro e applica il **lip-sync** a parte (Kling lip-sync o HeyGen) sul voiceover inglese della battuta.

**Nota Kling "Restricted content":** se Kling blocca il plate perché immagine AI-generated, croppa l'eventuale watermark in basso a destra → se persiste, passa a **Veo** (accetta reference AI-generated). Vedi memoria `feedback_kling_higgsfield_prompts`.

---

## Checklist consistenza (prima di approvare)
- [ ] Stesso volto Jago del character sheet?
- [ ] Full black top, collana ciondolo?
- [ ] Stesso muro bianco Capri + ombra netta + bougainvillea/mare sfocati?
- [ ] Stessa luce dorata vespro che raka da destra?
- [ ] Espressione stoica, zero sorriso, occhi fissi in camera?
- [ ] Lip-sync pulito sulla battuta?
