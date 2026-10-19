"""subtitle-chunks.py and the `subtitles` format: phrase-level subtitles from a word-level transcript."""
import json, os, unittest
from .helpers import run, scratch, write, read, load

WORDS = [  # (text, start, end)
    ("Questa", 0.0, 0.3), ("e", 0.35, 0.4), ("la", 0.45, 0.5), ("palette", 0.55, 1.0), ("colori.", 1.05, 1.5),
    ("Poi,", 2.5, 2.8), ("per", 2.85, 3.0), ("quanto", 3.05, 3.3), ("riguarda", 3.35, 3.8), ("l'impaginazione,", 3.85, 4.6),
    ("e", 4.65, 4.7), ("stata", 4.75, 5.0), ("utilizzata", 5.05, 5.6), ("sempre", 5.65, 6.0), ("Claud.", 6.05, 6.5),
]


def transcript(d):
    return write(os.path.join(d, "transcript.json"), {"words": [{"text": t, "start": s, "end": e} for t, s, e in WORDS]})


class SubtitleChunks(unittest.TestCase):
    def chunks(self, *extra):
        d = scratch(self)
        out = os.path.join(d, "subs.json")
        r = run("subtitle-chunks.py", "--transcript", transcript(d), "--out", out, *extra)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        return load(out)["chunks"], d

    def test_breaks_on_sentence_end_and_pause(self):
        ch, _ = self.chunks()
        self.assertEqual(ch[0]["text"], "Questa e la palette colori.")     # sentence end
        self.assertTrue(ch[1]["text"].startswith("Poi, per quanto"))        # a 1 s pause before it

    def test_timing_never_overlaps_and_lead_tail(self):
        ch, _ = self.chunks()
        self.assertAlmostEqual(ch[0]["at"], 0.0)                            # lead clamped at 0
        for a, b in zip(ch, ch[1:]):
            self.assertLessEqual(a["end"], b["at"])

    def test_long_chunk_is_two_balanced_lines(self):
        ch, _ = self.chunks("--max-chars", "120")
        long = [c for c in ch if len(c["text"]) > 40]
        self.assertTrue(long)
        for c in long:
            self.assertEqual(len(c["lines"]), 2)
            self.assertLess(abs(len(c["lines"][0]) - len(c["lines"][1])), 18)

    def test_keywords_and_name_fix(self):
        ch, _ = self.chunks("--em", "palette", "--fix", "Claud=Claude")
        self.assertIn(3, ch[0]["em"])                                       # "palette" is word 3 of the first chunk
        self.assertTrue(any("Claude." in c["text"] for c in ch))             # fixed, trailing dot kept
        self.assertFalse(any("Claud." in c["text"] for c in ch))

    def test_auto_em_picks_one_long_content_word(self):
        ch, _ = self.chunks("--auto-em")
        for c in ch:
            self.assertLessEqual(len(c["em"]), 1)
        self.assertTrue(any(c["em"] for c in ch))


class SubtitlesFormat(unittest.TestCase):
    def test_builds_with_preset_and_em_words(self):
        d = scratch(self)
        subs = os.path.join(d, "subs.json")
        r = run("subtitle-chunks.py", "--transcript", transcript(d), "--out", subs, "--em", "palette")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        spec = {"id": "t", "duration": 8.0, "preset": "elegante-portfolio", "subtitles": "both",
                "beats": [{"type": "subtitles", "id": "sb", "in": 0.0, "out": 8.0, "anchor": "-", "chunks": load(subs)["chunks"]},
                          {"type": "line", "id": "l1", "text": "hello there", "em": [1], "color": "cyan", "in": 1.0, "out": 3.0, "anchor": "-"}]}
        sp = write(os.path.join(d, "storyboard.json"), spec)
        r = run("compose.py", "--spec", sp, "--out", os.path.join(d, "public"))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        page = read(os.path.join(d, "public", "index.html"))
        self.assertIn('class="k-sub"', page)
        self.assertIn('<span class="em">palette</span>', page)
        self.assertNotIn("!important", page.split("</style>")[0].split(".k-sub-grad")[-1])   # nothing is shoved aside any more


if __name__ == "__main__":
    unittest.main()


class SubtitlesStepAside(unittest.TestCase):
    def build(self, line_in, line_out):
        d = scratch(self)
        chunks = [{"text": "one two three", "lines": ["one two three"], "at": 1.0, "end": 2.0, "em": []},
                  {"text": "four five six", "lines": ["four five six"], "at": 4.0, "end": 6.0, "em": []},
                  {"text": "seven eight", "lines": ["seven eight"], "at": 8.0, "end": 9.0, "em": []}]
        spec = {"id": "t", "duration": 10.0, "beats": [{"type": "subtitles", "id": "sb", "in": 0.0, "out": 10.0, "anchor": "-", "chunks": chunks},
                                                       {"type": "line", "id": "l1", "text": "hello there", "em": [1], "color": "cyan", "in": line_in, "out": line_out, "anchor": "-"}]}
        r = run("compose.py", "--spec", write(os.path.join(d, "s.json"), spec), "--out", os.path.join(d, "public"))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        return read(os.path.join(d, "public", "index.html"))

    def test_chunk_inside_a_line_window_is_dropped(self):
        page = self.build(3.5, 6.5)
        self.assertNotIn("four five six", page)
        self.assertIn("one two three", page); self.assertIn("seven eight", page)

    def test_chunk_outside_stays(self):
        page = self.build(9.2, 9.9)
        self.assertIn("four five six", page)


class SubtitlesMode(unittest.TestCase):
    def test_keywords_mode_drops_phrase_subtitles(self):
        d = scratch(self)
        chunks = [{"text": "one two three", "lines": ["one two three"], "at": 1.0, "end": 2.0, "em": []}]
        spec = {"id": "t", "duration": 5.0, "subtitles": "keywords",
                "beats": [{"type": "subtitles", "id": "sb", "in": 0.0, "out": 5.0, "anchor": "-", "chunks": chunks},
                          {"type": "line", "id": "l1", "text": "hello there", "em": [1], "color": "cyan", "in": 3.0, "out": 4.5, "anchor": "-"}]}
        r = run("compose.py", "--spec", write(os.path.join(d, "s.json"), spec), "--out", os.path.join(d, "public"))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        page = read(os.path.join(d, "public", "index.html"))
        self.assertNotIn("one two three", page)
        self.assertIn("hello there", page)
