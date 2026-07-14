# GUIDA OPERATIVA — Rendiconto Finanziario (OIC 10, metodo indiretto)

> Creata il 14/07/2026 per l'esame del 16/07. **Metodo passo-passo per risolvere l'esercizio d'esame** (stile Simulazione 2.4), con regole dei segni, esempio guidato, errori tipici e **un esercizio nuovo con soluzione in fondo**.

---

## 1. Il minimo di teoria che serve all'esercizio

- Obbligatorio dal **D.Lgs. 139/2015**; il codice fissa solo l'obiettivo (**art. 2425-ter**), forma e contenuto sono nell'**OIC 10**. Esonerati: abbreviato e micro.
- Misura la **variazione delle disponibilità liquide** (cassa + banca) dell'esercizio, spiegandola con tre aree: **A) operativa, B) investimento, C) finanziamento**.
- **Metodo indiretto** (quello chiesto all'esame): si parte dall'**utile** e lo si rettifica. Il metodo diretto parte invece da incassi/pagamenti effettivi.
- Verifica finale sempre: **A + B + C = Δ disponibilità liquide = liquidità finale − liquidità iniziale.**

## 2. Lo schema da compilare (versione d'esame)

```
A) FLUSSO DELL'ATTIVITÀ OPERATIVA (metodo indiretto)
   Utile (perdita) dell'esercizio
   + Ammortamenti, accantonamenti, svalutazioni      (costi NON monetari)
   ± Plusvalenze (−) / minusvalenze (+) da cessioni   (le sposto nell'area B)
   − Incremento crediti commerciali    (+ se decremento)
   − Incremento rimanenze              (+ se decremento)
   + Incremento debiti v/fornitori     (− se decremento)
   = FLUSSO OPERATIVO (FCO)

B) FLUSSO DELL'ATTIVITÀ DI INVESTIMENTO
   − Acquisti di immobilizzazioni (materiali, immateriali, finanziarie)
   + Prezzo incassato da cessioni di immobilizzazioni
   = FLUSSO DA INVESTIMENTI

C) FLUSSO DELL'ATTIVITÀ DI FINANZIAMENTO
   + Accensione mutui/finanziamenti      − Rimborso quote capitale
   + Aumenti di capitale a pagamento     − Dividendi pagati
   = FLUSSO DA FINANZIAMENTI

A + B + C = VARIAZIONE DELLE DISPONIBILITÀ LIQUIDE
```

La formula compatta del FCO (derivazione vista a lezione 9):

**FCO = Utile + Amm/Acc/Sval − ΔCCN**, dove **ΔCCN = Δcrediti + Δrimanenze − Δdebiti commerciali**

## 3. Le regole dei segni (il cuore dell'esercizio)

| Voce del testo | Area | Segno | Perché |
|---|---|---|---|
| Utile d'esercizio | A | + | Punto di partenza |
| Ammortamenti / accantonamenti / svalutazioni | A | **+** | Costi che NON escono di cassa: li riaggiungo |
| **Incremento** crediti v/clienti | A | **−** | Ho fatturato ma non incassato |
| **Decremento** crediti v/clienti | A | + | Ho incassato vecchi crediti |
| **Incremento** rimanenze | A | **−** | Ho comprato/prodotto merce pagandola, non venduta |
| **Decremento** rimanenze | A | + | Ho venduto magazzino senza ricomprarlo |
| **Incremento** debiti v/fornitori | A | **+** | Ho comprato senza ancora pagare |
| **Decremento** debiti v/fornitori | A | − | Ho pagato vecchi debiti |
| Interessi pagati / imposte pagate | A | − | OIC 10: stanno nell'operativa |
| Dividendi **incassati** | A | + | Operativa |
| Acquisto impianti/partecipazioni per cassa | B | − | Uscita da investimento |
| Prezzo di cessione di cespiti incassato | B | + | Entrata da disinvestimento (prezzo pieno, non plusvalenza) |
| Accensione mutuo | C | + | Nuovo capitale di debito |
| Rimborso **quota capitale** mutuo | C | − | (la quota interessi va in A!) |
| Aumento di capitale sottoscritto e versato | C | + | Capitale di rischio |
| Dividendi **pagati** | C | − | Remunerazione del capitale di rischio |

**Trucco per non sbagliare il segno sul circolante:** chiediti sempre "questa variazione ha messo soldi in tasca o li ha tolti?" — se l'**attivo** circolante cresce, la cassa **scende** (segno −); se il **passivo** cresce, la cassa **sale** (segno +).

## 4. Procedura in 5 passi

1. **Scrivi lo scheletro A / B / C** su carta, subito.
2. **Classifica ogni dato del testo** in un'area (matita: O, I, F accanto a ogni numero). Attenzione alle trappole: rata mutuo = quota capitale (C) + interessi (A); cessione cespite = prezzo incassato in B.
3. **Compila A**: utile → + ammortamenti → ± variazioni di circolante con la tabella dei segni.
4. **Compila B e C** (di solito 2-3 voci ciascuna).
5. **Somma e verifica**: A+B+C deve coincidere con la Δ liquidità se il testo dà cassa iniziale e finale. Se non torna, hai quasi sicuramente sbagliato **un segno** sul circolante.

## 5. Esempio guidato (Simulazione 2.4, Theta S.p.A.)

Dati: utile 100 · ammortamenti 50 · **incremento** crediti 30 · **decremento** rimanenze 10 · **incremento** debiti v/fornitori 20 · acquisto impianti per cassa 80 · rimborso quota capitale mutuo 40 · dividendi pagati 20.

| | Calcolo | Importo |
|---|---|---|
| **A) Operativa** | 100 + 50 − 30 + 10 + 20 | **+150** |
| **B) Investimento** | − 80 | **−80** |
| **C) Finanziamento** | − 40 − 20 | **−60** |
| **Δ disponibilità liquide** | 150 − 80 − 60 | **+10** |

