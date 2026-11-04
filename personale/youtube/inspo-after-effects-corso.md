# Corso After Effects: come ragiona e quali curve usa

*Analisi del 04/11/2026 sulle registrazioni in `Videos\Architettura Mentali 2`. Trascritti e frame stanno solo in locale, in `videos/inspo-after-effects/` (corso a pagamento, fuori da git).*

## In breve

**Serve, ma per il metodo: il programma non ci riguarda.** Noi montiamo con HyperFrames, quindi metà del corso (pannelli, plugin, Animation Composer) non si trasferisce. Si trasferiscono tre cose:

1. **La curva di velocità.** È il motivo per cui i suoi movimenti sembrano fluidi, ed è diversa da tutte quelle che usa oggi la skill.
2. **Il ragionamento:** collegare gli elementi tra loro invece di animarli uno a uno, e partire sempre da un riferimento.
3. **La regola "mantieni vivo l'effetto"**, che è la tua nota "mai ferma" detta da un'altra persona.

## Video per video

Sono parti del corso "Cash Flow Contents". Legenda: **Metodo** = serve per fare motion graphics come le sue. **Altro** = non è metodo di animazione, ma si collega a qualcosa che abbiamo. **Salta** = si può ignorare.

| Video | Lezione | Di cosa parla | Valore per noi |
|---|---|---|---|
| v1 `08-15-58` | Architettura Mentale 1 | Denaro, genitori, onde cerebrali, sogni | Solo come Altro, con cautela |
| v2 `12-15-47` | AE 1 | Interfaccia e concetti base | Basso |
| v3 `12-33-52` | AE 2 | Forme, sfumature, grafico di velocità | **Il più importante** |
| v4 `13-01-11` | AE 3 | Titolo animato, collegare i livelli | Alto |
| v5 `13-49-38` | AE 4 | Shape morphing, tracciato Bézier | Alto |
| *mancante* | AE 5 | Maschere e Continua Testi | Non registrata |
| v6 `14-20-28` | AE 6 | Motion tracking | Medio |
| v7 `14-51-15` | AE 7 | Lock-on tracking | Medio |

Le code di v4 (dopo 39:00), v5 (dopo 20:30) e v7 (dopo 13:05) sono solo schermate ferme: lì non c'è nulla.

### v1: Architettura Mentale (23 min)

| Minuto | Cosa | Tipo | Collegamento |
|---|---|---|---|
| 02:14 | Elenco dei blocchi: alzare i prezzi, esporsi, metterci la faccia, "non sono pronto" | Altro | Mandal-Art (area "metterci la faccia"), prezzo del Drop 1 |
| 03:31-10:30 | Rapporto col denaro = rapporto col padre; rapporto con la madre = relazioni | Altro, cautela | Vedi sotto |
| 10:32 | La ripetizione fissa i concetti | Altro | Struttura dei copioni YouTube |
| **11:52** | **"I contenuti portano una persona da uno stato mentale A a uno stato B"**; i trigger torneranno nella scrittura | **Altro, utile** | Copione del Video #3, skill `marketing-psychology` e `copywriting` |
| 12:19-18:36 | Onde cerebrali e come "riprogrammarsi" | Salta | |
| 19:02-22:36 | Significato dei sogni | Salta | |
| **19:59** | Chi scorre il feed è già predisposto a guardare: conta l'intenzione | **Altro, utile** | Gancio dei primi secondi, nota "Virality Predictor" |

**Cautela su v1.** Qui non c'è metodo verificabile, e alcune cose vanno prese per quello che sono:

- Le "centinaia di migliaia di studi" su padre e denaro non vengono citate, e non conosco prove del genere: è un'ipotesi presentata come fatto.
- Le fasce delle onde cerebrali esistono, ma il resto non regge: il sonno REM non è sonno delta, e l'idea di "riprogrammarsi" in stato theta o di persone che entrano nei sogni altrui non ha basi scientifiche.
- È un testo di vendita applicato a chi ha già pagato: lui stesso parla di "manipolazione", screditare gli altri corsi e promettere che "non puoi non fare i soldi". Vale la pena studiarlo come esempio di persuasione, non come verità.
- L'esercizio del "funerale" al padre tocca cose personali: una lezione registrata non sostituisce un percorso vero, se sono temi che pesano.

