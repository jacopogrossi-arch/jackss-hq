# SOP: explainer 3D animato (formato "serpentone Autogrill")

*Nata il 13/11/2026 dal video "Perché in Autogrill non si va mai dritti?" (v2.2, approvato da Jacopo: "veramente ottimo").*
Kit di codice: `formats/explainer3d/` (motore + prodotti + vegetazione + mix). Esempio completo: `formats/explainer3d/esempio-autogrill/`.

**Che cos'è.** Un video verticale/orizzontale di 60–100 s: una voce racconta una curiosità ("perché succede X?") mentre la camera attraversa **un unico mondo 3D in stile cartoon**: edifici senza tetto, oggetti riconoscibili, etichette che spuntano sulle parole giuste. Niente riprese, niente generazione video AI: tutto è codice (Three.js dentro HyperFrames), quindi ogni fotogramma è controllabile e rifacibile.

**Quando usarlo.** Un posto o un processo spiegabile "dall'alto" (un negozio, una fabbrica, un atelier, una sfilata, la filiera di un capo). Serve un luogo fisico da attraversare. Per la moda: il percorso di un capo dal tessuto al negozio, com'è organizzato un flagship, perché i saldi sono messi in fondo, ecc.

---

## 0. Le regole d'oro (dai feedback di Jacopo)

1. **Il primo secondo decide tutto** (Instagram). La voce parte entro 0,35 s, la camera è già in movimento al fotogramma 1, il titolo-domanda è a schermo da subito, un whoosh + un colpo d'apertura e un riser che culmina sulla prima battuta forte. Mai un'intro vuota.
2. **Gli oggetti devono sembrare quello che sono.** Un salame ha la rete e la fetta con i grassi, una scatola di biscotti ha il marchio e il disegno dei biscotti, un'auto ha passaruota, vetri e cerchi. Mai un cilindro marrone. Texture "come in Blender", stile cartoon.
3. **Inquadrature strette sui prodotti** quando la voce li nomina: devono leggersi in un telefono.
4. **Musica bassa, effetti presenti.** Musica circa 13 dB sotto la voce, più giù mentre si parla; effetti sonori fitti (pop, swish, whoosh).
5. **Musica scelta ogni volta**, mai la solita traccia di default.
6. **Contorno ricco.** Bosco profondo, alberi con chiome irregolari, siepi, colline nella nebbia: è quello che rende il mondo credibile nelle inquadrature da fuori.
7. **Niente sfarfallii** (vedi §8, "z-fighting").

---

## 1. Idea e copione (30 min)

