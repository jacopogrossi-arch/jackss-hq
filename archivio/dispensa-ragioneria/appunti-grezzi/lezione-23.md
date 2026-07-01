# Lezione 23 — Ragioneria (Prof. Moscarini, Sapienza)

## Argomento della lezione
**Gli strumenti finanziari derivati** (OIC n. 32) — definizione, finalità (copertura/hedging vs. speculativa), rilevazione iniziale e valutazioni successive (fair value, mark to market), scritture contabili di esempio.

*Numerazione slide originale: pagine 257–261.*

---

## Concetti e definizioni chiave

### Definizione normativa
- **Art. 2426, comma 1, lett. 11-bis), c.c.**: enuncia i **criteri di valutazione** degli strumenti finanziari derivati in bilancio, **senza fornirne una definizione**.
- Al **comma 2** della stessa norma, il Legislatore rinvia, per la definizione, ai **principi contabili internazionali IAS/IFRS**.
- Il **principio contabile nazionale di riferimento è l'OIC 32**.

### Strumento finanziario e strumento finanziario derivato
- Uno **strumento finanziario** è un contratto che genera un'attività finanziaria per una società e, specularmente, una passività finanziaria per un'altra società.
- Uno strumento finanziario è definito **derivato** quando il contratto presenta le seguenti caratteristiche:
  1. richiede un **investimento iniziale minimo o irrilevante**;
  2. prevede che le prestazioni delle parti (es. imprese da un lato, banche dall'altro) siano **regolate ad una data successiva** rispetto alla sottoscrizione;
  3. ha ad oggetto il valore che assume nel tempo un determinato **elemento sottostante**, le cui variazioni di valore incidono direttamente sul **fair value** del derivato.
- Esempi di elemento sottostante: un tasso di interesse, il prezzo di strumenti finanziari, il prezzo di merci, il tasso di cambio, l'indice di prezzo o di tasso, il rating di credito o indice di credito, altra variabile.
- **Fair value**: il prezzo che si percepirebbe per la vendita di un'attività ovvero che si pagherebbe per il trasferimento di una passività in una regolare operazione tra operatori di mercato alla data di valutazione.

### Finalità dei derivati
Le imprese sottoscrivono contratti derivati con le banche principalmente per due finalità:
a) **coprirsi da specifici rischi di natura finanziaria** (finalità di copertura o *hedging*);
b) **assumere volontariamente esposizioni al rischio** per conseguire un profitto (**finalità speculativa**).

Nell'ambito della copertura (sub a), si distinguono due tipologie:
- a1) derivati di **copertura dalla variazione dei flussi finanziari**
- a2) derivati di **copertura dalla variazione di fair value**

*Nota della lezione*: in genere sono le **banche stesse** a proporre alle imprese di sottoscrivere contratti derivati.

### Esempio di derivato di copertura — Interest Rate Cap
Un'impresa, in data 30 gennaio, ottiene dalla banca un finanziamento di **1 milione di euro**, da rimborsare in 5 anni con rate trimestrali a tasso variabile pari all'**Euribor 3 mesi** (3% al momento della stipula) **+ spread 1%**. L'impresa decide di tutelarsi da eventuali rialzi futuri dell'Euribor, sottoscrivendo un contratto derivato di copertura:
- acquista a un prezzo di **10.000 euro** un contratto derivato di durata pari al finanziamento (5 anni), che prevede il pagamento di interessi da parte della banca all'impresa se l'Euribor supera un certo valore fissato al **3,5% (cap rate)**.
- In data 30 aprile, l'impresa paga la rata prevista, pagando un interesse complessivo del **5%** (Euribor 4% + spread 1%).
- Avendo l'Euribor superato il cap rate, la banca accredita un **"differenziale" dello 0,5%** (Euribor 4% al netto del cap rate 3,5%).
- L'interesse **complessivamente pagato** dall'impresa nel trimestre è pari al **4,5%** (5% al netto del differenziale 0,5% ricevuto grazie alla copertura).

---

## Schemi / regole di rilevazione e valutazione

### Rilevazione iniziale e valutazioni successive
- La **rilevazione iniziale** concerne la registrazione in contabilità del costo pagato in fase di sottoscrizione del contratto derivato. È fondamentale qualificare sin da subito la tipologia di derivato (copertura o speculativo).
- Al termine di ogni esercizio (31.12.n), gli amministratori devono valutare i derivati al loro **fair value**. La banca invia all'impresa (in genere tra gennaio e marzo n+1) un documento con il **fair value** del derivato al 31.12.n (c.d. **mark to market – MTM**).
- Il fair value al 31.12 va confrontato con il valore della rilevazione iniziale. La **differenza positiva o negativa** va imputata **al patrimonio netto o al conto economico**, a seconda della tipologia di derivato.

**Tabella riassuntiva — modalità di contabilizzazione:**

