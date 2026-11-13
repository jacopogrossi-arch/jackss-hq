"""world3d.py: a motion plate in a real 3D world (format 52, Jacopo 10/11/2026: "wow bellissimo, aggiungiamo assolutamente al workflow, anche in più situazioni").

Drawn with three.js (assets/vendor/three.module.min.js, MIT) by the engine assets/vendor/world3d.js. Use it where flat cards cannot show the idea:
a garment that turns while its parts are named, the camera entering an object, pages and photos standing in space with the camera flying from one to
the next. NOT for a normal plate of titles, pills and links (scene.py is sharper and cheaper) and never for a product's interface.

    from world3d import World3D
    w = World3D("w1", 120.0, 127.5, title="Il *pantalone*", sub="Drop 1 · cotone drill")
    w.trouser("tr", pos=(0, 0, 0), rot_y=-0.42, turn=[(0, 2.9, -0.18, "glide"), (2.9, 1.5, 0.77, "hand")])      # (start, duration, to, ease)
    w.cam((0.34, 1.10, 0.86), look=(0.07, 0.975, 0))                           # the first cam() is where the camera starts
    w.cam((0.50, 0.80, 2.55), look=(0, 0.56, 0), t=122.9, d=1.5)               # then each cam() is one move: at second t (video time), lasting d
    w.label("tr", (0.200, 1.060, 0.03), "Vita *naturale*", t=120.9, anchor="vita", sub="regolatori laterali", dx=150, dy=-150)
    out = w.build()          # {"html", "js"}: append to what the block returns (plates-build.py) or to a storyboard's raw_html / raw_js
    w.stage(public_dir)      # copies three.js and the engine into <public>/vendor (plates-build.py does it by itself)

Times given to cam(), label() and the objects' `t` are VIDEO times, like in scene.py (the word's start in transcript.json); the engine works in
seconds from the plate's start. Units are metres: the trouser stands on y = 0 and its waist is at 1.08. `rot_y` / `turn` are radians.
Everything is a pure function of time (frames render out of order): no physics, no random, no requestAnimationFrame.
Lab without the pipeline: `World3D.page(folder, [w, ...])` writes a standalone index.html to snapshot or render.
Cost, measured 10/11/2026: about 10 s of render per second of video at 1080p draft; 4K at 60 fps not measured yet. Keep 3D plates few and short.
"""
import json, os, re, shutil

SK = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
VENDOR = ("three.module.min.js", "three-LICENSE.txt", "world3d.js", "atelier-kit.js")

CSS = """<style>
  .w3-host { background: var(--k-bg, #0A2B1E); overflow: hidden; font-family: var(--k-font, "Inter", "Segoe UI", system-ui, sans-serif); color: var(--k-text, #f4efe6); }
  .w3-wash { position: absolute; inset: 0; background: radial-gradient(900px 620px at 50% 100%, #17613F, rgba(23,97,63,0) 70%), radial-gradient(700px 520px at 0% 0%, rgba(23,97,63,.7), rgba(23,97,63,0) 70%); }
  .w3-grid { position: absolute; left: -240px; top: -240px; width: 2400px; height: 1560px; background-size: 80px 80px;
    background-image: linear-gradient(rgba(120,235,180,.13) 1px, transparent 1px), linear-gradient(90deg, rgba(120,235,180,.13) 1px, transparent 1px); }
  .w3-gl, .w3-ln { position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; }
  .w3-bar { position: absolute; left: 0; top: 0; width: 6px; height: 1080px; background: #e2472f; opacity: 0; box-shadow: 0 0 22px rgba(226,71,47,.55); }
  .w3-bar b { position: absolute; left: 14px; top: 18px; font: 700 20px/1 "IBM Plex Mono", "Consolas", monospace; letter-spacing: .08em; color: #e2472f; white-space: nowrap; }
  .w3-title { position: absolute; left: 110px; top: 100px; font-size: 96px; font-weight: 800; line-height: 1.05; opacity: 0; }
  .w3-sub { position: absolute; left: 114px; top: 226px; font-size: 34px; font-weight: 500; color: rgba(244,239,230,.66); opacity: 0; }
  .w3-title i, .w3-lab i { font-family: var(--k-serif, "Playfair Display", Georgia, serif); font-style: italic; font-weight: 500; color: var(--k-accent, #e3c47f); }
  .w3-lab { position: absolute; left: 0; top: 0; padding: 16px 26px; border-radius: 18px; background: rgba(244,239,230,.96); color: #15100b; font-size: 32px; font-weight: 700;
    white-space: nowrap; box-shadow: 0 24px 50px rgba(0,0,0,.45); opacity: 0; }
  .w3-lab i { color: #8a6a2a; }
  .w3-lab small { display: block; margin-top: 4px; font-size: 28px; font-weight: 500; color: rgba(21,16,11,.72); }
</style>"""


