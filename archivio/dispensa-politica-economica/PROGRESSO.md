# Progresso — Politica Economica

> **Per una sessione Claude nuova**: leggi questo file per intero prima di rispondere a "a che punto sono". Non serve rileggere altre conversazioni.

**Oggi**: venerdì 4 settembre 2026. **Esame**: martedì 8 settembre. **Giorni rimasti**: 4 (oggi compreso).

**Calendario** (da [`schemi/00e-quaderno-esercizi.md`](schemi/00e-quaderno-esercizi.md)):

- [x] **Giorno 1 — gio 3/9**: politica fiscale (01) + inflazione e Phillips (02) — A1 → A8
- [~] **Giorno 2 — ven 4/9**: monopolio (03) + benessere (04) + teoria normativa (11) — A9, A10, A11 fatti dal vivo; A12 e A13 lasciati a metà, da riprendere
- [ ] Giorno 3 — sab 5/9: lavoro (05) + economia aperta (06) + moneta (07) — B1 → B8
- [ ] Giorno 4 — dom 6/9: valutazione progetti (13) + argomenti lasciati in disparte (08, 09, 10, 12, 14) — B9, B10
- [ ] Giorno 5 — lun 7/9: le 3 simulazioni da 11 domande di `00d` + rifare a freddo gli esercizi sbagliati

---

## Giorno 1 (gio 3/9) — dettaglio

Lavorato dal vivo in chat sul [foglio del giorno 1](giornate/giorno-1-giovedi-3-settembre.md) (PDF: `Giorno 1 — giovedi 3 settembre.pdf`), esercizi A1-A8 del quaderno.

| Esercizio | Esito | Note |
|---|---|---|
| A1 (a-d) | ✅ tutti corretti al primo tentativo | Moltiplicatore spesa 5, moltiplicatore imposte −4, Haavelmo verificato (ΔY=+50) |
| A2 (a-d) | ✅ un errore intercettato e corretto | Nel punto (a) primo tentativo dava `0Y = 240` per parentesi sciolta male (`Y − 75 − 0,25Y` scritto come `Y − 75 + 0,25Y`); corretto → Y=600, moltiplicatore 2,5 |
| A3 (a-d) | ✅ risposte fornite, nessun errore riportato | Economia aperta, moltiplicatore 2, saldo commerciale −40 con G=150 |
| A4 (a-d) | ✅ risposte fornite, nessun errore riportato | Avanzo primario 2,6% del PIL; discussione su crescita vs tasso di interesse come leve |
| A5 (a-c) | ⚠️ **errore in esecuzione, corretto in chat** | Nel punto (a), ultima divisione: Jacopo ha calcolato 14.001,6/1,08 = 12.881,47 invece di **12.964,44**. Metodo giusto, esecuzione sbagliata. **Il file del quaderno resta corretto**: l'errore era solo nel tentativo dal vivo. |
| A6 (a) | ✅ corretto | u_N = 10,5% |
| A6 (b) | ⚠️ **errore da trabocchetto dei decimali, corretto in chat** | Jacopo ha ottenuto ẇ = 1% (invece di 10%) e quindi π = −0,5% (invece di 8,5%) — quasi certamente uno scivolone nella moltiplicazione `4 × 0,07`. Corretto con il controllo di plausibilità: π non può essere negativo con u sotto il naturale. |
| A6 (c) | 🔴 **punto debole dichiarato da Jacopo** | "Non mi viene" — l'esercizio "al contrario" (dato l'obiettivo di π, risalire a u passando per ẇ) richiesto con un hint prima di essere risolto |
| A7 (a-d) | ✅ risolto con guida | Tabella delle aspettative adattive costruita correttamente una volta vista una volta |
| A8 (a) | ✅ corretto | p = 1.875 |

### Il punto debole da riprendere — non uno stile, un tipo di esercizio

