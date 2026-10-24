"""grade-apply.py: the preview writes no video; a render is read back and checked against the preview's own prediction;
an uncertain profile is refused. A clip with the exposure pushed past the highlights must FAIL the check."""
import json, os, subprocess, unittest
from .helpers import needs_ffmpeg, run, scratch


@needs_ffmpeg
class GradeApply(unittest.TestCase):
    def clip(self, d, bright=False):
        v = os.path.join(d, "c.mp4")
        vf = "eq=saturation=0.4,colorlevels=rimax=0.8:gimax=0.8:bimax=0.8" + (",eq=brightness=0.25" if bright else "")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "testsrc2=s=320x180:d=2:r=25", "-vf", vf,
                        "-pix_fmt", "yuv420p10le", "-c:v", "libx265", "-x265-params", "log-level=error", v], check=True)
        return v

    def scan(self, d, v, *extra):
        out = os.path.join(d, "scan")
        r = run("grade-scan.py", "--video", v, "--out", out, "--samples", "3", *extra)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        return os.path.join(out, "report.json")

    def test_preview_writes_no_video(self):
        d = scratch(self)
        v = self.clip(d)
        rep = self.scan(d, v, "--profile", "dlogm")
        out = os.path.join(d, "apply")
        r = run("grade-apply.py", "--video", v, "--scan", rep, "--out", out, "--frames", "2")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertTrue(os.path.exists(os.path.join(out, "preview-sheet.png")))
        self.assertFalse(os.path.exists(os.path.join(out, "graded.mp4")))

    def test_uncertain_profile_is_refused(self):
        d = scratch(self)
        v = self.clip(d)
        rep = self.scan(d, v)                                  # no tag, no --profile: not certain
        r = run("grade-apply.py", "--video", v, "--scan", rep, "--out", os.path.join(d, "apply"))
        self.assertEqual(r.returncode, 1)
        self.assertIn("NOT certain", r.stdout)

    def test_render_is_checked_against_the_prediction(self):
        d = scratch(self)
        v = self.clip(d)
        rep = self.scan(d, v, "--profile", "dlogm")
        out = os.path.join(d, "apply")
        r = run("grade-apply.py", "--video", v, "--scan", rep, "--out", out, "--frames", "2", "--render", "--encoder", "x265", "--stops", "0.3")
        self.assertIn("matches the preview's prediction", r.stdout, r.stdout + r.stderr)
        self.assertTrue(os.path.exists(os.path.join(out, "graded.mp4")))
        self.assertTrue(os.path.exists(os.path.join(out, "CHECK.md")))

    def test_planted_overexposure_fails_the_check(self):
        d = scratch(self)
        v = self.clip(d, bright=True)
        rep = self.scan(d, v, "--profile", "dlogm")
        out = os.path.join(d, "apply")
        r = run("grade-apply.py", "--video", v, "--scan", rep, "--out", out, "--frames", "2", "--render", "--encoder", "x265", "--stops", "2")
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("FAIL clipped highlights", r.stdout)

    def test_absurd_exposure_is_refused(self):
        d = scratch(self)
        v = self.clip(d)
        rep = self.scan(d, v, "--profile", "dlogm")
        r = run("grade-apply.py", "--video", v, "--scan", rep, "--out", os.path.join(d, "apply"), "--stops", "4")
        self.assertEqual(r.returncode, 1)
        self.assertIn("out of range", r.stdout)

    def test_white_balance_gains_are_checked_and_applied(self):
        d = scratch(self)
        v = self.clip(d)
        rep = self.scan(d, v, "--profile", "dlogm")
        bad = run("grade-apply.py", "--video", v, "--scan", rep, "--out", os.path.join(d, "a1"), "--wb-gains", "1.5,0.7")
        self.assertEqual(bad.returncode, 1)
        self.assertIn("out of range", bad.stdout)
        junk = run("grade-apply.py", "--video", v, "--scan", rep, "--out", os.path.join(d, "a2"), "--wb-gains", "red")
        self.assertEqual(junk.returncode, 1)
        out = os.path.join(d, "a3")
        r = run("grade-apply.py", "--video", v, "--scan", rep, "--out", out, "--frames", "2", "--render", "--encoder", "x265", "--stops", "0", "--wb-gains", "1.05,0.95")
        self.assertIn("white balance: R x1.050, B x0.950", r.stdout, r.stdout + r.stderr)
        self.assertIn("matches the preview's prediction", r.stdout)          # the file has the colour shift the preview predicted
        self.assertNotIn("FAIL the file matches", r.stdout)

    def test_unknown_look_is_refused(self):
        d = scratch(self)
        v = self.clip(d)
        rep = self.scan(d, v, "--profile", "dlogm")
        r = run("grade-apply.py", "--video", v, "--scan", rep, "--out", os.path.join(d, "a"), "--look", "no-such-look")
        self.assertEqual(r.returncode, 1)
        self.assertIn("unknown look", r.stdout)

    def test_render_with_a_look_matches_the_prediction(self):
        d = scratch(self)
        v = self.clip(d)
        rep = self.scan(d, v, "--profile", "dlogm")
        out = os.path.join(d, "a")
        r = run("grade-apply.py", "--video", v, "--scan", rep, "--out", out, "--frames", "2", "--render", "--encoder", "x265", "--stops", "0", "--look", "blockbuster")
        self.assertIn("look: blockbuster", r.stdout, r.stdout + r.stderr)
        self.assertIn("PASS the file matches the preview's prediction", r.stdout, r.stdout + r.stderr)   # the baked 3D table does what the numpy look does
        self.assertIn("look blockbuster", open(os.path.join(out, "CHECK.md"), encoding="utf8").read())


if __name__ == "__main__":
    unittest.main()
