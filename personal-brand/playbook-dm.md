# Playbook DM v2 — Conversione outreach

> Creato 05/07/2026. Questo è il documento che spiega **perché** il DM v1 non ha convertito e **come funziona** il sistema v2. I template pronti da incollare stanno in `outreach.md` (sezione "Template DM") — quella resta l'unica fonte di verità per i testi. Qui c'è il metodo.

---

## 1. Diagnosi — perché 43 DM hanno prodotto 1 sola risposta (negativa)

I dati al 05/07/2026: ~43 DM inviati dal 12/06, 1 risposta (Vanence: "vogliamo un'immagine naturale, no AI"), 0 trattative. Tasso di risposta ~2%. Non è sfortuna: il messaggio v1 ha **cinque difetti strutturali**, in ordine di gravità.

### Difetto 1 — La proof lavora contro di te
Il DM linka un Reel di un brand **fittizio** (VESPRO/SCIROCCO) su un profilo con 9 follower e ~200 view. Il founder fa due click e conclude: "non ha mai lavorato per nessuno, e nessuno lo segue". Il link, che doveva essere la prova di valore, è la cosa che uccide la conversazione. Peggio: chiede al founder di **fare lui il lavoro** — aprire il link, guardare 30 secondi, immaginare come sarebbe sul suo brand.

### Difetto 2 — Personalizzata la prima frase, template tutto il resto
La prima frase è vera e specifica (bene), ma le tre frasi dopo sono **identiche in 40 DM**: stessa presentazione, stesso link, stessa domanda finale. I founder di micro-brand ricevono decine di pitch così e riconoscono il template al primo colpo d'occhio — la frase personalizzata in apertura non basta a salvarlo, anzi sembra il trucco che è.

### Difetto 3 — "usando AI" nella prima battuta
L'unica risposta di mercato ricevuta dice esattamente questo: nella nicchia targettizzata (artigianale, slow fashion, made in Italy, materiali veri) "AI" in apertura è un **repellente**, non un selling point. Il valore da vendere è il risultato (lookbook editoriale, 72h, frazione del costo di uno shooting). L'AI è il *come*, e si spiega quando lo chiedono — mai negarla, ma non metterla in vetrina.

### Difetto 4 — La CTA è una domanda facile da ignorare
"State lavorando a qualcosa del genere per la prossima collezione?" è una domanda sì/no che non costa nulla ignorare e non offre nulla in cambio della risposta. Nessuna ragione concreta per rispondere *ora*.

### Difetto 5 — Volume su un messaggio che non converte
Aggiungere 5 brand al giorno a una lista da 105 mentre il messaggio converte a zero significa **bruciare i candidati migliori** con la versione debole della proposta. La lista non è mai stata il collo di bottiglia. (Per questo la routine daily è in pausa dal 02/07.)

**La sintesi in una riga: nessuno dei 43 ha mai visto cosa sai fare *per lui*.**

