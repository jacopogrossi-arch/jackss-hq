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

**`Dispensa Politica Economica.pdf`** — il documento unico da cui studiare: 71 pagine, con struttura della prova e indice cliccabile in prima pagina che rimanda a ogni capitolo, tutti gli schemi + formulario + glossario + mappa di priorità + i 9 grafici, in ordine di priorità. Generato da `build_pdf.py` (Python + Chrome headless — rilanciare lo script dopo qualsiasi modifica agli schemi per rigenerare il PDF).

## Come orientarsi nei file sorgente

- **`schemi/00c-mappa-priorita.md`** — vista d'insieme argomento → priorità → tipo di esercizio, prima di aprire la dispensa.
- **`schemi/00b-glossario-simboli.md`** — i simboli (i, r, Q, MC, FBS, EEG...) usati in schemi diversi, fissati in un unico posto per evitare confusione.
- **`schemi/00a-formulario.md`** — tutte le formule chiave per il ripasso last-minute, con rimando allo schema che le spiega.
- **`schemi/`** — gli schemi di studio veri e propri, in ordine di priorità (numero crescente = priorità decrescente). Ogni schema ha in testa le domande d'esame reali collegate e chiude con un esercizio tipo svolto (dove pertinente).
- **`grafici/`** — i grafici richiamati negli schemi (SVG disegnati a mano, non generati da AI, per garantire precisione su assi/curve/etichette): IS-LM con crowding-out, AD-AS domanda/costi, curva di Phillips, monopolio+perdita secca, monopolio naturale/contendibile, esternalità, Edgeworth/Pareto, Mundell-Fleming, Lorenz/Gini.
- **`appunti-grezzi/`** — trascrizioni fedeli dei PDF sorgente, per argomento. Fonte per generare nuovi esercizi senza rileggere i PDF originali.
- **`pdf-fonte/`** — i PDF originali del corso (esclusa da git, materiale della docente).

## Mappa priorità (da analisi di 8 compiti/esercitazioni passati)

**Core — compaiono ripetutamente, quasi certi all'esame:**
1. `01-politica-fiscale-bilancio-pubblico.md` — bilancio, debito/PIL, teorema di Haavelmo
2. `02-inflazione-curva-phillips.md` — curva di Phillips, curva dei salari, AD-AS
3. `03-concorrenza-imperfetta-monopolio.md` — monopolio, monopolio naturale, mercati contendibili, antitrust
4. `04-economia-benessere-teoria-normativa.md` — Pareto, FBS, Primo Teorema

**Secondari — comparsi una volta, ma con esercizio articolato:**
5. `05-mercato-del-lavoro.md` — tassi di attività/occupazione/disoccupazione
6. `06-economia-aperta-bilancia-pagamenti.md` — modello IS-LM-BP, riserve ufficiali
7. `07-teorie-macro-moneta-bce.md` — teorie macro comparate, moneta, politica monetaria BCE
8. `08-esternalita-fallimenti-mercato.md` — esternalità, tassa pigouviana, cambiamento climatico (appendice)

**Zona a rischio — mai comparsi nei compiti passati, ma esposti alla preselezione a risposta multipla:**
9. `09-crescita-sviluppo.md` — misurazione PIL, crescita vs sviluppo, indicatori alternativi
10. `10-disuguaglianze-stato-sociale.md` — disuguaglianze economiche e di genere, Stato Sociale, redistribuzione (accorpa 4 PDF diversi)

## Materiale scartato (valutato e giudicato non prioritario)

- **"I sistemi di pagamento" (seminario BdI)** — slide tecnico-operative di un relatore esterno, scollegate dai temi d'esame.
- **"Lezioni F. Caffè - Dicembre 2025"** — ciclo di conferenze di ricerca avanzata (relatore esterno Guido Lorenzoni), non materiale del programma ufficiale.

## ⚠️ Punti da verificare prima dell'esame

Alcuni esercizi tipo negli schemi sono stati ricostruiti dagli agenti perché i PDF del corso contengono solo teoria/grafici, senza gli esercizi numerici specifici visti nei compiti passati. Andrebbero controllati con la professoressa o in un'esercitazione:

- **Schema 02 (Phillips)**: la curva dei salari usata nell'esercizio (ẇ=0,55-5u) non è nei due PDF letti — verificare i numeri esatti sul compito originale.
- **Schema 03 (monopolio)**: i tre esercizi (perdita secca, monopolio naturale, mercato contendibile) sono risolti con metodo standard di microeconomia, non con esempi del corso — controllare in particolare la convenzione sulla doppia radice nel caso di mercato contendibile.
- **Schema 04 (benessere)**: l'esercizio a 3 individui/3 stati è ricostruito da zero, coerente con le formule delle slide ma non è un esempio del corso.
- **Schema 06 (economia aperta)**: l'esercizio IS-LM-BP fornito manca del dato di offerta di moneta o tasso d'interesse — il reddito di equilibrio non è calcolabile come numero unico senza quel dato. Verificare "Esercitazione ec aperta.pdf" per il valore mancante.

## Non coperti dai compiti passati (ma presenti come lezioni)

Crescita e sviluppo, disuguaglianze (economiche e di genere), Stato sociale, cambiamento climatico non sono mai comparsi nei compiti/esercitazioni analizzati. Non significa che siano esclusi dall'esame — e con la preselezione a risposta multipla il rischio è concreto, perché le 11 domande possono pescare ovunque nel programma. Gli schemi 09-10 vanno quindi letti almeno una volta a livello di definizioni e indicatori (PIL e alternative, Lorenz/Gini, pilastri dello Stato sociale), anche se per lo scritto restano meno probabili dei core 1-4.
