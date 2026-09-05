## Come si usa questo foglio

Stessa logica del giorno 1: tre blocchi, ognuno con teoria minima, un tutorial svolto passo passo e poi le tracce vere da fare da solo. Le **soluzioni** sono in fondo — guardale solo dopo aver provato.

| Blocco | Argomento | Esercizi | Tempo indicativo |
|---|---|---|---|
| 1 | Monopolio, monopolio naturale, mercati contendibili | A9, A10 | 90 minuti |
| 2 | Efficienza paretiana e funzioni di benessere sociale | A11 | 45 minuti |
| 3 | Obiettivi, strumenti e regola di Tinbergen | A12, A13 | 60 minuti |

**Se il tempo non basta**, taglia in questo ordine: A10(d) (è un corollario di A10(a)-(c), non un metodo nuovo), poi A13(c)-(d) (varianti del ragionamento di A13(a)-(b), non calcoli nuovi). A9, A11 e A12 non si tagliano: sono i tre modelli, non le varianti.

**Segna con una crocetta ogni esercizio che sbagli.** Andranno rifatti nel giorno 5.

<div class="pagebreak"></div>

# Blocco 1 — Monopolio, monopolio naturale e mercati contendibili

## La teoria che serve

### Dalla domanda al monopolio: due passaggi, sempre uguali

```
      1) Ricavo totale:      TR = P · q = (a − bq) · q = aq − bq²
      2) Ricavo marginale:   MR = dTR/dq = a − 2bq
```

**dove:** `a` = intercetta della domanda (il prezzo massimo, a quantità zero) · `b` = pendenza della domanda. **Regola pratica da ricordare a memoria: il `MR` ha sempre la stessa intercetta della domanda e pendenza doppia.** Non serve rifare la derivata ogni volta.

Poi l'equilibrio: il monopolista impone **`MR = MC`** (non `P = MC` come in concorrenza perfetta), ricava `q_M`, e sostituisce nella domanda per avere `P_M`. Il confronto che conta sempre è con l'equilibrio **concorrenziale**, dove invece `P = MC`: dà `q_C` e `P_C`, ed è il termine di paragone per misurare quanto il monopolio si allontana dall'efficienza.

### La perdita secca: dove si trova e come si calcola

```
      DWL = ½ · (q_C − q_M) · [ P_M − MC(q_M) ]
```

**dove:** la **base** del triangolo è la quantità che il monopolio non produce rispetto alla concorrenza (`q_C − q_M`) · l'**altezza** è la distanza fra il prezzo di monopolio e il costo marginale **nel punto di monopolio**, `MC(q_M)` — non la distanza fra i due prezzi `P_M` e `P_C`, errore facile da fare. È il valore che i consumatori darebbero a un'unità in più, meno quanto costerebbe produrla.

**L'indice di Lerner** misura invece il ricarico, non il benessere perso:

```
      L = ( P_M − MC(q_M) ) / P_M
```

Vale 0 in concorrenza perfetta e cresce verso 1 quanto più forte è il potere di mercato. **Da non confondere: Lerner misura quanto l'impresa ricarica, DWL misura quanto benessere sparisce.**

### Monopolio naturale: si riconosce dal costo medio

Un monopolio è **naturale** quando il costo medio totale `ATC = TC/Q` è **decrescente** e resta **sempre sopra** il costo marginale — segno che un costo fisso alto si spalma su più unità. In quel caso un'unica impresa produce a costo minore di due che si dividono lo stesso mercato (il costo è **subadditivo**): dividerlo sarebbe uno spreco, non un guadagno di concorrenza.

**Nel mercato contendibile** (libertà di entrata e uscita senza costi affondati) il profitto va a zero anche restando un'unica impresa: si impone `P = ATC` invece di `MR = MC`. L'equazione che ne esce è di secondo grado e ha **due radici**: **si tiene sempre la maggiore**, l'unica in cui, per quantità più alte, il prezzo di domanda scende sotto l'`ATC` e nessun entrante trova conveniente restare. La radice minore non è un equilibrio stabile.

Se il regolatore impone il prezzo efficiente `P = MC` (**first best**), l'impresa va in **perdita esattamente pari al costo fisso**, perché con `ATC` decrescente si ha sempre `MC < ATC`. Da qui la scelta pratica fra sussidio (copre la perdita ma va finanziato con imposte distorsive) e regola **second best `P = ATC`** (azzera il profitto, rinuncia a un pezzo di efficienza).

<div class="pagebreak"></div>

## Tutorial 1 — equilibrio di monopolio e perdita secca

