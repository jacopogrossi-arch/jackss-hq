# Corso After Effects: come ragiona e quali curve usa

*Analisi del 04/11/2026 sulle registrazioni in `Videos\Architettura Mentali 2`. Trascritti e frame stanno solo in locale, in `videos/inspo-after-effects/` (corso a pagamento, fuori da git).*

## In breve

**Serve, ma per il metodo: il programma non ci riguarda.** Noi montiamo con HyperFrames, quindi metà del corso (pannelli, plugin, Animation Composer) non si trasferisce. Si trasferiscono tre cose:

1. **La curva di velocità.** È il motivo per cui i suoi movimenti sembrano fluidi, ed è diversa da tutte quelle che usa oggi la skill.
2. **Il ragionamento:** collegare gli elementi tra loro invece di animarli uno a uno, e partire sempre da un riferimento.
3. **La regola "mantieni vivo l'effetto"**, che è la tua nota "mai ferma" detta da un'altra persona.

## Cosa c'era nella cartella

| File | Contenuto | Utile qui? |
|---|---|---|
| v1 `08-15-58` | Lezione 1 di "Architettura Mentale" (denaro, onde cerebrali): **non è After Effects** | No |
| v2 `12-15-47` | Interfaccia di base, gestione dei livelli, scorciatoie | Poco |
| v3 `12-33-52` | Forme e sfumature. **Unica spiegazione del grafico di velocità (18:54-20:40)** | Sì, è il cuore |
| v4 `13-01-11` | Testo "Cashflow Contents" con Animation Composer, collegare i livelli | Sì, per il ragionamento |
| v5 `13-49-38` | Shape morphing e tracciato Bézier | Sì |
| v6 `14-20-28` | Motion tracking con oggetto Null | Solo in parte |

Le code di v4 (dopo 39:00) e v5 (dopo 20:30) sono la lezione successiva in pausa: lì non c'è nulla.

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

- Video a 720p e compressi. La curva è stata letta con precisione solo in v3 e nella scala di v5.
- Sono esercizi su forme e testi: le lezioni viste non mostrano motion graphics montate su un video con il volto.
- Il trascritto è automatico e alcuni nomi sono storpiati. Il creator citato in v3 è probabilmente Iman Gadzhi, da confermare.
