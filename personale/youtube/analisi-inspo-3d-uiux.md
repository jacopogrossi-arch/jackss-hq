# Analisi di due video di ispirazione: 3D con three.js e principi UX/animazione

*13/11/2026. Fonte: i due MP4 in iCloud Drive, cartella "ciao". Entrambi 720×1280, 30 fps, senza sottotitoli parlati: ho letto 5 fotogrammi al secondo (fogli di contatto da 12 fotogrammi = 2,4 s) più ingrandimenti a 8 fps sui momenti più veloci del 3D. L'audio non è stato analizzato.*

**Attenzione ai nomi dei file:** `14317…MP4` è il video **teorico UX** (non il 3D) e `8841…MP4` è il video **3D**. Erano invertiti rispetto alla descrizione.

---

## PARTE A. Il video 3D ("No Blender. Just Claude", @holcdenis, 25,6 s)

### Cos'è
Un corto 3D di una scrivania (carta, tazza, pianta, un vecchio Mac a tubo catodico) fatto interamente con codice three.js, mostrato dentro un laptop su una scrivania di legno. Il film 3D dura 649 fotogrammi (21,6 s a 30 fps): nell'angolo c'è un contatore `0265 / 0649`, e in alto a sinistra una piccola etichetta rossa `FRAME 0233 · PASS: FINAL`. Il testo sul foglio nella scena **è la skill stessa** ("3d-animator"): è il fotogramma più prezioso del video (vedi sotto).

### Cosa succede, secondo per secondo
| Tempo | Cosa si vede |
|---|---|
| 0,0–0,6 | Scrivania "argilla" (tutto bianco/marrone piatto, senza luci). Una **barra verticale che spazza** lo schermo la trasforma nella versione finale: luce a strisce, vapore dalla tazza, polvere. L'etichetta rossa `PASS: FINAL` accompagna la barra. |
| 0,6–3,5 | **Spinta lenta** verso il foglio, con sfocatura di profondità (la tazza in primo piano sfuoca). Si legge `# 3d-animator`. |
| 3,5–7 | Taglio-veloce (whip) sul Mac retrò. Testo rosso mono che si scrive a scatti: `NO` → `NOT BLENDER`. Sul terminale si digita: `cam = shotAt(t)` / `cam.roll = rollAt(t)` / `renderAt(t, 48)` / `// same t, same frame.` |
| 7–9 | Ritorno alla versione argilla: "Ask Claude for 3D, you get this." Poi di nuovo la barra spazzante verso il finale. |
| 9–11 | Spinta sul foglio: si legge il contenuto della skill (vedi sotto). |
| 11–12 | **CAMERA**: primo piano di un obiettivo con fiamma di luce. Poi la versione **a inchiostro** (carta bianca, solo contorni neri, linee dei raggi ottici) e ritorno. |
| 12–13 | **LIGHT**: veneziana con lame di luce, e la scritta `sun.through("blinds")` **luminosa e piegata lungo le lame**, dentro la scena. |
| 13,2–14,4 | **MOTION**: una traiettoria ad arco luminosa sopra il Mac, poi la versione a inchiostro. |
| 14,4–15,5 | **SOUND**: lo spettro audio è fatto di **barre 3D** in piedi sulla scrivania, vista bassa e radente. |
| 15,6–17,5 | **LINES OF CODE BY CLAUDE**: contatore rosso 0 → 1.345; la camera ruota e il pannello di codice vola come un piano in prospettiva, con motion blur forte e una riga rossa di scansione; versione a inchiostro nel mezzo. |
| 17,5–19,5 | Ritorno al terminale: `turn my desk into a 3D film`. |
| 19,5–22,5 | Chiusura: `Comment skill` / `I'll send you the file.` in **lettere 3D estruse** nella scena, con un ultimo passaggio a inchiostro e di nuovo il finale. |
| 22,5–25,6 | Dissolvenza a nero, logo Instagram + nome. |

