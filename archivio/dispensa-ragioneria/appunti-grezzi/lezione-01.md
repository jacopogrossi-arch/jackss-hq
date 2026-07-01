# Lezione 1 — Sistema Informativo Aziendale, Sistema Informativo Contabile, Libri Contabili

Corso di Ragioneria, Scienze Aziendali, Canale (E-M), a.a. 2024/2025 — Prof. Flaviano Moscarini, Sapienza Università di Roma.

## Argomento della lezione

Introduzione al Sistema Informativo Aziendale (SIA) e agli ERP, al Sistema Informativo Contabile (contabilità generale vs contabilità direzionale), ai libri contabili obbligatori (civilistici e fiscali) e ai libri sociali obbligatori. Appendice finale su metodo "tradizionale" vs "meccanografico" di rappresentazione delle scritture in partita doppia, con tre esempi numerici svolti.

## Concetti e definizioni chiave

- **Sistema informativo aziendale (SIA)**: "l'insieme dei processi che consentono la raccolta, l'elaborazione e la conservazione dei dati inerenti ai flussi di lavoro aziendali e la produzione di informazioni utilizzate ai fini decisionali."
- **Sottosistemi informativi**: il SIA è articolato in sottosistemi informativi che si differenziano per gli obiettivi perseguiti oppure per la natura/origine dei dati rilevati o impiegati. I sottosistemi più importanti gestiscono i dati del "ciclo del lavoro", "del ciclo delle vendite" e quelli che utilizzano il "conto" come strumento di rilevazione dei riflessi economico-patrimoniali-finanziari della gestione d'impresa (sottosistema informativo contabile).
- **Enterprise Resources Planning (ERP)**: insieme di software di gestione dei dati aziendali che consentono la digitalizzazione e l'automazione dei flussi di lavoro aziendali. Composto di "moduli" software gestionali modulari che in genere "dialogano" tra loro condividendo set e flussi di dati (es. software di contabilità, CRM). Esempi citati a slide: SAP, Dynamics 365, SaaS, TeamSystem, Zucchetti.
- **Sistema Informativo Contabile**: sottosistema del SIA finalizzato a fornire a determinate categorie di stakeholder (interni o esterni) informazioni di natura economica, patrimoniale e finanziaria; in genere (ma non sempre) utilizza il "conto" come strumento di rilevazione.
- **Contabilità generale**: "sistema (sottosistema informativo contabile) finalizzato alla rilevazione dei fatti amministrativi aziendali «esterni»." L'oggetto è la rilevazione di fatti che determinano scambi di diversa natura (denaro, beni, lavoro) tra l'azienda e una terza economia (fornitore, banca, lavoratore, ecc.), ovvero la rilevazione di fatti/eventi che incidono sull'economia dell'impresa (es. svalutazione di una valuta estera che incide sul valore recuperabile in valuta di conto di un credito).
  - Ripetuta anche a p.4 con formulazione leggermente diversa: "sistema di rilevazione dei fatti amministrativi esterni finalizzato a determinare il risultato economico dell'esercizio e la consistenza del patrimonio netto (o capitale di funzionamento) alla fine del periodo."
- **Bilancio e informativa esterna**: documento di natura "contabile" (deriva dalle informazioni prodotte dalla contabilità generale) redatto secondo norme generali e regole "tecniche" definite/accettate da autorità pubbliche (legislatore e standard setter) o generalmente condivisibili, finalizzato a informare soci e altri stakeholder dell'andamento della gestione nel corso dell'esercizio e della consistenza/composizione del patrimonio.
- **Contabilità direzionale**: informazioni e dati estratti dall'ERP ed elaborati in base alle esigenze conoscitive del decision maker interno (es. direzione aziendale). Ne fanno parte la Contabilità Analitica/Industriale e ogni altra informazione finalizzata a misurare le performance aziendali.
- Le informazioni di contabilità generale e direzionale sono usate anche per prospetti con dati previsionali (budget, business plan, ecc.).
- **Partita doppia (PD)**: tecnica di rilevazione comunemente impiegata in tutto il mondo. Prevede la rilevazione degli importi in appositi "conti" (mastri/mastrini) che funzionano a sezioni contrapposte (dare/avere), così che per ciascuna scrittura vengono movimentati almeno due o più conti e il totale degli importi imputati nelle sezioni contrapposte deve coincidere.
- **Libro Mastro**: libro che raccoglie i conti (mastri, mastrini, schede contabili).
- **Libro giornale**: libro dove le scritture che movimentano i conti vengono registrate in ordine cronologico.
- **Registro dei beni ammortizzabili (o Libro cespiti)**: completa il sistema di contabilità generale; accoglie i mastri "accesi" ai costi ad utilità pluriennale soggetti ad ammortamento.

