# Taste: motion numbers, what never to ship, and how to judge a draft

Distilled on 20/10/2026 from three public repos and re-written for this skill (no text copied):
- **motionmaxxing** by Tejashmakwana (Apache-2.0): measured motion from 53 professional moments, transitions, the "slop" review.
- **motion-video-kit** by echris6 (MIT): motion grammar, quality bar, audio rules, the independent-critic loop.
- **herk-edit-kit** by Nate Herk (no licence stated: ideas only, nothing copied): captions, sound palette, checks, "every note becomes a rule".

These numbers come from launch films and short-form reels, so they are a starting point for a **YouTube talking-head edit**,
not law. A preset (`presets/<name>/README.md`) may override any of them. Jacopo's own notes always win.

## 1. How things move (measured defaults, 30 fps)

| What | Default | Notes |
|---|---|---|
| Slide / scale entrance | 12 f (0.40 s) | p25 6 f, p75 24 f: below 0.2 s is a snap, above 0.8 s is slow |
| Opacity | 6 f (0.20 s) | a fade is a fast event, not a slow one |
| Blur in/out | 7 f (0.23 s) | |
| Exit | 10-14 f | **accelerates into the exit** (ease-in), does not float away |
| Landing | ease-out (58% of real landings) | heavy and certain; leaving is the opposite: speeds up |
| Closing / sign-off elements | 6 f | the end is the most staccato part; hero mark 18-30 f |
| A turn / contrast beat | longest exits (14-16 f) | things are pulled away and replaced |

- **Change speed, never drift at a constant rate:** readable target, fast exit, slow arrival.
- **Everything that moves has a cause.** A scan produces results, a prompt produces an artifact, a button produces a state.
- **Density by hierarchy:** one primary move, supporting staggers on labels/cards, small tertiary details, all overlapping. Do not stop and start the whole frame on every beat.
- **Overshoot only on the fun things** (~10% of moves in hooks/turns, almost none in proof and sign-off).
- **No dead frame:** nothing may sit unchanged for more than ~0.6 s unless it is a payoff hold (a readable list/number, up to 1.0 s; hero up to 1.2 s) or a designed breath (0.6-1.5 s before a payoff, with one living thing on it: slow drift of 3-5%, a caret, a shimmer). `scripts/qa-motion.py` measures it.

## 2. Joins between beats

- **The cut is the join.** Measured films have almost no scene-to-scene crossfades: the cut lands **on motion** (last 3-8 frames of A accelerate), and **B's first frame is already moving or already built**. A fade or dissolve is right only when it *is* the meaning (forgetting, privacy, calm brand voice).
- **Author a cut as a pair:** A's last 6 frames and B's first 6 frames together; something concrete is identical across the cut (position within ~2% of frame, scale, colour, blur, direction).
- **No empty frame** between a dive/zoom and the next scene (put B's first object on screen before A's exit ends; overlap ~2 f).
- **End on a peak** (peak velocity), not a settled frame, except the very last hold.
- **A transition must hide a real change of scene:** it builds on the old scene, peaks on the FIRST frame of the new one (`"scene": "<beat id>"`), and clears on the new scene. Never face -> effect -> the same face, with the actual scene change coming later (Jacopo, 20/10/2026).
- **Our `fx` transitions** (flash, whip, zoomblur, lightleak, burn) dress a cut the edit already makes; the rule above still holds: rare (Jacopo: ~1 per minute), only at scene changes, never mid-sentence.
- **Frame 0 is a finished composition,** not a half-entered word.

## 3. Never ship (delete, do not justify)

1. **Page chrome / HUD:** a brand name in a corner, tracked-caps labels, "02 / 05" counters, timecodes, progress bars, corner brackets. (Our subtitles and the chapter tag are not chrome; they carry spoken content.)
2. **Deck layouts:** a held left-aligned headline block with media on the right, a kicker above a headline, "title then content".
3. **A small card floating on empty ground** for a 1 s read; flat colour swatches as scenes.
4. **Invented proof:** stat walls, made-up numbers or UI passed as real (illustrative content only if plausible and declared in the notes, never as an on-screen disclaimer).
5. **Slogan copy** ("Not just X. It's Y.", "Unlock", "the future of").
6. **A pinned object** at the same coordinates through three or more shots.
7. **A web-footer ending** (logo + tagline + button + URL) held for seconds: a resolved end hold is 0.6-1.4 s and has something alive in it.
8. **An effect to show effort:** a new technique every beat. Use an effect because the idea needs it.

