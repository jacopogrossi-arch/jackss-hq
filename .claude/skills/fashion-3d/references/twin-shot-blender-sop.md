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

## Look (v1 → v2: the biggest gap was NOT the character, it was a milky, low-contrast image)
- EEVEE (`BLENDER_EEVEE` in 5.x), 64 samples, raytracing, **AgX - Punchy, exposure 0**, f/2.2 on the toy (strong DOF = small-scale cue), motion blur 0.45.
- What made v1 grey-green and washed out next to the AI clip: exposure +0.3, world background 0.5, haze 0.05, bloom 0.40, teal rim 6 W and a cool fill. v2: world 0.12, haze 0.025, bloom 0.22 above 75% luminance, teal rim 2.5 W, warm fill 1.5 W, warm key spot 40 W (1.0/0.66/0.38). Deep blacks first, then add light.
- Set dressing as in the AI clip: the cutting mat ENDS just behind the feet so the warm wooden table shows behind (a warm band = depth); paper, pencil and tape measure big in the blurred foreground; bookshelf bulbs at emission 25, not 60.
- **Haze**: world Principled Volume, density 0.025 at toy scale. 0.35 makes the whole frame milky. With fewer than ~48 samples the volume (and the bokeh) turns into a mosaic: never judge looks on a 16-sample test.
- City window behind: big brick-texture tiles (scale 5), emission ~0.9; small tiles become a honeycomb of bokeh discs.
- Wear (Lego Movie): noise roughness + stretched-noise scratches + micro bump on every material, subtle (bump 0.05-0.15).
- Post in ffmpeg, not in the Blender compositor (5.x compositor API changed): soft bloom (threshold curve + gblur, screen 0.4), vignette, moving grain.
- Camera: empty rig animated on an eased arc (quintic smoothstep), camera child with Camera Shakify (INVESTIGATION 0.35 + THE_CLOSEUP 0.25, location scale 0.1: real handheld translation is huge at toy scale).

## Numbers (GTX 1060 6 GB, 1080x1920)
- ~7 s per frame at 64 samples with volume → 121 frames ≈ 15 min. A 30 s Short at 24 fps ≈ 85 min.

