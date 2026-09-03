# Economia aperta, bilancia dei pagamenti e modello IS-LM-BP

**Domande d'esame collegate:**

- Modello IS-LM-BP completo (dato esempio: C=0,7Y consumo, I=600-400i investimenti, G=380 spesa pubblica, M=0,1Y importazioni, X=320 esportazioni, Ld=0,25Y+500-1000i domanda di moneta): calcolo del reddito di equilibrio, del saldo della bilancia commerciale, della domanda di moneta transattiva
- Da una tabella con Export/Import/Movimenti di capitale: calcolo della variazione delle riserve ufficiali e del suo effetto sulla base monetaria

---

**1. Perché l'economia aperta cambia il modello**

- In un'economia aperta l'economia nazionale ha relazioni commerciali e finanziarie con il **Resto del Mondo (RdM)**.
- Il modello di politica economica deve includere:
  - un **nuovo obiettivo**: l'equilibrio nei conti con l'estero (BP=0)
  - un **nuovo strumento**: il **tasso di cambio**

**2. La bilancia dei pagamenti (BP): definizione e registrazione**

- La **BP** è un documento contabile che registra le transazioni commerciali e finanziarie effettuate in un dato periodo tra i **residenti** di un paese e i **non residenti**.
- Le transazioni sono regolate in **valuta estera**.
- Principio della **doppia registrazione**: ogni transazione genera una scrittura e, con segno opposto, l'incasso/pagamento che ne deriva.

| Tipo di voce | Significato | Esempi |
|---|---|---|
| **A debito** | pagamento al RdM = esborso di valuta estera | importazioni di merci/servizi, trasferimenti unilaterali all'estero, acquisto di titoli esteri |
| **A credito** | incasso dal RdM = afflusso di valuta estera | esportazioni di merci/servizi, trasferimenti unilaterali dall'estero, vendita di titoli nazionali a non residenti |

**3. Struttura della bilancia dei pagamenti (tre conti)**

| Conto | Contenuto |
|---|---|
| **Conto corrente (CC)** | **bilancia commerciale** (scambi di merci) + partite invisibili (servizi, redditi, trasferimenti unilaterali correnti) |
| **Conto capitale (CK)** | attività intangibili (es. brevetti) + trasferimenti unilaterali in conto capitale |
| **Conto finanziario (CF)** | **movimenti di capitale (MK)** (investimenti diretti e di portafoglio) + variazione delle riserve ufficiali (RU) |

- In assenza di errori ed omissioni, il saldo complessivo della BP è nullo (per costruzione contabile).
- **Semplificando** (CK=0): **BP = CC + MK**, e questo saldo corrisponde algebricamente alla **variazione delle riserve ufficiali** (RU) cambiata di segno.
  - Disavanzo di BP → RU diminuiscono
  - Avanzo di BP → RU aumentano (→ creazione di base monetaria, BM)

- Logica macro: se X>M (esportazioni > importazioni), allora Y>C+I, cioè S>I: l'equilibrio richiede che il risparmio in eccesso trovi sbocco all'estero (deflusso di capitali).

**4. Il tasso di cambio**

- **Tasso di cambio nominale (e)**: prezzo di una valuta in termini di un'altra (quotazione certo per incerto: unità di valuta estera per 1 unità di valuta nazionale, es. USD per 1 Euro).
- **Apprezzamento**: aumento di e (es. da 1,2 a 1,25 USD per 1 Euro) → serve più valuta estera per comprare 1 unità di valuta nazionale.
- **Deprezzamento**: diminuzione di e (es. da 1,2 a 1,15 USD per 1 Euro).
- Cause: eccesso di domanda/offerta di valuta sul mercato dei cambi (le importazioni generano domanda di valuta estera, le esportazioni offerta di valuta estera).
- **Tasso di cambio reale**: misura la competitività, cioè quanto costano i beni interni rispetto a quelli esteri.

```
        p · e
      ─────────  =  e_r
          p_w
```

