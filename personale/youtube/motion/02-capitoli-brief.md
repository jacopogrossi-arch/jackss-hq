# Brief — scena "Capitoli" (video #2, parte 2) · v3

```
ROLE: You are the director, motion designer, composer and sound designer.

PRODUCT/STORY: Scene 2 of the YouTube video "Ho lasciato Claude ideare una collezione
al posto mio" (Jacopo, fashion student in Rome, building the menswear brand Inverso).
Hook: "Four steps. Who did what." It tells the viewer how the video is organised:
01 Brainstorming · 02 Impaginazione · 03 Disegno · 04 Presentazione.
Audience: 18–30, into fashion, AI, creative work, students.
Feeling: cinematic, confident, crafted by hand — not tech, not corporate.

BANNED: centered text, default gradients, generic fade-ins, small spaced-caps labels
above titles, thin rules under titles, Canva-style colour bands, tilted cards with drop
shadows, blue/neon "AI tech" look, slide bullet lists, icons, emoji.

PALETTE: #0E0D0C (warm black) · #F2F2F0 (off-white) · #E8692B (orange, keyword only)
· #BFA58F (plaster) · #6A6668 (grey)

TYPE: EB Garamond Italic (keywords, big) + Inter Tight 800 (numbers, structure words).
Asymmetric layout on a 12-column grid: text lives in the left or right third, never in
the middle; max 3 words on screen at once.

MOTION: expo-out "snap" easing (fast in, long settle); reveals = per-word mask wipe +
blur-to-sharp; whip pans with motion blur between chapters; slow continuous 3D camera
dolly through layered depth (parallax, depth of field). Pacing locked to the voice,
one beat ≈ 0.6 s.

TEXTURE: animated film grain (changes every frame), vignette, soft glow on orange only,
warm light leak from the left (Roman chiaroscuro), depth-of-field blur on far layers.
No scanlines.

STRUCTURE: see storyboard below (≈ 11 s, timings to resync on the real voice take).

AUDIO: generated in code. Low warm drone pad (D minor) under everything; filtered-noise
whoosh on each whip pan; soft low hit when each chapter number lands; small ticks when
the ideas fade; short riser into the last chapter; clean cut to silence at the end.
Music bed around -22 dB under the voice, SFX peaks around -12 dB.

GATE: Show the storyboard first and wait for approval.

DELIVERY: ≈ 11 s, 1920×1080, 30 fps, H.264. Two files: with audio and without
(so the sound can be remixed in DaVinci). Output: personale/youtube/motion/02-capitoli-v3.mp4
```

## Storyboard (in attesa di approvazione)

Voce di riferimento (dallo script): *"Prima di entrare nei dettagli ti dico come è fatto il video. Primo: il brainstorming. Secondo: l'impaginazione. Terzo: il disegno. E alla fine la presentazione."*

| # | Tempo | Cosa si vede | Suono |
|---|---|---|---|
| 1 | 0,0 – 1,4 | Buio caldo con grana. Una luce entra da sinistra. Nel terzo sinistro compare *quattro* in Garamond corsivo enorme, da sfocato a nitido; sotto, piccolo in Inter, "passaggi". La camera avanza piano. | drone che sale dal silenzio |
| 2 | 1,4 – 3,6 | **Whip pan** a destra con scia. Siamo dentro una nuvola di frasi vere delle idee di Claude ("Fuori dal feed, dentro la città", "Il rovescio non si posta", "Una, non sei"…), sospese a profondità diverse, quasi tutte sfocate. In primo piano a destra: **01** in Inter + *Brainstorming* in corsivo. Poi 27 frasi si spengono e cadono nel buio, 3 restano accese in arancio. | whoosh · colpo basso sul "01" · tick sulle frasi che si spengono |
| 3 | 3,6 – 5,8 | Whip pan. Pezzi di una tavola (foto, campioni di colore, figurino) volano da direzioni diverse e si incastrano in una griglia, uno per battuta, con uno scatto. Testo nel terzo sinistro: **02** *Impaginazione*. | whoosh · piccoli colpi secchi a ogni incastro |
| 4 | 5,8 – 8,0 | Macro su un flat in bianco e nero: la linea si rivela con una maschera che la "disegna", poi il colore riempie il figurino da sotto. Testo a destra: **03** *Disegno*. | whoosh · riser leggero |
| 5 | 8,0 – 10,2 | Il figurino finito sospeso nello spazio, una lama di luce lo attraversa, glow leggero. Testo a sinistra: **04** *Presentazione*. La camera si allontana e mostra le quattro scene come pannelli in profondità. | colpo pieno all'arrivo · coda del drone |
| 6 | 10,2 – 11,0 | I quattro numeri restano in fila in basso a sinistra, poi taglio netto al nero. | silenzio netto |

**Asset:** frasi reali da `accademia/idee-concept-trend-ai-2027-28.md`. Per ora flat e figurino sono di **After Hours** (segnaposto); nel definitivo vanno quelli del tema onlife.

**Fattibilità:** 3D con prospettiva CSS, motion blur fondendo più sotto-fotogrammi, audio sintetizzato in Python e unito con ffmpeg. Render stimato: alcuni minuti.
