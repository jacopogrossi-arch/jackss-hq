# Third-party Blender skills (installed 17/11/2026)

Source: github.com/RobLe3/cc-blender-skill, commit `a2634b5` (v1.4.0), MIT licence (text in `LICENSE-cc-blender-skill.txt`, copyright 2026 RobLe3). Copied unchanged.
Checked before install: no network calls, no shell or system commands in the scripts (7 small Python measuring scripts), the only URLs are documentation links.

## Installed in `.claude/skills/` (9 of the 30)
| Skill | Use for us |
|---|---|
| `blender-materials` | PBR recipes: cloth with Sheen, metals, wood (the hero garment's fabric) |
| `blender-lighting` | studio / HDRI / three-point lighting |
| `blender-cameras` | framing, depth of field, camera moves |
| `blender-rendering` | Eevee vs Cycles settings, render time |
| `blender-export` | `.glb` export for `w.glb()` |
| `blender-modeling` | geometry basics |
| `multiview-fit-loop` | render, compare, adjust, repeat (idea behind our critic loop) |
| `quality-refinement-autoloop` | what to do when a result is below expectation |
| `animation-quality-gate` | contact-sheet review of animations (same idea as our 8 fps review) |
Plus `text-to-blender/references/mcp-backends.md` (not a skill): every installed skill reads it to map Blender tool names. Our MCP is `mcp__blender__*`; its `look` tool plays the role of `render_viewport_to_path`.

## Not installed (21)
The reference-reconstruction, UV/atlas, HUD-motion and mascot-logo skills (not our workflow), and the orchestrator `text-to-blender` itself (it chain-loads everything). Add more later by copying the folder from the repo; check each first.

## Caveats
- Written for Codex first; tested by the author on Blender 5.1.1 (we run 5.1). Their text says "Claude Code behaviour still needs community testing".
- They make the agent run Python inside Blender (same risk as the MCP: localhost only, save the .blend first).
- Our own findings win over a generic skill: Jacopo's notes in `taste-3d.md` and the Drop 1 spec (no contrast stitching, flat hung trouser).

## Added 23/11/2026 (twin shot, phase 7)
Checked before copy: no network calls, no shell/subprocess, no file deletion in any script (grep for subprocess/socket/requests/os.system/exec/eval/rmtree/remove); the only URLs are documentation links.
| Folder in `.claude/skills/` | Source | Use for us |
|---|---|---|
| `blender-animation` | RobLe3/cc-blender-skill `a2634b5` (MIT, licence already in `LICENSE-cc-blender-skill.txt`), copied unchanged | F-curve easing, shape keys, NLA recipes. Its text wrongly calls the 15 visemes "ARKit". |
| `el4-animation` | EL4CTEO/blender-skills `1a1cc6c` (MIT, `LICENSE-el4cteo-blender-skills.txt`) — only `name:` renamed (was `blender-animation`, clashed) | slotted/layered actions, Mixamo retarget (`retarget.py`), bake (`bake_action.py`). |
| `el4-facial-shapekeys` | same, renamed from `blender-facial-shapekeys` | ARKit-52 / viseme shape-key sets, L/R split, drivers (`shapekeys.py`). |
| `el4-character-rigging` | same, renamed from `blender-character-rigging` | skinning with heat + voxel-proxy fallback (`bind_mesh.py`) for AI meshes, rig checks. |
EL4CTEO scripts are written for Blender 5.2 LTS+ (verified by the author on 5.3); we still run 5.1.1: test before relying on them.

## Blender add-ons (23/11/2026), installed OUTSIDE C: (C: is full)
- User resources moved with the env var `BLENDER_USER_RESOURCES=D:\blender-user` (set it before launching Blender, GUI or `-b`). Zips kept in `D:\blender-addons\`.
- Installed with `blender --command extension install-file -r user_default -e D:/blender-addons/<zip>`:
  - **Rhubarb Lip Sync NG 1.8.1** (Windows zip, 70 MB, MIT; ships `rhubarb.exe` at `D:\blender-user\extensions\user_default\rhubarb_lipsync\bin\rhubarb.exe` — we call it directly from scripts).
  - **Camera Shakify 0.5.1** (extensions.blender.org, GPL, shake data CC0).
  - **Wiggle Bones 1.1.2** (extensions.blender.org, GPL).
