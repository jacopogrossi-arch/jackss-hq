# "Tre vite di un pantalone": video 3D di 1:30 sulla moda

*13/11/2026, notte. Fatto in autonomia da Claude su richiesta di Jacopo. Lo script è in `script.md`.*

## Dove sono i file (tutti locali, fuori da git)
Cartella `videos/_bench/video-3d-moda/`:
| File | Cosa |
|---|---|
| `FINAL-tre-vite-di-un-pantalone-4k.mp4` | il video, **3840×2160, 30 fps, 90 s**, voce + musica + effetti |
| `FINAL-tre-vite-di-un-pantalone-1080.mp4` | lo stesso in 1080p (più leggero da guardare) |
| `prove/` | le prove degli effetti nuovi: coppie Prima \| Dopo e `PROVE.md` che le spiega |
| `build.py`, `mix.py`, `words.json` | la scena (camera, wipe, etichette agganciate alle parole), il mix audio, i tempi delle parole |

## Il video
- **Idea:** un pantalone passa da *tre vite* prima di essere un capo: **disegno** (look a inchiostro = il flat tecnico), **volume** (argilla = la tela di prova), **materia** (finale = cotone drill sotto la luce di un atelier). Le tre vite sono i tre "pass" del nostro motore 3D: il video parla di moda e mostra il 3D allo stesso tempo.
- **Struttura:** gancio 0:00-0:18 (luce a strisce, titolo) → disegno → volume → materia (dettagli con profondità di campo) → "si sente" (rotazione completa e carrello basso) → finale con i tre pantaloni affiancati (inchiostro, argilla, finale) e la card "Inverso · Drop 1".
- **Una sola scena 3D continua** (formato 52 di `world3d`): la camera non stacca mai, le barre rosse portano da un look all'altro. Etichette avorio agganciate ai punti del capo, ognuna sulla sua parola.
- **Voce:** Epidemic Sound, **Edward** (britannico, calmo, autorevole), lingua `it`. **Musica:** "Steall Waters" (Luba Hilman, ambient, senza voce) con ducking sotto la voce. **Effetti:** 3 (due whoosh sui wipe, uno stoffa sulle entrate). Tutto scaricato solo in locale (`assets/*/licensed/`, ignorato da git), crediti in `assets/sfx/licensed/CREDITS.md`.
- **Parole e tempi:** la voce è stata trascritta con faster-whisper (`words.json`) e ogni grafica parte sulla sua parola. Misura (`scripts/qa-lag.py`): **0 su 16 grafiche partono oltre 0,40 s dopo la loro parola**; i tre wipe anticipano la parola di 0,4-0,5 s apposta.

## Cosa è stato implementato (motore `world3d` e plate)
Dettagli in `references/formats.md` §52b. Tutto opzionale e retrocompatibile (rendering di un vecchio mondo verificato identico).
1. **Look atelier**: una luce calda attraverso la veneziana (ombre vere, a strisce che scivolano), riempimento freddo verde bosco, polvere in sospensione, pavimento e parete.
2. **Pass argilla / inchiostro / finale** con **barra di taglio** rossa e tag HUD `FRAME .... · PASS: ...`; ogni oggetto può avere il suo look (`look="ink"`): servono per il finale con i tre pantaloni.
3. **Motion blur** a sotto-fotogrammi sopra 0,6 m/s (otturatore 0,8 fotogramma).
4. **Profondità di campo** (12 render con la lente su un disco, il punto guardato resta nitido).
5. Card **flat** (senza luci né ombre) per i titoli.
6. **Principi UX nelle plate 2D** (proposte NON votate): `Board(arc=0.03)` (Jacopo 14/11: più lineare) (archi sulle swipe, opt-in, default spento), `plates_base.repeat_factor()` (frequenza d'uso), `scripts/qa-lag.py` (ritardo parola → effetto). Demo Prima \| Dopo in `videos/_bench/ux-prove/` (`UX-principi-prima-dopo.mp4`).

## Numeri misurati (GPU GTX 1060, WebGL hardware)
- Render completo **1080p: 2 min 18 s**. Render completo **4K: circa 6 min** (la stima iniziale di 35 s per secondo era dominata dall'avvio, non dal rendering).
- Le finestre con profondità di campo e blur sono le più lente (12 render per fotogramma); in tutto il video: 13 s di DOF.

## Cosa NON è stato verificato / limiti onesti
- **Non ho potuto ascoltare l'audio**: ho controllato livelli (volumedetect), durata, assenza di sovrapposizioni e i tempi delle parole, ma l'accento italiano di Edward e il bilanciamento a orecchio vanno ascoltati da te. Se la voce non convince, `GenerateVoiceover` con un'altra voce (`it`) e `python mix.py` rifanno tutto in un minuto.
- Il video non è stato visto "a occhi umani": ho guardato fotogrammi a campione (fogli di contatto ogni 1-5 s e 18 still), non il flusso a velocità normale.
- **Nessun voto di Jacopo** né sul look né sui principi UX: sono proposte da sottoporre ad A/B.
- Il 3D ha un vocabolario di oggetti ridotto (pantalone, card, solidi): niente modelli veri, niente tessuto che si muove.
- Notion (Jackss HQ) non aggiornato in questa notte.
- Il "pantalone" è un oggetto generato in codice, stilizzato: non è una fotografia del capo vero.

## Come rifarlo
```bash
cd videos/_bench/video-3d-moda
python build.py                                   # scena -> comp/index.html
npx hyperframes@0.9.35 render comp --resolution landscape-4k -q looks -o renders/video-4k-silent.mp4 --quiet
python mix.py                                     # audio -> renders/mix.wav
ffmpeg -i renders/video-4k-silent.mp4 -i renders/mix.wav -c:v copy -c:a aac -b:a 256k -shortest FINAL.mp4
```
