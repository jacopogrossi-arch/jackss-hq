# Studio: "Come monto i miei video con Claude" — Joseph (JOEDIT)

*Analisi del 01/11/2026. Video messo da Jacopo su Drive, cartella "motion plates": "Ho automatizzato completamente il montaggio video con Claude (processo completo)". 11:49, orizzontale 16:9, italiano.*
*Creator: Joseph, "AI video specialist" (marchio JOEDIT, corso "Content AI Academy", consulenze joeditconsulting). Monta reel e video per sé e per clienti con Claude Code + Remotion.*

Metodo dell'analisi: un fotogramma al secondo su tutto il video (710 fotogrammi), 5-10 fotogrammi al secondo sulle animazioni chiave per misurare i tempi, trascrizione completa del parlato. Trascrizione integrale e fotogrammi restano fuori dal repo (materiale di terzi, repo pubblico).

---

## 1. In una frase

Non è la bellezza delle singole grafiche a fare il video, è il **sistema**: un unico linguaggio visivo (piano blu elettrico, schede bianche, una "firma" blu su ogni cosa che entra) e **una grafica per ogni idea detta**, che entra sulla parola che la nomina e resta il tempo di capirla. E lo stesso sistema lo ha insegnato a Claude: prima gli ha fatto studiare 164 video Apple *capendo perché ogni animazione arriva su quella parola*, poi ha costruito una libreria di reference descritte, e ora approva/corregge piano, storyboard e revisioni.

---

## 2. Cosa dice: il metodo in 7 step

### L'idea di fondo: cervello + braccia
- **Claude = il cervello**: studia le informazioni, capisce le indicazioni, decide cosa costruire.
- **Remotion = le braccia**: esegue, cioè trasforma in animazione quello che Claude ha deciso.
- Primo passo pratico: dal sito di Remotion copia il comando di configurazione (`npx create-video`), lo passa a Claude Code chiedendo di "preparare il progetto e installare le skill di Remotion", poi gli fa aprire l'anteprima per controllare che funzioni.
- **Il problema che risolve**: "Claude non sa di base come vuoi i tuoi video. Se gli dici soltanto *editami questo video* magari crea anche delle animazioni, ma sceglie lui lo stile, i movimenti e il modo di rappresentare quello che dici usando il design di Claude base, che sarà uguale a tutti." (lo mostra con una slide crema/serif da "Claude di default": è il risultato da evitare).

### Step 1 — Studio delle reference (una volta sola, ≈10 ore)
- Ha scelto uno stile che gli piace: **i video Apple** — "come si muove la camera, come entrano i testi e come gli elementi si spostano mentre viene spiegata una cosa".
- Ha trascinato in Claude **164 video** del canale YouTube Apple: "Studia come sono costruiti".
- **Il punto chiave del video** (2:21-2:39): li ha fatti analizzare "sia quello che si vede sia quello che viene detto, per capire **perché una certa animazione arriva proprio in quel momento**. Perché una cosa è riconoscere il font o il colore di una scritta, un'altra è capire **perché quella scritta viene mostrata, su quale parola entra e come si muove per aiutare chi guarda a seguire il discorso**."
- Ha fatto raccogliere tutto con gli esempi in una **libreria** ("Libreria reference · 113 sequenze", sito interno "Reference da usare. Non solo da salvare."). Ogni scheda è una sequenza con un titolo che descrive *l'azione*, non lo stile, per esempio:
  - "Anelli di luce che si accendono e custodia frontale nel nucleo"
  - "Il conto cresce riga dopo riga"
  - "Intro di 70 s: ogni frase ha la sua immagine, sulla parola"
  - "Un oggetto per tutti i numeri: pillola → cerchio → squadrato → quadrato"
  - "Problema → richiesta → comportamento verificabile"
  - "Macro che arretra, uno vola via, gommini in fila e fermo per leggere"
  - "Confronto vero: le due voci affiancate, una dopo l'altra" (nata da una revisione, vedi step 6)
- "È da lì che il sistema riparte quando deve creare una nuova scena: ha già degli esempi di quello che voglio ottenere." Si fa **una volta sola**: quando gli ri-allega le reference, Claude risponde "ce li ho già nel mio brain, li ho studiati tutti la volta scorsa".
- Struttura delle cartelle che mostra: *Studio dello stile* → `Reference`, `Analisi`, `Libreria`, `Regole dello stile` (video studiati, fotogramma per fotogramma, la libreria, il mio stile).