> **Traccia.** Un mercato è descritto dalla domanda inversa `P = 48 − 4q` e dal costo marginale `MC = 8q`.
> a) Calcola quantità e prezzo di monopolio.
> b) Calcola quantità e prezzo di concorrenza perfetta.
> c) Calcola la perdita secca di benessere.
> d) Calcola l'indice di Lerner.

### Passo 1 (a) — Ricavo marginale ed equilibrio di monopolio

```
      TR = (48 − 4q) · q = 48q − 4q²
      MR = 48 − 8q            (stessa intercetta, pendenza doppia)

      MR = MC:   48 − 8q = 8q
                 48 = 16q
                 q_M = 3
                 P_M = 48 − 4 · 3 = 36
```

**Che cosa scrivi sul foglio:** prima l'uguaglianza in lettere (`MR = MC`), poi la sostituzione. È il passaggio che vale il punteggio anche se il numero finale è sbagliato.

### Passo 2 (b) — Equilibrio concorrenziale

Qui l'impresa (o il settore, in concorrenza) impone `P = MC`, non `MR = MC`:

```
      P = MC:    48 − 4q = 8q
                 48 = 12q
                 q_C = 4
                 P_C = 48 − 4 · 4 = 32
```

**Controllo di buon senso immediato:** `q_M < q_C` e `P_M > P_C` — il monopolista produce meno e vende più caro. Se ti esce il contrario, hai invertito le condizioni di equilibrio.

### Passo 3 (c) — Perdita secca

```
      MC nel punto di monopolio:  MC(q_M) = 8 · 3 = 24

      DWL = ½ · (q_C − q_M) · [ P_M − MC(q_M) ]
          = ½ · (4 − 3) · (36 − 24)
          = ½ · 1 · 12
          = 6
```

**Verifica con l'integrale** (stesso risultato, utile come controprova quando i numeri non tornano):

```
      DWL = ∫ da 3 a 4 di (48 − 4q − 8q) dq
          = [ 48q − 6q² ] da 3 a 4
          = (192 − 96) − (144 − 54)
          = 96 − 90 = 6      ✓
```

### Passo 4 (d) — Indice di Lerner

```
      L = (P_M − MC(q_M)) / P_M = (36 − 24)/36 = 12/36 = 1/3 ≈ 0,333
```

**Il commento che vale punti:** un terzo del prezzo di monopolio è puro ricarico sopra il costo marginale — è la stessa misura di potere di mercato, indipendentemente dalla scala del mercato (per questo si divide per `P`, non si guarda la differenza in valore assoluto).

<div class="pagebreak"></div>

## Tutorial 2 — monopolio naturale e mercato contendibile

> **Traccia.** Domanda inversa `P = 36 − Q`; costo totale `TC = 8Q + 96`.
> a) Verifica che si tratta di un monopolio naturale.
> b) Calcola quantità, prezzo e profitto del monopolista protetto.
> c) Calcola l'equilibrio in un mercato contendibile.
> d) Che cosa succede imponendo `P = MC`?

### Passo 1 (a) — Verifica del monopolio naturale

```
      ATC = TC/Q = (8Q + 96)/Q = 8 + 96/Q
      MC = 8
```

`ATC` è **decrescente** per ogni `Q` (il costo fisso 96 si spalma su più unità prodotte) e resta **sempre sopra** `MC = 8`. Due imprese che si dividessero la stessa quantità duplicherebbero il costo fisso: il costo è **subadditivo**. **→ È un monopolio naturale.**

### Passo 2 (b) — Monopolista protetto

```
      TR = (36 − Q) Q = 36Q − Q²
      MR = 36 − 2Q

      MR = MC:   36 − 2Q = 8   →   Q_M = 14
      P_M = 36 − 14 = 22

      profitto = 22 · 14 − (8 · 14 + 96) = 308 − 208 = 100
```

### Passo 3 (c) — Mercato contendibile: profitto nullo, `P = ATC`

**Perché si impone `P = ATC` e non `P = MC`**: la contendibilità azzera il profitto (nuovi entranti erodono ogni margine), ma non impone l'efficienza — impone solo che i costi siano coperti, non che il prezzo sia il costo marginale.

```
      36 − Q = 8 + 96/Q

      moltiplicando per Q:
      36Q − Q² = 8Q + 96
      Q² − 28Q + 96 = 0

      Q = [ 28 ± √(784 − 384) ] / 2 = (28 ± 20) / 2

      Q = 4     oppure     Q = 24
```

