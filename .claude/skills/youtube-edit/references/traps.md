# Animation traps and render traps

_Moved out of `SKILL.md` on 22/10/2026, text unchanged. Read this when: writing any entrance, composing by hand, or before ANY render. Rules here are still the rules: a new note rewrites the rule where it lives (see `SKILL.md` > Keeping the skill yours)._

## Animating glass (read before writing any entrance)

**Never fade a glass element through an ancestor's `opacity`:** Chrome drops `backdrop-filter` while any ancestor is
below opacity 1, so the frosted panel is missing for the whole fade and snaps in late. Hold the host at opacity 1 and
animate the look of the glass:

```js
tl.set('#host', { visibility:'visible', opacity:1 }, t);
tl.fromTo(glassSel,
  { backgroundColor:'rgba(255,255,255,0)', borderColor:'rgba(255,255,255,0)',
    boxShadow:'0 24px 80px rgba(0,0,0,0)', x:60 },
  { backgroundColor:'rgba(255,255,255,0.18)', borderColor:'rgba(255,255,255,0.58)',
    boxShadow:'0 24px 80px rgba(0,0,0,0.38)', x:0, duration:.42, ease:'power2.out' }, t);
tl.fromTo(contentSel, { opacity:0 }, { opacity:1, duration:.36 }, t + 0.04);   // text is safe to fade
```

The blur is live from frame one but invisible without tint, so this reads as a fade with panel, border and copy arriving
together; the exit reverses it. Copy sitting directly in the glass element needs an inner span to fade. Plain opacity
fades are fine without backdrop-filter (lower lines). Glass that has not arrived stays hidden, or it blurs the footage.

## Traps that waste a render

**Long renders**
- **Disk capture stores every frame first:** 12 minutes at 4K asked for ~714 GB of scratch. Over ~2 minutes, stream the
  encode with one worker (`PRODUCER_STREAMING_ENCODE_MAX_DURATION_SECONDS=3600`, `--workers 1`; ~35 minutes for 12
  minutes of 4K). Parallel streaming painted the footage BLACK for long stretches; `--low-memory-mode` is not the fix.
- **A long single-session 4K capture can hang** in Chrome's screenshot call. Over ~5 minutes, render segmented with a
  fresh browser per segment and keep `--resume` for a retry: `HF_SEGMENTED_CAPTURE=true HF_SEGMENT_FRAMES=1500
  HF_SEGMENT_BROWSER_RECYCLE=1` plus the streaming settings (8:53 rendered clean in 30 minutes).
- **Black footage under parallel workers:** `--workers 1`, and run `ffmpeg -i out.mp4 -vf
  "scale=192:-2,blackdetect=d=0.4:pix_th=0.08" -an -f null -` on every long render.
- **The frame cache fills the temp folder** (16 GB in a day) at `<tmpdir>/hyperframes-extract-cache-<uid>`: delete it
  when no render runs, or move it with `--frames-cache-dir`. Before an assembly, check free disk (about 2 x minutes x
  0.34 GB). Delete the `work-*` folder a failed run leaves; zsh aborts an `&&` chain on an empty glob (`work-*(N)`).
- **A note on a long render costs a patch, not a re-render:** `window-patch.py --public "$W/public" --t0 T0 --t1 T1 --out
  "$W/patch-a"`, rendered with the same flags, then overlaid on the full render (`overlay` with
  `enable='between(t,T0,T1)'`) or spliced in frame-exact (12 ms audio fades). Start the window before the card's host
  enters; prove alignment with `psnr` on the first and last frames (50 dB or more = the same frame). Anything held
  across a splice must be static on both sides.