**dove:**
- `e_r` = tasso di cambio **reale** (competitività)
- `p` = livello dei prezzi **interni**
- `p_w` = livello dei prezzi **esteri** (w sta per *world*)
- `e` = tasso di cambio **nominale**

  - Se `p · e = p_w` (quindi `e_r = 1`): vale la **parità dei poteri d'acquisto**, la "condizione di arbitraggio internazionale" — con la stessa somma si compra la stessa quantità di beni dentro e fuori.
  - **Apprezzamento reale** (`e_r` sale) → i nostri beni costano relativamente di più → **perdita** di competitività.
  - **Deprezzamento reale** (`e_r` scende) → **guadagno** di competitività.
  - **Versione dinamica** (in tassi di variazione, cioè "di quanto cambia ogni grandezza"):

```
      ė_r = ṗ + ė − ṗ_w
```

**dove** il puntino sopra la lettera significa "tasso di variazione di": `ṗ` = inflazione interna, `ṗ_w` = inflazione estera, `ė` = variazione del cambio nominale. In parole: **la competitività peggiora se la nostra inflazione supera quella estera**, e migliora se il cambio si deprezza.

**5. Regimi di cambio: fisso vs flessibile**

| | **Cambi fissi** | **Cambi flessibili** |
|---|---|---|
| Meccanismo | Cambio ancorato a una parità fissata dalle autorità monetarie (eventualmente con bande di oscillazione) | Cambio determinato liberamente da domanda/offerta di valuta |
| Ruolo Banca Centrale | Interviene acquistando/cedendo valuta estera per mantenere fisso e | Discrezionalità di intervento ("fluttuazione sporca"), nessun obbligo |
| Se BP>0 | Aumentano le **riserve ufficiali** (BC cede euro, assorbe valuta estera) | Il cambio si **apprezza** (↑e) |
| Se BP<0 | Diminuiscono le **riserve ufficiali** | Il cambio si **deprezza** (↓e) |
| Esempio storico | SME prima dell'UME | — |

**6. Meccanismi automatici di riequilibrio della BP**

- **Via movimenti di capitale (MK)**: sotto (perfetta) mobilità dei capitali, MK = 0 è garantito dalla **condizione di parità scoperta**:

```
      i = i_w − ė ᵉ
```

**dove:**
- `i` = tasso di interesse **interno**
- `i_w` = tasso di interesse **estero**
- `ė ᵉ` = deprezzamento **atteso** della valuta nazionale (il puntino = tasso di variazione, la "e" in alto = atteso)

  È una condizione di **non arbitraggio**: il rendimento atteso di un'attività in valuta nazionale deve eguagliare quello di un'attività estera analoga, al netto del deprezzamento atteso della valuta nazionale. Se `i` è **maggiore** di `i_w − ė ᵉ` → conviene investire da noi → afflusso di capitali → `i` tende a scendere finché l'uguaglianza è ristabilita.

- **Via cambi flessibili**: se BP>0 → ↑e → ↑e_r → ↓CC → BP torna a 0; se BP<0 → ↓e → ↓e_r → ↑CC → BP torna a 0.

- **Via variazione dei prezzi in cambi fissi (meccanismo "neoclassico")**: BP>0 → ↑RU → ↑BM → ↑p → ↑e_r → ↓CC → BP torna a 0 (e simmetrico per BP<0). Limiti: l'effetto di BM sui prezzi può essere debole; i prezzi sono spesso rigidi verso il basso, l'aggiustamento è lento e può generare inflazione/deflazione indesiderata.

- **Via variazione dei redditi in cambi fissi (meccanismo "keynesiano")**: uno shock su X si trasmette a Y e quindi a M, smorzando parzialmente lo squilibrio (es. ↑X → CC>0, ma ↑X → ↑Y → ↑M → ↓CC, quindi ↓BP verso 0). Limiti: il riequilibrio non è completo e il canale via riduzione del reddito ha un costo elevato in termini di disoccupazione.

**7. Le politiche di riequilibrio della BP**

- I meccanismi automatici hanno limiti (lentezza, incompletezza, costi su altri obiettivi) → servono **politiche attive**. In generale è preferibile intervenire sulle **cause** dello squilibrio, ma si può intervenire anche su fattori diversi da quelli che l'hanno generato (es. sui MK quando la causa è nei movimenti di beni).

