# Plate plan: the sentence-by-sentence table Jacopo approves

_Read when planning a video that has motion plates (every YouTube video with full-frame explainers). From the teardown of Joseph's video (01/11/2026):
his system never builds a scene before the plan is approved, and the plan is one line per sentence. We do the same, in chat, before the storyboard._

## 1. The plan table (goes in `BRIEF.md`, shown at Checkpoint B before the storyboard)

One row per sentence of the script that gets a plate. A sentence with no row stays on the face.

| # | Time | Sentence (spoken) | Job of the plate | Idea (one line) | Format | Anchor word(s) | Face |
|---|---|---|---|---|---|---|---|
| 1 | 0:03 | "Premiere, After Effects, CapCut..." | name -> logo | five logos, one per name, then they fall on "opzionali" | chips / trail | each name | PiP |

- **Job of the plate** is one of: *name* (a logo/object), *process* (steps), *metaphor* (an abstract idea), *number* (a count, a time, a price), *comparison* (A vs B),
  *avoid* (what not to do: struck through), *proof* (the real prompt/result on screen), *map* (where we are in the video), *emphasis* (the one sentence that must land).
  If you cannot name the job, the plate is decoration: drop it.
- **Idea** is what the viewer should *understand*, not how it looks. The look comes from the preset.
- **Anchor word(s)** are the words the elements enter on (they become `data-anchor`, and `beat-check.py` proves them).
- Jacopo answers each row with **Approva / Cambia: <what he wants>**. A change is written the way he says it, not translated ("farli combattere, con effetti stile anime" is an idea, not a format).
  The first idea is rarely the best: when Jacopo describes a stronger one, that one wins and the difference goes in `NOTES_LOG.md`.
- Then the **static storyboard** (stills of each plate with the PiP drawn, `format-still.py`) is approved a second time before any motion is rendered.
  Joseph approves the static drafts "almost always on the first look" because the plan was already right: the plan is where the thinking happens.

## 2. Where plates go (placement rules)

1. Name spoken -> its logo/object appears on that word (not before).
2. Abstract idea -> a metaphor plate (`diagram`), three to five objects, one strong colour behind.
3. A number -> `counter` (value counts up as it is said); a part of a whole -> split bar.
4. Two things compared -> `versus`, side by side.
5. A step of a process -> `tracker` at every chapter change (~3 s), so the viewer always knows where they are.
6. Something done on a computer (a prompt, an approval, an answer) -> `uiplane`, redrawn, with the hand cursor.
7. What the viewer should not do or no longer needs -> struck through and dimmed (`diagram` strike), not removed.
8. The one sentence that must land -> `herotitle` (46); the face stays on screen through the hook.
9. The face comes back every 20-40 s; when a plate lasts longer than ~12 s, split it or let the face breathe in the PiP.
10. When the creator waits, is surprised or works: a cutaway of him (checklist for shooting), never stock.

## 3. Revisions with a timecode

Jacopo can dictate notes to Claude in his own words (e.g. with a dictation tool), one per moment: `0:06 il titolo più in basso`, `0:14 il whoosh più forte qui`,
`0:21 più zoom out sulla CTA`, `li metterei uno a destra e uno a sinistra, proprio una comparison`. Procedure:
1. Apply each note to that second only; show the changed window, not the whole video.
2. One line per note in `NOTES_LOG.md` (date | his words | where the rule was rewritten | new wording).
3. If the same correction comes twice (e.g. "zoom out, not zoom in"), it is not a one-off: **rewrite the rule** in `taste.md` or the format's spec so it is right next time.
4. If he keeps correcting the same thing after the rule is saved, it is his taste: save it as taste (`taste.md`), not as a bug.
