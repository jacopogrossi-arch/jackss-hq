# Format library

_Moved out of `SKILL.md` on 22/10/2026, text unchanged. Read this when: the planner designs a storyboard, or the builder hand-builds a format. Rules here are still the rules: a new note rewrites the rule where it lives (see `SKILL.md` > Keeping the skill yours)._

## Format library

Vary the formats; never the same device twice in a row. **Variety across the video** (Jacopo, 26/10/2026): apart from the lower line (2) and transitions, no format takes more than a quarter of a video's graphics; each video uses at least three formats the previous video did not use, plus at least one new or adapted format (see `SKILL.md` > Keeping the skill yours); the counts of past videos are in `references/format-history.md`. `*` = built and snapshot-tested but used in fewer real
deliveries: read its first real snapshot with extra care and name it at Checkpoint B. The composer builds every format
with a type below (the JSON shapes are in compose.py's docstring); the specs give the numbers to check a snapshot
against, and to hand-build the rest.

| # | Format | Use for | Composer type |
|---|---|---|---|
| 1 | Big number behind the head | money and stakes figures | hand-built |
| 2 | Lower line | **any single line of copy, the default** | `line` |
| 3a | Glass card | lists, deliverables | `list` |
| 3b | Extended-left bullets | the same, for variety | `bullets` |
| 3c* | Glass pop-out | a short titled list when 3a and 3b were just used | `popout` |
| 4a | Logo card | naming a tool; the default for a list of tools | `logo` |
| 4b | Full-screen site cutaway | a site introduced as the subject, a glance under 3 s | `site` |
| 4c* | 3D floating browser | a site you talk about, held longer, or that scrolls | `browser3d` |
| 4d* | 3D screenshot fan | two or three screenshots at once: posts, wins, app screens | `fan3d` |
| 5 | Punchline chip | jokes, pattern interrupts | `chip` |
| 6 | Flow diagram | a long process with a detail line per step | hand-built |
| 7 | Ascending staircase | steps where each one earns the next | hand-built |
| 8 | Funnel | volume narrowing toward money | hand-built |
| 9 | Chapter tag | naming the section you just entered | `tag` |
| 9b | Progress tag | the same with N pips, on a numbered series | `tag` with `n`, `of` |
| 9c* | Slot wall | the video's parts as sockets, planted empty in the hook | `wall` |
| 10 | Success stamp | the moment something works | hand-built |
| 11 | Description pointer | "link in the description" | `pointer` |
| 12 | Key-word highlight | long form only: two or three key words | hand-built |
| 13 | Prompt window | reading out a prompt you give an AI | hand-built |
| 13b | AI chat window | the chat app itself: images drop in, the prompt types, the answer lands | `formats/claude_chat.py` |
| 14 | Subscribe bar | the ask, mid-video | hand-built |
| 16 | Shimmer sweep | a hero line | `"shimmer": true` on `line` |
| 17 | Vignette + grain | the awkward beat after a joke | `vignette` |
| 18 | Article cutaway with highlighter | one headline or quote from a page | hand-built |
| 18b | Doc read | two or three passages from one page, the rest out of focus | `doc` |
| 19 | Photo card | a named person | hand-built |
| 20 | Full-frame video cutaway | footage that needs hand work | hand-built |
| 20b | Before/after wipe | inside an image cutaway: the before becomes the after | hand-built |
| 20c | Clip | a full-frame cutaway: your screen, archive, stock, AI B-roll | `clip` |
| 21 | Logo swap plate | "X versus Y" | hand-built |
| 23 | Tutorial layout | screen + face in one glass composition | not built yet |
| 24* | Stat tiles | two to four numbers that belong together | `stats` |
| 25* | Growth card | one number that grew, with its shape | `growth` |
| 25m* | Chart morph | the growth bars turn into the trend line | `"morph": true` on `growth` |
| 26* | Bar comparison | "this takes X, that takes Y" | `bars` |
| 27* | Pipeline | three to five steps lit one by one: the fast version, a step about every 2 s | `pipeline` |
| 27b | 3D card chain | three to five spoken steps that are abstract labels (nothing to draw), when there is time to glide (about 3 s a step or more); steps you can draw go to 45 | `formats/chain3d.py` |
| 28* | Hub | one idea and the parts it is made of | `hub` |
| 29* | Equation | "A + B = C" said as one line | `equation` |
| 30* | Flowing paths | one thing becoming several, then one result | `flow` |
| 31* | Dashboard zoom | proof from a real dashboard: find one number, lift it out | `dashzoom` |
| 32* | Glass focus | walking through a table one row at a time | `lens` |
| 33* | Search → results | "I searched for X" | `search` |
| 34* | Magnetic dock | three or more tools named in a row | `dock` |
| 35* | Masked title | a full-frame chapter card | `masktitle` |
| 36* | Button → player | "watch this video", mid-video | `player` |
| 37* | Image reveal | a still opening behind slats | `image` |
| 38* | Exploded layers | what an app or a stack is made of | `layers` |
| 39 | World camera | a system you walk through: push in, pull back to reveal, travel | `world` |
| 40 | Numbered deck | the full-frame opener of each part of a numbered video | `deck` |
| 41 | Pills around the head | two to six short labels while you stay on camera | `pills` |
| 41b | Hanging chips | one to four tools or labels with real logos hung around the head, arrows to the face, a slow camera that carries them: **the default with the `elegante-portfolio` preset** | `formats/chips.py` |
| 42 | Chat (bubbles, window, phone) | a conversation | `chat` |
| 43 | Dot grid | a count you say out loud, in groups ("three outfits, three mood boards..."): one row per group fills on its word | `formats/dotgrid.py` |
| 44 | Outline rail | a list read out as an outline (what came out, the parts of a plan): rail, dots, names, ×N and bars | `formats/scaletta.py` |
| 45 | Living shape | three to six spoken steps of one process, told as ONE glowing shape that turns into the next thing (search bar, globe, logo, image grid, finished page): **the default for a process with ~2 s or more per step** | `formats/morph.py` |
| 46 | Hero line | the one sentence of a section that must land: full frame on a living warm gradient, words out of blur on their word, a logo slipping in | `formats/herotitle.py` |
| - | Check marker* | done and to-do lists: a check draws on each item | `"marker": "check"` on `list`, `bullets`, `popout` |
| - | Thumbnail grid | your own thumbnails; the cursor clicks one | `grid` |
| - | Coded scenes | money, catalog, room, plate, profile: B-roll with no stock | `scene` |

### When two formats compete

Pick the one that fits what you are saying. Tied: the one used least so far in this video (compose.py prints the
counts). Still tied: the one used least in your last video.

| You are... | Candidates | Pick |
|---|---|---|
| saying a count in groups ("three of each") | 43, 44, 3a | 43 when the numbers are the point; 44 when it is an outline or plan; 3a when the names alone are |
| naming one tool | 4a, 34 | 4a; three or more tools in a row: 34 |
| naming tools or labels while staying on camera | 41b, 41 | 41b with `elegante-portfolio` and real logos; 41 for five or six labels or icons only |
| showing a website | 4b, 4c | 4b for a glance under 3 s; 4c when you talk about it or it scrolls |
| giving numbers | 1, 24, 25 | 1 for one stakes figure; 24 for two to four that belong together; 25 when it grew and the shape matters (25m when the trend is the point) |
| explaining a process | 45, 27b, 6, 7, 8, 27, 30 | 45 when each step is a thing you can draw (a tool, a page, images) and steps are 1.2 s or more apart; 27b when the steps are abstract labels; 7 each step earns the next; 8 volume narrows to money; 30 one thing becomes several; 27 a quick sequence; 6 a long one |
| comparing | 26, 32, 21 | 26 for sizes (time, money); 32 for values read off a table; 21 for tool versus tool |
| listing | 3a, 3b, 3c, 41, check marker | never the same device twice in a row; the check marker for done or to-do; long form: no list panels |
| opening a section | 9, 9b, 9c, 35, 40 | 9c on a video with a spine; 40 for two to four numbered parts; 9b on a numbered series; 35 for a long break; 9 otherwise |
| showing an image or footage | 19, 20c, 37 | 19 for a named person; 20c for moving footage (20 when it needs hand work); 37 for a still |
| showing screenshots | 4d, 31, 4c | 31 when one number on it is the point; 4d for two or three; 4c for one site |
| typing | 13, 13b, 33 | 13 or 13b for a prompt to an AI (13b when the app itself matters); 33 for a search |
| saying one line | 2, 46, 29, 5 | 46 for the one sentence a section is about (at most one per section, 2 to 7 s, the face can leave the frame); 29 only for an "A + B = C" line; 5 for a punchline; 2 otherwise |
| showing parts of a whole | 28, 38, 39 | 38 for layers of a product or stack; 28 for parts of an idea; 39 when the camera should move between them |
| naming a few short things on camera | 3a, 41 | 41 for labels of one to three words around you; 3a when you count a list |
| a conversation | 13, 42 | 42 for people talking; 13 for a prompt to an AI |
| reading from a page | 18, 18b | 18 for one headline; 18b for two or three passages |
| pointing to another video | 36 | mid-video only; at the end the YouTube end screen does the job |

### Copy on screen

- **2. Lower line (the default).** Any single line of copy, never in a card: bottom-centre, no box, always centred,
  ~100 to 104 px/700, letter-spacing -.015em, white with the key phrase cyan (amber for money). Words rise in staggered
  ~0.055 s (opacity 0→1, y 26→0, `power2.out`), never typed; animate `opacity`, not `display`, so the line never shifts.
  One span per word from `data-text` at load, container `font-size:0` (or whitespace doubles the gaps). Holds 5 to 7 s.
- **46. Hero line** (won the blind A/B of 26/10/2026 against 2 on the `strumenti` bench window; idea from the @zeecreative
  Apple Intelligence reel). `formats/herotitle.py`: `herotitle(lines, t_in, t_out, logo, logo_at, gold_at)`. Full frame: a radial
  mask blooms from the centre over the face (0.45 s `power3.out`) onto a living gradient (four blurred blobs, gold, dark gold
  `#8a5a1c`, emerald, ivory, gathered in a vertical band that opens like a curtain in 1.2 s, then drifting; grain .06; push
  1.00 → 1.05). Line 1 Inter 700 120 px ivory, line 2 Playfair Display Italic 110 px gold → ivory gradient with a blurred
  duplicate as glow; each word comes out of blur (14 → 0 px, y 20 → 0, 0.5 s) on its spoken word. Both lines are laid out in
  their final place from frame one (only opacity and blur move): the one allowed move is the logo tile slipping in left of the
  first word and pushing it (0.5 s `power3.inOut`); `gold_at` turns line 1 to the gold gradient. Out: the mask closes (0.4 s).
  Two lines and six words at most, 2 to 7 s, once per section at most, no sound. Bench files `videos/_bench/ab/strumenti-titolo/`.
- **5. Punchline chip.** `rgba(17,17,17,.45)` glass, blur 18 px, radius 16, 64 to 76 px/700, the emphasis word solid
  magenta, bottom-centre 80 px up.
- **12. Key-word highlight (long form only).** A navy `#0005EE` block behind a word as you say it, white text, a glow;
  two or three words, never a sentence (word-by-word captions are for Shorts). ~78 px/700, bottom-centre, radius 14.
- **16. Shimmer sweep.** A cyan band crosses a hero line (`background-position` on a `background-clip:text` gradient),
  two passes of ~1.5 s; set the pre-sweep position inline or the words stay unpainted until the sweep.
- **29. Equation\*.** A glass strip bottom-centre (or `top`), 76 px terms rising on their words, `+` and `=` white at
  .6, the result cyan (`"em"`) or magenta (`"pay"`). Laid out from frame one so it never shifts; it takes the lower
  line's slot, never both.
- **41. Pills around the head.** Two to six glass pills (42 px icon + label, 88 px tall), each on its word: `sides`
  (alternating columns from `top` 290, clear of your face), `left`, `right` or `row` (bottom centre). `tone: "cyan"` for
  the one that matters, `"amber"` + `"mark": "x"` for a risk or a wrong answer. One to three words each; hidden until its
  word (glass that has not arrived blurs the footage).

### Cards and lists

Every light glass card uses one recipe:

```css
background: rgba(255,255,255,.18); backdrop-filter: blur(30px) saturate(1.25);
border: 3px solid rgba(255,255,255,.58); border-radius: 26px; box-shadow: 0 24px 80px rgba(0,0,0,.38);
```

- **41b. Hanging chips** (won the blind A/B of 23/10/2026 against 41 on the `strumenti` bench window; idea from the
  @realskytan reel; creator: "more coherent with the style we are building"; an earlier slower build was "a bit slow").
  `formats/chips.py`: `chips(items, t_out, duration, phrase, camera)`. Dark glass chips 320x96 (radius 48, fill
  rgba(20,15,10,.55), 2 px ivory .28 border, 24 px backdrop blur), real logo 56 px + name Inter 600 36 px, hung in the free
  space beside the head (bench: Claude centre (470, 420), Procreate (1450, 380), Canva (1480, 620)). Each from 0.05 s before
  its word: scale .94 to 1, y 10 to 0, blur 4 to 0 px in 0.4 s `expo.out`, a gold glow rising to .35 and falling once (0.8 s);
  a dotted curved arrow (3 px, dash 2/9, ivory .55, small head) draws 0.08 s later in 0.45 s `power2.out` and stops 25-45 px
  short of the face: **place the arrows on a snapshot**, the head leans (on the bench to x ~725 at 9.5 s). An optional phrase
  sits in a matching pill 18 px under its chip (Playfair Display Italic 36 px gold): never a radial veil behind text, it reads
  as a stain on a light wall. **Camera:** one function of time moves the footage and every chip host with the same scale and
  origin, so the chips stay pinned to the head; slow creep toward the first chip (1.00 to 1.07 over 3 s), a 0.6-0.7 s push of
  framing toward each new chip (`power3.inOut`, to 1.09-1.10), back toward the phrase, release to 1.03 at the end. Exits
  0.4 s (y -8, blur to 4 px), 0.05 s apart, the first chip last. No idle wobble, no sound. 41 stays when icons are enough or
  there are five or six labels.
- **43. Dot grid** (won the blind A/B of 23/10/2026 against 3a on the `lista` bench window; idea from the @realskytan reel,
  100 people as 100 dots; creator: "perfect"). `formats/dotgrid.py`: `dotgrid(rows, title, t_in, t_out, cols=3, right=1780,
  cy=540)` returns `html` + `js` for `raw_html`/`raw_js`. Two to five rows (one per spoken group), two to six dots a row (the
  spoken count). Dots 64 px, 22 px apart, on the free side of the face (right edge x 1780, centred on y 540); title in
  Playfair Display Italic 44 px above, right-aligned; labels Inter 600 32 px ivory, right-aligned 28 px left of their row,
  dark soft text-shadow. At `t_in` the title rises (y 12 to 0, 0.4 s) and every dot appears empty (2 px ivory .35 ring,
  scale .8 to 1, 0.02 s apart). On each group's word its row fills left to right (scale .5 to 1, 0.3 s `power2.out`,
  0.07 s apart, 24 px glow of its colour) and its label slides in (x -14 to 0, 0.4 s); the previous label drops to .65.
  Colours: gold, emerald, then both mixed 45 % toward ivory. Exit at `t_out`: opacity to 0, x +30, 0.4 s. No sound.
  Hold the last row at least 2 s before `t_out` (on the bench the window ends early and "Concept" reads only 0.8 s).
