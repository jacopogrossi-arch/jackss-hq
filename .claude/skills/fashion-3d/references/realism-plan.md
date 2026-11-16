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
2. Skill split (docs, SOPs, kit, taste): DONE 16/11. Engine code moves in phase 3.
3. Realism upgrade with before/after tests: TODO.
4. Blender garment test: TODO.
5. Metaphor-world format + Jacopo's 3D mascot: TODO.
6. Automatic checks (8 fps never-still scan, seek test, camera speed, z-fighting 3 frames): TODO.
