---
name: youtube-edit
description: Edit a YouTube video end to end in Claude Code. Takes a raw camera clip (retakes and all) or a flat cut, cuts it, adds animated overlays, cutaways, stock or AI B-roll, camera moves and the few sounds that earn a place, then renders a tagged 4K MP4 locally with HyperFrames. Use whenever the user drops a video file or an SD-card clip and says "cut this", "edit this", "overlay this", "add animations", "edit this hook", "add B-roll", "render it in 4K", "edit the Tella tutorial", "assemble the video" or "put the segments together", or names a video file to edit. Covers the cut stage (paper cut, hand cut, tighten, sliver and edge checks, dead-air scan), the storyboard composer and its format library, long-form pacing, camera, sound, Tella screen tutorials, assembly into one master, render checks and delivery.
---

# YouTube editor

Turns raw footage or a flat cut into a finished video: the cut, animated overlays, cutaways, camera moves, sound and a
tagged 4K MP4. Everything runs on your own machine through HyperFrames (Chrome + FFmpeg): no per-render cost, and no
footage leaves the computer.

**The house style.** This is a real channel's editing skill, so it has opinions: light glass cards, DM Sans 700, cyan
for key words, amber for money, magenta for punchlines, a camera anchored to the top of the frame, and silence unless
something on screen makes a sound. Those are the defaults, written to you, the creator. `STYLE-GUIDE.md` (in the kit
folder this skill came in) sums up the look: colours, font, cards, motion, camera, sound and cuts. When you change it,
Claude updates the matching rules here and the colour tokens in the `:root` block of `scripts/compose.py`. For the
look, the style guide wins.

**This skill keeps learning.** Every rule below came from a real note on a real video. When you give a note worth
keeping ("the text is too small", "no sound on this part"), say **"save this to the skill"**: Claude writes it into the
right section of this file as one plain rule, and the next edit starts from it. See "Keeping the skill yours".

Commands run from your project folder with `SK=".claude/skills/youtube-edit"` (where this skill is installed) and
`W="videos/<project>"` (one working folder per video).

## Setup check (first use, and after any update)

On first use Claude checks each line, installs what is missing (asking before anything that needs admin rights), then
runs the tests. Check again after updating HyperFrames or moving the skill.

| Needs | Check | Install when missing |
|---|---|---|
| Node.js 22 or newer | `node -v` | nodejs.org, or `brew install node` |
| HyperFrames CLI | `npx hyperframes --version`, then `npx hyperframes doctor` | comes through npx; `doctor` lists anything else it wants |
| FFmpeg and ffprobe | `ffmpeg -version` | `brew install ffmpeg` (Mac), `winget install ffmpeg` (Windows), the package manager (Linux) |
| Python 3 with numpy | `python3 -c "import numpy"` | `python3 -m pip install numpy` |
| auto-editor | `auto-editor --version` | `pip install auto-editor` or `brew install auto-editor` |
| Parakeet, the transcriber `npx hyperframes transcribe --engine parakeet` uses | transcribe a 5 s WAV with `--engine parakeet --json` | `npx hyperframes models install parakeet` |
| Google Chrome | snapshots, page captures and headless screenshots run in it | google.com/chrome |
| GSAP | compose.py prints a note when it falls back to the CDN (the first render then needs internet) | optional local copy: `mkdir -p "$SK/assets/vendor" && curl -sL https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js -o "$SK/assets/vendor/gsap.min.js"` |
| yt-dlp (optional) | `yt-dlp --version` | `brew install yt-dlp` or `pip install yt-dlp` |

Then, from the scripts folder (not from inside `tests/`): `cd "$SK/scripts" && python3 -m unittest tests`. The tests use
synthetic media and must end with `OK` (the media tests skip themselves without ffmpeg). Run them after touching any script.

- **What ships:** the scripts, `formats/`, and the fonts in `assets/fonts/` (DM Sans 400/500/700, SIL Open Font
  License), which compose.py stages into `public/fonts/` itself. **No sounds, images, logos or footage ship.** Keep yours
  in a shared folder that compose.py copies with `--shared DIR` (`DIR/sfx/`, `DIR/img/`, `DIR/img/thumbs/`): sounds from
  your Epidemic Sound account (its connector) or the free HyperFrames library (`npx hyperframes skills update media-use`
  puts 19 effects in the media-use skill's `audio/assets/sfx/`, Pixabay Content License, no attribution needed); logos
  from the brands' own press kits or sites (see `references/assets.md`).
- **Optional connectors:** Tella (screen tutorials) and Epidemic Sound. Without Tella, record the screen with anything.
- numpy scripts: `sync-tracks.py`, `tighten-cut.py`, `sliver.py`, `edge-audit.py`, `dead-air.py`. Node: `stutter-scan.py`
  (it runs `find-cut-candidates.mjs`) and the cut review page (`build-edl-review.mjs`).

## Taste (read before designing a draft)

`references/taste.md` holds the motion numbers (entrance 12 f, opacity 6 f, accelerate exits, cut on motion), the never-ship list
(page chrome, deck layouts, small cards on empty ground, invented proof, long end holds), the judgment rules and the sound palette,
distilled from motionmaxxing (Apache-2.0), motion-video-kit (MIT) and the Herk playbook (ideas only). `references/critic.md` has the
prompts for the independent critic. A preset's README overrides them; Jacopo's own notes always win.

## Presets (editing types)

The skill is a **general engine** (cut, transcribe, formats, camera, transitions, subtitles, sound, render, checks) plus **presets**: one preset
is one *editing type* the creator likes (palette, fonts, which formats to prefer or avoid, how many transitions and which, how loud the sound
is, subtitle mode, and its taste rules). The creator will add editing types over time; nothing in the engine should assume one look.

- A preset lives in `presets/<name>/` as `preset.json` (machine-readable defaults) and `README.md` (the taste rules and the references it came from).
  Use it with `compose.py --preset <name>` or `"preset": "<name>"` in the storyboard. The preset's `style` is merged under the storyboard's
  own `style` key by key (the storyboard wins); `subtitles`, `formats`, `transitions` and `sound` become defaults the later steps read.
- Shipped: **`elegante-portfolio`** (Jacopo's first editing type: warm dark, Inter + Playfair Display Italic, `trail` / `gallery` / `orbit` / `annotate`
  with `follow`; palette still provisional).
- Shipped: **`vacanze-grading`** (Jacopo's second editing type, 23/10/2026: a *grading-only* preset for log clips from his DJI cameras. It has no overlays and
  does not go through `compose.py`; its `grade` key holds every threshold and the LUT per profile for `grade-scan.py` and `grade-apply.py`; method and
  limits in its README).
- **Where a rule goes.** A rule that holds for every look (seek-safe motion, anchors, render traps, loudness) stays in this file. A rule of
  *taste* (no halo ring, serif key words, glow on plain backgrounds, a page rests then the camera pulls back) belongs to the preset README: in
  the "Explainer formats" section of `references/formats.md`, every rule marked "creator" is the `elegante-portfolio` preset's taste, not a law of the engine.
- **Adding a preset:** (1) the creator sends 2 to 4 reference videos of the new look; (2) for each, extract the MP3 and frames, transcribe in
  windows, run `teardown.py`, view the frames at the key moments and note word ↔ graphic; (3) propose palette, fonts, formats (existing or
  new), transitions, sound level and subtitle mode; (4) build a lab of 10 to 20 s windows and collect notes; (5) save `presets/<name>/` with its
  README. New *formats* go into `formats/` (the engine); the preset only chooses and styles them.

## The routes

| Input | Route |
|---|---|
| A flat cut you made (no baked zooms, captions or transitions; 4K preferred) | the Pipeline |
| One raw clip, 1 to 3 min (a hook, a segment intro) | Cut stage → `storyboard.json` → `compose.py` → `snap-beats.py` → render |
| Several raw clips for one video | `ingest.py` (order and join into `source.mp4`) → the same on `source.mp4` |
| A long talking-head section (over 3 min) | Cut stage + `stutter-scan.py` + `CUT-REVIEW.html` at Checkpoint A → storyboard under the long-form doctrine (`references/long-form.md`) → `gap-scan.py` + `beat-check.py` → render per section |
| A screen tutorial recorded in Tella (camera and screen as two tracks) | the Tella route (`references/tella.md`) |
| A tutorial recorded as two files (face + screen) | `sync-tracks.py` → Cut stage on the face file → the screen as full-frame `clip` cutaways; or upload both into Tella |
| A whole video (hook + intros + sections + tutorials) | `assemble.py` → one 4K master, level-matched, with the chapter list |
| A Short (9:16) | not the default routine; see "Shorts" |
| A channel you want to learn from | `teardown.py`; see "The teardown" |

Two checkpoints per video; everything else runs unattended. **A, the cut:** `PAPER-CUT.md` (plus `CUT-REVIEW.html`
when long) and `FACTS.md`, the numbers, dates, prices and tool claims the script says, for you to confirm line by line (ok / wrong: say what is right / cut; a claim nobody can prove is cut, never softened); you answer in plain words ("keep the earlier take of the studio line"). **B, the plan:** `storyboard.json` +
`snaps/sheet.png`, every card moment as a still. Then the render, `verify-render.py` on the file, delivery.

**The hook gate** (every hook, at Checkpoint B):
- The first 3 seconds convince someone to watch to the end. The first frame is a meaningful image, not a settling camera.
- Jacopo's face stays on screen through the hook (Jacopo, 26/10/2026): full-frame graphics (46 hero line, the kinetic phrase
  candidate) start right after the hook, on the first line that follows it, never inside it.
