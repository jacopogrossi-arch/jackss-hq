"""example-plate-block.py: one block of a plate plan, the shape `scripts/plates-build.py` expects (copy it to <project>/plates/b1.py and rewrite it).

A block is a chapter of the plan in BRIEF.md (about a minute). Every time below is the START of a word in <project>/transcript.json
(`scripts/phrase-times.py --transcript transcript.json "parola"`), never a guess. plates-build.py puts `formats/` on the path, times each plate on
its own elements and lays close plates on one board: the t_in / t_out given to Scene here only need to contain the plate's words.
Rules that decide what goes in a plate: references/plate-plan.md (the job of the plate), taste.md 9-14, prove-corso.md (what Jacopo voted)."""
from scene import Scene


def build():
    out = []

    # row 4 of the plan, 77.2-88.2  "uno strumento che dà una mano alla creatività... non deve sostituire": metaphor
    s = Scene("p4", 77.2, 88.2, title="Uno *strumento*", fade_in=0, fade_out=0)          # ONE key word in the title, between asterisks
    ai = s.disc(420, 600, t=77.51, anchor="strumento", text="AI", r=130)                 # in a real video: logo="img/logos/claude.svg", never the letters
    cr = s.pill(820, 330, "Creatività", t=79.19, anchor="creatività", w=360)             # every element enters on the word that names it
    so = s.pill(820, 640, "Sostituire", t=83.97, anchor="sostituire", kind="bad", w=360)
    s.link(ai, cr, 0); s.link(ai, so, 0)                                                 # a dashed link appears only after both its ends
    s.strike(so, 84.9)                                                                   # what is not needed is struck through, not removed
    out.append(s.build())

    # row 5, 88.2-93.1: a second plate less than 2.5 s after the first -> the same board, a swipe between the two pages
    s = Scene("p5", 88.2, 93.1, title="La *mappa*", fade_in=0, fade_out=0)
    for k, (lab, t) in enumerate((("Idea", 88.45), ("Design", 89.55), ("Prototipo", 90.45))):
        s.pill(300 + k * 420, 480, lab, t=t, anchor=lab.lower(), w=360)
    out.append(s.build())

    # a graphic BESIDE the full-screen face (taste.md 9c: 3-4 per video, on the right, never over the head): bg=False keeps it out of the boards
    g = Scene("g1", 120.0, 126.0, bg=False, fade_in=0.25)
    g.pill(1380, 300, "Tra un *anno*", t=120.4, anchor="anno", w=420)
    out.append(g.build())

    return {"html": "\n".join(o["html"] for o in out), "js": "\n".join(o["js"] for o in out)}
