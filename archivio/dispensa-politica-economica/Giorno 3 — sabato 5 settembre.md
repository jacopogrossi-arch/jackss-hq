# Giorno 3 — sabato 5 settembre

**Mercato del lavoro, economia aperta e moneta.** Esercizi B1 → B8 del quaderno, con la spiegazione e il
tutorial per svolgerli. Questo foglio è autosufficiente: tracce e soluzioni sono qui dentro,
non serve aprire la dispensa.

[TOC]

<div class="pagebreak"></div>


## Come si usa questo foglio

Stessa logica dei giorni 1 e 2: tre blocchi, ognuno con teoria minima, uno o più tutorial svolti passo passo e poi le tracce vere da fare da solo. Le **soluzioni** sono in fondo — guardale solo dopo aver provato.

| Blocco | Argomento | Esercizi | Tempo indicativo |
|---|---|---|---|
| 1 | Mercato del lavoro e legge di Okun | B1, B2 | 60 minuti |
| 2 | Economia aperta: cambio reale, Marshall-Lerner, IS-LM-BP, costi comparati | B3, B4, B5, B6 | 120 minuti |
| 3 | Moneta: moltiplicatore monetario e domanda di moneta | B7, B8 | 60 minuti |

**Se il tempo non basta**, taglia in questo ordine: B6 (costi comparati — è teoria del commercio, non il modello Mundell-Fleming che dà il nome al capitolo), poi B4(c)-(d) (le quattro ipotesi e la curva a J sono da leggere, non da ricalcolare). B1, B2, B3, B5 e B7-B8 non si tagliano: sono i modelli core del giorno, non le varianti.

**Segna con una crocetta ogni esercizio che sbagli.** Andranno rifatti nel giorno 5.

<div class="pagebreak"></div>

# Blocco 1 — Mercato del lavoro e legge di Okun

## La teoria che serve

### I tre tassi, e il denominatore che li distingue

```
      a = FL / Pop₁₅₊        (tasso di attività)
      n = N / Pop₁₅₊         (tasso di occupazione)
      u = U / FL             (tasso di disoccupazione)
```

**dove:** `FL` = forza lavoro = `N + U` · `N` = occupati · `U` = persone in cerca di occupazione · `Pop₁₅₊` = popolazione in età lavorativa (**non** la popolazione totale, se il testo le distingue).

**Attenzione al denominatore**: attività e occupazione hanno al denominatore la **popolazione**, la disoccupazione ha al denominatore la **forza lavoro**. È l'errore più frequente su questo argomento. Verifica sempre con l'identità:

```
      n = a · (1 − u)
```

**Chi esce dalla forza lavoro non è più disoccupato.** Un lavoratore che smette di cercare (uno **scoraggiato**) esce da `FL`: il tasso di disoccupazione può scendere senza che sia stato creato un solo posto di lavoro. Il tasso di occupazione `n`, che ha la popolazione al denominatore, non si lascia ingannare da questo spostamento.

### La legge di Okun

```
      Δu  ≈  − (crescita − crescita potenziale) / 2,5
```

**dove:** servono circa **2,5 punti** di crescita del PIL **oltre** quella potenziale per abbassare la disoccupazione di **1 punto**. Il rapporto è più che proporzionale: una parte della crescita serve solo a **stare fermi** (assorbire il nuovo ingresso di popolazione in età lavorativa e i guadagni di produttività), e solo l'eccedenza comincia a ridurre la disoccupazione.

<div class="pagebreak"></div>

## Tutorial 1 — I tre tassi del mercato del lavoro

> **Traccia.** In un paese: popolazione totale 320, popolazione in età lavorativa 180, occupati 120, persone in cerca di occupazione 15 (migliaia di persone).
> a) Calcola tasso di disoccupazione, tasso di attività e tasso di occupazione.
> b) Verifica la coerenza con `n = a · (1 − u)`.
> c) L'anno seguente 7 dei 15 disoccupati si scoraggiano e smettono di cercare lavoro; gli occupati restano 120. Ricalcola i tre tassi.
> d) Commenta: il paese sta meglio o peggio? Quale dei tre tassi racconta la verità?

### Passo 1 (a) — Forza lavoro e i tre tassi

