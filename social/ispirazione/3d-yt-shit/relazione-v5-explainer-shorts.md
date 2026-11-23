# Relazione v5 — «How to Make Viral 3D Explainer Shorts with Claude (Skill Included)»
*Analisi del 23/11/2026 sul materiale estratto in `videos/ispirazione-3d-yt/v5-explainer-shorts/` (480p, trascrizione Whisper small, 121 frame ogni 5 s, 6 fogli contatto, 55 frame a piena risoluzione dei prompt).*

## 1. Scheda del video
- **Autore**: nome del canale non leggibile nel materiale (non verificabile). Gestisce una community Skool chiamata «AI Quest» (6 $/mese, «100+ membri in due giorni»). Cita un suo video precedente sullo stile «Flat Pictures»/«Vogel» (trascrizione incerta sul nome).
- **Durata**: 10:05. Video interamente in motion graphics su fondo scuro (titoli bianchi, accento viola, card crema «pause to copy»). **Non c'è nessuna registrazione reale dello schermo**: terminale, log e codice sono ricostruzioni grafiche (a 05:30 la didascalia dice «wording from the build log»).
- **Promessa**: rifare con una skill di Claude Code gli Short 3D «spaccato» del canale *You Made It* (il loro «How a Jungle Hole Becomes the Cu Chi Tunnels» ha 37,7M di visualizzazioni a 00:05; 19 Short da ottobre, 105M totali). «Niente Blender, niente generatore di immagini, niente API key. È tutto codice» [00:13-00:20].
- **Stack reale (visto)**: Remotion + three.js (`[missing] Remotion and three.js (node_modules)` nel log di setup a 06:20), Python in `.venv`, FFmpeg, un manichino rigged `public/mannequin.glb`, font `public/caption.woff2`, script `scripts/setup.mjs` e `scripts/check.mjs`, timeline in `story.ts`.
- **A chi parla**: a chi usa (o vuole usare) Claude Code senza saper fare 3D; obiettivo commerciale: vendere l'iscrizione alla community (pitch a 00:43 e a 09:25).

## 2. Il metodo passo-passo
Legenda: **[V]** si vede a schermo · **[D]** lo dice solo a voce.

**Fase A — Come ha costruito la skill (racconto, una mattina, 4 versioni)**
1. [00:13] Mostra il suo Short accanto all'originale, stesso tema «per confrontarli inquadratura per inquadratura» [V: due Short affiancati, didascalia «You Made It · How a Jungle Hole Becomes…»].
2. [01:41] Claude «smonta» l'originale: 4.226 fotogrammi, più altri 3 Short del canale [V: striscia di frame e numero «4,226 frames»; l'analisi in sé è D].
3. [01:49-03:01] Estrae 6 caratteristiche dello stile [V: card numerate 1-6] — dettaglio in §4.
4. [03:07] «Serve Blender? No»: ombre dure e materiali semplici, un browser basta [D; V scritta «No.»].
5. [03:17] Prova da 10 s: 315 frame resi in 28 s (V: «315 frames · 26 s» sulla card, il parlato dice 28: piccola incoerenza). Bug: il buco del tunnel non si vede perché la camera è a 38 m e il buco è coperto dalla didascalia [V].
6. [03:32] Misura l'originale: il buco è il 10% della larghezza del frame → camera a 14,5 m [V].
7. [03:40] Il «trucco» del tunnel: il terreno è un unico muro piatto (sezione), e dove c'è un tunnel Claude «butta via i pixel»; fino a 48 buchi; cambiare un numero = scavare [V: card «one flat wall», «48 holes at once»; l'implementazione non si vede].
8. [03:57] Persone: prima capsule, poi l'unica cosa scaricata, un manichino di pubblico dominio con 46 animazioni; i vestiti sono «dipinti» per osso (testa/mani→pelle, spina/braccia→camicia, anche/gambe→pantaloni, piedi→scarpe) [V: tabella colori per osso e foglio di prova con 8 manichini a 04:05]. Bug: petto color pelle perché segue l'osso del collo [V].
9. [04:21] Primo Short completo, bug inattesi: inquadratura larga tutta nebbia; 50 sbuffi di fumo = un muro grigio; didascalie sottili nel video finale perché i test erano fatti con un browser diverso. Fix: confronto di tutti i frame suoi contro tutti i loro, rifatti cielo, alberi, terreno [V: card rosse con i bug, griglia di frame].
10. [04:45] Secondo e terzo Short senza tema: Claude sceglie un igloo [V]. Due errori trovati da lui: uomo seduto dentro il muro, contorno storto in cima [V].
11. [05:10] Prompt: «fix these two, and make sure it can't happen again» → nasce l'auto-controllo `check.mjs`: congela il mondo ogni 0,25 s (280 momenti), misura se un corpo è dentro un solido, 7 s [V card; durata 7 s D]. Rimettendo i bug, li trova entrambi (testa 30 cm fuori dalla cupola, contorno storto di 16 cm) più un terzo creato dal fix (gambe 16 cm dentro la panca) [V, frame `h_340`].

