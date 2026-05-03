# AI Content Automation — n8n

## Obiettivo

Sistema quasi completamente automatizzato che genera e pubblica contenuti video sulla nicchia **moda maschile + brand building**, canale anonimo (no faccia, voiceover sintetico).

## Pipeline completa

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

## Stack

| Tool | Ruolo | Costo |
|------|-------|-------|
| n8n (self-hosted) | Orchestrazione workflow | ~€10/mese VPS |
| Claude API (claude-sonnet-4-6) | Generazione script | Pay per use |
| ElevenLabs | Voiceover sintetico | ~€22/mese |
| HeyGen | Video con avatar AI | ~€29/mese |
| Buffer | Scheduling social | ~€15/mese |
| Google Sheets / Airtable | Content queue | Gratis |

## Monetizzazione

- Community Skool "Come costruire un brand di moda con €1.000" — €29-49/mese
- Target: 100 iscritti = €2.900-4.900/mese

## Accesso

- n8n: `n8n start` → http://localhost:5678
- Content queue: Google Sheet (colonne: A=data, B=argomento, C=script)
