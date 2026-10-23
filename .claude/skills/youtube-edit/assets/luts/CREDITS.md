# LUT

Tutte da DJI (Osmo Pocket 4P, profilo D-Log2 -> Rec.709, V1.0), scaricate il 20/10/2026 da https://www.dji.com/it/osmo-pocket-4p/downloads (file su terra-1-g.djicdn.com). File di testo .cube.
- `DJI-Pocket4P-DLog2-to-Rec709-size65.cube` — standard, 65 punti: **quella da usare**.
- `DJI-Pocket4P-DLog2-to-Rec709-size33.cube` — standard, 33 punti (piu' leggera).
- `DJI-Pocket4P-DLog2-to-Rec709-vivid-size65.cube` — variante vivid, piu' contrasto/saturazione.
Uso: `ffmpeg -vf "lut3d=file=...cube"` sulle clip a camera, MAI sul B-roll/presentazione.
Nota: la LUT D-Log2 e' diversa da quella D-Log (non mischiarle).

## D-Log (NON D-Log2, NON D-Log M) — Osmo Pocket 4P
Scaricate il 23/10/2026 dal sito ufficiale DJI (pagine "OSMO Pocket 4P D-Log to Rec.709", file su terra-1-g.djicdn.com, cartella HG224 LUT). Solo 33 punti: DJI non pubblica la 65 per il D-Log.
- `DJI-Pocket4P-DLog-to-Rec709-V2.0-size33.cube` — standard V2.0 (la piu' recente): **quella da usare per il D-Log**.
- `DJI-Pocket4P-DLog-to-Rec709-V1.0-size33.cube` — standard V1.0 (vecchia versione, per confronto).
- `DJI-Pocket4P-DLog-to-Rec709-vivid-V2.0-size33.cube` / `...vivid-V1.0-size33.cube` — varianti vivid.
Regola: clip girata in D-Log -> LUT D-Log; clip girata in D-Log2 -> LUT D-Log2. Mai incrociarle.
