# La valutazione dei progetti pubblici e l'analisi costi-benefici

**Domande d'esame collegate:** Calcolo del VAN (assoluto e relativo) di due progetti alternativi e scelta motivata · Calcolo del TIR e criterio di ammissibilità · "Che cosa sono i prezzi ombra e perché si usano?" · Differenze fra calcolo sociale e calcolo privato · Le fasi della scelta di un progetto pubblico · Come si valutano i beni non scambiati sul mercato

> **Nota sulle fonti.** Interamente dalle slide della professoressa (cap. 1, "La valutazione dei progetti pubblici" e "L'analisi costi-benefici"). È un argomento **da esercizio numerico**: la parte teorica serve, ma la domanda tipica è un calcolo.

---

## **1. Il problema: quali progetti finanziare**

- Prima di intervenire, i policy maker devono **valutare i potenziali progetti pubblici**: investimenti, nuovi servizi, regolamentazione.
- Questi progetti comportano **benefici e costi non solo finanziari**, e devono tener conto di **tutti gli effetti sulla collettività** (non solo di quelli che passano per il bilancio pubblico).
- Data la **scarsità delle risorse**, occorre decidere quali finanziare e in quale ordine.

## **2. Le cinque fasi della scelta**

Sono le stesse fasi di un imprenditore privato, ma con contenuti diversi (vedi §5):

1. **Individuazione delle alternative** — incluso lo **status quo** (non fare nulla è sempre un'alternativa da valutare).
2. **Individuazione delle conseguenze** di ogni progetto in **termini fisici** (quantità di input e output) e **per ogni periodo futuro**.
3. **Valutazione di costi e benefici** in termini monetari.
4. **Attualizzazione** di costi e benefici (renderli confrontabili riportandoli a oggi).
5. **Calcolo del tasso di rendimento atteso** → si sceglie il progetto con il rendimento più alto.

## **3. L'analisi costi-benefici (ACB): il VAN**

**Notazione:**

| Simbolo | Significato |
|---|---|
| **b_t** | Beneficio del progetto al tempo t |
| **c_t** | Costo del progetto al tempo t |
| **i** | **Tasso di sconto sociale** |
| **1/(1+i)** | **Fattore di sconto sociale** (per t periodi: 1/(1+i)^t) |

**Le formule:**

- **B = Σ₀ⁿ [ b_t / (1+i)^t ]** → somma dei valori attuali dei **benefici**
- **C = Σ₀ⁿ [ c_t / (1+i)^t ]** → somma dei valori attuali dei **costi**
- **VAN = B − C** → **valore attuale netto assoluto**
- **VAN_r = (B − C) / C** → **valore attuale netto relativo**

**I due criteri:**

- **Criterio di ammissibilità**: sono ammissibili i progetti con **VAN > 0**.
- **Criterio di scelta**: fra i progetti ammissibili si sceglie quello con il **VAN più alto**.

**Due avvertenze che valgono punti all'esame:**

1. Il **VAN relativo** serve a **neutralizzare l'effetto dimensione**: un progetto grande ha quasi sempre un VAN assoluto più alto, ma non è detto che renda di più per euro speso. Se il VAN assoluto è positivo lo è anche quello relativo, **ma la graduatoria dei progetti secondo i due criteri può essere diversa** (lo si vede nell'esercizio).
2. Il valore del VAN **dipende dal tasso di sconto adottato**: cambiando i, il segno e l'ordine dei progetti possono cambiare.

## **4. Il tasso interno di rendimento (TIR)**

**Definizione**: il TIR è il valore di **i** che rende **B − C = 0**, cioè che annulla il VAN:

**Σ₀ⁿ [ b_t/(1+i)^t ] − Σ₀ⁿ [ c_t/(1+i)^t ] = 0**

È quindi il tasso al quale benefici e costi attualizzati del progetto **si equivalgono**: il "rendimento interno" del progetto.

- **Criterio di ammissibilità**: **TIR > tasso di interesse di mercato** (o del tasso di sconto sociale) → il progetto conviene rispetto agli investimenti alternativi.
- **Criterio di scelta**: il progetto con il **TIR più alto**.