def key(text):
    """'Il *pantalone*' -> the key word in the italic serif (one per line at most)."""
    return re.sub(r"\*(.+?)\*", r"<i>\1</i>", text)


class World3D:
    def __init__(self, cid, t_in, t_out, title=None, sub=None, track=30, fade=0.3, fov=32, title_out=None):
        """title_out: video time at which the title leaves (give it when the camera will fly objects through the top-left of the frame)."""
        self.cid, self.t_in, self.t_out, self.title, self.sub, self.track, self.fade, self.fov, self.title_out = cid, t_in, t_out, title, sub, track, fade, fov, title_out
        self.objects, self.cams, self.labels, self.events = [], [], [], []
        self.room_spec, self.look_spec, self.base, self.passes, self.dofs, self.shutter_frames, self.exposure = None, None, "final", [], [], 0.8, None

    def _r(self, t):
        return round(t - self.t_in, 3)

    def _obj(self, _shape, oid, pos, rot_y, turn, move, t, **kw):
        o = dict(type=_shape, id=oid, pos=list(pos), rot=[kw.pop("rot_x", 0), rot_y, kw.pop("rot_z", 0)], **{k: v for k, v in kw.items() if v is not None})
        if turn:                                        # (start, duration, to_rot_y, ease) in seconds from the plate's start
            o["turn"] = [dict(t=a, d=d, to=[o["rot"][0], to, o["rot"][2]], ease=e) for a, d, to, e in turn]
        if move:                                        # (start, duration, to_pos, ease)
            o["move"] = [dict(t=a, d=d, to=list(to), ease=e) for a, d, to, e in move]
        if t is not None:
            o["t"] = self._r(t); self.events.append(t)
        self.objects.append(o)
        return oid

    def trouser(self, oid, pos=(0, 0, 0), rot_y=0.0, turn=None, move=None, t=None, color="#7b7d5a", pleats=2, cuff=True, scale=None, shadow=True, look=None, hang=None, pockets=True):
        """The Drop 1 trouser, built in code: natural waist with side adjusters, pleats (0, 1 or 2 per side), straight leg, turn-ups. Stylised, not a photo."""
        return self._obj("trouser", oid, pos, rot_y, turn, move, t, color=color, pleats=pleats, cuff=cuff, scale=scale, shadow=[1.5, 0.95] if shadow else None, floor=pos[1], pass_mode=look, hang=hang, pockets=None if pockets else False)

    def card(self, oid, pos, w=0.8, h=0.5, text=None, sub=None, img=None, rot_y=0.0, turn=None, move=None, t=None, color=None, size=None, look=None, flat=False):
        """An ivory sheet standing in space: a title with one *key* word, or a picture (`img`, a path inside public/, e.g. "img/moodboard.jpg") with an optional caption."""
        return self._obj("card", oid, pos, rot_y, turn, move, t, w=w, h=h, text=text, sub=sub, img=img, color=color, size=size, pass_mode=look, flat=flat or None)

    def solid(self, oid, shape, pos, size, color=None, fabric=False, metal=None, rough=None, rot_y=0.0, turn=None, move=None, t=None, shadow=None, look=None):
        """A plain object: shape "box" (size x, y, z), "cyl" (diameter, height) or "sphere" (diameter). fabric=True wears the drill weave (a roll of cloth)."""
        return self._obj(shape, oid, pos, rot_y, turn, move, t, size=list(size), color=color, fabric=fabric or None, metal=metal, rough=rough, shadow=shadow, floor=pos[1] - size[1] / 2 if len(size) > 1 else None, pass_mode=look)

    def cam(self, pos, look, t=None, d=1.3, ease="hand"):
        """The first call is the start; every later call is ONE move to (pos, look) starting at video time t and lasting d (curve D by default, like the swipes)."""
        if not self.cams:
            self.cams.append(dict(pos=list(pos), look=list(look)))
        else:
            if t is None:
                raise ValueError("%s: a camera move needs its time t" % self.cid)
            last = self.cams[-1]
            if len(self.cams) > 1 and self._r(t) < last["t"] + last["d"] - 1e-6:
                raise ValueError("%s: the camera move at %.2f starts before the one before it has ended (one move at a time)" % (self.cid, t))
            self.cams.append(dict(pos=list(pos), look=list(look), t=self._r(t), d=d, ease=ease)); self.events.append(t)
        return self

    def label(self, obj, point, text, t, anchor="", sub=None, dx=150, dy=-120, out=None):
        """An ivory label pinned to a point of an object (the object's own coordinates): it follows the object as it turns. dx/dy = where the label sits from the point, in pixels."""
        self.labels.append(dict(obj=obj, p=list(point), text=text, sub=sub, t=self._r(t), at=t, anchor=anchor, dx=dx, dy=dy, out=None if out is None else self._r(out)))
        self.events.append(t)
        return self

    def room(self, bg="#1b1511", key="#fff0d8", dir=(-6, 5, 2.5), key_i=3.2, hemi=("#fff0dd", "#6b4a30"), hemi_i=0.9, side_i=0.0, rim="#a9bfe8", rim_i=0.5, fog=None, box=(6, 5, 30), aim=(0, 0.8, 0), exposure=None, soft=4, far=80):
        """A lit ROOM (14/11/2026, from the autogrill reference): daylight through a window as the key light (real shadow map), a warm ambient, optional fog. Fill it with props: prop(...).
        A room is dense or it is empty: furnish every shot (floor, walls, window, shelves of cloth, a table with things on it, lamps). No venetian blinds (Jacopo: they read as a render error)."""
        self.room_spec = dict(bg=bg, key=key, dir=list(dir), key_i=key_i, hemi=list(hemi), hemi_i=hemi_i, side_i=side_i, rim=rim, rim_i=rim_i, box=list(box), aim=list(aim), soft=soft, far=far)
        if fog: self.room_spec["fog"] = list(fog)
        self.exposure = exposure
        return self

    def prop(self, shape, oid, pos, size=None, rot_y=0.0, turn=None, move=None, t=None, **kw):
        """A prop of the atelier kit (assets/vendor/atelier-kit.js). shape: woodfloor [x,z] · wall [len,h,thick] (hole=[cx,cy,w,h]) · window [w,h] · rollrack [len,h,depth] · bolts [w,d] (n=) · spoolwall [w,h] · table [len,h,depth]
        · paper [w,d] (kind="pattern"|"sketch"|"swatch"|"lines") · frame [w,h] (kind=) · ruler [len,w] · shears · sewing · mannequin · pendant [cord] (light=) · desklamp · plant [h] · rail [len,h] · rug [w,d] · cloth [w,d] (color=)."""
        return self._obj(shape, oid, pos, rot_y, turn, move, t, size=list(size) if size else None, **kw)

    def look(self, bg="#14100c", floor="#2b1d13", key="#ffc98a", dir=(-2.4, 1.5, 1.7), slats=9, gap=0.30, thick=0.09, dust=True, exposure=None, wall="#3b2b20", wall_z=-1.7):
        """An atelier look (13/11/2026, from the @holcdenis teardown): a dark room, ONE warm key light thrown through blinds (real shadow-map stripes that creep across the floor
        and the objects), dust in the light, a floor that catches it. Replaces the green wash and grid. `dir` = where the sun sits (x, y, z); `slats`/`gap`/`thick` = the blinds."""
        self.look_spec = dict(bg=bg, floor=floor, key=key, dir=list(dir), slats=slats, gap=gap, thick=thick, dust=dust, wall=wall, wall_z=wall_z)
        self.exposure = exposure
        return self

    def base_pass(self, mode):
        """What the plate shows before its first wipe: "final" (default, lit), "clay" (flat grey, no stripes) or "ink" (paper + black outlines: the technical drawing)."""
        self.base = mode
        return self

    def wipe(self, to, t, d=0.7):
        """A vertical bar sweeps left to right at video time t (lasting d) and what is behind it becomes `to` ("final", "clay" or "ink"). It carries a small HUD tag (FRAME .... . PASS: ..)."""
        self.passes.append(dict(t=self._r(t), d=d, to=to)); self.events.append(t)
        return self

    def dof(self, t, d, aperture=0.02):
        """Depth of field from t for d seconds (eases in and out in 0.35 s): the lens is spread over a disc of radius `aperture` metres and 12 renders are averaged; the point the camera looks at stays sharp. x12 render cost."""
        self.dofs.append(dict(t=self._r(t), d=d, ap=aperture)); self.events.append(t)
        return self

    def shutter(self, frames=0.8):
        """Motion blur: the shutter stays open `frames` of a frame (0.8 = fast whips smear). Applies by itself while the camera is faster than ~0.6 m/s; 0 turns it off. x2-x10 render cost on those frames only."""
        self.shutter_frames = frames
        return self

    def spec(self):
        if not self.cams:
            raise ValueError("%s: give the camera a start with cam(pos, look)" % self.cid)
        out = {} if self.title_out is None else {"out": self._r(self.title_out)}
        texts = [dict(id="%s-T" % self.cid, t=0.25, **out)] if self.title else []
        texts += [dict(id="%s-S" % self.cid, t=0.5, **out)] if self.sub else []
        extra = {}
        if self.look_spec: extra["look"] = self.look_spec
        if self.room_spec: extra["room"] = self.room_spec
        if self.exposure is not None: extra["exposure"] = self.exposure
        if self.base != "final": extra["base"] = self.base
        if self.passes: extra["passes"] = self.passes
        if self.dofs: extra["dof"] = self.dofs
        if self.shutter_frames != 0.8: extra["shutter"] = self.shutter_frames
        return dict(id=self.cid, t_in=self.t_in, dur=round(self.t_out - self.t_in, 3), fov=self.fov, objects=self.objects, cam=self.cams, texts=texts, **extra,
                    labels=[dict(obj=L["obj"], p=L["p"], t=L["t"], dx=L["dx"], dy=L["dy"], **({"out": L["out"]} if L["out"] is not None else {})) for L in self.labels])

    def build(self, standalone=False):
        c, d = self.cid, self.t_out - self.t_in
        wash = '' if (self.look_spec or self.room_spec) else '<div class="w3-wash"></div><div class="w3-grid" id="%s-grid"></div>' % c
        inner = [wash + '<canvas class="w3-gl" id="%s-gl" width="1920" height="1080"></canvas><canvas class="w3-gl w3-mb" id="%s-mb" width="1920" height="1080" style="display:none"></canvas>'
                 '<svg class="w3-ln" id="%s-ln" width="1920" height="1080" viewBox="0 0 1920 1080"></svg>' % (c, c, c)]
        if self.passes:
            inner.append('<div class="w3-bar" id="%s-bar"><b id="%s-bart"></b></div>' % (c, c))
        if self.title:
            inner.append('<div class="w3-title" id="%s-T">%s</div>' % (c, key(self.title)))
        if self.sub:
            inner.append('<div class="w3-sub" id="%s-S">%s</div>' % (c, key(self.sub)))
        for n, L in enumerate(self.labels):
            an = ' data-anchor="%s"' % L["anchor"].replace('"', "&quot;") if L["anchor"] else ' data-unanchored="1"'
            inner.append('<div class="w3-lab" id="%s-l%d" data-at="%.3f"%s>%s%s</div>' % (c, n, L["at"], an, key(L["text"]), "<small>%s</small>" % L["sub"] if L["sub"] else ""))
        vis = "visibility:visible;opacity:1;" if standalone else "visibility:hidden;opacity:0;"
        html = (CSS + '\n<div class="card-host clip w3-host" id="host-%s" data-card-id="%s" data-unanchored="1" data-start="%.3f" data-duration="%.3f" data-track-index="%d" '
                'style="left:0;top:0;width:1920px;height:1080px;position:absolute;%s%s">%s</div>\n'
                '<script type="module">import { mount } from "./vendor/world3d.js"; mount(%s);</script>'
                % (c, c, self.t_in, d, self.track, vis, ("background:%s;" % (self.room_spec or self.look_spec)["bg"]) if (self.look_spec or self.room_spec) else "", "".join(inner), json.dumps(self.spec(), ensure_ascii=False)))
        f = self.fade
        js = "\n".join([
            "tl.set('#host-%s', { visibility:'hidden', opacity:0 }, 0);" % c,
            "tl.set('#host-%s', { visibility:'visible' }, %.3f);" % (c, self.t_in),
            "tl.fromTo('#host-%s', { opacity:0 }, { opacity:1, duration:%.3f, ease:'power2.out', immediateRender:false }, %.3f);" % (c, f, self.t_in),
            # the same drawing the engine does on hf-seek, driven from the one timeline too (a pure function of time: drawing twice is harmless)
            "tl.fromTo({ k:0 }, { k:0 }, { k:1, duration:%.3f, ease:'none', immediateRender:false, onUpdate:function(){ var f = window.__w3d && window.__w3d['%s']; if (f) f(null, this.progress()); } }, %.3f);" % (d, c, self.t_in),
            "tl.fromTo('#host-%s', { opacity:1 }, { opacity:0, duration:%.3f, ease:'power2.in', immediateRender:false }, %.3f);" % (c, f, self.t_out - f),
            "tl.set('#host-%s', { visibility:'hidden' }, %.3f);" % (c, self.t_out),
        ])
        return {"html": html, "js": js}

    @staticmethod
    def stage(public):
        """Copies three.js and the engine into <public>/vendor (the html imports ./vendor/world3d.js)."""
        d = os.path.join(public, "vendor"); os.makedirs(d, exist_ok=True)
        for f in VENDOR:
            shutil.copy(os.path.join(SK, "assets", "vendor", f), d)

    @staticmethod
    def page(folder, worlds, duration=None):
        """A standalone lab page (no footage, no GSAP): folder/index.html + vendor + fonts, for `npx hyperframes snapshot|render folder`. Worlds must not overlap in time."""
        os.makedirs(os.path.join(folder, "fonts"), exist_ok=True)
        World3D.stage(folder)
        for f in ("Inter.ttf", "PlayfairDisplay-Italic.ttf"):
            shutil.copy(os.path.join(SK, "assets", "fonts", f), os.path.join(folder, "fonts"))
        t0 = min(w.t_in for w in worlds); duration = duration or max(w.t_out for w in worlds) - t0
        body = []
        for w in worlds:
            w0 = World3D.__new__(World3D); w0.__dict__.update(w.__dict__)
            body.append(w0.build(standalone=len(worlds) == 1)["html"])
        show = "" if len(worlds) == 1 else ("<script>window.addEventListener('hf-seek', function(e){ var t = e.detail.time; %s });</script>" % " ".join(
            "var h=document.getElementById('host-%s'); var on=t>=%.3f&&t<%.3f; h.style.visibility=on?'visible':'hidden'; h.style.opacity=on?1:0;" % (w.cid, w.t_in, w.t_out) for w in worlds))
        page = ('<!doctype html>\n<html lang="it"><head><meta charset="utf-8"><title>world3d lab</title><style>\n'
                '@font-face { font-family: "Inter"; src: url("fonts/Inter.ttf"); font-weight: 100 900; }\n'
                '@font-face { font-family: "Playfair Display"; src: url("fonts/PlayfairDisplay-Italic.ttf"); font-weight: 400 900; font-style: italic; }\n'
                'html, body { margin: 0; background: #0A2B1E; } #stage { position: relative; width: 1920px; height: 1080px; overflow: hidden; }\n</style></head><body>\n'
                '<div id="stage" data-composition-id="world3d-lab" data-no-timeline="1" data-start="0" data-duration="%.3f" data-fps="30" data-width="1920" data-height="1080">\n%s\n</div>\n%s\n</body></html>\n'
                % (duration + t0, "\n".join(body), show))
        open(os.path.join(folder, "index.html"), "w", encoding="utf-8").write(page)
        return os.path.join(folder, "index.html")
