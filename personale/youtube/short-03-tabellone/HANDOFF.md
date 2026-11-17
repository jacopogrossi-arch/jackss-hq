# HANDOFF — Short #3 "Quanto costa lanciare un pantalone (se non hai un brand)" (16/11/2026)

Stato: copione APPROVATO da Jacopo. NON pubblicare (lo decide lui). Da fare in una sessione nuova.

## Cosa esiste
- `script.md` + `README.md`: copione a 7 battute, ~65 s, gioco da tavolo (caselle: disegno, cartamodello, foto, pre-order, arrivo, CTA "Scrivi PANTALONE", logo).
- `build-anteprima.py`: copia dello script del motore (1080x1920). Originale locale: `videos/_bench/short3/build.py`; fogli di revisione in `videos/_bench/short3/review/` (locale, fuori da git). Per girarlo serve il motore in `.claude/skills/fashion-3d/engine/` (snapshot: `TMP=D:\hf-tmp ... npx hyperframes@0.9.35 snapshot <cartella> --at a,b,c --no-end -o OUT`).
- Il pantalone nella casella "arrivo" e' un glb locale: `videos/_bench/fashion3d/blender/trouser10b.glb` (v10, colore #414b27, `fabric=True, grain=2.6, tile=3` nel motore). Si rigenera con `.claude/skills/fashion-3d/scripts/blender_trouser10.py` (Blender MCP, ~80 s). Nello script dell'anteprima il glb e' ancora quello vecchio: aggiornare il percorso.

## Da fare
1. Voce: ElevenLabs va riautorizzato da `/mcp` (voce "Jacopo Prova", id 0CeJTHP08UsLHht7KIni, vedi memoria reference_voce_elevenlabs). Poi costruire sulle parole (words.json), mix, revisione a 8 fps (memoria feedback_analisi_video_8fps).
2. Correggere l'anteprima: la card "€500–1.500" e' tagliata a 55 s; la vista della finestra di notte si vede appena.
3. Sostituire il pantalone dell'anteprima col glb v10 e, se serve, la scena atelier unita (esempio: `scripts/lab_merge_example.py`).
4. Procedura generale: `.claude/skills/fashion-3d/references/short-3d-sop.md`. Regole: niente "tela" nei video, mai Magnific/Higgsfield, hashtag max 5, commit per nome file (repo pubblico, `videos/` fuori da git).

## Altro in sospeso (non e' del Short)
- Pantalone v10: idee non fatte in `.claude/skills/fashion-3d/references/HANDOFF-trouser-v10.md` (spot dalla lampada, busto, gambe).
- Chiave Gemini in `.env` (locale): consigliato cambiarla perche' incollata in chat.

