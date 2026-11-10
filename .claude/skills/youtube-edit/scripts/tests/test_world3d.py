"""formats/world3d.py (format 52, the 3D plate): the spec the engine reads, the host the composer times, anchors for beat-check, one camera move at a time."""
import json, os, sys, unittest
from .helpers import SCRIPTS, scratch

SK = os.path.dirname(SCRIPTS)
sys.path.insert(0, os.path.join(SK, "formats"))
from world3d import World3D, VENDOR  # noqa: E402


def world():
    w = World3D("w1", 120.0, 127.5, title="Il *pantalone*", sub="Drop 1")
    w.trouser("tr", rot_y=-0.4, turn=[(0, 2.9, -0.18, "glide")])
    w.card("c1", (1.5, 0.7, 0), text="L'*idea*", t=124.0)
    w.cam((0.34, 1.10, 0.86), look=(0.07, 0.975, 0))
    w.cam((0.46, 0.82, 2.45), look=(0.05, 0.56, 0), t=122.9, d=1.5)
    w.label("tr", (0.18, 1.06, 0.03), "Vita *naturale*", t=120.9, anchor="vita", sub="regolatori laterali")
    return w


class World(unittest.TestCase):
    def test_spec_is_in_seconds_from_the_plate_start(self):
        s = world().spec()
        self.assertEqual(s["dur"], 7.5)
        self.assertEqual(s["cam"][1]["t"], 2.9)
        self.assertEqual(s["labels"][0]["t"], 0.9)
        self.assertEqual([o["type"] for o in s["objects"]], ["trouser", "card"])
        self.assertEqual(s["objects"][1]["t"], 4.0)                      # the card enters 4 s into the plate
        json.dumps(s)

    def test_host_is_a_timed_clip_and_labels_carry_their_word(self):
        o = world().build()
        self.assertRegex(o["html"], r'class="card-host clip w3-host" id="host-w1"[^>]*data-start="120.000" data-duration="7.500"')
        self.assertIn('data-at="120.900" data-anchor="vita"', o["html"])
        self.assertIn("<i>naturale</i>", o["html"])
        self.assertIn('import { mount } from "./vendor/world3d.js"', o["html"])

    def test_timeline_is_seek_safe(self):
        for line in world().build()["js"].split("\n"):
            self.assertTrue(line.startswith("tl.set(") or (line.startswith("tl.fromTo(") and "immediateRender:false" in line), line)
            self.assertRegex(line, r"\}, \d+(\.\d+)?\);$")                # the shape plates-build.py can move onto a new cut

    def test_one_camera_move_at_a_time(self):
        w = world()
        with self.assertRaises(ValueError):
            w.cam((1, 1, 1), look=(0, 0, 0), t=123.5)                    # the move of 122.9 lasts until 124.4
        with self.assertRaises(ValueError):
            World3D("x", 0, 5).spec()                                    # no camera

    def test_title_can_leave_before_the_camera_flies(self):
        w = World3D("w2", 10.0, 20.0, title="Dall'idea al *capo*", title_out=12.4)
        w.cam((0, 1, 2), look=(0, 0.5, 0))
        self.assertEqual(w.spec()["texts"][0]["out"], 2.4)

    def test_engine_never_runs_on_a_clock(self):
        js = open(os.path.join(SK, "assets", "vendor", "world3d.js"), encoding="utf-8").read()
        for bad in ("requestAnimationFrame", "Math.random", "Date.now", "performance.now", "setTimeout", "setInterval"):
            self.assertNotIn(bad, js)
        self.assertIn('addEventListener("hf-seek"', js)

    def test_lab_page_stages_the_engine(self):
        d = scratch(self)
        World3D.page(d, [world()])
        for f in VENDOR:
            self.assertTrue(os.path.exists(os.path.join(d, "vendor", f)), f)
        page = open(os.path.join(d, "index.html"), encoding="utf-8").read()
        self.assertRegex(page, r'data-composition-id="world3d-lab" data-start="0" data-duration="127.500"')
