---
name: fashion-3d
description: Build 3D animated videos for Jacopo's channel and Inverso entirely in code (three.js, rendered by HyperFrames): vertical 3D Shorts in the atelier world, animated 3D explainers (the "Autogrill" format), metaphor worlds, a 3D garment that turns, and Jacopo's own 3D mascot. Use for any request about a 3D Short, a 3D scene, a 3D garment, "mondo 3D", mascotte, or realism of a 3D render. NOT for cutting camera footage, grading, plates on a talking head (that is youtube-edit).
---

# fashion-3d: 3D films in code

*Born 16/11/2026 as a split from `youtube-edit` (which keeps editing, motion plates, grading, sound). This skill owns everything about generating 3D.*

## Where things are

| Need | File |
|---|---|
| Make a vertical 3D Short (steps, voice, sound, review, render, publish) | `references/short-3d-sop.md` |
| Make a 3D explainer (one cartoon world the camera flies through) + product/scenery kit | `references/explainer-3d-sop.md`, `formats/explainer3d/` |
| Jacopo's verdicts and taste on 3D (read BEFORE building) | `references/taste-3d.md` |
| What the 8 fps study of the reference reels taught us (continuous camera, never still, metaphor worlds) | `references/inspo-8fps-2026-11-16.md` |
| Realism upgrade plan and the tools researched (Blender, Hunyuan3D, UniRig, dream-loop) | `references/realism-plan.md` |
| Engine code (world3d.py, atelier-*.js) | still in `youtube-edit/formats/world3d.py` and `youtube-edit/assets/vendor/` (moves here in phase 3, with the realism upgrade and a before/after test) |
| Sound, voice, mix | same method as `youtube-edit/references/sound.md`; the Short/explainer SOPs say which parts apply |

## Rules that always apply (from Jacopo's notes and the 8 fps study)

1. **Every frame is a pure function of time.** No clocks, no random, no state between frames (the render jumps around).
2. **Never still for more than 0.8 s.** Between words there is always an object move or a camera move; check it on an 8 fps contact sheet before every render. (Measured on our Shorts: 1.5 s holds with only a caption on screen.)
3. **The camera glides continuously and follows the object that acts**, with depth of field always on in the metaphor/diorama look. Whips are 3 frames with real motion blur, not the main move.
4. **The hero object gets the modelling hours** (garment with waistband, loops, welt pockets, seams, real fabric surface); the room comes second.
5. **A character who reacts** gives life to the empty moments: Jacopo's own 3D mascot (a small stylised Jacopo, built from `personale/style_jacopo` memory: fitted/wide silhouette, Texan boots, selvage denim, black + indigo + olive), never a spool or a generic thing. The channel is a personal brand.
6. **Open on the logo / a vivid first frame; the hook is TRUE in frame 1.**
7. **No venetian-blind light** (Jacopo: it reads as a render error). A real window with a real cross is fine.
8. **Review at 8 fps** (contact sheets of 24 frames = 3 s) before any 4K render. Time estimate to Jacopo before long renders.
9. **Show before you spend:** stills, then a draft, then the final. `videos/` is local only (outside git); renders go to iCloud › Video 3D moda with the version in the file name.

## Status

- Phase 1 (research of tools) and phase 2 (this split): done 16/11/2026.
- Next: phase 3 realism upgrade (environment lighting, single grade, soft shadows, `.glb`, bevels, window view); phase 4 Blender garment test; phase 5 metaphor-world format + the mascot; phase 6 automatic checks. Plan and progress: `references/realism-plan.md`.
