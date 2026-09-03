# Giorno 1 — giovedì 3 settembre

**Politica fiscale e inflazione.** Esercizi A1 → A8 del quaderno, con la spiegazione e il
tutorial per svolgerli. Questo foglio è autosufficiente: tracce e soluzioni sono qui dentro,
non serve aprire la dispensa.

[TOC]

<div class="pagebreak"></div>


## Come si usa questo foglio

Tre blocchi, uno per famiglia di esercizi. Ognuno ha sempre lo stesso ritmo:

1. **La teoria che serve** — solo quello che entra nei conti, mezza pagina.
2. **Il tutorial** — un esercizio svolto davanti a te, lentamente, con accanto a ogni passaggio il *perché* si fa così e **che cosa scrivi sul foglio**.
3. **Tocca a te** — le tracce del quaderno. Chiudi il tutorial e provaci.

Le **soluzioni** sono in fondo, tutte insieme. Guardale solo dopo aver provato: se guardi prima, non stai imparando a fare l'esercizio, stai leggendo un esercizio fatto da altri.

| Blocco | Argomento | Esercizi | Tempo indicativo |
|---|---|---|---|
| 1 | Reddito di equilibrio e moltiplicatori | A1, A2, A3 | 90 minuti |
| 2 | Debito pubblico e fiscal drag | A4, A5 | 45 minuti |
| 3 | Salari, costo pieno, curva di Phillips | A6, A7, A8 | 75 minuti |

**Se il tempo non basta**, taglia in questo ordine: A3 (economia aperta, è una variante di A2), poi A5 (fiscal drag, è aritmetica pura). A1, A2, A6 e A7 non si tagliano: sono i modelli, non le varianti.

**Segna con una crocetta ogni esercizio che sbagli.** Lunedì rifarai solo quelli.

<div class="pagebreak"></div>

# Blocco 1 — Reddito di equilibrio e moltiplicatori

## La teoria che serve

### Il modello in cinque righe

```
      Y = C + I + G          equilibrio: produzione = domanda
      C = C_0 + c (Y − T)    consumo
      I = I_0                investimenti (dati)
      G = G_0                spesa pubblica (data)
      T = T_0                imposte (date)
```

**dove:**
- `Y` = **reddito** (uguale alla produzione: tutto ciò che si produce è reddito di qualcuno)
- `C_0` = **consumo autonomo**: quanto si consuma anche a reddito zero, intaccando i risparmi
- `c` = **propensione marginale al consumo**: di ogni euro in più di reddito disponibile, quanto se ne consuma. Sta fra 0 e 1
- `(Y − T)` = **reddito disponibile**: quello che resta dopo le imposte
- `I_0`, `G_0`, `T_0` = variabili **esogene**, cioè decise fuori dal modello

**La riga da capire davvero è la prima.** `Y = C + I + G` non è una definizione: è una **condizione di equilibrio**. Dice che l'economia si ferma nel punto in cui quello che si produce è esattamente quello che qualcuno vuole comprare. Se si produce di più, restano scorte invendute e la produzione si riduce; se si produce di meno, le scorte si svuotano e la produzione aumenta.

**E la seconda spiega perché nasce il moltiplicatore.** Il consumo dipende dal reddito, ma il reddito dipende dal consumo: è un **circolo**. Una spesa in più diventa reddito di qualcuno, che ne consuma una quota `c`, che diventa reddito di qualcun altro, che ne consuma `c`… La somma di questa catena infinita è il moltiplicatore.

### Perché il reddito **disponibile** e non il reddito

Perché le famiglie decidono quanto consumare guardando quello che gli resta in tasca, non quello che hanno guadagnato lordo. È questo dettaglio che dà allo Stato una leva: cambiando `T` cambia `Y − T`, quindi il consumo, quindi il reddito.

### I quattro moltiplicatori (e la logica unica che li tiene insieme)

| Situazione | Moltiplicatore |
|---|---|
| Economia chiusa, imposta in somma fissa | `1/(1 − c)` |
| Economia chiusa, imposta proporzionale `T = tY` | `1/(1 − c(1−t))` |
| Economia aperta, imposta proporzionale, `M = mY` | `1/(1 − c(1−t) + m)` |
| Moltiplicatore delle **imposte** (invece che della spesa) | `−c/(1 − c)` |

**Non impararli a memoria: imparane la logica.** Al denominatore c'è sempre `1` meno *quanto di ogni euro in più torna in domanda interna*. Ogni cosa che **disperde** quel flusso lo fa scendere:

