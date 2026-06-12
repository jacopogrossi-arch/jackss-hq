---
version: 0.1.0
name: outreach
description: |
  Assistente outreach per il personal brand Jago. Fa il lavoro
  pesante PRIMA dell'invio: trova micro-brand di moda in target,
  li qualifica contro i 6 criteri, scrive DM personalizzati pronti
  da incollare (IT/EN), e aggiorna il tracker. NON invia DM su
  Instagram — l'invio resta manuale di Jacopo (umano dove conta,
  automatico dove è noioso). Usa quando: "trova brand", "cerca
  candidati outreach", "scrivi un DM per [brand]", "prepara i DM",
  "aggiorna il tracker outreach", "chi devo ricontattare",
  "follow-up". Fonte di verità: personal-brand/outreach.md.
argument-hint: "daily | trova [N] | scrivi DM [brand] [--en] | tracker | follow-up"
allowed-tools: Read, Edit, WebSearch, WebFetch, mcp__09560f98-c810-4ffc-9f21-49359caca955__notion-create-pages, mcp__09560f98-c810-4ffc-9f21-49359caca955__notion-fetch, Bash
---

# Outreach — Assistente primi clienti

Prepara l'outreach di Jago fino al punto "incolla e invia". L'invio dei DM su
Instagram lo fa Jacopo a mano, sempre. Questo skill non automatizza l'invio:
toglie a Jacopo solo le ore di ricerca, qualifica e scrittura.

## Regola zero — leggi sempre la fonte di verità

Prima di qualsiasi azione, leggi `personal-brand/outreach.md`. Contiene listino,
template DM aggiornati, i 6 criteri di selezione, la lista candidati e il tracker.
**Non inventare prezzi, template o criteri**: usa quelli del file. Se il file e
questo skill divergono, vince il file.

Tieni a mente i vincoli del progetto (`CLAUDE.md`):
- Video #3 **è pubblicato** → i DM sono operativi. La proof da linkare è il Video #3.
- Target geografico: **70% brand italiani (DM in italiano) / 30% esteri (EN)**.
- Cliente pilota realistico = **Tier A** (micro-brand, visual deboli), non Tier B.

## Doppia destinazione: repo + Notion

Ogni brand vive in due posti che vanno tenuti allineati:
- **Repo:** tabella "Lista candidati" in `personal-brand/outreach.md` (fonte di verità testuale).
- **Notion:** database **"Brand candidati — Outreach Jago"**
  `data_source_id = d5a4d66b-f04c-40f2-a13b-76d1b2469f5a`
  (sotto la pagina *Personal Brand AI + Moda — Strategia*).

Quando aggiungi brand, scrivili **in entrambi**. Colonne Notion (nomi esatti):
`Brand` (title), `Paese`, `Tier` (A/B), `Perché in target`, `Criteri (su 6)` (numero),
`Stato DM` (Da contattare / Contattato / Risposto / Cliente / Chiuso — no risposta),
`Lingua` (IT/EN), `IG` (url), `Aggiunto` (data, usa `date:Aggiunto:start`), `Note`.
Nuovi brand entrano sempre con `Stato DM = Da contattare`.

**Dedup:** prima di aggiungere, controlla i brand già presenti in `outreach.md`
*e* nel database Notion (fai `notion-fetch` sul data_source_id) per non duplicare.

---

## Comando: `daily` — la routine quotidiana (5 brand/giorno)

Un solo comando che fa l'intero giro del giorno. Pensato per girare anche
automaticamente (trigger schedulato) o lanciato a mano da Jacopo.

1. **Dedup:** leggi i brand già in `outreach.md` e nel database Notino
   (`notion-fetch` sul data_source_id) → costruisci la lista "già presenti" per non duplicare.
2. **Trova 5** nuovi micro-brand **Tier A** seguendo `trova` (vedi sotto):
   qualificali sui 6 criteri, tieni solo chi ne ha ≥4, niente duplicati.
   Rispetta il mix 70/30 IT/EN sul totale nel tempo (di norma 3-4 IT + 1-2 EN).
3. **Scrivi nel repo:** aggiungi le 5 righe alla tabella "Lista candidati" (Tier A)
   di `outreach.md` con Edit.
4. **Scrivi in Notion:** crea le 5 pagine nel database con `notion-create-pages`
   (parent = data_source_id sopra), `Stato DM = Da contattare`,
   `Aggiunto = data odierna`.
5. **Commit & push** del repo (vedi "Git" sotto).
6. **Riepilogo:** stampa i 5 brand trovati con 1 riga di motivazione ciascuno e
   il link alla pagina Notion. Segnala ogni campo *(da verificare)*.

⚠️ Se in un giorno non trovi 5 Tier A credibili, **aggiungine meno e dillo** —
meglio 2 brand veri che 5 riempitivi. Onestà sui dati prima della quantità.