**Fase B — Come la usa chi compra (3 prompt)**
12. [06:00] Requisiti: Claude Code con piano a pagamento, cartella vuota con lo zip; Node, Python, FFmpeg gratuiti; GPU «aiuta» (la sua: GTX 1080 del 2016) [V].
13. [06:14] Prompt 1: setup; controlla il PC, chiede prima di installare (~1 GB), poi propone il video di prova igloo (70 s con voce e suono). Tempi dichiarati: 1 min install, 3:41 per il test «misurato tre volte» [V].
14. [06:43] Prompt 2: 20 idee, ognuna «piccola cosa → grande cosa», saltando i temi già fatti dal canale; rispondi con un numero; script con fonte per ogni fatto (igloo: 269 parole, 17 righe) [V: lista 20 idee illeggibile a 480p, due righe con tag «source · Wikipedia» e una «flagged · this source»]. Poi Claude si ferma.
15. [07:10] Registri tu la voce (tua o ElevenLabs) [V].
16. [07:20] Prompt 3: 8 passi senza domande [V barra laterale]: parole (tempi per parola) → timeline (`story.ts`, ogni evento agganciato a una frase, mai a un secondo) → mondo → immagini di controllo «guardate tutte» → self-check (0 problemi su 280 momenti prima del render) → suono (76 suoni «fatti da codice», anche la musica) → render (4.188 frame in ~2:40) → revisione.
17. [08:10] Revisione: un secondo agente «che non ha mai visto il progetto» riceve un frame per frase e risponde a due domande: ha senso fisico? qualcuno attraversa un solido? [V].
18. [08:24] Se qualcosa non va: lo dici con il minuto («At 0:32 the man sitting on the bench sticks through the wall.»), Claude corregge e aggiunge un controllo [V].
19. [08:35] «Make it yours»: un campo fisso (storia/ingegneria/spazio), un look tuo (colori, ora, meteo, «mostrami tre immagini di prova prima»), la tua voce; dopo ogni Short una regola nuova nello SKILL.md [V].

## 3. Prompt, comandi e struttura della skill
**Recuperabile (citazioni brevi, verificate sui frame):**
- Prompt 1: `Set up the skill from the zip in this folder.`
- Prompt 2: `Use the 3D Explainer Shorts skill. Pitch me 20 ideas for a short.`
- Prompt 3: `My recording is voice.mp3. Make the short.`
- Correzione: `At 0:32 the man sitting on the bench sticks through the wall.`
- Look: «Give my shorts their own look: <colours, time of day, weather>. Show me three test pictures… before you change anything else.»
- Campo: «From now on every idea comes from one field: … Write that into the skill.»
- Log `check.mjs` (3 righe `[problem]`), log `setup.mjs` (found/missing), frammento `story.ts` (`dig T("dig the entrance")`, `camera T("But the wind")`, `sound T("locks the top")`).
- Formula dello script: titolo «How a [piccolo] Becomes [grande]»; righe «If you…, you have a… / But… a problem / So you… a fix / But… / So… / Congratulations. You have built…» («4 of 4 Shorts · line for line»).

**Manca (paywall)**: lo SKILL.md vero, i riferimenti, il codice Remotion/three.js, `check.mjs`, la generazione dei suoni, il mapping parola→evento, il manichino (nome e fonte non dichiarati: non verificabile quale sia), le regole accumulate. Il frame a 09:15 con `+ rule from Short 1/2/3` è decorativo.

