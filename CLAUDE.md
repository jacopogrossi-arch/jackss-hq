# CLAUDE.md

This file gives Claude Code the context to work well in this repository.
*Ultimo aggiornamento: 25/10/2026.*

---

## Chi è Jacopo

Giovane italiano (Roma) con un progetto imprenditoriale in sviluppo nel settore AI + moda. Studia Economia all'università e moda in accademia.
Non è uno sviluppatore: le spiegazioni devono essere pratiche (dove cliccare, cosa copiare, dove incollare).

**Principio guida: semplice e funzionante batte elegante e complesso.**

Per il contesto sulla vita personale (studi, sport, persone importanti), leggere la memoria `user_personal_life.md`.

**Obiettivo di fondo:** portare Inverso al Drop 1 (primo capo, pre-order) — chiudere il ciclo idea→capo→campagna→vendita.

---

## Mappa della repo

| Cartella | Cosa c'è |
|---|---|
| `inverso/` | Il brand: piano, strategia, analisi marketing, ricerca sul pantalone Drop 1 |
| `accademia/` | Progetti e consegne dell'accademia di moda |
| `personale/` | Canale YouTube personale, letture, Mandal-Art, regali e reel personali |
| `.claude/skills/youtube-edit/` | La skill che monta i video (script, formati, preset, look colore) |
| `video-editor/` | Pacchetto originale della skill (README, SETUP, PROMPTS, STYLE-GUIDE) — documentazione, la skill vera è in `.claude/skills/` |
| `videos/` | Cartelle di lavoro dei montaggi (footage, render) — **solo locale, fuori da git** |
| `cartamodelli/` | Tool SVG per cartamodelli jeans via Claude API |
| `assets/notion-covers/` | Cover della dashboard Notion (linkate via GitHub raw: il repo deve restare pubblico) |
| `.agents/` | `marketing-context.md` letto da tutte le skill marketing |
| `archivio/` | Progetti chiusi o dormienti (vedi sotto) |

**Il repo è pubblico.** Materiale riservato, file enormi e asset con licenza personale stanno in `.gitignore` (footage, suoni Artlist/Epidemic, LUT e pack di terzi, slide dei docenti). Se si crea una cartella nuova di questo tipo, aggiungerla al `.gitignore` **prima** di scriverci dentro.

---

## Progetto principale — INVERSO (dal 13/07/2026)

**Inverso** — brand menswear italiano reale, costruito in build-in-public col volto di Jacopo.
**Prima di tutto è un progetto personale di vita e ricerca**: sviluppo del gusto creativo, ricerca su tessuti e materiali, passione per la moda. I soldi finanziano la ricerca, non sono il fine.

File: `inverso/`
- `piano-inverso.md` — piano maestro (tabella di marcia con le caselle da spuntare)
- `briefing-2026-07-12-inverso-strategia.md` — briefing strategico fondativo
- `concept-*.md`, `spiegazione-del-nome.md`, `bio-profili.md` — identità e racconto del brand
- `analisi/` — analisi delle skill marketing (copywriting, psychology, social, product-marketing, idee, persona)
- `ricerca/` — studio del pantalone Drop 1, numerato 01→15 (silhouette, scheda tecnica, cartamodello, tela di prova, materiali)
- `assets-jago/` — asset dell'avatar Jago (logo, palette, moodboard, caroselli)

**Stato:** la prima tela di prova del pantalone è stata cucita e provata il 05/08/2026 (rilievi in `ricerca/14-prima-prova-tela-rilievi.md`): fit da correggere. Da settembre il lavoro su Inverso è fermo mentre si sono chiusi accademia e i video YouTube. Ripartire da `piano-inverso.md` §9.

**Struttura:** Jacopo = volto del processo (profilo IG personale) · @inversorome = risultato/drop · Jago = modello virtuale dei lookbook · @jagoworks = congelato, vetrina servizio.
**Marketing:** skill `/inverso-marketing` (strategia) + copywriting/psychology/social/product-marketing/marketing-ideas e le altre marketing in `.claude/skills/`. Contesto letto da tutte: `.agents/marketing-context.md`.
**Servizi (Lookbook AI, Idea→Campione):** solo dopo il Drop 1.

---

## YouTube personale + montaggio video

