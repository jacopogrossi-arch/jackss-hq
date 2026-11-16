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
