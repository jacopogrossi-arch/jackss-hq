# Video #6 — "L'influencer AI in ritardo di due anni"

**Status: 🟡 struttura visiva definita 01/07/2026 — cold open aggiunto, da generare**

Durata: ~29-30s (aggiornata da ~24s per il cold open) | Lingua: italiano | Formato: 9:16 vertical

---

## Concept

Prima uscita dalla formula "fake brand lookbook ad" usata in #3/#4/#5. Niente lookbook, niente brand fittizio come demo del servizio Lookbook, niente reveal del processo di Jacopo — Jago con un claim polarizzante, non una vetrina.

**Perché questo angolo (deciso in sessione 01/07/2026):**
- I video #3/#4 (stesso format lookbook ripetuto) hanno bassa retention (#4: avg view 4s, 2% supera i 10s) — al terzo giro il pubblico lo legge come pubblicità, non contenuto.
- Ricerca 2026: la pura spettacolarità (output AI) non basta più a trattenere l'attenzione — vincono i formati dove il personaggio ha un punto di vista riconoscibile (claim polarizzanti, non solo show-reel).
- Prima tessera del mix deciso: **~30% contenuti esperto / ~70% virale-broad**. Questo video apre il fronte "virale-broad" — Jago con un'opinione, non una vetrina.
- Claim scelto: gli **influencer AI** (non solo "AI" generica) — cavalca un trend riconosciuto più ampio della nicchia AI+moda, e Jago stesso ne è la prova vivente, senza bisogno di dimostrarlo.
- Target del claim: brand che non hanno ancora un volto AI — non tocca fotografi/designer (restano dalla parte di Jago), punta il dito sui ritardatari.

**Evoluzione visiva (stessa sessione, dopo revisione):** lo script era pronto ma la resa era 4 clip di talking head quasi statico — rischio "video fermo", scartato da Jacopo. Aggiunto un cold open narrativo con un secondo personaggio, un'azione fisica e un reveal, per dare un hook visivamente forte prima ancora che Jago parli.

---

## Apertura — Cold open "reveal a sorpresa" (nuovo, 01/07/2026)

Tre shot prima dell'inizio dello script originale. Meccanica: sembra un vero spot pubblicitario fino a quando Jago non lo interrompe fisicamente — solo uscendo dalla scena si scopre che era un set.

| Shot | Tempo | Contenuto |
|---|---|---|
| **A — Falso spot** | ≈0-2.5s | Un personaggio nuovo (il "Talent", non Jago) recita dritto in camera: *"L'artigianalità non si può replicare con un computer."* Deve sembrare a tutti gli effetti uno spot vero e finito — sfondo pulito/sfocato, luce alta chiave, nessun indizio di troupe o set. |
| **B — Cazzotto** | ≈2.5-4s | Jago entra a schermo e lo colpisce. Taglio secco **prima** del contatto visibile — si vede il movimento, non l'impatto (sicurezza policy Instagram + resa più affidabile su Seedance). |
| **C — Reveal + match cut** | ≈4-6.5s | La camera arretra mentre Jago esce dalla scena: si rivela tutta l'attrezzatura da studio (luci, riflettori, camera su treppiede, monitor, cavi) — era un set, non un ambiente reale. Nello stesso movimento di uscita, taglio sul suo ingresso nell'atelier vero (match cut sul movimento) — **è qui che parte la linea Hook.** |

**Perché funziona:** il contrasto luce piatta/alta chiave del falso spot (mondo pubblicitario tradizionale, patinato, impersonale) contro il chiaroscuro caldo dell'atelier (mondo di Jago, personale, autoriale) fa il lavoro tematico prima ancora che parta la prima parola di Jago. Il pugno non è gratuito — è la rottura fisica tra i due mondi.

### Personaggio nuovo — "il Talent"

- Ruolo: spokesperson generico di uno spot — rappresenta il mondo della pubblicità tradizionale, non un brand reale
- Look proposto, **volutamente opposto a Jago**: capelli chiari e corti, carnagione chiara, camicia bianca o pastello semplice, aspetto curato e convenzionale da "spot pubblicitario" — contrasto totale con capelli scuri mossi/carnagione olivastra/full black di Jago
- **Spec bloccato 03/07/2026** (vedi `talent-reference-prompt.md`): archetipo "testimonial da spot", biondo cenere brizzolato alle tempie (leggermente più maturo di Jago = mondo pubblicitario vecchio), occhi azzurri, rasato. Scartata l'idea del volto-sosia: rischio likeness su Higgsfield/Instagram
- Illuminazione Shot A: alta chiave, piatta, pulita — l'opposto del chiaroscuro drammatico dell'atelier
- **Nota tecnica:** personaggio nuovo e ricorrente per 2 inquadrature consecutive (A e B) — serve una reference lock via `banana-pro-director` prima di generare i prompt Seedance di questi shot, per garantire continuità del volto tra le due clip

