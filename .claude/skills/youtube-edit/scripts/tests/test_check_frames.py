"""check-frames.py: 10 fps sheets with gaps, one full-size frame, and the auto checks find defects planted on purpose
(a word said twice, a card shown too briefly). A checker that has never failed is a checker you cannot rely on."""
import json, os, subprocess, unittest
from .helpers import needs_ffmpeg, run, scratch, write

INDEX = ('<div id="stage" data-composition-id="t" data-start="0" data-duration="4.000">\n'
         '<div class="card-host clip" id="host-a" data-start="1.000" data-duration="0.300" data-anchor="big number"></div>\n'
         '<div class="card-host clip" id="host-b" data-start="2.000" data-duration="3.000" data-anchor="big number"></div>\n</div>\n')


@needs_ffmpeg
class CheckFrames(unittest.TestCase):
    def video(self, d):
        v = os.path.join(d, "v.mp4")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "testsrc2=s=320x180:d=4:r=30", "-pix_fmt", "yuv420p", v], check=True)
        return v

    def test_sheets_have_gaps_and_planted_defects_are_found(self):
        d = scratch(self)
        v = self.video(d)
        tr = write(os.path.join(d, "t.json"), {"words": [
            {"text": "this", "start": 0.0, "end": 0.2}, {"text": "is", "start": 0.3, "end": 0.4},
            {"text": "really", "start": 1.0, "end": 1.3}, {"text": "really", "start": 1.4, "end": 1.7}, {"text": "good", "start": 1.8, "end": 2.0}]})
        idx = write(os.path.join(d, "index.html"), INDEX)
        out = os.path.join(d, "check")
        r = run("check-frames.py", "--video", v, "--out", out, "--cols", "4", "--rows", "3", "--transcript", tr, "--index", idx)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertTrue(os.path.exists(os.path.join(out, "sheet_01.jpg")))
        self.assertIn('word said twice in a row: 1.0 s "really"', r.stdout)      # planted double word found
        self.assertIn("card at 1.0 s shows only 0.30 s", r.stdout)               # planted flash found
        self.assertNotIn("card at 2.0 s", r.stdout)                              # a card held 3 s is fine
        w = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=width", "-of", "csv=p=0", os.path.join(out, "sheet_01.jpg")],
                           capture_output=True, text=True).stdout.strip()
        self.assertEqual(int(w), 4 * 320 + 3 * 10)                               # 4 tiles + 3 gaps of 10 px: tiles never touch

    def test_single_full_size_frame(self):
        d = scratch(self)
        v = self.video(d)
        out = os.path.join(d, "check")
        r = run("check-frames.py", "--video", v, "--out", out, "--frame", "1.5")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertTrue(os.path.exists(os.path.join(out, "frame_1.5.png")))


if __name__ == "__main__":
    unittest.main()
