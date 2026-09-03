# Convenzioni per gli esercizi

> **Per una sessione Claude che genera un nuovo foglio di lavoro** (`giornate/giorno-N-*.md`): questo file descrive come sono fatti gli esercizi già prodotti, perché il giorno 2, 3, 4, 5 restino coerenti con il giorno 1. Non è materiale di studio per Jacopo — è una guida di stile per chi scrive.

## I due formati in uso

### 1. Formato "foglio del giorno" — pianificato, va a PDF

Quello di [`giornate/giorno-1-giovedi-3-settembre.md`](giornate/giorno-1-giovedi-3-settembre.md). Struttura fissa, blocco per blocco:

1. **La teoria che serve** — solo quanto entra nei conti, mezza pagina, mai un ripasso completo del capitolo (quello sta negli schemi).
2. **Il tutorial** — un esercizio svolto **passo per passo**, con:
   - numeri **diversi** da qualunque traccia già usata nella dispensa (quaderno, schemi, tutorial di altri giorni);
   - accanto a ogni passaggio, non solo il calcolo ma **il perché** si fa così e no altrimenti, e spesso una riga "che cosa scrivi sul foglio";
   - almeno un **controllo di buon senso** esplicito (un segno che non può essere negativo, un coefficiente che non può superare 1, un ordine di grandezza plausibile) — è la rete di sicurezza contro gli errori di esecuzione, non solo di metodo.
3. **Tocca a te** — le tracce vere del quaderno (stesso testo, senza modifiche), riportate per intero così il foglio resta autosufficiente.
4. **Soluzioni** — in coda, separate da un salto pagina, mai subito sotto la traccia corrispondente. Copiate/adattate dalle soluzioni ufficiali di `schemi/00e-quaderno-esercizi.md` (stesso numero, stesso risultato — non si reinventano).

Ogni blocco chiude con una **tabella degli errori tipici** (colonna sinistra: l'errore; colonna destra: come si evita) — costruita sugli errori che si osservano *davvero* mentre l'esercizio viene fatto, non su errori ipotetici.

### 2. Formato "ripasso lampo" — improvvisato, resta in chat

Usato quando c'è poco tempo (es. "ho 30 minuti per ripassare"). Niente teoria, niente tutorial: solo enunciati con un budget di tempo indicativo, pensati per allenare il recupero **sotto pressione**, quando gli appunti non sono sott'occhio. Non genera un PDF a sé stante. Se il tempo lo giustifica, gli enunciati e le soluzioni vanno comunque registrati — vedi l'esempio completo più sotto, e la voce corrispondente in `PROGRESSO.md` — perché altrimenti quel lavoro sparisce con la chat.

## Le cinque regole non negoziabili (valgono per entrambi i formati)

1. **Numeri sempre nuovi.** Mai riusare gli stessi valori di un esercizio già svolto in un altro punto della dispensa: si riconoscerebbe il risultato invece di rifare il conto.
2. **Verifica in Python prima di scrivere.** Ogni risultato numerico si ricalcola con uno script usa-e-getta (nella scratchpad, mai commesso al repo) prima di essere messo su carta. Questo ha già intercettato errori nella costruzione del quaderno originale — vale anche per il materiale improvvisato.
3. **Tracce e soluzioni separate**, mai adiacenti.
4. **Formule in blocco recintato + legenda `dove:`**, mai LaTeX — la convenzione generale è in `README.md` (sezione sulle formule) e vale identica qui.
5. **Il controllo di plausibilità economica è parte della soluzione**, non un extra. Non è mai stato solo un vezzo: il 3 settembre ha effettivamente permesso di individuare in tempo reale un errore di calcolo di Jacopo su un esercizio di curva dei salari (π negativo con disoccupazione sotto il naturale — impossibile, quindi si è ricontrollato e trovato l'errore).

## Istruzioni operative per generare il PDF di un nuovo giorno

1. Scrivi il file in `giornate/giorno-N-<nome-giorno>-<data>.md` (es. `giorno-2-venerdi-4-settembre.md`), seguendo la struttura della sezione 1 sopra.
2. **Non scrivere l'HTML a mano.** In fondo a `build_pdf.py` c'è già la chiamata di esempio per il giorno 1:
   ```python
   costruisci("Giorno 1 — giovedi 3 settembre", GIORNATE,
              ["giorno-1-giovedi-3-settembre.md"], HEADER_GIORNO_1, con_ancore=False)
   ```
   Per un nuovo giorno: scrivi un nuovo `HEADER_GIORNO_N` (stesso stile del giorno 1: titolo, una riga su cosa contiene, `[TOC]`, salto pagina) e aggiungi una chiamata analoga con `con_ancore=False` (i fogli giornalieri non hanno la mappa `ANCHOR_MAP` degli schemi).
3. Genera `.md` e `.html` con `python3 build_pdf.py`. Deve stampare `Controllo formule: nessun problema rilevato` — se stampa avvisi, vanno risolti prima di procedere (quasi sempre: riga troppo larga, o un `$`/`_` finito fuori da un blocco recintato).
4. Passaggio a PDF con Chrome headless — comando in `README.md`, sezione "Come studiare da qui".
5. Verifica finale con `pymupdf`: nessun blocco di testo oltre il margine destro della pagina, tutte le tracce e le rispettive soluzioni presenti, nessun link interno rotto. È lo stesso controllo già fatto per il giorno 1.

---

## Esempio completo — il ripasso lampo del 3 settembre

Costruito con numeri nuovi (mai usati in nessuna traccia della dispensa), format "ripasso lampo": budget di tempo, nessuna teoria, soluzioni verificate in Python. Riportato qui per intero come modello, e perché altrimenti non esisterebbe in nessun file.

### Blocco 1 — Moltiplicatori (7 minuti)

**Traccia.** Economia chiusa: `C = 150 + 0,6(Y − T)`, `I = 200`, `G = 150`, `T = 100`.

a) Calcola il reddito di equilibrio.
b) `G` sale a 190: di quanto cresce `Y`?
c) Partendo dalla situazione iniziale, `T` sale a 140: di quanto varia `Y`?

