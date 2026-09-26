# Mandal-Art — versione da stampare

`mandal-art-a4.pdf` — **il file da stampare.** Una pagina A4 verticale: griglia 9×9 completa + le tre regole in fondo. Pensato per una stampante di casa: fondo bianco, un solo riquadro pieno (il centro), testo a 6,4 pt che si legge da vicino.

**Come stamparlo:** apri il PDF, stampa a dimensione reale — *scala 100%* o *dimensione effettiva*, **non** "adatta alla pagina", altrimenti restringe i margini e il testo si rimpicciolisce ancora.

Contenuto identico a `../mandal-art-set-dic-2026.md`, con le frasi accorciate per stare nelle caselle.

---

## Come rigenerarlo

`mandal-art-a4.src.html` è il sorgente. Ha un segnaposto `/*FONTS*/` al posto dei font, perché i font (Bodoni Moda, IBM Plex Sans, IBM Plex Mono) vanno incorporati nel file prima di renderizzare: il PDF deve essere autonomo e Chrome headless non ha quei font di sistema.

Due passaggi, da questa cartella:

**1. Scaricare i font e incorporarli** (serve rete):

```bash
python3 embed-fonts.py     # produce build.html
```

**2. Renderizzare il PDF** con Chrome/Chromium headless:

```bash
chromium --headless --no-sandbox --disable-gpu --hide-scrollbars \
  --virtual-time-budget=8000 --no-pdf-header-footer \
  --print-to-pdf=mandal-art-a4.pdf "file://$PWD/build.html"
```

`build.html` è un file intermedio (13 KB di pagina + 266 KB di font incorporati): non va committato.

## Note di impaginazione

- Foglio A4 verticale, margini 8 mm.
- La griglia è **194 × 216 mm**: le caselle sono leggermente più alte che larghe. Serve a riempire il foglio e a dare respiro al testo — il quadrato perfetto lasciava una fascia bianca morta in fondo.
- Tre stati di casella, come nell'artifact: normale = parole di Jacopo · barra oliva a sinistra = conseguenza di una sua risposta · tratteggio diagonale = ancora da riempire (nove in tutto).
