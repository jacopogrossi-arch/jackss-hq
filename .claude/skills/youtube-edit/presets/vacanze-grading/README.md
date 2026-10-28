# Preset `vacanze-grading` — grading scientifico dei video vacanza di Jacopo

Secondo tipo di montaggio di Jacopo (idea del 23/10/2026). **Solo grading**: niente tagli, grafiche, suoni o musica (per ora). Vale per le clip girate
in log con le camere DJI di Jacopo. Non si usa con `compose.py`: si usa con `grade-scan.py` e `grade-apply.py` (cartella `scripts/`).
Tutti i numeri qui sotto stanno in `preset.json` (chiave `grade`): per cambiarli si cambia una riga, non il codice.

## Quale camera, quale profilo, quale LUT

| Camera | Profilo | Come lo riconosciamo | LUT (`assets/luts/`) |
|---|---|---|---|
| Osmo Pocket 4P | D-Log2 | tag `com.dji.camera.ColorGammaSxS` = D-Log2 (anche negli export di DJI Mimo) | `DJI-Pocket4P-DLog2-to-Rec709-size65.cube` |
| Osmo Pocket 4P | D-Log | stesso tag = D-Log | `DJI-Pocket4P-DLog-to-Rec709-V2.0-size33.cube` |
| Osmo Nano | D-Log M | il file porta solo il modello: "probabile", confermato solo se la LUT aggiunge colore | `DJI-OsmoNano-DLogM-to-Rec709-V1.cube` |

- **Mai incrociare** D-Log, D-Log2 e D-Log M: sono tre curve diverse. Se il profilo non e' certo, `grade-apply.py` rifiuta di lavorare.
- Per usare un'altra versione (V1.0 invece di V2.0, o la vivid) basta cambiare il nome del file in `preset.json` → `grade.luts`.
- Un'altra camera in log (drone, Action...) richiede la sua LUT ufficiale DJI e una riga nuova in `grade.luts`.

## LUT creative pronte per il Pocket 4P (adimology, aggiunte il 27/10/2026)
Pack gratuito di @adimology (Google Drive "adimology - DJI Pocket 4P Creative LUTs"): 5 LUT `.cube` che leggono **direttamente il log** e sostituiscono
la LUT tecnica DJI. Stanno in `assets/looks/external/adimology-p4p/` — **solo in locale**: la licenza vieta di ridistribuirle, quindi mai su GitHub.
**Non sono il predefinito** (deciso da Jacopo il 27/10/2026): il grading resta LUT tecnica DJI + look `pellicola-oro`; queste si usano solo se le chiede.
Si usano con `grade-apply.py --log-cube adimology-p4p/adimology-P4P-<Nome>.cube` (scan, anteprima e render restano uguali).

- **Sono costruite sulla curva D-Log**, non D-Log2 (misurato su una rampa di grigi: distanza dalla LUT DJI D-Log 0,03-0,05, dalla D-Log2 0,12-0,14).
  Su D-Log2 vengono piu' scure: l'autore consiglia di girare D-Log a EV +1 e D-Log2 a EV +2.
- Prova sulla clip D-Log della spiaggia (`videos/_grade-test/adimology/confronto-adimology.png`):
  - **IndieHaze**: la piu' vicina alla DJI ufficiale, acqua turchese, neri leggermente sollevati — la piu' adatta ai video vacanza.
  - **RetroWarm**: pelle calda e abbronzata, mare piu' spento.
  - **UrbanSlate**: desaturata fredda, mare grigio — da citta', non da mare.
  - **GoldenHour** e **StreetNoir** (bianco e nero): molto scure, pensate per girato a EV +1 o piu'; su clip esposte normalmente servono +1/+2 stop.
