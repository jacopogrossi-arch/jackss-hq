# HANDOFF — Short «Ho chiesto a 6 sconosciuti quanto pagherebbero un pantalone fatto bene» (idea 1)
*18/11/2026. Copione e titolo APPROVATI da Jacopo, morale approvata («non erano il mio cliente, ma mi hanno detto cosa non dimenticare»), scena nuova approvata (via di Roma di notte). Non pubblicare: lo fa lui.*

## Stato
- Scena fatta (`v1/room.py` = via di notte, `v1/build.py` = regia: 6 cartelli sui due lampioni, contatore «conferme N · schiaffi N», pantalone giocattolo in vetrina, narratore in strada, insegna INVERSO che si raddrizza in chiusura). Sviluppata con tempi STIMATI (`v1/words.json` + marcatore `v1/words.ESTIMATED`): vanno sostituiti con quelli della voce vera.
- Mix pronto (`v1/mix.py`, musica Epidemic "Heart Street" - Jobii), `v1/run.sh nome` fa build → mix → render bozza → mux → fogli a 10 fps.
- **BLOCCO (18/11 pomeriggio): la voce non e' ancora stata generata.** Il servizio `creative_generate_speech` (ElevenLabs via connettore) va in timeout; creato il flusso `jlHWFTCp2acyr9MGX6ZC` con il nodo `qy5sUSsAAl2yIv75uGvB` (testo completo, voce "Jacopo Prova" id 0CeJTHP08UsLHht7KIni, eleven_v4), stato «not_run». NON rigenerare con un'altra chiamata senza prima controllare con `creative_get_flow` che il nodo non sia gia' stato eseguito (si paga a ogni generazione, ~640 crediti). Se il nodo e' completato: scaricare l'audio (`creative_get_generations` → `full_res_url`) in `videos/_bench/short-sconosciuti/vo/vo.mp3`.

## Dopo la voce (stesso procedimento dello Short #11, vedi `social/short-11-pantalone-3d/HANDOFF.md`)
1. Trascrizione: `npx hyperframes@0.9.35 transcribe vo.mp3 -l it -d .` → `transcript.json` → words.json (campi w, s, e); correggere a mano le parole sbagliate; cancellare `v1/words.ESTIMATED`.
2. Mascella: `python social/short-03-tabellone/v8/jaw_curve.py vo.mp3 words.json v1/jaw.json`.
3. Animazione narratore sul nuovo parlato: `blender -b -P .claude/skills/fashion-3d/scripts/blender_perf.py -- social/short-03-tabellone/v8/jaw-raw.glb assets/perf-raw.glb words.json jaw.json DURATA "chiavi" ` poi `blender_prepare_rig.py ... anim`, poi `social/short-11-pantalone-3d/v1/smooth_anim.py` → `videos/_bench/short-sconosciuti/assets/narratore-perf-smooth.glb` (finora c'e' quello dello Short #11, solo per sviluppo).
4. `bash v1/run.sh draft` → rivedere TUTTI i fogli a 10 fps (SOP: `.claude/skills/fashion-3d/references/short-3d-sop.md`), correggere, mostrare la bozza a Jacopo, solo dopo il suo OK il 4K (`render --resolution portrait-4k --gpu --video-bitrate 60M --fps 60`) e iCloud › Video 3D moda.
5. Titolo e descrizione (max 5 hashtag, video correlato #4): scriverli in `pubblicazione.md`; poi Notion (Jackss HQ) e memoria `project_shorts_3d.md`.

- 18/11 sera: ElevenLabs e' giu' per tutti (sito compreso): Jacopo non riesce a generare la voce neanche a mano. Render muto con tempi stimati fatto e rivisto (20 fogli): layout OK, corretti testo dei cartelli e distanza delle spinte. Quando la voce c'e', seguire «Dopo la voce». I tempi di camera si adattano da soli (tutto e' agganciato alle parole).
