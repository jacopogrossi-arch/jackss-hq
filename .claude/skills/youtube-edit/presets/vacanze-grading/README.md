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
3. Il controllo `CHECK.md` deve dire PASS. Se la pelle o il mare non convincono, si regola con `--stops` o si scelgono le varianti del preset.
Nota: la mappa colore e' stata appresa solo sulle sue due clip (acqua, cielo, pelle, rosso): su scene con altri colori (interni, verdi, gialli) il WOW agisce solo con
il secondo passaggio di colore e va guardato prima di fidarsene.

## Limiti noti (da non scordare)
- Una clip dove la pelle e' scura e il mare e' chiaro (es. D-Log, 23/10) non si schiarisce abbastanza: le luci non lasciano margine. Servirebbe una **maschera locale** o un
  **roll-off morbido delle luci**: non fatti.
- Il bianco corretto dagli oggetti neutri e' solo una proposta: un tramonto caldo o un'ombra blu non sono dominanti. I Kelvin scelti in camera (`WhiteBalanceKelvin`, `WhiteBalanceTintCc`
  nei metadati) per ora sono solo letti, non usati.
- Nessun "look" (caldo mediterraneo, filmico...) e' ancora stato scelto: quando si fa, con il test A/B alla cieca della skill.

## Verificato su
Tre clip vere di Jacopo (23/10/2026): Pocket 4P D-Log (11,6 s), Pocket 4P D-Log2 (30,7 s), Osmo Nano D-Log M (9,2 s, arena al chiuso). Il file renderizzato coincide con la
previsione entro 0,2 IRE. Le clip stanno in `videos/_grade-test/` (fuori da GitHub).