- A `Q = 4`: `P = 32` e `ATC = 8 + 96/4 = 32`. Non è stabile: a una quantità intermedia (es. `Q = 14`) il prezzo di domanda (22) è ben sopra l'`ATC` (14,86), quindi un entrante può inserirsi con un prezzo più basso e restare comunque profittevole.
- A **`Q = 24`**: `P = 12` e `ATC = 8 + 96/24 = 12`. Oltre questa quantità il prezzo di domanda scende sotto l'`ATC`: nessun entrante ha convenienza a espandersi oltre. È l'equilibrio **stabile**.

**Regola da ricordare: fra le due radici, si tiene sempre la maggiore.**

Rispetto al monopolio protetto (`Q = 14`, `P = 22`, profitto 100), la sola minaccia di entrata porta la quantità a 24 e il prezzo a 12, azzerando il profitto — pur restando un'unica impresa a produrre.

### Passo 4 (d) — Regolamentazione `P = MC`

```
      P = MC = 8   →   36 − Q = 8   →   Q = 28

      TR = 8 · 28 = 224
      TC = 8 · 28 + 96 = 320

      profitto = 224 − 320 = −96
```

**La perdita (−96) è esattamente pari al costo fisso.** Il prezzo efficiente copre solo il costo marginale, mai il costo fisso, quando `ATC` è decrescente. È per questo che nella pratica regolatoria non si impone quasi mai il first best puro, ma un sussidio pari al costo fisso oppure la regola second best `P = ATC` del passo 3.

## Gli errori tipici del blocco 1

| Errore | Come si evita |
|---|---|
| Usare `P = MC` per il monopolista invece di `MR = MC` | `P = MC` vale solo per il termine di paragone concorrenziale, mai per l'equilibrio di monopolio |
| Calcolare l'altezza del triangolo di DWL come `P_M − P_C` | L'altezza è `P_M − MC(q_M)`: prezzo di monopolio meno costo marginale **nel punto di monopolio** |
| Nel mercato contendibile, tenere la radice minore | Si tiene sempre la radice **maggiore**: è l'unica in cui l'entrata non conviene più |
| Dimenticare il segno nella perdita da regolamentazione `P = MC` | Con `ATC` decrescente, `MC < ATC` sempre: il monopolista va **in perdita**, mai in pareggio |
| Confondere indice di Lerner e perdita secca | Lerner (`0`→`1`) misura il **ricarico**; DWL (in unità monetarie) misura il **benessere perso** |

<div class="pagebreak"></div>

## Tocca a te — esercizi A9, A10

### A9 — Perdita secca di monopolio e indice di Lerner

Un mercato è descritto dalla domanda inversa `P = 60 − 2q` e dal costo marginale `MC = 4q`.

a) Determina quantità e prezzo di monopolio.
b) Determina quantità e prezzo che si avrebbero in concorrenza perfetta.
c) Calcola la perdita secca di benessere.
d) Calcola l'indice di Lerner e commenta che cosa misura.

### A10 — Monopolio naturale e mercato contendibile

Domanda inversa `P = 30 − Q`; costo totale `TC = 6Q + 80`.

a) Verifica che si tratta di un monopolio naturale.
b) Calcola quantità, prezzo e profitto del monopolista protetto.
c) Calcola l'equilibrio in un mercato **contendibile** (profitti nulli) e spiega quale delle due radici va tenuta e perché.
d) Che cosa succederebbe se il regolatore imponesse la regola di *first best* `P = MC`? Quale problema sorge e come si risolve?

<div class="pagebreak"></div>

# Blocco 2 — Efficienza paretiana e funzioni di benessere sociale

## La teoria che serve

### Come si individuano gli stati Pareto-efficienti

Con `N` individui e `M` stati sociali dati in tabella, si confrontano gli stati **a coppie**, individuo per individuo:

- se uno stato ha **tutte** le utilità maggiori o uguali a un altro, e **almeno una** strettamente maggiore, **domina** quell'altro stato — lo stato dominato **non è** Pareto-efficiente;
- se il confronto è **misto** (in un'utilità sale, in un'altra scende), i due stati **non sono confrontabili** con Pareto: restano entrambi candidati efficienti.

**Uno stato è Pareto-efficiente se nessun altro stato lo domina.** Il limite classico, da scrivere quando capita: il criterio è **muto sull'equità** e dà un **ordinamento incompleto** — più stati possono risultare tutti efficienti e non dice quale scegliere.

### I tre criteri di funzione di benessere sociale (FBS)

| Criterio | Formula | Che cosa massimizza |
|---|---|---|
| **Utilitarista** | `W = Σ Uᵢ` | Il benessere **totale**, indifferente a come è distribuito |
| **Rawlsiana** | `W = min(Uᵢ)` | L'utilità dell'**individuo che sta peggio** (criterio maximin) |
| **Bergson-Samuelson** | es. `W = U1 · U2 · U3` | Un compromesso fra totale e uniformità — forma flessibile |

