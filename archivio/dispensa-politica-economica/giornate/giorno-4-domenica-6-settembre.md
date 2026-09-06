## Come si usa questo foglio

Oggi cambia un po' rispetto ai giorni 1-3: non ci sono cinque blocchi omogenei, perché il programma di oggi è per metà un argomento da esercizio (valutazione progetti) e per metà cinque capitoli letti finora solo di striscio. Tre blocchi:

| Blocco | Argomento | Esercizi | Tempo indicativo |
|---|---|---|---|
| 1 | Valutazione progetti pubblici: VAN, VAN relativo, TIR | B9 | 60 minuti |
| 2 | IS-LM: come si risponde a una domanda aperta con grafico | B10 | 30 minuti |
| 3 | Ripasso lampo dei cinque capitoli lasciati indietro (esternalità, crescita, disuguaglianze, fallimenti dello Stato, sistema monetario) | R1 → R5 | 90 minuti |

**Se il tempo non basta**, taglia nel blocco 3 in quest'ordine: R5 (sistema monetario — lo schema stesso lo segnala come il primo da sacrificare, perché non ha riscontro nei PDF della docente), poi R3 (disuguaglianze), poi R4 (fallimenti dello Stato), poi R2 (crescita). **R1 (esternalità) non si taglia**: è l'unico dei cinque comparso davvero nei compiti passati. I blocchi 1 e 2 non si tagliano in nessun caso: sono gli argomenti da scritto, non da preselezione.

**Segna con una crocetta ogni esercizio che sbagli.** Domani (giorno 5) rifai solo quelli.

<div class="pagebreak"></div>

# Blocco 1 — Valutazione dei progetti pubblici: VAN, VAN relativo, TIR

## La teoria che serve

### Le formule dell'analisi costi-benefici

```
                b_t                       c_t
      B = Σ ─────────          C = Σ ─────────
              (1+i)^t                   (1+i)^t

      VAN = B − C                  (valore attuale netto assoluto)

        B − C
      ─────────  =  VAN_r          (valore attuale netto relativo)
          C
```

**dove:** `b_t` = beneficio al tempo t · `c_t` = costo al tempo t · `i` = tasso di sconto sociale · `(1+i)^t` = fattore di sconto, elevato al numero di anni: più un beneficio è lontano, più pesa poco. Un costo interamente a `t=0` **non si attualizza** (`(1+i)^0 = 1`).

**I due criteri:** ammissibile se **VAN > 0**; fra gli ammissibili si sceglie il **VAN più alto**. Il **VAN relativo** (dividere per `C`) serve a **neutralizzare l'effetto dimensione**: un progetto grande ha quasi sempre un VAN assoluto più alto, ma non è detto che renda di più per euro speso — le due graduatorie possono divergere.

### Il tasso interno di rendimento (TIR)

```
      Σ b_t/(1+i)^t  −  Σ c_t/(1+i)^t  =  0
```

**dove:** il TIR è il valore di `i` (chiamiamolo `y = 1+i` una volta impostata l'equazione) che rende **B = C**, cioè annulla il VAN. Con un costo a `t=0` e benefici su due anni, l'equazione in `y` è di **secondo grado**: si risolve con la formula risolutiva e si tiene la radice **maggiore di 1** (un tasso di rendimento negativo non ha senso economico in questo contesto).

**Criterio di ammissibilità:** TIR > tasso di sconto sociale. **Criterio di scelta:** TIR più alto. **Relazione con il VAN** (controllo di buon senso): se il TIR supera il tasso usato per attualizzare, il VAN a quel tasso è positivo; se il TIR è inferiore, il VAN è negativo. Se sono uguali, il VAN è zero — per costruzione, è proprio la definizione di TIR.

### Perché non basta il prezzo di mercato: i prezzi ombra

I prezzi di mercato possono essere inaffidabili per tre motivi: sono **influenzati dal progetto stesso** (se grande), i mercati possono essere **distorti** (es. monopolio, P > MC), o riflettere una **distribuzione dei redditi** che il valutatore non condivide. Il **prezzo ombra** sostituisce il prezzo di mercato con il **costo-opportunità**: il valore del prodotto a cui si rinuncia impiegando le stesse risorse nel miglior progetto alternativo. Allo stesso modo, il **tasso di sconto sociale** può differire da quello di mercato — uno Stato che tiene conto delle generazioni future userà un tasso più basso, per dare più peso ai benefici lontani.

<div class="pagebreak"></div>

## Tutorial — VAN, VAN relativo e TIR

> **Traccia.** Un ente regionale deve scegliere fra due progetti alternativi, con tasso di sconto sociale **i = 8%**. I flussi (in migliaia di euro) sono:
>
> | Progetto | costo a t=0 | beneficio a t=1 | beneficio a t=2 |
> |---|---|---|---|
> | **A** — impianto di trattamento rifiuti (a regime solo dal secondo anno) | 400 | 60 | 460 |
> | **B** — efficientamento energetico degli edifici pubblici (risparmio immediato, che si riduce nel tempo) | 160 | 100 | 90 |
>
> a) Calcola il VAN assoluto dei due progetti. Sono entrambi ammissibili?
> b) Calcola il VAN relativo. La graduatoria cambia?
> c) Calcola il TIR di entrambi.
> d) Quale progetto scegli? Che cosa succede se il tasso di sconto sale al 14%?