- It works muted: the first overlay says the promise on its own. The first spoken word survives: no sound, card
  entrance or cut lands on it.
- The promise has a payoff time: `"loops": [{"question": "...", "planted": 2.1, "payoff": 412.0}]` in the storyboard,
  checked in the assembled master. One main loop open at a time, one secondary at most; an object that comes back without
  resolving anything is a callback, not a closed loop. Close the promised lesson before any call to action.

## Who plans, who builds (two models)

Planning is where a mistake spreads through the whole video (a wrong beat, a wrong format, a cut that leaves a fact in); building from a
finished plan is execution. So the strongest model plans and a mid-size one builds (the split behind the Claude Code Club's long edit:
Opus planned and directed, Sonnet builders did the sections; Opus plans at high effort, Sonnet builds at medium effort).

- **The planner is the main session** (Jacopo picks Opus in the model selector, high effort, before starting). It decides: what the
  cut keeps (reading `PAPER-CUT.md`, `FACTS.md` and Jacopo's answers), the beatmap and the storyboard (beats, formats, anchors, camera,
  open loops), the hook gate, the preset, what the critic's report means, and every rule a note rewrites. It writes the plan down in
  files (`storyboard.json` + a short `BRIEF.md` per section: what the section says, which formats and why, what must not happen), never
  in its head, because the builder starts with no memory of the conversation.
- **The builder is the `video-builder` subagent** (`.claude/agents/video-builder.md`, model Sonnet, medium effort). One builder per
  section or per task; give it the project folder, the section's `storyboard.json` part, its `BRIEF.md` and the files to read. It runs
  `compose.py`, `beat-check.py`, `snap-beats.py`, `gap-scan.py`, `broll-conform.py`, hand-builds a format from its spec, fixes what
  those checks report, and makes lab windows (`window-patch.py`). It returns a short report: what it built, the files, every check's
  result, and anything it could not do. **It never changes the design.** If the plan is unclear or a check can only pass by changing
  the plan, it stops and asks the planner.
- **Builders can run side by side on different sections** (long form: one per section, up to about four). **Renders never run side by
  side:** every render and every `apply-cut` goes through `scripts/render-queue.py`, one at a time (`--workers 1` on long renders).
  Snapshots run on a `lab/` copy with a light proxy of the video (the disk trap in `references/traps.md`).
- **The planner checks the work, not the builder's word:** it looks at `snaps/sheet.png` and the `check-frames.py` sheets itself, and
  sends the critic prompt (`references/critic.md`) to a fresh agent for the whole draft.
- **When not to split:** a hook of about a minute, or a small fix, is one session; the hand-over costs more than it saves. A new
  format, a break nothing here covers, or a note that contradicts several rules goes back to the strongest model, builders included.
- Cost shape from the guide this came from: about a third of the tokens on the planner, two thirds on builders; the strongest model on
  the building work spends tokens without making the result better.

## Recording so the cut works

- 4K at 30 fps (29.97 is fine), standard colour, flat (no in-camera zooms, captions or transitions), the mic on every
  file, one framing per session, a second of silence at each end. 1080p goes soft past ~112% zoom; 4K holds 200%.
- **Fluff a line? Pause about two seconds and restart the whole sentence from its first word.** The last take wins; redo
  the full sentence when a number, name or price came out wrong. "Cut that" or "scratch that" drops a stretch.
- No spoken slates or notes to yourself (they are speech and get kept); clap or hold fingers up instead. Say lists as
  lists, name tools out loud (logos come from the name), say money in full ("a thousand dollars a month", never "1K"),
  point where a graphic should go, leave the pause after a joke, end a segment on its outro line.
- Two-file tutorials: face and screen recorded at once, both with the mic, one clap, the same file stem.

## Scripts (`scripts/`)