- **44. Outline rail** (won the blind A/B of 23/10/2026 against 3a on the `lista` bench window; idea from the @realskytan
  reel, his Introduction / Struggle / Rise outline; creator: "perfect"). `formats/scaletta.py`: `scaletta(items, title,
  t_in, t_out)`, items `(name, t, anchor, count)`. Left of the face: title Playfair Display Italic 40 px at (110, 250);
  a 2 px dotted ivory .35 rail at x 139; items 118 px apart from y 330. Per item, from its word t: the rail segment draws
  down to it (clip-path, t-0.15, 0.35 s; scaleY would stretch the dashes), a 16 px dot in its colour pops (scale .6 to 1,
  t-0.05), the name Inter 600 38 px in its colour rises (y 12 to 0, 0.4 s) with "×N" Playfair Italic 40 px beside it, and N
  bars 8 px (300/240/270 px, .8) draw from the left (t+0.1, 0.08 s apart, 0.5 s). The previous item drops to .65.
  **No card and no radial veil** (a radial veil read as a dark stain on a light wall): a linear wash from the left edge
  (rgba .62 to 0 over 760 px) fades in with the first item; text carries a dark soft text-shadow. Exit at `t_out`: x -30,
  opacity 0, 0.4 s. Colours gold, emerald and their light mixes. No sound. Use 44 when the list is a plan or an outcome
  read as a structure; 43 when the numbers are the point; 3a when the names alone are the point.