### Passo 1 (a) — VAN assoluto

Il costo è tutto a `t=0`: non si attualizza, `C = c_0`.

```
      Progetto A
      B = 60/1,08 + 460/(1,08)²
        = 55,56 + 394,38
        = 449,93

      VAN_A = 449,93 − 400 = +49,93

      Progetto B
      B = 100/1,08 + 90/(1,08)²
        = 92,59 + 77,16
        = 169,75

      VAN_B = 169,75 − 160 = +9,75
```

**Che cosa scrivi sul foglio:** attualizza i due benefici **separatamente**, uno alla volta — è dove si annidano gli errori di segno e di potenza. Entrambi i VAN sono **positivi**: entrambi i progetti sono **ammissibili**. Sul VAN assoluto vince **A**.

### Passo 2 (b) — VAN relativo

```
      VAN_r = (B − C)/C

      A:  49,93/400 = 0,1248     →  12,48%
      B:   9,75/160 = 0,0610     →   6,10%
```

**Controllo di buon senso:** entrambi i VAN relativi restano positivi, come deve essere se il VAN assoluto lo è. Qui la graduatoria **non si ribalta** (vince ancora A, anche per euro investito) — non è sempre così: nell'esercizio B9 che segue, invece, si ribalta. È il motivo per cui il VAN relativo va sempre calcolato, non dato per scontato.

### Passo 3 (c) — TIR

Si pone VAN = 0. Con due periodi, posto `y = 1 + i`, si ottiene un'equazione di secondo grado.

```
      Progetto A
      400 y² = 60 y + 460
      400y² − 60y − 460 = 0
      20y² − 3y − 23 = 0        (diviso per 20)

      y = [ 3 ± √(9 + 4·20·23) ] / 40
        = [ 3 ± √1.849 ] / 40
        = (3 ± 43)/40

      y = 46/40 = 1,15        →  TIR_A = 15%
```

```
      verifica:  60/1,15 = 52,17  e  460/1,3225 = 347,83
                 52,17 + 347,83 = 400 = C     ✓  il VAN si annulla
```

```
      Progetto B
      160 y² = 100 y + 90
      160y² − 100y − 90 = 0
      16y² − 10y − 9 = 0         (diviso per 10)

      y = [ 10 ± √(100 + 4·16·9) ] / 32
        = [ 10 ± √676 ] / 32
        = (10 ± 26)/32

      y = 36/32 = 1,125       →  TIR_B = 12,5%
```

**Che cosa scrivi sul foglio:** il discriminante è un quadrato perfetto in entrambi i casi (`√1.849 = 43`, `√676 = 26`) — se al tuo esercizio non torna un numero pulito, quasi sempre l'errore è nel segno di uno dei due termini dell'equazione, non nella formula risolutiva in sé. **Anche sul TIR vince A** (15% contro 12,5%): qui tutti e tre i criteri sono concordi.

### Passo 4 (d) — Scelta e sensibilità al tasso

| Criterio | Vincitore |
|---|---|
| VAN assoluto | **A** (49,93 contro 9,75) |
| VAN relativo | **A** (12,48% contro 6,10%) |
| TIR | **A** (15% contro 12,5%) |

