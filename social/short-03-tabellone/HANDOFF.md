# HANDOFF — Short #3 "Quanto costa lanciare un pantalone (se non hai un brand)" (16/11/2026)

Stato: copione APPROVATO da Jacopo. NON pubblicare (lo decide lui). Da fare in una sessione nuova.

## Cosa esiste
- `script.md` + `README.md`: copione a 7 battute, ~65 s, gioco da tavolo (caselle: disegno, cartamodello, foto, pre-order, arrivo, CTA "Scrivi PANTALONE", logo).
- `build-anteprima.py`: copia dello script del motore (1080x1920). Originale locale: `videos/_bench/short3/build.py`; fogli di revisione in `videos/_bench/short3/review/` (locale, fuori da git). Per girarlo serve il motore in `.claude/skills/fashion-3d/engine/` (snapshot: `TMP=D:\hf-tmp ... npx hyperframes@0.9.35 snapshot <cartella> --at a,b,c --no-end -o OUT`).
- Il pantalone nella casella "arrivo" e' un glb locale: `videos/_bench/fashion3d/blender/trouser10b.glb` (v10, colore #414b27, `fabric=True, grain=2.6, tile=3` nel motore). Si rigenera con `.claude/skills/fashion-3d/scripts/blender_trouser10.py` (Blender MCP, ~80 s). Nello script dell'anteprima il glb e' ancora quello vecchio: aggiornare il percorso.

## Da fare
1. Voce: ElevenLabs va riautorizzato da `/mcp` (voce "Jacopo Prova", id 0CeJTHP08UsLHht7KIni, vedi memoria reference_voce_elevenlabs). Poi costruire sulle parole (words.json), mix, revisione a 8 fps (memoria feedback_analisi_video_8fps).
2. Correggere l'anteprima: la card "€500–1.500" e' tagliata a 55 s; la vista della finestra di notte si vede appena.
3. Sostituire il pantalone dell'anteprima col glb v10 e, se serve, la scena atelier unita (esempio: `scripts/lab_merge_example.py`).
4. Procedura generale: `.claude/skills/fashion-3d/references/short-3d-sop.md`. Regole: niente "tela" nei video, mai Magnific/Higgsfield, hashtag max 5, commit per nome file (repo pubblico, `videos/` fuori da git).

## Altro in sospeso (non e' del Short)
- Pantalone v10: idee non fatte in `.claude/skills/fashion-3d/references/HANDOFF-trouser-v10.md` (spot dalla lampada, busto, gambe).
- Chiave Gemini in `.env` (locale): consigliato cambiarla perche' incollata in chat.