- il **risparmio** disperde `(1 − c)` → per questo c'è `1 − c`;
- l'**imposta** disperde la quota `t` prima ancora che il consumatore decida → per questo `c` diventa `c(1−t)`;
- l'**importazione** disperde `m` verso l'estero → per questo `+ m` si somma al denominatore.

Più dispersioni, denominatore più grande, moltiplicatore più piccolo. Se ti ricordi questa frase, i quattro moltiplicatori li **riscrivi**, non li ricordi.

**Il moltiplicatore delle imposte è diverso da quello della spesa, e più piccolo in valore assoluto.** Motivo: un euro di spesa pubblica entra nella domanda **per intero**; un euro di tasse in meno entra nella domanda solo per la parte che viene **consumata**, cioè `c` — il resto viene risparmiato. Da qui il `c` al numeratore, e il segno meno (più tasse, meno reddito).

<div class="pagebreak"></div>

## Tutorial — esercizio svolto passo passo

> **Traccia.** Un'economia chiusa è descritta da `C = 200 + 0,75(Y − T)`, `I = 150`, `G = 250`, `T = 200`.
> a) Calcola il reddito di equilibrio.
> b) Il governo aumenta la spesa pubblica di 25. Di quanto cresce il reddito?
> c) E se, invece, aumentasse di 25 le imposte?
> d) E se facesse le due cose insieme?

### Passo 0 — Prima di calcolare: scrivi i dati e l'incognita

Sembra tempo perso. Non lo è: metà degli errori nasce dal leggere il testo e partire a memoria. Sul foglio scrivi:

```
      DATI                        INCOGNITA
      C_0 = 200                   Y di equilibrio
      c   = 0,75
      I   = 150
      G   = 250
      T   = 200
```

Colpo d'occhio utile subito: `c = 0,75` significa che di ogni euro in più se ne consumano 75 centesimi. Quindi il moltiplicatore sarà `1/(1 − 0,75) = 4`. **Puoi già dire che ogni manovra verrà moltiplicata per 4.**

### Passo 1 — Scrivi la condizione di equilibrio, in lettere

Non con i numeri. Prima in lettere, sempre:

```
      Y = C + I + G
```

Perché in lettere? Perché è il passaggio che il correttore cerca. Se sbagli un conto ma hai scritto l'equilibrio giusto, hai preso quasi tutto il punteggio; se azzecchi il numero senza aver scritto da dove viene, no.

### Passo 2 — Sostituisci le funzioni

```
      Y = 200 + 0,75 (Y − 200) + 150 + 250
```

### Passo 3 — Sciogli le parentesi

Qui si sbaglia più spesso di quanto sembri: il `0,75` moltiplica **tutta** la parentesi, quindi anche il `−200`.

```
      Y = 200 + 0,75 Y − 150 + 150 + 250
      Y = 0,75 Y + 450
```

**Che cosa è successo:** i pezzi senza `Y` si sono sommati in un unico numero (`200 − 150 + 150 + 250 = 450`). Quel numero ha un nome: è la **domanda autonoma**, cioè la spesa che c'è comunque, indipendentemente da quanto reddito produce l'economia.

### Passo 4 — Porta tutta la `Y` a sinistra

```
      Y − 0,75 Y = 450
      Y (1 − 0,75) = 450
      0,25 Y = 450
```

**Il pezzo `(1 − 0,75)` è il denominatore del moltiplicatore.** Non è una coincidenza: il moltiplicatore *nasce* qui, da questo raccoglimento. Se capisci questo passaggio non devi più ricordare nessuna formula — la riottieni ogni volta.

### Passo 5 — Isola `Y`

```
      Y = 450 / 0,25 = 1.800
```

**Risposta (a): il reddito di equilibrio è 1.800.**

### Passo 6 (b) — La manovra: usa il moltiplicatore, non rifare tutto

Questo è il punto in cui si guadagna tempo all'esame. Non riscrivere l'equazione da capo: usa

```
      ΔY = moltiplicatore · ΔG = 4 · 25 = +100

      nuovo Y = 1.800 + 100 = 1.900
```

**Perché funziona:** il moltiplicatore è già il rapporto fra variazione del reddito e variazione della domanda autonoma. Una volta calcolato al passo 4, vale per **qualsiasi** manovra su `G`, `I` o `C_0`.

