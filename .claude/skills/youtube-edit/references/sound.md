# Sound

_Moved out of `SKILL.md` on 22/10/2026, text unchanged. Read this when: touching any sound, music or the audio mix. Rules here are still the rules: a new note rewrites the rule where it lives (see `SKILL.md` > Keeping the skill yours)._

## Sound

**Sound rule (Jacopo, 20/10/2026, after video #2): a small sound on EVERY text that appears on screen, a pop on every logo, a click on every chapter tag, a swish that starts together with every 3D camera move.** `compose.py` queues these itself (`sub_cues`): a typing sound for text revealed progressively, a soft tap for list and callout items. Two cues closer than 0.28 s: the stronger stays. An explicit `sfx` on a beat still wins; `"sfx": null` silences it. A transition always carries its own sound (a flash is a shutter, a whip is a whoosh, a light leak is a long cinematic whoosh); a graphic that enters (trail, gallery, orbit, build, dive) gets a soft whoosh, an annotate arrow a tick. The overall level is set by the preset (`sound.level` low 0.6 / medium 1.0 / high 1.4 on top of each cue's own volume). Never a cue on plain speech. Whooshes belong to transitions and entering graphics, not to copy: a text line carries its small typing or tap sound, never a sweep. The "typing / click / pop on a real cause" table below holds for UI-like beats.

**Cue system (use this, not hand-written `<audio>`):** `assets/sfx/cues.json` names every sound (whoosh, shutter, hit,
glitch, riser, tick, ping, paper...) with file, max duration, volume and **lead** (seconds before the cut at which the
file starts, so its peak lands ON the cut). `compose.py` reads it: a transition beat plays its default sound; a graphic
plays its format's sound when the preset has `sound.sfx: true`. A beat can force one (`"sfx": "boom"`, or a list, or
`{"name","at","vol"}`) or silence itself (`"sfx": null`). Files are trimmed, faded out and staged in `public/sfx` by
compose (needs ffmpeg). 49 files, all CC0 or Pixabay licence, credits in `assets/sfx/CREDITS.md` (no attribution needed).
To add a sound: drop the file in a subfolder of `assets/sfx`, peak-normalise to -3 dBFS, add a line in `cues.json`, and
the credit in `CREDITS.md` (licence CC0 or equivalent only).
**Licensed sounds (Jacopo's own Artlist and Epidemic Sound subscriptions, 23/10/2026):** they live in
`assets/sfx/licensed/` (git-ignored: the repo is public and these files must never be redistributed), with their own
`cues.json` (same shape; `file` relative to `assets/sfx`) and `CREDITS.md`. `compose.py` merges that `cues.json` when the
folder exists, so a beat can name them (`"sfx": "al-whoosh-scrapy"`); on a machine without the folder they simply do not
exist, and nothing public may depend on them (tests, presets, the default cue maps). Names: `al-` Artlist, `es-` Epidemic.
Only sounds from those two libraries go there; a shared pack's file of unknown origin stays out.

**Transitions (`formats/fx.py`):** beat `{"type":"transition","id":..,"kind":..,"at":t,"dur":?,"color":?}` with kind
flash | whip | zoomblur | lightleak | burn (glitch, shake and dip were tried and REJECTED by Jacopo: not in the library). **A transition covers a CHANGE OF SCENE, with the peak ON the first frame of the new scene** (face -> effect -> the page/graphic; never face -> effect -> same face, with the real scene change coming later: Jacopo's note 20/10). Use `"scene": "<beat id>"` (+ optional `"offset"`) instead of a hand-typed `at`; compose warns when a transition is not within 0.4 s of a graphic starting or ending. `at` is the instant of the cut (the effect peaks
there; it dresses a cut the edit already makes). `{"type":"overlay","kind":"vignette"|"grain","in","out","opacity"}` for looks that
stay on a stretch. **Rare and only at scene changes** (from one scene or clip to the next), never mid-sentence; the preset sets kinds and density (`transitions.density`, `max_per_minute`).

| Sound | Allowed on | Volume | Never on |
|---|---|---|---|
| Typing | real typing, a prompt window or a search typing in, for exactly the typing time | 0.22 | anything that is not a keyboard |
| Pop | a logo appearing (4a, 21) | 0.34 | a chip or a caption (those carry the text cue) |
| Click | every on-screen cursor click | 0.28 | anything without a cursor |
| Ping / notification | a phone notification, literally | to taste | a number landing, a reveal, an accent |
| Cha-ching | a money count landing | 0.07 | anything louder than a whisper |
| Whoosh / swish | transitions and entering graphics (cue system) | per `cues.json` | copy: a text line carries its small typing or tap cue, never a sweep |
| Riser | a build-up into a reveal or a scene change, **always a METALLIC riser** (Jacopo, 23/10/2026: "when I say riser I mean a metallic riser"); the library has none yet: source a CC0 one before using a riser, never fall back to `riser`/`breathy-riser` | per `cues.json` | copy, logos, every beat: a riser is rare |

**Wiring:** `<audio id="sfx-typing" src="sfx/typing.mp3" data-start="8.22" data-duration="1.50" data-track-index="10"
data-volume="0.22"></audio>` as a direct child of the composition root, never inside a wrapper. Every `<audio>` needs an
`id`, or it is silent in the render while the preview plays fine (`check` reports `media_missing_id`). Overlapping sounds
need separate `data-track-index` values; trim any sound that would run past `data-duration`.

**Sourcing:** the Epidemic Sound connector (`SearchSoundEffects` filtered by duration, `DownloadSoundEffect`; for music
`SearchRecordings`, `DownloadRecording` with stems, `EditRecording` to an exact `targetDurationMs`), checked as attached
first; or the free HyperFrames library (typing, key-press, click, click-soft, pop, ping, notification, chime and more).

**Align the audible peak, not the file start:** trim the silence before the transient (`ffmpeg -af
silenceremove=start_periods=1:start_threshold=-40dB`) so the peak lands within two frames of its cause.

**Normalise before you mix:** library files differ up to 10x in level, so at one shared `data-volume` some vanish.
Peak-normalise each to -3 dBFS (read `max_volume` with `ffmpeg -i in.mp3 -af volumedetect -f null -`, then `-af
"volume=<-3 minus max_volume>dB"`), then use `data-volume` only for the mix. Sustained tones need less than transients.

**Verify the render contains each sound:** decode the render and the untouched footage to 16 kHz mono, gain-match on a
speech window, subtract, and read the RMS of the difference in each sound's window (offset to the file's own peak)
against two control windows (a pop shows ~650 against ~30). Never compare against a previous render: two AAC encodes
differ enough to hide a quiet effect.

