"""Generate a critic-loop TARGET image with the Gemini image API (16/11/2026).

Usage:  python gen_target.py "prompt" OUT.png [--ref IMG ...] [--aspect 9:16]
The key is read from D:/ClaudeCodeTest/.env (GEMINI_API_KEY), never from the command line; the
output should go under .critic/ (gitignored). Write the prompt with the banana-pro-director skill.
Cost: about 0.04-0.05 EUR per image (check the Google AI Studio price page).
"""
import argparse, base64, json, mimetypes, os, sys, urllib.request, urllib.error

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))

def env(name):
    if os.environ.get(name):
        return os.environ[name]
    p = os.path.join(ROOT, ".env")
    if os.path.exists(p):
        for line in open(p, encoding="utf-8"):
            k, _, v = line.strip().partition("=")
            if k == name and v.strip():
                return v.strip().strip('"').strip("'")
    return ""

def main():
    a = argparse.ArgumentParser(); a.add_argument("prompt"); a.add_argument("out"); a.add_argument("--ref", nargs="*", default=[]); a.add_argument("--aspect", default=None)
    o = a.parse_args()
    key = env("GEMINI_API_KEY")
    if not key:
        sys.exit("GEMINI_API_KEY is empty: paste it in D:/ClaudeCodeTest/.env (see .env.example)")
    model = env("GEMINI_IMAGE_MODEL") or "gemini-2.5-flash-image"
    parts = [{"text": o.prompt}]
    for r in o.ref:
        parts.append({"inline_data": {"mime_type": mimetypes.guess_type(r)[0] or "image/png", "data": base64.b64encode(open(r, "rb").read()).decode()}})
    body = {"contents": [{"parts": parts}], "generationConfig": {"responseModalities": ["IMAGE"]}}
    if o.aspect:
        body["generationConfig"]["imageConfig"] = {"aspectRatio": o.aspect}
    req = urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/models/%s:generateContent" % model,
                                 data=json.dumps(body).encode(), headers={"Content-Type": "application/json", "x-goog-api-key": key})
    try:
        res = json.load(urllib.request.urlopen(req, timeout=180))
    except urllib.error.HTTPError as e:
        sys.exit("HTTP %d: %s" % (e.code, e.read().decode(errors="replace")[:600]))
    for c in res.get("candidates", []):
        for p in c.get("content", {}).get("parts", []):
            d = p.get("inlineData") or p.get("inline_data")
            if d:
                os.makedirs(os.path.dirname(os.path.abspath(o.out)), exist_ok=True)
                open(o.out, "wb").write(base64.b64decode(d["data"])); print("saved", o.out, "model", model); return
    sys.exit("no image in the answer: " + json.dumps(res)[:600])

if __name__ == "__main__":
    main()