**La spiegazione economica**, che vale scriverla in una riga sotto il conto: lo Stato spende 25 in più; quei 25 diventano reddito di qualcuno, che ne consuma il 75% (18,75); quei 18,75 diventano reddito di un altro, che ne consuma il 75% (14,06)… La somma di tutti i giri è 100, cioè quattro volte la spinta iniziale.

### Passo 7 (c) — Le imposte hanno un moltiplicatore diverso

```
      ΔY = −c/(1 − c) · ΔT = −(0,75/0,25) · 25 = −3 · 25 = −75
```

**Attenzione: `−3`, non `−4`.** Ed è il punto teorico più importante della giornata.

**Perché il moltiplicatore delle imposte è più piccolo:** i 25 euro di spesa pubblica entrano nella domanda **tutti e 25**. I 25 euro di imposte in più, invece, non tolgono 25 euro di domanda: tolgono 25 euro di reddito **disponibile**, di cui il contribuente avrebbe consumato solo il 75% (18,75) e risparmiato il resto (6,25). Alla domanda mancano quindi 18,75, non 25. Da lì in poi la catena è la stessa, ma è partita più corta.

```
      controprova:  −18,75 · 4 = −75      ✓
```

### Passo 8 (d) — Le due cose insieme: il teorema di Haavelmo

```
      effetto della spesa:     +4 · 25 = +100
      effetto delle imposte:   −3 · 25 =  −75
      ------------------------------------------
      effetto netto:                     +25
```

```
      verifica diretta, rifacendo il conto con G = 275 e T = 225:
      Y = 200 + 0,75 (Y − 225) + 150 + 275
      Y = 0,75 Y + 456,25
      0,25 Y = 456,25   →   Y = 1.825        ✓  (1.800 + 25)
```

**È il teorema del bilancio in pareggio (Haavelmo).** Una manovra di spesa **interamente finanziata** da un pari aumento di imposte fa crescere il reddito **esattamente dell'importo della manovra**: il moltiplicatore del bilancio in pareggio vale **1**.

**Perché non si annullano** — è la domanda d'esame, e la risposta è già tutta nel passo 7: `G` entra nella domanda per intero, `T` la riduce solo per la quota consumata `c`. La differenza è `1 − c`, e moltiplicata per il moltiplicatore `1/(1 − c)` fa esattamente 1:

```
      1/(1−c) − c/(1−c) = (1−c)/(1−c) = 1
```

**Il messaggio di politica economica:** anche uno Stato che si obbliga al pareggio di bilancio può fare politica espansiva — solo, in misura pari alla manovra e non moltiplicata.

<div class="pagebreak"></div>

## Le due varianti che devi saper riconoscere

Sono lo stesso esercizio con una dispersione in più. Cambia **solo il denominatore**.

### Variante 1 — Imposta proporzionale

Se al posto di `T = 200` il testo scrive `T = 0,2 Y`, l'imposta non è più un numero: **cresce insieme al reddito**. Con gli stessi altri dati:

```
      Y = 200 + 0,75 (Y − 0,2 Y) + 150 + 250
      Y = 200 + 0,75 · 0,8 Y + 400
      Y = 0,6 Y + 600
      0,4 Y = 600
      Y = 1.500
```

```
      moltiplicatore = 1/(1 − c(1−t)) = 1/(1 − 0,75 · 0,8) = 1/0,4 = 2,5
```

Da 4 a 2,5, e il reddito da 1.800 a 1.500. **Perché:** a ogni giro del moltiplicatore lo Stato preleva il 20%, quindi alle famiglie arriva 0,8 e in consumo torna solo `0,75 · 0,8 = 0,6`. La catena si spegne prima.

**Il nome da usare all'esame: stabilizzatore automatico.** L'imposta proporzionale attutisce le espansioni *e* le recessioni, senza che nessuno debba decidere nulla — funziona da sola, subito, mentre una manovra discrezionale richiede mesi.

### Variante 2 — Economia aperta

Aggiungi esportazioni `X` (date: dipendono dal reddito **estero**) e importazioni `M = mY` (dipendono dal **nostro** reddito). Con `X = 100` e `m = 0,1`, tenendo `t = 0,2`:

```
      Y = 200 + 0,6 Y + 150 + 250 + 100 − 0,1 Y
      Y (1 − 0,6 + 0,1) = 700
      0,5 Y = 700
      Y = 1.400
```

```
      moltiplicatore = 1/(1 − c(1−t) + m) = 1/0,5 = 2
      saldo commerciale = X − M = 100 − 0,1 · 1.400 = 100 − 140 = −40
```

