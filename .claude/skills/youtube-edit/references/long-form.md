# Long form, explainers, camera and pacing

_Moved out of `SKILL.md` on 22/10/2026, text unchanged. Read this when: planning a section over ~3 min, placing explainers, or writing camera moves. Rules here are still the rules: a new note rewrites the rule where it lives (see `SKILL.md` > Keeping the skill yours)._

## Finding explainers in the transcript

Diagrams (6, 7, 8, 27, 30) are **found, not requested.** Scan the transcript for enumeration ("first / second / third"),
a sentence that promises a shape ("the way this works is", "there are three"), chained causation ("and then", "which
leads to"), stage vocabulary ("top of funnel", "cold / warm") and named tools in a list (they become chips).

| The passage says... | Format |
|---|---|
| A then B then C, each a distinct action | 6 flow diagram (27 when quick) |
| B is only possible because of A: a climb | 7 staircase |
| many become few become paying | 8 funnel |
| one thing becomes several | 30 flowing paths |
| it used to be X, now it is Y | 20b before/after wipe |

Node titles are 2 to 4 words in your phrasing; detail lines are your own point tightened, never an invented claim,
number or step ("about seven days" stays "seven days"); each beat is the word start of the sentence that introduces the
step; duration = last beat + ~8 s; no outcome said, no payoff banner. **Propose before building** (the passage, the
format, the step labels, in one short message): a diagram is 30 to 40 s of screen time, worth one round of confirmation.

## Read the footage, not just the transcript

1. Find the shot changes: `ffmpeg -v error -i in.mp4 -vf "select='gt(scene,0.12)',metadata=print:file=-" -f null -`.
2. Place per shot and measure the face-safe zone; overlays sit opposite you. Framings measured so far (add yours):
   - You sit LEFT: cards live right of x 1000.
   - You sit CENTRE at a desk with a mic (mic head around x 500 to 800, y 330 to 500): cards live left of x 660; `tl`
     clears the mic; an 840 px card at left 62 reached x 902 and covered the face.
   - A tight shot, mic bottom-right: your face fills x 750 to 1150, your chest the bottom-left. Cards go top-right (left
     1220, 640 px wide) or top-left (left 62, top 80, under ~720 px wide, above y 220); nothing bottom-left.
3. **A card never covers your face.** When the copy will not fit the safe zone, make it a lower line instead of
   shrinking the card; check the card's edge against your hair in a snapshot.
4. Re-anchor the camera per shot (`38% 0%` when you sit left, `52% 0%` centred), and release every move before a cut.
5. **If the frame already says it, do not say it again.** A big number once duplicated a timer held up to the lens, and
   an out-of-focus hand cut its first digit through the matte. The overlay went.

## Long-form doctrine

- **One persistent world.** A long video is one space the camera moves through, not a stack of unrelated cards. Decide
  the spatial grammar first (left to right = toward the outcome, up = a person, down = the system).
- **The chapter fixture returns at every boundary** (progress tag, slot wall or deck); an open loop is planted in the
  hook as something visibly incomplete (empty slots, a ghosted stack) and filled on screen, never "we'll come back to this".
- **One element at full brightness at a time.** What is drawn stays, dimmed but legible (context .56, spent .33, labels
  never below luma 90); retire a finished prop to 0, not 0.3. About 20 on-screen words per section, no sentences;
  everything reads in under 2 seconds.
- **Pacing:** no stretch without an overlay or a camera move over 15 s in the first 90 s, 20 s after, 30 s ever
  (`gap-scan.py`); about 7 overlays + 7 camera moves per 90 s. One card across a topic span (an item building midway)
  beats five flashes. Enter 0.15 to 0.25 s ahead of the anchor word; never divide a section evenly.
- **One gesture, not two moves.** Two moves in a row on one subject read as a glitch: merge them into one move with one
  symmetric ease (`power2.inOut`). A front-loaded ease (`power3.out`) on visible footage rushes, then crawls.
- **A full-frame graphic moves as a camera over one canvas:** push in on the part you name, pull back to show what it
  connects to, travel to the next, one move at a time (`world`, `deck`).
- **One opacity owner per element per window:** two tweens on one element's opacity strobe in the master. Fade the child
  or the wrapper, never both; let the lint's `overlapping_gsap_tweens` warning stop the build.
- **Audit audio at the acoustic level** (digital zero inside pauses: fill with room tone; level cliffs at joins) and
  verify motion on contiguous frames (see "Verify and deliver"): every gate can pass and a viewer still sees a freeze.
- **Compose per section** (hook, each intro, each body section) and join with `assemble.py`: each stays under the
  heavy-overlay budget, and a note costs one section's render.

**The house rules for long form:**
- **Your face is not the default background.** Aim for 40% or more of a talking section as **motion plates** (Jacopo's
  word for the full-frame graphic scenes on the brand wash). An abstract explanation (what a tool can do: files, programs,
  an output folder) goes on a plate as a `world` scene, never as a card over your face.
- **Every motion plate carries your face in picture-in-picture** (Jacopo, 28/10/2026, from an Ali Abdaal video): the same
  footage, in sync, in a small rounded crop in a corner, so the viewer never loses the person talking. Spec in
  `references/formats.md`, "Explainers (full frame)". Exceptions: the 46 hero line and 35 masked title (one sentence, a
  few seconds) and stock `clip` cutaways of other people.
- **Variety over lists.** No list or bullet panel in a long-form body: each list becomes a device (pills on each phrase,
  a `world` loop, one device per number, a pipeline).
- **Every person or job you name gets footage of that person:** a 2.6 to 3.4 s full-frame stock `clip` right after you
  describe the job, before the tool or answer is revealed; one or two AI shots of you where it lands a joke.
- **A board you fill one by one starts blurred:** each card shows only its icon, blurred, and clears on its own word.
- **Show a change the way you tell it:** "it was dark blue at first, I didn't like it" means dark blue first, switched on
  "didn't".
- **An app you name gets a designed window** (13b, its empty start state), not a screenshot of your real one; **a website
  you name gets the real page** (a 2x capture in a browser window), held until you move on.
- **Every on-screen click makes a light click** (0.28) on the frame the cursor bottoms out; a silent click reads as a mistake.
- **A thing you name in a joke gets its real picture** (say "chips" and two real bags sit either side of you): product
  photos from Open Food Facts (`cgi/search.pl?...&json=1`, swap `.400.jpg` for `.full.jpg`; CC BY-SA, so credit it),
  cut out with `npx hyperframes remove-background photo.jpg -o photo-cut.png` (pad a frame-filling photo 20% first),
  cropped to the alpha box, root-level `<img class="clip">` either side of you, in on the word with one pop.

## Camera

**Top-anchored origin, always** (`52% 0%` centred, `38% 0%` when you sit left): a centre-anchored zoom crops your head.

| Move | Numbers |
|---|---|
| Punch-in on emphasis (the number, the promise, a punchline) | 118 to 125%, 0.30 to 0.35 s, `power2.out` |
| Slow creep across a thought | 110 to 112% over 5 to 10 s, `power1.inOut`; release on the next cut |
| Zoom-out reveal | 110 → 100% over 0.5 s as a card enters |
| Snap back | to 100% at every shot change; never carry a zoom across a cut |
| Budget | 3 to 5 moves per 40 s hook; long form about 7 per 90 s |
| Limits | 1080p source: 112% at most; 4K: 150% freely, 200% for a deliberate crash-in |

- Compensate hero text for the zoom: at scale 1.12 with a 52% origin, a left-anchored element drags ~105 px left.
- **Jump cuts stay naked by default.** Dress one only when the energy changes (a pivot, a joke landing, a section
  start): a fast punch (scale 1.04 → 1.00 over 0.12 s), a zoom-through (scale up with a 10 px blur out) or a micro whip
  (12% x-shift with blur, 0.25 s). One or two per 40 s hook, at most one per 10 s in long form, never mid-word. On a long
  camera-only stretch, switch framing between jump cuts (1.0 / 1.09) so each reads as a punch, not a bump.
- **Put every reset on the jump frame.** Cut-map times are not frame-aligned: a `set` at 10.34 lands on the frame at
  10.367 while the footage jumped at 10.333, a one-frame double cut. Measure the jump frames once from a low-res decode
  (the max frame difference within ±4 frames of each cut) and set at `jump/30 - 0.003`.

## Pacing

- Hooks: about 6 overlay moments per 37 s (about 10 overlays + 4.5 to 7.5 camera moves a minute). Cards hold 3 to 7 s;
  past 7 s they need internal motion (staggered items, a count-up). Enter 0.4 s `power2.out`, exit 0.35 s `power2.in`;
  no bounces, no 3D flips, and blur never animates. One hero element at a time (a chip may sit with a logo card).
- **Motion from the first frame of a hook.** One pattern that worked: four short clips of your own work in glass cards
  around you (440x248 at x 36 / 1444, y 128 / 400), in 0.12 s apart from 0.35 s, all playing at once, out by 5.8 s;
  the title line lands about 1 s after the open, not on frame 0. The clips are root-level muted videos.
- **Reaction hooks (news, launches):** the hook moves the whole time; everything you name is on screen on the word
  (start a clip ~0.1 s in so its reveal hits the word). A count gets a click-click montage ("more than 20 releases":
  11 cards, one per ~0.3 s, a small counter). Event cutaways: one clean shot per clip (official streams switch cameras
  mid-shot), checked frame by frame. Posts 1560 px wide (1040 was unreadable on a phone), dark glass on a bright set, no
  big number over your face, a tag gone before the next full-frame cutaway.
