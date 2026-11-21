# Parameters and ops reference

## How the engine grades (in order)
1. **balance**: measures the color cast of the near-neutral pixels (grey, white, steel) and removes it, so the look starts from a clean base.
2. **tone**: builds a smooth luma curve that moves the source's black level, mids and highlights toward the reference percentiles.
3. **color**: splits the image into shadows, mids and highlights and moves each zone's color mean and spread to the reference zone (Monge-Kantorovich linear transfer in Lab).
4. **palette**: hue-specific matching with sliced optimal transport (Pitié iterative distribution transfer) on a color sample of the references. This is what puts teal in the sky and orange on skin instead of one tint over everything.
5. **recipe ops** (per pixel): hue curves, split tone, curves, saturation, mono, bleach bypass, Technicolor, day for night, channel mixer.
6. **masks**: skin protection (face detection plus a skin color model learned from that face), sky secondary, and mono selective color with skin excluded.
7. **finish**: haze, bloom, halation, softness, sharpening, vignette, grain.

Steps 1-5 are per pixel and can be exported as a .cube LUT. Steps 6-7 only exist in the full render.

## Parameters (`--set key=value`)
| key | default | meaning |
|---|---|---|
| balance | 0.6 | remove the source's own color cast (0-1) |
| tone | 0.65 | luma curve match strength |
| color | 0.85 | zone color match strength |
| palette | 0.35 | hue-specific match strength |
| palette_L | 0 | let the palette step move brightness too |
| sat | 1.0 | saturation multiplier after matching |
| skin | 0.55 | skin protection amount (0 = off) |
| skin_follow | 0.35 | how much of the look protected skin still takes |
| skin_lum | 0 | keep faces bright in dark looks |
| strength | 1.0 | mix of the whole per-pixel grade |
| match_exposure | 0.5 | guard rail: pull mid brightness back toward the source (0 = off, 1 = keep source brightness) |
| sat_limit | 1.6 | guard rail: max mean saturation as a multiple of the source's (0 = off) |
| chroma_knee | 50 | guard rail: soft roll-off for very saturated colors (0 = off) |
| max_cast | 20 | guard rail: max overall color shift in a*/b* units, stops one-color washes (0 = off) |

Guard rails keep every grade tasteful and consistent across a set of clips. For a deliberately extreme look, turn them off with `--set sat_limit=0 --set max_cast=0 --set match_exposure=0`.

## Ops (`--add-op '<json>'`)
Lab units: L 0-100, a* (-green / +red), b* (-blue / +yellow), roughly -60 to 60 for normal colors.

| op | fields | does |
|---|---|---|
| curve | points [[in,out],...] (L 0-100), amount | luma curve |
| split_tone | shadows/mids/highlights: [a,b], amount | adds a color offset per zone |
| hue_curves | keys: [{hue, width, shift, sat, lum}] | hue vs hue / sat / lum, e.g. `{"hue":140,"width":35,"shift":40}` turns greens toward teal |
| saturation | amount, vibrance | saturation, vibrance favors dull colors |
| mono | keep [lo,hi] hue, min_chroma, keep_sat, contrast, tint [a,b] | black and white, optional kept color (never skin) |
| bleach | amount | bleach bypass: silver contrast, low saturation |
| technicolor | amount | three-strip dye separation, vivid primaries |
| day_for_night | amount, tint [a,b], keep_lights, light_from | darken, cool, desaturate, bright lights survive |
| gamma | exposure (stops), gamma | brightness on luminance only |
| mix | matrix 3x3 | channel mixer |
| sky | ab [a,b], amount, lum | recolor the detected sky |
| haze | color [r,g,b] 0-1, amount | atmospheric lift in the shadows |
| bloom | amount, radius, threshold | soft diffusion glow (Pro-Mist) |
| halation | amount, radius, color, threshold | red-orange film glow around highlights |
| soften / sharpen | amount, radius | lens softness / crispness |
| vignette | amount, size | darkens the edges |
| grain | amount (0.008-0.04), size, chroma | film grain, strongest in the mids |

## Looks file
`looks/looks.json` holds the recipe per look (name, look term, aliases, params, ops).
`looks/stats.json` holds the measured color statistics (luma percentiles, zone means and covariances, a small color sample). Neither one contains images.
