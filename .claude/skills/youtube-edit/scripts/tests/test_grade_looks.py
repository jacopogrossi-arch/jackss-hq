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

    def test_learned_colour_map_changes_chroma_not_luma_and_gain_scales_it(self):
        gl = self.gl
        base = {"contrast": 0.0}
        cands = [(r, g, b) for r in (0.45, 0.6, 0.75) for g in (0.6, 0.72, 0.85) for b in (0.55, 0.7, 0.82)]
        chroma = lambda a: np.stack([(a[..., 2] - gl.gs.luma(a)) / 1.8556, (a[..., 0] - gl.gs.luma(a)) / 1.5748], axis=-1)
        best, bd = None, 0.0
        for c in cands:                                          # a colour the map actually moves (it only moves colours his clips contained)
            x = flat(c)
            dd = float(np.abs(chroma(gl.apply_look(x, dict(base, chroma_map="jacopo-chroma"))) - chroma(x)).max())
            if dd > bd:
                best, bd = c, dd
        self.assertGreater(bd, 0.002, "the learned map moves no colour at all")
        x = flat(best)
        one = gl.apply_look(x, dict(base, chroma_map="jacopo-chroma", chroma_gain=1.0))
        wow = gl.apply_look(x, dict(base, chroma_map="jacopo-chroma", chroma_gain=1.5))
        self.assertTrue(np.allclose(gl.gs.luma(one), gl.gs.luma(x), atol=2e-3))            # the light is the look's job, not the map's
        d1, d15 = chroma(one) - chroma(x), chroma(wow) - chroma(x)
        self.assertTrue(np.allclose(d15, 1.5 * d1, atol=2e-3))                              # the gain scales the shift
        far = flat((0.9, 0.1, 0.9))                                                         # a colour his clips never had: left almost alone
        self.assertLess(float(np.abs(gl.apply_look(far, dict(base, chroma_map="jacopo-chroma")) - far).max()), 0.02)

    def test_jacopo_looks_are_in_the_preset(self):
        looks = self.gl.gs.CFG["looks"]
        self.assertEqual(looks["jacopo-cinema"]["p"]["chroma_map"], "jacopo-chroma")
        self.assertIn("wow", looks["jacopo-cinema-wow"]["p"])                                     # the WOW is a real second colour pass, not a bigger gain on a near-zero correction
        lo, hi = self.gl.gs.CFG["skin_band"]
        self.assertLess(hi, 0.55)                                                               # his skin sits at 34-42 IRE: the exposure band follows it

    def test_wow_adds_colour_to_water_and_skin_without_touching_light(self):
        gl = self.gl
        looks = gl.gs.CFG["looks"]
        water, skin = flat((0.45, 0.70, 0.68)), flat((0.62, 0.45, 0.35))
        sat = lambda a: float(np.abs(a - gl.gs.luma(a)[..., None]).max(axis=-1).mean())
        for c in (water, skin):
            plain = gl.apply_look(c, looks["jacopo-cinema"]["p"])
            wow = gl.apply_look(c, looks["jacopo-cinema-wow"]["p"])
            self.assertGreater(sat(wow), sat(plain) * 1.05)                                       # clearly more colour
            self.assertTrue(np.allclose(gl.gs.luma(wow), gl.gs.luma(plain), atol=0.03))           # about the same light


if __name__ == "__main__":
    unittest.main()
