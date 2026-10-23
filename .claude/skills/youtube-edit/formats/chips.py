"""chips.py: hanging chips (format 41b), tools or labels as dark glass chips hung around the head, each with a dotted curved
arrow drawn toward the face, an optional phrase in a matching pill, and one slow camera that moves the footage AND the chips
with the same transform, so they stay pinned to the head. Built on the bench A/B of 23/10/2026
(`videos/_bench/ab/strumenti-chips/`, version B3), after the @realskytan reel: it beat the pills (41) on the `strumenti`
window; the creator: "more coherent with the style we are building" (B2 had been "a bit slow": B3 is the faster rhythm).

Usage (any build script; compose.py's "raw_html"/"raw_js"; logos in public/img):
    import sys; sys.path.insert(0, "<SK>/formats"); from chips import chips
    out = chips(items=[{"id": "claude", "name": "Claude", "logo": "img/claude.svg", "t": 1.109, "anchor": "Claude",
                        "centre": (470, 420), "arrow": ((630, 430), (690, 425), (705, 460), (700, 520))}, ...],
                t_out=9.6, phrase=("uno strumento in più", 7.909, "uno strumento", "claude"),
                camera=[(1.0, 4.0, "p2", 1.07, 38, 40), (6.23, 6.93, "p3", 1.09, 60, 40), ...])
    storyboard["raw_html"] = out["html"]; storyboard["raw_js"] = out["js"]
items: one to four chips; "centre" is the chip centre (320x96 chip), "arrow" a cubic Bézier (start, c1, c2, end) from the chip
edge to 25-45 px short of the face: place it on a snapshot, the head moves. phrase: (text, word time, anchor, chip id it sits
under) or None. camera: keyframes (t0, t1, ease p2|p3|sn, scale, origin x %, origin y %), each going from the previous state;
the camera starts at scale 1, origin 38% 40%. Spec and numbers: references/formats.md, 41b. Seek-safe: the camera is a pure
function of time driven by one tween, every other tween is a fromTo with explicit values. No sound.
"""
import math

OROC, IV = "212,175,95", "244,239,230"   # preset elegante-portfolio: gold #d4af5f, ivory #f4efe6
LEAD = 0.05                              # a chip starts 0.05 s before its word
BG0, BG1 = "rgba(20,15,10,0)", "rgba(20,15,10,0.55)"
B0, B1 = "rgba(%s,0)" % IV, "rgba(%s,0.28)" % IV

CAMJS = """(function(){
          var tg = [document.getElementById('video-zoom')].concat(Array.prototype.slice.call(document.querySelectorAll('%(sel)s')));
          function p2(x){return x<0.5?2*x*x:1-Math.pow(-2*x+2,2)/2;} function p3(x){return x<0.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2;}
          function sn(x){return 0.5-0.5*Math.cos(Math.PI*x);} function cl(x){return Math.max(0,Math.min(1,x));}
          // keyframes: [t0, t1, ease, scale, ox, oy] = go from the previous end state to (scale, ox, oy) between t0 and t1
          var K=%(K)s;
          function cam(t){ var s=1,ox=38,oy=40;
            for(var i=0;i<K.length;i++){ var k=K[i]; if(t<=k[0]) break; var u=k[2](cl((t-k[0])/(k[1]-k[0]))); s=s+(k[3]-s)*u; ox=ox+(k[4]-ox)*u; oy=oy+(k[5]-oy)*u; if(t<k[1]) break; s=k[3]; ox=k[4]; oy=k[5]; }
            return [s,ox,oy]; }
          function apply(t){ var c=cam(t); tg.forEach(function(e){ e.style.transformOrigin=c[1].toFixed(3)+'%% '+c[2].toFixed(3)+'%%'; e.style.transform='scale('+c[0].toFixed(5)+')'; }); }
          apply(0); var o={t:0};
          tl.fromTo(o,{t:0},{t:%(dur).3f,duration:%(dur).3f,ease:'none',immediateRender:false,onUpdate:function(){apply(o.t);}},0);
        })();"""


def _host(hid, t0, t1, anchor, inner):
    return ('<div class="card-host clip" id="host-%s" data-card-id="%s" data-start="%.3f" data-duration="%.3f" data-track-index="3" data-anchor="%s"'
            ' style="left:0;top:0;width:1920px;height:1080px;visibility:hidden;opacity:1;"><div class="card">%s</div></div>\n' % (hid, hid, t0, t1 - t0, anchor, inner))


