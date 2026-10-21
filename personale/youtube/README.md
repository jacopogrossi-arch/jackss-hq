# Canale YouTube personale

Video lunghi sul **canale personale** di Jacopo (non Inverso, non Jago).

## Video pubblicati

| # | Titolo | Pubblicato | File |
|---|---|---|---|
| 1 | Si può usare l'AI nella moda? | 15/10/2026 | copione `01-ai-accademia-moda.md` · titolo/descrizione/tag `01-pubblicazione.md` · miniatura `miniatura/miniatura-v3.jpg` |
| 2 | Ho lasciato Claude ideare una collezione al posto mio | **21/10/2026** · [link](https://youtu.be/KySnU629RFk) | script `02-claude-idea-collezione.md` · montaggio `02-montaggio.md` · titolo/descrizione/tag `02-pubblicazione.md` · miniatura `miniatura/miniatura-02-v2.jpg` |

## Metodo (dal video 1, da riusare)

**Copione.** Hook a camera *autentico*: chi sono → cosa ho fatto → cosa è successo (es. la frase di un collega) → la domanda. Non a memoria: si ricordano i 4 passaggi e si dice con parole proprie, 3 prese, si tiene la più naturale.

**Ripresa.** DJI Osmo Nano in **D-Log M**. Luce di finestra frontale/laterale, camera all'altezza degli occhi, sfondo con oggetti propri (manichino, macchina, tavole).

**Montaggio — DaVinci Resolve (gratuito, Windows):**
1. *Edit*: taglio grezzo (`Ctrl+B` taglia, `Shift+Canc` elimina chiudendo il buco), poi B-roll su V2 con Dynamic Zoom, zoom 1.15 alternato sui jump cut, titoli Text+ su V3.
2. *Color*: LUT DJI **D-Log M → Rec.709** (da dji.com → Osmo Nano → Download; installata da Project Settings → Color Management → Open LUT Folder → Update Lists). Nodo 01 = correzioni (esposizione, Temp/Tint), nodo 02 = LUT (`Alt+S`). Si copia su tutte le clip a camera con `Ctrl+C` / `Ctrl+V`. **Mai sul B-roll.**
3. *Audio*: voce normalizzata a **-16 LUFS** (tasto destro → Normalize Audio Levels, ITU-R BS.1770). Musica dalla **YouTube Audio Library** (attribuzione non richiesta) su A2 a circa **-22 dB**, dissolvenze in entrata/uscita, abbassata o tolta nella parte personale/etica (keyframe con `Alt+clic` sulla linea del volume).
4. *Deliver*: preset YouTube, MP4 H.264, risoluzione di ripresa (4K se girato in 4K), bitrate 40.000 Kb/s (1080p) / 80.000 (4K), audio AAC 320.

**Miniatura.** Stile "virale clean": fondo chiaro grigio-bianco (#F2F2F0), faccia grande a sinistra con contorno bianco, UN oggetto grande al centro, 2 parole. Generata in ChatGPT con i nostri asset e **senza testo** (ChatGPT sbaglia i font e gli accenti); il titolo si aggiunge dopo in **EB Garamond** (corsivo + tondo). Prompt e versioni scartate in `miniatura/prompt-chatgpt-miniatura.md`. Controllare sempre l'anteprima a 320×180. **Anche logo e frecce si aggiungono dopo** (ChatGPT sbaglia i loghi): HTML + Edge headless `--screenshot` (metodo del #2, sorgente `miniatura/miniatura-v6-sorgente.html`).

**Pubblicazione.** Titolo = domanda; miniatura = parola che la completa, non la ripete. Descrizione: prima riga chi sono + cosa è successo, domanda per i commenti, capitoli (il primo a 0:00), @thejacopogrossi, riga su @inversorome.
