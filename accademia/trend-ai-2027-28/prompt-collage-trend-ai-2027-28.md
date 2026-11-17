# Prompt GPT-2 — collage moodboard + tech board (19/10/2026)

Un collage per tema, orizzontale (formato 16:9 da impostare nell'interfaccia, non nel prompt). Metà sinistra = moodboard emotiva, metà destra = tech board. Nessun testo nell'immagine: titoli e concept restano nella pagina Canva.
Riferimento di stile: il collage del collega (fondo nero con carta strappata, polaroid, spilli dorati). Esito in Canva: pagina 2 di ogni tema.

## 1. ROYAL HUMOUR

```
A wide horizontal artistic moodboard collage on a black textured paper background, the frame split into two halves with a narrow black gap down the center. Left half, the emotional moodboard: six or seven vintage polaroids and torn paper photo scraps pinned with small gold pushpins and held with strips of aged tape, overlapping at slight angles — a grand baroque palace corridor with gilded mirrors, an opulent rococo salon with red velvet curtains, a surreal fashion editorial of a giant stone frog on a polished parquet floor, a portrait of a figure with a powdered pastel wig and a cheap paper crown, a banquet table with papier-mâché domed cloches over plastic fruit and a sugar-paste cake, a cardboard pop-up theatre stage with painted wings, hair rollers and a chewing-gum bubble used as playful royal props. Right half, the technical board: torn paper swatches and fabric close-ups pinned the same way — gold-threaded damask, metallic lurex knit, heavy jacquard brocade, tassel and fringe trims, loose feathers, perforated filigree lace, a Delft blue and white ceramic tile, a gilded rococo frame detail, a lacquered red leather sample, a jewel button, candy pink and pale yellow wool. Palette of lacquered red, antique gold, cobalt blue, candy pink and deep black. Everything reads as a handmade scrapbook collage on a pinboard, rich contrast, no text, no letters, no captions, no logos.

Real printed photographs and real fabric swatches, real paper grain with torn edges, soft natural shadows under each pinned piece, fine film grain across the whole frame. Photographed not generated.
```

## 2. BODY TALK

```
A wide horizontal artistic moodboard collage on a black textured paper background, the frame split into two halves with a narrow black gap down the center. Left half, the emotional moodboard: six or seven polaroids and torn paper photo scraps pinned with small gold pushpins and paper clips, overlapping at slight angles — a collarbone in raking window light, the nape of a neck in soft shadow, two hands almost touching, a sheer curtain lifting in the wind, a shadow cast over crumpled bed sheets, a dark chiaroscuro portrait with the face turned away, a single open collar shirt in grainy film, dark velvety flowers and translucent white petals as tender accents. Right half, the technical board: torn paper swatches and fabric close-ups pinned the same way — ultra fine gauge silk-cashmere knit, soft lamb nappa leather, sheer silk voile, nude chantilly lace, deep bordeaux velvet, glossy patent leather, a draped black tulle, a fleshy soft round tricot knit, a hidden red lining peeking from a seam. Palette of nude skin tones, powder pink, deep passion red, black and a touch of intense blue. Everything reads as a handmade scrapbook collage on a pinboard, quiet and sensual, bodies shown only in fragments, no explicit nudity, no text, no letters, no captions, no logos.

Real printed photographs and real fabric swatches, real paper grain with torn edges, soft natural shadows under each pinned piece, fine film grain across the whole frame. Photographed not generated.
```

## 3. ONLIFE

```
A wide horizontal artistic moodboard collage on a black textured paper background, the frame split into two halves with a narrow black gap down the center. Left half, the emotional moodboard: six or seven polaroids and torn photocopy scraps pinned with gold pushpins and strips of masking tape, overlapping at slight angles — a skateboarder crossing an empty street at golden hour, friends laughing in a night street lit by camera flash, a long empty street with warm lampposts, a supermarket trolley left on the pavement, a stack of worn vinyl records, snapshots pinned to a bedroom wall with tape, roller skates on asphalt, sunlight falling through a bedroom window onto a messy bed, motion-blurred candid frames like memories caught in a hurry. Right half, the technical board: torn paper swatches and fabric close-ups pinned the same way — wide wale corduroy, matte ripstop nylon, stiff raw denim, brushed grey fleece, quilted padding, a reinforced knee patch with visible topstitching, a nylon zip, a drawcord hem, an orange lining peeking from a black jacket, concrete and plaster textures. Streaks of yellow and black hazard tape cross the collage. Palette of asphalt grey, concrete, plaster beige, tar black with accents of mustard yellow, signal red and faded blue. Everything reads as a handmade zine scrapbook on a pinboard, instinctive and imperfect, no text, no letters, no captions, no logos.

Real printed photographs and real fabric swatches, real paper grain with torn edges, soft natural shadows under each pinned piece, fine 35mm film grain across the whole frame. Photographed not generated.
```

## v2 — tech board con CAPI veri (19/10, dopo il primo risultato Royal Humour)

Il collage Royal Humour è piaciuto (moodboard a sinistra OK). La tech board a destra deve avere **capi interi e dettagli di capi** (giacche, pantaloni, camicie, colletti, bottoni, tasche, scarpe), non solo campioni di tessuto, come nel riferimento del collega.

**Flusso:** in GPT-2 allegare (1) il collage già generato come riferimento di stile e (2) 5-8 foto di capi scaricate da Pinterest per tema. Chiedere di rifare SOLO la metà destra con quei capi. Poi in Canva si assembla la pagina (sinistra del collage vecchio + destra nuova) oppure si usa l'immagine nuova intera.

**Prompt (uguale per i 3 temi, cambia solo [ELENCO]):**
```
Use the first attached image as the exact style reference for the collage: black textured paper background, torn paper scraps, aged tape, small gold pushpins, handmade scrapbook look. Keep the left half exactly as it is. Redo only the right half as a technical board made of the garments in the other attached images: cut out each garment and pin it on the black paper as a torn-edge scrap with tape and pushpins, overlapping slightly at different angles, a few of them as close-up details. Show whole garments and garment details (silhouettes, cuts, collars, pockets, buttons, trims, hems, shoes), not only fabric swatches, with two or three small fabric swatches as accents at most. Keep each garment exactly as in its reference photo, do not redesign them. [ELENCO]. No text, no letters, no captions, no logos. Real printed photographs, real paper grain, soft natural shadows under each pinned piece, fine film grain. Photographed not generated.
```

**[ELENCO] per tema** (e cosa scaricare da Pinterest, 5-8 foto):
- **ROYAL HUMOUR:** `hussar jacket gold frogging men` · `lace jabot shirt men` · `black wide trousers gold side stripe` · `brocade damask coat men` · `tailcoat tassel fringe` · `ruffle collar shirt` · `gold button military jacket detail` · `black cowboy boots gold stitching`.
- **BODY TALK:** `fine gauge knit open neck men` · `wide leg leather trousers pleated men` · `camel overcoat red lining` · `sheer voile shirt men` · `lace detail sleeve` · `draped scarf neck knit` · `bordeaux velvet jacket men` · `black cowboy boots pointed`.
- **ONLIFE:** `black nylon bomber orange lining` · `baggy raw denim knee patch` · `wide corduroy trousers men` · `quilted puffer jacket men` · `drawcord hem jacket detail` · `ribbed fitted t-shirt white men` · `brushed fleece hoodie grey` · `worn canvas sneakers`.

## Dopo la generazione
1. Salvare i 3 collage (uno per tema) e darmeli.
2. Inserirli in Canva come pagina 2 di ogni tema, dopo la pagina concept.
3. Se un collage esce male, rigenerare solo quello senza toccare gli altri: cambia solo l'elenco di immagini della metà che non convince.