Slide test (30 s): cover all the text with your hand. If more than half the frames are "a flat colour with a card on it", it is a deck: fix the picture, not the type.

## 4. Judgment (what is worth making)

1. **The idea belongs to the subject.** Use what the subject already owns (its real pages, logo, material, verb) and invent only the surroundings. If a competitor's logo swapped in still works, it is a generic film.
2. **The viewer watches something happen** (a consequence, a result) rather than reading a claim in type.
3. **Every beat causes the next:** turn the current object into the next one (a click that floods the frame, a page that becomes the next ground).
4. **Emphasis is spent, not spread:** two sizes doing the work (huge for the one word that matters, small for the rest); one lit thing per frame; endings usually get *smaller* than the climax.
5. **Time breathes:** hold before something matters; stop before the idea is exhausted. Reading time: 1-3 display words 0.5-1 s, a sentence 1.5-2 s, never a paragraph.
6. **It sounds like the speaker:** keep the real phrasing of the voice; silence before a hit is a sound.
7. **One hero per frame:** two panels only if one is at least 2x the other's area or the camera moves between them.

## 5. Talking-head rules worth keeping (from the Herk playbook; ideas only)

- Cut between phrases at real silence, never inside one; keep the natural beat after a comma or "First,". Never speed the voice. Never fade the last spoken word.
- Captions: one look for the whole video (same box/edge); never light text on a light scene (measure the pixels behind it); never over the mouth or chin, least of all in the first second; on text-heavy shots move captions to a clear zone instead of blinking out.
- Every shot moves (real footage, screen recording, animated UI, slow push-in): no frozen frames; video beats still images.
- UI floating small in empty space is the fastest "AI edit" tell: crop and zoom so it fills the panel.
- A raw recording caps the edit: script the hook before recording.
- Encoding segments separately and concatenating drifts lip sync: select exact frames in one pass.

## 6. Sound palette (merged with `references/sound.md`)