Lettura (chiesta spesso come commento): la gestione operativa genera 150 di cassa, sufficienti a coprire integralmente investimenti (80) e rimborsi/dividendi (60), con un residuo di +10 che incrementa la liquidità. Situazione **equilibrata e autofinanziata**.

## 6. Errori tipici (quelli che costano mezza risposta)

1. **Segno invertito sulle variazioni di circolante** → usa sempre la domanda "cassa in tasca o fuori?".
2. **Dimenticare che gli ammortamenti si sommano** (non si sottraggono: sono già dentro l'utile come costo).
3. **Mettere i dividendi pagati in A** → vanno in **C** (i dividendi *incassati* invece stanno in A).
4. **Mettere l'intera rata del mutuo in C** → solo la **quota capitale**; gli interessi restano in A.
5. **Mettere la plusvalenza in B** → in B va il **prezzo incassato**; la plusvalenza va *tolta* da A (è dentro l'utile ma non è flusso operativo).
6. **Non fare la verifica finale** A+B+C = Δ liquidità.

---
---

# ESERCIZIO NUOVO — Società Sigma S.p.A. (da fare a tempo: 20 minuti, senza guardare sopra)

Dai bilanci della Sigma S.p.A. al 31/12/n risultano i seguenti dati:

- utile d'esercizio **80**
- ammortamenti **60**
- accantonamento a fondo rischi per cause legali **10**
- **decremento** crediti commerciali **15**
- **incremento** rimanenze **25**
- **decremento** debiti verso fornitori **20**
- acquisto di un macchinario pagato per banca **120**
- cessione di un terreno: **prezzo incassato 50** (valore contabile 40, plusvalenza 10)
- accensione di un nuovo mutuo **70**
- rimborso quota capitale di vecchi finanziamenti **30**
- aumento di capitale a pagamento sottoscritto e versato **40**
- dividendi pagati ai soci **25**
- disponibilità liquide iniziali **35**

**a)** Compilare il rendiconto finanziario (metodo indiretto) nelle aree A, B, C e determinare la variazione delle disponibilità liquide e la liquidità finale.
**b)** Commentare in 2 righe la situazione finanziaria della società.

**Domande a risposta multipla:**

1. Il flusso dell'attività operativa è pari a:
   1) 120  2) 110  3) 100  4) Nessuna delle precedenti

2. La plusvalenza di 10 sulla cessione del terreno:
   1) si somma nell'area A  2) si sottrae nell'area A (il prezzo pieno 50 va in B)  3) va in area C  4) non entra nel rendiconto

3. L'aumento di capitale a pagamento si classifica:
   1) nell'attività operativa  2) di investimento  3) di finanziamento  4) fuori dal rendiconto

---
---

# SOLUZIONE (guardare solo dopo aver provato!)

### a) Rendiconto

**A) Attività operativa:**

| Voce | Importo |
|---|---|
| Utile d'esercizio | +80 |
| Ammortamenti | +60 |
| Accantonamento fondo rischi | +10 |
| **Plusvalenza cessione terreno** (rettifica: il flusso vero sta in B) | **−10** |
| Decremento crediti commerciali | +15 |
| Incremento rimanenze | −25 |
| Decremento debiti v/fornitori | −20 |
| **Flusso operativo (A)** | **+110** |

**B) Attività di investimento:**

| Voce | Importo |
|---|---|
| Acquisto macchinario | −120 |
| Prezzo incassato dalla cessione del terreno | +50 |
| **Flusso da investimenti (B)** | **−70** |

**C) Attività di finanziamento:**

| Voce | Importo |
|---|---|
| Accensione nuovo mutuo | +70 |
| Rimborso quota capitale finanziamenti | −30 |
| Aumento di capitale a pagamento | +40 |
| Dividendi pagati | −25 |
| **Flusso da finanziamenti (C)** | **+55** |

**Δ disponibilità liquide = 110 − 70 + 55 = +95** → **liquidità finale = 35 + 95 = 130.**

### b) Commento

La gestione operativa genera un flusso ampiamente positivo (110) che copre da solo gli investimenti netti (70). I flussi di finanziamento (+55: mutuo e aumento di capitale superano rimborsi e dividendi) si aggiungono, portando la liquidità da 35 a 130: la società si sta dotando di risorse, presumibilmente in vista di ulteriori investimenti.

### Risposta multiple

1. → **2) 110** (attento alla rettifica della plusvalenza: 80+60+10−10+15−25−20).
2. → **2)** la plusvalenza si **sottrae** in A e in B entra il **prezzo pieno di 50** — altrimenti conteresti 10 due volte.
3. → **3)** finanziamento (capitale di rischio, come i dividendi pagati).

### Nota sui due punti più insidiosi di questo esercizio

- **Accantonamento a fondo rischi (+10 in A):** come gli ammortamenti, è un costo che non muove cassa quest'anno → si riaggiunge.
- **Cessione del terreno:** dentro l'utile c'è la plusvalenza di 10, ma la cassa vera entrata è 50 e appartiene all'area investimenti. Quindi: −10 in A, +50 in B. Effetto netto totale +40? No: +50 di cassa (il valore contabile 40 non era mai stato un flusso).
