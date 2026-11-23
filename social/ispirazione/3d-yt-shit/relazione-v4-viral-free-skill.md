# Relazione v4 — «How to Make VIRAL 3D Animated Videos With Claude (FREE SKILL)»

*Analisi del 23/11/2026, solo su materiale v4. Testi verbatim dei prompt: `videos/ispirazione-3d-yt/v4-viral-free-skill/prompt-e-comandi.md` (locale, fuori da git). Qui li parafraso: il repo è pubblico.*

Legenda: **VISTO** = in un fotogramma · **DETTO** = solo nel parlato · **DEDOTTO** = ricostruito da me · **NV** = non verificabile.

---

## 1. Scheda del video

| Voce | Dato |
|---|---|
| Autore | «Money Degree» (canale tutorial AI/soldi) |
| Durata / qualità | 17:50, file a 480p (854x480), inglese |
| Data | prove generate il 14/11/2026 (VISTO nella cronologia Higgsfield, 11:20); dati canale «as of Nov 15» |
| Sponsor | Higgsfield (Black Friday, fino a -60%), dichiarato a 01:21 e richiamato a 16:11 e 17:37 |
| Modello di business | skill gratis ma scaricabile solo dal **canale Telegram** dell'autore (Telegram → Google Doc «Video Resources» → Drive → SKILL.md da 30 KB). Il guadagno vero è l'affiliazione Higgsfield + la lista Telegram |
| A chi parla | principianti che vogliono aprire un canale «faceless» monetizzabile, non creator 3D |

**Promessa vs realtà.**
- «3D»: lo stile è 3D (testa a sfera bianca, toon-shaded), ma **nessuna scena 3D viene costruita**. Sono immagini Nano Banana Pro animate con Seedance 2.5 (VISTO).
- «Blender»: il titolo non lo cita, ma il gancio a 00:07 è proprio «niente Blender, niente keyframe». Blender non compare mai.
- Stack reale (VISTO):
  - Claude app (Opus 5.5 Medium) con la skill;
  - ElevenLabs per la voce: il file caricato si chiama `ElevenLabs_2026-11-14…_v4.wav`, frame 04:16;
  - Higgsfield con Nano Banana Pro (immagini) e Seedance 2.5 / Seedance 2.5 Draft (video con audio «On»);
  - CapCut per il montaggio.
- Il presenter in facecam ha un aspetto molto levigato da avatar generato (sfondo con fumo rosso/blu a 17:45). Che sia un avatar AI è **NV**.

## 2. Il metodo passo-passo