- Effects follow **visible actions**: a soft air whoosh on a real spatial move, a damped tap when something lands, a dry click for small UI, paper for documents, one short warm tone for a check. No laser zaps, pitch-drop plops, sci-fi chirps, boomy air-wind whooshes.
- Choose whooshes with little energy below ~150 Hz and a gentle 80-400 ms rise; high-pass ~150-220 Hz, low-pass ~9-11 kHz, click-free fades.
- **Vary the files** for repeated items so a list does not sound like a percussion loop; soften sounds that cluster within ~0.15 s (x0.6).
- Levels are set **per event against the music-only mix** (about +3-4 dB in the effect's own band; never let 2-8 kHz clicks poke out). Full-band loudness is useless for this.
- Music bed 9-14 dB under the voice (ours: `add-music.py --db -14` plus ducking), a limiter on the delivery, true peak at or below -1.5 dBTP, **measure the final encoded stereo file** (a mono file reads 3 dB lower).
- When someone says "that whoosh", first listen to the music-only version at that moment: music snares and risers sound like whooshes.
- Always keep a no-music twin. Change one thing per round and name it by timestamp.

## 7. The critic loop (the builder is not the judge)

Before Jacopo sees a draft, a **fresh reviewer** looks at the real render, not at the builder's story. Prompts are in `references/critic.md`. In short:

1. Build the draft, run `verify-render.py` and `qa-motion.py`.
2. Spawn a fresh agent (Agent tool, general-purpose) with only: the render path, the brief, Jacopo's own words and the preset README. Never give it a list of what you think you fixed.
3. It extracts frames itself (contact sheet every 0.2 s, dense windows around each transition), checks frozen stretches, empty frames, text collisions (including mid-crossfade), and reports ranked defects with timestamps.
4. Fix the biggest gap first; a **second fresh agent** verifies each item FIXED / PARTLY / STILL PRESENT and looks for regressions.
5. Keep a ledger in the project folder (round, critic findings, change, measured result). Two passes is the budget.
6. Jacopo's pass is the final gate: critics measure only what they are asked to; he catches things every check misses.

## 8. Never certify your own work

State what you looked at and quote the numbers. "Verified" without numbers is not a result (a black render was once certified clean). Say plainly what could not be checked (for example: nobody has listened to the sound).


## 9. Rules from the Joseph teardown (01/11/2026)

From `personale/youtube/inspo-motion-plates-joseph.md` (his motion plates, and the way he places them). They sit on top of sections 1-8 and of Jacopo's own notes, which win.
1. **One plate per idea, never to decorate.** Before building one: *what must the viewer understand at this second?* Name -> a logo; process -> a metaphor; number -> a counter;
   comparison -> side by side; what to avoid -> struck through and dimmed.
2. **Land on the word.** An element enters on the word that names it, not before, not after; a list of five names is five entrances ~0.5 s apart.
3. **The key word changes font** (sans -> italic serif, in the key colour); one per sentence at most.
4. **Show the default before the better thing** ("the Claude look" -> our look): the contrast is the argument.
5. **A recurring map in long videos**: the same plate again at every chapter change, state different (done ticked, current lifted).
6. **Redraw interfaces, tilt them in 3D, add a hand cursor**; never a raw screen recording.
7. **Numbers are alive**: counters, chips landing as the number is said, a bar that splits "mine" from "the whole".
8. **What you no longer need is struck through and dimmed**, not removed: leaving carries meaning as much as arriving.
9. **The face is the anchor**: it comes back every 20-40 s to keep the relationship; big text enters at the sides, never over it.
9b. **No twin plates (Jacopo, 03/11/2026: "vedo che usi sempre lo stesso formato")**: the same structure (disc + pills + dashed links) at most once in any ~6 neighbouring plates; the others are different shapes (an ID card, a receipt, a slider, a crowd...), invented in this style. When the line says "l'AI", show the real logo of the tool he means (Claude, ChatGPT), never the letters "AI".
9c. **Graphics beside the full-screen face (Jacopo, 03/11/2026)**: allowed, but rare: 3-4 per video at most, only where they make sense and look good (a name, a number, an object he points at), on the side of the frame away from his head, never over the face. When in doubt, a motion plate with the PiP instead. Put them on the RIGHT of the frame, and hide the PiP square while they are up (the face is already full screen). Cards and boxes on a plate are ivory, not black (Jacopo 03/11: "perché sei ritornato a usare il nero").
9e. **No face PiP on plates (Jacopo, 04/11/2026)**: "leverei il riquadro in basso a destra nelle plate": a plate is full screen with nothing else, the voice runs under it, and when it ends the face comes back full screen. Supersedes the PiP rule (28/10). The only face inside a plate is a deliberate one (the live face in Video #3's ID card).
9d. **Screen recordings stay real (Jacopo, 03/11/2026)**: when he recorded the screen, never redraw it as a graphic. Frame the real recording in a window on the plate, zoomed on the paragraph he is reading (about 1.9x), panning down as he reads; highlights, strikes and ticks go on top at the word's measured pixel position (measure the word boxes on the frame, never guess). Keep the recording's own auto-zooms where they happen. Skip any stretch that shows private files or a forbidden name, and replace just that moment with a graphic.
10. **The video demonstrates what it says**: use the method on screen (real prompt, real result) instead of describing it.
11. **Cutaways of the creator** (at the desk, waiting, surprised) serve the story's emotion; they are not filler. Shoot them with the checklist, not stock.
12. **Notes with a timecode become rules**: "0:14 the whoosh stronger here" is saved in `NOTES_LOG.md` and, when it repeats, in this file (see `plate-plan.md`).
13. **Motion on plates is a fluid camera on one digital board (Jacopo, 04/11/2026; replaces the zoom kicks of 01/11)**: no bounce, no kicks, no overshoot. A run of plates is one big board (formats/board.py): the camera glides with strong easing to what is being named, then pulls back; page to page is an eased swipe to an empty part of the board, never a fade and never a few frames of face in between; face to board is one continuous swipe. A plate starts ON the word that opens it, never seconds before, and it does not hold: after the last element it moves or it ends. Fewer plates: if a plate does not keep the listener attentive, the face is better. Animate the content too (type the prompt in the bar, light each card on its name). Motion is judged only in motion: show a short rendered window before spreading a new motion, stills prove nothing.
14. **The green plates are the look of the whole system** (Jacopo, 01/11/2026, blind A/B on the 16.5 s window of Video #2: "decisamente meglio, una spanna"): preset `plates-verde`
    is the default of `compose.py`; `--preset none` gives the old fixed cyan/blue look back, `--preset elegante-portfolio` the portfolio look.


14c. **Course tests voted (Jacopo, 05/11/2026):** the yes, maybe and no list is `prove-corso.md`; read it before inventing a move, and never propose its "No" items again.

14b. **Scene improvvisate, non formati da catalogo (01/11/2026).** Ogni spiegazione = una motion plate su misura nei canoni di Joseph (vedi `formats.md`, "Scene improvvisate"). Non fermarsi a "quale formato uso"; non rimettere le vecchie grafiche su sfondo verde (Jacopo: "così le migliori" non basta). Le linee tratteggiate compaiono solo quando collegano due elementi già in scena.
