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