**Disk (Windows, small system drive)**
- **`snapshot`, `check` and `render` record a revision of the project in `~/.cache/hyperframes/history/<id>/blobs`**, and every revision copies the media: a full
  4K flat cut cost **2.2 GB per run** and filled a 223 GB `C:` to 0 bytes in one afternoon (tests then fail with "No space left on device"). Always export
  `HYPERFRAMES_HISTORY_ROOT=D:\hf-history` on a PC where it is not set. **On Jacopo's PC it is fixed since 10/11/2026, nothing to export:** three user
  environment variables (set with `setx`, read by every program started afterwards) send it all to `D:`: `HYPERFRAMES_CACHE_DIR=D:\hyperframes-cache`
  (Chrome, Parakeet, fonts, background removal: moved there from `C:\Users\<name>\.cache\hyperframes`), `HYPERFRAMES_HISTORY_ROOT=D:\hf-history` and
  `HYPERFRAMES_EXTRACT_CACHE_DIR=D:\hf-cache` (the extracted frames, the same folder as `--frames-cache-dir`). Check them with `reg query HKCU\Environment`.
  Windows' own `TEMP` stays on `C:` because other programs use it: for a long render still pass `TEMP=TMP=D:\hf-tmp`. Take snapshots on a `window-patch.py` copy or a small
  lab video instead of the full project. **Clean up with the CLI, not by hand** (HyperFrames 0.8.214, 29/10/2026): after each approved checkpoint
  and after every delivery, `npx hyperframes clean "$W" --dry-run` lists what it would remove (history media copies, extracted frames), then
  `npx hyperframes clean "$W"` removes it; add `--snapshots` only once the snapshots are approved. Never while a render runs. The first dry run
  found 1.8 GB of history copies; the revisions are only a rewind feature.

**Encoding and files**
- **`--gpu` ignores CRF** (`--quality high --gpu` gave 14 Mb/s at 4K): always `--video-bitrate 60M` at 60 fps (45M at 30).
- **The render drops two colour tags:** always the BT.709 remux, or faces look redder than the camera original.
- **Skipping `assemble.py`:** the render keeps the camera level (~-25 LUFS). Level the voice to -14 first (a one-segment
  `assembly.json` does it), then add music; measure the file with `ebur128`.
- **The render finishes; the file can still be wrong** (black footage, a missing tag, audio a frame short):
  `verify-render.py` catches these, the pre-render sheet cannot. Its 40 Mb/s floor fails on mostly still screens
  (hardware encoders undershoot); if every other line passes, that is not a quality problem.

**Composition**
- **Every timed element needs `class="clip"`** or it shows for the whole video. Keep `data-has-audio="true"` on the
  footage (`video_missing_muted` is real) or the render is silent.
- **A second `<video>` on `input-video.mp4` does not paint:** cut the span to its own file and give it a `z-index` above
  `.card-host` (10). **One root composition per `public/`:** a backup inside it doubles the audio.
- **Never put CSS translate(), scale() or rotate() in the style of an element GSAP also moves:** GSAP replaces the whole
  value and the lint fails. Start states go in a `tl.fromTo`; lasting centring goes in the separate CSS `translate` property.
- **A count-up is an `onUpdate` on a proxy tweened on the one timeline;** write the start value in at load.
- **Text that changes step by step (typing, a clock) comes from one proxy tween, never a `tl.set` per step,** which
  leaves letters behind on a backward seek: tween `{ n: 0 }` to the length with `ease: 'none'` and write `slice(0,
  floor(n))`. The check for the whole class: seek past a beat, seek back inside it, compare with a fresh seek.
- **Heavy overlays have a budget:** `composition_heavy_overlay_count_high` counts every `filter: blur`,
  `radial-gradient` and `clip-path`, hidden ones included; around 40 and the capture paints black for the first half
  (every full-frame wash counts). Compose long form per section; prefer `box-shadow` glows.
- **The linter is wrong twice:** `text_occluded` behind the subject is the point, and `text_not_painted` fires on
  `background-clip:text`, which renders fine. Two text blocks in one rebuilt logo box trip `content_overlap` (draw the
  small word with `::before`); an SVG with `width="1em"` renders 16 px (give explicit width and height).

**Fonts, transcription, snapshots**
- **The house font look:** the three 7 KB `assets/fonts/DMSans-{400,500,700}.woff2` subsets under the stack `"DM Sans",
  ui-sans-serif, system-ui, sans-serif`, so Chrome draws in the system face (San Francisco on a Mac) at these metrics.
  That is the approved look; the full variable DM Sans reads rounder and wider. Body `font-family` lists concrete names,
  never a CSS variable, and a scene element never sets `"DM Sans"` alone (a whole scene once rendered in Times).
- **Always pass `--engine parakeet`:** with `auto`, a missing Parakeet falls back to whisper without a word.
- **Snapshot filenames:** `snapshot --at 8.0` writes `frame-00-at-8s.png` (no ".0") and wipes the folder each run; copy
  by exact name (`snap-beats.py` does).
