# personale/ — privato

**Scopo:** materiale personale non legato a un progetto (vita, letture, famiglia, viaggi). Il canale YouTube ora sta in `social/`.

**Contenuto**
- `vita/` — letture, Mandal-Art set→dic 2026, pannello studio (`pannello-studio.json`)
- `look-jacopo/` — riferimenti di stile e foto
- `reel-corsica/`, `reel-zanzibar/`, `reel-zanzibar-2/` — reel di viaggio per amici e famiglia
- `compleanno-papa/` — quadretto di compleanno
- `stampa/` — versione da stampare della Mandal-Art

**Colore dei reel travel "The Jacopo Grossi"** (dal 21/11/2026)
- Tre look a disposizione: `pellicola-oro` (youtube-edit, caldo e dreamy), `look-jacopo` (il suo colore Mimo) e la skill **`color-grade`** (`.claude/skills/color-grade/`), che copia il look di un film o di foto di riferimento. Ha 20 look pronti, i fotogrammi da TMDB, l'export .cube e il video senza sfarfallio.
- Ordine fisso: prima la LUT DJI (log → Rec.709), poi `color-grade` sul file già convertito. Mai sul log grezzo.
- Prima l'anteprima (`video.py --preview`) con il foglio prima/dopo, poi `--mode full` per il render finale. `fast` va bene solo per le bozze.
- Mai sui video YouTube: lì si fa solo D-Log → 709.

**Convenzioni**
- Esami e studio: il materiale vero sta in `studio-privato/` (solo locale).

**Non fare**
- Il repo è pubblico: non aggiungere qui foto, misure o documenti sensibili senza prima metterli in `.gitignore`.
- TODO: da compilare (decidere se `personale/` esce dal tracciamento git).
