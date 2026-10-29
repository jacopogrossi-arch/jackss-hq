# Reel Zanzibar #2 — "Like a Tattoo"

Secondo reel Instagram del viaggio a Zanzibar (21–27/10/2026), sulla canzone "Like a Tattoo" di Sade. **Finito il 29/10/2026**: il file è su iCloud in REEL ZANZIBAR, `reel2-like-a-tattoo_pellicola-oro_INSTAGRAM_4x3.mp4`.
Questa cartella è la **copia su git** di scaletta e script. Clip, render e prove stanno in `videos/zanzibar/reel2/`, solo in locale.

## Il video
- Riferimento: un edit TikTok (macchina al tramonto). L'audio è estratto in `ref/riferimento.wav`. La canzone si usa da 0 a 36,3 s: a 36,5 s c'è il suono del logo TikTok.
- **Tagli:** sono gli stacchi del video di riferimento, misurati fotogramma per fotogramma (2,43 · 5,70 · 7,37 · 8,70 · 11,17 · 13,00 · 16,47 · 19,93 · 21,37 · 23,50 · 24,80 · 29,13), più 33,11 (un attacco) e la fine a 36,3. Jacopo ha confermato il primo stacco a 2,4 s. La griglia di mh-video-editor (~119 BPM) e quella di beat-sync-edit (~92 BPM) sbagliavano il primo attacco: la canzone è suonata dal vivo e senza cassa.
- **Formato:** 4:3 come il primo reel (2880x2160), inquadrato clip per clip (`crop43_x`). Le barre del cinemascope sono state provate e scartate. Niente firma e niente titoli.
- **Scaletta:** una giornata che scorre. Si apre sulla barca a vela al tramonto, poi il mattino (palme, arco, spiaggia vuota), la partenza in barca, il capitano, la laguna, il tuffo, il banco di sabbia, e si chiude di nuovo al tramonto. È in `shots.json`, approvata il 29/10.
- **Regole di gusto (29/10):** visuali smooth, con la camera che scivola o con un movimento morbido dentro l'inquadratura (va bene anche la camera ferma). Niente selfie, niente facce in camera, niente clip confuse. La prima inquadratura deve colpire subito. Ogni clip parte dove il movimento è pulito: si misura con `finestre.py`, perché dai fotogrammi fermi non si vede quando si stava ancora sistemando l'inquadratura.

## Script (si lanciano da `videos/zanzibar/reel2/`)
| File | Cosa fa |
|---|---|
| `script/provini.py` | Fogli provini dagli originali 4K, con la LUT giusta per profilo (D-Log, D-Log2, D-Log M o nessuna) |
| `script/finestre.py` | Per ogni clip trova la finestra col movimento più pulito, secondo per secondo |
| `script/movimento.py` | Velocità e tremolio di tutte le clip (non ancora usato) |
| `script/animatic.py` | Animatic da `shots.json`: clip vere, solo LUT, cinemascope, musica |

## Colore (29/10)
- **Scelto pellicola-oro** dopo un confronto con il look di Jacopo, con le due versioni complete e un video affiancato (anche questi su iCloud). Jacopo: "due look diversi, tutti e due belli"; per questa canzone pellicola-oro è "più fairy, più dreamy".
- **Nitidezza:** la prima bozza sembrava sfocata accanto agli export di DJI Mimo. Le cause erano la bozza in 1080 ridotta per il telefono, la riduzione del rumore e il fatto che Mimo aggiunge uno sharpening. Ora: niente riduzione rumore + `unsharp=5:5:0.8` sul 4K. Sulla stessa scritta della barca la nitidezza è 54,5 contro i 59,9 di Mimo.

## Script del render (si lanciano da `videos/zanzibar/reel2/`)
| File | Cosa fa |
|---|---|
| `script/prepara.py` | Colore pellicola-oro: grade-scan, grade-match solo sul Pocket, grade-apply. La Nano non in log passa da una LUT neutra |
| `script/prepara_jacopo.py` | Versione col look di Jacopo: i suoi export Mimo dove ci sono, altrimenti la ricetta (`personale/look-jacopo/`) |
| `script/edl.py` | EDL per mh-video-editor: curva a S + sharpening, spinta lenta 5% (`--jacopo` per l'altra versione) |
| `script/finale.py` | Render 16:9, ritaglio 4:3 sul fotogramma reale degli stacchi, versione telefono, export Instagram (`--4k`, `--jacopo`) |

## Suono (29/10)
File finale su iCloud: `REEL ZANZIBAR/reel2-like-a-tattoo_FINALE-CON-SUONO_INSTAGRAM_4x3.mp4`. Script: `script/suono-mix.py`, che va messo in `videos/zanzibar/reel2/suono/mix.py`. I suoni Epidemic stanno in `suono/es/` e restano solo in locale.
- **Audio originale delle clip:** scartato. Misurandolo, in barca c'è solo vento sul microfono e motore (70% dell'energia sotto 200 Hz, picchi a 0 dB), e in un paio di clip si sentono voci.
- **Ambiente:** un'onda/barca a vela solo sulla prima clip, a -32 LUFS, cioè ~18 dB sotto la canzone. Dopo c'è un altro mare (acqua calma) solo sulle clip di mare, a -40 LUFS, "si deve quasi non sentire": Jacopo l'ha chiesto prima più basso (-43), poi "un filo di più". Palme e grilli della sera sono stati provati e tolti.
- **Clip del capitano (13,0–16,5):** un motoscafo, cioè fuoribordo e acqua che corre, a -32.
- **Tuffo:** splash sullo stacco a 19,93. Sotto le due clip subacquee la canzone si ovatta (passa-basso 420 Hz) e si riapre di colpo sulla barca a 23,5. Era la "versione B": Jacopo pensava che sarebbe venuta male, invece "la B è bellissima".
- **Giorno → sera (29,13):** light leak dorato (05, 1,25–2,0 s, 35%) con un soffio d'aria al posto del whoosh.
- **Sullo stacco laguna → sott'acqua niente transizione.** Provati uno swoosh e tre transizioni visive: zoom con sfocatura ("non mi piace"), whip pan orizzontale ("non so se mi convince"), tuffo verticale con lampo. Alla fine Jacopo: "forse è meglio senza transition".