### Step 2 — Audio e clone (≈10 min)
- Parte **dall'audio**, non dal video. Di solito usa il suo **clone AI** (non si registra davanti alla camera); la voce la registra col telefono o la genera con **Fish Audio** dal clone della sua voce.
- Passa a Claude registrazione + script: "Preparalo per il montaggio: togli gli errori, le ripetizioni e i silenzi". Poi **riascolta** per controllare che le frasi siano naturali e non manchino parole.
- Claude passa da solo alla creazione del **clone parlante**: alla fine ha un video in cui "compare lui" e dice il testo, senza camera, scena, luci.

### Step 3 — Piano (≈15 min)
- Prima di animare, Claude usa il parlato per preparare il **piano del montaggio**: "cosa mostrerei, frase per frase".
- Formato del piano (lo mostra nella loro **piattaforma interna JOEDIT**): per ogni frase → la frase dello script in corsivo tra virgolette + sotto, in grassetto, **l'idea visiva in una riga** + una miniatura. Esempi:
  - «Se non stai clonando te stesso nel 2026…» → **Il clone scansionato si divide: TU a sinistra, CLONE a destra.**
  - «Ogni volta che devi pubblicare un contenuto…» → **La settimana del Calendario di Apple che si riempie.**
  - «Appena la settimana si riempie di impegni, la produzione si ferma» → **Gli impegni grigi cadono uno dopo l'altro.**
- Per ogni riga: **✓ Approva** oppure **Scrivi qui** (nota). Esempio di nota: "Più semplice: solo la settimana che si riempie".
- **Qui mette il suo gusto** (4:46-5:11): "È una scelta che faccio prima di costruire la scena. Sto decidendo quale azione voglio far vedere e come deve essere percepito quel confronto da chi guarda. È qui che mi serve quello che ho imparato nel video editing e nella psicologia dei contenuti. Il sistema mi propone delle idee, ma devo essere io a capire se aiutano davvero a raccontare quello che sto dicendo." → Esempio: per "Chi edita meglio, ChatGPT o Claude?" la proposta era "i due loghi entrano e si fermano faccia a faccia"; lui scrive "Farei proprio un fight: i due loghi si danno i pugni, con sound effect stile anime" → risultato: due robot-logo che fanno boxe con arbitro, versione manga in bianco e nero.

### Step 4 — Storyboard (≈30 min)
- Claude prepara **bozze statiche** di ogni scena (testi, elementi, design finale) **prima di animare**: "voglio vedere come apparirà prima di far animare tutto".
- Interfaccia a mazzo di carte: **✕ Rifiuta / ✎ Modifica / ✓ Approva** per ogni fotogramma.
- Per un reel di 30-40 s "spesso approvo tutto, oppure chiedo una modifica".
- Esempio di correzione (6:01-6:27): per "incolla lo script" la bozza mostrava i tasti ⌘ V su un telefono. Lui: "guardando quei due tasti sul telefono, si capisce subito che sto incollando? Preferivo far vedere direttamente **il gesto dell'interfaccia**" → nota: "Niente ⌘V: la manina di Apple va nel campo «Scrivi o incolla il tuo testo», clicca, e lo script compare in blu prima di tornare al colore normale". **Regola implicita: mostrare il gesto reale, non un simbolo.**

### Step 5 — Montaggio (20-30 min, lavora Claude)
- A questo punto Claude ha tutto: **il parlato, il piano, lo storyboard approvato, le reference**. Crea le animazioni e le sincronizza col parlato.
- Può lavorare su **5 reel in parallelo**: "nel frattempo io scrivo altri contenuti, seguo i miei studenti oppure esco a fare una passeggiata col cane". Ha impostato una **notifica** ("Ho finito le animazioni di «Se non ti stai clonando»") e torna a guardare il risultato.

