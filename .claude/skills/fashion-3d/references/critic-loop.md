# Critic loop (adapted from dream-loop, MIT, github.com/achimala/dream-loop, 16/11/2026)

Idea taken: build toward a TARGET image, and let a fresh, independent judge compare the live frame to the target and list what is wrong, round after round, until it scores high. Our version differs in three ways:
- The target is a real photo chosen by Jacopo, OR (from 16/11/2026, Jacopo chose Gemini) a target generated with `scripts/gen_target.py` (Gemini image API, key in the gitignored `.env`, output in the gitignored `.critic/`; prompt written with the banana-pro-director skill and Jacopo's Drop 1 spec: wide straight leg, double Italian pleats, side adjusters, turn-ups, olive drill). The fal.ai script of dream-loop is NOT installed.
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

## First round (16/11/2026, Blender trouser v11, no target image, Sonnet judge)
The judge gave 4/10: composition 1, light 1, materials 1, details 1.
- **Applied:** fix 1 ("the twill reads as huge diagonal stripes / moire"). `w.glb(..., fabric=True)` now uses a finer, weaker twill (`clothMat` `tile` 2.5, normal 0.4). The before/after is in `videos/_bench/fashion3d/blender/twill_ab.jpg`. `clothMat` without `tile` is unchanged, so Short #2 is not touched.
- **Rejected:**
  - "legs too wide": the wide straight leg is the Drop 1 design;
  - "cartoon set / no mannequin": that is a lab setting, not the target.
- **Open, by impact:**
  - pleats not readable from the front (they need sharper geometry);
  - fly and crotch bulge;
  - turn-ups too round;
  - orange rim on the waistband top (rim light);
  - bartack glitch at the pocket end.
Lesson: without a real target the judge measures against a generic "product photo" and pushes toward slim trousers, so give it Jacopo's spec (`project_inverso_pantalone_drop1`) and a real reference.

## Round with a real target (16/11/2026, Gemini target `.critic/target.png`, prompt in `.critic/target_prompt.txt`)
- The target was generated with `gen_target.py` (gemini-2.5-flash-image, 9:16, one image for about 0.04 EUR). It is good: sharp creases, brass adjusters, 4 cm turn-ups, a night atelier.
- Our matching shot is `videos/_bench/fashion3d/lab_target.py`. The judge gave **3/10**. Its main gaps: no pressed crease, pleats not readable, olive too saturated, flat bright light, a bulge at the fly, lumpy turn-ups.
- **Applied:**
  - drill colour `#66664a` (less saturated, browner);
  - pressed crease and pleat ridges added AFTER the cloth sim (`P["crease"]`, `P["pleat"]`; the sim and the 7 mm voxels washed them out);
  - voxels at 5.5 mm, so the bake now takes about 110 s;
  - a darker key-light setup in the lab.
- **Result:** colour and mood are closer. The crease is now there but only faintly visible, because the voxel size still rounds the ridge and DOF softens it.
- **Next fix by impact:**
  - a real crease, as a hard edge (edge split / a crease seam in the mesh) or a normal-map line, not a displacement;
  - remove the fly bulge (the crotch relax step pushes material forward);
  - crisper turn-ups.
