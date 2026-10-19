#!/usr/bin/env python3
"""subtitle-chunks.py: turn a word-level transcript into phrase-level subtitle chunks (1 to 2 lines, read comfortably), for the `subtitles` format.

Where a chunk ends: a sentence end (. ? ! ...), a comma / semicolon / colon once the chunk is already ~22 characters long, a pause of
--pause seconds between two words, or the chunk reaching --max-chars (two lines). Each chunk is shown from just before its first word to just
after its last word (never over the next chunk). Lines are balanced at a space near the middle when the chunk is longer than --line-chars.

Key words (the ones the format sets in the italic serif): --em "word,word" (case-insensitive, punctuation ignored) and/or --auto-em, which marks at
most one long content word per chunk (7+ letters, not a stop word). Mis-heard names: --fix "Claud=Claude,Cloud=Claude" (applied to the shown text only).

Usage:
  python3 subtitle-chunks.py --transcript W/transcript.json --out W/subtitles.json [--em tecnicismi,creatività] [--auto-em] [--fix "Claud=Claude"]
Writes {"chunks": [{"text", "lines": [..], "at", "end", "em": [word indices in text.split()]}]} (times in the transcript's timeline).
"""
import argparse, json, re

STOP = set("""a ad al allo alla alle ai agli anche che chi ci come con cui da dal dalla dei del della delle dello di dove e ed è era
fra gli ha hanno ho i il in io la le lo loro lui ma me mi molto ne nei nel nella nelle non noi o per perché più quando quel quella
quello questa queste questo questi se sei si sia sono su sul sulla suo sua tra tu un una uno vi voi the and that this with from for are was were have has
had you your they them their what when where which would could should there about into than then just very also been being""".split())

ap = argparse.ArgumentParser()
ap.add_argument("--transcript", required=True); ap.add_argument("--out", required=True)
ap.add_argument("--max-chars", type=int, default=76); ap.add_argument("--line-chars", type=int, default=40)
ap.add_argument("--pause", type=float, default=0.45); ap.add_argument("--min-dur", type=float, default=0.9)
ap.add_argument("--lead", type=float, default=0.05); ap.add_argument("--tail", type=float, default=0.22)
ap.add_argument("--em", default=""); ap.add_argument("--auto-em", action="store_true"); ap.add_argument("--fix", default="")
args = ap.parse_args()

norm = lambda s: re.sub(r"[^\w]", "", s.lower())
raw = json.load(open(args.transcript, encoding="utf-8"))
words = [w for w in (raw["words"] if isinstance(raw, dict) else raw) if str(w.get("text", "")).strip()]
fixes = {norm(a): b.strip() for a, b in (p.split("=", 1) for p in args.fix.split(",") if "=" in p)}
em_set = {norm(w) for w in args.em.split(",") if w.strip()}


def show(text):
    k = norm(text)
    if k in fixes:   # keep the trailing punctuation of the original word
        tail = re.search(r"[^\w]*$", text).group(0)
        return fixes[k] + tail
    return text


chunks, cur = [], []
def flush():
    global cur
    if cur:
        chunks.append(cur); cur = []

for i, w in enumerate(words):
    cur.append(w)
    txt = " ".join(x["text"] for x in cur)
    nxt = words[i + 1] if i + 1 < len(words) else None
    t = w["text"].strip()
    end = bool(re.search(r"[.?!…]+[\"')\]]*$", t)) or nxt is None
    soft = bool(re.search(r"[,;:]$", t)) and len(txt) >= 22
    gap = nxt is not None and (nxt["start"] - w["end"]) >= args.pause
    too_long = len(txt) + (len(nxt["text"]) + 1 if nxt else 0) > args.max_chars
    if end or soft or gap or too_long:
        flush()

out = []
for ci, ch in enumerate(chunks):
    texts = [show(w["text"].strip()) for w in ch]
    text = " ".join(texts)
    # balance two lines near the middle when the chunk is long
    lines = [text]
    if len(text) > args.line_chars and len(texts) > 1:
        best = None
        for k in range(1, len(texts)):
            l1, l2 = " ".join(texts[:k]), " ".join(texts[k:])
            score = abs(len(l1) - len(l2))
            if best is None or score < best[0]:
                best = (score, l1, l2)
        lines = [best[1], best[2]]
    em = []
    for k, w in enumerate(ch):
        if norm(w["text"]) in em_set:
            em.append(k)
    if args.auto_em and not em:
        cand = [(len(norm(w["text"])), k) for k, w in enumerate(ch) if len(norm(w["text"])) >= 7 and norm(w["text"]) not in STOP]
        if cand:
            em.append(max(cand)[1])
    at = max(0.0, ch[0]["start"] - args.lead)
    end = ch[-1]["end"] + args.tail
    if end - at < args.min_dur:
        end = at + args.min_dur
    out.append({"text": text, "lines": lines, "at": round(at, 3), "end": round(end, 3), "em": em})
for a, b in zip(out, out[1:]):   # never overlap the next chunk
    if a["end"] > b["at"] - 0.02:
        a["end"] = round(max(a["at"] + 0.3, b["at"] - 0.02), 3)
json.dump({"chunks": out}, open(args.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("%d chunks, %.1f chars on average, longest %d" % (len(out), sum(len(c["text"]) for c in out) / max(1, len(out)), max((len(c["text"]) for c in out), default=0)))