## Libri contabili — normativa e regimi

- **Art. 2214 c.c.**: "l'imprenditore che esercita un'attività commerciale deve tenere il libro giornale e il libro degli inventari. Deve altresì tenere le altre scritture contabili che siano richieste dalla natura e dalle dimensioni dell'impresa e conservare ordinatamente per ciascun affare gli originali delle lettere, dei telegrammi e delle fatture ricevute, nonché le copie delle lettere, dei telegrammi e delle fatture spedite. Le disposizioni di questo articolo non si applicano ai piccoli imprenditori".
- Dal punto di vista fiscale (**DPR 600/1973**) distinguiamo tra imprese che operano in:
  - **Regime di contabilità ordinaria** (incluse tutte le S.p.A., S.r.l., ecc.)
  - **Regime di contabilità semplificata** (società di persone e ditte individuali — imprese minori con volume d'affari fino a 500 K€ per attività di prestazione di servizi / 800 K€ per altre attività)

### Libri/registri obbligatori per le imprese in regime di contabilità ordinaria (normativa civilistica e fiscale)

- Libro giornale
- Libro mastro
- Registro beni ammortizzabili (o "libro cespiti")
- Libro giornale di magazzino ("scritture ausiliarie di magazzino")
- Libro inventari
- Registri IVA (DPR 633/1972 — Decreto IVA):
  - Registro delle fatture emesse
  - Registro dei corrispettivi (per i commercianti al minuto)
  - Registro degli acquisti

Nota della slide: "Nelle slide seguenti sono riportati degli «screen shot» tratti da software contabili. È ovvio che la modalità di rappresentazione di una scrittura o di un conto o di un libro contabile varia a seconda del software contabile utilizzato."

### Esempi da software contabili reali (screenshot, dati anonimizzati)

- **Libro giornale** (estratto Gruppo X S.p.A.): formato con colonne Data | Rif.registraz./N.Reg.giornale | Conto/Partitario | Causale | Rif. documento | DARE | AVERE. Esempio di righe: 22/03/17 conto 550301 "Acq.beni materiali per produz. serviz" (Dare 153,00), conto 350101 "IVA su acquisti" (Dare 33,66), conto 330301 "GDS MEDIA&COMMUNICATION SRL" (Dare 1.000,00), conto 750107 "Commissioni e spese bancarie" (Dare 0,69), conto 190101 "MONTE DEI PASCHI DI SIENA" (Avere 1.000,69).
- **Libro mastro** (estratto Gruppo X S.p.A.): "Scheda contabile" per Conto 19.01.01 Banca c/c, Partitario "MONTE DEI PASCHI DI SIENA", con colonne Data/Numero registrazione, Causale, Riferimenti documento, Importo Dare, Importo Avere, Saldo progressivo (es. saldo che scende da 132.148,77 a 3.548,82 nel periodo osservato).
- **Libro giornale — libro mastro** (estratto Fin xx SRL): esempio con fatture di acquisto da "ANxxxx CONSULTING SRL" per consulenze gestionali contabili (conto 04.05.905), imponibile 500,00 + IVA 110,00 (conto 01.33.002 IVA c/acquisti); il libro mastro del conto "Consulenze gestionali contabili" mostra tre fatture mensili da 500,00 ciascuna con saldo progressivo che arriva a 1.500,00.
- **Registro beni ammortizzabili** (estratto Fin xx SRL, art. 16 DPR 600/73): esempio concreto per un Cespite "Fabbricato commerciale Via Trionfale" — Categoria 001 Fabbricati industriali e commerciali, Coeff. min. fisc. 3,000%, Costo storico 1.169.328,31, Amm. ord. prec. 140.200,02, %le 1,500, Amm. ordin. (quota dell'anno) 17.539,92, Residuo 1.011.588,37.
- **Registro IVA acquisti** (estratto Fin xx SRL): esempio Mese di Marzo 2016, righe con Data reg./Numero protocollo/Data doc./Descrizione/O T A N.I./Totale doc./Imponibile IVA/Imposta/Note; aliquota IVA 22% su due fatture (300,00 e 8.580,00 di imponibile); tabella di riepilogo IVA con voci: 22% Aliquota iva 22%, A10 Esente art.10, A15 Escluso art.15, A27 N.I. art. 27 del DL 98/2011; legenda codici O (Operatività: F=Fattura, N=Nota accredito, C=Corrispettivo, S=Storno corrispettivo, I=Incasso, D=Documento di spesa/ricavo, R=Ricevuta fiscale, U=Storno ricevuta fiscale), A (Area: I=Italiano, C=Comunitario, E=Extracomunitario, S=San Marino, V=Vaticano), T (Tipo: E=Esigibilità differita, A=Autofattura, I=Acquisti con autofattura, S=Subfornitura, D=Incasso/Pagamento esigibilità differita, C=Autofattura per autoconsumo, G=Esigibilità per cassa, H=Incasso/Pagamento esigibilità per cassa, P=IVA versata dal committente art. 17-ter scissione dei pagamenti).
- **Scritture ausiliarie di magazzino** (estratto): "Giornale di Magazzino" con colonne Data Reg./Data Doc./Numero Doc./Cod. Descr. Causale/Cod. CLI-FOR/Codice Articolo/Descrizione Articolo/UM/Dep/Tipo Mov./Qtà Carico/Qtà Scarico — esempio con movimenti "Scarico per vendite", "Carico libero", "Scarico libero" per un articolo (G0119, camomilla) in vari depositi (D1, A2, B1, A1).

### Esempio didattico semplice (Libro giornale e Libro mastro)

**Caso**: "Pagata in giornata la fattura per acquisto di merci con rilascio di assegno bancario."

Libro giornale in partita doppia:

| Data | Conti | Dare | Avere |
|---|---|---|---|
| 27/12 | Debiti v/ fornitori | 1.800,00 | |
| 27/12 | Banca c/c | | 1.800,00 |

Libro mastro aggiornato in base al giornale di contabilità (mostra anche la scrittura originaria di acquisto, non esplicitata nel dettaglio ma desumibile dai saldi dei mastrini):

- **Merci c/acquisti**: Dare 1.500,00
- **Iva ns. credito**: Dare 300,00
- **Debiti v/ Fornitori**: Dare 1.800,00 (pagamento) — Avere 1.800,00 (fattura originaria) → saldo a zero
- **Banca c/c**: Avere 1.800,00

(Nota: la slide mostra graficamente le frecce di riporto dal libro giornale ai singoli mastrini — Debiti v/Fornitori si chiude a saldo zero dopo il pagamento, la Banca c/c si movimenta in Avere per l'uscita di cassa/assegno).

## Libro giornale — regole di tenuta

- Obbligatorio per tutti i soggetti titolari di reddito di impresa in regime di contabilità ordinaria. È un registro cronologico nel quale devono essere trascritte tutte le operazioni relative all'esercizio dell'impresa. Ogni operazione deve essere caratterizzata da: data, descrizione, rappresentazione contabile e importi relativi distinti per mastri.
- Tutte le operazioni devono essere perentoriamente trascritte sul Libro giornale **entro e non oltre 60 giorni dal loro accadimento** (data in cui l'operazione è stata effettuata o data in cui l'azienda ne è venuta a conoscenza).
- Il Libro Giornale deve essere "stampato" (fisicamente o in formato digitale pdf) **entro l'ultimo giorno del terzo mese successivo al termine di presentazione della Dichiarazione dei Redditi** (di norma la Dichiarazione dei Redditi deve essere presentata entro il 30 settembre dell'anno successivo a cui si riferisce → quindi la scadenza per la "stampa" del libro giornale è di norma il **31 dicembre**).
- Sul libro giornale "stampato" devono essere apposte delle **marche da bollo**.
- Abbinata alla stampa del Libro Giornale vi è la stampa dei mastrini/partitari, nella quale devono essere contenute tutte le movimentazioni contabili registrate. **Tuttavia la stampa del Libro Mastro non è obbligatoria.**

## Libro inventari — regole di tenuta

- Deve contenere l'indicazione e la valutazione delle attività e delle passività relative all'impresa, nonché delle attività e delle passività dell'imprenditore, estranee alla stessa (es. beni di terzi in leasing o noleggio). Necessario anche ai fini fiscali, in quanto previsto dall'**art. 15 DPR 600/1973** fra le scritture obbligatorie degli imprenditori commerciali.
- Fornisce una "fotografia" della composizione e della valutazione del patrimonio aziendale alla fine dell'esercizio.
- Dal libro devono emergere una parte sintetica (Stato Patrimoniale, Conto Economico e Nota Integrativa) e una analitica (consistenza di ciascun bene aziendale e valore attribuito).
- Sul libro inventari stampato devono essere apposte marche da bollo.
- Deve essere stampato entro lo stesso termine del libro giornale (ultimo giorno del terzo mese successivo al termine di presentazione della Dichiarazione dei Redditi, quindi di norma il 31 dicembre).

## Registro dei beni ammortizzabili e Scritture Ausiliarie di Magazzino — regole di tenuta

- **Registro dei beni ammortizzabili (libro cespiti)**: racchiude tutte le informazioni inerenti i cespiti di proprietà dell'azienda. In particolare rileva: *anno di acquisizione, costo originario, rivalutazioni o svalutazioni, coefficiente di ammortamento, fondo ammortamento aggiornato al periodo precedente, quota annuale di ammortamento ed eliminazione dal processo produttivo.*
  - Deve essere aggiornato entro il termine di presentazione della Dichiarazione dei Redditi. Non c'è obbligo di stampa, ma deve essere messo a disposizione in caso di verifica da parte delle Autorità (Agenzia delle Entrate e GdF).
- **Scritture ausiliarie di magazzino (libro di magazzino)**: obbligo di tenuta per tutte le imprese che per almeno due periodi di imposta consecutivi: realizzano un volume di ricavi annuo superiore a **5.164.569 Euro**; E dichiarano alla fine del periodo di imposta rimanenze finali per un valore complessivo superiore a **1.032.914 Euro**.
  - Devono essere stampate entro l'ultimo giorno del terzo mese successivo al termine di presentazione della Dichiarazione dei Redditi. Non c'è obbligo di stampa, ma devono essere messe a disposizione in caso di verifica da parte delle Autorità.

## Conservazione digitale "sostitutiva"

- In sostituzione della stampa cartacea dei libri contabili, l'azienda può optare per la conservazione digitale dei documenti.
- La conservazione sostitutiva è una procedura informatica che dà validità legale ai documenti informatici, similmente ai documenti originali cartacei, rendendo un documento digitale a valore probatorio.
- La valenza legale rispetto a forma e contenuto del documento, nonché alla sua data certa, è attestata dalla **firma digitale** e dalla **marcatura temporale** apposte sui documenti:
  - La firma digitale attribuisce al documento un riferimento temporale che corrisponde alla data in cui la firma è apposta ("data certa").
  - La marca temporale rappresenta il servizio offerto da un soggetto che certifica il riferimento temporale della rilevazione, rendendolo opponibile ai terzi.
- La conservazione sostitutiva rende il documento non deteriorabile (diversamente dai registri cartacei soggetti all'usura del tempo), oltre a ridurre i costi di stampa e gli spazi di archiviazione.

## Libri sociali obbligatori

- Oltre ai libri contabili, le imprese che esercitano l'attività in forma "societaria" (es. S.p.A. e S.r.l.) devono tenere determinati libri da cui è possibile desumere lo svolgersi della vita e delle decisioni degli organi sociali.
- Per le società per azioni, i libri sociali obbligatori sono indicati all'**art. 2421 c.c.**

**Art. 2421 c.c. — Libri sociali obbligatori** (testo riportato integralmente a slide):

"Oltre i libri e le altre scritture contabili prescritti nell'articolo 2214 [2519], la società deve tenere:
1. il libro dei soci [2346, 2478], nel quale devono essere indicati distintamente per ogni categoria il numero delle azioni, il cognome e il nome dei titolari delle azioni nominative, i trasferimenti e i vincoli ad esse relativi e i versamenti eseguiti [2355, 2355 bis];
2. il libro delle obbligazioni [2412], il quale deve indicare l'ammontare delle obbligazioni emesse e di quelle estinte, il cognome e il nome dei titolari delle obbligazioni nominative e i trasferimenti e i vincoli ad esse relativi [2414, n. 4, 2418];
3. il libro delle adunanze e delle deliberazioni delle assemblee, in cui devono essere trascritti anche i verbali redatti per atto pubblico [2375];
4. il libro delle adunanze e delle deliberazioni del consiglio di amministrazione [2380-bis, 2388, 2392] o del consiglio di gestione;
5. il libro delle adunanze e delle deliberazioni del collegio sindacale ovvero del consiglio di sorveglianza o del comitato per il controllo sulla gestione;
6. il libro delle adunanze e delle deliberazioni del comitato esecutivo [2381], se questo esiste;
7. il libro delle adunanze e delle deliberazioni delle assemblee degli obbligazionisti [2415], se sono state emesse obbligazioni;
8. il libro degli strumenti finanziari emessi ai sensi dell'articolo 2447 sexies.

I libri indicati nel primo comma, numeri 1), 2), 3), 4) e 8) sono tenuti a cura degli amministratori o dei componenti del consiglio di gestione, il libro indicato nel numero 5) a cura del collegio sindacale ovvero del consiglio di sorveglianza o del comitato per il controllo sulla gestione, il libro indicato nel numero 6) a cura del comitato esecutivo e il libro indicato nel numero 7) a cura del rappresentante comune degli obbligazionisti."

