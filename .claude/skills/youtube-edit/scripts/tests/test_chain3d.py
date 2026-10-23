"""formats/chain3d.py (format 27b): the chain builds with the bench numbers, soft arrows, a swish per travel, no pops."""
import os, re, sys, unittest
from .helpers import SCRIPTS, scratch, needs_ffmpeg

sys.path.insert(0, os.path.join(os.path.dirname(SCRIPTS), "formats"))
from chain3d import chain3d, write_swish  # noqa: E402

STEPS = [("Claude in Chrome", "browser", 2.6, "Chrome"), ("Naviga sul web", "globe", 7.395, "navigare"),
         ("Pinterest", "search", 9.56, "Pinterest"), ("Sceglie le immagini", "doc", 11.8, "immagini"),
         ("Le impagina da solo", "check", 15.28, "impaginate")]


class Chain3d(unittest.TestCase):
    def test_bench_travels(self):
        o = chain3d(STEPS, 1.9, 16.3)
        self.assertEqual(o["travels"][1:], [(5.395, 7.295), (7.895, 9.46), (10.06, 11.7), (13.28, 15.18)])
        for ts, te in o["travels"][1:]:
            self.assertGreaterEqual(round(te - ts, 3), 1.4)

    def test_cards_arrows_sound(self):
        o = chain3d(STEPS, 1.9, 16.3)
        self.assertEqual(len(re.findall(r'class="glass bc"', o["html"])), 5)
        self.assertEqual(len(re.findall(r'id="ar\d"', o["html"])), 4)
        self.assertEqual(o["html"].count("<audio"), 4)
        self.assertIn('data-volume="0.25"', o["html"])
        self.assertNotIn("pop", o["html"].lower())
        self.assertIn("blur(1.6px)", o["html"])          # soft arrow body
        self.assertIn("205,0,238", o["html"])            # the last card and arrow are magenta

    def test_three_steps(self):
        o = chain3d([("A", "doc", 2.0, "a"), ("B", "doc", 6.0, "b"), ("C", "check", 10.0, "c")], 1.5, 12.0)
        self.assertEqual(len(re.findall(r'class="glass bc"', o["html"])), 3)
        self.assertEqual(len(re.findall(r'id="ar\d"', o["html"])), 2)

    def test_step_count_guard(self):
        with self.assertRaises(AssertionError):
            chain3d(STEPS[:2], 1.9, 16.3)

    @needs_ffmpeg
    def test_swish_file(self):
        d = scratch(self)
        write_swish(d)
        self.assertGreater(os.path.getsize(os.path.join(d, "sfx", "swish.mp3")), 1000)


if __name__ == "__main__":
    unittest.main()
