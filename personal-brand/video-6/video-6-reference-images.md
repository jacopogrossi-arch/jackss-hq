# Reference Images — Video #6 (workflow: prima le foto, poi le clip)

**Regola di produzione:** prima di generare qualsiasi clip Seedance si generano TUTTE le foto reference — start/end frame e plate d'ambientazione — così ogni prompt video ha un'istruzione visiva chiara, non solo testuale.

Aggiornato 03/07/2026 — generazione via MCP Magnific (account by Jago).

---

## Mappa reference → clip

| # | Reference | Serve a | Stato |
|---|-----------|---------|-------|
| R1 | **Plate soundstage** (ambientazione, no persone) | Shot C1 (reveal) + prima metà Shot C unificato 10s | ✅ 2 varianti generate 03/07 (Recraft V4.1, 9:16) — **da scegliere** |
| R2 | **Plate atelier** (ambientazione, no persone) | Shot C2 + Build + Provocazione + Firma (@image2 nei prompt Seedance) | ✅ 2 varianti generate 03/07 (Recraft V4.1, 9:16) — **da scegliere** |
| R3 | **Start frame Shot A** — Talent in camicia bianca, backdrop avorio | Shot A (falso spot): risolve il gap wardrobe (la face lock ha la canotta, lo spot vuole la camicia) + identità per Shot B | ⬜ in attesa della face lock Talent confermata |
| R4 | **Start frame Shot B** — Talent a x=58%, terzo sinistro vuoto | Shot B (cazzotto): frame di partenza prima dell'ingresso di Jago | ⬜ dipende da R3 |
| R5 | **Start frame Shot C1** — Jago nel soundstage, pugno abbassato | Shot C1 / Shot C 10s: keyframe di partenza dopo il cazzotto | ⬜ dipende dalla plate R1 scelta |
| R6 | **End frame Shot C2** — Jago piantato dietro il worktable | Shot C2 (end frame) + blocking identico a Firma (e alla ex Clip 1) | ⬜ dipende dalla plate R2 scelta |

Identità già disponibili su Magnific:
- **Jago:** character sheet caricato (upload `jago-character-sheet`)
- **Talent:** ✅ risolto 03/07 — `talent-reference.png` (la verticale lockata) ricaricata su Magnific come nuova creation via URL GitHub. ⚠️ Nota: l'immagine re-inviata in chat da Jacopo era la variante ORIZZONTALE scartata ("troppo argento") — verificato visivamente e NON usata; il face lock resta la verticale del repo.

---

## R1 — Plate soundstage (✅ SCELTA 03/07: variante 2)

- Variante 1 (scartata): https://www.magnific.com/app/creation/1su9Tizr4r
- **Variante 2 (SCELTA)**: https://www.magnific.com/app/creation/l75ZdGqgv9

## R2 — Plate atelier (✅ SCELTA 03/07: variante 1)

- **Variante 1 (SCELTA)**: https://www.magnific.com/app/creation/iA7pum83uK
- Variante 2 (scartata): https://www.magnific.com/app/creation/l75Zd0fgv9

Questa plate diventa l'ancora visiva di **4 clip** (C2, Build, Provocazione, Firma).

---

## R3 — Start frame Shot A (prompt pronto)

**Modello:** Nano Banana Pro (`imagen-nano-banana-2`), 9:16, reference: face lock Talent (creation confermata).

```
Vertical cinematic still, start frame of a television commercial. The man from the reference image — identical face, identical short ash-blond side-part hair with subtle silver graying at the temples, light blue eyes — now wearing a crisp white dress shirt, top button open, no tie, no jacket, no jewelry, polished spokesperson styling. Chest-up framing occupying approximately 60% of frame height, anchored dead center, body squared to camera, shoulders open, chin level, gaze locked directly into the lens, warm confident presenter expression, lips closed and relaxed. Background: a softly blurred warm ivory seamless backdrop with a gentle out-of-focus gradient, clean empty negative space on both sides of the figure, no props, no set elements, no equipment visible — a pristine finished advertisement world. Bright high-key commercial lighting, flat and even, wraparound with no visible shadow edges. Skin reads real and matte — zero shine on forehead, nose bridge, cheekbones, temples, and chin, real peach fuzz at the jaw and hairline, real soft fine even pore texture, warmth preserved and natural, never plastic, never waxy — fine flattering texture, no blemishes. Thin atmosphere separates the figure from the blurred backdrop so he sits inside real depth. Highlights rolled off softly never clipping to white, shadows lifted gently, every surface matte and diffuse. Clean spherical 50mm at a wide aperture, natural round bokeh, mild diffusion bloom, fine grain. Photographed not generated, no on-screen text, no captions, no typography.
```

## R4 — Start frame Shot B (prompt pronto)

**Modello:** Nano Banana Pro, 9:16, reference: R3 (per camicia + backdrop + identità).

