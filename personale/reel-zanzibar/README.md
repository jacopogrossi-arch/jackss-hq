# Reel "The beauty of Zanzibar"

Reel di viaggio per Instagram dal viaggio a Zanzibar (21–27/10/2026), girato con l'Osmo Pocket 4P. Finito il 29/10/2026.
Questa cartella è la **copia su git** di piano, script e smistamento. Il lavoro vero (clip, render, cartelle di lavoro) sta in `videos/zanzibar/`, solo in locale, e i video finiti sono su iCloud Drive in **REEL ZANZIBAR**.

## Il video
- 16:9 e 4:3, 37,4 s, 17 inquadrature tagliate sulle battute di "Mrs Magic" (Strawberry Guy). Il modello è un reel su Krabi.
- Titolo "The beauty of ZANZIBAR" con l'effetto macchina da scrivere e i tasti veri di una macchina antica (Sonniss GDC 2026).
- Colore pellicola-oro con una curva a S in più. Le clip 1-2 hanno l'esposizione misurata clip per clip, le altre il colore della versione approvata.
- Sotto la musica: onde (0–17 s), giungla (17–26 s), poi di nuovo onde. Una light leak leggerissima con uno swoosh sul passaggio al tramonto.
- Il 4:3 è inquadrato clip per clip sui terzi (`crop43_x` in `shots.json`).
- La versione per Instagram è H.264 High, 25 Mbps in due passate, con i tag colore BT.709.

## File
| File | Cosa contiene |
|---|---|
| `video-brief.md` | Piano e stato, con tutte le decisioni in ordine di data |
| `shots.json` | Tagli, clip, punto di partenza, ritocchi per clip (`stops`, `smooth`, `extra`, `crop43_x`) |
| `script/prepara.py` | Taglia ogni pezzo e fa il colore (grade-scan, grade-match, grade-apply della skill youtube-edit) |
| `script/edl.py` | Scrive l'EDL per mh-video-editor (tagli, contrasto, spinta lenta) |
| `script/anima.py`, `script/titoli.py` | Titolo animato (`--4k`) e le 20 proposte di titolo |
| `script/finale.py` | Unisce titolo, reel, ambienti, light leak e swoosh (`--4k`) |
| `script/controllo.py` | Controllo clip per clip: misure e fogli prima/dopo |
| `script/inventario.py`, `script/strisce.py` | Smistamento dai proxy LRF: inventario, provini, strisce di fotogrammi |
| `smistamento/` | Elenco delle scene del Pocket (171 clip) e della Nano (64 clip, per un possibile secondo reel sott'acqua) |

Gli script si lanciano da `videos/zanzibar/reel/` (usano percorsi relativi a quella cartella), quindi qui sono una copia di riferimento.
