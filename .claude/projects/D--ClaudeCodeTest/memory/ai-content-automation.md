---
name: ai-content-automation
description: Progetto n8n per video automatici su moda maschile — stato e prossimi passi
metadata:
  type: project
---

# AI Content Automation — Moda Maschile

Sistema automatizzato per generare e pubblicare video su **moda maschile + brand building**.
Canale anonimo, voiceover sintetico (ElevenLabs), nessuna faccia in video.

Pagina Notion: https://www.notion.so/35030837a9e681169218f20d895d9ebb

> Vedi anche: `n8n-automation/overview.md` e `n8n-automation/progress.md` per dettagli tecnici completi.

## Stato (10/05/2026) — PIPELINE COMPLETA

| Componente | Stato |
|-----------|-------|
| n8n + Claude API + Google Sheets | ✅ Funzionante |
| ElevenLabs voiceover | ✅ Funzionante |
| Google Drive (salvataggio audio) | ✅ Funzionante |
| HeyGen video (avatar Adriana) | ✅ Funzionante |
| Telegram notifiche | ✅ Funzionante |
| n8n su VPS Hetzner | ⏳ Prossimo step |
| Buffer pubblicazione social | ⏳ Da integrare |

## Roadmap prossimi step (in ordine di priorità)

1. **Migrare n8n su Hetzner VPS** — Hetzner CX22 (~€4/mese, Docker). Piano dettagliato: `.claude/plans/si-mettiamo-l-opzione-c-jazzy-ocean.md`
2. **Integrare Buffer** — pubblicazione automatica TikTok, Instagram, YouTube
3. **Aggiungere B-roll cinematografico** — Kling API
4. **Editing automatico con Shotstack** — motion graphics, transizioni, testi
5. **Avatar personalizzato HeyGen** — solo dopo che il canale ha trazione
6. **Trend Scouting** — Google Trends o Reddit API
7. **3 script per formato** — TikTok 60s, Reels, YouTube 8min (oggi genera solo TikTok 60s)

## Stack e accesso

- n8n: `n8n start` → http://localhost:5678 (attualmente su Mac locale, da migrare su VPS)
- Content queue: Google Sheets (colonne: A=data, B=argomento, C=script)
- Voice ID ElevenLabs: `SAz9YHcvj6GT2YYXdXww`
- HeyGen avatar: `Adriana_Business_Front_public` (1080×1920)
- Schedule: ogni 48h

## Monetizzazione pianificata

Community Skool "Come costruire un brand di moda con €1.000" — €29–49/mese
Target: 100 iscritti = €2.900–4.900/mese
