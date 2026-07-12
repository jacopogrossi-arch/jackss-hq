# Soluzione — Esercizio "Palazzine" (Esercizi 2.pdf)

Svolgimento dell'esercizio sulla commessa delle due palazzine del file `Esercizi 2.pdf` (Downloads/Universita/Ragioneria): **lavori in corso su ordinazione (LIC)** con il **metodo della percentuale di completamento**.

---

## Dati

La società Alfa costruisce **2 palazzine identiche (A e B)** in 2 anni.

| Budget | Palazzina A | Palazzina B | Totale |
|---|---|---|---|
| Ricavi | 200 | 200 | **400** |
| Costi | 160 | 160 | **320** |
| Utile | 40 | 40 | **80** |

- Fine anno 1: completata la palazzina A (costi 160 come da budget) → **50% dei lavori**. Incassato **anticipo = 50% dei ricavi totali = 200**.
- Fine anno 2: completata la palazzina B (costi 160), consegna e incasso del **saldo = 200**.

## Il punto dell'esercizio

La domanda vera è: **in quale anno va l'utile di 80?** L'incasso non c'entra: l'anticipo di 200 **non è un ricavo** ma un **debito verso il committente** (voce "Anticipi" del passivo — gli devo ancora la palazzina B). Con la percentuale di completamento l'utile matura man mano che si lavora: **40 nell'anno 1 e 40 nell'anno 2**.

Il meccanismo contabile: siccome la commessa non è ancora consegnata, il ricavo maturato dell'anno 1 entra in conto economico **tramite le rimanenze**. I LIC si valutano **al corrispettivo maturato, non al costo** — è l'unica rimanenza valutata sopra il costo, ed è così che l'utile emerge nell'anno 1.

**Percentuale di completamento** = costi sostenuti / costi totali = 160/320 = **50%**
**Corrispettivo maturato** = 50% × 400 = **200** → valore dei LIC al 31/12/X1.

---

## Anno 1

### Conto economico anno 1

| Voce | Importo |
|---|---|
| Costi dell'esercizio | (160) |
| Variazione rimanenze **finali** LIC | +200 |
| **Utile** | **40** |

### Stato patrimoniale 31/12/X1

| Attivo | | Passivo | |
|---|---|---|---|
| Banca c/c | 40 | Anticipi | 200 |
| Lavori in corso di ordinazione | 200 | Utile | 40 |
| **Totale** | **240** | **Totale** | **240** |

Banca = 200 di anticipo incassato − 160 di costi pagati = **40**. L'utile di 40 emerge anche se non si è "venduto" nulla: è la competenza economica.

---

## Anno 2

La commessa è completata e consegnata: si rileva il **ricavo intero di 400** e si scaricano le rimanenze iniziali con variazione **negativa** di 200 (per non contare due volte la parte già maturata nell'anno 1).

### Conto economico anno 2

| Voce | Importo |
|---|---|
| Ricavi dell'esercizio | 400 |
| Variazione rimanenze **iniziali** LIC | (200) |
| Costi dell'esercizio | (160) |
| **Utile** | **40** |

Ricavo di competenza dell'anno 2 = 400 − 200 = 200; meno costi 160 → utile **40**. ✓

### Stato patrimoniale 31/12/X2

| Attivo | | Passivo | |
|---|---|---|---|
| Banca c/c | 80 | Anticipi | 0 |
| Lavori in corso di ordinazione | 0 | Utili (X1 + X2) | 80 |
| **Totale** | **80** | **Totale** | **80** |

Banca = 40 (da X1) + 200 di saldo − 160 di costi = **80** = utile totale della commessa, tutto incassato. Gli anticipi si chiudono contro il ricavo, i LIC spariscono con la consegna.

---

## I 3 errori classici che l'esercizio vuole smascherare

1. **Mettere l'anticipo tra i ricavi dell'anno 1** — no: è un debito (passivo, voce "Anticipi").
2. **Valutare i LIC al costo (160) invece che al corrispettivo maturato (200)** — la valutazione al corrispettivo è l'eccezione alla regola del costo per le rimanenze, ed è ciò che ripartisce l'utile 40/40.
3. **Confondere con il metodo della commessa completata** — lì i LIC stanno al costo (160), l'anno 1 chiude a utile 0 e tutto l'utile di 80 finisce nell'anno 2. La percentuale di completamento rappresenta meglio la competenza economica ed è ammessa (OIC 23) quando la commessa è pluriennale, il contratto è vincolante e i corrispettivi/costi sono stimabili in modo attendibile.
