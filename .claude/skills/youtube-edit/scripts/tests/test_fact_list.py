"""fact-list.py: sentences with a number, year, price or tool are listed; plain sentences are not; nothing is ever 'verified'."""
import os, unittest
from .helpers import read, run, scratch, write


def words(text, t0=0.0):
    out, t = [], t0
    for w in text.split():
        out.append({"text": w, "start": t, "end": t + 0.3}); t += 0.35
    return out


class FactList(unittest.TestCase):
    def test_lists_checkable_sentences_only(self):
        d = scratch(self)
        ws = (words("I like sitting at my desk.", 0) + words("The collection has 12 pieces.", 10)
              + words("It started in March 2026.", 20) + words("Canva exports the file.", 30) + words("Then we go home.", 40))
        tr = write(os.path.join(d, "t.json"), {"words": ws})
        out = os.path.join(d, "FACTS.md")
        r = run("fact-list.py", "--transcript", tr, "--out", out)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        text = read(out)
        self.assertIn("12 pieces", text)                       # a number
        self.assertIn("March 2026", text)                      # a date and a year
        self.assertIn("tool: Canva", text)                     # a tool claim, in its own softer group
        self.assertNotIn("sitting at my desk", text)           # plain speech is not listed
        self.assertNotIn("go home", text)
        self.assertIn("Nothing here has been checked", text)   # it lists, it never verifies
        self.assertLess(text.index("12 pieces"), text.index("Canva exports"))   # hard facts come before tool claims


if __name__ == "__main__":
    unittest.main()
