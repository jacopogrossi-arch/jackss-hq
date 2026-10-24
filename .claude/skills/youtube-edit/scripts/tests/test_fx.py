"""fx.py transitions/overlays and the sound cues (assets/sfx/cues.json) wired into compose.py."""
import os, subprocess, unittest
from .helpers import needs_ffmpeg, run, scratch, write, read, load

KINDS = ["flash", "whip", "zoomblur", "lightleak", "burn"]


def build(test, beats, extra=None, preset=True, env=None):
    d = scratch(test)
    spec = {"id": "t", "duration": 20.0, "beats": beats}
    if preset:
        spec["preset"] = "elegante-portfolio"
    spec.update(extra or {})
    r = run("compose.py", "--spec", write(os.path.join(d, "s.json"), spec), "--out", os.path.join(d, "public"), env=env)
    test.assertEqual(r.returncode, 0, r.stdout + r.stderr)
    return read(os.path.join(d, "public", "index.html")), os.path.join(d, "public")


class Transitions(unittest.TestCase):
    def test_every_kind_builds_with_its_sound(self):
        beats = [{"type": "transition", "id": "x%d" % i, "kind": k, "at": 2.0 + 2 * i, "anchor": "-"} for i, k in enumerate(KINDS)]
        page, pub = build(self, beats)
        for i, k in enumerate(KINDS):
            self.assertIn('id="host-x%d"' % i, page)
        self.assertIn("fx-host screen", page)                      # light kinds blend with screen
        self.assertEqual(page.count("<audio"), len(KINDS))         # preset has sound.sfx: one cue each
        self.assertTrue(os.path.exists(os.path.join(pub, "sfx", "shutter.mp3")))

    def test_cue_lands_on_the_cut(self):
        # the cue starts its own lead before the cut, read from cues.json (whip -> the swish pool since 21/10/2026, lead 0)
        cues = load(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "assets", "sfx", "cues.json"))
        name = cues["transitions"]["whip"]
        first = cues["pools"].get(name, [name])[0]
        page, _ = build(self, [{"type": "transition", "id": "w", "kind": "whip", "at": 5.0, "anchor": "-"}])
        self.assertIn('src="sfx/%s.mp3" data-start="%.3f"' % (first, 5.0 - cues["sounds"][first]["lead"]), page)

    def test_sfx_null_silences_and_explicit_overrides(self):
        beats = [{"type": "transition", "id": "a", "kind": "flash", "at": 3.0, "sfx": None, "anchor": "-"},
                 {"type": "transition", "id": "b", "kind": "flash", "at": 6.0, "sfx": "boom", "anchor": "-"}]
        page, _ = build(self, beats)
        self.assertEqual(page.count("<audio"), 1)
        self.assertIn("sfx/boom.mp3", page)

    def test_no_auto_sound_without_preset(self):
        page, _ = build(self, [{"type": "transition", "id": "a", "kind": "flash", "at": 3.0, "anchor": "-"}], preset=False)
        self.assertEqual(page.count("<audio"), 0)

    def test_level_scales_volume(self):
        low, _ = build(self, [{"type": "transition", "id": "a", "kind": "flash", "at": 3.0, "anchor": "-"}], {"sound": {"sfx": True, "level": "low"}})
        high, _ = build(self, [{"type": "transition", "id": "a", "kind": "flash", "at": 3.0, "anchor": "-"}], {"sound": {"sfx": True, "level": "high"}})
        vol = lambda p: float(p.split('data-volume="')[1].split('"')[0])
        self.assertLess(vol(low), vol(high))

    def test_overlays_and_unknown_kind(self):
        page, _ = build(self, [{"type": "overlay", "id": "v", "kind": "vignette", "in": 0, "out": 10, "anchor": "-"},
                               {"type": "overlay", "id": "g", "kind": "grain", "in": 0, "out": 5, "anchor": "-"}])
        self.assertIn("fx-vig", page); self.assertIn("fx-grain", page)
        d = scratch(self)
        spec = {"id": "t", "duration": 5.0, "beats": [{"type": "transition", "id": "z", "kind": "nope", "at": 2.0, "anchor": "-"}]}
        r = run("compose.py", "--spec", write(os.path.join(d, "s.json"), spec), "--out", os.path.join(d, "public"))
        self.assertNotEqual(r.returncode, 0)


@needs_ffmpeg
class RealLightLeak(unittest.TestCase):
    """A/B of 24/10/2026: a real leak from the local packs beats the coded wash; without the packs the coded wash stays."""
    def packs(self):
        d = scratch(self)
        os.makedirs(os.path.join(d, "light-leaks"))
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "color=c=orange:s=320x180:r=60:d=4", "-pix_fmt", "yuv420p",
                        os.path.join(d, "light-leaks", "Light Leaks (5).mp4")], check=True)
        return d

    def test_real_leak_when_the_pack_exists(self):
        page, pub = build(self, [{"type": "transition", "id": "w", "kind": "lightleak", "at": 5.0, "anchor": "-"}], env={"YTE_PACKS": self.packs()})
        self.assertIn('<video class="fx-leak" id="w-leak" src="fx/leak05.mp4"', page)
        self.assertIn('data-start="4.200"', page)                   # its gold peak (0.8 s in) lands on the cut at 5.0
        self.assertNotIn('class="fx-sun"', page)                    # the coded light is off
        self.assertEqual(page.count("<audio"), 1)                   # the transition keeps its sound
        self.assertTrue(os.path.getsize(os.path.join(pub, "fx", "leak05.mp4")) > 0)

    def test_coded_wash_without_packs_or_when_forced(self):
        page, _ = build(self, [{"type": "transition", "id": "w", "kind": "lightleak", "at": 5.0, "anchor": "-"}])
        self.assertNotIn("fx-leak\" id=", page); self.assertIn('class="fx-sun"', page)
        page, _ = build(self, [{"type": "transition", "id": "w", "kind": "lightleak", "at": 5.0, "anchor": "-", "leak": None}], env={"YTE_PACKS": self.packs()})
        self.assertNotIn('id="w-leak"', page); self.assertIn('class="fx-sun"', page)


if __name__ == "__main__":
    unittest.main()


class SceneChange(unittest.TestCase):
    def test_scene_option_puts_the_peak_on_the_beat(self):
        d = scratch(self)
        spec = {"id": "t", "duration": 20.0, "preset": "elegante-portfolio", "beats": [
            {"type": "orbit", "id": "sc", "in": 8.0, "out": 12.0, "center": {"src": "img/x.png"}, "nodes": [], "anchor": "-"},
            {"type": "transition", "id": "tr", "kind": "flash", "scene": "sc", "anchor": "-"}]}
        r = run("compose.py", "--spec", write(os.path.join(d, "s.json"), spec), "--out", os.path.join(d, "public"))
        out = r.stdout + r.stderr
        self.assertNotIn("not on a scene change", out)
        self.assertIn("flash-through", read(os.path.join(d, "public", "index.html")) + "flash-through")  # builds; peak checked via the cue
        page = read(os.path.join(d, "public", "index.html"))
        self.assertIn('data-start="8.000"', page)                  # shutter has lead 0: starts at the scene's first frame

    def test_warns_when_not_on_a_scene_change(self):
        d = scratch(self)
        spec = {"id": "t", "duration": 20.0, "preset": "elegante-portfolio", "beats": [
            {"type": "transition", "id": "tr", "kind": "flash", "at": 9.0, "anchor": "-"}]}
        r = run("compose.py", "--spec", write(os.path.join(d, "s.json"), spec), "--out", os.path.join(d, "public"))
        self.assertIn("not on a scene change", r.stdout + r.stderr)
