# Color Grade skill for Claude

Upload an image or a video plus a few reference images, and Claude grades it like a colorist. It matches the black level, the contrast, the color in the shadows, mids and highlights, the palette, skin tones, and film texture like grain and halation. Nothing in the picture changes, only the color.

It comes with 20 built-in movie looks: The Matrix, The Grand Budapest Hotel, Sin City, Mad Max: Fury Road, Blade Runner 2049, Amélie, Saving Private Ryan, Se7en, The Godfather, Joker, Dune, Her, La La Land, The Wizard of Oz, The Dark Knight, Apocalypse Now, The Revenant, Pan's Labyrinth, Hero and Drive.

## Install
- **Claude Code:** put the `color-grade` folder in `~/.claude/skills/` (or `.claude/skills/` in your project).
- **Claude app (claude.ai):** Settings > Capabilities > Skills > Upload skill, and choose the zip.

The skill needs Python with `numpy` and `opencv-python-headless` (Claude installs them on first use). Video also needs `ffmpeg`.

## Use it
- "Color grade this like the references" plus your image and 1 to 5 reference stills.
- "Give this photo the Blade Runner 2049 look."
- "Grade this mp4 like these stills, full quality."
- "Make a LUT from this reference so I can use it in CapCut."

More stills from the same movie give a better match. If you upload a movie cover or still, Claude recognizes the film and can pull extra stills by itself.

## Good to know
- It changes color, not light. A sunny photo with a night look becomes a dark, cold version of the same photo.
- No movie images are included, only color measurements.

Made by @ai.volve.news