### Il contenuto della skill (letto sul foglio nella scena)
> `# 3d-animator` — *You are the whole crew.*
> **camera**: one lens, one curve, one eased move · 180° shutter, 0.8 on fast whips · end on a slow push into the hero
> **light**: one strong key with a reason · blinds paint the stripes · flat light is the enemy
> **motion**: …· **sound**: … (illeggibili: il foglio esce dall'inquadratura)

Quattro capitoli **camera / luce / movimento / suono**, gli stessi quattro che compaiono come etichette rosse nel video. È una struttura da copiare: il video spiega la skill *mentre la usa*.

### Le tecniche, una per una
1. **I "pass" di render come linguaggio visivo.** Tre look della stessa scena: *argilla* (senza luci), *finale* (luci, ombre, vapore), *inchiostro* (contorni neri su carta bianca). Si passa dall'uno all'altro con una **barra di taglio verticale** che porta un'etichetta HUD. Significato: "prima/dopo", "come è costruito", "ecco il disegno". In three.js è fattibile: stesso `scene` renderizzato con materiali sostitutivi (argilla = `MeshStandardMaterial` bianco senza luci o `MeshBasicMaterial`; inchiostro = `EdgesGeometry` + `LineSegments` su fondo chiaro) e un taglio a forbice (scissor) o un mix per pixel.
2. **La luce è il personaggio.** Una sola luce forte "con un motivo" (la finestra con veneziana), buio tutto intorno, tavolozza calda (marroni bruciati, crema, ambra). Le lame sono ombre proiettate da una luce direzionale attraverso una griglia di listelli. Piccoli dettagli vivi: vapore, pulviscolo in sospensione.
3. **Camera: una curva, un movimento.** Spinte lente verso l'eroe, tagli-veloci con **motion blur vero** (otturatore 180°, "0.8 sui whip") e **sfocatura di profondità** sul primo piano. Il contrario del movimento continuo uniforme: veloce nel mezzo, piano in arrivo.
4. **Deterministico: `renderAt(t, 48)` — "same t, same frame".** È esattamente la nostra regola ("tutto è una funzione pura del tempo", `world3d.py`). Qui lo usano per scrivere un contatore `FRAME xxxx / 0649` sull'immagine: il render è il tempo.
5. **Testo dentro la scena, non sopra.** `sun.through("blinds")` luminoso e inclinato lungo le lame; `Comment skill` in rilievo con ombre; barre dello spettro come oggetti sul tavolo; traiettoria ad arco come linea luminosa. Il testo 2D rosso mono (CAMERA, LIGHT, MOTION, SOUND) si scrive lettera per lettera con un glitch di mezza parola (`LI` → `LIGHT`).
6. **I dati sono oggetti.** "Lines of code" è un contatore che sale con curva; "suono" è una scultura di barre. Il concetto astratto diventa qualcosa che la camera può attraversare.
7. **Confezione per Instagram.** Laptop su legno con ombre di finestra, intestazione "✗ → asterisco Claude", didascalia `No Blender. Just Claude 😮`, chiusura con parola chiave in commento ("Comment skill → I'll send you the file"). Ritmo: un evento visivo ogni 0,4–0,8 s, un cambio di scena ogni 1,5–2,5 s, tutto legato da barre spazzanti o tagli-veloci.

### Cosa fa già `world3d.py` e cosa gli manca (verificato nel codice)
| Ingrediente del video | Nostro motore oggi |
|---|---|
| Scena come funzione pura del tempo | **Sì** (identico principio) |
| Camera con curva e spinta lenta | **Sì** (`cam()`, "la camera non sta mai ferma") |
| Etichette agganciate agli oggetti | **Sì** (`label()`) |
| Luci direzionali + emisferica, tone mapping | Sì |
| **Ombre proiettate** (veneziana, strisce) | **No**: non c'è nessuna `castShadow` |
| **Pass argilla / inchiostro + barra di taglio** | **No** |
| **Motion blur** (sub-frame) e **sfocatura di profondità** | **No** (nessun post-processing) |
| Testo estruso 3D, testo luminoso in scena | No (solo etichette in HTML e `CanvasTexture`) |
| Particelle (polvere, vapore) | No |
| Barre/curve come oggetti-dato | No |

### Cosa copiare (in ordine di valore / costo)
1. **Pass "argilla → finale → inchiostro" con barra di taglio.** Collegamento fortissimo con la moda: l'**inchiostro è il disegno tecnico** (il flat), l'argilla è il toile/la tela di prova (05/08), il finale è il capo. Idea per il video del pantalone (#5): flat a inchiostro → cartamodello → tela → pantalone finito, con la barra che attraversa. Costo: basso-medio, nessuna dipendenza nuova.
2. **Ombre a strisce di veneziana** su un oggetto (il pantalone drill in luce calda). È la firma del video e costa poco: `castShadow` su una luce direzionale + un pannello di listelli davanti. Si adatta alla palette (ruggine, sabbia, inchiostro).
3. **Motion blur e sfocatura solo sui tagli-veloci.** Poiché ogni frame è una funzione di `t`, si fa con sub-frame (renderizzare t±otturatore e mediare 4–8 immagini). Costo: **×4–×8 sui frame di whip**: va misurato (il 4K a 60 fps non è ancora misurato). Solo 2–3 whip per plate.
4. **Particelle di polvere/vapore** e **testo estruso** per la parola chiave. Costo medio, effetto "wow".
5. **Struttura "capitoli = etichette"** (CAMERA / LIGHT / MOTION / SOUND): dà ritmo e un indice visivo; per noi diventano i quattro passi di una scheda (idea · cartamodello · tela · capo).
6. **Chiusura a parola chiave** ("Comment skill → I'll send you the file"): coerente con l'obiettivo del canale (accendere discussioni nei commenti), e va valutata per i video "fai con me" (come #4).

**Non copiare:** il laptop-cornice con ombre (rompe la regola 9d, schermate vere restano vere) e il formato verticale (noi 16:9).

---

## PARTE B. Il video teorico ("20 Principles of UX & Animation in under 30 seconds", @charles.unemployed, 26,9 s)

### Forma del video
Volto in alto, elenco dei 20 principi che si **riempie man mano** (quello corrente in arancione), un **timer LED rosso** (00.06 → 26.89) e sotto una **scheda bianca "Before | After"** con una mini-demo animata per ogni principio, più una riga di didascalia. Chiusura: "Comment 'motion' and I will send you the skill that teaches Claude to do all of this". Cioè: **stessa meccanica della parola chiave**.

Spunto di formato (non di contenuto): lista fissa che si completa + una demo prima/dopo di ~1,3 s per voce. Il nostro `versus.py` e `chips.py` coprono già il "prima/dopo" e le liste.

### I 20 principi e il verdetto per le nostre motion graphics
Legenda: **SÌ** = già nostro o da adottare · **SÌ, ADATTATO** = utile con una modifica · **NO** = in conflitto con un gusto votato da Jacopo · **N/A** = riguarda un'interfaccia da cliccare, non un video.

| # | Principio (demo nel video) | Verdetto | Come si applica alle nostre plate (esempio) |
|---|---|---|---|
| 1 | **Squash & stretch** (le cose si schiacciano all'impatto) | **NO** (come rimbalzo) · SÌ (come motion blur) | Gusto 13: "niente bounce". L'unica forma ammessa è lo *stretch* come scia di motion blur sui tagli-veloci 3D (Parte A). |
| 2 | **Anticipation** (piccola carica prima del gesto grande) | **SÌ, ADATTATO** — da provare in A/B | Non un "calcio": un contro-movimento di 2–4 fotogrammi (1–2 %) prima di una swipe lunga della board. Non è nei gusti votati: test cieco prima di adottarlo. |
| 3 | **Staging the focus** (guida l'occhio su una cosa alla volta) | **SÌ** (già: "un movimento primario") | Un solo elemento in movimento forte; gli altri si attenuano (opacità/desaturazione) mentre uno parla. |
| 4 | **Pose to pose** (fissa le pose chiave, il resto si riempie) | **SÌ** | È il modo in cui scriviamo già `cam()` e le plate: pose ai tempi delle parole, la curva fa il resto. |
| 5 | **Follow through** (le parti continuano dopo che il corpo si ferma) | **SÌ, ADATTATO** | Senza overshoot: gli elementi secondari **arrivano in ritardo di 2–4 fotogrammi** e si posano con ease-out (etichette dopo la card, ombra dopo l'oggetto). |
| 6 | **Slow in & slow out** | **SÌ** (già, regola "cambia velocità, mai costante") | Atterraggi ease-out, uscite ease-in. Verificare che nessun `ease:'none'` sopravviva sui movimenti visibili (il contatore del 3D usa `none` solo per il tempo). |
| 7 | **Moving in arcs** (curve, non linee rette) | **SÌ — da adottare** | Oggi le swipe della board sono dritte. Una swipe diagonale può seguire un arco leggero (2–5 % di curvatura); idem il cursore nei Tella. È il principio più "gratuito" della lista. |
| 8 | **Secondary action** (piccolo gesto che sostiene il principale) | **SÌ** (già: "una cosa viva", regola del dead frame) | Esempio: mentre appare un numero, una scintilla/linea sottile su un secondo livello. Mai più di una. |
| 9 | **Snappy timing** (durata = sensazione, UI sotto i 300 ms) | **SÌ** (già: 12 f = 0,40 s) | Le entrate sono a 0,40 s; **le micro-transizioni (cursore, chip, tick) vanno a 0,15–0,25 s**. |
| 10 | **Exaggerated feedback** (spingere oltre il reale perché il momento arrivi) | **SÌ, ADATTATO** | La nostra regola dell'unico overshoot (timbro di successo) è proprio questo: tenerlo come eccezione unica. |
| 11 | **Solid drawing in 3D** (dare profondità ai piatti) | **SÌ** (`world3d`, card in prospettiva) | Card/foto con leggera inclinazione e ombra morbida; **mai** inclinare un'interfaccia di prodotto (regola 52). |
| 12 | **Overall appeal** (somma di ogni dettaglio fatto con cura) | **SÌ** | Checklist di rifinitura prima del render (allineamenti, ombre coerenti, nessun frame morto). |
| 13 | **Fitts's law** (bersagli grandi e vicini sono più veloci) | **N/A** per il video; **SÌ, ADATTATO** per i Tella | Il cursore nei tutorial deve fare un arco, decelerare e atterrare **sul bersaglio ingrandito** (zoom sul pulsante prima del click). |
| 14 | **Bigger hit areas** (zona cliccabile > di ciò che appare) | **N/A** | Si traduce solo nei mockup: pulsanti disegnati con area generosa, mai minuscoli. |
| 15 | **Hick's law** (più scelte = decisioni più lente) | **SÌ** | Max 3–4 opzioni sullo schermo; elenchi lunghi a scoperta progressiva (una voce alla volta). Coerente con "meno plate, meno elementi". |
| 16 | **Miller's law** (teniamo ~7 elementi, raggruppa) | **SÌ** | Numeri e codici a gruppi (`4532 0151 1283 0366`), liste ≤ 7 voci, mai un muro di righe. |
| 17 | **Doherty threshold** (risposta entro ~400 ms) | **SÌ, ADATTATO — molto utile** | In video: l'effetto grafico parte **entro 12 fotogrammi dalla parola**. Già il nostro "la plate parte SULLA parola"; aggiungere un controllo del ritardo parola→primo movimento nei `qa-motion`. |
| 18 | **Postel's law** (accetta input sporco, restituisci pulito) | **N/A** | Si applica alle app, non al montaggio. (Analogo debole: tollerare piccole imprecisioni di tempi parlati senza spezzare la plate.) |
| 19 | **Jakob's law** (le persone si aspettano che la tua app funzioni come le altre) | **SÌ, ADATTATO** | Dentro un video: **grammatica visiva coerente** (stessa card, stesso ease, stessa grafica ad ogni plate: "le plate verdi sono il look del sistema") e finte interfacce che *somigliano* a quelle vere (chat di Claude come la vera). |
| 20 | **Frequency of use** (più si usa, meno deve animare) | **SÌ — il più importante per i video lunghi** | Gli elementi ricorrenti (etichette di capitolo, contatori, lower third) animano **a piena durata la prima volta, poi sempre più rapidi e sottili** a ogni ripetizione. Evita la stanchezza nei video da 10+ minuti. |

**Riassunto:** 14 su 20 si applicano (6 già nostri, 5 adattati, 3 nuovi: archi, frequenza d'uso, ritardo parola→effetto); 4 sono **N/A** (14, 18, parte del 13, 15 solo come regola di densità); **1** va a **NO** (squash & stretch come rimbalzo) e **1** è **da provare in A/B** prima di entrare (anticipation).

### I tre principi nuovi da proporre alla skill (da votare)
1. **Archi sulle swipe diagonali** della board e sul cursore dei Tella.
2. **Frequenza d'uso:** il secondo, terzo, ennesimo uso dello stesso elemento è più breve (−30 %, poi −50 %) e più sobrio.
3. **Ritardo parola→effetto ≤ 12 fotogrammi** come controllo automatico in `qa-motion.py`.

---

## Prossimi passi proposti (nessuno ancora eseguito)
1. **Prova 3D con ombre a strisce + pass argilla/inchiostro** su `world3d.py` (pantalone Drop 1): lab da 6–8 s a 1080p, misurare il tempo di render. Passi stimati: ombre ≈ 20 min, pass + barra ≈ 45 min, motion blur sub-frame ≈ 45 min + misure.
2. **Test cieco A/B** su una plate: stesso movimento con e senza arco; con e senza follow-through (ritardo 3 f).
3. **Aggiornare la skill solo dopo il voto di Jacopo**: i principi nuovi vanno in `references/taste.md` (non ancora toccato) e le tecniche 3D in `references/formats.md` §52.
4. Valutare per il video #5 la **chiusura a parola chiave** ("scrivi 'pantalone' e ti mando la scheda tecnica") in linea con "il canale serve a capire cosa sbaglia e a accendere discussioni".
