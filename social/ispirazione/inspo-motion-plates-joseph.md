# Teardown — "Ho automatizzato completamente il montaggio video con Claude (processo completo)"

*Analisi del 01/11/2026. Video di ispirazione di Joseph (Content AI Academy), 11:49, 16:9 orizzontale (il file ha una etichetta di rotazione -90 sbagliata). Fonte: MOTION PLATES su iCloud Drive.*
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


---

## Addendum (01/11/2026, sera) — dinamismo e sound design MISURATI

*Correzione:* il video è **16:9 orizzontale** (11:49). Il file ha un tag di rotazione -90 sbagliato: per questo i primi fogli di anteprima uscivano storti.

### 1. Dinamismo (flusso ottico a 15 fotogrammi al secondo, 10.638 fotogrammi)
Classificati per colore: plate blu 39% del tempo, plate scure a interfaccia 37%, faccia 24%. Stesse misure sui nostri A (catena 3D) e B (diagramma verde, prima versione) sulla finestra di 16,5 s del Video #2.

| Misura (solo plate) | Joseph | A catena 3D | B (prima versione) |
|---|---|---|---|
| Tempo in movimento | 63-66% | 56% | 32% |
| Pausa ferma più lunga | 2,1 s (blu), 4,7 s (UI) | 2,7 s | 4,1 s |
| Pausa ferma, 90° percentile | 0,2-0,3 s | 2,1 s | 1,0 s |
| Scatti di movimento ogni 10 s | 4,8 | 5,2 | 0,7 |
| Movimento tra un fotogramma e l'altro, 90° percentile | 5-7 | 3,1 | 0,8 |
| Pan mentre si muove (px/s a 1080p), mediana / 90° | 2 / 44-51 | 85 / 159 | 2 / 9 |
| Zoom mentre si muove (%/s), mediana / 90° | 0,4 / 4,5 | 1,9 / 4,2 | 0,2 / 0,9 |
| Rotazione (gradi/s), mediana / 90° | 0,1 / 1,1 | 1,7 / 3,3 | 0,1 / 0,3 |

Lettura: **Joseph non fa grandi giri di camera.** Ha (1) uno **zoom lento continuo** (~0,4%/s, quasi una deriva), (2) **uno scatto di movimento ogni ~2 s** (un elemento che entra, uno che reagisce, un piccolo push-in fino al 4,5%/s) e (3) pan e rotazione quasi nulli. Ciò che si vede come "non sta mai fermo" è la **frequenza degli scatti**, non la loro ampiezza: la pausa di 4,7 s è un caso isolato (una schermata UI), nel 90% del tempo non si resta fermi più di 0,3 s.
La nostra B era ferma perché aveva 0,7 scatti ogni 10 s: ogni elemento entrava e poi tutto restava immobile fino alla parola dopo.

### 2. Sound design (cosa so e cosa NO)
**Cosa NON posso dire:** non posso ascoltare e la voce domina il file (parla il 95% del tempo; il file scaricato è ricompresso, banda utile fino a ~16 kHz). Spettrogrammi e rilevatori di eventi non separano in modo affidabile gli effetti dalla voce: i miei rilevatori automatici hanno contato centinaia di "eventi" che erano consonanti e armoniche. **Nessun valore di livello o di tipo dei suoni è quindi misurato.** Se Jacopo ricorda dei momenti precisi in cui il suono lo ha colpito, indicarli e li misuro lì.
**Cosa vedo con certezza:**
- Nella spiegazione del passo 7 (8:40-8:50) la timeline mostrata dal video piazza i suoni **sui tagli di scena**, **due suoni per taglio su due tracce** (A2 e A3), con questi nomi di file: *Whoosh, Hit, Pop, Camera, Swipe, Glitch* (A2) e *Click, Riser, Whoosh, Click 4, Hit* (A3). 10 scene in ~22 s = un taglio ogni ~2,2 s, circa 20 suoni.
- Le cartelle della libreria (mostrate a 8:25): Whoosh, Riser, Camera, Impatti, Click, Pop, Glitch, Swipe, Hit, Texture, circa 100 file ciascuna.
- Il sistema li sceglie **studiando i progetti vecchi dell'autore** ("come avevo usato quei suoni in video simili") e non chiede revisioni sul suono.
- Nella forma d'onda del tratto 507-510 s si vedono righe tonali tra 7 e 11 kHz in corrispondenza del contatore "507 → 1000+ sound effects": probabili tick digitali del contatore (una sola osservazione, da confermare all'orecchio).
**Per noi:** ciò che si copia è la *struttura* (il suono è attaccato ai tagli di scena, due strati, scelto dal gusto dell'autore), non i file: i gusti di Jacopo (niente pop, whoosh morbido, riser metallico solo su suspense, niente sotto i titoli eleganti) restano la regola. Vedi `references/sound.md` ("Suono delle plate").