### Step 6 — Revisioni (≈15 min)
- "Qui sono abbastanza perfezionista, soprattutto sul primo giro. Il video magari già funziona, ma c'è un elemento che vorrei far entrare in un altro modo oppure un confronto che renderei più chiaro." Di solito dopo le prime indicazioni Claude capisce; i giri successivi sono rifiniture di gusto.
- Player del video + campo "Scrivi una nota a **questo secondo**": note con timecode, tipo Frame.io. Esempi: "0:01 Il logo deve entrare in un altro modo", "0:03 Il confronto non è chiaro", "0:06 Il titolo più in basso", "0:14 Il whoosh più forte qui", "0:21 Più zoom out sulla CTA" → **Invia a Claude** → V02.
- Esempio: ElevenLabs vs Fish Audio mostrati uno dopo l'altro → nota "Li metterei tipo comparazione: uno a destra e uno a sinistra, proprio fare comparison, vera" → V02 split a due colonne.
- **Le note diventano memoria**: in animazione decine di note ("Zoom out, non zoom in", "Niente frecce in diagonale", "Sottotitoli più piccoli", "Mai sulla faccia", "Il logo più grande", "Entra su questa parola"…) vengono assorbite dal cervello; una "Correzione 0:06 Il titolo più in basso" diventa una "**Preferenza** · mai la stessa entrata di seguito". E le scene corrette entrano nella libreria come nuove reference. È "la sua base", che migliora a ogni video.
- Usa **Wispr Flow** (dettatura) per scrivere le note a voce: "parlo come se le stessi spiegando a un amico… senza dover spiegare quali tasti premere in un programma di editing".
- Contrasto: prima doveva sapere tutte le scorciatoie di Premiere (⌘K, C, ⇧⌘D, ⌥⌘L, Q, W…), ora scrive cosa vuole.

### Step 7 — Sound design (≈5 min)
- Libreria propria di **1000+ effetti sonori** in cartelle: Whoosh, Riser, Camera, Impatti, Click, Pop, Glitch, Swipe, Hit, Texture (100 per cartella).
- Gli passa la cartella + i suoi vecchi progetti Premiere/After Effects: "Studia questi, studia pure tutto" → Claude studia **come ha usato i suoni in video simili** ("Reel clienti") e poi "mette i suoni sui tagli". "Io non sto a scegliere e posizionare ogni singolo suono, e su questa parte non ho avuto bisogno di chiedere revisioni."

### Il conto finale
- Reel di 40 s: ≈10 min + 15 + 30 + 20-30 + 15 + 5 = **≈1 h 40** (lo studio dello stile, 10 ore, si paga una volta sola).
- Di questi, **≈30 min sono suoi** (+ controlli); il resto lavora il sistema "mentre io scrivo altri contenuti o seguo i clienti". 1 video = 4 ore prima; ora 5 video nelle stesse 4 ore.
- Il sistema migliora da solo: "le correzioni, le preferenze e il lavoro che facciamo sui video entrano nella sua base". Dal mese prossimo gli editor che lavorano con lui non apriranno più Premiere o After Effects per questi contenuti.
- Messaggio di chiusura: "dare in pasto un video a Claude e chiedergli di editarlo non basta. Io continuo a scrivere, a scegliere la direzione e a controllare quello che esce. **Il risultato dipende sempre da come lo dirigi, non dallo strumento in sé.**"
- CTA: Content AI Academy (setup già pronto, collegato al tuo stile, scripting, psicologia del video editing, immagini e video AI, call one-to-one) + link Calendly in descrizione.

---

## 3. Il linguaggio visivo (il "design system")

**Tre ambienti, sempre gli stessi** (misurato su tutto il video, 2 fotogrammi al secondo):

| Ambiente | Quota del video | Durata tipica di un blocco | A cosa serve |
|---|---|---|---|
| Lui a camera (+ qualche B-roll) | 43% | mediana 3,5 s (max ~30 s) | voce, fiducia, respiro |
| **Piano blu** con grafiche | 31% | mediana 5 s (max 21 s) | concetti, schemi, numeri |
| **Interfaccia scura** (UI ricostruite) | 26% | mediana 3,5 s (max 21 s) | il "come si fa": chat, piattaforma, timeline |

Cambio di ambiente ogni **~5,7 s** (10,6 cambi al minuto). Mai un ambiente estraneo: tutto il video sta in questi tre mondi.

**Palette**
- Blu elettrico pieno (circa `#2B3BE8`) con **griglia sottilissima** quasi invisibile: è il "foglio" di tutte le spiegazioni.
- Bianco puro per testi e schede attive; **lavanda** (bianco semitrasparente sul blu) per le schede inattive.
- Blu più chiaro/saturo come **colore d'accento** sulle parole e sugli elementi che stanno entrando.
- UI scura neutra (`#1E1E1E` circa), stile app macOS/Claude.
- Talking head: set scuro blu notte (pannelli fonoassorbenti, braccio del microfono in diagonale), felpa navy → il blu del set e il blu delle grafiche sono **la stessa famiglia**: il passaggio camera→grafica non stona mai.
- Un solo colore "estraneo" ammesso: il rosa del cervello e l'arancio del logo Claude (oggetti, non sfondi).