```
      Passo 1 — Forza lavoro
      FL = N + U = 120 + 15 = 135

      Passo 2 — Tasso di disoccupazione   (denominatore: FORZA LAVORO)
      u = U/FL = 15/135 = 0,1111        →  11,1%

      Passo 3 — Tasso di attività         (denominatore: POPOLAZIONE 15+)
      a = FL/Pop = 135/180 = 0,75        →  75%

      Passo 4 — Tasso di occupazione      (denominatore: POPOLAZIONE 15+)
      n = N/Pop = 120/180 = 0,6667       →  66,7%
```

**Che cosa scrivi sul foglio:** la popolazione **totale** (320) è un dato-trappola — non entra in nessuna delle tre formule. Si usa sempre la popolazione **in età lavorativa** (180).

### Passo 2 (b) — Verifica

```
      n = a · (1 − u) = 0,75 · 0,8889 = 0,6667        ✓
```

### Passo 3 (c) — Sette disoccupati si scoraggiano

Chi smette di cercare lavoro **esce dalla forza lavoro**: non è più disoccupato, diventa inattivo. Restano `15 − 7 = 8` disoccupati.

```
      FL = 120 + 8 = 128

      u = 8/128   = 0,0625    →  6,25%   (era 11,1%)
      a = 128/180 = 0,7111    →  71,1%   (era 75%)
      n = 120/180 = 0,6667    →  66,7%   (invariato)
```

**Controllo di buon senso:** il tasso di occupazione `n` non può cambiare in questo passaggio, perché al numeratore c'è `N` (invariato, 120) e al denominatore la popolazione (invariata, 180). Se ti esce un `n` diverso, hai sbagliato uno dei due dati.

### Passo 4 (d) — Commento

Il tasso di disoccupazione crolla da 11,1% a 6,25% — quasi si dimezza — **senza che sia stato creato un solo posto di lavoro**. È l'effetto dei lavoratori scoraggiati: si spostano da "disoccupati" a "inattivi", e il tasso che ha la forza lavoro al denominatore migliora artificialmente. Il tasso che dice la verità è il **tasso di occupazione** (`n = 66,7%`, immobile): ha la popolazione al denominatore, e non può essere "migliorato" spostando persone da una categoria all'altra.

## Tutorial 2 — Legge di Okun

> **Traccia.** Il PIL di un paese cresce del **5%**, mentre il PIL potenziale cresce del **2%**. La disoccupazione di partenza è del **10%**.
> a) Di quanto varia il tasso di disoccupazione? A quanto arriva?
> b) Quale tasso di crescita servirebbe per portare la disoccupazione dal 10% al 7% (cioè −3 punti) in un anno?
> c) Perché il rapporto è "più che proporzionale"?

### Passo 1 (a) — Variazione della disoccupazione

```
      crescita oltre il potenziale = 5% − 2% = 3 punti

      Δu ≈ − 3/2,5 = −1,2 punti

      nuovo tasso: 10% − 1,2% = 8,8%
```

**Che cosa scrivi sul foglio:** prima isola la crescita "in eccesso" (quella oltre il potenziale), solo dopo la dividi per 2,5. Sommare direttamente crescita e disoccupazione è l'errore più comune di questa scheda.

### Passo 2 (b) — Crescita necessaria per −3 punti

```
      servono 3 · 2,5 = 7,5 punti di crescita oltre il potenziale

      crescita richiesta = 2% + 7,5% = 9,5%
```

**Controllo di buon senso:** 9,5% di crescita annua è un tasso da economia emergente in forte recupero, non da economia matura. Non è realistico in un solo anno — ed è proprio il punto (c).

### Passo 3 (c) — Perché il rapporto è più che proporzionale

Nel frattempo crescono anche la **popolazione in età lavorativa** (quindi la forza lavoro: servono nuovi posti solo per non peggiorare) e la **produttività** (quindi ogni occupato produce di più, e a parità di output ne servono meno). Una parte della crescita serve soltanto a **stare fermi**: solo l'eccedenza oltre quella soglia comincia ad assorbire disoccupazione. È il motivo per cui una crescita positiva ma modesta può convivere con una disoccupazione **crescente**, e per cui la disoccupazione scende lentamente anche a ripresa in corso.

## Gli errori tipici del blocco 1

