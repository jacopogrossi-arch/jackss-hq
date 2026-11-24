# HANDOFF — Reel «Le 3 misure» (24/11/2026)
Testo e voce APPROVATI da Jacopo (voce: videos/_bench/reel-3-misure/vo/vo.wav, 32.74 s, 447 crediti spesi). Vedi script.md.
Jacopino NON parla: attore in scena al tavolo, non guarda mai la camera, niente primi piani frontali.
## Stato
- reel.py: aggiunti (dietro chiavi della partitura) TAVOLO (tavolo + pantaloni piatti con cartellino «M» 3D), MISURE (linee che si tracciano + metro), HIDE_OLD, IK_WORLD (mani in coordinate mondo). Patch gia' applicata, MAI TESTATA: non ha ancora girato.
- score_misure.py: scritta (prima stesura, tempi dalla voce, camere e mani da tarare a occhio).
## Prossimo passo (gate 1, prima di animare)
Renderizzare 3 still a 48 campioni e mostrarli a Jacopo: gancio (t=1.5 s, frame 37), misura vita (t=9.4 s, frame 226), cavallo (t=15.5 s, frame 373). Comando: blender -b -P social/gemello/reel.py -- OUT --score social/reel-3-misure/score_misure.py --frames N-N --samples 48 (BLENDER_USER_RESOURCES=D:\blender-user, in background).
Poi: gate sagoma pantalone (waist/rise/inseam nei punti giusti), aggiungere al --check il controllo dello sguardo (angolo testa-camera > ~35 gradi), plate in post (×2 solo sulla vita), numeri veri di Jacopo (3 misure di un suo pantalone) al posto dei segnaposto.
## Tempi
786 fotogrammi: anteprima mezza risoluzione ~20 min, render finale 1080x1920 ~90 min.

## 24/11 sera — Gate 1 superato (3 still: videos/_bench/reel-3-misure/g1/g1c.png)
Il codice di reel.py (tavolo, pantaloni piatti, cartellino «M» 3D, linee, metro, IK mondo) GIRA. Bug risolti: l'import del GLB cancellava le azioni di props/linee/metro (ora PRE_ACTIONS le salva); chiavi di visibilita' una per fotogramma; beccheggio testa NEGATIVO = guarda in basso; mani piatte (FING 0); fstop 6-8.
Da sistemare dopo il giudizio di Jacopo: gancio (taglia in alto la testa e il bordo del pantalone sinistro), metro lungo 0.13 sporge molto (valutare 0.09), linea di misura coperta dal metro (alzare z o allargare), mano destra sembra un pugno nel cavallo, moiré da pochi campioni (a 48 e' normale).
Poi: --check sguardo, plate, numeri veri, animazione completa (anteprima mezza risoluzione ~20 min).

## 24/11 sera — v4 (video: videos/_bench/reel-3-misure/reel-3-misure-v4b.mp4)
Feedback di Jacopo sulla v3 (scritte mal posizionate/stile diverso, taglio a 0:03 scattoso, camera macchinosa, metro nei pantaloni/fibbia, striscia rosa e "effetto patinato", tutto sparisce di colpo, disordinato e poco luxury) -> risolti:
- CAUSA DEL "GLITCH" su giacca/capelli: NEBBIA VOLUMETRICA (VOLD) a pochi campioni = reticolo a quadretti. Ora VOLD=0 nella partitura (reel.py: `--vol` / chiave VOLD).
- Pantaloni antracite + gesso bianco OPACO (no emissione) accanto al metro; niente passanti/bottone; un metro per misura (lunghezza = misura + 1 cm) che si srotola e si ritira in 0.4 s; etichette 3D VITA/CAVALLO/INTERNO con pop; segnalini (NON scalarli: bug del blocco bianco gigante a 8 s).
- CAM_SOFT (movimento quasi lineare), camera che SEGUE il metro; Jacopino a PUPPET_Y=0.18 (7 cm dietro il tavolo), MAT_COLORS scuri, props ridotti, JACKET_WEAVE 170.
- Sottotitoli = captions.py (Inter ExtraBold + Playfair corsivo #ffb48f, una parola alla volta, pop, CY=250) coi tempi della voce (Whisper corretto a mano); assemble.sh aggiunge flash caldo sui tagli (forte a 3.24) e la voce.
- reel.py: ATTENZIONE alla riga che cancella le azioni dopo l'import del GLB (ora salva PRE_ACTIONS).
## Da fare
Tre misure vere di Jacopo (le etichette non hanno numeri: i numeri d'esempio sono stati tolti dai sottotitoli), suono (swish Epidemic), render finale 1080p (VOLD=0: piu' veloce di prima, da misurare), controllo guardando il video intero.