- **Canale personale** (video lunghi, non Inverso) → `personale/youtube/` — README con video pubblicati e metodo copione→montaggio→miniatura→pubblicazione.
  - #1 "Si può usare l'AI nella moda?" — pubblicato 15/10/2026
  - #2 "Ho lasciato Claude ideare una collezione al posto mio" — pubblicato 21/10/2026, montato con la skill `youtube-edit`
  - #3 — idea da decidere
- **Skill `youtube-edit`** → `.claude/skills/youtube-edit/` (`SKILL.md` = regole, `scripts/`, `formats/`, `presets/`, `references/`). Monta da clip grezza a MP4 4K. Ogni nota di gusto di Jacopo va salvata nella skill. Grading: look scelto `jacopo-cinema-wow`.
- **Agente `video-builder`** (`.claude/agents/`) — esegue le sezioni del piano scritto dal pianificatore, non decide il design.
- I video in lavorazione vivono in `videos/<nn-nome>/` (locale, non su GitHub).

---

## Accademia di Moda

`accademia/` — indice in `accademia-moda.md` (specchio del hub Notion "Fashion Design").

- **Digital Fashion Design — "After Hours"** (Gucci × Tom Ford) — consegnato 09/10/2026
- **Trend A/I 2027-28** (onlife, body toll, conviviality) — `progetto-trend-ai-2027-28.md`, progetto Canva unico
- **Fashion Design — "Cinque giacche per cinque outfit"** (Roue Libre) — `progetto-fashion-design-cinque-giacche.md`, portfolio in `Roue_Libre_portfolio_FINALE.pdf`
- File per progetto: `concept-*`, `cartella-*`, `moodboard-*`, `outfit-*`, immagini in `img-*/`

Strumento collegato: **Cartamodelli** → `cartamodelli/` (avvio: `.claude/launch.json`, configurazione `cartamodelli-tool`).

---

## Vita personale

Materiale personale non legato a un progetto sta in `personale/`:

- **YouTube personale** → `personale/youtube/` (vedi sopra)
- **Letture** (lista con tracking, personali + Inverso) → `personale/letture.md`
- **Mandal-Art set→dic 2026** (griglia 9×9 stile Ohtani del 30/08/2026: centro "venduto a uno sconosciuto" + 8 aree — capo, metterci la faccia, università, tempo, corpo, persone, Chiara, crescita; nove caselle vuote apposta) → `personale/mandal-art-set-dic-2026.md`, versione da stampare in `personale/stampa/`
- **Pannello studio** (stato rapido YouTube/accademia/università) → `personale/pannello-studio.json`
- **Reel Corsica** (serie per amici e famiglia) → `personale/reel-corsica/`
- **Quadretto compleanno papà** → `personale/compleanno-papa/`

---

## Archivio

Tutto ciò che è dormiente o chiuso sta in `archivio/` (dettaglio in `archivio/README.md`):

- **Canale Jago** (7 video, outreach, strategia — chiuso il 13/07/2026, Jago vive come strumento di Inverso) → `archivio/canale-jago/`. La skill `/jago-creative-director` resta per eventuali video lookbook di Inverso.
- **Dispensa Politica Economica** (esame 8/09/2026, metodo in memoria `metodo-dispense-esami`) → `archivio/dispensa-politica-economica/`
- **AI Content Automation** (pipeline n8n, dormiente) → `archivio/n8n-automation/`
- **AI Image & Video** (corso completato) → `archivio/ai-content-claude/`
- **Log Jackss** (routine dismesse) → `archivio/logs-jackss/`

Fuori repo: media del canale Jago in `Desktop\archivio-jago-assets\`; dispense di Diritto Pubblico e Ragioneria in `Desktop\archivio-studio\`.

---

## Strumenti

- **Immagini/video AI:** solo Magnific (Nano Banana Pro, GPT-2, Seedance, Kling 3.0) — Higgsfield dismesso dal 03/07/2026. I prompt si scrivono con le skill `banana-pro-director` (immagini) e `cinema-worldbuilder-pro` (video).
- **Notion — Jackss HQ:** workspace personale con hub su AI/video, salute/sport e studio. Per stato progetti non in repo, usare il MCP Notion.

---

## Git workflow

- Remote: github.com/jacopogrossi-arch/jackss-hq — branch `master`
- Commit e push dopo ogni unità di lavoro significativa.
- **Doppio salvataggio:** oltre al push su GitHub, aggiornare anche Notion (Jackss HQ, via MCP) con lo stato di avanzamento a fine di ogni unità di lavoro.
- Stage per filename, non `git add -A`.
- Commit messages: imperativo, cosa è cambiato e perché.