- Regola del pacchetto: bilanciamento del bianco ed esposizione si correggono **prima** della LUT (e' gia' l'ordine di `grade-apply.py`).

## Il metodo (sempre in questo ordine)
1. **Scan:** `grade-scan.py --video clip --out cartella`. Misura 12 fotogrammi: zebra a 95 IRE e sulle luci bruciate, neri schiacciati, mediana, pelle,
   waveform, vectorscope, istogramma. Scrive `REPORT.md`, `scopes-sheet.png` e una **proposta** di esposizione. Non cambia niente.
2. **Anteprima:** `grade-apply.py --video clip --scan cartella/report.json --out cartella2` (senza `--render`). Tre colonne: log come girato / solo LUT /
   LUT piu' esposizione con zebra, piu' gli scope. Nessun video scritto. **Jacopo guarda e approva** (o dice un altro valore con `--stops`).
3. **Render:** stesso comando con `--render`. 4K, HEVC 10 bit, la scheda video se c'e'. Poi il file viene **riletto e misurato**: deve coincidere con la
   previsione, non avere luci bruciate (max 1 %) ne' neri schiacciati (max 5 %), e la pelle deve essere piu' vicina alla fascia di prima. `CHECK.md`: PASS o FAIL.

## Regole imparate sulle clip vere (23/10/2026)
- **L'esposizione si ancora sulla pelle** (fascia 30-50 IRE: e' dove il suo stesso grading porta la pelle, 34-42 IRE; con la fascia 50-68 che avevo supposto schiarivo troppo; si sposta solo fino al bordo della fascia, non al centro), non sulla mediana: una spiaggia luminosa faceva proporre -1,5 stop a una clip gia' giusta.
  Se in scena non c'e' pelle si usa la mediana (fascia 35-55, bersaglio 42).
- **Il limite delle luci guarda il canale di colore piu' luminoso** del fotogramma peggiore (il 99° percentile non deve passare 97 IRE): il mare satura in verde
  mentre la luminanza e' ancora bassa. Con la luminanza sola, +1 stop bruciava il mare.
- **L'esposizione e' un guadagno sul segnale gia' graduato** (codice x 2^(stop/2.4)), mai sul log. Massimo ±2 stop: oltre non e' un grading, e' da rigirare (limite di ffmpeg incluso).
- **Il bilanciamento del bianco si misura solo su oggetti quasi neutri** (nuvole, barca bianca, muro grigio: colore sotto 0,02, luminosita' 45-92 %, almeno l'1 % del fotogramma),
  mai sul colore medio: il mare e il cielo sono colorati di proposito. Con la soglia larga (0,06) lo scan "correggeva" del 9 % il blu della laguna. Se gli oggetti neutri
  mancano (spiaggia) o si contraddicono tra i fotogrammi, lo scan lo dice e non propone niente. Si applica solo se lo chiedi: `grade-apply.py --wb` (guadagni dello scan)
  o `--wb-gains R,B` (tuoi), massimo ±12 %. Sulle tre clip vere: D-Log2 e Nano gia' neutre (scarto 1,3 % e 0,5 %), D-Log da spiaggia senza oggetti neutri.
- Un frame con pochi neri veri (laguna luminosa) ha il 1° percentile alto: non e' un errore, non si segnala.

## Il gusto di Jacopo (24/10/2026): meraviglioso, non realistico
Jacopo vuole **esaltare la bellezza dei posti**, non rappresentare la realta': preferisce il suo grading veloce (acqua e cielo ciano molto vividi, "quasi finti")
al naturale. Il suo grading e' stato misurato su due clip (acqua e cielo saturazione x1,9-2,3, pelle x1,2, pelle a 34-42 IRE, immagine piu' morbida della camera)
e il look `jacopo-cinema` ne impara i colori con una **mappa colore** (`assets/looks/jacopo-chroma.npz`, 17^3 celle) sopra il contrasto cinema. `jacopo-cinema-wow`
li esaspera (x1,5). Verificato su fotogrammi non usati nell'allenamento: errore di colore dal suo grading dimezzato rispetto al look a manopole (2,9/2,6 -> 1,4/1,4 su 255).
Limite: la mappa conosce solo i colori delle sue due clip (589 celle su 4913); gli altri colori (rossi, gialli, interni) restano come li lascia il look.
`--smooth 1|2` aggiunge una leggera riduzione del rumore prima della LUT (il suo grading e' piu' morbido della camera: nitidezza 0,37 contro 0,52).

