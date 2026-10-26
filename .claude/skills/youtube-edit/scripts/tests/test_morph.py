"""formats/morph.py (format 45): one shape that changes, the bench times, a swish per change, no pops, the spacing guard."""
import os, re, sys, unittest
from .helpers import SCRIPTS, scratch, write

sys.path.insert(0, os.path.join(os.path.dirname(SCRIPTS), "formats"))
from morph import morph, write_swish  # noqa: E402

IMGS = ["a.jpg", "b.jpg", "c.jpg", "d.jpg", "e.jpg", "f.jpg"]
STEPS = [
    {"kind": "pill", "label": "Claude in Chrome", "at": 2.6, "anchor": "Chrome", "text": "Claude in Chrome", "click": 5.6},
    {"kind": "circle", "label": "Naviga sul web", "at": 7.395, "anchor": "navigare", "icon": "globe"},
    {"kind": "square", "label": "Pinterest", "at": 9.56, "anchor": "Pinterest", "logo": "p.png"},
    {"kind": "grid", "label": "Sceglie le immagini", "at": 11.8, "anchor": "immagini", "images": IMGS},
    {"kind": "page", "label": "Le impagina da solo", "at": 15.28, "anchor": "impaginate", "images": IMGS, "title": "Royal Humour", "check_at": 15.7},
]


class Morph(unittest.TestCase):
    def test_bench_times(self):
        t = morph(STEPS, 1.3, 16.3)["times"]
        self.assertEqual(t["start"], [1.8, 6.595, 8.76, 11.0, 14.48])
        self.assertEqual(t["end"], [2.5, 7.295, 9.46, 11.7, 15.18])
        self.assertEqual(t["line_at"], 1.3)
        self.assertEqual(t["duration"], 16.5)
        for s, e in zip(t["start"], t["end"]):
            self.assertAlmostEqual(e - s, 0.7, places=3)

    def test_late_t_in_starts_early(self):
        t = morph(STEPS, 2.0, 16.3)["times"]
        self.assertEqual(t["card_start"], 1.3)          # line (0.5 s) + change (0.7 s) + 0.1 s need 1.3 s before the word

    def test_swish_and_no_pop(self):
        o = morph(STEPS, 1.3, 16.3)
        self.assertEqual(o["times"]["swish"], [6.595, 8.76, 11.0, 14.48])
        self.assertEqual(o["html"].count("<audio"), 4)
        self.assertIn('data-volume="0.25"', o["html"])
        self.assertNotIn("pop", o["html"].lower())
        self.assertIn("power3.inOut", o["js"])
        self.assertIn("Playfair Display", o["html"])
        self.assertIn("Inter", o["html"])

    def test_every_tween_is_fromto(self):
        js = morph(STEPS, 1.3, 16.3)["js"]
        self.assertNotRegex(js, r"tl\.to\(")
        self.assertEqual(len(re.findall(r'id="tl3_\d"', morph(STEPS, 1.3, 16.3)["html"])), 6)   # grid tiles, reused by the page

    def test_three_steps(self):
        o = morph([{"kind": "pill", "label": "A", "at": 3.0, "anchor": "a", "text": "ciao"},
                   {"kind": "circle", "label": "B", "at": 6.0, "anchor": "b", "icon": "globe"},
                   {"kind": "grid", "label": "C", "at": 9.0, "anchor": "c", "images": IMGS[:3]}], 2.0, 11.0)
        self.assertEqual(o["html"].count("<audio"), 2)
        self.assertEqual(len(re.findall(r'class="tile"', o["html"])), 3)

    def test_guards(self):
        with self.assertRaises(AssertionError):
            morph(STEPS[:2], 1.3, 16.3)
        close = [dict(s) for s in STEPS]
        close[1]["at"] = 3.5                              # 0.9 s after the first
        with self.assertRaises(AssertionError) as cm:
            morph(close, 1.3, 16.3)
        self.assertIn("27", str(cm.exception))
        back = [dict(s) for s in STEPS]
        back[2]["at"] = 6.0
        with self.assertRaises(AssertionError):
            morph(back, 1.3, 16.3)

    def test_public_copy(self):
        d = scratch(self)
        src = write(os.path.join(d, "src", "x.jpg"), "x")
        o = morph([{"kind": "pill", "label": "A", "at": 3.0, "anchor": "a", "text": "ciao"},
                   {"kind": "grid", "label": "B", "at": 6.0, "anchor": "b", "images": [src, src]},
                   {"kind": "page", "label": "C", "at": 9.0, "anchor": "c", "images": [src, src]}], 2.0, 11.0, public=os.path.join(d, "public"))
        self.assertTrue(os.path.exists(os.path.join(d, "public", "img", "x.jpg")))
        self.assertIn('src="img/x.jpg"', o["html"])


if __name__ == "__main__":
    unittest.main()
