# Progress — n8n Automation

_Ultimo aggiornamento: 03/05/2026_

## Completato

- [x] Node.js v24 installato
- [x] n8n installato globalmente (`npm install -g n8n`) — si avvia con `n8n start`
- [x] Account n8n creato su http://localhost:5678
- [x] Claude API key collegata in n8n (credenziale Anthropic attiva, credito $5 caricato)
- [x] OAuth Client ID creato su console.cloud.google.com
- [x] Google Sheets API e Google Drive API abilitate su Google Cloud Console
- [x] Google Sheets collegato in n8n (OAuth2, credenziale attiva)
- [x] Google Sheet content queue creato — foglio "Sheet1", colonne: A=data, B=argomento, C=script
- [x] Foglio "Argomenti" aggiunto al Google Sheet — header in A1, 8 argomenti nelle righe 2-9
- [x] Schedule Trigger ogni 48h attivato (ha sostituito il trigger manuale)
- [x] Nodo Code: legge foglio Argomenti, sceglie argomento a caso, costruisce prompt
- [x] Basic LLM Chain: Claude genera script TikTok 60s (output in `$json.text`)
- [x] Bug risolto (26/04/2026): nodo Code dopo LLM Chain che unisce script+argomento+data
- [x] ElevenLabs integrato (26/04/2026): HTTP Request Raw → voiceover generato. Voice ID: `SAz9YHcvj6GT2YYXdXww`

## In corso / Prossimi passi

- [ ] **PROSSIMO STEP:** Salvare l'audio su Google Drive — aggiungere nodo Google Drive dopo HTTP Request per salvare il file `.mp3` di ElevenLabs
- [ ] Integrare HeyGen → video assemblato automaticamente
- [ ] Aggiungere nodo Telegram finale → notifica preview con link al video
- [ ] Integrare Buffer → pubblicazione social automatica

## Note tecniche importanti

- n8n si avvia con `n8n start` — poi aprire http://localhost:5678
- `npx n8n` NON funziona con Node.js v24 — usare sempre `npm install -g n8n` + `n8n start`
- Output di Basic LLM Chain → `{{ $json.text }}`
- Nel nodo Code dopo LLM Chain: `const script = $input.first().json.text` (non `.script`)
- URI redirect OAuth Google: `http://localhost:5678/rest/oauth2-credential/callback`
- `{{ $json.script }}`, `{{ $json.argomento }}`, `{{ $json.data }}` → colonne Google Sheet
