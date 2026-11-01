"""Presets (editing types): compose.py loads presets/<name>/preset.json, merges its style under the storyboard's own, and fails clearly on a typo."""
import json, os, re, unittest
from .helpers import run, scratch, write, read

SCRIPTS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRESETS = os.path.join(os.path.dirname(SCRIPTS), "presets")
LINE = {"type": "line", "id": "l1", "text": "hello there", "em": [1], "color": "cyan", "in": 1.0, "out": 4.0, "anchor": "-"}


def board(**extra):
    spec = {"id": "t", "duration": 10.0, "beats": [dict(LINE)]}
    spec.update(extra)
    return spec


class Presets(unittest.TestCase):
    def build(self, spec, *extra):
        d = scratch(self)
        sp = write(os.path.join(d, "storyboard.json"), spec)
        r = run("compose.py", "--spec", sp, "--out", os.path.join(d, "public"), *extra)
        page = read(os.path.join(d, "public", "index.html")) if r.returncode == 0 else ""
        return r, page, d

    def test_every_preset_is_valid_json_with_a_style(self):
        names = [n for n in os.listdir(PRESETS) if os.path.isdir(os.path.join(PRESETS, n))]
        self.assertTrue(names, "no preset shipped")
        for n in names:
            with open(os.path.join(PRESETS, n, "preset.json"), encoding="utf-8") as fh:
                p = json.load(fh)
            self.assertEqual(p["name"], n)
            self.assertIn("style", p)
            self.assertTrue(os.path.exists(os.path.join(PRESETS, n, "README.md")), n + " has no README")

    def test_preset_style_reaches_the_page(self):
        r, page, d = self.build(board(), "--preset", "elegante-portfolio")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("preset: elegante-portfolio", r.stdout)
        self.assertIn("--k-accent:#d4af5f", page)
        self.assertIn('font-family:"Inter"', page)                     # @font-face from the preset's font_faces
        self.assertTrue(os.path.exists(os.path.join(d, "public", "fonts", "Inter.ttf")))

    def test_preset_named_in_the_storyboard(self):
        r, page, _ = self.build(board(preset="elegante-portfolio"))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("--k-accent:#d4af5f", page)

    def test_storyboard_style_wins_over_the_preset(self):
        r, page, _ = self.build(board(style={"accent": "#112233", "lines": {"size": 50}}), "--preset", "elegante-portfolio")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("--k-accent:#112233", page)
        self.assertIn("--k-accent2:#4aa585", page)                      # untouched values still come from the preset
        self.assertIn("font-size:50px", page)                           # lines merged key by key: size overridden...
        self.assertIn("font-weight:600", page)                          # ...weight kept from the preset

    def test_no_preset_keeps_the_old_look(self):
        r, page, _ = self.build(board())
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn("preset:", r.stdout)
        self.assertIn("--k-accent:#d4af5f", page)                       # studio.py's own default palette

    def test_default_preset_is_plates_verde(self):
        """No --preset and none in the storyboard: the whole system wears plates-verde (Jacopo, 01/11/2026); --preset none gives the old look back."""
        d = scratch(self)
        spec = write(os.path.join(d, "s.json"), {"id": "t", "duration": 8.0, "video": "x.mp4", "beats": [{"type": "line", "id": "a", "text": "Hello *world*", "in": 1.0, "out": 3.0, "anchor": "-"}], "camera": []})
        r = run("compose.py", "--spec", spec, "--out", os.path.join(d, "public"), env={"YTE_DEFAULT_PRESET": "1"})
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("preset: plates-verde", r.stdout)
        page = read(os.path.join(d, "public", "index.html"))
        self.assertIn("--k-bg:#0A2B1E", page)                 # the preset's tokens reached the page
        self.assertNotIn("0AF0F0", page.upper())              # the old cyan was repainted (legacy_swap)
        r2 = run("compose.py", "--spec", spec, "--out", os.path.join(d, "public2"), "--preset", "none")
        self.assertNotIn("preset:", r2.stdout)

    def test_ivory_look_reaches_the_older_formats(self):
        """plates-verde: the older formats get solid ivory cards, Inter instead of DM Sans, an italic serif key word; --preset none keeps the glass look."""
        d = scratch(self)
        spec = write(os.path.join(d, "s.json"), {"id": "t", "duration": 8.0, "video": "x.mp4", "beats": [
            {"type": "list", "id": "l", "eyebrow": "Cosa serve", "items": [["Una camera", 1.5, "-"]], "in": 1.0, "out": 4.0, "pos": "tl"},
            {"type": "stats", "id": "s", "layout": "row", "title": "I *numeri*", "items": [{"value": 5, "label": "x", "at": 5.0}], "in": 4.5, "out": 7.0}], "camera": []})
        r = run("compose.py", "--spec", spec, "--out", os.path.join(d, "public"), env={"YTE_DEFAULT_PRESET": "1"})
        self.assertEqual(r.returncode, 0, r.stderr)
        page = read(os.path.join(d, "public", "index.html"))
        self.assertIn("look ivory", page)                                       # the stylesheet layer
        self.assertIn("rgba(244,239,230,0.97)", page)                           # glassIn lands on ivory
        self.assertNotIn("rgba(255,255,255,0.18)", page.split("<script>")[-1])   # no light-glass tint left in the scripts
        self.assertNotRegex(page, r'font-family:\s*"DM Sans"(?!;\s*src)')        # only the @font-face lines still name DM Sans
        r2 = run("compose.py", "--spec", spec, "--out", os.path.join(d, "public2"), "--preset", "none")
        page2 = read(os.path.join(d, "public2", "index.html"))
        self.assertNotIn("look ivory", page2); self.assertIn("rgba(255,255,255,0.18)", page2)

    def test_smooth_sound_and_camera_reach_the_older_formats(self):
        """plates-verde (sound.smooth): every thing that appears gets a smooth swish, the full-frame formats get a push-in and kicks; --preset none keeps pops and no camera."""
        d = scratch(self)
        spec = write(os.path.join(d, "s.json"), {"id": "t", "duration": 14.0, "video": "x.mp4", "beats": [
            {"type": "stats", "id": "st", "layout": "row", "title": "I *numeri*", "items": [{"value": 5, "label": "a", "at": 2.0}, {"value": 7, "label": "b", "at": 3.5}], "in": 1.0, "out": 6.0},
            {"type": "pipeline", "id": "pl", "title": "", "steps": [{"label": "Idea", "icon": "chat", "at": 8.0}, {"label": "Video", "icon": "video", "at": 9.5}], "in": 7.0, "out": 13.0},
            {"type": "line", "id": "ln", "text": "Hello world", "em": [1], "in": 6.2, "out": 6.9, "anchor": "-"}], "camera": []})
        r = run("compose.py", "--spec", spec, "--out", os.path.join(d, "public"), env={"YTE_DEFAULT_PRESET": "1"})
        self.assertEqual(r.returncode, 0, r.stderr)
        page = read(os.path.join(d, "public", "index.html"))
        smooth = re.findall(r'<audio id="sfx-[^"]*" src="sfx/(?:es-[a-z-]+|pl-soft)\.mp3"', page)
        self.assertGreaterEqual(len(smooth), 6)                               # entrance + 2 items for stats, entrance + 2 steps for the pipeline, the line: some may share a cue
        self.assertNotIn("sfx/typing", page)                                  # a line that is not typed out gets a smooth swish, not a typing sound
        self.assertIn("#host-st .card", page); self.assertIn("#host-pl .card", page)   # camera kicks on the cards of the full-frame formats
        self.assertIn("scale:1.035", page.replace(" ", ""))                   # the slow push-in
        r2 = run("compose.py", "--spec", spec, "--out", os.path.join(d, "public2"), "--preset", "none")
        page2 = read(os.path.join(d, "public2", "index.html"))
        self.assertNotIn("#host-st .card", page2)                             # no camera without the preset
        self.assertNotRegex(page2, r'src="sfx/(?:es-[a-z-]+|pl-soft)\.mp3"')

    def test_unknown_preset_lists_the_available_ones(self):
        r, _, _ = self.build(board(), "--preset", "does-not-exist")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("elegante-portfolio", r.stdout + r.stderr)


if __name__ == "__main__":
    unittest.main()
