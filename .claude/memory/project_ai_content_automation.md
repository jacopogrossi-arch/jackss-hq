---
name: AI Content Automation — Fashion Niche
description: n8n-based pipeline that scouts trends, generates scripts via Claude API, produces voiceover (ElevenLabs), assembles video (HeyGen), and publishes to social. Monetizes via Skool community.
type: project
originSessionId: c4cf44b3-cbd3-4c1f-8268-2a197ebde75b
---
**Obiettivo:** sistema quasi completamente automatizzato per contenuti video su moda maschile + brand building, canale anonimo (no faccia).

**Pipeline principale:**
Schedule (48h) → Claude API (script TikTok 60s) → ElevenLabs voiceover → Google Drive (salva audio) → HeyGen video → Telegram (notifica con link)

**Stack:**
- n8n self-hosted — orchestrazione
- Claude API — generazione script
- ElevenLabs — voiceover (Voice ID: `SAz9YHcvj6GT2YYXdXww`)
- HeyGen — video con avatar (Avatar: `Adriana_Business_Front_public`)
- Google Drive — storage audio
- Google Sheets — content queue
- Telegram — notifica finale
- Buffer (~€15/mese) — scheduling social (da integrare)

**Monetizzazione target:** community Skool "Come costruire un brand di moda con €1.000" a €29-49/mese → target 100 iscritti

**STATO AL 10/05/2026 — PIPELINE COMPLETA E FUNZIONANTE:**
- [x] n8n installato e attivo su localhost:5678
- [x] Claude API collegata
- [x] Google Sheets + Drive collegati (OAuth2)
- [x] ElevenLabs integrato (voiceover)
- [x] Google Drive: salva audio + rende file pubblico
- [x] HeyGen integrato: genera video con avatar Adriana
- [x] Telegram: notifica con link video
- [x] Workflow end-to-end testato e funzionante

**Struttura workflow in n8n:**
```
Schedule Trigger (48h)
→ Google Sheets (leggi argomenti)
→ Code in JavaScript (scegli argomento, costruisci prompt)
→ Basic LLM Chain (Claude sonnet-4-6)
→ Code in JavaScript1 (unisci output)
→ Google Sheets (append row)
→ HTTP Request (ElevenLabs voiceover)
→ Google Drive Upload file
→ Google Drive Share (rendi pubblico)
→ HTTP Request1 (HeyGen genera video)
→ Wait (12 minuti)
→ HTTP Request2 (HeyGen status check)
→ Telegram (notifica con link)
```

**Note tecniche critiche:**
- n8n: `n8n start` → http://localhost:5678 (aprire in incognito se cache problema)
- `npx n8n` NON funziona con Node.js v24
- `argomento` nel secondo Code node: `const argomento = $('Code in JavaScript').first().json.argomento`
- HeyGen auth: Header Auth manuale con `X-Api-Key` (non credenziale OAuth)
- File Drive deve essere pubblico prima di passare URL a HeyGen
- URL audio per HeyGen: `https://drive.google.com/uc?export=download&id={{ $('Upload file').first().json.id }}`
- Wait HeyGen: 12 minuti (7 non bastano)
- HeyGen API: pay-as-you-go separato dall'abbonamento (~$1/min video)

**Prossimi passi:**
1. Migliorare qualità video: B-roll cinematografico con Kling API
2. Editing automatico con Shotstack (motion graphics, transizioni)
3. Integrare Buffer per pubblicazione social automatica

**Agente schedulato:** routine `trig_01KtQnMQVzwBW11FqaE8KxRz` — ogni giorno alle 8:00 (CEST) organizza Notion e aggiorna `n8n-automation/progress.md` su GitHub (`jackss-hq`)

**Why:** monetizzare tramite contenuti AI su social, portare traffico alla community Skool, in parallelo al brand fisico Inverso.
**How to apply:** suggerire soluzioni semplici e funzionanti per n8n; preferire MVP veloci. Per lo stato aggiornato leggere `n8n-automation/progress.md`.
