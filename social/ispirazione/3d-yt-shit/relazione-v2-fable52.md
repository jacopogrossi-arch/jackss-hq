# Relazione v2: «Fable 5.2 Make 3D Animations With Claude and Blender»

*Analisi del 23/11/2026 sul materiale in `videos/ispirazione-3d-yt/v2-fable52/`: trascrizione integrale, `prompt-e-comandi.md`, 17 fogli-contatto, frame a piena risoluzione (854x480). I timestamp con "~" vengono da `frames_full/` e possono essere spostati di qualche secondo. VISTO = inquadrato. DETTO = solo parlato.*

---

## 1. Scheda del video

- **Autore.** Canale/scuola **GenHQ**: logo a ~18:48, cartella "GenHQ" sul desktop. Il protagonista del film si chiama Rourke. L'account in basso nell'app è "rourke · Max" (~28:00), quindi Rourke è probabilmente anche il presentatore. Questo è un'inferenza: il nome del presentatore non è mai scritto.
- **Durata e formato.** 39:17, inglese. Parlato frontale a camera, alternato a grafiche e a schermate dell'app Claude e di un Google Doc.
- **Promessa** (00:40-02:35). Un framework "in 10 passi con prompt esatti" per fare scene 3D realistiche in Blender "senza nessuna conoscenza 3D", con i costi e una variante da 30 s "per clienti". Dice: «I'm not editing this for YouTube retention purposes».
- **"Fable 5.2".** È l'etichetta del selettore di modello nell'app Claude: «Fable 5.2 · Medium · Bypass permissions», visibile in ogni schermata di chat. Per il sound design dice di aver usato «Claude opus 5.5» (34:27, come trascritto). Non spiego altro: nel materiale non c'è.
- **Stack reale (VISTO).**
  - App Claude desktop (Mac) con tool Bash: `ffmpeg -i real_clip.mp4 -vf signalstats …` a ~33:38, `ls "Ocular Sound Effects" · 412 files` a ~35:12.
  - Blender pilotato "as code": il codice non si vede mai.
  - FFmpeg.
  - Higgsfield MCP: `generate_video · Seedance 2.5 · 16:9 · 1080p` (~06:44) e `generate_image · GPT Image 2` (~12:12).
  - Poly Haven, per esplicita autorizzazione nel prompt del passo 2.
  - ShotDeck per i riferimenti (14:54).
  - Render farm nominate (32:36): GarageFarm, RebusFarm, Fox Renderfarm, Blendergrid.
- **A chi parla.** Creativi senza competenze 3D che vogliono vendere spot. Il video chiude con il funnel GenHQ ("turn AI into your full-time career").
- **Il film d'esempio.** 16:9, 1920x1080, 24 fps, circa 45 s totali: clip reale + 35 s di CG + clip reale. Un robot-Claude arancione a blocchi, alto 10 cm, con cappa e maschera nere, finisce il montaggio di Rourke su un portatile in un parco.

---

## 2. Il metodo per capitolo

