# Context for Grok — improving my HyperFrames video-editing workflow

> How to use: paste everything below the line into Grok. It is in English on purpose,
> so Grok searches X/Twitter where most of the HyperFrames / Claude Code community posts.

---

Hi Grok. I'd like you to search X/Twitter (posts, threads, replies, demos from the last few months) and tell me how the community is using **HyperFrames** (HTML → video, rendered with headless Chrome + FFmpeg) together with **Claude Code**, and what I could change in my workflow. Below is exactly what I do today and where it hurts.

## Who I am

- Italian creator (Rome), fashion + AI. Not a developer: I direct, Claude Code writes and runs the code.
- I make long-form YouTube videos (talking head, 8–15 min), travel reels (16:9, beat-synced) and short b-roll pieces with a text hook.
- Machine: Windows 10, small system drive (C:), footage on a second drive (D:). Cameras: DJI Osmo Pocket 3/4 and Nano, shooting D-Log / D-Log M.

## My current pipeline (all local, all driven by Claude Code)

1. **Ingest + cut** — raw clips joined, transcribed (Parakeet via `npx hyperframes transcribe`), "paper cut" in Markdown, auto-editor for silences, my own scripts for stutters/dead air. Checkpoint 1: I approve the cut.
2. **Storyboard** — a `storyboard.json` lists every beat: which graphic format, when, with which words. A Python composer (`compose.py`) turns it into one HyperFrames composition (HTML + GSAP timeline).
3. **Format library** — ~10 custom formats I built (3D chain, chips, fake Claude chat UI, dot grid, hero title, morph, glass cards…), plus "presets" for editing styles (an elegant portfolio look, a grading-only travel look).
4. **Checks** — snapshot contact sheets of every key moment, beat checks, gap scans, an independent "critic" agent reviewing the draft. Checkpoint 2: I approve the plan.
5. **Two models** — Opus plans (storyboard, design decisions), a Sonnet sub-agent builds sections from the written plan.
6. **Render** — 4K, `--workers 1`, streaming encode, segmented capture for anything over ~5 min, then a BT.709 remux and loudness to -14 LUFS.
7. **Colour** — my own FFmpeg scripts: D-Log → Rec.709 LUT, scene scan, grade match between clips, a default "film/gold" look.
8. **Sound** — Epidemic Sound via its MCP connector; very few SFX (I hate pops and cheap whooshes), music under the voice.

## Where it hurts (be specific about these)

1. **Render time and stability** — ~35 min for 12 min of 4K; long single-session captures can hang; parallel workers sometimes painted the footage black. Is anyone rendering long 4K faster/more reliably (cloud render, GPU, chunking tricks, different settings)?
2. **Disk** — the HyperFrames history/revision cache and frame cache filled my C: drive (2 GB+ per snapshot run). Best practices people use?
3. **Heavy overlays** — around 40 `blur` / `radial-gradient` / `clip-path` elements and the capture goes black; `backdrop-filter` (glass) breaks when an ancestor fades. How do people get rich "glass / motion design" looks without hitting these limits?
4. **Creative variety** — my graphics start to look the same from video to video. Where are people finding or sharing good HyperFrames blocks/components, templates, registries, prompt patterns for motion design?
5. **Speed of iteration** — a single note ("move this card, change this word") still costs me a snapshot + patch window. Faster preview/edit loops people use (live preview, timeline editors, partial renders)?
6. **Beat-synced travel reels** — how are people combining HyperFrames with beat detection and real footage (not just typography)?
7. **Claude Code setup** — skills, sub-agents, MCP servers, CLAUDE.md patterns that people share specifically for video editing.

## What I want from you

- **Real examples from X**: link the posts/threads, name the accounts worth following, say what each one does better than my setup.
- For each pain point above: **1–3 concrete changes**, ranked by impact vs. effort, and how sure you are (seen it working in several posts / one post / your own guess).
- Anything in my pipeline that the community would consider **outdated or overcomplicated**: tell me what to drop.
- Tools or repos that pair well with HyperFrames (Remotion comparisons welcome, but I'm staying on HyperFrames unless the case is very strong).
- Keep it practical. If something is just hype with no demo, say so.

Please answer in English with links; I'll bring your answer back to Claude Code to apply it.
