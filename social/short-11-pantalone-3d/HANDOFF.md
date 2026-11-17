# HANDOFF — Short #11 «Ho dato un disegno a un'AI e mi ha restituito un pantalone 3D»
*Jacopo dorme dal 17/11/2026 ~23:50. Lavoro autonomo notturno. Aggiorna la sezione STATO a ogni passo.*

## Compito
Costruire lo Short #11 (verticale 9:16, ~38 s). Copione APPROVATO: `script.md` (qui accanto). Decisioni di Jacopo: nel testo dire «un'AI», mai «Claude»; data «inizio dicembre»; nel blocco 3 usare le 4 viste GIOCATTOLO coerenti con il GLB: `social/assets-3d/gemini/01-pantalone-d-fronte.png`, `-retro.png`, `-left.png`, `-right.png` (foglio `_pantalone-d-4viste.jpg`), approvate da lui.

## Regole
- Leggi `social/CLAUDE.md` e la SOP `.claude/skills/fashion-3d/references/short-3d-sop.md`. Lavora solo in `social/` e `videos/` (locale, fuori da git).
- Voce ElevenLabs "Jacopo Prova" (id 0CeJTHP08UsLHht7KIni), modello eleven_v4, imperativo a UNA persona. Niente bocca finta sul narratore, `recv=False` sul narratore. Mai nominare la tela. Frase-firma: studente, niente da vendere, documento.
- Scena: sala campioni + narratore (`social/short-03-tabellone/assets/action-figure-perf.glb`); pantalone `videos/_bench/assets3d/finali/pantalone.glb`; esempio di scena `social/assets-3d/scena-oggetti.py`; sorgenti di riferimento `social/short-03-tabellone/v6/` e `v8/`.
- Revisione a 10 fps su TUTTI i fogli PRIMA di ogni 4K; prova breve (`CLIP=`) prima del render lungo; max ~2 giri, poi si propone la pubblicazione.
- **NON fare il 4K finale: prima Jacopo deve vedere la bozza e dare l'OK** (regola dello Short #2). Fermati alla bozza 1080p + contact sheet.
- Git: commit per nome file, mai `git add -A`, messaggi all'imperativo, `git push origin master`. Il repo è pubblico: niente file grandi/riservati.
- Fine lavoro: aggiornare Notion (Jackss HQ) e memoria `project_shorts_3d.md`.

## Passi (spunta quando fatti)
1. [x] Cartella progetto locale `videos/_bench/short11/`, voce per paragrafi + words.json
2. [x] `social/short-11-pantalone-3d/v1/`: build.py + room.py + mix (musica da Epidemic Sound, diversa da quelle già usate)
3. [x] Bozza 1080p a 10 fps + contact sheet, revisione di tutti i fogli, correzioni
4. [x] Bozza finale 1080p con audio → copia in `videos/_bench/short11/` e preparare titolo/descrizione (video correlato = #4)
5. [x] Commit/push, aggiorna HANDOFF, messaggio per Jacopo con cosa vedere e cosa decidere

## STATO
- 17/11 23:50 — Copione approvato, 4 viste giocattolo generate e approvate. Nessun altro passo iniziato.
- 18/11 00:05 — Voce fatta (1 take eleven_v4, 573 crediti, 34,5 s): `videos/_bench/short11/vo/vo.mp3` (locale); words.json e jaw.json in `v1/`. Animazione narratore (perf sul nuovo parlato): `videos/_bench/short11/assets/narratore-perf.glb` (locale; si rigenera con blender_perf.py su `short-03-tabellone/v8/jaw-raw.glb`). Scena `v1/build.py` + `room.py` + `mix.py` (musica Epidemic "Skyline" - Jobii, 19 suoni) fatti e controllati con snapshot (4 viste in griglia 2x2, narratore davanti al piedistallo). Mix: `videos/_bench/short11/renders/mix.wav`. Bozza 1080p 30 fps in render: `videos/_bench/short11/renders/draft-raw.mp4`.
- Come si costruisce: `cd social/short-11-pantalone-3d/v1 && python -I build.py` (poi copiare `comp/` in `videos/_bench/short11/comp`), `python mix.py`, render con `npx hyperframes@0.9.35 render comp --quality draft --fps 30 --workers 3 -o renders/draft-raw.mp4` (TMP=D:\hf-tmp). Snapshot: `npx hyperframes snapshot comp --at 1,2,3 -o /d/hf-tmp/x`.
- Da fare ora: attendere il render, mux con mix.wav (ffmpeg), revisione a 10 fps (fogli da 24 fotogrammi), correzioni, bozza finale, titolo/descrizione, commit.
- 18/11 00:15 — BOZZA v1 FATTA (passi 1-4 completati). Revisione a 10 fps di tutti i 13 fogli, corrette: scrivania (la scheda ora si vede), 4 viste in griglia 2x2 che appaiono su «quattro viste», pantalone che finisce di fronte, narratore che entra solo nel primo piano, logo INVERSO che si raddrizza nell'ultima scheda. File locali: `videos/_bench/short11/short11-pantalone-3d-bozza-v1.mp4` (1080p 60 fps, 52 MB, -16 LUFS) e `bozza-leggera.mp4` (720p, 6 MB, mandata a Jacopo in chat). La copia in iCloud NON e' stata fatta (il permesso e' stato negato dal sistema): da fare solo se Jacopo la vuole. Per rifare tutto: `bash social/short-11-pantalone-3d/v1/run.sh nome`.
- Resta: ascolto/ok di Jacopo, eventuali correzioni (max 1-2 giri), poi 4K (`render --resolution portrait-4k --gpu --video-bitrate 60M --fps 60`) e iCloud, titolo+descrizione (max 5 hashtag, video correlato #4), aggiornare Notion e memoria. Non pubblicare.
- Note di qualita': la striscia scura in fondo all'ultima inquadratura (camera fuori dal pavimento) e la mancanza del narratore nel blocco delle 4 viste sono difetti minori noti.
- 18/11 00:25 — Passi 1-5 FATTI. Titolo e descrizione in `pubblicazione.md`, memoria `project_shorts_3d.md` aggiornata, tutto su git (commit 54fe554). UNICA cosa automatizzabile rimasta: aggiornare Notion (Jackss HQ, `35c30837-a9e6-81ca-8fc5-ccfcb3f440ce`) con una riga sullo Short #11 (bozza pronta, in attesa dell'ok) e, se c'e', la pagina del registro Shorts. Se l'hai gia' fatto o i tool Notion non sono disponibili, scrivilo qui e fermati. NON rifare render o voce, NON pubblicare.
- 18/11 00:35 — Notion (Jackss HQ) aggiornato con la riga dello Short #11. NIENTE altro da fare: gli agenti di ripresa (1:50 e 7:00) devono solo scrivere una riga di verifica qui e fermarsi.