**Il punto d'esame:** i tre criteri esprimono **giudizi di valore diversi** sul peso relativo di efficienza ed equità. Non c'è un criterio "neutro": la FBS, a differenza di Pareto, richiede **confronti interpersonali di utilità**, ed è proprio questo che le permette di dare un ordinamento **completo** anche fra stati tutti Pareto-efficienti.

### Il criterio di compensazione di Kaldor

Confronta i **guadagni** dei vincitori con le **perdite** dei perdenti, entrambi valutati in una stessa unità (es. euro):

```
      il test è superato se   Σ guadagni  >  Σ perdite
```

**Superare il test non significa che il perdente venga risarcito davvero**: significa solo che i vincitori **potrebbero** risarcirlo integralmente e restare comunque in guadagno. La compensazione è **potenziale**, non effettiva — ed è proprio questo il punto debole del criterio: dichiara "un miglioramento" una situazione in cui qualcuno resta realmente peggio di prima.

<div class="pagebreak"></div>

## Tutorial — esercizio svolto passo passo

> **Traccia.** Tre individui (1, 2, 3) e tre stati sociali (I, II, III), con le utilità:
>
> | Stato | U1 | U2 | U3 |
> |---|---|---|---|
> | **I** | 5 | 5 | 5 |
> | **II** | 11 | 6 | 1 |
> | **III** | 2 | 4 | 9 |
>
> a) Quali stati sono Pareto-efficienti?
> b) Quale stato sceglie la FBS utilitarista, quale la rawlsiana, quale quella di Bergson-Samuelson (`W = U1 · U2 · U3`)?
> c) Nel passaggio da I a II l'individuo 3 subisce una perdita valutata 25 euro, mentre gli individui 1 e 2 guadagnano rispettivamente 15 e 40 euro. Il passaggio supera il criterio di Kaldor?

### Passo 1 (a) — Confronto a coppie

```
      I vs II:   5→11 sale, 5→6 sale, 5→1 scende      → misto
      I vs III:  5→2 scende, 5→4 scende, 5→9 sale     → misto
      II vs III: 11→2 scende, 6→4 scende, 1→9 sale    → misto
```

**Che cosa scrivi sul foglio:** una riga per ogni coppia, individuo per individuo, con la freccia che indica se sale o scende. In ogni confronto qualcuno guadagna e qualcuno perde: nessuno stato domina un altro.

**Risposta (a): tutti e tre gli stati sono Pareto-efficienti.**

### Passo 2 (b) — I tre criteri, in tabella

```
      utilitarista (Σ):        I = 15    II = 18    III = 15
      rawlsiana (min):         I = 5     II = 1     III = 2
      Bergson-Samuelson (×):   I = 125   II = 66    III = 72
```

| Stato | Utilitarista | Rawlsiana | Bergson-Samuelson |
|---|---|---|---|
| I | 15 | **5** | **125** |
| II | **18** | 1 | 66 |
| III | 15 | 2 | 72 |

- **Utilitarista** → sceglie **II** (somma massima, 18): è lo stato più diseguale dei tre, ma il criterio non se ne accorge.
- **Rawlsiana** → sceglie **I** (il peggiore ha utilità 5, contro 1 e 2 negli altri stati): è l'unico stato perfettamente egualitario.
- **Bergson-Samuelson** → sceglie anch'essa **I** (125, il valore più alto): qui il criterio "intermedio" **coincide** con quello rawlsiano, perché il prodotto premia fortemente l'uniformità quando nessuna utilità è vicina a zero.

**Il commento che vale punti:** i tre stati sono ugualmente efficienti secondo Pareto, ma **due criteri su tre** (rawlsiano e Bergson-Samuelson) convergono su I nonostante abbia il totale più basso — mostra che il peso dato all'equità, non solo quello dato al totale, decide l'esito. Non è un caso fisso: con altri numeri i tre criteri possono divergere tutti e tre, come nell'esercizio A11.

### Passo 3 (c) — Il test di Kaldor

```
      guadagni:  15 + 40 = 55
      perdita:   25

      55 > 25    →   il test è SUPERATO, con un margine di 30
```

**Il commento:** i vincitori (individui 1 e 2) potrebbero risarcire per intero il perdente (individuo 3, 25 euro) e restare comunque con un guadagno netto di 30. **Potrebbero**: nell'esercizio non c'è nessuna clausola che dica che lo facciano davvero. Se non lo fanno, l'individuo 3 resta effettivamente più povero, e il test di Kaldor lo classifica comunque come "miglioramento" — è il limite del criterio.

## Gli errori tipici del blocco 2

