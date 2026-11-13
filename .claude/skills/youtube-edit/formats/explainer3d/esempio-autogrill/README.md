# Autogrill: perché non si va mai dritti

Explainer 3D in stile cartoon (Three.js + HyperFrames), 1080p 60 fps, 92,7 s. Versione finale: **v2.2** (13/11/2026).
I video finiti sono in iCloud Drive › Video Claude (`autogrill-serpentone-v2.2.mp4` e la v1 `autogrill-serpentone.mp4`).

## Come si rifà

```bash
python make_engine.py        # costruisce vendor/world3d.js: base-world3d.js + engine-extra.js + products.js + scenery.js
python video.py              # scrive page/ (la composizione) e timing.json
python sfx.py                # voce/voce-only.wav + effetti -> voce/voce-pause.wav
bash finish.sh draft         # anteprima 30 fps + QA
bash finish.sh final         # master 60 fps + copia leggera (<= 30 MB)
```

## File

| File | Cosa fa |
|---|---|
| `video.py` | la regia: mondo 3D, camere, etichette, scritte, vegetazione, tempi agganciati alla voce (`at("parola")`). `video-v1.py` è la v1 |
| `store.py` | l'edificio e gli scaffali (`HDR` = reparti con colore e insegna) |
| `products.js` | **kit prodotti riusabile**: texture disegnate su canvas (salame con rete, parmigiano, vino, biscotti, panettone, peluche, macchinine…), `shelf2()` = gondola con prodotti instanced |
| `scenery.js` | **kit vegetazione riusabile**: alberi a chioma irregolare, pini, bosco instanced, siepi, colline |
| `engine-extra.js` | auto (estrusione con passaruota, vetri, cerchi, fari), scaffale v1, altri oggetti |
| `base-world3d.js` | motore World3D **bloccato** alla versione git 043948d della skill (quella nuova va in conflitto: `const hash`) |
| `make_engine.py` | unisce i pezzi sopra, aggiunge i tipi `forest`/`hedge`/`hills`, ombre (bias -0.0006, normalBias 0.04) |
| `sfx.py` | sound design: whoosh + riser d'apertura allineato al picco su "colpa del pavimento", pop/swish/whoosh automatici, +5 dB |
| `mix.py` | mix a guadagno **fisso**: musica 13 dB sotto la voce + sidechain, poi tutto a -16 LUFS (niente loudnorm dinamico) |
| `lab2.py` | pagina di prova dei prodotti |
| `vendor/world3d.py` | copia del modulo Python World3D della skill (commit 0543f57) per sicurezza |

Dipendenze esterne: la skill `D:/ClaudeCodeTest/.claude/skills/youtube-edit` (modulo `formats/world3d.py`, effetti in `assets/sfx/`, musica `assets/music/licensed/es-disque-magique.mp3`).

## Lezioni imparate

- **Primo secondo forte**: niente intro vuota (LEAD 0,35 s, camera già in movimento, titolo subito, whoosh + riser).
- **Prodotti riconoscibili**: texture vere e inquadrature strette, non cilindri colorati.
- **Sfarfallio sotto gli scaffali** = z-fighting di facce complanari: i pezzi interni vanno rientrati (`L - 0.08`) rispetto ai fianchi.
- **Musica troppo alta** con loudnorm a passata singola (alza la musica nelle pause): usare `mix.py`.
