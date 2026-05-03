# Workflow 01 — Generazione Script + Voiceover

_Stato: ATTIVO e funzionante al 26/04/2026_

## Schema completo

```
Schedule Trigger (ogni 48h)
    ↓
Google Sheets — leggi foglio "Argomenti"
    ↓
Code (JavaScript) — scegli argomento a caso + costruisci prompt
    ↓
Basic LLM Chain  ←  Anthropic Chat Model (claude-sonnet-4-6)
    ↓
Code (JavaScript) — unisci script + argomento + data
    ↓
Google Sheets — Append row in "Sheet1"
    +
HTTP Request → ElevenLabs API → voiceover .mp3
```

## Dettaglio nodi

### 1. Schedule Trigger
- Frequenza: ogni 48 ore
- Sostituisce il vecchio "Manual Trigger"

### 2. Google Sheets — Leggi argomenti
- Operazione: Read Rows
- Foglio: "Argomenti"
- Struttura: A1 = header "Argomenti", righe 2-9 = lista argomenti

### 3. Code — Scegli argomento (JavaScript)
- Legge tutte le righe dal nodo precedente
- Sceglie un argomento a caso
- Costruisce il prompt completo per Claude
- Output: `{ argomento, prompt }`

### 4. Basic LLM Chain
- Collegato a: Anthropic Chat Model (claude-sonnet-4-6)
- Input: prompt costruito dal nodo Code
- Output: `{ text: "..." }` → lo script generato

### 5. Code — Unisci output (JavaScript)
- `const script = $input.first().json.text` _(attenzione: `.text`, non `.script`)_
- Output: `{ script, argomento, data }`

### 6. Google Sheets — Append Row
- Foglio: "Sheet1"
- Mappatura colonne:
  - A (data): `{{ $json.data }}`
  - B (argomento): `{{ $json.argomento }}`
  - C (script): `{{ $json.script }}`

### 7. HTTP Request — ElevenLabs
- Metodo: POST
- Modalità: Raw (JSON)
- Voice ID: `SAz9YHcvj6GT2YYXdXww`
- Il nodo Code prepara `elevenLabsBody` con `JSON.stringify`
- Output: file audio `.mp3`

## Prossima evoluzione → Workflow 02

Aggiungere dopo HTTP Request:
- Nodo **Google Drive** → salva il file `.mp3`
- Nodo **HeyGen** → assembla il video
- Nodo **Telegram** → notifica finale con preview
