# CLAUDE.md
*Aggiornato il 17/11/2026. La versione lunga precedente è in `archivio/CLAUDE-radice-2026-11-17.md`.*

## Chi sono
Jacopo, italiano (Roma). Studio Economia all'università e moda in accademia. Non sono uno sviluppatore: spiegami le cose in pratica (dove cliccare, cosa copiare, dove incollare). Progetto principale: **Inverso**, brand menswear italiano, obiettivo Drop 1 (primo capo, pre-order).

## Come rispondere
- Diretto, senza giri di parole. Sfidami se ragiono male.
- Semplice e funzionante batte elegante e complesso.
- Italiano sempre. Per lavori lunghi dammi subito una stima dei tempi.

## Mappa delle cartelle
- `inverso/` — il brand: piano, strategia, identità, ricerca sul pantalone Drop 1
- `social/` — canale YouTube, Shorts 3D, reel e montaggio (skill `youtube-edit`, `fashion-3d`)
- `accademia/` — progetti e consegne dell'accademia di moda
- `personale/` — privato (vita, studio, famiglia, viaggi)
- `archivio/` — progetti chiusi o dormienti (consultabili, non in sviluppo)
- `.claude/` skill e agenti · `.agents/` contesto marketing · `cartamodelli/` tool SVG · `assets/` cover Notion
- Solo locale, fuori da git: `videos/` (footage e render), `studio-privato/`
- Fuori da questo repo: `D:\claude-3d-shop`, side hustle con un amico (dal 25/11/2026): una pagina sui video 3D fatti con Claude e una skill nostra in vendita a 5–10 €. È un repo separato apposta: non leggerlo e non portarne il contesto qui, né viceversa.

## Regola d'oro
**Lavora solo nella cartella dell'area richiesta** e leggi il suo `CLAUDE.md`. Non toccare le altre aree se non te lo chiedo.

## Repo e git
- Il repo è **pubblico** (`github.com/jacopogrossi-arch/jackss-hq`, branch `master`). Materiale riservato o enorme va in `.gitignore` PRIMA di creare la cartella.
- Commit e push dopo ogni unità di lavoro; stage per nome file, mai `git add -A`; messaggi all'imperativo.
- Doppio salvataggio: a fine lavoro aggiorna anche Notion (Jackss HQ) via MCP.

## Strumenti
- Immagini/video AI: Magnific non c'è più, non proporlo. Higgsfield (dal 25/11/2026) si può usare quando serve davvero: anche una sola clip in tutto il video, per una scena che non si gira e non si fa in 3D. Prima verifica che sia collegato e dimmi i crediti.
- 3D: Tripo AI (genero io il GLB, tu lo alleggerisci con gli script in `.claude/skills/fashion-3d/scripts/`).
- Suoni e musica: Epidemic Sound via MCP, file solo in locale.