- **3a. Glass card.** 600 px, monochrome (colour lives in the lower line): eyebrow 30 px/700 white at .92, items 64 to
  72 px/700 with white dots and no sub-text (each item stands alone: "Invite teammates", not "Invite feature" plus an
  explainer). Items start `display:none` and appear on their word, so the card grows with the list. Every text gets a
  dark `text-shadow`: at 18% white the card follows the footage behind it (a cyan eyebrow measured 2.4:1).
- **3b. Extended-left bullets.** `#video-wrap` pushes to scale 1.18, x 150 (0.75 s `power2.inOut`, origin `50% 0%`;
  back in 0.65 s), and the 173 px overhang covers the shift. Scrim `linear-gradient(90deg, rgba(0,0,0,.97) 0%,
  rgba(0,0,0,.82) 34%, rgba(0,0,0,.45) 46%, transparent 60%)`; items 68 px/700 at left 96, top 318, cyan dots, no card.
- **3c. Glass pop-out\*.** The 3b move with a glass panel at left 72, top 230 (40 px title, 62 px items, 560 to 820 px
  wide) that leaves 0.7 s before the release so the camera returns onto clean footage. Never zoom from `0% 50%`: it
  crops the head.
- **Check marker\*.** A 44 px ring per item; a beat after the item lands it fills cyan and a dark check draws in 0.3 s.
  Done and to-do lists only, not plain nouns.
