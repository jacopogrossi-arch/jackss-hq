# Soluzioni — "Esercizi 1.pdf"

Svolgimento completo dei 4 esercizi del file `Esercizi 1.pdf` (Downloads/Universita/Ragioneria), risolti con il metodo del professore (stesse convenzioni di `ESERCIZI_SVOLTI.md`: CMP periodico ponderato su tutte le entrate, IRES 24%, nomi dei conti della dispensa).

---

## Esercizio 1 — Impairment dell'impianto (Alfa SpA)

**Dati**: costo storico 5.000, fondo ammortamento 2.000 → valore contabile netto **3.000**; vita residua 5 anni, quote costanti → ammortamento annuo = 3.000 / 5 = **600**. Prezzo netto di vendita stimato dal perito: **1.700**.

### Tabella del piano industriale (caselle colorate)

| Piano industriale | 2023 | 2024 | 2025 | 2026 | 2027 |
|---|---|---|---|---|---|
| Ricavi delle vendite | 15.000 | 14.000 | 13.000 | 12.000 | 11.000 |
| Costi diretti | −10.500 | −10.300 | −10.200 | −9.800 | −8.900 |
| Costi indiretti | −4.000 | −3.300 | −2.500 | −1.800 | −1.800 |
| = Margine lordo industriale | 500 | 400 | 300 | 400 | 300 |
| **Ammortamento Impianto** | **−600** | **−600** | **−600** | **−600** | **−600** |
| **= Margine industriale netto** | **−100** | **−200** | **−300** | **−200** | **−300** |
| **Capacità di ammortamento** | **1.900** | | | | |

La **capacità di ammortamento** = somma dei margini lordi industriali dei 5 anni (500 + 400 + 300 + 400 + 300 = **1.900**) ed è la stima del **valore d'uso** dell'impianto.

### Ragionamento

1. **Valore recuperabile** = maggiore tra prezzo netto di vendita (1.700) e valore d'uso (1.900) → **1.900**
2. Confronto con valore contabile: 1.900 < 3.000 → **perdita durevole di valore di 1.100**, l'impianto va svalutato

### Risposte

| Domanda | Risposta | Motivo |
|---|---|---|
| Valore di iscrizione al 31/12/2022 | **2) 1.900** | Valore recuperabile 1.900 < valore contabile 3.000 |
| Quota di ammortamento nei 5 esercizi successivi | **1) 380** | 1.900 / 5 anni = 380 |
| Se prezzo netto di vendita = 2.600, valore da ammortizzare | **2) 2.600** | Recuperabile = max(2.600; 1.900) = 2.600, comunque < 3.000 quindi si svaluta a 2.600 |

---

## Esercizio 2 — Imposte correnti, differite e anticipate (Alfa S.r.l.)

**Dati**: risultato lordo 200.000. Costi 30.000 deducibili in n+1 (diff. temporanea deducibile → imposte anticipate); costi 10.000 indeducibili (diff. permanente); ricavi 12.000 imponibili in esercizi futuri (diff. temporanea tassabile → imposte differite).

### Punto a) — Tabella calcolo imposte

| Tabella calcolo imposte | Anno "n" | Diff. Temp. Tassabili | Diff. Temp. Deducibili | Diff. Permanente |
|---|---|---|---|---|
| Risultato lordo dell'esercizio | 200.000 | | | |
| Riprese in aumento | 40.000 | | 30.000 | 10.000 |
| Riprese in diminuzione | (12.000) | 12.000 | | |
| **Reddito imponibile** | **228.000** | | | |
| Aliquota IRES (%) | 24% | | | |
| **Imposte correnti** | **54.720** | (228.000 × 24%) | | |
| **Imposte differite** | **2.880** | (12.000 × 24%) | | |
| **Imposte anticipate** | **−7.200** | (−30.000 × 24%) | | |
| **Imposte di competenza del bilancio** | **50.400** | (54.720 + 2.880 − 7.200) | | |

**Verifica**: le sole differenze permanenti restano nel carico fiscale di competenza → (200.000 + 10.000) × 24% = 50.400 ✓

### Punto b) — Scritture contabili

| Dare | | Avere | Importo |
|---|---|---|---|
| Imposte correnti | a | Debiti tributari | 54.720 |
| Imposte differite | a | Fondo Imposte Differite | 2.880 |
| Imposte Anticipate (credito) | a | Imposte anticipate | 7.200 |

**Logica**: le imposte correnti sono un costo con contropartita il debito verso l'Erario; le differite sono un costo aggiuntivo accantonato a fondo (si pagheranno quando i 12.000 diventeranno imponibili); le anticipate rilevano un credito nell'attivo con contropartita una rettifica in diminuzione delle imposte a CE.

---

## Esercizio 3 — Magazzino con criterio CMP (Alfa, capi di abbigliamento)