**Relazione fra VAN e TIR** (utile per controllarsi negli esercizi): se il TIR è maggiore del tasso di sconto usato, il VAN calcolato a quel tasso è **positivo**; se è minore, è **negativo**. Se sono uguali, il VAN è zero.

## **5. Calcolo sociale e calcolo privato: le tre differenze**

Il policy maker deve tener conto di ciò che l'imprenditore privato ignora:

| Differenza | Contenuto |
|---|---|
| **Effetti diretti e indiretti** | In particolare le **esternalità** (positive e negative) prodotte dal progetto. Esempio della metropolitana: effetti **diretti** = acquisto di cemento, ferro, lavoro (input) e maggiore disponibilità di trasporto (output); effetti **indiretti** = riduzione del traffico di superficie e della congestione in altri mercati |
| **Costi e benefici incommensurabili e intangibili** | Non esistono prezzi di mercato per qualità della vita, salute, ambiente |
| **Effetti distorsivi** | Il progetto stesso può modificare l'offerta e quindi i prezzi |

## **6. I prezzi ombra**

**Perché servono**: i prezzi di mercato spesso **non sono affidabili** per valutare costi e benefici, per tre ragioni:

- sono **influenzati dal progetto stesso**, se di grandi dimensioni;
- i mercati possono essere **distorti** (es. in monopolio, dove P > MC);
- possono essere influenzati dalla **distribuzione dei redditi**.

**Definizione**: il **prezzo ombra** (o sociale) esprime il **costo-opportunità**, cioè il valore del prodotto ottenibile impiegando le risorse in progetti alternativi ai quali si rinuncia per realizzare quello in esame.

- I prezzi ombra corrispondono ai prezzi che si formerebbero in **mercati di concorrenza perfetta e completi** — quelli che rilevano correttamente la scarsità.
- Analogamente, il **tasso di sconto sociale** può differire da quello di mercato: per esempio, uno Stato che tiene conto delle **generazioni future** adotterà un tasso più basso, dando più peso ai benefici lontani nel tempo.

**In sintesi, l'ACB si distingue dall'analisi di redditività privata per due ragioni:**

