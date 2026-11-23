# Reel «Sbaglia prima. Taglia dopo.» (24/11/2026) — ripartenza da zero

Sostituisce «Il tessuto non torna indietro» (sospeso: Jacopino parlava in camera, quindi restava lui il narratore).
**Regia:** voce di Jacopo FUORI CAMPO, a UNA persona, imperativo. Jacopino e' un attore dentro la scena: lavora (disegna, cancella, misura, posa le forbici), non guarda mai la camera, mai primo piano frontale (di profilo, tre quarti, dall'alto, mani). Blender only, metodo gemello. 9:16, 24 fps.

## Voce (una frase = una generazione, "Jacopo Prova", eleven_v4, 1 take, 241 crediti, 24/11)
| # | Testo | Durata |
|---|---|---|
| 1 | «Prima di tagliare il tessuto... sbaglia.» | 2.67 s |
| 2 | «Ma sulla CARTA. Disegna il capo, in scala, e cancella finche' non torna.» | 5.13 s |
| 3 | «Poi prendi il metro. Misura due volte.» | 2.72 s |
| 4 | «Una gomma costa zero. Un taglio sbagliato... ti costa il tessuto.» | 4.70 s |
| 5 | «Sbaglia prima. Taglia dopo.» | 2.05 s |
Montata: `videos/_bench/reel-nuovo/vo/vo.wav` = 18.87 s (pause 0.35 / 0.40 / 0.40 / 0.45 s). Locale, fuori da git.

## Perche' cosi' (dai 5 video e dal dossier retention)
- Gancio = affermazione che sorprende, detta a una persona; il plate porta la frase intera, si capisce anche muto (dossier §2).
- Schema regola → come → costo → chiusura (V4 «E se…», V5 «Se tu / Ma / Quindi»); niente numeri da difendere (dossier §2, V3: claim verificabili).
- Una frase per generazione, punteggiatura e UNA parola in maiuscolo (CARTA); nessun tag (voce clonata, tag instabili).
- Loop: l'ultima frase («Sbaglia prima. Taglia dopo.») rima col gancio e il quadro finale = quadro del gancio.

## Mappa a blocchi (camera / azione di Jacopino, mai in camera)
| # | s | voce | camera | Jacopino |
|---|---|---|---|---|
| 1 gancio | 0-2.7 | P1 | bassa, tre quarti, figura intera; forbici aperte sopra il tessuto in primo piano nitido; frame 1 = il problema leggibile | posa le forbici, prende la matita |
| 2 carta | 3.0-8.1 | P2 | spinta lenta, poi stacco dall'alto sul foglio | disegna il pantalone, sbaglia una linea, la cancella |
| 3 metro | 8.5-11.2 | P3 | tavolo, tre quarti dal lato del metro | srotola il metro sul foglio, due passaggi; plate «×2» sul «due volte» |
| 4 costo | 11.6-16.3 | P4 | foglio sbagliato accartocciato, poi spinta alle forbici sul tessuto, pausa 0.4 s | gomma/foglio nel cestino, plate «€0»; avvicina le forbici al tessuto e si ferma |
| 5 chiusura | 16.7-18.9 | P5 | stesso quadro del gancio (loop) | posa le forbici sul tessuto, senza tagliare |

Caption: «mandalo a chi taglia prima di misurare». Suoni: solo swish sui tagli, tick sul plate (Epidemic, locale).
Controlli prima del render: storyboard bassa qualita' → `reel.py --check` a 0 problemi → test 3 s della scena piu' difficile (mani + forbici) → render finale.
