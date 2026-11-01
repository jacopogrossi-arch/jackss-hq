"""formats/tracker.py, counter.py, versus.py, diagram.py, uiplane.py (formats 47-51, 01/11/2026): shape, spoken anchors, seek-safety,
no sound, and the face PiP corner stays clear (plates_base.check_pip)."""
import os, re, sys, unittest
from .helpers import SCRIPTS

sys.path.insert(0, os.path.join(os.path.dirname(SCRIPTS), "formats"))
from plates_base import check_pip, keyword, plan_kicks, CAM_ORIGIN, CAM_DRIFT, PIP, MARGIN, GAP  # noqa: E402
from tracker import tracker  # noqa: E402
from counter import counter  # noqa: E402
from versus import versus  # noqa: E402
from diagram import diagram  # noqa: E402
from uiplane import uiplane  # noqa: E402

STEPS = ["Reference", "Audio", "Piano", "Storyboard", "Montaggio", "Revisioni", "Suoni"]


def seek_safe(test, o):
    """Every GSAP tween is a fromTo with immediateRender:false (or a tl.set), and nothing plays sound."""
    for line in o["js"].split("\n"):
        line = line.strip()
        if "tl.to(" in line or "tl.from(" in line:
            test.fail("not seek-safe: " + line)
        if "tl.fromTo(" in line:
            test.assertIn("immediateRender", line)
    for tag in re.findall(r"<audio[^>]*>", o["html"]):   # every sound has an id (else it is silent in the render) and its own track
        test.assertRegex(tag, r'id="sfx-')
        test.assertRegex(tag, r'data-track-index="\d+"')
        test.assertNotIn("@TRACK@", tag)


class PlatesBase(unittest.TestCase):
    def test_keyword_markup(self):
        self.assertEqual(keyword("Quanto *tempo* serve"), 'Quanto <i class="pl-key">tempo</i> serve')

    def test_pip_guard(self):
        check_pip(110, 330, 1300, 270)           # a row that ends at x 1410: clear
        with self.assertRaises(ValueError):
            check_pip(110, 600, 1700, 200)       # a wide strip across the PiP corner
        with self.assertRaises(ValueError):
            check_pip(1500, 700, 200, 100)       # inside the PiP margin


class Camera(unittest.TestCase):
    def test_kicks_fill_gaps_and_keep_spacing(self):
        ks = plan_kicks([2.0, 2.3, 9.0], 0.0, 12.0)           # 2.0 and 2.3 are one event; 2.0 -> 9.0 is a 7 s gap
        times = [t for t, _ in ks]
        self.assertEqual(times, sorted(times))
        self.assertTrue(all(b - a <= GAP + 0.01 for a, b in zip([0.3] + times, times + [11.3])), ks)   # nothing waits longer than GAP
        self.assertEqual(sum(1 for t, a in ks if a == 0.016), 2)                                      # the strong kicks: 2.0 and 9.0
        self.assertTrue(all(b - a >= 1.0 for (a, _), (b, _) in zip(ks, ks[1:])))

    def test_camera_never_pushes_anything_into_the_pip(self):
        """The camera scales about CAM_ORIGIN with at most CAM_DRIFT[0] * 1.016 and translates (x, y): a point outside the PiP zone must stay outside."""
        ox, oy = CAM_ORIGIN; sc, tx, ty = CAM_DRIFT; smax = sc * 1.016 * 1.008
        zx, zy = PIP[0] - MARGIN, PIP[1] - MARGIN
        for x in range(0, zx, 24):
            for y in list(range(0, 1080, 24)):
                x2, y2 = ox + (x - ox) * smax + tx, oy + (y - oy) * smax + ty
                self.assertFalse(x2 >= zx and y2 >= zy, (x, y, x2, y2))
        for y in range(0, zy, 24):
            for x in range(0, 1920, 24):
                x2, y2 = ox + (x - ox) * smax + tx, oy + (y - oy) * smax + ty
                self.assertFalse(x2 >= zx and y2 >= zy, (x, y, x2, y2))


class Sound(unittest.TestCase):
    def test_plate_sounds_on_and_off(self):
        on = tracker(STEPS, 3, "x", 0.0, 6.0)
        self.assertIn('id="sfx-tk-in"', on["html"]); self.assertIn('id="sfx-tk-out"', on["html"])
        off = tracker(STEPS, 3, "x", 0.0, 6.0, sound=False)
        self.assertNotIn("<audio", off["html"])

    def test_ui_typing_and_click_only_with_a_cursor(self):
        o = uiplane("P", {"text": "abc", "t": 2.0, "anchor": "a"}, 0, 12, button={"label": "Ok", "click_at": 9.5})
        self.assertIn('id="sfx-ui-type"', o["html"]); self.assertIn('id="sfx-ui-click"', o["html"])
        o2 = uiplane("P", {"text": "abc", "t": 2.0, "anchor": "a"}, 0, 12)
        self.assertNotIn("sfx-ui-click", o2["html"])


