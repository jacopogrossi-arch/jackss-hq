# Basic Pant Foundation Armstrong — costruita con i numeri del Drop 1

> Scritto il 02/08/2026, **corretto il 02/08/2026 dopo aver guardato le pagine vere del libro** (pag. 613-614 stampate, "Basic Pant Foundation for Trouser", Figure 1-4 — immagini estratte in sessione da `cartamodelli/prompts/Patternmaking for Fashion Design ( PDFDrive ).pdf`, pagine PDF 620-621). La prima versione di questo foglio (sezioni 3 e 4) era sbagliata: dedotta dal testo senza guardare le figure. Jacopo l'ha beccato disegnando a mano e confrontando con le figure — vedi `feedback_pattern_drafting_verifica.md` in memoria.
>
> **03/08/2026: sezione 4 chiusa.** Riguardate le Figure 3 e 4 ad alta risoluzione: la curva grigia è il centro + cavallo (non il fianco), R e S sono le punte della forchetta, da lì parte l'interno gamba. Il foglio ora è completo: si può disegnare tutto. Il punto aperto rimasto è il compromesso forchetta/coscia (sezione 5), che si risolve col metro di costa e poi sulla tela.

## Come leggere questo foglio

I numeri Drop 1 (`09`) sono già misure di capo finito. Le formule Armstrong si applicano direttamente a quei numeri, senza aggiungere ease una seconda volta.

**Regola imparata a caro prezzo in questa sessione: mai dedurre una posizione da una formula "X–Y = lunghezza" senza sapere la DIREZIONE dalla figura.** Il libro scrive solo la lunghezza del segmento, non la direzione — e in due punti diversi di questo stesso foglio la direzione giusta era quella opposta a quella "ovvia". Ogni valore qui sotto è stato verificato guardando l'immagine della pagina, non dedotto a tavolino.

---

## 1 — Griglia (confermata, invariata)

| Punto | Formula | Calcolo | Valore |
|---|---|---|---|
| A–B | lunghezza vita-orlo | 30 (cavallo) + 72 (int. gamba) | **102** |
| A–C | crotch depth | già misura di capo | **30** |
| C–D | hip depth = ⅓ di C–A | 30 ÷ 3 | **10** (fianchi a 20 da vita) |
| C–E | knee depth = ½ di C–B, meno ~2 | 72÷2 − 2 | **34** (ginocchio a 64 da vita) |

## 2 — Rettangolo di partenza (confermato, invariato)

| Punto | Valore |
|---|---|
| D–F = C–G = A–H (dietro, fianco/cavallo/vita) | **30 cm dal centro** |
| D–J = C–K = A–L (davanti, fianco/cavallo/vita) | **28,5 cm dal centro** |
| X dietro (metà di G–H) | 15 cm sopra G, sul lato |
| X davanti (metà di K–L) | 15 cm sopra K, sul lato |

Il cavallo parte largo quanto il fianco (rettangolo pieno), si ritaglia dopo — non si estende oltre.

---

## 3 — Vita e pieghe — **CORRETTO**

⚠️ La prima versione diceva N a 26,5 e O a 27,5 dal centro (vicino a H/L). **Sbagliato.** Guardando la figura: O e N stanno **vicino al centro**, non vicino a L/H.

| Punto | Formula | Calcolo | Valore |
|---|---|---|---|
| H–M | 3/4" verso il centro, 3/4" più in alto | 30 − 1,9 | **M = 28,1 cm dal centro** (poco sopra la linea vita) |
| M–N | back waist arc + margine = 22,5 (lunghezza, verso il centro da M) | 28,1 − 22,5 | **N = 5,6 cm dal centro** |
| L–O | front waist arc + margine = 27,5 (lunghezza, verso il centro da L) | 28,5 − 27,5 | **O = 1,0 cm dal centro** |

**Pieghe davanti** (Figura 2, `L–Q = ⅓ di L–O`, misurata da L verso il centro):
- Piega 1: **19,3 cm dal centro** (28,5 − 9,2)
- Piega 2: **16,1 cm dal centro** (19,3 − 3,2)
- Lunghezza: 7,6 cm dalla vita, chiusa a punta

**Pinces dietro** (Armstrong ha un solo dart: `H–P = ½ di M–N + 0,5"`, misurata da H verso il centro):
- Dart unico Armstrong: **17,5 cm dal centro** (30 − 12,5)
- Drop 1 vuole 2 pinces da 2 cm: distribuite intorno a 17,5 → **15,5-17,5** e **19,5-21,5 cm dal centro**
- Lunghezza: 8,9 cm dalla vita, chiusa a punta

**Il punto "Z" (centro dietro a 4 cm, inclinazione) inventato nella prima versione non esiste nel metodo — va ignorato.** N sostituisce quel ruolo.

---

## 4 — La curva del cavallo — **RISOLTO** (03/08, riguardando Figure 3 e 4 ad alta risoluzione)

⚠️ Anche la terza interpretazione ("la curva grigia è il fianco") era **sbagliata**. Ritagli delle pagine salvati in `img/armstrong-fig3-cavallo.png`, `img/armstrong-fig4-fascia-crotch.png`, `img/armstrong-formule-cavallo.png` — sono da tenere accanto al foglio mentre si disegna.