**Come la ricostruiremmo da zero** (senza comprarla):
1. `SKILL.md` con: formula dello script, le 6 regole di stile come numeri (distanza camera, altezza didascalia, durata movimento), gli 8 passi, il protocollo «errore → regola».
2. `words.json` da Whisper (lo abbiamo già) → `story` = lista di eventi `{tipo, ancora: "frase", offset}` risolti in frame al momento del build.
3. Mondo: in three.js (Remotion `@remotion/three`) o in Blender via bpy, stessa partitura.
4. `check`: campionare il tempo ogni 0,25 s e fare test geometrici (BVH/raycast in Blender, `Box3`/raycaster in three.js) sulle regole note.
5. Revisione cieca: subagente fresco con un frame per frase e domande fisse.

## 4. Tecnica: animazione, rendering, ritmo
- **Camera**: una sola ripresa, 0 tagli in 70 s, 21 movimenti di circa 1 s ciascuno [V/D 01:49]; sale dal lato alla vista dall'alto e una volta vola dentro un tunnel [V 02:05]. Distanza tarata sulla leggibilità dell'oggetto (buco = 10% del frame).
- **Inquadratura**: spaccato tipo plastico: terreno in sezione (terra rossa piatta), giungla sopra; personaggi piccoli. Didascalia al 52% dell'altezza [D 02:24].
- **Luce/look**: ombre dure, materiali semplici, nebbia; è il look «browser/WebGL», non fotorealistico. L'igloo: neve bianca, cielo chiaro, contrasto basso.
- **Movimento**: «il mondo cresce soltanto», niente sparisce; finale con camera che si allontana e tutto ancora lì [V 02:10-02:15]. Scavo = un parametro che allunga il buco. Persone con animazioni preconfezionate (cammina, inginocchiati, salta, balla) «ciascuna su una parola» [D 01:20].
- **Testo a schermo**: una parola alla volta, 277 parole = 277 didascalie, accese all'inizio esatto della parola [V]; bianco grassetto con bordo nero, singola parola centrata («Bombs», «Gas», «Rice», «Sleeping»). Su «this is…» un contorno si disegna attorno all'oggetto, 4 volte per Short [V 02:35].
- **Sound**: voce fuori campo; 76 suoni sincronizzati sulle parole, musica compresa, generati da codice [D; V solo forme d'onda illustrative]. Qualità dei suoni: non giudicabile dal materiale (audio a 16 kHz mono, non ascoltato nel dettaglio).
- **Hook**: i primi 3 s **non sono analizzabili fotogramma per fotogramma**: abbiamo frame ogni 5 s. A 00:00 si vedono i due Short affiancati, sinistro con la didascalia «Bombs» e il terreno in sezione già in vista, destro oscurato con «Come». Dell'hook degli Short originali sappiamo solo la formula verbale («If you…»). Hook del video lungo: numero grande (37,7M) + «Claude built it» + negazioni barrate (Blender/image generator/API key) entro 20 s.
- **Struttura narrativa**: «Se tu… (situazione) → Ma… (problema) → Quindi… (soluzione)» ripetuto, chiusa «Congratulations, you have built…». È un loop problema-soluzione con il mondo che si accumula: ogni «So» aggiunge un pezzo visibile.
- **Durata Short mostrati**: originale ~70 s (4.226 frame: se 60 fps = 70,4 s, coerente con «0 cuts in 70 seconds»); igloo 70 s (4.188 frame → 60 fps, deduzione). Il test da 10 s ha 315 frame, cioè ~30 fps: incoerenza non spiegata.
- **Render**: 4.188 frame in ~2:40 (≈26 frame/s) su GPU di 10 anni [D]. Per confronto, noi: ~7 s per frame in EEVEE.

## 5. Personaggi, voce, lip-sync, volto
- **Volto e lip-sync: nulla.** Il manichino non ha volto leggibile (testa liscia, cappello di paglia nei soldati, a 04:05), e la camera sta a ~14,5 m: i personaggi sono figurine. Nessuna bocca, nessuna espressione, nessun dialogo in campo.
- **Voce**: narratore fuori campo; «la tua o una voce AI tipo ElevenLabs, non importa» [07:10]. Tempi per parola calcolati dalla registrazione (strumento non nominato: non verificabile, plausibilmente Whisper).
- **Personaggi**: un solo modello rigged, ricolorato per osso; 12 persone nello Short; 46 animazioni di libreria; errori tipici = compenetrazioni (corpo nel muro, gambe nella panca).
- Conseguenza per noi: questo formato **elude** il problema della bocca invece di risolverlo.

## 6. Valutazione critica
**Funziona davvero (e si vede):**
- Il processo di «reverse engineering misurato» del riferimento (frame contati, % del frame, altezza didascalia) invece del gusto a parole.
- Il self-check geometrico prima del render e la regola «ogni errore diventa un controllo»: è la parte più solida e meglio documentata del video.
- La timeline ancorata alle frasi: ri-registrare la voce non rompe il montaggio.
- Il revisore cieco con domande binarie.
- La formula dello script, semplice e ripetibile.

**Marketing / fumo:**
- «I modelled nothing, animated nothing, edited nothing» e «you don't do any of this»: ci sono volute una mattina, 4 versioni, test su più Short e lui stesso ha trovato gli errori a occhio. Il «one prompt» è il prodotto finito, non il processo.
- La «viralità» è dell'originale (37,7M di You Made It); delle visualizzazioni del suo Short non viene mostrato alcun numero. Nessuna prova che la copia abbia performato.
- I log e il codice sono rifatti graficamente: non sono prove dirette.
- «Nothing else costs money» omette il piano Claude a pagamento e la community a 6 $/mese.
- Lo Short dei tunnel, l'unico confrontabile con l'originale, non è nello zip «di proposito».

**Limiti e semplificazioni:**
- Estetica WebGL: ombre dure, materiali piatti, figurine senza volto. Va bene per l'explainer storico, non per un personaggio-brand.
- «È tutto codice» vale perché lo stile è volutamente povero di dettaglio; il manichino è comunque un asset scaricato.
- Suoni «da codice» = risparmio, non qualità; non dimostrata.
- Il check trova solo compenetrazioni e contorni storti, cioè errori misurabili; non dice nulla su ritmo, recitazione, leggibilità.
- Il formato è già saturo: lo dice lui stesso («lo stile è facile da copiare ora»).

## 7. Trasferibilità al nostro caso
Ordinata per rapporto impatto/sforzo. B = Blender, R = Remotion/three.js.

| Idea | Come la useremmo | Sforzo | Impatto | Rischio |
|---|---|---|---|---|
| **Self-check misurabile prima del render** (B) | Script bpy che campiona ogni 0,25 s: compenetrazioni mano/corpo/tavolo (BVH), **area visibile della bocca in pixel** (render ID/maschera a bassa risoluzione o proiezione del decal sulla camera), distanza camera-viso < 0,33 m, mano fuori quadro. Blocca il render se fallisce. Attacca direttamente la «bocca che sparisce nei primi piani» e la «mano tagliata» dell'HANDOFF | medio | alto | basso |
| **Revisore cieco, un frame per frase** (B/R) | Subagente fresco riceve 1 frame per frase + clip labiale; domande fisse: si legge la bocca? la mano esce dal quadro? il gesto è sulla parola giusta? | basso | medio-alto | basso (giudizio LLM su frame singoli non vede il sync: resta la clip labiale) |
| **Errore → regola nella skill, sempre** | Lo facciamo già nelle SOP; renderlo obbligatorio a fine di ogni Short con una sezione «regole nate da errori» + un controllo automatico quando l'errore è misurabile | basso | medio | basso |
| **Timeline ancorata alle frasi** (B) | `score.py` oggi ha tempi in secondi; passare a ancore `T("misuri due volte")` risolte da `words.json`: se rifacciamo la voce (o passiamo a speech-to-speech) shot, gesti e plate si riallineano da soli. Il labiale a mano resta da rifare | medio | alto | medio (Whisper ±0,1 s: ok per camera e plate, non per la bocca) |
| **Formula script «Come un X diventa Y»** | Serie Inverso build-in-public: «Come un rotolo di drill diventa un pantalone», «Come una linea di gesso diventa una piega». Struttura Se tu… / Ma… / Quindi… / Complimenti, hai costruito… — in italiano, una persona, imperativo (coerente col metodo «fai con me») | basso | alto | medio (formula riconoscibile; va variata l'apertura) |
| **Mondo che cresce, piano sequenza in spaccato** (R o B) | Il pantalone che si costruisce pezzo per pezzo su un tavolo-plastico: cartamodello → taglio → cuciture → piega, niente sparisce, camera che sale e si allontana alla fine. Jacopino lontano, voce fuori campo | medio-alto | alto | medio |
| **Uscire dal lip-sync quando non serve** | Nei beat descrittivi Jacopino lavora a distanza o di spalle mentre la voce è narrazione; la bocca si usa solo in 1-2 primi piani (hook e punchline) dove la verifichiamo frame per frame. Toglie gran parte del problema bocca in attesa del nuovo metodo | basso | alto | medio (Jacopino perde presenza se lo facciamo sempre) |
| **Una parola alla volta + contorno su «questo è»** (HyperFrames) | Test A/B su uno Short: didascalia parola per parola al 52% vs i nostri plate a frasi chiave; contorno che si disegna sul capo quando la voce lo nomina | basso | medio | basso (la nostra ricerca dice «niente karaoke»: va misurato, non deciso) |
| **Misurare il riferimento in numeri** | Nei teardown aggiungere misure: % del frame occupata dal soggetto, altezza testo, movimenti camera/s, durata media dei movimenti | basso | medio | basso |
| **Stack Remotion + three.js** (R) | Per explainer/infografiche 3D veloci (render ~20-30 frame/s contro ~7 s/frame in EEVEE), oggetti Tripo in GLB, look da plastico. Abbiamo già il formato 52 three.js nella skill youtube-edit: estenderlo prima di introdurre Remotion | alto | medio per explainer, basso per Jacopino | alto (secondo stack da mantenere; qualità luce/materiali e personaggio inferiori a Blender) |
| **Manichino unico ricolorato per osso + libreria animazioni** | Per comparse (clienti, sarti) attorno a Jacopino: un rig Mixamo ricolorato per gruppi di ossa | medio | basso-medio | medio |

**Cosa NON conviene copiare:**
- Il modello di vendita (paywall della skill, «one prompt» come promessa).
- Il tema o lo stile dei tunnel: è saturo, e copiarlo ci rende uno dei tanti.
- I suoni «fatti da codice»: abbiamo Epidemic Sound con licenza, è meglio.
- L'estetica WebGL povera e i personaggi senza volto come formato principale: Jacopino è il marchio, e l'HANDOFF dice che il divario con l'AI è proprio nella recitazione del viso.
- Migrare Jacopino su three.js per risolvere la bocca: non la risolve, la nasconde.

## 8. Dubbi aperti e cosa verificare a piena risoluzione
- **Primi 3 s fotogramma per fotogramma** dello Short originale e dell'igloo: con frame ogni 5 s non è possibile. Estrarre 8 fps dei primi 5 s da entrambi.
- **Fps reali** degli Short (60 vs 30: 4.188 frame per 70 s contro 315 per 10 s).
- **Quale manichino** (nome/licenza) e quale strumento per i tempi delle parole: non dichiarati.
- **Lista delle 20 idee** a 06:50 e lista dei temi saltati a 06:55: illeggibili a 480p.
- **Testo piccolo** sotto le card (percorso `…/example.mp4` a 06:30, didascalie delle griglie di frame a 04:40): illeggibile.
- **Come vengono «buttati via i pixel»** del terreno (clipping plane? shader? CSG?): non mostrato.
- **Qualità dei 76 suoni** e mix: da ascoltare sull'audio originale, non sulla traccia a 16 kHz.
- **Numeri del suo Short** (visualizzazioni, retention): assenti. Cercare il canale e lo Short pubblicato per vedere se la copia ha funzionato.
- **Incoerenze**: 28 s (parlato) contro 26 s (card) per il test da 10 s; «one prompt» contro «4 versioni».
