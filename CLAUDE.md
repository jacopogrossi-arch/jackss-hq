# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A collection of browser-based games built with **vanilla JS, HTML5 Canvas, and CSS** — no build tools, no frameworks, no dependencies. Each game is a single self-contained `.html` file.

## Running the Games

Open any `.html` file directly in a browser. There is no server, build step, or install required:

```
start tictactoe.html
start snake3.html
```

Or via the shell: `cmd.exe /c start "" "<absolute-path>.html"`

## Repository & Git Workflow

- Remote: https://github.com/jacopogrossi-arch/browser-games
- Default branch: `master`
- **Commit and push after every meaningful unit of work** — a new feature, a bug fix, a visual tweak. Never leave work uncommitted at the end of a session.
- Commit messages: imperative mood, describe *what changed and why* (e.g. `Fix self-collision skip distance for 3-headed snake` not `updated snake3.html`).
- Stage specific files by name (`git add snake3.html`) rather than `git add -A` to avoid committing unintended files.
- Always run `git push` immediately after committing so the GitHub remote reflects the latest state and can be used to revert if needed.

## Architecture

Every game follows the same single-file pattern:

```
<head>   — charset, viewport, title
<style>  — all CSS inline (no external sheets)
<body>   — HTML structure (canvas, HUD divs, overlay)
<script> — all game logic (no modules, no imports)
```

### Visual language (shared across all games)

| Token | Value |
|---|---|
| Page background | `#1a1a2e` |
| Surface / arena | `#16213e` |
| Wall / border | `#0f3460` |
| Accent red | `#e94560` |
| Accent cyan | `#a8dadc` |

All new games or UI additions should use these colours to stay visually consistent.

### `snake3.html` — core concepts

- **Trail-based body**: `snake.trail` is a flat `[{x,y}]` array. Index 0 = tail, last = fork point. Growth works by increasing `targetLength` and draining `pendingGrowth` one point per frame.
- **3-head geometry**: `getHeads(snake)` returns three positions fanned out from the fork point using the perpendicular vector `(-sin(angle), cos(angle))`. This is the architectural centrepiece — all collision and rendering branches off it.
- **Game loop**: `requestAnimationFrame` only; no `setInterval`. State machine: `'start' | 'running' | 'dead'`.
- **Persistence**: high score in `localStorage` key `snake3_hi`.

### `tictactoe.html` — core concepts

- Pure DOM (no canvas). Board is a CSS Grid; cells use `data-i` attributes for indexing.
- Win detection iterates `WINS` (8 static triplets) each move.
- Session scores live in a plain object `{ x, o, d }`; no persistence.

---

## AI Content Automation Project

### Obiettivo

Sistema quasi completamente automatizzato che genera e pubblica contenuti video sulla nicchia **moda maschile + brand building**, canale anonimo (no faccia, voiceover sintetico).

### Pipeline principale

```
Schedule Trigger (ogni 48h)
    ↓
Trend Scouting (Google Trends + Reddit API)
    ↓
Claude API → 3 script (TikTok 60s / Reels / YouTube 8min)
    ↓
ElevenLabs API → voiceover
    ↓
HeyGen API → video assemblato
    ↓
Google Drive → salvataggio media
    ↓
Buffer API → pubblicazione social
    ↓
Notifica Telegram → preview per revisione
```

### Stack

| Tool | Ruolo | Costo |
|------|-------|-------|
| n8n (self-hosted) | Orchestrazione workflow | ~€10/mese VPS |
| Claude API | Generazione script | Pay per use |
| ElevenLabs | Voiceover sintetico | ~€22/mese |
| HeyGen | Video con avatar AI | ~€29/mese |
| Buffer | Scheduling social | ~€15/mese |
| Google Sheets / Airtable | Content queue | Gratis |

### Monetizzazione

- Community Skool "Come costruire un brand di moda con €1.000" — €29-49/mese
- Target: 100 iscritti = €2.900-4.900/mese

### Regole di lavoro su questo progetto