## Result (23/11/2026): v2 vs the AI clip, 8 fps sheets `videos/_bench/gemello/review/v2-8fps-0{1,2}.jpg`
Files: `videos/_bench/gemello/v2.mp4` (5 s, 1080x1920, 24 fps, real audio), `v2-vs-ai.mp4` (side by side), `v1*` kept for the before/after.
Close to the AI clip: framing, set, warm night palette, deep blacks, DOF/bokeh, push-in (ours is MORE visible than the AI's), two readable gestures on the right words, a mouth that changes on every syllable, brows above the glasses. Cost: 0 credits, ~15 min of render.
Gaps left, by weight:
1. **Facial acting**: the AI grins, squints, moves cheeks and jaw; our replacement mouths read in closeup but are small at full body and the face around them is rigid. Next: smile/cheek shape keys (sculpted, not the ragged jawOpen), bigger mouths when the camera is wide, a head bob on stressed syllables; try iPhone face capture (ARKit) later.
2. **Hands**: Tripo fingers are fused (no index pointing, no relaxed finger spread); the AI's hand-on-chest + pointing reads more human. Next: re-rig the hands (separate finger weights with `el4-character-rigging` `bind_mesh.py --method proxy`) or a cleaner hand from Tripo.
3. **Material**: our jacket is lighter, smoother olive plastic; the AI's is darker with cloth texture and wear. Next: darken the albedo and add a fabric normal on the jacket only.
4. **Post**: the ffmpeg bloom still lifts a faint veil and the vignette darkens the foreground paper: try bloom 0.12 and a gentler vignette.
## v3 (23/11/2026): face, pointing index, jacket, softer post (no new Tripo model needed)
Jacopo asked whether to remodel on Tripo: NO for these gaps. A new mesh resets all calibration (mouth centre, brow weights, IK rest poses, ~1-2 h) and still has a frozen face; check what the current rig can do first.
- **Smile shape key sculpted by script** (`smile`, flag `--cheek 1.6`): cheek "apples" (centres ±0.050 lateral, z 0.797 raw, radius 2.8 cm) moved forward 3.5 mm + up 3.2 mm; mouth corners / nasolabial (±0.034, z 0.781) up 2 mm, back 0.6 mm; vertices inside the mouth ellipse (±0.034 x ±0.014) never move, so the replacement mouths never sink. Keyed 0.35 baseline → 0.65 on «Io» → 1.0 on «trenta», held. No squint: the eyes are behind dark glasses, it would not show.
- **Grin set**: a second series of the 9 replacement mouths ("Xg"…"Hg", smile curvature 15 instead of 6, 6% wider, closed X/A show upper teeth) swapped in from 3.25 s (`--grint`). Reads clearly as a grin in closeup.
- **Mouth size follows the camera**: the mouth groups are scaled 1.22 → 1.0 along the same eased push-in (`--mwide 1.22-1.0`), so the mouth reads at full body and does not get clownish in the closer end of the shot.
- **Head nods on stressed syllables** (PAR-to, CAR-ta, ma-TI-ta, ME-tro, ME-no, TREN-ta): +4° pitch impulses through a stiff spring (omega 20, zeta 0.45), added on top of the head track (`--nod`).
- **Pointing index works on this rig**: the finger weights are NOT fused (each finger has its own bones/weights). Curl middle/ring/pinky ~70° (+ thumb 25°) and leave the index at ~8°: the index reads as pointing down at the paper at mid and wide framing (`work/t3_point.jpg`). The v2 "fist" came from curling all fingers by the same amount. At 85° the low-poly fingers crumple: stay ≤ 70°.
- **Jacket only, by colour mask** (the Tripo model has one material and one texture): mask = green / max(red, blue) mapped 0.96→1.00, MULTIPLIED by saturation 0.22→0.38 (without the saturation term the grey T-shirt gets blotchy, with a tighter ratio range the jacket becomes camouflage because of JPEG blocks in the texture). On the mask: albedo x0.55, roughness 0.82, cloth bump (two crossed wave bands, scale 900, strength 0.35).
- **Post**: bloom screen 0.12 (was 0.22), vignette PI/7 (was PI/5): `BLOOM=… VIG=… bash finish.sh v3`.
- Blender trap: launch with an ABSOLUTE `D:/...` output path. A relative `videos/_bench/...` was resolved against C:\ and wrote the frames to `C:\videos\...`.

Result v3 (`videos/_bench/gemello/v3.mp4`, `v3-vs-ai.mp4`, sheets `review/v3-8fps-0{1,2}.jpg`, still `work/v2v3.jpg`): the grin and the darker matte jacket read at full body, the index points at the paper, the bloom veil is gone. Render ~15 min, 0 credits. Still behind the AI: the AI face is darker and more contrasted (ours is pale, flatter skin), its mouth opens wider with the jaw, and its hand-on-chest gesture reads more human than our arm-out gestures. Send the phone a re-encoded copy (crf 22, ~1.4 MB): the crf 15 master is ~37 MB, over the 30 MB Remote Control limit.

## v4 (23/11/2026): realistic lip sync (Jacopo: "the mouth still looks fake: timing, how it opens, expression")
- **Rhubarb is wrong on Italian**: even in phonetic mode its cues were off by about 0.1 s and it MISSED the lip closures (p of «parto», m of «metro», «meno»). Lips that never meet on m/b/p are the main reason lip sync reads fake. Fix: an Italian lip score written by hand (`LIPS` in twin.py) against the voice loudness printed every 10 ms (python wave + RMS, one digit per 10 ms: dips = closures of p/t/k/m, peaks = vowels). Map: a=D, e=C, i=B, o=E, u=F, m/b/p=A, f/v=G, l=H, t d n s r k=B. Takes ~15 min for a 4 s line and beats any automatic tool on Italian. Next: automate it with word timestamps (Whisper) + an Italian letter-to-viseme table.
- **Continuous mouth** (`--mouth cont`, default; v3 swap = `--mouth decal`): one decal per layer (lip, interior, upper/lower teeth, tongue) with FIXED topology and one shape key per shape (A-H) plus a grin variant of EVERY shape (Ag…Hg). Weights are springs (omega 34, zeta 0.82) on ONES, so shapes blend like a real mouth (coarticulation) instead of popping.
  - Lip and interior: the 56-point superellipse outline, same point count for every shape.
  - Teeth and tongue: STRIPS (NT=24 columns x 4 rows between a lower and an upper edge), never a fan from the centroid. On curved bands the fan from the centroid filled the whole mouth white. A shape without teeth = a strip of zero height along the lip, so teeth grow out of the lip instead of popping in.
  - Grin: never add one "grin delta" computed from X on top of other shapes (teeth came out of the lips as fangs). Blend each shape with its own grin version: weight w*(1-g) on K and w*g on Kg, rest of the mouth (1-sum) on Xg.
  - Crooked smile: rotate the whole mouth group a few degrees around the face's forward axis (`--smirk 5`), not a tilt delta.
  - `slider_max` 1.4 on every key: louder syllables push the open shapes past 1 (opening = 0.62 + 0.75 x loudness, clamped 0.6-1.25).
- **Closures**: a separate very stiff spring (omega 70) for A (m/b/p), applied ON TOP of the vowel shape (during the closure the mouth keeps the nearby vowel's shape and the lips press shut). Never blend the closure through the soft vowel spring: it smears and the lips never meet.
- **Lead**: the mouth anticipates the sound by 0.06 s (~1.5 frames, `--lead`).
- **Jaw**: a new "jaw" bone (child of Head, pivot 5.5 cm behind and 2 cm above the mouth) moves only the chin skin below the widest open decal (z < 0.749 raw), up to 3° with the opening (`--jawdeg`).
- **Face**: brows pop (+2.5 mm) on every stressed syllable, head nods +4°, smile and crooked smile ramp up on «meno di trenta».
- **Review**: the 8 fps sheets cannot show a 1-2 frame sync error. Judge lip sync on a 24 fps face-cam clip with the audio, a `showwaves` strip under it and a half-speed copy (`videos/_bench/gemello/prova-bocca-v4.mp4`), and send it to the phone before the full render.

## v5 (23/11/2026): skin, shirt, wider mouth (Jacopo after v4: "already better, perfect everything you can")
Face-to-face still against the AI (`work/skin_cmp.jpg`): the AI skin is warm tan with modelled shadows, the shirt is matte black, and its grin fills almost the whole width between the cheeks.
- **Skin** (`skin_shirt()` in twin.py, Tripo texture masked by colour): mask = orange hue (0.03-0.10) x value of the texture 0.30→0.42 (the hair is darker) x saturation 0.12→0.20. It catches face, neck and hands, not hair. On the mask: albedo x (0.90, 0.75, 0.64) and subsurface 0.35 (radius 1/0.35/0.2, scale 0.004). (0.92, 0.70, 0.55) was too orange. Check any mask with `--skinmask` / `--shirtmask`: they plug the mask into Base Color.
- **Shirt**: the texture is ALREADY near-black; it looked grey because of the vinyl specular. So don't darken it: make it matte. Mask = value < 0.025-0.05 x saturation < 0.18-0.30 (shirt and shoes), minus everything above z 0.70 raw (otherwise the sunglass lenses go matte too). On the mask: roughness 0.95, specular 0.10.
- **Mouth width** `--mscale 1.35` (was 1.15). The smile shape key's protected ellipse and its mouth-corner region move out with it (+0.025 per +1.0 of scale).

Possible next step to test on a real Short: Blender 5.2.4 LTS is out as a portable zip (install on D:, keep 5.1 as fallback); the EL4CTEO skills need it.
