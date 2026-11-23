# Research: tools and skills for a top-level Blender (23/11/2026)

Why: Jacopo's call (23/11) — no AI shots mixed into our 3D Shorts (the quality jump shows); our Blender must reach the level of the hybrid test clip by itself (`realism-plan.md` phase 7, target `videos/_bench/ibrido/video/lipsync-v1.mp4`). Pace to hold: one Short every 2 days, so every tool must be fast and free or one-off.

Machine limits checked today: **GTX 1060 6 GB** (driver 576.52), **C: is FULL (1.1 GB free)**, D: has 362 GB. Every install, cache, model and render goes on D:. Blender 5.1.

## The gap, and what closes it (ranked)

### 1. Face and mouth (the biggest gap: "sewn mouth")
| Option | What | Cost / licence | Verdict |
|---|---|---|---|
| **Rhubarb Lipsync NG** (github.com/Premik/blender_rhubarb_lipsync_ng) | audio → 9 mouth cues (A–H, X) keyed on shape keys OR pose Actions | free, MIT, CPU only; tested on Blender 5.1 and 5.2 (Windows); zip v1.8.1 dragged into Blender | **USE.** Baking shape-key NLA needs the separate "Bake Shape Keys" add-on. |
| **Replacement mouths** (stop-motion / Lego / Laika method) | 8–10 mouth SHAPES as separate objects or decal textures swapped per frame (visibility or UV Warp), driven by Rhubarb cues | free | **Probably best for Jacopino**: a faceted Tripo head has no clean face topology for deforming shape keys; a swapped mouth reads as "toy" and is crisp. Test against shape keys in the twin shot. |
| EL4CTEO `blender-facial-shapekeys` skill | creates ARKit 52 / visemes, split/mirror, correctives via `scripts/shapekeys.py` | MIT, updated 21/11/2026; needs Blender 5.2 LTS+ | Worth installing if we upgrade to 5.2 LTS; read its script before use. |
| Faceit (paid ~60 $) / FaceKeys (paid) | auto facial shape keys for any character | paid | Only if shape keys win and making them by hand is too slow. |
| Brows | Jacopino wears sunglasses always: the BROWS above the frames carry the emotion (the AI clip proved it) | — | Add 2 brow objects/shape keys (up, down, frown, one-side). |
| iPhone face capture (Live Link Face + free Blender add-on, Face Cap, FACEMOTION3D) | Jacopo acts the line on the iPhone, 52 ARKit weights onto our shape keys | free/freemium; needs ARKit-named shape keys | Phase 2: real performance with zero animation hours. |
| NVIDIA Audio2Face-3D (open: SDK MIT, models NVIDIA Open Model Licence) | audio → ARKit blendshapes with emotion | runs as ONNX-TRT; 6 GB GTX 1060 NOT confirmed | Skip for now. |

### 2. Body acting
| Option | What | Verdict |
|---|---|---|
| **Jacopo acts the gesture on his phone → mocap → Jacopino** | the most natural acting for zero animation skill | best long-term path |
| ↳ **VideoIntoBlenderModel (v2bm)** github.com/s0ck3t/VideoIntoBlenderModel | monocular video → skinned .glb, 61-bone rig + 52 ARKit morphs; CPU by default (MediaPipe); Apache-2.0, commercial OK; Blender 4.2+/5.2 extension | **Try first.** Needs our rig as a BINARY FBX in T-pose (Mixamo names OK): convert the Tripo GLB. Don't enable CUDA (CuPy) on Pascal without checking. |
| ↳ RGB MoCap (toyxyz; fork mayalhc/Chamiseul_RGBMocap) | GVHMR / FlowHMR / ExMR, Mixamo retarget, FBX/BVH, Blender bridge | top quality but ~41 GB of models, peak VRAM 5.7–6.1 GB (only "low memory" mode fits our 6 GB), model weights NON-commercial. Second choice. |
| Text-to-motion: Tencent HY-Motion 1.0 (24–26 GB VRAM), NVIDIA ARDY (07/2026), MotionGPT3 | motion from a sentence | Not local on a 1060. Keep as idea only. |
| **Acting rules (Disney/Larson/Hooks)** | body first, lip sync last; 3/4 to camera; phrase the line as ONE gesture, don't hit every word; anticipation → action → reaction, don't dwell; bolder than live action; the shot must read with sound OFF | Put these in `blender_perf.py` choices and in the review: max 2 gestures per 5 s. |
| **Wiggle 2 / Wiggle Bones / Jiggle Physics** (free, GPL) | spring bones for follow-through: jacket collar, hair tuft, watch | Wiggle Bones is fixed for 5.0+; bake before render (the dynamic effect breaks motion blur). |

