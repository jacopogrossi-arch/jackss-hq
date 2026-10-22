# Notes log

Ogni nota di Jacopo che cambia una regola della skill finisce qui, con la regola che è stata RISCRITTA.
Il registro serve a una cosa: quando una nota nuova contraddice una vecchia, la vecchia si riscrive, non si accumula
sotto una seconda. Una riga per nota.

Formato: `data | la nota (parole di Jacopo) | dove sta la regola riscritta (sezione di SKILL.md o file) | nuova formulazione in breve`

Procedura (la stessa di "Keeping the skill yours" in `SKILL.md`):
1. Correggi il video su cui sei.
2. Chiediti: "quale regola, se fosse esistita, avrebbe evitato questo errore?" e trovala (cerca la parola chiave con grep).
3. RISCRIVI quella regola perché copra anche questo caso. Non aggiungerne una seconda accanto. Se due regole ora dicono la stessa
   cosa, uniscile; se una contraddice quella nuova, quella vecchia sparisce. Se nessuna regola calza, aggiungi UNA riga corta
   nella sezione più vicina.
4. Aggiungi una riga qui sotto.
5. Fai una nuova bozza, controllala (`check-frames.py`, `qa-motion.py`) e mostrala.

Esempio (cancella quando hai righe vere): `2026-10-15 | l'ultima parola della frase è tagliata | Cut stage, "Edges" | il taglio finisce quando il suono dell'ultima parola è davvero finito, più un margine minimo`

## Registro

2026-10-22 | (revisione con lo starter kit del Claude Code Club) regole su suono e musica accumulate: "Earlier rule" accanto alla nuova, "mai un suono su un testo" accanto a "un suono su OGNI testo", tre livelli di musica, un default (`--db -14`) che non esisteva più | SKILL.md, sezione Sound e Sound iteration | una sola regola: un suono piccolo su ogni testo, pop sui logo, click sui tag, swish con la camera, whoosh solo per transizioni e grafiche; musica a 13-15 dB sotto la voce con i default veri degli script (`add-music --db -3`, `mix-audio --music-db -7`); tolta la ricetta ffmpeg a mano