| Errore | Come si evita |
|---|---|
| Concludere che uno stato "domina" da un confronto misto | Domina solo se **tutte** le utilità sono ≥ e **almeno una** è >. Un solo segno diverso rende il confronto misto |
| Scegliere lo stato con la somma più alta per il criterio rawlsiano | Rawls guarda il **minimo**, non la somma: cerca chi sta peggio in ciascuno stato |
| Trattare il test di Kaldor come una compensazione avvenuta davvero | È **potenziale**: il test dice solo che i vincitori *potrebbero* risarcire, non che lo fanno |
| Sommare utilità e valutazioni monetarie nello stesso conto | Il test di Kaldor lavora sempre in un'unica unità (di solito euro): non si mescolano scale diverse |

<div class="pagebreak"></div>

## Tocca a te — esercizio A11

### A11 — Efficienza paretiana e funzioni di benessere sociale

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

<div class="pagebreak"></div>

# Blocco 3 — Obiettivi, strumenti e regola di Tinbergen

## La teoria che serve

### I tre elementi di un programma di politica economica

**Obiettivi** (variabili endogene: inflazione, disoccupazione, crescita…) · **strumenti** (variabili esogene manovrabili: spesa pubblica, imposte, cambio…) · **modello** (le relazioni che collegano gli strumenti agli obiettivi).

### Dalla forma strutturale alla decisione

```
      forma ridotta:         obiettivo = f(strumenti)  → EFFICACIA
      forma ridotta inversa: strumento = f(obiettivo)  → decisione
```

**L'efficacia di uno strumento su un obiettivo è la derivata dell'uno rispetto all'altro**: quanto si muove l'obiettivo per una unità in più dello strumento. Si legge direttamente dal coefficiente dello strumento nella forma ridotta.

### La regola aurea di Tinbergen

**Per raggiungere tutti gli obiettivi, servono almeno tanti strumenti indipendenti quanti sono gli obiettivi.**

| Strumenti vs obiettivi | Nome | Conseguenza |
|---|---|---|
| Strumenti > obiettivi | sotto-determinato | più combinazioni raggiungono lo stesso risultato |
| Strumenti = obiettivi | — | soluzione unica (se il sistema non è degenere) |
| Strumenti < obiettivi | sovradeterminato | non tutti gli obiettivi sono raggiungibili |

**Con due obiettivi e due strumenti**, il sistema si scrive in forma ridotta come due equazioni lineari e si mette a sistema imponendo i valori-obiettivo. **Il determinante dice se il sistema ha soluzione unica:**

```
            |  α   β  |
      det = |         |  =  αδ − βγ
            |  γ   δ  |
```

- `det ≠ 0` → i due strumenti sono **linearmente indipendenti** (agiscono sui due obiettivi in proporzioni diverse): esiste una e una sola combinazione che centra entrambi gli obiettivi.
- `det = 0` → i due strumenti hanno lo **stesso profilo di effetti** (uno è un multiplo dell'altro): **non sono davvero due strumenti indipendenti**, e in generale non esiste una soluzione che centri entrambi gli obiettivi contemporaneamente.

Se il governo ha un solo strumento per due obiettivi (caso sovradeterminato), le alternative sono: rinunciare a un obiettivo (trattarlo come **flessibile**), oppure adottare il **metodo delle priorità** — fissare l'obiettivo più importante e accettare per l'altro il valore che ne risulta.

<div class="pagebreak"></div>

## Tutorial 1 — un obiettivo, uno strumento: l'efficacia

> **Traccia.** Il modello è:
> ```
>       Y_off = θ N                    θ = 20
>       Y_dom = C + I + G
>       C = c Y_d                      c = 0,6
>       Y_d = (1 − t) Y
>       I = 1.500
> ```
> L'obiettivo è un'occupazione `N = 1.200`.
> a) Quale spesa pubblica `G` raggiunge l'obiettivo se `t = 0`?
> b) E se `t = 0,25`?
> c) Qual è l'efficacia dello strumento nei due casi?

### Passo 1 — La forma ridotta, in lettere prima che in numeri

```
      N = (1/θ) · [ 1/(1 − c(1−t)) ] · (I + G)
```

**dove:** `(1/θ)` traduce reddito in occupazione (ogni addetto produce `θ` unità) · la parentesi quadra è il moltiplicatore keynesiano · `(I + G)` è la domanda autonoma. **Rovesciandola** si ottiene lo strumento in funzione dell'obiettivo:

```
      G = θ · [ 1 − c(1−t) ] · N − I
```

### Passo 2 (a) — Caso `t = 0`

