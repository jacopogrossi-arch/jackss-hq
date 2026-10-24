# Sourcing assets, stock and AI B-roll

_Moved out of `SKILL.md` on 22/10/2026, text unchanged. Read this when: you need a logo, a screenshot, a sound, stock footage or generated B-roll. Rules here are still the rules: a new note rewrites the rule where it lives (see `SKILL.md` > Keeping the skill yours)._

## Sourcing assets

**Local editing packs (`assets/packs/`, never pushed).** Real light leaks (25, 1080p60, blend `screen`, warm 1-10 fit the
`elegante-portfolio` look), 12 creative LUTs (Rec.709 + log versions), paper sounds and a camera shutter, paper and dot overlays, from the
free Saturn's Ring / Ali Abdaal packs Jacopo got with a course bonus (24/10/2026). No licence file: Jacopo's own videos only. The catalogue
with every clip's look is `assets/packs/README.md`. They are **candidates**: each enters a format, a transition or the cue list only after it
wins a blind A/B on the bench. A missing folder (a new PC) means the packs were not downloaded there: ask Jacopo, never fetch them again
unasked.

**Find the assets yourself (standing instruction from the creator, 19/10/2026).** Never ask the creator to supply logos, fonts or
images: fetch them from a trustworthy source, check the file (an SVG must contain no script or external link), say in the report which
file came from where, and keep it in the skill (`assets/logos`, `assets/fonts`) with its licence. What worked: tool and brand **logos** as
single-colour SVGs from the open-source Simple Icons set through jsDelivr (`https://cdn.jsdelivr.net/npm/simple-icons@11.14.0/icons/<name>.svg`;
a name missing in the newest release is often still in an older one), tinted with the brand colour on a white disc (`orbit`/`trail` `logo`);
**fonts** from the Google Fonts repository (`https://raw.githubusercontent.com/google/fonts/main/ofl/<family>/<File>.ttf` plus its `OFL.txt`);
anything behind a script or a login (a press kit, a brand page) through the browser tools: **Playwright first** (see below), the
built-in browser to look at a page, Claude in Chrome only when the page needs the person's own session. Never download from an unknown
mirror, never run a downloaded file.

**Playwright (`mcp__playwright__*`, standing instruction 23/10/2026): search and download on its own, no asking.** It is the default
tool for finding a page, reading it and pulling a file whenever the plain `curl`/API route does not reach it (a "Download" button, a
script-rendered page, a search that needs a browser). Load the tools with ToolSearch ("playwright"). The routine:
1. `browser_navigate` to the source, `browser_snapshot` to read it (text beats screenshots); `browser_find`, `browser_click`,
   `browser_type` to search and open the right item.
2. Download with `browser_run_code_unsafe`, waiting for the browser's own download event (tested 23/10: it works, a file with a
   `Content-Disposition: attachment` header lands on disk): `const dp = page.waitForEvent('download'); await page.click(<button>)`
   (or `page.goto(url).catch(()=>{})` for a direct link), then `const d = await dp; await d.saveAs('<abs path under $W/broll/raw/ or the skill assets>')`.
   Inside that code `require` does not exist: only the `page` object. A cross-site `<a download>` link does not trigger a download; click
   the site's real button or use the direct file URL. Plain files with no script (logos on jsDelivr, fonts on GitHub raw) stay on `curl`.
3. Check the file as always (SVG without script or external link, clip duration/resolution with ffprobe), then conform it.
4. Same limits as every other route: licence first (Pexels, Coverr, Mixkit free, Simple Icons, OFL fonts, NASA), no login or
   payment, no bot-detection or CAPTCHA workaround (a "Just a moment..." page is retried once, then you switch source), nothing from an
   unknown mirror, nothing executed. Report in the storyboard note which file came from which page and licence.
Playwright's own scratch (snapshots, default downloads) goes to `.playwright-mcp/`, which is git-ignored; only files you moved into the
project count.

- **Tool logos:** the brand's press kit, or `npx hyperframes capture <url>` and the `<svg>` out of `extracted/page.html`
  (the real vector; watch for `fill="none"` paths and near-black wordmarks, make white variants for dark plates). The
  media-use skill's `scripts/resolve.mjs --type logo --intent "..." --project .` is another route (also `image`, `icon`,
  `bgm`, `sfx`).