```
Vertical cinematic still, start frame. The same man from the reference image — identical face, hair, and crisp white dress shirt with top button open — now framed waist-up and anchored center-right at 58% of frame width, the left third of the frame completely empty, only the softly blurred warm ivory high-key backdrop filling that negative space. He speaks toward the lens with polished presenter posture, gaze into the camera, mid-sentence composure. Same pristine bright high-key commercial world as the reference: warm ivory seamless backdrop softly out of focus, flat even wraparound light, no visible shadow edges, no equipment, no crew, nothing but clean bright space. Skin reads real and matte — zero shine, real peach fuzz, fine even pore texture, warmth natural, never plastic — no blemishes. Thin atmosphere between figure and backdrop for real depth, highlights rolled off softly, shadows lifted gently, everything matte and diffuse. Vintage 40mm 2x anamorphic character at a wide aperture, oval bokeh, soft frame-edge falloff, light diffusion bloom, color-negative film rendition with fine grain. Photographed not generated, no on-screen text, no captions, no typography.
```

## R5 — Start frame Shot C1 (prompt pronto)

**Modello:** Nano Banana Pro, 9:16, reference: character sheet Jago + plate soundstage scelta (R1).

```
Vertical cinematic still, start frame. The man from the first reference image — identical face, dark wavy hair, olive skin — wearing a fitted black crew-neck tee and a silver pendant necklace, no jacket. Framed waist-up, anchored dead center at 50% of frame width, standing inside the dark soundstage from the second reference image: behind him the small bright ivory commercial set glows like a receding island deep in the frame, light stands with softboxes silhouetted at the left edge, a cinema camera on a tripod and a monitor cart with faintly glowing screen at the right edge, thick cables crossing dark concrete, thin haze catching the rig light. His right fist is lowered at his side just after a punch, chin lifting, gaze locked dead into the lens, expression stoic — jaw set, brow level, no smile, cold unhurried authority. Skin reads true cinematic matte — zero shine on forehead, nose bridge, cheekbones, temples, and chin, real peach fuzz at the jaw and hairline, real soft fine even pore texture, warmth preserved and natural, never plastic, never harsh — fine flattering texture, no blemishes. Light haze suspended between camera, figure, and the shrinking lit set behind him, each deeper plane softer, desaturated, lower-contrast. The backdrop glow rolls off softly never clipping to white, the soundstage blacks stay lifted and open holding texture. Vintage 40mm 2x anamorphic character at a wide aperture, oval bokeh, soft frame-edge falloff, light diffusion bloom, color-negative film rendition with fine 35mm grain, neutral dark grade holding the warm high-key island deep in frame. Photographed not generated, no on-screen text, no captions, no typography.
```

## R6 — End frame Shot C2 / blocking Firma (prompt pronto)

**Modello:** Nano Banana Pro, 9:16, reference: character sheet Jago + plate atelier scelta (R2).

```
Vertical cinematic still, end frame. The man from the first reference image — identical face, dark wavy hair, olive skin — wearing a fitted black crew-neck tee, no jacket, silver pendant necklace resting at the base of the throat. Standing centered behind the dark wooden worktable of the atelier from the second reference image, chest-up framing occupying approximately 65% of frame height, both hands resting lightly on the table's edge, shoulders squared to camera, weight even. Gaze locked directly into the camera, expression stoic and unmoved — jaw set, mouth flat, no upward curve. The worktable's edge with fashion sketches and a leather notebook crosses the lower 12% of frame; the black tailor's dress form mannequin holds soft-focus in the upper-right background; the grid-paned window casts its warm golden amber light band across his right shoulder, the rest of the room in deep brown-black chiaroscuro. Skin reads true cinematic matte — zero shine on forehead, nose bridge, cheekbones, temples, chin, and collarbones, real peach fuzz catching the window light at the jaw and hairline, real soft fine even pore texture, light absorbed like true subsurface scattering, warmth preserved and natural, never plastic, never harsh — fine flattering texture, no blemishes. Thin atmosphere between camera, subject, and the mannequin behind him, background softer and lower-contrast than the foreground. Shadows lifted gently holding texture, highlights rolled off softly never clipping on the amber band, all speculars removed from skin, hair, and fabric. Vintage 55mm 2x anamorphic character at a wide aperture, oval bokeh on the background mannequin and window, soft frame-edge falloff, light diffusion bloom, color-negative film rendition with fine 35mm grain, warm amber grade with deep brown-black shadow bias, shallow depth of field. Photographed not generated, no on-screen text, no captions, no typography.
```

---

## Uso nelle clip Seedance

- **Shot A:** @image1 = R3 (start frame). Il wardrobe camicia bianca è già nel frame — niente più mismatch canotta/camicia.
- **Shot B:** @image1 = R4 (start frame), @image2 = character sheet Jago (per l'ingresso).
- **Shot C1 / Shot C 10s:** @image1 = R5 (start frame). Per il piano B frame-chaining: end frame di B → confrontare con R5.
- **Shot C2:** @image1 = character sheet Jago, @image2 = R2 (plate atelier), end frame target = R6.
- **Build / Provocazione / Firma:** @image1 = character sheet Jago, @image2 = R2. La Firma parte dal blocking di R6.

## Vincoli di questa sessione (nota operativa)

Il policy di rete della sessione blocca download/upload diretti dai CDN Magnific: le immagini si scelgono dai link `magnific.com/app/creation/...` e i file locali del repo non sono caricabili direttamente — per usare `talent-reference.png` come reference serve re-inviarla in chat (viene importata come creation via MCP).
