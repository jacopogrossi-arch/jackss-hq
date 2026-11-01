# Teardown — "Ho automatizzato completamente il montaggio video con Claude (processo completo)"

*Analisi del 01/11/2026. Video di ispirazione di Joseph (Content AI Academy), 11:49, verticale 9:16. Fonte: MOTION PLATES su iCloud Drive.*
*Metodo: trascrizione Whisper + 142 frame (uno ogni 5 s) + finestre dense a 2 fps su hook, cervello, fight, revisioni.*
*Limiti: sorgente a 480p. Whisper ha storpiato alcune parole ("Cloud" = Claude); manca la trascrizione dei secondi 357-387 (sono coperti dai frame). I frame stanno solo in locale in `videos/motion-plates/` (fuori da git).*

---

## 1. In una frase

Il video **è la dimostrazione di ciò che racconta**: ogni passaggio del sistema (7 step) viene spiegato con una *motion plate* che appare **nel momento esatto in cui la parola viene detta**, e il video stesso è montato con quel sistema. Circa tre quarti del tempo è grafica/plate; la faccia è l'ancora che torna ogni 20-40 s.

---

## 2. Cosa dice: come ha "allenato" Claude (il metodo)

**Architettura:** Claude = cervello (decide), Remotion = braccia (costruisce le animazioni). Si collegano una volta sola copiando le istruzioni dal sito di Remotion dentro Claude Code (`npx create-video`, installa le skill).

**Il problema che risolve:** se dici a Claude "editami questo video", sceglie lui stile, movimenti e design → design Claude di base, uguale per tutti (nel video lo mostra con la card crema/serif/terracotta, vedi §4).

**La soluzione — fase di studio, una volta sola (~10 ore):**
1. Raccoglie video con lo stile che ama (per lui: video Apple — come si muove la camera, come entrano i testi, come gli elementi si spostano mentre si spiega).
2. Li dà a Claude (164 video) e gli chiede di analizzare **sia ciò che si vede sia ciò che viene detto**.
3. Il punto chiave, parole sue: una cosa è riconoscere font e colore, **un'altra è capire perché quella scritta viene mostrata, su quale parola entra e come si muove per aiutare chi guarda a seguire il discorso**.
4. Claude salva tutto in una **libreria** (113 sequenze: riferimenti + indicazioni di montaggio + esempi). Da lì riparte per ogni scena nuova. Titolo della libreria: *"Reference da usare. Non solo da salvare."*

**I 7 step di ogni video:**

| # | Step | Tempo (reel 40 s) | Chi lavora |
|---|---|---|---|
| 01 | Studio delle reference | ~10 ore, una volta sola | Claude + lui |
| 02 | Audio e clone: registra solo la voce, Claude toglie errori/ripetizioni/silenzi, poi crea il clone parlante | ~10 min | Claude |
| 03 | **Piano**: frase per frase, cosa mostrare, nella sua piattaforma interna (Approva / Scrivi qui) | ~15 min | Claude propone, lui decide |
| 04 | **Storyboard**: bozze statiche delle scene (testi, elementi, design) da approvare *prima* dell'animazione | ~30 min | lui approva |
| 05 | Montaggio/animazione, sincronizzata al parlato, anche 5 reel in parallelo, notifica quando finisce | 20-30 min | Claude |
| 06 | Revisioni: le detta a voce con Wispr Flow "come a un amico", senza dire quali tasti premere | ~15 min | lui + Claude |
| 07 | Sound design: Claude ha studiato la sua libreria (10 cartelle, 1000+ effetti) e i suoi progetti Premiere/After Effects, poi mette i suoni da solo | ~5 min | Claude |

Totale ~1h40 di lavoro del sistema, ma **solo ~30 min suoi** (piano, approvazioni, revisioni).

