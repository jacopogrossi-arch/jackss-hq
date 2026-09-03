# Quaderno di esercizi da svolgere

**A che cosa serve.** Gli esercizi che trovi dentro gli schemi sono già svolti: si leggono, non si fanno. Leggere una soluzione dà l'illusione di saperla rifare. Qui invece ci sono **23 tracce senza soluzione** (le soluzioni stanno tutte in fondo, lontane) e, prima di ognuna, la **procedura** della famiglia a cui appartiene: come la riconosci, quali passi fai, dove si sbaglia.

**Regola d'uso: prima si prova, poi si guarda.** Anche male, anche impantanandosi. Il valore sta nel tentativo, non nella lettura della risposta.

Alcune tracce (A1, A2, A3, B3, B10) sono **esercizi della professoressa**, proposti nelle sue slide e mai svolti a lezione: sono le più vicine a quello che può uscire.

---

## Calendario dei cinque giorni

L'esame è **martedì 8 settembre**. Restano cinque giorni pieni.

| Giorno | Argomenti | Esercizi |
|---|---|---|
| **Gio 3/9** | Politica fiscale (01) · Inflazione e Phillips (02) — foglio di lavoro dedicato: *Giorno 1 — giovedì 3 settembre* | A1 → A8 |
| **Ven 4/9** | Monopolio (03) · Benessere (04) · Teoria normativa (11) | A9 → A13 |
| **Sab 5/9** | Lavoro (05) · Economia aperta (06) · Moneta (07) | B1 → B8 |
| **Dom 6/9** | Valutazione progetti (13) + gli argomenti lasciati in disparte: esternalità (08), crescita (09), disuguaglianze (10), fallimenti dello Stato (12), sistema monetario internazionale (14) | B9, B10 |
| **Lun 7/9** | Ripasso: le tre simulazioni da 11 domande della [banca domande](00d-domande-preselezione.md) + rifare **a freddo** gli esercizi sbagliati nei giorni precedenti | — |

**Segnati gli errori.** Ogni volta che sbagli, scrivi accanto alla traccia una crocetta. Lunedì rifai solo quelli: sono l'unico ripasso che rende davvero.

---

## Come si affronta l'esercizio all'esame

Lo scritto dura **un'ora** per due domande aperte e un esercizio. La ripartizione ragionevole è **20 minuti a testa**, con l'esercizio fatto per **primo o per ultimo**, mai in mezzo: è l'unica parte in cui puoi restare bloccato, e non deve rubare tempo alle domande aperte.

**I quattro gesti, sempre gli stessi:**

1. **Scrivi i dati** in colonna, con il simbolo a sinistra, prima di calcolare qualsiasi cosa. Metà degli errori nasce dal leggere il testo e partire a memoria.
2. **Scrivi l'incognita**: che cosa ti sta chiedendo, con che simbolo, in che unità (percentuale o decimale? milioni o unità?).
3. **Scrivi la condizione di equilibrio** del modello, in forma letterale: `Y = C + I + G`, `MR = MC`, `L = M_s`, `VAN = 0`. Poi sostituisci, poi isola. Mai il contrario.
4. **Commenta il risultato in una riga.** "Il moltiplicatore scende da 5 a 2,5 perché l'imposta proporzionale drena reddito a ogni giro." Vale punti quanto il calcolo, e in più ti fa accorgere se il numero è assurdo.

**Le tre trappole ricorrenti:**

- **Percentuali contro decimali.** Nelle curve dei salari e nella Phillips la `u` va in decimali (10% si scrive 0,10); nei tassi di disoccupazione e nel debito/PIL si ragiona in punti percentuali. Sbagliare unità è l'errore più comune e più costoso.
- **Domanda diretta contro domanda inversa.** `P = a − bq` è già inversa (P in funzione di q) e si deriva subito il ricavo marginale. Se il testo dà `q = a − bP`, prima la rovesci.
- **Variazioni contro livelli.** "Di quanto cambia" vuole `ΔY`, "quanto vale" vuole `Y`. Se ti danno una variazione e la formula chiede un livello (o viceversa) il numero esce giusto e la risposta è sbagliata.

---

## Le schede-procedura

Nove famiglie: ogni esercizio del quaderno appartiene a una di queste. Impara il **gesto**, non il numero.

### Scheda 1 — Reddito di equilibrio e moltiplicatore *(schema [01](01-politica-fiscale-bilancio-pubblico.md))*

- **Come la riconosci** — il testo dà una funzione del consumo `C = C_0 + c(Y − T)`, investimenti e spesa pubblica, e chiede il reddito di equilibrio o l'effetto di una manovra.
- **Dati tipici** — `C_0`, `c`, `I`, `G`, `T` (in somma fissa oppure `T = T_0 + tY`), a volte `X` e `M = mY`.
- **I passi** — (1) scrivi `Y = C + I + G` (aggiungi `+ X − M` se aperta); (2) sostituisci le funzioni; (3) raccogli tutta la `Y` a sinistra; (4) il coefficiente che resta davanti alla `Y` è l'inverso del moltiplicatore; (5) per le variazioni usa `ΔY = moltiplicatore · ΔG`, senza rifare tutto il conto.
- **L'errore tipico** — usare `1/(1−c)` quando l'imposta è proporzionale. Con `T = T_0 + tY` il moltiplicatore è `1/(1 − c(1−t))`, in economia aperta `1/(1 − c(1−t) + m)`. E ricorda: il moltiplicatore delle imposte è `−c/(1−c)`, **negativo e più piccolo in valore assoluto** di quello della spesa — è la ragione per cui il teorema di Haavelmo dà 1 e non 0.

### Scheda 2 — Sostenibilità del debito *(schema [01](01-politica-fiscale-bilancio-pubblico.md))*

- **Come la riconosci** — compaiono tasso di interesse, inflazione, crescita e il rapporto debito/PIL, e la domanda è "il rapporto sale o scende?" oppure "quale avanzo primario serve?".
- **Dati tipici** — `i`, `ṗ`, `Ẏ`, il livello di `B/Y`, il saldo primario.
- **I passi** — (1) calcola il tasso reale `i − ṗ`; (2) confrontalo con la crescita reale `Ẏ`: se è maggiore, la palla di neve gonfia il rapporto; (3) quantifica con `Δ(B/Y) ≈ (i − ṗ − Ẏ) · (B/Y) − avanzo primario/Y`; (4) poni l'espressione uguale a zero se ti chiedono l'avanzo necessario.
- **L'errore tipico** — confrontare il tasso **nominale** con la crescita **reale**. I due termini vanno resi omogenei: o entrambi reali (`i − ṗ` contro `Ẏ`) o entrambi nominali (`i` contro `Ẏ + ṗ`).

### Scheda 3 — Curva dei salari, costo pieno e Phillips *(schema [02](02-inflazione-curva-phillips.md))*

- **Come la riconosci** — c'è una relazione fra crescita dei salari e disoccupazione, oppure un mark-up sui costi, e si chiede inflazione o disoccupazione.
- **Dati tipici** — la curva `ẇ = a − b·u`, il mark-up `g`, la produttività `θ` e la sua variazione `θ̇`.
- **I passi** — (1) il tasso naturale `u_N` è quello che annulla `ẇ`; (2) per un dato `u`, calcola `ẇ` dalla curva; (3) passa all'inflazione col costo pieno `π = ẇ − θ̇ + (1+g)˙`; (4) se ci sono le aspettative, `π_t = γ(u_t) + πᵉ_t` con `πᵉ_t = π_(t−1)`, e si itera periodo per periodo.
- **L'errore tipico** — dimenticare `θ̇`. Se la produttività cresce del 2%, salari a +6% danno inflazione al 4%, non al 6%: la produttività **assorbe** una parte della crescita salariale. È il punto teorico dell'intero capitolo.

### Scheda 4 — Monopolio, perdita secca, mercato contendibile *(schema [03](03-concorrenza-imperfetta-monopolio.md))*

- **Come la riconosci** — domanda inversa `P = a − bq` più una funzione di costo, e si chiede quantità, prezzo, perdita secca, indice di Lerner o l'effetto della contendibilità.
- **Dati tipici** — `P = a − bq`; `MC` costante o crescente; oppure `TC = cq + F`.
- **I passi** — (1) `TR = P · q`, poi `MR` (con domanda lineare: stessa intercetta, pendenza doppia); (2) monopolio: `MR = MC`; (3) concorrenza: `P = MC`; (4) perdita secca: triangolo `½ · (q_C − q_M) · [P_M − MC(q_M)]`; (5) Lerner: `(P − MC)/P`; (6) mercato contendibile: `P = ATC`, equazione di secondo grado, si tiene la **radice maggiore**.
- **L'errore tipico** — usare `P_M − P_C` come altezza del triangolo. L'altezza è la distanza fra **prezzo di monopolio e costo marginale nel punto di monopolio**, non fra i due prezzi. E nel contendibile si impone `P = ATC`, mai `P = MC`.

### Scheda 5 — Benessere: Pareto e funzioni di benessere sociale *(schema [04](04-economia-benessere-teoria-normativa.md))*

- **Come la riconosci** — una tabella di utilità con individui in colonna e stati sociali in riga.
- **Dati tipici** — tre individui, tre stati, numeri piccoli.
- **I passi** — (1) confronta gli stati **a coppie**, individuo per individuo: uno domina l'altro solo se nessuno peggiora e almeno uno migliora; (2) applica le tre funzioni di benessere: utilitarista `ΣU_i`, rawlsiana `min(U_i)`, Bergson-Samuelson (di solito il prodotto); (3) commenta le divergenze.
- **L'errore tipico** — dire che uno stato non è Pareto-efficiente perché ha la somma più bassa. Pareto **non somma**: se il confronto è misto (qualcuno guadagna, qualcuno perde) gli stati sono semplicemente non comparabili, ed entrambi restano efficienti.