Con i tre criteri concordi, la scelta è semplice: **si finanzia A**. Con tasso di sconto al **14%**:

```
      A:  B = 60/1,14 + 460/1,2996 = 52,63 + 354,00 = 406,63
          VAN_A = 406,63 − 400 = +6,63     >0  →  ancora ammissibile

      B:  B = 100/1,14 + 90/1,2996 = 87,72 + 69,25 = 156,97
          VAN_B = 156,97 − 160 = −3,03     <0  →  NON più ammissibile
```

**Controllo di buon senso incrociato con il TIR:** A ha TIR 15% > 14%, quindi il suo VAN a quel tasso **deve** restare positivo — torna. B ha TIR 12,5% < 14%, quindi il suo VAN **deve** essere negativo — torna anche questo, senza bisogno di ricalcolare da zero. **A resiste a un tasso più alto perché il suo TIR è più lontano dal tasso di sconto**: un margine di sicurezza che B, con un TIR più vicino al tasso di partenza, non ha.

## Gli errori tipici del blocco 1

| Errore | Come si evita |
|---|---|
| Attualizzare anche il costo a `t=0` | `(1+i)^0 = 1`: il costo iniziale entra nel calcolo **così com'è**, non si divide per nulla |
| Dimenticare di dividere per `C` nel VAN relativo (confonderlo col VAN assoluto) | Il VAN relativo è sempre **(B−C)/C**, un numero puro (%), non in migliaia di euro come il VAN assoluto |
| Nell'equazione del TIR, sbagliare il segno di uno dei termini a destra | Riscrivi sempre prima `C·y² = b₁·y + b₂`, **poi** porta tutto a sinistra: `C·y² − b₁·y − b₂ = 0` |
| Tenere la radice minore (o negativa) dell'equazione di secondo grado | Il TIR è sempre la radice **maggiore di 1**: un tasso di rendimento sotto zero non ha senso in questo contesto |
| Concludere "VAN più alto quindi si sceglie" senza controllare anche il vincolo di bilancio | Se le risorse sono limitate, il criterio giusto è il VAN **relativo** (o il TIR), non quello assoluto — vale il progetto che rende di più **per euro investito** |

<div class="pagebreak"></div>

## Tocca a te — esercizio B9

### B9 — Analisi costi-benefici: VAN, VAN relativo e TIR

Un comune deve scegliere fra due progetti. Il tasso di sconto sociale è `i = 4%`. I flussi (in migliaia di euro) sono:

| Progetto | costo a t=0 | beneficio a t=1 | beneficio a t=2 |
|---|---|---|---|
| **A** | 500 | 300 | 360 |
| **B** | 200 | 150 | 125 |

a) Calcola il VAN assoluto dei due progetti. Sono entrambi ammissibili?
b) Calcola il VAN relativo. La graduatoria cambia?
c) Calcola il TIR di entrambi.
d) Quale progetto scegli, e con quale motivazione? Che cosa succede se il tasso di sconto sale al 20%?

<div class="pagebreak"></div>

# Blocco 2 — IS-LM: come si risponde a una domanda aperta con grafico

## La teoria che serve

Il blocco 2 è diverso dagli altri: **B10 non è un esercizio numerico**, è una domanda aperta con grafico — il formato più probabile per una delle due domande dello scritto. Non serve quindi un tutorial con numeri nuovi: serve un **metodo per strutturare la risposta**, e i numeri già pronti dell'esercizio B5 (giorno 3) bastano a illustrarlo.

**Come si imposta una risposta di questo tipo (schema in quattro mosse):**

1. **Definisci le due curve** — la IS è l'equilibrio del mercato dei beni (inclinata negativamente: un tasso più basso stimola gli investimenti e quindi il reddito), la LM è l'equilibrio del mercato della moneta (inclinata positivamente: un reddito più alto alza la domanda di moneta per transazioni e, a offerta data, il tasso deve salire).
2. **Descrivi lo spostamento** che la manovra provoca — quale curva si sposta, in che direzione, di quanto (`moltiplicatore × ΔG`, se è uno spostamento di IS).
3. **Leggi il nuovo equilibrio** sul grafico, e confronta l'aumento di reddito **effettivo** con lo spostamento **a tasso invariato** della curva: la differenza è sempre il concetto che la domanda vuole verificare (qui, lo spiazzamento).
4. **Cita un caso numerico**, se ne hai uno pronto: in una domanda aperta vale sempre punti mostrare che sai anche calcolare l'effetto, non solo descriverlo a parole.

