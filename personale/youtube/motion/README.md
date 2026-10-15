# Motion graphics — canale YouTube

Grafiche animate costruite in codice (HTML/CSS/JS → fotogrammi con Chromium → MP4 con ffmpeg). Si mettono su DaVinci sopra la voce.

**Regola:** ogni scena parte da un brief compilato con la tabella qui sotto. **Prima lo storyboard, poi il render** (GATE).

## Tabella brief (da compilare per ogni scena)

```
ROLE: You are the director, motion designer, composer and sound designer.
PRODUCT/STORY: [what it is, one-line hook, audience, feeling]
BANNED: centered text, default gradients, generic fade-ins, [your pet hates]
PALETTE: [4-5 hex codes, nothing else]
TYPE: [headline font] + [body font], [layout rule]
MOTION: [easing style], [reveal style], [pacing]
TEXTURE: [grain, glow, scanlines, etc.]
STRUCTURE: [shot-by-shot with timestamps]
AUDIO: [music style, key moments, SFX], generated in code
GATE: Show the storyboard first and wait for approval.
DELIVERY: [length, resolution, fps, output path]
```

## Sistema fisso del canale (vale per tutte le scene, dal 15/10/2026)

- **Stile:** cinematografico alla Iman Gadzhi, adattato a Jacopo: spazio 3D scuro, testo a tempo con la voce, oggetti veri del lavoro sospesi nello spazio.
- **Palette:** `#0E0D0C` nero caldo · `#F2F2F0` bianco miniatura · `#E8692B` arancio (solo parola chiave) · `#BFA58F` intonaco · `#6A6668` grigio
- **Font:** EB Garamond corsivo (parole chiave) + Inter Tight 800 (numeri, parole di struttura)
- **Vietato sempre:** testo centrato, gradienti di default, dissolvenze generiche, etichette piccole in maiuscolo spaziato sopra i titoli, linee sottili sotto i titoli, fasce colorate e cartoncini inclinati "stile Canva", blu/neon "tech AI", elenchi puntati da slide, icone ed emoji.

## Timing sull'audio vero (dal 15/10/2026)

1. Jacopo finisce i tagli in DaVinci ed esporta **solo l'audio** della timeline (Deliver → spunta solo Audio → WAV o MP3).
2. Claude trascrive con i tempi parola per parola, oppure, se la trascrizione non è disponibile, usa i silenzi rilevati con ffmpeg e il copione. Ne esce una **tabella di timing**: tempo · frase detta · grafica.
3. Jacopo approva la tabella (GATE).
4. Ogni grafica viene renderizzata lunga esattamente quanto il suo pezzo, con il tempo d'inizio nel nome (es. `03m12s_capitoli.mp4`), così su DaVinci si trascina al punto giusto.

## Scene

| Scena | Brief | Stato |
|---|---|---|
| Capitoli (parte 2) | `02-capitoli-brief.md` | storyboard v3 in attesa di approvazione · v1 e v2 scartate (troppo "Claude" / troppo "Canva") |