### Scheda 6 — Obiettivi e strumenti *(schema [11](11-teoria-normativa-obiettivi-strumenti.md))*

- **Come la riconosci** — c'è un **obiettivo** con un valore desiderato (occupazione, reddito, saldo estero) e si chiede il livello dello **strumento** che lo raggiunge.
- **Dati tipici** — produttività `θ`, propensione al consumo `c`, aliquota `t`, investimenti `I`, obiettivo `N` o `Y`.
- **I passi** — (1) scrivi la **forma ridotta**, cioè l'obiettivo in funzione degli strumenti; (2) **rovesciala**: strumento in funzione dell'obiettivo (forma ridotta inversa); (3) sostituisci i numeri; (4) l'**efficacia** dello strumento è il coefficiente che moltiplica lo strumento nella forma ridotta, cioè `dN/dG`.
- **L'errore tipico** — con due obiettivi e due strumenti, provare a risolvere a occhio. Si imposta un **sistema** e si verifica che il determinante non sia nullo: se lo è, i due strumenti agiscono in modo proporzionale e di fatto ne hai uno solo — la regola aurea di Tinbergen non è soddisfatta nonostante il conteggio.

### Scheda 7 — Tassi del mercato del lavoro e legge di Okun *(schema [05](05-mercato-del-lavoro.md), [09](09-crescita-sviluppo.md))*

- **Come la riconosci** — dati di popolazione, occupati e persone in cerca di lavoro; oppure crescita del PIL e variazione della disoccupazione.
- **I passi (tassi)** — (1) forza lavoro `FL = N + U`; (2) disoccupazione `u = U/FL` — denominatore **forza lavoro**; (3) attività `a = FL/Pop` e occupazione `n = N/Pop` — denominatore **popolazione in età lavorativa**; (4) verifica sempre con `n = a · (1 − u)`.
- **I passi (Okun)** — servono **2,5 punti** di crescita **oltre il potenziale** per ridurre la disoccupazione di **1 punto**: `Δu ≈ − (crescita − crescita potenziale) / 2,5`.
- **L'errore tipico** — mettere la popolazione al denominatore del tasso di disoccupazione. Sono tre tassi con **due denominatori diversi**: sbagliarli è l'errore più frequente in assoluto su questo argomento.

### Scheda 8 — Economia aperta: cambio reale, Marshall-Lerner, IS-LM-BP *(schema [06](06-economia-aperta-bilancia-pagamenti.md))*

- **Come la riconosci** — compaiono cambio, competitività, elasticità di esportazioni e importazioni, oppure tre equazioni IS, LM e BP.
- **I passi (cambio reale)** — `ė_r = ṗ + ė − ṗ_w`. Se `ė_r` sale è apprezzamento reale, cioè **perdita** di competitività.
- **I passi (Marshall-Lerner)** — somma le elasticità in valore assoluto: se supera 1 la svalutazione migliora il saldo corrente, altrimenti lo peggiora. Nel breve periodo vale comunque la curva a J.
- **I passi (IS-LM-BP)** — (1) metti IS e LM a sistema e trova `i` e `Y`; (2) sostituisci in BP per vedere se il saldo esterno è in pareggio, avanzo o disavanzo; (3) per una manovra, sposta la curva giusta e ripeti; (4) confronta l'aumento del reddito con quello che ci sarebbe stato a tasso invariato: la differenza è lo **spiazzamento finanziario**.
- **L'errore tipico** — sbagliare il verso del cambio. In questa dispensa `e_r = p·e/p_w`, quindi un **aumento** di `e` è un **apprezzamento** e peggiora la competitività. Prima di rispondere, rileggi il segno.

### Scheda 9 — Moneta e valutazione dei progetti *(schemi [07](07-teorie-macro-moneta-bce.md) e [13](13-valutazione-progetti-acb.md))*

- **Moltiplicatore monetario** — `M = [(1 + h)/(h + j)] · H`, dove `h` è il rapporto circolante/depositi e `j` il coefficiente di riserva. Se ti chiedono la base monetaria necessaria per un dato `M`, dividi invece di moltiplicare.
- **Domanda di moneta** — poni `L(Y, i) = M_s/p` e isola `i`. È l'equazione della LM.
- **VAN e TIR** — (1) attualizza ogni flusso con `(1+i)^t`; (2) `VAN = B − C`; (3) `VAN relativo = (B − C)/C`, e serve a togliere l'effetto dimensione; (4) il **TIR** è il tasso che annulla il VAN: con due periodi diventa un'equazione di secondo grado in `y = 1 + i`, e si tiene la radice positiva.
- **L'errore tipico** — attualizzare anche il costo iniziale. Il flusso al tempo `t = 0` **non si attualizza**: `(1+i)^0 = 1`.

---

# Blocco A — esercizi sugli argomenti core

*Le soluzioni sono nella sezione «Soluzioni», in fondo al quaderno. Prova prima.*

## A1 — Reddito di equilibrio e manovre di finanza pubblica

> **Traccia della professoressa** (proposta nelle slide sul bilancio pubblico e non svolta a lezione).

Un'economia chiusa è descritta da:

```
      Y = C + I + G
      C = 100 + 0,8 (Y − T)
      I = 100
      G = 100
      T = 75
```

a) Calcola il reddito di equilibrio.
b) Che cosa accade se `I` passa da 100 a 50? Calcola il nuovo reddito e confrontalo col precedente.
c) Ripartendo dalla situazione iniziale, che cosa accade se `G` passa da 100 a 150?
d) E se, insieme a `G`, anche `T` aumenta di 50? Che nome ha il risultato che ottieni?

*Riferimento: [schema 01](01-politica-fiscale-bilancio-pubblico.md), moltiplicatore e teorema di Haavelmo.*

## A2 — Lo stesso modello con imposta proporzionale

> **Traccia della professoressa**, dalla stessa sezione.

Stessa economia di A1, ma ora l'imposta è `T = 75 + 0,25 Y`.

a) Calcola il moltiplicatore della spesa pubblica e il reddito di equilibrio.
b) Confronta moltiplicatore e reddito con quelli di A1: perché sono più bassi?
c) Aumenta `G` di 50: di quanto cresce il reddito e di quanto cresce il **gettito**? Il bilancio migliora o peggiora?
d) Aumenta contemporaneamente `G` di 50 e la parte fissa dell'imposta di 50: quanto vale ora il moltiplicatore del bilancio in pareggio? Il teorema di Haavelmo vale ancora?

## A3 — Il modello reddito-spesa in economia aperta

> **Traccia della professoressa**, dalla stessa sezione.

```
      Y = C + I + G + X − M
      C = c (1 − t) Y        con c = 0,8 e t = 0,25
      I = 100
      G = 100
      X = 50
      M = m Y                con m = 0,1
```

a) Calcola il moltiplicatore e il reddito di equilibrio.
b) Qual è il saldo commerciale `X − M` all'equilibrio?
c) Il governo aumenta `G` a 150: calcola il nuovo reddito e il nuovo saldo commerciale.
d) Commenta: perché una manovra espansiva peggiora il saldo con l'estero? Come si chiama il fenomeno per cui la propensione a importare riduce il moltiplicatore?

## A4 — Sostenibilità del debito pubblico

Un paese ha un tasso di interesse nominale sul debito `i = 5%`, un'inflazione `ṗ = 2%`, una crescita reale `Ẏ = 1%` e un rapporto debito/PIL pari al **130%**.

a) Quale avanzo primario (in percentuale del PIL) serve per **stabilizzare** il rapporto debito/PIL?
b) E se la crescita reale salisse al 3%, ferme le altre variabili?
c) E se invece il tasso di interesse salisse al 7%, con crescita all'1%?
d) Commenta: quale delle due leve — crescita o tasso di interesse — è nelle mani del governo, e quale no?

*Riferimento: [schema 01](01-politica-fiscale-bilancio-pubblico.md), condizione `i − ṗ < Ẏ`.*

## A5 — Fiscal drag

Un sistema fiscale ha due scaglioni: **25%** fino a 15.000 euro, **35%** sulla parte eccedente. Un contribuente guadagna 20.000 euro. L'anno seguente l'inflazione è del 10% e il suo reddito nominale sale a 22.000 euro, quindi il suo reddito **reale è invariato**.

a) Calcola imposta pagata e aliquota media nei due anni.
b) Il reddito netto **reale** del contribuente è aumentato, diminuito o rimasto uguale?
c) Come si chiama il fenomeno e come si corregge?

## A6 — Curva dei salari e costo pieno

Il mercato del lavoro di un paese è descritto dalla curva dei salari:

```
      ẇ = 0,42 − 4 · u
```

con `u` espressa **in decimali** (10% si scrive 0,10).

a) Determina il tasso di disoccupazione naturale `u_N`.
b) Se la disoccupazione effettiva è del 7% e la produttività cresce del 2% (`θ̇ = 2%`) con mark-up costante, calcola `ẇ` e l'inflazione `π`.
c) La banca centrale vuole portare l'inflazione all'8%, sempre con `θ̇ = 2%`: quale tasso di disoccupazione è compatibile con quell'obiettivo?
d) Commenta il "prezzo" della disinflazione in termini di posti di lavoro.

## A7 — Phillips con aspettative adattive

Stessa curva dei salari di A6, ma ora con `θ̇ = 0` e mark-up costante, quindi `π_t = γ(u_t) + πᵉ_t`, con aspettative adattive `πᵉ_t = π_(t−1)` (cioè `λ = 1`) e `πᵉ` inizialmente nulla.

