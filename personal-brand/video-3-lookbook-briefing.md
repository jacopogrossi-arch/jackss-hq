# Briefing generazione lookbook — Video #3 (Stone Island Ghost Piece)

Briefing per generare le immagini lookbook con la **stessa consistenza del video di riferimento**. Da leggere prima di aprire qualsiasi tool. Più l'idea è bloccata qui, più gli shot escono coerenti.

---

## 1. Cosa ha fatto il riferimento (workflow reale osservato)

Il reel di riferimento (brand finto "Jeko") ha costruito il lookbook così:

1. **Bloccato il prodotto prima di tutto** — polo a righe verde/bianco disegnata in Canva con scheda tecnica completa: tessuto (cotone piquet verde), colori (verde scuro + verde menta), posizione e colore del ricamo ("Jeko" bianco), numero "3", fronte/retro. Questo capo identico ricompare in **ogni** shot → è l'àncora della consistenza.
2. **Generato con Higgsfield, modello "Nano Banana Pro"** (visibile negli screen-rec a 35–39s). Prompt semplice: *"campagna artistica di polo ralph lauren, il concept principale sarà il golf"*. In input: il design del capo + la campagna reference reale.
3. **Copiato una vera campagna**: Polo Ralph Lauren "The Heritage Swing" — tenuta da golf, prato curato, palme, golden hour, sacca da golf, cavalli, staccionata del ranch.

**Lezione:** non hanno "fatto tante immagini a caso". Hanno bloccato modello + capo + mondo + luce, e fatto variare **solo posa e inquadratura**. Per questo 5 shot sembrano una sola campagna.

---

## 2. I 6 pilastri della consistenza (da replicare)

| Pilastro | Nel riferimento | → Nostro (Stone Island Ghost Piece) |
|---|---|---|
| **Stesso modello** | Stesso volto in tutti gli shot | **Jago** (Soul ID Higgsfield) in ogni shot con volto visibile |
| **Stesso capo bloccato** | Polo identica (righe, ricamo, "3") | **Ghost Piece identica**: nylon ripstop antracite, cappuccio, compass badge braccio sinistro, zip coerente |
| **UN solo mondo** | Tenuta golf (prato, palme, ranch, staccionata) | **UN ambiente industriale**: cortile di capannone, scala antincendio arrugginita, muri di cemento grezzo. Stesso luogo per tutti gli shot |
| **Una sola luce/ora** | Golden hour caldo ovunque | Scelta unica e costante (vedi §4) — non mischiare ore del giorno |
| **Una sola color grade** | Caldo, desaturato, filmico | Fredda/desaturata industriale: antracite, grigio cemento, ruggine, sabbia |
| **Props ricorrenti** | Sacca da golf, mazza, cavalli | Scala antincendio, scaffali metallici, blocchi di cemento, bidoni — ricorrono e legano gli shot |

**Regola d'oro:** modello + capo + mondo + luce + grade = BLOCCATI. Solo posa e framing cambiano.

---

## 3. Tipi di shot (mappati dal riferimento)

Il riferimento usa questi tipi — li replichiamo con contenuto industriale:

| # | Tipo shot riferimento | → Nostro shot Ghost Piece |
|---|---|---|
| 1 | Full body con sacca, in piedi | Full body nel cortile industriale, Ghost Piece zip chiusa, cappuccio giù |
| 2 | Accovacciato con mazza (posa bassa dinamica) | Accovacciato su gradino di cemento / base scala antincendio |
| 3 | Azione (golf swing) | Azione: Jago che si muove/cammina deciso — per il b-roll Seedance |
| 4 | Editoriale ambientale (staccionata + cavalli) | Editoriale: appoggiato alla ringhiera della scala antincendio |
| 5 | Wide ambiance (figura piccola nel paesaggio) | Wide: figura piccola nel capannone, spazio industriale che la ingloba |
| 6 | Dettaglio logo/capo | Close-up compass badge + texture nylon ripstop |

---

## 4. Parametri da BLOCCARE (decisioni da confermare con Jacopo)

Prima di generare confermiamo questi, così non si mischiano tra shot:

- **Tool/modello:** Higgsfield + **Nano Banana Pro** (come il riferimento), partendo da Soul ID di Jago. *(da confermare)*
- **Ora/luce:** UNA tra:
  - **A — Cielo coperto industriale**: luce diffusa, fredda, piatta (mood editoriale severo)
  - **B — Golden hour rasante**: sole basso che taglia cemento e ferro (più caldo, drammatico)
  - **C — Crepuscolo/dusk**: blu-grigio freddo con interni a luce fluorescente
  *(da confermare — il riferimento è coerente perché ne usa una sola)*
- **Bottom:** cargo dritti sabbia/khaki **oppure** tecnici neri — uno solo, coerente in tutti gli shot *(da confermare)*
- **Stato Ghost Piece:** zip a metà o chiusa, cappuccio su o giù — definire la regola per shot *(vedi §5 del brief in video-3.md)*
- **Campagna Stone Island di riferimento reale** da copiare per pose/inquadrature: da scegliere *(da reperire)*

---

## 5. Approccio prompt di generazione

Replicando il metodo del riferimento (prompt semplice + reference forti):

1. **Input al modello:** reference pulita della Ghost Piece (capo) + Soul ID di Jago + 1–2 frame della campagna Stone Island reale scelta.
2. **Prompt base (stesso per tutti gli shot, cambia solo la posa):**
   > *"Artistic fashion campaign for Stone Island, hero piece the Ghost Piece jacket, single industrial urban setting, [POSA/FRAMING dello shot], stoic male model, consistent [LUCE scelta], anthracite/concrete/rust palette, editorial campaign quality, indistinguishable from a real Stone Island campaign."*
3. **Cambia solo il blocco [POSA/FRAMING]** shot per shot (vedi §3 e il Brief Lookbook in `video-3.md`).
4. **3–4 varianti per shot**, si seleziona la più forte. Si scartano quelle dove capo/volto/luce derivano.

---

## 6. Checklist di consistenza (prima di approvare ogni shot)

- [ ] È lo stesso volto di Jago?
- [ ] La Ghost Piece è identica (cappuccio, compass badge braccio sinistro, colore, texture)?
- [ ] Lo sfondo è lo stesso mondo industriale (non una location diversa)?
- [ ] La luce/ora è la stessa degli altri shot?
- [ ] La color grade combacia (antracite/cemento/ruggine)?
- [ ] Il bottom (pantaloni) è coerente con gli altri shot?

Se anche solo una casella salta → si rigenera, non si tiene "perché bella". La consistenza batte la singola immagine.

---

## Prossimi passi (briefing prima di generare)

1. Confermare i parametri di §4 (tool, luce, bottom, campagna SI di riferimento).
2. Reperire la campagna Stone Island reale da copiare (pose + inquadrature).
3. Procurare una reference pulita della Ghost Piece.
4. Solo dopo: generare shot per shot seguendo §3 + Brief Lookbook in `video-3.md`.