| Tempo | Passo | Tipo |
|---|---|---|
| 00:00-00:35 | Gancio: un video di un altro canale (What If… IQ, ~2,3 M) contro «questo è mio»; poi i dati del canale What If | VISTO |
| 00:24 / S00:26 | Dati NexLev: 4.037.482 viste in 30 giorni. Ricavo stimato **$7.283** in un fotogramma e **$8.640** in un altro; a voce «quasi 9.000». RPM stimato $2,14 | VISTO, cifre incoerenti, tutte stime |
| 00:28 | Tesi: «si clicca per una regola impossibile, si resta per vedere cosa costa» | DETTO |
| 01:43-02:15 | Download da Telegram/Drive, poi Claude: + → Skills → Manage → Upload | VISTO (anteprima skill illeggibile) |
| 02:19-03:32 | Si lancia `/what-if-studio`. Setup a domande numerate, una alla volta (§3) | VISTO |
| 03:35-03:55 | 10 idee in tabella; Claude ne consiglia una e dice perché; si sceglie la #1 «Skip Your Workday» | VISTO |
| 03:57-04:20 | Script + indicazioni per la voce + fact check (cita la stima di 90.000 ore di Gettysburg College). Voce: «qualsiasi tool o la tua» | VISTO / DETTO |
| 04:22-04:44 | Si carica il WAV. Claude restituisce i prompt di personaggi e luoghi | VISTO |
| 04:47-06:20 | Higgsfield: Nano Banana Pro, 16:9, 2K, batch 2. Prima «You.png», poi lo si allega come riferimento a tutte le altre immagini. Si scartano i tentativi brutti | VISTO + DETTO |
| 06:22-07:04 | «next»: prompt delle clip 1-5, poi 6-7, poi overlay opzionali con orari | VISTO |
| 07:05-09:25 | Seedance 2.5: durata, 16:9, bitrate High, 4K. **Trucco draft 480p** (45 crediti invece di 420 per 15 s). Riferimenti allegati nell'ordine indicato. 3 draft per clip | VISTO |
| 09:45-10:30 | Scelta della take su 3 criteri (azione, camera, volti), poi rigenerazione in 4K | VISTO |
| 10:33-11:10 | Seconda via: 4K diretto senza draft | VISTO |
| 11:11-12:46 | Clip 2: meno riferimenti («Seedance si concentra su ciò che serve»), 10 s, 4K a 280 crediti oppure 1080p a 160 | VISTO |
| 12:48-14:28 | CapCut: voce su timeline, clip in fila senza buchi, volume clip a -12 dB, export 4K | VISTO |
| 14:29-15:08 | «Risultato finale»: si vedono solo **circa 20 s su 60** | VISTO |
| 15:11-16:10 | Pacchetto upload: 5 titoli con conteggio caratteri, descrizione con capitoli, tag (339/500), 3 thumbnail, checklist | VISTO |
| 16:11-17:50 | Prezzi Higgsfield, contest da $1M, chiusura «pubblica stasera» | VISTO |

**Contraddizioni tra ciò che si mostra e ciò che si afferma**
- **Thumbnail.** Quelle mostrate su Higgsfield (15:54) hanno il testo dentro l'immagine: «ONE MORE?», «1 SECOND. AGE 25 / AGE 45», «TOO EASY. 9AM→5PM». I prompt della skill invece dicono «No text» e propongono testi diversi da aggiungere sopra: «9 TO 5 IN 1 SEC», «20 YEARS GONE», «DON'T TAP IT». **Le thumbnail mostrate non vengono dai prompt mostrati.**
- **Viste del suo episodio.** Il video con «oltre 2 milioni» è di un altro canale. Le viste dell'episodio dell'autore non si vedono mai (NV).
- **«Claude sincronizza ogni shot alla tua voce».** Il meccanismo non si vede mai: si vedono solo i tempi decimali (es. 0-2.6 s, 2.6-5.5 s). Che usi le pause del WAV, una trascrizione o una stima è NV.

## 3. La skill «What If Studio»: ricostruzione

**Cosa si vede**
- Il SKILL.md non viene mai aperto.
- Si vedono: la descrizione nel Google Doc (7 passi), il messaggio di avvio e le uscite in chat.
- La chat si intitola «Repeated "1" inputs»: l'autore ha risposto «1» a tutte le domande.

**Struttura ricostruita (DEDOTTO dalle uscite)**
1. **Avvio.** Una riga di promessa, poi i comandi `NEXT · REDO · FIX 03 [problema] · MORE · NEW · SERIES`.
   - FIX con il numero di clip permette di correggere una clip senza rifare tutto.
   - SERIES/NEW servono a fare puntate con gli stessi personaggi. L'ultimo messaggio dice: «Episode done. Type NEW for the next episode with the same characters and style» (VISTO, 16:08).
2. **Setup, una domanda per messaggio**, con opzione consigliata (stella) e «go» per accettarla:
   - Q1 formato: 8 nicchie (What If, passato, viaggio nel tempo, luoghi impossibili, come funziona, corto AI, motivazione, libero);
   - sotto-focus (per What If: soldi/vita quotidiana, informazioni nascoste che diventano visibili, scelte impossibili, tecnologia che sparisce, versioni alternative di te);
   - Q2 look: 8 stili, consigliato «3D white ball-heads»;
   - Q3 durata: 60 s / 3 / 5 / 7-9 (consigliato) / 10+ min;
   - Q4 destinazione: 16:9 oppure Shorts 9:16.