**Il grafico non è un extra:** la traccia lo chiede esplicitamente ("anche graficamente"). Disegna sempre IS e LM, la curva che si sposta, il vecchio e il nuovo equilibrio, e — quando serve — le due distanze da confrontare sull'asse orizzontale (lo spostamento della curva e l'aumento effettivo di Y).

## Gli errori tipici del blocco 2

| Errore | Come si evita |
|---|---|
| Rispondere solo a parole, senza il grafico richiesto dalla traccia | Il grafico va **sempre** fatto quando la domanda lo chiede: è parte della risposta, non un'illustrazione facoltativa |
| Confondere lo spostamento della curva con l'aumento effettivo di `Y` | Sono due segmenti diversi sull'asse orizzontale: la differenza fra i due **è** lo spiazzamento, non un dettaglio da citare a parte |
| Dimenticare il caso della politica **accomodante** (banca centrale che espande l'offerta di moneta insieme alla manovra fiscale) | È l'estensione che chiude il discorso: senza spiazzamento la LM si sposta anch'essa, e la politica fiscale diventa pienamente efficace |
| Non citare i due casi limite (LM orizzontale/trappola della liquidità, LM verticale/caso monetarista) | Sono il modo per mostrare di aver capito il modello, non solo il caso intermedio — vale punti extra in una risposta aperta |

<div class="pagebreak"></div>

## Tocca a te — esercizio B10

### B10 — IS-LM: moltiplicatore e spiazzamento (domanda aperta con grafico)

> **Formulazione esatta** trovata nel materiale del corso ("Compito di ripasso teorie"). Non è un esercizio numerico: è una domanda aperta con grafico, ed è il formato più probabile per una delle due domande dello scritto.

Utilizza il modello IS-LM per spiegare, **anche graficamente**, le affermazioni seguenti:

a) La politica fiscale (aumento della spesa pubblica) è efficace per la stabilizzazione della domanda aggregata (il moltiplicatore "keynesiano").
b) Un aumento della spesa pubblica non accompagnato da un aumento dell'offerta di moneta (politica economica non "accomodante") provoca un aumento del tasso di interesse e quindi una riduzione degli investimenti privati (spiazzamento finanziario).

*Suggerimento: la risposta al punto (b) è già mezza fatta nell'esercizio B5, punto (d). Fai il grafico prima di scrivere.*

<div class="pagebreak"></div>

# Blocco 3 — Ripasso lampo: i cinque capitoli lasciati indietro

Questi cinque schemi (08, 09, 10, 12, 14) non sono mai comparsi nei compiti passati analizzati, ma la **preselezione** pesca su tutto il programma: una domanda su un argomento mai visto costa quanto una sui core. Vanno letti a livello di **definizioni e classificazioni**, non di esercizio — con l'eccezione dell'esternalità (08), che è l'unico dei cinque **davvero comparso** in un compito, ed è esercizio-shaped come il blocco 1.

Per ciascun argomento: una scheda con **quello che serve sapere**, poi una traccia di autoverifica. Soluzioni in fondo, come sempre.

## R1 — Esternalità (08)

**Quello che serve sapere**

- **Esternalità**: effetto di produzione o consumo che ricade su altri agenti **per una via diversa dai prezzi di mercato**; nessun corrispettivo monetario compensa il danno o il vantaggio.
- **Negativa**: il costo sociale supera quello privato → senza correttivi, **sovra-produzione/consumo**. **Positiva**: il beneficio sociale supera quello privato → **sotto-produzione/consumo**.
- Equilibrio di **concorrenza**: `MB_P = MC_P` (grandezze private). **Ottimo sociale**: `MB_S = MC_S`, dove `MC_S = MC_P + costo esterno marginale` (esternalità negativa di produzione).
- **Tassa pigouviana**: `t = costo esterno marginale`, riporta il produttore a eguagliare `P = MC_P + t`, che coincide con la condizione dell'ottimo sociale.
- **Teorema di Coase**: se i costi di transazione sono nulli, lo scambio di diritti negoziabili conduce all'ottimo sociale indipendentemente da chi li riceve inizialmente. Una **tassa fissa il prezzo** e lascia il mercato determinare la quantità; un **cap-and-trade fissa la quantità** e lascia il mercato determinare il prezzo.