a) Il governo mantiene la disoccupazione stabilmente al **7%**, sotto il tasso naturale. Costruisci la tabella dell'inflazione per `t = 0, 1, 2`.
b) Che cosa dimostra questa dinamica sul rapporto di lungo periodo fra inflazione e disoccupazione?
c) Per **ridurre** l'inflazione di 10 punti in un periodo, quale disoccupazione servirebbe?
d) Qual è la conclusione di Friedman e Phelps che questo esercizio illustra?

## A8 — Prezzi di costo pieno (cost-plus)

Un'impresa fissa il prezzo con un mark-up `g = 25%` sul costo del lavoro per unità di prodotto. Il salario annuo per addetto è `w = 30.000` euro e la produttività è `θ = 20` unità di prodotto per addetto.

a) Calcola il prezzo `p`.
b) L'anno seguente i salari crescono del 6% e la produttività del 2%, con mark-up invariato: quanto vale l'inflazione?
c) Se invece, oltre a quelle variazioni, l'impresa alza il mark-up dal 25% al 30%, quanto vale l'inflazione?
d) Quali dei tre termini della formula del costo pieno può controllare un sindacato, e quali una politica dei redditi?

## A9 — Perdita secca di monopolio e indice di Lerner

Un mercato è descritto dalla domanda inversa `P = 60 − 2q` e dal costo marginale `MC = 4q`.

a) Determina quantità e prezzo di monopolio.
b) Determina quantità e prezzo che si avrebbero in concorrenza perfetta.
c) Calcola la perdita secca di benessere.
d) Calcola l'indice di Lerner e commenta che cosa misura.

## A10 — Monopolio naturale e mercato contendibile

Domanda inversa `P = 30 − Q`; costo totale `TC = 6Q + 80`.

a) Verifica che si tratta di un monopolio naturale.
b) Calcola quantità, prezzo e profitto del monopolista protetto.
c) Calcola l'equilibrio in un mercato **contendibile** (profitti nulli) e spiega quale delle due radici va tenuta e perché.
d) Che cosa succederebbe se il regolatore imponesse la regola di *first best* `P = MC`? Quale problema sorge e come si risolve?

## A11 — Efficienza paretiana e funzioni di benessere sociale

Tre individui (1, 2, 3) e tre stati sociali (I, II, III), con le utilità:

| Stato | U1 | U2 | U3 |
|---|---|---|---|
| **I** | 6 | 6 | 6 |
| **II** | 10 | 7 | 2 |
| **III** | 3 | 8 | 9 |

a) Quali stati sono Pareto-efficienti?
b) Quale stato si sceglie con la funzione di benessere **utilitarista**, con quella **rawlsiana** e con quella di **Bergson-Samuelson** nella forma `W = U1 × U2 × U3`?
c) Nel passaggio da I a III l'individuo 1 subisce una perdita valutata 30 euro, mentre gli individui 2 e 3 guadagnano rispettivamente 20 e 60 euro. Il passaggio supera il **criterio di compensazione** di Kaldor? Che cosa significa, esattamente, "superare" quel test?
d) Che cosa dimostra il confronto fra i tre criteri?

## A12 — Obiettivo occupazione e strumento spesa pubblica

> Variante numerica dell'esercizio proposto dalla professoressa nelle slide di teoria normativa.

Il modello è:

```
      Y_off = θ N                    θ = 25
      Y_dom = C + I + G
      C = c Y_d                      c = 0,75
      Y_d = (1 − t) Y
      I = 2.000
```

L'obiettivo è un'occupazione `N = 1.600`.

a) Quale livello di spesa pubblica `G` raggiunge l'obiettivo se `t = 0`?
b) E se `t = 0,2`?
c) Qual è l'**efficacia** dello strumento sull'obiettivo nei due casi?
d) Di quanto cala l'efficacia? A quale teorema visto in politica fiscale si collega il risultato?

## A13 — Due obiettivi, due strumenti (regola aurea di Tinbergen)

Un governo ha due obiettivi — il reddito `Y` e il saldo delle partite correnti `CC` — e due strumenti — la spesa pubblica `G` e il tasso di cambio `e`. La forma ridotta del modello è:

```
      Y  =  2 G + 1 e
      CC = −0,4 G + 0,8 e
```

Gli obiettivi fissi sono `Y* = 500` e `CC* = 0` (pareggio esterno).

a) Calcola i livelli di `G` e `e` che raggiungono entrambi gli obiettivi.
b) Verifica che il sistema sia risolvibile calcolando il determinante. Che cosa significa economicamente?
c) Se il governo disponesse del solo strumento `G`, potrebbe raggiungere entrambi gli obiettivi? Che cosa dovrebbe fare?
d) Supponi che la seconda equazione fosse invece `CC = 1 G + 0,5 e`. Calcola il determinante: che cosa scopri, e che cosa insegna sulla regola aurea di Tinbergen?

---

# Blocco B — esercizi sugli argomenti secondari

## B1 — I tre tassi del mercato del lavoro

In un paese: popolazione totale 200, popolazione in età lavorativa 150, occupati 90, persone in cerca di occupazione 10 (migliaia di persone).

a) Calcola tasso di disoccupazione, tasso di attività e tasso di occupazione.
b) Verifica la coerenza con la relazione `n = a · (1 − u)`.
c) L'anno seguente 5 disoccupati **si scoraggiano** e smettono di cercare lavoro; gli occupati restano 90. Ricalcola i tre tassi.
d) Commenta: il paese sta meglio o peggio? Quale dei tre tassi racconta la verità?

## B2 — Legge di Okun

Il PIL di un paese cresce del **3,5%**, mentre il PIL potenziale cresce del **2%**. La disoccupazione di partenza è del 9%. Applica la legge di Okun nella versione della dispensa (servono circa 2,5 punti di crescita oltre il potenziale per ridurre la disoccupazione di 1 punto).

a) Di quanto varia il tasso di disoccupazione? A quanto arriva?
b) Quale tasso di crescita servirebbe per portare la disoccupazione dal 9% al 7% in un anno? È realistico?
c) Perché il rapporto è "più che proporzionale"? (È il punto che la domanda d'esame chiede di spiegare, non il numero.)

## B3 — Variazione del cambio reale

> **Traccia della professoressa** (esercizio proposto in una slide su bilancia dei pagamenti e competitività).

Il tasso di cambio nominale si **apprezza del 2%**, l'inflazione interna è dell'**1%** e quella estera del **2%**.

a) Calcola la variazione del tasso di cambio reale.
b) L'inflazione relativa (interna meno estera) di quanto contribuisce?
c) La variazione calcolata indica un **aumento** o una **perdita** di competitività? Perché?

*Attenzione alla convenzione della dispensa: `e_r = p·e/p_w`, quindi un aumento di `e` è un apprezzamento.*

## B4 — Condizione di Marshall-Lerner

Un paese svaluta la propria moneta del 10%.

a) Se l'elasticità della domanda di esportazioni è 0,6 e quella delle importazioni 0,3, il saldo corrente migliora o peggiora?
b) E se le elasticità fossero 0,9 e 0,5?
c) Quali sono le quattro ipotesi sotto cui vale la condizione?
d) Che cosa dice la curva a J sul comportamento del saldo **nei mesi immediatamente successivi** alla svalutazione, e perché?

## B5 — IS-LM-BP completo

Un'economia aperta è descritta da:

```
      IS:  Y = 2.200 − 4.000 i
      LM:  M_s/p = 0,25 Y − 1.000 i        con M_s/p = 450
      BP:  CC = 250 − 0,1 Y
           MK = 2.000 i − 150
```

**dove:** `CC` = saldo delle partite correnti · `MK` = saldo dei movimenti di capitale · `BP = CC + MK`.

a) Calcola il tasso di interesse e il reddito di equilibrio interno.
b) Verifica se la bilancia dei pagamenti è in pareggio.
c) Il governo attua una manovra fiscale espansiva che sposta la IS a `Y = 2.400 − 4.000 i`. Calcola il nuovo equilibrio.
d) Il reddito è cresciuto di 200, come lo spostamento della IS? Quanto vale lo **spiazzamento finanziario**?
e) Che cosa succede ora alla bilancia dei pagamenti, e come si chiude il sistema in **cambi flessibili** e in **cambi fissi**?

## B6 — Costi comparati

Le ore di lavoro necessarie a produrre un'unità di ciascun bene sono:

| | Vino | Stoffa |
|---|---|---|
| **Paese A** | 4 | 2 |
| **Paese B** | 12 | 3 |

a) Quale paese ha il vantaggio **assoluto**? In quali beni?
b) Calcola i costi comparati (quante unità di stoffa costa un'unità di vino in ciascun paese).
c) In quale bene si specializza ciascun paese?
d) Entro quale intervallo deve stare la ragione di scambio perché lo scambio convenga a entrambi?

## B7 — Moltiplicatore monetario

Il rapporto circolante/depositi è `h = 0,2`, il coefficiente di riserva è `j = 0,05`, la base monetaria è `H = 500`.

a) Calcola il moltiplicatore monetario e l'offerta di moneta.
b) La banca centrale vuole portare l'offerta di moneta a 3.000, a parità di `h` e `j`: quanta base monetaria deve creare in più?
c) Le banche però aumentano le riserve libere e `j` sale a 0,10. Con la base monetaria del punto (b), quanto vale ora l'offerta di moneta?
d) Come si chiama il problema illustrato dal punto (c)?

## B8 — Domanda di moneta ed equilibrio del mercato monetario

La domanda di moneta è `L = 0,3 Y + 150 − 2.000 i`, l'offerta reale è `M_s/p = 600` e il reddito è `Y = 2.000`.

a) Calcola il tasso di interesse di equilibrio.
b) La banca centrale porta l'offerta reale a 700: quale diventa il tasso di equilibrio?
c) Quale delle tre motivazioni keynesiane della domanda di moneta è rappresentata dal termine `0,3 Y` e quale dal termine `− 2.000 i`?
d) In quale situazione la manovra del punto (b) non avrebbe alcun effetto sul tasso?