3. **Idee.** Una tabella di 10 righe: titolo «What If…», gancio in una frase, twist, testo della thumbnail. Poi la scelta di Claude con il motivo («la regola si capisce in un secondo, il twist colpisce anche in 60 s»). MORE ne genera altre 10.
4. **Script** in righe brevi, una frase per riga, in seconda persona.
   - Gancio nella prima riga; posta in gioco che sale; svolta «And there's a cost»; chiusa con un oggetto emotivo (scritta a pastello) e una domanda al pubblico.
   - Sotto: indicazioni per la voce (leggera, poi più lenta e scura, ultima riga sussurrata) e fact check con fonte.
5. **Timing.** Si aspetta il WAV, poi annuncia i tempi di ogni animazione.
6. **Bibbia visiva.**
   - Un blocco di stile identico, ripetuto parola per parola in ogni prompt.
   - Una scheda per ogni personaggio (corpo intero, frontale, sfondo grigio, niente oggetti né testo) e per ogni luogo (inquadratura larga, vuoto, niente scritte).
   - Ordine di generazione: prima il protagonista, poi tutto il resto con lui come riferimento di stile.
   - Varianti d'età trattate come personaggi separati: You / You-older, Lily / Lily-teen.
   - Criteri per scegliere tra i tentativi: testa a sfera pulita, vestiti che coprono il corpo, niente bande nere. Se un'immagine fallisce il controllo di sicurezza, la riformula.
7. **Clip.** Ogni clip contiene:
   - intestazione con numero, durata, formato e qualità;
   - riga «Attach (in this order)»;
   - frase «Image N è …» che ridescrive ogni riferimento;
   - blocco di stile;
   - luce per gruppi di shot;
   - lista di shot con tempi (inquadratura, movimento, azione, espressione);
   - «Hard cut between every shot»;
   - effetti sonori per shot;
   - coda fissa: niente musica, dialoghi, voci o narrazione; niente testo né loghi; volti, teste e vestiti identici; niente bande nere.
   - La qualità è decisa dalla skill: clip 1 in 4K, le altre in 1080p, sempre prima un draft.
8. **Overlay opzionali** con tempo: «9:01 AM» a 0:00, «5:00 PM» a 0:03, «90,000 HOURS» a 0:18, scritta a mano a 0:57, title card a 0:59 (VISTO, 06:56).
9. **Pacchetto upload.**
   - 5 titoli con conteggio caratteri; descrizione con capitoli e 3 hashtag; tag contati sul limite di 500.
   - 3 thumbnail (A rivelazione del potere, B costo, C scelta), ognuna con l'immagine da allegare e il testo da aggiungere.
   - Checklist: Test & Compare, commento fissato già scritto. Alla voce «Altered or synthetic content» risponde **No**, «è un look cartoon» (VISTO, 16:08).

**Clip recuperate dai fotogrammi** (prima non trascritte)
- Clip 05: 8 s, notte, You anziano da solo; 4 shot fino a 8 s.
- Clip 06: 5 s, 1080p, allega You-older, Lily-teen, Graduation.
- Clip 07: circa 8 s, finale con il disegno a pastello.
- Clip 04: **mai inquadrata**.
- Durate note: 15+10+7+8+5+8 = 53 s. Per arrivare a 60 s la clip 04 dovrebbe durare circa 7 s (DEDOTTO). I capitoli della descrizione (0:15, 0:32, 0:51) tornano con le clip 1-3 ma non con il resto: NV.

**Come scriveremmo una skill equivalente** (per il canale; per Inverso solo come serie collaterale, vedi §4)