### v2: Lezione AE 1, interfaccia (18 min)

| Minuto | Cosa | Tipo | Collegamento |
|---|---|---|---|
| 01:24-04:24 | Pannelli e confronto con Premiere | Salta | |
| **04:50** | Composizioni come scatole dentro scatole | **Metodo** | Stesso principio dei gruppi HTML in HyperFrames |
| 05:47 | Metraggi: un video come sequenza di immagini | Altro | Render a frame di HyperFrames |
| 08:53-10:13 | Tinta unita come sfondo | Salta | |
| 10:41 | Scorciatoie (A, P, S, T, R) | Solo per chi usa AE | |
| 14:20 | Annuncia roto e marionetta | Salta | |

### v3: Lezione AE 2, forme (27 min)

| Minuto | Cosa | Tipo | Collegamento |
|---|---|---|---|
| **00:30** | Perché le forme: "qualsiasi cosa è una forma"; il riferimento è lo stile dei video di Gadzhi | **Metodo** e Altro | Direzione del canale |
| 03:19 | Come cercare un effetto ragionando | Metodo | Stesso approccio per scegliere un formato |
| 02:53-06:39 | Sfondo: sfumatura radiale, poi blocca il livello | Metodo | Sfondi delle plate (`plates_base.py`) |
| 07:05-10:54 | Forma contro tracciato | Solo per chi usa AE | |
| **15:14-18:29** | **Dimensione contro scala:** la dimensione tiene fissi tratto e sfumatura, la scala ingrandisce tutto | **Metodo** | Da noi: `width` contro `transform: scale`. Spiega i bordi che ingrassano nello zoom |
| **18:54-20:40** | **Grafico di velocità** | **Metodo, il cuore** | Sezione curve qui sotto |
| 21:53-23:57 | Da quadrato a cerchio con la rotondità | Metodo | `formats/morph.py` |
| 24:35-25:16 | Trattini animati con lo scostamento | Metodo | Linee tratteggiate che si disegnano |
| 26:05 | Taglia tracciati | Metodo | Lo approfondisce in v5 |

### v4: Lezione AE 3, titolo "Cashflow Contents" (39 min)

| Minuto | Cosa | Tipo | Collegamento |
|---|---|---|---|
| 02:28-05:33 | Punto di ancoraggio e testo centrato al millimetro | Metodo | `transform-origin`: le animazioni di scala partono da lì |
| **09:59** | Due righe della stessa larghezza: "occhio grafico" | **Metodo** | Titoli, `formats/herotitle.py` |
| 12:19 | Usa sempre grassetto e maiuscole | Altro | Stile suo, non per forza nostro |
| **12:40-13:33** | "Minimo sforzo": non si anima lettera per lettera, si usa un preset | **Metodo** | Il nostro catalogo di formati |
| 14:00-23:00 | Animation Composer: scelta preset, poi toglie wiggle e rumore | Metodo come logica | Il plugin no, il "togliere" sì |
| **23:28-24:13** | **Mantieni vivo l'effetto:** scala lenta | **Metodo** | Nota "mai ferma", regola "No dead frame" in `taste.md` |
| 25:55-26:48 | Overshoot: un rimbalzo invece di due, e ritardo tra gli elementi | Metodo | Tua nota sui rimbalzi |
| **27:44-30:52** | **"Ragnatela":** gli elementi seguono il titolo | **Metodo** | Un gruppo padre nelle plate |
| 31:00-32:37 | Glitter dalla libreria | Altro | Gusto da valutare, non è il tuo stile |
| 33:02-35:16 | Ombra esterna e bagliore; bagliore minimo su rosso per effetto VHS | Altro | Look delle plate |
| 35:51-38:20 | Tasto iscriviti animato | Altro | Chiusura dei video YouTube |
| 38:40 | Con riferimento chiaro, meno di 10 minuti | Metodo | Lavorare sempre da un riferimento |

### v5: Lezione AE 4, morphing e Bézier (20 min)

