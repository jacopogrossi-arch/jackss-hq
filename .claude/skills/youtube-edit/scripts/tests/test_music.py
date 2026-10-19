"""add-music.py: a bed under the voice, video copied, duration kept."""
import os, subprocess, unittest
from .helpers import run, scratch


class AddMusic(unittest.TestCase):
    def test_bed_added_and_duration_kept(self):
        d = scratch(self)
        src, out = os.path.join(d, "in.mp4"), os.path.join(d, "out.mp4")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "color=c=black:s=320x180:d=6:r=30", "-f", "lavfi", "-i", "sine=f=220:d=6",
                        "-c:v", "libx264", "-c:a", "aac", "-shortest", src], check=True)
        r = run("add-music.py", "--video", src, "--out", out, "--track", "lofi-01")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out], capture_output=True, text=True).stdout)
        self.assertAlmostEqual(dur, 6.0, delta=0.3)

    def test_unknown_track_fails(self):
        d = scratch(self)
        r = run("add-music.py", "--video", os.path.join(d, "x.mp4"), "--out", os.path.join(d, "o.mp4"), "--track", "nope")
        self.assertNotEqual(r.returncode, 0)


if __name__ == "__main__":
    unittest.main()