| Errore | Come si evita |
|---|---|
| Mettere la popolazione **totale** al denominatore di un tasso | Usare sempre la popolazione **in età lavorativa**, mai quella totale, se il testo le distingue |
| Confondere il denominatore di `u` con quello di `a` e `n` | `u` ha **forza lavoro** al denominatore; `a` e `n` hanno la **popolazione**: sono due denominatori diversi |
| Trattare uno scoraggiato come un disoccupato in più | Lo scoraggiato **esce dalla forza lavoro**: va tolto sia dai disoccudati sia dal totale di `FL`, non solo aggiunto da nessuna parte |
| Sommare crescita e disoccupazione senza passare dall'eccedenza sul potenziale | In Okun conta solo la crescita **oltre** il potenziale, divisa per 2,5 — non la crescita assoluta |

<div class="pagebreak"></div>

## Tocca a te — esercizi B1, B2

### B1 — I tre tassi del mercato del lavoro

In un paese: popolazione totale 200, popolazione in età lavorativa 150, occupati 90, persone in cerca di occupazione 10 (migliaia di persone).

a) Calcola tasso di disoccupazione, tasso di attività e tasso di occupazione.
b) Verifica la coerenza con la relazione `n = a · (1 − u)`.
c) L'anno seguente 5 disoccupati **si scoraggiano** e smettono di cercare lavoro; gli occupati restano 90. Ricalcola i tre tassi.
d) Commenta: il paese sta meglio o peggio? Quale dei tre tassi racconta la verità?

### B2 — Legge di Okun

Il PIL di un paese cresce del **3,5%**, mentre il PIL potenziale cresce del **2%**. La disoccupazione di partenza è del 9%. Applica la legge di Okun nella versione della dispensa (servono circa 2,5 punti di crescita oltre il potenziale per ridurre la disoccupazione di 1 punto).

a) Di quanto varia il tasso di disoccupazione? A quanto arriva?
b) Quale tasso di crescita servirebbe per portare la disoccupazione dal 9% al 7% in un anno? È realistico?
c) Perché il rapporto è "più che proporzionale"? (È il punto che la domanda d'esame chiede di spiegare, non il numero.)

<div class="pagebreak"></div>

# Blocco 2 — Economia aperta: cambio reale, Marshall-Lerner, IS-LM-BP, costi comparati

## La teoria che serve

### Cambio reale e competitività

```
        p · e
      ─────────  =  e_r
          p_w
```

**dove:** `e_r` = tasso di cambio reale (competitività) · `p` = prezzi interni · `p_w` = prezzi esteri · `e` = tasso di cambio nominale. Con questa convenzione un **aumento** di `e` è un **apprezzamento** (serve più valuta estera per comprare un'unità di valuta nazionale). Versione dinamica, in tassi di variazione:

```
      ė_r = ṗ + ė − ṗ_w
```

**Se `ė_r` sale** (apprezzamento reale) → **perdita** di competitività. **Se scende** (deprezzamento reale) → **guadagno**.

### La condizione di Marshall-Lerner

```
      | ε_x | + | ε_m |  >  1
```

**dove:** `ε_x` = elasticità delle esportazioni al cambio · `ε_m` = elasticità delle importazioni al cambio. Se la somma supera 1, una svalutazione **migliora** il saldo corrente; altrimenti lo **peggiora**. Nel brevissimo periodo vale comunque la **curva a J**: il saldo peggiora prima di migliorare, perché i prezzi si aggiustano subito e le quantità lentamente.

### Il modello IS-LM-BP (Mundell-Fleming)

```
      IS:  equilibrio dei beni
      LM:  L_d(Y,i) = M_s/p
      BP:  CC(Y) + MK(i) = 0
```

**dove:** la IS dà `Y` in funzione di `i` · la LM è l'equilibrio del mercato monetario · la BP è l'equilibrio con l'estero.

**I passi**: (1) metti IS e LM a sistema, trova `i` e `Y`; (2) sostituisci in `CC` e `MK` per vedere se la bilancia dei pagamenti è in pareggio, avanzo o disavanzo; (3) per una manovra, sposta la curva giusta e ripeti; (4) confronta l'aumento di reddito ottenuto con quello che ci sarebbe stato a tasso invariato — la differenza è lo **spiazzamento finanziario**.

### Costi comparati

Anche se un paese ha il vantaggio **assoluto** in tutti i beni (meno ore in ognuno), conviene comunque specializzarsi: si guarda il **costo-opportunità** — quante unità dell'altro bene "costa" produrne una — e ciascun paese si specializza dove quel costo è **minore**.

<div class="pagebreak"></div>

## Tutorial 1 — Cambio reale e condizione di Marshall-Lerner

> **Traccia.** Il tasso di cambio nominale di un paese si **deprezza del 3%**, l'inflazione interna è del **4%** e quella estera del **2%**.
> a) Calcola la variazione del tasso di cambio reale.
> b) Quanto contribuisce l'inflazione relativa (interna meno estera)?
> c) Il risultato indica un **aumento** o una **perdita** di competitività?
>
> Lo stesso paese valuta poi una **svalutazione** aggiuntiva del cambio nominale del 20%. Le elasticità sono: esportazioni 0,55, importazioni 0,35.
> d) La condizione di Marshall-Lerner è soddisfatta? Il saldo corrente migliora o peggiora?

