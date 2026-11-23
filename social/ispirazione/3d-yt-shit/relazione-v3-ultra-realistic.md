# Relazione v3 — "How to Make Ultra-Realistic 3D Animated Shorts Using Claude (Full Workflow)"

*Analisi del 23/11/2026, solo su materiale grezzo in `videos/ispirazione-3d-yt/v3-ultra-realistic/` (trascrizione integrale, 6 fogli, frames_hi, frames_scene). Legenda: **[VISTO]** = a schermo; **[DETTO]** = solo nel parlato; **[DEDOTTO]** = ragionamento mio.*

## 1. Scheda del video

- **Autore:** "mr omi" / "Mr Omi" (canale YouTube; community Skool `skool.com/mr-omi-1113`) [VISTO 10:24]. Pagina Skool: "4.8K subs & 345K+ views in 3 weeks", **12 membri**, 45 $/mese [VISTO h_0105]. Il video precedente "How to Make Viral Animated Shorts Using Claude" ha ~250K viste [VISTO 11:42]. Gli "80 miliardi di viste" sono di Zack D. Films, non suoi.
- **Promessa:** rifare lo stile Zack D. Films (Shorts 3D anatomici/scientifici) con Claude + Blender, "real 3D, every single frame", render "da 8 h a 1 h" [DETTO 00:11-00:24].
- **Stack reale visto:** app Claude desktop su Mac, modello "Opus 5.5 Ultracode", piano Max [VISTO]; Blender 5.2 (citato "Install extension into Blender 5.2") con motore **Cycles** (citato nel profilo di render) [VISTO 05:54, 10:12]; dock con Blender, VS Code, Chrome, Terminale [VISTO 02:06]. Nessun MCP Blender nominato: Claude lavora via Bash/script (blocchi "Bash" a schermo) [VISTO]. Come esattamente pilota Blender: non verificabile.
- **Durata:** 12:25. Di cui ~1:40 finali = vendita della skill.
- **A chi parla:** principianti "faceless channel" che vogliono produrre Shorts in serie senza saper usare Blender ("you don't need to know Blender") [DETTO 11:10].

## 2. Il metodo passo-passo

