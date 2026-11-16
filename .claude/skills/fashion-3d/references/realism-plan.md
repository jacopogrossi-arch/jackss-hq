# Realism plan and tool research (16/11/2026)

## What the 3d-animator skill (from @holcdenis, `INSPO 3D/3d-animator.zip`) does that our engine does not
Verified by grep on `world3d.js` + `atelier-*.js`: no environment lighting (IBL), no bloom, no single grade (ACES/vignette/grain/fringe), no soft-shadow accumulation or sky-fill AO, no `.glb` loader, no bevelled boxes, no window view.
We already have: pure function of time, camera curves, DOF (`dof()`), motion blur (`shutter()`), shadows, ink/clay passes, looks.
New useful methods from it: seek test (a frame rendered alone must equal the same frame inside the video, PSNR > 40 dB), camera-speed print to find jerks, per-version `NOTES.md`, phone-speaker sound rule (effects in 1-8 kHz, effects bus peaks under -10 dBFS, effect ~ voice -6 dB), glb credit line in captions (CC-BY).
Not to import: venetian blinds; the laptop-frame composite as a default.

## Tools researched (web search 16/11/2026; nothing installed)
| Tool | Finding | Verdict for Jacopo's PC (GTX 1060 6 GB, Windows, Blender 5.1 already installed) |
|---|---|---|
| Blender MCP (ahujasid, renamed `mcp-for-blender` on 01/09/2026) | MIT per most sources, install with `uvx`; Claude drives a live Blender | **Installed 16/11 (Jacopo's call: no copy-pasting code).** Headless scripts (`blender -b -P script.py`) stay the fallback for batch renders. |
| Blender skills (`kevinbadi/blender-skills`, `RobLe3/cc-blender-skill`) | Skill folders for Claude; kevinbadi's needs a Meshy API key (paid) | Unverified contents; read the repo before adopting anything. Write our own small Blender recipe for the garment instead. |
| Hunyuan3D 2.1 | 10 GB VRAM shape, 21 GB texture, 29 GB both; Community License EXCLUDES the EU/UK/South Korea | **No.** The GPU is too small and the licence excludes Italy. |
| UniRig (VAST-AI) | MIT, but the full checkpoints were still "coming soon" | Low priority; only for walking the mascot later. |
| dream-loop (`achimala/dream-loop`) | MIT, critic subagent scores each screenshot on a gated 0-10 ladder and the build is redone until it passes | Idea adopted: our own version in `critic-loop.md` (not installed as is). |

## Installed on 16/11/2026 (Jacopo: "installala")
- **Blender MCP** (`mcp-for-blender`, MIT): registered in Claude Code at USER scope (`claude mcp add blender -s user`, telemetry off, uv cache on `D:/uv-cache`); addon `blender_mcp` installed and enabled in Blender 5.1 (auto-starts the server on localhost:9876 when Blender opens). Tested: a socket command returned the scene. The MCP tools appear in a NEW Claude session. Security notes: it can run arbitrary Python inside Blender and the socket has no authentication, so keep it on localhost only and never expose the port; save the .blend before big scripts. Optional paid integrations in the addon (Meshy, Tripo, WorldLabs, "Premium") stay unused. Run only one MCP client at a time.
- **dream-loop**: NOT installed as is (needs an image generator; its helper uses fal.ai). Its method is adapted in `critic-loop.md` (MIT credit kept).
- **kevinbadi/blender-skills**: NOT installed (no licence stated; its 3D-generation skills send photos to Meshy, paid). We write our own camera recipes (turntable, push-in, crane) in the Blender notes.

## Hybrid decision
Keep the three.js world, camera and sound (deterministic, cheap, fast to iterate). Use **Blender headless only for hero garments** (cloth simulation, seams, real folds), export `.glb`, load it in the world. Measure the render and export cost on the GTX 1060 before committing.

## Phases and status
1. Research of tools: DONE 16/11.
2. Skill split (docs, SOPs, kit, taste, ENGINE): DONE 16/11. Engine moved to `fashion-3d/engine`; 6 frames of Short #2 pixel-identical before/after.
3. Realism upgrade: DONE 16/11, all opt-in (old Shorts unchanged; Short #2 re-checked: 4 frames identical, 1 at 109 dB).
   - `room(env=..., grade=...)` / `photo()`: studio reflections (IBL) + one linear grade (bloom, fringe, vignette, ACES, grain). **A/B on Short #2 (real frames): env 0.55 made the image washed-out (blacks lifted); tuned to env 0.22, ambient x0.75, vignette 0.42, bloom 0.28, grain 0.03 = a modest photographic polish, NOT a jump in realism.** Honest conclusion: realism comes from hero geometry and materials, not from post.
   - `w.glb(...)`: loads `.glb` (GLTFLoader, three r170 add-ons vendored). Verified with a Blender-exported bevelled cube.
   - `solid("rbox", radius=...)`: bevelled boxes.
   - Not done: soft-shadow accumulation and sky-fill AO (the engine draws one render per frame; it would need the sub-frame loop for every frame), window view.
4. Blender garment test: DONE 16/11/2026 (first pass, ~1 h of work). Files in `videos/_bench/fashion3d/blender/` (`trouser_test.blend`, `trouser.glb`, `still_eevee.png`, `still_cycles.png`, `confronto.jpg`), lab `videos/_bench/fashion3d/lab_cmp.py`.
   - Method: engine profile (same CX/RX/RZ tables) lofted as 2 legs + seat, voxel remesh 7 mm (33k verts), cloth sim pinned at the waist (drill-like: tension/compression 40, bending 12, 40 frames), mixed 60% with the rest shape (pure sim = legs collapse like a skirt), crease displaced by hand, details as separate meshes placed by ray-cast (waistband, 9 loops, button, J-fly, slanted open pockets + bar-tacks, back welts + buttons, turn-ups), solidify 1.8 mm, procedural twill bump.
   - **Numbers (GTX 1060, 1080x1920):** cloth bake 73-75 s (40 frames); Eevee 64 samples **3.3 s**; Cycles 128 samples + OptiX denoise **27 s warm** (33 s cold); glb export 0.9 s, **3.4 MB**; engine snapshot with the glb 17 s (first run hung 6 min, second fine).
   - **Honest result:** the Blender trouser does NOT beat the engine's `trouserHi` yet. In the engine the glb looks plastic and washed out (procedural twill does not export to glTF; the crotch from the remesh shows an artefact). Cycles gives soft light and a natural drape but a plain surface. The engine version reads better: visible twill, side adjusters, crease, saturated colour (it has many hours of tuning).
   - Rule check: a Cycles hero still is under 30 s, so Blender CAN render hero shots, but 3 s at 60 fps = 180 frames x 27 s ≈ 81 min per shot.
   - What would make Blender win: a garment sewn from 2D pattern pieces (real seams and drape), a BAKED twill normal map + roughness texture (exports to glb), a clean crotch. Decision pending with Jacopo.
5. Metaphor-world format (`metaphor-world-sop.md`) + Jacopo's 3D mascot: DONE as v1. `w.mascot` (Jacopino: walks, waves, hops, blinks; primitives, needs Jacopo's corrections), `dotgrid` and `ctaplate` props. Not done: a full metaphor-world Short.
6. Automatic checks: `scripts/review8.py` (8 fps sheets, never-still scan with DEAD/DRIFT levels, seek test). Measured on our Shorts: Short #1 has 13 dead stretches over 0.8 s, Short #2 has 15 (some legit, e.g. the end card). Camera-speed print and z-fighting check: not done.
