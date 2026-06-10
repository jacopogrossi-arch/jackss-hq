# Workflow 01 — Pipeline Completa

_Stato: ATTIVO e funzionante al 10/05/2026_

## Schema completo

```
Schedule Trigger (ogni 48h)
    ↓
Google Sheets — leggi foglio "Argomenti"
    ↓
Code in JavaScript — scegli argomento a caso + costruisci prompt
    ↓
Basic LLM Chain  ←  Anthropic Chat Model (claude-sonnet-4-6)
    ↓
Code in JavaScript1 — unisci script + argomento + data
    ↓
Google Sheets — Append row in "Sheet1"
    +
HTTP Request — ElevenLabs → voiceover .mp3
    ↓
Google Drive (Upload file) — salva audio .mp3
    ↓
Google Drive (Share) — rende il file pubblico
    ↓
HTTP Request1 — HeyGen → genera video con avatar
    ↓
Wait (12 minuti)
    ↓
HTTP Request2 — HeyGen status check → prende video_url
    ↓
Telegram — invia notifica con link video
```

## Dettaglio nodi

### 1. Schedule Trigger
- Frequenza: ogni 48 ore

### 2. Google Sheets — Leggi argomenti
- Operazione: Read Rows
- Foglio: "Argomenti"
- Struttura: A1 = header "Argomenti", righe 2-9 = lista argomenti

### 3. Code in JavaScript — Scegli argomento
- Legge tutte le righe dal nodo precedente
- Sceglie un argomento a caso
- Costruisce il prompt completo per Claude
- Output: `{ argomento, prompt }`

### 4. Basic LLM Chain
- Collegato a: Anthropic Chat Model (claude-sonnet-4-6)
- Output: `{ text: "..." }`

### 5. Code in JavaScript1 — Unisci output
- `const script = $input.first().json.text`
- `const argomento = $('Code in JavaScript').first().json.argomento`
- Output: `{ script, argomento, data, elevenLabsBody }`

### 6. Google Sheets — Append Row
- Foglio: "Sheet1" — colonne: A=data, B=argomento, C=script

### 7. HTTP Request — ElevenLabs
- Metodo: POST, modalità Raw
- Voice ID: `SAz9YHcvj6GT2YYXdXww`
- Response Format: `File`

### 8. Google Drive — Upload file
- Operation: Upload
- Input Data Field Name: `data`
- Nome file: `{{ $('Code in JavaScript1').first().json.argomento }}_{{ $('Code in JavaScript1').first().json.data }}.mp3`
- Parent Folder: Root

### 9. Google Drive — Share
- Operation: Share
- File ID: `{{ $json.id }}`
- Permessi: Anyone with the link → Reader

### 10. HTTP Request1 — HeyGen genera video
- Metodo: POST
- URL: `https://api.heygen.com/v2/video/generate`
- Auth: Header manuale `X-Api-Key`
- Avatar ID: `Adriana_Business_Front_public`
- Audio URL: `https://drive.google.com/uc?export=download&id={{ $('Upload file').first().json.id }}`
- Dimensioni: 1080x1920 (verticale)

### 11. Wait
- 12 minuti (HeyGen impiega circa 10-12 min per un video da 60s)

### 12. HTTP Request2 — HeyGen status check
- Metodo: GET
- URL: `https://api.heygen.com/v1/video_status.get?video_id={{ $('HTTP Request1').first().json.data.video_id }}`
- Auth: Header manuale `X-Api-Key`

### 13. Telegram — Notifica finale
- Operazione: Send a Text Message
- Chat ID: personale
- Testo:
```
✅ Video pronto!

Argomento: {{ $('Code in JavaScript1').first().json.argomento }}
Data: {{ $('Code in JavaScript1').first().json.data }}

🎬 Link video: {{ $('HTTP Request2').first().json.data.video_url }}
```

## Note tecniche
- Il nodo Wait va lasciato a 12 minuti — con 7 minuti il video non è ancora pronto
- La credenziale HeyGen è Header Auth con `X-Api-Key` (non OAuth)
- L'audio ElevenLabs viene restituito in formato `.mpga` (MPEG audio) — rinominato `.mp3` su Drive va bene
- Il file Drive deve essere pubblico prima di passare l'URL a HeyGen
