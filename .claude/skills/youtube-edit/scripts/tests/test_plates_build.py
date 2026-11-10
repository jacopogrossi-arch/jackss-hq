"""plates-build.py: plates timed on their own elements, joined into boards when close, graphics beside the face kept as they are, and the whole
timeline moved onto a new cut."""
import importlib.util, json, os, re, unittest
from .helpers import SCRIPTS, run, scratch, write

spec = importlib.util.spec_from_file_location("plates_build", os.path.join(SCRIPTS, "plates-build.py"))
pb = importlib.util.module_from_spec(spec); spec.loader.exec_module(pb)

BLOCK = r'''
from scene import Scene


def build():
    out = []
    s = Scene("p1", 10.0, 20.0, title="Uno *strumento*", fade_in=0, fade_out=0)
    s.pill(300, 400, "Idea", t=11.0, anchor="idea"); s.pill(300, 520, "Ricerca", t=12.0, anchor="ricerca")
    out.append(s.build())
    s = Scene("p2", 15.0, 30.0, title="La *mappa*", fade_in=0, fade_out=0)
    s.pill(300, 400, "Tappa", t=15.5, anchor="tappa")
    out.append(s.build())
    s = Scene("p3", 58.0, 70.0, title="Il *prezzo*", fade_in=0, fade_out=0)
    s.pill(300, 400, "Costo", t=60.0, anchor="costo")
    out.append(s.build())
    s = Scene("side1", 40.0, 44.0, bg=False, fade_in=0.2)
    s.pill(1300, 300, "Accanto", t=40.5, anchor="accanto")
    out.append(s.build())
    return {"html": "\n".join(o["html"] for o in out), "js": "\n".join(o["js"] for o in out)}
'''


class Recut(unittest.TestCase):
    def test_times_move_onto_the_new_cut(self):
        T = pb.make_T([{"insert": 88.3, "dur": 1.0}, {"cut": [206.7, 214.0]}])      # the two changes of Video #3
        self.assertEqual(T(50.0), 50.0)
        self.assertAlmostEqual(T(100.0), 101.0)
        self.assertAlmostEqual(T(210.0), 207.7)             # inside the removed stretch: its start
        self.assertAlmostEqual(T(300.0), 300.0 + 1.0 - 7.3)
        self.assertEqual(pb.make_T(None)(12.5), 12.5)

    def test_retime_refuses_half_a_timeline(self):
        js = "tl.set('#a', { opacity:0 }, 0);\ntl.fromTo('#a', {x:0}, {x:1, duration:.4}, 3.5);"
        self.assertIn("}, 4.500);", pb.retime_js(js, pb.make_T([{"insert": 1.0, "dur": 1.0}])))
        with self.assertRaises(SystemExit):
            pb.retime_js("tl.set('#a', { opacity:0 }, t0);", lambda t: t)

    def test_a_host_keeps_its_end_and_a_sound_its_length(self):
        T = pb.make_T([{"cut": [12.0, 14.0]}])
        h = pb.retime_html('<div class="clip" data-start="10.000" data-duration="10.000"></div><audio id="s" data-start="16.000" data-duration="1.50"></audio>', T)
        self.assertIn('data-start="10.000" data-duration="8.000"', h)
        self.assertIn('data-start="14.000" data-duration="1.50"', h)


class Build(unittest.TestCase):
    def build(self, plan=None):
        d = scratch(self)
        write(os.path.join(d, "plates", "b1.py"), BLOCK)
        write(os.path.join(d, "plates", "plan.json"), dict({"duration": 80.0}, **(plan or {})))
        r = run("plates-build.py", d, "--no-compose")
        self.assertEqual(r.returncode, 0, r.stderr[-800:])
        return json.load(open(os.path.join(d, "build", "storyboard.json"), encoding="utf-8")), open(os.path.join(d, "build", "PLATES.md"), encoding="utf-8").read()

    def test_close_plates_share_a_board_and_start_on_their_first_element(self):
        sb, md = self.build()
        self.assertIn("3 plates in 2 runs", md)
        self.assertIn("| 0 | p1 | 0:10.8 | 0:15.2 |", md)        # in 0.25 s before "idea" (not the 10.0 of the block); out on the swipe to p2, which starts 0.25 s before "tappa"
        self.assertIn("| 1 | p3 | 0:59.8 | 1:01.8 |", md)        # alone: out 1.8 s after its last element, not the 70.0 of the block
        self.assertIn("| 0 | p2 |", md)
        self.assertIn("| 1 | p3 |", md)
        self.assertIn("side1", sb["raw_html"])                   # the graphic beside the face is in the video, outside the boards
        self.assertNotIn("| side1 |", md)
        self.assertEqual(sb["preset"], "plates-verde")

    def test_plan_overrides_drops_and_recuts(self):
        sb, md = self.build({"override": {"p3": [59.0, 66.0]}, "drop": ["p2"], "transitions": [9.5], "recut": [{"cut": [30.0, 35.0]}]})
        self.assertIn("2 plates in 2 runs", md)
        self.assertIn("| 1 | p3 | 0:54.0 | 1:01.0 |", md)        # by hand, then 5 s earlier on the new cut
        self.assertEqual(sb["duration"], 75.0)
        self.assertEqual(sb["beats"][0]["at"], 9.5)
        self.assertFalse(re.search(r"back\.out", sb["raw_js"]))
