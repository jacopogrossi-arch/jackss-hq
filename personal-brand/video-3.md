# Video #3 — "A Fashion Lookbook — Built with AI"

**Status: in produzione** — immagini lookbook ✅ generate, Seedance prompts ✅ pronti

Durata: ~33s | Lingua: inglese | Formato: 9:16 vertical

**Concept:** dimostra il servizio AI Lookbook con un hook sul contrasto costo/valore. Non presuppone che lo spettatore conosca Jago — funziona per chiunque nel fashion. Obiettivo primario: audience e follower. Secondario: generare richieste del servizio.

---

## Script voiceover

> *"Stone Island spends €20,000 on a lookbook like this. I spent zero."*
>
> *"Same quality. One afternoon."*
>
> *"Here's how."*
>
> *"I start with a creative brief. Concept. Mood. Lighting. Camera angles. Poses. Written with AI. Every decision locked before I open a single tool."*
>
> *"Then I generate. One character. Five looks. Campaign-quality."*
>
> *"Every visual stays coherent because the brief was coherent."*
>
> *"No photographer. No studio. No model."*
>
> *"This isn't AI-generated content."*
>
> *"This is what fashion production looks like when you use AI as a creative director."*
>
> *"Comment 'LOOKBOOK'. I'll send you the full system."*

---

## Brief scene-by-scene

| Scena | Durata | Tool | Descrizione visiva | Audio |
|---|---|---|---|---|
| **1 — Hook** (Talking Head) | 6s | Kling 3.0 Avatar | Jago MCU frontale, atelier dark-luxury. Consegna piatta, stoica. Pausa prima di "I built one in an afternoon." | *"A fashion lookbook costs €5,000. I built one in an afternoon."* |
| **2 — Lookbook montage** | 10s | HiggsField + Seedance 2.0 | 5 tagli rapidi (~2s cad.) — immagini campaign-quality dark-luxury. Jago che indossa i capi, editorial shots. Nessun testo sullo schermo. | *"No photographer. No studio. No model."* |
| **3 — Process flash** | 5s | Screen rec | Schermata tool con prompt visibile → output immagine. Veloce, non spiegato. Tool visibile ma non nominato. | *(silenzio)* |
| **4 — Reveal** | 5s | Screen rec / Canva | Griglia delle immagini finali a schermo intero — proof del deliverable completo. | *"This is what AI does to fashion production."* |
| **5 — CTA** (Talking Head) | 7s | Kling 3.0 Avatar | Jago frontale, MCU, stesso atelier. Stoico. Tiene il contatto visivo 1-2s dopo l'ultima parola. | *"Comment 'LOOKBOOK' if you want yours."* |

**Durata totale: ~33s**

---

## Note produzione