## B9 — Analisi costi-benefici: VAN, VAN relativo e TIR

Un comune deve scegliere fra due progetti. Il tasso di sconto sociale è `i = 4%`. I flussi (in migliaia di euro) sono:

| Progetto | costo a t=0 | beneficio a t=1 | beneficio a t=2 |
|---|---|---|---|
| **A** | 500 | 300 | 360 |
| **B** | 200 | 150 | 125 |

a) Calcola il VAN assoluto dei due progetti. Sono entrambi ammissibili?
b) Calcola il VAN relativo. La graduatoria cambia?
c) Calcola il TIR di entrambi.
d) Quale progetto scegli, e con quale motivazione? Che cosa succede se il tasso di sconto sale al 20%?

## B10 — IS-LM: moltiplicatore e spiazzamento (domanda aperta con grafico)

> **Formulazione esatta** trovata nel materiale del corso ("Compito di ripasso teorie"). Non è un esercizio numerico: è una domanda aperta con grafico, ed è il formato più probabile per una delle due domande dello scritto.

Utilizza il modello IS-LM per spiegare, **anche graficamente**, le affermazioni seguenti:

a) La politica fiscale (aumento della spesa pubblica) è efficace per la stabilizzazione della domanda aggregata (il moltiplicatore "keynesiano").
b) Un aumento della spesa pubblica non accompagnato da un aumento dell'offerta di moneta (politica economica non "accomodante") provoca un aumento del tasso di interesse e quindi una riduzione degli investimenti privati (spiazzamento finanziario).

*Suggerimento: la risposta al punto (b) è già mezza fatta nell'esercizio B5, punto (d). Fai il grafico prima di scrivere.*

---

# Soluzioni

*Guarda una soluzione solo dopo aver provato. Se il risultato non torna, cerca prima l'errore da solo: quasi sempre è un'unità di misura o un segno.*

### Soluzione A1

**(a) Reddito di equilibrio**

```
      Y = C + I + G
      Y = 100 + 0,8 (Y − 75) + 100 + 100
      Y = 100 + 0,8Y − 60 + 200
      Y − 0,8Y = 240
      0,2 Y = 240
      Y = 1.200
```

Il moltiplicatore è `1/(1 − 0,8) = 5`.

**(b) Investimenti da 100 a 50**

```
      ΔY = 5 · ΔI = 5 · (−50) = −250
      Y = 1.200 − 250 = 950
```

**dove:** `ΔI` = variazione degli investimenti · il moltiplicatore trasforma una caduta di 50 in una caduta di reddito **cinque volte più grande**: è l'effetto a catena per cui il reddito perso da qualcuno è la domanda persa di qualcun altro.

**(c) Spesa pubblica da 100 a 150**

```
      ΔY = 5 · ΔG = 5 · 50 = +250
      Y = 1.200 + 250 = 1.450
```

Una manovra di spesa di 50 compensa **esattamente** il crollo di 50 degli investimenti del punto (b): è la stabilizzazione keynesiana.

**(d) `G` e `T` aumentano entrambi di 50**

```
      effetto della spesa:    ΔY = +1/(1−c) · ΔG = 5 · 50 = +250
      effetto dell'imposta:   ΔY = −c/(1−c) · ΔT = −4 · 50 = −200
      effetto netto:          ΔY = +50
```

```
      verifica diretta:
      Y = 100 + 0,8 (Y − 125) + 100 + 150
      0,2 Y = 250   →   Y = 1.250        ✓  (1.200 + 50)
```

**È il teorema di Haavelmo**: un aumento di spesa **interamente finanziato** da un pari aumento delle imposte fa crescere il reddito esattamente dell'importo della manovra — il moltiplicatore del bilancio in pareggio vale **1**. La ragione è che `G` entra nella domanda per intero, mentre `T` la riduce solo per la quota consumata `c`: la differenza `1 − c` è ciò che resta.

### Soluzione A2

**(a) Moltiplicatore e reddito**

```
      Y = 100 + 0,8 [ Y − 75 − 0,25Y ] + 100 + 100
      Y = 100 + 0,8 (0,75 Y − 75) + 200
      Y = 100 + 0,6 Y − 60 + 200
      0,4 Y = 240
      Y = 600
```

```
      moltiplicatore = 1/(1 − c(1−t)) = 1/(1 − 0,8 · 0,75)
                     = 1/0,4 = 2,5
```

**(b) Confronto con A1** — il moltiplicatore scende da **5 a 2,5** e il reddito da **1.200 a 600**. Il motivo: a ogni giro del moltiplicatore lo Stato preleva il 25% del reddito aggiuntivo, quindi solo `0,75` arriva alle famiglie e solo `0,8 · 0,75 = 0,6` torna in consumo. La catena si spegne prima. È l'aspetto di **stabilizzatore automatico** dell'imposta proporzionale: attutisce sia le espansioni sia le recessioni.

**(c) Aumento di `G` di 50**

```
      ΔY = 2,5 · 50 = +125          →  Y = 725
      ΔT = 0,25 · ΔY = 0,25 · 125 = +31,25
```

Il gettito cresce di 31,25 a fronte di una spesa in più di 50: **il bilancio peggiora di 18,75**. Una parte della manovra si autofinanzia, ma solo una parte.

**(d) `G` e la parte fissa dell'imposta aumentano entrambi di 50**

```
      effetto della spesa:     ΔY = +2,5 · 50 = +125
      effetto dell'imposta:    ΔY = −c/(1−c(1−t)) · ΔT_0
                                  = −(0,8/0,4) · 50 = −100
      effetto netto:           ΔY = +25

      moltiplicatore del bilancio in pareggio = 25/50 = 0,5
```

**Il teorema di Haavelmo non vale più**: il moltiplicatore del bilancio in pareggio scende da 1 a 0,5. È lo stesso meccanismo che nell'esercizio A12 fa crollare l'efficacia della spesa pubblica come strumento di politica economica.

### Soluzione A3

**(a) Moltiplicatore e reddito**

```
      Y = 0,8 · 0,75 Y + 100 + 100 + 50 − 0,1 Y
      Y = 0,6 Y − 0,1 Y + 250
      Y (1 − 0,6 + 0,1) = 250
      0,5 Y = 250
      Y = 500
```

```
      moltiplicatore = 1/(1 − c(1−t) + m) = 1/0,5 = 2
```

**dove:** `m` = propensione marginale a importare. Compare con il segno **più** al denominatore perché ogni euro di domanda in più si disperde in parte all'estero: è una **dispersione** del moltiplicatore, come l'imposta.

**(b) Saldo commerciale**

```
      M = 0,1 · 500 = 50
      X − M = 50 − 50 = 0        →  pareggio
```

**(c) Spesa pubblica a 150**

```
      Y = (100 + 150 + 50)/0,5 = 600
      M = 0,1 · 600 = 60
      X − M = 50 − 60 = −10      →  disavanzo
```

**(d) Commento** — la manovra fa crescere il reddito di 100, ma il reddito più alto tira su le importazioni (che dipendono da `Y`) mentre le esportazioni restano ferme (dipendono dal reddito **estero**). Il saldo commerciale passa da 0 a −10. È il **vincolo estero** alla politica fiscale: un paese molto aperto non può espandere la domanda interna senza peggiorare i conti con l'estero, e il moltiplicatore stesso è più piccolo perché una parte della spesa "esce" (`1/0,5 = 2` contro `1/0,4 = 2,5` in economia chiusa).

### Soluzione A4

**(a) Avanzo primario necessario**

```
      Δ(B/Y) ≈ (i − ṗ − Ẏ) · (B/Y) − avanzo primario/Y

      tasso reale:      i − ṗ = 5% − 2% = 3%
      differenziale:    3% − 1% = 2%
      effetto palla di neve:  2% · 1,30 = 2,6% del PIL

      per stabilizzare:  avanzo primario = 2,6% del PIL
```

**dove:** `B/Y` = rapporto debito/PIL · l'**avanzo primario** è il saldo di bilancio **al netto degli interessi**: è la parte che il governo controlla davvero.

**(b) Crescita reale al 3%**

```
      (5% − 2% − 3%) = 0   →   basta il PAREGGIO primario
```

Quando il tasso reale eguaglia la crescita, il debito cresce alla stessa velocità del PIL e il rapporto resta fermo da solo. È la condizione `i − ṗ = Ẏ`.

**(c) Tasso di interesse al 7%**

```
      (7% − 2% − 1%) = 4%
      4% · 1,30 = 5,2% del PIL di avanzo primario
```

**(d) Commento** — due punti di interesse in più raddoppiano l'avanzo primario richiesto (da 2,6% a 5,2% del PIL): è uno sforzo di austerità enorme, socialmente e politicamente. Ed è la leva che il governo **non** controlla, perché `i` lo fissa il mercato (e, per l'area euro, la BCE). La crescita invece è la leva "buona" ma lenta. Da qui l'importanza dell'effetto **denominatore**: più il debito è alto, più ogni punto di interesse pesa — con `B/Y = 130%` ogni punto costa 1,3 punti di PIL di avanzo.

### Soluzione A5

**(a) Imposta e aliquota media**

```
      Anno 1 — reddito 20.000
      15.000 · 0,25 = 3.750
       5.000 · 0,35 = 1.750
      T = 5.500        aliquota media = 5.500/20.000 = 27,5%

      Anno 2 — reddito 22.000
      15.000 · 0,25 = 3.750
       7.000 · 0,35 = 2.450
      T = 6.200        aliquota media = 6.200/22.000 = 28,18%
```

**(b) Reddito netto reale**

