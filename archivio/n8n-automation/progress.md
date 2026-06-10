# Progress — n8n Automation

_Ultimo aggiornamento: 10/05/2026_

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
- [x] Schedule Trigger ogni 48h attivato
- [x] Nodo Code: legge foglio Argomenti, sceglie argomento a caso, costruisce prompt
- [x] Basic LLM Chain: Claude genera script TikTok 60s
- [x] Bug risolto (26/04/2026): nodo Code dopo LLM Chain che unisce script+argomento+data
- [x] ElevenLabs integrato: HTTP Request Raw → voiceover generato. Voice ID: `SAz9YHcvj6GT2YYXdXww`
- [x] Google Drive integrato (10/05/2026): audio .mp3 salvato su Drive + reso pubblico
- [x] HeyGen integrato (10/05/2026): genera video con avatar Adriana (`Adriana_Business_Front_public`)
- [x] Telegram integrato (10/05/2026): notifica finale con link video
- [x] **PIPELINE COMPLETA E FUNZIONANTE** — workflow end-to-end testato con successo

## Prossimi step

- [ ] **Migrare n8n su Hetzner VPS** — server sempre acceso, indipendente dal PC locale. Piano completo in `.claude/plans/si-mettiamo-l-opzione-c-jazzy-ocean.md` (Hetzner CX22 €3.79/mese, Docker, 9 fasi)
- [ ] Integrare Buffer → pubblicazione social automatica
- [ ] Migliorare qualità video: aggiungere B-roll cinematografico con Kling API
- [ ] Aggiungere editing automatico con Shotstack (motion graphics, transizioni, testi)
- [ ] Valutare avatar personalizzato su HeyGen

## Note tecniche importanti

- n8n si avvia con `n8n start` — poi aprire http://localhost:5678
- `npx n8n` NON funziona con Node.js v24
- n8n in incognito se il browser normale non carica (problema di cache)
- Output di Basic LLM Chain → `{{ $json.text }}`
- `argomento` nel secondo Code node: `const argomento = $('Code in JavaScript').first().json.argomento`
- HeyGen: credenziale Header Auth con nome `X-Api-Key` (non OAuth)
- Il file Drive deve essere reso pubblico prima di passare l'URL a HeyGen
- Wait HeyGen: 12 minuti (7 non bastano per video da 60s)
- URI redirect OAuth Google: `http://localhost:5678/rest/oauth2-credential/callback`
