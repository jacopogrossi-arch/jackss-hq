"""formats/dotgrid.py (format 43): rows fill on their words, the shape follows rows x cols, guards hold, no sound."""
import os, re, sys, unittest
from .helpers import SCRIPTS

sys.path.insert(0, os.path.join(os.path.dirname(SCRIPTS), "formats"))
from dotgrid import dotgrid  # noqa: E402

ROWS = [("Outfit", 7.259, "tre outfit"), ("Mood board evocative", 7.899, "tre mood board"),
        ("Mood board tecniche", 9.659, "tre mood board"), ("Concept", 10.859, "tre concept")]


class Dotgrid(unittest.TestCase):
    def test_bench_shape(self):
        o = dotgrid(ROWS, "Tre di ogni cosa", 6.2, 11.5)
        self.assertEqual(len(re.findall(r'class="dgd"', o["html"])), 12)
        self.assertEqual(len(re.findall(r'class="dgl"', o["html"])), 4)
        self.assertIn('data-start="6.000"', o["html"])
        self.assertNotIn("<audio", o["html"])

    def test_rows_fill_on_their_words(self):
        o = dotgrid(ROWS, "Tre di ogni cosa", 6.2, 11.5)
        for r, (_, t, _) in enumerate(ROWS):
            self.assertIn("immediateRender:false }, %.3f);" % t, o["js"].split("tl.fromTo('#f%d0'" % r)[1].split("\n")[0])
            self.assertIn("tl.fromTo('#f%d2'" % r, o["js"])

    def test_other_shape(self):
        o = dotgrid(ROWS[:2], "Due", 1.0, 5.0, cols=5)
        self.assertEqual(len(re.findall(r'class="dgd"', o["html"])), 10)

    def test_guards(self):
        with self.assertRaises(AssertionError):
            dotgrid(ROWS[:1], "x", 1.0, 5.0)
        with self.assertRaises(AssertionError):
            dotgrid(ROWS, "x", 1.0, 5.0, cols=7)


if __name__ == "__main__":
    unittest.main()
