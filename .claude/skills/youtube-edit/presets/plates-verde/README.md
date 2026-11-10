# Preset `plates-verde` — motion plate su verde con griglia

**È il preset predefinito di `compose.py` dal 01/11/2026** (nessun `--preset` = plates-verde; `--preset none` = look vecchio con ciano/blu fissi; `--preset elegante-portfolio` = look portfolio). `legacy_swap` ridipinge ciano, magenta, ambra e blu fissi dei formati più vecchi nella palette verde/oro/menta. Il `style` dello storyboard vince sempre sul preset.

## Cos'è
Le **motion plate** (scene grafiche a tutto schermo, vedi `references/formats.md` → Explainers) su **verde profondo con griglia blueprint**, parola-chiave
in **oro**, spunte/connettori/barre in **verde menta**. Nato il 01/11/2026 dal teardown del video di Joseph (`personale/youtube/inspo-motion-plates-joseph.md`):
prendiamo la *logica* (una plate per idea, ingresso sulla parola che la nomina), non il suo blu elettrico. Font identici al preset `elegante-portfolio`
(Inter + Playfair Display Italic), quindi i due preset si possono alternare nello stesso canale.

**Palette: scelta da Claude, confermata da Jacopo il 01/11/2026 ("il verde va benissimo").** Variante D "verde vivo" del lab `videos/_bench/plates-verde/lab/`
(A bosco, B nero caldo + griglia verde, C ibrido, D vivo, E medio). Le altre restano come alternative.

## Palette
| Ruolo | Valore | Nota |
|---|---|---|
| Fondo plate | `#0A2B1E` | verde bosco profondo; sul fondo due aloni `#17613F` (in basso al centro, in alto a sinistra) |
| Griglia | `rgba(120,235,180,.13)`, passo 80 px | linee da 1 px; si può far scorrere del 3-4% perché non ci siano fotogrammi morti |
| Testo | `#f4efe6` avorio | |
| Parola chiave | `#e3c47f` oro, Playfair Display Italic | una per frase al massimo |
| Verde menta | `#5EE6A8` | spunte, connettori, barre di avanzamento, bottoni "fatto" |
| Card | avorio `rgba(244,239,230,.95)` su testo nero caldo | numero della card in menta scuro |
| Plate interfaccia | nero caldo `#121110` | chat, piano, finestre: due fondi, come nel video di Joseph (blu + grigio carbone) |
| Errore / da non fare | `#e0645c` | solo per il barrato |

**Regola d'uso del colore (verde su verde):** sul fondo verde la parola-chiave è **oro o avorio**, mai verde; il menta si usa per strutture e stati.
Su nero caldo (plate interfaccia) la parola-chiave può essere menta.
**Niente riquadro con la faccia nelle plate** (Jacopo, 04/11/2026, `taste.md` 9e). Il token `ring` (menta `#5EE6A8`) resta per un PiP voluto apposta (`formats/pip.py`).

## Formati preferiti (nuovi, 01/11/2026)
`tracker` (47: mappa dei passi con spunte che torna ai cambi di capitolo), `counter` (48: valori che salgono sulla parola + barra divisa),
`versus` (49: confronto sempre affiancato), `diagram` (50: metafora con linee tratteggiate, barrato per ciò che non serve più),
`uiplane` (51: interfaccia ridisegnata in 3D con manina che clicca). In più `trail`, `build`, `annotate`, `line`.
Da evitare (come in elegante-portfolio): `halo`, `chip`, `image`. Moduli in `formats/` (`plates_base.py` per le parti comuni); prove senza pipeline: `scripts/format-still.py`.

## Regole di gusto
- Una plate per idea; ogni elemento entra **sulla parola che lo nomina** (`data-at` + `data-anchor`, lo verifica `beat-check.py`).
- Parola-chiave nel corsivo serif; mai etichette piccole in maiuscolo spaziato, mai linee sotto i titoli (restano nel "vietato sempre").
- La plate è a tutto schermo senza faccia; le grafiche accanto alla faccia a tutto schermo non coprono mai il volto (`taste.md` 9c).
- Interfacce **ridisegnate**, mai screen recording grezze; manina 3D che arriva e preme.
- Confronto = sempre affiancato; numeri = contatori vivi, non testo fermo.
- Ciò che non serve più si **barra e si abbassa** (strike + opacità .4), non sparisce.
- Il resto delle regole (movimento, transizioni, suoni) è quello di `references/taste.md` e di elegante-portfolio.

## Test e limiti
- 11 test nuovi in `scripts/tests/test_plates.py` (forma, ancore parlate, seek-safety, nessun suono, guardia PiP).
- Verificato con still a risoluzione piena (`format-still.py`) su 5 formati con il PiP disegnato: nessuna grafica nell'angolo.
- **Provato con HyperFrames il 01/11/2026** su una finestra reale (16,5 s del Video #2, `videos/_bench/plates-verde/ab/`): `compose.py --preset plates-verde` + `npx hyperframes check` (0 errori,
  contrasto 28/28 AA, un solo avviso: l'ultima riga a schermo 0,94 s perché la finestra finisce lì) + render 1080p bozza in 57 s. Render di controllo senza faccia: nell'angolo del PiP l'indicatore YMAX
  resta 80 (max 86) durante la plate, quindi nessuna grafica ci entra. `qa-motion.py` ha trovato il diagramma troppo fermo tra una parola e l'altra: aggiunti i trattini che scorrono sui connettori.
- **A/B alla cieca con la catena 3D (27b), 01/11/2026: vince il verde "decisamente meglio, di una spanna"** (Jacopo), ma "voglio più movimento di camera". Dati: la prima versione aveva 32 % del tempo in movimento e 0,7 scatti ogni 10 s (A: 56 % e 5,2); con la camera di `plates_base` (deriva + scatti ai momenti chiave + scatti di riempimento) 86,6 % e 5,2 scatti, pausa massima 0,53 s. Joseph: 63-66 % e 4,8.
- Il suono non c'è nei formati (Jacopo scarta i pop): per i tracker/diagram un whoosh morbido a ogni cambio, come nel resto della skill.

## Look avorio sui formati vecchi (01/11/2026)
`look: "ivory"` nel preset: tutti i formati vecchi di `compose.py` (liste, statistiche, barre, pipeline, hub, equazione, muro, flow, lente, dock, titolo mascherato, mazzo, pillole, chat, ricerca, tag, catena 3D) portano card avorio piene, testo scuro in Inter 800, parola chiave in corsivo serif, menta per gli stati, niente neon. Vedi `formats/look_ivory.py` e `references/formats.md` ("The ivory look on the older formats").

## Suono smooth e camera su tutto il motore (01/11/2026)
`sound.smooth: true` nel preset: i formati vecchi di `compose.py` hanno uno swish morbido Epidemic per ogni cosa che appare e i formati a tutto schermo hanno deriva lenta + scatti di camera. Misurato sullo zoo: da 51% a 94% del tempo in movimento. Vedi `references/formats.md`.
