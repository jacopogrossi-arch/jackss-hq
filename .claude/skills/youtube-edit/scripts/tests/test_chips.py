"""formats/chips.py (format 41b): chips land just before their words, arrows follow, the camera carries footage and chips."""
import os, re, sys, unittest
from .helpers import SCRIPTS

sys.path.insert(0, os.path.join(os.path.dirname(SCRIPTS), "formats"))
from chips import chips  # noqa: E402

ITEMS = [{"id": "claude", "name": "Claude", "logo": "img/claude.svg", "t": 1.109, "anchor": "Claude", "centre": (470, 420),
          "arrow": ((630, 430), (690, 425), (705, 460), (700, 520))},
         {"id": "canva", "name": "Canva", "logo": "img/canva.svg", "t": 7.349, "anchor": "Canva", "centre": (1480, 620),
          "arrow": ((1320, 620), (1255, 640), (1210, 620), (1185, 570))}]
CAM = [(1.0, 4.0, "p2", 1.07, 38, 40), (7.35, 7.91, "p3", 1.10, 62, 46), (9.0, 9.8, "sn", 1.03, 50, 40)]


class Chips(unittest.TestCase):
    def build(self):
        return chips(ITEMS, 9.6, 10.033, phrase=("uno strumento in più", 7.909, "uno strumento", "claude"), camera=CAM)

    def test_shape(self):
        o = self.build()
        self.assertEqual(len(re.findall(r'class="ch" ', o["html"])), 2)
        self.assertEqual(len(re.findall(r'<g id="ag-', o["html"])), 2)
        self.assertIn('id="phs">uno strumento in più<', o["html"])
        self.assertNotIn("<audio", o["html"])
        self.assertNotIn("radial-gradient", o["html"])

    def test_timing(self):
        o = self.build()
        self.assertIn('data-start="1.059"', o["html"])                            # 0.05 s before the word
        self.assertIn("duration:0.45, ease:'power2.out', immediateRender:false }, 1.139);", o["js"])   # arrow 0.08 s after
        self.assertIn("}, 9.600);", o["js"]); self.assertIn("}, 9.550);", o["js"])  # first chip leaves last

    def test_camera_carries_the_chips(self):
        o = self.build()
        self.assertIn("#host-ch-claude .card, #host-ch-canva .card, #host-phr .card", o["js"])
        self.assertIn("var K=[[1.0,4.0,p2,1.07,38,40],[7.35,7.91,p3,1.1,62,46],[9.0,9.8,sn,1.03,50,40]];", o["js"])

    def test_no_camera(self):
        self.assertNotIn("video-zoom", chips(ITEMS, 9.6, 10.033)["js"])

    def test_guard(self):
        with self.assertRaises(AssertionError):
            chips(ITEMS * 3, 9.6, 10.033)


if __name__ == "__main__":
    unittest.main()
