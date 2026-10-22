"""ab-compare.py: both versions end up as 1/2 in some order, the key names them, the side-by-side and sequence files exist."""
import os, subprocess, unittest
from .helpers import needs_ffmpeg, read, run, scratch


def clip(d, name, colour):
    path = os.path.join(d, name)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "color=c=%s:s=320x180:r=30:d=2" % colour, "-f", "lavfi", "-i",
                    "sine=f=330:d=2", "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", path], check=True)
    return path


@needs_ffmpeg
class AbCompare(unittest.TestCase):
    def test_blind_pair_and_key(self):
        d = scratch(self)
        cur, new = clip(d, "current.mp4", "red"), clip(d, "candidate.mp4", "blue")
        out = os.path.join(d, "ab")
        r = run("ab-compare.py", "--a", cur, "--b", new, "--out", out, "--labels", "current,new", "--seed", "3")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        for f in ("1.mp4", "2.mp4", "side-by-side.mp4", "in-sequence.mp4", "KEY.md"):
            self.assertTrue(os.path.exists(os.path.join(out, f)), f)
        key = read(os.path.join(out, "KEY.md"))
        self.assertIn("current", key); self.assertIn("new", key)
        self.assertNotIn("current", r.stdout.split("KEY.md")[0])     # the console line never says which is which
        sizes = {os.path.getsize(os.path.join(out, f)) for f in ("1.mp4", "2.mp4")}
        self.assertEqual(sizes, {os.path.getsize(cur), os.path.getsize(new)})   # both versions are there, unchanged


if __name__ == "__main__":
    unittest.main()
