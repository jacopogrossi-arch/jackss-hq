# Tella route (screen tutorials)

_Moved out of `SKILL.md` on 22/10/2026, text unchanged. Read this when: the input is a Tella screen tutorial or a two-file face + screen recording. Rules here are still the rules: a new note rewrites the rule where it lives (see `SKILL.md` > Keeping the skill yours)._

## Tella route (screen tutorials)

You record tutorials in the Tella app (camera and screen as two tracks). The cut happens locally, the layouts and zooms
go in through the Tella connector (MCP), and the 4K export joins the rest at assembly.

```
get_timeline(videoId)                    # clips and durations; include layouts / zooms / cuts as needed
list_sources(videoId, clipId)            # the camera+mic signed URL: write it to "$W/tella/cam-url.txt" with a heredoc, never retype it
python3 "$SK/scripts/tella-pull-source.py" --url-file "$W/tella/cam-url.txt" --out "$W/tella/<clip>-camera.mp4" --wav "$W/tella/<clip>-audio-raw.wav"
                                         # the Cut stage on that file; PAPER-CUT.md = Checkpoint A
python3 "$SK/scripts/tella-cuts.py" --cut-list "$W/tella/cut-list.json" --source-duration <ffprobe of the mp4> --clip-max <clip.maxDurationSeconds>
update_clip(cuts=[...])                  # then get_transcript: the first kept word must sit near 0.4 s, or the offset is wrong
get_transcript + get_mouse_events        # words and clicks on the playback timeline → layouts and zooms by the rules below
apply_video_edits(...)                   # one batch: remove stale ranged layouts, add camera-only sections (spring), add manual zooms
get_clip_frame at every boundary, get_storyboard for the video     # Checkpoint B, saved in "$W/tella/snaps/"
export_video(resolution "4k", fps "30") → get_export_status → curl -L -o "$W/tella/<segment>-4k.mp4" "<url>"
```

- ffmpeg cannot open the signed playlist, hence `tella-pull-source.py`; one mistyped character in a signed URL is a 403.
  Tella's clip timeline starts ~2.4 s into the downloadable source; `tella-cuts.py` applies that lead-in.
- Work on the real video only after Checkpoint A; anything exploratory goes on a `duplicate_video` copy. Layouts and
  zooms survive a re-cut (Tella anchors them to the footage).
- `remove_silences` and `remove_fillers` cannot tell a retake from a keeper, so the cut stays local (`remove_fillers`
  after our cut is fine). `generate_auto_layouts` replaces every layout and uses hard cuts: a first draft on an empty
  clip only.
- **Never upload a HyperFrames render into Tella** (it re-encodes at ~15 Mb/s and comes back softer, SSIM 0.88). The
  export is 3840x2160, 30 fps, BT.709, ~9 Mb/s; a 720p camera track becomes an upscale, so record the camera higher.

**Settings** (`update_video`, the house defaults): canvas 1920x1080 with your background image; studio sound, motion
blur and `shrinkCameraDuringZooms` off; a large cursor (size about 3), no smoothing, no click ripple; hard cuts between
clips and `spring` for layout changes; no subtitles, nothing burned in, no music in Tella. Mic volume 1; system audio 0
(or ~0.05) where a video plays on screen while you talk.

**The three views** (every screen clip visits all three):
1. **You left, screen right:** `side-by-side`, position `left`, style `regular`, the base of every screen clip. Never
   `overlap` (your face never sits on the screen you are showing; new recordings often arrive that way) and never
   `side-by-side even` (it crops the screen to half width).
2. **A square or portrait card of you** on the wash (`camera-only`, style `middle`, shapes alternating) for short face
   moments. Long commentary stays `camera-only fullscreen` so the overlays have a full frame.
3. **The screen full frame** (`screen-only`, `fullscreen`, screenFit `cover`) while you draw, type or click and the
   screen is the point.

**The full-face rule.** Enter on the first word of a commentary sentence when nothing happens on screen for the next
~6 s (no click, scroll or typing in `get_mouse_events`), and while you talk to camera about a list until you reach the
item you then show. Return at the first sentence that points at the screen ("this", "right here", a price, a product
name) or the next click. Cap it at 12 to 13 s; one or two per minute; `spring` transitions; clips open and end on the screen.