**Tipografia**
- Sans geometrico **bold** (tipo SF Pro / Inter Display) per quasi tutto.
- **Serif corsivo sottile** per UNA parola per titolo, quella emotiva/concettuale: "sono diventati *opzionali*", "Claude come un *cervello*", "Gli servono anche delle *braccia*", "*7* step", "Quanto *tempo* serve", "questo livello di *controllo*", "*1000+* sound effects". È la firma tipografica: tondo per l'informazione, corsivo per il significato.
- Corsivo serif anche per le **annotazioni a mano** ("font e colore", "entra su questa parola", "sale e frena", "su un telefono?", "Wispr Flow") con una **freccia disegnata** che punta all'oggetto.
- Maiuscolo bold gigante solo per i titoli attorno alla testa ("2 COSE", "IL SISTEMA / LAVORA", "+ MATERIALE", "PER I MIEI / STUDENTI").

**Superfici**
- Schede bianche con angoli molto arrotondati, ombra morbida, leggera prospettiva 3D (le finestre sono spesso inclinate, come appoggiate su un tavolo, con la camera che ci gira attorno).
- Icone delle app in stile macOS 3D, "glass" (bolla di vetro che contiene le app, tile vetro Camera/Scena/Clip).
- Pill bianche per le etichette ("Libreria reference · 113 sequenze", "per un reel di 40 secondi", "una volta sola").

**Stati (sempre gli stessi, così chi guarda li impara)**
- *Attivo* = bianco pieno, leggermente più grande/sollevato.
- *Inattivo* = lavanda semitrasparente.
- *Fatto* = spunta blu in alto a destra.
- *Scartato* = barrato e sbiadito (Camera e Scena barrate, "Studio dello stile" barrato nella ricevuta).
- *Errore* = X rossa / badge rosso "Non si apre".

---

## 4. Come si muove (misurato)

- **Firma di entrata**: ogni elemento nuovo entra **sfocato + leggermente più grande (≈110%) + colorato di blu**, e in ≈0,2 s diventa nitido, 100% e bianco. Vale per parole, icone, numeri, schede. È l'equivalente visivo di "ecco, guarda qui".
- **Sottotitoli karaoke**: 1 riga di 2-5 parole, in basso sotto il mento (mai sul volto). Ogni parola arriva sul suo suono, blu e sfocata, poi diventa bianca; le parole chiave restano blu ("è *morto*", "il modo più *semplice*", "quello che ha *pensato*", "le *animazioni*", "per i propri *clienti*"). **Non sono sempre accesi**: spariscono quando parte una grafica e anche in lunghi tratti di camera (es. 0:38-0:44, 2:40-2:45) → i sottotitoli non sono decorazione, sono uno strumento usato a tratti.
- **Ritmo delle liste**: un elemento ogni 0,7-0,8 s, cioè al ritmo delle parole (le icone Pr, Ae, CapCut, DaVinci, Final Cut entrano esattamente quando le nomina).
- **Camera**: push-in lento (≈0,8 s) sull'oggetto di cui sta parlando, poi **zoom-out veloce con motion blur** (≈0,5 s) per mostrare il quadro intero, atterraggio morbido (ease-out). Lo stesso al contrario: zoom dentro una scheda fino a entrare nella sua anteprima (tasti ⌘V che diventano grandi, poi zoom-out e si scopre che è un telefono).
- **Whip laterali** con motion blur per passare da una scheda all'altra o da 1 a 5 finestre in parallelo.
- **Morph**: l'icona di Claude si trasforma nel cervello (≈0,5 s); "Come fa Claude a" + **MONTARE** gigante con l'icona sovrapposta; la scheda dello step si apre nella sua finestra.
- **Contatori che rollano**: cifre che scorrono verticalmente con blur (0:07 → 0:30 → 0:40; 307 → 886 → 999 → 1000+; ≈1 min → ≈1 h 29 → ≈1 h 40; i timer sotto ogni step).
- **Talking head con punch-in**: quando appare un titolo gigante ai lati della testa, l'inquadratura fa uno zoom-in rapido (≈115%) e si assesta; il titolo entra blu e diventa bianco.
- **Cose che si disegnano**: linee tratteggiate curve dagli input al cervello, curva a 7 nodi che sale ("Step 1 Reference… Step 7 Sound design") disegnata sopra la camera, linea a puntini da **A** a **Z** attorno alla testa ("dall'inizio alla fine"), ellisse a mano attorno alla parola "tempo".
- **UI ricostruite, non registrate**: la chat di Claude, la piattaforma JOEDIT, il Finder, Premiere sono rifatte in animazione (testo che si digita con cursore, cursore-manina che clicca, drag&drop di file con badge "+161", messaggio di stato "Sto analizzando 164 video…"). Sono pulite, leggibili e con la camera che segue il cursore.
- **Effetto "si sta generando"**: bordo luminoso che scorre attorno alla griglia di thumbnail; sweep di luce sulla preview che si rigenera; barre "Animazioni · 0% → 27%".