> **Traccia.** La domanda inversa di un bene è `P = 30 − 3q`, il costo marginale privato è `MC_P = 2q`. La produzione genera un costo esterno marginale costante di **15** per unità.
>
> a) Calcola quantità e prezzo di equilibrio in concorrenza perfetta.
> b) Calcola la quantità socialmente ottima.
> c) Quale tassa pigouviana riporta il mercato all'ottimo sociale? Verificalo.

## R2 — Crescita e misurazione del PIL (09)

**Quello che serve sapere**

- **PIL nominale** = Σ pᵢqᵢ ai prezzi correnti. **PIL reale (Y)** = stessa somma a prezzi di un anno base. **Deflatore P = PIL nominale/PIL reale**.
- Tre metodi di calcolo equivalenti: **produzione** (Σ valori aggiunti), **spesa** (`C+I+G+(X−M)`), **reddito** (salari+profitti+imposte nette).
- **Crescita ≠ sviluppo**: la crescita è l'aumento del PIL; lo sviluppo è il miglioramento delle condizioni di vita (salute, istruzione, ambiente) — **può esserci crescita senza sviluppo**.
- Limiti del PIL come misura di benessere: non registra il deprezzamento del capitale (prodotto e naturale), non distingue beni "buoni" da "cattivi", conta le spese difensive come valore aggiunto, ignora l'economia sommersa e la distribuzione del reddito.
- Indicatori alternativi: **BES** (ISTAT, 4 macro-aree), **ISU/HDI** (ONU: longevità, scolarità, standard di vita), **SDGs** (17 obiettivi ONU).

> **Traccia.** Un paese produce pasta e biciclette.
> - 2023 (anno base): pasta 1,50 € × 2.000 unità; biciclette 300 € × 50 unità.
> - 2025, a prezzi 2025: pasta 1,80 € × 2.200 unità; biciclette 350 € × 55 unità.
>
> a) Calcola il PIL 2023, il PIL nominale 2025 e il PIL reale 2025 (a prezzi 2023).
> b) Di quanto è cresciuto il PIL in termini nominali? E in termini reali?
> c) Quanta parte della crescita nominale è dovuta all'inflazione, e quanta alla crescita reale delle quantità?

## R3 — Disuguaglianze e Stato Sociale (10)

**Quello che serve sapere**

- **Curva di Lorenz**: quota cumulata di reddito vs quota cumulata di popolazione. **Indice di Gini = 2A** (A = area fra bisettrice e curva di Lorenz): 0 = uguaglianza perfetta, 1 = disuguaglianza massima. Il Gini sui redditi **di mercato** è sempre più alto di quello sui redditi **disponibili**: tasse e trasferimenti riducono la disuguaglianza.
- **Redistribuzione** (ex post, su reddito disponibile: tasse/trasferimenti) vs **pre-distribuzione** (ex ante, su reddito di mercato: es. salario minimo).
- Imposte: **in somma fissa** (non dipende dal reddito), **proporzionale** (aliquota costante), **progressiva** (aliquota crescente col reddito). **Aliquota marginale** = sull'ultimo euro guadagnato; **aliquota media** = imposta totale/reddito totale — in un sistema progressivo, la media è sempre **≤** la marginale.
- **Stato Sociale**, tre modelli di welfare: **Bismarck** (contributi, occupazionale), **Beveridge anglosassone** (fiscalità generale, mirato ai poveri), **Beveridge scandinavo** (fiscalità generale, universalistico).
- **Gender Pay Gap = (Wm − Wf)/Wm**; si scompone (Blinder-Oaxaca) in una componente **spiegata** (istruzione, esperienza, settore) e una **non spiegata** (possibile discriminazione).