| Tipo di riequilibrio | Leva |
|---|---|
| **Riequilibrio dei MK** | Politica monetaria (variazione di i) o controllo diretto dei movimenti di capitale (es. "tassa di Tobin") |
| **Riequilibrio del CC** | Politiche per la domanda aggregata (fiscali/monetarie, agiscono su Y) oppure politiche per la competitività (agiscono su p, p_w, e) |

- **Politica monetaria sui MK**: se `i` è **minore** di `i_w − ė ᵉ` (quindi conviene portare i capitali all'estero), la BC può fare politica monetaria **restrittiva** per alzare `i` ed evitare il deflusso; MA questo ha effetti restrittivi su Y e può aggravare il debito pubblico (tassi più alti). In alternativa: controllo diretto dei MK. Attenzione: le politiche influenzano anche le **aspettative** `ė ᵉ`, che a loro volta muovono i MK.

- **Politiche di domanda sul CC**. Il saldo commerciale dipende da tre variabili, due con segno negativo e una con segno positivo:

```
      CC = X − M = f( e_r , Y , Y_w )
                       −    −    +
```

**dove** il segno sotto ogni variabile indica come il saldo reagisce a un suo aumento:
- `e_r` = cambio reale: se sale (apprezzamento reale) **perdiamo competitività** → CC peggiora **(−)**
- `Y` = reddito **interno**: se sale, importiamo di più → CC peggiora **(−)**
- `Y_w` = reddito **estero**: se sale, il resto del mondo compra di più da noi → CC migliora **(+)**

  Se CC > 0: politica espansiva (Y↑ → M↑ → CC↓); se CC < 0: politica restrittiva (Y↓ → M↓ → CC↑). **Se CC < 0, l'obiettivo esterno (BP = 0) è in conflitto con l'obiettivo interno di crescita di Y** (trade-off classico).

- **Politiche sulla competitività**: agiscono su p (politiche dei prezzi/redditi), su p_w (politiche protezionistiche, non ammesse in UE), su e (manovra del cambio: modifica della parità in cambi fissi, o pilotaggio del cambio in cambi flessibili). Se CC<0 → ↓e → ↑CC; se CC>0 → ↑e → ↓CC.

**8. Efficacia della svalutazione: la condizione di Marshall-Lerner**

- Il saldo commerciale, espresso **in valuta estera**:

```
      CC = (p_x · e) · q_x − p_m · q_m
```

**dove:**
- `p_x` = prezzo delle **esportazioni** (in valuta nazionale) · `q_x` = quantità esportate
- `p_m` = prezzo delle **importazioni** (già in valuta estera) · `q_m` = quantità importate
- `e` = tasso di cambio nominale, che converte il valore delle esportazioni in valuta estera
- Un deprezzamento del cambio (↓e) ha due effetti opposti:
  - fa **aumentare le quantità** esportate e ridurre quelle importate → CC>0 (effetto quantità)
  - **riduce il prezzo in valuta estera** delle esportazioni (`p_x · e`) → CC<0 (effetto prezzo)

- L'effetto complessivo è positivo solo se prevale l'effetto quantità, cioè se c'è sufficiente elasticità delle quantità al cambio:
```
      | ε_x | + | ε_m | > 1          ← condizione di Marshall-Lerner
```

**dove:**
- `ε_x` = **elasticità delle esportazioni** al cambio (di quanto % variano le quantità esportate per una variazione dell'1% del cambio)
- `ε_m` = **elasticità delle importazioni** al cambio
- le barre verticali `| |` indicano il **valore assoluto**: si sommano i due numeri senza guardare al segno

In parole: **la somma delle due sensibilità deve superare 1**, altrimenti l'effetto prezzo prevale su quello quantità e la svalutazione peggiora il saldo invece di migliorarlo.

**Le quattro ipotesi su cui poggia la condizione** (da citare se la domanda chiede "quando la svalutazione funziona?"):

1. **`p` e `p_w` dati e costanti** (prezzi interni ed esteri): non c'è trasferimento della variazione del cambio sui prezzi (niente *pass-through*);
2. **Nessun vincolo di offerta**: il paese è in grado di produrre di più per soddisfare la maggiore domanda estera. In **pieno impiego** l'offerta non può crescere e l'aumento della domanda estera si scarica sui **prezzi** (aggravato dal rincaro dei beni importati);
3. **Le quantità reagiscono più velocemente dei prezzi** — se non è vero, il saldo inizialmente **peggiora** (curva a J, qui sotto);
4. **Nessun effetto sulle aspettative di deprezzamento futuro**: se la svalutazione genera attese di ulteriori svalutazioni, si innesca un **deflusso di capitali** che peggiora la BP invece di migliorarla.

**La curva a J** — l'ipotesi 3 spiegata: se le quantità importate calano e quelle esportate crescono **lentamente**,

- **nel primo periodo** prevale l'effetto prezzo: la svalutazione riduce il valore in valuta estera delle esportazioni (`p_x · e`) e il saldo **peggiora**;
- **dopo un certo tempo** le quantità si adeguano e, se vale Marshall-Lerner, il saldo **migliora**.

Il saldo dei movimenti di beni disegna quindi nel tempo una **J**: prima scende, poi risale sopra il livello di partenza. È il motivo per cui gli effetti di una svalutazione **non si giudicano nel breve periodo**.

**9. Politiche commerciali: liberismo, protezionismo, autarchia**

| Politica commerciale | Definizione |
|---|---|
| **Liberismo** (*free trade*) | massima libertà di commercio, rimozione degli ostacoli a import/export; fondamento: **principio dei costi comparati** di D. Ricardo — ogni paese si specializza nel bene per cui ha un vantaggio comparato |
| **Protezionismo** | difesa della produzione interna dalla concorrenza estera |
| **Autarchia** | chiusura totale dell'economia nazionale verso l'estero |

- **Grado di apertura** dell'economia — quanto un paese commercia con l'estero rispetto a quanto produce:

```
                           X + M
      grado di apertura = ───────
                             Y
```

**dove:** `X` = esportazioni · `M` = importazioni · `Y` = PIL

**Il principio dei costi comparati con i numeri** (schema dell'esempio tipico). Il paese B ha un vantaggio **assoluto** in entrambi i beni, ma conviene comunque specializzarsi e scambiare:

| | Costo unitario in B (unità di lavoro) |
|---|---|
| Bene **x** | 10 |
| Bene **y** | 30 |

- **Ragione di scambio interna (autarchia)**: rinunciando a 1 unità di y si liberano 30 unità di lavoro = **3 unità di x** → il rapporto interno è **p_y/p_x = 3**.
- Con **60 lavoratori**, B può: (i) produrre **2 unità di y** direttamente, oppure (ii) produrre **6 unità di x** e scambiarle.
- Se i prezzi internazionali sono p_x = 30 e p_y = 50: le 6 unità di x valgono 6 · 30 = **180**, con cui si acquistano 180/50 = **3,6 unità di y** > 2. **Conviene lo scambio.**
- **Regola generale**: conviene la "produzione indiretta" se 6·p_x > 2·p_y, cioè se **p_y/p_x < 3** — se la ragione di scambio **internazionale** è minore di quella **interna**.
- **Conclusione da scrivere**: se la ragione di scambio internazionale è **compresa fra le due ragioni di scambio interne in autarchia**, l'apertura commerciale conviene **a entrambi i paesi** — anche a quello che ha il vantaggio assoluto in tutti i beni.
- Strumenti del protezionismo:
  - **Tariffario**: **dazi** (imposta sui beni importati, genera gettito fiscale)
  - **Non tariffario**: **contingenti** (limiti fisici/di valore alle importazioni), regolamentazioni, sussidi alle esportazioni, svalutazione competitiva del cambio

- **Effetti di un dazio** (prezzo internazionale invariato, ipotesi paese "piccolo"): il prezzo interno sale da `p` a `p · (1 + d)`, dove `d` è l'aliquota del dazio →
  - effetto consumo: -↓ consumo interno
  - effetto produzione: +↑ produzione interna
  - effetto importazione: ↓ importazioni
  - effetto entrate fiscali: + gettito (importazioni residue · aliquota del dazio)
  - effetto redistribuzione: consumatori pagano un prezzo più alto (trasferimento verso i produttori interni e lo Stato)

**Lettura grafica del dazio** (domanda e offerta interne, prezzo internazionale dato). Con i segmenti sull'asse delle quantità:

| | Prima del dazio (prezzo p) | Dopo il dazio (prezzo p(1+d)) |
|---|---|---|
| **Offerta interna** | OA | O**B** (aumenta) |
| **Domanda interna** | OE | O**D** (diminuisce) |
| **Importazioni** | **AE** (= domanda − offerta interna) | **BD** (ridotte) |

- Il **gettito** per lo Stato è il rettangolo: importazioni residue **BD** · dazio unitario.
- Il **dazio proibitivo** è quello che porta domanda e offerta interne a coincidere: le importazioni si azzerano (autarchia) e — punto controintuitivo da ricordare — **il gettito è nullo**, perché non c'è più nulla da tassare.

- Giustificazioni del protezionismo:
  - **Ragioni di scambio**: un dazio può spingere i produttori esteri a ridurre il prezzo al netto del dazio (*pricing to market*), migliorando la **ragione di scambio** `TT = (p_x · e) / p_m`, cioè il rapporto fra il prezzo di ciò che esportiamo e il prezzo di ciò che importiamo (più è alto, meglio è: vendiamo caro e compriamo a buon mercato). Vale però **solo se il paese non è piccolo**: serve che la sua riduzione di domanda sposti il prezzo internazionale. In tal caso il dazio è **efficace sulla ragione di scambio ma meno efficace nel proteggere la produzione interna** (il prezzo estero scende e compensa in parte il dazio)
  - **Industria nascente**: economie di scala dinamiche (*learning by doing*) — una protezione temporanea permette al paese nuovo entrante di ridurre i costi unitari fino a essere competitivo. Benefici aggiuntivi di **spillover** su altri settori; problemi: individuare i settori che diventeranno vitali, e la difficoltà **politica** di rimuovere il dazio una volta introdotto
  - **Difesa dal lavoro straniero a buon mercato** (*dumping sociale*): concorrenza di economie con salari molto più bassi. **Obiezione da conoscere**: i salari tendono a seguire la produttività, quindi le differenze in termini di **costo del lavoro per unità di prodotto** (w/q) sono molto più piccole di quelle in termini di salari

- **Attenzione**: rischio di **contromisure** — un paese protezionista può subire ritorsioni simmetriche dagli altri paesi.
- **Beggar-my-neighbour** ("impoverire il vicino"): dazi e svalutazione riducono la propensione a importare, aumentano il moltiplicatore e — se il sistema **non è in pieno impiego** — hanno effetti espansivi su reddito e occupazione. Ma lo fanno **riducendo le esportazioni del resto del mondo**: il guadagno interno è il danno altrui, da cui le ritorsioni. L'eccezione: se le politiche sono accompagnate da **politiche fiscali o monetarie espansive**, il maggior reddito interno fa risalire le importazioni e il resto del mondo non viene danneggiato.

**10. Il modello Mundell-Fleming (IS-LM-BP)**

- Estende il modello IS-LM ad un'economia aperta.
- **Obiettivo aggiuntivo**: BP=0. **Strumento aggiuntivo**: tasso di cambio.
- Aggiunge al mercato dei beni le esportazioni nette (X-M) e la condizione di equilibrio esterno BP=0.
- **Tre mercati, tre curve**:
  - Mercato dei beni → curva **IS**
  - Mercato della moneta → curva **LM**
  - Mercato estero (valutario/dei capitali) → curva **BP**

- L'equilibrio generale del sistema è dato dall'**intersezione simultanea** di IS, LM e BP nel piano (Y, i).

**Costruzione delle equazioni:**

- **IS** (mercato dei beni). Si parte da `Y = C + I + G + X − M`, con `C = c·Y`, `I = I(i)`, `M = m·Y`, `X` dato. Risolvendo per Y:

```
                 1
      Y = ───────────────  ·  [ I(i) + G + X ]
             1 − c + m
```

**dove:**
- `c` = propensione marginale al **consumo** (quanta parte di un euro in più di reddito viene consumata)
- `m` = propensione marginale a **importare** (quanta parte di un euro in più di reddito viene spesa in beni esteri)
- `1 / (1 − c + m)` = **moltiplicatore in economia aperta**: più piccolo di quello in economia chiusa `1/(1−c)`, perché una parte della domanda "esce" all'estero sotto forma di importazioni
- `I(i)` = investimenti, che dipendono **negativamente** dal tasso di interesse · `G` = spesa pubblica · `X` = esportazioni (date)
  (multiplo keynesiano ridotto dalla propensione a importare m)

- **LM** (mercato della moneta): condizione `L_d(Y, i) = M_s`, cioè **domanda di moneta = offerta di moneta**, dove `L_d` è la domanda di moneta (cresce con Y, cala con i) e `M_s` è l'offerta di moneta decisa dalla banca centrale. La LM è **crescente** nel piano (i, Y): a Y più alto serve un i più alto per tenere in equilibrio il mercato monetario, data `M_s`.

- **BP** (equilibrio con l'estero): la bilancia dei pagamenti è in pareggio quando il saldo commerciale e i movimenti di capitale si compensano.

```
      BP = CC(Y, e) + MK(i) = 0

      esplicitamente:   X(e) − m(e)·Y + MK(i) = 0
```

**dove:** `CC` = saldo di conto corrente (dipende da Y e dal cambio `e`) · `MK` = saldo dei movimenti di capitale (dipende dal tasso `i`)
  - **Curva BP inclinata positivamente**: a Y più alto (→ più importazioni, CC peggiora) serve i più alto (→ più afflusso di capitali) per mantenere BP=0.
  - **Pendenza della BP e mobilità dei capitali**:
    - se i movimenti di capitale sono **vietati** (mobilità nulla) → BP **verticale** (BP dipende solo da Y, tramite CC)
    - se la mobilità dei capitali è **crescente**, la BP diventa più **piatta**
    - in caso di **perfetta mobilità dei capitali** → BP **orizzontale**, in corrispondenza del tasso di interesse internazionale `i_w` (qualunque `i` diverso da `i_w` genera flussi di capitale infiniti)
  - Sopra la curva BP: zona di **avanzo**; sotto: zona di **disavanzo**.
  - Una **svalutazione del cambio** (↓e) sposta la BP verso il basso (più esportazioni a parità di Y) e la rende meno inclinata (minore propensione a importare in termini reali): `Y = [ X(e) + MK(i) ] / m(e)`

**11. Effetti delle politiche in cambi fissi vs flessibili (schema generale Mundell-Fleming)**

| Politica | Cambi fissi | Cambi flessibili |
|---|---|---|
| **Fiscale espansiva** | Efficace: BC deve espandere BM per difendere il cambio, rafforzando l'effetto su Y | Meno efficace/inefficace con alta mobilità dei capitali: l'afflusso di capitali (↑i) apprezza il cambio, che spiazza le esportazioni nette |
| **Monetaria espansiva** | Inefficace nel lungo periodo: ↓i causa deflusso di capitali/perdita di riserve, costringendo la BC a riassorbire liquidità per difendere la parità | Efficace: ↓i deprezza il cambio, che stimola le esportazioni nette e amplifica l'effetto espansivo su Y |

(Nota: le slide analizzate presentano gli elementi costitutivi del modello — IS, LM, BP, pendenze e meccanismi — ma non sviluppano graficamente ogni singolo caso politica/regime; la tabella sintetizza la logica standard del modello Mundell-Fleming coerente con quanto esposto su MK, competitività e riequilibrio.)

![Modello Mundell-Fleming: IS, LM e BP al variare della mobilità dei capitali](../grafici/mundell-fleming-is-lm-bp.svg)

---

## Esercizio tipo svolto

**Dati del problema:**

```
      C   = 0,7 · Y                  consumi
      I   = 600 − 400 · i            investimenti
      G   = 380                      spesa pubblica
      X   = 320                      esportazioni
      M   = 0,1 · Y                  importazioni
      L_d = 0,25 · Y + 500 − 1000 · i    domanda di moneta
```

**dove:**
- `Y` = reddito (PIL) · `i` = tasso di interesse, **in decimali** (5% si scrive 0,05)
- `0,7` = propensione al consumo `c` · `0,1` = propensione a importare `m`
- in `L_d`, la parte `0,25 · Y` è la domanda di moneta **transattiva** (dipende dal reddito), la parte `500 − 1000 · i` è quella **speculativa** (dipende dal tasso)

### 1. Equazione IS (equilibrio del mercato dei beni)

Si parte dall'equilibrio e si sostituiscono i dati:

```
      Y = C + I + G + X − M
      Y = 0,7Y + (600 − 400i) + 380 + 320 − 0,1Y
```

Si portano a sinistra tutti i termini con Y:

```
      Y − 0,7Y + 0,1Y = 1300 − 400i
      0,4 · Y         = 1300 − 400i
```

Si divide tutto per 0,4:

```
      Y = 3250 − 1000 · i          ←  equazione della curva IS
```

**Come si legge**: se il tasso di interesse sale di 1 punto (0,01), il reddito di equilibrio scende di 10 (1000 · 0,01), perché tassi più alti riducono gli investimenti.

### 2. Saldo della bilancia commerciale (CC = X − M) in funzione di i

```
      CC = X − M = 320 − 0,1 · Y
```

Sostituendo dentro l'equazione IS trovata al punto 1:

```
      CC = 320 − 0,1 · (3250 − 1000i)
      CC = 320 − 325 + 100i
      CC = 100 · i − 5             ←  saldo commerciale in funzione di i
```

**Come si legge**: il saldo commerciale **migliora al crescere del tasso di interesse**. Catena causale: `i` sale → gli investimenti calano → Y cala (via IS) → le importazioni `M = 0,1·Y` calano → CC migliora. Il saldo è in pareggio (CC = 0) quando `i = 0,05`, cioè al 5%.

### 3. Domanda di moneta transattiva in funzione di i

La componente **transattiva** di `L_d` — che qui indichiamo `L_trans` — è `0,25 · Y` (solo la parte che dipende dal reddito). Sostituendo di nuovo la IS:

```
      L_trans = 0,25 · Y = 0,25 · (3250 − 1000i)
      L_trans = 812,5 − 250 · i
```

### 4. Chiusura numerica del sistema (nota metodologica)

Per ottenere un **valore numerico unico** di Y (e quindi di `i`, di CC e della domanda di moneta) serve anche la curva **LM**, cioè la condizione:

```
      L_d = M_s
```

**dove** `M_s` è l'**offerta di moneta**, un dato che deve essere fornito dal testo d'esame (in alternativa il testo può dare direttamente il valore di `i`).

Con i soli dati di questo esercizio (la IS e la funzione `L_d`, ma **senza** `M_s`) il sistema è **sottodeterminato**: si possono esprimere Y, CC e la domanda di moneta soltanto **in funzione di i**, come fatto sopra. Non è un errore di svolgimento: è che manca un dato.

**Esempio illustrativo** — solo per mostrare il procedimento completo. Il valore di `i` qui è **ipotizzato**, e all'esame va sostituito con quello ricavato da `M_s` o fornito dal testo. Se `i` = 5% (cioè 0,05):

```
      Y = 3250 − 1000 · 0,05 = 3200
      I = 600 − 400 · 0,05   = 580

      verifica:
      Y = 0,7·(3200) + 580 + 380 + 320 − 0,1·(3200)
        = 2240 + 580 + 380 + 320 − 320
        = 3200   ✓

      CC = 100 · 0,05 − 5 = 0        (commercio in pareggio)
      L_trans = 0,25 · 3200 = 800
```

Il metodo — **ricavare l'equazione IS, poi sostituirla dentro CC e dentro la componente transattiva della domanda di moneta** — resta identico qualunque sia il valore di `i` fornito dal testo d'esame.