1. **[00:00-00:27] Hook:** quattro Short affiancati, due di Zack D. Films e due suoi, "Doesn't look like AI, right?" [VISTO+DETTO].
2. **[00:12] Primo prompt:** due URL di Shorts + "go download this video and watch it frame by frame. Can we make the exact same video?" [VISTO].
3. **[01:00-01:48] Analisi della reference a 30 fps:** estrazione fotogrammi ("Extract 30fps frames, 10fps sheets, cuts, motion analysis") [VISTO h_0054], phase correlation per misurare zoom e pan per fotogramma. Output leggibile: stitches = 930 fotogrammi, pan medio 0,20 px/frame, 23% fotogrammi fermi, zoom jerk medio 0,0507 [VISTO ~01:36]. Conclusione: un'unica ripresa, dolly in per spiegare e dolly out per risolvere, zero pan [DETTO+VISTO].
4. **[01:57-02:38] Statistiche sui 50 Short più visti** (47.709 fotogrammi): luminanza mediana 0,52, contrasto 0,18, saturazione 0,44, sfondo RGB 82,164,222, loudness mediana **−10,4 LUFS**, 2,77 parole/s, quota tagli netti 0,14 [VISTO h_0022]. 16 copioni su 50 aprono con "If you…" [DETTO; lista evidenziata VISTA 02:18].
5. **[02:39-03:12] Regola chiave:** misurare il proprio render con la stessa pipeline; "the delta… is your to-do list" [DETTO]. Grafico "Camera motion: his short vs our first test" [VISTO h_0030]. Il primo test di 9 s aveva 8 volte il jerk; camera bloccata su un solo asse dolly con easing; jerk quasi dimezzato [DETTO].
6. **[03:13-04:24] Personaggio e ferita:** scansione umana scaricata (pantaloni lunghi, inutilizzabile) → "Nathan", scansione già riggata con camminata [VISTO 03:18-03:42]. View transform cambiata per salvare il blu; 2.600 peli 3D intorno al taglio; bug della ferita (decal a 0,25 mm che la triangolazione del render faceva attraversare), risolto usando la stessa triangolazione del renderer e legando la ferita alla pelle [VISTO testo ~04:00]. Ricerca su 869 texture Poly Haven: nessuna carne, usata una spugna scansionata [VISTO+DETTO]. Un agente Claude separato giudica gli still [DETTO; a schermo un "Opus check" con cifre poco leggibili].
7. **[04:25-04:54] Suono:** room tone di base, colpi a strati (peso + suono + dettaglio), riverbero che segue la camera, 19 tracce per 9 s [VISTO lista + timeline 04:36]. Correzione volume: stitch da 5,7 a 16,5 LU sotto la voce [VISTO].
8. **[04:55-06:43] Video vero ("blood vessels"):** copione riscritto con fact-check ("scientists estimate") [VISTO h_0054]. Faccia: Nathan ha solo vertex group (eye, eyebrow, eyelid, jaw, mouth) e `SHAPEKEYS None` [VISTO]. MetaHuman scartato (serve account + token, manca la libreria RigLogic compilata) [VISTO h_0059]. Sostituito da un'estensione open source dal sito ufficiale di Blender, verificata con checksum, 52 blend shapes "iPhone face capture" [VISTO h_0060, h_0066]. Claude stesso giudica il risultato "più un personaggio CG da videogioco che una persona reale" [VISTO h_0066]. Bug: occhi, denti, capelli e maglietta non attaccati all'armatura. Generatore di vasi sanguigni scritto da Claude [VISTO].
9. **[06:44-08:11] Ambienti:** erba 3D scartata (nera) → foto reale di stadio con piano che cattura solo le ombre; stadio fatto a mano bocciato come "AI slop" → copiata la soluzione della reference (campo su azzurro). Regola: "se esiste il reale, scaricalo". Ossa da database anatomico, città di ~440 edifici da kit di facciate Poly Haven, 34 nuvole volumetriche, Terra con immagini NASA [VISTO+DETTO].
10. **[08:12-09:30] Realismo:** 21 tutorial scaricati, 4 agenti in parallelo [VISTO h_0084]. Diagnosi: render "troppo perfetti" → bloom, vignetta, grana, motion blur, cambio della view transform (quella scelta "clippa le luci"), sole basso, ~1.300 alberi/auto/condizionatori, pelle opaca + SSS, denti verdi = luce rimbalzata dall'erba (fix: togliere la correzione) [VISTO h_0088].
11. **[09:31-10:21] Render:** 11 h → 7,5 h con impostazioni "identiche a occhio" [VISTO h_0097] → 3,5 h con render 1080p + upscale a 2K [VISTO h_0100] → cronometro per fotogramma e per inquadratura (log "TIMING f466 shot 3: render 8.7 s") [VISTO h_0103]: l'haze era trattata come sorgente luminosa (città 19 → 8 s), nuvole nella modalità volume lenta di Blender 5 (40 → 14 s); due Blender in parallelo; **888 fotogrammi in 61 minuti** [VISTO h_0104].
12. **[10:22-11:26] "Metodo facile":** allega `3d-shorts-skill.zip`, scrive "Use the 3D shorts skill. Here's his stitches short" [VISTO h_0107], 13 messaggi, dalle 19 alle 2 di notte [DETTO]. Mostra il confronto e una versione clay [VISTO 11:00-11:18].
13. **[11:27-12:25] Vendita** della community.

## 3. Prompt, comandi e struttura della skill

**Recuperabile (citazioni brevi):**
- Prompt iniziale: "go download this video and watch it frame by frame".
- Prompt "realismo": "Watch all of the videos… How to make a scene realistic" [h_0084].
- Prompt render: "Figure out if there is any way we can render it under 50 minutes without losing any quality" [h_0100].
- Prompt skill: "Use the 3D shorts skill. Here's his stitches short." + a voce "recreate it beat for beat but better".
- Nomi dei passi di Claude: "Measure camera + object motion", "Probe Nathan face bones/weights", "Retry Poly Haven texture index fetch + search", "Read the per-frame timing profile", "Re-time the 12 frames with all speed switches on".