**Zooms.** Manual, on the thing you name, never on clicks: ~5 s, scale 1.33 to 1.6 (2.0 for small text), starting with
that sentence; one or two per 30 s of screen time, none during full face or while a video plays in the recording. **No
zoom when a page first appears** (show the whole page), no `generate_auto_zooms`, no tracking zooms; a zoom that lands on
neighbouring cards becomes a fixed-origin zoom on the subject. A Tella zoom shrinks your camera into a bubble over the
page, so for a moment where the screen is the point, zoom in HyperFrames on the whole frame with an origin that pushes
your card out: a card whose right edge sits at fraction c of the width leaves once `origin_x * (1 - 1/scale) > c`.

**Cut rules for tutorials:**
- **The screen cut is tighter than the talking-head cut:** after our cut, `remove_silences` mode `fast` on the screen
  clips. It can clip a quiet word, so read the export's transcript, not Tella's.
- Cut forms with personal data (from before the click to after the close, with the sentence that described it),
  restarts and repeats even inside a demo (keep the last), a sentence that re-announces a step the next clip announces,
  and a mumbled line from another take even when its words are fine (check the join by level and a fresh transcription).
- **A browser resize is dead air:** cut it whole; when the page is then narrow, slide the window to the centre of the
  background instead of showing the desktop.
- **A live run shows the result, not the wait:** cut status lines and log read-outs, keep one of a repeated intro line,
  put an "N minutes later" pill on the cut and open on the result already playing (80 s became 37 s).
- Text and images you pasted into an AI chat get shown (13b with the attachments); a product you introduce gets its
  homepage (~3 s, after the name lands); "download the app" gets the real download page, held until you move on.

**The overlay pass on a Tella export.** The 4K export becomes `public/input-video.mp4` (re-encoded, a keyframe every
30 frames) and gets transcribed. Jump cuts are the union of the cuts you sent AND a frame-difference scan of the export
(96x54 grey, a spike over 3.5x the local median): duplicated clips carry cuts of their own, and the scan alone misses
subtle cuts on a still talking head. Overlays live on the full-face windows only (a tag per section, lines, chips, cards,
a logo, a site cutaway); anchors come from `phrase-times.py`; the camera gets `set 1.0` at every jump cut and window
edge, one creep per window, punches 1.6 s clear of any cut. Then the Pipeline.

**Many clips in one pass.** Duplicate the video, export the copy UNCUT once (1080p) and slice its audio per clip by the
timeline's start and duration: raw clip time, so no lead-in offset and no signed URLs. Per clip: windowed Parakeet +
paper-cut, hand cuts, `tighten-cut.py` (`--maxgap 1.2` on demo clips, 0.35 elsewhere), `update_clip` cuts; clamp face
windows to the clip's playback length or `apply_video_edits` rejects the batch.

**When the connector only takes strings** ("must be object (got string)"): ID-only calls still work (`remove_zoom`,
`remove_layout`, `export_video` with "4k" and "30", every `list_*`), and layouts go through `save_layout(videoId, clipId,
layoutId, name)` on a clip that has the one you want, then `apply_saved_layout(videoId, clipId, savedLayoutId)`. Cuts
then happen after the export: remove spans frame-exact (12 ms audio fades) and map every timing through the cut.

**Lip sync.** In one Tella setup the picture ran 3 frames (~100 ms) behind the mic; camera-card footage measured 0.
Measure once per setup on an uncut camera-only export: a box on the lips (80x48 grey, frame differences) cross-correlated
with the rise of the audio envelope over 9 to 15 minutes; the peak is the lag (short files with jump cuts are too noisy).
Fix it where you build the flat cut locally from an uncut export, never by moving the audio: shift the picture once,
then cut as usual, so every picture segment comes N frames after its audio and the audio cuts stay put (moving the
audio clips word tails and pulls slivers of dropped takes into the joins):

```bash
ffmpeg -ss 0.100 -i in.mp4 -i in.mp4 -map 0:v -map 1:a -c:v libx264 -crf 16 -c:a copy -shortest in-synced.mp4
```

**A Tella video you already edited:** work on a `duplicate_video` copy. Screen-only clips get `add_highlight` masks
(intensity 0.55) on the menu you explain, while it is open (no cards over dense UI); camera clips get `camera-only
fullscreen` sections by the full-face rule, where the graphics live. A step tag on white UI is dark glass.

**Two-file tutorials:** `sync-tracks.py --a <face> --b <screen> --write-aligned "$W/aligned"`, the Cut stage on the face
file, the screen as `clip` cutaways. `screen-activity.py` shows where a recording goes still (full-face candidates);
`tella-timeline.py` lines sentences up with clicks and activity.
