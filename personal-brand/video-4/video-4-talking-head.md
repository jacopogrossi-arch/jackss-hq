# Video #4 — Talking head (scena 16) — mondo Capri

> **Scena 16 — 30–37s (~7s).** Jago MCU frontale, contatto visivo fisso, delivery piatta e stoica.
> **Battuta (lip-sync):** *"Give me one garment and one idea, and in seventy-two hours your brand has a campaign."*
> **Decisione 15/06/2026:** lo sfondo NON è più l'atelier — è il **mondo Capri**, stesso muro bianco intonacato della clip 2 (scena 6), stessa luce dorata vespro. Così la talking head resta dentro la stessa scena cinematografica delle clip Seedance.
> **Prompt generati dalle skill** (15/06/2026): plate via `banana-pro-director` (Mode 3A, M1), video via `cinema-worldbuilder-pro` (M1 Narrative). Mai scritti a mano — vedi memoria `feedback_skill_prompt_generation`.

**Metodo in 2 passaggi:**
1. **Plate** — genera l'immagine ferma chest-up (Nano Banana Pro + character sheet Jago, sfondo Capri).
2. **Animazione parlata** — anima il plate + applica il lip-sync sulla battuta.

**Modello di rendering (deciso 15/06/2026):** per il parlato usare un modello avatar audio-driven, NON un I2V generico. Prima scelta in Higgsfield: **Kling AI Avatar / Speak v2** (1080p/48fps, espressione contenuta che aiuta lo stoico). Fallback realismo: **OmniHuman 1.5**. Il prompt video qui sotto resta valido come direzione scena: serve al primo frame/plate e come riferimento di delivery; il lip-sync vero lo fa il modello avatar sul VO.

---

## Passaggio 1 — Plate image (Banana Pro / Nano Banana Pro)

**Reference da allegare:** `personal-brand/assets/jago-character-sheet.jpeg` (identità Jago) → `@image1`. NO Soul ID.

**Prompt immagine — chest-up frontale, sfondo Capri** (aspect 9:16 si imposta nella UI)
```
A cinematic anamorphic still photograph captured on a real set — a frontal chest-up hero portrait of the man from the attached character reference standing close to a sunlit whitewashed plaster wall on a Mediterranean coast at the golden vespro hour, the camera at eye level square to him in a chest-up framing, his body centered and squared to the lens, the warm pale stone wall filling the frame behind him with his own hard cast shadow thrown across it, the composition holding a still, composed, self-possessed stillness.

The character carrying identically from the attached character reference — his dark wavy semi-long hair, face, and identity locked from the reference, a thin pendant necklace at his throat. He wears a minimal fitted full-black top, matte black with no accents, nothing else in frame. His shoulders are level and settled, his chin level, his gaze direct into the lens, his expression stoic and held — jaw set, mouth flat, no upward curve, no raised cheeks, calm and unwavering, never smiling, effortless and at ease in the heat.

Behind him the whitewashed Capri wall reads as warm lime-washed plaster, smooth and sunlit, his hard-edged cast shadow falling across it to screen-left where the low sun rakes him from screen-right. In the right third of the frame, far out of focus behind a shallow depth of field, a thin spill of magenta bougainvillea and a sliver of deep blue Tyrrhenian sea sit as the only color accents, strongly blurred so the face stays the protagonist. Light atmospheric haze suspended between him and the distant water gives the air real physical body, the sea rendered softer and lower-contrast than the foreground.

The warm golden late-afternoon Mediterranean light is the anchor of the frame — low, hard, directional, raking across the right side of his face and catching the matte skin and the wall in a warm glow, crisp dark shadows falling to the left, high contrast, the warm key meeting the cool blue sea-light bleeding faintly into his shadow side.

Captured with a wide-latitude cinema look and a vintage 55mm-equivalent 2x anamorphic character at a wide aperture, a light diffusion bloom softening the highlights, color-negative daylight film rendition, in an M1 cinematic narrative register. Real anamorphic optical character with oval bokeh on the blurred bougainvillea and sea, organic operator breath, soft frame-edge falloff. Real human skin — peach fuzz catching light along the jawline and hairline, fine even pore texture, subsurface scattering at the ear edges and nostrils with warm undertone bleed, true natural skin tone preserved, matte with zero specular shine on forehead, nose bridge, cheekbones, temples and chin, never plastic, never waxy, no blemishes, no harsh clinical texture, fine flattering skin that looks good and real. Hair rendered strand by strand with realistic flyaways lifting faintly in the sea breeze. Theatrical fine 35mm film grain across the entire frame — skin, plaster, haze. Warm golden-hour grade, shadows lifted gently never crushed, highlights rolled off softly never clipping. Real photographic frame captured on a real cinema camera, real anamorphic lens, real plaster wall, real human subject, real sea haze — no CGI, no rendered look, no digital cleanliness, no plastic surfaces, no AI smoothness, no skin smoothing, no glow, no glossy highlights.
```

> Genera 3–4 varianti, tieni quella col volto più fedele al character sheet e l'espressione più stoica. Salva come `talking-head-capri-v1.png` (ecc.) in `video-4/`.

---

## Passaggio 2 — Animazione parlata (modello avatar + lip-sync)