### Passo 1 (a) — Variazione del cambio reale

Un deprezzamento nominale del 3% significa `ė = −3%` (con la convenzione della dispensa, un **aumento** di `e` è un apprezzamento, quindi una diminuzione è un deprezzamento):

```
      ė_r = ṗ + ė − ṗ_w = 4% + (−3%) − 2% = −1%
```

### Passo 2 (b) — Contributo dell'inflazione relativa

```
      inflazione relativa = ṗ − ṗ_w = 4% − 2% = +2%
```

L'inflazione interna è **più alta** di quella estera: da sola peggiorerebbe la competitività di 2 punti.

### Passo 3 (c) — Aumento o perdita di competitività

`ė_r` è **negativo**: deprezzamento reale, quindi **guadagno di competitività**, ma di **solo 1 punto**. Il deprezzamento nominale (3 punti) più che compensa il maggior differenziale di inflazione interna (2 punti), lasciando un guadagno netto piccolo.

**Controllo di buon senso:** i due canali della competitività — prezzi e cambio — vanno in direzioni opposte (l'inflazione interna più alta la peggiora, il deprezzamento nominale la migliora): il segno finale dipende da quale dei due prevale, mai da uno solo dei due termini.

### Passo 4 (d) — Marshall-Lerner sulla svalutazione aggiuntiva

```
      condizione di Marshall-Lerner:  η_x + η_m > 1

      0,55 + 0,35 = 0,90 < 1     →  NON soddisfatta
```

Il saldo corrente **peggiora**: la svalutazione rende le importazioni più care in valuta nazionale, ma le quantità reagiscono troppo poco per compensare l'effetto prezzo negativo.

<div class="pagebreak"></div>

## Tutorial 2 — IS-LM-BP completo

> **Traccia.** Un'economia aperta è descritta da:
> ```
>       IS:  Y = 2.500 − 5.000 i
>       LM:  M_s/p = 0,25 Y − 1.250 i        con M_s/p = 500
>       BP:  CC = 205 − 0,1 Y
>            MK = 3.000 i − 130
> ```
> **dove:** `CC` = saldo delle partite correnti · `MK` = saldo dei movimenti di capitale · `BP = CC + MK`.
>
> a) Calcola il tasso di interesse e il reddito di equilibrio interno.
> b) Verifica se la bilancia dei pagamenti è in pareggio.
> c) Il governo attua una manovra fiscale espansiva che sposta la IS a `Y = 2.750 − 5.000 i`. Calcola il nuovo equilibrio.
> d) Di quanto è cresciuto il reddito rispetto allo spostamento della IS? Quanto vale lo spiazzamento finanziario?
> e) Che cosa succede ora alla bilancia dei pagamenti, e come si chiude il sistema in cambi flessibili e in cambi fissi?

### Passo 1 (a) — Equilibrio interno

Prima si riscrive la LM in forma esplicita:

```
      500 = 0,25 Y − 1.250 i
      0,25 Y = 500 + 1.250 i
      Y = 2.000 + 5.000 i
```

Poi IS = LM:

```
      2.500 − 5.000 i = 2.000 + 5.000 i
      500 = 10.000 i
      i = 0,05                →  5%
      Y = 2.000 + 5.000 · 0,05 = 2.250
```

**Controllo di buon senso:** verifica sostituendo `i = 0,05` anche nella IS: `2.500 − 5.000 · 0,05 = 2.250` — stesso risultato, il sistema è coerente.

### Passo 2 (b) — Bilancia dei pagamenti