Nome: `episodio-3d`, in italiano. L'uscita **non** sono prompt Seedance ma una **partitura `score.py`** per `reel.py`. La struttura per clip della skill si mappa quasi uno a uno: DUR, VO, SHOTS (tempi, camera, lente, azione), luce per shot, SFX per shot, taglio netto, overlay con tempo.

Sezioni del SKILL.md:
1. **Avvio e comandi**: AVANTI · RIFAI · CORREGGI shot N [problema] · ALTRE IDEE · NUOVA PUNTATA.
2. **Setup, una domanda alla volta**, ognuna con la risposta consigliata:
   - formato: «E se…» moda / errore di sartoria / mito sul capo / diario del brand;
   - durata: 20-30 s (consigliata) / 45 s / 60 s;
   - formato video: 9:16 (consigliato) / 16:9;
   - personaggio: Jacopino / Jacopino + capo / solo oggetto;
   - chi parla: narratore (consigliato, vedi §6) / Jacopino in camera.
3. **10 idee** in tabella: gancio, regola, costo/twist, testo copertina, oggetto eroe. Più la scelta motivata e il controllo che non ripeta un gancio già usato (taste-3d).
4. **Copione** in righe brevi: indicazioni per la voce in parametri eleven_v4, fact check con fonte, controllo «ha senso anche muto e solo letto».
5. **Timing deterministico** da Whisper `words.json` (lo abbiamo già), non da una stima: gli shot si tagliano sulle pause misurate.
6. **Bibbia visiva**: asset Blender/Tripo esistenti, palette, lenti; per ogni shot la distanza minima dal viso (≥ 0,33 m).
7. **Partitura** `score.py` + checklist dei controlli: clip di prova, foglio a 8 fps, clip labiale.
8. **Pacchetto upload** in italiano: titoli con conteggio, descrizione, max 5 hashtag su IG, 3 copertine per Test & Compare, commento fissato.

## 4. La formula «What If»

**Schema ripetibile (DEDOTTO dallo script e dalle 10 idee)**
1. **Regola impossibile** in una frase, capibile in 1 s, su un dolore quotidiano (lavoro, soldi, capo).
2. **Benefici in escalation**: un elenco ritmato («Mondays, skipped. Meetings, skipped. Whole bad years, skipped.»).
3. **Prezzo nascosto**: il potere costa memoria, vita o affetti. Le 10 idee usano quasi tutte la stessa famiglia di costi.
4. **Oggetto simbolo** che misura il costo (l'anello d'oro che si consuma).
5. **Scelta finale e domanda al pubblico**, che diventa anche il commento fissato.

**Ritmo e numeri**
- 60 s = 7 clip da 5-15 s, ognuna con 3-6 shot da 1-3 s, tutti a taglio netto: circa 25-30 inquadrature al minuto.
- La clip 1 da 15 s fa da gancio: 6 shot con cambio di luce da mattina a tramonto.
- Narratore in seconda persona («tu»), protagonista generico e senza volto realistico, 2-3 personaggi fissi.

**Perché dovrebbe funzionare**
- Curiosità sulla regola, poi «loss aversion» sul costo, poi identificazione grazie al «tu».
- La domanda finale divide il pubblico e porta commenti.
- Stile riconoscibile e serializzabile (stessi personaggi, nuova regola).

**Regge?** Come meccanica narrativa sì: è una struttura «premessa, escalation, costo, scelta» solida e indipendente dallo strumento.

Detto questo:
- (a) Le prove sulla viralità sono di **un altro canale** e i soldi sono stime NexLev incoerenti tra loro.
- (b) Le idee sono tutte variazioni dello stesso costo (memoria/tempo/vita): dopo 3 puntate stanca, e il formato è già saturo.
- (c) È un formato **faceless di finzione**. Il canale di Jacopo è build-in-public («studente, niente da venderti, documento») e il formato cozza con quella firma se diventa il contenuto principale.

