"""uiplane.py: a rebuilt interface floating in 3D, with a hand cursor that clicks (format 51). From the teardown of Joseph's video (01/11/2026):
whenever he shows "what I typed" or "where I approve", it is a clean, redrawn window (dark, rounded, tilted in perspective, soft shadow), never a
raw screen recording: legible text, no noise, and a pointing-hand cursor that arrives and presses. Use it for a prompt, an AI answer, an approval.

Usage (compose.py "raw_html"/"raw_js", or a build script):
    import sys; sys.path.insert(0, "<SK>/formats"); from uiplane import uiplane
    out = uiplane(title="Piano · Se non ti stai clonando", prompt={"text": "Preparalo per il montaggio: togli errori e silenzi", "t": 3.0, "anchor": "preparalo"},
                  replies=[{"text": "Ecco l'audio pronto: ho tolto errori e ripetizioni.", "t": 7.0, "anchor": "pronto"}],
                  button={"label": "Approva", "done": "Approvato", "click_at": 10.2, "anchor": "approvo"}, t_in=2.0, t_out=13.0)
prompt: typed into the field at about 24 characters a second from `t`. replies: one or two answer lines (a small spark mark + text), each on its time.
button: optional; the hand arrives and presses at click_at, the button turns green and says `done`.
The window is 1260 x 640 at (120, 240): its right edge (1380) stays left of the face PiP corner (checked). The tilt eases from -26 to -8 degrees
on entry and keeps a slow drift. Seek-safe: typing uses the same put()/onUpdate pattern as compose.py; every tween is a fromTo.
"""
import json
from plates_base import *

WX, WY, WW, WH = 120, 240, 1260, 640
HAND = ('<svg id="uiH" viewBox="0 0 40 48" style="position:absolute;left:0;top:0;width:76px;height:91px;opacity:0;z-index:5;filter:drop-shadow(0 8px 10px rgba(0,0,0,.55))">'
        '<path d="M14 3c2.2 0 4 1.8 4 4v14l2-.6c2-.6 4 .8 4.2 2.8l1.6-.4c2-.5 3.8.8 4 2.8l1.2-.2c2-.3 3.8 1.2 3.8 3.2V36c0 6-4.4 11-11 11h-5c-4 0-6.6-2-8.6-5.2L4.4 33c-.8-1.4-.4-3.2 1-4 1.2-.7 2.6-.4 3.6.6L10 31V7c0-2.2 1.8-4 4-4z" '
        'fill="#fff" stroke="#111" stroke-width="2.2" stroke-linejoin="round"/></svg>')


SPARK = '<svg viewBox="0 0 44 44" style="position:absolute;inset:0"><path d="M22 9v26M10.7 15.5l22.6 13M10.7 28.5l22.6-13" stroke="#1a1405" stroke-width="4.2" stroke-linecap="round" fill="none"/></svg>'


