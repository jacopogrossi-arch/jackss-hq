# Video brief: zanzibar-reel
Status: CONFIRMED (28/10/2026, confermato da Jacopo in chat: "mi fiderei di mh videoeditor", e vanno inclusi sconosciuti e bambini del posto)

- Riferimento: `ref/riferimento.mp4` (reel su Krabi). Copiamo solo la struttura: titolo in apertura, un taglio netto circa ogni 2 s, chiusura sul tramonto.
- Footage: `videos/zanzibar/pocket/mp4` per gli originali 4K e `pocket/lrf` per i proxy 720p delle clip ancora da caricare. Un proxy va sostituito quando arriva il suo originale.
- Musica: Strawberry Guy, "Mrs Magic". Il file di lavoro è `ref/riferimento.wav` (39,8 s, ~119 BPM, suonata dal vivo). Su Instagram la canzone si prende dalla libreria.
- Tempi: dalle battute di mh-video-editor (4 tempi = ~2,0 s), con il colpo più forte a 38,07 s. Stanno in `shots.json`.
- Formato: 16:9. La v1 è in 1920x1080 a 25 fps; la finale in 3840x2160. Ritaglio 4:3 alla fine.
- Durata: 39,8 s.
- Testo: "The beauty of zanzibar" nello stile del riferimento (sans light + serif), nei primi 5,4 s.
- Da includere: persone del posto, bambini compresi, per raccontare Zanzibar oltre al luogo. La lista delle 18 inquadrature è in `shots.json`.
- Da escludere: watermark e schermata finale con il logo.
- Effetti: nessuno, solo tagli netti e una dissolvenza a nero finale.
- Colore: pellicola-oro con grade-match fra le clip (`prepara.py`).
- Output: `zanzibar-reel_v1.mp4` in questa cartella.
- Lingua dei report: italiano.

## Stato al 28/10/2026 (v5 approvata)
- Titolo: macchina da scrivere nello stile della 4 (`titoli/anima.py`, `v4t`), con i tasti veri di Sonniss.
- Clip 3 = 0042 (laguna); 14 = 0085, 15 = 0072; trampolieri tolti; il reel finisce a 37,45 s.
- Colore: pellicola-oro + curva a S (in `edl.py`).
- Ambienti: onde 0-17 s, giungla 17-26 s, poi di nuovo onde. Light leak 05 leggerissima al taglio di 34,05 s con es-swoosh-wide.
- Volume dello swoosh già abbassato (0,28 -> 0,22) in `finale.py`: entra nel render 4K.
- **Per il 4K:** caricare gli originali di 0008 0017 0042 0070 0072 0083 0085 0124 0129 0138 0158. Poi in `shots.json` cambiare "lrf" in "mp4", lanciare `prepara.py` e `titoli/anima.py` (solo `v4t`, rigenera la clip 1), poi `finale.py` con `edl.py --width 3840 --height 2160`. Infine il ritaglio 4:3.

## 28/10/2026 sera: render finale fatto
- `zanzibar-reel_4k.mp4` (3840x2160) e `zanzibar-reel_4k_senza-musica.mp4`; ritaglio 4:3 centrale `zanzibar-reel_4k_4x3*.mp4` (2880x2160).
- Tutte le clip sono originali 4K; titolo disegnato direttamente in 4K (`titoli/anima.py --4k`). Rifare: `prepara.py`, `titoli/anima.py --4k`, `finale.py --4k`.
- Nel 4:3 il capitano con la maglia dell'Inter (clip 6) è tagliato a sinistra: si può spostare il ritaglio solo per quella clip.

## 29/10/2026: versione FINALE
- `zanzibar-reel_FINALE*.mp4` (16:9 e 4:3, con e senza musica), caricati su iCloud in REEL ZANZIBAR.
- Montaggio unito: clip 1-2 dal render "nuovo" (esposizione clip per clip: 0008 +0,30, 0017 0 con smooth 2), clip 3-17 dal render approvato (tutte a -0,22 stop, bianco R 0,970 B 1,015: il valore uscito per sbaglio, ma a Jacopo piace di più). L'unione è fatta al fotogramma 198 (7,92 s).
- Per rifarlo da zero: in `shots.json` mettere `stops` -0,22 sulle clip 3-17 (e il bianco 0,970/1,015, che `prepara.py` non passa ancora).