- **1. Big number behind the head.** Full digits (`$207,000,000`, never `$207M`) so your head covers about one glyph in
  twelve. White, solid, never a gradient: ~230 px/700 + `-webkit-text-stroke: 5px`, centred at `top:17%`, counting up
  with `toLocaleString('en-US')` (~1.4 s `power2.out`). Inside `#video-zoom`: footage → number → matte. Supporting copy
  in front at the bottom, ~94 px/700, the key phrase amber. (The linter's `text_occluded` is the point here.)
  - Short figures lose digits behind a centred head: write the unit inline (`$1,000 A MONTH`, 200 px, left-anchored at
    150), or put the figure beside the head (170 to 200 px, no matte, 60 px clear of its edge measured on a frame).
  - **Counter split around the head:** a 190 px white number right-anchored so its last digit tucks ~24 px behind the
    hair (the head measured from the matte), a 120 px cyan unit 8 px clear on the other side (a tucked "/" vanishes),
    `font-variant-numeric: tabular-nums`. The count runs from the money word to the END of the amount word
    (`power2.out`, a 6% bump, a cha-ching at 0.07 on the landing); the unit enters on its word. Matte only that window
    (`ffmpeg -ss -t` → `remove-background --quality best`, `data-media-start="0"`); mark the text
    `data-layout-allow-occlusion`.
  - **Pixelated logo teaser:** mosaic a 480 px logo to 5x5 (`scale=5:5,scale=480:480:flags=neighbor`; 4x4 for a
    letterform logo, which still reads at 5x5), revealed in steps: blocks 48, 24, 12, clean, 0.1 s each.
- **24. Stat tiles\*.** Numbers 112 px (92 stacked) counting up in full digits over 1.1 s, 34 px labels; `layout: "row"`
  (full frame, a 76 px title) or `"stack"` (a column at `tl`/`tr`); `em_tiles` turns a number cyan. Only numbers you can
  source get a tile.
- **25. Growth card\*.** 600 px at `tr`/`tl`: the number counting up cyan at 120 px, then bars rising (the last one cyan)
  and a glowing white line drawing over them to a dot (`count_at`, `bars_at`, `line_at`). Once per video at most.
  **25m** (`"morph": true`): the bars thin to stems (1.1 s, 0.16 s apart) while a smooth Catmull-Rom line draws through
  their tops in 1.4 s at an even speed, then an optional `badge`.

### Sections

- **9. Chapter tag.** A pill top-right: a live cyan dot + 34 px/700 label, light glass, held ~5 s then dropped (one that
  stayed 76 s read as static), on its own `data-track-index` (`overlapping_clips_same_track` otherwise). **9b** (`n`,
  `of`) adds N pips (done, now, next) for the first ~5 s of each segment; the viewer sees the slots fill.
- **9c. Slot wall\*.** A glass strip top centre, one 264x74 slot per part: empty, dashed and numbered in the hook
  (`filled: 0`); at each section the live slot fills cyan with its name on the word (`filled`, `now`, `fill_at`; spent
  slots .56); at the recap (`recap: true`) every slot lights and a cyan thread draws under them. It replaces the progress
  tag on a video with a spine; never both in one section.
- **40. Numbered deck.** Two to four 380x520 glass cards (italic number, 112 px icon, a 40 px title of five words or
  fewer) under a `head` ("3 PREDICTIONS"). `now: 1`: the row arrives, the camera pushes in on card 1 (1.5x, 1.1 s), the
  others drop to .38; `now: k` slides from card k-1 to k (1.0 s); `recap_at` pulls back to the row. It returns at every
  part boundary; never with a progress tag in one section.
- **35. Masked title\*.** A letter-spaced eyebrow ("PART 2"), the word as a thin white outline filling solid from the
  bottom (1.5 s `power3.inOut`, with a cyan edge line and a small handle), then a 64 px sub line rising from behind a
  mask. `size` 220 px by default. Never over your face.

### Tools, sites and screenshots

- **4a. Logo card.** Logo only, no name (you say it): a 380 px glass plate, the logo ~264 px tall (150 px was "quite a
  bit too small"), `tl` at a desk, `tr` on a tight shot, one pop. **21. Logo swap plate:** one plate; the first logo
  slides out (x → -50) on the second name and the second slides in (x 50 → 0), one pop on the swap.
- **34. Magnetic dock\*.** White 114 px app tiles in a glass dock; the oversized cursor walks to each tool on its word,
  the tile under it swells to 1.75 on a smooth falloff and a tooltip names it. One driver tween, so any frame renders
  the same.
- **4b. Site cutaway** (`site`). The homepage fills the frame ~3 s: a 62 px chrome bar, traffic-light dots, the bare
  domain in a 21 px URL pill, no copy, a drift 1.00 → 1.06. From a real `npx hyperframes capture` (optional `scroll`).
- **4c. 3D floating browser\*.** A full-page capture in a 1340x830 window rising in already turned (rotateY 27→15°,
  rotateX 16→7°, z -420→0, 1.0 s `power3.out`), then a slow camera orbit toward it while the page scrolls (`scroll`, in
  displayed px); one sheen; `near` picks the edge closer to camera, `callout` rings a spot. No flip: the tilt only settles.
- **4d. 3D screenshot fan\*.** Two or three images in depth (the middle 30 px forward at 1.05, the sides turned 16° and
  70 px back) rising 0.14 s apart, the fan orbiting rotateY 5 → -5; `focus` brings one forward (z 160, 1.12) while the
  rest drop to .4. `"frame"`: card (560x700, default), `"phone"` (330x700) or `"browser"` with `domains`, `fit`
  (`"width"` = a long page from its top, `"contain"` = a whole post) and `scroll` (`{index, at, by, dur}`).
- **Screenshots are browser windows showing the page, never crops of video frames.** Posts come from X's official embed
  (see "Sourcing assets"). When a live page blocks headless capture, read its text in the browser, rebuild the long page
  in HTML with the site's fonts, then `"<Chrome binary>" --headless=new --force-device-scale-factor=2
  --window-size=760,2600 --screenshot`.
- **31. Dashboard zoom\*.** Your real analytics screenshot (one 16:9 screen; give `"size": [w, h]`): at `find_at` the
  camera pushes to `focus` (a rect in image px, zoom capped at 3.2x) and cyan brackets find it; at `lift_at` the tile
  lifts into a 760x420 glass card with leader lines back, then the number counts up with a delta chip and a sparkline.
  Real numbers only, read off the screenshot.
- **32. Glass focus\*.** A 1200 px card of up to six rows, all out of focus (a static blur); a glass lens glides to each
  row in `stops` on its word (0.6 s `power3.inOut`), sharp inside at 54 px with the value cyan. The lens's copy moves the
  opposite way to line up, and its glass is nearly opaque so the row never doubles.
- **33. Search → results\*.** A pill opens from 520 to 1200 px (0.55 s); from `type_at` the query types at `cps` (16) with
  a cyan caret; two to four result rows drop in. `"sound": true` adds typing for exactly the typing time.

### Explainers (full frame)

Every full-frame scene sits on an ambient three-radial brand wash plus a 96 px grid at .28, never flat black.

- **6. Flow diagram.** A rail 1840 px wide at left 40: N nodes of 320 px, 56 px gaps, a 44 px arrow centred in each
  (five nodes: lefts 0/376/752/1128/1504, arrows 326/702/1078/1454; recompute for another N). A node: a cyan number
  badge, a hand-drawn SVG glyph, a 30 px/700 two-line title, chips for specifics. One beat per spoken step (~6.4 s
  apart): the shaft draws (scaleX 0→1, origin `0% 50%`), the head fades, the node lands (y 34→0, scale .965→1), then a
  44 px detail line under the rail. Cyan for mechanical steps, amber for urgency, a magenta payoff banner once the rail
  dims to .5. No `drawSVG` (not in `gsap.min.js`).
- **7. Ascending staircase** ("therefore" where the flow says "then"). Treads 300x200, each +356 px right and -112 px up
  (lefts 60/416/772/1128/1484, tops 670/558/446/334/222), fixed height so the risers meet them. Risers span only the gap,
  (L+300, T+100) → (L+356, T-12), drawn with a dash sweep (`getTotalLength()`, `strokeDashoffset`). Treads arrive from
  below-left, the previous drops to .42, all return to .85 at the end; the last magenta, the rest cyan.
- **8. Funnel.** SVG polygons, not `clip-path` (borders do not follow it): bands 180 px tall, 14 px apart, narrowing 90 px
  a side: `200,280 920,280 830,460 290,460` / `290,474 830,474 740,654 380,654` / `380,668 740,668 660,848 460,848`.
  Cyan (reach) → amber (warming) → magenta (money); metrics count up inside the bands, text at left 1010. Every metric box
  shares one `left` on the centre axis (following the taper put boxes 45 and 90 px off). Done stages dim (band .5, panel
  .66, never lower or contrast fails).
- **27. Pipeline\*.** Three to five 290 px glass nodes; each lands on its word as a cyan light runs the connector, lit
  cyan while the previous settles white; `payoff: true` lands magenta. The fast version of 6.
- **27b. 3D card chain** (won the blind A/B of 23/10/2026 against 27 on the `processo` bench window; creator: "much smoother",
  asked for the arrows, hated the pop sounds). `formats/chain3d.py`: `chain3d(steps, t_in, t_out)` returns `html` + `js`
  for `raw_html`/`raw_js`; `write_swish(public)` makes `sfx/swish.mp3`. Three to five glass cards 560x340 (badge icon, number,
  one-line title 56 px/700 of three words at most) on a `perspective: 1500px` stage; card centres X = 0/980/1960/..., Y = 0/-70/+60/-50/0,
  Z = 0/-120/0/-120/0, rotY = -10/+10 alternating. The camera is `#bcc` (x, y, z) with `sine.inOut`: the next card is at rest in
  the centre 0.1 s before its word (travel [word-2.0, word-0.1], never under 1.4 s, 0.6 s of rest after the previous arrival);
  the new card fades/scales in during the last second (`power3.out`, scale .92 to 1, rotY to 0), the old one goes behind
  (opacity .4, z -160, `power2.inOut`, 1.0 s); the title has 60 px of parallax; at rest the stage drifts 0.6 %/s. Cyan edge on the
  active card, magenta on the last. **Soft arrows** card to card (right edge to left edge, 3D, inside the same camera): 6 px body
  with 0 to .9 to 0 opacity along its length and 1.6 px blur, a 26x30 px head with a soft glow, 36 px short so it stops about 16 px
  before the next card; drawn in 0.6 s (`power2.inOut`) at the start of each travel, head fading in at +0.5 s, back to .4 with the
  old card; the last arrow is magenta. **Sound: one soft swish per travel, no pops, no clicks**: `assets/sfx/mixclap/whoosh-ethereal.mp3`
  cut to 1.9 s (attack 0.08 s, release 0.5 s), volume 0.25, at the start of each travel. Measured peak camera speed on the bench
  is 750 to 1100 px/s (the creator found it smooth, not fast); a longer window than 16 s allows slower travels, never faster.
  State sheet: `videos/_bench/ab/processo-glide/lab-B/STATE-SHEET.md`. Pipeline (27) stays for steps closer than 2.5 s apart.
- **45. Living shape** (won the blind A/B of 26/10/2026 against 27b on the `processo` bench window; idea from the
  @themilesholden reel, one neon shape that becomes a search bar, a price card, an eye; notes in
  `videos/_teardown/INSPO-NOTES.md` section 3). `formats/morph.py`: `morph(steps, t_in, t_out, public)`, steps are dicts with a
  `kind`: `pill` (logo + text typed letter by letter behind a gold spark, optional cursor `click`), `circle` (`icon`; the "globe" stands still as approved, `spin: true` turns it),
  `square` (`logo`, `logo_color` for a single-colour svg), `grid` (2 to 6 images; only the 6-image layout is checked on a render), `page` (the grid's tiles fly into a moodboard layout, `title` in Playfair Italic,
  `check_at` an emerald check). ONE shape, never a cut: it starts as a line with a spark, each change is 0.7 s `power3.inOut`
  ending 0.1 s before the word; old content blurs out (0.25 s), new content blurs in (0.35 s). Border 3 px gradient
  gold → ivory → emerald, dark glass inside, gold + emerald glow, two soft colour blobs (gold, emerald) following the shape 0.12 s
  late; the label (gold number + 44 px Inter name) rides 80 px under the shape. The camera drifts 1.00 → 1.05 in every state.
  Sound: the 27b swish once per change, nothing else. Steps closer than 1.2 s: use 27. Bench files `videos/_bench/ab/processo-morph/`.
- **28. Hub\*.** The idea in a 300 px glass circle with a cyan ring closing (`ring_at`), two to six parts arriving at the
  ends of spokes; `resolve_at` dims them to .56 and lights the centre ("all of that is really this").
- **30. Flowing paths\*.** An input pill left, two to four outputs, an optional result right, joined by S-curves and dim
  (.42) from frame one. A packet of light runs each path (0.9 s) and the pill lights on its word; at `result.at` light
  runs from every output 0.14 s apart and the result lands magenta; a second wave keeps it moving (`"repeat": false`).
- **38. Exploded layers\*.** One flat card tilts (rotateY -30, rotateX 16) at `split_at` and separates into two to four
  layers in depth (1.4 s, 0.22 s apart), labels on their layers, then a slow orbit.
- **26. Bar comparison\*.** A 76 px title, two to four rows of label (46 px) and bar, each on its word, growing 0.5 to
  0.9 s; the longest stops at 80% of the track; your row (`hi`) cyan with a glow, the rest white.
- **39. World camera.** One canvas in home-frame px (1920x1080 = zoom 1; nodes may sit off screen, or on a ring with
  `"polar": [cx, cy, r, deg]`). Node kinds: `card` (300 px: number, icon, 42 px label, 26 px sub), `pill`, `orb`, `hex`,
  `stat` (a 118 px number counting up + a cyan bar; `to` moves both on after the first count), `text`, `img`. Each node
  arrives on its word (glass stays hidden until then), can `lit` (cyan or `lit_color`), `dim` (.56; spent .33) and take
  amber `alerts`; `links` draw in 0.5 s and `run` sends a light along; `rings`, `window`, `dock` add circles, a window, a
  row of logos. `cam` = `[t, x, y, zoom, dur]`, one gesture each (`power2.inOut`, 1.0 s); a move that starts before the
  last ends fails the build. Open close on the thing you name (zoom 1.5 to 1.8), pull back to 0.8 to 1.0 as you say what
  it connects to, push to the next. Text 32 px or more at the zoom it is read at (the composer warns over 3.2).

### Cutaways and pages

- **18. Article cutaway with highlighter.** Full screen while you read from a page, cut in where your eyes drop (in a
  cut, the jump cut). Rebuild the page in HTML (real headline, byline, date, hero image, the site's own font): headless
  Chrome hits consent walls, and a rebuild makes the highlighter exact. Headline words get an amber block each
  (`rgba(255,185,4,.66)`, scaleX 0→1) stroked in one pass as the page appears (0.14 s a word, 0.035 s stagger), then a
  zoom into the headline for the rest of the read (1.0 → 1.42, `power1.inOut`), clipped under the 62 px chrome bar.
  Hard cuts in and out.
- **18b. Doc read.** The page rebuilt from the real kicker, title, date and paragraphs (a mark that is not verbatim fails
  the build; `"theme": "dark"` for dark pages, which get an amber underline). 0.35 s before each mark's word the camera
  glides to it at `zoom` (1.3), and on the word it is stroked in one pass; `focus` blurs the rest (a static copy; only
  opacity moves). Highlight on "highlight", zoom on "zoom": a mark can take its own `"zoom"` and `"move": false`.
- **19. Photo card.** Light glass 420 px wide, top-left: a 372 px square photo (radius 16), name 40 px/700, role 26 px.
  In on the name (x -40 → 0), gone ~1.8 s later.
- **20. Full-frame video cutaway** (hand-built). Your own screen recording first, public-domain archive for a metaphor
  second, then nothing. The `<video>` is a direct child of the root (`class="cutaway-video clip"`, its own timing
  attributes, `muted`, `z-index:20`); inside a timed wrapper it fails lint and shows the wrong frames.
  `object-fit:contain` does not paint its letterbox: `pad` to 16:9 with ffmpeg. Crop recordings to the window, re-encode
  like the footage (30 fps, dense keyframes, no audio), hard cuts, drift 1.0 → 1.04, 2 to 4 s; it hides a jump cut.
- **20b. Before/after wipe.** Two layers in a 1600x900 plate; the opaque after layer goes from `clip-path: inset(0px
  1600px 0px 0px)` to `inset(0px 0px 0px 0px)` (px on both ends so it interpolates) while a 5 px cyan line rides the
  edge, 0.65 to 1.1 s on the verb.
- **20c. Clip** (`clip`). Format 20 in the composer (muted, root level, z 20, drift, hard cuts, `anchor` on your words)
  for screen, archive, stock and AI B-roll conformed by `broll-conform.py`; an optional `label` or checklist (`items`).
- **37. Image reveal\*.** An image behind seven dark slats that close to their centres on `reveal_at` (1.1 s, 0.12 s
  apart), then a push 1.00 → 1.06; `"close": true` shuts them before the cut back. Stills only.
- **13. Prompt window.** A dark window, the prompt typing in as you read it (a cyan mic glyph and "Dictated" if you
  dictate). Characters start `display:none`, never `opacity:0`, or the caret parks at the finished width.
- **42. Chat.** Messages one by one: yours (`me`) cyan with dark text, theirs (`them`) white. `float` (up to five bubbles
  beside you), `window` (a dark app window that grows with the thread and scrolls once full) or `phone`. No anchor unless
  you read a message out. A client message is your example or a real one with permission, never made up.
- **36. Button → player\*.** A glass "Watch this next" pill grows into a 600x444 player at `morph_at` (1.1 s), the play
  icon travelling into the thumbnail; the real thumbnail, title and length fill in and the scrubber moves.
- **Thumbnail grid** (`grid`). Six of your thumbnails in a 3x2 grid; the oversized cursor clicks one (`click_index`,
  `click_at`) and the rest dim. Get them with `yt-dlp --flat-playlist -j <channel url>` and
  `https://i.ytimg.com/vi/<id>/maxresdefault.jpg`.
- **Coded scenes** (`scene`, no stock): `money` (amber $ chips drop on the word, never a digit), `catalog` (frames fill,
  one shine), `room` (furniture drops into a line-art room), `plate` (a phone with a plate: sweep, sparkles, steam),
  `profile` (the avatar gets its ring on "headshot"); `steps` time each kind, `label*` keys add the caption.

### Accents and asks

- **10. Success stamp.** A cyan circle with a dark check, a 62 px/700 label, glass with a cyan border, scale .86 → 1
  `back.out(2)` ~0.45 s (the house's one overshoot), bottom-left, ~5 s, on your own word ("boom", "it worked"), never on
  a read of the screen.
- **11. Description pointer** (`pointer`). A glass bar at bottom 34, "Everything is linked in the description" (cyan on
  the link phrase), three chevrons cascading beneath (0.14 s stagger, ~0.78 s cycle) on a finite loop, never `repeat:-1`.
- **14. Subscribe bar.** A pill glass bar: your channel mark in a dark avatar circle, the name 42 px/700, a 22 px/500
  tagline, a YouTube-red `#FF0000` pill 30 px/700 pulsing a finite 3 times (scale 1.08). Away from your head, under
  ~720 px wide.
- **17. Vignette + grain** (`vignette`). Radial darkening and fine grain: a beat, not a look (the pause after a dad joke).
- **23. Tutorial layout (not built yet).** The screen as a rounded plate, your face in a rounded crop bottom-right (a
  360x540 corner, right and bottom 48, radius 32; full to corner in 0.6 s `power3.inOut`, 0.3 s before the word),
  switched with `tl.set`, never a class toggle (not seek-safe).

### Explainer formats (formats/studio.py): the graphic is built on the spoken word

Added 19/10/2026 from the inspiration study (Iman Gadzhi, Callaway, Pedro Andrade, Marshall Crew; notes in the project's
`inspo-analisi/ANALISI.md`). In every reference the graphic IS the explanation, built piece by piece on the word, with real objects
(a logo, a swatch, a flat), a camera that moves through space, and one visual identity. Colours and font are CSS variables
(`--k-*`, `DEFAULT_STYLE` in studio.py, overridable with `"style": {...}` in the storyboard), so the creator's palette changes once.

| Type | Use for | Shape (all times are word starts; every item has an `anchor`) |
|---|---|---|
| `build` | a list said out loud: picture, then label, then value (swatches, assets, specs) | `{"type":"build","title":"ASSET","items":[{"img":"img/a.jpg","label":"Immagini","value":"..","at":t,"label_at":t,"value_at":t,"label_anchor":".."}]}` (1 to 4 items) |
| `annotate` | one picture (a flat, a figurino) with callouts whose lines DRAW onto it, each on its word | `{"type":"annotate","src":"img/flat.png","max_h":860,"callouts":[{"label":"..","sub":"..","x":.33,"y":.36,"side":"l|r","dy":0,"to":[x2,y2],"at":t,"anchor":".."}]}` (x/y fractions of the picture; `to` = a measured segment) |
| `orbit` | a card beside the speaker that is carried into a dark space where satellites (logos, people) fly in and connect to it | `{"type":"orbit","center":{"src":".."}|{"text":"..","sub":".."},"card":[w,h],"pre":{"go_at":t},"nodes":[{"src":"img/logo.svg","logo":true,"caption":"..","at":t,"anchor":".."}]}` |
| `dive` | a screen or page: starts zoomed on one detail, then the camera pulls back to reveal the whole | `{"type":"dive","src":"img/page.png","focus":{"x","y","w","h"},"reveal_at":t,"reveal_dur":0.75,"click":{"x","y","at"},"tilt":true}` |
| `trail` | **a page, a still or a tool that rests on screen, then the camera pulls back through 3D space, the window shrinks and an arrow leads to the next thing** (a key word, a logo, another page). The default for showing a page of the creator's work | `{"type":"trail","nodes":[{"id":"p","kind":"page","src":"img/p07.png","w":1100,"x":0,"y":0,"rot":-5,"at":t,"anchor":".."},{"id":"k","kind":"key","text":"Palette colori","x":1250,"y":-60,"z":140,"at":t2,"anchor":"-"}],"links":[{"from":"p","to":"k","at":t2}],"cam":[[t,0,0,1.2,-3,0],[t_pull,cx,cy,zoom,-13,2,1.35]]}` (kinds: page, key, logo, card; the camera's first row is the starting pose, the others are moves; zoom 1 = 1920 x 1080 of canvas) |
| `captions` | **word-by-word captions in the middle of the frame** (bold sans, one word at a time with a small pop); the key words in the **italic serif** (Playfair Display) | `{"type":"captions","top":650,"words":[{"text":"tecnicismi","at":t,"end":t2,"em":true,"color":"#e14a4a"}]}` |
| `halo` | **REJECTED for long-form (creator, 19/10: "more vertical TikTok / Instagram than long content"); do not use it in a YouTube video.** A dashed ring around the speaker's head with short labels and a line above the head | `{"type":"halo","cx":1010,"cy":540,"r":360,"top":{"text":"ASSET","at":t},"pills":[{"text":"Immagini","at":t,"angle":198}]}` (measure the head on a frame first; a glow behind the head needs a subject matte) |
| `gallery` | a wall of the creator's pages under a small tag ("Portfolio 17 tavole"); one is picked, the rest dim, and it flies to the centre at the size the next `trail` starts from (`enter: false` on that page) | `{"type":"gallery","images":[..],"cols":6,"tag":"Portfolio","tag_em":"17 tavole","select":{"index":0,"at":t,"w":1100}}` |
| `agenda` | a fixed list beside the speaker that gets one more line at every topic and stays | `{"type":"agenda","pos":"tl|ml|bl|tr","items":[["Tessuti",t,"anchor"],["Costruzione",t]]}` |

Rules from the creator's notes on the first test (these are the taste of the `elegante-portfolio` preset; another preset may choose differently):
- **A logo, not a word, for a tool or a brand** (`orbit` nodes with `src` + `"logo": true`; the text disc is a placeholder until the file exists).
  **Never write a technical term the audience does not need** ("MCP"): say "Claude connected to Canva" with two logos, not three labels.
- **`dive` must be fast.** It enters already zoomed, the pull-back starts within ~0.5 s of entering and lasts at most 0.8 s
  (`reveal_dur`); never hold the zoomed state 2 to 3 s. The `focus` is a small detail (zoom 3x or more; a focus as tall as the
  picture barely zooms). A giant face of a person as the zoomed start reads badly: pick a neutral detail or a title.
- **`build` holds only as long as the last item needs** (end ~1 s after the last label), not until the sentence ends.
- **`agenda` only where it matches the spoken moment:** each line enters on the word that names its topic; never a list the
  speaker is not reading out. **`annotate` is the creator's approved look** (lines drawing onto a figurino, label per spoken
  instruction); only the font and colours change.
- **A page never just appears and leaves, and a plain note line over it is not enough** (creator's note on the v3 test): the page rests a few
  seconds, then the camera pulls back, the window shrinks and an arrow leads somewhere else (`trail`). **Approved by the creator, "in every
  way it is used":** the arrow trail is the model for every page, flat and diagram in the video. The camera never stops: after the last move it keeps
  drifting until the scene ends. Frame every node in the pull-back (the lab builder's `fit()`).
- **Camera on every explainer scene, figures included** (creator, 19/10: the figurino test "moves too little, we do not even notice"). `annotate` with
  `space: true, frame: false, dolly: [1.12, 0.96], label_z: 110` keeps a garment centred, and **`follow: {"zoom": 1.24, "pan": 0.54}` swings the camera
  fast toward each arrow and its label (about 0.4 s), holds about 1 s while the text is read, and returns to the figure**; the swing stays modest so the
  head is not cut off. Clarity first.
- **The secondary font is applied to the key words, not only to captions** (creator on v5: "I do not see the new font"): `style.keyfont` / `keystyle` / `keysize`
  set the key word at the end of a `trail` arrow, and `style.lines.serif_em` (+ `serif_em_scale`) sets the `em` words of every lower line, both in the italic
  serif (Playfair Display Italic, the creator's choice). Declare it in `style.font_faces` or it falls back to the system serif.
- **An explainer scene ends right after its last element has been read** (about 0.5 to 1 s), then back to the main camera; never hold it to the end of the
  sentence (creator on the figurino test: "the end must be cut, it is too long"). **`gallery` into `trail` is approved ("practically perfect")**: the picked page
  flies to the centre at the size the `trail` starts from (`enter: false`, `rot: 0`, first camera zoom 1.0), so there is no cut.
- **Fonts: the base sans only** (Inter, the free SF Pro look; real SF Pro is licensed for Apple-platform UI only). **No handwriting font**
  (the creator rejected it; do not use Caveat, `style.hand`/`hand_em` stay off). On a scene with one plain background, give the key
  words **glow and gradients** instead (`text-shadow` glow in the accent colour, gradient text): no white bands or chips behind labels
  (`build` labels are gradient text with a glow line, not a white chip). **Key words in captions use an italic serif, Playfair Display** (SIL OFL, `assets/fonts/PlayfairDisplay-Italic.ttf`; the creator's reference was a high-contrast italic logotype, and the inspiration reel emphasises words exactly this way); everything else Inter.
- **Work in the lab, not on the whole video** (creator's request, 19/10/2026): test every change on a small window with
  `window-patch.py` (10 to 25 s, rendered in about a minute) and put it in the full video only after approval; a full render costs
  35 to 70 minutes and many tokens.
- Pages of a portfolio shown as stills: a 3D window (`browser3d`) at most 6 s, whole page, never cropped; no slat-reveal slides.

### Rejected (do not rebuild)

- Freeze-frame and paper-and-tape dressing; an outro or end card; a "Next video" pill at the end (the YouTube end screen
  does that job); payment or system notification banners.
- The `halo` ring with pills around the head and short-form-style word-by-word captions over the face: vertical-feed language, not long-form (the creator discarded the ring; captions are on hold until he confirms).
- Typing with a trailing caret for lower lines; word-by-word highlighter pacing on an article (one stroke, then zoom).
- The flash cut on a return (two white blinks read as a mistake): for energy use the fast punch, or leave the cut naked.
- Dark blue `#0005EE` for highlighted words (it disappears on dark footage); magenta outside the chip and payoffs.
- Pop sounds (`pop1`) on the 3D card chain's steps (creator, 23/10/2026: the sound effects are bad); on that format only the soft swish per camera travel.
- Bounces, elastic type, spring stacks, particle logos, idle wobble; generic stock of a smiling founder at a laptop.
- From the @toolandtea reel (26/10/2026, muted demos in `videos/_bench/ab/`): the paper-cutout collage of torn photos
  (`collage-onlife`, "inguardabile") and the stylized street map with a walking route (`mappa-tessutai`, "inguardabile").
- The curved wall of pages (camera inside a cylinder of the creator's boards, columns lit by group): lost the blind A/B of
  26/10/2026 against the dot grid (43) on the `lista` bench window ("I prefer the grid, even if it is simpler"). Bench files
  `videos/_bench/ab/lista-muro/`.
