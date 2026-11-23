# Relazione v1 — «Claude + Blender Is The Best Way To Make AI Videos (Full Course)»

*Analisi del 23/11/2026 sul materiale in `videos/ispirazione-3d-yt/v1-full-course/` (trascrizione Whisper, indice, prompt-e-comandi, 6 fogli contatto, ~25 fotogrammi a piena risoluzione e a cambio scena guardati uno per uno). Video a 480p: dove il testo non si legge lo scrivo.*

Legenda: **[VISTO]** = si vede a schermo · **[DETTO]** = solo nel parlato · **[NOSTRO]** = cosa facciamo già · **[NV]** = non verificabile dal materiale.

---

## 1. Scheda del video

- **Autore**: creator anglofono con un canale tutorial di video AI. In Claude desktop il saluto è «Good afternoon, dan» e il percorso dell'add-on mostra l'utente `daankieft` [VISTO, t1025/t1040]: il nome è «Dan». Ha la targa d'argento di YouTube sullo scaffale e un personaggio ricorrente, il robot **Bruiser** (cappello a rana, visiera con occhi LED, armatura arancione «07»).
- **Promessa**: «Blender + AI = coerenza tra scene e camera esatta». Due motivi dichiarati [DETTO 02:55-03:20]: 1) coerenza perfetta perché la scena esiste in 3D; 2) un riferimento di camera/oggetti migliore del solo prompt.
- **Stack reale mostrato**: Blender 5.2 (macOS), plugin Higgsfield per Blender (Scene builder con dentro Opus 5.5), Claude desktop (Opus 5.5 Medium) con connettore Blender MCP, Higgsfield Image (Nano Banana Pro, Seedream 5.0, Ideogram 4.5, GPT 2.5 Flare), Higgsfield Video con **Seedance 2.5** (Draft/Full), una skill scaricabile `seedance-2-5-prompter`.
- **Durata**: 22:29. Circa 2:49 di sketch iniziale (il «prodotto finito», interamente AI), poi circa 19 minuti di tutorial.
- **A chi parla**: principianti assoluti di Blender (spiega rotella, Shift, tasto 0) che pagano già Higgsfield. Non parla a chi sa usare Blender o scrive codice.
- **Quanto è «corso» davvero**: è un walkthrough di due flussi, con un buco centrale. Il flusso base è quasi tutto dentro il plugin Higgsfield. Nel flusso avanzato i prompt veri per Blender sono saltati di proposito: «this is all custom… you're not recreating my exact scene» [DETTO 20:00-20:07]. Niente codice, niente comandi da terminale, niente tempi né crediti totali. Il link al plugin Higgsfield è in descrizione e c'è una scritta grande «HIGGSFIELD LINK IN THE DESCRIPTION» [VISTO t240]: è un video con funzione di affiliazione.

## 2. Il metodo passo per passo

