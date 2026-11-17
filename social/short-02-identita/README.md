# Short #2: "Il nome del mio brand ha tre significati"

**Costruito in autonomia la notte del 13/11/2026** (Jacopo: «hai carta bianca»). Rivisto con Jacopo il 14/11: v2 approvata per il 4K (non ancora pubblicato).
9:16, ~72 s, tutto 3D (three.js + HyperFrames), voce clonata ElevenLabs "Jacopo Prova", musica «locomotivate» – Auxjack (Epidemic).
**Video correlato:** il #4 (https://youtu.be/aPDByKvlb5c), di cui questo Short è un ritaglio: il nome Inverso spiegato in tre significati.
**File finiti:** iCloud › Video 3D moda › `short-tre-significati-v2-4k.mp4` (2160×3840, 60 fps) e `-v2-leggero.mp4` (la v1 della notte resta lì come storico). Progetto di lavoro: `videos/_bench/short2/` (solo locale).

- **Copione e regia:** `script.md` · **Brief di partenza:** `BRIEF.md`
- **Sorgenti:** `src/`: build.py (camera, oggetti, etichette, testi, pillola), room.py (lo studio), mix.py (suono), finish.sh (bozza/finale), transcribe.py (words.json)
- **Oggetti 3D nuovi:** `.claude/skills/youtube-edit/assets/vendor/atelier-studio.js` (totem di cubi-lettera, pannello dritto/rovescio, stender fast fashion, orologio, scatole e sneaker, diagramma a terra, Roma di notte, finestra crittall, libreria, sughero, palette, terrazzo)
- **Procedura:** `.claude/skills/youtube-edit/references/short-3d-sop.md`

## Scena nuova (perché gli Short non siano tutti uguali)
Short #1 = l'atelier di giorno. Short #2 = **lo studio di Inverso di notte**: pareti verde bosco, pavimento in terrazzo, finestra in ferro nero su Roma illuminata, lampade calde, libreria, sughero con le card, la palette del brand al muro. Stesso linguaggio (mappa aerea a stazioni, macro, etichette agganciate, frasi grandi, pillola di fase), oggetti tutti nuovi.

## Titolo e descrizione (proposta)
**Il nome del mio brand ha tre significati #shorts**

> Il mio brand si chiama Inverso, e il nome nasconde tre significati.
> Uno: il rovescio del capo, cioè come è fatto davvero. Per questo ti mostro il mio: ore di studio, errori, costi.
> Due: il contrario della fretta. Un capo per volta, in mesi e non in settimane.
> Tre: né l'ostentazione di chi ha, né il flexing di chi non ha.
> Sono uno studente, non ho niente da venderti: sto documentando tutto.
> Come ho creato l'identità del brand (logo, palette, nome) 👉 https://youtu.be/aPDByKvlb5c
> #moda #brand #fashiondesign #menswear #shorts

## Revisione notturna (giri di snapshot e bozza a 10 fps)
| Giro | Trovato | Corretto |
|---|---|---|
| s2a | parola orizzontale non entra nel 9:16, etichetta tessuta specchiata, asterischi nelle card, tavolo bruciato | totem verticale, etichetta specchiata giusta, luce/esposizione |
| s2b | t-shirt di taglio (sembrano assi), filo del pantalone fino al soffitto, sneaker "spillatrice", logo del dischetto rovesciato, badge visibili fuori dalla mappa, card "tela" | t-shirt a ventaglio, gruccia senza filo, sneaker a loft (suola dalla sagoma, tomaia a sezioni), badge per ogni mappa, card "v1 cartamodello" |
| s2c–e | diagramma sotto le macchie di luna, striscia coperta dal tappeto, chi ha / chi non ha sopra i dischi, scatole tagliate | diagramma spostato su un tappeto bosco, push-in finale sul logo, camera delle scatole arretrata |
| bozza 1 (10 fps, 9 fogli) | etichetta tessuta capovolta, card del sughero piccole, orologio e scatole inquadrati male, diagramma lontano | etichetta ruotata di 180°, card più grandi, camera più bassa sul diagramma, asse più lungo |
| bozza 2 + s2h | scatole ancora piccole con mezzo quadro vuoto | camera del terzo tuffo più vicina: le scatole riempiono il quadro |

QA bozza: −16 LUFS, picco −1,4 dB, nessun fotogramma congelato.

## Revisione di Jacopo (14/11/2026) → v2
| Nota di Jacopo | Corretto |
|---|---|
| All'inizio il **logo** invece della scritta, per farlo ricordare | insegna nera laccata col logo (`logosign`) che si gira all'apertura e di nuovo sull'ultima frase |
| Il **rovescio** non sembrava un pantalone ma un pezzo di stoffa | pantalone rimodellato da zero: dritto con cinturino, passanti, tasche a filo con bottone in corno, pences, piega; rovescio con cuciture aperte rifinite a macchina, sacchi tasca, fascia interna ruggine, etichetta tessuta e di lavaggio, orli; quello "sbagliato" con bordi sfilacciati e fili liberi |
| Sul sughero «ore di studio» tagliata | testo dei cartellini che si rimpicciolisce finché entra; card spostate |
| Troppi pop | un solo pop basso quando appare un cartellino (salta quelli a meno di 0,4 s) |
| Riser a ~1:01 bruttissimo | riser lungo dell'Autogrill (`cc-riser-lungo`) |
| (bozza 5) «v1» del sughero che sfarfalla | due cartellini sovrapposti sullo stesso piano (z-fighting): ogni card ora sta 2,5 mm sopra la precedente |
| (revisione a 10 fps) tavolo buio poi luce di colpo all'arrivo del primo tuffo | la lampada che sparisce al volo della camera spegneva anche la sua luce: ora sparisce solo il paralume |
