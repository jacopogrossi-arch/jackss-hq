# Tavola 10 — Stampa all-over After Hours

Contenuti per la tavola 10 del progetto After Hours (`concept-after-hours.md`). Avviata il 29/09/2026. Criteri dal PDF della prof (appunti in `stampa-piazzata-after-hours.md`, sezione finale).

**Richiesta della consegna:** rapporto di ripetizione in scala 1:1, 2 varianti colore, mockup.

**Cosa intende la prof per all-over:** disegno che si ripete all'infinito sulla pezza. Si costruisce un **modulo** (rapporto): il quadrotto in cui ciò che esce da un lato rientra da quello opposto, senza interruzioni. Ripetizione **grid** o **half-drop** (salto di mezzo modulo in verticale, più naturale). Output: un file del modulo (es. 64 × 64 cm a 300 dpi) che la stampante tessile ripete su tutto il rotolo. Nel suo esempio la tavola mostra: modulo ripetibile, rotolo di tessuto stampato, prodotto finale, capo indossato.

---

## Il motivo: "Catena della notte"

Due elementi disegnati nello stesso stile a incisione della stampa piazzata Room Key, così le due stampe sono sorelle:
1. **il morsetto** (due anelli uniti dalla barretta);
2. **una piccola chiave d'albergo con la targhetta "4"**.

Sparsi sulla pezza in diagonale, alternati, con ripetizione **half-drop**. Da lontano sembrano una catena che corre sul tessuto; da vicino si scopre la chiave.

**Da dire all'esame:** la piazzata racconta la chiave una volta sola, in grande; l'all-over la nasconde tra i morsetti, come un segreto che si vede solo da vicino.

## Metodo (perché non generare direttamente il pattern)

I generatori di immagini non fanno moduli davvero senza interruzioni: i bordi non combaciano. Quindi:
1. **ChatGPT genera solo i due elementi**, separati, su fondo pieno.
2. **Il modulo lo costruisco io con uno script Python**: ritaglio gli elementi, li dispongo in half-drop con i bordi che rientrano dal lato opposto. Il modulo è matematicamente continuo, come lo vuole la prof.
3. Le **due varianti colore** si ottengono ricolorando lo stesso modulo.
4. **Rotolo e capo finito** li generiamo con ChatGPT allegando il modulo.

## Stato (29/09)

✅ **Elementi generati** con ChatGPT → `img-after-hours/allover-elementi.webp` (morsetto + chiave con targhetta "4").
✅ **Modulo costruito** con `img-after-hours/modulo_allover.py`: 32 × 32 cm a 300 dpi, 4 colonne × 2 righe, colonne dispari sfalsate di mezza cella (half-drop). I morsetti formano una **catena in diagonale**, le chiavi corrono nella diagonale accanto. Continuo sui bordi (gli elementi che escono da un lato rientrano dal lato opposto).
- moduli di produzione: `allover-modulo-A.jpg` (oro su cioccolato), `allover-modulo-B.jpg` (avorio su smeraldo);
- anteprime 3 × 3 con il modulo riquadrato (come nell'esempio della prof): `allover-ripetizione-A.jpg`, `allover-ripetizione-B.jpg`.

Mancano: rotolo di tessuto stampato e capo finito (giacca da camera look 5), da generare con ChatGPT allegando il modulo A.

## Varianti colore

| Variante | Motivo | Fondo | Dove |
|---|---|---|---|
| **A — principale** | Oro Morsetto `#B8913F` | Cioccolato Raso `#3B2620` | giacca da camera, look 5 (raso stampato) |
| **B — alternativa** | Avorio Lenzuolo `#EDE4D3` | Smeraldo Velluto `#0F4D3A` | fodera della vestaglia, look 2 |

## Dati tecnici del modulo

- Rapporto: **32 × 32 cm** in scala 1:1, ripetizione **half-drop**.
- File di produzione: 32 × 32 cm a 300 dpi (3780 × 3780 px), stampa digitale a getto d'inchiostro su raso di seta.
- Vantaggi (dalla prof): taglio libero, poco spreco, lo stesso tessuto va bene per giacca, pigiama o fodera.

---

## Prompt per ChatGPT — i due elementi

```
Two separate ornaments on a plain solid chocolate brown background (#3B2620), side by side with a lot of empty space between them, both drawn in exactly the same style: vintage engraving illustration in gold (#B8913F), bold confident lines with solid filled areas and minimal hatching, like a luxury 1990s silk scarf print. LEFT: a classic equestrian horsebit, two round rings joined by a short bar, horizontal, perfectly symmetrical. RIGHT: a small ornate vintage hotel room key, vertical, with an oval key tag hanging from it on a short chain; on the tag a single elegant serif numeral "4". Both ornaments roughly the same height. Flat, even background with no texture, no shadows, no gradients. No other text, no logos, no brand names, no frame, no border.
```

Stesso stile del Room Key della tavola 09: se viene troppo diverso, allega l'immagine `stampa-room-key-A-FINALE.webp` e aggiungi *"Same drawing style as the reference image."*