- **Your own screen recordings** are the strongest cutaway: they are proof. **Public-domain archive** for a metaphor:
  NASA (`images-api.nasa.gov/search?q=...&media_type=video`, then the asset manifest's mp4).
- **Site captures:** request the explicit `/en` URL (a bare domain can geo-route to another language); a Cloudflare "Just
  a moment..." page is transient, retry. Never work around bot detection.
- **Pages that block robots:** do not work around it. Open the page in a real browser (Claude's browser tools), pull the
  facts with JavaScript (headline, date, nav, the logo `<svg>`, `@font-face` URLs, hero media), fetch fonts and images
  from their CDNs where allowed, and rebuild the top of the page at its real 1360 px layout, scaled to 50% into a 680 px
  browser card (resize the pane to 1360x765 first, scroll with `window.scrollTo`).
- **Stitched screenshots cannot fake a scroll** (pinned sections duplicate): one frame with a drift, a full-page capture
  in a scrolling window (4c, 4d), or your own screen recording.
- **X posts:** X's official embed (`platform.twitter.com/embed/Tweet.html?id=<ID>&theme=light&dnt=true&lang=en`) in
  headless Chrome at device scale 6, screenshotting the post's bordered parent (3300 px wide). Prove the text with the
  syndication JSON (`cdn.syndication.twimg.com/tweet-result?id=<ID>&token=<T>`, T =
  `((ID/1e15)*Math.PI).toString(36).replace(/(0+|\.)/g,'')`); post videos via `yt-dlp` as 1.1 s cutaways with a handle
  pill. Logged-out x.com answers headless Chrome with 403: never fake a user agent to get past it.
- **Person photos:** ask for the file. **Footage with captions burned in:** crop the plate about 10%, top-anchored.

## Stock B-roll route

The house routine runs this automatically (pick, download, clean, conform) and lists every clip in the storyboard. If
you would rather approve a shortlist first, say so and note it here.

- **Where:** every person or job you name, a 2.5 to 3.5 s full-frame `clip` right after you describe them, before the
  tool or answer is revealed (1.5 s is fine for an opener).
- **Search** in a forked subagent on a smaller model: two candidates per slot with page, licence, duration, resolution,
  fps, size, risks and the seconds to use, in `$W/broll-shortlist.md`, downloading nothing. Take the first unless a risk
  below rules it out.
- **Licence:** Pexels first (free on YouTube, no credit required, 4K), then Coverr and Mixkit's free licence. Never
  Mixkit's Restricted licence, never a clip labelled AI-generated, never a paid tier.
- **Look:** real people, a dark or moody room lit by screens, horizontal, 4K, no watermark, nobody looking into the lens,
  no readable brand logo or third-party UI (a recognisable but unreadable editor is fine).
- **Download** through the Pexels API (a free key in the `Authorization` header; take the 3840-wide entry in
  `video_files`) or the page's download button via Playwright (see "Playwright" above), into `$W/broll/raw/`.
- **Clean and conform** in one script per video (`$W/broll/conform-stock.sh`, the record of every window):
  `python3 "$SK/scripts/broll-conform.py" --4k --in "$W/broll/raw/<file>" --out "$W/public/broll/<job>.mp4" --start
  <s> --dur <slot + 1>`. Blur anything readable with `--vf "split[a][b];[b]crop=W:H:X:Y,boxblur=8[bb];[a][bb]overlay=X:Y"` in SOURCE
  pixels (find X and Y with ffmpeg's `drawgrid`); a crop rarely clears a label without wrecking the framing.
- **Pick the window by measured sharpness** (one clip breathed out of focus mid-window): the mean neighbour-pixel
  difference per 0.5 s on a 640x360 grey frame; take the steadiest high stretch. Snapshot every slot before rendering.

## AI B-roll route

Generated shots of you, from an image service and an image-to-video service of your choice. Narrow on purpose: these
shots work because the person is the presenter and the shot is the scene the sentence describes.

- **It stars you, or nobody:** never another real person; extras are generic and in the background. It shows the
  specific scene you describe, 2 to 5 s, on your words; if a viewer could not say what it shows in three words, cut it.
- **Never proof:** no fake dashboards, revenue, students, crowds, screenshots or results; proof is your real screen.
- About one shot a minute at most, never two in a row, each a `clip` with an anchor. **Label it on upload** (YouTube's
  "Altered or synthetic content": Yes). Every generation costs credits: quote the cost and get a yes for every run.

**The chain:**
1. Shot list first, `$W/BROLL.md`: anchor sentence, scene in one line, outfit (the one in your footage), camera move,
   length. Approved at Checkpoint B; nothing generates before.
2. References: a face pack (6 to 12 photos on a plain wall in video light: front, three-quarters, neutral and smiling,
   one half-body at your desk), photos of your empty set, and two or three frames from your footage (`ffmpeg -ss <t> -i
   "$W/public/input-video.mp4" -frames:v 1 ref-<n>.png`). The same set for every shot, or the face drifts. You upload
   your photos to the service yourself; Claude never posts them from the shell.
3. The still, 16:9, 2K: "The person from the reference photos, same face and hair, wearing [outfit], [one action] in [a
   specific place], [time of day] window light, 35mm lens at eye level, shallow depth of field, natural skin texture, no
   text, no logos, 16:9." Keep screens turned away or out of focus: generated screens show fake text.
4. Check the still (face, hands, anything written) before paying for motion: a bad still is a rerun, not a video.
5. Motion: image-to-video, 5 to 8 s, audio off, prompting the camera and one small action only ("slow push-in, he types,
   then looks up at the screen, natural motion, no cuts, no new people").
6. `python3 "$SK/scripts/broll-conform.py" --in "$W/broll/raw/<shot>.mp4" --out "$W/public/broll/<shot>.mp4" --start
   0.5 --dur 4 --grade` (`--start` skips the model's settle-in, `--grade` nudges it toward your footage), then read its
   sheet. Budget version: the still alone, `--in <shot>.png --dur 4`, a slow push-in (`--push 1.08`).
7. Into the storyboard as a `clip` beat on your words, with a `label` or a checklist when the shot carries a point.