```
      moltiplicatore = 1/(1 − 0,6) = 2,5
      1 − c(1−t) = 1 − 0,6 = 0,4

      G = 20 · 0,4 · 1.200 − 1.500
        = 9.600 − 1.500
        = 8.100
```

**Verifica**, sempre utile: `Y = θN = 20 · 1.200 = 24.000`; dal lato della domanda, `Y = 2,5 · (I+G) = 2,5 · (1.500+8.100) = 2,5 · 9.600 = 24.000` ✓.

### Passo 3 (b) — Caso `t = 0,25`

```
      1 − c(1−t) = 1 − 0,6 · 0,75 = 1 − 0,45 = 0,55

      G = 20 · 0,55 · 1.200 − 1.500
        = 13.200 − 1.500
        = 11.700
```

**Il commento immediato:** per lo stesso obiettivo di occupazione serve più spesa pubblica (da 8.100 a 11.700), perché l'imposta drena reddito a ogni giro del moltiplicatore.

### Passo 4 (c) — Efficacia: la derivata, non il livello

```
      dN/dG = (1/θ) · [ 1/(1 − c(1−t)) ]

      t = 0:      dN/dG = (1/20) · (1/0,4)  = 0,125
      t = 0,25:   dN/dG = (1/20) · (1/0,55) ≈ 0,0909
```

**Attenzione a non confondere `G` (livello) con `dN/dG` (efficacia)**: sono due domande diverse, "quanto strumento serve" contro "quanto rende ogni euro di strumento". Il calo di efficacia (`0,125 → 0,0909`, circa **−27%**) è lo stesso meccanismo del teorema di Haavelmo: l'imposta proporzionale spegne parte della catena del moltiplicatore.

<div class="pagebreak"></div>

## Tutorial 2 — due obiettivi, due strumenti: la regola aurea

> **Traccia.** Un governo ha due obiettivi — il reddito `Y` e il saldo delle partite correnti `CC` — e due strumenti — la spesa pubblica `G` e il tasso di cambio `e`. La forma ridotta è:
> ```
>       Y  =  3 G + 2 e
>       CC = −0,5 G + 1 e
> ```
> Obiettivi: `Y* = 900`, `CC* = 0`.
> a) Calcola i livelli di `G` e `e` che raggiungono entrambi gli obiettivi.
> b) Verifica con il determinante che il sistema sia risolvibile.
> c) Con il solo strumento `G`, il governo può raggiungere entrambi gli obiettivi?
> d) Se la seconda equazione fosse `CC = 1,5 G + 1 e`, che cosa cambia?

### Passo 1 (a) — Mettere a sistema

```
      900 =  3 G + 2 e
        0 = −0,5 G + 1 e
```

Conviene isolare una variabile dall'equazione più semplice e sostituire:

```
      dalla seconda:   e = 0,5 G

      sostituendo:     900 = 3G + 2(0,5G) = 3G + G = 4G
                        G = 225
                        e = 0,5 · 225 = 112,5
```

```
      verifica:  Y  = 3 · 225 + 2 · 112,5 = 675 + 225 = 900     ✓
                 CC = −0,5 · 225 + 1 · 112,5 = −112,5 + 112,5 = 0   ✓
```

### Passo 2 (b) — Determinante

```
      det = (3 · 1) − (2 · (−0,5)) = 3 + 1 = 4    ≠ 0
```

**Che cosa dice, in economia:** i due strumenti sono linearmente indipendenti — `G` alza `Y` e **peggiora** `CC`, mentre `e` alza `Y` e **migliora** `CC`. Proprio perché i loro "profili" sono diversi, una loro combinazione può centrare qualunque coppia di obiettivi. Un determinante diverso da zero è la traduzione algebrica della **regola aurea di Tinbergen** rispettata.

### Passo 3 (c) — Con il solo strumento `G`

No. Con un solo strumento si può centrare **un solo** obiettivo:

```
      per Y* = 900:   3G = 900   →   G = 300
      a quel G:       CC = −0,5 · 300 = −150   → disavanzo, non CC* = 0
```

Il governo dovrebbe rinunciare a `CC* = 0` come obiettivo fisso (trattarlo come **flessibile**) oppure usare il **metodo delle priorità**: fissare `Y*` e accettare il valore di `CC` che ne risulta — è esattamente il caso **sovradeterminato** della regola di Tinbergen.

### Passo 4 (d) — La seconda equazione diventa dipendente

```
      CC = 1,5 G + 1 e

      det = (3 · 1) − (2 · 1,5) = 3 − 3 = 0
```

