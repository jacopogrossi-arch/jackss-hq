# Preset `elegante-portfolio` — primo tipo di montaggio di Jacopo

Per usarlo: `compose.py --preset elegante-portfolio` oppure `"preset": "elegante-portfolio"` nello storyboard. Il `style` dello storyboard
vince sempre sul preset (si possono cambiare singoli valori per un video).

## Cos'è
Video lunghi su YouTube (moda, progetti): sfondo scuro caldo, **Inter** per quasi tutto, **Playfair Display Italic** per le parole chiave,
oro + smeraldo + avorio (**palette confermata il 20/10/2026**, variante A). Il lavoro di Jacopo (pagine del portfolio, figurini) è il protagonista: le pagine non
appaiono e spariscono, ma si muovono nello spazio e portano a una freccia.

## Formati preferiti
`trail` (pagina ferma → camera indietro → freccia → parola chiave), `gallery` → `trail`, `orbit` (card con loghi), `build` (asset uno alla volta),
`annotate` con `follow` (figurino con camera che segue le frecce), scritte in basso, `stats`.

## Regole di gusto (dai pareri di Jacopo, 19/10/2026)
- **Niente** anello `halo` attorno alla testa e niente slide a lamelle (`image`): linguaggio da verticale TikTok/Reels o statico.
- Il primo testo non è una domanda: è quello che dice. Niente termini tecnici che il pubblico non serve (es. "MCP"); loghi al posto delle parole.
- Parole chiave nel corsivo serif; su scene a sfondo unico **glow e sfumature**, mai bande o chip bianchi dietro le etichette.
- Una pagina resta ferma qualche secondo, poi camera indietro e freccia (`trail`); la camera non si ferma mai; una scena explainer finisce
  subito dopo l'ultima etichetta letta.
- Lo zoom con rivelazione (`dive`) deve essere velocissimo (sotto il secondo) o non va usato.
- Sottotitoli: a frasi e scritte chiave, accendibili per video; mai parola per parola su video lunghi.
- Lavorare su finestre piccole (`window-patch.py`) e mettere nel video solo ciò che è approvato.

- Transizioni e suoni (Jacopo, 20/10/2026): flash, whip, zoom-blur, light leak, film burn (glitch, shake e dip SCARTATI da Jacopo il 20/10/2026), pochissimi: solo nel passaggio da una
  scena all'altra (la transizione copre il cambio: il picco cade sul primo fotogramma della scena nuova, `"scene": id`), mai viso → effetto → stesso viso (max ~1 al minuto); ogni transizione porta il suo suono (`assets/sfx/cues.json`), le grafiche che entrano un
  whoosh morbido; musica leggera sotto la voce. Vignetta e grana molto leggere come finitura.

## Pareri sul video #2 (Jacopo, 20/10/2026, pagina Notion "COMMENTO VIDEO 2") — regole salvate
- **Suono su ogni testo:** ogni volta che compare un testo a schermo (scritta in basso, voce di lista, etichetta, freccia, logo) parte un piccolo suono (`tick`, `pop`); un `click` su ogni etichetta di capitolo; un whoosh morbido a ogni mossa di camera nello spazio 3D. Il motore lo fa da solo (`compose.py`, `sub_cues`), con filtro anti-sovrapposizione (due suoni a meno di 0,28 s: resta il piu' forte). Livello preset 1,0 (a 0,7 erano "bassi e pochi").
- **Gancio:** riser (tensione) che segue la voce, immagini del concept con glow dietro e zoom lento (`gallery` con `glow`, `zoom`).
- **Etichette dei capitoli piu' grandi** (`tags[].size` 1.45) e col click. Piacciono: scritta + pallino.
- **Scritta chiave con `typewriter`** (campo `typewriter: true` nel beat `line`) e suono di battitura.
- **Mai una scena ferma tra due voci** (retention): se tra due elementi passano piu' di ~3 s, inserire movimento (pillole sulle parole, un'altra scena, camera) o spezzare la scena. Ravvicinare le voci, non allungarle.
- **Scene "motion graphic" = una sola scena continua**, non due formati in sequenza: i loghi e le frasi entrano come nodi di un unico `trail`, la camera si sposta a ogni passo (Claude -> Canva -> pagina; Claude -> Chrome -> naviga sul web -> Pinterest). "Poco fluide e coese, mancano di ritmo" = tagli tra formati diversi.
- **Coerenza di stile:** tutte le grafiche nei colori del preset (oro/smeraldo, Inter + Playfair Display Italic; `style.theme_legacy`). Per "fatto bene / fatto male": STESSA lista, colori opposti (`tone: good` verde con spunte, `tone: bad` rosso con croci), mai due stili diversi.
- **Font:** niente maiuscolo grassetto per le etichette del figurino (`annotate`): Playfair Display Italic per il testo, Inter per il sottotitolo.
- **Film burn e light leak:** piacciono molto, "qualche transizione in piu'" (`max_per_minute` 2, almeno ogni ~30 s su un vero cambio di scena); il film burn un filo piu' basso (`hit` 0,38).
- **Musica lo-fi** sotto la voce (`add-music.py`, lofi-02): Jacopo ha chiesto di "aggiungerla" anche se la bozza v1 l'aveva a -14 dB: probabilmente non si sentiva; ora -11.

## Riferimenti
Video analizzati: Iman Gadzhi, Callaway, Pedro Andrade, Marshall Crew, Reel "edited by Claude" (note in `videos/test-dji/inspo-analisi/ANALISI.md`).
Font di esempio di Jacopo: corsivo serif ad alto contrasto (logotipo CleanMyMac) → Playfair Display Italic.

## Come si aggiunge un nuovo preset (nuovo tipo di montaggio)
1. Jacopo manda 2-4 video di riferimento del nuovo stile.
2. Per ognuno: estrarre MP3 e fotogrammi, trascrivere a finestre, `teardown.py` (tagli, burst, loudness, parole al minuto), guardare i fotogrammi nei momenti chiave e annotare parola ↔ grafica.
3. Proporre palette, font, formati (esistenti o nuovi), transizioni, livello suoni, sottotitoli; costruire un lab con finestre di 10-20 s e raccogliere i pareri.
4. Salvare `presets/<nome>/preset.json` + `README.md` con le sue regole di gusto; i formati nuovi vanno nel motore (`formats/`), non nel preset.

## Palette
Confermata: **A** — sfondo `#0b0907` (nero caldo, bagliore oro in basso e verde a sinistra), testo avorio `#f4efe6`, accento oro `#d4af5f`, secondo accento smeraldo `#4aa585`.
Provate e non scelte (restano come riferimento per altri preset): **B rame** (`bg #0f0816`, `bg2 #2a1238`, accento `#e08a3c`, `#f2b479`, crema `#fbe5c8`) e **C denim** (`bg #070a14`, `bg2 #18265a`, accento `#9db4ee`, oliva `#a3a85a`, osso `#ece6d6`).
