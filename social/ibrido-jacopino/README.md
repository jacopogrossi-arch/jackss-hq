# Prova ibrida Jacopino (23/11/2026)

Obiettivo: unire il controllo di Blender (posizioni, camera, oggetti) con la recitazione di un modello image-to-video.

Pipeline:
1. **Character sheet** con Gemini 3 Pro Image (`gen_target.py`, prompt con la skill banana-pro-director): `sheet-identita.jpg` e `sheet-espressioni.jpg`. Riferimenti: disegno DEFINITIVO fronte/lato/retro e un render della v8.
2. **Layout in Blender** (`layout.py`): GLB vero di Jacopino alto 22 cm, tavolo, tappetino, foglio A4, matita e metro come fermaposto in scala reale; camera frontale in asse e due inquadrature (iniziale e finale con avvicinamento). Render grezzi in `videos/_bench/ibrido/layout/` (locale).
3. **Rifinitura dei fotogrammi chiave** con Gemini: il layout è il riferimento dominante per la messa in scena, le tavole servono per l'identità. Prima si blocca `start.jpg`, poi si genera `end.jpg` usando start come riferimento del set (senza questo passaggio il set cambia: metro spostato, oggetti nuovi). Gli occhiali vanno ribaditi nel prompt, altrimenti spariscono.
4. **Video** su ElevenLabs Flows con Seedance 2.5: fotogramma iniziale e finale, le due tavole come riferimento, prompt in `prompt-video.txt` (skill cinema-worldbuilder-pro).
5. **Voce**: la battuta vera («Io parto da carta, matita e metro, meno di 30»), sincronia labiale come passaggio separato.

Le immagini qui sono leggere (JPG) perché servono come link pubblici per ElevenLabs. I file pesanti restano in `videos/_bench/ibrido/`.

## Esito prova 1 (23/11/2026)
- Clip Seedance 2.5 720p (14.003 crediti) + lipsync Sync 3 con la voce vera (4.075 crediti). File in `videos/_bench/ibrido/video/`: `seedance-720-v1.mp4`, `lipsync-v1.mp4`, `confronto-v8-vs-ibrido.mp4`.
- Funziona: identità stabile, occhiali sempre, set fermo come nel layout, bocca vera ed espressioni.
- Da migliorare: troppi gesti per 5 s (ha saltato matita e metro), avvicinamento della camera quasi assente.
- Lezioni complete nella skill: `.claude/skills/fashion-3d/references/hybrid-blender-ai-sop.md`.