```
      CC = 205 − 0,1 · 2.250 = 205 − 225 = −20
      MK = 3.000 · 0,05 − 130 = 150 − 130 = +20

      BP = CC + MK = −20 + 20 = 0     →  pareggio esterno
```

Un disavanzo corrente di 20 è finanziato esattamente da un afflusso di capitali di 20.

### Passo 3 (c) — Manovra fiscale espansiva

```
      2.750 − 5.000 i = 2.000 + 5.000 i
      750 = 10.000 i
      i = 0,075               →  7,5%
      Y = 2.000 + 5.000 · 0,075 = 2.375
```

### Passo 4 (d) — Spiazzamento finanziario

```
      spostamento della IS (a tasso invariato):  2.750 − 2.500 = +250
      aumento effettivo del reddito:             2.375 − 2.250 = +125
      spiazzamento:                              250 − 125 = 125
```

**Metà della manovra è stata spiazzata.** Il meccanismo: più reddito → più domanda di moneta per motivo transattivo → con offerta di moneta **ferma** a 500, il tasso deve salire (dal 5% al 7,5%) per riequilibrare il mercato monetario → il tasso più alto **scoraggia gli investimenti privati**, che si riducono e mangiano metà dell'espansione.

### Passo 5 (e) — Bilancia dei pagamenti dopo la manovra

```
      CC = 205 − 0,1 · 2.375 = 205 − 237,5 = −32,5
      MK = 3.000 · 0,075 − 130 = 225 − 130 = +95

      BP = −32,5 + 95 = +62,5               →  AVANZO
```

`CC` **peggiora** (più importazioni, perché `Y` è cresciuto) e `MK` **migliora** (più capitali in entrata, attratti dal tasso più alto): l'afflusso di capitali più che compensa il peggioramento del saldo corrente.

- **Cambi flessibili** — l'avanzo genera domanda di valuta nazionale, che si **apprezza**. L'apprezzamento peggiora la competitività, riduce `CC` e riporta BP a zero — ma spiazza anche le esportazioni, aggiungendo un secondo spiazzamento a quello finanziario.
- **Cambi fissi** — la banca centrale deve difendere la parità: compra valuta estera cedendo moneta nazionale, quindi le riserve ufficiali e la **base monetaria aumentano**. La LM si sposta a destra, il tasso torna a scendere e il reddito cresce ancora: la manovra fiscale viene **rafforzata**.

<div class="pagebreak"></div>

## Tutorial 3 — Costi comparati

> **Traccia.** Le ore di lavoro necessarie a produrre un'unità di ciascun bene sono:
>
> | | Riso | Lana |
> |---|---|---|
> | **Paese Alfa** | 5 | 4 |
> | **Paese Beta** | 15 | 6 |
>
> a) Quale paese ha il vantaggio **assoluto**? In quali beni?
> b) Calcola i costi comparati (quante unità di lana costa un'unità di riso in ciascun paese, e viceversa).
> c) In quale bene si specializza ciascun paese?
> d) Entro quale intervallo deve stare la ragione di scambio perché lo scambio convenga a entrambi?

### Passo 1 (a) — Vantaggio assoluto

Il paese Alfa impiega **meno ore in entrambi** i beni (5 contro 15 nel riso, 4 contro 6 nella lana): ha il vantaggio assoluto in tutto. Secondo la sola teoria dei vantaggi **assoluti** non ci sarebbe motivo di commerciare — ed è qui che entra il ragionamento di Ricardo sui costi comparati.

### Passo 2 (b) — Costi comparati

Si guarda quanto costa un bene **in termini dell'altro**, dentro ciascun paese:

```
      Paese Alfa:  1 riso = 5/4  = 1,25 unità di lana
      Paese Beta:  1 riso = 15/6 = 2,5  unità di lana
```

Letto al contrario:

```
      Paese Alfa:  1 lana = 4/5 = 0,8 unità di riso
      Paese Beta:  1 lana = 6/15 = 0,4 unità di riso
```

### Passo 3 (c) — Specializzazione

- Il **paese Alfa** produce riso sacrificando solo 1,25 lana (contro le 2,5 di Beta) → **vantaggio comparato nel riso**.
- Il **paese Beta** produce lana sacrificando solo 0,4 riso (contro 0,8 di Alfa) → **vantaggio comparato nella lana**.

