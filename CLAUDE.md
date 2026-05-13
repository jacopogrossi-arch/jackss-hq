# CLAUDE.md

This file gives Claude Code the context to work well in this repository.

---

## Chi lavora qui

Jacopo è un giovane italiano che studia fashion design ed economia, e in parallelo agli studi studia e applica l'AI — soprattutto automazioni e generazione video. Claude Code è il suo secondo cervello: lo usa sia per imparare che per costruire concretamente le cose su cui sta lavorando.

Sul piano tecnico, Jacopo non è uno sviluppatore. Usa Claude Code con una certa fluidità, capisce la logica dei workflow, ma non ha esperienza con API, n8n, o programmazione generale. Questo non è un limite — è il punto di partenza. Quando lavoro con lui, l'obiettivo non è fare le cose al suo posto: è fargli capire quello che stiamo costruendo insieme, perché domani potrebbe doverlo spiegare agli iscritti della sua community.

Il principio guida di questo repo: **semplice e funzionante batte elegante e complesso**. Non perché Jacopo non possa imparare cose complesse — ma perché il suo tempo vale di più sull'apprendimento e sulle decisioni strategiche.

---

## Notion — Jackss HQ

Jacopo gestisce tutta la sua vita e i suoi progetti in un unico workspace Notion chiamato **Jackss HQ**. È il suo sistema centrale, non uno strumento secondario. Contiene:

- **Studio personale** — appunti, risorse, percorsi di apprendimento su AI, moda, economia e tutto quello che studia in autonomia.
- **AI & Video Generation** — documentazione, idee, esperimenti e avanzamento sui progetti di automazione (n8n) e generazione creativa (immagini/video AI).
- **Salute e sport** — tracking allenamenti, obiettivi fisici, abitudini.

Quando si fa riferimento a documentazione personale, note di ricerca, o stato di un progetto che non è in questo repo, è probabile che si trovi su Notion / Jackss HQ. Usare il MCP Notion per accedervi se necessario.

---

## Git workflow

- Remote: https://github.com/jacopogrossi-arch/jackss-hq — default branch `master`
- Commit and push after every meaningful unit of work. Stage by filename, not `git add -A`.
- Commit messages: imperative mood, what changed and why.

---

## AI Content Automation (n8n-automation/)

### La visione

L'obiettivo finale non è "fare video" — è costruire una macchina che pubblica contenuti sulla nicchia moda maschile quasi in automatico, così Jacopo può concentrarsi su Inverso e sulla community Skool. Il canale è anonimo (no faccia, voiceover AI sintetico): non per timidezza, ma perché un sistema anonimo è scalabile — non dipende da una presenza personale.

Questo progetto è anche un prodotto da vendere: la community Skool "Come costruire un brand di moda con €1.000" mostrerà esattamente questo sistema come esempio reale. Ogni cosa che costruiamo qui è potenzialmente materiale didattico.

### Come collaborare su questo progetto

Jacopo sta imparando n8n e le API mentre costruisce. Non conosce ancora il funzionamento interno dei workflow, ma capisce il "perché" quando lo si spiega bene. Le spiegazioni devono arrivare fino al livello pratico — dove cliccare, cosa copiare, dove incollare. I termini tecnici vanno spiegati al primo utilizzo.

In n8n, le soluzioni visuali (drag-and-drop tra nodi) sono da preferire al codice custom. Quando il codice è necessario, va commentato in italiano. Ogni nuova API si testa prima con un nodo HTTP Request minimale, prima di integrarla nella pipeline. Ogni workflow deve terminare con un nodo Telegram — è la conferma visibile che la macchina ha funzionato.

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

Community Skool "Come costruire un brand di moda con €1.000" — €29-49/mese. Target: 100 iscritti = €2.900-4.900/mese.

### Stato corrente

Vedi `n8n-automation/progress.md` per lo stato aggiornato. File progetto in `n8n-automation/`:
- `overview.md` — obiettivo, stack, pipeline, monetizzazione
- `progress.md` — stato avanzamento, note tecniche, prossimi passi
- `workflows/workflow-01.md` — workflow attuale step by step
- `prompts/system-prompt.md` — system prompt Claude per generare gli script

---

## AI Image & Video Generation (ai-content-claude/)

### La visione

Questo progetto non è automazione — è un percorso di apprendimento creativo. L'obiettivo è sviluppare un "occhio" per la generazione di immagini e video AI di qualità professionale, applicato al settore moda/lusso. La skill, una volta acquisita, diventa un servizio da offrire a clienti.

> Questo progetto è completamente separato da quello n8n sopra. Non usa workflow automatizzati. Il lavoro è manuale, iterativo, creativo — più vicino alla post-produzione fotografica che alla programmazione.

### Brand di studio

Il sandbox è un'identità visiva luxury Italian fashion: giovane uomo italiano elegante (~25 anni) in Ferrari convertibile anni '80, campagna Toscana, strade con pini. L'aesthetic è old money — dolce vita, Riviera italiana, lusso senza ostentazione. Non è il brief di un cliente reale: è un terreno di prova scelto perché il lusso richiede precisione comunicativa. O funziona visivamente, o non funziona — non c'è via di mezzo.

- Palette: amber `#F5E6C8`, gold `#C9A46A`, deep red `#8B0000`, near-black `#1E1E1E`
- Riferimenti: campagne Marlboro anni '70, Helmut Newton, *Blade Runner 2049*

### Come collaborare su questo progetto

Su questo progetto si ragiona come un direttore della fotografia che dà note — non come un programmatore. La struttura naturale di ogni prompt è:

**SHOT TYPE → LENS → LIGHT → TEXTURE → COMPOSITION → STYLE**

I tool hanno caratteristiche diverse: Gemini/NanoBanana per iterazioni veloci e moodboard; Midjourney per qualità alta; Krea per ritratti fashion realistici; HiggsField per campagne ultra-realistiche; Kling per video (Text-to-Video e Image-to-Video).

### Stato avanzamento

- [x] Homework 1: 3 varianti prompt immagine + JSON prompt (Gemini)
- [x] Homework 2: TTV e I2V con Kling (brand Ferrari/Toscana)
- [ ] Homework 3 e successivi (in corso)

File progetto in `ai-content-claude/`:
- `style-guide.md` — identità visiva, palette, sistema prompt
- `platform-cheatsheet.md` — quale tool usare per cosa
- `prompts/hw1-image-prompts.md` — prompt immagini Homework 1
- `prompts/hw2-video-prompts.md` — prompt video Homework 2 (Kling)
- `progress.md` — log avanzamento e prossimi step

---

## Segnali dal Daily Log Agent

Il file `claude-signals.md` nella root del repo viene aggiornato automaticamente ogni notte dall'agente `Jackss — Daily Log Processor`, che legge i Daily Log di Notion e rileva nuovi progetti, contatti, decisioni e obiettivi.

**All'inizio di ogni sessione:** leggi `claude-signals.md` se esiste. Per ogni blocco marcato `Da processare`:
1. Estrai le informazioni rilevanti (nuovi progetti, contatti, decisioni, obiettivi)
2. Salva nei file di memoria appropriati in `C:\Users\Jacopo Grossi\.claude\projects\D--ClaudeCodeTest\memory\`
3. Marca il blocco come `Processato` (sostituisci `Da processare` con `Processato`)
4. Salva con Edit