---

## 5. QUANDO mette le grafiche (la parte d'oro)

Regole dedotte guardando cosa succede secondo per secondo rispetto a cosa dice.

1. **Ogni idea detta = una grafica, sulla parola che la nomina.** Dice "Premiere Pro, After Effects, CapCut, DaVinci, Final Cut" → le icone entrano una per nome. Dice "come un cervello" → l'icona diventa cervello sulla parola "cervello". Dice "le braccia" → appaiono timeline e braccio con le X rosse. È esattamente quello che ha insegnato a Claude: "su quale parola entra".
2. **Grafiche per i concetti, camera per le opinioni.** Va sul piano blu quando spiega un *meccanismo* (cervello/braccia, step, tempi, libreria). Torna in camera quando dà un *giudizio o un'emozione* ("mi è venuto da pensare: ma aspetta…", "questa è la parte su cui mi concentro di più", "il risultato dipende da me"). La camera è il momento della fiducia, la grafica quello della comprensione.
3. **Mostra, non dire.** Quando racconta un'azione la mostra come gesto in un'interfaccia (trascina 164 video, digita il prompt, clicca Approva, scrive la nota) invece di scriverla. E nella revisione lo dice esplicitamente: niente tasti ⌘V, meglio la manina che clicca nel campo.
4. **Una mappa ricorrente (le 7 schede) come indice del video.** Le mostra nell'hook (0:19-0:32: "7 step"), poi la stessa riga torna **prima di ogni capitolo** con la scheda corrente accesa e le precedenti spuntate (1:38, 3:07, 4:03, 5:31, 6:36, 7:08, 8:19), poi si trasforma nella tabella dei tempi (9:00) e nell'ultima inquadratura "questo livello di controllo" (11:17). Chi guarda sa sempre **dove si trova e quanto manca**. Questo è il dispositivo più potente del video.
5. **Hook = promessa + anteprima visiva di tutto.** In 52 s: tesi provocatoria con effetto distruttivo ("è morto" → la timeline si spezza), cosa ha ottenuto (2 reel al giorno, calendario), la mappa dei 7 step, il reel finito che si genera (contatore 0:07→0:40), la curva dei 7 step disegnata mentre ripete "dall'inizio alla fine". Tutto quello che vedremo è già stato *visto* una volta.
6. **Metafora visiva per l'astratto.** Un concetto che non si può filmare diventa un oggetto: Claude = cervello, Remotion = braccia, le revisioni = note assorbite dal cervello, la memoria = "la sua base". Lo stesso oggetto (il cervello) torna 4 volte nel video: la metafora è un personaggio.
7. **I numeri si vedono crescere.** Mai un numero statico: 164 video (badge "+161"), 113 sequenze, 1000+ sound effects (cartelle che si riempiono), il tempo (timer per step → ricevuta → totale che rolla). Il contatore rende il numero un evento.
8. **Il confronto si mette fianco a fianco.** ElevenLabs | Fish Audio, versione A sbiadita | versione B attiva, TU | CLONE. Due cose da confrontare = due colonne, quella attiva piena e l'altra sbiadita.
9. **Prima/dopo dentro la stessa scena.** La proposta di Claude → la nota → la nuova versione, nella stessa finestra (V01 → V02), così il cambiamento si vede senza spiegarlo.
10. **Il talking head non è mai "vuoto" ma nemmeno sempre coperto.** Sopra la camera mette solo cose leggere che lasciano libero il volto: sottotitoli, curve, titoli giganti *ai lati* della testa, una colonna di 3 miniature a destra, una barra di avanzamento in basso, il widget Wispr Flow. Nei tratti di ragionamento la camera resta pulita anche 5-6 secondi.
11. **B-roll di atmosfera solo come pausa.** Lui al buio col mento sulla mano, lui seduto che guarda in alto, mani sulla tastiera, lui al monitor con la lampada: arrivano dopo un passaggio denso o su una frase riflessiva ("mi è venuto da pensare…"), 3-4 s, luce calda diversa dal set. Sono il respiro tra due blocchi di grafiche.
12. **Annotazioni a mano per indicare *dove guardare*.** "font e colore" con freccia sul titolo, "entra su questa parola", "sale e frena", "su un telefono?", "Wispr Flow ↙". Quando c'è un dettaglio piccolo nello schermo, una scritta corsiva con freccia lo indica: è il dito di un professore sulla lavagna.
13. **Ritmo di alternanza.** Nessun blocco di grafica supera ~20 s senza tornare a lui (anche solo 1-2 s), e nessun blocco di camera supera ~30 s senza qualcosa che si muove. In media cambia ambiente ogni 5-6 s.
14. **La chiusura riprende l'apertura.** "Il video editing è morto / i software sono opzionali" (0:00) → dock delle app dove Premiere e After Effects "Non si aprono" e si apre Claude (10:47). Stesse icone, stesso messaggio, cerchio chiuso.