**Due conclusioni da scrivere sempre:** (1) il moltiplicatore si riduce ancora, perché una parte della domanda "esce" dal paese; (2) una manovra espansiva **peggiora il saldo con l'estero**, perché le importazioni salgono col reddito mentre le esportazioni restano ferme. È il **vincolo estero** alla politica fiscale.

## Gli errori tipici del blocco 1

| Errore | Come si evita |
|---|---|
| Usare `1/(1−c)` con imposta proporzionale | Chiediti sempre: `T` è un numero o contiene `Y`? Se contiene `Y`, il moltiplicatore è `1/(1 − c(1−t))` |
| Dimenticare di moltiplicare `c` anche per il termine negativo dentro la parentesi | Sciogli la parentesi in una riga a sé, senza fare due passaggi in testa |
| Usare il moltiplicatore della spesa per una manovra sulle imposte | Il moltiplicatore delle imposte è `−c/(1−c)`: **negativo e più piccolo** |
| Rispondere con il livello quando chiedono la variazione (o viceversa) | "Di quanto cambia" → `ΔY`. "Quanto vale" → `Y` |
| Non commentare il risultato | Una riga: che cosa dice il numero. Vale punti quanto il conto |

<div class="pagebreak"></div>

## Tocca a te — esercizi A1, A2, A3

### A1 — Reddito di equilibrio e manovre di finanza pubblica

> **Traccia della professoressa** (proposta nelle slide sul bilancio pubblico e non svolta a lezione).

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

### A2 — Lo stesso modello con imposta proporzionale

> **Traccia della professoressa**, dalla stessa sezione.

Stessa economia di A1, ma ora l'imposta è `T = 75 + 0,25 Y`.

a) Calcola il moltiplicatore della spesa pubblica e il reddito di equilibrio.
b) Confronta moltiplicatore e reddito con quelli di A1: perché sono più bassi?
c) Aumenta `G` di 50: di quanto cresce il reddito e di quanto cresce il **gettito**? Il bilancio migliora o peggiora?
d) Aumenta contemporaneamente `G` di 50 e la parte fissa dell'imposta di 50: quanto vale ora il moltiplicatore del bilancio in pareggio? Il teorema di Haavelmo vale ancora?

### A3 — Il modello reddito-spesa in economia aperta

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

<div class="pagebreak"></div>

# Blocco 2 — Debito pubblico e fiscal drag

## La teoria che serve

### Perché il debito si guarda in rapporto al PIL

Un debito di mille miliardi non dice niente da solo: dice qualcosa solo confrontato con la capacità del paese di produrre reddito e quindi gettito. Per questo si guarda il **rapporto debito/PIL**, `B/(pY)`.

Ed è una **frazione**. Quindi la domanda "il rapporto sale o scende?" non è una domanda sul debito: è una domanda su **quale dei due, numeratore o denominatore, corre più veloce**.

```
      numeratore   → il debito cresce al tasso di interesse i
                     (gli interessi si aggiungono al debito)

      denominatore → il PIL nominale cresce al tasso Ẏ + ṗ
                     (crescita reale più inflazione)
```

**Da qui, senza formule, la condizione di sostenibilità:**

```
      il rapporto è stabile quando   i = Ẏ + ṗ

      cioè, in termini reali:        i − ṗ = Ẏ
```

**dove:** `i` = tasso di interesse nominale sul debito · `ṗ` = inflazione (il puntino sopra significa "tasso di variazione di") · `Ẏ` = crescita reale del PIL · `i − ṗ` = **tasso di interesse reale**.

- Se `i − ṗ < Ẏ` → il debito cresce più lentamente del PIL, il rapporto **scende da solo**.
- Se `i − ṗ > Ẏ` → il rapporto **sale anche in pareggio di bilancio**. È l'effetto **palla di neve** (*snowball*): il debito si gonfia da sé, per i soli interessi.

### La formula operativa (quella che usi negli esercizi)

```
      Δ(B/Y) ≈ (i − ṗ − Ẏ) · (B/Y) − avanzo primario/Y
```

**dove** l'**avanzo primario** è il saldo di bilancio **al netto degli interessi**: entrate meno spese escluse quelle per interessi. È la parte che il governo controlla davvero — gli interessi no, li decide il mercato.

**L'errore da non fare mai: confrontare il tasso nominale con la crescita reale.** I due termini devono essere omogenei. O entrambi reali (`i − ṗ` contro `Ẏ`), o entrambi nominali (`i` contro `Ẏ + ṗ`). Mischiarli fa sbagliare di un'intera inflazione.