**Che cosa scopri:** `det = 0` perché la seconda riga è ora **proporzionale** alla prima (`CC` reagisce a `G` ed `e` nella stessa identica proporzione di `Y`, solo scalata): i due "strumenti" non sono più indipendenti nell'effetto che producono sui due obiettivi — è come averne uno solo. **Lezione della regola aurea di Tinbergen**: non basta contare gli strumenti sulla carta, contano solo se **linearmente indipendenti** nei loro effetti; due strumenti che si muovono sempre nella stessa proporzione valgono come uno solo, e un obiettivo resta fuori portata.

## Gli errori tipici del blocco 3

| Errore | Come si evita |
|---|---|
| Confondere il livello dello strumento (`G`) con la sua efficacia (`dN/dG`) | "Quanto serve" è una domanda sul livello; "quanto rende" è una domanda sulla derivata: sono risposte diverse |
| Dimenticare di verificare il risultato sostituendolo nelle equazioni originali | Una riga di verifica in più intercetta quasi tutti gli errori di segno nel sistema |
| Concludere che un solo strumento può sempre raggiungere due obiettivi "aggiustando bene" i numeri | La regola di Tinbergen è **strutturale**: con un solo strumento indipendente un secondo obiettivo fisso non è raggiungibile, qualunque sia il suo valore |
| Non riconoscere il caso `det = 0` come "strumenti non indipendenti" | Un determinante nullo non è un errore di calcolo: è il segnale che le due equazioni dicono la stessa cosa in proporzioni diverse |

<div class="pagebreak"></div>

## Tocca a te — esercizi A12, A13

### A12 — Obiettivo occupazione e strumento spesa pubblica

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

### A13 — Due obiettivi, due strumenti (regola aurea di Tinbergen)

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

<div class="pagebreak"></div>

# Soluzioni

*Guardale solo dopo aver provato. Se il risultato non torna, cerca prima l'errore da solo: quasi sempre è un segno o un termine dimenticato — e trovarlo da soli vale più della soluzione.*

## Soluzione A9

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

**dove:** l'altezza del triangolo è la distanza fra **prezzo di monopolio e costo marginale nel punto di monopolio**, non fra i due prezzi.

**(d) Indice di Lerner**

```
      L = (P_M − MC(q_M))/P_M = (45 − 30)/45 = 1/3 ≈ 0,333
```

Un terzo del prezzo è puro ricarico di potere di mercato. **Lerner misura il ricarico, DWL misura il benessere distrutto**: non sono la stessa cosa, anche se nascono dallo stesso equilibrio.

## Soluzione A10

**(a) Verifica del monopolio naturale**

```
      ATC = TC/Q = (6Q + 80)/Q = 6 + 80/Q
      MC = 6
```

`ATC` è **decrescente** per ogni `Q` e resta **sempre sopra** `MC`. Due imprese che si dividessero la stessa quantità duplicherebbero il costo fisso: il costo è **subadditivo** → è un monopolio naturale.

**(b) Monopolista protetto**

```
      TR = (30 − Q) Q = 30Q − Q²
      MR = 30 − 2Q

      MR = MC:   30 − 2Q = 6   →   Q_M = 12
      P_M = 30 − 12 = 18
      profitto = 18 · 12 − (6 · 12 + 80) = 216 − 152 = 64
```

**(c) Mercato contendibile**

Si impone profitto nullo, `P = ATC`:

```
      30 − Q = 6 + 80/Q
      30Q − Q² = 6Q + 80
      Q² − 24Q + 80 = 0

      Q = [ 24 ± √(576 − 320) ] / 2 = (24 ± 16)/2

      Q = 4   oppure   Q = 20
```

- A `Q = 4`: `P = 26`, `ATC = 26`. Non stabile: a quantità intermedie il prezzo di domanda supera l'`ATC`, quindi un entrante può inserirsi.
- A **`Q = 20`**: `P = 10`, `ATC = 10`. Oltre questa quantità il prezzo di domanda scende sotto l'`ATC`: nessun entrante conviene. È l'equilibrio **stabile**.

**Regola da ricordare: si tiene sempre la radice maggiore.**

**(d) Regola di first best `P = MC`**

```
      P = 6   →   Q = 30 − 6 = 24
      ricavi = 6 · 24 = 144
      costi  = 6 · 24 + 80 = 224
      perdita = −80          (esattamente il costo fisso)
```

Il prezzo pari al costo marginale è efficiente ma manda l'impresa in perdita perché `MC < ATC` sempre, con costi medi decrescenti. Le soluzioni: un **sussidio** pari al costo fisso, oppure la regola **second best `P = ATC`**.

## Soluzione A11

**(a) Stati Pareto-efficienti**