## File caricati in repo (16/11, perche' Jacopo non debba spostare nulla)
In `assets/`: `trouser10b.glb` (pantalone v10, colore finale), `anteprima-1.jpg` e `anteprima-2.jpg` (fogli di revisione dell'anteprima), `confronto-pantalone-round11.jpg` (riferimento vs scena unita). Nello script dell'anteprima usare `assets/trouser10b.glb` al posto del glb locale. Resta fuori dal repo SOLO la chiave `.env` (segreta, non va mai caricata).

## Aggiornamento 16/11 (sessione 2)
- Fatto: glb v10 (`assets/trouser10b.glb`) nell'anteprima, pantalone ridotto (fit 0.7), card €500–1.500 spostata in quadro.
- Resta: voce (serve /mcp → elevenlabs), finestra di notte quasi invisibile (parete troppo chiara), poi sottotitoli/mix/revisione 8 fps.

## Aggiornamento 16/11 (sessione 2, dopo la riconnessione ElevenLabs)
- Voce fatta: 7 paragrafi con "Jacopo Prova" (eleven_v3, 1 take ciascuno, ~760 crediti), posizionati all'inizio di ogni scena (0 / 5.0 / 14.9 / 26.2 / 38.2 / 50.2 / 58.6 s). File SOLO in locale: `videos/_bench/short3/vo/` (vo-placed.mp3 = 62,6 s). words.json (corretto a mano) e build nel repo.
- Anteprima: sottotitoli parola per parola + 2 frasi grandi ("Quanto costa lanciare un pantalone?" 0-3,6 s; "10, poi 20 non cento" 45-49,6 s); niente sottotitoli sotto le frasi grandi e dopo 58,4 s (la CTA 3D porta il testo). Camera allargata sui cartellini prezzi.
- Resta: musica Epidemic (non la stessa traccia dello Short precedente) + suoni, mix a -16 LUFS, bozza con finish.sh, revisione a 8 fps di TUTTO, finestra di notte (parete troppo chiara), poi 4K e consegna in iCloud. NON pubblicare.

## Aggiornamento 16/11 (sessione 2, sera): mix + bozza + revisione 8 fps
- Musica: Epidemic "Pixel Ghost" (HiP CoLouR, 98 bpm) in `assets/music/licensed/es-pixel-ghost.mp3` (locale, credito in CREDITS.md). `mix.py` (nel repo): voce + 23 suoni agganciati agli eventi del tabellone + musica 13 dB sotto la voce, -16 LUFS. Output `videos/_bench/short3/renders/mix.wav`.
- Bozza: `videos/_bench/short3/renders/draft.mp4` (30 fps). Revisione a 8 fps su tutti i 22 fogli: nessun sfarfallio. Corretti: cartellino €3.000-8.000 tagliato e laptop in ritardo (camera piu' larga 29-35 s), frase "10, poi 20" riallineata alla voce (46.5 s).
- Resta (decisioni/qualita'): finestra di notte (parete chiara), cartellino "tempo, non EUR" illeggibile nella vista dall'alto (20-26 s, il sottotitolo lo dice), finale un po' affollato (card + CTA + logo + Jacopino). Poi: ascolto reale della bozza da parte di Jacopo, render 4K (~20 min), consegna iCloud. NON pubblicare.

## 16/11 sera: render finale
- Finestra con foro (vista crepuscolo), cartellino tempo ingrandito, finale alleggerito. Render 1080p 60 fps: `videos/_bench/short3/short3-tabellone-v1.mp4` (65 s, 87 MB), copia in iCloud `Video 3D moda\short3-tabellone-v1.mp4`. Resta: ascolto/ok di Jacopo, eventuale 4K, titolo+descrizione (max 5 hashtag), pubblicazione SOLO se la decide lui.

## 16/11 notte: VERSIONE 2 (il tabellone e' bocciato)
- Jacopo ha bocciato la versione "gioco da tavolo" (troppo lenta, Jacopino e grafiche brutti). Rifatto come **sala campioni di notte** (stile studio di notte, mondo nuovo): `v2/` (build.py, room.py, mix.py, final1080.sh). Progetto locale `videos/_bench/short3b/`. Voce e words.json invariati (non rigenerare).
- Struttura: logo capovolto -> 5 postazioni (scrivania disegno, tavolo da taglio, set foto, parete 100 pezzi 10+20, pantalone appeso) con 5 salite sulla mappa; contatore "il mio costo"; un movimento camera ogni 2-3 s; fine con logo + CTA "Scrivi PANTALONE".
- Musica Epidemic "Pixel Ghost". Render finale: `short3-sala-campioni-v2.mp4` (1080x1920, 60 fps) in iCloud `Video 3D moda\`.
- Da migliorare se Jacopo lo chiede: set foto (macchina e softbox ancora blocchi semplici), colore dominante marrone, inquadrature scure a 17-19 s.

## 17/11: VERSIONE 3 (review di Jacopo sulla v2)
Note di Jacopo sulla v2 e cosa e' stato fatto (progetto locale `videos/_bench/short3c/`, sorgenti in `v3/`):
- Voce non sua / poco espressiva -> rigenerata con `eleven_v4` (la v2 usava `eleven_v3`, errore). Misurato: v4 ~ voce Short #2. Nuovo testo CTA: "A quanto lo vendo, alla fine? Scrivi PANTALONE nei commenti e ti dico il prezzo finale." (plate "Scrivi PANTALONE nei commenti" + card "e ti dico il prezzo finale").
- Logo che gira a 0:00 gia' usato nello Short #2 -> apertura sul pantalone appeso con card "€ ?"; logo solo alla fine (cade e gira).
- Pop sound (0:10, 0:23, 0:35, 0:53) -> sostituiti da swish morbidi (regola: niente pop).
- Plate "< €30" entrava prima e usciva subito -> entra su "30", resta fino alla salita sulla mappa (pausa piu' lunga prima della seconda tappa).
- Stampella mancante -> gancio + barretta + due pinze.
- "Te in miniatura": il busto di cartone con la foto e' stato BOCCIATO ("cartonato no"). Ora e' un omino stile Lego con occhiali tondi, capelli sparati in su, maglia nera, jeans con cimosa rossa, stivali texani: `.claude/skills/fashion-3d/engine/vendor/atelier-mini.js`, `w.minime(...)`. Parla (bocca, testa, mano) sulle parole. Resta il tipo `w.standee` (cartonato) nel motore, non usato.
- Render: `short3-sala-campioni-v3.mp4` (1080x1920, 60 fps) in iCloud `Video 3D moda\`.

## 17/11 sera: omino da foto (in sospeso)
- Provato Blender headless (`.claude/skills/fashion-3d/scripts/blender_minime.py`, 2 giri): volto scolpito da script NON convince (testa a uovo, capelli a squame). Le nuove skill Blender (blender-modeling ecc.) dicono che i personaggi organici sono fuori dal loro campo.
- Jacopo (17/11): provare image-to-3D dalla sua foto e/o le skill Blender con l'MCP. Il Blender MCP NON e' collegato in questa sessione (server `blender` in timeout; serve Blender aperto con addon connesso + riavvio sessione). Gli unici image-to-3D visibili qui sono Higgsfield `generate_3d` e Magnific `models3d_generate`, due servizi che Jacopo ha dismesso: non usati senza il suo ok.
- Input pronti in `videos/_bench/minime-input/` (locale). Nel video v3 resta l'omino stile Lego senza occhiali.

## 17/11 notte: PIANO CONCORDATO CON JACOPO PER L'OMINO (da riprendere in nuova sessione)
**Tutti i pareri di Jacopo, in sintesi (da rispettare):**
- Omino: NO cartone, NO "tre solidi uno sopra l'altro"; deve ASSOMIGLIARGLI ma NON realistico: stile giocattolo/cartoon coerente col video. Senza occhiali. Capelli alzati/dritti. "Se no semplicemente lasciamo stare."
- Strumenti: ok a un servizio image-to-3D SOLO via API a consumo (niente abbonamenti); lui crea la chiave e mette i dati di pagamento. Prima mi serve il Blender MCP collegato (Blender aperto con addon, sessione riavviata) e le nuove skill Blender (9 MIT in `.claude/skills/`).
- Voce: solo `eleven_v4` (mai v3). Niente suoni "pop": solo swish morbidi. Apertura mai uguale a un video precedente. Plate "< €30" deve entrare sulla parola e restare. CTA chiara ("scrivi PANTALONE nei commenti e ti dico il prezzo finale"). Stampella visibile.
- Bozza v3 (`short3-sala-campioni-v3.mp4`) in revisione da parte di Jacopo: aspettare i suoi pareri; NON pubblicare.

**Fatto stanotte:** immagine stilizzata (toy/vinyl, full body, A-pose, fronte, sfondo grigio, senza occhiali, maglia nera, jeans cimosa, stivali texani) generata con Gemini `gemini-3-pro-image-preview` dalla sua foto: `videos/_bench/minime-input/toy-jacopo-v1.png` (locale, fuori da git). E' l'input per l'image-to-3D.
**Prossimi passi (nuova sessione):**
1. Jacopo: Blender aperto + MCP connesso; crea la chiave API del servizio image-to-3D (a consumo) e la mette in `.env`.
2. Eventuale rifinitura dell'immagine (vista di fianco/retro per migliori risultati multi-view).
3. image-to-3D -> GLB -> pulizia in Blender (scala, orientamento, peso) -> `w.glb(..., fit~0.3)` al posto dell'omino Lego in `short3c/build.py` `me()` -> render 1080p60.

## 17/11 notte: OMINO SCELTO (stile PS2 low-poly, variante B3 corretta)
Scelto da Jacopo: stile PS2 low-poly, testa grossa, occhiali da sole neri tipo Wayfarer, Barbour verde oliva aperta su maglia nera, orologio argento al polso sinistro, NIENTE collanina, jeans leggermente svasati che coprono gli stivali, stivali NERI punta quadrata. Immagini (locali, in `videos/_bench/minime-input/`): `toy-jacopo-v4-front.png`, `-side.png`, `-back.png` (confronto-v4.png). Sono l'input per l'image-to-3D (multi-vista).

## 17/11 notte: DEFINITIVO + regola di regia
- Design omino DEFINITIVO (approvato da Jacopo): copie in `videos/_bench/minime-input/DEFINITIVO/jacopo-ps2-{front,side,back}.png` (locale).
- Jacopo ha visto la v3 ("praticamente perfetta"). UNICA modifica richiesta per la versione con l'omino nuovo: quando l'omino parla/e' animato, ZOOM di camera su di lui; poi stacco/spostamento IMMEDIATO della scena sull'argomento che sta dicendo. Cosi' si capisce che e' il NARRATORE e non un oggetto staccato dalla scena. In build.py: per ogni apparizione `me()` aggiungere cam raw sull'omino all'inizio della frase, poi cam sull'argomento.
- Prossima sessione: Jacopo apre Blender+MCP, chiave API image-to-3D.

## 17/11 notte: STATO PER LA NUOVA SESSIONE (leggi questo per primo)
**Obiettivo:** sostituire l'omino Lego di `short3c/build.py` (`me()`) con l'omino PS2 definitivo in 3D vero, poi render 1080p60. v3 approvata da Jacopo ("praticamente perfetta"): cambia SOLO l'omino + regola di regia (zoom su di lui quando parla, poi stacco subito sull'argomento).
**Immagini definitive (locali):** `videos/_bench/minime-input/DEFINITIVO/jacopo-ps2-{front,side,back}.png`.
**Image-to-3D, cronologia:**
- Tripo/Meshy: export GLB solo con abbonamento (12 euro): Jacopo non vuole.
- fal.ai: ricarica minima 10 euro: scartato. Chiave `FAL_KEY` messa in `.env` ma NON usata (puo' essere cancellata).
- Scelta attuale: Hunyuan3D open source su Hugging Face (Space `tencent/Hunyuan3D-2mv` = multi-vista fronte/lato/retro, oppure `Hunyuan3D-2.1` per le texture a colori). Jacopo ha finito la quota ZeroGPU gratuita, poi ha caricato credito su Hugging Face.
- Jacopo installa l'MCP Hugging Face: `claude mcp add hf-mcp-server -t http "https://huggingface.co/mcp?login"` + login con `/mcp` in sessione nuova. Con quello chiamare il Space Hunyuan3D (tool `dynamic_space`) e scaricare il GLB. Se non funziona, Jacopo usa la pagina web e mi da' il GLB in `videos/_bench/minime-input/`.
**Impostazioni 3D consigliate:** formato GLB, texture a colori, ~30.000 triangoli (stile PS2), niente luci cotte nelle texture, posa A.
**Dopo il GLB:** Blender (MCP se collegato, altrimenti headless `"C:\Program Files\Blender Foundation\Blender 5.1\blender.exe" -b -P script.py`): scala, orientamento, pulizia, controllo texture -> `w.glb(..., fit~0.3)`. Animazione parlata: dondolio/rotazione della testa e del busto sui `talk` windows (il GLB e' statico).
**Da dire a Jacopo all'inizio:** aprire Blender con addon connesso (MCP), verificare `/mcp`.