**Manca:** il contenuto della skill (SKILL.md, script, riferimenti), tutto il codice Python/Blender, i valori di render (campioni, denoiser, bounce), il nome della view transform e quello dell'estensione dei volti. Non c'è nessun frame che mostri un file della skill.

**Come lo ricostruiremmo noi.** Con quello che si vede la skill è con buona probabilità [DEDOTTO] un insieme di quattro blocchi, e noi ne abbiamo già tre:
1. `analyze_reference.py`: fotogrammi a 30 fps, phase correlation (zoom/pan/jerk), luminanza/contrasto/saturazione, colore dominante dello sfondo, LUFS, parole/s (Whisper), tagli netti. Stesso script lanciato sul nostro render → tabella "delta".
2. Una regola sugli asset ("scarica il reale, non modellare a mano"), da adattare al nostro stile.
3. Una checklist di realismo (post, view transform, SSS) e una di velocità (profilo per fotogramma).
4. Un ciclo con giudice separato che dà un voto agli still prima del render.

## 4. Tecnica

- **Asset:** scansioni umane (Nathan), estensione open source per il volto, Poly Haven (spugna per la carne, kit di facciate), foto reale dello stadio, database anatomico per le ossa, NASA per la Terra. Pochissimo è modellato. Le eccezioni sono la ferita, i vasi (procedurali) e i peli.
- **Materiali:** pelle opaca con pori e SSS; spugna scansionata come interno della ferita. Valori: non verificabili.
- **Luce:** sole basso con ombre lunghe in città; sfondo azzurro RGB 82,164,222 come firma. HDRI: **mai nominato** (non verificabile). Interessante il problema del rimbalzo verde dell'erba sui denti: è luce globale vera di Cycles.
- **Camera:** un solo asse dolly, easing, niente pan, misurato con il jerk. Le transizioni della reference sono per 6/7 di movimento (whip pan, zoom-through) [DETTO]. Focali e DoF: non verificabili.
- **Animazione:** walk cycle già incluso nella scansione, espressione "sorpresa" da blend shapes, filo delle suture che "si disegna" lungo il percorso (un punto ogni 6-8 fotogrammi nella reference). Nessun parlato del personaggio.
- **Post:** bloom, vignetta, grana e motion blur, più la view transform cambiata per non bruciare le luci. Il nome della view transform non è mostrato. Che Claude avesse scelto "Standard" è una mia deduzione dal "clippa le luci".
- **Render:** Cycles; 888 fotogrammi (~30 s a 30 fps) in 61 min con due istanze. Trucchi: 1080p + upscale, esclusione dell'haze emissiva dalla light list, modalità volume corretta. GPU: non verificabile.
- **Audio:** room tone, strati per i colpi, riverbero per distanza di camera, una base per ogni ambiente, effetti sul fotogramma esatto ("bone knock" sulla parola "bones"). Mix finale: musica +3 dB, effetti −6 dB [VISTO h_0097]. **Incoerenza:** a voce dice che la reference sta "around −15 LUFS" [04:26], ma il suo stesso pannello dà mediana −10,4 LUFS [02:06].
- **Ritmo e hook:** la reference parla a 2,77 parole/s, apre in seconda persona ("If you…"), usa la ripresa unica per Short. Il suo video lungo apre con un confronto "4 video, quali sono AI?" in 12 s.

## 5. Personaggi, volto, bocca, lip-sync, voce