```
      Anno 1:  20.000 − 5.500 = 14.500
      Anno 2:  22.000 − 6.200 = 15.800 nominali
               15.800 / 1,10 = 14.363,6 reali

      perdita reale = 14.500 − 14.363,6 ≈ 136 euro
```

Il contribuente ha lo **stesso reddito reale** ma paga più imposte in termini reali: ha perso potere d'acquisto senza che nessuno abbia votato un aumento delle tasse.

**(c) Nome e correzione** — è il **fiscal drag** (drenaggio fiscale): l'inflazione spinge il reddito **nominale** verso scaglioni più alti, alzando l'aliquota media anche a reddito reale invariato. Si corregge **indicizzando all'inflazione gli scaglioni** (e le detrazioni). È una forma di aumento occulto della pressione fiscale: nasconde una decisione politica dentro un fenomeno monetario.

### Soluzione A6

**(a) Tasso naturale**

```
      ẇ = 0   →   0,42 − 4 u_N = 0
      4 u_N = 0,42
      u_N = 0,105        →  10,5%
```

**(b) Disoccupazione al 7%**

```
      ẇ = 0,42 − 4 · 0,07 = 0,42 − 0,28 = 0,14      →  14%

      costo pieno:  π = ẇ − θ̇ + (1+g)˙
                    π = 14% − 2% + 0 = 12%
```

**dove:** `θ̇` = tasso di crescita della produttività · `(1+g)˙` = variazione del mark-up. Con `u = 7%` sotto il naturale del 10,5%, il mercato del lavoro è surriscaldato e i salari corrono; ma **la produttività ne assorbe 2 punti**, quindi l'inflazione è 12% e non 14%.

**(c) Obiettivo di inflazione all'8%**

```
      π = ẇ − θ̇   →   8% = ẇ − 2%   →   ẇ = 10%

      0,10 = 0,42 − 4 u
      4 u = 0,32
      u = 0,08         →  8%
```

**(d) Commento** — per far scendere l'inflazione dal 12% all'8% (4 punti) bisogna far salire la disoccupazione dal 7% all'8% (1 punto). È il **tasso di sacrificio**: la disinflazione ha un prezzo in posti di lavoro. Le alternative che non passano dalla disoccupazione sono due, e sono esattamente i due temi del capitolo: la **politica dei redditi** (sposta la curva invece di muoversi lungo di essa) e le **politiche per la produttività** (alzano `θ̇`, che entra col segno meno).

### Soluzione A7

**(a) Tabella dell'inflazione**

```
      γ(7%) = 0,42 − 4 · 0,07 = 0,14   →  14%  in ogni periodo
```

| t | `πᵉ_t` | `u_t` | `π_t = γ(u_t) + πᵉ_t` |
|---|---|---|---|
| 0 | 0% | 7% | 14% |
| 1 | 14% | 7% | 28% |
| 2 | 28% | 7% | 42% |

**(b) Che cosa dimostra** — tenere la disoccupazione **sotto** il tasso naturale non produce un'inflazione più alta ma **stabile**: produce un'inflazione che **accelera** senza limite, 14 punti in più a ogni periodo. Il guadagno in occupazione si paga con un'inflazione che non si ferma mai.

**(c) Disinflazione**

```
      serve γ(u) = −10%:
      −0,10 = 0,42 − 4 u
      4 u = 0,52
      u = 0,13         →  13%
```

Per **togliere** 10 punti di inflazione serve portare la disoccupazione al 13%, cioè 2,5 punti **sopra** il naturale. La simmetria è brutale: l'inflazione si accumula in fretta e si smaltisce lentamente.

**(d) Conclusione di Friedman e Phelps** — nel **lungo periodo** la curva di Phillips è **verticale** in corrispondenza del tasso naturale `u_N`. Non esiste un trade-off permanente fra inflazione e disoccupazione: la politica monetaria può comprare occupazione solo finché **inganna** le aspettative, e ogni volta il prezzo è un livello di inflazione più alto. Da qui l'argomento a favore delle **regole** contro la discrezionalità ([schema 11](11-teoria-normativa-obiettivi-strumenti.md)).

### Soluzione A8

**(a) Prezzo**

```
      p = (1 + g) · w/θ
        = 1,25 · 30.000/20
        = 1,25 · 1.500
        = 1.875
```

