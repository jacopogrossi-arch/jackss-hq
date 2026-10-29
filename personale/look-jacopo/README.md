# Look Jacopo (DJI Mimo)

Il colore che Jacopo fa da solo in DJI Mimo, misurato il 29/10/2026 su 6 sue clip di Zanzibar (export Mimo confrontati con gli originali).
**Il suo workflow:** "recupero colore" (Mimo converte il log in Rec.709), poi esposizione e luminosità un po' giù, contrasto, saturazione e vividezza un po' su. Bianchi e neri non li tocca a mano.

**Cosa ne esce** (rispetto alla LUT DJI V2.0):
- neri più profondi, bianchi pieni e toni medi più bassi;
- saturazione circa x1,2, con i caldi più vivi;
- il mare spinto a occhio, clip per clip;
- bianchi neutri, niente grana, alone o vignetta.

È diverso da pellicola-oro (caldo, crema, grana, "dreamy"). Sono due look per contesti diversi: nel reel Zanzibar #2 Jacopo ha scelto pellicola-oro per la canzone lenta.

| File | Cosa fa |
|---|---|
| `coppie.py` | Abbina ogni export Mimo alla clip originale e al punto d'inizio, confrontando i contorni → `coppie.json` |
| `misura.py` | Luce, saturazione per zona, bianchi e nitidezza per ogni coppia → `misure.json` |
| `impara.py` | Primo tentativo: polinomio libero (scuriva i tramonti, scartato) |
| `ricetta.py` | Ricetta a manopole regolata sui suoi export Pocket D-Log → `ricetta.json`, `look-jacopo-ricetta.cube` (da applicare DOPO la LUT DJI) |

Gli script si lanciano da `videos/look-jacopo/` (locale): lì ci sono gli export (cartella iCloud "FILE X CLAUDE_"). La ricetta da sola non indovina quanto spingere il mare: va ritoccata clip per clip.
