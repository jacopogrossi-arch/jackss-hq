---
name: cartamodelli-stato
description: Stato attuale del tool Generatore di Carta Modelli — aggiornamenti recenti e architettura
metadata:
  type: project
---

# Cartamodelli — Stato Progetto

Tool web (`cartamodelli/tool.html`) che genera carta modelli SVG stampabili in scala 1:1.
Usa Claude API con Metodo Müller per modellistica tecnica maschile.

## File del progetto

- `cartamodelli/tool.html` — interfaccia + logica principale (tutto in un file HTML)
- `cartamodelli/system-prompt.md` — system prompt per Claude API (fonte di verità per le costruzioni)

## Tipi di capo supportati

| Capo | Stato | Note |
|------|-------|-------|
| Jeans | ✅ Supportato | Funzionale dall'inizio |
| Pantaloni | ✅ Aggiunto 26/05/2026 | Commit `fe86e7f` |

## Aggiornamento del 26/05/2026 — Supporto Pantaloni (commit fe86e7f)

Cosa è stato aggiunto a `tool.html` (+360 righe):

- **Selettore tipo capo**: abilitato "Pantaloni" nel dropdown (prima era disabilitato)
- **Card "Opzioni pantalone"**: selettore pieghe (nessuna / 1 piega / 2 pieghe), visibile solo quando si seleziona Pantaloni
- **Funzione `buildPiecePromptsTrousers()`** con formule sartoriali Müller specifiche pantaloni:
  - Ease vita ridotta rispetto ai jeans (+5 mm vs +10 mm)
  - Volume posteriore extra aumentato (+20 mm vs +15 mm)
  - `pleat_mm` aggiunto alla larghezza pannello frontale per le pieghe
- **Pezzo 4**: cambiato da "tasca posteriore jeans" a "tasca a bocca (welt pocket) con fondo" per i pantaloni
- **Progress bar**: etichette ora dinamiche (non hardcoded sui nomi jeans)
- **Nome file download**: ora usa "pantaloni" o "jeans" in base alla selezione

## Fogli SVG generati (4 per capo)

| Foglio | Formato |
|--------|---------|
| Davanti | 594 mm × altezza variabile |
| Dietro | 594 mm × altezza variabile |
| Cintura | A3 orizzontale (420 × 297 mm) |
| Tasca posteriore | A4 (297 × 210 mm) |

**Scala**: 1 unità SVG = 0,1 mm → stampa 1:1 senza ridimensionare.
**Margini cucitura**: 15 mm già inclusi.

## Input richiesti

### Misure corporee (in mm)
- Giro vita, Giro fianchi, Giro coscia
- Lunghezza pantaloni, Profondità cavallo

### Brief creativo
- **Silhouette**: Ultra-slim / Slim / Regular / Relaxed / Baggy
- **Slider Vita** (0–10): altezza vita
- **Slider Gamba** (0–10): conicità
- **Slider Cavallo** (0–10): alza/abbassa cavallo

## Come si usa

1. Aprire `tool.html` nel browser
2. Inserire misure e scegliere silhouette/slider
3. Cliccare **Genera** → Claude API restituisce i 4 SVG
4. Scaricare e stampare 1:1