- **SVG line that draws slowly:** with `pathLength="1"` and a dash offset from 1 to 0 Chrome pops the line in one go; use `pathLength="1000"` (Video #3, plate p24).
- **Two stacked sheets, the top one moved sideways:** the one below shows in the strip it leaves. Fade the lower sheet out once the upper is opaque (Video #3, reaction panel).
- **4K at 60 fps stops in "Extracting video frames" with `ffmpeg_timeout=1`:** not the `FFMPEG_PROCESS_TIMEOUT_MS` limit. A keyframe probe (`runFfprobe`) has a fixed 30 s deadline and, most likely, starves on the hard disk while 6 extractors write frames. Two runs failed (05/11/2026). With the deadline raised to 10 min (`deadlineAtMs: Date.now() + 6e5` in the hyperframes `chunk-QXGT6KRX.js` in the npx cache, original kept as `.orig-05-11`, Jacopo's ok) extraction passed in 22 min. One pass, so it fits the cause without proving it. An hyperframes update drops the edit: reapply it.
- **`--keyframe-interval 1` is ignored with `--gpu`:** the 4K comes out with a keyframe every 250 frames (Video #3). Don't plan a splice on whole seconds: read the keyframes first with `ffprobe -show_entries packet=pts_time,flags`. Method in `prove-corso.md`.


## PC, Windows and pipeline traps (collected 19/10 - 09/11/2026)

- **`PYTHONUTF8=1` before the skill scripts** (Italian accents break the default Windows codepage); `compose.py` and `snap-beats.py` already read and write UTF-8 and use `shutil.which("npx")`.
- **Long render:** `FFMPEG_PROCESS_TIMEOUT_MS=14400000` (frame extraction passes the 5-minute default), `TEMP/TMP` and `--frames-cache-dir` on `D:`, hardware GPU works on the GTX 1060. Launch renders with the Bash tool's `run_in_background: true`: a `nohup bash -c` started in a new session does not find `npx` (EXIT=127). If the session closes the render dies but the finished segments stay: rerun the same command with `--resume` (13520 of 14843 frames done: 4 min instead of 35).
- **Rendering a window of a long film:** `render --start/--end` on a long film fails with PLAN_TOO_LARGE after 20-45 min and no file; use `window-patch.py` and put the audio back with `mix-audio.py`. `--fps` goes up to 240 and `--end` only with 24/25/30/60. A motion blur is a copy slowed 4x at 240 fps, then frame blending.
- **Parakeet:** deterministic but changes slightly between runs; writes "Claud/Cloud" for Claude (anchors with variants `a|b` in `build-storyboard.py`); transcribes files over 3 min badly (use windows cut on silences). `faster-whisper` on GPU needs `nvidia-cublas-cu12` + `nvidia-cudnn-cu12` from pip (it failed on `cublas64_12.dll`); with `av` 19 pass the audio as a numpy array. OpenCV 5 has no Haar cascades: use YuNet.
- **ffmpeg in a pipe without `-nostdin` (or `stdin=DEVNULL`) hangs.**
- **A long apply-cut on 4K costs about 45 min:** group every correction to the cut into one re-encode.
- **iCloud on Windows:** files look full-size before they are downloaded (copy them locally before analysing them), and copying with `robocopy` also downloads a copy on `C:`, which fills it. After checking the copy on `D:`, free the space with `attrib -P +U <folder>\* /S` (the files stay on iCloud: 31 GB came back). A file that will not download (Nano 0226) is probably an incomplete upload.
- **Crop 4:3 per clip:** switch the crop on the frame number `n` (`if(lt(n,135),480,...)`), not on the time `t`: the render rounds a cut down to the previous frame and one frame of the new clip showed with the old crop (a visible jerk). Measure the real cut frames on the 16:9 render (frame difference) and check that each cut is a single jump.
- **IG delivery (settings from Jacopo's DaVinci export, 29/10/2026):** H.264 High, 25 Mbps in two passes, 25 fps, keyframe every 2 s, BT.709 colour tags written in the file, AAC 320k, `+faststart`, 2880x2160 (IG does the resizing). The NVENC render of mh-video comes out with colour tags "unknown": on IG and iPhone contrast and colours can shift. Always deliver the tagged file.
- **After touching an EDL, check the style in the generated JSON, not only the script** (a comment in `edl.py` once deleted the push-in style).

- **Footage at 25 fps (DJI Pocket, Video #4, 10/11/2026):** `auto-editor --export v1` writes the speech chunks in source frames and no `timebase`, and `paper-cut.py` / `patch-cut.py` assume 30. On a 25 fps source every cut lands 17 % early (edge-audit reported 247 "mid-sound" edges and whole spoken phrases were removed as silence). Add `"timebase": "25/1"` to `speech.v1` before the paper cut, and run `apply-cut.py --fps 25`. A paper cut that fails edge-audit by the hundreds is a wrong time base, not noisy audio.
- **Writing while dictating reads as retakes:** on a clip where Jacopo writes by hand and repeats what he writes, or reads a list from the screen, `paper-cut.py` strikes whole answers as "retake (kept the later take)". Read every struck line of `PAPER-CUT.md` and put the false ones back with `patch-cut.py --add` (Video #4: 10 of 14 removals were false).
- **Every piece starts on the voice, never on the clip's first frame (Jacopo, Video #4, 11/11/2026):** after `tighten-cut`, merges and `edge-audit --fix` the pieces had 0.35-0.6 s of quiet before the first word, and five clips began on frame one, hands still on the camera and the breath before speaking: "sembra che partano tutti mezzo secondo prima". Before `apply-cut`, measure every head and tail on the audio (10 ms RMS: first and last frame above -32 dB) and trim to 0.10 s before the onset and 0.15 s after the decay; on a clip's first piece ask for sustained level (5 of 8 frames above -36 dB) so handling noise is not taken for speech, and on its last piece drop a burst under 0.2 s that follows 0.25 s of quiet (the hand reaching for the button). Never move a clip's first piece back to the clip start to "fix" an edge.
- **A screen recording that cannot be read is rebuilt as real text, not upscaled (Jacopo, 11/11/2026):** OBS at 1280x720 on a wide monitor leaves a chat column about 430 px wide; an AI upscaler invents letters on small text. Read the text off enlarged frames, set it on a card (`build-pages.py` in the Video #4 folder: tall PNG + anchors), and scroll it on the words he reads. Dark chat stays a dark card. Ask for OBS base = output = monitor resolution (1080p at least), the window full screen, browser zoom 125-150 %.
- **`drawtext` crashes ffmpeg on this machine** (fontconfig has no config file): build contact sheets with `tile` only, no burned-in labels.
- **Never rebuild a video a render is reading:** `plates-build.py` hard-links the footage into `public/`; `ffmpeg -y` on the same file truncates it under the running render. Stop the render first, delete `public/input-video.mp4`, rebuild.
- **A long 4K render is made in windows under 120 s, never in one pass (Video #4, 12/11/2026):** HyperFrames 0.9.35 extracts the source video's frames in 120 s blocks, six ffmpeg at once (half the cores, no option). On a 21 min 4K source (8 GB) on this PC the first blocks end well and the render then dies with `VIDEO_EXTRACTION_FAILED; ffmpeg_timeout=1`: five failed attempts in one night; a longer `FFMPEG_PROCESS_TIMEOUT_MS`, a faster ffprobe and a limit on parallel ffmpeg did not help, and `--resume` starts the extraction again. What works: cut the timeline into windows of at most 118 s with `window-patch.py --fps 25` (cut points outside every timed element, 0.6 s clear, snapped to the source frame), render each window on its own through `render-queue.py` (`--workers 1`, about 31 min per 115 s window at 4K 50 fps), check each window's frame count, join them with the concat demuxer and `-c copy`, check the total frame count, then mix the audio on the joined file. A failed window is rendered again alone. Working scripts (kept from Video #4): `references/windowed-4k/` (`make-windows.py`, `run-windows.sh`, `run-4k.sh`, and the `ffmpeg.cs` / `ffprobe.cs` wrappers).
- **Pin the HyperFrames version in a long job (`npx hyperframes@0.9.35`):** plain `npx hyperframes` fetched a new version by itself in the middle of the night.
- **`verify-render.py --res` wants `3840x2160`, not `4k`:** with `4k` it stops with a traceback and writes no `VERIFY.md`.
- **Never run `taskkill ffmpeg` or `du` on `D:/hf-cache` while a render is running:** the first kills the render's own extraction, the second holds the mechanical disk for an hour.
- **iCloud Drive is on C: (6 GB free):** an 8 GB 4K master does not fit there. It stays on D: and Jacopo uploads it from the PC.