## File caricati in repo (16/11, perche' Jacopo non debba spostare nulla)
In `assets/`: `trouser10b.glb` (pantalone v10, colore finale), `anteprima-1.jpg` e `anteprima-2.jpg` (fogli di revisione dell'anteprima), `confronto-pantalone-round11.jpg` (riferimento vs scena unita). Nello script dell'anteprima usare `assets/trouser10b.glb` al posto del glb locale. Resta fuori dal repo SOLO la chiave `.env` (segreta, non va mai caricata).

## Aggiornamento 16/11 (sessione 2)
- Fatto: glb v10 (`assets/trouser10b.glb`) nell'anteprima, pantalone ridotto (fit 0.7), card €500–1.500 spostata in quadro.
- Resta: voce (serve /mcp → elevenlabs), finestra di notte quasi invisibile (parete troppo chiara), poi sottotitoli/mix/revisione 8 fps.

## Aggiornamento 16/11 (sessione 2, dopo la riconnessione ElevenLabs)
- Voce fatta: 7 paragrafi con "Jacopo Prova" (eleven_v3, 1 take ciascuno, ~760 crediti), posizionati all'inizio di ogni scena (0 / 5.0 / 14.9 / 26.2 / 38.2 / 50.2 / 58.6 s). File SOLO in locale: `videos/_bench/short3/vo/` (vo-placed.mp3 = 62,6 s). words.json (corretto a mano) e build nel repo.
- Anteprima: sottotitoli parola per parola + 2 frasi grandi ("Quanto costa lanciare un pantalone?" 0-3,6 s; "10, poi 20 non cento" 45-49,6 s); niente sottotitoli sotto le frasi grandi e dopo 58,4 s (la CTA 3D porta il testo). Camera allargata sui cartellini prezzi.
- Resta: musica Epidemic (non la stessa traccia dello Short precedente) + suoni, mix a -16 LUFS, bozza con finish.sh, revisione a 8 fps di TUTTO, finestra di notte (parete troppo chiara), poi 4K e consegna in iCloud. NON pubblicare.

## Aggiornamento 16/11 (sessione 2, sera): mix + bozza + revisione 8 fps
- Musica: Epidemic "Pixel Ghost" (HiP CoLouR, 98 bpm) in `assets/music/licensed/es-pixel-ghost.mp3` (locale, credito in CREDITS.md). `mix.py` (nel repo): voce + 23 suoni agganciati agli eventi del tabellone + musica 13 dB sotto la voce, -16 LUFS. Output `videos/_bench/short3/renders/mix.wav`.
- Bozza: `videos/_bench/short3/renders/draft.mp4` (30 fps). Revisione a 8 fps su tutti i 22 fogli: nessun sfarfallio. Corretti: cartellino €3.000-8.000 tagliato e laptop in ritardo (camera piu' larga 29-35 s), frase "10, poi 20" riallineata alla voce (46.5 s).
- Resta (decisioni/qualita'): finestra di notte (parete chiara), cartellino "tempo, non EUR" illeggibile nella vista dall'alto (20-26 s, il sottotitolo lo dice), finale un po' affollato (card + CTA + logo + Jacopino). Poi: ascolto reale della bozza da parte di Jacopo, render 4K (~20 min), consegna iCloud. NON pubblicare.

## 16/11 sera: render finale
- Finestra con foro (vista crepuscolo), cartellino tempo ingrandito, finale alleggerito. Render 1080p 60 fps: `videos/_bench/short3/short3-tabellone-v1.mp4` (65 s, 87 MB), copia in iCloud `Video 3D moda\short3-tabellone-v1.mp4`. Resta: ascolto/ok di Jacopo, eventuale 4K, titolo+descrizione (max 5 hashtag), pubblicazione SOLO se la decide lui.

## 16/11 notte: VERSIONE 2 (il tabellone e' bocciato)
- Jacopo ha bocciato la versione "gioco da tavolo" (troppo lenta, Jacopino e grafiche brutti). Rifatto come **sala campioni di notte** (stile studio di notte, mondo nuovo): `v2/` (build.py, room.py, mix.py, final1080.sh). Progetto locale `videos/_bench/short3b/`. Voce e words.json invariati (non rigenerare).
- Struttura: logo capovolto -> 5 postazioni (scrivania disegno, tavolo da taglio, set foto, parete 100 pezzi 10+20, pantalone appeso) con 5 salite sulla mappa; contatore "il mio costo"; un movimento camera ogni 2-3 s; fine con logo + CTA "Scrivi PANTALONE".
- Musica Epidemic "Pixel Ghost". Render finale: `short3-sala-campioni-v2.mp4` (1080x1920, 60 fps) in iCloud `Video 3D moda\`.
- Da migliorare se Jacopo lo chiede: set foto (macchina e softbox ancora blocchi semplici), colore dominante marrone, inquadrature scure a 17-19 s.

## 17/11: VERSIONE 3 (review di Jacopo sulla v2)
Note di Jacopo sulla v2 e cosa e' stato fatto (progetto locale `videos/_bench/short3c/`, sorgenti in `v3/`):
- Voce non sua / poco espressiva -> rigenerata con `eleven_v4` (la v2 usava `eleven_v3`, errore). Misurato: v4 ~ voce Short #2. Nuovo testo CTA: "A quanto lo vendo, alla fine? Scrivi PANTALONE nei commenti e ti dico il prezzo finale." (plate "Scrivi PANTALONE nei commenti" + card "e ti dico il prezzo finale").
- Logo che gira a 0:00 gia' usato nello Short #2 -> apertura sul pantalone appeso con card "€ ?"; logo solo alla fine (cade e gira).
- Pop sound (0:10, 0:23, 0:35, 0:53) -> sostituiti da swish morbidi (regola: niente pop).
- Plate "< €30" entrava prima e usciva subito -> entra su "30", resta fino alla salita sulla mappa (pausa piu' lunga prima della seconda tappa).
- Stampella mancante -> gancio + barretta + due pinze.
- "Te in miniatura": il busto di cartone con la foto e' stato BOCCIATO ("cartonato no"). Ora e' un omino stile Lego con occhiali tondi, capelli sparati in su, maglia nera, jeans con cimosa rossa, stivali texani: `.claude/skills/fashion-3d/engine/vendor/atelier-mini.js`, `w.minime(...)`. Parla (bocca, testa, mano) sulle parole. Resta il tipo `w.standee` (cartonato) nel motore, non usato.
- Render: `short3-sala-campioni-v3.mp4` (1080x1920, 60 fps) in iCloud `Video 3D moda\`.

## 17/11 sera: omino da foto (in sospeso)
- Provato Blender headless (`.claude/skills/fashion-3d/scripts/blender_minime.py`, 2 giri): volto scolpito da script NON convince (testa a uovo, capelli a squame). Le nuove skill Blender (blender-modeling ecc.) dicono che i personaggi organici sono fuori dal loro campo.
- Jacopo (17/11): provare image-to-3D dalla sua foto e/o le skill Blender con l'MCP. Il Blender MCP NON e' collegato in questa sessione (server `blender` in timeout; serve Blender aperto con addon connesso + riavvio sessione). Gli unici image-to-3D visibili qui sono Higgsfield `generate_3d` e Magnific `models3d_generate`, due servizi che Jacopo ha dismesso: non usati senza il suo ok.
- Input pronti in `videos/_bench/minime-input/` (locale). Nel video v3 resta l'omino stile Lego senza occhiali.

## 17/11 notte: PIANO CONCORDATO CON JACOPO PER L'OMINO (da riprendere in nuova sessione)
**Tutti i pareri di Jacopo, in sintesi (da rispettare):**
- Omino: NO cartone, NO "tre solidi uno sopra l'altro"; deve ASSOMIGLIARGLI ma NON realistico: stile giocattolo/cartoon coerente col video. Senza occhiali. Capelli alzati/dritti. "Se no semplicemente lasciamo stare."
- Strumenti: ok a un servizio image-to-3D SOLO via API a consumo (niente abbonamenti); lui crea la chiave e mette i dati di pagamento. Prima mi serve il Blender MCP collegato (Blender aperto con addon, sessione riavviata) e le nuove skill Blender (9 MIT in `.claude/skills/`).
- Voce: solo `eleven_v4` (mai v3). Niente suoni "pop": solo swish morbidi. Apertura mai uguale a un video precedente. Plate "< €30" deve entrare sulla parola e restare. CTA chiara ("scrivi PANTALONE nei commenti e ti dico il prezzo finale"). Stampella visibile.
- Bozza v3 (`short3-sala-campioni-v3.mp4`) in revisione da parte di Jacopo: aspettare i suoi pareri; NON pubblicare.

**Fatto stanotte:** immagine stilizzata (toy/vinyl, full body, A-pose, fronte, sfondo grigio, senza occhiali, maglia nera, jeans cimosa, stivali texani) generata con Gemini `gemini-3-pro-image-preview` dalla sua foto: `videos/_bench/minime-input/toy-jacopo-v1.png` (locale, fuori da git). E' l'input per l'image-to-3D.
**Prossimi passi (nuova sessione):**
1. Jacopo: Blender aperto + MCP connesso; crea la chiave API del servizio image-to-3D (a consumo) e la mette in `.env`.
2. Eventuale rifinitura dell'immagine (vista di fianco/retro per migliori risultati multi-view).
3. image-to-3D -> GLB -> pulizia in Blender (scala, orientamento, peso) -> `w.glb(..., fit~0.3)` al posto dell'omino Lego in `short3c/build.py` `me()` -> render 1080p60.

## 17/11 notte: OMINO SCELTO (stile PS2 low-poly, variante B3 corretta)
Scelto da Jacopo: stile PS2 low-poly, testa grossa, occhiali da sole neri tipo Wayfarer, Barbour verde oliva aperta su maglia nera, orologio argento al polso sinistro, NIENTE collanina, jeans leggermente svasati che coprono gli stivali, stivali NERI punta quadrata. Immagini (locali, in `videos/_bench/minime-input/`): `toy-jacopo-v4-front.png`, `-side.png`, `-back.png` (confronto-v4.png). Sono l'input per l'image-to-3D (multi-vista).

## 17/11 notte: DEFINITIVO + regola di regia
- Design omino DEFINITIVO (approvato da Jacopo): copie in `videos/_bench/minime-input/DEFINITIVO/jacopo-ps2-{front,side,back}.png` (locale).
- Jacopo ha visto la v3 ("praticamente perfetta"). UNICA modifica richiesta per la versione con l'omino nuovo: quando l'omino parla/e' animato, ZOOM di camera su di lui; poi stacco/spostamento IMMEDIATO della scena sull'argomento che sta dicendo. Cosi' si capisce che e' il NARRATORE e non un oggetto staccato dalla scena. In build.py: per ogni apparizione `me()` aggiungere cam raw sull'omino all'inizio della frase, poi cam sull'argomento.
- Prossima sessione: Jacopo apre Blender+MCP, chiave API image-to-3D.

## 17/11 notte: STATO PER LA NUOVA SESSIONE (leggi questo per primo)
**Obiettivo:** sostituire l'omino Lego di `short3c/build.py` (`me()`) con l'omino PS2 definitivo in 3D vero, poi render 1080p60. v3 approvata da Jacopo ("praticamente perfetta"): cambia SOLO l'omino + regola di regia (zoom su di lui quando parla, poi stacco subito sull'argomento).
**Immagini definitive (locali):** `videos/_bench/minime-input/DEFINITIVO/jacopo-ps2-{front,side,back}.png`.
**Image-to-3D, cronologia:**
- Tripo/Meshy: export GLB solo con abbonamento (12 euro): Jacopo non vuole.
- fal.ai: ricarica minima 10 euro: scartato. Chiave `FAL_KEY` messa in `.env` ma NON usata (puo' essere cancellata).
- Scelta attuale: Hunyuan3D open source su Hugging Face (Space `tencent/Hunyuan3D-2mv` = multi-vista fronte/lato/retro, oppure `Hunyuan3D-2.1` per le texture a colori). Jacopo ha finito la quota ZeroGPU gratuita, poi ha caricato credito su Hugging Face.
- Jacopo installa l'MCP Hugging Face: `claude mcp add hf-mcp-server -t http "https://huggingface.co/mcp?login"` + login con `/mcp` in sessione nuova. Con quello chiamare il Space Hunyuan3D (tool `dynamic_space`) e scaricare il GLB. Se non funziona, Jacopo usa la pagina web e mi da' il GLB in `videos/_bench/minime-input/`.
**Impostazioni 3D consigliate:** formato GLB, texture a colori, ~30.000 triangoli (stile PS2), niente luci cotte nelle texture, posa A.
**Dopo il GLB:** Blender (MCP se collegato, altrimenti headless `"C:\Program Files\Blender Foundation\Blender 5.1\blender.exe" -b -P script.py`): scala, orientamento, pulizia, controllo texture -> `w.glb(..., fit~0.3)`. Animazione parlata: dondolio/rotazione della testa e del busto sui `talk` windows (il GLB e' statico).
**Da dire a Jacopo all'inizio:** aprire Blender con addon connesso (MCP), verificare `/mcp`.

## 17/11 pomeriggio: VERSIONE 4 (omino 3D vero, bocca, regia) — render fatto
- **Omino:** Hunyuan3D-2.1 su un Space PRIVATO dell'utente (`jjjjjjeeeeeeee/hunyuan3d-2-1-jacopo`, GPU A10G large, ora in PAUSA; il ZeroGPU gratuito non basta: quota). Il Space ha richiesto patch (python 3.10, gradio 5.33, senza bpy, senza zero.startup). La fase texture della macchina si rompe (custom_rasterizer): usata SOLO la forma (multi-vista fronte/retro/lato, 417k facce), poi colorata da noi.
- **Colore:** `.claude/skills/fashion-3d/scripts/blender_color_project.py` (proietta le 3 immagini DEFINITIVO sui vertici con controllo di visibilita', conversione sRGB->lineare, lisciatura che preserva i bordi, k-means "giocattolo", regole: pelle solo su testa/mani, giacca/jeans presi dal disegno, mento pulito). Comando: `blender -b -P blender_color_project.py -- shape.glb front.png back.png side.png out.glb 70000 0.07 30 14 0.95 indigo`. Output in repo: `assets/jacopo-ps2-color.glb` (70k triangoli, colori per vertice).
- **Motore:** `engine/vendor/world3d.js` `glbObj` accetta `mouth=[x,y,z,w,h]` + `talk=[[t0,t1]...]`: bocca scura che si apre sulle parole (per l'omino: `mouth=[0,0.455,0.241,0.075,0.05]`).
- **Regia (v4/build.py, `me()`):** apparizione dopo il dive, dondolio a tempo di voce, zoom camera sull'omino ~1 s, poi stacco subito sull'argomento (camera del dive). Le camere "storia" che cadono sullo zoom vengono scartate (`_flush`).
- **Render:** `short3-sala-campioni-v4.mp4` (1080x1920, 60 fps, 65 s) in `videos/_bench/short3d/` e in iCloud `Video 3D moda\`. Voce eleven_v4 e mix identici alla v3. NON pubblicare.
- **Feedback di Jacopo durante il lavoro (da rispettare):** colori non sbiaditi, niente "pennellate" sui jeans, faccia pulita. Residui noti: qualche sfumatura scura sulle maniche, bordo color pelle sul colletto, jeans molto scuri sotto le luci calde.
- **Costi HF:** pochi dollari sui €5 caricati. Per riusare il Space: riavviarlo (`HfApi().restart_space`), poi rimetterlo in pausa. Se non serve piu', cancellarlo.
- **Token HF:** in `.env` (locale, fuori da git). Il file sul Desktop `huggin.env.txt` contiene il token in chiaro: cancellarlo.

## 17/11 sera: VERSIONE 4 FINALE (omino Tripo AI)
- **Omino:** `assets/action-figure-3d.glb` = `Action figure 3d.glb` fatto da Jacopo con **Tripo AI** (originale 877k tris + 3 texture 4K, 32 MB, in locale `videos/_bench/minime-input/action-figure-3d-orig.glb`), alleggerito con `.claude/skills/fashion-3d/scripts/blender_optimize_glb.py` (100k tris, texture 2048, ~3 MB). Guarda -Y in Blender (= +Z in glTF), nessuna rotazione necessaria.
- **Hugging Face / Hunyuan ABBANDONATO** (richiesta di Jacopo): Space privato `jjjjjjeeeeeeee/hunyuan3d-2-1-jacopo` in PAUSA (cancellarlo solo su richiesta); token in `.env`, file `huggin.env.txt` sul Desktop da cancellare. Spesi circa 2,5 $ in tutto. Gli script `blender_color_project.py`, `blender_color_transfer.py`, `blender_color_merge.py`, `blender_paint_parts.py` (colorazione a mano) restano come storico ma NON servono piu'.
- **Movimento (v4/build.py `me()` + `engine/vendor/world3d.js` `glbObj`):** segue il RITMO DEL PARLATO, non la musica: inviluppo della voce a 60 fps (`env.json`, da `vo/vo-placed.mp3`) su rimbalzo e cenno + cenno in avanti su ogni inizio parola; fermo fuori dal parlato; NIENTE bocca finta (l'opzione `mouth` esiste ancora nel motore ma non e' usata).
- **Regia:** dopo il dive la camera fa zoom ~1 s sull'omino che parla, poi stacca subito sull'argomento; le camere "storia" che cadono sullo zoom sono scartate (`_flush`).
- **Render:** `videos/_bench/short3d/short3-sala-campioni-v4.mp4` (1080x1920, 60 fps, 65 s, 123 MB) + copia in iCloud `Video 3D moda\`. Revisione a 8 fps sui fogli chiave: nessuno sfarfallio. NON pubblicato: decide Jacopo. Possibile ritocco: jeans un po' scuri sotto le luci calde.

## 17/11 sera: VERSIONE 5 (regia nuova + animazioni Tripo) — render fatto
- **Render:** `videos/_bench/short3e/short3-sala-campioni-v5.mp4` (1080x1920, 60 fps, 65 s, 142 MB) + copia in iCloud `Video 3D moda\`. Sorgenti in `v5/`. NON pubblicato.
- **Personaggio:** `assets/action-figure-anim.glb` = export Tripo "Anima" (scheletro Mixamo 54 ossa + 3 clip da 4,96 s: riposo / "spiega" / "energia", i tre prompt che avevo scritto), preparato con `.claude/skills/fashion-3d/scripts/blender_prepare_rig.py ... anim`. Niente bocca (decisione di Jacopo). Il motore (`world3d.js` `glbObj`) riproduce le clip come funzione pura del tempo: riposo quando tace, "spiega" mentre parla, "energia" sui passaggi forti della voce (inviluppo `env.json`), con sfumatura tra i pesi.
- **Regia (Jacopo, 17/11):** narratore SEMPRE presente ma DI LATO (riquadro in basso a sinistra sotto lo spazio sottotitoli) mentre la camera lavora sull'argomento; sulle 5 frasi importanti ("Io parto…", "Costa tempo…", "Io il mio lookbook…", "Ne faccio solo…", "Il resto è tempo…") primo piano per TUTTA la frase con riser (`cc-riser-corto-b`) che culmina sulla prima parola, poi si torna di lato; finale su "A quanto lo vendo alla fine…" in primo piano con la scritta INVERSO dietro. Niente piu' zoom da 1 s a meta' scena.
- **Motore:** nuovo livello narratore `w.narrator(...)` (Python `world3d.py`) + `narratorPass` (JS): seconda scena con camera e luci proprie disegnata sopra la scena principale dentro un rettangolo in px che segue `layout` (start/to = [x, y, w, h, lookY, dist, rot_y]); viene disegnata in ogni sotto-frame del motion blur.
- **Sottotitoli** spostati in alto (`top=340`) per non coprire la faccia nei primi piani; la CTA "Scrivi PANTALONE nei commenti e ti dico il prezzo finale" e' ora testo grande in alto (`w.big`), non piu' il cartello sul pavimento. 
- **Bug vecchio corretto:** il cartello INVERSO restava rovesciato (flip di 2π invece di π: il pannello e' disegnato capovolto di proposito).
- **Da vedere con Jacopo:** nel primo piano #1 la testa copre il cartellino €300–800; il cartello INVERSO resta capovolto per ~2 s prima del flip (voluto: "cade e gira"). Hugging Face resta abbandonato.

## 17/11 notte: VERSIONE 6 (narratore DENTRO la scena + movimento fluido) — render fatto
- **Render:** `videos/_bench/short3e/short3-sala-campioni-v6.mp4` (1080x1920, 60 fps, 65 s, 123 MB) + copia in iCloud `Video 3D moda\`; sorgenti in `v6/` (usa `CLIP="9,17" python build.py` per costruire solo una finestra di prova). NON pubblicato. La v5 (livello "narratore" sovrapposto in basso a sinistra) e' SCARTATA da Jacopo: "deve far parte della scena, non appeso al nulla".
- **Narratore:** 5 istanze in scena (una per tappa, `me()` in `v6/build.py`) con il GLB Tripo animato `assets/action-figure-anim-smooth2.glb`; posizione scelta in automatico (`_score`) in modo che si veda di lato nelle inquadrature della tappa; rotazione verso la camera media. Tappa 5 = punto del finale (0.9, 0, 3.55), dietro c'e' il cartello INVERSO (abbassato a height 0.78, ENDS z=3.0).
- **Primi piani:** camera DENTRO la scena su di lui (`d=1.2*h`, camera a 0.62h guarda 0.80h) per tutta la frase, riser prima; le camere "storia" dentro l'intervallo vengono scartate (`HERO_INT` in `_flush`). Sottotitoli in alto (`top=340`); CTA finale come testo grande sopra.
- **Movimento (feedback Jacopo: "scattante"):** cause trovate e corrette: (1) colpetto in avanti a inizio parola (disattivato con le clip), (2) clip riavviata a ogni pausa e mix spiega/energia a ogni sillaba (ora tempo continuo, rampe 0.55/0.7 s, media mobile della voce), (3) clip Tripo gia' scattose di per se' (filtro gaussiano circolare `blender_prepare_rig.py ... anim smooth=4.5`), riproduzione al 72% (`clipSpeed`). Jacopo sulla clip di prova (smooth=2.5, 80%): "piu' fluido, poteva esserlo un po' di piu' ma gia' va bene"; per il render finale smooth=4.5 e 72%.
- **Da vedere con Jacopo:** nessuna bocca (voluto); il narratore nelle inquadrature molto ravvicinate sui cartellini puo' uscire dal campo; nel finale il testo CTA sfiora il bordo alto del cartello.

## 17/11/2026 notte: PUBBLICATO
- **Short #3 pubblicato da Jacopo il 17/11/2026** (v6, `videos/_bench/short3e/short3-sala-campioni-v6.mp4`, copia in iCloud `Video 3D moda\`). Link non ancora registrato (Jacopo non l'ha mandato): aggiungerlo qui quando lo da'.
- Testi usati: titolo «Quanto costa lanciare un pantalone (se non hai un brand)»; descrizione con CTA «Scrivi PANTALONE nei commenti e ti dico il prezzo finale» e link al #4 (https://youtu.be/aPDByKvlb5c); hashtag (5): #inverso #modaitaliana #fashionbrand #buildinpublic #pantaloni; primo commento «Scrivi PANTALONE e ti rispondo con il prezzo finale e il perché.»
- **Da fare dopo:** rispondere ai commenti "PANTALONE" con il prezzo finale (150–200 €, pre-order, numerati; mai nominare la tela); dopo qualche giorno guardare le metriche e cosa scrivono per capire cosa non ha funzionato (lo scopo del canale = riscontri). Verifica dopo 6 Shorts (piano-canale.md). Prossimo: Short #2 (pronto da pubblicare) o Short per il #5 (~04/12).
- Decisione di Jacopo (17/11): «se stiamo a fare perfezionisti non andremo mai avanti» → pubblicare quando i difetti sono minori.

## 17/11 sera: v7 (clip Tripo da 10 s) e v8 (mascella + performance sul parlato) — PROVE, non pubblicate
- **v7:** `assets/action-figure-anim10.glb` (4 clip da 10 s, catalogo in `assets/clip-catalogo.png`: 0 ferma, 1 gesti medi, 2 gesti ampi, 3 spiega). Una sola clip per inquadratura. Bug trovato: il motore avviava il mixer solo con `env`/`beat`; ora anche con `segs`/`jaw`. Render: `videos/_bench/short3e/short3-sala-campioni-v7.mp4`.
- **v8 mascella:** `.claude/skills/fashion-3d/scripts/blender_add_jaw.py` (fessura = facce scure in una lente sulla piega della bocca, shape key `jawOpen`, riposo chiuso). Curva di apertura dalla voce: `v8/jaw_curve.py` -> `v8/jaw.json` (60 fps). Motore: opzione `jaw=[60,[..]]` + `jawGain` in `glbObj`.
- **v8 performance:** `.claude/skills/fashion-3d/scripts/blender_perf.py` impara il vocabolario di pose dalle 3 clip parlate (k-means) e costruisce UNA animazione di 65 s legata a parole chiave/picchi di voce (anticipo 0.3 s, molla smorzata, braccio sinistro in ritardo 0.1 s, cenno della testa). Output `assets/action-figure-perf.glb` (clip 'performance'), `v8/build.py` la riproduce con `segs=[[0,DUR+1,0,0,1]]`.
- **Pipeline v8:** `blender_add_jaw.py` -> `v8/jaw-raw.glb` -> `blender_perf.py` -> `v8/perf-raw.glb` -> `blender_prepare_rig.py ... anim` -> `assets/action-figure-perf.glb`.
- Prove da 8 s (finestra 9-17 s) inviate a Jacopo: `videos/_bench/short3e/prova-A-mascella.mp4`, `prova-B-performance.mp4`. Render completo v8 NON fatto: aspettare il parere di Jacopo.
- **v8, difetto "pixelato" risolto (17/11 sera):** causa = il passaggio sulla bocca perdeva le NORMALI PERSONALIZZATE del modello Tripo (sono quelle che lo fanno sembrare liscio: senza, la geometria a faccette si vede e la pelle e' a chiazze). `blender_add_jaw.py` ora le ritrasferisce dalla copia originale (DATA_TRANSFER, verificato: 0.402 rad come l'originale) e suddivide la bocca con cuts=5 (bordi netti). Prova pulita: `videos/_bench/short3e/prova-B2-pulita.mp4`. Resta da fare: render completo v8 (NAME=v8 in final1080.sh) dopo l'OK di Jacopo.