## Il look scelto e come si usa su una clip nuova (24/10/2026)
Dopo V1-V5 Jacopo ha scelto **`jacopo-cinema-wow`**: i suoi colori molto spinti su acqua e cielo, **pelle "piu' viva"** (saturazione pelle laguna 0,57; la
variante `jacopo-cinema-wow-pelle-media` e' piu' sobria), contrasto cinema. Ricetta per ogni clip log nuova, in quest'ordine:
1. `grade-scan.py --video clip --out scan` (profilo dal tag DJI; sulla Nano "probabile" e confermato dall'immagine). Guarda `REPORT.md` e la proposta di esposizione.
2. `grade-apply.py --video clip --scan scan/report.json --out out --look jacopo-cinema-wow --smooth 1` (senza `--render` = solo anteprima), poi con `--render`.
   **Dal 27/10 il look predefinito e' `pellicola-oro`** (vedi "Il grading professionale" piu' sotto): stessa ricetta con `--look pellicola-oro`.
   **Reel montati (28/10, reel Zanzibar):** sull'intero reel pellicola-oro sembrava "un po' flat". Sopra il look, al montaggio, va una curva a S
   `curves=all='0/0 0.25/0.21 0.5/0.5 0.75/0.79 1/1',eq=saturation=1.12` ("decisamente meglio"). Giudicare il colore su fotogrammi a piena
   risoluzione: la copia 480p per il telefono appiattisce.
   Su clip corte con acqua veloce (scia, schiuma) il controllo "file uguale all'anteprima" puo' fallire (3,5 IRE) senza un vero difetto:
   i momenti misurati cadono su fotogrammi diversi. Guardare il file invece di rifarlo.
3. Il controllo `CHECK.md` deve dire PASS. Se la pelle o il mare non convincono, si regola con `--stops` o si scelgono le varianti del preset.
Nota: la mappa colore e' stata appresa solo sulle sue due clip (acqua, cielo, pelle, rosso): su scene con altri colori (interni, verdi, gialli) il WOW agisce solo con
il secondo passaggio di colore e va guardato prima di fidarsene.

## Il grading professionale (27/10/2026): pipeline pellicola, match tra clip, look da riferimento
Nato da cinque video d'ispirazione di Jacopo (travel film Tokyo/Dolomiti/canyon, "the power of color grading" Hawaii/Tokyo/sott'acqua, Dolomiti):
"mi piace la grana, l'effetto film, colori belli senza essere esagerati". Copie locali in `videos/inspo-grading/` (fuori da GitHub).

**Cosa avevano in comune (misurato):** luci dorate (R+12/+21, B−20/−32), bianchi che arrivano al bianco, neri profondi (1° percentile 5-8),
ombre neutre o teal, cielo verso il ciano. Il nostro `jacopo-cinema` faceva il contrario: luci leggermente fredde, ombre magenta, e sulla laguna
le luci ferme a 189/255 (nuvole grigie). La causa non era la LUT DJI (sul Pocket le clip non arrivano nemmeno alla sua spalla) ma l'esposizione
come guadagno *dopo* la LUT. Sulla Nano invece la LUT D-Log M e' quasi una retta senza spalla: li' serve una spalla nostra.

**I cinque pezzi:**
1. **Pipeline pellicola** (`scripts/grade-film.py`, look con la chiave `film`, es. `pellicola-oro`): esposizione e bianco in luce lineare,
   contrasto attorno al grigio medio, le luci piu' forti di ogni clip portate verso il 95 % (misurate una volta per clip, a partire da 1 stop sopra
   il grigio cosi' la pelle non si sposta), spalla morbida che non brucia mai, luci dorate con **acqua e cielo protetti dalla maschera colore**
   (senza maschera il turchese diventa verde), densita' del colore. LUT DJI + grading in UNA sola tabella (meta' del lavoro).
2. **Match tra clip** (`grade-match.py`): esposizione (ancora pelle) e dominante portate a meta' strada verso il gruppo, max 0,3 stop e 3 %.
   Il match pieno e' stato provato e scartato: spegneva la laguna e ingrigiva un muro caldo.
3. **Correzioni mirate:** cielo sfumato (`finish.sky_grad`, scurisce l'alto del quadro piu' sulle zone chiare) e soggetto piu' luminoso
   (`skin_luma`), entrambi spenti di default; maschera pelle e acqua gia' esistenti.