**Gli esercizi "al contrario" sulla curva di Phillips** (dato l'obiettivo di inflazione o la sua variazione, risalire al tasso di disoccupazione, passando per `ẇ`) sono l'unico punto su cui Jacopo ha bisogno di un hint esplicito per partire, anche dopo averlo già visto una volta (è successo sia su A6(c) sia sul blocco 4 del ripasso lampo, sotto).

**Da riprovare domani, a freddo, prima di studiare argomenti nuovi** (deciso insieme in chat): un esercizio come A6(c) e uno come il blocco 4 del ripasso — senza guardare soluzioni. Se vengono sciolti, il punto è chiuso; se no, va ripreso con più esempi.

---

## Ripasso lampo di oggi (non è in nessun PDF — solo qui)

Dopo A1-A8, Jacopo ha chiesto 30 minuti di ripasso a tempo. Ho costruito 4 blocchi con numeri nuovi (mai usati altrove nella dispensa). Non generano un PDF a sé — il formato e le regole sono documentati in [`CONVENZIONI-ESERCIZI.md`](CONVENZIONI-ESERCIZI.md), il testo completo con soluzioni è lì in fondo come esempio.

**Esito**: blocco 1 (moltiplicatori) tutto corretto; blocco 2 (fiscal drag) un errore nella divisione finale, corretto; blocco 3 (curva salari) punto (a)-(b) con l'errore dei decimali già visto su A6, punto (c) non riuscito senza guida; blocco 4 (Phillips iterata) non riuscito senza guida — stesso punto debole di A6(c).

---

## Giorno 2 (ven 4/9) — dettaglio

Foglio: [`giornate/giorno-2-venerdi-4-settembre.md`](giornate/giorno-2-venerdi-4-settembre.md) (PDF: `Giorno 2 — venerdi 4 settembre.pdf`). Lavorato dal vivo in chat, passo passo su richiesta esplicita di Jacopo ("A9 e A10 li faccio piano piano che non ci ho capito veramente nulla") — molto più granulare del giorno 1: ogni formula scomposta in singoli pezzi (un numero alla volta), mai un conto in un colpo solo.

| Esercizio | Esito | Note |
|---|---|---|
| Tutorial 1-2 (monopolio + naturale) | ✅ fatti prima della sessione | — |
| A9 (a-b) | ✅ corretto | `q_M=7,5`, `P_M=45`, `q_C=10`, `P_C=40` |
| A9 (c) | ⚠️ **errore corretto in chat** | Aveva calcolato base×altezza = 37,5 ma **dimenticato il `½`** della formula del DWL, facendo il conto in un colpo solo invece che a pezzi separati. Una volta scomposto (base, altezza, poi `½×`), l'ha visto da solo. Risultato corretto: `DWL=18,75` |
| A9 (d) | ✅ corretto, con un errore di arrotondamento intercettato | Primo tentativo `L=0,3` (sbagliato: era `15/50` invece di `15/45`); rifatta la divisione, arrivato a `0,333...` da solo |
| A10 (a-b) | ✅ corretto | Monopolio naturale verificato, `Q_M=12`, `P_M=18`, profitto=64 |
| A10 (c) | ⚠️ **errore concettuale sulla formula risolutiva, corretto in chat** | Non sull'equazione di secondo grado in sé (discriminante fatto bene una volta scomposto: `b²=576`, `4ac=320`, `Δ=256`, `√Δ=16`), ma sulla **divisione finale**: pensava che nella formula `(−b±√Δ)/2a` si dovesse dividere per 2 **solo la radice**, non l'intero numeratore. Chiarito con parentesi esplicite `(24±16)/2`, in due passi separati (prima la somma/sottrazione, poi la divisione). Risultato corretto: radici 4 e 20, tenuta quella maggiore (`Q=20, P=10=ATC`) |
| A10 (d) | ✅ dato in sintesi da Claude (concetto già acquisito) | perdita = −80, pari al costo fisso |
| A11 (a-d) | ✅ **tutto corretto, fatto da solo**, senza guida | Buon segnale: la parte concettuale (Pareto, i tre criteri FBS, Kaldor) è passata bene una volta letta sul foglio, a differenza della meccanica di calcolo di A9-A10 |
| A12 | 🔴 **non risolto, messo da parte** | Bloccato già al primo passaggio di sostituzione (`Y = θN` dentro il modello) — ha detto esplicitamente "non ho capito nulla" e ha chiesto di rimandarlo. Da riprendere ripartendo da zero con **solo numeri**, mai lettere, un conto alla volta (vedi sotto) |
| A13 | 🔴 **non affrontato**, messo da parte su richiesta di Jacopo | Si era arrivati a impostare il sistema (`500=2G+e`, `0=−0,4G+0,8e`) ma non risolto |

### Il pattern di oggi — errori di meccanica, non di logica

A differenza del giorno 1 (dove il punto debole era concettuale, gli esercizi "al contrario" di Phillips), oggi gli errori erano tutti su **come si esegue un calcolo a più pezzi**, non su cosa significa:

- dimenticare un fattore (`½`) quando la formula si prova a fare "a mente" in un colpo solo invece che a pezzi;
- fraintendere **cosa copre la barra di frazione** in `(−b±√Δ)/2a` — pensare che la divisione riguardi solo l'ultimo pezzo scritto, non tutto il numeratore.

**La correzione che ha funzionato**: costringerlo a scomporre ogni formula in passaggi separati e dargli **un solo numero per volta** da calcolare, mai una formula intera. Con questo metodo A9 e A10 sono stati chiusi bene. Su A12 lo stesso approccio (ma partendo da lettere/sostituzioni astratte invece che da numeri concreti) non ha funzionato — è saltato al primo passaggio.

### A12 — cosa NON rifare, e come ripartire

Il primo tentativo di oggi ha introdotto la sostituzione `Y_d = (1−t)·θN` troppo presto e in forma simbolica: Jacopo si è perso subito. **Da riprendere ripartendo da zero, sempre con i numeri della traccia (θ=25, c=0,75, I=2.000, N=1.600) mai con le lettere**, un pezzo alla volta:

1. `Y = θ·N = 25·1.600 = 40.000` (fatto, gli è tornato)
2. Poi (da fare): `C = c·Y = 0,75 · 40.000` con `t=0` (si era fermato qui)
3. Poi: `Y = C + I + G` con i numeri → isolare `G`
4. Solo alla fine, se regge, generalizzare con `t=0,2` e introdurre la formula in lettere come "scorciatoia" per il caso generale — mai come punto di partenza.

## Come continuare da qui

1. **Riprendere A12** con il metodo sopra (solo numeri, mai lettere all'inizio).
2. Poi **A13** (Tinbergen): si era arrivati a impostare il sistema, manca solo risolverlo — dovrebbe scorrere più facile di A12 perché è puramente meccanico (stesso tipo di scomposizione a pezzi che ha funzionato per A9/A10).
3. Rimane ancora aperto dal giorno 1: proporre a freddo un esercizio "al contrario" sulla curva di Phillips (vedi sopra) — non ancora fatto, va ripreso appena c'è occasione.
4. Una volta chiusi A12-A13, il **giorno 2 è completo**. Poi proseguire con il **giorno 3** (B1-B8): lavoro, economia aperta, moneta. Verificare se esiste già `giornate/giorno-3-*.md` — se non esiste, crearlo seguendo `CONVENZIONI-ESERCIZI.md`.
