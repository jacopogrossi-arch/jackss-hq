# HANDOFF: Short #16 «Non ho niente da venderti» (idea 16)
*20/11/2026. Copione, scena (banco di mercato all'alba) e chiamata finale approvati da Jacopo («va bene tutto»). Non pubblicare: lo fa lui.*

## Stato
- Voce: 5 paragrafi eleven_v4 "Jacopo Prova" (~510 crediti, 1 take ciascuno), uniti con pause 0,45 s: `videos/_bench/short-16/vo/vo.mp3` (36,7 s, locale). words.json corretto a mano (prio->primo, I->AI) e jaw.json in `v1/`.
- Narratore: `videos/_bench/short-16/assets/narratore-perf-smooth.glb` (blender_perf -> prepare_rig -> smooth_anim).
- v1 BOCCIATA da Jacopo («camera storta, mai centrata, card sbagliate, pantalone glitchato»). v2 rifatta da capo nella stessa cartella `v1/`:
  - `room.py`: banco frontale e simmetrico, telo scuro dietro (contrasto), filo sotto la tenda per le card, due piedistalli (pantalone a sinistra, quaderno a destra).
  - `build.py`: camera sempre in asse e in bolla (assert in `_flush`), controllo automatico `_layout_check` (card dentro il quadro e sotto i sottotitoli, fascia mai sotto i testi), card = fatti con fonte in `script.md`, una card alla volta su «ogni strumento/costo/errore», fascia INVERSO solo su «Inverso» e su «apro il brand» (sparisce su «fino ad allora»), cartello IN VENDITA -> IN CORSO sul secondo «documento».
  - Motore: `world3d.js` ora mostra il sottotitolo chiaro sulle card neutre con ink chiaro e il bordo (border=) anche senza badge.
- Bozza v2: `videos/_bench/short-16/renders/draft.mp4`, leggera `bozza-leggera-v2.mp4` mandata a Jacopo. Controllata a piena risoluzione (fine di ogni movimento, comparsa del pantalone a 10 fps) e fogli 10 fps.
- Pillola: «in vendita: 0» -> «in vendita: 0 · in corso: tutto».

## Da fare
1. Aspettare OK/correzioni di Jacopo sulla bozza v2.
2. 4K: `render --resolution portrait-4k --gpu --video-bitrate 60M --fps 60` (vedi SOP), poi iCloud › Video 3D moda › short-16-niente-da-venderti-v1.mp4.
3. `pubblicazione.md` (titolo + descrizione, max 5 hashtag, video correlato #4), Notion (Jackss HQ), memoria project_shorts_3d.