> **Traccia.** Applica gli scaglioni IRPEF 2025 (23% fino a 28.000 €; da 28.001 a 50.000 €, 6.440 € + 35% sull'eccedenza; oltre 50.000 €, 14.140 € + 43% sull'eccedenza) a un reddito di **42.000 €**.
>
> a) Calcola l'imposta dovuta.
> b) Calcola l'aliquota media e l'aliquota marginale.
> c) Perché, in un sistema progressivo, l'aliquota media è sempre minore o uguale a quella marginale?

## R4 — I fallimenti dello Stato (12)

**Quello che serve sapere**

- Un **fallimento dello Stato** si ha quando l'intervento pubblico "reale" non corrisponde a quello "ideale": non realizza l'interesse collettivo, o i risultati sono peggiori in efficienza e/o equità.
- **Le tre cause** (la domanda più probabile su questo schema):
  1. **Informazioni incomplete** — politici e burocrati non conoscono tutte le variabili rilevanti (es. il vero costo marginale sociale per fissare una tassa pigouviana, o le reazioni future degli agenti → incoerenza temporale).
  2. **Opportunismo** — si perseguono vantaggi personali (rielezione, potere) anche a costo della collettività; si declina come selezione avversa/azzardo morale.
  3. **Ricerca della rendita (rent seeking)** — i gruppi di interesse cercano di influenzare le decisioni discrezionali di politici e burocrati: lobbying, nei casi estremi corruzione.
- **Ciclo politico-economico (Nordhaus)**: politiche espansive prima delle elezioni, restrittive dopo → l'economia è resa instabile dal calendario elettorale, non dalla congiuntura.
- **Doppio problema di agenzia**: elettori → politici → burocrati, un problema principale-agente si somma all'altro a ogni passaggio della delega.
- Il punto da non perdere: un fallimento del mercato è condizione **necessaria ma non sufficiente** per giustificare l'intervento pubblico — va confrontato con l'esito **realistico**, non ideale, dell'intervento.

> **Traccia.** Per ciascuno dei seguenti episodi, indica quale delle tre cause dei fallimenti dello Stato lo spiega meglio, e perché:
>
> a) Il regolatore fissa una tassa pigouviana troppo bassa perché non conosce il vero costo esterno marginale dell'inquinamento.
> b) Un ministro concentra la spesa pubblica sui collegi elettorali in bilico in vista delle elezioni.
> c) Un'associazione di categoria finanzia la campagna elettorale di un politico in cambio di una norma che protegge il settore dalla concorrenza estera.

## R5 — Il sistema monetario internazionale (14)

**Quello che serve sapere**

- Il **sistema monetario internazionale** è l'insieme delle regole su come si determinano i cambi, quali attività fungono da riserva, quali obblighi hanno le banche centrali.
- **Cambi flessibili**: riequilibrio automatico di BP tramite il cambio, non servono riserve; ma incertezza sui prezzi internazionali e — nella realtà — "fluttuazione sporca" (la banca centrale interviene comunque).
- **Cambi fissi**: disciplinano i prezzi interni e costringono a politiche per la competitività (non potendo svalutare); ma con alta mobilità dei capitali il tasso interno resta legato a quello estero, e servono riserve per difendere la parità.
- **Collegamento con Mundell-Fleming** (schema 06): in cambi fissi con alta mobilità dei capitali è efficace la **politica fiscale**, inefficace quella **monetaria**; in cambi flessibili vale l'opposto.
- **Gold standard**: riserve auree pari alla moneta emessa, cambi fissi per costruzione. **Bretton Woods (1944)**: gli altri paesi usano il **dollaro** come riserva, cambi fissi ma aggiustabili — fino al **1971**, inconvertibilità del dollaro in oro.
- **Dilemma di Triffin**: per sostenere il commercio mondiale servono sempre più dollari all'estero (disavanzi persistenti USA), ma se il contenuto aureo resta costante quei dollari in eccesso non sono più coperti → **liquidità internazionale sufficiente** e **credibilità della conversione** sono in contraddizione. Nel 1971 si è sciolta sospendendo la convertibilità.

> **Traccia.**
>
> a) Un paese con alta mobilità dei capitali sceglie i cambi fissi: quale politica economica resta efficace, fiscale o monetaria? Perché?
> b) In che cosa consiste il dilemma di Triffin, e perché ha portato alla fine di Bretton Woods nel 1971?
> c) Cita un vantaggio e uno svantaggio dei cambi flessibili.

