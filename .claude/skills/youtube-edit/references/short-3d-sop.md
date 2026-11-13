# SOP: Short verticale 3D (formato "atelier", dal 13/11/2026)

Lo Short #1 "Il mio primo pantalone sembrava una gonna" (pubblicato il 13/11/2026, v5) è il modello. Questa procedura dice come rifarne uno da zero in una sessione nuova, senza ripagare gli errori già fatti. Va letta insieme a `explainer-3d-sop.md` (metodo Autogrill: voce, suono, mix) e a `taste.md` (note di gusto, sezioni "Short").

**Progetto di riferimento:** `videos/_bench/short1/` (locale, fuori da git). Copia dei sorgenti nel repo: `personale/youtube/short-primo-pantalone/src/` (build.py, room.py, mix.py, finish.sh, transcribe.py). Per uno Short nuovo: copia la cartella `src/` in `videos/_bench/shortN/` e parti da lì.

---

## 0. Le regole d'oro (tutte da note di Jacopo)
1. **Testo a schermo per tutto il video.** Sottotitoli parola per parola (`w.captions`, top=1180, size 96) alternati a frasi grandi (`w.big`, 76–82 px, un numero fino a ~96). Una riga, due al massimo.
2. **Voce clonata espressiva:** ElevenLabs "Jacopo Prova" (instant, id `0CeJTHP08UsLHht7KIni`), UN PARAGRAFO ALLA VOLTA con punteggiatura espressiva (… ! ?), uniti con pause di 0,35–0,55 s. Una sola take lunga viene piatta.
3. **Il gancio si vede nel primo fotogramma.** La frase d'apertura deve essere VERA sullo schermo (Short #1: tela di 3/4 dal lato del fianco gonfio mentre dice "sembrava una gonna").
4. **Un contatore che segue le FASI.** Short #1: la pillola in alto "costo di un errore": disegno = niente, cartamodello = un foglio di carta, tela = un pezzo di stoffa. Cambia quando cambia la fase, non con una parola che arriva dopo.
5. **Niente testo doppio.** Se un'etichetta 3D dice la stessa cosa del sottotitolo nello stesso momento, l'etichetta arriva 0,8 s dopo, oppure ANTICIPA (compare sulla parola prima, es. "Pantalone COS" su "le ho copiate").
6. **La fisica deve tornare.** Il metro gira INTORNO al capo e ruota con lui; un segno di gesso sta SU un oggetto, mai sospeso; un contorno tratteggiato abbraccia il capo e non attraversa altro (manichini, pavimento).
7. **La camera non attraversa niente.** Le lampade a sospensione si spengono in dissolvenza durante il volo verso la mappa (`pendant(hide=[[t0,t1]])`); gli oggetti "in attesa" si parcheggiano SOPRA la camera della mappa (y 30), mai sotto (l'insegna INVERSO a y 11,5 faceva una macchia nera).
8. **Revisione a 10 fps prima di ogni render finale** (§6). Il 4K parte solo dopo.
9. **Da migliorare sul prossimo (confronto con l'Autogrill, `taste.md`):** più cambi di SCALA (aereo ↔ macro), un momento-diagramma che spiega, un colore di contrasto forte in ogni inquadratura, una pausa dopo le frasi chiave con il cambio di vista dentro la pausa, la musica scelta sul montaggio.

## 1. Idea e copione (30 min)
- Un errore o una scoperta vera, con un numero vero. Struttura: gancio (3 s) → percorso a fasi → svolta → morale → brand → "seguimi".
- 70–90 s, ~245 parole. Fatti presi dai file del repo (mai inventati). Firma del canale: "Sono uno studente, non ho niente da venderti: sto documentando tutto". Mai "non sono un esperto".
- Copione in `personale/youtube/<short>/script.md`, confermato da Jacopo prima della voce.

## 2. Voce e parole (15 min)
1. Genera un paragrafo per volta col connettore ElevenLabs (creative_generate_speech, voce "Jacopo Prova"). I link firmati del download NON vanno nel repo.
2. Unisci (ffmpeg, pause 0,35–0,55 s) → `vo.mp3`.
3. `python transcribe.py vo.mp3` → `words.json` (faster-whisper small, word timestamps). In `build.py` tutto si aggancia alle parole: `at("parola", n)`, `end(...)`, `wend(radice, dopo)`.

## 3. Il mondo 3D (formato 52, `formats/world3d.py` + `assets/vendor/atelier-*.js`)
- **`room.py` → `furnish(w, hide=...)`:** l'atelier a 360°: pavimento in legno, pareti con finestre, tavolo da disegno (tappetino, squadra, gesso, lampada), tavolo da cucito, manichini, parete di rocchetti, rastrelliera dei rotoli, binario con capi, piante, quadri, lampade a sospensione. Ogni lato del set deve essere bello (Jacopo: "cura bene… a 360 gradi").
- **Oggetti narrativi (`build.py`):** `w.trouser(...)` (tela, COS, hero; `turn`, `move` con valori assoluti), `sketchdraw` (matita che disegna), `patterncut` (forbici che tagliano: direzione mediata su ±8 punti), `hoop` (metro ad anello che segue la rotazione del capo), `pathdots` (contorni e percorsi), `floorbadge` (stazioni numerate a terra), `logoplate` (insegna finale).
- **Mappa aerea:** `MAP = ((3.45, 12.5, 1.45), (0.45, 0, 1.35))`, le 4 stazioni compaiono tutte PRIMA del tuffo, il percorso rosso si disegna tra una stazione e l'altra.
- **Camera:** `C(t, durata, pos, look, ease)`. Il semi-campo orizzontale è ~12° (fov 42, 9:16): un oggetto a più di ~12° dall'asse esce di quadro. Mai colpi di frusta sotto 1,1 s.
- **Etichette:** `w.label(oggetto, punto, "Testo *corsivo*", t, out, anchor, dx, dy)`. Non sulla banda dei sottotitoli (y ≈ 1180) né sul bordo né sulla pillola del costo (top 118).

- **Second world (Short #2, 13/11/2026):** `assets/vendor/atelier-studio.js` holds the night studio. It is loaded by `atelier-kit.js`, and the room is laid out in `videos/_bench/short2/room.py`, copied into `personale/youtube/short-02-identita/src/`. Objects:
  - `wordblocks` (letter-cube totem)
  - `seampanel` (right side / reverse side, also `dirty`)
  - `fastrail`
  - `wallclock` (`spin`)
  - `shoeboxes`
  - `sneaker`
  - `axisline` (floor diagram with puck)
  - `crossmark`
  - `cityview`
  - `crittall`
  - `bookshelf`
  - `pinboard` (`cards` that pop in)
  - `swatchwall`
  - `laptop`
  - `deskset`
  - `terrazzo`

  The brand fonts (Instrument Serif, IBM Plex Sans) live in `assets/fonts/`. For the next Short, build a NEW world: copy the pattern, not the room.
- **Long unattended work (overnight):** keep a `HANDOFF.md` in the work folder (task, rules, commands, to-do list, timed STATE) and schedule a one-off resume agent about 15 min after the token reset. The agent reads HANDOFF and resumes only if the main session has stopped.

## 4. Suono (`mix.py`, metodo Autogrill)
- Musica Epidemic (licenza, `assets/music/licensed/`, riga in CREDITS.md); mai la stessa traccia ad aprire due video di fila. Short #1: "Ghost Band – Run".
- Eventi fissi (whoosh + colpo d'apertura, riser col picco sulla parola-gancio, mappa, tuffi, forbici, contatore, cambi della pillola) + automatici (pop sulle etichette, swish sulle frasi grandi, whoosh sui movimenti), mai due suoni entro 0,35 s.
- Musica 13 dB sotto la voce MISURATA in LUFS, sidechain, poi guadagno FISSO a −16 LUFS + limiter.

## 5. Build e verifica
```bash
python build.py
TMP="D:\hf-tmp" TEMP="D:\hf-tmp" TMPDIR="D:\hf-tmp" npx hyperframes@0.9.35 snapshot comp --at 0.1,5,12,24 -o /d/hf-tmp/snap
```
Guarda il contact sheet a ogni modifica. Per trovare un oggetto misterioso: variabile `SKIP` in `room.py` e snapshot a confronto (bisezione).

## 6. Bozza e revisione a 10 fps (~10 + 15 min)
```bash
rm -f renders/draft-raw.mp4 renders/draft.mp4 renders/mix.wav     # SEMPRE: finish.sh salta i file che esistono già
bash finish.sh draft                                               # 30 fps, voce+sfx+musica, QA
ffmpeg -i renders/draft.mp4 -vf "fps=10,scale=240:-2,drawtext=fontfile=a.ttf:text='%{pts\:hms}':x=4:y=4:fontsize=18:fontcolor=yellow:box=1:boxcolor=black,tile=8x4" s%02d.jpg
```
Guarda TUTTI i 28 fogli (3,2 s ciascuno) cercando: sfarfallii, oggetti che attraversano o fluttuano, etichette tagliate o sovrapposte, testo doppio, contatori sbagliati per la fase, inquadrature dove il soggetto esce. Correggi → snapshot dei tempi cambiati → poi il 4K. Utile anche: stampare per ogni etichetta i movimenti di camera che la attraversano (`B.w.labels` × `B.CAMS`).

## 7. Render finale 4K (~20 min sulla GTX 1060) e consegna
Script: `/d/hf-tmp/final4k.sh` (rigenera il mix, poi):
```bash
npx hyperframes@0.9.35 render comp --quality high --resolution portrait-4k --gpu --video-bitrate 60M --fps 60 --workers 4 -o renders/final4k-raw.mp4
# mux con renders/mix.wav + tag BT.709 → <nome>-vN-4k.mp4 ; copia leggera 1080p 2-pass 2300k → <nome>-vN-leggero.mp4 (~28 MB)
```
- Verifica sempre che il file si legga fino in fondo: `ffmpeg -v error -ss 87 -i file.mp4 -f null -`. **Dopo un crash del PC i file a metà sono corrotti (blocchi di zeri) anche se la durata sembra giusta:** cancella draft-raw, draft, mix.wav e rifai.
- Consegna in iCloud `C:\Users\Jacopo Grossi\iCloudDrive\Video 3D moda\`; da lì Jacopo pubblica dal telefono. Il connettore Google Drive accetta solo file fino a 10 MB (niente video).
- C: ha poco spazio: TMP sempre su `D:\hf-tmp`.

## 8. Pubblicazione
- Titolo con `#shorts`, descrizione: l'errore + il numero, la morale, il percorso, la firma, il link al video lungo, max 5 hashtag.
- **Video correlato** sempre puntato al video lungo collegato (Short #1 → #4, poi #5). Registro in `personale/youtube/piano-canale.md` › Shorts.
- Sorgenti nel repo (`personale/youtube/<short>/src/`), note di gusto in `taste.md`, stato su Notion.