### 3. Render look
- **Move the final render from three.js to Blender EEVEE** (~3 s/frame at 1080x1920 on the 1060 = ~50 min for 30 s at 30 fps). Volumetric haze, real DOF, AgX, compositor grain. Blender 5.0 renamed the engine id to `BLENDER_EEVEE`; 5.2 LTS overhauls screen-space ray tracing (better reflections on vinyl).
- **Toy realism, Lego Movie method (Animal Logic):** wear on every surface — scratches, fingerprints, dust ("well loved"); strong depth of field as the main cue of small scale; real light transport on plastic. Animal Logic dropped motion blur on the figures for a stop-motion feel — an option for us too.
- Rim light from its own light/layer (Blender Studio "Wing It").

### 4. Camera
- **Camera Shakify** (free, GPL, shake data CC0; v0.5.1 for Blender 4.4+, 07/02/2026): real captured handheld shakes, layered and animated in influence. Parent the Shakify camera to an empty (reviews: it can disturb complex scene hierarchies).
- Curved path + eased F-curves (the installed `blender-cameras` skill), never linear.

## Agent skills (for Claude) found on GitHub
| Repo | Verdict |
|---|---|
| RobLe3/cc-blender-skill (we have 9 of its skills) | Add **`blender-animation`** (concrete F-curve/easing/shape-key/NLA recipes, Blender 5.x layered-action helper; note: it wrongly calls the 15 visemes "ARKit"). |
| **EL4CTEO/blender-skills** (MIT, 28 skills, 21/11/2026) | Strongest: `blender-facial-shapekeys`, `blender-character-rigging`, `blender-animation` (mocap retarget). Targets 5.2 LTS+. Its installer writes to global skill folders: copy folders by hand into `.claude/skills/` after reading the scripts. |
| ra100/blender-claude-plugin | bpy API reference, placeholder values; skip. |
| arjun988/blender-skills (94) | broad, marketing-heavy, ships MCP configs; skip. |
| composio opencode `blender-rigging-animation` | generic shortcuts; skip. |
| **Official Blender Lab MCP** (blender.org/lab/mcp-server; v1.0.3, 11/09/2026; needs Blender 5.1+) | exposes the bundled manual + API docs to the agent; compare with our community `mcp-for-blender` before switching (run only one at a time). |

## Suggested order for the twin shot (new session)
1. Upgrade to Blender 5.2 LTS on D: (needed by the EL4CTEO skills; better EEVEE). Keep 5.1 until the twin shot works.
2. Install Rhubarb NG + Camera Shakify + Wiggle Bones; copy `blender-animation` (RobLe3) and the 3 EL4CTEO animation skills after reading them.
3. Twin shot v1 in EEVEE on the `social/ibrido-jacopino/layout.py` scene: replacement mouths + brows driven by Rhubarb from `battuta.mp3`, `blender_perf.py` gestures (max 2), Shakify camera push-in.
4. Side-by-side with `lipsync-v1.mp4` at 8 fps; list the gaps; iterate.
5. Then try v2bm: Jacopo films the line, his gestures go onto Jacopino.

Sources: github.com/Premik/blender_rhubarb_lipsync_ng · extensions.blender.org/add-ons/iocgpoly-lip-sync · github.com/s0ck3t/VideoIntoBlenderModel · github.com/mayalhc/Chamiseul_RGBMocap · pixelsham.com (RGB MoCap review, 10/11/2026) · extensions.blender.org/add-ons/camera-shakify · extensions.blender.org/add-ons/wiggle-bones · github.com/EL4CTEO/blender-skills · github.com/RobLe3/cc-blender-skill · blender.org/lab/mcp-server · fxguide.com (Lego Movie) · animallogic.com · developer.nvidia.com/blog (Audio2Face) · arxiv.org/abs/2512.23464 (HY-Motion) · superhivemarket.com (Faceit, FaceKeys, Swap Animator) · blenderartists.org (replacement mouth, UV Warp) · developer.blender.org release notes 5.0 / 5.2.