**Due regole di metodo da ricordare:**
- *Il risultato dipende da come lo dirigi, non dallo strumento.* Lui sceglie la direzione; il sistema propone. L'esempio: la prima idea per l'hook era "due loghi si fermano uno davanti all'altro", lui ha scritto "voglio uno scontro, loghi che si danno i pugni, effetti sonori stile anime" → risultato che "nel pratico non saprei nemmeno costruire".
- **Le correzioni vengono salvate nella base** ("Zoom out, non zoom in" entra nel cervello): una preferenza spiegata una volta non va rispiegata. Se continua a correggere la stessa cosa è gusto personale, non errore del sistema.

---

## 3. Linguaggio visivo (cosa ha di riconoscibile)

- **Palette:** blu elettrico pieno (~#2B3BFF) con griglia "blueprint" molto tenue come sfondo delle plate; grigio carbone caldo per le plate di interfaccia; bianco; accento Claude arancio/corallo; card crema per il "design Claude base". Il blu torna anche nelle parole enfatizzate dei sottotitoli.
- **Tipografia:** due voci sempre insieme — **sans bold compatta** per il fatto, **serif corsivo elegante** per la parola da ricordare ("sono diventati *opzionali*", "Claude come un *cervello*", "Quanto *tempo* serve", "*7* step" con il 7 in corsivo gigante). La parola-chiave è quella che cambia font.
- **Sottotitoli sulla faccia:** poche parole alla volta, sincronizzati; le parole in arrivo sono blu, quelle dette passano al bianco; la parola-chiave diventa blu serif corsivo ("Perdendo", "tempo"). Posizione: terzo inferiore, sul petto, mai sul viso.
- **Schermate come oggetti 3D:** le screen recording non sono piatte: sono piani con angoli arrotondati, leggermente curvi e inclinati in prospettiva, con ombra, che scorrono/ruotano nello spazio. Cursore a **manina 3D** che clicca (anche in finti schermi costruiti da zero).
- **Movimento:** ingressi con scala + blur-in (le icone appaiono a ~0,5 s l'una dall'altra, ognuna **sul nome detto**), uscite con blur + caduta/dissolvenza, camera che scorre lungo le card (dolly orizzontale), liste che si illuminano riga per riga, contatori che salgono. Pochissimi elementi fermi: c'è sempre una cosa viva.
- **Stacchi:** tagli netti faccia ↔ plate (niente transizioni decorative), plate di 3-12 s, faccia di 3-10 s. Qualche cutaway cinematografico di lui al computer (lampada, mani sulla tastiera, sguardo sul monitor, luce bassa) per i momenti "di attesa" o di stupore.

---

## 4. QUANDO mette le grafiche e PERCHÉ (la parte più importante)

Ogni plate ha **una funzione didattica precisa**. Le ho raggruppate per funzione, con minutaggio:

### A. Nomi → icone (appaiono quando la parola è pronunciata)
- 0:03-0:09 — dice "Premiere Pro, After Effects, CapCut, DaVinci, Final Cut": le 5 icone entrano una alla volta, ognuna sul suo nome. Poi la frase "sono diventati *opzionali*" e le icone **cadono sfocate** → l'idea ("opzionali") è nel movimento.
- 10:45-10:55 — le stesse icone tornano in un dock con Claude accanto; la manina **clicca Claude**. Apertura e chiusura si specchiano: stesso oggetto, significato cambiato.
- 3:25 — "camera, scena, clip": tre icone 3D con i nomi esatti; camera e scena sfumano (le cose che *non* devi più fare), resta solo il parlato.

### B. Metafora disegnata quando il concetto è astratto
- 1:00-1:20 — "pensa a Claude come un cervello": il logo diventa un cervello rosa luminoso; **input** (reference, testo, video) entrano da sinistra con linee tratteggiate, **prompt** in una pill ("Monta questo reel nel mio stile"), **output** a destra. Poi "gli servono delle braccia": strumenti barrati con una X rossa, entra l'icona del braccio, poi Remotion collegato con una linea. Ogni elemento compare quando lo nomina. Il diagramma è sempre **semplice: 3-5 oggetti**.
- 2:30-2:40 — per spiegare "perché l'animazione arriva proprio su quella parola" mostra una forma d'onda con le parole, una **parola cerchiata** ("tempo") e annotazioni a mano ("sale e frena", "entra su questa parola"). Non lo dice e basta: lo *fa vedere sul dato*.

### C. Mappa di navigazione ricorrente (il "7 step")
- Le 7 card si aprono a 0:18, tornano a 1:36, 3:05, 5:30, 6:35, 9:00, 10:25, 11:15. A ogni ritorno **lo step in corso è sollevato/evidenziato e quelli finiti hanno la spunta**. Sono il "dove siamo" di un video da 12 minuti, senza una parola in più.
- 0:48 — una linea curva con i 7 step sovrapposta a lui (roadmap sulla faccia), prima di entrare nel dettaglio.

### D. Prova pratica = schermo (mai solo a parole)
- 1:25, 3:35-4:05 — mostra *davvero* il prompt che scrive ("Preparalo per il montaggio: togli gli errori, le ripetizioni e i silenzi"), la risposta, il lettore audio, "Sto creando il tuo clone parlante". Le interfacce sono **ricostruite pulite** (mock a schermo), non registrate: testo leggibile, zero rumore.
- 4:05-4:35 — la sua piattaforma "Piano": la frase tra virgolette, l'idea proposta in grassetto, bottoni Approva/Scrivi qui, la nota digitata. Quando dice "se mi convince la tengo, altrimenti gli spiego" si vede il cursore fare esattamente quello.
- 7:10-8:10 — le revisioni con **timecode** ("0:06 il titolo più in basso", "0:14 il whoosh più forte qui", "0:21 più zoom out sulla CTA"): la granularità delle note si vede in un colpo d'occhio.

### E. Il "prima/dopo" con lo stile
- 1:50 — "Il video editing è cambiato." in una card **crema/serif/terracotta**: è il look Claude di default, appare proprio mentre dice "design di Claude base… uguale a tutti". Subito dopo: Apple (iPhone 17, selfie) → le reference → il suo blu. Il contrasto *è* l'argomento.
- 5:15 — il risultato del fight dei loghi, mostrato **a schermo intero** dopo averlo visto come bozza piccola nel piano: prima il piccolo (decisione), poi il grande (payoff).

### F. Confronti: gli elementi si affiancano
- 4:50-5:00 — mentre racconta "il fight", i tre candidati (fight, sketch) in miniatura a destra dei suoi occhi: il pubblico vede l'alternativa scartata.
- 7:25-7:50 — ElevenLabs e Fish Audio **una card a destra e una a sinistra**, stessa frase, stessa waveform: è la revisione che lui stesso ha chiesto, e il video la usa come esempio. (La spiegazione del metodo è esempio del metodo.)

### G. Numeri e tempo → contatori e barre
- 8:25-8:30 — "10 cartelle con più di 1000 effetti": il contatore **507 → 1000+**, le cartelle (Whoosh, Riser, Camera, Impatti, Click, Pop, Glitch, Swipe, Hit, Texture) si riempiono a 100 ciascuna.
- 9:00-9:50 — "Quanto *tempo* serve" per un reel da 40 s: sotto ognuna delle 7 card compare il **chip di tempo** (≈10 ore · ≈10 min · ≈15 min · ≈30 min · 20-30 min · ≈15 min · ≈5 min) *nel momento in cui lo dice*, poi una tabella riassuntiva.
- 9:50-10:10 — "2 COSE" gigante a schermo + barra: **≈30 min miei** + controlli, dentro **1h40 in tutto**, "il resto: per altro". Una barra divisa spiega la distinzione più importante del video.
- 10:35-10:45 — "4 ore di montaggio" = linea del tempo con righello 0h-3h-4h; poi **5 video in parallelo** nello stesso arco.

### H. Elenchi e call to action
- 11:15-11:45 — i punti del corso compaiono in una **linea verticale che scorre**: ognuno si illumina quando viene nominato (Il setup già pronto → Collegato al tuo stile → Scripting → Psicologia del video editing → Immagini e video AI → Call one to one) con un'anteprima a destra. Chiude con la manina che clicca il link nella descrizione.

### I. Momenti di respiro (B-roll di lui)
- 4:55-5:25 (fight "mi è venuto da pensare ma aspetta"), 6:50 (digita/attende), 7:05-7:10 (mentre il sistema lavora), 8:00 (revisiona al PC): il B-roll di lui **serve il racconto emotivo** (stupore, attesa, lavoro mentre l'AI lavora), non è riempitivo.

---

## 5. Regole estratte (playbook per le nostre motion plates)

1. **Una plate per idea, mai per decorare.** Prima di creare una plate: *che cosa deve capire chi guarda in questo momento?* (nome → icona; processo → metafora; numero → contatore; confronto → affiancato; errore da evitare → barrato/dissolto).
2. **Aggancio alla parola.** L'oggetto entra **sulla parola che lo nomina** (non prima, non dopo). Se elenca 5 cose, 5 ingressi a ~0,5 s.
3. **Parola-chiave = cambio di font** (sans → serif corsivo, e/o blu). Una per frase al massimo.
4. **Metafora semplice** quando il concetto è astratto: 3-5 oggetti, linee tratteggiate per i flussi, un solo colore forte dietro.
5. **Mostrare il prima di dire il dopo.** Il default Claude (crema/serif) appare per dire "non così"; poi lo stile vero.
6. **Il tracker ricorrente** in un video lungo: stessa plate, stato diverso (✓ per fatto, sollevato per in corso).
7. **Interfacce ricostruite pulite**, inclinate 3D, con cursore a manina. Mai screen recording grezze.
8. **Numeri vivi:** contatori che salgono, chip che compaiono mentre si dice il numero, barre che si dividono.
9. **Il confronto è sempre affiancato**, mai in sequenza.
10. **Faccia come ancora.** Ritorna ogni 20-40 s per riportare la relazione; il testo grande entra "dietro" o ai lati, mai sul viso.
11. **Cosa non serve più → sfumato/barrato/caduto.** La scomparsa comunica quanto la comparsa.
12. **Il video dimostra ciò che dice.** Non descrivere il metodo: usarlo davanti al pubblico (schermo vero, prompt vero, risultato reale).

---

## 6. Confronto col nostro sistema (`youtube-edit` + HyperFrames)

**Già allineati:** storyboard prima del render, formati variati, note di gusto salvate nella skill, PiP quadrato, regole sul sound, piano scritto da un pianificatore e costruito da `video-builder`.

**Differenze da colmare (idee, non ancora applicate):**
- **Libreria di reference "con il perché"** — oggi la skill ha formati; manca una libreria di plate *analizzate* (video + parlato + "entra su questa parola perché…"). Potremmo costruirla da questo video (le sezioni §4 sono già l'indice) e dai video che Jacopo manda.
- **Piano frase-per-frase approvabile** — per ogni frase: l'idea della plate, una riga, Approva/Modifica; solo dopo lo storyboard statico. Il `storyboard.json` c'è: manca il passaggio di approvazione fatto da Jacopo prima del render.
- **Revisioni con timecode** ("0:14 il whoosh più forte") salvate come note → regole.
- **Tracker ricorrente** (stato di capitoli) per i video lunghi: nel Video #2 abbiamo i capitoli, ma non la plate che torna con le spunte.
- **Plate di interfaccia ricostruite 3D** (prompt → risposta → cursore a manina): un formato nuovo da aggiungere.
- **Contatori / barre divise** per i numeri.
- **Bookend:** stesso oggetto in apertura e chiusura con significato cambiato.

**Attenzione:** è il suo stile (blu elettrico + serif corsivo), non il nostro. Prendiamo la *logica* (quando e perché), non palette e font: i nostri restano quelli di Jacopo (vedi `motion/` e `taste.md`).