- Una **domanda** come titolo ("Perché in Autogrill *non si va mai dritti*?") e una **risposta-colpo** entro 5 s ("È colpa del *pavimento*.").
- Struttura: gancio → contesto/storia (date, nomi) → il meccanismo spiegato camminando nel luogo → il trucco svelato ("percorso obbligato travestito da negozio") → chiusura ironica che riprende il titolo.
- 180–230 parole = 80–95 s. Frasi brevi, una parola chiave per frase (sarà l'etichetta).
- Segna nel copione le **parole-ancora**: ogni oggetto ed etichetta apparirà esattamente su quella parola.

## 2. Voce

- Voce generata (connettore Epidemic Sound voiceover o simili) in mp3, poi **tempi parola per parola** in `voce/transcript.json` (lista di `{text, start, end}`).
- In `video.py`: `LEAD = 0.35` (attacco), `BREAKS` = pause aggiunte dopo le parole che chiudono un paragrafo (0,4–1,1 s), `TAIL` ≈ 3 s per il finale. La funzione `at("parola", n, dopo_secondi)` restituisce il tempo video di una parola: **tutto il video si aggancia a `at()`**, mai a secondi scritti a mano.

## 3. Storyboard prima del 3D

- Una tabella frase per frase: cosa si vede, dove sta la camera, quale etichetta o scritta. Poi uno **storyboard a fotogrammi** (contact sheet di snapshot) da far approvare a Jacopo prima di qualunque render (`esempio-autogrill/storyboard-autogrill.jpg`).
- Un solo mondo continuo: la camera non "taglia", vola. Esterno (arrivo in auto, panoramica) → il tetto si toglie → dentro, ad altezza persona lungo il percorso → dettagli stretti → si riesce fuori.

## 4. Costruire il mondo

Copia `formats/explainer3d/` nella cartella del progetto (es. `D:\videoeditor\<nome>\`) e lavora lì: la skill non si tocca.

| File | Cosa ci metti |
|---|---|
| `base-world3d.js` | motore base **bloccato** (commit 043948d della skill). Il `world3d.js` attuale della skill va in conflitto (`const hash`): non sostituirlo |
| `engine-extra.js` | oggetti speciali: auto (`car`), strada/parcheggio (`road`), pavimento, varchi, lampioni |
| `products.js` | il **kit prodotti**: `ctex()` disegna texture su canvas; `K(nome)` restituisce un prodotto (salame, parmigiano, vino, biscotti, panettone, peluche, macchinina, lecca-lecca…); `PLAN` dice cosa va su quale ripiano; `shelf2()` costruisce lo scaffale con testata e insegna |
| `scenery.js` | **vegetazione**: `tree` (alberi "eroe" vicini, con ombra), `forest` (centinaia di alberi instanced in un'area), `hedge`, `hills` |
| `make_engine.py` | unisce tutto in `vendor/world3d.js` e registra i tipi nuovi. **Rilancialo dopo ogni modifica ai .js** |
| `store.py` (esempio) | la pianta del luogo in metri: muri, banconi, scaffali, percorso `PATH` |
| `video.py` (esempio) | la regia: oggetti, camere (`w.cam`), etichette 3D (`w.label`), scritte (`ov`) |

**Per un tema nuovo (es. moda):** aggiungi in `products.js` le texture (`TX`) e i prodotti (`K`): capi piegati, grucce, rotoli di tessuto, scatole di scarpe, cartellini. Stesso metodo: forma semplice + texture disegnata con i dettagli che fanno riconoscere l'oggetto (cuciture, etichette, trama). Prova ogni oggetto nella pagina di laboratorio (`lab2.py`) prima di metterlo nel video.

Numeri usati:
- Alberi: 18 "eroe" + 8 laterali + 4 boschi (520 + 150 + 150 + 420 alberi), siepi da 22 cespugli, 7 colline.
- Ombre: `shadows`, `bias -0.0006`, `normalBias 0.04`, mappa 4096.
- Erba con texture (`tex="grass"`), nebbia per profondità, cielo al tramonto in CSS.

## 5. Camera ed etichette

- La camera parte **bassa e già in corsa** accanto all'oggetto protagonista (l'auto rossa), con ease "out" fino alla prima parola-ancora.
- Mosse ≥ 0,8 s ricevono un whoosh automatico (`sfx.py`). Dentro, ad altezza occhi (1,1–1,6 m); sui prodotti, 0,7–1,0 m dallo scaffale.
- Etichette: `w.label(oggetto, posizione, "testo con *parola* evidenziata", t=at(...), out=at(...))`, max 2–3 a schermo, sempre con uscita.
- Scritte grandi (`ov`): titolo, numeri (*1977*), la morale. 84–150 px.
- Contatori e dissolvenze vanno scritti come **funzione del tempo** (evento `hf-seek`), mai con timer: il render salta tra i fotogrammi.

## 6. Controllo visivo prima del render

```bash
python make_engine.py
python video.py
npx hyperframes snapshot page --at 0.05,1.2,10,29,45,60,68,80 --no-end -o snaps-prova --timeout 120000
```
Leggi il contact sheet. Controlla in particolare il primo fotogramma, le inquadrature da fuori sugli scaffali e il finale. Per lo sfarfallio prendi **3 fotogrammi consecutivi** (es. 29.0, 29.017, 29.033): se qualcosa cambia tra l'uno e l'altro, è z-fighting.

## 7. Suono

**Effetti** (`sfx.py`, dalla libreria della skill `assets/sfx/`):
- Apertura: `cc-zoom-whoosh` a 0 s + `impact-bass-1` + `cc-riser-lungo` **allineato al picco** sulla battuta forte + `cc-impact` lì.
- Eventi del racconto: auto che sfrecciano (`es-swoosh-wide`), tetto che si alza (`whoosh-cinematic`), contatore (`es-number-counter`), campanello alla cassa (`chime`), impatto sulla rivelazione, `es-reverse-glass` alla ripartenza.
- Automatici: pop sulle etichette, swish sulle scritte, whoosh sulle mosse di camera. Mai due suoni a meno di 0,35 s, mai sopra un evento fisso.
- Effetti +5 dB rispetto alla prima prova (erano bassi).

**Musica e mix** (`mix.py`):
- Traccia scelta per il video (licenza Epidemic, solo locale).
- `BED = 13` dB sotto la voce **misurati in LUFS**, sidechain (threshold 0.05, ratio 3), poi guadagno **fisso** fino a −16 LUFS e limiter 0.89.
- Mai `loudnorm` dinamico a passata singola: alza la musica nelle pause ed è il motivo della "musica esageratamente alta" della v2.

## 8. Trappole (già pagate)

| Sintomo | Causa | Rimedio |
|---|---|---|
| Sfarfallio sotto gli scaffali o sull'espositore | due facce sullo stesso piano (z-fighting) | rientra i pezzi interni (`Li = L - 0.08`), fianchi un po' più grandi, mai facce complanari |
| Scritte di etichette al contrario | la faccia del cilindro guarda indietro | `rotateY(Math.PI)` sulla geometria |
| Tavoletta/scatola orientata male | la texture è disegnata in verticale | ruota la geometria (`rotateX(-π/2)`) e il testo nel canvas |
| Fiocco del peluche sembra una ciambella | toro | due sfere schiacciate |
| Colline come dune color sabbia | colori caldi + nebbia | verdi-blu scuri (`#2c4a3a`, `#34543f`, `#284236`) |
| `make_engine.py` fallisce l'assert | il motore della skill è cambiato | usa `base-world3d.js` bloccato |
| QA dice "nero 0,15 s alla fine" | è la dissolvenza finale voluta | ignorare |

## 9. Render e consegna

```bash
bash finish.sh draft      # 1080p 30 fps + QA: lo guarda Jacopo
bash finish.sh final      # 1080p 60 fps, tag BT.709, copia leggera <= 30 MB
```
- Il master (~250 MB) va in iCloud Drive › Video Claude con **numero di versione nel nome** (`-v2.2`): se sovrascrivi con lo stesso nome, sul telefono sembra il file vecchio.
- La copia leggera (x264, ~28 MB) per inviarlo in chat.
- Salva il progetto con git nella sua cartella (render, mp4, wav e snapshot nel `.gitignore`).

## 10. Checklist finale

- [ ] Fotogramma 1: camera in movimento, titolo, suono.
- [ ] Battuta-risposta entro 5 s, con impatto.
- [ ] Ogni prodotto nominato si riconosce in un'inquadratura stretta.
- [ ] Nessuno sfarfallio (3 fotogrammi consecutivi nei punti a rischio).
- [ ] Musica diversa dall'ultima volta, ~13 dB sotto la voce; effetti udibili; −16 LUFS.
- [ ] Contorno: bosco, siepi, colline visibili nelle inquadrature da fuori.
- [ ] Draft approvato prima del final; versione nel nome del file.

Tempo reale del primo video: dal 12/11 sera al 13/11 pomeriggio (v1 → v2.2).