def chips(items, t_out, duration, phrase=None, camera=()):
    assert 1 <= len(items) <= 4, "one to four chips"
    end = t_out + 0.4
    css = """
      .ch { position:absolute; width:320px; height:96px; border-radius:48px; box-sizing:border-box; background:rgba(20,15,10,0);
        backdrop-filter:blur(24px) saturate(1.2); -webkit-backdrop-filter:blur(24px) saturate(1.2); border:2px solid rgba(%(iv)s,0); }
      .ch-g { position:absolute; width:320px; height:96px; border-radius:48px; opacity:0; box-shadow:0 0 44px 8px rgba(%(or)s,.55); }
      .ch-in { position:absolute; inset:0; display:flex; align-items:center; gap:18px; padding-left:20px; opacity:0; }
      .ch-in img { width:56px; height:56px; object-fit:contain; display:block; }
      .ch-in span { font-family:"Inter","Segoe UI",sans-serif; font-weight:600; font-size:36px; line-height:1; color:#f4efe6; letter-spacing:-.01em; }
      .ar-svg { position:absolute; left:0; top:0; width:1920px; height:1080px; overflow:visible; }
      .ar-svg g path { filter:drop-shadow(0 1px 2px rgba(11,9,7,.55)); }
      #phr { position:relative; height:64px; box-sizing:border-box; padding:0 26px; border-radius:32px; display:flex; align-items:center; background:rgba(20,15,10,0); border:2px solid rgba(244,239,230,0); backdrop-filter:blur(24px) saturate(1.2); -webkit-backdrop-filter:blur(24px) saturate(1.2); }
      #phs { font-family:"Playfair Display",Georgia,serif; font-style:italic; font-weight:500; font-size:36px; line-height:1; color:#d4af5f; white-space:nowrap; opacity:0; }
""" % {"iv": IV, "or": OROC}
    html, js, hosts = "<style>%s</style>\n" % css, [], []
    for i, it in enumerate(items):
        cid, (cx, cy), (p0, p1, p2, p3) = it["id"], it["centre"], it["arrow"]
        t0 = round(it["t"] - LEAD, 3)
        tx = round(t_out - 0.05 * i, 3)   # exits staggered 0.05 s, the first chip leaves last
        d = "M%d %d C%d %d %d %d %d %d" % (p0[0], p0[1], p1[0], p1[1], p2[0], p2[1], p3[0], p3[1])
        a = math.atan2(p3[1] - p2[1], p3[0] - p2[0]); L = 15; s = math.radians(28)
        h = "M%.1f %.1f L%d %d L%.1f %.1f" % (p3[0] - L * math.cos(a - s), p3[1] - L * math.sin(a - s), p3[0], p3[1], p3[0] - L * math.cos(a + s), p3[1] - L * math.sin(a + s))
        inner = ('<div class="ch-g" id="g-%s" style="left:%dpx;top:%dpx"></div>'
                 '<div class="ch" id="c-%s" style="left:%dpx;top:%dpx"><div class="ch-in" id="ci-%s"><img src="%s" alt=""/><span>%s</span></div></div>'
                 '<svg class="ar-svg" viewBox="0 0 1920 1080"><defs><mask id="m-%s" maskUnits="userSpaceOnUse" x="0" y="0" width="1920" height="1080">'
                 '<path id="mp-%s" d="%s" pathLength="1" fill="none" stroke="#fff" stroke-width="14" stroke-dasharray="1 2" stroke-dashoffset="1"/></mask></defs>'
                 '<g id="ag-%s"><path d="%s" fill="none" stroke="rgba(%s,.55)" stroke-width="3" stroke-linecap="round" stroke-dasharray="2 9" mask="url(#m-%s)"/>'
                 '<path id="ah-%s" d="%s" fill="none" stroke="rgba(%s,.55)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></g></svg>'
                 % (cid, cx - 160, cy - 48, cid, cx - 160, cy - 48, cid, it["logo"], it["name"], cid, cid, d, cid, d, IV, cid, cid, h, IV))
        html += _host("ch-" + cid, t0, end, it["anchor"], inner); hosts.append("#host-ch-" + cid)
        js += [
            "tl.set('#c-%s', { backgroundColor:'%s', borderColor:'%s', scale:0.94, y:10, filter:'blur(4px)' }, 0);" % (cid, BG0, B0),
            "tl.set('#ci-%s', { opacity:0 }, 0); tl.set('#g-%s', { opacity:0 }, 0); tl.set('#ag-%s', { opacity:1, y:0 }, 0);" % (cid, cid, cid),
            "tl.set('#mp-%s', { strokeDashoffset:1 }, 0); tl.set('#ah-%s', { opacity:0 }, 0);" % (cid, cid),
            # entrance: 0.4 s expo.out, blur melts, a soft gold glow rises and falls once
            "tl.fromTo('#c-%s', { backgroundColor:'%s', borderColor:'%s', scale:0.94, y:10, filter:'blur(4px)' }, { backgroundColor:'%s', borderColor:'%s', scale:1, y:0, filter:'blur(0px)', duration:0.4, ease:'expo.out', immediateRender:false }, %.3f);" % (cid, BG0, B0, BG1, B1, t0),
            "tl.fromTo('#ci-%s', { opacity:0 }, { opacity:1, duration:0.4, ease:'expo.out', immediateRender:false }, %.3f);" % (cid, t0),
            "tl.fromTo('#g-%s', { opacity:0 }, { opacity:0.35, duration:0.4, ease:'sine.out', immediateRender:false }, %.3f);" % (cid, t0),
            "tl.fromTo('#g-%s', { opacity:0.35 }, { opacity:0, duration:0.4, ease:'sine.in', immediateRender:false }, %.3f);" % (cid, t0 + 0.4),
            # arrow draws 0.08 s after the chip in 0.45 s, its head lands at the end
            "tl.fromTo('#mp-%s', { strokeDashoffset:1 }, { strokeDashoffset:0, duration:0.45, ease:'power2.out', immediateRender:false }, %.3f);" % (cid, t0 + 0.08),
            "tl.fromTo('#ah-%s', { opacity:0 }, { opacity:1, duration:0.12, ease:'sine.out', immediateRender:false }, %.3f);" % (cid, t0 + 0.41),
            # exit: 0.4 s, rises 8 px and blurs out
            "tl.fromTo('#c-%s', { backgroundColor:'%s', borderColor:'%s', y:0, filter:'blur(0px)' }, { backgroundColor:'%s', borderColor:'%s', y:-8, filter:'blur(4px)', duration:0.4, ease:'sine.inOut', immediateRender:false }, %.3f);" % (cid, BG1, B1, BG0, B0, tx),
            "tl.fromTo('#ci-%s', { opacity:1 }, { opacity:0, duration:0.4, ease:'sine.inOut', immediateRender:false }, %.3f);" % (cid, tx),
            "tl.fromTo('#ag-%s', { opacity:1, y:0 }, { opacity:0, y:-8, duration:0.4, ease:'sine.inOut', immediateRender:false }, %.3f);" % (cid, tx),
        ]
    if phrase:   # the phrase sits in a dark glass pill, centred 18 px under its chip
        text, pt, panchor, under = phrase
        ucx, ucy = [it["centre"] for it in items if it["id"] == under][0]
        tp = round(pt - LEAD, 3)
        html += _host("phr", tp, end, panchor, '<div id="phw" style="position:absolute;left:%dpx;top:%dpx;width:600px;display:flex;justify-content:center;"><div id="phr"><span id="phs">%s</span></div></div>'
                      % (ucx - 300, ucy + 48 + 18, text))
        hosts.append("#host-phr")
        js += ["tl.set('#phr', { backgroundColor:'%s', borderColor:'%s', scale:0.94, y:10, filter:'blur(4px)' }, 0); tl.set('#phs', { opacity:0 }, 0);" % (BG0, B0),
               "tl.fromTo('#phr', { backgroundColor:'%s', borderColor:'%s', scale:0.94, y:10, filter:'blur(4px)' }, { backgroundColor:'%s', borderColor:'%s', scale:1, y:0, filter:'blur(0px)', duration:0.4, ease:'expo.out', immediateRender:false }, %.3f);" % (BG0, B0, BG1, B1, tp),
               "tl.fromTo('#phs', { opacity:0 }, { opacity:1, duration:0.4, ease:'expo.out', immediateRender:false }, %.3f);" % tp,
               "tl.fromTo('#phr', { backgroundColor:'%s', borderColor:'%s', y:0, filter:'blur(0px)' }, { backgroundColor:'%s', borderColor:'%s', y:-8, filter:'blur(4px)', duration:0.4, ease:'sine.inOut', immediateRender:false }, %.3f);" % (BG1, B1, BG0, B0, t_out),
               "tl.fromTo('#phs', { opacity:1 }, { opacity:0, duration:0.4, ease:'sine.inOut', immediateRender:false }, %.3f);" % t_out]
    if camera:   # one proxy moves the footage and every chip host with the SAME transform: they stay pinned to the head
        K = "[" + ",".join("[%s,%s,%s,%s,%s,%s]" % tuple(str(v) for v in k) for k in camera) + "]"
        js.append(CAMJS % {"sel": ", ".join(h + " .card" for h in hosts), "K": K, "dur": duration})
    return {"html": html, "js": "\n        ".join(js)}
