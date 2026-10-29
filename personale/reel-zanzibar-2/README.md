# Reel Zanzibar #2 — "Like a Tattoo"

Secondo reel Instagram del viaggio a Zanzibar (21–27/10/2026), sulla canzone "Like a Tattoo" di Sade.
Questa cartella è la **copia su git** di scaletta e script. Clip, render e prove stanno in `videos/zanzibar/reel2/`, solo in locale.

## Il video
- Riferimento: un edit TikTok (macchina al tramonto). L'audio è estratto in `ref/riferimento.wav`. La canzone si usa da 0 a 36,3 s: a 36,5 s c'è il suono del logo TikTok.
- **Tagli:** sono gli stacchi del video di riferimento, misurati fotogramma per fotogramma (2,43 · 5,70 · 7,37 · 8,70 · 11,17 · 13,00 · 16,47 · 19,93 · 21,37 · 23,50 · 24,80 · 29,13), più 33,11 (un attacco) e la fine a 36,3. Jacopo ha confermato il primo stacco a 2,4 s. La griglia di mh-video-editor (~119 BPM) e quella di beat-sync-edit (~92 BPM) sbagliavano il primo attacco: la canzone è suonata dal vivo e senza cassa.
- **Formato:** cinemascope 2,39:1 con le barre nere. Niente firma e niente titoli.
- **Scaletta:** una giornata che scorre. Si apre sulla barca a vela al tramonto, poi il mattino (palme, arco, spiaggia vuota), la partenza in barca, il capitano, la laguna, il tuffo, il banco di sabbia, e si chiude di nuovo al tramonto. È in `shots.json`, approvata il 29/10.
- **Regole di gusto (29/10):** visuali smooth, con la camera che scivola o con un movimento morbido dentro l'inquadratura (va bene anche la camera ferma). Niente selfie, niente facce in camera, niente clip confuse. La prima inquadratura deve colpire subito. Ogni clip parte dove il movimento è pulito: si misura con `finestre.py`, perché dai fotogrammi fermi non si vede quando si stava ancora sistemando l'inquadratura.

## Script (si lanciano da `videos/zanzibar/reel2/`)
| File | Cosa fa |
|---|---|
| `script/provini.py` | Fogli provini dagli originali 4K, con la LUT giusta per profilo (D-Log, D-Log2, D-Log M o nessuna) |
| `script/finestre.py` | Per ogni clip trova la finestra col movimento più pulito, secondo per secondo |
| `script/movimento.py` | Velocità e tremolio di tutte le clip (non ancora usato) |
| `script/animatic.py` | Animatic da `shots.json`: clip vere, solo LUT, cinemascope, musica |