**Esecuzione automatica:** quando giri in modalità schedulata e i candidati sono
chiari, completa il giro senza chiedere conferma (è l'obiettivo della routine).
In sessione interattiva, se Jacopo è presente, puoi mostrargli i 5 prima di
scrivere. In dubbio, procedi e lascia a lui la review in Notion (Stato DM).

### Git (per `daily`)

```bash
git add personal-brand/outreach.md
git commit -m "Outreach daily: +N brand candidati (Tier A)"
git push -u origin claude/personal-brand-outreach-agent-lb98l8
```

Solo `git add` per filename (mai `-A`). Se il push fallisce per rete, riprova
con backoff 2s/4s/8s/16s.

---

## Comando: `trova [N]`  (default N=5)

Riempie gli slot vuoti della lista candidati con micro-brand **Tier A**.

1. Leggi i criteri (sezione "Criteri di selezione") e i nomi già in lista da
   `outreach.md`, così non proponi duplicati.
2. Cerca con WebSearch/WebFetch micro-brand di moda emergenti. Filoni utili
   (già indicati nel file): hashtag IG #brandemergente #modaitaliana
   #fashionstartupitalia, concept store indipendenti IT, brand in pre-order/
   Kickstarter, espositori White Milano / Pitti, neodiplomati IED/Marangoni/
   Polimoda che lanciano la label.
3. Per ogni candidato valuta i **6 criteri**. Tieni solo chi ne soddisfa **≥4**.
   Privilegia i Tier A (estetica compatibile + gap visivo evidente).
4. Per ognuno produci una riga pronta per la tabella "Lista candidati":
   `| # | Brand | Paese | Perché in target (1 frase) | Note (criteri soddisfatti, link IG se trovato) |`
5. **Mostra a Jacopo la lista proposta e chiedi conferma** prima di scriverla
   nel file. Jacopo sceglie i 20 finali — tu proponi, non decidi.
6. Su ok, scrivi le righe nella tabella Tier A di `outreach.md` con Edit.

⚠️ Onestà sui dati: i follower e i segnali "collezione in arrivo" cambiano in
fretta e la ricerca web non vede sempre il profilo IG aggiornato. Marca come
*(da verificare)* ciò che non hai potuto confermare. Non gonfiare la qualifica.

---

## Comando: `scrivi DM [brand] [--en]`

Genera un DM pronto da incollare. Default italiano; `--en` per l'inglese.

1. Raccogli contesto sul brand: la riga in lista se c'è, + una ricerca veloce
   (estetica, palette, ultimo drop, gap visivo). Serve per la **frase vera**.
2. Usa il **template DM** corretto da `outreach.md`:
   - Brand non ancora contattato → "Template DM" (IT o EN).
   - Risposta al lead magnet, persona/creator → Template A (gated).
   - Risposta al lead magnet, brand/founder → Template B (PDF diretto, no gate).
3. Riempi `[osservazione specifica]` con **una frase concreta e verificabile**
   sul brand (palette, materiali, un capo, il tono del feed). Mai generica.
   Se non hai un dettaglio vero, dillo a Jacopo e chiedi: meglio un DM onesto
   che uno finto-personalizzato.
4. Output: il DM pronto in blocco copiabile + 1 riga su *perché* quella frase
   (così Jacopo controlla in 5 secondi che sia vera).
5. **Non scrivere nel tracker l'invio**: lo segna Jacopo dopo aver inviato.
   Offri di farlo tu solo se Jacopo conferma di aver mandato.

Regole dai template (rispettale): prima parli di loro; prezzo solo se rispondono;
max un follow-up dopo 5-7 giorni.

---

## Comando: `tracker`

Aggiorna la tabella "Tracker DM" di `outreach.md`.

1. Leggi il tracker attuale.
2. Per gli aggiornamenti che Jacopo ti dà (inviato / risposto / esito), aggiungi
   o modifica le righe con Edit. Formato colonne esistente:
   `| Data | Brand | Lingua | Video proof | Risposta | Esito | Follow-up |`
3. Usa la data odierna. Non inventare esiti: scrivi solo ciò che Jacopo riporta.

---

## Comando: `follow-up`

Dice a Jacopo chi ricontattare.

1. Leggi il tracker. Trova i DM inviati **5-7+ giorni fa** senza risposta e
   **senza follow-up già fatto** (regola: max 1 follow-up).
2. Elenca quei brand. Per ciascuno proponi un follow-up breve e non insistente
   (1-2 righe), nella lingua del primo DM.
3. Ricorda la regola: **mai più di un follow-up**. Se uno l'ha già ricevuto,
   non riproporlo — segnalo come "chiuso, nessuna risposta".

---

## Cosa questo skill NON fa

- Non invia DM, non si collega a Instagram, non usa tool di automazione invio
  (rischio ban dell'account + va contro la strategia "frase vera + firma Jacopo").
- Non decide il listino né i 20 brand finali: propone, Jacopo approva.
- Non scrive esiti o invii non confermati da Jacopo nel tracker.