**Reference da allegare:** il plate scelto al passaggio 1 (`talking-head-capri-vX.png`) come primo frame → `@image1`.

**Seedance prompt — 7s** (direzione scena M1; il lip-sync sul VO lo fa il modello avatar)
```
Scene & Mood: A man stands against a sunlit whitewashed wall on a Mediterranean coast at the golden vespro hour and speaks one calm, controlled line straight to camera — self-possessed, expensive, unhurried. He doesn't perform; he states a fact and lets it land.

Frame Map: @image1 centered, x=50%, foreground, medium close-up from mid-chest up, his head filling the upper-center of the frame and occupying roughly 65% of frame height. His own hard cast shadow falls across the plaster wall to screen-left; a strongly blurred sliver of magenta bougainvillea and deep blue sea holds the right third as shallow-focus negative space.

Subject Lock — @image1: Face, dark wavy hair, thin pendant necklace, fitted full-black top, and silhouette identical throughout. Body squared to camera, head frontal and level, shoulders settled. Gaze locked directly into the lens the entire shot, never breaking. Expression stoic and held — jaw set, mouth flat between words, no upward curve, no raised cheeks, no eyebrow raise, calm and unwavering, never smiling. Lips move only to speak the line, mouth shapes natural and accurate.

Cross-Frame Rules: Single subject — he holds the center of the frame the full runtime, never drifts to the edges, the wall and cast shadow stay fixed behind him, the blurred bougainvillea and sea stay locked in the right third. No other figure enters.

Movement: He speaks one line across the full 7 seconds — "Give me one garment and one idea, and in seventy-two hours your brand has a campaign." — delivered flat, even, and stoic, jaw set, eyes never leaving the lens. Micro-motion only: a faint breath settling the chest between phrases, dark hair lifting almost imperceptibly in the sea breeze, a single calm blink near 4 seconds. The hard cast shadow holds steady on the wall, faint heat shimmer rising off the stone, the blurred bougainvillea trembling lightly at the right edge. Nothing else moves.

Last Frame: He holds centered, x=50%, the line just finished, mouth settling flat, gaze still locked into the lens, chest settled on the exhale, the cast shadow steady on the wall and the blue sea quiet in the right third. No on-screen text, no captions, no signage typography, no rendered text in the frame.

World Plate: Anchored to @image1 — minimal whitewashed Mediterranean coastal architecture, a smooth warm lime-washed plaster wall, magenta bougainvillea and deep blue Tyrrhenian sea far out of focus behind. Late-afternoon golden vespro sun raking from screen-right, hard crisp shadows, clear sky, high contrast.

Sound Bed: Diegetic only — a calm, even male voice speaking the line in frame, soft sea breeze, distant waves and faint gulls, light fabric stir, no music, no other dialogue.

Capture Realism: The figure sits inside real depth — light haze suspended in the air between camera, subject, and the distant sea, the far water rendered softer, desaturated, and lower-contrast than the foreground so he sits within the air rather than pasted on a flat plane. Skin reads true cinematic matte — zero shine on forehead, nose bridge, cheekbones, temples, chin, and collarbones, real peach fuzz catching light at the jaw and hairline, real soft fine even pore texture, light absorbed like true subsurface scattering, warmth preserved and natural, slightly desaturated but never pale or washed-out, never plastic, never doll-skin, never harsh — no blemishes, no enlarged pores, fine flattering texture that keeps the face looking good. Low-contrast curve — shadows lifted gently holding texture, highlights rolled off softly never clipping to white, nothing crushed to black. All specular highlights surgically removed from skin, hair, and fabric, every pixel reading matte and diffuse. Slightly desaturated grade with warmth preserved.

Camera Capture: wide-latitude cinema capture, vintage 75mm 2x anamorphic character at a wide aperture — oval bokeh, soft frame-edge falloff — light diffusion bloom softening highlights, stable camera with an extremely slow push-in from medium close-up to slightly tighter medium close-up, no handheld shake, color-negative daylight film rendition with fine 35mm grain, warm golden-hour grade, shallow depth of field, 24fps 180° shutter, 7 seconds.
```

**Lip-sync:** la battuta è già inclusa nel prompt così le labbra si muovono. Per la sincronia pulita, applica il VO inglese al modello avatar (**Kling AI Avatar / Speak v2** → fallback **OmniHuman 1.5**). Tieni lo sfondo del plate pulito (il nostro Capri è a shallow DoF, ✓) e il plate chest-up frontale ben illuminato (✓).

**Nota "Restricted content":** se Kling blocca il plate perché immagine AI-generated, croppa l'eventuale watermark in basso a destra → se persiste, passa a **Veo/OmniHuman** (accettano reference AI-generated). Vedi memoria `feedback_kling_higgsfield_prompts`.

---

## Checklist consistenza (prima di approvare)
- [ ] Stesso volto Jago del character sheet?
- [ ] Full black top, collana ciondolo?
- [ ] Stesso muro bianco Capri + ombra netta + bougainvillea/mare sfocati?
- [ ] Stessa luce dorata vespro che raka da destra?
- [ ] Espressione stoica, zero sorriso, occhi fissi in camera?
- [ ] Lip-sync pulito sulla battuta?