Ciascuno si specializza dove il **costo-opportunità** è minore, anche se Alfa è più efficiente in assoluto in entrambi i beni.

### Passo 4 (d) — Ragione di scambio

```
      1,25 lana  <  prezzo internazionale di 1 riso  <  2,5 lana
```

Se un riso si scambia, per esempio, con **2 unità di lana**: Alfa ottiene 2 lana per un riso che internamente gliene costava 1,25 (guadagna 0,75); Beta ottiene un riso per 2 lana quando internamente gliene costava 2,5 (guadagna 0,5). **Entrambi guadagnano.** Fuori da quell'intervallo, per uno dei due conviene tornare a produrre tutto in casa.

## Gli errori tipici del blocco 2

| Errore | Come si evita |
|---|---|
| Sbagliare il verso del cambio | Con `e_r = p·e/p_w`, un **aumento** di `e` è un **apprezzamento**: rileggi sempre il segno di `ė` prima di sommarlo |
| Confondere "svalutazione migliora sempre il saldo" | Vale solo se **Marshall-Lerner è soddisfatta** (somma delle elasticità > 1): va verificata, non assunta |
| Dimenticare l'offerta di moneta **reale** (`M_s/p`) nella LM | La LM va sempre riscritta in forma esplicita prima di metterla a sistema con la IS |
| Confondere lo spostamento della IS con l'aumento effettivo di `Y` | Sono due numeri diversi: la differenza **è** lo spiazzamento finanziario |
| Nei costi comparati, confrontare i costi assoluti invece del costo-opportunità | Il vantaggio comparato si legge dal **rapporto** fra i due beni dentro lo stesso paese, non dalle ore in assoluto |

<div class="pagebreak"></div>

## Tocca a te — esercizi B3, B4, B5, B6

### B3 — Variazione del cambio reale

> **Traccia della professoressa** (esercizio proposto in una slide su bilancia dei pagamenti e competitività).

Il tasso di cambio nominale si **apprezza del 2%**, l'inflazione interna è dell'**1%** e quella estera del **2%**.

a) Calcola la variazione del tasso di cambio reale.
b) L'inflazione relativa (interna meno estera) di quanto contribuisce?
c) La variazione calcolata indica un **aumento** o una **perdita** di competitività? Perché?

*Attenzione alla convenzione della dispensa: `e_r = p·e/p_w`, quindi un aumento di `e` è un apprezzamento.*

### B4 — Condizione di Marshall-Lerner

Un paese svaluta la propria moneta del 10%.

a) Se l'elasticità della domanda di esportazioni è 0,6 e quella delle importazioni 0,3, il saldo corrente migliora o peggiora?
b) E se le elasticità fossero 0,9 e 0,5?
c) Quali sono le quattro ipotesi sotto cui vale la condizione?
d) Che cosa dice la curva a J sul comportamento del saldo **nei mesi immediatamente successivi** alla svalutazione, e perché?

### B5 — IS-LM-BP completo

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

### B6 — Costi comparati

Le ore di lavoro necessarie a produrre un'unità di ciascun bene sono:

| | Vino | Stoffa |
|---|---|---|
| **Paese A** | 4 | 2 |
| **Paese B** | 12 | 3 |

a) Quale paese ha il vantaggio **assoluto**? In quali beni?
b) Calcola i costi comparati (quante unità di stoffa costa un'unità di vino in ciascun paese).
c) In quale bene si specializza ciascun paese?
d) Entro quale intervallo deve stare la ragione di scambio perché lo scambio convenga a entrambi?

<div class="pagebreak"></div>

# Blocco 3 — Moneta: moltiplicatore monetario e domanda di moneta

## La teoria che serve

### Il moltiplicatore monetario

```
            1 + h
      M = ─────────  ·  H
            h + j
```

**dove:** `M` = offerta di moneta · `H` = base monetaria (creata dalla banca centrale) · `h` = rapporto circolante/depositi · `j` = coefficiente di riserva. Il moltiplicatore è sempre maggiore di 1: il sistema bancario **crea moneta** oltre quella emessa dalla banca centrale. Se ti chiedono la base monetaria necessaria per un dato `M`, **dividi** invece di moltiplicare: `H = M / moltiplicatore`.