## Tutorial — esercizio svolto passo passo

> **Traccia.** Un paese ha `i = 4%`, `ṗ = 1,5%`, `Ẏ = 2%` e un rapporto debito/PIL del **100%**.
> a) Quale avanzo primario serve per stabilizzare il rapporto?
> b) Se il paese ha un avanzo primario dell'1,5% del PIL, il rapporto sale o scende, e di quanto?

### Passo 1 — Tasso di interesse reale

```
      i − ṗ = 4% − 1,5% = 2,5%
```

### Passo 2 — Confronto con la crescita reale

```
      2,5%  >  2%      →  differenziale = +0,5 punti
```

Il costo reale del debito supera la crescita: la palla di neve è in moto. Senza avanzo primario il rapporto **salirebbe**.

### Passo 3 — Quanto pesa il differenziale

Il differenziale va moltiplicato per **quanto debito c'è**: mezzo punto in più su un debito enorme costa molto più che sullo stesso mezzo punto su un debito piccolo.

```
      0,5% · 1,00 = 0,5% del PIL
```

**Risposta (a): serve un avanzo primario dello 0,5% del PIL.**

### Passo 4 (b) — Con l'avanzo primario dato

```
      Δ(B/Y) = 0,5% − 1,5% = −1 punto percentuale

      il rapporto scende dal 100% al 99% in un anno
```

### Il commento che vale punti

Il **fattore dimensione** è il punto da scrivere sempre. Con `B/Y = 100%` mezzo punto di differenziale costa mezzo punto di PIL di avanzo primario; con `B/Y = 130%` — il caso italiano — lo stesso differenziale ne costa 0,65. **Più il debito è alto, più ogni punto di interesse pesa**, e più il paese è vulnerabile a un rialzo dei tassi che non ha deciso lui. È esattamente questa asimmetria a rendere il debito alto un problema politico e non solo contabile.

<div class="pagebreak"></div>

## Il fiscal drag in un tutorial breve

> **Traccia.** Scaglioni: **20%** fino a 10.000 euro, **30%** sulla parte eccedente. Un contribuente guadagna 12.000 euro. L'anno dopo l'inflazione è del 5% e il suo reddito nominale sale a 12.600 euro: **il suo reddito reale è identico**. Che cosa succede alle imposte?

### Passo 1 — Imposta e aliquota media, anno 1

Un'imposta a scaglioni si calcola **a fette**, non applicando un'aliquota unica al totale.

```
      primi 10.000  ·  0,20  =  2.000
      restanti 2.000 ·  0,30  =    600
      T = 2.600

      aliquota media = 2.600/12.000 = 21,67%
```

### Passo 2 — Anno 2, stesso reddito reale

```
      primi 10.000  ·  0,20  =  2.000
      restanti 2.600 ·  0,30  =    780
      T = 2.780

      aliquota media = 2.780/12.600 = 22,06%
```

L'aliquota media è **salita** senza che nessuno abbia votato nulla.

### Passo 3 — Il reddito netto in termini reali

Il confronto va fatto in termini reali, altrimenti il +600 nominale inganna: si divide per `1 + inflazione`.

```
      anno 1:  12.000 − 2.600 = 9.400 reali
      anno 2:  12.600 − 2.780 = 9.820 nominali
               9.820 / 1,05   = 9.352 reali

      perdita reale ≈ 48 euro
```

**Il meccanismo:** gli **scaglioni sono in euro nominali**, ma il reddito nominale cresce con l'inflazione. Il contribuente scivola verso l'alto negli scaglioni senza essere diventato più ricco. **Il rimedio:** indicizzare gli scaglioni (e le detrazioni) all'inflazione. **La lezione politica:** è un aumento occulto della pressione fiscale — nasconde una decisione politica dentro un fenomeno monetario.

## Tocca a te — esercizi A4, A5

### A4 — Sostenibilità del debito pubblico

Un paese ha un tasso di interesse nominale sul debito `i = 5%`, un'inflazione `ṗ = 2%`, una crescita reale `Ẏ = 1%` e un rapporto debito/PIL pari al **130%**.

a) Quale avanzo primario (in percentuale del PIL) serve per **stabilizzare** il rapporto debito/PIL?
b) E se la crescita reale salisse al 3%, ferme le altre variabili?
c) E se invece il tasso di interesse salisse al 7%, con crescita all'1%?
d) Commenta: quale delle due leve — crescita o tasso di interesse — è nelle mani del governo, e quale no?