Può funzionare come **serie collaterale breve** (9:16, 20-30 s) se la regola tocca la moda e il costo racconta il mestiere. Esempio: «E se ogni capo che compri durasse per sempre… ma ne potessi avere solo uno?». In questa forma serve Inverso, non lo diluisce. Non come format principale.

## 5. Coerenza, costi, tempi

**Come tiene la coerenza** (VISTO)
- Un'immagine madre del protagonista generata per prima e usata come riferimento di stile per tutte le altre.
- Blocco di stile identico in ogni prompt.
- Riferimenti allegati in un ordine fisso, con la frase «Image 1 è You (maglione…, orologio…)» che li ridescrive a parole.
- Allegare solo i riferimenti che servono a quella clip.
- Coda «volti, teste e vestiti uguali in ogni shot».
- Varianti d'età come personaggi separati.
- La scelta della take guarda anche i volti.

Nei fotogrammi finali la coerenza regge (maglione arancio, orologio, Lily gialla). Unica deviazione vista: nella clip delle stagioni il protagonista è una silhouette nera in controluce. **Nota:** il loro problema di coerenza non è il nostro. In Blender la coerenza è gratis.

**Costi (VISTO sui pulsanti)**
- Seedance 2.5: 4K ≈ 28 crediti/s (15 s = 420; 10 s = 280); 1080p = 16/s (10 s = 160; 15 s = 240; 30 s = 480); draft 480p = 3/s (15 s = 45).
- Stima (DEDOTTA) per l'episodio da 60 s come impostato dalla skill: clip 1 in 4K (420) + 45 s in 1080p (≈ 720) + draft (≈ 180 se 1 draft per clip, ≈ 540 se 3) ≈ **1.300-1.700 crediti**, immagini escluse.
- Costo delle immagini: illeggibile sul pulsante (NV).
- Il piano Ultra consigliato dà 3.000 crediti/mese, cioè circa 2 episodi da 60 s. Un episodio da 7-9 min (la durata «consigliata») in 1080p costa circa 7.000-8.600 crediti senza draft: **più di un mese di Ultra**. La promessa «una serata libera» regge solo per 60 s.
- Prezzi a voce: Plus da 49 a 39 $/mese, Ultra da 129 a 79, Ultra annuale 65. Nel fotogramma (16:32) si leggono Plus 29 $ e Ultra 65 $ (probabilmente annuale): i 29 non tornano con il parlato (NV).

**Tempi.** Generazioni «in pochi secondi», ma il video è montato. Il tempo reale per episodio è NV.

**Per noi**, senza Higgsfield:
- Seedance 2.5 via ElevenLabs costa circa **108k crediti per uno Short da 30 s** sulla via ibrida (twin-shot-blender-sop, riga 3), contro 0 crediti e circa 15 min di render del gemello Blender per 5 s.
- «Draft economico, poi finale una volta» lo facciamo già (still a 16-24 campioni, clip di prova): è una **conferma**, non un'idea nuova.

## 6. Volto, bocca, lip-sync, voce

Qui il video è utile proprio per ciò che **evita**.
- **Nessun personaggio parla mai in camera.** Ogni prompt di clip chiude con «niente musica, niente dialoghi, niente voci, niente canto, niente narrazione» (VISTO). La storia la racconta un **narratore fuori campo in seconda persona**.
- **La bocca è una linea disegnata sulla sfera.** L'emozione passa da sopracciglia, occhi, postura e mani, scritta in ogni shot: sopracciglia che crollano, sopracciglio alzato, ghigno, occhi lucidi, «bocca aperta per lo shock» solo nella thumbnail B.
- Tra i 3 criteri per scegliere una take c'è «i volti», ma non il labiale.
- **Voce**: ElevenLabs (VISTO nel nome file) o voce propria (DETTO). Le indicazioni per la voce sono testuali, non parametri. Gli effetti sonori li genera Seedance dentro la clip, poi si abbassano a -12 dB sotto la voce.
- **Volto del presenter**: possibile avatar AI (NV). Non si parla di lip-sync del presenter.

