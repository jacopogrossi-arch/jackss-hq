"""fx.py transitions/overlays and the sound cues (assets/sfx/cues.json) wired into compose.py."""
import os, unittest
from .helpers import run, scratch, write, read, load

KINDS = ["flash", "whip", "zoomblur", "lightleak", "burn"]


def build(test, beats, extra=None, preset=True):
    d = scratch(test)
    spec = {"id": "t", "duration": 20.0, "beats": beats}
    if preset:
        spec["preset"] = "elegante-portfolio"
    spec.update(extra or {})
    r = run("compose.py", "--spec", write(os.path.join(d, "s.json"), spec), "--out", os.path.join(d, "public"))
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
        page, _ = build(self, [{"type": "transition", "id": "w", "kind": "whip", "at": 5.0, "anchor": "-"}])
        self.assertIn('data-start="4.820"', page)                  # whoosh-fast leads by 0.18 s

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


if __name__ == "__main__":
    unittest.main()