- L'utente è un **principiante assoluto** su n8n, API e automazioni — non dare mai nulla per scontato
- Spiega **sempre** ogni passaggio, anche quello che sembra ovvio: dove cliccare, cosa copiare, dove incollare
- Usa un linguaggio **semplice e diretto**, senza gergo tecnico non spiegato
- Se usi un termine tecnico, **spiegalo subito** tra parentesi o con un esempio
- Spiega ogni nodo/blocco di codice **in italiano semplice**
- Preferisci **soluzioni visuali in n8n** (senza codice) quando possibile
- Scrivi sempre un **test minimale** prima di integrare un'API nuova
- Ogni workflow n8n deve terminare con un **nodo notifica Telegram**
- Il codice nei nodi custom va **commentato in italiano**
- Priorità: **semplice e funzionante** > elegante e complesso

### Struttura file progetto

I file del progetto sono in `n8n-automation/`:
- `overview.md` — obiettivo, stack, pipeline, monetizzazione
- `progress.md` — stato avanzamento dettagliato, note tecniche, prossimi passi
- `workflows/workflow-01.md` — workflow attuale step by step
- `prompts/system-prompt.md` — system prompt Claude per generare gli script

### Stato (vedi `n8n-automation/progress.md` per il dettaglio aggiornato)

Workflow funzionante con Schedule Trigger ogni 48h, argomento casuale da Google Sheet, generazione script con Claude, e voiceover ElevenLabs. Prossimo step: salvare l'audio su Google Drive.

---

## AI Image & Video Generation Project

> **ATTENZIONE — Questo progetto è completamente separato dal progetto n8n sopra.**
> NON usa n8n, NON ha pipeline automatizzata, NON pubblica sui social in automatico.
> Riguarda la generazione manuale di immagini e video AI come skill creativa e potenziale servizio.

### Obiettivo

Imparare a generare immagini e video AI di qualità professionale usando strumenti come Gemini, Kling, Midjourney, Krea. Obiettivo finale: offrire questo come servizio a clienti nel settore moda/lusso.

### Stack strumenti

| Tool | Tipo | Uso |
|------|------|-----|
| Gemini / NanoBanana | Generatore immagini (free) | Concetti veloci, moodboard, test prompt |
| Midjourney | Generatore immagini (pro) | Immagini ad alta qualità |
| Krea | Generatore immagini (pro) | Ritratti realistici, stile fashion |
| HiggsField | Generatore immagini (pro) | Ultra-realistico, campagne editoriali |
| Kling | Generatore video | Text-to-Video e Image-to-Video |
| HeyGen | Avatar AI | Presentatori video |
| ElevenLabs | Voiceover AI | Narrazione sintetica |

### Brand di riferimento (progetto di studio)

Visual identity **luxury Italian fashion / old money**:
- Soggetto: giovane uomo italiano elegante, ~25 anni, stile classico
- Scenario: Ferrari convertibile anni '80, campagna Toscana, strade con pini
- Mood: dolce vita, Riviera Italiana anni '80, lusso senza ostentazione
- Palette: amber `#F5E6C8`, gold `#C9A46A`, deep red `#8B0000`, near-black `#1E1E1E`
- Riferimenti: campagne Marlboro anni '70, Helmut Newton, *Blade Runner 2049*

### Struttura file progetto

I file del progetto sono in `ai-content-claude/`:
- `style-guide.md` — identità visiva, palette, sistema prompt
- `platform-cheatsheet.md` — quale tool usare per cosa
- `prompts/hw1-image-prompts.md` — prompt immagini Homework 1
- `prompts/hw2-video-prompts.md` — prompt video Homework 2 (Kling)
- `progress.md` — log avanzamento e prossimi step

### Stato avanzamento (maggio 2026)

- [x] Homework 1: 3 varianti prompt immagine + JSON prompt (Gemini)
- [x] Homework 2: TTV e I2V con Kling (brand Ferrari/Toscana)
- [ ] Homework 3 e successivi (in corso)

### Regole di lavoro su questo progetto

- Parla di **prompt visivi**, non di workflow o nodi n8n
- Il lavoro è **manuale e creativo**, non automatizzato
- Usa terminologia da **fotografia e regia**: lens, lighting, composition, shot type
- Quando suggerisci miglioramenti ai prompt, usa la struttura: SHOT + LENS + LIGHT + TEXTURE + COMPOSITION + STYLE
- NON mescolare mai questo progetto con il progetto n8n/automazioni