4. **Finitura** (`finish`): alone sulle luci forti, grana ingrandita (la grana della pellicola e' piu' grande di un pixel 4K), vignetta.
   Costo: ~10 s ogni 3 s di 4K in piu' (una clip di 40 s ~7 min). Il cielo sfumato con `geq` per pixel costava 48 s al secondo: ora la
   sfumatura si disegna su una copia 2x64 del fotogramma e si ingrandisce.
5. **Look da riferimento** (`grade-ref.py`): misura luci/ombre/neri/contrasto/colore sui fotogrammi che piacciono e sposta il look al 60 %.
   Le tinte si misurano solo su cio' che la scena non colora da se' (la prima prova scambiava l'acqua turchese per "ombre teal").
   **Mai copiare il prima/dopo di un creator come LUT:** il loro log non e' il nostro DJI (luci viola, pelle scura, provato).

**Ricetta per un video con piu' clip:** `grade-scan.py` su ogni clip → `grade-match.py --clip A=scanA --clip B=scanB --out match` →
`grade-apply.py --video A --scan scanA --out outA --match match/match.json --look pellicola-oro --smooth 1` (anteprima, poi `--render`).
Verificato: render della spiaggia D-Log 4K, il file coincide con l'anteprima (0,4 IRE), nessuna luce bruciata.

**Cosa il grading non puo' fare (lo fa Jacopo in ripresa):** luce dell'ora d'oro, bilanciamento del bianco fisso (non automatico), filtro ND
per il mosso del cinema (tempo di scatto circa il doppio dei fps). E' meta' del look dei video che gli piacciono.

## Limiti noti (da non scordare)
- Una clip dove la pelle e' scura e il mare e' chiaro (es. D-Log, 23/10) non si schiarisce abbastanza: le luci non lasciano margine. Servirebbe una **maschera locale** o un
  **roll-off morbido delle luci**: non fatti.
- Il bianco corretto dagli oggetti neutri e' solo una proposta: un tramonto caldo o un'ombra blu non sono dominanti. I Kelvin scelti in camera (`WhiteBalanceKelvin`, `WhiteBalanceTintCc`
  nei metadati) per ora sono solo letti, non usati.
- Nessun "look" (caldo mediterraneo, filmico...) e' ancora stato scelto: quando si fa, con il test A/B alla cieca della skill.

## Verificato su
Tre clip vere di Jacopo (23/10/2026): Pocket 4P D-Log (11,6 s), Pocket 4P D-Log2 (30,7 s), Osmo Nano D-Log M (9,2 s, arena al chiuso). Il file renderizzato coincide con la
previsione entro 0,2 IRE. Le clip stanno in `videos/_grade-test/` (fuori da GitHub).

## Stabilizzazione (27/10/2026, prima prova su clip Nano camminata, 41 s)
Si stabilizza **dopo** il grading, sul file graduato (stessa risoluzione: le trasformazioni misurate sul log valgono pari pari). Due passaggi ffmpeg (vidstab):
1. `ffmpeg -i clip-log.mp4 -vf "vidstabdetect=shakiness=6:accuracy=15:stepsize=6:result=transforms.trf" -f null -` (4K, ~8 min su 41 s)
2. `ffmpeg -i graded.mp4 -vf "vidstabtransform=input=transforms.trf:smoothing=25:optzoom=1:interpol=bicubic,unsharp=5:5:0.4:3:3:0,format=p010le" -c:v hevc_nvenc -preset p6 -rc vbr -cq 18 -b:v 0 -tag:v hvc1 -c:a copy stabilizzato.mp4`
- `smoothing=25` (1 s a 25 fps) tiene le panoramiche volute e toglie il saltellio del passo; `optzoom=1` = zoom fisso minimo, niente bordi neri (~10-15 % di crop).
- Misurato (vidstabdetect ascii, `fileformat=1`, su copie 960 px): scatti verticali -65 %, orizzontali -40 %. Il mosso (motion blur) dei fotogrammi resta: la stabilizzazione non lo toglie.
