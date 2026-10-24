"""grade-looks.py: a look is a pure colour function. Neutral changes nothing, contrast spreads darks and lights apart,
and the hue windows touch only the colour they name (skin lift leaves the sea alone, and the other way round)."""
import importlib.util, os, unittest
import numpy as np
from .helpers import run, scratch


def load():
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    spec = importlib.util.spec_from_file_location("grade_looks", os.path.join(here, "grade-looks.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def flat(c):
    a = np.zeros((20, 20, 3), np.float32)
    a[:] = c
    return a


class GradeLooks(unittest.TestCase):
    def setUp(self):
        self.gl = load()

    def test_neutral_changes_nothing_and_every_preset_look_runs(self):
        px = np.random.default_rng(1).random((16, 16, 3)).astype(np.float32)
        self.assertTrue(np.allclose(self.gl.apply_look(px, {}), px))
        looks = self.gl.gs.CFG["looks"]
        self.assertGreaterEqual(len(looks), 10)
        for name, lk in looks.items():
            out = self.gl.apply_look(px, lk["p"])
            self.assertEqual(out.shape, px.shape, name)
            self.assertTrue(np.isfinite(out).all() and out.min() >= 0 and out.max() <= 1, name)
            self.assertTrue(lk["title"] and lk["desc"], name)

    def test_contrast_darkens_darks_and_brightens_lights(self):
        dark, light = flat((0.2, 0.2, 0.2)), flat((0.8, 0.8, 0.8))
        p = {"contrast": 0.6}
        self.assertLess(self.gl.apply_look(dark, p)[0, 0, 1], 0.2)
        self.assertGreater(self.gl.apply_look(light, p)[0, 0, 1], 0.8)

    def test_skin_window_lifts_skin_but_not_water(self):
        skin, water = flat((0.62, 0.45, 0.35)), flat((0.45, 0.70, 0.68))
        p = {"skin_luma": 1.2}
        self.assertGreater(self.gl.gs.luma(self.gl.apply_look(skin, p))[0, 0], self.gl.gs.luma(skin)[0, 0] * 1.1)
        self.assertTrue(np.allclose(self.gl.apply_look(water, p), water, atol=1e-4))

    def test_water_window_deepens_water_but_not_skin(self):
        skin, water = flat((0.62, 0.45, 0.35)), flat((0.45, 0.70, 0.68))
        p = {"sea_sat": 1.4, "sea_luma": 0.9}
        self.assertLess(self.gl.gs.luma(self.gl.apply_look(water, p))[0, 0], self.gl.gs.luma(water)[0, 0])
        self.assertTrue(np.allclose(self.gl.apply_look(skin, p), skin, atol=1e-4))

    def test_dither_keeps_a_smooth_gradient_smooth(self):
        ramp = np.tile(np.linspace(0.30, 0.31, 2000, dtype=np.float32)[None, :, None], (4, 1, 3))   # 1 % of the range across 2000 px
        u8 = self.gl.gs.to_u8(ramp).astype(np.float32)
        left, right = u8[:, :200].mean(), u8[:, -200:].mean()
        self.assertGreater(right, left)                                      # the slope survives
        self.assertLess(abs((right - left) - 0.01 * 255 * 0.9), 0.6)         # and is not lost to hard 8-bit steps


if __name__ == "__main__":
    unittest.main()