---

## 6. Catalogo delle grafiche (con timecode)

| Tempo | Grafica | Mentre dice | Perché funziona |
|---|---|---|---|
| 0:00-0:03 | Sottotitoli karaoke + timeline 3D che sale e viene tagliata da una linea di luce, i pezzi esplodono | "Il video editing come lo conosci oggi è morto" | la tesi diventa un'azione distruttiva |
| 0:04-0:09 | Icone delle app una per nome, poi rimpiccioliscono e sfumano verso il basso | "I software… sono diventati *opzionali*" | lista = sequenza visiva; "opzionali" = spariscono |
| 0:10-0:15 | Icona Claude al centro tra le miniature dei reel → calendario Lun-Dom "2 *reel*" | "uso Claude per montare… pubblicare due volte al giorno" | il risultato reso concreto |
| 0:19-0:32 | 7 schede numerate: push-in su 01-02, zoom-out veloce, "*7* step", le schede si accendono una per una | "il processo completo in 7 step" | indice del video, mostrato per primo |
| 0:33-0:37 | Scheda del reel che si genera + contatore 0:07→0:40 | "quanto tempo per un reel di 40 secondi" | anticipa la risposta (open loop) |
| 0:49-0:51 | Curva ascendente a 7 nodi disegnata sopra la camera | "ti accompagnerò dall'inizio alla fine" | il percorso diventa una salita |
| 0:54-0:55 | "Come fa Claude a" + MONTARE gigante con icona sovrapposta | la domanda del capitolo | titolo di capitolo leggibile in 1 s |
| 0:58-1:05 | Icona → cervello rosa; input (video, doc, prompt) con linee tratteggiate entrano, output in pill escono | "pensare a Claude come un cervello… studiare le informazioni" | metafora che spiega input→output |
| 1:06-1:12 | Rami verso timeline e braccio con X rosse → "Gli servono anche delle *braccia*" | "un cervello da solo non può far tutto" | il limite mostrato con una X |
| 1:13-1:22 | Cervello → linea → Remotion; un prompt viaggia lungo la linea; anello che pulsa; escono 3 video; Claude ─ Remotion collegati | "Claude gli dice cosa costruire… Remotion esegue" | il flusso del lavoro è un viaggio |
| 1:23-1:34 | Sito Remotion in finestra 3D, click su "npx create-video" (toast "Copiato"), chat Claude con prompt digitato | "copio le istruzioni e le passo a Claude Code" | tutorial vero, ma ripulito |
| 1:43-1:45 | Le app chiuse dentro una bolla di vetro, Claude fuori | "Claude non sa di base come vuoi i tuoi video" | ciò che Claude non conosce è "chiuso" |
| 1:48-1:55 | Slide crema/serif generica ("Il video editing è cambiato", "Dall'idea al video") | "usa il design di Claude base, uguale a tutti" | mostra il *brutto* da evitare |
| 2:01-2:13 | Drag&drop dello spot iPhone 17, clip Apple in scheda | "a me piace lo stile dei video Apple" | la reference vista, non descritta |
| 2:16-2:28 | Canale YouTube Apple → trascina 164 video ("+161") → griglia di thumbnail con spunte e waveform, bordo luminoso che scorre | "ho raccolto tutte le reference… studiare come erano costruite" | la quantità si vede |
| 2:29-2:39 | "Ceramic Shield 2" con nota a mano "font e colore"; reel con waveform e parole, "tempo" cerchiato, "entra su questa parola", "sale e frena" | "una cosa è il font… un'altra capire su quale parola entra e come si muove" | **spiega la sua tesi con un esempio annotato** |
| 2:46-2:56 | Sito "Libreria reference · 113 sequenze" in prospettiva, scroll lento | "se apro la libreria che ha costruito" | prova tangibile del metodo |
| 3:00-3:04 | Chat: "Studia di nuovo questi" → "Bro, ce li ho già nel mio brain" | "questa fase si fa una singola volta" | ironia + memoria |
| 3:09-3:35 | registrazione.wav; reel del clone + "non registro"; tile Camera/Scena/Clip con Camera e Scena barrate; microfono + timer rec | "non mi registro davanti alla camera… mi è bastato registrare il parlato" | ciò che si toglie viene barrato |
| 3:36-3:59 | Chat: allega audio+script, "togli errori, ripetizioni e silenzi" → player voce-pulita.wav → "Ecco il video del tuo clone" | step 2 | UI = prova del processo |
| 4:06-4:27 | Piano frase-per-frase nella piattaforma JOEDIT, Approva / Scrivi qui | step 3 | si vede *dove* entra il suo giudizio |
| 4:28-5:19 | "Chi edita meglio": proposta → nota "fight stile anime" → versioni A/B → risultato boxe con arbitro; colonna di 3 miniature accanto alla camera | "io invece mi immaginavo uno scontro" | il prima/dopo del suo gusto |
| 5:35-5:53 | Storyboard come mazzo di carte: Rifiuta / Modifica / Approva | step 4 | un'azione = un gesto |
| 5:54-6:35 | Zoom dentro la bozza (⌘V su telefono), note a mano "incolla il testo →" "su un telefono?", nota scritta, rigenerazione, Approvata | l'esempio della manina | critica visiva in diretta |
| 6:38-6:51 | 4 schede ingredienti (parlato, piano, storyboard, reference) → finestra che renderizza con % → 5 finestre in parallelo | "ha tutto quello che gli serve… 5 reel in parallelo" | input → lavoro → scala |
| 7:00-7:07 | Notifica macOS "Ho finito le animazioni" + il reel finito che scorre | | ricompensa |
| 7:10-7:55 | Revisioni con note per secondo; ElevenLabs vs Fish Audio che diventa split; widget Wispr Flow annotato; tasti di scelta rapida che piovono su Premiere | step 6 | prima (shortcut) vs ora (frasi) |
| 8:03-8:18 | Note che si moltiplicano attorno al cervello e vengono assorbite; la libreria si aggiorna | "le revisioni diventano la sua base" | l'apprendimento è visibile |
| 8:27-8:48 | Finder SOUND EFFECTS con cartelle che si riempiono, "*1000+* sound effects"; Claude studia i progetti; timeline con i suoni che compaiono sui tagli | step 7 | numero che cresce + risultato |
| 8:52-8:57 | Parlato + clone + animazioni = il reel (linee che si uniscono nel telefono) | | l'assemblaggio in un'immagine |
| 9:00-9:51 | "Quanto *tempo* serve" → timer sotto ogni step → **ricevuta** con totale che rolla a ≈1 h 40 | la risposta all'open loop dell'hook | lo scontrino rende il tempo un costo concreto |
| 9:52-9:56 | "2 COSE", "1°", "1 h 40 È IL TEMPO IN CUI LAVORA IL…" giganti ai lati della testa con punch-in | | enfasi senza lasciare la camera |
| 10:01-10:08 | Barra di avanzamento sotto la camera: "≈30 min miei · + controlli · il resto: per altro · 1 h 40 in tutto" | | proporzione resa intuitiva |
| 10:09-10:16 | Cervello: "Correzione" che diventa "Preferenza"; "la sua *base*" | | |
| 10:29-10:31 | A → Z con linea a puntini attorno alla testa | "dall'inizio alla fine" | |
| 10:37-10:42 | "1 video · 4 ore" → timeline che si moltiplica in "5 video · 4 ore" | | il guadagno in un'immagine |
| 10:47-10:58 | Dock: Premiere e After Effects "Non si apre", si apre Claude | | chiude il cerchio con l'hook |
| 11:17-11:42 | "questo livello di *controllo*" + 7 schede spuntate; CTA a timeline verticale con moduli del corso | | |
| 11:45-11:48 | Zoom out sulla pagina YouTube, click sul link in descrizione | | la CTA mostra *dove* cliccare |

