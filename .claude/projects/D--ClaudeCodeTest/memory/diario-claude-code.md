---
name: diario-claude-code
description: Log delle sessioni di lavoro recenti con Claude Code (sincronizzato da Notion)
metadata:
  type: reference
---

# Diario Claude Code — Sessioni Recenti

Fonte: https://www.notion.so/36c30837a9e6811dbf67e5e19d5faa0f
Aggiornato automaticamente ogni sera dall'agente Claude Code.

---

## 12/06/2026

### ✅ Agente outreach automatico (personal brand Jago)

**[Personal Brand] Creato skill `/outreach` + routine daily** — branch poi mergiato su `master`
- Skill `.agents/skills/outreach/SKILL.md` con comandi: `daily` (5 brand/giorno), `trova N`, `scrivi DM [brand] [--en]`, `tracker`, `follow-up`
- Principio di design: l'agente fa **prep** (trova + qualifica + scrive DM + tracker); l'invio DM resta **manuale di Jacopo** (no automazione IG → rischio ban @jagoworks + preserva la "frase vera")
- Doppia destinazione tenuta allineata: `personal-brand/outreach.md` (repo) + database Notion
- Merge diretto su `master` autorizzato da Jacopo (commit `d302b4c`)

**[Notion] Creato database "Brand candidati — Outreach Jago"** — sotto pagina *Personal Brand AI + Moda — Strategia*
- `data_source_id = d5a4d66b-f04c-40f2-a13b-76d1b2469f5a`
- Colonne: Brand, Paese, Tier (A/B), Perché in target, Criteri (su 6), Stato DM, Lingua (IT/EN), IG, Aggiunto, Note
- Popolato: 12 brand Tier B (migrati da outreach.md) + 5 Tier A (test routine: MTL Studio, Alchètipo, ES'GIVIEN, Yali, P. Andrade)

**[Onestà tecnica] Scraping Instagram = non fattibile** — IG risponde 403, no API pubblica di discovery, violazione ToS = ban. Il check IG (follower/feed/drop) resta umano, 30 sec a brand.

### ⏳ In sospeso (Jacopo, da casa)
- **Creare la Routine** su claude.ai/code/routines per l'esecuzione daily automatica.
  Istruzioni complete in `personal-brand/outreach-routine-SETUP.md` (prompt pronto + 2 setting: connettore Notion + Network access Full).

---

## 26/05/2026

### ✅ Attività svolte

**[Cartamodelli] Aggiunto supporto ai Pantaloni nel tool HTML** — Commit `fe86e7f` (ore 18:40)
- Abilitato tipo capo "Pantaloni" nel selettore
- Card "Opzioni pantalone" con selettore pieghe (nessuna / 1 piega / 2 pieghe)
- Funzione `buildPiecePromptsTrousers()` con formule Müller pantaloni:
  - Ease vita: +5 mm (vs +10 mm dei jeans)
  - Volume posteriore: +20 mm (vs +15 mm)
  - `pleat_mm` per le pieghe nel pannello frontale
- Pezzo 4: "tasca a bocca (welt pocket) con fondo" per pantaloni
- Progress bar con etichette dinamiche
- Nome file download adattivo ("pantaloni" / "jeans")
- +360 righe aggiunte a `cartamodelli/tool.html`

**[Repo] Pulizia CLAUDE.md** — Commit `bb7336b` (ore 19:36)
- Rimossi dettagli dei singoli progetti da CLAUDE.md (gestiti nei file dedicati del repo)
- Rimossa sezione "Daily Log Agent"
- Ridotto da 147 righe a 7

---

*Le sessioni precedenti al 26/05/2026 non sono disponibili nel diario Notion al momento della sincronizzazione.*