## Gli errori tipici del blocco 3

| Errore | Come si evita |
|---|---|
| Nell'esternalità, dimenticare che il costo esterno si somma al **costo marginale privato**, non al prezzo | `MC_S = MC_P + costo esterno marginale`: è il costo che sale, non la domanda |
| Confondere PIL nominale e reale nel calcolo con due beni | Il PIL **reale** usa sempre i prezzi dell'**anno base** applicati alle quantità dell'anno corrente; il PIL **nominale** usa i prezzi correnti |
| Applicare l'aliquota IRPEF più alta a **tutto** il reddito, invece che solo alla parte eccedente lo scaglione | Il sistema è per scaglioni: l'aliquota del 35% (o 43%) si applica solo alla quota di reddito **oltre** la soglia, non al totale |
| Confondere i fallimenti dello **Stato** con i fallimenti del **mercato** | I primi riguardano l'intervento pubblico (informazioni incomplete, opportunismo, rent seeking); i secondi il meccanismo dei prezzi (concorrenza imperfetta, mercati incompleti) |
| Nel sistema monetario, dare per scontato che i cambi fissi tolgano sempre autonomia alla politica monetaria | Vale solo con **alta mobilità dei capitali** (risultato di Mundell-Fleming): è la condizione da citare, non solo la conclusione |

<div class="pagebreak"></div>

# Soluzioni

*Guardale solo dopo aver provato. Se il risultato non torna, cerca prima l'errore da solo: quasi sempre è un'unità di misura o un segno.*

## Soluzione B9

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

## Soluzione B10

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

## Soluzione R1 — Esternalità

**(a) Equilibrio di concorrenza perfetta**

```
      P = MC_P
      30 − 3q = 2q
      30 = 5q      →   q_CP = 6
      P_CP = 30 − 3 · 6 = 12
```

**(b) Quantità socialmente ottima**

Il costo marginale sociale include il costo esterno: `MC_S = MC_P + 15 = 2q + 15`.

```
      P = MC_S
      30 − 3q = 2q + 15
      15 = 5q      →   q_OS = 3
      P_OS = 30 − 3 · 3 = 21
```

`q_OS (3) < q_CP (6)`: il mercato concorrenziale, ignorando il costo esterno, produce **il doppio** della quantità socialmente desiderabile.

**(c) Tassa pigouviana**

```
      t = costo esterno marginale = 15
```

Verifica: con la tassa, il produttore eguaglia `P = MC_P + t = 2q + 15`, cioè esattamente la condizione dell'ottimo sociale calcolata al punto (b): `30 − 3q = 2q + 15 → q = 3 = q_OS`, prezzo pagato dal consumatore `P = 21` (di cui 15 vanno allo Stato come imposta). **La tassa pigouviana di 15 riporta l'equilibrio esattamente sull'ottimo sociale**, eliminando la sovra-produzione.

## Soluzione R2 — Crescita e PIL

**(a) I tre PIL**

```
      PIL 2023 (anno base):
      pasta  1,50 · 2.000 =  3.000
      bici   300  ·    50 = 15.000
      PIL 2023 = 18.000

      PIL nominale 2025 (prezzi 2025):
      pasta  1,80 · 2.200 =  3.960
      bici   350  ·    55 = 19.250
      PIL nominale 2025 = 23.210

      PIL reale 2025 (a prezzi 2023):
      pasta  1,50 · 2.200 =  3.300
      bici   300  ·    55 = 16.500
      PIL reale 2025 = 19.800
```

**(b) Crescita nominale e reale**

```
      crescita nominale = (23.210 − 18.000)/18.000 = 28,9%
      crescita reale    = (19.800 − 18.000)/18.000 = 10,0%
```

**(c) Quota dovuta all'inflazione**

La differenza fra le due variazioni (28,9% − 10,0% ≈ 18,9 punti) è dovuta all'**inflazione**: il PIL nominale cresce sia perché si produce di più (le quantità), sia perché i prezzi sono saliti. Il PIL reale, valutato a prezzi costanti (2023), isola la sola componente di **crescita reale delle quantità** (10%): è quella la cifra che conta per giudicare se l'economia sta davvero producendo di più, non semplicemente vendendo agli stessi volumi a prezzi più alti.

