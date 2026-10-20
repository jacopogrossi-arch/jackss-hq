# LUT

- `DJI-OsmoNano-DLogM-to-Rec709-V1.cube` — LUT ufficiale DJI "Osmo Nano D-Log M to Rec.709 (vivid)", 3D 33 punti, testo .cube.
  Fonte: https://www.dji.com/it/nano/downloads (file su terra-1-g.djicdn.com). Scaricata il 20/10/2026.
  Uso: `ffmpeg -vf "lut3d=file=...cube"` sulle clip a camera, MAI sul B-roll (regola del metodo #1).
