"""grade-scan.py: measures a log clip and proposes a correction. Checks that it flags a planted defect (a burnt clip),
stays quiet on a mid-grey clip, and never calls a profile certain when the file carries no camera or profile."""
import json, os, subprocess, unittest
from .helpers import needs_ffmpeg, run, scratch


@needs_ffmpeg
class GradeScan(unittest.TestCase):
    def clip(self, d, name, colour):
        v = os.path.join(d, name)
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "color=c=%s:s=320x180:d=3:r=30" % colour,
                        "-pix_fmt", "yuv420p10le", "-c:v", "libx265", "-x265-params", "log-level=error", v], check=True)
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


if __name__ == "__main__":
    unittest.main()