**dove:** `w/θ` = **costo del lavoro per unità di prodotto** (quanto lavoro, in euro, sta dentro un'unità di prodotto) · `(1 + g)` = il ricarico che l'impresa applica sopra quel costo.

**(b) Inflazione con mark-up costante**

```
      π = ẇ − θ̇ + (1+g)˙
        = 6% − 2% + 0
        = 4%
```

**(c) Con aumento del mark-up dal 25% al 30%**

```
      variazione del mark-up:  (1,30 − 1,25)/1,25 = 0,04   →  4%

      π = 6% − 2% + 4% = 8%
```

Attenzione: il mark-up passa da 25% a 30%, ma la **variazione** che entra nella formula è quella di `(1+g)`, cioè da 1,25 a 1,30, che è il **4%** — non 5 punti percentuali.

**(d) Chi controlla che cosa**

| Termine | Chi lo muove |
|---|---|
| `ẇ` (salari) | Contrattazione sindacale · politica dei redditi (moderazione salariale concordata) |
| `θ̇` (produttività) | Investimenti, formazione, innovazione: politiche **strutturali**, lente |
| `(1+g)˙` (mark-up) | Le imprese, tanto più liberamente quanto meno il mercato è concorrenziale → **politiche per la concorrenza** ([schema 03](03-concorrenza-imperfetta-monopolio.md)) |

Il punto d'esame: l'inflazione da costi **non si combatte solo con la politica monetaria**. Ognuno dei tre termini ha una politica economica diversa che lo governa.

### Soluzione A9

**(a) Equilibrio di monopolio**

```
      TR = P · q = (60 − 2q) · q = 60q − 2q²
      MR = 60 − 4q                (stessa intercetta, pendenza doppia)

      MR = MC:   60 − 4q = 4q
                 60 = 8q
                 q_M = 7,5
                 P_M = 60 − 2 · 7,5 = 45
```

**(b) Equilibrio concorrenziale**

```
      P = MC:    60 − 2q = 4q
                 60 = 6q
                 q_C = 10
                 P_C = 60 − 2 · 10 = 40
```

**(c) Perdita secca**

```
      MC nel punto di monopolio:  MC(7,5) = 4 · 7,5 = 30

      DWL = ½ · (q_C − q_M) · [ P_M − MC(q_M) ]
          = ½ · (10 − 7,5) · (45 − 30)
          = ½ · 2,5 · 15
          = 18,75
```

```
      verifica con l'integrale:
      DWL = ∫ da 7,5 a 10 di (60 − 2q − 4q) dq
          = [ 60q − 3q² ] da 7,5 a 10
          = (600 − 300) − (450 − 168,75)
          = 300 − 281,25 = 18,75      ✓
```

**dove:** l'altezza del triangolo è la distanza fra **prezzo di monopolio e costo marginale nel punto di monopolio**, non fra i due prezzi: è il valore che i consumatori attribuiscono all'ultima unità meno quanto costa produrla.

**(d) Indice di Lerner**

```
      L = (P_M − MC(q_M))/P_M = (45 − 30)/45 = 1/3 ≈ 0,333
```

Misura il **potere di mercato**: quanta parte del prezzo è ricarico sopra il costo marginale. Vale 0 in concorrenza perfetta (dove `P = MC`) e tende a 1 quanto più l'impresa è capace di prezzare sopra i costi. Qui un terzo del prezzo è puro potere di monopolio. Da non confondere con la perdita secca: **Lerner misura il ricarico, DWL misura il benessere distrutto**.

### Soluzione A10

**(a) Verifica del monopolio naturale**

```
      ATC = TC/Q = (6Q + 80)/Q = 6 + 80/Q
      MC = 6
```

`ATC` è **decrescente** per ogni `Q` (il costo fisso 80 si spalma su più unità) e resta **sempre sopra** il costo marginale. Due imprese che si dividessero la stessa quantità duplicherebbero il costo fisso: il costo è **subadditivo**, un'unica impresa produce a costo minore. È un monopolio naturale.

**(b) Monopolista protetto**

```
      TR = (30 − Q) Q = 30Q − Q²
      MR = 30 − 2Q

      MR = MC:   30 − 2Q = 6   →   Q_M = 12
      P_M = 30 − 12 = 18
      profitto = 18 · 12 − (6 · 12 + 80) = 216 − 152 = 64
```

**(c) Mercato contendibile**

Si impone profitto nullo, cioè `P = ATC`:

```
      30 − Q = 6 + 80/Q
      30Q − Q² = 6Q + 80
      Q² − 24Q + 80 = 0

      Q = [ 24 ± √(576 − 320) ] / 2 = (24 ± 16)/2

      Q = 4   oppure   Q = 20
```

- A `Q = 4`: `P = 26` e `ATC = 6 + 20 = 26`. Non è stabile: a quantità intermedie (es. `Q = 12`) il prezzo di domanda (18) supera l'`ATC` (12,7), quindi un entrante può inserirsi con un prezzo più basso e guadagnare comunque.
- A **`Q = 20`**: `P = 10` e `ATC = 6 + 4 = 10`. Oltre questa quantità il prezzo di domanda scende sotto il costo medio: nessun entrante ha convenienza a espandersi. È l'equilibrio **stabile**, a prova di *hit and run*.

**Regola da ricordare: si tiene sempre la radice maggiore.**

Rispetto al monopolio protetto (`Q = 12`, `P = 18`, profitto 64), la sola **minaccia** di entrata porta la quantità a 20 e il prezzo a 10, azzerando il profitto — pur restando un'unica impresa a produrre.

**(d) Regola di first best `P = MC`**

```
      P = 6   →   Q = 30 − 6 = 24
      ricavi = 6 · 24 = 144
      costi  = 6 · 24 + 80 = 224
      perdita = −80          (esattamente il costo fisso)
```

Il prezzo pari al costo marginale è **Pareto-efficiente** ma manda l'impresa in perdita, perché con costi medi decrescenti `MC < ATC` sempre. Le soluzioni: un **sussidio** pari al costo fisso (ma va finanziato con imposte distorsive), oppure la regola di **second best `P = ATC`**, che copre i costi e azzera il profitto rinunciando a un pezzo di efficienza. È il punto in cui questo esercizio incontra il **teorema del second best** ([schema 04](04-economia-benessere-teoria-normativa.md)).

### Soluzione A11

**(a) Stati Pareto-efficienti**

Si confrontano a coppie, individuo per individuo:

- **I vs II**: 6→10 sale, 6→7 sale, 6→2 **scende** → confronto misto.
- **I vs III**: 6→3 **scende**, 6→8 sale, 6→9 sale → confronto misto.
- **II vs III**: 10→3 **scende**, 7→8 sale, 2→9 sale → confronto misto.

In ogni confronto qualcuno guadagna e qualcuno perde: nessuno stato domina un altro.

**→ Tutti e tre gli stati sono Pareto-efficienti.** È il limite classico del criterio paretiano: **ordinamento incompleto**, non permette di scegliere.

**(b) Le tre funzioni di benessere sociale**

| Stato | Utilitarista `ΣU_i` | Rawlsiana `min(U_i)` | Bergson-Samuelson `U1×U2×U3` |
|---|---|---|---|
| I | 18 | **6** | **216** |
| II | 19 | 2 | 140 |
| III | **20** | 3 | **216** |

- **Utilitarista** → sceglie **III** (somma massima, 20), incurante di come è distribuita.
- **Rawlsiana** → sceglie **I** (l'individuo che sta peggio ha 6, contro 2 e 3 negli altri stati): l'unico perfettamente egualitario.
- **Bergson-Samuelson** → **pareggio fra I e III** (216 entrambi): il criterio, in questa forma, **non discrimina**. È un risultato interessante: la funzione moltiplicativa premia sia il totale sia l'uniformità, e qui i due effetti si compensano esattamente.

**(c) Criterio di compensazione (Kaldor)**

```
      guadagni:  20 + 60 = 80
      perdite:   30
      80 > 30    →  il test è SUPERATO
```

Superare il test di Kaldor significa che i vincitori **potrebbero** risarcire integralmente il perdente (30 euro) e restare comunque in guadagno (80 − 30 = 50). **Potrebbero**: la compensazione è solo **potenziale**, non deve avvenire davvero. È esattamente ciò che rende il criterio contestabile — dichiara "un miglioramento" una situazione in cui qualcuno resta effettivamente peggio di prima.

**(d) Che cosa dimostra il confronto** — i tre stati sono ugualmente efficienti secondo Pareto, ma i criteri li ordinano in modo **diverso e inconciliabile**. La scelta dipende interamente dal **giudizio di valore** incorporato nella funzione di benessere, cioè da quanto peso si dà all'efficienza rispetto all'equità. Non esiste una risposta neutra: il compito della teoria normativa è **dichiarare esplicitamente** quale criterio si sta adottando, non nasconderlo dietro la tecnica.

### Soluzione A12

**(a) Spesa pubblica con `t = 0`**

Prima la forma ridotta (obiettivo in funzione degli strumenti):

```
      N = (1/θ) · [ 1/(1 − c(1−t)) ] · (I + G)
```

**dove:** `(1/θ)` traduce reddito in occupazione (con `θ = 25`, ogni addetto produce 25 unità) · la parentesi quadra è il moltiplicatore keynesiano · `(I + G)` è la domanda autonoma.

Poi la si **rovescia** (strumento in funzione dell'obiettivo):

```
      G = θ (1 − c(1−t)) · N − I
```

Con `t = 0`:

```
      moltiplicatore = 1/(1 − 0,75) = 4
      I + G = N · θ / 4 = 1.600 · 25/4 = 10.000
      G = 10.000 − 2.000 = 8.000
```

**(b) Spesa pubblica con `t = 0,2`**

```
      moltiplicatore = 1/(1 − 0,75 · 0,8) = 1/0,4 = 2,5
      I + G = 1.600 · 25/2,5 = 16.000
      G = 16.000 − 2.000 = 14.000
```

Per lo **stesso** obiettivo di occupazione serve una spesa pubblica quasi doppia.

**(c) Efficacia dello strumento**

L'efficacia è la derivata dell'obiettivo rispetto allo strumento, cioè il coefficiente che moltiplica `G` nella forma ridotta:

```
      t = 0:     dN/dG = (1/25) · 4   = 0,16
      t = 0,2:   dN/dG = (1/25) · 2,5 = 0,10
```

Con `t = 0` ogni euro di spesa crea 0,16 posti di lavoro; con `t = 0,2` solo 0,10.

**(d) Calo dell'efficacia e collegamento**

```
      (0,16 − 0,10)/0,16 = 0,375     →  −37,5%
```

L'imposta proporzionale **riduce l'efficacia dello strumento fiscale di oltre un terzo**, perché drena reddito a ogni giro del moltiplicatore. È lo stesso identico meccanismo del **teorema di Haavelmo** dell'esercizio A2: il moltiplicatore del bilancio in pareggio vale 1 con imposta in somma fissa e **crolla a 0,5** con aliquota proporzionale. Due esercizi, due capitoli, un solo meccanismo.

### Soluzione A13

**(a) Livelli degli strumenti**

Si mette a sistema la forma ridotta imponendo i valori obiettivo:

```
      500 =  2 G + 1 e
        0 = −0,4 G + 0,8 e
```

```
      dalla seconda:   0,8 e = 0,4 G   →   e = 0,5 G

      sostituendo:     500 = 2 G + 0,5 G = 2,5 G
                       G = 200
                       e = 100
```

```
      verifica:  Y  = 2 · 200 + 100 = 500          ✓
                 CC = −0,4 · 200 + 0,8 · 100 = 0   ✓
```

**(b) Determinante**

```
      det = (2 · 0,8) − (1 · (−0,4)) = 1,6 + 0,4 = 2 ≠ 0
```

Diverso da zero, quindi il sistema ha **una e una sola soluzione**. Economicamente: i due strumenti sono **linearmente indipendenti**, cioè agiscono sui due obiettivi in proporzioni **diverse**. La spesa pubblica alza il reddito e peggiora il saldo estero; il cambio alza il reddito ma **migliora** il saldo estero. Proprio perché il loro "profilo di effetti" è diverso, combinandoli si può centrare qualsiasi coppia di obiettivi.

**(c) Con il solo strumento `G`**

No. Con un solo strumento si può raggiungere **un solo obiettivo**: fissando `G = 250` si otterrebbe `Y = 500` ma `CC = −100`, un disavanzo. Il governo dovrebbe **rinunciare a un obiettivo** — trattandolo come obiettivo **flessibile** invece che fisso — oppure adottare il **metodo delle priorità**: raggiungere il più importante e accettare per l'altro il valore che ne risulta.

**(d) Con `CC = 1 G + 0,5 e`**

```
      det = (2 · 0,5) − (1 · 1) = 1 − 1 = 0
```

Determinante **nullo**: il sistema non ha soluzione (o ne ha infinite). I due strumenti hanno effetti **esattamente proporzionali** su entrambi gli obiettivi — la seconda equazione è la prima divisa per 2 — quindi `e` non aggiunge nulla che `G` non faccia già: sono **due strumenti che valgono come uno solo**.

**L'insegnamento sulla regola aurea di Tinbergen**: la regola non dice "conta gli strumenti e conta gli obiettivi". Dice che servono strumenti **linearmente indipendenti** in numero pari agli obiettivi. Contarli non basta: due strumenti che fanno la stessa cosa sono uno strumento. È la precisazione che distingue chi ha capito il teorema da chi ne ricorda l'enunciato.

### Soluzione B1

**(a) I tre tassi**

```
      Passo 1 — Forza lavoro
      FL = N + U = 90 + 10 = 100

      Passo 2 — Tasso di disoccupazione   (denominatore: FORZA LAVORO)
      u = U/FL = 10/100 = 0,10        →  10%

      Passo 3 — Tasso di attività        (denominatore: POPOLAZIONE 15+)
      a = FL/Pop = 100/150 = 0,6667   →  66,7%

      Passo 4 — Tasso di occupazione     (denominatore: POPOLAZIONE 15+)
      n = N/Pop = 90/150 = 0,60        →  60%
```

**Attenzione al dato-trappola**: la popolazione totale è 200, ma non entra in nessuna delle tre formule. Si usa sempre la **popolazione in età lavorativa** (150).

**(b) Verifica**

```
      n = a · (1 − u) = 0,6667 · 0,90 = 0,60      ✓
```

**(c) Cinque disoccupati si scoraggiano**

Chi smette di cercare lavoro **esce dalla forza lavoro**: non è più disoccupato, diventa inattivo.

```
      FL = 90 + 5 = 95

      u = 5/95   = 0,0526    →  5,3%   (era 10%)
      a = 95/150 = 0,6333    →  63,3%  (era 66,7%)
      n = 90/150 = 0,60      →  60%    (invariato)
```

**(d) Commento** — il tasso di disoccupazione si **dimezza** senza che sia stato creato **un solo posto di lavoro**. È l'effetto dei **lavoratori scoraggiati**, e mostra perché il tasso di disoccupazione, da solo, è un indicatore fragile: si può abbassare peggiorando la situazione. Il tasso che dice la verità qui è il **tasso di occupazione** (`n = 60%`, immobile), perché ha al denominatore la popolazione e non la forza lavoro — non può essere "migliorato" spostando gente da una categoria all'altra. È esattamente per questo che le statistiche serie affiancano sempre i tre tassi.

### Soluzione B2

**(a) Variazione della disoccupazione**

```
      crescita oltre il potenziale = 3,5% − 2% = 1,5 punti

      Δu ≈ − 1,5/2,5 = −0,6 punti

      nuovo tasso: 9% − 0,6% = 8,4%
```

**(b) Crescita necessaria per −2 punti**

```
      servono 2 · 2,5 = 5 punti di crescita oltre il potenziale
      crescita richiesta = 2% + 5% = 7%
```

**Non è realistico** per un'economia matura: un tasso del 7% è da economia emergente. È il motivo per cui la disoccupazione scende **lentamente** anche quando la ripresa è in corso — e per cui una recessione la fa salire in fretta mentre la ripresa la fa scendere piano (**isteresi**, [schema 05](05-mercato-del-lavoro.md)).

**(c) Perché il rapporto è più che proporzionale** — perché nel frattempo crescono anche la **popolazione** (quindi la forza lavoro: servono nuovi posti solo per non peggiorare) e la **produttività** (quindi ogni addetto produce di più, e a parità di prodotto ne servono meno). Una parte della crescita serve soltanto a **stare fermi**: solo l'eccedenza oltre quella soglia comincia ad assorbire disoccupazione. Ne segue il corollario da citare all'esame: **una crescita positiva ma modesta può convivere con una disoccupazione crescente**.

### Soluzione B3

**(a) Variazione del cambio reale**

```
      ė_r = ṗ + ė − ṗ_w
```

Con la convenzione della dispensa (`e_r = p·e/p_w`, quindi un **aumento** di `e` è un **apprezzamento**), un apprezzamento nominale del 2% significa `ė = +2%`:

```
      ė_r = 1% + 2% − 2% = +1%
```

**(b) Contributo dell'inflazione relativa**

```
      inflazione relativa = ṗ − ṗ_w = 1% − 2% = −1%
```

L'inflazione interna è **più bassa** di quella estera: da sola migliorerebbe la competitività di 1 punto. Ma l'apprezzamento nominale di 2 punti la peggiora più di quanto il differenziale di inflazione la migliori.

**(c) Aumento o perdita di competitività**

`ė_r` è **positivo**: apprezzamento reale, quindi **perdita di competitività** di 1 punto percentuale. I beni nazionali diventano relativamente più cari di quelli esteri, le esportazioni si contraggono e le importazioni crescono.

**Il punto da capire**: i due canali della competitività — **prezzi** e **cambio** — possono muoversi in direzioni opposte. Qui la disciplina sui prezzi interni (inflazione più bassa dell'estero) viene **annullata e superata** dall'apprezzamento del cambio. È il motivo per cui in un'unione monetaria, dove il cambio interno non esiste più, **tutto l'aggiustamento della competitività deve passare dai prezzi e dai salari** — la cosiddetta svalutazione interna.

### Soluzione B4

**(a) Elasticità 0,6 e 0,3**

```
      condizione di Marshall-Lerner:  η_x + η_m > 1

      0,6 + 0,3 = 0,9 < 1     →  NON soddisfatta
```

Il saldo corrente **peggiora**. La svalutazione rende le importazioni più care, ma le quantità reagiscono troppo poco: si paga di più per comprare quasi lo stesso, e il conto peggiora.

**(b) Elasticità 0,9 e 0,5**

```
      0,9 + 0,5 = 1,4 > 1     →  soddisfatta
```

Il saldo corrente **migliora**: l'effetto quantità (più esportazioni, meno importazioni) supera l'effetto prezzo negativo.

**(c) Le quattro ipotesi**

1. Si parte da una situazione di **saldo corrente in pareggio**.
2. L'offerta di beni è **perfettamente elastica** (si può produrre di più senza che i prezzi salgano).
3. I **prezzi interni** non reagiscono alla svalutazione (nessuna spirale svalutazione-inflazione).
4. Nessun effetto sulle **aspettative** di svalutazione futura, che altrimenti innescherebbero un deflusso di capitali peggiorando la bilancia invece di migliorarla.

**(d) Curva a J** — nei primi mesi il saldo **peggiora** prima di migliorare, disegnando una J. Il motivo: i **prezzi cambiano subito** (le importazioni costano immediatamente di più), mentre le **quantità si aggiustano lentamente** — i contratti sono già firmati, i fornitori non si cambiano in un mese, i consumatori non modificano subito le abitudini. Nel brevissimo periodo le elasticità sono quindi molto più basse e Marshall-Lerner **non è soddisfatta**; diventa soddisfatta col tempo, quando le quantità hanno modo di reagire. Il messaggio di politica economica: una svalutazione va giudicata **dopo** qualche trimestre, non subito.

### Soluzione B5

**(a) Equilibrio interno**

Prima si riscrive la LM in forma esplicita:

```
      450 = 0,25 Y − 1.000 i
      0,25 Y = 450 + 1.000 i
      Y = 1.800 + 4.000 i
```

Poi IS = LM:

```
      2.200 − 4.000 i = 1.800 + 4.000 i
      400 = 8.000 i
      i = 0,05                →  5%
      Y = 2.200 − 4.000 · 0,05 = 2.000
```

**(b) Bilancia dei pagamenti**

```
      CC = 250 − 0,1 · 2.000 = 250 − 200 = +50
      MK = 2.000 · 0,05 − 150 = 100 − 150 = −50

      BP = CC + MK = 50 − 50 = 0     →  pareggio esterno
```

L'economia è in **equilibrio interno ed esterno insieme**: un avanzo corrente di 50 finanzia un deflusso di capitali di 50.

**(c) Manovra fiscale espansiva**

```
      2.400 − 4.000 i = 1.800 + 4.000 i
      600 = 8.000 i
      i = 0,075               →  7,5%
      Y = 2.400 − 4.000 · 0,075 = 2.100
```

**(d) Spiazzamento finanziario**

```
      spostamento della IS (a tasso invariato):  +200
      aumento effettivo del reddito:             +100
      spiazzamento:                              100
```

**Metà della manovra è stata spiazzata.** Il meccanismo: più reddito → più domanda di moneta per motivo transattivo → con offerta di moneta **ferma** a 450, il tasso deve salire (dal 5% al 7,5%) per riequilibrare il mercato monetario → il tasso più alto **scoraggia gli investimenti privati**, che si riducono e mangiano metà dell'espansione.

**La lezione**: la politica fiscale è efficace **solo se accomodata** dalla politica monetaria. Se la banca centrale avesse aumentato l'offerta di moneta per tenere il tasso al 5%, il reddito sarebbe cresciuto di 200 pieni. È esattamente la domanda B10.

**(e) Bilancia dei pagamenti dopo la manovra**

```
      CC = 250 − 0,1 · 2.100 = +40     (peggiora: più import)
      MK = 2.000 · 0,075 − 150 = 0     (migliora: capitali in entrata)

      BP = 40 + 0 = +40                 →  AVANZO
```

L'afflusso di capitali attratto dal tasso più alto **più che compensa** il peggioramento del saldo corrente. Come si chiude:

- **Cambi flessibili** — l'avanzo genera domanda di valuta nazionale, che si **apprezza**. L'apprezzamento peggiora la competitività, riduce `CC` e riporta BP a zero. L'apprezzamento però **spiazza le esportazioni**, aggiungendo un secondo spiazzamento a quello finanziario: è il motivo per cui, con alta mobilità dei capitali, **la politica fiscale è debole in cambi flessibili**.
- **Cambi fissi** — la banca centrale deve **difendere la parità**: compra valuta estera cedendo moneta nazionale, quindi le riserve ufficiali e la **base monetaria aumentano**. La LM si sposta a destra, il tasso torna a scendere e il reddito cresce ancora: la manovra fiscale viene **rafforzata**. È il risultato speculare del modello Mundell-Fleming ([schema 06](06-economia-aperta-bilancia-pagamenti.md)).

### Soluzione B6

**(a) Vantaggio assoluto**

Il paese A impiega **meno ore in entrambi** i beni (4 contro 12 nel vino, 2 contro 3 nella stoffa): ha il vantaggio assoluto in tutto. Secondo la teoria dei vantaggi **assoluti** di Smith, non ci sarebbe ragione di commerciare — ed è qui che entra Ricardo.

**(b) Costi comparati**

Si guarda quanto costa un bene **in termini dell'altro** dentro ciascun paese:

```
      Paese A:  1 vino = 4/2 = 2 unità di stoffa
      Paese B:  1 vino = 12/3 = 4 unità di stoffa
```

Letto al contrario:

```
      Paese A:  1 stoffa = 2/4 = 0,5 unità di vino
      Paese B:  1 stoffa = 3/12 = 0,25 unità di vino
```

**(c) Specializzazione**

- Il **paese A** produce vino sacrificando solo 2 stoffe (contro le 4 di B) → **vantaggio comparato nel vino**.
- Il **paese B** produce stoffa sacrificando solo 0,25 vini (contro 0,5 di A) → **vantaggio comparato nella stoffa**.

Ciascuno si specializza dove il **costo-opportunità** è minore, anche se uno dei due è più efficiente in assoluto in entrambi i beni.

**(d) Ragione di scambio**

```
      2 stoffe  <  prezzo internazionale di 1 vino  <  4 stoffe
```

Se un vino si scambia, per esempio, con **3 stoffe**: il paese A ottiene 3 stoffe per un vino che internamente gliene costava 2 (guadagna 1); il paese B ottiene un vino per 3 stoffe quando internamente gliene costava 4 (guadagna 1). **Entrambi guadagnano.** Fuori da quell'intervallo, per uno dei due conviene tornare a produrre in casa.

### Soluzione B7

**(a) Moltiplicatore e offerta di moneta**

```
      moltiplicatore = (1 + h)/(h + j) = (1 + 0,2)/(0,2 + 0,05)
                     = 1,2/0,25 = 4,8

      M = 4,8 · 500 = 2.400
```

**dove:** `h` = rapporto circolante/depositi (quanta parte del denaro il pubblico tiene in contanti) · `j` = coefficiente di riserva (quanta parte dei depositi le banche non prestano) · `H` = base monetaria. Il moltiplicatore è sempre maggiore di 1 perché il sistema bancario **crea moneta** oltre quella emessa dalla banca centrale.

**(b) Base monetaria per `M = 3.000`**

```
      H = M/moltiplicatore = 3.000/4,8 = 625

      base monetaria aggiuntiva = 625 − 500 = 125
```

**(c) Se `j` sale a 0,10**

```
      nuovo moltiplicatore = 1,2/(0,2 + 0,10) = 1,2/0,3 = 4

      M = 4 · 625 = 2.500        invece dei 3.000 desiderati
```

**(d) Il problema** — è il problema di **controllabilità** dell'offerta di moneta: la banca centrale controlla direttamente solo `H`, ma `h` e `j` sono **endogeni**, cioè dipendono dai comportamenti del pubblico e delle banche (e dai tassi correnti e attesi). Le banche che accumulano riserve libere — tipico nelle fasi di sfiducia — spengono il moltiplicatore, e la manovra della banca centrale arriva attenuata o non arriva. È l'argomento centrale contro la ricetta monetarista del controllo diretto degli aggregati monetari, e la ragione per cui le banche centrali moderne governano il **tasso di interesse** invece della quantità di moneta.

### Soluzione B8

**(a) Tasso di equilibrio**

L'equilibrio del mercato monetario è `L = M_s/p`:

```
      0,3 · 2.000 + 150 − 2.000 i = 600
      600 + 150 − 2.000 i = 600
      2.000 i = 150
      i = 0,075               →  7,5%
```

**(b) Offerta reale a 700**

```
      750 − 2.000 i = 700
      2.000 i = 50
      i = 0,025               →  2,5%
```

Un'espansione monetaria di 100 fa scendere il tasso di 5 punti percentuali. La sensibilità è data dal coefficiente 2.000: più la domanda di moneta è sensibile al tasso, meno il tasso deve muoversi per riassorbire la liquidità in più.

**(c) I motivi keynesiani**

- `0,3 Y` → domanda di moneta per motivi **transattivo e precauzionale**: dipende dal reddito, perché più si scambia più contante serve.
- `− 2.000 i` → domanda di moneta **speculativa**: col segno **meno** perché se il tasso sale conviene comprare titoli invece di tenere moneta, che non rende. È il termine che collega moneta e mercato finanziario, e che dà alla LM la sua inclinazione positiva.

**(d) Quando la manovra non avrebbe effetto** — nella **trappola della liquidità**: quando il tasso è già vicino allo zero, la domanda di moneta diventa **piatta** (elasticità infinita rispetto a `i`) e qualunque quantità di moneta in più viene assorbita **senza che il tasso scenda**. La LM diventa orizzontale, la politica monetaria perde presa e resta solo la politica fiscale. È la situazione keynesiana per eccellenza, ed è quella vissuta dalle economie avanzate dopo il 2008.

### Soluzione B9

**(a) VAN assoluto**

Il costo è tutto al tempo `t = 0` e **non si attualizza**.

**Progetto A**

```
      B = 300/1,04 + 360/(1,04)²
        = 300/1,04 + 360/1,0816
        = 288,46 + 332,84
        = 621,30

      VAN_A = 621,30 − 500 = +121,30
```

**Progetto B**

```
      B = 150/1,04 + 125/1,0816
        = 144,23 + 115,57
        = 259,80

      VAN_B = 259,80 − 200 = +59,80
```

Entrambi hanno VAN positivo, quindi **entrambi sono ammissibili**. Sul criterio del VAN assoluto **vince A**.

**(b) VAN relativo**

```
      VAN_r = (B − C)/C

      A:  121,30/500 = 0,2426    →  24,26%
      B:   59,80/200 = 0,2990    →  29,90%
```

**La graduatoria si ribalta: vince B.** A produce più valore in assoluto, ma B ne produce di più **per ogni euro investito**. Il VAN relativo serve proprio a neutralizzare l'**effetto dimensione**: un progetto grande ha quasi sempre un VAN assoluto più alto, senza per questo rendere di più.

**(c) TIR**

Si pone `VAN = 0` e si risolve in `i`. Con due periodi, posto `y = 1 + i`, si ottiene un'equazione di secondo grado.

**Progetto A**

```
      500 y² = 300 y + 360
      500 y² − 300 y − 360 = 0

      y = [ 300 ± √(90.000 + 4 · 500 · 360) ] / 1.000
        = [ 300 ± √810.000 ] / 1.000
        = (300 ± 900)/1.000

      y = 1,20        →  TIR_A = 20%
```

```
      verifica:  300/1,20 = 250  e  360/1,44 = 250
                 250 + 250 = 500 = C     ✓  il VAN si annulla
```

**Progetto B**

```
      200 y² = 150 y + 125
      200 y² − 150 y − 125 = 0

      y = [ 150 ± √(22.500 + 4 · 200 · 125) ] / 400
        = [ 150 ± √122.500 ] / 400
        = (150 ± 350)/400

      y = 1,25        →  TIR_B = 25%
```

**Anche sul TIR vince B.**

**(d) Scelta e sensibilità al tasso**

| Criterio | Vincitore |
|---|---|
| VAN assoluto | **A** (121,30 contro 59,80) |
| VAN relativo | **B** (29,90% contro 24,26%) |
| TIR | **B** (25% contro 20%) |

La risposta corretta è **condizionata al vincolo di bilancio**: senza vincolo di risorse si sceglie **A**, che genera più valore sociale in assoluto (121,30 contro 59,80). Con un vincolo stringente — o potendo replicare il progetto piccolo più volte — si sceglie **B**, che rende di più per euro speso.

**Con tasso di sconto al 20%:**

```
      VAN_A = 300/1,20 + 360/1,44 − 500 = 250 + 250 − 500 = 0
      VAN_B = 150/1,20 + 125/1,44 − 200 = 125 + 86,81 − 200 = +11,81
```

A `i = 20%` il progetto A è **esattamente sulla soglia** (il 20% è il suo TIR, per definizione il tasso che annulla il VAN), mentre B resta ammissibile. **Il progetto grande è molto più sensibile al tasso di sconto**, perché i suoi benefici sono più lontani e pesanti: alzare il tasso li penalizza di più. Da qui l'importanza della scelta del **tasso di sconto sociale**, che non è un dettaglio tecnico ma una decisione politica su quanto peso dare alle generazioni future.

### Soluzione B10

Non è un esercizio numerico: è una domanda aperta con grafico. Ecco l'impostazione che l'esame si aspetta.

**Impostazione comune** — la IS è l'insieme delle combinazioni di `Y` e `i` che equilibrano il **mercato dei beni** (inclinata negativamente: un tasso più basso stimola gli investimenti e quindi il reddito). La LM è l'insieme delle combinazioni che equilibrano il **mercato della moneta** (inclinata positivamente: un reddito più alto alza la domanda di moneta per transazioni e, con offerta data, il tasso deve salire). L'equilibrio è l'intersezione.

**(a) Efficacia della politica fiscale**

Un aumento di `G` sposta la **IS verso destra**, di un ammontare pari a `moltiplicatore × ΔG`. Il nuovo equilibrio ha reddito più alto: la politica fiscale **stabilizza la domanda aggregata**, ed è l'argomento keynesiano centrale contro l'idea che l'economia si autoregoli.

*Nel grafico*: IS che trasla a destra, LM ferma, il punto di equilibrio che risale lungo la LM. Segna sull'asse orizzontale **due** distanze: lo spostamento della IS e l'aumento effettivo di `Y`. Sono diverse, ed è tutto il punto (b).

**(b) Spiazzamento finanziario**

Il reddito più alto fa crescere la **domanda di moneta a scopo transattivo**. Se la banca centrale **non accomoda** la manovra, cioè lascia l'offerta di moneta invariata, l'equilibrio monetario si ristabilisce solo con un **tasso di interesse più alto**. Il tasso più alto **riduce gli investimenti privati**: una parte dell'espansione pubblica sostituisce, invece di aggiungersi, alla spesa privata. È lo **spiazzamento finanziario** (*crowding out*).

*Nel grafico*: lungo la LM, il movimento verso l'alto da `i_0` a `i_1`; l'aumento effettivo di `Y` è **minore** dello spostamento orizzontale della IS, e la differenza è lo spiazzamento.

**I numeri già pronti** — nell'esercizio B5 la IS si sposta di **200** ma il reddito cresce solo di **100**, con il tasso che sale dal 5% al 7,5%: **metà della manovra è spiazzata**. Citare un caso numerico in una domanda aperta vale sempre punti.

**Le due estensioni che completano la risposta:**

- **Politica accomodante**: se la banca centrale espande l'offerta di moneta insieme alla manovra fiscale, la LM si sposta anch'essa a destra, il tasso resta fermo e lo spiazzamento **sparisce**. La politica fiscale è pienamente efficace **solo in accordo con quella monetaria**: è il punto di *policy mix*.
- **I due casi limite**: con LM **orizzontale** (trappola della liquidità) lo spiazzamento è **nullo** e la politica fiscale è massimamente efficace; con LM **verticale** (caso monetarista classico, domanda di moneta insensibile al tasso) lo spiazzamento è **totale** e la politica fiscale non produce alcun aumento del reddito. Le due visioni del capitolo — keynesiana e neoclassica — sono esattamente questi due casi limite dello stesso grafico.