### Scoperta 05/07 — il mittente conta più del messaggio
Alcuni DM partiti **per sbaglio dal profilo personale di Jacopo** invece che da
@jagoworks hanno ricevuto risposte (anche solo un grazie, o "mandami tutto via
mail") — mentre gli stessi messaggi da Jago venivano ignorati. Il segnale è
chiaro: un profilo personale vero, con una faccia e una vita dietro, supera il
filtro "spam/bot" che un account brand sconosciuto da 9 follower fa scattare
a prescindere dal contenuto. **Regola nuova: i DM partono dal profilo personale
di Jacopo.** Jago resta il portfolio — lo si nomina nel messaggio ("il progetto
Jago") e chi è curioso se lo va a vedere, ma il primo contatto è da persona a
persona. E "mandami tutto via mail" è di per sé una porta: quando arriva,
rispondere chiedendo l'indirizzo e mandare le immagini + 3 righe di proposta.

---

## 2. I principi del v2

1. **Show, don't tell.** L'allegato batte il link. Il DM porta 2-3 immagini campaign-quality fatte sul **loro capo** — il valore è dentro il messaggio, non a due click di distanza su un profilo che non aiuta.
2. **Il risultato prima del metodo.** "Lookbook editoriali per label emergenti, 72h, frazione del costo di uno shooting" — la parola AI non compare nel primo messaggio. Se chiedono come, si spiega con orgoglio e trasparenza totale.
3. **Regalo, non richiesta.** Il tono è "ho fatto una cosa per voi, guardatela", non "guardate cosa so fare, vi interessa?". Chi riceve un regalo risponde più spesso di chi riceve una richiesta.
4. **Qualità sul volume.** 3-5 DM a settimana fatti così battono 14 al giorno col template. Ogni DM costa 30-60 minuti (immagini incluse): è il costo che rende il messaggio credibile.
5. **Un solo follow-up, ma vero.** Il follow-up non è un sollecito ("hai visto il mio messaggio?"): è la **seconda consegna di valore** — le immagini custom per chi al primo giro aveva ricevuto solo il link.

---

## 3. Il processo "DM pack" — passo per passo (30-60 min a brand)

Questo è il giro completo per un DM v2. In Claude Code basta dire: **"prepara il dm-pack per [brand]"** — la skill `outreach` guida tutti i passi.

1. **Scegli il brand** (vedi sezione 4 per le priorità) e apri il suo feed IG.
2. **Scegli 1 capo** — il più fotogenico e riconoscibile del loro catalogo recente (idealmente dal drop in corso o in arrivo). Salva 1-2 foto pulite del capo dal feed.
3. **Genera 2-3 shot campaign-quality** col workflow lookbook esistente: prompt via skill `banana-pro-director` (mai a mano), Nano Banana Pro con doppia reference (character sheet Jago + silhouette del capo) per gli shot on-model, oppure still-life editoriale se il capo rende meglio da solo. **Valida il primo shot prima di generare gli altri.** Estetica: la loro, non quella di Jago — il lookbook deve sembrare *loro*.
4. **Scrivi il DM** col template v2 da `outreach.md`: osservazione vera + immagini allegate + presentazione risultato-first + micro-CTA.
5. **Invia a mano da IG** (le immagini come foto nel DM, non come link), poi aggiorna tracker in `outreach.md` e database Notion (Stato DM → Contattato, data, follow-up).

**Regola di onestà:** le immagini si presentano per quello che sono — una prova fatta di iniziativa, non un lavoro commissionato. E se il brand risponde "come le hai fatte?", la risposta è la verità.

---

## 4. A chi mandarlo — priorità

Con 30-60 min a DM, la selezione conta più che mai. Ordine di priorità:

1. **Follow-up in scadenza con immagini** (la seconda chance vera): dei ~25 DM v1 in attesa, scegliere i **5 migliori** — criteri 6/6, capo fotogenico, founder raggiungibile. Prima candidatura dal briefing 02/07: Sciamāt Vibe, TRC, Blue of a Kind, Garcias, Maragno Studio.
2. **Play partner** (OUTLAW, Magazzino Ricambi): qui il dm-pack è il mini-look già deciso — farlo e mandarlo finito, senza chiedere permesso.
3. **Brand nuovi 6/6 non ancora contattati**: partono direttamente col v2 — nessun nuovo brand riceve mai più il formato v1.

I brand v1 in attesa che **non** rientrano nei 5 migliori ricevono il follow-up breve classico (o si chiudono a "nessuna risposta"): non si spendono 60 minuti su un candidato mediocre.

---

## 5. Misurazione e criteri di decisione

Il v2 è un esperimento con soglie decise **prima**:

- **Obiettivo:** 3-5 risposte (anche solo curiose) → si riattiva la routine volume (`daily`) col formato v2.
- **Campione minimo:** 10 DM v2 con immagini prima di trarre conclusioni.
- **Se 10 DM v2 → 0 risposte:** il problema è più a monte del messaggio — fermarsi e sistemare il profilo IG come landing page (bio, Reel pinnato, highlight Lookbook — consiglio #6 del briefing 02/07) prima di inviarne altri. Un DM con immagini forti muore comunque se il profilo dietro dice "account vuoto".
- **Tracciare nel tracker** quale formato ha ricevuto ogni brand (v1 link / v2 immagini), così i numeri dei due formati restano confrontabili.

---

## 6. Regole sempre valide (ereditate dal v1, restano)

- Mai aprire con "ho visto [nome brand]" — dritti all'osservazione specifica, che deve essere **vera e verificabile**.
- Niente costruzioni analitiche da recensione ("quella silhouette che...") — reazione genuina.
- Prima parli di loro. Prezzo solo se rispondono.
- Max **un** follow-up (5-7 giorni), poi il brand si chiude.
- DM **dal profilo personale di Jacopo** (dato 05/07: da Jago vengono ignorati,
  dal profilo personale rispondono). Ci si presenta come "Jacopo, il creatore
  del progetto Jago" — Jago è il portfolio, non il mittente.
- Mix 70% IT / 30% EN.
- L'invio è **sempre manuale** — nessuna automazione su Instagram.
- Nei DM il video di riferimento, se serve, è il **Video #5 SCIROCCO** — mai il #6 (virale-broad, non demo del servizio). Ma nel v2 il video è opzionale: le immagini sono la proof.
