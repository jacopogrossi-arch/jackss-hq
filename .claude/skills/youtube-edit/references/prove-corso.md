# Prove del corso: what Jacopo voted (05/11/2026)

45 tests from the "Cash Flow Contents" After Effects and Premiere modules, voted one by one on the private page (https://claude.ai/artifact/JBkKXuCWwJo6ZE5GX21SxW, db collection `votes`). 38 yes, 4 maybe, 2 no, 1 note without a vote.

Read this when designing plates, cuts or reels. The working code of the plate tests is in `lab-corso.py`: the name in brackets is its function there. It is lab code on the `Seg`/`Lab` bench, so port the idea into `scene.py` or by hand; `tl.fromTo` with explicit values stays the rule. A yes means "allowed, use it where it serves the sentence", not "use it everywhere". The variety rules in `taste.md` still apply.

## Already the default in `formats/board.py`

- **Swipes:** curve D `cubic-bezier(.54,0,0,1)` at 1.3 s. Note on the dome comparison: "curva D tutta la vita". Don't propose the dome again for swipes.
- **Grid depth:** the grid travels at half the speed of the pages (`GRID_DEPTH`; `Board(depth=1)` turns it off). "Poca differenza ma è un dettaglio che conta."
- **Camera glides inside a page:** `cubic-bezier(.5,0,.3,1)`, peak near 40% (`GLIDE_EASE`). The 40% was read by eye from the lesson, not measured.

## Yes, with his note

| Test | What it is | His note |
|---|---|---|
| Phrase that accumulates [`phrase`] | words stack up as they are said | "questo bellissimo" |
| Text from an invisible edge [`edge`] | text slides out from behind a line | "bellissimo" |
| Light sweep on a card [`sweep`] | a band of light crosses the card | "bellissima" |
| Vertical swipe, short side [`swipe(vert=True)`] | pages one above the other, `at=(0, 1)` | "molto bella" |
| One master per plate [`master`] | one driver, staggered starts | "molto meglio partenze sfalsate": the normal way to bring in a group |
| J cut on reactions | audio leads the cut | "ottimo taglio a J" |
| Circular tilted grid [`cgrid`] | | "bellissima se lavoriamo su piani 3d": only on 3D planes |
| Video inside the letters [`letters`] | | "bello x i travel blog": travel, not plates |
| Pieces that assemble [`pieces`] | | "curva D": use D, not the late peak. This overrides the late-peak family from lesson 18 |
| Light arrives with the pieces [`pieces`, glow option] | | "arrivo con i pezzi": the event light, not the fixed glow |
| Motion blur [bench `sw/`] | | "scia lunga molto bella": see Open below |
| Still background, no grid [`swipe(mode="fermo")`] | | "utile in alcuni contesti" |
| Focus follows the word [`focus`] | | "utile in alcuni contesti" |
| Slight wiggle [`wiggle`] | | "differenza quasi impercettibile": only survives on a high quality file (crf 15) |

Yes without a note: slow scale that never stops [`slow`], plate change in the speed peak [`peakcut`], transition across the cut (move the title too, onto a word of the sentence that is ending, or about 1 s of board stays empty), big number behind [`bignum`], text hidden by mosaic [`mosaic`], text behind the head, tightening spacing [`spacing`], number in a ring [`ring`], word on a line [`online`], 3D text with thickness [`text3d`], light reveals the title [`lightreveal`], camera inside the text [`inside`], lens mask [`lens`], proximity [`prox`], edge follows the light [`border`], glow and vignette on top [`finish`], fake 3D shapes [`cyl`], transition with a repeated shape [`shapetr`], speed ramp with invented frames (reels; check slow parts for soft or double edges).

Grading: `scripts/grade-1090.py` is the fixed 10-90 check after a grade.

## Maybe: only with a reason

- **White flash** against the light leak: "questo flash non è bellissimo". The light leak stays first choice.
- **Gesture with rotation** [`rot`]: "un po' macchinoso". Not by default.
- **Turbulence wave** [`turb`]: "non bellissima".
- **Speed ramp on footage shot slow:** "dipende dalla situazione": decide per clip.

## No: don't propose again

- **Inverted colours on a strong sentence:** "non adatto al nostro stile".
- **Curve D on the plate opening (face to board):** "meglio uno swipe più veloce in questo caso". `PUSH` stays at 0.9 s with `power3.inOut`.

## 60 fps and motion blur (Jacopo, 05/11/2026)

- **60 fps is the standard** for YouTube finals: `--fps 60`, 60M. The footage stays at 30, the graphics get 60. Drafts stay at 30. A window of Video #3 rendered at 60 came out at 360 frames in 6 s, in 105 s. A full 4K costs nearly double the 30 fps time, not the +40% of the short test.
- **Motion blur with the long trail: sparingly.** "Rende tutto molto più clean, usiamolo con parsimonia per non aumentare troppo i tempi." Only on the few swipes that matter most, chosen in the plate plan, and tell Jacopo which. It costs about ×10 on the shots it touches.
- **Method:** copy slowed 4×, render at 240 fps (960 effective), then fuse. Slow down both the `data-start`/`data-duration` values and the `__outer` tween duration, or the copy comes out at normal speed. For a 60 fps output: `tmix=frames=32,select='eq(mod(n\,16)\,15)',setpts=N/60/TB`. Script of Video #3: `videos/03-brand-ai/final-v5/scia.sh` (local). Real cost in 4K: 7 s of window in 39 min.
- **Choosing the window:** plate only, no face. Start and end where the picture is nearly still, measured frame by frame on the raw, so the trail does not vanish abruptly. A window can run longer than the swipe it was chosen for.
- **Splicing (tested on Video #3, 06/11/2026):** with `--gpu` the keyframes fall every 250 frames, `--keyframe-interval 1` is ignored. Re-encode only the keyframe-to-keyframe stretch holding the window with `h264_nvenc -profile:v main -rc vbr -b:v 60M -maxrate 120M -bufsize 120M -g 250 -bf 0`: that gives the same SPS as the raw. Then join with the concat demuxer in stream copy (`inpoint`/`outpoint`), and check that the frame count is unchanged and that the picture outside the windows matches the raw.
