# Dispensa Politica Economica — esame 08/09/2026

Costruita a partire dal materiale della professoressa (37 file in `pdf-fonte/`, esclusa da git) e da un'analisi dei compiti/esercitazioni passati per capire cosa viene davvero chiesto all'esame.

## Struttura della prova (da Moodle, modalità d'esame 2026-2027)

Tre fasi:

1. **Preselezione** — test a risposta multipla: **11 domande in 10 minuti**, superata con **almeno 6 risposte corrette**. È uno sbarramento: senza preselezione non si accede allo scritto.
2. **Scritto** — **due domande aperte + un esercizio**, tempo **1 ora**.
3. **Orale** — facoltativo (per alzare il voto) oppure **a richiesta del docente**.

**Testo di riferimento:** Paesani, P., *Manuale di politica economica*, II edizione, Giappichelli, 2020.

**Date d'appello**
- a.a. 2025-26: **8 settembre 2026** · 6 novembre 2026 (appello straordinario, riservato a fuori corso, part time, studenti con disabilità e DSA, studenti genitori e lavoratori)
- a.a. 2026-27: 20 gennaio · 10 febbraio · 16 giugno · 14 luglio · 8 settembre

**Cosa comporta per lo studio**
- La preselezione pesca su tutto il programma, non sui soli argomenti dei compiti passati: gli schemi 9-10 (crescita/sviluppo, disuguaglianze) smettono di essere copertura opzionale e diventano necessari almeno a livello di definizioni.
- 11 domande in 10 minuti = ~55 secondi l'una: serve richiamo immediato, non ragionamento. Per questa fase il materiale giusto è il **formulario** + il **glossario**, ripassati fino all'automatismo.
- Lo scritto è 1 ora per tre pezzi (~20 minuti l'uno) e contiene **un solo esercizio**: quasi certamente da uno degli argomenti core 1-4 (o 5-6). Conviene arrivare con gli esercizi tipo già svolti, per metodo più che a memoria.
- L'orale può essere chiesto dal docente: le risposte aperte vanno scritte in modo difendibile, perché un passaggio ambiguo diventa la domanda dell'orale.

## Come studiare da qui

**`Dispensa Politica Economica.pdf`** — il documento unico da cui studiare: 151 pagine, con struttura della prova e indice cliccabile in prima pagina che rimanda a ogni capitolo, i 14 schemi + formulario + glossario + mappa di priorità + quaderno di esercizi + banca domande per la preselezione + i 9 grafici. Generato da `build_pdf.py`, che assembla gli schemi in un unico `.md` e `.html` (rilanciare lo script dopo qualsiasi modifica agli schemi). Il passaggio finale a PDF è **manuale**, con Chrome headless:

```
python3 build_pdf.py
/opt/pw-browsers/chromium-*/chrome-linux/chrome --headless --disable-gpu \
  --no-sandbox --no-pdf-header-footer \
  --print-to-pdf="$PWD/Dispensa Politica Economica.pdf" \
  "file://$PWD/Dispensa Politica Economica.html"
```

Lo stesso comando, cambiando nome al file, rigenera i fogli in `giornate/`.

L'ordine dei capitoli nel PDF segue la **priorità**, non la numerazione dei file: i core (1, 2, 3, 4, **11**) vengono per primi, poi i secondari (5, 6, 7, 8, **13**, **12**), poi le coperture di sicurezza (9, 10, **14**), e in coda la banca domande. Il **quaderno di esercizi** sta davanti a tutto, subito dopo il formulario: è materiale di lavoro quotidiano, non di lettura.

## Come orientarsi nei file sorgente

- **`PROGRESSO.md`** — a che punto è arrivato Jacopo: esercizi fatti, errori intercettati e corretti, punti deboli ancora aperti, calendario spuntato giorno per giorno. Prima cosa da leggere se si riprende il lavoro in una sessione nuova.
- **`CONVENZIONI-ESERCIZI.md`** — come sono fatti gli esercizi che si generano di volta in volta (nei fogli di `giornate/` e nei ripassi improvvisati): struttura, regole non negoziabili sui numeri e sulla verifica, istruzioni per generare il PDF di un nuovo giorno restando coerenti con quelli già fatti.
- **`schemi/00c-mappa-priorita.md`** — vista d'insieme argomento → priorità → tipo di esercizio, prima di aprire la dispensa.
- **`schemi/00b-glossario-simboli.md`** — i simboli (i, r, Q, MC, FBS, EEG...) usati in schemi diversi, fissati in un unico posto per evitare confusione.
- **`schemi/00a-formulario.md`** — tutte le formule chiave per il ripasso last-minute, con rimando allo schema che le spiega.
- **`schemi/00e-quaderno-esercizi.md`** — **23 tracce da svolgere a mano**, con le soluzioni in una sezione separata in fondo. Contiene anche nove **schede-procedura** (come riconosci l'esercizio, i passi in ordine, l'errore tipico) e il calendario degli ultimi giorni prima dell'esame. Cinque tracce (A1, A2, A3, B3, B10) sono **esercizi proposti dalla professoressa** nelle slide e mai svolti a lezione, recuperati da `appunti-grezzi/`.
- **`schemi/00d-domande-preselezione.md`** — 68 domande a risposta multipla su tutti e 14 gli argomenti, con risposte e rimando allo schema, più **tre simulazioni cronometrate da 11 domande** per allenare i 55 secondi a domanda della preselezione.
- **`schemi/`** — gli schemi di studio veri e propri. Ogni schema ha in testa le domande d'esame collegate e chiude con un esercizio tipo svolto (dove pertinente). ⚠️ **Il numero del file non indica la priorità**: gli schemi 01-10 sono ordinati per priorità, gli 11-14 sono stati aggiunti in un secondo momento per coprire capitoli del programma che nei compiti passati non erano mai comparsi, e alcuni di essi (11 e 13) sono più importanti di schemi con numero più basso. La priorità sta nella colonna dedicata della mappa.
- **`giornate/`** — i **fogli di lavoro giornalieri**, uno per giorno del calendario del quaderno: teoria minima, tutorial svolto passo passo, tracce del giorno e soluzioni in coda. Sono autosufficienti (non serve aprire la dispensa) e passano dalla stessa pipeline di `build_pdf.py`, quindi dagli stessi cinque controlli automatici. Ogni foglio genera un PDF a sé.
- **`grafici/`** — i grafici richiamati negli schemi (SVG disegnati a mano, non generati da AI, per garantire precisione su assi/curve/etichette): IS-LM con crowding-out, AD-AS domanda/costi, curva di Phillips, monopolio+perdita secca, monopolio naturale/contendibile, esternalità, Edgeworth/Pareto, Mundell-Fleming, Lorenz/Gini.
- **`appunti-grezzi/`** — trascrizioni fedeli dei PDF sorgente, per argomento. Fonte per generare nuovi esercizi senza rileggere i PDF originali.
- **`pdf-fonte/`** — i PDF originali del corso (esclusa da git, materiale della docente).

## Mappa priorità

Stabilita analizzando **8 compiti/esercitazioni d'esame passati** per gli schemi 01-10; gli schemi 11-14 sono stati aggiunti dopo il confronto con appunti di altri studenti dello stesso corso (vedi sotto) e collocati in base al peso che hanno nel programma del manuale.

**Core — quasi certi all'esame:**
1. `01-politica-fiscale-bilancio-pubblico.md` — bilancio, debito/PIL, teorema di Haavelmo
2. `02-inflazione-curva-phillips.md` — curva di Phillips, curva dei salari, AD-AS
3. `03-concorrenza-imperfetta-monopolio.md` — monopolio, monopolio naturale, mercati contendibili, antitrust, privatizzazioni
4. `04-economia-benessere-teoria-normativa.md` — Pareto, FBS, Primo e Secondo Teorema, second best
5. `11-teoria-normativa-obiettivi-strumenti.md` — obiettivi/strumenti/modello, regola aurea di Tinbergen, assegnazione appropriata, incoerenza temporale ⭐ **il capitolo che dà il nome al corso**

**Secondari — comparsi una volta, o con esercizio articolato:**
6. `05-mercato-del-lavoro.md` — tassi di attività/occupazione/disoccupazione
7. `06-economia-aperta-bilancia-pagamenti.md` — modello IS-LM-BP, riserve ufficiali, Marshall-Lerner e curva a J, dazi e costi comparati
8. `07-teorie-macro-moneta-bce.md` — teorie macro comparate, moneta, canali di creazione della base monetaria, BCE
9. `08-esternalita-fallimenti-mercato.md` — esternalità, tassa pigouviana, beni pubblici, asimmetrie informative, cambiamento climatico
10. `13-valutazione-progetti-acb.md` — VAN, TIR, prezzi ombra ⭐ **l'unico degli argomenti aggiunti con un esercizio numerico proprio**
11. `12-fallimenti-stato-political-economy.md` — le tre cause, ciclo di Nordhaus, doppio problema di agenzia, corruzione

**Copertura di sicurezza — mai comparsi nei compiti passati, ma esposti alla preselezione:**
12. `09-crescita-sviluppo.md` — misurazione PIL, crescita vs sviluppo, legge di Okun, indicatori alternativi
13. `10-disuguaglianze-stato-sociale.md` — disuguaglianze economiche e di genere, Stato Sociale, redistribuzione
14. `14-sistema-monetario-internazionale.md` — cambi fissi vs flessibili, gold standard, Bretton Woods, dilemma di Triffin

## Come si scrivono le formule

Il PDF è generato da `build_pdf.py` con `python-markdown`, che **non traduce il LaTeX**: una formula scritta con `$...$` o `\frac{}{}` finisce nel PDF come codice grezzo e diventa illeggibile. In più, un trattino basso o un asterisco fuori posto può essere interpretato come comando di formattazione e **far sparire pezzi di testo**. Da qui la convenzione:

**1. Formula in evidenza → blocco recintato con tre apici inversi.** Dentro un blocco markdown non tocca nulla: nessun carattere può essere mangiato.

**2. Subito sotto, la legenda dei simboli**, introdotta da `**dove:**`, con un punto elenco per simbolo. Va messa dove il simbolo compare **la prima volta in quello schema** — ogni schema deve essere autosufficiente.

**3. Frazioni composte su due righe**, con la linea di frazione `─` (U+2500). Il font monospace del PDF (DejaVu Sans Mono) copre `─ │ · × − ≈ √ Σ ε θ π Δ` e pedici/apici. Le frazioni semplici restano in linea, con `/`.

**4. Pedici e apici si scrivono `Q_M` e `(1+i)^t`** nel sorgente, e `build_pdf.py` li trasforma in pedici e apici **tipografici veri** al momento di generare l'HTML. Il sorgente resta leggibile, il PDF esce come il manuale. Per un pedice lungo o composto si usano le parentesi: `Y_(t−1)`, mai le graffe LaTeX.

**5. Simboli citati nel testo scorrevole → fra apici inversi singoli**: `` `L_d` ``, `` `MC_S` ``. Protegge allo stesso modo, e li fa risaltare.

Esempio completo:

    ```
                 p · e
          e_r = ───────
                   p_w
    ```

    **dove:**
    - `e_r` = tasso di cambio reale (competitività)
    - `p` = prezzi interni · `p_w` = prezzi esteri
    - `e` = tasso di cambio nominale

**Il controllo automatico.** `build_pdf.py` verifica a ogni generazione che non ci siano `$`, comandi LaTeX, graffe nei pedici o corsivi inventati da markdown, **e che numeratori e denominatori restino centrati sulla barra di frazione** (il pedice reso è più stretto del sorgente, quindi le frazioni allineate a occhio si spostano). Stampa **file e numero di riga** di ogni problema. Se stampa `Controllo formule: nessun problema rilevato`, il PDF è pulito. Non blocca la generazione: avvisa.

## Provenienza delle fonti

| Fonte | Copre |
|---|---|
| **PDF della professoressa** (37 file, `pdf-fonte/`, trascritti in `appunti-grezzi/`) | Tutti gli schemi **tranne il 14**, e tranne le sezioni 9-13 dello schema 11 |
| **Manuale Paesani** (II ed.), via appunti di altri studenti dello stesso corso | Schema 14 (interamente) · schema 11 §9-13 (critica di Lucas, teoria dei giochi, incoerenza temporale, banchiere conservatore) · schema 12 §5-7 (Nordhaus, doppio problema di agenzia, corruzione) · teorema del second best (schema 04) |

Le sezioni che dipendono **solo** dalla seconda fonte sono marcate nel testo con la dicitura *(manuale)* o con un avviso in testa allo schema: sono materiale del testo di riferimento, ma non abbiamo la conferma che la docente le abbia trattate a lezione.

## Materiale scartato (valutato e giudicato non prioritario)

- **"I sistemi di pagamento" (seminario BdI)** — slide tecnico-operative di un relatore esterno, scollegate dai temi d'esame.
- **"Lezioni F. Caffè - Dicembre 2025"** — ciclo di conferenze di ricerca avanzata (relatore esterno Guido Lorenzoni), non materiale del programma ufficiale.

## ⚠️ Punti da verificare prima dell'esame

Alcuni esercizi tipo negli schemi sono stati ricostruiti dagli agenti perché i PDF del corso contengono solo teoria/grafici, senza gli esercizi numerici specifici visti nei compiti passati. Andrebbero controllati con la professoressa o in un'esercitazione:

- **Schema 02 (Phillips)**: la curva dei salari usata nell'esercizio (ẇ=0,55-5u) non è nei due PDF letti — verificare i numeri esatti sul compito originale.
- ~~**Schema 03 (monopolio)**: convenzione sulla doppia radice nel mercato contendibile~~ → **risolto**: appunti di altri studenti dello stesso corso confermano che negli esercizi si impone **P = costo medio** e si tiene la radice maggiore (l'unica hit-and-run-proof), che è esattamente il metodo usato nel nostro esercizio. Restano ricostruiti con metodo standard di microeconomia gli altri due esercizi (perdita secca, monopolio naturale).
- **Schema 04 (benessere)**: l'esercizio a 3 individui/3 stati è ricostruito da zero, coerente con le formule delle slide ma non è un esempio del corso.
- **Schema 06 (economia aperta)**: l'esercizio IS-LM-BP fornito manca del dato di offerta di moneta o tasso d'interesse — il reddito di equilibrio non è calcolabile come numero unico senza quel dato. Verificare "Esercitazione ec aperta.pdf" per il valore mancante. *(Aggirato: l'esercizio B5 del [quaderno](schemi/00e-quaderno-esercizi.md) è una versione completa e risolvibile dello stesso modello, con l'offerta di moneta data.)*

## Non coperti dai compiti passati (ma presenti nel programma)

Crescita e sviluppo, disuguaglianze, Stato sociale, cambiamento climatico, teoria normativa operativa, fallimenti dello Stato, valutazione dei progetti pubblici e sistema monetario internazionale **non sono mai comparsi** negli 8 compiti/esercitazioni analizzati. Con la **preselezione a risposta multipla** il rischio è però concreto: le 11 domande possono pescare ovunque nel programma, e una domanda su un argomento mai visto costa quanto una sui core.

Gli schemi 09, 10, 12 e 14 vanno quindi letti almeno a livello di **definizioni e classificazioni**, anche se per lo scritto restano meno probabili. Gli schemi **11 e 13** sono un caso diverso: non erano nei compiti passati, ma sono pienamente coperti dai PDF della docente e il 13 è **esercizio-shaped** (VAN/TIR) — vanno studiati come i core.

## Cronologia degli aggiornamenti

- **Costruzione iniziale**: 10 schemi dai 37 PDF della docente, con priorità tarata su 8 compiti passati.
- **28/08/2026 — struttura della prova**: registrate le modalità d'esame 2026-2027 (preselezione, scritto, orale) e le date d'appello.
- **28/08/2026 — chiusura dei buchi**: dal confronto con appunti completi di un altro studente dello stesso corso (82 pagine, sui 16 capitoli del Paesani) sono emersi 4 capitoli scoperti → aggiunti gli schemi **11, 12, 13, 14** e la banca domande **00d**; integrati negli schemi esistenti second best, efficienza "x" e dinamica, legge di Okun, curva a J e ipotesi di Marshall-Lerner, beggar-my-neighbour e dumping sociale, privatizzazioni, canali di creazione della base monetaria e divorzio Banca d'Italia-Tesoro, cause del debito italiano anni '80, ed esempi numerici (faro, lemons, costi comparati, dazio, fiscal drag).