**Per noi** è un'opzione concreta, in linea con il verdetto del HANDOFF («La bocca della prova è brutta», Reel sospeso) e con la trappola della bocca che sparisce sotto 0,30 m:
1. **Narratore + Jacopino che reagisce.** La voce clonata di Jacopo diventa voce fuori campo. Jacopino recita con sopracciglia, occhi (dietro gli occhiali: serve compensare con testa e mani), gesti e sorriso (shape key `smile` già pronta). Bocca chiusa o quasi ferma: niente labiale A-H da fare a mano su P1/P2/P4.
2. **Ibrido**: labiale solo su 1-2 battute in medio (dove la decal regge, ≥ 0,33 m). Tutti i primi piani diventano mani, oggetti, spalle, controcampo: inquadrature in cui la bocca non si vede.
3. Lo stile «linea disegnata» insegna anche che una bocca **più semplice** (meno forme, più grafica) si legge meglio di una bocca semi-realistica in uno stile giocattolo. Da considerare quando Jacopo rifà il metodo.

## 7. Valutazione critica

**Funziona**
- La skill come **regista conversazionale**: domande una alla volta con default, comandi brevi, FIX per singola clip, NEW per la serie.
- Il prompt delle clip come mini-partitura (tempi, ordine dei riferimenti, luce, SFX, taglio netto).
- Draft economico, poi finale una sola volta.
- Il pacchetto upload completo (conteggio caratteri, Test & Compare, commento fissato).
- Il fact check dentro lo script.

**Marketing**
- «Viral» senza un solo dato sul proprio video.
- Ricavi stimati e incoerenti ($7.283 / $8.640 / «quasi 9.000»).
- «Ci ho messo giorni a costruirla», «nessun gatekeeping», ma la skill passa da Telegram.
- Il risultato finale mostrato a metà.
- Thumbnail mostrate che non vengono dai prompt.
- Il sincronismo alla voce come «parte magica» senza mostrarne il meccanismo.
- Tutorial sponsorizzato: Higgsfield presentato come l'unico posto possibile.

**Limiti**
- Costi che esplodono sulla durata consigliata (7-9 min).
- Idee ripetitive.
- Personaggi generici.
- Nessun controllo su recitazione e labiale.

**Rischi**
- **Divulgazione AI**: la checklist dice di rispondere «No» ad «Altered or synthetic content» perché è un cartoon. Per la policy YouTube l'animazione chiaramente irreale in genere non richiede l'etichetta, ma è un consiglio da non prendere a scatola chiusa: noi siamo già trasparenti sull'AI, e dichiarare costa poco.
- **Formato saturo** e copiabile.
- **Volti reali**: non usati nel video. Per noi il rischio vale solo se si genera Jacopo realistico con AI.
- **Dipendenza dalla piattaforma**: sicurezza, region lock del 4K, crediti.

## 8. Trasferibilità

Ordinata per impatto/sforzo.