1. include fra costi e benefici anche quelli che ricadono su **soggetti diversi** da chi realizza il progetto (esternalità);
2. valuta i costi come **costo-opportunità**, usando **prezzi ombra** al posto dei prezzi di mercato (e un tasso di sconto "ombra" per l'attualizzazione).

## **7. I beni non scambiati sul mercato** *(integrazione dal manuale)*

Alcuni beni non hanno prezzo e vanno comunque valutati:

| Bene | Metodo di valutazione |
|---|---|
| **Valore della vita umana** | **QALY** (*Quality-Adjusted Life Years*): indice che pondera l'aspettativa di vita per la qualità (mobilità, assenza di dolore). In alternativa, dal mercato del lavoro: **flusso attualizzato dei redditi futuri** persi, oppure **preferenze rivelate** |
| **Danno ambientale** | Costo da sostenere per riportare la situazione allo stato pre-intervento (metodologia **V.I.A.**, valutazione di impatto ambientale) |
| **Tempo libero** | Costo-opportunità del tempo sottratto |
| **Effetti redistributivi** | Rientrano come questione di **equità**, non riducibile a un prezzo |

**L'esempio delle preferenze rivelate**: dall'altra parte della strada c'è una borsa con 1 milione di euro; attraversare comporta l'1% di probabilità di essere investiti e morire. Se accettate il rischio, **per voi stessi la vostra vita non vale più di 100 milioni** (1 milione ÷ 0,01). Il metodo mostra sia la logica sia il suo limite etico: chi ha il diritto di esprimere quel giudizio, e vale per tutti allo stesso modo?

---

## **Esercizio tipo svolto**

**Testo.** Un comune deve scegliere tra due progetti alternativi. Il **tasso di sconto sociale è i = 5%**. I flussi (in migliaia di euro) sono:

| Progetto | c₀ (costo, t=0) | b₁ (beneficio, t=1) | b₂ (beneficio, t=2) |
|---|---|---|---|
| **A** — linea tranviaria | 1.000 | 550 | 605 |
| **B** — rete ciclabile | 300 | 180 | 180 |

Si chiede di: (a) calcolare B, C e il **VAN assoluto** dei due progetti; (b) calcolare il **VAN relativo**; (c) calcolare il **TIR** di entrambi; (d) scegliere motivando, e verificare che cosa succede se il tasso di sconto sale al 12%.

---

### **(a) Valore attuale netto assoluto**

Il costo è **tutto al tempo 0**, quindi non va attualizzato: C = c₀.

**Progetto A**
B = 550/1,05 + 605/(1,05)² = 550/1,05 + 605/1,1025 = 523,81 + 548,75 = **1.072,56**
C = **1.000**
**VAN_A = 1.072,56 − 1.000 = +72,56**

**Progetto B**
B = 180/1,05 + 180/1,1025 = 171,43 + 163,27 = **334,69**
C = **300**
**VAN_B = 334,69 − 300 = +34,69**

Entrambi sono **ammissibili** (VAN > 0). Sul criterio del VAN assoluto **vince A**.

### **(b) Valore attuale netto relativo**

VAN_r = (B − C)/C

- **A**: 72,56 / 1.000 = 0,0726 → **7,26%**
- **B**: 34,69 / 300 = 0,1156 → **11,56%**

**Sul criterio del VAN relativo vince B.** È esattamente il caso in cui **le due graduatorie divergono**: A produce più valore in assoluto, ma B ne produce di più **per ogni euro investito**. Con risorse illimitate si sceglie A; con un vincolo di bilancio stringente (o potendo replicare B più volte) conviene B.

### **(c) Tasso interno di rendimento**

Si pone VAN = 0 e si risolve in i. Con due periodi si ottiene un'equazione di secondo grado: posto **y = 1 + i**,

**Progetto A**: 1.000·y² = 550·y + 605 → 1.000y² − 550y − 605 = 0 → 200y² − 110y − 121 = 0
y = [110 ± √(110² + 4·200·121)] / (2·200) = [110 ± √(12.100 + 96.800)] / 400 = [110 ± 330] / 400
y = 440/400 = **1,10** → **TIR_A = 10%**

*(verifica: 550/1,10 = 500 e 605/1,21 = 500, somma 1.000 = C ✓ il VAN si annulla esattamente)*

**Progetto B**: 300·y² = 180·y + 180 → 5y² − 3y − 3 = 0
y = [3 ± √(9 + 60)] / 10 = [3 ± 8,307] / 10 = **1,1307** → **TIR_B ≈ 13,1%**

Entrambi ammissibili (TIR > i = 5%); **sul criterio del TIR vince B**, coerentemente con il VAN relativo.

### **(d) Che cosa cambia con i = 12%**

**A**: B = 550/1,12 + 605/1,2544 = 491,07 + 482,30 = 973,37 → **VAN_A = −26,63 < 0 → non ammissibile**
**B**: B = 180/1,12 + 180/1,2544 = 160,71 + 143,49 = 304,21 → **VAN_B = +4,21 > 0 → ammissibile**

**Commento finale.** Il risultato conferma i due punti teorici del §3-4:

- il **VAN dipende dal tasso di sconto**: alzandolo, i benefici futuri pesano meno e A — che ha i benefici più lontani e un costo iniziale più alto — diventa non conveniente, mentre B resiste;
- il segno del VAN è **coerente con il TIR**: A ha TIR 10% < 12% → VAN negativo; B ha TIR 13,1% > 12% → VAN positivo. Il confronto fra TIR e tasso di sconto dice il segno del VAN **senza doverlo ricalcolare**.

**Da dire sempre nel commento**: la scelta finale non è solo aritmetica. Vanno considerati gli **effetti indiretti** (decongestione, inquinamento evitato), i **benefici intangibili** (salute, qualità della vita) e gli **effetti redistributivi** — e se i prezzi usati non riflettono i valori sociali, l'intero calcolo andrebbe rifatto con i **prezzi ombra**.