```
      I vs II:   6→10 sale, 6→7 sale, 6→2 scende    → misto
      I vs III:  6→3 scende, 6→8 sale, 6→9 sale     → misto
      II vs III: 10→3 scende, 7→8 sale, 2→9 sale    → misto
```

In ogni confronto qualcuno guadagna e qualcuno perde: nessuno stato domina un altro. **→ Tutti e tre gli stati sono Pareto-efficienti.**

**(b) Le tre funzioni di benessere sociale**

| Stato | Utilitarista `ΣU_i` | Rawlsiana `min(U_i)` | Bergson-Samuelson `U1×U2×U3` |
|---|---|---|---|
| I | 18 | **6** | **216** |
| II | 19 | 2 | 140 |
| III | **20** | 3 | **216** |

- **Utilitarista** → sceglie **III** (somma massima, 20).
- **Rawlsiana** → sceglie **I** (l'individuo che sta peggio ha 6, contro 2 e 3 negli altri stati): l'unico perfettamente egualitario.
- **Bergson-Samuelson** → **pareggio fra I e III** (216 entrambi): la funzione moltiplicativa premia sia il totale sia l'uniformità, e qui i due effetti si compensano esattamente.

**(c) Criterio di compensazione (Kaldor)**

```
      guadagni:  20 + 60 = 80
      perdite:   30
      80 > 30    →  il test è SUPERATO
```

I vincitori **potrebbero** risarcire integralmente il perdente (30 euro) e restare comunque in guadagno (80 − 30 = 50). **Potrebbero**: la compensazione è solo **potenziale**, non deve avvenire davvero.

**(d) Che cosa dimostra il confronto** — i tre stati sono ugualmente efficienti secondo Pareto, ma i criteri li ordinano in modo **diverso e inconciliabile**. La scelta dipende interamente dal **giudizio di valore** incorporato nella funzione di benessere. Non esiste una risposta neutra: il compito della teoria normativa è **dichiarare esplicitamente** quale criterio si sta adottando.

## Soluzione A12

**(a) Spesa pubblica con `t = 0`**

```
      forma ridotta:  N = (1/θ) · [ 1/(1 − c(1−t)) ] · (I + G)
      forma inversa:  G = θ (1 − c(1−t)) · N − I

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

Per lo stesso obiettivo occupazionale serve una spesa pubblica quasi doppia.

**(c) Efficacia dello strumento**

```
      t = 0:     dN/dG = (1/25) · 4   = 0,16
      t = 0,2:   dN/dG = (1/25) · 2,5 = 0,10
```

**(d) Calo dell'efficacia**

```
      (0,16 − 0,10)/0,16 = 0,375     →  −37,5%
```

L'imposta proporzionale riduce l'efficacia dello strumento fiscale di oltre un terzo, perché drena reddito a ogni giro del moltiplicatore — lo stesso meccanismo del **teorema di Haavelmo**: il moltiplicatore del bilancio in pareggio vale 1 con imposta in somma fissa e crolla a 0,5 con aliquota proporzionale (esercizio A2).

## Soluzione A13

**(a) Livelli degli strumenti**

```
      500 =  2 G + 1 e
        0 = −0,4 G + 0,8 e

      dalla seconda:   0,8 e = 0,4 G   →   e = 0,5 G

      sostituendo:     500 = 2 G + 0,5 G = 2,5 G
                       G = 200
                       e = 100
```

```
      verifica:  Y  = 2 · 200 + 100 = 500          ✓
                 CC = −0,4 · 200 + 0,8 · 100 = 0    ✓
```

**(b) Determinante**

```
      det = (2 · 0,8) − (1 · (−0,4)) = 1,6 + 0,4 = 2 ≠ 0
```

Diverso da zero: il sistema ha **una e una sola soluzione**. I due strumenti sono linearmente indipendenti: la spesa pubblica alza il reddito e peggiora il saldo estero, il cambio alza il reddito e lo **migliora**. Combinandoli si può centrare qualsiasi coppia di obiettivi.

**(c) Con il solo strumento `G`**

No. Fissando `G = 250` si otterrebbe `Y = 500` ma `CC = −100`, un disavanzo. Il governo dovrebbe trattare `CC` come obiettivo **flessibile**, oppure adottare il **metodo delle priorità**.

**(d) Con `CC = 1 G + 0,5 e`**

```
      det = (2 · 0,5) − (1 · 1) = 1 − 1 = 0
```

Determinante nullo: i due strumenti non sono più indipendenti nei loro effetti (la seconda equazione è proporzionale alla prima). Non esiste, in generale, una combinazione che centri entrambi gli obiettivi contemporaneamente — è il caso in cui la **regola aurea di Tinbergen non è rispettata**, anche se sulla carta gli strumenti sono ancora due.
