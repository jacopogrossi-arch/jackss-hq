# CLAUDE.md

This file gives Claude Code the context to work well in this repository.

---

## Chi lavora qui

Jacopo è un giovane italiano che studia fashion design ed economia, e in parallelo agli studi studia e applica l'AI — soprattutto automazioni e generazione video. Claude Code è il suo secondo cervello: lo usa sia per imparare che per costruire concretamente le cose su cui sta lavorando.

Sul piano tecnico, Jacopo non è uno sviluppatore. Usa Claude Code con una certa fluidità, capisce la logica dei workflow, ma non ha esperienza con API, n8n, o programmazione generale. Questo non è un limite — è il punto di partenza. Quando lavoro con lui, l'obiettivo non è fare le cose al suo posto: è fargli capire quello che stiamo costruendo insieme, perché domani potrebbe doverlo spiegare agli iscritti della sua community.

Il principio guida di questo repo: **semplice e funzionante batte elegante e complesso**. Non perché Jacopo non possa imparare cose complesse — ma perché il suo tempo vale di più sull'apprendimento e sulle decisioni strategiche.

---

## Struttura del repository

```
browser-games/
├── CLAUDE.md                        ← questo file
├── snake3.html                      ← gioco browser (3-Headed Snake)
├── n8n-automation/                  ← pipeline AI content automation
│   ├── overview.md
│   ├── progress.md
│   ├── workflows/workflow-01.md
│   └── prompts/system-prompt.md
└── ai-content-claude/               ← corso generazione immagini/video AI
    ├── style-guide.md
    ├── platform-cheatsheet.md
    ├── progress.md
    └── prompts/
        ├── hw1-image-prompts.md
        └── hw2-video-prompts.md
```

---

## Git workflow

- Remote: https://github.com/jacopogrossi-arch/browser-games — default branch `master`
- Commit and push after every meaningful unit of work. Stage by filename, not `git add -A`.
- Commit messages: imperative mood, what changed and why.

---

## Browser Games (snake3.html)

Il repo si chiama `browser-games` e contiene un gioco browser scritto in HTML/CSS/JS vanilla, tutto in un singolo file auto-contenuto.

**3-Headed Snake** (`snake3.html`):
- Snake game con twist: il giocatore ha una testa centrale che si biforca in 3 teste
- 3 AI avversari con comportamento autonomo (inseguono il cibo, evitano i muri)
- Controlli: frecce / A-D per girare, mouse opzionale per puntare
- Salvataggio high score via `localStorage`
- Stack: HTML Canvas API, JavaScript puro, CSS — zero dipendenze esterne

Per aprire: basta aprire il file in un browser. Non serve server, build step, o npm.

---

## AI Content Automation (n8n-automation/)

### La visione

L'obiettivo finale non è "fare video" — è costruire una macchina che pubblica contenuti sulla nicchia moda maschile quasi in automatico, così Jacopo può concentrarsi su Inverso e sulla community Skool. Il canale è anonimo (no faccia, voiceover AI sintetico): non per timidezza, ma perché un sistema anonimo è scalabile — non dipende da una presenza personale.

Questo progetto è anche un prodotto da vendere: la community Skool "Come costruire un brand di moda con €1.000" mostrerà esattamente questo sistema come esempio reale. Ogni cosa che costruiamo qui è potenzialmente materiale didattico.

### Stato attuale: PIPELINE COMPLETA ✅

La pipeline end-to-end è funzionante al 10/05/2026. Tutti i nodi principali sono stati integrati e testati con successo.

### Pipeline attiva (workflow-01)

```
Schedule Trigger (ogni 48h)
    ↓
Google Sheets — leggi foglio "Argomenti"
    ↓
Code (JS) — scegli argomento a caso + costruisci prompt
    ↓
Basic LLM Chain ← Anthropic Chat Model (claude-sonnet-4-6)
    ↓
Code (JS) — unisci script + argomento + data
    ↓
Google Sheets — Append row in "Sheet1"
    +
HTTP Request — ElevenLabs → voiceover .mp3
    ↓
Google Drive — Upload + rendi pubblico
    ↓
HTTP Request — HeyGen → genera video con avatar Adriana
    ↓
Wait (12 minuti)
    ↓
HTTP Request — HeyGen status check → prende video_url
    ↓
Telegram — notifica con link video
```

### Stack

| Tool | Ruolo | Costo |
|------|-------|-------|
| n8n (self-hosted) | Orchestrazione workflow | ~€10/mese VPS |
| Claude API (claude-sonnet-4-6) | Generazione script | Pay per use |
| ElevenLabs | Voiceover sintetico (Voice ID: `SAz9YHcvj6GT2YYXdXww`) | ~€22/mese |
| HeyGen | Video con avatar AI (Adriana_Business_Front_public) | ~€29/mese |
| Buffer | Scheduling social (da integrare) | ~€15/mese |
| Google Sheets | Content queue (argomenti + log script) | Gratis |
| Google Drive | Storage audio .mp3 | Gratis |
| Telegram | Notifica finale con link video | Gratis |

### Note tecniche critiche