**Come stanno davvero le cose (verificato sulle figure):**

- La **curva grigia spessa non è il fianco: è il centro + la curva del cavallo.** Dietro: da M scende lungo il centro dietro inclinato, passa per X, gira l'angolo vicino a G e finisce a **R**, che è la **punta della forchetta dietro**. Davanti, speculare: da L per X, gira vicino a K, finisce a **S**, punta della forchetta davanti.
- Il **fianco (outseam)** è l'altra linea, quella quasi dritta: curva fianchi da **N a D** (dietro) e da **O a D** (davanti), poi da D scende nella gamba fino all'orlo passando vicino a C, fondendosi ("blending with D"). Nella Figura 4 le due linee grigie che scendono da D nel canale tra le gambe sono proprio i due fianchi.
- **Non c'è niente da "chiudere" tra R/S e C**: sono i due lati opposti del pannello. La linea orizzontale "Crotch" (C–W–V) è **solo costruzione, non si taglia**. Da S e da R parte l'**interno gamba (inseam)** che scende fino all'orlo; il pannello nella fascia fianchi–cavallo è delimitato dal cavallo da un lato e dal fianco dall'altro. Il tratto grigio che "continuava nella gamba" oltre R/S era l'inseam che comincia lì — per questo la linea sembrava proseguire.

**I punti della forchetta (formule pag. 614, applicate ai numeri Drop 1):**

| Punto | Formula | Calcolo | Valore |
|---|---|---|---|
| G–R (forchetta dietro) | ½ di G–C | 30 ÷ 2 | **R = 45 cm dal centro** |
| K–S (forchetta davanti) | ¼ di K–C | 28,5 ÷ 4 | **S = 35,6 cm dal centro** |
| G–T e K–U | 1/3" sulla diagonale dell'angolo | — | **0,85 cm** (vedi nota) |

⚠️ **Nota su T e U:** il testo del libro dice 1/3" (0,85 cm), ma nella figura T e U sembrano molto più lontani dall'angolo (~3 cm in scala). La figura è schematica, quindi non fa testo — ma nemmeno la cifra va presa come dogma: la diagonale serve solo a guidare il curvilineo. La curva si disegna da X, sfiora la diagonale, arriva a R (o S); fa fede la **misura di costa** finale, non il punto esatto.

**V e W confermati** (22,8 e 18,1 dal centro): derivano proprio da R=45 e S=35,6 (`R–V = ½ R–C − 0,3` · `S–W = ½ S–C − 0,3`). Da V e W scendono le creaseline, perpendicolari, fino all'orlo.

**La gamba (Figura 4), coi numeri Drop 1, centrata sulle creaseline:**

| Livello | Davanti (creaseline W) | Dietro (creaseline V) |
|---|---|---|
| Ginocchio | 24,5 → **12,25 per lato** | 26,5 → **13,25 per lato** |
| Orlo | 25 → **12,5 per lato** | 27 → **13,5 per lato** |

- **Inseam:** segna 1,3 cm (½") verso l'interno da S e da R, tira una retta fino al segno d'orlo; poi dal ginocchio in su la si curva fino a **toccare S e R** (la cucitura vera passa per le punte).
- **Outseam:** dal segno d'orlo sale dritta fino al ginocchio, poi si fonde in D.

---

## 5 — Sulla forchetta — il conflitto ora ha i numeri

Resta vero che il verdetto finale è della misura di costa e poi della tela — ma ora il conflitto è visibile a tavolino, ed è la versione quantificata del "da tenere d'occhio" di `09`:

- **Forchette Armstrong** (7,1 davanti + 15 dietro): le curve del cavallo vengono lunghe circa quanto serve (obiettivo 32 + 42,5 = 74,5), ma la **coscia** disegnata viene ~34 davanti / ~43 dietro — controllo `09` a 29 / 32, cioè **~15 cm in più a gamba**. È la coscia di un classico ampio anni '40, non del Drop 1.
- **Forchette da `09`** (0,5 + 2): coscia giusta, ma la curva dietro non può fisicamente arrivare a 42,5 (con 30 di profondità e 2 di forchetta si ferma verso i 34-35).

Le due cose non possono essere vere insieme con questa geometria: **la manopola è la forchetta, soprattutto dietro.**

**Ordine di lavoro sul foglio:**
1. Disegnare le curve con le forchette Armstrong (R=45, S=35,6).
2. Misurarle di costa → accorciare la forchetta (spostando R e S verso il centro lungo la linea del cavallo) fino a centrare **32 davanti / 42,5 dietro**.
3. A quel punto misurare la coscia risultante: verrà comunque più larga di 29/32. Annotare di quanto — quella differenza si decide **sulla tela**, non sul foglio (se il cavallo veste, una coscia più piena su un pantalone ampio è il rischio minore; strizzarla a tavolino rischia di rubare forchetta).

[[project-inverso-pantalone-drop1]]
[[feedback_pattern_drafting_verifica]]