| Minuto | Cosa | Tipo | Collegamento |
|---|---|---|---|
| 00:03 | Parte dal risultato finale, poi scompone | Metodo | Struttura delle prove |
| 02:41-05:00 | Sfondo a 4 colori più vignettatura: "molto più professionale" | **Metodo** | Sfondo verde delle plate: più profondità |
| **05:23-08:21** | Morphing: entrambe le forme diventano tracciati, si copia un keyframe sull'altro | **Metodo** | `formats/morph.py` |
| **08:21-10:24** | Come risolve un difetto: lo nomina, cerca il parametro | **Metodo** | Vale per ogni correzione delle bozze |
| 10:53-12:55 | Disegnare con la penna | Solo per chi usa AE | |
| **12:02** | **I loghi vanno fatti in vettoriale, così si animano** | **Altro, utile** | Logo Inverso, cartella `assets-jago`, prova "IN VERSO" |
| **13:02-15:33** | Taglia tracciati: una scia che corre lungo una linea, a goccia | **Metodo** | Linee che si disegnano; `stroke-dashoffset` in SVG |
| **16:20-19:18** | Tutto in una precomposizione, poi ombra radiale, bagliore, rotazione e scala sul blocco | **Metodo** | Il gruppo unico delle plate |
| 19:39-20:06 | Rifà rotazione e scala con le curve, sceglie il verso a gusto | Metodo | Sezione curve |

### v6: Lezione AE 6, motion tracking (15 min)

| Minuto | Cosa | Tipo | Collegamento |
|---|---|---|---|
| **00:48** | Quando serve: scritta o oggetto incollati a mano, dito, ambiente | **Altro, utile** | Formato "b-roll + scritta virale" |
| **04:10-05:07** | Si tracciano punti ad alto contrasto: il programma vede colori, non oggetti | **Metodo** | Vale per ogni tracciamento nostro |
| 05:16 | Area grande: più lento, più preciso | Solo per chi usa AE | |
| **05:57-08:42** | Oggetto Null: il movimento va su un elemento vuoto, tutto il resto lo segue | **Metodo** | Stesso principio del "maestro" di v4 |
| **08:53-10:48** | Testo a terra in 3D con ombra: copia nera, sfocata e schiacciata | **Metodo** | Si può fare anche in CSS 3D |
| 11:24-13:14 | Con zoom e rotazione servono due punti | Metodo | Clip dei reel con camera che si muove |
| **13:38-15:00** | Puntatore: linea più cerchio, disegnati con taglia tracciati | **Metodo** | Etichette delle plate; reel travel |

### v7: Lezione AE 7, lock-on tracking (13 min)

| Minuto | Cosa | Tipo | Collegamento |
|---|---|---|---|
| 00:29 | Effetto già automatico in CapCut, qui più pulito | Altro | Decisione "resta su CapCut" del passato |
| **01:40** | Sottotitoli che seguono il volto | Altro, utile | Idea per i reel, non per le plate |
| **03:27-03:41** | Stabilizza movimento: l'oggetto resta fermo e si muove il mondo | **Altro, utile** | Reel travel: inquadrature "bloccate" su un dettaglio |
| 04:28 | Se sballa un frame, si corregge a mano e non si rifà tutto | Metodo | Correggere la parte, non rifare da zero |
| **07:10** | Si sceglie la zona piena di dettagli | Metodo | Come il contrasto in v6 |
| **07:56-09:05** | Il video si sposta e scopre i bordi, quindi va ingrandito: serve più risoluzione | **Altro, utile** | `checklist-riprese.md`: girare in 4K e larghi dà margine |
| 09:44-11:18 | Scritta su un punto del soggetto che segue anche la rotazione | Metodo | Come v6 |
| 12:37 | Mostra "lo stretto necessario": ciò che si vede ogni giorno sui suoi profili | Metodo | Focus su ciò che serve |

### Il filo che lega i video

