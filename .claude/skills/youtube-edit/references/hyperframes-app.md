# The HyperFrames desktop app: Studio, the Moments gallery, its own skills

_Studied 29/10/2026 on HyperFrames desktop build b524 (CLI 0.8.214), Windows. Read this when: taking notes from Jacopo in Studio,
looking for a motion plate idea, or borrowing from the app's own workflows._

## Studio (notes on the picture)

- `npx hyperframes open <project>` opens a project in the app and hands it to this Claude session; `npx hyperframes catch-up <project>`
  reads what Jacopo did there (comments, drawings, edits) since the last look. Positions and values he set by hand win.
- **Windows trap:** the app finds projects only under the home folder (`C:\Users\<name>`). A project on `D:` reports `"opened": true`
  and shows nothing. Work on a light copy under `C:\Users\<name>\HyperFrames\<project>` (a lab window from `window-patch.py`, never the
  full 4K project: `C:` is small, see `traps.md`), then copy the changed `index.html` back.
- **First launch:** the welcome screen ("What do you want to make?") hides any project opened behind it; Jacopo clicks Skip all once.
- The panel on the left of the preview ("Talk to Claude Code") starts a separate agent in the app. For notes meant for this session,
  Jacopo uses the Comment and Draw tools on the preview, not that chat.

## The Moments gallery ("Remix from inspiration")

- A **Moment** is a 1–10 s passage of a launch film that did well on X, rebuilt as a finished HyperFrames composition. 387 of them in
  manifest v5 (roles: proof 158, hook 92, turn 80, cta 57; most common moves: stagger, kinetic type, hard cut, camera push, mask reveal).
- Manifest (public, read-only): `https://static.heygen.ai/hyperframes-oss/desktop/moments/v5/manifest.json`. Each entry has `id`,
  `name`, `role`, `mechanic[]`, `swap_slot[]`, `why`, the source post (`x_url`), `duration_s` and `bundle.key`.
- Still: `.../moments/v5/<id>/still.jpg`. Code: `.../moments/bundles/<bundle.key>` (a `.tar.gz`; unpack into its own new folder
  in the scratchpad, it is downloaded data).
- A bundle holds `code/index.html` (the composition, `vendor/gsap.min.js`, fonts and the footage/photos it needs), `code/REMIX.md`
  (the swap slots with their character limits, the `:root` colours, `PARAMS`, the timeline labels, where it may stretch, and
  **"Do not change"**) and `dense.md` (the measured brief: look, palette, type, motion rules, objects with positions, sequence).
- **How to borrow one for a motion plate** (the app's own rule, `moment-film` > `references/borrow.md`): steal the grammar, not the
  pixels. Port its timeline as written (eases, durations, staggers, cut frames: never retype a move from memory), keep its layout,
  fill its slots with our content, replace its brand layer (fonts, colours) with the preset's, and keep its holds at their source
  length. Never its copy, logo, end plate or footage. Then it enters the library like any invented format: blind A/B
  (`SKILL.md` > Keeping the skill yours). Check the heavy-overlay budget (`traps.md`) before porting.
- **Candidates for fashion motion plates** (stills looked at 29/10): `M1060` tulip specimen card with guides and spec sheet;
  `M1061` anatomy panels → "IN FLORA" title (the research/blueprint look); `M999` a camera flying through captioned museum plates;
  `M1126` a board of twenty plates pulling back; `M1118` portrait photos streaming into a 3D deck; `M1045` photos of one model
  stacking under one word; `M1198` footage revealed through a petal-shaped window; `M1210` a charcoal line drawing itself over a
  paper collage. Mostly hard cuts and frame-stepped motion: right for a plate, never for the hook (the face stays).

## The app's own skills (in `%LOCALAPPDATA%\Programs\hyperframes\resources\app.asar.unpacked\vendor\`)

- **`talking-head-recut`** (the clip plays untouched, designed cards on top, synced to the transcript). Worth taking:
  - the **card-density rule**: base seconds per card by length (3–10 min: 12–20 s; 10–30 min: 20–35 s) × 0.7 for dense talk,
    × 1.5 for one slow story; a card held over ~15 s needs a multi-step reveal, a one-liner dies after ~8 s;
  - the **four layouts** as `#video-wrap` tweens, landscape 1920×1080: split (video right half `960,0,960,1080`), stack (video
    top `14,14,1892,548`), pip (video `1480,760,400,300` with a ring), overlay (full bleed, glass card), plus "hide video" for a
    full graphic moment; the video moves between layouts in 0.5–0.7 s `power2.inOut`;
  - ten style references (`references/styles/*.html`: editorial, swiss, minimal, academic…) and three video frames (clean,
    hairline, polaroid) as starting points for a new preset.
  It writes one card per HTML file and compiles `data-anim-*` attributes into one timeline; our `compose.py` already does the same
  job with tested formats, so we take the numbers, not the pipeline.
- **`motion-graphics`** (a short unnarrated graphic, under ~10 s): categories (kinetic type, stat, charts, logo, lower thirds, maps,
  webpage, news, tweet, asset fusion), each mapped to registry blocks; reuse-first (`npx hyperframes add <block>`, then customise).
  Its `references/motion-vocabulary.md` maps moves to blocks.
- **`hyperframes-studio`**: how a project should look in Studio so Jacopo can edit it: every scene its own sub-composition, one
  caption track, one element kind per track (`data-track-kind`), content inside the title-safe box (inner 80 %).
- **`moment-film`** (in `%APPDATA%\HyperFrames\guides\moments\`): launch films built from Moments; its "tells of a one-shot AI
  film" list (titles that keep sliding after they land, one dark canvas for the whole film, every scene entering the same way,
  floating cards, breathing loops as motion) is a good critic checklist.