def uiplane(title, prompt, t_in, t_out, replies=(), button=None, bg=True, cid="ui", sound=True):
    check_pip(WX, WY, WW, WH, "uiplane window")
    css = BASE_CSS + """
  .ui-st { position:absolute; inset:0; perspective:1800px; perspective-origin:50%% 40%%; }
  .ui-w { position:absolute; left:%dpx; top:%dpx; width:%dpx; height:%dpx; border-radius:30px; background:linear-gradient(180deg,#1b1a18,#121110); opacity:0; overflow:hidden;
          box-shadow:0 60px 120px rgba(0,0,0,.6), 0 0 0 2px rgba(255,255,255,.1); transform-origin:50%% 50%%; font-family:var(--k-font); color:var(--k-text); }
  .ui-h { height:66px; display:flex; align-items:center; gap:10px; padding:0 26px; border-bottom:1px solid rgba(255,255,255,.08); font-weight:600; font-size:24px; color:var(--k-mute); }
  .ui-h i { width:14px; height:14px; border-radius:50%%; background:rgba(255,255,255,.2); display:block; } .ui-h span { margin-left:14px; }
  .ui-body { position:absolute; left:46px; right:46px; top:96px; }
  .ui-r { display:flex; gap:20px; align-items:flex-start; margin-bottom:26px; opacity:0; }
  .ui-sp { width:44px; height:44px; border-radius:50%%; background:var(--k-accent); flex:none; position:relative; }
  .ui-rt { font-weight:500; font-size:36px; line-height:1.3; padding-top:2px; }
  .ui-f { position:absolute; left:40px; right:40px; bottom:40px; height:150px; border-radius:24px; background:rgba(255,255,255,.06); border:1.5px solid rgba(255,255,255,.1); }
  .ui-ft { position:absolute; left:30px; right:200px; top:28px; font-weight:500; font-size:34px; line-height:1.35; color:var(--k-text); }
  .ui-ft u { text-decoration:none; display:inline-block; width:3px; height:34px; background:var(--k-accent2); vertical-align:-6px; margin-left:3px; }
  .ui-b { position:absolute; right:24px; bottom:24px; height:64px; padding:0 34px; border-radius:32px; background:var(--k-accent); color:#1a1405; font-weight:800; font-size:28px; line-height:64px; white-space:nowrap; }
  .ui-b.ok { background:var(--k-accent2); color:#06140d; }
""" % (WX, WY, WW, WH)
    inner = '<div class="ui-st"><div class="ui-w" id="uiW"><div class="ui-h"><i></i><i></i><i></i><span>%s</span></div>\n<div class="ui-body">' % esc(title)
    for i, r in enumerate(replies):
        inner += '<div class="ui-r" id="uiR%d"%s><div class="ui-sp">%s</div><div class="ui-rt">%s</div></div>' % (i, at_attrs(r["t"], r.get("anchor", "")), SPARK, esc(r["text"]))
    inner += '</div>\n<div class="ui-f"><div class="ui-ft" id="uiP"%s><span id="uiPt"></span><u></u></div>' % at_attrs(prompt["t"], prompt.get("anchor", ""))
    if button:
        inner += '<div class="ui-b" id="uiB"%s>%s</div>' % (at_attrs(button["click_at"], button.get("anchor", "")), esc(button["label"]))
    inner += '</div></div></div>\n' + HAND
    extra = []
    if sound:   # typing for exactly the typing time, a click on the click (sound.md table: typing 0.22, click 0.28)
        extra.append('<audio id="sfx-%s-type" src="sfx/typing.mp3" data-start="%.3f" data-duration="%.3f" data-track-index="@TRACK@" data-volume="0.22"></audio>'
                     % (cid, float(prompt["t"]), min(max(len(prompt["text"]) / 24.0, 0.5), 2.2)))
        if button:
            extra.append('<audio id="sfx-%s-click" src="sfx/click.mp3" data-start="%.3f" data-duration="0.34" data-track-index="@TRACK@" data-volume="0.28"></audio>' % (cid, float(button["click_at"])))
    html, pre, post = wrap(cid, t_in, t_out, css, inner, bg=bg, kicks=[prompt["t"]] + [r["t"] for r in replies] + ([button["click_at"]] if button else []), sound=sound, audio=extra,
                          sfx_events=[t_in + 0.6] + [r["t"] for r in replies])
    js = list(pre)
    js.append("tl.set('#uiW', { opacity:0, rotateY:-26, rotateX:5, y:30, scale:0.94 }, 0);")
    js.append(fromto("#uiW", "{opacity:0,rotateY:-26,rotateX:5,y:30,scale:0.94}", "{opacity:1,rotateY:-8,rotateX:3,y:0,scale:1}", t_in + 0.2, 0.9, "power3.out"))
    js.append("tl.fromTo('#uiW', { rotateY:-8 }, { rotateY:-5, duration:%.3f, ease:'sine.inOut', immediateRender:false }, %.3f);" % (max(t_out - t_in - 1.6, 1.0), t_in + 1.1))   # slow drift
    txt, t0 = prompt["text"], float(prompt["t"])
    dur = max(len(txt) / 24.0, 0.5)
    js.append("(function(){ var el = document.getElementById('uiPt'), Q = %s, o = { n: 0 }, put = function () { el.textContent = Q.slice(0, Math.floor(o.n)); };"
              " put(); tl.fromTo(o, { n: 0 }, { n: Q.length + 0.999, duration: %.3f, ease: 'none', immediateRender: false, onUpdate: put }, %.3f); })();" % (json.dumps(txt), dur, t0))
    for i, r in enumerate(replies):
        js.append("tl.set('#uiR%d', { opacity:0, y:16 }, 0);" % i)
        js.append(fromto("#uiR%d" % i, "{opacity:0,y:16}", "{opacity:1,y:0}", r["t"] - 0.05, 0.5))
    if button:
        ta = float(button["click_at"])
        bx, by = WX + WW - 40 - 24 - 90, WY + WH - 40 - 24 - 32   # about the centre of the button in screen space (the tilt moves it a few px)
        js.append("tl.set('#uiH', { opacity:0, x:%d, y:%d }, 0);" % (bx + 260, by + 200))
        js.append(fromto("#uiH", "{opacity:0,x:%d,y:%d}" % (bx + 260, by + 200), "{opacity:1,x:%d,y:%d}" % (bx - 10, by + 34), ta - 1.0, 0.8, "power2.inOut"))
        js.append(fromto("#uiH", "{scale:1}", "{scale:0.86}", ta - 0.12, 0.12, "power2.in"))
        js.append(fromto("#uiH", "{scale:0.86}", "{scale:1}", ta, 0.2, "power2.out"))
        js.append("(function(){ var b = document.getElementById('uiB'), o = { v: 0 }, put = function () { var ok = o.v >= 1; b.classList.toggle('ok', ok); b.textContent = ok ? %s : %s; };"
                  " put(); tl.fromTo(o, { v: 0 }, { v: 1, duration: 0.01, ease: 'none', immediateRender: false, onUpdate: put }, %.3f); })();" % (json.dumps("✓ " + button.get("done", "Fatto")), json.dumps(button["label"]), ta))
        js.append(fromto("#uiB", "{scale:1}", "{scale:1.06}", ta, 0.18, "power2.out"))
        js.append(fromto("#uiH", "{opacity:1}", "{opacity:0}", ta + 1.2, 0.4, "power2.in"))
    js.extend(post)
    return {"html": html, "js": "\n        ".join(js)}