### A5 — Fiscal drag

Un sistema fiscale ha due scaglioni: **25%** fino a 15.000 euro, **35%** sulla parte eccedente. Un contribuente guadagna 20.000 euro. L'anno seguente l'inflazione è del 10% e il suo reddito nominale sale a 22.000 euro, quindi il suo reddito **reale è invariato**.

a) Calcola imposta pagata e aliquota media nei due anni.
b) Il reddito netto **reale** del contribuente è aumentato, diminuito o rimasto uguale?
c) Come si chiama il fenomeno e come si corregge?

<div class="pagebreak"></div>

# Blocco 3 — Salari, costo pieno e curva di Phillips

## La teoria che serve

### Le tre equazioni, e come si incastrano

Questo è il blocco in cui ci si perde, perché le equazioni sono tre e sembrano scollegate. In realtà sono una **catena**: ognuna passa il proprio risultato alla successiva.

```
      1. CURVA DEI SALARI       ẇ = γ(u)
         quanto crescono i salari, data la disoccupazione

                    ↓  ẇ

      2. COSTO PIENO            π = ẇ − θ̇ + (1+g)˙
         come i salari diventano prezzi

                    ↓  π

      3. PHILLIPS AUMENTATA     π_t = γ(u_t) + πᵉ_t
         che cosa succede quando la gente se lo aspetta
```

**dove:**
- `ẇ` = tasso di variazione dei **salari monetari** (il puntino = "tasso di variazione di")
- `u` = tasso di disoccupazione
- `π` = **inflazione**
- `θ̇` = tasso di crescita della **produttività**
- `(1+g)˙` = variazione del **mark-up**, cioè del ricarico che le imprese applicano sui costi
- `πᵉ_t` = inflazione **attesa** per il periodo `t` (la "e" in alto = *expected*)

### Che cosa dice ciascuna, in una riga

**1. Curva dei salari** — meno disoccupazione, più forza contrattuale, salari che corrono. Il tasso di disoccupazione che rende i salari **stabili** (`ẇ = 0`) è il **tasso naturale `u_N`**.

**2. Costo pieno** — l'impresa fissa il prezzo come costo del lavoro per unità di prodotto più un ricarico: `p = (1 + g) · w/θ`. In tassi di variazione diventa la seconda equazione. Da leggere così: **i salari spingono i prezzi in su, la produttività li tira in giù**. Se i salari crescono del 6% e la produttività del 2%, l'inflazione è 4%, non 6: due punti di aumento salariale sono "pagati" dal fatto che ogni addetto produce di più.

**3. Phillips aumentata** — se i lavoratori si **aspettano** inflazione, chiedono quell'aumento in più solo per non perdere potere d'acquisto. L'inflazione attesa si somma quindi a quella "di mercato". Con **aspettative adattive** l'attesa di oggi è l'inflazione di ieri: `πᵉ_t = π_(t−1)`.

### Il trabocchetto dei decimali

Nella curva dei salari `u` va **in decimali**: 8% si scrive `0,08`. Nel commento si torna ai punti percentuali. Confondere i due è l'errore più frequente e più costoso di tutto il programma, perché il conto "funziona" lo stesso e sbaglia di un fattore 100.

**Regola pratica:** dentro il blocco recintato, decimali. Fuori, percentuali. E un controllo di buon senso: se ti esce un tasso di disoccupazione del 400%, hai sbagliato unità.

<div class="pagebreak"></div>

## Tutorial — esercizio svolto passo passo

> **Traccia.** La curva dei salari di un paese è `ẇ = 0,36 − 3 u`, con `u` in decimali.
> a) Qual è il tasso di disoccupazione naturale?
> b) Con disoccupazione al 9% e produttività che cresce dell'1%, quanto vale l'inflazione?
> c) Se il governo tiene la disoccupazione al 9% periodo dopo periodo, con aspettative adattive e `θ̇ = 0`, che cosa succede all'inflazione?
> d) Quale disoccupazione servirebbe per togliere 6 punti di inflazione?

### Passo 1 (a) — Il tasso naturale annulla `ẇ`

Definizione: `u_N` è la disoccupazione a cui i salari monetari sono **stabili**. Quindi si pone `ẇ = 0` e si risolve.

```
      0,36 − 3 u_N = 0
      3 u_N = 0,36
      u_N = 0,12          →  12%
```

**Che cosa hai appena calcolato:** non un tasso "buono" o "desiderabile", ma il tasso che il mercato del lavoro produce quando nessuno spinge. Sotto quel livello i salari accelerano, sopra rallentano.