**Il problema di controllabilità**: la banca centrale controlla direttamente solo `H`, ma `h` e `j` sono **endogeni** — dipendono dai comportamenti del pubblico e delle banche. Se le banche aumentano le riserve libere (j sale), il moltiplicatore si riduce e la manovra della banca centrale arriva attenuata.

### La domanda di moneta e l'equilibrio del mercato monetario

```
      L(Y,i) = M_s/p
```

**dove** la domanda di moneta `L` ha una componente **transattiva** (cresce con `Y`) e una **speculativa** (cala con `i`, col segno meno: se il tasso sale conviene tenere titoli invece di moneta). Isolando `i` in questa equazione si ottiene la curva **LM**.

<div class="pagebreak"></div>

## Tutorial 1 — Moltiplicatore monetario e controllabilità

> **Traccia.** Il rapporto circolante/depositi è `h = 0,25`, il coefficiente di riserva è `j = 0,05`, la base monetaria è `H = 900`.
> a) Calcola il moltiplicatore monetario e l'offerta di moneta.
> b) La banca centrale vuole portare l'offerta di moneta a 5.000, a parità di `h` e `j`: quanta base monetaria deve creare in più?
> c) Le banche però aumentano le riserve libere e `j` sale a 0,10. Con la base monetaria del punto (b), quanto vale ora l'offerta di moneta?
> d) Come si chiama il problema illustrato dal punto (c)?

### Passo 1 (a) — Moltiplicatore e offerta di moneta

```
      moltiplicatore = (1 + h)/(h + j) = (1 + 0,25)/(0,25 + 0,05)
                     = 1,25/0,30 = 4,1667

      M = 4,1667 · 900 = 3.750
```

**Che cosa scrivi sul foglio:** calcola prima il moltiplicatore da solo, poi moltiplicalo per `H` — mai in un unico passaggio a mente, è dove si annidano gli errori di arrotondamento.

### Passo 2 (b) — Base monetaria per `M = 5.000`

```
      H = M/moltiplicatore = 5.000/4,1667 = 1.200

      base monetaria aggiuntiva = 1.200 − 900 = 300
```

**Controllo di buon senso:** verifica moltiplicando all'indietro: `4,1667 · 1.200 = 5.000` — torna.

### Passo 3 (c) — Se `j` sale a 0,10

```
      nuovo moltiplicatore = 1,25/(0,25 + 0,10) = 1,25/0,35 = 3,5714

      M = 3,5714 · 1.200 = 4.285,71        invece dei 5.000 desiderati
```

### Passo 4 (d) — Il problema

È il problema di **controllabilità** dell'offerta di moneta: la banca centrale controlla direttamente solo `H`, ma `h` e `j` sono **endogeni**. Le banche che accumulano riserve libere — tipico nelle fasi di sfiducia — spengono il moltiplicatore, e la manovra della banca centrale arriva attenuata: con la stessa base monetaria aggiuntiva, l'offerta di moneta resta 715 euro sotto l'obiettivo.

## Tutorial 2 — Domanda di moneta ed equilibrio del mercato monetario

> **Traccia.** La domanda di moneta è `L = 0,2 Y + 100 − 1.500 i`, l'offerta reale è `M_s/p = 250` e il reddito è `Y = 1.800`.
> a) Calcola il tasso di interesse di equilibrio.
> b) La banca centrale porta l'offerta reale a 310: quale diventa il tasso di equilibrio?
> c) Quale delle tre motivazioni keynesiane della domanda di moneta è rappresentata dal termine `0,2 Y` e quale dal termine `− 1.500 i`?
> d) In quale situazione la manovra del punto (b) non avrebbe alcun effetto sul tasso?

### Passo 1 (a) — Tasso di equilibrio

L'equilibrio del mercato monetario è `L = M_s/p`:

```
      0,2 · 1.800 + 100 − 1.500 i = 250
      360 + 100 − 1.500 i = 250
      460 − 1.500 i = 250
      1.500 i = 210
      i = 0,14                →  14%
```

### Passo 2 (b) — Offerta reale a 310

```
      460 − 1.500 i = 310
      1.500 i = 150
      i = 0,10                →  10%
```

Un'espansione monetaria di 60 fa scendere il tasso di 4 punti percentuali.

### Passo 3 (c) — I motivi keynesiani

- `0,2 Y` → domanda di moneta per motivi **transattivo e precauzionale**: dipende dal reddito, perché più si scambia più contante serve.
- `− 1.500 i` → domanda di moneta **speculativa**: col segno **meno** perché se il tasso sale conviene comprare titoli invece di tenere moneta, che non rende.

