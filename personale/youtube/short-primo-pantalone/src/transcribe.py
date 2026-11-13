# words.json from the voiceover mp3 with faster-whisper (word timestamps). Usage: python transcribe.py vo.mp3
import json, sys
from faster_whisper import WhisperModel
m = WhisperModel("small", device="cpu", compute_type="int8")
segs, _ = m.transcribe(sys.argv[1], language="it", word_timestamps=True, vad_filter=False)
words = [{"w": w.word.strip(), "s": round(w.start, 2), "e": round(w.end, 2)} for s in segs for w in s.words]
json.dump(words, open("words.json", "w", encoding="utf-8"), ensure_ascii=False)
print(len(words), "words; ends", words[-1]["e"])