## Soluzione R3 — IRPEF, aliquota media e marginale

**(a) Imposta dovuta**

Il reddito di 42.000 € ricade nel secondo scaglione (28.001-50.000 €):

```
      T = 6.440 + 0,35 · (42.000 − 28.000)
        = 6.440 + 0,35 · 14.000
        = 6.440 + 4.900
        = 11.340
```

**(b) Aliquote**

```
      aliquota media = T/reddito = 11.340/42.000 = 0,27  →  27%
      aliquota marginale = 35%  (scaglione dell'ultimo euro)
```

**(c) Perché la media è sempre ≤ la marginale**

L'aliquota media è una **media ponderata** delle aliquote di tutti gli scaglioni attraversati (23% sui primi 28.000 €, 35% solo sull'eccedenza): finché almeno una parte del reddito è tassata a un'aliquota più bassa di quella marginale, la media resta sotto quest'ultima. Solo un contribuente con reddito **arbitrariamente alto**, dove la parte tassata al 43% domina il totale, vedrebbe la propria aliquota media avvicinarsi (ma mai superare) la marginale.

## Soluzione R4 — Le tre cause dei fallimenti dello Stato

**(a) Informazioni incomplete.** È esattamente uno dei tre casi tipici citati per questa causa: il regolatore non conosce il vero costo marginale sociale, quindi non può fissare la tassa pigouviana al livello corretto (`t = costo esterno marginale`, schema 08). Non è malafede: è un limite informativo.

**(b) Opportunismo.** Il ministro persegue un obiettivo proprio (la rielezione) invece del massimo benessere sociale, concentrando la spesa su chi "premia col voto" (gli elettori nei collegi in bilico) anziché su dove il beneficio sociale sarebbe più alto. È lo stesso meccanismo, su scala macro, del **ciclo politico-economico di Nordhaus**.

**(c) Ricerca della rendita.** L'associazione di categoria esercita **lobbying** per ottenere una decisione politica a proprio vantaggio (una barriera protettiva) attraverso il finanziamento della campagna elettorale — la definizione stessa di *rent seeking*: usare risorse non per produrre valore, ma per influenzare chi ha potere discrezionale.

## Soluzione R5 — Sistema monetario internazionale

**(a) Politica efficace in cambi fissi con alta mobilità dei capitali**

Resta efficace la **politica fiscale**; la politica **monetaria perde autonomia**. Con cambi fissi e capitali mobili, il tasso di interesse interno è **ancorato** a quello estero (altrimenti si innescherebbero flussi di capitale che la banca centrale dovrebbe neutralizzare per difendere la parità): la banca centrale non può quindi usare il tasso come leva propria. È il risultato speculare di Mundell-Fleming rispetto ai cambi flessibili, dove vale l'opposto.

**(b) Il dilemma di Triffin**

La liquidità internazionale coincide con la valuta di riserva (il dollaro): perché il commercio mondiale cresca, il mondo ha bisogno di **sempre più dollari** all'estero, cioè di disavanzi persistenti degli Stati Uniti. Ma se il contenuto in oro del dollaro resta costante, quei dollari in eccesso non sono più coperti dalle riserve auree USA: o gli Stati Uniti **limitano** l'emissione (e il sistema non fornisce abbastanza liquidità al commercio mondiale), o **emettono abbastanza** dollari (e la convertibilità in oro diventa via via meno credibile). Le due esigenze — liquidità sufficiente e credibilità della conversione — sono in contraddizione strutturale: nel 1971 si è sciolta nel modo prevedibile, con gli Stati Uniti che hanno sospeso la convertibilità del dollaro in oro, chiudendo Bretton Woods e aprendo l'era dei cambi flessibili.

**(c) Cambi flessibili: un vantaggio e uno svantaggio**

**Vantaggio**: assicurano un riequilibrio automatico della bilancia dei pagamenti attraverso le oscillazioni del cambio, senza bisogno di accumulare riserve ufficiali di valuta estera. **Svantaggio**: l'incertezza sui tassi di cambio futuri ostacola gli scambi commerciali e i movimenti di capitale — e nella pratica il riequilibrio automatico è spesso incompleto, per cui le banche centrali intervengono comunque ("fluttuazione sporca").