- **Lip-sync: nessuno.** In tutto il video il personaggio non parla mai in sincrono. La voce è fuori campo (narratore). Il volto fa solo un'espressione di sorpresa tenuta.
- **Volto:** la scansione ha solo ossa/gruppi grezzi e nessuna shape key [VISTO]. L'estensione open source dà 52 forme in stile ARKit, ma il risultato a 09:00-09:12 è un volto da videogioco: pelle cerosa, bocca rigida, denti verdastri [VISTO h_0091]. Il nome dell'estensione non è mostrato. La descrizione (sito ufficiale delle estensioni, nessun account, umano completo con rig ed espressioni) è compatibile con MPFB (MakeHuman), ma è un'ipotesi da verificare.
- **Voce:** "keep my voice" e "16.5 LU under your voice" [VISTO] dicono che la narrazione è "sua". La community però vende "Free AI voiceovers" [VISTO h_0105], quindi se sia registrata o sintetica non è verificabile.
- **In sostanza:** il formato Zack D. Films *evita* il problema bocca (narratore fuori campo + personaggio che reagisce). Il video non porta nessuna soluzione al nostro problema di labiale.

## 6. Valutazione critica

**Funziona davvero:**
- Il metodo "misura la reference, misura il tuo render, lavora sul delta". È la cosa migliore del video ed è indipendente dallo stile.
- Il profilo dei tempi per fotogramma per trovare i colli di bottiglia, invece di applicare a caso i "trucchi velocità" (lo dice anche Claude: "It's not the 3000× faster the video titles promise").
- La regola "scarica il reale" applicata con giudizio (lo stadio fatto a mano bocciato come slop).
- I macro sulla pelle (polpaccio con suture, 11:00-11:12) sono il punto più credibile [VISTO h_0111].