| # | Tempo | Cosa fa | Visto / detto |
|---|---|---|---|
| 1 | [00:00-02:49] | Sketch: lui e Bruiser in un rettilario, «wish granted», finiscono nel terrario inseguiti da camaleonte e serpente. Tutto video AI fotorealistico, con dialoghi e labiale degli umani. | VISTO (il parlato manca a 00:16-00:33 e 01:04-02:05) |
| 2 | [02:49-03:36] | Perché Blender: coerenza e riferimento di camera. Due flussi: «Beginner» e «Advanced». | VISTO (slide) + DETTO |
| 3 | [03:36-04:24] | Installa Blender, trascina lo zip del plugin Higgsfield, fa il login, preme `N`, scheda Higgsfield > MCP > «Enable MCP control». | VISTO: pannello con stato «Not connected», «Local execution bridge is off», URL `https://bridge.higgsfield.ai/mcp` (t260) |
| 4 | [04:41-05:45] | Scene builder: sceglie Opus 5.5 (alternativa gratuita «Higgsfield 3»), prompt POV del rientro a casa, chiude con «Create a low poly scene here in blender». Il prompt si spezza in chip numerati (01…06). Genera. | VISTO (prompt quasi intero) |
| 5 | [05:45-06:25] | Scena pronta in «5-10 minuti»: il corridoio, la moglie come pupazzo a blocchi, la stanza col PC. «Might look a bit glitchy… still our reference». | VISTO il risultato, DETTO il tempo |
| 6 | [06:28-07:46] | Navigazione base: rotella, Shift+rotella, Numpad 0 o View > Cameras > Active Camera. | VISTO (overlay) |
| 7 | [07:48-09:05] | Save As; Output > cartella > MP4 H.264 > Render Animation. «Ombre più naturali» del viewport. | VISTO |
| 8 | [09:06-09:38] | Modifica a prompt («the woman is carrying a crying baby…»), rigenera, rirenderizza. | VISTO |
| 9 | [09:39-11:23] | Asset: character sheet della moglie (fronte/retro/viso, fatto «come nei video precedenti», non mostrato). «Visual anchors»: screenshot di Blender (corridoio, postazione) dato a Nano Banana Pro 2K con «change this reference image… realistic and cinematic as if it was a live action still». | VISTO il risultato, prompt in parte |
| 10 | [11:24-12:52] | Installa la skill zip in Claude (Settings > Customize > Skills > Upload). Messaggio con `/seedance-2-5-prompter`, 1 video e 3 immagini, ognuna taggata a parole. | VISTO (testo leggibile) |
| 11 | [12:53-14:07] | Copia il prompt generato in Higgsfield Video, Seedance 2.5, carica gli asset e controlla a mano che @Image1/2/3 corrispondano (a lui no: «I upload these wrong»). Durata = reference (25 s). Consiglia Draft e poi upscale 1080p. Pulsante «Generate +400». | VISTO |
| 12 | [14:07-14:50] | Risultato 25 s: corridoio e stanza realistici, mano in POV, camera che ricalca il Blender. | VISTO (pochi fotogrammi, parlato assente) |
| 13 | [14:51-15:57] | Avanzato. Location: chiede a Claude un prompt text-to-image per un «location reference sheet» a 4 pannelli, lo prova su 4 modelli e sceglie Seedream 5.0. | VISTO |
| 14 | [15:57-17:36] | Collega Claude a Blender via MCP (dettagli al §3). | VISTO |
| 15 | [17:37-18:54] | Trascina il location sheet in Claude e chiede la scena. Claude costruisce un terrario di primitive (Python eseguito via MCP). Problemi: troppo piccolo, troppa vegetazione. Chiede «4x in size, remove the top…»; poi lo svuota fino a un asset «bare bone». «I dettagli li aggiunge il generatore video». | VISTO (parte del testo di Claude leggibile a t1105) |
| 16 | [18:55-19:38] | Consigli: «don't let Claude do the creative thinking», fai prima uno storyboard (griglia di fotogrammi AI della scena di inseguimento). | VISTO |
| 17 | [19:39-20:36] | Dà a Claude storyboard, immagini di Bruiser, sua e del camaleonte, più una descrizione a voce lunga. Claude blocca la Scena 01: 12 s, 24 fps, 288 fotogrammi, camera `CAM_Chase_Sh01`, tabella dei beat. Lui accorcia i beat parlando. | VISTO (testo quasi intero) |
| 18 | [20:36-21:35] | Export del reference (vista dall'alto: due figurine e un **blocco verde = il camaleonte**). Seedance 2.5 Draft: @Video1 + 4 immagini + **2 file audio con le voci** (sua e di Bruiser), 10 s, 16:9, 480p, «Generate draft +30». | VISTO il pannello; l'audio e il resto del prompt sono DETTI o illeggibili |
| 19 | [21:36-22:29] | Risultato: Bruiser e il camaleonte nella foresta, due battute. «Segue la camera esattamente… mi ha fatto risparmiare crediti». | VISTO + DETTO |

## 3. Setup Claude + Blender MCP

**Passi mostrati** [VISTO 16:00-17:36]:
1. Claude desktop > Settings > Customize > **Connectors** > cerca «Blender» > Install (lui l'aveva già). Toggle «Enabled».
2. View Details > Instructions: porta a una pagina «MCP Server» del sito Blender Lab. Requisiti: **Blender 5.1 o superiore**, Add-on, LLM Client, MCP Server. Avviso di sicurezza: l'MCP esegue Python generato dall'LLM senza sandbox.
3. Add-on: si scarica lo zip **senza aprirlo** e si trascina in Blender. La pagina, evidenziata in giallo, dice che col drag & drop **va fatto due volte**: la prima volta aggiunge il repository Blender Lab, la seconda installa l'add-on.
4. Edit > Preferences > Add-ons: deve comparire «**MCP**», altrimenti c'è un errore.
5. Preferences > System > Network: **Allow Online Access** attivo.
6. Add-ons > MCP: attivarlo e premere «**Start MCP Bridge Server**». Visto a t1040: host `localhost`, **porta 9876**, Auto Start, Timer Interval 250 ms.
7. Test in chat: «am I connected to blender?». Poi l'overlay «Claude MCP connected to Blender».

**Trappole che si vedono anche se lui non le commenta:**
- Nella lista ci sono **due add-on insieme**: «MCP» (estensione Blender Lab 1.0.0, in `extensions/user_default/mcp`) e «MCP for Blender» (il vecchio **BlenderMCP 1.6** legacy, `addons/blender_mcp.py`, «Connect Blender to Claude via MCP»). C'è anche l'add-on Higgsfield.
- Sotto il pulsante del bridge, a t1040: «**Server is stopped — [Errno 48] Address already in use**». Due server sulla stessa porta: con BlenderMCP e l'add-on ufficiale attivi insieme, il bridge non parte. Lui non lo dice. Regola per noi: **un solo add-on MCP attivo**.
- «Allow Telemetry» non spuntato nel BlenderMCP legacy.
- Claude lavora con il tool «Blender: Execute Python Code» (scritta visibile a t1105): costruisce tutto da Python, ma il codice non si vede mai.

**Confronto con noi** [NOSTRO]: abbiamo già il server `blender` in Claude Code, con `execute_blender_code`, `look`, `get_scene_info`, `import_asset`, `generate_3d`, `get_addon_status`. Il punto 7 equivale a chiamare `get_addon_status`. Soprattutto, la nostra pipeline seria gira **headless** (`blender -b -P script.py`, partiture esterne, una camera per inquadratura), che è più riproducibile della chat interattiva del video. Dal setup non c'è niente da copiare. Le due cose utili sono il controllo «un solo add-on sulla porta 9876» e il requisito Blender ≥ 5.1, che abbiamo già.

## 4. Prompt e struttura

**4.1 Scene builder (Higgsfield)** [VISTO t330]: un paragrafo narrativo in prima persona con l'azione in ordine, il tono della camera («sluggish replicating our exhaustion») e il vincolo tecnico «Create a low poly scene here in blender». La coda dopo «The …» non si legge. Il metodo è separabile dallo strumento: lo stesso paragrafo dato a Claude Code con il nostro MCP produce la stessa cosa.

**4.2 Location sheet** [VISTO t930]: «cinematic terrarium location reference sheet with 4 panels. one large horizontal image at the top which will be our main reference, and then 3 smaller panels at the bottom… close ups». Un pannello master grande e tre dettagli: un formato utile anche come riferimento d'ambiente per Claude in Blender. Da noi: Gemini 3.1 flash image / 3-pro al posto di Seedream.

**4.3 Tabella camera 0-12 s** [VISTO t1210], scritta da Claude dopo il blocking:
- 0-2 s dall'alto · 2-4 s scende su Dan · 4-6 s primo piano di Dan, tracking all'indietro da 3/4 frontale sinistro, «not head-on», battuta a 5 s · 6-7 s scivola su Bruiser · 7-9 s primo piano di Bruiser, battuta a 8 s · 9-11 s gira basso oltre Bruiser sul camaleonte · 11-12 s lingua.
- Tecnica dichiarata da Claude: camera che «follows an invisible aim target with a light handheld shake», **ogni beat segnato come marker sulla timeline**, scala **1 unità Blender = 1 cm** così le misure di riferimento entrano dirette, personaggi come primitive in una collection propria della scena, run cycle automatici, velocità derivata dallo spazio disponibile («2 body-heights per second»).
- Le battute sono messe su istanti precisi (5 s e 8 s) **prima** di generare il video: la partitura parlato-camera viene decisa nel blocking.

**4.4 Prompt Seedance generato dalla skill** [VISTO t780, parziale]. La struttura è la parte più trasferibile:
- frase-riassunto («A 25-second first-person POV scene, one continuous take…»);
- `[REFERENCES]`: un paragrafo per riferimento. La chiave è «@video1 is the motion and camera reference. Copy its camera path, timing… exactly. **Take only motion, camera and layout from @video1. Do not use its grey blockout look**, flat materials or simple figure shapes.»;
- `[CONTINUITY]`: Subjects (quanti, «One wife, one baby. Her outfit never changes»), Scene (cosa sta a sinistra/destra/davanti), Props (stesso oggetto per tutta la scena);
- `[STAGE 1 | 0-25s | …]`: camera, poi tempi a finestre (0-3 s, 3-7 s…). Dopo «The camera drifts…» il resto non è leggibile [NV].
- Nell'avanzato: «@Video 1 — Camera angles, framing and continuous camera path only… **Add strong handheld energy to this camera path.** The green block in @Video 1 marks …» (troncato). Come vengono taggati i due audio: [NV].

**4.5 Messaggio a Claude con la skill** [VISTO t770]: `using /seedance-2-5-prompter … write a 25 sec scene prompt`, poi una riga per ogni riferimento («@image1 is the character sheet of the woman»…), un vincolo di continuità («the pc stays turned off») e il contesto della scena. Lui lo ripete: «describe what each reference is».

**Cosa manca e come lo ricostruiremmo:** il contenuto della skill `seedance-2-5-prompter` (scaricabile solo dal link in descrizione, non nel materiale). Non serve: abbiamo già `cinema-worldbuilder-pro`, con Frame Map, Subject Lock, Movement e Last Frame. Le cose da aggiungere sono tre: un blocco **REFERENCES** con la formula «take only X from @video1, do not use its blockout look», un blocco **CONTINUITY** (soggetti contati, props fissi, layout sinistra/destra) e i **tempi a finestre allineati ai marker di Blender**. Non abbiamo né la descrizione a voce lunga inviata a Claude per la scena (vista solo la coda) né il prompt di generazione del terrario.

## 5. Il flusso ibrido Blender → riferimento → video AI

**Come passa la camera.** Nel video il render di Blender diventa un **video di riferimento** (@Video1) dato a Seedance 2.5, non un fotogramma iniziale e finale. La camera, i tempi e il layout si copiano dal video; l'aspetto viene dalle immagini. La durata del clip è uguale a quella del render (25 s / 10 s). L'avanzato aggiunge «strong handheld energy» sopra il percorso.

**Come si tiene la coerenza del personaggio.** Character sheet (pannelli dello stesso soggetto: «All panels represent one woman»), immagini come «visual anchors» degli ambienti ottenute dagli screenshot di Blender, la frase «Her outfit never changes» e il conteggio dei soggetti. Si vede un dettaglio che lui non commenta (t1295): i proxy in Blender sono **codificati a colori come i personaggi veri**. Il proxy di Bruiser ha il cappello verde e la visiera blu, il camaleonte è un blocco verde. Probabilmente aiuta il modello ad associare blocco e personaggio [interpretazione mia].

**Voce / lip-sync.** Nessun passaggio di lip-sync separato. Nell'avanzato carica **due file audio con le voci dei personaggi** come riferimento, «so we have that voice locked in» [DETTO 21:17-21:28]. È un riferimento di **timbro**: dal materiale non risulta che dia la battuta già registrata da sincronizzare. Il dialogo del risultato («Bruiser, get us out of here» / «I can't, I set a timer…») sembra generato da Seedance. Se la voce finale sia davvero la sua clonata: [NV].

**Confronto con la nostra prova ibrida** [NOSTRO, `hybrid-blender-ai-sop.md`]:

| | Video v1 | Noi (23/11) |
|---|---|---|
| Ingresso camera | render Blender come **reference_video** | layout → keyframe Gemini come **start/end frame** |
| Identità | sheet + anchor come reference_images | identità «dentro» i keyframe; gli sheet sono rifiutati con start/end |
| Push-in | ricalcato dal video | «quasi assente»: il modello l'ha ignorato |
| Voce | audio come riferimento di timbro, battuta generata | battuta vera + Sync 3 a parte (4.075 crediti) |
| Costo | non dichiarato (Draft 10 s 480p = 30 crediti Higgsfield) | 18.078 crediti EL per 5 s a 720p |

**Verificato oggi sul nostro connettore ElevenLabs** (`creative_get_model_schema`, gratuito): `bytedance-seedance-v2.5` ha le porte **`reference_videos`**, `reference_images` e `reference_audios`, oltre a start/end frame; durata 4-30 s; 9:16; 480p-4K. La guida del modello dice fino a 10 riferimenti e che con un audio collegato il modello «choreographs video to sound… with lip sync» (testo del fornitore, da provare). Quindi **il metodo del video è replicabile senza Higgsfield**: modalità a riferimenti, senza start/end frame (sappiamo già che con i frame i riferimenti vengono rifiutati). Che l'insieme video + immagini + audio venga accettato da ElevenLabs va controllato con `estimate_only` [NV].

## 6. Personaggi, volto, bocca, lip-sync

- **Sulla bocca e sul lip-sync non dice niente.** Nessuna tecnica, nessun passaggio dedicato.
- Si vede che **Bruiser non ha una bocca animata**: occhi LED su una visiera e una griglia rigida dove sarebbe la bocca (t1305/t1315). «Parla» senza labiale. Questo dribbla il problema invece di risolverlo, ed è una scelta di design del personaggio.
- Gli umani (lui, la moglie) hanno bocca ed espressioni fotorealistiche generate interamente da Seedance (smorfia a 01:46, battute). Nel blocking di Blender i volti non esistono: le figure sono primitive senza faccia.
- Per noi il punto è netto: **nel suo metodo la bocca la fa sempre il modello video**, mai il 3D. È l'opposto del nostro gemello (decal A-H a mano sul grafico in dB), e dal video non viene nessun aiuto per migliorare il decal.

## 7. Valutazione critica

**Cosa funziona davvero:**
- Separare *blocking* (camera, tempi, posizioni, scala) da *look* (immagini) e chiederlo esplicitamente nel prompt («take only motion, camera and layout… do not use its grey blockout look»). È il cuore utile del video.
- Riferimento video invece di prompt per una camera complessa: dall'alto, discesa, pan, tilt, in un solo piano. Lui dice che a solo prompt non ci riusciva.
- Scena ridotta all'osso («bare bone»): il dettaglio lo aggiunge il generatore. Si risparmiano tempo e viewport.
- Beat temporali come marker sulla timeline, letti poi dal prompt.

**Cosa è marketing o promozione:**
- Il flusso base è un tutorial del plugin Higgsfield (abbonamento a pagamento, link in descrizione, scritta gigante). «Full control over all of your generations» è esagerato: lui stesso carica male le immagini e la scena è «glitchy».
- L'apertura di 2:49 è il prodotto finito, ma il tutorial mostra solo **una** scena (10 s) di quella sequenza. Quante generazioni sono servite per lo sketch: [NV]. «After playing around with this» [20:23] non dice quante prove.
- Il titolo dice «Claude + Blender», ma metà del valore viene da Seedance 2.5 e dagli asset Higgsfield.

**Limiti:**
- Non mostra il codice né i prompt per Blender dell'avanzato. Non tratta né lip-sync né montaggio, né formato verticale (tutto 16:9).
- Nessun confronto A/B «con e senza reference»: la tesi «risparmio crediti» è solo dichiarata.
- I personaggi in Blender sono primitive: funziona per inseguimenti e POV, ma non dice niente su recitazione e primi piani parlati, cioè il nostro caso.

**Costi nascosti:**
- Higgsfield: abbonamento a pagamento, più «+400» per 25 s Full e «+30» per un Draft 10 s 480p. Il valore in euro: [NV]. Scene builder con Opus 5.5: crediti [NV].
- Per noi via ElevenLabs [NOSTRO]: 720p 5 s ≈ 14.000 crediti, 1080p 5 s ≈ 31.300. A prezzo lineare (ipotesi) **10 s a 720p ≈ 28.000** e 25 s ≈ 70.000, cioè metà del piano mensile (131k). Il suo flusso di prova «Draft» va sostituito con 480p su Seedance 2.5 via EL; il costo dei 480p non è nel nostro dossier e va chiesto con `estimate_only`.
- Generazioni multiple degli asset (4 modelli immagine per la location) e iterazioni non contate.

## 8. Trasferibilità

Ordinata per impatto/sforzo (prima le migliori).

| Idea | Come la useremmo (senza Higgsfield) | Sforzo | Impatto | Rischio |
|---|---|---|---|---|
| **Render Blender come `reference_videos` a Seedance 2.5** invece di start/end frame | Il layout di `ibrido-jacopino` (camera con push-in vero, Jacopino GLB) renderizzato EEVEE veloce → porta `reference_videos` su ElevenLabs Flows + sheet Gemini in `reference_images`. Risolve il «push-in quasi assente» | basso | alto | il set può derivare più che con i keyframe (senza start frame); combinazione di porte da verificare con `estimate_only`; crediti |
| **Clausola «take only motion/camera/layout from @video1, do not use its blockout look»** + blocchi REFERENCES / CONTINUITY | Aggiungerla a `cinema-worldbuilder-pro` come sezione per la modalità a riferimenti video | basso | alto | nessuno |
| **Voce vera come `reference_audios`** (lip-sync nativo) | Dare la battuta ElevenLabs «Jacopo Prova» come audio di riferimento: se Seedance anima la bocca sulla traccia, salta Sync 3 (−4.075 crediti) e la bocca la fa il modello. Test A/B contro Sync 3 su 5 s | basso | alto (sul nostro problema bocca) | il modello può rigenerare o alterare l'audio invece di usarlo: tenere sempre la traccia originale in montaggio e controllare il sync a 24 fps |
| **Partitura beat → marker** (battute su istanti precisi, scritte nel blocking) | Già simile alla nostra `score.py`: esportare i marker/tempi nel prompt Seedance come finestre 0-2 s, 2-4 s… | basso | medio | nessuno |
| **Proxy codificati a colori** come i personaggi | Nel layout usare il GLB vero (meglio dei blocchi); per i props usare il colore del prop finale | basso | medio | basso |
| **Location sheet a 4 pannelli** (master + 3 close-up) | Gemini 3.1 flash / 3-pro per il set dell'atelier; serve sia a Claude in Blender sia come reference_image | basso | medio | Gemini può inventare dettagli diversi dal layout: generarlo DAL render (vedi riga sotto) |
| **Visual anchor = screenshot Blender ristilizzato** | Render del layout → Gemini «same layout, realistic/toy-cinematic still» → reference_image dell'ambiente. È quasi il nostro passo 3 | basso | medio | è già nel nostro SOP: impatto solo marginale |
| **Scala 1 unità = 1 cm, camera su aim target, beat come marker** | Convenzioni per gli script headless (`reel.py`): utili ma già quasi coperte (empty rig + Shakify) | basso | basso | nessuno |
| **Scena «bare bone»** per il riferimento | Per il pass a Seedance basta un layout povero: render EEVEE a pochi campioni in pochi minuti invece di ~85 min | basso | medio (tempo) | se il blockout è troppo povero il modello inventa il set |
| Clip lunghe 25 s in un solo piano | Seedance 2.5 su EL arriva a 30 s, ma per i Reel servono tagli ogni 2-3 s: meglio 3-5 clip da 4-6 s con la stessa camera rig | medio | medio | crediti alti (25 s ≈ 70k a 720p) |

**Cosa NON conviene copiare:**
- Il plugin Higgsfield, lo Scene builder e il Draft Higgsfield: non esistono più per noi. Il loro equivalente è Claude Code + il nostro MCP + gli script headless, che è già più avanti.
- La skill `seedance-2-5-prompter` scaricata da un link di terzi: abbiamo `cinema-worldbuilder-pro`; integrare solo i blocchi citati.
- Il setup del connettore Blender in Claude desktop: l'abbiamo già, e due add-on MCP attivi insieme rompono la porta (Errno 48).
- La «scena dal solo prompt» lasciando a Claude la regia: lo dice lui stesso, e la nostra regola «camera centrata e frontale» (Short 16) va imposta nel layout.
- Il 16:9 e i 25 s in un piano unico: sbagliati per i nostri Reel 9:16.
- La «bocca risolta» togliendo la bocca (griglia rigida alla Bruiser): Jacopino ha bisogno della bocca, perché la voce è il brand.

## 9. Dubbi aperti e 1080p

Dove il 480p ha impedito di leggere:
1. **[20:45-21:25]** il prompt Seedance completo della scena avanzata: come dice «the green block marks…», **come tagga i due audio** (@Audio1/2?) e come lega le voci ai personaggi. È l'informazione più utile per il nostro test `reference_audios`. **Da riscaricare.**
2. **[13:00-13:15]** il resto del prompt della scena 25 s (STAGE dopo 3-7 s). Nel materiale non risulta che sia mai a schermo intero: a 1080p potrebbe restare troncato. Utilità media.
3. **[17:40-18:25]** il prompt dato a Claude con il location sheet e la prima risposta lunga (liste di oggetti, camera 24 mm). Utilità media: ci serve poco, il nostro metodo è headless.
4. **[19:40-20:00]** la descrizione iniziale della scena con storyboard e immagini: si vede solo la coda. Utilità bassa.
5. **[12:00-12:20]** nomi dei file della skill: inutile.
6. Durata e crediti reali dell'intera sequenza d'apertura: non sono nel video in nessuna risoluzione.

Il parlato mancante (00:16-00:33, 01:04-02:05, 14:07-14:33) è lo sketch e il risultato: non contiene istruzioni, non serve recuperarlo.

**Verdetto 1080p: parziale.** Vale riscaricare solo 20:40-21:30 (e, se costa poco, 12:45-13:15 e 17:40-18:25). Il resto del metodo è già chiaro, e il test vero si fa sul nostro connettore.