## Altri "libri" obbligatori

- Oltre ai libri previsti dalla normativa civilistica e tributaria, l'impresa è soggetta all'obbligo di tenuta di altri libri e documenti previsti da diverse normative. Uno di questi, opportuno da menzionare, è il **Libro Unico del Lavoro (LUL)**, obbligatorio per tutte le imprese che hanno almeno un lavoratore alle proprie dipendenze.
- All'interno del LUL sono registrati tutti i dati relativi sia al datore di lavoro (impresa) che ai lavoratori.
- Con riferimento al datore di lavoro: ragione sociale, sede di lavoro, posizioni INPS (ai fini delle dinamiche pensionistiche) e INAL/INAIL (assicurazione obbligatoria per infortuni sul lavoro).
- Con riferimento ai lavoratori: dati anagrafici, dati relativi al rapporto di lavoro (data assunzione, qualifica, livello inquadramento, elementi retributivi di base…), dati su variazioni retributive, prestazioni per malattie, maternità/paternità, infortunio, ritenute fiscali e previdenziali.

## Appendice — Metodo "tradizionale" vs metodo "meccanografico"

Sono due modalità di rappresentazione della "registrazione" in Partita Doppia assolutamente equivalenti. Alcuni software gestionali utilizzano il metodo "tradizionale", altri il metodo "meccanografico". Nel corso verranno impiegati entrambi i metodi.

