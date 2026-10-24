"""grade-scan.py: measures a log clip and proposes a correction. Checks that it flags a planted defect (a burnt clip),
stays quiet on a mid-grey clip, and never calls a profile certain when the file carries no camera or profile."""
import json, os, subprocess, unittest
from .helpers import needs_ffmpeg, run, scratch


@needs_ffmpeg
class GradeScan(unittest.TestCase):
    def clip(self, d, name, colour, gamma=None):
        v = os.path.join(d, name)
        meta = ["-movflags", "use_metadata_tags", "-metadata", "com.dji.camera.ColorGammaSxS=%s" % gamma] if gamma else []
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "color=c=%s:s=320x180:d=3:r=30" % colour,
                        "-pix_fmt", "yuv420p10le", "-c:v", "libx265", "-x265-params", "log-level=error"] + meta + [v], check=True)
        return v

    def scan(self, d, v, *extra):
        out = os.path.join(d, "scan-" + os.path.basename(v))
        r = run("grade-scan.py", "--video", v, "--out", out, "--samples", "3", *extra)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        with open(os.path.join(out, "report.json")) as f:
            return json.load(f), out

    def test_planted_burnt_clip_is_flagged(self):
        d = scratch(self)
        rep, out = self.scan(d, self.clip(d, "burnt.mp4", "white"), "--profile", "dlogm")
        self.assertGreater(rep["graded"]["clip"]["mean"], 0.5)
        self.assertTrue(any("clipped" in x or "zebra" in x for x in rep["flags"]), rep["flags"])
        self.assertTrue(os.path.exists(os.path.join(out, "scopes-sheet.png")))
        self.assertTrue(os.path.exists(os.path.join(out, "REPORT.md")))

    def test_mid_grey_clip_has_no_zebra_and_a_proposal(self):
        d = scratch(self)
        rep, _ = self.scan(d, self.clip(d, "grey.mp4", "0x606060"), "--profile", "dlogm")
        self.assertLess(rep["graded"]["zebra95"]["mean"], 0.01)
        self.assertFalse(any("zebra" in x for x in rep["flags"]), rep["flags"])
        self.assertLessEqual(abs(rep["proposal"]["exposure_stops"]), 1.5)

    def test_profile_is_not_certain_without_metadata(self):
        d = scratch(self)
        rep, _ = self.scan(d, self.clip(d, "plain.mp4", "0x606060"))
        self.assertFalse(rep["profile"]["certain"])
        self.assertEqual(len(rep["profile"]["scores"]), 3)        # every candidate LUT was tried

    def test_given_profile_is_certain(self):
        d = scratch(self)
        rep, _ = self.scan(d, self.clip(d, "given.mp4", "0x606060"), "--profile", "dlog2")
        self.assertTrue(rep["profile"]["certain"])
        self.assertEqual(rep["profile"]["chosen"], "dlog2")

    def test_profile_is_read_from_the_dji_tag(self):
        d = scratch(self)
        for gamma, key in (("D-Log", "dlog"), ("D-Log2", "dlog2"), ("D-LogM", "dlogm")):
            rep, _ = self.scan(d, self.clip(d, "t-%s.mp4" % key, "0x606060", gamma))
            self.assertTrue(rep["profile"]["certain"], gamma)
            self.assertEqual(rep["profile"]["chosen"], key, gamma)

    def test_skin_pixels_are_found_and_anchor_the_proposal(self):
        import importlib.util
        import numpy as np
        spec = importlib.util.spec_from_file_location("grade_scan", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "grade-scan.py"))
        gs = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(gs)
        skin = np.zeros((90, 160, 3), np.float32)
        skin[:] = (0.78, 0.59, 0.47)                      # a skin colour, on the graded signal
        st = gs.frame_stats(skin)
        self.assertGreater(st["skin_frac"], 0.9)
        blue = np.zeros((90, 160, 3), np.float32)
        blue[:] = (0.3, 0.5, 0.8)                         # sky: never skin
        self.assertLess(gs.frame_stats(blue)["skin_frac"], 0.01)
        p = gs.propose([st, st, st])
        self.assertEqual(p["exposure_anchor"], "skin")

    def test_preset_names_real_luts_and_drives_the_thresholds(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location("grade_scan", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "grade-scan.py"))
        gs = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(gs)
        for key, (label, fname) in gs.PROFILES.items():
            self.assertTrue(os.path.exists(os.path.join(gs.LUTS, fname)), "%s: LUT %s missing" % (key, fname))
        self.assertEqual(sorted(gs.PROFILES), ["dlog", "dlog2", "dlogm"])
        cfg = gs.load_cfg("no-such-preset")                   # a missing preset falls back to the built-in values
        self.assertEqual(cfg["skin_band"], [0.50, 0.68])
        self.assertEqual(gs.CFG["skin_target"], 0.60)

    def load_gs(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location("grade_scan", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "grade-scan.py"))
        gs = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(gs)
        return gs

    def test_white_balance_uses_only_near_neutral_pixels(self):
        import numpy as np
        gs = self.load_gs()
        warm = np.zeros((90, 160, 3), np.float32)
        warm[:] = (0.66, 0.60, 0.54)                       # a grey wall under a warm light: a real cast
        gains, frac = gs.wb_estimate(warm)
        self.assertIsNone(gains)                           # (0.66,0.6,0.54) has chroma above the neutral limit: a coloured wall, not a neutral one
        grey = np.zeros((90, 160, 3), np.float32)
        grey[:] = (0.61, 0.60, 0.585)                      # nearly neutral, a slight warm lean
        gains, frac = gs.wb_estimate(grey)
        self.assertGreater(frac, 0.9)
        self.assertLess(gains[0], 1.0)                      # too much red -> red is pulled down
        self.assertGreater(gains[1], 1.0)                   # too little blue -> blue is pushed up
        sea = np.zeros((90, 160, 3), np.float32)
        sea[:] = (0.35, 0.65, 0.62)                         # a lagoon: coloured on purpose, never "corrected"
        gains, frac = gs.wb_estimate(sea)
        self.assertIsNone(gains)
        self.assertLess(frac, 0.01)


if __name__ == "__main__":
    unittest.main()