### Passo 2 (b) — Dalla disoccupazione ai salari

Sostituisci `u = 0,09` nella curva. Nota: `0,09`, non `9`.

```
      ẇ = 0,36 − 3 · 0,09
         = 0,36 − 0,27
         = 0,09              →  9%
```

### Passo 3 (b) — Dai salari ai prezzi: il costo pieno

```
      π = ẇ − θ̇ + (1+g)˙
        = 9% − 1% + 0
        = 8%
```

**Il passaggio da non saltare mai è il `− θ̇`.** Se il testo dice che la produttività cresce, **quella crescita va sottratta**: senza, l'inflazione esce sistematicamente troppo alta. Il mark-up costante fa sparire il terzo termine, ma vale la pena scriverlo lo stesso e annotare "mark-up costante": mostra al correttore che sai che c'è.

**Il commento:** con `u = 9%` sotto il naturale del 12%, il mercato del lavoro è surriscaldato e i salari corrono al 9%; ma la produttività ne assorbe un punto, quindi ai prezzi ne arrivano 8.

### Passo 4 (c) — Le aspettative adattive, periodo per periodo

Qui non c'è una formula da applicare una volta: c'è una **tabella da costruire**, riga per riga, portando avanti il risultato precedente.

Con `θ̇ = 0` il costo pieno diventa `π = ẇ`, e la curva dà sempre lo stesso contributo:

```
      γ(9%) = 0,36 − 3 · 0,09 = 0,09   →  9%  in ogni periodo
```

Poi si itera, ricordando che `πᵉ_t = π_(t−1)`:

| t | `πᵉ_t` (= π del periodo prima) | `u_t` | `π_t = γ(u_t) + πᵉ_t` |
|---|---|---|---|
| 0 | 0% | 9% | 0 + 9 = **9%** |
| 1 | 9% | 9% | 9 + 9 = **18%** |
| 2 | 18% | 9% | 18 + 9 = **27%** |

**Come si scrive sul foglio:** una tabella di quattro colonne, e la freccia che porta `π_t` nella casella `πᵉ` della riga sotto. Fatto così non si sbaglia; fatto a mente, sì.

**Che cosa dimostra — è la risposta d'esame:** tenere la disoccupazione **sotto** il tasso naturale non produce un'inflazione più alta ma **stabile**. Produce un'inflazione che **accelera**, 9 punti in più a ogni periodo, senza fermarsi. Il guadagno in occupazione non si paga una volta: si paga per sempre.

### Passo 5 (d) — La disinflazione costa disoccupazione

Per **togliere** inflazione serve che la curva dia un contributo **negativo**, cioè che i salari scendano:

```
      serve γ(u) = −6% = −0,06

      −0,06 = 0,36 − 3 u
      3 u = 0,42
      u = 0,14            →  14%
```

Per togliere 6 punti di inflazione bisogna portare la disoccupazione dal 12% naturale al **14%**, cioè 2 punti sopra. È il **tasso di sacrificio**: quanti punti di disoccupazione (o di PIL) costa un punto di inflazione in meno.

**La conclusione teorica da citare — Friedman e Phelps:** nel **lungo periodo** la curva di Phillips è **verticale** sul tasso naturale. Non esiste uno scambio permanente fra inflazione e disoccupazione: la politica monetaria può comprare occupazione solo finché **inganna** le aspettative, e ogni volta il prezzo è un livello di inflazione più alto. È l'argomento più forte a favore delle **regole** contro la discrezionalità.

### Il tutorial breve sul cost-plus in livelli

L'esercizio A8 chiede la formula in **livelli**, non in variazioni. Cambia poco:

```
      p = (1 + g) · w/θ
```

Con mark-up `g = 20%`, salario `w = 24.000` euro l'anno e produttività `θ = 15` unità per addetto:

```
      w/θ = 24.000/15 = 1.600      costo del lavoro per unità di prodotto
      p = 1,20 · 1.600 = 1.920
```

E se poi i salari crescono del 5%, la produttività dell'1,5% e il mark-up passa dal 20% al 23%:

```
      variazione del mark-up = (1,23 − 1,20)/1,20 = 0,025   →  2,5%

      π = 5% − 1,5% + 2,5% = 6%
```

**Attenzione:** il mark-up passa da 20% a 23%, ma la variazione che entra nella formula **non** è 3 punti: è la variazione di `(1+g)`, cioè da 1,20 a 1,23, che vale **2,5%**. È il punto in cui si sbaglia di più in questo esercizio.