### Metodo "tradizionale"

**Articolo semplice** (un solo conto movimentato in dare e un solo conto movimentato in avere) — schema tabellare:

| Nr. progressivo | Conto movimentato in DARE | a | Conto movimentato in AVERE | Parziali | Totali |
|---|---|---|---|---|---|
| | *Descrizione dell'operazione* | | | | |

**Articolo complesso** (più conti movimentati in dare e più conti movimentati in avere) — schema tabellare "Diversi a Diversi":

| Nr. progressivo | Diversi (conti in DARE) | a | Diversi (conti in AVERE) | Parziali | Totale |
|---|---|---|---|---|---|
| | Conto movimentato in DARE / Conto movimentato in DARE | a / a | Conto movimentato in AVERE / Conto movimentato in AVERE | Parziali / Parziali | |
| | *Descrizione dell'operazione* | | | Parziali / Parziali | |

### Metodo "meccanografico"

Schema tabellare a colonne: Nr. progressivo | Data operazione | Nome del conto movimentato | Valore in DARE | Valore in AVERE (righe separate per ciascun conto movimentato, senza la notazione "a"/"Diversi a Diversi").

## Esempi numerici svolti (con scrittura contabile completa, entrambi i metodi)

### Esempio 1 — Acquisto di merce

**Testo**: acquisto di merce dal fornitore Alfa SpA per euro 1.000 + IVA al 22%.