**Marketing o fumo:**
- "Ultra-realistic" vale per i macro su pelle e per la Terra. I volti e la città (blocchi bianchi tutti uguali, 09:54) sono chiaramente CG. Il titolo vende più di quanto si vede.
- "Da 8 h a 1 h" nell'hook, ma la cronologia reale è 11 → 7,5 → 3,5 h → 61 min, ottenuta anche abbassando la risoluzione nativa a 1080p.
- "13 messaggi" omette le ~7 ore di orologio e i giorni (dice "più di sei giorni") passati a costruire la skill.
- "Non dovete sapere Blender": i bug risolti (triangolazione, armatura, light list dell'haze, modalità volume) richiedono qualcuno che riconosca un errore guardando. È l'autore a notarli ("I noticed a bright strip").
- Il voto del giudice è riportato in modo incoerente tra voce (7 → 7,5 → 8,5) e schermo (si legge "6.5/10, up from 7.5", cifre incerte).
- La skill non si vede: tutta la parte "facile" è indimostrabile. Il pitch anti-"AI slop" per giustificare il prezzo è retorica di vendita. La community a 45 $ ha 12 membri.

**Limiti:** stile fotoreale Cycles, macchina non dichiarata, nessun codice, nessun personaggio che parla.

## 7. Trasferibilità al nostro caso

Il filtro che decide: noi siamo **EEVEE, stile giocattolo, personaggio che parla con la voce di Jacopo**. Lui è **Cycles, fotoreale, narratore fuori campo**.

| Idea | Come la useremmo | Sforzo | Impatto | Rischio |
|---|---|---|---|---|
| Misurare la reference e il nostro render con la stessa pipeline (zoom/pan/jerk per frame, luminanza, contrasto, LUFS, parole/s, tagli) | Script `measure_shot.py` nella skill fashion-3d: lo lanciamo su 3-5 Reel di riferimento e su ogni nostra prova; tabella delta al posto del giudizio "a occhio" | medio | alto | basso (rischio di inseguire numeri e non il gusto) |
| Jerk della camera come metrica | Controllo automatico su rig + Shakify: oggi Shakify aggiunge jerk; misurarlo sui medi parlati | basso | medio | basso |
| Cronometro per fotogramma e per inquadratura nel render | Stampare `TIMING fNNN shot X` in `reel.py`; trovare cosa costa (volume/haze, bokeh) prima del render da ~50 min | basso | medio | basso |
| Giudice separato sugli still con voto | Già vicino a `animation-quality-gate`: aggiungere un voto e una soglia ("render solo da 8/10") con un agente che non ha costruito la scena | basso | medio | medio (il giudice LLM è indulgente sulla bocca: va guardata a 24 fps) |
| Statistiche di copione: apertura in seconda persona, parole/s | Misurare le parole/s della voce Jacopo Prova contro reference italiane; testare l'apertura "Se tu…" su un Reel | basso | medio | basso |
| Transizioni di movimento (whip/zoom-through) invece del taglio netto | Tra due inquadrature di `reel.py`, mai dentro una battuta labiale | medio | medio | medio (motion blur che sbava: lo abbiamo già visto) |
| Suono che segue la camera (riverbero/top più spento nei campi larghi, secco nei primi piani) + room tone sempre presente | Due preset di EQ/riverbero in ffmpeg per larghi e stretti; tono di stanza sotto tutto | basso | medio | basso |
| Narratore fuori campo + Jacopino che reagisce (aggira il labiale) | Solo per alcuni Reel/beat: voce su B-roll di oggetti, Jacopino con espressioni e gesti, labiale solo sulla battuta finale | medio | alto sulla bocca | **alto: si perde il personaggio parlante, che è il marchio** |
| "Se esiste il reale, scaricalo" | Versione giocattolo: kit Poly Haven / Sketchfab per oggetti di scena e texture di tessuto, non modellare a mano | basso | medio | medio (asset realistici stonano col toy, come il pantalone Tripo) |
| Le 52 forme ARKit come vocabolario | Usare i nomi e la logica (jawOpen, mouthClose, mouthFunnel…) per ordinare le nostre forme A-H; più avanti cattura iPhone | alto | medio | alto (sul mesh Tripo `jawOpen` apre buchi frastagliati, già visto) |
| Post "camera imperfetta" (bloom, vignetta, grana, motion blur, view transform che non brucia le luci) | **Conferma**, non novità: già in SOP gemello (AgX Punchy, bloom 0,12, vignetta, grana ffmpeg) | — | — | — |
| Pelle opaca + SSS | **Conferma**: già nella v5 del gemello | — | — | — |

**Da NON copiare:**
- Scansioni umane, MetaHuman, volti fotoreali: per uno stile giocattolo sono la direzione sbagliata, e il suo stesso risultato è da videogioco.
- I trucchi di velocità specifici di Cycles (light list dell'haze, modalità volume): noi siamo su EEVEE. Vale solo il *metodo* del profilo.
- Città procedurali, nuvole volumetriche, 1.300 alberi: costo di render e manutenzione senza beneficio per una scena da tavolo da sarto.
- Render a 1080 + upscale: noi siamo già a 1080x1920 nativi.
- Il modello commerciale (community a pagamento, pitch anti-slop) e la promessa "senza sapere Blender".
- Il ritmo Zack D. Films (ripresa unica da 30 s, 2,77 parole/s "calmo"): contrasta con la nostra regola di un cambiamento visibile ogni ~2 s. Va misurato prima di adottarlo.

## 8. Dubbi aperti e verifiche (1080p sì o no)

Il 480p ha comunque permesso di leggere quasi tutti i testi della chat grazie ai frames_hi. Nessuna risoluzione mostrerà la skill o un lip-sync, perché non sono nel video. Il 1080p serve solo dove un dettaglio cambierebbe una nostra decisione:
- **[05:48-06:18]** Nome dell'estensione open source dei volti e del suo operatore (forse visibile in una riga di Bash scorrendo). È utile se vogliamo provare le forme ARKit.
- **[07:30], [08:00-08:06], [11:18]** Pannelli di Blender in finestra piccola: forse le proprietà di render/colore (view transform, campioni). Utile solo per curiosità tecnica, perché non usiamo Cycles.
- **[04:36]** Nomi delle 19 tracce audio nella timeline: utile per copiare la struttura degli strati sonori.
- **[01:36], [04:24]** Cifre coperte o incerte (zoom jerk max, voti del giudice): utilità bassa.

Non verificabili a nessuna risoluzione: contenuto della skill, codice, GPU usata, se la voce è registrata o sintetica, HDRI.

**Verdetto: parziale.** Conviene riscaricare solo la finestra 05:48-06:18, e al massimo 04:36. Il resto non serve.
