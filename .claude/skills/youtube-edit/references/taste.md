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
- **Overshoot: none on plates and camera moves (13 below, 04/11/2026).** It is allowed only where `formats.md` defines it (the success stamp, "the house's one overshoot"); the old "~10% of moves in hooks/turns" no longer holds.
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
- Music bed level, limiter and true peak: the numbers live only in `sound.md` (Music and the sound report); **measure the final encoded stereo file** (a mono file reads 3 dB lower).
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
9c. **Graphics beside the full-screen face (Jacopo, 03/11/2026)**: allowed, but rare: 3-4 per video at most, only where they make sense and look good (a name, a number, an object he points at), on the side of the frame away from his head, never over the face. When in doubt, a motion plate instead. Put them on the RIGHT of the frame. Cards and boxes on a plate are ivory, not black (Jacopo 03/11: "perché sei ritornato a usare il nero").
9e. **No face PiP on plates (Jacopo, 04/11/2026)**: "leverei il riquadro in basso a destra nelle plate": a plate is full screen with nothing else, the voice runs under it, and when it ends the face comes back full screen. Supersedes the PiP rule (28/10). The only face inside a plate is a deliberate one (the live face in Video #3's ID card).
9f. **Reading time is decided by what he says, not by the gap between elements (Jacopo, 04/11/2026, Video #3 experiment)**: the automatic rule (face back after a plate waits 6.5 s) did not know he was reading answers aloud, and the board zoom cut the text. Mark the reading intervals by hand and keep the whole text on screen for them; no automatic zoom on text he reads; the face only when he comments.
9d. **Screen recordings stay real (Jacopo, 03/11/2026)**: when he recorded the screen, never redraw it as a graphic. Frame the real recording in a window on the plate, zoomed on the paragraph he is reading (about 1.9x), panning down as he reads; highlights, strikes and ticks go on top at the word's measured pixel position (measure the word boxes on the frame, never guess). Keep the recording's own auto-zooms where they happen. Skip any stretch that shows private files or a forbidden name, and replace just that moment with a graphic.
10. **The video demonstrates what it says**: use the method on screen (real prompt, real result) instead of describing it.
11. **Cutaways of the creator** (at the desk, waiting, surprised) serve the story's emotion; they are not filler. Shoot them with the checklist, not stock.
12. **Notes with a timecode become rules**: "0:14 the whoosh stronger here" is saved in `NOTES_LOG.md` and, when it repeats, in this file (see `plate-plan.md`).
13. **Motion on plates is a fluid camera on one digital board (Jacopo, 04/11/2026; replaces the zoom kicks of 01/11)**: no bounce, no kicks, no overshoot. A run of plates is one big board (formats/board.py): the camera glides with strong easing to what is being named, then pulls back; page to page is an eased swipe to an empty part of the board, never a fade and never a few frames of face in between; face to board is one continuous swipe. A plate starts ON the word that opens it, never seconds before, and it does not hold: after the last element it moves or it ends. Fewer plates: if a plate does not keep the listener attentive, the face is better. Animate the content too (type the prompt in the bar, light each card on its name). Motion is judged only in motion: show a short rendered window before spreading a new motion, stills prove nothing.
14. **The green plates are the look of the whole system** (Jacopo, 01/11/2026, blind A/B on the 16.5 s window of Video #2: "decisamente meglio, una spanna"): preset `plates-verde`
    is the default of `compose.py`; `--preset none` gives the old fixed cyan/blue look back, `--preset elegante-portfolio` the portfolio look.


14c. **Course tests voted (Jacopo, 05/11/2026):** the yes, maybe and no list is `prove-corso.md`; read it before inventing a move, and never propose its "No" items again.

14b. **Scene improvvisate, non formati da catalogo (01/11/2026).** Ogni spiegazione = una motion plate su misura nei canoni di Joseph (vedi `formats.md`, "Scene improvvisate"). Non fermarsi a "quale formato uso"; non rimettere le vecchie grafiche su sfondo verde (Jacopo: "così le migliori" non basta). Le linee tratteggiate compaiono solo quando collegano due elementi già in scena.


## 15. Travel reels and colour taste (reels Zanzibar, 27-29/10/2026; Jacopo's notes)

- **The mood is the type of shot, not the light** (reel #2, "Like a Tattoo", slow emotional song): cinematic landscape, wide, a camera that glides (gimbal). People only as part of the landscape (from behind, far, a silhouette); never selfies or smiles to camera; drop confused, abstract, handheld or murky-underwater clips ("the perfect way to make people not open a reel").
- **The first shot is the hook:** readable on the first frame, beautiful, with a clear move. Before proposing a running order, look at the clips through this filter, not through a "chapters of the story" scheme.
- **Subjects (reel #1, 28/10):** local people and children, never several similar boatmen in a row. Cuts on the beat every 4 beats (about 2 s): trust mh-video-editor on timing. A slow push-in of 5% on every clip is approved ("il push in mi piace"). Format 4:3 for IG; the cinemascope bars were refused.
- **No lyrics on screen** in the slow reel (17 styles tried, he chose none). If it is redone he pastes the text himself (copyright) and the times come from Whisper or are marked by hand.
- **Light leak in a reel:** use only the golden strip 1.25-2.0 s of leak 05 at about 35%; after 1.9 s it fills the frame with yellow and veils everything in olive.
- **Colour, travel:** the goal is to make the place look beautiful, not real. Bright sea and sky are not darkened to reach a mean exposure: a vivid turquoise and full light beat the "correct" exposure (29/10: he kept the bright version on 15 clips of 17, the "correct" one only on the arch and the sailboat). Never change the colour of an already approved video without a side-by-side first.
- **"Poco poco" means very little:** between two intensities he picks the lighter (27/10: red x1.15, skin x1.10, vibrance 0.40 on `pellicola-oro`). On village and green scenes the full WOW is a bit much.
- **Colour is judged on full-resolution frames:** the 480p phone copy flattens (see also `SKILL.md`, travel-reel drafts).

## UX / animation principles applied to plates (13/11/2026): PROPOSALS, NOT VOTED BY JACOPO
From `personale/youtube/analisi-inspo-3d-uiux.md` (20 principles, verdict for our plates). Nothing here replaces a voted rule; adopt only after a blind A/B.
- **Moving in arcs** (new): `Board(..., arc=0.03)` bows a diagonal swipe by 3% of its length (Jacopo 14/11: 5% was too curved, keep it nearly linear: voted OK with this), same speed profile (`board.arc_path`). Default `ARC = 0` (straight). Test: the same page-to-page swipe with and without.
- **Frequency of use** (new): an element that returns (chapter label, counter, lower third) animates in full the first time, then shorter and quieter: `plates_base.repeat_factor(n)` = 1.0, 0.7, 0.5, 0.35 (floor 0.35) for the 1st..4th+ appearance. Not wired into any format yet: multiply an entrance duration by it by hand.
- **Word -> effect delay <= 12 frames** (new): `scripts/qa-lag.py --words words.json --starts starts.json` lists every graphic whose first movement comes more than 0.40 s after the word that opens it.
- **Follow-through, without overshoot**: secondary elements arrive 2-4 frames after the primary and settle with ease-out (labels after the card, the shadow after the object). Never a bounce.
- **Squash and stretch: NO as a bounce** (conflicts with 13 above); only as motion blur on 3D whips (`w.shutter()`).
- **Anticipation: to be tested in A/B only**: a 2-4 frame counter-move (1-2%) before a long swipe.

## 3D worlds: Jacopo's verdict (14/11/2026, on the first 3D fashion video)
- **Keep:** motion blur on the whips, depth of field on close shots, the camera moves. The UX proposals (arcs, follow-through, frequency of use, word-to-effect delay) are all OK; arcs nearly linear.
- **Never:** venetian-blind light (reads as a render error; only a real window with a real cross is allowed), the ink/"disegno" pass as a published look (not good enough), an empty room, a trouser standing like two tubes.
- **Do:** a dense, cartoon-but-real room in the autogrill way (many props in every shot, real daylight through a window, pendants with halos), a trouser with pockets, loops, fly and creases hung on a hanger, a camera tour between stations, cuts every 2-3 s, and a layer of sound effects (whip, label tick, chapter riser, material sounds) because silence kills retention.

## 3D Short "primo pantalone": Jacopo's notes on proof 1 (14/11/2026)
"Continuano così che quasi ci siamo." The direction is right; the bar is REALISM: the more correct details, the better the result.
- **Garments look like real garments.** Tailored trousers have NO contrast top-stitching on the side seams, inseam or hem (blind hem). Thread is tone-on-tone. Pockets read OPEN (a dark mouth with the front edge standing proud and a bar-tack at each end), never as a stitched-shut line. A hung trouser is flat front-to-back: no puffy hips or waist. Toile marks are the real ones (grain line, hip line, knee line), not random strokes.
- **Every action must be legible.** A tool never "moves at random": shears cut ALONG a drawn outline, with the cut appearing behind the blades. Pin a label on what the voice names (grain line, notch).
- **No empty beats.** A shot of a blank sheet or an empty table is a retention hole. Start the action as the cut lands.
- **Transitions.** A film burn / light leak with a whoosh on the hook-to-story cut (`World3D.leak(t, d)`, sounds `es-whoosh-medium-transition` + `es-film-advance-wind`).
- **Captions** need a soft dark pill so they read on white paper. Labels in 9:16 need about 56 px.
- **End card = the real logo** (`logoplate`, the paths of `inverso/logo/inverso-logo.svg`), not typed text.
- **The background counts too.** Spools stand upright, plant leaves hang on stalks, folded cloth has weave and a rolled fold. Anything that reads as a primitive box gets fixed.

## 3D Shorts: the detailed atelier method + the autogrill method (14/11/2026)
For Shorts, use the detailed "primo pantalone" world (realism) together with the autogrill workflow (`explainer-3d-sop.md`). Both are the default from now on.
- **Text on screen for the WHOLE video** ("sui reel fa tanto la differenza"). Word captions (`captions`) alternate with big statements (`big()`: title, numbers, the moral, the CTA). A big statement replaces the captions it overlaps. Each caption and big holds until the next text arrives, so there is no gap even in the pauses. Check with a script that the gap list is empty and no spoken word is uncovered.
- **The voice needs emotion.** Generate the cloned voice ONE PARAGRAPH AT A TIME with expressive punctuation (… ! ?), then join the paragraphs with 0.35–0.55 s gaps. A single long take came out flat.
- **Sound** follows the autogrill rules: an opening whoosh + hit, a riser peaking on the punch word, story events, automatic pops/swishes/whooshes at least 0.35 s apart, music 13 dB under the voice measured in LUFS, fixed gain to −16 LUFS.
- **Render** with `finish.sh`: a 30 fps draft with QA that Jacopo listens to (a contact sheet does not show the sound), then the 60 fps final with BT.709 tags, a version number in the name and a light copy. Before the draft, check for flicker across 3 consecutive frames.
- **Big statements stay modest in 9:16:** about 76–82 px (a number-punch like «117 cm» up to ~96). ONE line, TWO at most: three lines "non mi piace". A longer sentence becomes two statements in a row, or the tail goes back to the captions. At 100–175 px Jacopo found them "veramente troppo grosso"; the look must stay close to the captions.
- **Labels must not sit on the caption band** (y ≈ 1180 in 9:16) or cross the frame edge. Check them on the contact sheet.

## Short "primo pantalone" v3 vs Autogrill v2.2: why the Autogrill is better (14/11/2026)
Jacopo, on v3: "ce lo facciamo andare bene, però il risultato non mi fa impazzire… quello dell'autogrill rimane molto, molto meglio: i tempismi, la canzone di sottofondo, tutto". Measured differences, to fix on Short #2:
- **Change of view.** The Autogrill has 17 real changes of view in 93 s (exterior, aerial plan, road, macro on the shelves). The Short has 2: the same warm atelier at a medium distance, joined by blurred whips. Next time vary the SCALE: wide/aerial ↔ macro, and use a different place or angle for each paragraph.
- **A visual device that explains.** The Autogrill draws the dotted red path on the plan and runs a live counter («prodotti che ti passano davanti: 485»). The Short only shows objects. Each Short needs at least one diagram-like moment, for example the correct outline drawn over the wrong one, or 117 cm against the right measure.
- **Palette and contrast.** The Autogrill is bright and saturated (red, green, white). The Short is all beige and warm, so on a phone it reads flat. Keep a strong contrast colour in every shot.
- **Timing.** The Autogrill adds a pause after the words that close a paragraph (`BREAKS`, 0.4–1.1 s), and the view changes inside that pause. The Short joins the voice paragraphs with fixed gaps and does not cut on them.
- **Music.** It gets chosen against the edit (energy and bpm that match the cuts), not just as "a new track".

## Review frame by frame before the 4K (Short v4, 13/11/2026)
Jacopo: "prima di mandare il 4K… ti fai tutti i frame, 10 per secondo… capisci se c'è qualcosa che non va". He also means any physical or logical mistake, not only flicker.
- **Always do a 10 fps review of the draft before the final.** Extract the frames with `ffmpeg -vf "fps=10,scale=240:-2,drawtext=…pts…,tile=8x4"` into contact sheets of 3.2 s each and look at ALL of them. Then fix, snapshot the times you changed, and only after that render the 4K.
- **The physics must hold.** A tape measure wraps AROUND the garment and turns with it, so it never goes into the fabric. A marker (chalk, dot, pin) must sit ON an object, never float in the air. A dotted outline hugs the garment it explains and does not cross other things (dress forms, the floor).
- **The camera never goes through objects.** Before a fly to the aerial map, the pendant lamps fade out (`pendant(hide=[[t0,t1]])`); going through one gave the "flicker".
- **Every element of the aerial map is on screen before the dive.** Labels go near their badge without covering each other, the caption band or the frame edge.
- **Tools follow the path smoothly.** The shears turn at a corner by averaging the direction over ±8 points, never in a single 90° step.
- **Stale renders.** If a render was stopped, kill the hyperframes processes and DELETE `draft-raw.mp4` before re-rendering, then check the timestamp: `finish.sh` skips the render when the file already exists.

## Short v4 → v5: Jacopo's frame-by-frame notes (13/11/2026)
- **A live counter moves on with each PHASE, not with a word that comes later.** The cost pill read "niente" all through the pattern and "un foglio di carta" all through the toile, so at 52 s it contradicted the big statement. The rule: drawing = niente, pattern = paper (from "carta"), toile = cloth (from "tela").
- **No double text.** When a 3D label and the caption say the same thing at the same moment ("Gamba dritta" / "gamba dritta"), the label comes in 0.8 s later, once the caption has moved on, or it is dropped.
- **The hook must show the claim in the first frame.** "Sembrava una gonna" over a toile seen from the front doesn't read: open at 3/4, on the side where the volume is.