1. **Una gerarchia, non tanti oggetti:** scatole (v2), ragnatela (v4), precomposizione (v5), oggetto Null (v6) sono la stessa idea detta quattro volte. Un elemento porta il movimento, gli altri lo seguono.
2. **Linee che si disegnano:** trattini (v3), taglia tracciati (v5), puntatore (v6). Ci serve per le tue note sui tratteggi.
3. **Profondità dello sfondo:** sfumatura radiale (v3-v4), 4 colori più vignettatura (v5), ombra a terra (v6).
4. **Risolvere per nome:** in tutte le lezioni nomina il difetto prima di toccare qualcosa. È anche il modo migliore per darmi note sulle bozze.

## La curva di velocità

![Curva di velocità](img-inspo-after-effects/curva-velocita.png)

Il suo processo, nella lezione sulle forme (v3):

1. Parte da due keyframe lineari: velocità costante, 235,69 unità/sec, poi si ferma di colpo. Lui lo dice: "si arresta molto bruscamente".
2. Apre l'editor grafico in modalità **grafico velocità**.
3. Porta a zero la velocità di entrambi i keyframe. Oppure usa il tasto automatico, "con la metà del tempo".
4. Il tasto automatico però non gli basta: **lavora a mano sulle maniglie** fino a stringere la curva in un picco alto e spostato a sinistra.

Ho digitalizzato le curve pixel per pixel:

| Curva | Equivalente | Picco (× media) | Dove cade il picco | Metà strada | 90% della strada |
|---|---|---|---|---|---|
| Tasto automatico | `cubic-bezier(.33, 0, .67, 1)` | 1,5 | circa a metà | 50% del tempo | 81% |
| **A mano, quadrato (v3)** | **`cubic-bezier(.54, 0, 0, 1)`** | **4,4** | **30%** | **33%** | **55%** |
| A mano, scala (v5) | circa `cubic-bezier(.48, 0, 0, 1)` | 4,7 | 26% | 31% | 51% |
| `power3.inOut` (skill) | | 4,0 | 50% | 50% | 67% |
| `power3.out` (skill) | | 4,0 | 0% | 16% | 44% |
| `power2.inOut` (skill) | | 3,0 | 50% | 50% | 71% |

Correzione del 04/11: picco e percentuali della riga "A mano, quadrato" sono misurati sulla curva disegnata. La formula `cubic-bezier(.54, 0, 0, 1)` calcolata da sola ha un picco un po' più alto: 5,1 volte la media, al 30% della durata, con il 90% della strada al 57%. La forma è la stessa, ma per il passo in pixel vale il 5,1.

**Cosa significa, a parole:** il movimento parte piano per un attimo, scatta forte intorno al 30% della durata, poi passa quasi metà del tempo ad assestarsi sull'ultimo 10% di strada. Prima lo stacco, poi la planata.

Nessuna curva della skill ha questa forma. Le `inOut` sono simmetriche, con il picco a metà. Le `.out` partono già al massimo, senza alcuna rincorsa.

**Quanto sono affidabili questi numeri:**

- Digitalizzando il tasto automatico esce `.331 / .672`, cioè il valore noto dell'Easy Ease (33%): il metodo legge giusto.
- Il tooltip conferma la velocità lineare: 436 ÷ 1,85 s = 235,7 unità/sec.
- Misurando il quadrato frame per frame mentre va in play, la curva a mano sbaglia di circa 1 pixel su 105. L'Easy Ease sbaglia di 11.

**Altre curve viste, stimate a occhio:**

- **Rotazione finale (v5):** stessa famiglia ma più estrema, picco intorno al 20%.
- **Morphing quadrato → asterisco (v5):** prima campana simmetrica, poi spostata a sinistra.

Spiega il grafico di velocità in un solo passaggio esteso e non dà mai numeri: lavora a occhio. I valori qui sopra sono quello che la sua mano ha prodotto in due esempi, non una regola dichiarata da lui.

## Il ragionamento dietro