---

## 7. Cosa abbiamo già nella skill `youtube-edit` e cosa manca

**Già nostro (stesso spirito):** sottotitoli parola per parola, hero line (46), forma viva che si trasforma (45, come il cervello), catena di schede 3D (27b), chat di Claude animata (13b), pill attorno alla testa (41/41b), dock (34), browser 3D (4c), contatori/numero dietro la testa (1), barra di progresso del capitolo (9b), scaletta (44), confronto (21/26), il principio "il cut è il join" e "una sola cosa illuminata per frame" in `references/taste.md`.

**Differenze di gusto da notare:**
- Lui usa **un unico fondo per tutte le spiegazioni** (piano blu con griglia); la nostra skill varia di più fondi e gradienti. Un piano "di casa" sempre uguale rende il video riconoscibile.
- Lui usa **barre di avanzamento e tracker** (le 7 schede, la barra 30 min / 1 h 40) che il nostro `taste.md` mette tra le "cose da non fare mai" come HUD. Da lui funzionano perché **portano contenuto detto** (il capitolo corrente, il tempo), non sono decorazione. Va chiarita la regola, non copiata.
- Lui **ricostruisce le interfacce** invece di registrarle (chat, Finder, Premiere): più pulite e con la camera che segue il cursore.

**Mancano (candidati da provare col test A/B alla cieca sul banco, come da regola della skill):**
1. **Mappa ricorrente del video** — le N schede degli step che tornano prima di ogni capitolo, con la corrente accesa e le precedenti spuntate, e alla fine diventano il riepilogo. (Il nostro 9c "slot wall" è il parente più vicino.)
2. **Nota a mano con freccia** — corsivo serif + freccia disegnata che indica un dettaglio dentro una schermata ("entra su questa parola").
3. **Ricevuta** — scontrino bianco con voci e pill, totale che rolla: per tempi, costi, ingredienti.
4. **Barrato** — tile di cose che "non servono più" che vengono barrate e sbiadiscono (Camera, Scena → resta Clip).
5. **Titoli giganti ai lati della testa con punch-in** — due parole a sinistra e a destra del volto, entrata blu→bianco, zoom 115% della camera.
6. **Linea A→Z / curva a nodi sopra la camera** — percorso disegnato attorno alla persona.
7. **Revisione a timecode** — player + note per secondo + V01→V02 (per i video in cui raccontiamo il nostro processo).
8. **Firma di entrata "blu→bianco"** — non un formato ma una regola del preset: ogni elemento entra sfocato e colorato d'accento, poi si assesta nel colore neutro.