| Script | Does | Options |
|---|---|---|
| `ingest.py` | probe, order and join several raw clips; `ingest.json` maps source time back to (clip, time) | `--raw --out [--concat] [--order A,B] [--only A,B] [--name]` |
| `sync-tracks.py` | audio cross-correlation offset between a face file and a screen file | `--a cam --b screen [--write-aligned DIR] [--window 180]` |
| `paper-cut.py` | what to remove from a raw take: restarts, "cut that", retakes (keeps the last), false starts, long pauses | `--transcript --duration --out-dir --speech`; writes `cut-list.json` + `PAPER-CUT.md` |
| `hand-cut.py` | rebuilds `cut-list.json` from the lines you keep | `--keep A-B` (starts of the first and last kept word; `A-B!` keeps it whole) `--transcript --speech --duration --out-dir` |
| `tighten-cut.py` | trims lead-ins, tails and inner pauses by the sound | `--audio --cut-list --out [--lead 0.07] [--tail 0.11] [--maxgap 0.30]` |
| `sliver.py` | what edge-audit lets through: breath-only segments, heads carrying a dropped word's decay, tails leaking the next onset, edges under 40 ms | `--cut-list --audio [--fix]` |
| `edge-audit.py` | every cut edge checked by the audio: starts or ends mid-sound, restart fragments | `--audio --cut-list --transcript [--keeps FILE] [--fix] [--threshold 300]` |
| `apply-cut.py` | one frame-accurate re-encode into `public/input-video.mp4` + `cut-map.json` (every jump cut); `--lut file.cube` puts the log-to-Rec.709 conversion in the SAME encode, `--encoder nvenc` uses the GPU (4K 6:43 in ~20 min instead of ~45) | `--input --cut-list --out [--fps 30] [--crf 16] [--lut LUT] [--encoder x264\|nvenc]` |
| `dead-air.py` | every pause in the flat cut over 0.40 s after a sentence end (0.45 s elsewhere), by the audio | `W [--plan] [--keep T] [--max 0.45] [--max-sentence 0.40] [--target 0.30]` |
| `patch-cut.py` | small fixes to a cut list | `--cut-list` with `--add A-B`, `--drop T` or `--drop-flat A-B` (flat time, mapped back through `cut-map.json`) |
| `stutter-scan.py` | word-level stutters and a retake pass on the flat-cut transcript, a second opinion | `--transcript --out-dir` |
| `cutlist-to-edl.py` | the cut list as an EDL for the side-by-side review page (`node build-edl-review.mjs`) | `--cut-list --out` |
| `phrase-times.py` | where a phrase is said (start of its first word, end of its last) | `--transcript "phrase" ... [--after T]` |
| `compose.py` | `storyboard.json` → `public/index.html` | `--spec --out [--shared DIR] [--preset NAME]` |
| `beat-check.py` | each anchored element enters 0.10 s after to 0.60 s before its word; fails unanchored cards and a stale transcript | `--index --transcript [--suggest] [--allow-stale] [--video]` |
| `snap-beats.py` | one snapshot per beat and per state inside a beat, tiled into `snaps/sheet.png` | `--project [--at T ...]` |
| `gap-scan.py` | long-form coverage: stretches with no overlay and no camera move; density per 90 s | `--index [--early 15] [--body 20] [--max 30]` |
| `storyboard-md.py` | the delivery `STORYBOARD.md` from one or more storyboards | `--title --project dir:slug:title --out [--note] [--concern]` |
| `broll-conform.py` | a stock clip, generated clip or still → a cutaway (30 fps, no audio, a keyframe every 15 frames, BT.709) + a 3-frame sheet + the beat to paste | `--in --out [--start] [--dur] [--4k] [--grade] [--push 1.08] [--vf FILTERS]` |
| `window-patch.py` | a render-ready copy covering only [T0, T1], for a fix inside a long render | `--public --t0 --t1 --out` |
| `verify-render.py` | checks the rendered file: black runs, size, BT.709 tags, bitrate, duration, A/V, clipped words | `--render [--index] [--res] [--words --kept] [--out]`; exit 1 on a FAIL |
| `ab-compare.py` | a blind A/B of two renders of the same bench window: shuffled into 1 and 2, side by side and in sequence, the key only in `KEY.md` | `--a --b --out [--labels "current,new"]` |
| `sound-report.py` | the numbers of a mix (Claude cannot listen): voice, effects and music loudness and distance under the voice, every effect against the voice, master LUFS and true peak, WARN outside the house targets | `--stems --index --final --out` (stems from `mix-audio.py --stems DIR`) |
| `fact-list.py` | the sentences of the RAW transcript with a number, year, date, price, percentage or tool name, as `FACTS.md` to confirm at Checkpoint A; it lists, never verifies | `--transcript --out [--tools "A,B"]` |
| `check-frames.py` | the render as a viewer watches it: 10 frames a second in sheets with a gap between tiles, one full-size frame on demand, a word said twice, a card too brief to read | `--video --out [--fps 10] [--start T --end T] [--transcript] [--index]` or `--frame T` |
| `render-queue.py` | runs any heavy command (a render, `apply-cut`) one at a time: a second one waits in line on a lock file; the command's flags pass through untouched | `[--lock F] [--wait-minutes 240] -- <command>` |
| `assemble.py` | `assembly.json` → one 4K master at -14 LUFS + `ASSEMBLY.md` + `chapters.txt` | `--manifest --out [--gpu] [--keep-work]` |
| `tella-pull-source.py` | downloads a Tella raw recording from the signed URL `list_sources` returns | `--url-file --out [--wav] [--audio-only]` |
| `tella-cuts.py` | `cut-list.json` → the `cuts` array for Tella's `update_clip`, lead-in offset applied | `--cut-list --source-duration --clip-max` |
| `tella-timeline.py` | a cut Tella clip's sentences on the playback timeline, with clicks and screen activity | `--clip-dir --cuts-json --key [--tella-words] [--clicks] [--activity]` |
| `screen-activity.py` | how much a screen recording changes over time (`activity.json`) | `--video --out [--fps 2]` |
| `grade-scan.py` | measures a LOG clip (D-Log, D-Log2, D-Log M) before grading: profile from the file's DJI tag (or camera name + the picture), LUT effect, zebra 95 / clip, crushed blacks, skin and median, scopes sheet (waveform parade, vectorscope, histogram), exposure proposal anchored on skin. Writes, never changes | `--video --out [--profile auto\|dlog\|dlog2\|dlogm] [--samples 12]` |
| `grade-apply.py` | LUT + approved exposure. Without `--render` only a before/after preview with scopes; with it the graded 4K 10-bit HEVC (video card by default) read back and checked against the preview's prediction (`CHECK.md`, exit 1 on a FAIL) | `--video --scan report.json --out [--stops N] [--match match.json] [--wb\|--wb-gains R,B] [--look NAME\|--look-cube FILE [--look-mix 0-1]] [--smooth 0-2] [--frames 3] [--render] [--encoder auto\|x265\|nvenc]` |
| `grade-film.py` | the film pipeline (module, no command line): tone in linear light with per-clip highlight stretch and shoulder, split tone with water protected, density, hue shifts; the `finish` ffmpeg graph (halation, grain, vignette, graduated sky) scaled to any width. Used by grade-apply / match / ref / looks for every look with a `film` key | — |
| `grade-match.py` | shot matching for one video: per clip, exposure (skin anchor) and cast moved half-way towards the set, within 0.3 stop / 3 %; `match.json` + before/after sheet | `--clip VIDEO=SCAN [--clip ...] --out DIR [--look NAME]`, then `grade-apply.py --match DIR/match.json` |
| `grade-ref.py` | a film look started from reference frames: split tone, blacks, contrast, saturation measured on what the scene does not colour, moved 60 % of the way; `look.json` + sheet (base / 50 % / 100 %) | `--ref IMG\|VIDEO@SEC [--ref ...] --video --scan report.json --out DIR [--base pellicola-oro] [--save NAME]` |
| `grade-looks.py` | the preset's looks (numbers in `presets/vacanze-grading/preset.json` -> `grade.looks`) applied to ONE frame of a clip as a labelled contact sheet, to choose a look with the eyes. A look is a pure colour function (contrast curve, saturation, tints, hue windows on skin and water), so it can later be baked into a 3D LUT | `--video --scan report.json --out sheet.png [--t SEC] [--looks a,b] [--cube-dir DIR [--mix 0-1]] [--cols 3]` |
| `clip-score.py` | pre-selection of footage (b-roll library, travel reels): Open-Sora v1.2 aesthetic score 1-10 (CLIP ViT-L/14 + LAION MLP; 5.5 fair, 6.5 high) and optical-flow motion per clip, sorted CSV + JSON. Runs on the GPU with `D:/tools/video-ai/Scripts/python.exe`, not the system Python. Motion only on clips without grain (grain reads as motion). A first sort, never the choice: the eyes still decide | `--dir FOLDER --out scores.csv [--frames 5]` |
| `teardown.py` | measures any video; counts a storyboard exactly; compares reports | `--video` / `--storyboard` / `--compare`, `--out [--transcript] [--every 2]` |

