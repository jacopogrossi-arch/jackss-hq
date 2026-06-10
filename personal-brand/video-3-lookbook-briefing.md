# Briefing generazione lookbook — Video #3 (Stone Island Marina SS26)

Briefing per generare le immagini lookbook con la **stessa logica del video di riferimento**: prendere UNA vera campagna e replicarla 1:1 cambiando solo il modello (→ Jago). Da leggere prima di aprire qualsiasi tool. Più l'idea è bloccata qui, più gli shot escono coerenti.

---

## 0. Decisione presa: copiamo Stone Island Marina SS26

Come il riferimento ha copiato Polo Ralph Lauren "The Heritage Swing" (mondo golf), noi copiamo **Stone Island Marina SS26** (mondo costiero/nautico). Prendiamo tutto il pacchetto: capo hero + ambiente + luce + pose.

**Perché Marina SS26:**
- Ambiente solido e coerente (come la tenuta da golf): un solo mondo = barca a vela + costa ligure + mare.
- È il **DNA originario di Stone Island** (la bussola, il mare) → riconoscibilità immediata.
- Stone Island per Marina **non usa modelli professionisti ma persone reali del mondo creativo** (artisti, musicisti, designer) → Jago, creativo che costruisce un brand, calza perfettamente.

---

## 1. La campagna reale (parametri estratti dalle fonti)

**Stone Island Marina SS26** — foto **Louis Flashman**, video Calum Glenday.

- **Ambiente:** a bordo di una **barca a vela** lungo la **costa ligure**, in condizioni marine reali (vento, salsedine, riverbero), poi transizione alla **riva** (rocce, superfici, texture sotto la luce).
- **Luce:** naturale marina — luminosa, riverbero forte dall'acqua, foschia salina; luce di riva sulle rocce.
- **Hero piece:** la **sailing jacket** classica rivisitata — **cappuccio ripiegabile, chiusure in gomma, tiretti in legno** (dettagli heritage); in alternativa la **coach jacket** in nyco garment-dyed (nylon/cotone) per profondità di colore. Sheen quasi iridescente da garment-dyeing.
- **Simbolo centrale:** la **bussola** (il logo) — "la direzione non è fissa, si riaggiusta di continuo".
- **Palette:** marittima — **navy, ecru/naturale, giallo, bianco**, blu garment-dyed profondo. Ambiente: mare blu + roccia grigia + cielo.
- **Mood:** performance tecnica in condizioni reali, funzionale, resiliente, movimento. Editoriale, non documentario.

> **Da procurare:** 3–5 frame reali della campagna Marina SS26 come reference visiva (pose + inquadrature + luce) da dare in input al generatore. Cercare "Stone Island Marina SS26 campaign" (Dazed, Highsnobiety, stoneisland.com).

---

## 2. I 6 pilastri della consistenza (da bloccare)

| Pilastro | Marina SS26 (reale) | → Nostro |
|---|---|---|
| **Stesso modello** | Persona reale creativa | **Jago** (Soul ID Higgsfield) in ogni shot con volto visibile |
| **Stesso capo bloccato** | Sailing jacket (cappuccio ripiegabile, chiusure gomma, tiretti legno) | **Identica** in ogni shot — stesso colore, stessi dettagli, badge bussola Marina |
| **UN solo mondo** | Barca a vela + costa ligure + mare | **Stesso mondo costiero** per tutti gli shot: barca, riva rocciosa, mare, porticciolo |
| **Una sola luce** | Luce marina naturale, riverbero | Una sola condizione (vedi §4) — non mischiare ore/meteo |
| **Una sola color grade** | Navy/ecru/giallo + mare blu + roccia grigia | Stessa grade marittima in tutti gli shot |
| **Props ricorrenti** | Barca, cime/sartie, tiretti legno, mare | Cime, sartiame, timone, salvagente, roccia — ricorrono e legano gli shot |

**Regola d'oro:** modello + capo + mondo + luce + grade = BLOCCATI. Solo posa e framing cambiano.

---

## 3. Tipi di shot (mappati dal riferimento golf → marina)

