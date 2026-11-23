# Twin shot: the hybrid AI clip rebuilt in Blender only (23/11/2026)

Why: `realism-plan.md` phase 7. The hybrid test (`hybrid-blender-ai-sop.md`) looked great but costs ~108k credits per 30 s Short; mixing AI moments into our 3D shows the quality jump. So the SAME 5 s shot (`videos/_bench/ibrido/video/lipsync-v1.mp4`: Jacopino on the cutting table at night, «Io parto da carta, matita e metro, meno di 30») was rebuilt in Blender EEVEE with no generative AI, then compared side by side at 8 fps.

Files: `social/gemello/twin.py` (whole shot, one headless script), `social/gemello/finish.sh` (post + side-by-side + 8 fps sheets). Renders and work files: `videos/_bench/gemello/` (local, outside git).

## Pipeline (one command each)
1. **Mouth cues**: `rhubarb.exe -r phonetic -f json -d dialog.txt --extendedShapes GHX -o cues.json battuta.wav` (1.5 s). Use the PHONETIC recognizer for Italian (the default one is English-only). Exe from the Rhubarb NG add-on: `D:\blender-user\extensions\user_default\rhubarb_lipsync\bin\rhubarb.exe`. Convert mp3 to mono wav first (ffmpeg).
2. **Shot**: `set BLENDER_USER_RESOURCES=D:\blender-user` then `blender -b -P social/gemello/twin.py -- videos/_bench/gemello --dir v1 --samples 64` (writes PNGs). Test flags: `--frames a-b --step n --pct 30 --samples 48 --cam mid|hand|face --mouth decal|keys --vol 0 --nowear --debug --norender`.
3. **Finish**: `bash social/gemello/finish.sh v1` → `v1.mp4` (with the real audio), `v1-vs-ai.mp4`, `review/v1-8fps-0N.jpg`.

## Character
- Use the Tripo rigged figure `social/short-03-tabellone/v8/jaw-raw.glb` (Mixamo skeleton, 21k verts, textures, jaw shape key), NOT `assets/jacopo-ps2-color.glb`: the ps2-color one has no skeleton and its vertex colours look washed out next to the Tripo texture (side-by-side render 23/11).
- In this GLB only the HEAD is turned 15.6° towards +X; the body already faces the camera. Correct it on the Head/Neck bones (`--headyaw -15.6`), never by rotating the whole figure (that turns the torso away).
- Work in the GLB's own ("raw") coordinates and scale a root empty to 22 cm: all measures from `blender_add_jaw.py` (mouth centre 0.0215/-0.0218/0.776) stay valid.

## Face
- **Replacement mouths beat the shape key** (closeup comparison, `work/mouth2.jpg`): the 9 Rhubarb shapes (A-H, X) built as flat decals that follow the face surface (each vertex ray-cast on the head, 0.6-1.5 mm in front), with lip rim, dark interior, teeth and tongue as layers, parented to the Head bone and swapped with `hide_render` keys. They read crisp and "toy" even at full-body size. The `jawOpen` shape key driven by the same cues opens ragged holes in the Tripo mesh.
- Decal geometry: centre + rings (6 rings x 56 points) projected on the face; a flat fan sinks behind a curved face.
- Timing: cue 1 frame early, minimum 2 frames per shape ("on twos", stop-motion feel). Mouths 15% bigger than the sculpted crease.
- **Brows**: don't add brow objects on top of the sculpted ones (you get double brows). Add two bones (browR/browL, children of Head) and weight the SCULPTED brow vertices to them (smooth falloff, never the glasses: z > 0.872 raw). Then raise/tilt them in bone space (move along the bone-local "world up").

## Body (max 2 gestures in 5 s)
- Arms by IK (chain 2 on the forearm, targets/poles as empties in raw coordinates, influence keyed), hands/fingers/head/spine by keyed local rotations, every channel driven by a damped spring over step targets (anticipation and overshoot for free). Check with `--debug --norender`: it prints wrist vs IK target per frame.
- **Silhouette rule**: a hand moving towards the camera is invisible in a frontal shot; a gesture reads only when the hand leaves the body outline. Point with the hand on the SAME side as the object (paper on screen-right → character's left hand); crossing the body reads as a fist on the belly.
- Tripo fingers are fused: curling the "other" fingers also curls the index → a fist. No pointing index: use an open presenting hand.
- Palm up on this rig: right hand local rotation (10, +80, 0) degrees.
- Head looks at the paper during gesture 1, then back to camera with a tilt on the punchline; brows up on «Io», small raise on «metro», big raise + tilt on «meno di trenta».

## Look
- EEVEE (`BLENDER_EEVEE` in 5.x), 64 samples, raytracing, AgX Medium High Contrast, exposure +0.3, f/2.2 on the toy (strong DOF = small-scale cue), motion blur 0.45.
- **Haze**: world Principled Volume, density 0.05 at toy scale. 0.35 makes the whole frame milky. With fewer than ~48 samples the volume (and the bokeh) turns into a mosaic: never judge looks on a 16-sample test.
- City window behind: big brick-texture tiles (scale 5), emission ~0.9; small tiles become a honeycomb of bokeh discs.
- Wear (Lego Movie): noise roughness + stretched-noise scratches + micro bump on every material, subtle (bump 0.05-0.15).
- Post in ffmpeg, not in the Blender compositor (5.x compositor API changed): soft bloom (threshold curve + gblur, screen 0.4), vignette, moving grain.
- Camera: empty rig animated on an eased arc (quintic smoothstep), camera child with Camera Shakify (INVESTIGATION 0.35 + THE_CLOSEUP 0.25, location scale 0.1: real handheld translation is huge at toy scale).

## Numbers (GTX 1060 6 GB, 1080x1920)
- ~7 s per frame at 64 samples with volume → 121 frames ≈ 15 min. A 30 s Short at 24 fps ≈ 85 min.