`formats/claude_chat.py` is the AI chat window (format 13b). `formats/chain3d.py` is the 3D card chain (format 27b). `formats/dotgrid.py` is the dot grid (format 43). `formats/scaletta.py` is the outline rail (format 44). `formats/chips.py` is the hanging chips with the camera (format 41b). `formats/morph.py` is the living shape (format 45). `formats/herotitle.py` is the hero line on a living gradient (format 46).

## Cut stage (raw clip to flat cut)

```bash
mkdir -p "$W/raw" "$W/public" && cp "<card or folder>/<clip>.MP4" "$W/raw/"     # eject the card only after the copy is confirmed
ffmpeg -y -v error -i "$W/raw/<clip>.MP4" -vn -acodec pcm_s16le -ar 16000 -ac 1 "$W/audio-raw.wav"
npx hyperframes transcribe "$W/audio-raw.wav" -d "$W" --engine parakeet --json && mv "$W/transcript.json" "$W/transcript-raw.json"
auto-editor "$W/raw/<clip>.MP4" --edit audio:-30dB --margin 0.12s,0.35s --export v1 -o "$W/speech.v1"   # speech chunks by the audio
python3 "$SK/scripts/fact-list.py" --transcript "$W/transcript-raw.json" --out "$W/FACTS.md"   # Checkpoint A: what Jacopo must confirm
python3 "$SK/scripts/paper-cut.py" --transcript "$W/transcript-raw.json" --duration <seconds> --out-dir "$W" --speech "$W/speech.v1"
#   read PAPER-CUT.md; fix misreads with hand-cut.py (it rewrites cut-list.json)
python3 "$SK/scripts/tighten-cut.py" --audio "$W/audio-raw.wav" --cut-list "$W/cut-list.json" --out "$W/cut-list.json"
python3 "$SK/scripts/sliver.py" --cut-list "$W/cut-list.json" --audio "$W/audio-raw.wav" --fix
python3 "$SK/scripts/edge-audit.py" --audio "$W/audio-raw.wav" --cut-list "$W/cut-list.json" --transcript "$W/transcript-raw.json" --fix
python3 "$SK/scripts/edge-audit.py" --audio "$W/audio-raw.wav" --cut-list "$W/cut-list.json" --transcript "$W/transcript-raw.json"  # 0 issues
python3 "$SK/scripts/apply-cut.py" --input "$W/raw/<clip>.MP4" --cut-list "$W/cut-list.json" --out "$W/public/input-video.mp4"
ffmpeg -y -v error -i "$W/public/input-video.mp4" -vn -acodec pcm_s16le -ar 16000 -ac 1 "$W/audio.wav"
npx hyperframes transcribe "$W/audio.wav" -d "$W" --engine parakeet --json      # transcript.json, in flat-cut time
python3 "$SK/scripts/dead-air.py" "$W" --plan
#   each proposed range: patch-cut.py --cut-list "$W/cut-list.json" --drop-flat A-B, then edge-audit to 0 issues,
#   apply-cut, re-transcribe, and dead-air again until it prints 0 pauses
```

The order on every clip: paper cut → hand fixes → tighten-cut → sliver → edge-audit to 0 → apply-cut → re-transcribe →
dead-air → patch-cut `--drop-flat` → edge-audit → apply-cut → re-transcribe → dead-air prints 0. `<seconds>` comes from
`ffprobe -v error -show_entries format=duration -of csv=p=0 <clip>`. edge-audit's `--keeps FILE` holds your hand-cut
`--keep A-B` arguments; leave it out after a plain paper cut.

**paper-cut.py** keeps the **last take** of every line, cuts restarts inside a sentence from the audio, drops other takes
of the same beat, honours "cut that / scratch that / let me redo / start over / take two" (the marker and the sentence
before it go), drops short false starts and trims long pauses. A later take that only adds a leading filler ("So, ...")
loses to the clean earlier take.

