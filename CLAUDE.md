# CLAUDE.md

This file gives Claude Code the context to work well in this repository.

---

## Chi è Jacopo

Giovane italiano (Roma) con un progetto imprenditoriale in sviluppo nel settore AI + moda.
Non è uno sviluppatore: le spiegazioni devono essere pratiche (dove cliccare, cosa copiare, dove incollare).

**Principio guida: semplice e funzionante batte elegante e complesso.**

Per il contesto sulla vita personale (studi, sport, persone importanti), leggere la memoria `user_personal_life.md`.

**Obiettivo immediato:** primo cliente pagante per servizi AI (SVG, campagne, consulenza) — non i follower.

---

## Progetto principale

**Personal Brand AI + Moda** — canale YouTube/Instagram con avatar AI Jago.
Posizionamento: "costruisco pubblicamente un brand di moda usando AI."

File: `personal-brand/`
- Strategia e operatività nella root: `strategy.md`, `content-calendar.md`, `analytics.md`, `outreach.md`, `lead-magnet-lookbook.md`
- **Nuovo video**: quando Jacopo dice "Iniziamo il processo di creazione di un nuovo video" usare la skill `/jago-creative-director` (propone direzioni creative, poi Campaign Blueprint in `video-N/video-N-brief.md`)
- Un video = una cartella: `video-1/`, `video-2/`, `video-3/` (script, prompt, moodboard, immagini)
- `assets/` contiene solo gli asset condivisi del brand (logo, palette, moodboard Jago)

---

## Progetti attivi

- **Cartamodelli** (tool SVG jeans via Claude API, attivo) → `cartamodelli/`

## Archivio

Tutto ciò che è dormiente o fuori tema sta in `archivio/`:

- **AI Content Automation** (pipeline n8n, dormiente) → `archivio/n8n-automation/`
- **AI Image & Video** (corso completato, tecniche ora nel personal brand) → `archivio/ai-content-claude/`
- **Dispensa diritto pubblico** (appunti universitari, esame superato) → `archivio/dispensa-diritto-pubblico/`
- **Dispensa ragioneria** (esame 16/07/2026) → `archivio/dispensa-ragioneria/`
- **Log Jackss** (briefing/check-in delle routine dismesse) → `archivio/logs-jackss/`

---

## Notion — Jackss HQ

Workspace personale con hub su AI/video, salute/sport e studio.
Per documentazione personale o stato progetti non in repo, usare il MCP Notion.

---

## Git workflow

- Remote: github.com/jacopogrossi-arch/jackss-hq — branch `master`
- Commit e push dopo ogni unità di lavoro significativa.
- Stage per filename, non `git add -A`.
- Commit messages: imperativo, cosa è cambiato e perché.
