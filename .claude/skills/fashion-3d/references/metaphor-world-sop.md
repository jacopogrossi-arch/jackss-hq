# SOP: metaphor-world Short (new format, 16/11/2026)

From the drillup.io reels studied at 8 fps (see `inspo-8fps-2026-11-16.md`): an abstract idea becomes a physical game world, and the whole Short is a camera that glides through it following one character.

**Examples that worked for them:** a gym (reps = tries), a claw machine (one more grab costs nothing), a Monopoly board (money between friends). **For fashion (ideas, to be chosen with Jacopo):**
- "Quanto costa un pantalone" = a board game where each square is a cost (tessuto, taglio, cucito, margine) and a token (Jacopino) walks it, the price counter rising.
- "Perché il pre-order" = a claw machine with garments; one grab = one drop.
- "Un errore costa" = a corridor of doors, each phase (disegno, cartamodello, tela, capo) with the cost of a mistake as a counter.

## Rules (all from the 8 fps study and Jacopo's notes)
1. **One idea, one world, one character.** The character is Jacopino (`w.mascot`), the small 3D Jacopo; the world changes per Short, the language stays (map, pinned labels, phase pill).
2. **The camera never stops.** Continuous glide, shallow depth of field on (`w.dof`), follows the object that acts. Check with `scripts/review8.py still` (no dead stretch over 0.8 s).
3. **Every action starts ON its word** (a card flies on "send"). Time everything to `words.json` with `at("word")`, never to hand-written seconds.
4. **Data are objects:** `dotgrid` (1 tile of 10 lights up = "1 in 10"), counters, bars, a coin stack. The number is spoken AND physical.
5. **A change every ~1 s** somewhere in the frame (objects pop in staggered, a light crossfades, a card swaps with a 3-frame blurred slide). A caption alone never counts.
6. **The ask lives in the world:** `ctaplate` ("Scrivi *PANTALONE*"), written on an object, not a sticker. Pair it with a first-comment keyword (the channel's goal is discussion in the comments).
7. **Hook TRUE in frame 1:** the first frame already shows the world and Jacopino in motion; the logo is seen early.
8. **The hero object gets the modelling hours** (garment: waistband, loops, welt pockets, seams, real fabric). From now on a hero garment is a Blender `.glb` loaded with `w.glb(...)` when the Blender test (see `blender-test-plan.md`) shows it is worth the render time.

## Beat template (60-75 s)
| Time | Beat |
|---|---|
| 0-3 s | The world in motion + Jacopino + the hook line. Logo seen. |
| 3-15 s | The first square/phase: character walks to it, the number appears as an object. |
| 15-45 s | Two or three more phases; each a different camera idea (aerial, macro, low sideways) and a different colour contrast. |
| 45-60 s | The twist (the surprising number) as a physical event (the grid lights, the token falls). |
| 60-70 s | The morale, then the `ctaplate`, then the logo plate. |

## Build and review
Same steps as `short-3d-sop.md` (voice per paragraph, words, mix, 10 fps draft) but review at **8 fps**: `python scripts/review8.py sheets VIDEO OUTDIR` and `python scripts/review8.py still VIDEO`. New engine pieces: `w.mascot`, `w.prop("dotgrid"|"ctaplate", ...)`, `w.glb`, `w.photo()`.