**Dati**: esistenze iniziali 3.000 unità × 15 € = 45.000. Movimenti dell'esercizio: gennaio +2.000 @ 14 € e −1.000; settembre −1.500; ottobre +1.000 @ 18 €; dicembre −2.500.

### Punto a) — Quantità e valorizzazione

Quantità in giacenza al 31/12/n:

```
3.000 + 2.000 + 1.000 − 1.000 − 1.500 − 2.500 = 1.000 unità
```

CMP (metodo periodico: si ponderano **tutte le entrate**, inclusa l'esistenza iniziale; le uscite non modificano il CMP):

```
CMP = (3.000 × 15 + 2.000 × 14 + 1.000 × 18) / (3.000 + 2.000 + 1.000)
    = 91.000 / 6.000 = 15,17 €
```

| Codice prodotto | Quantità giacenti al 31/12/n | Costo d'acquisto - CMP |
|---|---|---|
| 1001 | 1.000 | 15,17 |
| **Valorizzazione delle rimanenze** | | **15.166,67 ≈ 15.167** |

Il valore di realizzazione di mercato non è inferiore al CMP → si mantiene il costo, nessuna svalutazione (art. 2426 n. 9 c.c.).

### Punto b) — Scritture contabili

**Riapertura dei conti al 1/1/n:**

| Dare | | Avere | Importo |
|---|---|---|---|
| Rimanenze Iniziali di merce | a | Stato patrimoniale Iniziale | 45.000 |
| Variazione rimanenze iniziali di merce | a | Rimanenze Iniziali di merce | 45.000 |

**Scritture dell'esercizio n (acquisti):**

| Dare | | Avere | Importo |
|---|---|---|---|
| Merce c/acquisti | a | Debito verso fornitori | 28.000 (gennaio: 2.000 × 14) |
| Merce c/acquisti | a | Debito verso fornitori | 18.000 (ottobre: 1.000 × 18) |

Totale acquisti dell'esercizio = 28.000 + 18.000 = **46.000**

**Assestamento al 31/12/n:**

| Dare | | Avere | Importo |
|---|---|---|---|
| Rimanenze finali di merce | a | Variazione rimanenze finali di merce | 15.167 |

**Epilogo al 31/12/n:**

| Dare | | Avere | Importo |
|---|---|---|---|
| Conto economico | a | Merce c/acquisti | 46.000 |
| Conto economico | a | Variazione rimanenze iniziali di merce | 45.000 |
| Variazione rimanenze finali di merce | a | Conto economico | 15.167 |
| Stato Patrimoniale | a | Rimanenze finali di merce | 15.167 |
| Debito verso fornitori | a | Stato Patrimoniale | 46.000 |

### Punto c) — Bilancio contabile di verifica

**Conto economico "n":**

| Dare | Avere |
|---|---|
| Merce c/acquisti 46.000 | Variazione rimanenze finali di merce 15.167 |
| Variazione rimanenze iniziali di merce 45.000 | |

**Stato Patrimoniale al 31/12/n:**

| Dare | Avere |
|---|---|
| Rimanenze finali di merce 15.167 | Debito verso fornitori 46.000 |

### Punto d) — Rappresentazione nel bilancio civilistico

- **Stato Patrimoniale**: C) Attivo circolante → **Merci 15.167**; D) Debiti → **Debiti verso fornitori 46.000**
- **Conto Economico**: B) Costi della produzione → costi per merci **46.000**; variazione delle rimanenze di merci **+29.833** (iniziali 45.000 − finali 15.167)

> ⚠️ Attenzione al segno: qui il magazzino è **diminuito**, quindi la variazione **aumenta** i costi della produzione (+29.833). Nell'esercizio analogo in dispensa il magazzino cresceva e la variazione era negativa (−8.500): il segno dipende dalla direzione della variazione.

---

## Esercizio 4 — Indici di bilancio

| Indice | Formula | Calcolo | Risultato | Risposta |
|---|---|---|---|---|
| Tesoreria secondario | (Liquidità immediate + differite) / Passività correnti | (76.600 + 300 + 505.000 + 7.000) / 467.000 = 588.900 / 467.000 | 1,26 | **[a]** |
| Struttura primario | Patrimonio netto / Attivo immobilizzato | 798.800 / 810.500 | 0,99 | **[b]** |
| ROI | EBIT / Totale impieghi | 145.000 / 1.811.600 | 8,00% | **[c]** |
| ROS | EBIT / Ricavi | 145.000 / 3.500.000 | 4,14% | **[d]** |

Note sulle formule (come da dispensa):
- La **tesoreria secondaria** esclude le rimanenze dall'attivo corrente (liquidità differite = crediti commerciali entro l'esercizio + ratei attivi; liquidità immediate = banca + cassa).
- La **struttura primaria** misura quanto il patrimonio netto copre l'attivo immobilizzato (qui 0,99: copertura quasi integrale).
- **ROI** e **ROS** usano l'**EBIT** (margine operativo netto), mai il risultato d'esercizio.