**Soluzione**

```
      (a)  Y = 150 + 0,6(Y − 100) + 200 + 150
           Y = 0,6Y + 440
           0,4 Y = 440
           Y = 1.100

      moltiplicatore spesa    = 1/(1−0,6) = 2,5
      moltiplicatore imposte  = −0,6/0,4  = −1,5

      (b)  ΔG = +40  →  ΔY = 2,5 · 40 = +100  →  Y = 1.200
      (c)  ΔT = +40  →  ΔY = −1,5 · 40 = −60  →  Y = 1.040
```

Esito il 3/9: tutti e tre corretti al primo tentativo.

### Blocco 2 — Fiscal drag (6 minuti)

**Traccia.** Scaglioni: 15% fino a 12.000, 28% oltre. Anno 1: reddito 16.000. Anno 2: inflazione 8%, reddito nominale 17.280 (stesso reddito reale).

a) Imposta e aliquota media nei due anni.
b) Il reddito netto reale è aumentato, diminuito o uguale?

**Soluzione**

```
      Anno 1:  T = 12.000·0,15 + 4.000·0,28 = 1.800 + 1.120 = 2.920
               aliquota media = 2.920/16.000 = 18,25%
               netto = 16.000 − 2.920 = 13.080

      Anno 2:  T = 12.000·0,15 + 5.280·0,28 = 1.800 + 1.478,4 = 3.278,4
               aliquota media = 3.278,4/17.280 = 18,97%
               netto nominale = 17.280 − 3.278,4 = 14.001,6
               netto reale    = 14.001,6/1,08 = 12.964,44

      perdita reale ≈ 115,56 euro  →  (b) diminuito, è fiscal drag
```

Esito il 3/9: metodo corretto; errore nell'ultima divisione (12.881,47 invece di 12.964,44), corretto in chat con il controllo "rimoltiplica e verifica che torni al dato di partenza".

### Blocco 3 — Curva dei salari e costo pieno (8 minuti)

**Traccia.** Curva dei salari: `ẇ = 0,30 − 2,5 u`.

a) Tasso naturale `u_N`.
b) Con `u = 8%` e `θ̇ = 1,5%` (mark-up costante), calcola `ẇ` e `π`.
c) Per un obiettivo di inflazione del 5% (sempre `θ̇ = 1,5%`), quale `u` serve?

**Soluzione**

```
      (a)  0 = 0,30 − 2,5 u_N  →  u_N = 0,12  →  12%

      (b)  ẇ = 0,30 − 2,5·0,08 = 0,10  →  10%
           π = ẇ − θ̇ = 10% − 1,5% = 8,5%

      (c)  5% = ẇ − 1,5%  →  ẇ = 6,5%
           0,065 = 0,30 − 2,5 u  →  u = 0,235/2,5 = 0,094  →  9,4%
```

Esito il 3/9: (a) corretto; (b) errore da trabocchetto dei decimali (ẇ letto come 1% invece di 10%, quindi π negativo invece di 8,5%); (c) non risolto senza guida — è il punto debole, vedi `PROGRESSO.md`.

### Blocco 4 — Phillips con aspettative adattive (9 minuti)

**Traccia.** Stessa curva del blocco 3, con `θ̇ = 0`. Il governo tiene `u = 8%` (sotto il naturale) per tre periodi, aspettative adattive `λ = 1`, `πᵉ_0 = 0`.

a) Costruisci la tabella dell'inflazione per `t = 0, 1, 2`.
b) Quale `u` servirebbe per ridurre l'inflazione di 8 punti in un periodo?

**Soluzione**

```
      γ(8%) = 0,30 − 2,5·0,08 = 0,10   →  10%  (costante, perché u non cambia)
```

| t | `πᵉ_t` | `u_t` | `π_t = γ(u_t) + πᵉ_t` |
|---|---|---|---|
| 0 | 0% | 8% | 10% |
| 1 | 10% | 8% | 20% |
| 2 | 20% | 8% | 30% |

```
      (b)  γ(u) = −8%
           −0,08 = 0,30 − 2,5 u  →  u = 0,38/2,5 = 0,152  →  15,2%
```

Esito il 3/9: non risolto senza guida — stesso punto debole del blocco 3(c).