### Ambientazioni nuove

- **Falso set spot (Shot A):** backdrop pulito/sfocato, alta chiave, nessun elemento da studio visibile — deve leggersi come location reale di uno spot
- **Soundstage rivelato (Shot C, prima metà):** stessa location di Shot A ma inquadrata più larga — luci su stativi, riflettori, camera su treppiede, monitor, cavi a terra
- **Atelier (Shot C, seconda metà + resto del video):** invariata, vedi `reference_sfondo_jago` — nessun asset nuovo da generare

---

## Script voiceover (finale, timing aggiornato)

| Beat | Tempo | Voiceover |
|---|---|---|
| Cold open A | ≈0-2.5s | *(Talent)* "L'artigianalità non si può replicare con un computer." |
| Cold open B | ≈2.5-4s | — (nessun dialogo, solo azione) |
| Cold open C | ≈4-6.5s | — (nessun dialogo, reveal + match cut) |
| **Hook** | ≈6.5-11.5s | *"Il tuo brand non ha ancora un influencer AI. Sei già indietro di due anni."* |
| **Build** | ≈11.5-19.5s | *"Tu stai ancora valutando un casting. Io ho già la campagna pronta."* |
| **Provocazione** | ≈19.5-25.5s | *"So già chi non sarà d'accordo. Chi vive ancora di shooting tradizionali."* |
| **Firma** | ≈25.5-30.5s | *"Tra due anni sarai ancora indietro. Stavolta saprai perché."* |

La Firma chiude il cerchio sull'hook (i "due anni" tornano) — effetto a tenaglia invece di una semplice uscita. La battuta del Talent ("l'artigianalità non si può replicare") viene smentita in diretta dal resto del video: è Jago, generato al 100% con AI, a "vincere" la scena.

**Regole rispettate:** nessuna domanda retorica, nessuna lista "zero X zero Y" (scartata in revisione perché già usata in altri script), nessuna CTA esplicita tipo "commenta X" — chiude lasciando la palla allo spettatore-brand.

---

## Produzione

- **Tool talking head (Hook/Build/Provocazione/Firma):** Magnific Seedance (M1 Narrative) — confermato 01/07/2026 al posto di Kling Avatar: testato su Video #5, Seedance batte nettamente Kling per i talking head di Jago (vedi `feedback_kling_vs_seedance_talkie`)
- **Tool cold open:** Shot A e C in M1 Narrative, Shot B (cazzotto) in **M3 Action** — modalità diversa per l'unica azione fisica del video
- **Sfondo atelier:** vedi `reference_sfondo_jago` in memoria — invariato, nessun asset nuovo
- **Ambientazioni cold open:** da generare ex novo (falso set spot + soundstage) — non riusano l'atelier
- **Personaggio Talent:** reference lock da generare con `banana-pro-director` prima dei prompt Seedance di Shot A/B
- **Match cut Shot C:** probabile gestione in due clip separate (uscita dal soundstage + ingresso in atelier) tagliate a stacco in CapCut, salvo che Seedance regga la transizione in un'unica generazione continua
- **Montaggio:** CapCut, tagli secchi tra i beat, caption a schermo sincronizzata sull'hook
- **Scope aumentato rispetto al piano originale:** non più "zero immagini nuove" — ora serve 1 reference personaggio + 2 ambientazioni nuove prima di generare i video

---

## Asset

| Asset | Stato |
|-------|-------|
| Reference "Talent" (banana-pro-director) | 🟡 prompt pronto 03/07 — vedi `talent-reference-prompt.md`, da generare in Magnific (Nano Banana Pro, 3:4, 2k) |
| Prompt Seedance Shot A (falso spot) | ⬜ da generare — dopo lock Talent |
| Prompt Seedance Shot B (cazzotto, M3) | ⬜ da generare — dopo lock Talent |
| Prompt Seedance Shot C (reveal + match cut) | ⬜ da generare |
| Prompt Seedance Hook/Build/Provocazione/Firma | ✅ generati con `cinema-worldbuilder-pro` — vedi `video-6-prompts.md` (timing da rinominare, contenuto invariato) |
| Clip Shot A (Seedance) | ⬜ |
| Clip Shot B (Seedance) | ⬜ |
| Clip Shot C (Seedance) | ⬜ |
| Clip Hook/Build/Provocazione/Firma (Seedance) | ⬜ da generare in Magnific |
| Caption a schermo | ⬜ da impaginare in CapCut |
| Montaggio CapCut | ⬜ |
| Caption Instagram + hashtag | ⬜ da scrivere (max 5 hashtag, vedi `feedback_ig_caption_rules`) |
