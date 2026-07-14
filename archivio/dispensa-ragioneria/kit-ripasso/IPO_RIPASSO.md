# IPO / OPVS — Scheda di revisione + svolgimento esercizio Alfa S.p.A.

> Creato il 14/07/2026 per l'esame del 16/07. Prima la **scheda-metodo** (teoria + procedura), poi lo **svolgimento completo dell'esercizio ufficiale del corso** (IPO di Alfa S.p.A.), il cui PDF contiene solo la traccia.
>
> ⚠️ **Lo svolgimento numerico è mio, non del docente** (non esiste un soluzionario nel materiale): il procedimento segue le regole standard del codice civile (artt. 2438 ss., 2431), ma i valori vanno presi come riferimento ragionato, non come soluzione ufficiale.

---

## 1. Scheda-metodo

### Il vocabolario dell'IPO (la parte descrittiva)

- **IPO (Initial Public Offering)**: la quotazione in borsa di una società. Può combinare due componenti:
  - **OPS (Offerta Pubblica di Sottoscrizione)**: il mercato sottoscrive **azioni di nuova emissione** → aumento di capitale a pagamento → **soldi freschi alla società**.
  - **OPV (Offerta Pubblica di Vendita)**: un socio esistente **vende azioni già emesse** → i soldi vanno **al socio**, non alla società.
  - Insieme = **OPVS (Offerta Pubblica di Vendita e Sottoscrizione)** — è il caso dell'esercizio.
- **Advisor / banca d'affari** (es. Rothschild): stima il **valore intrinseco** (valore corrente/di mercato) della società e propone il **prezzo per azione** da offrire al mercato.
- **Roadshow**: incontri pre-IPO tra AD, CFO e advisor con gli **investitori istituzionali** per presentare l'azienda.
- **Flottante**: le azioni in mano al mercato dopo la quotazione (qui: nuove azioni sottoscritte + azioni vendute dal socio uscente).
- **Liquidity event**: l'uscita di un socio dall'investimento tramite cessione delle azioni, con eventuale **plusvalenza** rispetto al valore di carico.

### Le tre regole contabili chiave

1. **Plusvalenza del socio venditore** = prezzo di cessione − **valore di carico** della partecipazione (non il valore nominale!).
2. **Aumento di capitale con sovrapprezzo**: per ogni azione emessa sopra il nominale → il **nominale** va a **Capitale Sociale**, la **differenza** va a **Riserva sovrapprezzo azioni** (art. 2431 c.c.).
3. **La vendita di azioni tra soci/mercato NON tocca la contabilità della società**: cambia solo il libro soci. Le scritture della plusvalenza stanno nel libro giornale **del socio venditore**.

### Aumento scindibile vs inscindibile (art. 2439, co. 2, c.c.)

