# Loghi (per le plate: riferimento al prodotto nominato nel video, mai come marchio dell'autore)

| File | Origine | Colore | Preso il |
|---|---|---|---|
| `claude.svg` | Simple Icons | arancio Claude `#D97757` | prima del 01/11/2026 |
| `canva.svg` | Simple Icons | (vedi file) | prima del 01/11/2026 |
| `chrome.svg` | Wikimedia Commons, "Google Chrome icon (February 2022)" | colori ufficiali (rosso/giallo/verde/blu) | 01/11/2026, via Playwright |
| `pinterest.svg` | Simple Icons (`pinterest.svg`) | rosso ufficiale `#BD081C` | 01/11/2026, via Playwright |

Come se ne aggiunge uno: Playwright (`browser_navigate` all'URL dell'SVG, poi `browser_evaluate` con `XMLSerializer` per leggerlo) da Simple Icons (`cdn.jsdelivr.net/npm/simple-icons@latest/icons/<nome>.svg`, monocromatico: dargli il colore del marchio in `fill`) oppure da Wikimedia Commons quando serve il logo a colori. Mettere il file qui e aggiungere una riga a questa tabella.
