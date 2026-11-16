# Blender test plan (next session, 16/11/2026)

Goal: decide how much of our 3D comes from Blender. Honest A/B result of the three.js realism upgrade (`realism-plan.md`): environment light + grade are only a modest polish; **the big lever is the hero garment**, so this test is the point.

## Setup already done
- Blender 5.1 at `C:\Program Files\Blender Foundation\Blender 5.1\blender.exe`. GPU: GTX 1060 6 GB. C: is small: put every scratch file on `D:`.
- **Blender MCP** (`mcp-for-blender`, user scope) registered in Claude Code; addon `blender_mcp` enabled, auto-starts the server on localhost:9876 when Blender opens. In a NEW session the tools `mcp__blender__*` should exist; check `/mcp`. If not, fallback: headless `blender -b --python script.py` (example: `videos/_bench/fashion3d/mk_glb.py` exports a bevelled cube to `.glb`; it WORKS).
- The engine loads the result: `w.glb("id", "path.glb", fit=<height in m>, pos=..., double=True)` (see `videos/_bench/fashion3d/lab_glb.py`, verified).
- Security: the MCP runs arbitrary Python inside Blender and has no authentication; localhost only; save the .blend before big scripts.

## Tasks
1. **Open Blender, confirm the MCP answers** (get scene info). Save work in `D:\ClaudeCodeTest\videos\_bench\fashion3d\blender\`.
2. **Model the hero trouser (Drop 1 spec in memory `project_inverso_pantalone_drop1`: cotone drill, vita naturale, side adjusters, double pleats, straight leg with a slight flare, medium rise).** Parts: waistband with loops, fly, welt pockets with bar-tacks, centre-back seam, two legs, crease, hems. Tone-on-tone thread, NO contrast stitching, hung flat front-to-back (Jacopo's notes in `taste-3d.md`).
3. **Fabric:** a cloth simulation (pinned at the waistband/hanger) for real folds; a PBR material with a drill weave normal map and a soft sheen; seam and stitch relief at about 2 px/mm.
4. **Measure:** time of a Blender still (Eevee and Cycles at 1080x1920) on the GTX 1060; export time and size of the `.glb`; load time in `world3d.js`. Report numbers, not impressions.
5. **Import** the trouser in a scene of Short #2 with `w.glb(...)`, render a still with `w.photo()`, compare side by side with the current `trouserHi` hero at the same camera. Show Jacopo the pair.
6. **Decision rule:** if a Blender still of a hero shot is under ~30 s on the GTX 1060, hero shots can be rendered in Blender and composited; otherwise Blender is only the modeller and three.js renders.
7. Note results in `realism-plan.md` (phase 4) and commit.

## After the Blender test (remaining plan)
- Build Jacopino v2 (the first version is primitives; he waves, walks, hops; review his look with Jacopo: face, hair, glasses, boots; the vest is optional and rough).
- A first metaphor-world Short with the new pieces (`metaphor-world-sop.md`).
- The critic loop needs an image API (about 0.05 EUR per image, Jacopo's idea): ask him which service, store the key in a git-ignored `.env`, never in chat or in the repo.
