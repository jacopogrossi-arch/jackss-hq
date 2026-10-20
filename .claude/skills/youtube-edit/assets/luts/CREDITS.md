# LUT

Tutte da DJI (Osmo Pocket 4P, profilo D-Log2 -> Rec.709, V1.0), scaricate il 20/10/2026 da https://www.dji.com/it/osmo-pocket-4p/downloads (file su terra-1-g.djicdn.com). File di testo .cube.
- `DJI-Pocket4P-DLog2-to-Rec709-size65.cube` — standard, 65 punti: **quella da usare**.
- `DJI-Pocket4P-DLog2-to-Rec709-size33.cube` — standard, 33 punti (piu' leggera).
- `DJI-Pocket4P-DLog2-to-Rec709-vivid-size65.cube` — variante vivid, piu' contrasto/saturazione.
Uso: `ffmpeg -vf "lut3d=file=...cube"` sulle clip a camera, MAI sul B-roll/presentazione.
Nota: la LUT D-Log2 e' diversa da quella D-Log (non mischiarle).
