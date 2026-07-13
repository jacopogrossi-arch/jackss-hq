# Routine Outreach — Setup (da fare quando sei a casa)

> Tutto è già pronto e testato (12/06/2026). Manca solo creare la **Routine** sul web:
> serve farlo dal browser perché dentro una sessione Claude Code il comando è disattivato.
> Tempo richiesto: ~2 minuti.

---

## I 5 passi

1. Vai su **claude.ai/code/routines** → **New routine**
2. **Nome:** `Outreach Jago — 5 brand al giorno`
3. **Prompt** (copia-incolla esatto):
   ```
   Esegui lo skill /outreach daily per il personal brand Jago.
   Trova 5 nuovi micro-brand Tier A, qualificali sui 6 criteri di
   personal-brand/outreach.md, scrivili sia in outreach.md sia nel
   database Notion "Brand candidati — Outreach Jago"
   (data_source_id d5a4d66b-f04c-40f2-a13b-76d1b2469f5a) con
   Stato DM = "Da contattare". Niente duplicati. Se non trovi 5 brand
   veri, aggiungine meno e dillo. Non inviare DM.
   ```
4. **Repository:** `jacopogrossi-arch/jackss-hq` · **Trigger:** *Schedule → Daily* + ora (es. 8:00)
5. **Create** → premi **Run now** per il primo giro

## ⚠️ I 2 setting da non dimenticare

- **Connettore Notion** incluso (serve per scrivere nel database) — di default c'è già.
- **Network access → Full** nelle impostazioni ambiente della routine.
  Senza, la ricerca brand sul web non funziona (il "Trusted" di default blocca i siti di moda).

---

## Cosa è già fatto (non serve rifarlo)

- ✅ Skill `/outreach` su `master` — comandi: `daily`, `trova N`, `scrivi DM [brand] [--en]`, `tracker`, `follow-up`
- ✅ Database Notion **"Brand candidati — Outreach Jago"** (sotto la pagina Strategia)
- ✅ 12 brand Tier B + 5 Tier A già caricati (test del 12/06/2026)
- ✅ `outreach.md` aggiornato (Video #3 online → DM operativi)

## Come si usa, ogni giorno

1. La routine (o `/outreach daily` a mano) aggiunge 5 brand Tier A nel database Notion
2. Apri Notion → per ogni brand fai il check umano da 30 sec su Instagram
   (follower 1k-50k? feed con visual deboli? collezione in arrivo?) — sono i campi *(da verificare)*
3. Per i brand buoni: `/outreach scrivi DM [brand]` → ti preparo il messaggio da incollare
4. Mandi il DM a mano da **@jagoworks**, firmato Jacopo, e aggiorni `Stato DM` in Notion

## Nota onesta sullo scraping Instagram

Non automatizzabile: IG blocca le richieste (403) e violarlo rischia il ban di @jagoworks.
Per questo il check IG resta umano — è anche il punto dove il tuo occhio vale più di un bot.