---

## 8. La lezione per noi (oltre alle grafiche)

Il suo metodo e la nostra skill sono quasi lo stesso progetto: lui ha una "libreria di reference" e una piattaforma di approvazione, noi abbiamo `formats.md`, `taste.md`, `NOTES_LOG.md` e i Checkpoint. Tre cose che fa lui e possiamo fare meglio:

1. **Studiare le reference sul *perché*, non sul *come appare*.** Per ogni reference: su quale parola entra, cosa sta spiegando in quel momento, cosa capisce chi guarda grazie a quella grafica. È la differenza fra copiare uno stile e capirlo. (La nostra sezione "teardown" misura i pixel; va aggiunta la domanda "perché qui?".)
2. **Un piano frase-per-frase da approvare *prima* di costruire.** Per ogni frase: la citazione + l'idea visiva in una riga. Jacopo approva o scrive una nota. Il nostro Checkpoint B fa già questo, ma la forma "frase → idea in una riga → Approva / Nota" è più veloce da leggere.
3. **Ogni nota diventa una regola** — lo facciamo già (`NOTES_LOG.md`), ed è esattamente il "brain" che mostra lui. Bene così.

E una per il racconto: **il suo video è un tutorial che si guarda come un film** perché ha una mappa (7 step), una metafora (cervello/braccia), un open loop (quanto tempo?) che si chiude con un'immagine (la ricevuta), e un finale che riprende l'inizio. È una struttura riusabile per il video #3.
