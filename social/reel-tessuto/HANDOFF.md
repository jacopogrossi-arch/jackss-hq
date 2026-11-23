# HANDOFF — Reel «Il tessuto non torna indietro» (23/11/2026)

Ricerca: `.claude/skills/fashion-3d/references/research-reel-retention-2026-11-23.md`. Copione e mappa: `script.md`. Metodo: gemello (`social/gemello/`), Blender only.

## Stato (23/11)
- Voce FATTA: eleven_v4 "Jacopo Prova", 4 paragrafi, 200 crediti, 1 take ciascuno → `videos/_bench/reel-tessuto/vo/` (p1-p4, `vo.wav` montata 16.0 s con pause 0.50/0.55/0.60 s; locale). Tempi parole Whisper in `words.json`.
- Labiale: P3 («Poi prendi il metro, e misuri due volte», 8.2-11.0 s) scritto A MANO sull'inviluppo in dB (`score.py` LIPS_P3). P1, P2, P4 = bozza automatica `lips_auto.json` (`social/gemello/lips_draft.py`): NON ancora a mano, ha nuclei sbagliati. Da rifare con lo stesso metodo (stampa dB a 10 ms, 5 dB per cifra, 0.5 s per riga, chiusure m/b/p una per una).
- `social/gemello/reel.py` = twin.py + partitura esterna (`--score score.py`: DUR, VO, LIPS, STRESS, SHOTS, tracce gesti) e UNA camera per inquadratura (taglio netto, niente sbavatura del motion blur). Shakify per camera con offset diverso.
- Clip di prova FATTA e inviata a Jacopo: finestra 8.0-11.0 s (fotogrammi 193-265, 1080x1920, 48 campioni), `videos/_bench/reel-tessuto/prova1.mp4` (master), `prova1-telefono.mp4`, `prova1-labiale.mp4`, foglio `prova1-sheet.jpg`. Contiene 2 tagli (s4 medio -> s5 primo piano viso su «metro» -> s6 medio stretto). Iterazioni: s5 prima macro sul rotolo (illeggibile), poi taglio sul gesto (decentrato, perspettiva deformata), infine primo piano viso 65 mm. Gesti: la mano destra indica (indice dritto) ma nel medio stretto esce dal quadro a sinistra: da ricontrollare in s6.
- Punti deboli visti nella prova: bocca piccola nei medi (valutare mw0 piu' alto), brows poco visibili, mano che indica tagliata fuori.

## Da fare (in ordine)
1. Risposta di Jacopo alla clip di prova (labiale, taglio, gesti, voce).
2. Labiale a mano di P1, P2, P4.
3. Macro sulla carta (s3, 5.2-6.6 s): oggi foglio bianco = buco di retention. Aggiungere un disegno tecnico del pantalone che si traccia (curva con bevel_factor_end animato) e la matita che segue lo stesso percorso; oppure sostituire con taglio di scala come s5.
4. Plate «€0» su «zero» e «×2» su «due volte» (post in ffmpeg), swish sui tagli (Epidemic, locale).
5. Render completo: 385 fotogrammi, circa 7 s l'uno a 1080x1920 e 48 campioni = ~45-50 min (inquadrature macro più veloci).
6. Audio finale: voce + swish, niente musica o letto sotto -26 LUFS; master loudnorm -14.

## Trappole
- Blender in background: lanciare `blender -b -P ...` come comando in background del tool, NON con `nohup ... &` (il processo muore con la shell: restano pochi fotogrammi).
- Percorsi di uscita sempre assoluti `D:/...`.
- 40 campioni o meno: mosaico sulla texture/volume, non giudicare l'immagine; i still di controllo a 16-24 campioni servono solo per posa e inquadratura.
- Macro sul metro: il rotolo è un cilindro liscio e la coda con le tacche sta sotto il foglio; un taglio vicino (<0.3 m) deforma la prospettiva. Il taglio s5 è oggi un taglio di scala frontale 85 mm su mano e petto.
- Il tool voce dell'MCP non espone stability/seed; vedi dossier §6.