**Music (Jacopo: light lo-fi / chill hip-hop type beat, 20/10/2026):** `assets/music/lofi-01..04.mp3` (CC0, -20 LUFS, credits in
`assets/music/CREDITS.md`). `python3 scripts/add-music.py --video master.mp4 --out master-music.mp4 --track lofi-02` lays the bed
under a finished video, looped, faded in/out, **ducked by a sidechain keyed on the voice** (defaults `--db -3`, `--duck-ratio 2.5`,
`--duck-threshold 0.2`; the bed rises in pauses). Video is copied, the voice is untouched; keep the no-music master. Do it after the
render, so a music change never costs a render. To add tracks: CC0 only (Openverse API `audio/?q=...&license=cc0`), loudnorm to -20 LUFS,
credit in CREDITS.md. **Level:** the bed sits about 13-15 dB under the voice (measured on video #2: the first bed, ratio 10, was inaudible
on a phone; -3 dB with ratio 2.5 and the track lofi-02 was "too loud"): the track matters more than the level, so prefer soft, non-busy
beds, and change the level with `mix-audio.py --music-db` (default -7), which costs a minute, not a render. `assemble.py`'s `music` key is
the simplest bed (levelled after the voice reaches -14 LUFS); there is no hand-written ffmpeg recipe any more: use the scripts.

## Sound iteration without a render (`mix-audio.py`)

The sound design is rebuilt from `public/index.html` (every `<audio data-start data-duration data-volume>`) + the voice of the flat cut, so a note
like "lower the effects", "change the music" or "that whoosh is ugly" costs about a minute, not a render:

```bash
python3 "$SK/scripts/mix-audio.py" --index "$W/public/index.html" --voice "$W/public/input-video.mp4" --video "$W/output-4k-raw.mp4"   --out "$W/final.mp4" --sfx-gain -3 --music lofi-02 --music-db -7
```

It mixes voice + cues (x `--sfx-gain`), measures and applies loudnorm to -14 LUFS (voice + effects), lays the music bed (ducked, same rules as
`add-music.py`) and muxes it onto the picture of a render (copied, not re-encoded). So the order for a delivery is: picture render -> `mix-audio.py` ->
`verify-render.py`. To compare tracks, mix 30 s with each and send them to Jacopo as mp3 (he picks a letter).

**Music beds beyond `assets/music`:** CC0 tracks of `kmilo93sd/agent-video-editor` (OpenGameArt: ambient piano, acoustic, lofi lobby/tea), see its
`library/LICENSES.md`. The level rule is under "Music" above.