| # | Shot riferimento (golf) | → Nostro shot Marina |
|---|---|---|
| 1 | Full body con sacca, in piedi | Full body sul ponte della barca, sailing jacket, mare dietro |
| 2 | Accovacciato con mazza (posa bassa) | Accovacciato sulla roccia di riva / sul ponte, mano su una cima |
| 3 | Azione (golf swing) | Azione: Jago che tira una cima / regola una vela — per il b-roll Seedance |
| 4 | Editoriale ambientale (staccionata + cavalli) | Editoriale: appoggiato alla battagliola della barca, sguardo all'orizzonte |
| 5 | Wide ambiance (figura piccola nel paesaggio) | Wide: figura piccola sulla riva rocciosa, mare e cielo che la inglobano |
| 6 | Dettaglio logo/capo | Close-up badge bussola Marina + dettagli (tiretti legno, chiusure gomma) |

---

## 4. Parametri da BLOCCARE (confermare con Jacopo)

- **Tool/modello:** Higgsfield + **Nano Banana Pro** (come il riferimento), partendo da Soul ID di Jago. *(confermato)*
- **Capo hero:** sailing jacket Marina SS26 (cappuccio ripiegabile, chiusure gomma, tiretti legno) — colore da scegliere tra navy / ecru / giallo. *(da confermare)*
- **Luce/condizione:** UNA tra:
  - **A — Pieno giorno marino**: cielo luminoso, riverbero forte sull'acqua, alto contrasto (più Marina "performance")
  - **B — Foschia salina / cielo coperto**: luce diffusa morbida, palette desaturata (più editoriale/atmosferico)
  - **C — Luce di riva calda**: sole basso sulla costa, rocce calde (più cinematografico)
  *(da confermare — il riferimento resta coerente perché ne usa una sola)*
- **Bottom:** pantaloni coerenti in tutti gli shot — proposta tecnici navy o ecru. *(da confermare)*

---

## 5. Approccio prompt di generazione

Replicando il metodo del riferimento (prompt semplice + reference forti):

1. **Input al modello:** Soul ID di Jago + reference della sailing jacket Marina + 1–2 frame reali della campagna Marina SS26.
2. **Prompt base (stesso per tutti gli shot, cambia solo la posa):**
   > *"Artistic fashion campaign for Stone Island Marina, hero piece the sailing jacket with folding hood, aboard a sailing boat on the Ligurian coast, [POSA/FRAMING dello shot], real maritime conditions, [LUCE scelta], navy/ecru/yellow nautical palette, sea and grey rock environment, editorial campaign quality, indistinguishable from a real Stone Island Marina campaign."*
3. **Cambia solo il blocco [POSA/FRAMING]** shot per shot (vedi §3 e il Brief Lookbook in `video-3.md`).
4. **3–4 varianti per shot**, si seleziona la più forte. Si scartano quelle dove capo/volto/luce/mare derivano.

---

## 6. Checklist di consistenza (prima di approvare ogni shot)

- [ ] È lo stesso volto di Jago?
- [ ] La sailing jacket è identica (cappuccio, chiusure gomma, tiretti legno, colore, badge bussola)?
- [ ] È lo stesso mondo costiero (barca / riva / mare), non un'altra location?
- [ ] La luce/condizione marina è la stessa degli altri shot?
- [ ] La color grade combacia (navy/ecru/giallo + mare blu + roccia)?
- [ ] Il bottom è coerente con gli altri shot?

Se anche solo una casella salta → si rigenera, non si tiene "perché bella". La consistenza batte la singola immagine.

---

## 7. Prossimi passi (briefing prima di generare)

1. Confermare i parametri di §4 (colore capo, luce, bottom).
2. Reperire 3–5 frame reali della campagna Marina SS26 (reference pose/luce).
3. Procurare una reference pulita della sailing jacket Marina.
4. **Rigenerare le moodboard** (le attuali in `video-3-moodboard.md` sono Ghost Piece industriale → ora off-concept).
5. Solo dopo: generare shot per shot seguendo §3 + Brief Lookbook in `video-3.md`.