### Passo 4 (d) — Quando la manovra non avrebbe effetto

Nella **trappola della liquidità**: quando il tasso è già vicino allo zero, la domanda di moneta diventa **piatta** (elasticità infinita rispetto a `i`) e qualunque quantità di moneta in più viene assorbita **senza che il tasso scenda**. La LM diventa orizzontale e la politica monetaria perde presa.

## Gli errori tipici del blocco 3

| Errore | Come si evita |
|---|---|
| Moltiplicare invece di dividere per trovare la base monetaria necessaria | Se il dato è `M` desiderato e l'incognita è `H`: `H = M/moltiplicatore`, mai il contrario |
| Trattare `h` e `j` come costanti fissate dalla banca centrale | Sono **endogeni**: dipendono da pubblico e banche, non sono leve dirette della BC |
| Dimenticare il segno meno nel termine speculativo della domanda di moneta | `− 1.500 i` significa che un tasso più alto **riduce** la domanda di moneta, mai il contrario |
| Confondere l'offerta di moneta **nominale** con quella **reale** (`M_s/p`) | L'equilibrio del mercato monetario è sempre `L = M_s/p`: se il testo dà `M_s` e `p` separati, dividi prima di uguagliare |

<div class="pagebreak"></div>

## Tocca a te — esercizi B7, B8

### B7 — Moltiplicatore monetario

Il rapporto circolante/depositi è `h = 0,2`, il coefficiente di riserva è `j = 0,05`, la base monetaria è `H = 500`.

a) Calcola il moltiplicatore monetario e l'offerta di moneta.
b) La banca centrale vuole portare l'offerta di moneta a 3.000, a parità di `h` e `j`: quanta base monetaria deve creare in più?
c) Le banche però aumentano le riserve libere e `j` sale a 0,10. Con la base monetaria del punto (b), quanto vale ora l'offerta di moneta?
d) Come si chiama il problema illustrato dal punto (c)?

### B8 — Domanda di moneta ed equilibrio del mercato monetario

La domanda di moneta è `L = 0,3 Y + 150 − 2.000 i`, l'offerta reale è `M_s/p = 600` e il reddito è `Y = 2.000`.

a) Calcola il tasso di interesse di equilibrio.
b) La banca centrale porta l'offerta reale a 700: quale diventa il tasso di equilibrio?
c) Quale delle tre motivazioni keynesiane della domanda di moneta è rappresentata dal termine `0,3 Y` e quale dal termine `− 2.000 i`?
d) In quale situazione la manovra del punto (b) non avrebbe alcun effetto sul tasso?

<div class="pagebreak"></div>

# Soluzioni

*Guardale solo dopo aver provato. Se il risultato non torna, cerca prima l'errore da solo: quasi sempre è un'unità di misura o un segno.*

## Soluzione B1

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

## Soluzione B2

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

**Non è realistico** per un'economia matura: un tasso del 7% è da economia emergente. È il motivo per cui la disoccupazione scende **lentamente** anche quando la ripresa è in corso — e per cui una recessione la fa salire in fretta mentre la ripresa la fa scendere piano (**isteresi**, schema 05).

**(c) Perché il rapporto è più che proporzionale** — perché nel frattempo crescono anche la **popolazione** (quindi la forza lavoro: servono nuovi posti solo per non peggiorare) e la **produttività** (quindi ogni addetto produce di più, e a parità di prodotto ne servono meno). Una parte della crescita serve soltanto a **stare fermi**: solo l'eccedenza oltre quella soglia comincia ad assorbire disoccupazione. Ne segue il corollario da citare all'esame: **una crescita positiva ma modesta può convivere con una disoccupazione crescente**.

## Soluzione B3

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

## Soluzione B4

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

## Soluzione B5

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
- **Cambi fissi** — la banca centrale deve **difendere la parità**: compra valuta estera cedendo moneta nazionale, quindi le riserve ufficiali e la **base monetaria aumentano**. La LM si sposta a destra, il tasso torna a scendere e il reddito cresce ancora: la manovra fiscale viene **rafforzata**. È il risultato speculare del modello Mundell-Fleming.

## Soluzione B6

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

## Soluzione B7

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

## Soluzione B8

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