**Scene 1 e 5 — Talking Head**
- Reference immagine: `hf_20260531_185739_f3fc7fb6-e5e8-483d-bb12-11b7e09a33da.png` (stesso Video #1 e #2)
- Framework Dan Kieft: FORMAT / SUBJECT / ENVIRONMENT / STYLE ANCHOR / DELIVERY / LOGIC RULE / NEGATIVE PROMPT / ACTION
- Ridondanza obbligatoria su espressione stoica in LOGIC RULE e NEGATIVE PROMPT
- Lip sync attivo in Kling 3.0
- Scena 1: pausa lunga e deliberata tra "€5,000." e "I built one in an afternoon." — è lì che sta la tensione

**Scena 2 — Lookbook montage**
- 5 shot da ~2s ciascuno, tagli netti
- Immagini selezionate per il montage (una per look):
  - Shot 1 Look 1: `af0a92cd` — bust, vicolo romano, amber chiaroscuro
  - Shot 2 Look 2: `eb69b9bc` — bust, scalone palazzo, luce laterale cool
  - Shot 3 Look 3: `d26553b8` — full body, campagna tramonto, golden raking
  - Shot 4 Look 4: `28cd9162` — full body, libreria scura, amber lamp
  - Shot 5 Look 5: `54170ff3` — full body, atelier, pantaloni extremely wide

**Scena 3 — Process flash**
- Screen rec di HiggsField con prompt visibile (solo 2-3 secondi)
- Taglio immediato sull'output — il contrasto "testo grezzo → immagine fashion" è il punto
- Silenzio totale — lascia respirare prima della CTA

**Scena 4 — Reveal**
- Griglia Canva o schermo con tutte le immagini finali affiancate
- Deve sembrare un deliverable professionale, non uno screenshot
- Voiceover piatto sopra la griglia

---

## Asset richiesti

| Asset | File / Link | Status |
|---|---|---|
| Lookbook images (~20 foto) | `C:\Users\Jacopo Grossi\Downloads\lookbok\` | ✅ Generato |
| Seedance prompts (Scena 2) | Vedi sezione sotto | ✅ Pronti |
| Clip animati Seedance x5 | Seedance 2.0 I2V | ⬜ Da generare |
| Screen rec process (Scena 3) | HiggsField screen rec | ⬜ Da registrare |
| Lookbook grid Canva (Scena 4) | Canva | ⬜ Da creare |
| Talking head Scena 1 | Kling 3.0 Avatar | ⬜ Da generare |
| Talking head Scena 5 | Kling 3.0 Avatar | ⬜ Da generare |

---

## Ordine di produzione

1. ✅ **Genera immagini lookbook** — HiggsField Soul ID, ~20 immagini, 5 look
2. ⬜ **Anima immagini** — Seedance 2.0 I2V, push-in lento su 5 shot (~2-3s ciascuno)
3. ⬜ **Scena 3** — screen rec HiggsField con prompt → output
4. ⬜ **Scena 4** — griglia Canva con le immagini finali
5. ⬜ **Scene 1 e 5** — Kling 3.0 Avatar talking head con lip sync
6. ⬜ **Montaggio CapCut** — ordine: 1→2→3→4→5

---

## Seedance prompts — Scena 2

Ogni prompt va incollato in Seedance 2.0 con **una sola immagine** allegata (quella indicata).

### Shot 1 — Look 1 The Core | `af0a92cd` | 2s

```
Scene & Mood: A still stoic figure holds position in a narrow Roman alley at night as the camera slowly advances — warm amber lamp light carving one side of the frame, wet cobblestones glowing below.

Frame Map: @image1 centered foreground, chest-up framing occupying 60% of frame height. Right edge holds the amber lamp source. Left side falls into deep shadow. Wet alley recedes into darkness behind.

Subject Lock — @image1: Face, hair, black tee, indigo jeans, square-frame sunglasses, chain necklace with pendant identical throughout. Body squared toward camera, arms loose. Jaw set, expression stoic and unreadable, no softness. Eyes directed slightly past camera — no gaze break, no expression shift across the runtime.

Cross-Frame Rules: Single subject. @image1 holds centered throughout. No drift.

Movement: @image1 holds completely still — only a single slow controlled exhale, chest barely rising. Hair still, no wind. Amber lamp holds steady with no flicker. The camera executes a slow controlled frontal push-in closing distance smoothly at a minimal pace across the full runtime.

Last Frame: Camera has advanced to a tighter chest-up of @image1, face and collarbone filling more of the frame, amber light reading on the right jaw, chain necklace visible at the collarbone, wet alley wall further softened behind. No on-screen text, no captions, no signage typography, no rendered text in the frame.

World Plate: Narrow ancient Roman cobblestone alley at night — wet lastricato stones reflecting amber lamp glow in distorted patches, damp stone walls on both sides, warm iron street lamp at upper right casting the primary amber key, alley curving into darkness beyond.

Sound Bed: Diegetic only — distant city ambience, faint wet stone drip, subtle lamp hum, no footsteps, no wind, no music, no dialogue.

Capture Realism: @image1 sits inside real depth — thin atmosphere suspended between camera, subject, and the wet stone wall behind, background rendered softer and lower-contrast so the figure sits within the air. Skin reads true cinematic matte — zero shine on forehead, nose bridge, cheekbones, temples, chin — real peach fuzz at jaw and hairline, real soft fine even pore texture, subsurface scattering, warmth preserved, never plastic, never harsh, no acne, no blemishes, fine flattering texture. Low-contrast curve — shadows lifted gently, highlights rolled off softly, nothing clipping. All specular highlights removed from skin, hair, denim, stone. Slightly desaturated grade with amber warmth preserved.

Camera Capture: wide-latitude cinema capture, vintage 75mm 2x anamorphic character at a wide aperture — oval bokeh, soft frame-edge falloff — light diffusion bloom lifting the amber practical into soft warm halation, slow controlled frontal push-in with minimal operator breath, color-negative daylight film rendition pushed toward amber and deep shadow with fine 35mm grain, teal-amber grade, 24fps 180° shutter, 2 seconds.
```

### Shot 2 — Look 2 Layered | `eb69b9bc` | 2s

```
Scene & Mood: A composed figure stands mid-staircase in a grand Italian palazzo, cool lateral window light raking across one shoulder, the camera climbing slowly toward the face as marble and iron architecture recede into atmosphere behind.

Frame Map: @image1 centered foreground, three-quarter bust framing occupying 65% of frame height. Ornate iron balustrade visible at left. Arched window light source at upper right casting a wide lateral cool beam. Marble steps recede upward into soft background.

Subject Lock — @image1: Face, hair, dark charcoal wool jacket, white shirt, chain necklace, woven tan leather bag, and silhouette identical throughout. Body angled three-quarters toward camera, one hand on the balustrade. Jaw set, expression fully stoic — no smile, no warmth, no break. Gaze level past camera. No weight shift, no step, no head turn.

Cross-Frame Rules: Single subject. @image1 holds centered throughout. No drift.

Movement: @image1 holds still — single slow breath, chest barely rising. Wool jacket fabric completely still. Chain necklace motionless. Fine dust particles drift almost imperceptibly in the lateral window light shaft. Camera executes a slow controlled upward push-in, advancing toward the face from a chest-height start and climbing slightly so the face gains prominence by end of runtime.

Last Frame: Camera has advanced and risen — @image1 in a tight bust framing, face and jacket collar filling the frame, cool lateral window light reading clearly on the left shoulder and jaw, marble balustrade softened in background, arched window glow at upper right edge. No on-screen text, no captions, no signage typography, no rendered text in the frame.

World Plate: Grand Italian palazzo marble staircase — white marble steps worn at center, ornate wrought-iron balustrade with dark aged patina, tall arched window at the upper landing casting wide lateral cool light, fine dust in the shaft, warm golden ambient from marble walls deeper in the palazzo.

Sound Bed: Diegetic only — faint marble echo, very distant palazzo ambient, deep interior stillness, no footsteps, no wind, no music, no dialogue.

Capture Realism: @image1 sits inside real depth — light atmosphere suspended between camera, subject, and the marble staircase behind, background rendered softer, desaturated, lower-contrast so the figure reads within the air. Skin reads true cinematic matte — zero shine on forehead, nose bridge, cheekbones, temples, chin — real peach fuzz at jaw and hairline, fine soft even pore texture, subsurface scattering, warmth preserved, never plastic, never harsh, fine flattering texture. Low-contrast curve — shadows lifted gently, highlights rolled off softly from the window light, nothing clipping. All specular highlights removed from skin, hair, fabric, marble. Slightly desaturated grade with cool window key and warm marble ambient preserved.

Camera Capture: wide-latitude cinema capture, vintage 75mm 2x anamorphic character at a wide aperture — oval bokeh, soft frame-edge falloff — light diffusion bloom on the window light source, slow controlled upward push-in with minimal operator breath, color-negative daylight film rendition with fine 35mm grain, teal-amber grade, 24fps 180° shutter, 2 seconds.
```

### Shot 3 — Look 3 Utility | `d26553b8` | 3s

```
Scene & Mood: A lone figure stands anchored in the Italian countryside at golden hour, raking sunset light cutting hard across one side, as the camera drifts slowly in from the right and the golden horizon narrows behind.

Frame Map: @image1 anchored in the left third, x=30%, foreground, full-body framing occupying 70% of frame height. Open countryside and low ridge horizon fill the right two-thirds as negative space. Golden sky above, dry bleached grass below. Camera push-in closes from screen-right, the horizon compressing slightly as it advances.

Subject Lock — @image1: Face, hair, olive wide-leg cargo trousers, black fitted tee, black texan boots, square-frame sunglasses, chain necklace, and silhouette identical throughout. Body turned slightly from camera, weight settled on the back foot, arms loose at sides. Jaw set, expression stoic behind the sunglasses. Boots planted on the same dry ground marks across the full runtime. No weight shift, no step, no head turn.

Cross-Frame Rules: Single subject. @image1 holds the left third throughout. No drift from the left anchor.

Movement: @image1 holds still — boots planted, posture held. Only breath moves, barely visible against the fitted tee. Raking golden light from screen-right stays fixed and directional with no flicker. Dry grass in the foreground catches a very faint breath of air, a few individual strands moving at the bottom of the frame. Camera executes a slow lateral push-in from screen-right, advancing and very slightly narrowing its angle toward @image1 across the runtime, keeping the golden sunset horizon in the right portion of the frame throughout.

Last Frame: Camera has advanced from the right — @image1 occupies a larger portion of the left frame, golden horizon compressed into the right third, raking sunset light still reading hard on the right side of the figure, dry grass in foreground blurred softly. No on-screen text, no captions, no signage typography, no rendered text in the frame.

World Plate: Open Italian countryside at golden hour — dry bleached grass foreground, cracked pale earth, flat open farmland receding to a low rolling ridge at the horizon, warm golden-amber raking light from screen-right casting long horizontal shadows across the ground, sky grading from deep amber at the horizon to pale blue overhead.

Sound Bed: Diegetic only — very faint dry-grass rustle in the foreground, distant open-field ambient, no footsteps, no wind gust, no music, no dialogue.

Capture Realism: @image1 sits inside real depth — fine golden-dust haze suspended in the air between camera, subject, and the far countryside horizon, distant hills rendered softer, desaturated, lower-contrast than the foreground figure. Skin reads true cinematic matte — zero shine on forehead, nose bridge, cheekbones, temples, chin — real peach fuzz catching the raking golden light at the jaw and hairline, fine soft even pore texture, subsurface scattering, warmth preserved at the true golden-hour register, never plastic, never harsh, fine flattering texture. Low-contrast curve — shadows lifted gently, highlights rolled off softly from the raking key, nothing clipping. All specular highlights removed from skin, hair, fabric, ground. Warm amber grade preserved with slightly desaturated distant planes.

Camera Capture: wide-latitude cinema capture, vintage 55mm 2x anamorphic character at a wide aperture — oval bokeh on the far countryside, soft frame-edge falloff — light diffusion bloom on the raking sun source, slow controlled lateral push-in from screen-right with minimal operator breath, color-negative daylight film rendition pushed toward warm amber with fine 35mm grain, warm amber grade, 24fps 180° shutter, 3 seconds.
```

### Shot 4 — Look 4 Ivory Contrast | `28cd9162` | 2s

```
Scene & Mood: A figure stands composed in a dim scholarly studio, a single amber lamp cutting hard across one side, as the camera advances slowly through the low light toward the ivory-and-black silhouette.

Frame Map: @image1 in the right third, foreground, full-body framing occupying 65% of frame height. Tall dark bookshelf fills the background behind the subject. Amber reading lamp key enters from screen-right off-frame, its pool catching the right side of the figure and nearest shelf edge. Left side and center hold in deep shadow as negative space.

Subject Lock — @image1: Face, hair, ivory crewneck knit sweater, wide-leg black tailored trousers, dark loafers, chain necklace, wristwatch, and silhouette identical throughout. Body upright and still, one hand resting against the bookshelf edge. Jaw set, expression stoic, gaze directed level toward camera. No weight shift, no step, no head turn. Feet planted on the same floor marks.

Cross-Frame Rules: Single subject. @image1 holds the right third throughout. No drift.

Movement: @image1 holds completely still — single controlled breath, chest barely rising against the ivory knit. Amber lamp key holds steady with no flicker. Bookshelf spines remain motionless in the deep shadow. Camera executes a slow controlled frontal push-in, advancing toward the figure through the low amber light, closing distance smoothly across the full runtime.

Last Frame: Camera has advanced — @image1 in a tighter waist-up framing, ivory crewneck and face more prominent, amber key reading clearly on the right jaw and knit texture, bookshelf receding into soft shadow behind. No on-screen text, no captions, no signage typography, no rendered text in the frame.

World Plate: Dim private studio interior at night — tall floor-to-ceiling dark wood bookshelves with leather-bound volumes, a single amber reading lamp off-frame right casting a narrow hard key, deep shadow filling most of the room, warm amber pool on the floor at the figure's feet, far wall in near-black.

Sound Bed: Diegetic only — very faint room tone, subtle lamp hum, deep interior stillness, no footsteps, no pages turning, no music, no dialogue.

Capture Realism: @image1 sits inside real depth — thin atmosphere suspended between camera, subject, and the dark bookshelf behind, background rendered softer and lower-contrast so the figure sits within the room's air. Skin reads true cinematic matte — zero shine on forehead, nose bridge, cheekbones, temples, chin — real peach fuzz at jaw and hairline, fine soft even pore texture, subsurface scattering with warm amber undertone bleed reading as semi-translucent biology, warmth preserved, never plastic, never harsh, fine flattering texture. Low-contrast curve — shadows lifted gently holding open detail in the deep blue-charcoal shadow register, highlights rolled off softly from the amber key, nothing clipping. All specular highlights removed from skin, hair, ivory knit, bookshelf surfaces. Deep low-contrast tungsten-leaning grade with amber warmth preserved.

Camera Capture: wide-latitude cinema capture, vintage 55mm 2x anamorphic character at a wide aperture — oval bokeh on the deep bookshelf background, soft frame-edge falloff — light diffusion bloom on the amber practical source, slow controlled frontal push-in with minimal operator breath, color-negative tungsten-balanced film rendition pushed for night work with fine 35mm grain, deep amber-shadow grade, 24fps 180° shutter, 2 seconds.
```

### Shot 5 — Look 5 All Black | `54170ff3` | 3s

```
Scene & Mood: An all-black figure stands centered in a high industrial atelier at dusk, voluminous draped trousers cascading to the floor, as the camera rises slowly from below and builds the silhouette against the large factory window behind.

Frame Map: @image1 centered foreground, full-body framing occupying 80% of frame height. Large divided-light factory window fills the upper background. Metal pipe shelving visible at left. Camera starts slightly below eye level and rises to eye level across the runtime, the window growing more prominent behind the figure as the camera ascends and advances.

Subject Lock — @image1: Face, hair, extremely wide-leg black draped trousers, black henley, cropped black canvas jacket with stand collar, square-toe black boots, chain necklace, wristwatch, black leather belt, and silhouette identical throughout. Body centered and still, feet at shoulder width, arms loose, weight even. Jaw set, expression stoic, gaze fixed directly at camera. No step, no weight shift, no head turn. The voluminous trouser fabric holds its cascading drape with gravity across the full runtime.

Cross-Frame Rules: Single subject. @image1 holds center throughout. No drift.

Movement: @image1 holds completely still — single slow breath, barely visible against the henley. Extremely wide trouser fabric holds its draped position — a very subtle sway of the hem from residual air movement only, no exaggerated fabric motion. Cool dusk light from the factory window holds steady with no flicker. Camera executes a slow controlled upward push-in — starting slightly below eye level and rising to eye level while advancing, so the silhouette of the voluminous trousers and jacket shoulder line build against the factory window behind across the runtime.

Last Frame: Camera has risen to eye level and advanced — @image1 in a tighter full-body framing, factory window reading behind as cool blue-grey dusk glow, cool rim on the jacket shoulder and cascading trouser hem prominent against the light, metal shelving softened in the left background. No on-screen text, no captions, no signage typography, no rendered text in the frame.

World Plate: High-ceilinged industrial atelier at dusk — raw plaster walls, large divided-light factory window at the far end letting in fading cool blue-grey dusk light as the primary ambient source, heavy metal pipe shelving loaded with folded fabric at left, wooden worktable with vintage sewing machine at left midground, unlit mood board on the wall behind the figure.

Sound Bed: Diegetic only — very faint industrial ambient, distant city through the factory window, subtle fabric weight settling, no footsteps, no machinery, no music, no dialogue.

Capture Realism: @image1 sits inside real depth — cool dusk atmosphere suspended between camera, subject, and the factory window behind, background rendered softer, desaturated, lower-contrast so the silhouette sits within the atelier air. Skin reads true cinematic matte — zero shine on forehead, nose bridge, cheekbones, temples, chin — real peach fuzz at jaw and hairline, fine soft even pore texture, subsurface scattering, warmth preserved against the cool ambient, never plastic, never harsh, fine flattering texture. The all-black wardrobe holds distinct texture variation between the trouser drape, the henley cotton, and the structured canvas jacket — no flat undifferentiated black, real fabric grain in each layer. Low-contrast curve — shadows lifted gently holding open detail in the deep near-black garments, dusk window highlights rolled off softly never clipping. All specular highlights removed from skin, hair, fabric, metal shelving. Cool blue-grey dusk grade with warm ambient preserved on the face.

Camera Capture: wide-latitude cinema capture, vintage 40mm 2x anamorphic character at a wide aperture — oval bokeh on the deep atelier background, soft frame-edge falloff — light diffusion bloom on the factory window dusk light, slow controlled upward push-in with minimal operator breath, color-negative daylight film rendition pushed toward cool blue-grey with fine 35mm grain, cool dusk grade with warm face ambient, 24fps 180° shutter, 3 seconds.
```

---

## Caption Instagram

A fashion lookbook costs €5,000. I built one in an afternoon.

No photographer. No studio. No model.
Three tools. The right prompts. A clear brief.

This is what AI does to fashion production.

Comment "LOOKBOOK" and I'll show you how.

#fashiondesign #AIdesign #lookbook #fashiontech #brandidentity #fashionbranding #artificialintelligence #fashionphotography #AIart #fashioncontent