| Tipologia di derivati | Derivati di copertura dei flussi finanziari | Derivati di copertura dalla variazione di fair value; Derivati speculativi |
|---|---|---|
| **Modalità di contabilizzazione** | Cash flow hedge | Fair value hedge |
| **Riclassifica di bilancio** | Patrimonio Netto | Conto Economico |
| In caso di **variazione positiva** | (ad incremento) voce VII - Riserva per operazioni di copertura dei flussi finanziari attesi | (componente positivo) Voce D.18.d – rivalutazioni di strumenti finanziari derivati |
| In caso di **variazione negativa** | (a decremento) voce VII - Riserva per operazioni di copertura dei flussi finanziari attesi* | (componente negativo) Voce D.19.d – svalutazioni di strumenti finanziari derivati |

*\* in caso di decremento, il valore della Riserva può assumere anche valori negativi, riducendo l'ammontare complessivo del Patrimonio Netto.*

### Riclassifica in stato patrimoniale
- La voce **"Strumenti finanziari derivati attivi"** va riclassificata nella voce **C.III.5 dell'Attivo Circolante** (Attività finanziarie che non costituiscono immobilizzazioni) se concerne:
  - un derivato di copertura avente come sottostante una **passività** (es. debito);
  - un derivato di copertura avente come sottostante un'**attività finanziaria dell'Attivo Circolante**;
  - un **derivato speculativo**.
- Se invece concerne un derivato di copertura avente come sottostante un'**immobilizzazione finanziaria**, va riclassificato nella voce **B.III.4 (Immobilizzazioni finanziarie)**.
- La voce **"Strumenti derivati passivi"**, che origina in caso di fair value negativo, va riclassificata nella voce **B.3 del Passivo di Stato Patrimoniale** (Fondi rischi e oneri), in quanto il valore negativo rappresenta una **passività potenziale** (in caso di cessione a terzi genererebbe una minusvalenza).
- In caso di fair value **positivo**, si tratta di un'attività potenzialmente cedibile a terzi che genererebbe una **plusvalenza**.

### Effetti fiscali sulla Riserva di copertura
- Nel caso di fair value **positivo**, si generano **imposte anticipate**; nel caso di fair value **negativo**, si generano **imposte differite**.
- L'**OIC 32, punto 29**, specifica che la Riserva per operazioni di copertura dei flussi finanziari va indicata **"al netto degli effetti fiscali differiti"**.
  - Fair value positivo: `Riserva  a  Fondo imposte differite`
  - Fair value negativo: `Crediti per imposte anticipate  a  Riserva`

---

## Riferimenti normativi

- **Art. 2426, comma 1, lett. 11-bis), c.c.**: criteri di valutazione degli strumenti finanziari derivati
- **Art. 2426, comma 2, c.c.**: rinvio ai principi contabili internazionali IAS/IFRS per la definizione
- **OIC 32**: principio contabile nazionale sugli strumenti finanziari derivati (incluso il punto 29 sugli effetti fiscali della riserva di copertura)

---

## Scritture contabili di esempio

### Esempio 1 — Derivato di copertura dei flussi attesi con variazione di fair value POSITIVA
La Società Alfa S.r.l., il 15 aprile 2023, sottoscrive un derivato di copertura dei flussi finanziari al prezzo di **10.000 euro** (fair value iniziale). A febbraio 2024 la banca comunica che il MTM al 31.12.2023 è pari a **12.000 euro**.

```
15/04/2023
Strumenti finanziari derivati attivi   a   Riserva per operazioni di copertura dei flussi finanziari    10.000

31/12/2023
Strumenti finanziari derivati attivi   a   Riserva per operazioni di copertura dei flussi finanziari     2.000
```

### Esempio 2 — Derivato di copertura dei flussi attesi con variazione di fair value NEGATIVA
La Società Alfa S.r.l., il 20 maggio 2023, sottoscrive un derivato di copertura al prezzo di **13.000 euro**. A gennaio 2024 la banca comunica che il MTM al 31.12.2023 è pari a **9.000 euro**.

```
20/05/2023
Strumenti finanziari derivati attivi                        a   Riserva per operazioni di copertura dei flussi finanziari   13.000

31/12/2023
Riserva per operazioni di copertura dei flussi finanziari attesi   a   Strumenti derivati attivi                              4.000
```

### Esempio 3 — Derivato di copertura con variazione di fair value negativa SUPERIORE al valore iniziale
La Società Alfa S.r.l., il 16 giugno 2023, sottoscrive un derivato di copertura dei flussi finanziari al prezzo di **2.000 euro** (fair value iniziale). A marzo 2024 la banca comunica che il MTM al 31.12.2023 è **negativo, pari a 1.000 euro**.

```
16/06/2023
Strumenti finanziari derivati attivi                              a   Riserva per operazioni di copertura dei flussi finanziari attesi   2.000

31/12/2023
Riserva per operazioni di copertura dei flussi finanziari attesi   a   Diversi                                                                3.000
                                                                        Strumenti finanziari derivati attivi        2.000
                                                                        Strumenti finanziari derivati passivi       1.000
```

Il saldo finale della Riserva è **negativo e pari a 1.000 euro**, e andrà in diminuzione del Patrimonio Netto al 31.12.2023.

La voce "Strumenti derivati passivi" (1.000) va riclassificata nella voce **B.3 del Passivo** (Fondi rischi e oneri), in quanto rappresenta una passività potenziale (in caso di cessione a terzi, genererebbe una minusvalenza di 1.000 euro).