**Where it misreads (fix with hand-cut.py):** a list read as restarts ("candles, soap, t-shirts"); a spoken slate; a
retake with the wrong number in it; one sentence retaken many times without a pause (Parakeet merges the takes and the
paper cut keeps fragments: `--keep` the last clean take); the same phrase twice with a different ending ("is able to find
the fact, is able to find a screenshot" is a restart: keep the second). hand-cut keeps restarts spoken without a pause, so
after every apply scan the flat transcript for the same 3 to 4 word phrase twice within 7 s and remove the real ones.

**Edges:**
- **Sentence starts come from Parakeet, ends from the audio.** Parakeet stretches a last word into the pause (one read
  8.8 s long), so silences never come from word gaps. It also marks phrase starts up to 0.4 s early after a pause, the
  source of "too much breathing room": tighten-cut took one cut from 3:12 to 3:02 with no word lost.
- **Audit every edge by the audio, every time.** A leaked sliver of a dropped take hides in the transcript but plays as
  "right. [ght] A couple hours ago". Heads move BACKWARD from the first kept word to the quiet gap (searching forward
  clipped words); check the joins of the new file the same way.
- **Dead air:** no pause over 0.40 s after a sentence end, 0.45 s elsewhere; `--plan` brings each to 0.30 s with both new
  edges in room tone, `--keep T` protects a deliberate beat. Run it on every section and every Tella flat cut.
- **A cut in the quiet dip before a sentence's last word deletes that word,** and edge-audit passes it. After every
  apply, compare the last word of each kept segment with the fresh flat transcript; when the next word runs straight on,
  cut through speech at the word boundary and check the join by ear and by transcription.
- **Deliberate air:** a segment of your own room tone (`"room_tone": true`, the quietest 0.5 s of a long pause), never
  digital silence, with its picture hidden under a full-frame cutaway.
- **Raw files over ~3 minutes:** Parakeet can drop whole sentences. Transcribe ~25 s windows cut at auto-editor
  silences, shift each window's word times by its start, merge.

**apply-cut.py** does one frame-accurate re-encode (trim/atrim + concat, 20 ms audio fades at every join, CRF 16, a
keyframe every 30 frames, 30 fps, BT.709) straight into `public/input-video.mp4`, every edge snapped to the source frame
grid (without the snap, the picture drifted 4 frames behind the voice over 24 segments). The output is checked against
`cut-map.json` (duration within a frame, A/V under 0.12 s); a DRIFT line means do not dress that file. `cut-map.json`
lists every jump cut: put cutaways on those cuts and dress at most one or two of the rest.

**Grading log footage (holiday clips): scan, approve, apply.** `grade-scan.py` first, always: it reads the profile from the file's tag
(`com.dji.camera.ColorGammaSxS` on the Pocket 4P: D-Log or D-Log2; the Osmo Nano carries only its model, so D-Log M is "probable" and is confirmed
only if the LUT visibly adds colour). A profile that is not certain is never graded: `grade-apply.py` refuses it. Then look at `scopes-sheet.png` and
the proposal, run `grade-apply.py` without `--render` for the before/after preview, and only on a yes run it with `--render`. Rules learned on real
clips (23/10/2026): exposure is anchored on **skin**, not on the median (a bright beach fooled the median); but "skin" brighter than its band in a frame whose median is fine and whose highlights do not clip is warm paving, sand or flowers, so the median wins (28/10/2026: a Zanzibar arch with no people came out 1.3 stops too dark); the highlight limit looks at the brightest
**colour channel** of the worst frame (sea and sky clip in green or blue while luma is still low); a gain above x2 is refused (ffmpeg limit); white balance is measured only on near-neutral objects (never on the average colour: sea and sky are coloured on purpose) and applied only on request (`--wb`, `--wb-gains R,B`, max 12 %); the exposure is a gain on the graded
signal (code x 2^(stops/2.4)), never on the log signal; lifting a subject that the highlights do not leave room for needs a local mask, which these scripts do not do.
The look (`--look NAME`, chosen with `grade-looks.py`) is the last step: it is baked into a 65-point 3D table and applied after the LUT, exposure and white balance; skin saturation is solved per look so skin stays natural (x1.15-1.25, measured: contrast and saturation alone took it to x1.5), and the skin hue window must stay wide and soft (a narrow one makes blotches and a halo on skin edges). LUTs per profile and every threshold are in `presets/vacanze-grading/preset.json` (`grade`; LUT files in `assets/luts/`, CREDITS.md): never cross D-Log, D-Log2 and D-Log M.

**The professional grade (27/10/2026): film pipeline, shot matching, reference looks.** Built from five inspiration videos Jacopo liked (grain, film feel, "beautiful colours without exaggerating"). A look with a `film` key (default `pellicola-oro`) runs through `grade-film.py` instead of the gain-after-LUT path: exposure and white balance in linear light, contrast in stops around middle grey, a highlight stretch measured once per clip (its brightest highlights to ~95 %, starting one stop above grey so skin does not move), a shoulder that never clips, warm highlights / teal shadows with water and sky protected by the hue mask (warming the highlights without it turns turquoise water green), then a `finish` graph (halation, enlarged grain, vignette, optional graduated sky `sky_grad`). DJI LUT and grade are baked into ONE table (two 4K lookups in a row cost double). For a video with several clips: `grade-match.py` first (balances exposure and cast half-way towards the set, max 0.3 stop / 3 %: full matching dulled the lagoon and greyed a warm wall), then `grade-apply.py --match match.json`. To start a look from frames Jacopo likes: `grade-ref.py` (measures tints only on pixels the scene does not colour; never copy a creator's before/after as a LUT: their log is not ours). What the grade cannot do: golden-hour light, locked white balance, ND filter for motion blur: tell Jacopo, it is half of every look he admires.

**Log footage (DJI Osmo Pocket 4P, D-Log2):** the official LUTs are in `assets/luts/` (`DJI-Pocket4P-DLog2-to-Rec709-size65.cube` is the one to use; D-Log2 is not D-Log: never mix them). Apply it with `apply-cut.py --lut`, only on camera clips, never on stills or B-roll. Phone exports from DJI Mimo stay in D-Log2 too. Run ffmpeg from the project folder with a relative `lut.cube` or let apply-cut escape the path (a Windows `D:` path breaks `lut3d` otherwise).

## Pipeline (flat cut to 4K MP4)

```bash
VIDEO="/path/to/flat-cut.mp4"; mkdir -p "$W/public" "$W/snaps"
# 1. Probe + 16 kHz mono audio, then transcribe locally
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate,color_transfer \
  -show_entries format=duration -of json "$VIDEO" > "$W/metadata.json"
ffmpeg -y -v error -i "$VIDEO" -vn -acodec pcm_s16le -ar 16000 -ac 1 "$W/audio.wav"
npx hyperframes transcribe "$W/audio.wav" -d "$W" --engine parakeet --json
# 2. Re-encode at the SOURCE resolution with dense keyframes, or the render freezes on seek (the Cut stage did this already)
ffmpeg -y -v error -i "$VIDEO" -map 0:v:0 -map 0:a:0 -r 30 -c:v libx264 -crf 16 -preset fast -g 30 -keyint_min 30 \
  -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709 -color_range tv \
  -movflags +faststart -c:a aac -b:a 256k -ar 48000 "$W/public/input-video.mp4"
# 3. Only for text behind you: the subject matte
npx hyperframes remove-background "$W/public/input-video.mp4" -o "$W/public/subject-matte.webm" --quality best
# 4. Storyboard → compose → checks → snapshots (Checkpoint B: read the sheet before rendering)
python3 "$SK/scripts/compose.py" --spec "$W/storyboard.json" --out "$W/public" --shared videos/_shared
npx hyperframes check "$W/public"
python3 "$SK/scripts/beat-check.py" --index "$W/public/index.html" --transcript "$W/transcript.json"
python3 "$SK/scripts/snap-beats.py" --project "$W"
# 5a. DRAFT first, every time: 1080p at draft quality (flags from `hyperframes render --help`; the Video #2 drafts ran this way).
#     check-frames.py + qa-motion.py on the draft, Jacopo's notes, fixes, a new draft. Only an approved draft earns the 4K below.
python3 "$SK/scripts/render-queue.py" -- npx hyperframes render "$W/public" --quality draft --resolution 1080p --gpu --workers 1 -o "$W/draft-1080p.mp4"
# 5b. Render 4K (only after the draft is approved): the 1920x1080 composition renders at 2x. --gpu ignores CRF, so give the bitrate (45M = YouTube's 2160p
#    figure). About a minute per 30 s on a recent Mac; without a hardware encoder, drop --gpu.
PRODUCER_BROWSER_GPU_MODE=hardware NODE_OPTIONS=--max-old-space-size=8192 \
  python3 "$SK/scripts/render-queue.py" -- npx hyperframes render "$W/public" --resolution 4k --video-bitrate 45M --gpu --workers 4 -o "$W/output-4k-raw.mp4"
# 6. Full BT.709 tags (the render leaves them "unknown" and QuickTime shows faces darker and redder). Lossless.
ffmpeg -y -v error -i "$W/output-4k-raw.mp4" -c copy -color_primaries bt709 -color_trc bt709 -colorspace bt709 \
  -color_range tv -movflags +write_colr+faststart "$W/output-4k.mp4"
# 7. Check the FILE (exit 1 = do not deliver), then deliver
python3 "$SK/scripts/verify-render.py" --render "$W/output-4k.mp4" --index "$W/public/index.html"
mkdir -p "$HOME/Movies/YouTube Renders/<project>" && cp "$W/output-4k.mp4" "$HOME/Movies/YouTube Renders/<project>/<project>-4k.mp4"
```

**Snapshot every card moment before rendering** (a snapshot is seconds, a render is minutes) and read the PNGs; never
assume. What the composer does not build goes into `raw_html` / `raw_js`, or a hand-built page on the skeleton below
(copy `$SK/assets/fonts/*.woff2` into `public/fonts/` for a hand build).

## Composition skeleton

```html
<div id="stage" data-composition-id="..." data-start="0" data-duration="D"
     data-fps="30" data-width="1920" data-height="1080">
  <div class="video-wrapper" id="video-wrap">     <!-- push-over moves (format 3b) -->
    <div id="video-zoom">                          <!-- the camera -->
      <video id="bg-video" src="input-video.mp4" playsinline data-has-audio="true"
             data-start="0" data-duration="D" data-track-index="1"></video>
      <div id="behind-layer"> ...text behind you... </div>
      <video id="fg-matte" src="subject-matte.webm" playsinline muted
             data-start="0" data-duration="D" data-track-index="2"></video>
    </div>
  </div>
  <div class="card-host clip" id="host-card-01" data-card-id="card-01" data-anchor="spoken phrase"
       data-start="..." data-duration="..." data-track-index="3"
       style="left:0;top:0;width:1920px;height:1080px;visibility:hidden;opacity:0;">...</div>
</div>
```

Two nested wrappers on purpose: `#video-wrap` carries push-over moves, `#video-zoom` the camera; two moves on one
element conflict and fail QA. What must ride the camera (footage, text behind you, matte) lives inside `#video-zoom`;
front cards stay outside so they never scale.

## The composer (`compose.py`) and `storyboard.json`

The storyboard is the review artifact **and** the source: retiming a card is editing one number and rebuilding.

```json
{"id": "hook", "duration": 38.0, "video": "input-video.mp4", "origin": "52% 0%",
 "tag": {"n": 1, "of": 5, "label": "Thumbnails", "in": 0.2, "out": 5.3, "pos": "tr", "anchor": "-"},
 "beats": [
   {"type": "line", "id": "l1", "text": "You clicked on a thumbnail", "em": [4], "color": "cyan", "in": 8.5, "out": 11.6, "anchor": "clicked on a thumbnail"},
   {"type": "logo", "id": "yt", "src": "img/youtube.svg", "in": 11.85, "out": 14.9, "pop": 11.92, "pos": "tl", "anchor": "YouTube"},
   {"type": "list", "id": "ls", "pos": "tr", "in": 15.6, "out": 20.4, "anchor": "candles",
    "items": [["Candles", 15.9], ["Soap", 17.12, "a bar of soap"], ["T-shirts", 18.3]]}],
 "camera": [["creep", 0.3, 5.4, 1.10], ["set", 9.698, 1.0], ["punch", 18.3, 1.18], ["release", 21.0, 0.5]],
 "loops": [{"question": "Why that thumbnail?", "planted": 2.1, "payoff": 31.0}], "raw_html": "", "raw_js": ""}
```

| Key | What it is |
|---|---|
| `id`, `duration`, `video` | composition id, length in seconds (the flat cut), the footage file in `public/` |
| `origin` | the camera anchor, always on the top edge: `"52% 0%"` centred, `"38% 0%"` when you sit left |
| `tag` / `tags` | the chapter or progress tag; `tags` is a list (long form: it returns at every section) |
| `glass_bg`, `glass_bg_cut` | the tint glass lands on (light `rgba(255,255,255,0.18)` by default; a bright room takes `"rgba(17,17,17,0.55)"`), and the tint inside full-frame scenes on the wash (defaults to `glass_bg`; keep it light) |
| `loops`, `raw_html`, `raw_js` | the hook's open loops (checked at Checkpoint B, ignored by the composer); hand-authored formats |

Every beat has `type`, `id`, `in`, `out` and an `anchor` (the spoken phrase; `"-"` marks a deliberate unanchored beat,
written as `data-unanchored`). List and bullet items carry their own time and anchor (`["Soap", 7.12, "a bar of soap"]`;
the text by default, `"-"` = not spoken), so beat-check proves every item. Full-frame beats take `"transition":
"zoomthrough"` (the footage pushes in and blurs 0.22 s before the cut) or `"punch"` (a 2-frame pop on return), and an
optional `label` (the 88 px scene caption).

| Camera op | Does |
|---|---|
| `["set", t, scale]` | jumps to a scale; `["set", t, 1.0]` at every jump cut in `cut-map.json` (never carry a zoom across a cut) |
| `["creep", t0, t1, scale]` | slow push across a thought, `power1.inOut` |
| `["punch", t, scale]` | punch-in, 0.32 s `power2.out` |
| `["release", t, dur]` / `["reveal", t]` | back to 1.0 / a zoom-out reveal, 1.10 to 1.00 as a card enters |

- Positions: `tl` = left 70, top 96 (clears a desk mic); `tr` = right 70, top 96. A lower line holds ~33 characters at
  100 px (split longer ones); list items over ~18 characters need `"width"` and `"size"` on the beat.
- The composer's two sounds are `sfx/pop.mp3` (the logo pop, 0.34) and `sfx/typing.mp3` (search typing, 0.22), copied
  from your `--shared` folder; logos and images go in its `img/`.
- Each build prints the snapshot moments, the count of every format, and a WARN when the same device runs twice in a row
  (lower lines excepted). Fix it; never ship past it.
- Line icons: doc browser bolt chat money check user code video mail gear chart search shield lock robot globe cloud key
  alert folder eye bank chip.

**The AI chat window (13b) is one shared function:** `formats/claude_chat.py`, `chat_css()` + `chat_scene(p, prompt,
t_in, t_out, type_t0, type_t1, send, think_end, head, items, ..., attachments=[...], att_times=[...])` returning `(html,
js_lines)`: image thumbnails drop into the composer box, the prompt types in as you say it, the message sends, the answer
rows land on your words. Each word is a nowrap span with real spaces between words and the box grows from the bottom, so
any prompt wraps (non-breaking spaces once made a prompt run out of the box). Call it from a build script; never hand-roll it.

## Where the rest lives (read on demand)

| File | Read it when |
|---|---|
| `references/formats.md` | designing a storyboard (the format library, which format when two compete, every format's numbers) or hand-building a format |
| `references/long-form.md` | planning a section over ~3 min; placing explainers in the transcript; reading the footage; camera moves; pacing |
| `references/sound.md` | touching any sound, music or the audio mix (`mix-audio.py`, `add-music.py`) |
| `references/traps.md` | writing any entrance, composing by hand, and before ANY render (seek-safe motion, black footage, GPU and bitrate traps) |
| `references/assets.md` | you need a logo, a screenshot, a sound, stock footage or generated B-roll |
| `references/tella.md` | the input is a Tella screen tutorial or a two-file face + screen recording |
| `references/taste.md`, `references/critic.md` | before designing a draft; before the critic reviews a render |
| `references/NOTES_LOG.md` | after any note from Jacopo that changes a rule |
| `references/format-history.md` | planning a storyboard (which formats the last videos used) and after each delivery (add the video's line) |

Each file is the same text that used to sit in this one, moved so that a routine pass does not have to read ~45,000 tokens of it. A rule
still lives in exactly one place: a new note rewrites it there.

## Assembly (one master)

```bash
python3 "$SK/scripts/assemble.py" --manifest "$W/assembly.json" \
  --out "$HOME/Movies/YouTube Renders/<project>/<project>-full-4k.mp4" --gpu
```

```json
{"project": "my-video", "width": 3840, "height": 2160, "fps": 30, "loudness": -14,
 "music": {"file": "bed.mp3", "db": -26, "fade": 2.0},
 "segments": [{"name": "Hook", "file": "~/Movies/YouTube Renders/my-video/hook-4k.mp4"},
              {"name": "1 · Thumbnails", "file": "intro-01-4k.mp4"},
              {"name": "1 · Tutorial", "file": "tella/01-tutorial-4k.mp4", "trim": [0.0, 71.4], "chapter": false}]}
```

Relative paths resolve against the manifest; `trim` is [start, end] seconds; `"chapter": false` hides a segment from the
chapter list; `music` is optional (silence is the default); `"loudness": null` leaves levels alone. Each segment is
conformed once (CRF 16, or `--gpu` at 45 Mb/s) and loudness-normalised in two passes (camera renders arrive around -25 to
-33 LUFS, Tella exports around -23: without this the joins jump 10 dB), then joined with stream copy and tagged BT.709.
Next to the master: `ASSEMBLY.md` (start times, loudness in, md5) and `chapters.txt` for the description. Changes mean
editing the manifest and running again: **the master is never hand-edited.**

## Verify and deliver

- **`verify-render.py` on every render:** black runs (one-frame flashes included), size, BT.709 tags, at least 40 Mb/s at
  4K, duration = `data-duration` ± 1 frame, A/V under 0.12 s; it writes `VERIFY.md` and `render-sheet.png`. Exit 1 = do
  not deliver. **Clipped words:** transcribe the render's audio and add `--words <that> --kept "$W/transcript.json"`.
- **`qa-motion.py` on every draft** (`--video render.mp4 --out qa/`): frozen stretches over 0.6 s, an end hold over 1.4 s, black
  runs, loudness and true peak, plus a contact sheet. Exit 1 = fix first. Then the **critic loop** (`references/critic.md`): a
  fresh agent reviews the real render before Jacopo sees it, and the taste rules in `references/taste.md` are the bar
  (motion numbers, never-ship list, sound palette). State what was measured and what nobody could check (e.g. the sound by ear).
- **`check-frames.py` on every draft, before `qa-motion.py`'s sheet:** nobody watches a video one frame a second, so look at it
  at 10 (`--video draft.mp4 --out check/ --transcript transcript.json --index public/index.html`; a long video: one section at a
  time with `--start/--end`). Read EVERY sheet in order and hunt six things, by time: an animation that plays twice; a graphic that
  flashes (under 0.5 s) or a pop; text that lands too late to read; a graphic over the face; a word said twice; lips out of sync
  (compare mouth and word at five moments). Say what you saw ("card at 8.2 s covers the chin"), never "looks good". Tiles have a gap
  because tiles that touch make two neighbouring frames look like one glitch: before calling a defect, look at ONE full-size frame
  (`--frame 8.2`). When the checker has never failed on something real, plant a defect (a 2-frame flash, a doubled word) and see it caught.
- **Motion on contiguous frames:** `ffmpeg -i out.mp4 -vf "select='between(n,A,B)',scale=480:270,tile=6x7" -frames:v 1
  strip.png` across every transition window; look for a jump-then-crawl, a dead stop between moves, a one-frame pop.
- **Sound** as in `references/sound.md`, with `sound-report.py` on the mix (its numbers go in the report); **loudness** with `ebur128` (about -14 LUFS, true peak under -1); **lip sync** on a long cut:
  a flat frame matches the source near `src_start + x` within one frame for a few late segments.
- **Deliver** to `~/Movies/YouTube Renders/<project>/<project>-4k.mp4` (md5 it against the render) with `STORYBOARD.md`
  next to it (`storyboard-md.py`: time / beat / what is on screen, what changed, your concerns, every stock clip with
  page, licence and seconds) and, for a cut from raw, `PAPER-CUT.md`. Open it from Finder (or Explorer); never pass the
  MP4 through a chat download, since a hosted round trip can change the file.
- **Report** the folder, what was added and where, and **your own concerns** (a card held too long, a word lost on the
  shirt, a cut hidden under a cutaway). Version numbers keep going (v2, v3...). Notes come back in plain words; nothing
  is ever locked.
- **Retiming an approved design onto a new cut of the same content is the cheapest edit:** copy the reference `public/`,
  re-transcribe, move every `data-start` and timeline time to the new words, snapshot, render.

## The teardown (learning from a channel you admire)

Every two videos, measure two recent videos from a channel you want to learn from against your last two edits. Pull them
for private analysis (`yt-dlp -f "bv*[height<=1080]+ba" -o "videos/_teardown/<slug>.%(ext)s" <url>`, captions with
`--write-auto-subs --skip-download`); if a download is refused, do not force it.

```bash
python3 "$SK/scripts/teardown.py" --video videos/_teardown/<ref>.mp4 --out videos/_teardown/<ref>/ [--transcript words.json]
python3 "$SK/scripts/teardown.py" --storyboard videos/<ours>/storyboard.json --out videos/_teardown/<ours>-sb/
python3 "$SK/scripts/teardown.py" --compare videos/_teardown/*/report.json --out videos/_teardown/COMPARE.md
```

The script measures what pixels can tell (hard cuts against the local median frame change, since a same-framing jump
cut is 4 to 17 times the median; bursts; the quietest 15 s stretches; luma; loudness; words a minute). The contact sheets
are for the rest, counted by eye: overlay moments, entrances, on-screen words, camera moves, face presence, cutaway types,
captions. Never claim to have heard audio from waveform numbers. Turn each gap into one rule here (and in
`STYLE-GUIDE.md` when it is the look). Dense edits usually keep their density inside the card (a new element about every
second), not in the number of cards; keep the read-in-under-2-seconds rule anyway.

## Shorts (9:16)

Not the default routine. If you make one: a separate 1080x1920 composition (never a centre crop of the 16:9), hero type
88 to 110 px, cards full width minus 48 px, the caption chip ~280 px from the bottom, word-exact captions on the kept
words, a specific reason to stay in the first three seconds that the video pays off, one main open loop.

## Keeping the skill yours

- **After every delivery:** your note in plain words → edit the storyboard (one number) or the format (one rule) →
  rebuild → snapshot → render. The skill exists so the next first prompt is just "edit these intros".
- **"Save this to the skill":** write the note as one plain rule in the section it belongs to, with its number when it
  has one. When it changes the look, update `STYLE-GUIDE.md` and the composer's tokens too. When a new rule contradicts
  an old one, replace the old one; never leave both.
- **Every note becomes a REWRITTEN rule, with a log line:** fix the video, then ask "which rule, had it existed, would have
  prevented this?", find it (grep a keyword), rewrite that same rule so it covers the case, and add one line to
  `references/NOTES_LOG.md` (date | the note | the rule rewritten | new wording). Two rules that now say the same thing are
  merged; "earlier rule" and "older note" paragraphs are never left behind (stacked rules drift, bloat and contradict each
  other: the sound and music paragraphs once did). The code is the truth for numbers: before writing a level or a time in
  prose, read what `compose.py` / `cues.json` / the preset actually do.
- **The planner chooses, adapts and invents formats on its own, inside Jacopo's style** (Jacopo, 26/10/2026: "ogni video non
  deve avere sempre le solite 5 grafiche"; Video #2 used 6 formats for 20 graphics, 14 of them `trail` or `line`). Three levels:
  1. **Choose** (no question to Jacopo): pick the format that fits each spoken moment from `references/formats.md`, reading
     "When two formats compete" and the variety rule there, which counts the last videos in `references/format-history.md`.
  2. **Adapt** (no A/B): change an approved format to fit the moment (the content, the count of items, the side, the size,
     the timing, a preset colour, a logo or image instead of an icon, two approved formats joined into one continuous scene).
     The style never changes: preset palette and fonts, eases, sound rules, nothing from "Rejected". Name each adaptation at
     Checkpoint B; if Jacopo likes it, it becomes a variant line in the format's spec.
  3. **Invent** (blind A/B): when no format fits a moment, or a reference shows a device the library lacks, design a new one in
     the preset's style and test it as below; it can run on the video's own window instead of the bench, against the format
     it would replace. Every video brings at least one new or adapted format: the library grows with every video.
- **A new animation or graphic enters the skill only after it wins a blind A/B on the bench** (Jacopo, 22/10/2026).
  1. **State sheet first:** name every state before any code (what is on screen, where, size, colour) and every change
     between two states (what moves, the property, the ease, the time). A format without a state sheet drifts, and the review
     has nothing to point at.
  2. **Build it on the bench, not on a real video:** `videos/_bench/` holds fixed 1080p windows with their own
     `transcript.json` (`strumenti` 10 s: tools named; `lista` 12 s: a four-item list; `processo` 16 s: a chain of steps). Pick
     the window that fits the new graphic; always the same windows, so tests stay comparable. Missing bench (a new PC): cut
     them again from `videos/02-claude-collezione/public/input-video.mp4` at 41.45-51.45, 101.95-113.65 and 187.55-204.0 s, shifting
     the transcript.
  3. **Two versions of the same moment:** B = the new graphic; A = what the skill does today at that moment (the current best
     format). Same window, same timing, same sound level: only the graphic differs. Snapshot each state, fix round by round,
     run the seek-back check (`references/traps.md`), render both at 1080p draft.
  4. **Blind:** `scripts/ab-compare.py --a A.mp4 --b B.mp4 --out videos/_bench/ab/<name>/ --labels "current,new"` shuffles them into
     1 and 2; show `side-by-side.mp4` and `in-sequence.mp4` without saying which is new. Jacopo picks and says why.
  5. **Only the winner enters:** a row in the library table (`references/formats.md`) plus a spec with its numbers, a test under
     `scripts/tests/`, and a line in `references/NOTES_LOG.md` with the result and Jacopo's reason. A loser is listed under
     "Rejected (do not rebuild)" with the reason, so nobody builds it again. The same A/B settles a model question (the scene
     built by Opus versus by Sonnet from one plan: `--labels "sonnet,opus"`).
- **Model and tokens:** the strongest model plans, a mid-size one builds (see "Who plans, who builds"). Most tokens go to
  snapshots and tool output: one snapshot per moment, scripts over retyping.
- **Where a saved rule goes:** in the file that holds that topic (`SKILL.md` for the pipeline and the cut, `references/` for
  formats, sound, traps, assets, long form, Tella), never copied into two files.
