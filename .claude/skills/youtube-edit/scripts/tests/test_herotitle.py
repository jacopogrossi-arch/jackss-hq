"""formats/herotitle.py (format 46): hero phrase on a living gradient; nothing moves when a word appears."""
import os, re, sys, unittest
from .helpers import SCRIPTS

sys.path.insert(0, os.path.join(os.path.dirname(SCRIPTS), "formats"))
from herotitle import herotitle  # noqa: E402

L = [[("Claude", 1.11)], [("come", 3.99), ("strumento", 4.55)]]


def build(**k):
    a = dict(lines=L, t_in=1.11, t_out=5.8, logo="x/claude.svg", logo_at=1.59, gold_at=3.11)
    a.update(k)
    return herotitle(**a)


class Herotitle(unittest.TestCase):
    def test_line2_no_position_tween(self):
        js = build()["js"]
        found = re.findall(r"tl\.fromTo\('#w2_\d'[^;]*;", js)
        self.assertEqual(len(found), 2)
        for m in found:
            self.assertNotRegex(m, r"\b(x|left)\s*:")
        self.assertNotIn("display", js)
        self.assertNotIn("repeat", js)

    def test_word_count(self):
        o = build()
        self.assertEqual(len(re.findall(r'class="wd w[12]"', o["html"])), 3)
        self.assertEqual(len(re.findall(r"tl\.fromTo\('#w[12]_\d'", o["js"])), 3)
        self.assertEqual(o["html"].count("<audio"), 0)

    def test_mask_in_and_out(self):
        js = build()["js"].replace(" ", "")
        self.assertIn("{r:0},{r:1320,duration:0.45", js)
        self.assertIn("onUpdate:ap},1.110);", js)
        self.assertIn("{r:1320},{r:0,duration:0.400", js)
        self.assertIn("onUpdate:ap},5.400);", js)

    def test_logo_and_gold_optional(self):
        o = build(logo=None, logo_at=None, gold_at=None)
        self.assertNotIn('id="tile"', o["html"])
        self.assertNotIn(".gb'", o["js"])
        self.assertIn("img/claude.svg", build()["html"])

    def test_guards(self):
        with self.assertRaises(AssertionError):
            build(lines=L + [[("a", 3.0)]])
        with self.assertRaises(AssertionError):
            build(lines=[[(w, 2.0) for w in "abcd"], [("e", 3.0), ("f", 3.0), ("g", 3.0)]])
        with self.assertRaises(AssertionError):
            build(t_out=2.5)
        with self.assertRaises(AssertionError):
            build(t_out=9.0)


if __name__ == "__main__":
    unittest.main()
