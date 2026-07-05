# Video #6 — "L'influencer AI in ritardo di due anni"

**Status: 🟡 tutti i prompt pronti 03/07/2026 (4 talking head + 4 cold open) — da generare le clip in Magnific**

Durata: ~28s (rivista 03/07: hook recitato in movimento nel cold open) | Lingua: italiano | Formato: 9:16 vertical

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
| **C — Reveal + walk-through** | ≈4-9s | *(rivisto 03/07)* Jago si aggancia all'obiettivo e avanza verso la camera parlando, mentre la camera arretra al suo passo: l'attrezzatura da studio (luci, riflettori, camera su treppiede, monitor, cavi) sfila ai bordi del frame — era un set. A metà passo, taglio sull'atelier: stessa camminata frontale, stessa scala (walk-through transition). **L'hook è recitato qui, in movimento**, e si chiude con Jago che si pianta dietro al worktable. |

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
| **Hook parte 1** (C1, reveal) | ≈4-6.5s | *(Jago, camminando in camera)* "Il tuo brand non ha ancora un influencer AI." |
| **Hook parte 2** (C2, atelier) | ≈6.5-9s | *(Jago, camminando, chiude al worktable)* "Sei già indietro di due anni." |
| **Build** | ≈9-17s | *"Tu stai ancora valutando un casting. Io ho già la campagna pronta."* |
| **Provocazione** | ≈17-23s | *"So già chi non sarà d'accordo. Chi vive ancora di shooting tradizionali."* |
| **Firma** | ≈23-28s | *"Tra due anni sarai ancora indietro. Stavolta saprai perché."* |

La Firma chiude il cerchio sull'hook (i "due anni" tornano) — effetto a tenaglia invece di una semplice uscita. La battuta del Talent ("l'artigianalità non si può replicare") viene smentita in diretta dal resto del video: è Jago, generato al 100% con AI, a "vincere" la scena.

**Regole rispettate:** nessuna domanda retorica, nessuna lista "zero X zero Y" (scartata in revisione perché già usata in altri script), nessuna CTA esplicita tipo "commenta X" — chiude lasciando la palla allo spettatore-brand.

---

## Produzione

- **Tool talking head (Hook/Build/Provocazione/Firma):** Magnific Seedance (M1 Narrative) — confermato 01/07/2026 al posto di Kling Avatar: testato su Video #5, Seedance batte nettamente Kling per i talking head di Jago (vedi `feedback_kling_vs_seedance_talkie`)
- **Tool cold open:** Shot A e C in M1 Narrative, Shot B (cazzotto) in **M3 Action** — modalità diversa per l'unica azione fisica del video
- **Sfondo atelier:** vedi `reference_sfondo_jago` in memoria — invariato, nessun asset nuovo
- **Ambientazioni cold open:** da generare ex novo (falso set spot + soundstage) — non riusano l'atelier
- **Personaggio Talent:** reference lock da generare con `banana-pro-director` prima dei prompt Seedance di Shot A/B
- **Transizione Shot C (rivista 03/07):** due clip (C1 soundstage + C2 atelier) con **walk-through transition** — Jago cammina frontale verso la camera in entrambe, dead center alla stessa scala, taglio a metà passo in CapCut; l'hook è parlato lungo tutta la camminata
- **Clip 1 "Hook" statica eliminata (03/07):** l'hook vive in C1+C2; i talking head al tavolo restano 3 (Build, Provocazione, Firma)
- **Montaggio:** CapCut, tagli secchi tra i beat, caption a schermo sincronizzata sull'hook
- **Scope aumentato rispetto al piano originale:** non più "zero immagini nuove" — ora serve 1 reference personaggio + 2 ambientazioni nuove prima di generare i video

---

## Asset

| Asset | Stato |
|-------|-------|
| Reference "Talent" (banana-pro-director) | ✅ generata 03/07 con Magnific GPT-2 — `talent-reference.png` |
| End frame Clip 1 (Talent che cade, Banana Pro) | ✅ generato 05/07 |
| Prompt + Clip 1 Seedance (Shot A+B fusi, keyframe start+end) | ✅ generata 05/07 — 🟡 migliorabile (ingresso Jago un po' da "guardia"), correzione pronta in `video-6-cold-open-prompts.md` per futuro rigeneration |
| End frame Clip 2 (Jago a piena falcata, soundstage) | ✅ generato 05/07 con Nano Banana Pro |
| Prompt + Clip 2 Seedance (turn + reveal soundstage, hook parte 1 EN) | ✅ generata 05/07 — buona, tenuta |
| End frame Clip 3 (Jago al worktable, atelier) | ✅ generato 05/07 con Nano Banana Pro (manica lunga, verticale nativo) |
| Prompt Clip 3 Seedance (transizione soundstage→atelier, hook parte 2 EN) | ✅ generato 05/07 — da generare in Magnific |
| Prompt Build/Provocazione (atelier, EN) | ✅ in `video-6-prompts.md` |
| Esperimento Firma nel soundstage backstage | ❌ scartato 05/07 — 3 tentativi immagine con problemi di integrazione/prospettiva mai risolti, vedi nota in `video-6-prompts.md` |
| Prompt Firma (torna nell'atelier, riusa end frame Clip 3, EN) | ✅ versione definitiva 05/07 in `video-6-prompts.md` |
| Clip Shot A+B / Clip 1 (Seedance) | 🟡 generata, vedi nota sopra |
| Clip Firma (Seedance) | ✅ generata 05/07 — atelier, worktable |
| Clip 2, Clip 3, Build, Provocazione (Seedance) | ⬜ da generare in Magnific |
| Caption a schermo | ✅ montate in CapCut |
| Montaggio CapCut | ✅ completato 05/07 |
| Copertina IG | ✅ 05/07 — `copertina-varianti/copertina-finale.png` (template magazine del #5, foto Magnific Jago+soundstage, titolo "2 Years Behind") — design Canva: https://www.canva.com/d/pKIL_lCyCo8Qo44 |
| Caption Instagram + hashtag | ✅ scritta 05/07 (inglese, 5 hashtag) — vedi sotto |

---

## Caption Instagram (finale — 05/07/2026)

The ad you saw at the start? Fake. The spokesperson? Never existed. Neither do I — and that's the point.

Your brand doesn't have an AI influencer yet. You're already two years behind.

While you're still weighing a casting call, the campaign could already be done. No studio. No crew. No reshoots.

I'm Jago. 100% AI-generated.

In two years you'll still be behind. This time you'll know why.

#aiinfluencer #fashiontech #artificialintelligence #aifashion #digitalfashion