Metodo tradizionale:

| Diversi | a | Fornitore Alfa SpA | | 1.220 |
|---|---|---|---|---|
| Merci c/acquisto | | | 1.000 | |
| Iva a Credito | | | 220 | |
| *Acquisto di merce da Alfa* | | | | |

Metodo meccanografico:

| Nome del conto movimentato | Valore in DARE | Valore in AVERE |
|---|---|---|
| Merci c/acquisto | 1.000 | |
| Iva a Credito | 220 | |
| Fornitore Alfa SpA | | 1.220 |

### Esempio 2 — Cessione di merce

**Testo**: cessione di merce al cliente Beta SpA per euro 1.000 + IVA al 22%.

Metodo tradizionale:

| Cliente Beta SpA | a | Diversi | | 1.220 |
|---|---|---|---|---|
| | | Merci c/vendite | | 1.000 |
| | | IVA a debito | | 220 |
| *Cessione di merce a Beta* | | | | |

Metodo meccanografico:

| Nome del conto movimentato | Valore in DARE | Valore in AVERE |
|---|---|---|
| Merci c/vendite | | 1.000 |
| Iva a Debito | | 220 |
| Cliente Beta SpA | 1.220 | |

### Esempio 3 — Cessione di un impianto (con minusvalenza)

**Testo**: cessione di un impianto al cliente Delta SpA per euro 1.000 + IVA al 22%. Il valore contabile netto dell'impianto è pari a 1.100 (quindi si deve rilevare la minusvalenza). Per semplicità si ipotizza che il fondo ammortamento sia pari a zero.

