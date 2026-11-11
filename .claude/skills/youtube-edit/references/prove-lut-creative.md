# Prove LUT creative — 09/11/2026

Test di tutte le LUT creative che abbiamo sul PC, su girato vero del **Pocket 4P**, per capire quali usare sopra la conversione DJI.
**Stato:** indoor quasi deciso (due finaliste), outdoor rimandato a un'altra sessione.

## Come è stato fatto
- Catena: **LUT tecnica DJI** (D-Log o D-Log2 → Rec.709, dallo scan di `grade-scan.py`) → esposizione dello scan → **LUT creativa sopra il Rec.709**.
- Le LUT che leggono direttamente il log (adimology, nic-lowkey) vanno invece **al posto** della LUT DJI.
- Fotogrammi di prova:
  - **Indoor** (Video 3, D-Log): `0186` stanza di mattina, `0196` stanza di pomeriggio
  - **Outdoor** (Zanzibar): `0034` mare (D-Log), `0028` capitano, pelle e cielo (D-Log), `0008` arco di bouganville (D-Log2)
- Prima i fogli di confronto al 100% (138 LUT), poi due video di confronto con le finaliste **al 70%**.
- Tutto in locale: `videos/_grade-test/lut-creative/`
  - `fogli/`: un foglio per pack per fotogramma
  - `FINALISTI-indoor.jpg` e `FINALISTI-outdoor.jpg`
  - `CONFRONTO-indoor.mp4` e `CONFRONTO-outdoor.mp4`, più le copie `-telefono`

## Pack provati
| Pack | Dove | Esito |
|---|---|---|
| cine-luts-2 (12, Rec.709) | `assets/packs/cine-luts-2/` | indoor ottime; outdoor girano il turchese in blu profondo |
| Hollywood (67) | `D:\download\MASTER BUNDLE\...\LUTS COLLECTION\HOLLYWOOD LUTS` | molto forti, molte schiacciano i neri: usarle al 50-70% |
| Cinematic Effects (32) | MASTER BUNDLE, `CINEMATIC LUTS` | per lo più dominanti forti (verde, viola, azzurro) |
| Acid Colors (20) | MASTER BUNDLE | **scartate**: effetti psichedelici, non grading |
| Thermal | MASTER BUNDLE | non provate (effetto termico) |
| adimology P4P (5, log) | `assets/looks/external/adimology-p4p/` | su D-Log2 quasi nere (fatte sulla curva D-Log) |
| FreeVisuals Tropical, nic-lowkey | `assets/looks/` | nella media, nessuna spicca |

## Indoor — scelta di Jacopo (09/11)
Le due che gli piacciono di più, nel confronto al 70% contro `pellicola-oro`:
- **SINGULARITY** (cine-luts-2): pelle calda, viso con più contrasto, muro pulito.
- **VISIBLE CARBON** (cine-luts-2): la più contrastata, viso scolpito, ombre profonde.

Le altre provate e non scelte: FILMIC, The Irishman, Spotlight.
**Da fare:** scegliere tra le due (A/B alla cieca su una finestra del prossimo video parlato) e decidere la dose (70% o diversa). Poi si valuta se diventa il look predefinito per i video YouTube indoor al posto di `pellicola-oro`.

Comando (al 70%):
```
python grade-apply.py --video clip.MP4 --scan DIR/report.json --out DIR --look-cube "assets/packs/cine-luts-2/SINGULARITY.cube" --look-mix 0.7
python grade-apply.py --video clip.MP4 --scan DIR/report.json --out DIR --look-cube "assets/packs/cine-luts-2/VISIBLE CARBON.cube" --look-mix 0.7
```
Aggiungere `--render` quando l'anteprima va bene.

## Outdoor — rimandato
Finaliste viste al 70%, tutte «molto carine» per Jacopo, senza una scelta:
- **Doctor Strange**: turchese acceso, cielo pulito, pelle calda.
- **Uncut Gems**: turchese, un po' più contrastata.
- **Jumanji**: turchese, più calda.
- **Spider-Man FFH**: la più vivida, da cartolina.

Da riprendere in un'altra sessione partendo da `CONFRONTO-outdoor.mp4`.

## Note
- Nei confronti `pellicola-oro` non aveva vignetta e grana: è stato confrontato solo il colore.
- Le LUT dei pack sono a uso personale: restano in locale, mai su GitHub (le cartelle sono in `.gitignore`).

## Indoor — scelta sul Video #4 (11/11/2026)
- Jacopo ha scelto **VISIBLE CARBON al 35%** per il Video #4 (stanza, Pocket 4P D-Log2), dopo aver visto 50/70/80/100: «la 50 mi è piaciuta di più, però abbasserei ancora», poi «35». Al 100% è un teal and orange pieno (pelle arancione, muro verde-acqua). SINGULARITY scartata in questo giro.
- **Catena usata:** clip 4K a 10 bit → `lut3d` DJI D-Log2→Rec.709 → curva di esposizione per clip (le clip del pomeriggio erano più scure: gamma calcolata sulla luminanza media, corretta ai 2/3) → VISIBLE CARBON miscelata al 35% → primo encode a 8 bit. Il look va messo PRIMA del primo encode a 8 bit.
- **Trappola della miscela con ffmpeg:** in `blend=all_opacity=X` l'opacità vale per il PRIMO ingresso. `[lut][originale]blend=all_opacity=0.35` = 35% di LUT; con gli ingressi al contrario le prove «al 70%» erano in realtà al 30% (errore dell'11/11: Jacopo le trovava «molto leggere»). Controllo: la serie 0/50/70/80/100 deve salire in modo regolare.
- **Mai giudicare la grana su una copia ricompressa:** su una copia 1080p a 8 bit passata da quattro encode la LUT mostra i blocchi della compressione sul muro; dal 4K a 10 bit spariscono. Le prove di look si fanno dalle clip originali.
- **Niente riduzione del rumore temporale** (`hqdn3d`) sul parlato: lascia una scia dietro le mani. A dosi sotto il 50% non serve.
