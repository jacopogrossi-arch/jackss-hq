# Mappe colore dei look

`jacopo-chroma.npz`: una griglia 17x17x17 (rosso, verde, blu del segnale gia' graduato) con, per ogni colore, di quanto spostare la
crominanza (Cb, Cr) per ottenere il colore del grading veloce che Jacopo ha fatto a mano il 23/10/2026 sulle due clip della laguna (D-Log2)
e della spiaggia (D-Log). Appresa dalle coppie di fotogrammi (originale / graduato da lui), ammorbidita e ridotta verso zero dove i
dati sono pochi: i colori che nelle sue clip non compaiono restano come li lascia il look (celle popolate: 589 su 4913).
Verifica: su fotogrammi mai visti in allenamento l'errore di colore dal suo grading scende da 2,9 / 2,6 (look a manopole) a 1,4 / 1,4 (su 255).
Si usa col parametro `chroma_map` di un look (`presets/vacanze-grading/preset.json`), con `chroma_gain` per esagerare (1,0 = come il suo).
Solo la crominanza: la luce (contrasto, neri) la decide il look cinema.
