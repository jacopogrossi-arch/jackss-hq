# HANDOFF — Short #11 «Ho dato un disegno a un'AI e mi ha restituito un pantalone 3D»
*Jacopo dorme dal 17/11/2026 ~23:50. Lavoro autonomo notturno. Aggiorna la sezione STATO a ogni passo.*

## Compito
Costruire lo Short #11 (verticale 9:16, ~38 s). Copione APPROVATO: `script.md` (qui accanto). Decisioni di Jacopo: nel testo dire «un'AI», mai «Claude»; data «inizio dicembre»; nel blocco 3 usare le 4 viste GIOCATTOLO coerenti con il GLB: `social/assets-3d/gemini/01-pantalone-d-fronte.png`, `-retro.png`, `-left.png`, `-right.png` (foglio `_pantalone-d-4viste.jpg`), approvate da lui.

## Regole
- Leggi `social/CLAUDE.md` e la SOP `.claude/skills/fashion-3d/references/short-3d-sop.md`. Lavora solo in `social/` e `videos/` (locale, fuori da git).
- Voce ElevenLabs "Jacopo Prova" (id 0CeJTHP08UsLHht7KIni), modello eleven_v4, imperativo a UNA persona. Niente bocca finta sul narratore, `recv=False` sul narratore. Mai nominare la tela. Frase-firma: studente, niente da vendere, documento.
- Scena: sala campioni + narratore (`social/short-03-tabellone/assets/action-figure-perf.glb`); pantalone `videos/_bench/assets3d/finali/pantalone.glb`; esempio di scena `social/assets-3d/scena-oggetti.py`; sorgenti di riferimento `social/short-03-tabellone/v6/` e `v8/`.
- Revisione a 10 fps su TUTTI i fogli PRIMA di ogni 4K; prova breve (`CLIP=`) prima del render lungo; max ~2 giri, poi si propone la pubblicazione.
- **NON fare il 4K finale e NON copiare in iCloud: prima Jacopo deve vedere la bozza e dare l'OK** (regola dello Short #2). Fermati alla bozza 1080p + contact sheet.
- Git: commit per nome file, mai `git add -A`, messaggi all'imperativo, `git push origin master`. Il repo è pubblico: niente file grandi/riservati.
- Fine lavoro: aggiornare Notion (Jackss HQ) e memoria `project_shorts_3d.md`.

## Passi (spunta quando fatti)
1. [ ] Cartella progetto locale `videos/_bench/short11/`, voce per paragrafi + words.json
2. [ ] `social/short-11-pantalone-3d/v1/`: build.py + room.py + mix (musica da Epidemic Sound, diversa da quelle già usate)
3. [ ] Bozza 1080p a 10 fps + contact sheet, revisione di tutti i fogli, correzioni
4. [ ] Bozza finale 1080p con audio → copia in `videos/_bench/short11/` e preparare titolo/descrizione (video correlato = #4)
5. [ ] Commit/push, aggiorna HANDOFF, messaggio per Jacopo con cosa vedere e cosa decidere

## STATO
- 17/11 23:50 — Copione approvato, 4 viste giocattolo generate e approvate. Nessun altro passo iniziato.
