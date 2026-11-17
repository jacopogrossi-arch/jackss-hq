# Oggetti 3D in stile giocattolo: Gemini → Tripo → Claude

*Preparato il 17/11/2026 mentre Jacopo era in palestra. Tutto qui è pronto da copiare e incollare.*

## Il flusso (per ogni oggetto)
1. **Gemini** (Nano Banana Pro): allega i riferimenti indicati e incolla il prompt → ottieni l'immagine nello stile giocattolo.
2. **Tripo AI**: carica l'immagine (pantalone: le 4 viste; tutti gli altri: 1 sola immagine) → genera il 3D.
3. **Esporta GLB**. Se Tripo ti dà l'opzione, scegli **senza compressione** (`meshopt` off). Se non puoi, va bene lo stesso: ora ho il decompressore.
4. **Mandami il GLB** in chat. Ci penso io: `scripts/prepare_prop.sh` lo decomprime, lo alleggerisce a ~100.000 triangoli, fa 4 viste di controllo e lo metto in scena accanto al narratore.

## Cosa ho già fatto
- **Pantalone Tripo (realistico):** decompresso (era 1,86 milioni di triangoli, compresso `EXT_meshopt`) e alleggerito a 100.000 triangoli: `videos/_bench/trousers-tripo/olive-trousers-100k.glb` (4 MB). Visivamente è perfetto, ma troppo realistico per il nostro mondo (giocattolo morbido). Per questo lo rifacciamo in stile.
- **4 viste del pantalone vero** (fronte, retro, due lati), da usare come riferimento in Gemini: `social/assets-3d/pantalone/` (il file con le 4 viste insieme è `rif-4-viste.jpg`).
- **Riferimenti di stile** presi dal video v8: `social/assets-3d/riferimenti-stile/` (`narratore-intero.jpg` è il più importante: è il tuo pupazzo, è il "linguaggio" a cui tutti gli oggetti devono assomigliare).

## Cosa allegare a Gemini (sempre)
- `social/assets-3d/riferimenti-stile/narratore-intero.jpg` → **stile del personaggio** (forme tonde, superfici opache, texture morbida).
- Opzionale, per la palette: `tavolo-taglio.jpg` e `set-foto.jpg` (terracotta, crema, verde, ottone).

## Blocchi riusabili (in inglese, per Gemini)
**STYLE** (va in ogni prompt):
```
Stylized collectible-toy 3D look, like a chunky hand-sculpted vinyl and clay figurine: simplified rounded forms, slightly exaggerated proportions, soft matte surfaces, gentle baked shading, painted-on surface detail only where it helps (stitching, buttons, seams). Warm muted palette of terracotta, cream, olive green, brass and deep brown. Match the surface finish, softness and level of simplification of the attached character reference. Not a photograph, not photorealistic, no fabric micro-weave, no film grain, no harsh specular highlights.
```
**SETUP** (sfondo e luce, utili a Tripo):
```
Single object, centered, fully visible, plain even neutral mid-gray seamless background with no seam and no gradient, soft diffused studio light from the front-left, only a faint contact shadow, no text, no logos, no brand names, no people, no hands, no props.
```

---

## 1. PANTALONE (4 viste in un'unica immagine)
**Allega:** `social/assets-3d/pantalone/rif-4-viste.jpg` (il disegno da rispettare) + `riferimenti-stile/narratore-intero.jpg` (lo stile).

```
Redraw the real trousers shown in the first attached image in the toy style of the second attached image. Keep the design exactly: olive-green straight-leg trousers with a single front pleat, a fly with button, belt loops, small side buckle adjusters at the waist, back welt pockets, a clean plain hem. Output ONE image containing four views of the same trousers arranged in a 2x2 grid with thin even gaps: top-left front view, top-right back view, bottom-left left side view, bottom-right right side view. Every view straight-on, full length, same scale and same height, the trousers standing on their own with full 3D volume as if worn by an invisible body, no mannequin, no body, no hanger. Simplify the fabric into smooth matte surfaces with a few soft sculpted folds, color olive green, stitching and buttons painted in a slightly darker tone. [STYLE] [SETUP]
```
*(Sostituisci [STYLE] e [SETUP] con i blocchi sopra.)*
Poi **ritaglia le 4 viste** (o dimmelo e lo faccio io) e caricale su Tripo in modalità multi-vista: fronte, retro, sinistra, destra.

## 2-7. GLI ALTRI OGGETTI (una sola immagine ciascuno)
**Allega:** `riferimenti-stile/narratore-intero.jpg`. Vista consigliata per Tripo da singola immagine: tre quarti dall'alto, oggetto intero.

Struttura: `[OGGETTO] + [STYLE] + [SETUP]`

**2. Macchina da cucire**
```
A compact vintage-style sewing machine with a cream-colored body, a deep brown base, a brass hand wheel and a small needle arm, a spool of thread on top. Three-quarter view from slightly above, fully visible. [STYLE] [SETUP]
```
**3. Manichino sartoriale**
```
A tailor's dress form: a cream fabric torso without head or arms, mounted on a slim dark-wood stand with three feet and a small brass ball on the neck. Three-quarter view, fully visible from the neck ball to the feet. [STYLE] [SETUP]
```
**4. Fotocamera su treppiede**
```
A mirrorless camera with a short lens, matte black body with a cream accent, mounted on a deep brown wooden-style tripod with brass joints. Three-quarter view, fully visible including the three tripod legs. [STYLE] [SETUP]
```
**5. Laptop aperto**
```
An open laptop with a matte dark-gray body, a blank dark screen and a simple keyboard, slightly tilted open at about 110 degrees. Three-quarter view from slightly above, fully visible. [STYLE] [SETUP]
```
**6. Forbici da sarto**
```
A large pair of tailor's shears with brass-colored blades and deep brown handles, slightly open, lying flat. Three-quarter view from above, fully visible. [STYLE] [SETUP]
```
**7. Rotoli di tessuto**
```
A neat stack of four fabric bolts lying on their sides: olive green, cream, terracotta and dark navy, each a thick cardboard-core roll wrapped in cloth with a small plain paper tag. Three-quarter view, fully visible. [STYLE] [SETUP]
```

## Impostazioni consigliate su Tripo
- Gli oggetti singoli: input 1 immagine; il pantalone: multi-vista (4 immagini).
- Texture alta va bene (le riduco io a 2048); niente remesh particolare: lo faccio io.
- **Esporta GLB**, se possibile senza compressione. Nome file chiaro (es. `macchina-da-cucire.glb`).
- Se il risultato è troppo realistico: rigenera l'immagine in Gemini aggiungendo *"even more simplified, chunkier, more toy-like"* al prompt. Lo stile si decide in Gemini, non in Tripo.

## Quando me li mandi
Dimmi in che ordine li vuoi in scena. Io ti faccio vedere ogni oggetto accanto al narratore (stessa luce) prima di metterlo nel video. Il primo che mi manderesti: **macchina da cucire**, è il test di stile più rapido.
