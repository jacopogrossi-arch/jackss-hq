"""grade-film.py and its users (27/10/2026): the shoulder never passes white, the highlight stretch lands a clip's white on
target without moving skin, the warm split tone leaves the sea alone, the finish graph runs, a film look renders and the file
matches the preview; grade-match moves clips towards each other within limits; grade-ref writes a look and a sheet."""
import importlib.util, json, os, subprocess, unittest
import numpy as np
from .helpers import needs_ffmpeg, run, scratch, SCRIPTS


def load():
    spec = importlib.util.spec_from_file_location("grade_film", os.path.join(SCRIPTS, "grade-film.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def flat(c, n=8):
    a = np.zeros((n, n, 3), np.float32)
    a[:] = c
    return a


class GradeFilm(unittest.TestCase):
    def setUp(self):
        self.gf = load()
        self.look = self.gf.gs.CFG["looks"]["pellicola-oro"]["p"]

    def test_shoulder_is_smooth_and_never_reaches_white(self):
        d = np.linspace(-6, 12, 2000)
        out = self.gf.shoulder(d, 1.5)
        self.assertTrue((np.diff(out) >= 0).all())
        self.assertLess(out.max(), self.gf.WHITE_STOPS)
        self.assertTrue(np.allclose(out[d < 1.5], d[d < 1.5]))

    def test_stretch_lands_the_clip_white_on_target_and_leaves_skin(self):
        f = self.gf.film_params(self.look)
        white = 0.75                                                  # a dim clip: brightest highlights at 0.75 linear (86 % on screen)
        out = self.gf.tone(flat(white ** (1 / 2.4)), self.look, 0.0, None, white)
        self.assertAlmostEqual(float(out[0, 0, 1]), f["white_target"], delta=0.02)
        self.assertLessEqual(self.gf.stretch_for(0.3, f), f["stretch_max"] + 1e-6)   # a very dim clip: the stretch stops at its limit
        skin = flat((0.62, 0.45, 0.36))                              # a face around 40 IRE: below stretch_from
        a = self.gf.tone(skin, self.look, 0.0, None, white)
        b = self.gf.tone(skin, self.look, 0.0, None, None)
        self.assertTrue(np.allclose(a, b, atol=1e-4))

    def test_nothing_clips_even_with_a_big_push(self):
        px = np.random.default_rng(3).random((32, 32, 3)).astype(np.float32)
        out = self.gf.apply(px, self.look, 1.5, [1.05, 0.95], 0.9)
        self.assertTrue(np.isfinite(out).all() and out.min() >= 0 and out.max() <= 1)

    def test_warm_split_tone_leaves_the_sea_alone(self):
        sea = flat((0.25, 0.75, 0.70))
        sand = flat((0.85, 0.80, 0.72))
        look = {"film": {"warm": [[0.05, 0.02, -0.05], [0, 0, 0]]}}
        plain = {"film": {}}
        ds = np.abs(self.gf.colour(sea, look) - self.gf.colour(sea, plain)).max()
        dd = self.gf.colour(sand, look)[0, 0] - self.gf.colour(sand, plain)[0, 0]
        self.assertLess(ds, 0.01)
        self.assertGreater(dd[0], 0.02)
        self.assertLess(dd[2], -0.02)

    def test_saturation_per_hue_touches_only_its_hue(self):
        red, sea = flat((0.7, 0.25, 0.28)), flat((0.25, 0.70, 0.68))
        look = {"film": {"sat_hue": [[355, 25, 1.3]]}}
        plain = {"film": {}}
        def chroma(a):
            return float(a.max(-1).mean() - a.min(-1).mean())
        self.assertGreater(chroma(self.gf.colour(red, look)), chroma(self.gf.colour(red, plain)) * 1.15)
        self.assertAlmostEqual(chroma(self.gf.colour(sea, look)), chroma(self.gf.colour(sea, plain)), delta=0.005)

    def test_bake_with_the_dji_lut_equals_lut_then_grade(self):
        d = scratch(self)
        lut_path = os.path.join(self.gf.gs.LUTS, "DJI-OsmoNano-DLogM-to-Rec709-V1.cube")
        lut = self.gf.gs.load_cube(lut_path)
        self.gf.bake(self.look, os.path.join(d, "f.cube"), 0.2, None, 0.6, n=33, pre=lut)
        table = self.gf.gs.load_cube(os.path.join(d, "f.cube"))
        px = np.random.default_rng(5).random((16, 16, 3)).astype(np.float32)
        direct = self.gf.apply(self.gf.gs.apply_lut(px, lut), self.look, 0.2, None, 0.6)
        self.assertLess(float(np.abs(self.gf.gs.apply_lut(px, table) - direct).mean()), 0.01)

    @needs_ffmpeg
    def test_finish_graph_runs_and_changes_the_picture(self):
        img = flat((0.5, 0.5, 0.5), 64)
        img[20:30, 20:30] = 1.0                                       # a bright spot for the glow
        out = self.gf.finish_image(img, self.look)
        self.assertEqual(out.shape, img.shape)
        self.assertGreater(float(np.abs(out - img).mean()), 0.003)    # grain / vignette / glow did something
        self.assertLess(float(out[0, 0].mean()), float(out[32, 32].mean()) + 0.02)   # corners not brighter than the centre

    @needs_ffmpeg
    def test_graduated_sky_darkens_the_bright_top_only(self):
        img = flat((0.8, 0.8, 0.8), 90)
        img[:, 45:] = 0.2
        out = self.gf.finish_image(img, {"finish": {"sky_grad": 0.3}})
        self.assertLess(float(out[2, :45].mean()), 0.7)               # bright sky at the top: darker
        self.assertAlmostEqual(float(out[85, :45].mean()), 0.8, delta=0.02)   # bottom half untouched
        self.assertAlmostEqual(float(out[2, 45:].mean()), 0.2, delta=0.03)    # dark things at the top barely move


@needs_ffmpeg
class FilmScripts(unittest.TestCase):
    def clip(self, d, name="c.mp4", vf="eq=saturation=0.4,colorlevels=rimax=0.8:gimax=0.8:bimax=0.8"):
        v = os.path.join(d, name)
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "testsrc2=s=320x180:d=2:r=25", "-vf", vf,
                        "-pix_fmt", "yuv420p10le", "-c:v", "libx265", "-x265-params", "log-level=error", v], check=True)
        return v

    def scan(self, d, v, tag):
        out = os.path.join(d, "scan-" + tag)
        r = run("grade-scan.py", "--video", v, "--out", out, "--samples", "3", "--profile", "dlogm")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        return os.path.join(out, "report.json")

    def test_film_look_renders_and_matches_the_preview(self):
        d = scratch(self)
        v = self.clip(d)
        rep = self.scan(d, v, "a")
        out = os.path.join(d, "a")
        r = run("grade-apply.py", "--video", v, "--scan", rep, "--out", out, "--frames", "2", "--render", "--encoder", "x265", "--stops", "0", "--look", "pellicola-oro")
        self.assertIn("Film look: clip white", r.stdout, r.stdout + r.stderr)
        self.assertIn("PASS the file matches the preview's prediction", r.stdout, r.stdout + r.stderr)

    def test_match_moves_clips_towards_each_other_within_limits(self):
        d = scratch(self)
        a = self.clip(d, "a.mp4")
        b = self.clip(d, "b.mp4", "eq=saturation=0.4,colorlevels=rimax=0.8:gimax=0.8:bimax=0.8,eq=brightness=-0.08")
        out = os.path.join(d, "m")
        r = run("grade-match.py", "--clip", a + "=" + self.scan(d, a, "a"), "--clip", b + "=" + self.scan(d, b, "b"), "--out", out, "--look", "pellicola-oro")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        m = json.load(open(os.path.join(out, "match.json"), encoding="utf8"))["clips"]
        for c in m.values():
            rep = json.load(open(c["scan"], encoding="utf8"))
            self.assertLessEqual(abs(c["stops"] - rep["proposal"]["exposure_stops"]), 0.3 + 1e-6)
            if c["wb_gains"]:
                self.assertLessEqual(max(abs(g - 1) for g in c["wb_gains"]), 0.03 + 1e-6)
        self.assertTrue(os.path.exists(os.path.join(out, "match-sheet.png")))
        r2 = run("grade-apply.py", "--video", b, "--scan", m["b.mp4"]["scan"], "--out", os.path.join(d, "ab"), "--frames", "1", "--match", os.path.join(out, "match.json"))
        self.assertIn("the shot matching", r2.stdout, r2.stdout + r2.stderr)

    def test_ref_writes_a_film_look_and_a_sheet(self):
        d = scratch(self)
        v = self.clip(d)
        ref = os.path.join(d, "ref.png")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "testsrc2=s=480x270", "-frames:v", "1", "-vf", "colorbalance=rh=0.15:bh=-0.15", ref], check=True)
        out = os.path.join(d, "r")
        r = run("grade-ref.py", "--ref", ref, "--video", v, "--scan", self.scan(d, v, "r"), "--out", out)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        lk = json.load(open(os.path.join(out, "look.json"), encoding="utf8"))["p"]
        self.assertIn("film", lk)
        self.assertTrue(os.path.exists(os.path.join(out, "ref-sheet.png")))


if __name__ == "__main__":
    unittest.main()
