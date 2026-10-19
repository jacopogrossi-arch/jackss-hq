"""qa-motion.py: frozen stretches, black runs and loudness are measured and gated."""
import os, subprocess, unittest
from .helpers import run, scratch


def make(d, name, vf):
    out = os.path.join(d, name)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", vf, "-f", "lavfi", "-i", "sine=f=220:d=6",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", out], check=True)
    return out


class QaMotion(unittest.TestCase):
    def test_moving_video_passes(self):
        d = scratch(self)
        v = make(d, "move.mp4", "testsrc2=s=320x180:d=6:r=30")
        r = run("qa-motion.py", "--video", v, "--out", os.path.join(d, "qa"))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertTrue(os.path.exists(os.path.join(d, "qa", "sheet.jpg")))

    def test_long_freeze_fails(self):
        d = scratch(self)
        v = make(d, "still.mp4", "color=c=0x336699:s=320x180:d=6:r=30")
        r = run("qa-motion.py", "--video", v, "--out", os.path.join(d, "qa"))
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("FAIL", r.stdout)


if __name__ == "__main__":
    unittest.main()
