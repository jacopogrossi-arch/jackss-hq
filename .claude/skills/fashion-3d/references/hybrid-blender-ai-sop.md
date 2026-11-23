# Hybrid shot: Blender layout + generative video (first test 23/11/2026)

Why: our 3D gives full control (placement, props, camera) but stiff acting (sewn mouth, robotic gestures, camera not smooth). Image-to-video models give expressive acting (real mouth, brows, head tilts, natural hands) but drift. The hybrid keeps Blender for the blocking and lets the model act. First test: `social/ibrido-jacopino/` (prompts, layout script, keyframes); heavy files in `videos/_bench/ibrido/`.

Origin: a TikTok "PS2-style" drama (IMVU/Sims-looking avatars in a car). 8 fps teardown: image-to-video, not real 3D — 2-5 s shots with a near-still camera, rich facial acting, soft hands, background extras that change count between shots, smeared bokeh.

## Pipeline (cost of the first test: ~0.10 EUR Gemini + 18,078 ElevenLabs credits)
1. **Character sheets** with Gemini 3 Pro Image (`scripts/gen_target.py`, `GEMINI_IMAGE_MODEL=gemini-3-pro-image-preview`; the `.env` default 2.5 flash is weaker). Prompts written with banana-pro-director Mode 2, with an explicit *stylization override* (the skill defaults to photoreal). Two 6-panel sheets: identity (front, 3/4, back, profile, face, watch detail) and expressions/mouths (neutral, "ah", "oh", grin, skeptical, surprised). Refs: DEFINITIVO front/side/back + one clean v8 render.
2. **Layout in Blender** (`social/ibrido-jacopino/layout.py`, headless `blender -b -P`): the real GLB at toy scale (22 cm), stand-in props in real scale, camera square and centered (Short 16 lesson), two renders = start and end of the move. Fix in the layout, not in the AI: the first pass showed the table edge and left Jacopino too small.
3. **Keyframe beauty pass** with Gemini: layout render as FIRST ref (blocking, "must not move"), sheets after it. Lessons:
   - Restate the sunglasses in the prompt ("his eyes are never visible"): the first pass dropped them.
   - Generate START first, approve it, then generate END with start as the set reference ("same shot a few seconds earlier, nothing added, tape stays on the left"). Generating both from scratch moved props and added objects.
   - Check by putting layout and keyframe side by side; a drifted keyframe goes back.
4. **Video**: ElevenLabs Flows connector (`creative_*` tools; no new account needed — it hosts Seedance 2.5, Kling 3/4, Veo 3.1). Seedance 2.5, start_frame + end_frame, 9:16, 5 s. Prompt written with cinema-worldbuilder-pro (10 blocks, ~430 words; the first draft was 713, too long). Files reach the flow via public GitHub raw URLs (`creative_attach_reference_file` with `url`); the picker widget is no use over Remote Control.
   - **Seedance 2.5 refuses reference images/audio together with start or end frames** (validation error): keep the frames, drop the sheets — identity is already inside the keyframes.
   - Cost: 720p 5 s = 14,003 credits (2.55 $); 1080p = 31,324 (5.70 $). Test at 720p, redo the keeper at 1080p.
   - Always `estimate_only` first and tell Jacopo the credits before launching (Creator plan: 131k credits/month, reset on the 13th).
5. **Lip-sync** with the real voice: `sync-lipsync-v3`, ports `video` (the Seedance node) + `audio` (the real line), `sync_mode: silence` when the audio is shorter than the clip. 4,075 credits (0.74 $), ~2 min. Works on the stylized toy face: mouth shapes vary, the face stays stable.

## Result of test 1
- Kept: identity across 5 s, sunglasses always on, set and props fixed (Blender blocking respected), real mouth and expressions, a natural palm-up gesture to end.
- Missed: one gesture per word (it pointed at the paper but skipped pencil and tape); the push-in barely happened (the end stayed full body). Next time: fewer beats per 5 s (max 2 gestures), and a bigger framing difference between start and end, or a camera move done in the edit (crop/zoom) instead of asking the model.
- Not checked by ear by Claude: the voice sync quality is Jacopo's call.
