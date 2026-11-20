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

- 18/11 sera tardi: ElevenLabs tornato. Voce = take B del flusso (gen usphcKY0P8qLbUSstyCd, 53,7 s): `videos/_bench/short-sconosciuti/vo/vo.mp3` (takeA.mp3 di riserva). words.json (corretto a mano) e jaw.json veri; narratore `assets/narratore-perf-smooth.glb` rifatto sul nuovo parlato. BOZZA v1 fatta (`renders/draft.mp4`, 55,9 s, 19 fogli rivisti), `renders/bozza-leggera.mp4` mandata a Jacopo. Aspetto il suo OK/correzioni; poi 4K + iCloud + pubblicazione.md. NON pubblicare.

- 19/11: BOZZA v2 (correzioni Jacopo): fascia INVERSO + targhetta DROP 1 sulla vetrina, camera piu vicina, lampioni che lampeggiano verde/rosso (opzione motore pendant flash=), cartelli nuovi (card badge/border). Mandata a Jacopo (renders/bozza-leggera-v2.mp4). Attendo OK per 4K.

- 19/11: BOZZA v4: pantalone vetrina piu grande + luce bianca dal basso (prop uplight) e lampada vetrina bianca; lampioni FISSI verde/rosso (niente lampeggio); facciata piu romana (travertino, cornici, persiane a lamelle, balconcini, cornicione, targa Via dellAgo, Vespa). File: renders/bozza-leggera-v4.mp4. Attendo OK per 4K.

- 19/11: BOZZA v5: partenza da lontano + zoom velocissimo sulla vetrina; card1 «Vestibilita corretta / spenderebbe 200 € se andasse bene», card2 «Compro solo quando costa poco / 65 vs 200» (testi di Jacopo). renders/bozza-leggera-v5.mp4. Attendo OK 4K.

- 19/11 mattina: 4K FATTO (2160x3840, 60 fps, 55,9 s, 405 MB) dopo il via di Jacopo; copiato in iCloud › Video 3D moda › short-sconosciuti-v1.mp4. pubblicazione.md scritta. Resta SOLO la pubblicazione (la fa Jacopo).

- 19/11 sera: PUBBLICATO da Jacopo. Primo commento: «200 euro per un jeans e troppo, lo pagherei 70». Short chiuso; prossimo = nuova sessione (idea 16 «Non ho niente da venderti», poi 14, 19; vedi memoria project_shorts_3d e social/piano-canale.md).
