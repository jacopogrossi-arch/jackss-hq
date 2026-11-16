# Critic loop (adapted from dream-loop, MIT, github.com/achimala/dream-loop, 16/11/2026)

Idea taken: build toward a TARGET image, and let a fresh, independent judge compare the live frame to the target and list what is wrong, round after round, until it scores high. Our version differs in three ways:
- The target is a REAL reference chosen by Jacopo or by us from real photos (a real pair of trousers on a hanger, a real atelier), never a generated "dream" image (we have no image generator connected; the fal.ai script of dream-loop is NOT installed).
- The frame is an 8 fps contact sheet or a still from the HyperFrames/Blender render, not a browser screenshot.
- The judge is a fresh subagent with the Agent tool (model: sonnet is enough), with no memory of the builder's story.

## Loop
1. Fix the target (`.critic/target.png`, gitignored) and the shot to judge (time `t` or Blender camera).
2. Build/render the current frame (`snapshot` for the three.js world; a Blender still render for hero shots).
3. Give a fresh judge: the frame, the target, the previous frame and verdict, and the rubric below.
4. Fix EVERYTHING the judge named (actionable items only), re-render, judge again.
5. Exit rules: score >= 8 done; stall (no +1 point in 2 rounds, or the same gap named twice) -> stop tweaking, rethink the whole approach once; if that fails, ask Jacopo.

## Rubric for the judge (our version, 0-10)
- **Composition (0-3):** camera, framing, scale and position of every major element vs the target.
- **Light (0-3):** palette, exposure, shadows (soft/contact), contrast, reflections, glow.
- **Materials (0-3):** every surface right: fabric weave and sheen, folds, seams and stitches, wood grain, metal; nothing blocky, plasticky or flat unless the target is.
- **Details (0-1):** small things: belt loops, welt pocket bar-tacks, buttons, labels, dust, wear.
Instruct the judge to be nitpicky, to name the exact cause of any "fake" impression and the exact fix, and to say when a prop must be redesigned.

## Fixed checks that need no judge (automatic, from the 8 fps study)
- Never-still scan: no more than 6 consecutive frames at 8 fps (0.8 s) with no object or camera change except captions.
- Seek test: one frame rendered alone equals the same frame inside the video (PSNR > 40 dB).
- Camera speed per frame: no spikes.
- Three consecutive frames at the risky spots: nothing flickers (z-fighting).
