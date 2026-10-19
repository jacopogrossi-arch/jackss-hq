# Critic prompts (fresh agent, never the builder)

Fill the `<>` slots, send to a **fresh** agent. Keep your own reasoning out. Give it the actual file and let it extract frames itself.

## Full-draft critic

```
You are an independent, blunt video critic. You did NOT make this edit; judge rendered pixels and measured audio, not intentions.

Artifact: <path to MP4> (<duration> s, <resolution>, with audio). A YouTube video by Jacopo (young Italian, menswear/fashion + AI). Preset: <preset name>, see <path to presets/<name>/README.md> for the taste rules and <path to references/taste.md>. Jacopo's own words about this video / his notes so far: <paste verbatim>.

Method: with ffmpeg extract a contact sheet every 0.2 s into <scratch dir> plus dense 1/30 s windows around every transition and graphic entrance (<times>). Find frozen stretches (ffmpeg freezedetect) and empty frames. Measure loudness with ebur128 (integrated, true peak). Check whether sounds land on visual events.

Check: dead frames > 0.6 s without a living element; text over text (also mid-crossfade); subtitles covering the mouth or clashing with a lower line; light text on a light scene; a card floating small in empty ground; transitions that are not at a scene change or that land on a settled frame; chrome (corner labels, counters); an end hold over 1.4 s; a first frame that is a half-entered word; sounds too loud, boomy or repeated identically.

Report (under 700 words), also written to <path>:
1. Per segment: time range, what is on screen, ranked problems.
2. The 6-8 changes ranked by impact, each concrete and implementable with timestamps.
3. What you could NOT judge (for example sound quality by ear).
```

## Verification critic

```
You did NOT make this. Artifact: <new render>. Previous report: <path>. Times may have moved by about <x> s.
For every item in the previous report give FIXED / PARTLY / STILL PRESENT with timestamps, then list NEW defects (glitch frames, overlaps, clipped text, awkward transitional frames).
Write the report (under 500 words) to <path>, ending with SHIP or ONE MORE PASS (at most 3 fixes).
```

## Ledger (one table per video, in the project folder)

| Round | Artifact | Critic's top findings | Change made | Measured result |
|---|---|---|---|---|
