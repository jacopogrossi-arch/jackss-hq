"""Presets (editing types): compose.py loads presets/<name>/preset.json, merges its style under the storyboard's own, and fails clearly on a typo."""
import json, os, unittest
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

    def test_unknown_preset_lists_the_available_ones(self):
        r, _, _ = self.build(board(), "--preset", "does-not-exist")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("elegante-portfolio", r.stdout + r.stderr)


if __name__ == "__main__":
    unittest.main()
