# Inspiration library: references analysed *with the why*

_Read when choosing which plate to build for a sentence, and when Jacopo sends a new video to learn from. Joseph's rule (01/11/2026): a reference is
not "the font and the colour": it is **why this graphic arrives on this word and how it moves to help the viewer follow**. So every reference here is
stored as a table `word -> graphic -> job`, plus the measured numbers, not as a folder of screenshots._

## How to add a reference (about 20 minutes)
1. Download it into `videos/_teardown/<name>/` (local only, outside git).
2. `scripts/teardown.py --video ... --out ... [--transcript words.json]` for the numbers (cuts, loudness, words per minute) and extract a frame every 3-5 s (contact sheets with the timestamp), denser (2 fps) on the interesting moments.
3. Transcribe it (faster-whisper; with `av` 19 pass the audio as a numpy array, not the path).
4. For every graphic write one line in the table below: **time, the words being said, the graphic, its job**.
5. Write the rules that come out of it (what to copy: the *logic*; what not: palette and fonts that are the creator's signature) in `taste.md`, and the new formats in `formats.md`.
6. Keep the long write-up in the repo (`personale/youtube/inspo-<name>.md`), not here: this file only keeps the index and the shortest useful table.

## Index
| Reference | Date | What it taught | Where |
|---|---|---|---|
| Joseph (Content AI Academy), "Ho automatizzato completamente il montaggio video con Claude" (11:49, 16:9) | 01/11/2026 | the 7-step system, the "plate has a job, lands on the word" logic, formats 47-51, taste section 9 | `personale/youtube/inspo-motion-plates-joseph.md` |
| Ali Abdaal (motion plates + PiP face) | 28/10/2026 | the face PiP on every plate | `formats.md`, Explainers |
| Iman Gadzhi, Callaway, Pedro Andrade, Marshall Crew, @realskytan | 19-23/10/2026 | build / annotate / orbit / dive / agenda, dot grid, outline rail | `studio.py`, `formats.md` |

## Word -> graphic -> job (Joseph, 01/11/2026; the short version)
| Time | Said | Graphic | Job |
|---|---|---|---|
| 0:03-0:09 | "Premiere Pro, After Effects, CapCut, DaVinci, Final Cut... sono diventati opzionali" | five logos land one per name (0.5 s apart), then fall blurred on "opzionali" | name + emphasis |
| 1:00-1:20 | "pensa a Claude come un cervello... gli servono delle braccia" | brain node, inputs with dashed lines, prompt pill, crossed-out tools, arm + Remotion connected | metaphor |
| 1:50 | "...il design di Claude base, uguale a tutti" | a cream/serif/terracotta card (the default look) | avoid / before |
| 2:15-2:30 | "analizzare sia quello che si vede sia quello che viene detto" | a grid of 164 video thumbnails, each with a waveform under it and a tick | proof (the work done) |
| 2:30-2:40 | "su quale parola entra e come si muove" | a waveform with the word circled and handwritten notes ("sale e frena") | proof (shows the principle on real data) |
| 3:25 | "camera, scena, clip" | three 3D icons named exactly; two blur out | name + avoid |
| 4:05-4:35 | "propone cosa mostrare... se mi convince la tengo" | the plan UI: the sentence, the idea, Approva / Scrivi qui, the cursor clicking | proof (interface) |
| 7:10-8:10 | "Queste indicazioni gli do con Wispr Flow" | revision list with timecodes, a dictation widget, keyboard shortcuts floating (what he avoids) | proof + avoid |
| 8:25-8:30 | "circa 10 cartelle con più di 1000 sound effects" | counter 507 -> 1000+, folders filling to 100 | number |
| 9:00-9:50 | "quanto tempo serve" | seven cards, a time chip under each as it is said, then a table | number + map |
| 9:50-10:10 | "due cose importanti" | "2 COSE" on the face, then a split bar: 30 min mine inside 1h40 | number + emphasis |
| 10:35-10:45 | "quattro ore di montaggio... cinque in parallelo" | a 4 h ruler, then five videos on the same span | number |
| 10:45-10:55 | "gli editor non apriranno più Premiere" | the opening logos return in a dock, the cursor clicks Claude | map (bookend) |
| 11:15-11:45 | the course list | a vertical line, each item lights up as it is named, preview on the right | list / CTA |