class Tracker(unittest.TestCase):
    def test_shape_and_state(self):
        o = tracker(STEPS, 3, "*7* step", 0.0, 6.0, at=2.2, anchor="storyboard")
        self.assertEqual(len(re.findall(r'class="pl-card tk-c"', o["html"])), 7)
        self.assertEqual(len(re.findall(r'class="pl-ck"', o["html"])), 3)         # the three steps before the active one are ticked
        self.assertIn('data-at="2.200" data-anchor="storyboard"', o["html"])      # the active card carries its word
        seek_safe(self, o)

    def test_guards(self):
        with self.assertRaises(AssertionError):
            tracker(STEPS[:2], 0, "x", 0, 5)
        with self.assertRaises(AssertionError):
            tracker(STEPS, 7, "x", 0, 5)


class Counter(unittest.TestCase):
    ITEMS = [("Studio", "≈10 ore", 1.4, "dieci ore"), ("Piano", "≈15 min", 2.4, "un quarto d'ora"), ("Storyboard", "≈30 min", 3.4, "mezz'oretta")]

    def test_count_up_on_the_word(self):
        o = counter(self.ITEMS, "Quanto *tempo* serve", 0, 9, bar=(0.34, "≈30 min miei, dentro *1h40*", 6.0, "mezz'ora"))
        self.assertEqual(len(re.findall(r'class="pl-card ct-c"', o["html"])), 3)
        self.assertIn("onUpdate: put", o["js"])
        self.assertIn("{ v: 15, duration: 0.6", o["js"])
        self.assertIn('data-anchor="mezz&#x27;ora"', o["html"])
        seek_safe(self, o)

    def test_text_values_do_not_count(self):
        o = counter([("A", "sì", 1.0, "a"), ("B", "no", 2.0, "b")], "x", 0, 5)
        self.assertNotIn("onUpdate: put", o["js"])

    def test_guards(self):
        with self.assertRaises(AssertionError):
            counter(self.ITEMS[:1], "x", 0, 5)


class Versus(unittest.TestCase):
    def test_two_cards_and_a_winner(self):
        o = versus({"label": "A", "t": 2.0, "anchor": "a"}, {"label": "B", "t": 3.4, "anchor": "b"}, "x", 0, 10, win="right", win_at=6.5)
        self.assertEqual(len(re.findall(r'class="pl-card vs-c"', o["html"])), 2)
        self.assertIn("#vsV", o["js"])
        self.assertIn("scale:1.04", o["js"])
        seek_safe(self, o)


class Diagram(unittest.TestCase):
    def test_shape_strike_and_connectors(self):
        o = diagram({"label": "Claude", "t": 1.2, "anchor": "cervello"},
                    [{"label": "A", "t": 2.0, "anchor": "a"}, {"label": "B", "t": 3.0, "anchor": "b", "strike_t": 5.0}],
                    [{"label": "C", "t": 6.0, "anchor": "c"}], "x", 0, 9)
        self.assertEqual(len(re.findall(r'class="dg-svg"', o["html"])), 3)         # one connector per pill
        self.assertIn('id="dgxi1"', o["html"])                                      # only the struck pill has a strike
        self.assertNotIn('id="dgxi0"', o["html"])
        seek_safe(self, o)

    def test_pip_and_size_guards(self):
        with self.assertRaises(AssertionError):
            diagram({"label": "C", "t": 1}, [{"label": "a", "t": 2}], [{"label": str(i), "t": 3} for i in range(4)], "x", 0, 9)   # a 4th output would enter the PiP corner


class Uiplane(unittest.TestCase):
    def test_typing_reply_and_click(self):
        o = uiplane("Piano", {"text": "Preparalo per il montaggio", "t": 2.0, "anchor": "preparalo"},
                    0, 12, replies=[{"text": "Fatto.", "t": 5.0, "anchor": "fatto"}], button={"label": "Approva", "done": "Approvato", "click_at": 9.5})
        self.assertIn("onUpdate: put", o["js"])                                      # the prompt types out
        self.assertIn("Approvato", o["js"])                                          # the button changes on the click
        self.assertIn('id="uiH"', o["html"])                                         # the hand cursor
        seek_safe(self, o)


if __name__ == "__main__":
    unittest.main()