| | **Scindibile** | **Inscindibile** |
|---|---|---|
| Sottoscrizione parziale entro il termine | L'aumento **resta efficace per la parte sottoscritta** | L'aumento è **inefficace per intero**: i sottoscrittori sono liberati e i versamenti restituiti |
| Quando si usa | Offerte al mercato (come un'IPO), dove non si sa quanti aderiranno | Operazioni in cui serve **tutto** l'importo (es. ricapitalizzazione minima) |
| Regola di default | La deliberazione deve **prevedere espressamente** la scindibilità; in mancanza, l'aumento è inscindibile | — |

### Riserve di utili vs riserve di capitale (la tabella da sapere a memoria)

| Riserva | Tipo | A: aumento CS | B: copertura perdite | C: dividendi |
|---|---|---|---|---|
| **Riserva legale** (art. 2430) | Utili | No (finché non supera 1/5 del CS; sì solo per l'eccedenza) | **Sì** (dopo le altre riserve) | **No, mai** |
| **Riserva straordinaria** | Utili | **Sì** | **Sì** | **Sì** |
| **Riserva sovrapprezzo azioni** (art. 2431) | **Capitale** | **Sì** | **Sì** | Solo se la riserva legale ha raggiunto 1/5 del CS |

> Logica: le **riserve di utili** nascono da utili non distribuiti (legale, straordinaria); le **riserve di capitale** nascono da apporti dei soci (sovrapprezzo, versamenti in conto capitale). Il sovrapprezzo NON è un utile: è denaro versato dai soci oltre il nominale.

---
---

## 2. Esercizio ufficiale del corso — IPO di Alfa S.p.A.

### Dati (dal PDF del corso)

**SP Alfa S.p.A. al 31/12/n** — Attivo: Banca c/c 1.000, Immobile 2.000, Avviamento 500 (tot. 3.500). Passivo: F.do amm.to 1.000, Debiti 500, CS 1.000, Ris. legale 200, Ris. straordinaria 800 (tot. 3.500).

- CS = **500 azioni ordinarie da 2 € nominali**. Soci: **Giulia Rossi 400 azioni (80%)**, **FINSAP S.r.l. 100 azioni (20%)**, con valore di carico **300 €** nel bilancio di FINSAP.
- Rothschild stima il valore di mercato di Alfa in **2.500 €** → prezzo di collocamento **5 €/azione**.
- OPVS del 30/6/n+1: emissione di **50 nuove azioni a 5 €** (aumento scindibile, tutto sottoscritto e versato in denaro entro 10 giorni) + **FINSAP vende le sue 100 azioni a 5 €**.
- Nell'esercizio n+1 nessun'altra operazione.

---

### Richiesta 1 — Plusvalenza di FINSAP

- Prezzo di cessione = 100 azioni × 5 € = **500**
- Valore di carico = **300** (attenzione: NON il nominale di 200)
- **Plusvalenza = 500 − 300 = 200**

### Richiesta 2 — Scritture sul libro giornale

#### Nel libro giornale di ALFA (solo l'aumento di capitale)

Le 50 nuove azioni a 5 € valgono 250, di cui: nominale 50 × 2 = **100** → CS; sovrapprezzo 50 × 3 = **150** → Riserva sovrapprezzo.

**30/6/n+1 — Sottoscrizione:**

| Conto | Dare | Avere |
|---|---|---|
| Azionisti c/sottoscrizione | 250 | |
| Capitale sociale | | 100 |
| Riserva sovrapprezzo azioni | | 150 |

**Entro 10 gg — Versamento:**

| Conto | Dare | Avere |
|---|---|---|
| Banca c/c | 250 | |
| Azionisti c/sottoscrizione | | 250 |

**Cessione FINSAP → mercato: NESSUNA scrittura per Alfa** (l'operazione avviene tra il socio e i nuovi investitori; Alfa aggiorna solo il libro soci).

#### Nel libro giornale di FINSAP (per completezza)

| Conto | Dare | Avere |
|---|---|---|
| Banca c/c | 500 | |
| Partecipazione in Alfa S.p.A. | | 300 |
| Plusvalenza da cessione partecipazione | | 200 |

### Richiesta 3 — SP di Alfa al 31/12/n+1

Unica variazione rispetto al 31/12/n: +250 in banca, +100 CS, +150 riserva sovrapprezzo (la traccia esclude altre operazioni, quindi niente ammortamenti).

| Attivo | € | Passivo | € |
|---|---|---|---|
| Banca c/c | 1.250 | F.do Amm.to | 1.000 |
| Immobile | 2.000 | Debiti | 500 |
| Avviamento | 500 | CS | 1.100 |
| | | Ris. sovrapprezzo azioni | 150 |
| | | Ris. legale | 200 |
| | | Ris. straordinaria | 800 |
| **Totale** | **3.750** | **Totale** | **3.750** |

### Richiesta 4 — Classificazione del PN al 31/12/n+1

| Voce | Importo | Natura | A: aumento CS | B: copertura perdite | C: dividendi |
|---|---|---|---|---|---|
| Capitale sociale | 1.100 | Capitale | — | — | — |
| Ris. sovrapprezzo azioni | 150 | **Riserva di capitale** | Sì | Sì | Solo se ris. legale ≥ 1/5 CS (qui 200 < 220 → **no**) |
| Ris. legale | 200 | **Riserva di utili** | No | Sì | No |
| Ris. straordinaria | 800 | **Riserva di utili** | Sì | Sì | Sì |

> Nota trappola: dopo l'aumento, il quinto del CS è 1.100/5 = **220**. La riserva legale (200) è scesa **sotto** il quinto → torna l'obbligo di accantonare il 5% degli utili futuri, e il sovrapprezzo non è distribuibile (art. 2431).

### Richiesta 5 — Scindibile vs inscindibile

Vedi scheda-metodo sopra: lo **scindibile** resta efficace per la parte sottoscritta anche se l'aumento non viene sottoscritto per intero entro il termine; l'**inscindibile** cade per intero se non integralmente sottoscritto. Nell'IPO si usa lo scindibile perché l'adesione del mercato non è nota in anticipo.

### Richiesta 6 — Compagine post IPO

Totale azioni post aumento = 500 + 50 = **550**.

| Socio | Azioni | % |
|---|---|---|
| Giulia Rossi | 400 | **72,73%** |
| Mercato (flottante: 100 ex FINSAP + 50 nuove) | 150 | **27,27%** |
| FINSAP | 0 | 0% |
| **Totale** | **550** | 100% |

> Giulia Rossi si **diluisce** dall'80% al 72,73% senza vendere nulla: effetto dell'emissione di nuove azioni sottoscritte da terzi. Mantiene comunque il controllo di diritto (>50%).
