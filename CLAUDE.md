# CLAUDE.md

This file gives Claude Code the context to work well in this repository.

---

## Chi è Jacopo

Giovane italiano (Roma) con un progetto imprenditoriale in sviluppo nel settore AI + moda.
Non è uno sviluppatore: le spiegazioni devono essere pratiche (dove cliccare, cosa copiare, dove incollare).

**Principio guida: semplice e funzionante batte elegante e complesso.**

Per il contesto sulla vita personale (studi, sport, persone importanti), leggere la memoria `user_personal_life.md`.

**Obiettivo:** portare Inverso al Drop 1 (primo capo, pre-order) — chiudere il ciclo idea→capo→campagna→vendita.

---

## Progetto principale — INVERSO (dal 13/07/2026)

**Inverso** — brand menswear italiano reale, costruito in build-in-public col volto di Jacopo.
**Prima di tutto è un progetto personale di vita e ricerca**: sviluppo del gusto creativo, ricerca su tessuti e materiali, passione per la moda. I soldi finanziano la ricerca, non sono il fine.

File: `inverso/`
- `piano-inverso.md` — piano maestro del progetto
- `briefing-2026-07-12-inverso-strategia.md` — briefing strategico fondativo
- `analisi/` — analisi delle skill marketing (copywriting, psychology, social, positioning, idee)
- `assets-jago/` — asset dell'avatar Jago (logo, palette, moodboard), ora strumento di Inverso

**Struttura:** Jacopo = volto del processo (profilo IG personale) · @inverso = risultato/drop · Jago = modello virtuale dei lookbook · @jagoworks = congelato, vetrina servizio.
**Marketing:** skill `/inverso-marketing` (strategia) + copywriting/psychology/social/product-marketing/marketing-ideas (globali, coreyhaines31). Contesto letto da tutte: `.agents/marketing-context.md`.
**Servizi (Lookbook AI, Idea→Campione):** solo dopo il Drop 1.

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
- **Canale Jago** (7 video pubblicati, outreach, strategia — chiuso come progetto autonomo il 13/07/2026, Jago vive come strumento di Inverso) → `archivio/canale-jago/`. La skill `/jago-creative-director` resta per eventuali video lookbook di Inverso.

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
