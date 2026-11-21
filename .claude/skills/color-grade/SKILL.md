---
name: color-grade
description: Expert color grading of images and videos from reference images or a named movie look. Matches black level, contrast, the color of shadows/mids/highlights, hue-specific palette, skin tones, grain and film texture like a colorist would, without changing anything in the picture. Trigger when the user uploads an image or video plus one or more reference images and asks to "color grade this", "match this look", "make it look like [movie]", "apply this grade", "give it the Matrix look", or asks for a LUT from a reference. Also trigger for /color-grade. Works for jpg/png/webp stills and mp4/mov video. Comes with 20 built-in movie looks.
---

# Color Grade

Grade the user's image or video so it carries the look of their references, the way a professional colorist would. The engine never generates or edits content: the picture stays pixel-identical, only color, tone and film texture change.

## Setup (once per environment)

```bash
python3 -c "import numpy, cv2" 2>/dev/null || pip install -r requirements.txt
```
If pip refuses (externally managed Python), create a venv: `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`, then run the scripts with `.venv/bin/python`. Video also needs `ffmpeg` and `ffprobe`. All scripts live in `scripts/` next to this file, so resolve paths relative to this SKILL.md.

## Workflow

### 1. Intake
Identify:
- **Target:** the image(s) or video to grade.
- **References:** one or more images of the look. Several stills from the same film give the most reliable result.
- **Movie:** look at every reference yourself. Is it a recognizable film still, a poster or DVD cover (title text, actors), or does the filename or the user name a movie?

### 2. Choose the route
| Situation | Route |
|---|---|
| The movie is one of the built-in looks (`python scripts/grade.py --list`) | `--look <slug>` plus the user's references as `--ref`. The look holds a hand-tuned recipe, the refs pull it toward the exact scene the user wants. |
| A known movie that is not built in | Run `scripts/fetch_stills.py "<title>" --year <y> --out <dir> --n 12`. Open the stills and keep only the ones that share the look the user showed you (drop day scenes for a night look, promo art, posters with text). Grade with `--ref` = the user's references + the kept stills. |
| A poster or cover only | Use it, but prefer film stills: fetch some if the movie is known. Poster text and key art skew the colors. |
| No recognizable movie | Grade from the user's references only. |
| User wants to reuse the look later | `scripts/build_look.py "<Name>" <stills...>` saves it as a new look (numbers only, no images). |

### 3. First pass (fast preview)
```bash
python scripts/grade.py TARGET [--look SLUG] [--ref REF ...] --max-side 1200 --out pass1.jpg
python scripts/sheet.py sheet.jpg TARGET pass1.jpg REF1 --labels original pass1 reference
python scripts/compare.py [--look SLUG | --ref REF ...] --images TARGET pass1.jpg
```
Open the sheet and look at it properly. Use the compare numbers as scopes, not as the goal. A grade can match the numbers and still look wrong, so your eye decides.

### 4. Diagnose and refine like a colorist
Judge in this order, and change one or two things per pass. Three passes at most.
1. **Exposure and contrast:** black level, how bright the mids are, highlight roll-off.
2. **Color balance per zone:** what color sits in the shadows, the mids and the highlights.
3. **Color separation:** are the right colors in the right places (teal sky vs orange skin, green kept, blues pulled)?
4. **Skin:** faces must read as human unless the look itself colors them (Apocalypse Now, Blade Runner, Sin City).
5. **Texture:** grain, glow, haze, softness, vignette.

| Problem you see | Fix |
|---|---|
| Too dark or too bright, wrong contrast | `--set tone=0.4..0.9`, or add a `curve` op |
| Blacks too crushed or not lifted enough | `curve` op, e.g. `[[0,10],[50,52],[100,96]]` lifts blacks |
| Wrong cast in shadows or highlights | `split_tone` op, values in Lab a*/b* (a: -green/+red, b: -blue/+yellow) |
| Overall color too weak or too strong | `--set color=0.5..1.0` |
| Colors land in the wrong places, palette off | `--set palette=0.2..0.6` |
| A specific hue is off (greens, sky, reds) | `hue_curves` op (hue in Lab degrees, see table below) |
| Faces too colored | `--set skin=0.7 --set skin_follow=0.3` |
| Faces too dark in a night look | `--set skin_lum=0.4..0.6` |
| Image looks over-processed | `--set strength=0.8` |
| Grain too heavy or too light | `--add-op '{"op":"grain","amount":0.015}'` |
| Original had a strong color cast that leaks through | `--set balance=0.9` |

Add an op with `--add-op '<json>'` (it replaces an op of the same name), and remove one with `--drop-op NAME`. All ops and parameters are documented in [reference/ops.md](reference/ops.md).

Lab hue angles: red ~30, orange/skin ~55-65, yellow ~90-100, green ~130-150, cyan/teal ~190-220, blue ~260-290, purple/magenta ~310-340.

### 5. Deliver
- Render at full resolution: run the same command without `--max-side`.
- Show a before/after sheet with the reference.
- On request, add `--lut name.cube` to export the per-pixel part of the grade as a LUT for CapCut, Premiere, DaVinci or Final Cut. Skin protection, glow and grain are not part of the LUT.
- Tell the user in one or two lines what you matched and anything the look can't do (see limits).
- Each grade is one-off by default and saves nothing. End with a single line offering to keep it: save it as a named look in this skill (`build_look.py`, reusable on any image or video by name, no references needed) and/or export a `.cube` LUT for other editing apps. Only do either if the user says yes.

## Video
```bash
python scripts/video.py CLIP.mp4 [--look SLUG] [--ref ...] --preview 2.0      # graded still first
python scripts/video.py CLIP.mp4 [--look SLUG] [--ref ...]                   # fast: LUT + grain + vignette in ffmpeg
python scripts/video.py CLIP.mp4 [--look SLUG] [--ref ...] --mode full       # full quality, same as the image grade
```
The grade is fitted once on frames sampled across the whole clip, so it never flickers. Always check one or two `--preview` stills, then refine with the same `--set` and `--add-op` flags as for images. Use `fast` for long clips and quick drafts. Use `full` (about 0.2 s per 720p frame) when skin protection, halation, bloom or haze matter. Audio is copied untouched.

## Built-in looks
the-matrix, the-grand-budapest-hotel, sin-city, mad-max-fury-road, blade-runner-2049, amelie, saving-private-ryan, se7en, the-godfather, joker, dune, her, la-la-land, the-wizard-of-oz, the-dark-knight, apocalypse-now, the-revenant, pans-labyrinth, hero, drive. Each look is color statistics measured from several film stills plus a hand-tuned recipe. No movie images are included.

## Limits (tell the user when relevant)
- **Color, not light.** The engine cannot move light or add light sources. Night looks (Drive, The Dark Knight) on a daylight image become a dark, cold "day for night" version, not a real night shot.
- **Very busy references** (posters, collages) give weaker matches than clean film stills.
- **Selective color** (Sin City red) keeps real red objects and never skin. If the image has no strong red, the result is close to pure black and white.
