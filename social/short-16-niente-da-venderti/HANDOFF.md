# HANDOFF: Short #16 «Non ho niente da venderti» (idea 16)
*20/11/2026. Copione, scena (banco di mercato all'alba) e chiamata finale approvati da Jacopo («va bene tutto»). Non pubblicare: lo fa lui.*

## Stato
- Voce: 5 paragrafi eleven_v4 "Jacopo Prova" (~510 crediti, 1 take ciascuno), uniti con pause 0,45 s: `videos/_bench/short-16/vo/vo.mp3` (36,7 s, locale). words.json corretto a mano (prio->primo, I->AI) e jaw.json in `v1/`.
- Narratore: `videos/_bench/short-16/assets/narratore-perf-smooth.glb` (blender_perf -> prepare_rig -> smooth_anim).
- Scena `v1/room.py` (piazza all'alba, banco con tendone a strisce) + regia `v1/build.py` + `v1/mix.py` (musica Epidemic "Happiest Moment") + `v1/run.sh draft`.
- Bozza 1080p 30 fps: `videos/_bench/short-16/renders/draft.mp4` (39 s), leggera `bozza-leggera.mp4` mandata a Jacopo. Revisione a 10 fps fatta (2 giri): corretti colori (campioni piu lontani), etichette sopra la testa del narratore, close-up su «il laboratorio», finale con push-in e chiusura sul narratore.
- Contatore: «in vendita 0 · documentato N» (N sale con colori, pantalone, errori, costi).

## Da fare
1. Aspettare OK/correzioni di Jacopo sulla bozza.
2. 4K: `render --resolution portrait-4k --gpu --video-bitrate 60M --fps 60` (vedi SOP), poi iCloud › Video 3D moda › short-16-niente-da-venderti-v1.mp4.
3. `pubblicazione.md` (titolo + descrizione, max 5 hashtag, video correlato #4), Notion (Jackss HQ), memoria project_shorts_3d.