| Tempo | VISTO | DETTO |
|---|---|---|
| [00:00] | Film finale: robot sul portatile, crash di Premiere, mail inviata, robot davanti agli sticker. Clip reali in apertura e chiusura. | "Fatto tutto con Fable 5.2". |
| [01:27] | Grafica "FFmpeg — Free tool that lets Claude read every frame of a video". | Servono Claude Code con Fable, Blender e FFmpeg; senza FFmpeg "Claude non vede i video". |
| [02:41] | Lavagna "Great At": places, products, materials, lighting. | Non va bene per persone e animali fotorealistici; per quelli rimanda a Unreal "in un video futuro". |
| [03:48] | Barra "Real / CG / Real", Rourke ripreso su un tetto e poi la panchina "retextured" (~10:00, Original vs Retextured). | Il CG in mezzo è "tutto Blender, niente AI"; l'AI serve solo a restilizzare la clip reale. |
| [04:53] | Chat con 3 allegati (MOV, foto della panchina, Costa cup). Prompt di restyle. Output `park-restyle.mp4 · 0:14`. Griglia di 4 look ("Same Take · Four Looks", 07:00). | "Una sola chat per tutto il progetto". Promo Higgsfield con 3 giorni gratis. |
| [07:12] | Prompt per FFmpeg, risposta con `brew install ffmpeg`. Google Doc "10-Step Prompt Guide". | Copia-incolla e riempi le [INSERT]. |
| [08:04] | Passo 1. Character sheet "superClaude" (11:12-11:24), grafica dell'altezza 1 ft contro una persona (11:36). Prompt «Make me a character sheet of the Claude Code robot, but as a superhero with a black cape. Use GPT Image 2.» (~12:12). | Consiglia ~30 s per i token e per il render: 2,5-3 h su "un MacBook aggiornato". Character sheet a 360°, dimensioni esplicite. |
| [14:08] | Passo 2. Confronto "The Real Frame — Claude's Version" (16:36). "Continuity": laptop girato al contrario, "A Photo Of The Back" con gli sticker (17:24-17:36). Schermata Blender e riquadro "Same in Both? Colour Grade ✓ Textures ✓" (17:12). | Variante senza footage = "gamble". ShotDeck per i riferimenti. |
| [18:02] | Promo GenHQ. | — |
| [19:04] | Passo 3. Grafica "22 Shots". Shot list (11 voci visibili su 22) + "Storyboard Sheet" + "Test Pictures" (24:12). Piano Max a 200 $/mese, "25% Used", "$50 A Week · So About $12.50". | Gli schermi disegnati in Blender battono l'AI, che "scramble" i testi. |
| [25:21] | Passo 4. Animatic grezzo (26:24). | "Rende in minuti". Si giudicano solo storia, tempi e movimento. |
| [26:52] | Passo 5. Chat: v7 (~27:06), «Please fix the things that aren't working» come esempio sbagliato, v12 con nota a 0:32 (~28:06). Rough cut grigiastro (~27:40). | 22 iterazioni. Note con timecode + "don't change anything else". |
| [28:37] | Passo 6. Grafica "Time Estimate ~60 Min", "All Frames Rendered", "844 / 844". Prompt visibile solo in parte. | Si misura un fotogramma prima di stimare. |
| [29:57] | Passo 7. Before/after (30:55): robot sfocato dal motion blur. "2.5 Hours To Render — Our final render in Blender, on a MacBook Pro" (31:59). Render farm "~30 Min". | Fili d'erba, pieghe e vento sulla cappa, motion blur. Farm a ~5 $. |
| [32:50] | Passo 8. Original Footage vs Blender Render (33:12). Tabella Shadows/Blacks/Whites con i valori non leggibili (~33:38). Bash `ffmpeg … signalstats`. | Ombre del CG a 46, del reale a 20, portate a 28. |
| [34:00] | Passo 9: solo la barra "Opening Clip / Claude + Blender / Closing Clip" (34:10). Passo 10: prompt in chat (~34:36-34:42), cartella "Ocular Sound Effects" (~35:12). | Ore di rifinitura del suono con Opus 5.5. SFX da una cartella, da librerie gratuite o via MCP. |
| [35:28] | "Realism route": magazzino "Amazon". "Blender: Grey Shapes" → "Nano Banana: Start Frame" → "Seedance 2.5: Real Footage", "Almost Every Shot Is A Seedance Generation". | L'AI è più reale ma rovina gli schermi e i testi. |
| [38:26] | "Amazon Ad", 1.400 crediti contro una cifra in $ sfocata (si intravedono ~55 $ e 12,50 $). PDF + "superClaude Chat" in descrizione. | Per la parte Blender "costa questo". |

---

## 3. Il "10-Step Prompt Guide"

Ogni passo del documento ha la stessa struttura: *What you do / Copy this prompt / What you get back / Move on when / Watch out*. Questa struttura è la parte più utile del video: un cancello di uscita esplicito per ogni fase.