- **Parte dal risultato.** Ogni lezione apre con l'effetto finito, poi lo scompone. Dice che con idea e riferimento chiari un lavoro da 40 minuti di lezione ne richiede meno di 10.
- **Cerca gli effetti per logica:** "che tipo di cosa è?" (si genera? allora sta in Genera), non a memoria.
- **Davanti a un difetto, prima lo nomina.** Nel morphing: "sono le punte che sporgono", quindi cerca dove si controllano le punte. Si risolve in un parametro.
- **Automatizza ciò che non si vede:** "minimo sforzo, massimi soldi". Il testo lettera per lettera lo fa fare al preset, poi lo corregge togliendo.
- **Toglie il rumore dai preset.** Azzera il wiggle perché il default è "confusionario", riduce la rotazione, passa i rimbalzi da 2 a 1: "molto più pulita". È la tua stessa nota sui rimbalzi.
- **Un maestro, gli altri seguono.** Con la "ragnatela" (imparentamento) i cubi seguono il testo senza keyframe propri: si muovono insieme e, se cambia il tempo, cambia tutto. Scalare ogni elemento per conto suo dà un risultato diverso, perché ognuno scala dal proprio centro.
- **Mantieni vivo l'effetto.** Quando l'animazione si ferma "non è bello": aggiunge una scala lenta sotto tutto (nel testo parte da 107%; il valore d'arrivo nel video non si legge bene). Lo consiglia anche nel montaggio, quando un video "non ti cattura".
- **Una precomposizione raggruppa, poi si anima il gruppo.** Morphing e tracciato finiscono in un solo blocco: bagliore, rotazione e scala vanno sul blocco intero. Così il movimento finale è uno solo, non tanti.
- **Spinge i parametri al massimo per capirli**, poi torna indietro.

## Cosa applicherei alla skill

Da provare su una finestra corta prima di propagare, come da nota del 04/11:

1. **Nuova curva `stacco`, `cubic-bezier(.54, 0, 0, 1)`, sullo swipe di lavagna** in `formats/board.py`, al posto di `SWIPE_EASE = "power3.inOut"`. È il candidato più diretto per il movimento di camera che cerchi. GSAP accetta una funzione come curva; il codice oggi passa un nome tra virgolette, quindi serve un piccolo ritocco. La funzione è già provata in Node, non ancora in un render.
2. **Una sola scala lenta su tutta la plate**, che continua dopo l'ultimo elemento, per la regola "mai ferma".
3. **Un maestro per plate:** gli elementi figli di un gruppo che fa il movimento finale.

Nei suoi esempi la curva dura 1,7-1,9 secondi. Su mosse molto più corte il picco potrebbe diventare uno scatto: da verificare sulla prova.

## Limiti

- La mappa nasce dall'intero parlato di tutti i video e da un frame ogni 30 secondi: i frame sono stati studiati da vicino solo nei punti sui grafici.
- Manca la Lezione 5 (Maschere e Continua Testi): si vede ferma in coda a v5, ma non è stata registrata.
- Video a 720p e compressi. La curva è stata letta con precisione solo in v3 e nella scala di v5.
- Sono esercizi su forme e testi: le lezioni viste non mostrano motion graphics montate su un video con il volto.
- Il trascritto è automatico e alcuni nomi sono storpiati. Il creator citato in v3 è probabilmente Iman Gadzhi, da confermare.

## Prima prova sulla lavagna (04/11)

Stesso swipe del Video #3, da "Uno strumento" a "La mappa", 2500 px a 30 fps, senza sfocatura di movimento. Montato a parte con i frame veri del render, perché la coda era occupata dal render completo: non è ancora passato da HyperFrames.

| Versione | Picco di velocità | Passo più lungo | 90% della strada | Ultimi 10 frame |
|---|---|---|---|---|
| A: `power3.inOut`, 1,0 s (oggi) | a 0,50 s | 301 px per frame | 0,67 s | 247 px |
| B: curva del corso, 1,0 s | a 0,30 s | 397 px per frame | 0,60 s | 130 px |
| C: curva del corso, 1,6 s | a 0,49 s | 263 px per frame | 0,93 s | 44 px |

**Cosa insegna:** la curva da sola, a parità di durata, peggiora lo scatto a 30 fps. Funziona con la sua durata: nel corso le curve durano 1,7-1,9 s. A 1,6 s il picco cade quasi dove cade oggi, quindi inizio dello swipe e suono possono restare dove sono: cambia soltanto l'atterraggio, 0,6 s più lungo. Il giudizio a occhio spetta a Jacopo.
