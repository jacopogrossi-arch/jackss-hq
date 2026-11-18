# social/ — YouTube, Shorts e montaggio

**Scopo:** canale YouTube personale (non Inverso), Shorts 3D e reel. Metodo: copione → montaggio → miniatura → pubblicazione.

**File chiave**
- `README.md` — video pubblicati e metodo · `piano-canale.md` — piano #5→#12 e registro Shorts
- `direzione-canale.md`, `checklist-riprese.md`
- `video-01/` … `video-05/` — materiali di ogni video lungo
- `short-primo-pantalone/`, `short-02-identita/`, `short-03-tabellone/` — Shorts 3D (HANDOFF.md dentro lo Short #3)
- `assets-3d/` — oggetti 3D in stile giocattolo (Gemini → Tripo): prompt pronti in `PROMPT-COMPLETI.md`, flusso in `PRONTO-GEMINI-TRIPO.md`
- `ispirazione/` — teardown di video di riferimento · `miniatura/`, `motion/`, `video-3d-moda/`, `fashion-3d-prove/`

**Convenzioni**
- Montaggio con la skill `.claude/skills/youtube-edit/`; video 3D con `.claude/skills/fashion-3d/` (SOP degli Shorts in `references/short-3d-sop.md`).
- Le regole di gusto video stanno nelle skill (`references/taste.md`, `sound.md`), non qui.
- Instagram: max 5 hashtag per post.

**Non fare**
- Footage e render vivono in `videos/` (locale, fuori da git): mai qui dentro.
- Mai nominare la tela di prova del 05/08 nei video.
- TODO: da compilare (link degli Shorts #3 e #11 pubblicati).
