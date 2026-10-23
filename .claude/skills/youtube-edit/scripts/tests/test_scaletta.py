"""formats/scaletta.py (format 44): items land on their words, bars follow the count, the wash waits for the first item."""
import os, re, sys, unittest
from .helpers import SCRIPTS

sys.path.insert(0, os.path.join(os.path.dirname(SCRIPTS), "formats"))
from scaletta import scaletta  # noqa: E402

ITEMS = [("Outfit", 7.26, "tre outfit", 3), ("Mood board evocative", 7.90, "tre mood board evocative", 3),
         ("Mood board tecniche", 9.66, "tre mood board tecniche", 3), ("Concept", 10.86, "tre concept", 3)]


class Scaletta(unittest.TestCase):
    def test_bench_shape(self):
        o = scaletta(ITEMS, "Cosa doveva uscire", 6.2, 11.5)
        self.assertEqual(len(re.findall(r'class="tl-e"', o["html"])), 4)
        self.assertEqual(len(re.findall(r'class="tl-bar"', o["html"])), 12)
        self.assertEqual(o["html"].count("×3"), 4)
        self.assertNotIn("<audio", o["html"])
        self.assertNotIn("radial-gradient", o["html"])

    def test_wash_waits_for_first_item(self):
        o = scaletta(ITEMS, "Cosa doveva uscire", 6.2, 11.5)
        self.assertIn("tl.fromTo('#tlw', {opacity:0}, Object.assign({}, {opacity:1}, { duration:0.400, ease:'power3.out', immediateRender:false }), 7.100);", o["js"])

    def test_counts(self):
        o = scaletta([("A", 2.0, "a", 0), ("B", 4.0, "b", 5)], "T", 1.5, 8.0)
        self.assertEqual(len(re.findall(r'class="tl-bar"', o["html"])), 5)
        self.assertNotIn("×0", o["html"])

    def test_guard(self):
        with self.assertRaises(AssertionError):
            scaletta(ITEMS[:1], "T", 1.0, 5.0)


if __name__ == "__main__":
    unittest.main()