- n8n si avvia con `n8n start` — poi aprire http://localhost:5678
- `npx n8n` NON funziona con Node.js v24
- n8n in incognito se il browser normale non carica (problema di cache)
- Output di Basic LLM Chain → `{{ $json.text }}`
- Riferimento a nodo precedente nel secondo Code node: `$('Code in JavaScript').first().json.argomento`
- HeyGen: credenziale Header Auth con nome `X-Api-Key` (non OAuth)
- Il file Drive deve essere reso pubblico prima di passare l'URL a HeyGen
- Wait HeyGen: 12 minuti (7 non bastano per video da 60s)
- OAuth redirect URI Google: `http://localhost:5678/rest/oauth2-credential/callback`
- L'audio ElevenLabs viene restituito come `.mpga` — va bene rinominarlo `.mp3` su Drive

### Come collaborare su questo progetto

Jacopo sta imparando n8n e le API mentre costruisce. Le spiegazioni devono arrivare fino al livello pratico — dove cliccare, cosa copiare, dove incollare. I termini tecnici vanno spiegati al primo utilizzo.

In n8n, le soluzioni visuali (drag-and-drop tra nodi) sono da preferire al codice custom. Quando il codice è necessario, va commentato in italiano. Ogni nuova API si testa prima con un nodo HTTP Request minimale, prima di integrarla nella pipeline.

### Prossimi step

- [ ] Aggiungere B-roll cinematografico con Kling API
- [ ] Editing automatico con Shotstack (motion graphics, transizioni, testi)
- [ ] Integrare Buffer → pubblicazione social automatica
- [ ] Valutare avatar personalizzato su HeyGen

### File di progetto

- `overview.md` — obiettivo, stack, pipeline, accesso
- `progress.md` — stato avanzamento, note tecniche, prossimi passi
- `workflows/workflow-01.md` — workflow attuale step by step con dettaglio ogni nodo
- `prompts/system-prompt.md` — system prompt Claude per generare gli script

### Monetizzazione

Community Skool "Come costruire un brand di moda con €1.000" — €29-49/mese. Target: 100 iscritti = €2.900-4.900/mese.

---

## AI Image & Video Generation (ai-content-claude/)

### La visione

Questo progetto non è automazione — è un percorso di apprendimento creativo. L'obiettivo è sviluppare un "occhio" per la generazione di immagini e video AI di qualità professionale, applicato al settore moda/lusso. La skill, una volta acquisita, diventa un servizio da offrire a clienti.

> Questo progetto è completamente separato da quello n8n sopra. Non usa workflow automatizzati. Il lavoro è manuale, iterativo, creativo — più vicino alla post-produzione fotografica che alla programmazione.

### Brand di studio

Il sandbox è un'identità visiva luxury Italian fashion: giovane uomo italiano elegante (~25 anni) in Ferrari convertibile anni '80, campagna Toscana, strade con pini. L'aesthetic è old money — dolce vita, Riviera italiana, lusso senza ostentazione.

- Palette: amber `#F5E6C8`, gold `#C9A46A`, deep red `#8B0000`, near-black `#1E1E1E`
- Riferimenti: campagne Marlboro anni '70, Helmut Newton, *Blade Runner 2049*

### Come collaborare su questo progetto

Su questo progetto si ragiona come un direttore della fotografia che dà note — non come un programmatore. La struttura naturale di ogni prompt è:

**SHOT TYPE → LENS → LIGHT → TEXTURE → COMPOSITION → STYLE**

I tool hanno caratteristiche diverse: Gemini/NanoBanana per iterazioni veloci e moodboard; Midjourney per qualità alta; Krea per ritratti fashion realistici; HiggsField per campagne ultra-realistiche; Kling per video (Text-to-Video e Image-to-Video).

### Stato avanzamento homework

- [x] HW 1 — Image Prompting (Gemini): 3 varianti prompt + JSON prompt
- [x] HW 1.3 — Costruire il Gusto Visivo: moodboard + 10 keyword estetiche + 3 immagini coerenti
- [x] HW 1.4 — Aesthetic Types: 3 Pinterest board + estetica cinematica scelta
- [x] HW 1.5 — Character Creation: personaggio via PromptEngine + JSON strutturato
- [x] HW 1.6 — Campaign Generation: campaign con PromptEngine + immagini MidJourney (OmniReference)
- [x] HW 2 — Video Generation (Kling): TTV prompt + I2V prompt (bug: Ferrari va in reverse — workaround da testare)
- [x] HW 2.4 — Camera Movement: 3-4 versioni con movimenti diversi (Static/Push-in/Pan/Tracking)
- [x] HW 2.5 — LipSync: talking avatar con Kling, stili e personaggi diversi
- [ ] HW 3 — (da assegnare)

### Prossimi step

- [ ] Risolvere bug reverse-motion in Kling I2V
- [ ] Testare Kling Pro vs standard
- [ ] Esplorare HiggsField per qualità superiore rispetto a Gemini
- [ ] Costruire Prompt System riutilizzabile per il brand (Advanced Option A, HW1)
- [ ] Test griglia lens + lighting: 35mm/daylight vs 85mm/tungsten vs 24mm/neon vs 50mm/backlit

### File di progetto

- `style-guide.md` — identità visiva, palette, sistema prompt, negative prompts
- `platform-cheatsheet.md` — quale tool usare per cosa
- `prompts/hw1-image-prompts.md` — prompt immagini Homework 1
- `prompts/hw2-video-prompts.md` — prompt video Homework 2 (Kling)
- `progress.md` — log completo avanzamento e prossimi step