1. **Brief.** STORY in 3-6 frasi, LENGTH, SHAPE, WHAT IS REAL, WHAT IS CG, CHARACTER, MOOD in 3 parole, REFERENCE. Chiusura chiave: «tell me the story back in one sentence, send me a timestamped structure of the film, and list everything you need from me». *Watch out:* hanno tagliato gag che andavano spiegate (lunch bag, tokens, la foglia che cade).
2. **Mondo e personaggio.** Salvare l'ultimo frame della clip d'apertura e il primo di quella di chiusura come riferimento. Costruire la location «to match those pictures exactly», copiando posizione della camera, lente, posizione e orientamento degli oggetti. Luce su riferimento, Poly Haven permesso, personaggio da character sheet con la taglia esplicita, props da foto. Il testo dopo il punto 5 non si vede.
3. **Storyboard.** «Now plan the film. Do not animate yet.» Per ogni shot: numero, secondi, camera, azione in una frase. Momenti chiave da rendere leggibili. Ogni schermo progettato «as its own picture», con il testo leggibile alla dimensione che ha nello shot. Regole di camera. Poi «one low-quality test picture for every shot… as a single sheet». *Move on when:* un estraneo capisce la storia dal foglio.
4. **Animatic.** Tutto il film a bassa qualità, giunto con le clip reali. Poi l'autoverifica: «look at a sheet of frames yourself and check: nothing passes through anything else, hands and feet touch what they should, and the camera is never blocked», e «tell me honestly what you did not check».
5. **Note loop.** Nessun prompt-modello. Note con timecode, una correzione per nota, «don't change anything else».
6. **Render finale.** *(L'inizio non si vede; dal parlato: "the film is locked".)* Elenco puntato di cosa migliora rispetto all'animatic e stima dei tempi: «Measure one full-quality frame first; do not guess». Render in background «in a way that can pick up where it left off». Alla fine si controlla che i fotogrammi di ogni shot coincidano con la shot list.
7. **Max pass (opzionale).** Mettere i frame accanto a una foto reale e «list honestly what still looks computer-made». Correggere suolo, oggetto più grande, superficie del personaggio, ciò che si muove col vento, leggero drift a mano. Alzare la qualità e riportare il tempo per fotogramma. Non toccare storia e animazione. Prima un foglio before/after di 4 frame.
8. **Grade.** «Do it by measuring, not by eye»: stesse aree (ombre, erba, panchina) nel reale e nel CG, confronto dei numeri, foglio affiancato più tabella prima/dopo.
9. **Final cut.** **Mai inquadrato**: si legge solo il titolo.
10. **Sound.** MUSIC (umore e stile) e SOUND EFFECTS (lista dei momenti). Poi la cartella SFX dell'utente.

**Cosa manca e come lo ricostruiremmo.** Il passo 9 sarebbe un prompt di unione delle clip. Lo scriverei così: unisci in ordine le clip, controlla che durata e fotogrammi coincidano, normalizza il loudness, mandami un foglio dei tagli con ±2 frame attorno a ogni giunta. L'inizio del 6 è con ogni probabilità «The film is locked, do not change the story». La fonte giusta però è il PDF e la chat condivisa in descrizione, non una ricostruzione (vedi §9).

**Confronto con ciò che facciamo già.**
- **Già nostro.**
  - La partitura esterna (`score.py`: DUR, VO, LIPS, SHOTS) equivale alla shot list del passo 3, ma noi la scriviamo dopo, mentre animiamo.
  - La clip di prova di 3 s del Reel corrisponde al passo 4 in piccolo.
  - I fogli a 8 fps (`finish.sh`, `reel_finish.sh`) sono il "sheet of frames".
  - Le correzioni puntuali con timecode le facciamo già con Jacopo.
  - Una camera per inquadratura (`reel.py`) è più rigorosa della loro gestione degli shot, che non si vede.
- **Non nostro.**
  - Il cancello "Move on when" scritto per ogni fase.
  - Lo storyboard di still a bassa qualità di TUTTI gli shot prima di animare: nella prova del Reel lo shot s5 è passato per tre inquadrature (macro, taglio sul gesto, primo piano), e il foglio le avrebbe scartate prima.
  - La frase «tell me honestly what you did not check».
  - Il grade misurato.
  - Il render ripartibile con il conteggio dei fotogrammi per shot.

---

## 4. Tecnica in Blender

**Cosa si vede davvero.** Quasi niente del "come". Non c'è codice Python, il viewport di Blender compare solo in un riquadro a ~17:12, e non si vedono rig, curve, nodi o impostazioni di render. Tutto quello che segue è dedotto dai prompt e dai risultati.

- **Scena.** Ricostruita da frame di riferimento: camera, lente, posizione degli oggetti. Asset da Poly Haven. Laptop con gli sticker presi da una foto del retro (17:36). Gli schermi sono immagini progettate a parte e applicate al display (passo 3, punto 3): timeline Premiere, errore di crash, barra di export, Gmail. Gli screenshot reali di Gmail e Premiere sono stati dati come riferimento (21:38).
- **Personaggio e rig.** Un robot fatto di parallelepipedi: corpo, 4 zampe, 2 braccia a blocco, visiera nera con occhi emissivi, cappa (00:16-00:34). È un rig rigido per parti, oppure oggetti con parent: non c'è deformazione organica. **Non verificabile**: nessun rig inquadrato. La cappa nel max pass "si muove col vento e fa pieghe" (DETTO, 31:09): forse cloth o shape key, **non verificabile**.
- **Animazione.** Tutta dichiarativa nel prompt: «works frantically with his hands on the keys; shows feelings only through his eyes and by shaking». Gli errori corretti nelle note riguardano compenetrazioni (mano dentro il coperchio a 0:32) e reazioni mancanti (v7).
- **Camera.** Regole verbali: varietà di shot, niente wide vuoti, lato o dall'alto per vedere lo schermo. Nel film: dettagli macro sul robot, profondità di campo forte, scala giocattolo come la nostra. Nel max pass c'è il drift a mano.
- **Luce e materiali.** "Flat overcast daylight" uguale alla clip reale, materiali plastici opachi, poi usura e sporco nel max pass. Il motore di render non viene mai nominato né mostrato (Cycles o EEVEE: **non verificabile**). L'erba a fili e il motion blur fanno pensare a Cycles, ma è un'inferenza.
- **Verifica.** Non esiste un agente-giudice separato. L'unico ciclo di controllo è **Claude che guarda i propri fogli-contatto tramite FFmpeg**: storyboard (passo 3), sheet dell'animatic con la checklist compenetrazioni/contatti/camera (4), conteggio dei fotogrammi (6), before/after (7), misure con `signalstats` (8). Il resto lo giudica l'umano.
- **Iterazioni.** 22 versioni dell'animatic (DETTO), ma la barra laterale mostra una chat "Robot animatic v24" (~28:00). Nella chat inquadrata si vedono v7 e v12. Il robot dello storyboard (24:12, banda rossa) è diverso da quello finale: anche il design è cambiato strada facendo.
- **Tempi di render (incoerenti tra loro):**
  - 2,5-3 h per 30 s su MacBook (09:19);
  - passo 6 "~60 Min" (grafica);
  - max pass 2,5 h (parlato e grafica 31:59);
  - "about four hours for the whole film" nel documento (passo 7);
  - render farm ~30 min per ~5 $.

  Coerenza interna: 844 fotogrammi a 24 fps fanno 35,2 s, cioè i 35 s di CG dichiarati. Questo dato regge.

---

## 5. Sound design e post

- **Cosa fa.**
  - Prompt in due blocchi (musica + lista degli SFX legati a momenti precisi), poi la cartella locale di 412 file. Claude la scorre con Bash e "sceglie un suono per ogni momento" (~35:12).
  - Ammette "ore di rifinitura" con Opus 5.5: il primo passaggio automatico non basta.
  - Il mix e le eventuali misure di loudness non si vedono.
- **Post.**
  - Il grade è fatto in FFmpeg con le misure `signalstats` per area.
  - Il montaggio finale (passo 9) è dichiarato ma non mostrato.
  - Correzione del colore delle clip reali: fatta a monte con Seedance.
- **Cosa ci serve.**
  - Abbiamo già l'equivalente: Epidemic Sound via MCP con i file in locale, regole in `sound.md`, voce sopra ed effetti ~-18 dB.
  - L'unica idea nuova è la forma del prompt: **una lista di momenti con il suono atteso, data prima del montaggio**. Va bene per gli swish sui tagli e i tick sui plate del Reel (HANDOFF, punto 4).
  - La loro libreria è un pacchetto commerciale ("Ocular Sound Effects"): non serve.

---

## 6. Personaggi, rig, volto, bocca, lip-sync, voce

**Sulla bocca e sul lip-sync il video non dice e non mostra nulla. È voluto: il robot non parla e non ha la bocca.**

- **Espressione.** Due rettangoli emissivi che cambiano forma: alti e stretti a 00:22, quadratini piccoli a 00:25. A questo si aggiungono il "tremare" e la postura (si sporge, si nasconde dietro lo schermo). Lo dice il prompt del passo 4: «shows feelings only through his eyes and by shaking».
- **Voce.** Nessuna voce del personaggio. La risatina finale è un SFX. L'unico che parla è Rourke, in carne e ossa, nelle clip reali.
- **Persone.** Dichiarate fuori portata di Blender. Per gli umani realistici il video passa a Seedance ("realism route").

**Cosa vuol dire per noi.** Non è una soluzione da copiare così com'è:
- Jacopino porta **occhiali scuri**. Il SOP del gemello lo dice: niente strizzate d'occhi, "it would not show". La sua faccia recita solo con bocca, sopracciglia e testa, quindi il trucco degli occhi emissivi non si trasferisce.
- Inoltre Jacopino parla con la voce di Jacopo: togliere la bocca cambia il format.

**L'idea trasferibile è di regia:** decidere shot per shot **dove Jacopino parla in camera e dove reagisce soltanto**.
- I primi piani (dove la bocca sparisce sotto ~0,30 m, HANDOFF "Trappole") vanno messi sulle pause, sulle reazioni o sulla voce fuori campo, con sopracciglia, cenni e gesti.
- La bocca si mostra nei medi, dove regge.

Così si aggira il problema dei primi piani, ma non si risolve la qualità della bocca nei medi: quella resta un lavoro separato (Jacopo ci sta lavorando in un'altra sessione).

---

## 7. Valutazione critica

**Cosa funziona davvero:**
- La disciplina di produzione: approvare la frase-sintesi, la shot list, lo storyboard e l'animatic prima della qualità.
- I criteri di uscita per ogni fase.
- Le note con timecode + "non cambiare altro".
- Misurare un fotogramma invece di stimare.
- Il render ripartibile.
- Il grade misurato.
- Gli schermi come immagini: il punto più forte contro l'AI, e dimostrato dal film, dove crash di Premiere e Gmail si leggono bene.
- Il risultato finale in 480p ha un buon look "giocattolo macro" e regge il confronto con le clip reali.

**Marketing e promozione:**
- Sponsor Higgsfield con link e 3 giorni gratis (05:36, 06:48); in sovrimpressione compare un banner Black Friday (05:24).
- Segmento GenHQ (18:02-18:59) e chiusura.
- «tens of thousands of dollars in research», «proprietary information», "senza nessuna conoscenza 3D": nessuna prova a supporto.

**Contraddizioni tra detto e visto:**
- **"Una sola chat"** (04:57-05:22) contro una barra laterale con una ventina di chat: "Robot animatic v24", "Shot list v3", "Final cut + stitch", "Grass blades test", "Cape c…", "Laptop stickers fix", "Poly Haven assets", "Max pass renders", "Amazon grey blockout", "Thumbnail donut"… (~28:00, ~35:12, 12:12). In pratica il lavoro è stato diviso per fase.
- **"22 iterazioni"** contro "v24".
- **Le schermate di chat sembrano rifatte per la camera** (inferenza): in ogni passo, sopra il nuovo messaggio, compaiono sempre e solo il brief e la stessa risposta «Love this…» (14:36, ~28:00, ~33:38, ~35:12). In una chat reale ci sarebbero decine di messaggi in mezzo.
- **Tempi di render**: quattro numeri diversi (vedi §4).
- **La promessa "spot da 30 s per clienti"** viene mantenuta solo come realism route, in 3 minuti, con il progetto "Amazon" mostrato a frammenti.
- **La shot list a 24:12** racconta una storia diversa dal brief: il cliente chiede «Can we change the music?», «sends v8», «Wait, what? I'll take it». La storia è evoluta, il che è normale; il video però la presenta come lineare.

**Cosa mostra davvero rispetto alla promessa.**
- Mostra prompt, risultati e grafiche.
- Non mostra codice, scena Blender, errori veri di Claude, tempi reali di lavoro dell'umano o un fallimento.
- Il personaggio è il caso più facile possibile: un robot rigido senza volto. Niente deformazioni, niente bocca, niente dita.
- La garanzia "nessuna conoscenza 3D" vale per questo personaggio; per Jacopino, con rig Mixamo, bocca e mani, non vale.

---

## 8. Trasferibilità

Ordinata per impatto/sforzo.

| Idea | Come la useremmo | Sforzo | Impatto | Rischio |
|---|---|---|---|---|
| **Primi piani senza parlato** (regia attorno al limite, §6) | In `score.py`, ogni shot marcato "parla" (medio, bocca visibile) o "reagisce" (primo piano su pause o reazioni, sopracciglia e cenni) | basso | alto | basso: aggira il problema della bocca nei primi piani, non risolve quella nei medi |
| **Foglio storyboard di still a bassa qualità per ogni shot, prima di animare** | `reel.py --norender` + un frame per shot a 16 campioni → un foglio unico con i numeri degli shot, da mandare a Jacopo prima della clip di prova | basso | alto | basso |
| **Cancelli "Move on when / Watch out" per fase** | Una riga per fase in `twin-shot-blender-sop.md` (es. "move on when Jacopo capisce la storia dal foglio senza audio") | basso | medio-alto | basso |
| **Schermi e grafiche come immagini leggibili sul telefono** | Il foglio bianco di s3 (HANDOFF punto 3) diventa una texture col disegno tecnico del pantalone. I plate «€0» e «×2» (punto 4) controllati alla dimensione del telefono | medio | alto | basso |
| **Autoverifica con checklist + «dimmi cosa NON hai controllato»** | Nella skill `animation-quality-gate`: compenetrazioni (mano nel tavolo), contatti piedi/mani, camera mai ostruita, bocca visibile nei primi piani. Il rapporto finisce sempre con "non controllato: …" | basso | medio | basso |
| **Note con timecode + "non cambiare altro"** | Lo facciamo già; da formalizzare come regola per le correzioni chieste da Jacopo | basso | medio | nullo |
| **Render ripartibile + conteggio fotogrammi per shot** | `reel.py` salta i PNG già scritti; a fine render uno script confronta i PNG per shot con `SHOTS` di `score.py`. Contro la trappola di Blender in background (HANDOFF) | basso | medio | basso |
| **Misurare 1 fotogramma prima della stima** | Già in pratica (~7 s/fotogramma); renderlo obbligatorio prima di ogni render completo | basso | basso-medio | nullo |
| **Grade misurato** (`signalstats` su aree uguali) | Non abbiamo footage reale. Riferimento: la clip AI del test ibrido o lo Short precedente approvato; misurare ombre, pelle e tavolo e regolare la curva di `finish.sh` sui numeri invece che a occhio | medio | medio | medio: un riferimento sbagliato porta a un look sbagliato fatto bene |
| **Max pass "cosa sembra ancora finto" accanto a una foto reale** | Foto vera di un tavolo da taglio o di un tessuto accanto al render, con l'elenco dei difetti. Già fatto in parte nel gemello v2-v6 | medio | medio | tempo di render più che raddoppiato |
| **Prompt SFX come lista di momenti** | Lista "momento → suono" prima del montaggio, poi ricerca su Epidemic | basso | basso-medio | basso |
| **Restyle della clip reale** (Higgsfield/Seedance) | Separabile dallo strumento: Seedance 2.5 via ElevenLabs con video di riferimento ≤30 s (la loro clip è di 14 s). Solo se un giorno mettiamo Jacopo vero in apertura o chiusura | medio | basso oggi | crediti; il volto vero può cambiare |
| **Character sheet** (GPT Image 2 via Higgsfield) | Separabile: Gemini 3.1 flash image o 3-pro, poi Tripo. Ce l'abbiamo già (`assets-3d/`) | basso | basso (già fatto) | — |

**Cosa NON conviene copiare:**
- **La "realism route"** (Blender grigio → Nano Banana/Seedream → Seedance). Per noi sarebbe Gemini image + Seedance via ElevenLabs, ed è il test ibrido che abbiamo già fatto: bello, ma ~108k crediti per uno Short da 30 s. Per loro stessi distrugge schermi e testi, cioè proprio i nostri plate e disegni tecnici.
- **"Una sola chat per tutto"**: non lo fanno neanche loro, e da noi lo stato vive negli HANDOFF e nelle SOP, che reggono meglio.
- **Il personaggio senza bocca e con occhi emissivi**: Jacopino ha occhiali scuri e parla.
- **Higgsfield in qualsiasi forma** (per Jacopo non esiste più).
- **Il max pass a fili d'erba e cloth "al massimo"**: a 7 s per fotogramma su GTX 1060 raddoppia o triplica il render per un dettaglio che in 9:16 sul telefono si vede poco.
- **Le render farm a pagamento**: la spesa va chiesta e il guadagno è solo di tempo.

---

## 9. Dubbi aperti e 1080p

- **Non leggibile e non recuperabile col 1080p**, perché non è mai inquadrato o è sfocato di proposito:
  - testo del passo 9;
  - inizio del passo 6 (il frame di ~29:00 parte già da «Before you start»);
  - testo del passo 2 dopo il punto 5;
  - valori della tabella del grade a ~33:38 (celle vuote nel frame);
  - cifre in $ a 38:24-38:30 (sfocatura grafica).
- **Fonte migliore del 1080p:** il **PDF "The 10-Step Prompt Guide" e la "superClaude Chat" condivisa**, linkati in descrizione (38:36). Conviene che Jacopo apra la descrizione e li scarichi lui: un Google Doc o una chat condivisa difficilmente si leggono via fetch automatico. Dalla chat si capirebbe anche se esiste codice Blender riutilizzabile e quanti messaggi è costato davvero il film.
- **Dove il 1080p aiuterebbe**: solo per giudicare la qualità del render (texture, erba a fili, motion blur, gestione del macro). Le finestre utili sono:
  - **00:05-00:37** (film finale);
  - **30:50-31:20** (before/after del max pass);
  - **33:10-33:30** (affiancamento reale/CG dopo il grade).
- **Il resto non serve**: i prompt sono già leggibili a 480p.

**Verdetto 1080p: parziale.** Solo i tre intervalli sopra, e solo se vogliamo un confronto visivo con il nostro render. Per il metodo serve il PDF, non il 1080p.
