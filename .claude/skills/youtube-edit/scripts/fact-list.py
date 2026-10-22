#!/usr/bin/env python3
"""fact-list.py: the sentences of a transcript that state something checkable, so Jacopo confirms them at Checkpoint A.

AI will happily invent a fact that sounds right (a number, a date, what a tool can do). This script never fixes anything and never
says a claim is true: it lists, by time, every sentence that holds a number, a year, a date, a price or percentage, or a named
tool, and writes FACTS.md. Jacopo answers each line (ok / wrong: say what is right / cut). A line that cannot be proven is cut from
the video, not softened. Run it on the RAW transcript (before the cut), so a wrong fact is removed with the retakes.

Usage: python3 fact-list.py --transcript W/transcript-raw.json --out W/FACTS.md [--tools "Claude,Canva,..."] [--gap 0.8]
Exit code 0 always (it lists, it does not gate).
"""
import argparse, json, re, sys

DEFAULT_TOOLS = ("Claude,ChatGPT,GPT,Gemini,Canva,Notion,Midjourney,Magnific,Higgsfield,Kling,Seedance,Veo,Procreate,CapCut,"
                 "Pinterest,Chrome,MCP,Opus,Sonnet,Haiku,HyperFrames,Photoshop,Figma,Instagram,TikTok,YouTube,Shopify").split(",")
MONTHS = ("gennaio febbraio marzo aprile maggio giugno luglio agosto settembre ottobre novembre dicembre "
          "january february march april may june july august september october november december").split()
NUMBER_WORDS = ("due tre quattro cinque sei sette otto nove dieci venti trenta quaranta cinquanta cento mille milione milioni miliardo miliardi "
                "two three four five six seven eight nine ten twenty thirty forty fifty hundred thousand million billion").split()
MONEY = re.compile(r"[$€£]|\b(euro|dollari|dollar|dollars|eur|usd)\b", re.I)
# "uno" and "one" are left out on purpose: they are mostly an article or a pronoun, and flood the list
PERCENT = re.compile(r"%|\bper cento\b|\bpercent\b", re.I)

ap = argparse.ArgumentParser()
ap.add_argument("--transcript", required=True); ap.add_argument("--out", required=True)
ap.add_argument("--tools", default=",".join(DEFAULT_TOOLS)); ap.add_argument("--gap", type=float, default=0.8,
                help="a pause this long (s) also ends a sentence when the transcript has no punctuation")
a = ap.parse_args()
raw = json.load(open(a.transcript, encoding="utf-8"))
words = raw["words"] if isinstance(raw, dict) and "words" in raw else raw
words = [w for w in words if w.get("text")]
tools = [t.strip() for t in a.tools.split(",") if t.strip()]

sentences, cur = [], []
for i, w in enumerate(words):
    cur.append(w)
    nxt = words[i + 1] if i + 1 < len(words) else None
    if re.search(r"[.?!]$", w["text"].strip()) or nxt is None or float(nxt["start"]) - float(w["end"]) >= a.gap:
        sentences.append(cur); cur = []


def tc(t):
    t = int(t)
    return "%d:%02d" % (t // 60, t % 60)


rows = []
for s in sentences:
    text = " ".join(w["text"] for w in s)
    low = re.sub(r"[^\w%$€£' ]", " ", text.lower()).split()
    why = []
    if re.search(r"\d", text):
        why.append("number")
    if any(t in NUMBER_WORDS for t in low):
        why.append("number (in words)")
    if re.search(r"\b(19|20)\d\d\b", text):
        why.append("year")
    if any(m in low for m in MONTHS):
        why.append("date")
    if MONEY.search(text):
        why.append("price")
    if PERCENT.search(text):
        why.append("percentage")
    hit = [t for t in tools if re.search(r"\b%s\b" % re.escape(t), text, re.I)]
    if hit:
        why.append("tool: " + ", ".join(hit))
    if why:
        rows.append((float(s[0]["start"]), text, why))

hard = [r for r in rows if any(not w.startswith("tool") for w in r[2])]
soft = [r for r in rows if all(w.startswith("tool") for w in r[2])]
L = ["# Facts to confirm (Checkpoint A)", "",
     "Answer each line: **ok**, **wrong** (say what is right) or **cut**. A claim that cannot be proven is cut, never softened.",
     "Nothing here has been checked: this is only what the transcript says.", "",
     "## Numbers, dates, prices (%d)" % len(hard), ""]
L += ["- [ ] %s  \"%s\"  _(%s)_" % (tc(t), x, ", ".join(w)) for t, x, w in hard] or ["- none found"]
L += ["", "## What a tool can do (%d)" % len(soft), "",
      "Only the sentences that name a tool and nothing else checkable; confirm the ones that claim what it does or how it works.", ""]
L += ["- [ ] %s  \"%s\"  _(%s)_" % (tc(t), x, ", ".join(w)) for t, x, w in soft] or ["- none found"]
text = "\n".join(L) + "\n"
open(a.out, "w", encoding="utf-8").write(text)
print(text)