Metodo tradizionale ("Diversi a Diversi"):

| Diversi | a | Diversi | | |
|---|---|---|---|---|
| Cliente Delta SpA | | | 1.220 | |
| Minusvalenza | | | 100 | |
| | a | Impianti | | 1.100 |
| | a | IVA a debito | | 220 |

Metodo meccanografico:

| Nome del conto movimentato | Valore in DARE | Valore in AVERE |
|---|---|---|
| Cliente Delta SpA | 1.220 | |
| Minusvalenza | 100 | |
| Impianti | | 1.100 |
| IVA a debito | | 220 |

Nota: la minusvalenza (100) è calcolata come differenza tra il valore contabile netto del bene (1.100) e il corrispettivo di cessione al netto IVA (1.000): 1.100 − 1.000 = 100 di minusvalenza (perdita da cessione).

## Riferimenti normativi citati in questa lezione

- Art. 2214 c.c. (obbligo libro giornale e libro degli inventari, esonero piccoli imprenditori)
- DPR 600/1973 (regimi di contabilità ordinaria/semplificata; art. 15 — libro inventari fra le scritture obbligatorie; art. 16 — registro dei beni ammortizzabili)
- DPR 633/1972 — "Decreto IVA" (registri IVA: fatture emesse, corrispettivi, acquisti)
- Art. 2421 c.c. (libri sociali obbligatori delle società per azioni, con rimandi interni a 2346, 2478, 2355, 2355-bis, 2412, 2414 n.4, 2418, 2375, 2380-bis, 2388, 2392, 2381, 2415, 2447-sexies, 2519, 2214)
