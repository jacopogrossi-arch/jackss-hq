"""mix-audio.py --stems + sound-report.py: the stems are written, the master lands at -14 LUFS under -1 dBTP (the limiter's auto
level once pushed it to 0 dBTP), and a planted too-loud effect is flagged."""
import os, subprocess, unittest
from .helpers import needs_ffmpeg, read, run, scratch, write


def ff(*a):
    subprocess.run(["ffmpeg", "-y", "-v", "error", *a], check=True)


@needs_ffmpeg
class SoundReport(unittest.TestCase):
    def test_report_and_planted_loud_effect(self):
        d = scratch(self); pub = os.path.join(d, "public"); os.makedirs(os.path.join(pub, "sfx"))
        # "voice": a 220 Hz tone pulsing like speech, on a small video
        ff("-f", "lavfi", "-i", "color=c=black:s=160x90:r=30:d=10", "-f", "lavfi", "-i", "sine=f=220:d=10,volume='0.5*gt(sin(2*PI*t*0.7),-0.3)':eval=frame",
           "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", os.path.join(pub, "input-video.mp4"))
        ff("-f", "lavfi", "-i", "sine=f=1200:d=0.4", os.path.join(pub, "sfx", "tick.mp3"))
        ff("-f", "lavfi", "-i", "sine=f=90:d=10", "-ar", "48000", os.path.join(d, "bed.wav"))
        write(os.path.join(pub, "index.html"), '<div id="stage">\n'
              '<audio id="a1" src="sfx/tick.mp3" data-start="2.000" data-duration="0.4" data-volume="0.05"></audio>\n'
              '<audio id="a2" src="sfx/tick.mp3" data-start="6.000" data-duration="0.4" data-volume="1.0"></audio>\n</div>\n')
        stems, final = os.path.join(d, "stems"), os.path.join(d, "final.mp4")
        r = run("mix-audio.py", "--index", os.path.join(pub, "index.html"), "--voice", os.path.join(pub, "input-video.mp4"),
                "--video", os.path.join(pub, "input-video.mp4"), "--out", final, "--music", os.path.join(d, "bed.wav"), "--music-db", "-7", "--stems", stems)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        for n in ("voice", "fx", "music"):
            self.assertTrue(os.path.getsize(os.path.join(stems, n + ".wav")) > 1000, n)
        out = os.path.join(d, "SOUND-REPORT.md")
        r = run("sound-report.py", "--stems", stems, "--index", os.path.join(pub, "index.html"), "--final", final, "--out", out)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        rep = read(out)
        self.assertIn("effect at 6.00 s (tick.mp3)", rep)           # the planted loud effect is flagged
        self.assertIn("too loud", rep)
        self.assertNotIn("master true peak", rep)                  # the limiter keeps the master under -1 dBTP
        self.assertNotIn("master at", rep)                         # and at -14 LUFS


if __name__ == "__main__":
    unittest.main()