## Gli errori tipici del blocco 3

| Errore | Come si evita |
|---|---|
| Mettere `u` in punti percentuali nella curva dei salari | Dentro il conto sempre decimali: 9% → `0,09` |
| Dimenticare `− θ̇` | Se il testo nomina la produttività, quel termine c'è |
| Calcolare la variazione del mark-up come differenza di punti | Si calcola su `(1+g)`: da 1,20 a 1,23 è `+2,5%`, non `+3%` |
| Nelle aspettative adattive, riusare sempre la stessa `πᵉ` | Costruisci la tabella: la `π` di una riga è la `πᵉ` della riga dopo |
| Rispondere "l'inflazione è più alta" alla domanda (c) | La risposta è "**accelera**", ed è tutta un'altra cosa |

<div class="pagebreak"></div>

## Tocca a te — esercizi A6, A7, A8

### A6 — Curva dei salari e costo pieno

Il mercato del lavoro di un paese è descritto dalla curva dei salari:

```
      ẇ = 0,42 − 4 · u
```

con `u` espressa **in decimali** (10% si scrive 0,10).

a) Determina il tasso di disoccupazione naturale `u_N`.
b) Se la disoccupazione effettiva è del 7% e la produttività cresce del 2% (`θ̇ = 2%`) con mark-up costante, calcola `ẇ` e l'inflazione `π`.
c) La banca centrale vuole portare l'inflazione all'8%, sempre con `θ̇ = 2%`: quale tasso di disoccupazione è compatibile con quell'obiettivo?
d) Commenta il "prezzo" della disinflazione in termini di posti di lavoro.

### A7 — Phillips con aspettative adattive

Stessa curva dei salari di A6, ma ora con `θ̇ = 0` e mark-up costante, quindi `π_t = γ(u_t) + πᵉ_t`, con aspettative adattive `πᵉ_t = π_(t−1)` (cioè `λ = 1`) e `πᵉ` inizialmente nulla.

a) Il governo mantiene la disoccupazione stabilmente al **7%**, sotto il tasso naturale. Costruisci la tabella dell'inflazione per `t = 0, 1, 2`.
b) Che cosa dimostra questa dinamica sul rapporto di lungo periodo fra inflazione e disoccupazione?
c) Per **ridurre** l'inflazione di 10 punti in un periodo, quale disoccupazione servirebbe?
d) Qual è la conclusione di Friedman e Phelps che questo esercizio illustra?

### A8 — Prezzi di costo pieno (cost-plus)

Un'impresa fissa il prezzo con un mark-up `g = 25%` sul costo del lavoro per unità di prodotto. Il salario annuo per addetto è `w = 30.000` euro e la produttività è `θ = 20` unità di prodotto per addetto.

a) Calcola il prezzo `p`.
b) L'anno seguente i salari crescono del 6% e la produttività del 2%, con mark-up invariato: quanto vale l'inflazione?
c) Se invece, oltre a quelle variazioni, l'impresa alza il mark-up dal 25% al 30%, quanto vale l'inflazione?
d) Quali dei tre termini della formula del costo pieno può controllare un sindacato, e quali una politica dei redditi?

<div class="pagebreak"></div>

# Soluzioni

*Guardale solo dopo aver provato. Se il risultato non torna, cerca prima l'errore da solo: quasi sempre è un'unità di misura o un segno — e trovarlo da soli vale più della soluzione.*

## Soluzione A1

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

## Soluzione A2

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

## Soluzione A3

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

## Soluzione A4

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

## Soluzione A5

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

## Soluzione A6

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

## Soluzione A7

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

**(d) Conclusione di Friedman e Phelps** — nel **lungo periodo** la curva di Phillips è **verticale** in corrispondenza del tasso naturale `u_N`. Non esiste un trade-off permanente fra inflazione e disoccupazione: la politica monetaria può comprare occupazione solo finché **inganna** le aspettative, e ogni volta il prezzo è un livello di inflazione più alto. Da qui l'argomento a favore delle **regole** contro la discrezionalità (**schema 11**).

## Soluzione A8

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
| `(1+g)˙` (mark-up) | Le imprese, tanto più liberamente quanto meno il mercato è concorrenziale → **politiche per la concorrenza** (**schema 03**) |

Il punto d'esame: l'inflazione da costi **non si combatte solo con la politica monetaria**. Ognuno dei tre termini ha una politica economica diversa che lo governa.
