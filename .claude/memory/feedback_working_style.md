---
name: Working style — AI Content Automation project
description: Rules for how Claude should behave when working on the n8n/AI automation project
type: feedback
originSessionId: 1e6f79a3-68d1-482e-841a-d69ed4bc8f72
---
- Spiega sempre cosa fa ogni nodo/blocco di codice **in italiano semplice**
- Preferisci soluzioni **semplici e funzionanti** rispetto a soluzioni eleganti ma complesse
- Quando un'API non ha documentazione chiara, scrivi prima un **test minimale**
- Ogni workflow n8n deve avere un **nodo di notifica Telegram finale** per il monitoring
- Il codice nei nodi custom deve essere **commentato in italiano**
- Se qualcosa si può fare visualmente in n8n **senza codice**, preferisci quello
- Quando l'utente scrive **"riprendiamo"**: leggere subito la memoria, identificare l'ultima task in sospeso e ripartire da lì senza aspettare ulteriori istruzioni
- **Fine sessione**: chiedere sempre all'utente di salvare la memoria aggiornata e indicare chiaramente quale sarà la prossima task da svolgere nella sessione successiva

**Why:** l'utente è principiante su n8n e API — priorità alla semplicità e alla comprensione. Le regole di continuità tra sessioni servono a non perdere mai il filo del lavoro.
**How to apply:** su ogni risposta relativa a n8n o integrazioni API, seguire queste regole senza che l'utente debba ricordarmele ogni volta. A fine sessione, ricapitolare sempre lo stato e la prossima task prima di chiudere.
