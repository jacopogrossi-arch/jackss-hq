# Video #2 — montaggio (stato 21/10/2026)

File di lavoro in `videos/02-claude-collezione/` (fuori da git: file enormi). Qui solo il registro delle decisioni.

## Girato e taglio
- DJI Osmo Pocket 4P, **D-Log2**, 12 clip 4K HEVC 10 bit (9 DJI + 3 export DJI Mimo dal telefono, anch'essi D-Log2). LUT ufficiali DJI in `.claude/skills/youtube-edit/assets/luts/` (usata: `DJI-Pocket4P-DLog2-to-Rec709-size65.cube`).
- Taglio 9:33 -> 6:43 con `apply-cut.py --lut ... --encoder nvenc --vf <grading>` (taglio + colore in un solo ricodificamento, ~20 min).
- **Grading scelto: B (leggero)**: `curves=all='0/0 0.25/0.22 0.5/0.5 0.75/0.78 1/0.95',eq=saturation=1.08:contrast=1.04` (solo sul viso).
- Frasi che il taglio automatico aveva sbagliato e sono state corrette a mano: "ha fatto molto bene..." (rimessa), inizio di "bisogna saperla implementare", prese ripetute.

## Note di Jacopo (Notion "COMMENTO VIDEO 2") e come sono state applicate
Suono su ogni testo/capitolo/mossa di camera (motore: `sub_cues`); riser + glow + zoom nel gancio; capitoli piu' grandi col click; scena richieste con movimento (build + pillole + pagina di concept); typewriter su "Non capiva i titoli"; scena Claude+Canva e Claude+Chrome+Pinterest come UNA scena continua con camera che si muove; etichette del figurino in Playfair Display Italic; liste "fatto bene/male" nello stesso stile con colori opposti; piu' transizioni (light leak/film burn, ~1 ogni 40 s); musica lo-fi (lofi-02) piu' presente. Regole salvate in `presets/elegante-portfolio/README.md` e `SKILL.md`.

## Prossimi passi
1. Controllo completo a 1080p (bozza `lab/draft-1080p`), da guardare prima del 4K.
2. Render 4K (~65 min) solo dopo il via libera di Jacopo; poi remux BT.709, loudnorm -14 LUFS, musica lofi-02 (-11 dB), `verify-render.py`.
3. Miniatura, titolo/descrizione/tag in `02-pubblicazione.md`.
