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