| Idea | Come la useremmo (senza Higgsfield) | Sforzo | Impatto | Rischio |
|---|---|---|---|---|
| **Narratore fuori campo, personaggio che reagisce, niente labiale** | Voce eleven_v4 «Jacopo Prova» fuori campo; Jacopino recita con sopracciglia, testa, mani, `smile`. Sblocca il Reel sospeso | Basso | Alto | Perde il «Jacopino che parla» come firma: da testare su 1 Reel |
| **Primi piani senza bocca** | Primi piani su mani, tessuto, metro, spalle; labiale solo nei medi ≥ 0,33 m | Basso | Alto | Nessuno |
| **Skill «regista» a domande con default e comandi** (AVANTI/RIFAI/CORREGGI N/NUOVA PUNTATA) che produce `score.py` | Nuova skill in `.claude/skills/`, outline in §3 | Medio | Alto | Va mantenuta allineata a reel.py |
| **Prompt clip = partitura** (tempi da `words.json`, luce per shot, SFX per shot, taglio netto, overlay con tempo) | Formato standard di `score.py` + elenco overlay per HyperFrames/ffmpeg | Basso | Medio-alto | Nessuno |
| **Tabella 10 idee** (gancio / regola / costo / testo copertina) + scelta motivata | Passo fisso prima di ogni Short | Basso | Medio | Idee ripetitive: chiedere varietà di costo |
| **Pacchetto upload** (titoli con conteggio, 3 copertine Test & Compare, commento fissato, fact check) | Ultimo passo della skill; IG max 5 hashtag | Basso | Medio | Nessuno |
| **Formula «E se…» moda** come serie collaterale 9:16 | 3 puntate di prova, stessi personaggi, regola sul mestiere | Medio | Medio (NV) | Diluisce il canale se diventa format principale |
| **Bibbia di stile ripetuta parola per parola** + scheda personaggio madre | Per i still Gemini (3.1 flash image / 3-pro) di oggetti e copertine; per il 3D vale già il GLB Tripo | Basso | Medio | — |
| **Clip AI con più shot e SFX generati dentro** | Solo per momenti eroe, Seedance 2.5 via ElevenLabs, dopo aver detto i crediti | Alto (crediti) | Medio | ~108k crediti/30 s: non sostenibile per ogni clip |
| **Draft economico, poi finale** | Lo facciamo già (still bassi campioni, clip di prova) | — | Conferma | — |

**Prompt.** La regola di Jacopo dice: prompt con banana-pro-director e cinema-worldbuilder-pro. I loro SKILL.md non sono né in `D:\ClaudeCodeTest\.claude\skills` né in `C:\Users\Jacopo Grossi\.claude` (cercati). Dalle descrizioni:
- banana-pro-director è **legata a Higgsfield e fotorealistica**: è in conflitto sia con lo stile giocattolo sia con «niente Higgsfield». Va deciso da Jacopo se adattarla a Gemini/stile toy o derogare. Non lo risolvo io.
- cinema-worldbuilder-pro («solo audio diegetico, mai musica») è coerente con la convenzione delle clip What If.

**NON conviene copiare**
- Higgsfield e il flusso copia-incolla manuale tra due finestre.
- La durata 7-9 min con clip AI (costi).
- Lo stile «testa a sfera bianca», ormai firma di un genere altrui.
- La risposta automatica «No» alla divulgazione AI.
- I ganci sui ricavi stimati.
- La skill dietro Telegram come modello: per il canale vale «niente da venderti».

## 9. Dubbi aperti e 1080p

Due cause diverse per il testo mancante:

**A. Illeggibile per risoluzione** (il 1080p aiuterebbe)
- 02:48-02:56: anteprima e descrizione della skill nella finestra Upload (unico posto dove forse si legge un pezzo del SKILL.md).
- 04:32-04:44: prompt di Lily, Lily-teen, Office, Home (scorrono in piccolo).
- 15:40-15:46: parte centrale dei tag.
- 05:36 / 15:54: costo in crediti sul pulsante Generate delle immagini.
- 16:24-16:32: tabella prezzi (Plus 29 $ contro i 39 detti).

**B. Mai inquadrato perché scorso via** (il 1080p serve solo estraendo a 2-4 fps esattamente in quelle finestre, e potrebbe non esserci comunque)
- Clip 04 (06:40-06:52).
- Shot 3-6 e SFX della clip 01 (06:32-06:40).
- Prime righe dello script (03:57-04:00).

**Verdetto 1080p: parziale.** Vale riscaricarlo solo per 02:48-02:56, 04:28-04:48 e 06:28-06:56 (a 4 fps). Il resto non cambia le conclusioni: il metodo è già ricostruito, e il SKILL.md vero non si vede in nessuna risoluzione.
