# words.json from the voiceover mp3 with faster-whisper (word timestamps). Usage: python transcribe.py vo.mp3
import json, sys, subprocess, numpy as np
from faster_whisper import WhisperModel
m = WhisperModel("small", device="cpu", compute_type="int8")
pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", sys.argv[1], "-f", "s16le", "-ac", "1", "-ar", "16000", "-"], capture_output=True).stdout   # decode with ffmpeg (PyAV in this env rejects faster-whisper's args)
audio = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
segs, _ = m.transcribe(audio, language="it", word_timestamps=True, vad_filter=False)
words = [{"w": w.word.strip(), "s": round(w.start, 2), "e": round(w.end, 2)} for s in segs for w in s.words]
# spell the words as the script does (captions and at() lookups read them)
FIX = [(("carta", "modello"), "cartamodello"), (("117", "cm"), "centodiciassette centimetri"), (("tenendo", "la"), "tenendola"), (("all", "'errore"), "all'errore"), (("all", "'italiana"), "all'italiana"), (("c", "'era"), "c'era"), (("l", "'errore"), "l'errore")]
i, out = 0, []
while i < len(words):
    for (a, b), rep in FIX:
        if i + 1 < len(words) and words[i]["w"].lower().strip(".,") == a and words[i + 1]["w"].lower().rstrip(".,").startswith(b):
            tail = words[i + 1]["w"][len(b):]; parts = rep.split()
            if len(parts) == 1: out.append({"w": rep + tail, "s": words[i]["s"], "e": words[i + 1]["e"]})
            else: out += [{"w": parts[0], "s": words[i]["s"], "e": words[i]["e"]}, {"w": parts[1] + tail, "s": words[i + 1]["s"], "e": words[i + 1]["e"]}]
            i += 2; break
    else:
        w = dict(words[i]); w["w"] = {"cos.": "COS.", "cos": "COS", "inverso,": "Inverso,"}.get(w["w"], w["w"]); out.append(w); i += 1
words = out
json.dump(words, open("words.json", "w", encoding="utf-8"), ensure_ascii=False)
print(len(words), "words; ends", words[-1]["e"])
