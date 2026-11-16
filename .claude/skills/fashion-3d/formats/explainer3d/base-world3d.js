// world3d.js: the engine of the 3D motion plates (formats/world3d.py writes the spec, this draws it with three.js).
// Everything on screen is a pure function of time: HyperFrames renders frames out of order, so nothing here keeps state between frames.
// mount(spec) -> draws spec.id's world on <canvas id="<id>-gl">, moves the DOM labels <div id="<id>-l<n>"> onto their 3D points, and registers
// window.__w3d[<id>](globalTime) so a GSAP proxy can drive it too. Spec: see formats/world3d.py.
import * as THREE from "./three.module.min.js";

const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const lerp = (a, b, k) => a + (b - a) * k;
const smooth = (k) => { k = clamp(k); return k * k * (3 - 2 * k); };
function bezier(x1, y1, x2, y2) {
  const f = (t, a, b) => 3 * (1 - t) * (1 - t) * t * a + 3 * (1 - t) * t * t * b + t * t * t;
  return (x) => { x = clamp(x); let lo = 0, hi = 1; for (let i = 0; i < 24; i++) { const m = (lo + hi) / 2; if (f(m, x1, x2) < x) lo = m; else hi = m; } return f((lo + hi) / 2, y1, y2); };
}
const EASE = { hand: bezier(.54, 0, 0, 1), glide: bezier(.5, 0, .3, 1), smooth, linear: (k) => clamp(k), out: (k) => 1 - Math.pow(1 - clamp(k), 3) };
const prog = (t, a, d, e) => (EASE[e] || smooth)(d > 0 ? (t - a) / d : (t >= a ? 1 : 0));
const softmax = (a, b, k = 0.0006) => 0.5 * (a + b + Math.sqrt((a - b) * (a - b) + k));
const wrap = (a) => { a = (a + Math.PI) % (Math.PI * 2); if (a < 0) a += Math.PI * 2; return a - Math.PI; };
const groove = (a, at, w) => Math.exp(-Math.pow(wrap(a - at) / w, 2));

// ---------- fabric: a twill weave painted once
let _weave;
function weave() {
  if (_weave) return _weave;
  const c = document.createElement("canvas"); c.width = c.height = 256; const g = c.getContext("2d");
  g.fillStyle = "#e6e6e6"; g.fillRect(0, 0, 256, 256); g.lineWidth = 3;
  for (let i = -256; i < 512; i += 8) {
    g.strokeStyle = "#ffffff"; g.beginPath(); g.moveTo(i, 0); g.lineTo(i + 256, 256); g.stroke();
    g.strokeStyle = "#c4c4c4"; g.beginPath(); g.moveTo(i + 4, 0); g.lineTo(i + 260, 256); g.stroke();
  }
  _weave = new THREE.CanvasTexture(c); _weave.wrapS = _weave.wrapT = THREE.RepeatWrapping; _weave.repeat.set(26, 34); _weave.anisotropy = 8; _weave.colorSpace = THREE.SRGBColorSpace;
  return _weave;
}
const fabric = (color) => new THREE.MeshStandardMaterial({ color, roughness: 0.95, metalness: 0, map: weave(), bumpMap: weave(), bumpScale: 1.2, side: THREE.DoubleSide });
const shade = (hex, k) => { const c = new THREE.Color(hex); c.multiplyScalar(k); return c; };

// ---------- a lofted tube: rings of ellipses with a relief function (creases)
function loft(keys, relief, seg = 128, steps = 90) {
  const pos = [], uv = [], idx = [];
  const at = (y) => { let i = 0; while (i < keys.length - 2 && y > keys[i + 1].y) i++; const a = keys[i], b = keys[i + 1], k = smooth((y - a.y) / (b.y - a.y)); return { cx: lerp(a.cx, b.cx, k), rx: lerp(a.rx, b.rx, k), rz: lerp(a.rz, b.rz, k) }; };
  const y0 = keys[0].y, y1 = keys[keys.length - 1].y;
  for (let j = 0; j <= steps; j++) {
    const y = lerp(y0, y1, j / steps), r = at(y);
    for (let i = 0; i <= seg; i++) { const a = (i / seg) * Math.PI * 2, d = relief ? relief(a, y) : 0; pos.push(r.cx + (r.rx + d) * Math.sin(a), y, (r.rz + d) * Math.cos(a)); uv.push(i / seg, (y - y0) / (y1 - y0)); }
  }
  for (let j = 0; j < steps; j++) for (let i = 0; i < seg; i++) { const p = j * (seg + 1) + i; idx.push(p, p + 1, p + seg + 1, p + 1, p + seg + 2, p + seg + 1); }
  const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3)); g.setAttribute("uv", new THREE.Float32BufferAttribute(uv, 2)); g.setIndex(idx); g.computeVertexNormals(); return g;
}

// ---------- the trouser (metres: hem 0, crotch 0.80, waist 1.08): natural waist with side adjusters, double pleats, straight leg, turn-ups
function trouser(o) {
  const color = o.color || "#7b7d5a", cloth = fabric(color), dark = fabric(shade(color, 0.86));
  const gold = new THREE.MeshStandardMaterial({ color: 0xe3c47f, roughness: 0.38, metalness: 0.9 }), horn = new THREE.MeshStandardMaterial({ color: 0x2b2118, roughness: 0.5, metalness: 0.1 });
  const CROTCH = 0.80, WAIST = 1.08, LEG = { cx: 0.116, rx: 0.121, rz: 0.134 }, PL = o.pleats === 0 ? [] : (o.pleats === 1 ? [0.36] : [0.30, 0.54]);
  const hem = o.hem || 0.112, g = new THREE.Group();
  for (const s of [-1, 1]) {
    g.add(new THREE.Mesh(loft([
      { y: 0.00, cx: s * 0.128, rx: hem, rz: hem + 0.006 }, { y: 0.30, cx: s * 0.124, rx: 0.104, rz: 0.112 }, { y: 0.52, cx: s * 0.120, rx: 0.108, rz: 0.118 },
      { y: 0.70, cx: s * LEG.cx, rx: LEG.rx, rz: LEG.rz }, { y: CROTCH, cx: s * LEG.cx, rx: LEG.rx, rz: LEG.rz }],
      (a, y) => 0.005 * groove(a, 0, 0.07) * smooth((0.80 - y) / 0.25) + 0.004 * groove(a, Math.PI, 0.07) - 0.003 * Math.max(0, Math.sin(a * 5 + y * 40 + s)) * smooth((0.25 - y) / 0.25)), cloth));
    if (o.cuff !== false) g.add(new THREE.Mesh(loft([{ y: 0.0, cx: s * 0.128, rx: hem + 0.0045, rz: hem + 0.0105 }, { y: 0.048, cx: s * 0.1275, rx: hem + 0.004, rz: hem + 0.010 }], null, 128, 4), dark));
  }
  const outline = (a) => {                                // the outline of the two leg tops, seen from the centre
    const sn = Math.sin(a), co = Math.cos(a); let best = 0;
    for (const c of [-LEG.cx, LEG.cx]) { const A = sn * sn / (LEG.rx * LEG.rx) + co * co / (LEG.rz * LEG.rz), B = -2 * sn * c / (LEG.rx * LEG.rx), C = c * c / (LEG.rx * LEG.rx) - 1; best = Math.max(best, (-B + Math.sqrt(B * B - 4 * A * C)) / (2 * A)); }
    return best;
  };
  const keys = [{ y: CROTCH, rx: 0.236, rz: 0.142 }, { y: 0.90, rx: 0.226, rz: 0.142 }, { y: 1.00, rx: 0.205, rz: 0.128 }, { y: 1.045, rx: 0.192, rz: 0.118 }];
  const pos = [], uv = [], idx = [], seg = 256, steps = 90;
  for (let j = 0; j <= steps; j++) {
    const y = lerp(CROTCH, 1.045, j / steps); let i0 = 0; while (i0 < keys.length - 2 && y > keys[i0 + 1].y) i0++;
    const k0 = keys[i0], k1 = keys[i0 + 1], kk = smooth((y - k0.y) / (k1.y - k0.y)), rx = lerp(k0.rx, k1.rx, kk), rz = lerp(k0.rz, k1.rz, kk);
    const open = smooth((y - CROTCH) / 0.13), fade = smooth((y - 0.84) / 0.16) * (1 - smooth((y - 1.02) / 0.022));
    for (let i = 0; i <= seg; i++) {
      const a = (i / seg) * Math.PI * 2, sn = Math.sin(a), co = Math.cos(a), ell = 1 / Math.sqrt(sn * sn / (rx * rx) + co * co / (rz * rz));
      let r = lerp(softmax(outline(a), ell * 0.84), ell, open);          // the two legs grow into one body; the dip between them stays shallow and round
      for (const sd of [-1, 1]) for (const p of PL) {                    // a pleat is a fold: a sharp edge towards the fly, a soft slope towards the side seam, opening as it goes down
        const d = wrap(a - sd * p) * sd, wide = 0.05 + 0.05 * (1 - smooth((y - 0.86) / 0.18));
        r += 0.0075 * fade * (d > 0 ? Math.exp(-Math.pow(d / wide, 2)) : Math.exp(-Math.pow(d / 0.010, 2)));
      }
      r -= 0.003 * groove(a, 0, 0.02) * fade;
      pos.push(r * sn, y, r * co); uv.push(i / seg, j / steps * 0.3);
    }
  }
  for (let j = 0; j < steps; j++) for (let i = 0; i < seg; i++) { const q = j * (seg + 1) + i; idx.push(q, q + 1, q + seg + 1, q + 1, q + seg + 2, q + seg + 1); }
  const sg = new THREE.BufferGeometry(); sg.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3)); sg.setAttribute("uv", new THREE.Float32BufferAttribute(uv, 2)); sg.setIndex(idx); sg.computeVertexNormals();
  g.add(new THREE.Mesh(sg, cloth));
  g.add(new THREE.Mesh(loft([{ y: 1.040, cx: 0, rx: 0.1965, rz: 0.1215 }, { y: WAIST, cx: 0, rx: 0.190, rz: 0.117 }], null, 128, 6), dark));
  for (const s of [-1, 1]) {
    const tab = new THREE.Mesh(new THREE.BoxGeometry(0.006, 0.02, 0.11), dark); tab.position.set(s * 0.1955, 1.060, -0.02); g.add(tab);
    const b = new THREE.Mesh(new THREE.TorusGeometry(0.0095, 0.0018, 10, 28), gold); b.rotation.y = Math.PI / 2; b.scale.set(1, 1, 1.5); b.position.set(s * 0.1985, 1.060, 0.03); g.add(b);
  }
  const bt = new THREE.Mesh(new THREE.CylinderGeometry(0.0062, 0.0062, 0.003, 24), horn); bt.rotation.x = Math.PI / 2; bt.position.set(0.014, 1.062, 0.1205); g.add(bt);
  const body = new THREE.Group(); g.scale.set(0.9, 1, 0.94); body.add(g); return body;
}

// ---------- a card in space: ivory sheet with a title (one *key* word in the italic serif), a small line, or a picture
function roundRect(w, h, r) {
  const s = new THREE.Shape(), x = -w / 2, y = -h / 2;
  s.moveTo(x + r, y); s.lineTo(x + w - r, y); s.quadraticCurveTo(x + w, y, x + w, y + r); s.lineTo(x + w, y + h - r); s.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
  s.lineTo(x + r, y + h); s.quadraticCurveTo(x, y + h, x, y + h - r); s.lineTo(x, y + r); s.quadraticCurveTo(x, y, x + r, y);
  const g = new THREE.ShapeGeometry(s, 12), p = g.attributes.position, uv = [];
  for (let i = 0; i < p.count; i++) uv.push((p.getX(i) + w / 2) / w, (p.getY(i) + h / 2) / h);
  g.setAttribute("uv", new THREE.Float32BufferAttribute(uv, 2)); return g;
}
function cardTexture(o, img) {
  const W = 1024, H = Math.round(W * o.h / o.w), c = document.createElement("canvas"); c.width = W; c.height = H; const g = c.getContext("2d");
  g.fillStyle = o.color || "#f4efe6"; g.fillRect(0, 0, W, H);
  let top = 0;
  if (img) {                                             // the picture fills the card, or its upper part when there is a title under it
    const ih = o.text ? H * 0.72 : H, k = Math.max(W / img.width, ih / img.height), dw = img.width * k, dh = img.height * k;
    g.save(); g.beginPath(); g.rect(0, 0, W, ih); g.clip(); g.drawImage(img, (W - dw) / 2, (ih - dh) / 2, dw, dh); g.restore(); top = ih;
  }
  if (o.text) {
    const size = o.size || Math.round(H * (img ? 0.11 : 0.2)), parts = String(o.text).split("*"); let wsum = 0;
    const font = (k) => (k % 2 ? "italic 500 " + Math.round(size * 1.12) + 'px "Playfair Display", Georgia, serif' : "800 " + size + 'px "Inter", "Segoe UI", sans-serif');
    parts.forEach((s, k) => { g.font = font(k); wsum += g.measureText(s).width; });
    let x = (W - wsum) / 2; const y = img ? top + (H - top) / 2 : (o.sub ? H * 0.46 : H / 2);
    g.textBaseline = "middle";
    parts.forEach((s, k) => { g.font = font(k); g.fillStyle = k % 2 ? (o.key || "#8a6a2a") : (o.ink || "#15100b"); g.fillText(s, x, y); x += g.measureText(s).width; });
    if (o.sub && !img) { g.font = "500 " + Math.round(size * 0.46) + 'px "Inter", "Segoe UI", sans-serif'; g.fillStyle = "rgba(21,16,11,.66)"; g.textAlign = "center"; g.fillText(o.sub, W / 2, H * 0.72); }
  }
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; return t;
}
function card(o, img) {
  const m = new THREE.Mesh(roundRect(o.w, o.h, o.radius ?? Math.min(o.w, o.h) * 0.07), new THREE.MeshStandardMaterial({ map: cardTexture(o, img), roughness: 0.82, metalness: 0, side: THREE.DoubleSide }));
  const back = new THREE.Mesh(roundRect(o.w, o.h, o.radius ?? Math.min(o.w, o.h) * 0.07), new THREE.MeshBasicMaterial({ color: 0x000000, transparent: true, opacity: 0.28 }));
  back.position.set(0.012, -0.018, -0.02); const g = new THREE.Group(); g.add(back); g.add(m); return g;
}
function solid(o) {
  const mat = o.fabric ? fabric(o.color || "#7b7d5a") : new THREE.MeshStandardMaterial({ color: o.color || "#f4efe6", roughness: o.rough ?? 0.6, metalness: o.metal ?? 0 });
  const s = o.size || [0.3, 0.3, 0.3];
  const geo = o.type === "sphere" ? new THREE.SphereGeometry(s[0] / 2, 48, 32) : o.type === "cyl" ? new THREE.CylinderGeometry(s[0] / 2, s[0] / 2, s[1], 64) : new THREE.BoxGeometry(s[0], s[1], s[2]);
  return new THREE.Mesh(geo, mat);
}
const loadImage = (src) => new Promise((ok) => { const i = new Image(); i.onload = () => ok(i); i.onerror = () => ok(null); i.src = src; });

// ---------- keyframed values: [{t, d, to, ease}] applied in order from a start value; each is a pure function of t
function track(start, keys, t) {
  let v = Array.isArray(start) ? start.slice() : start;
  for (const k of keys || []) {
    const p = prog(t, k.t, k.d ?? 1, k.ease || "glide");
    if (p <= 0) break;
    v = Array.isArray(v) ? v.map((x, i) => lerp(x, k.to[i], p)) : lerp(v, k.to, p);
  }
  return v;
}

export function mount(spec) {
  const W = spec.w || 1920, H = spec.h || 1080, DUR = spec.dur;
  const host = document.getElementById("host-" + spec.id);
  const T0 = host && host.dataset.start != null ? parseFloat(host.dataset.start) : (spec.t_in || 0);     // the host's data-start wins: a recut moves it, the spec does not know
  const canvas = document.getElementById(spec.id + "-gl");
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1); renderer.setSize(W, H, false); renderer.outputColorSpace = THREE.SRGBColorSpace; renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = spec.exposure || 1.3;
  const scene = new THREE.Scene(), camera = new THREE.PerspectiveCamera(spec.fov || 32, W / H, 0.05, 60);
  const key = new THREE.DirectionalLight(0xfff1de, 2.7); key.position.set(1.6, 2.4, 2.2); scene.add(key);          // warm key, cool rim in the preset's mint, a low fill
  const rim = new THREE.DirectionalLight(0x8fe8c4, 2.0); rim.position.set(-2.0, 1.6, -2.2); scene.add(rim);
  const side = new THREE.DirectionalLight(0xfff4e0, 0.7); side.position.set(-2.2, 0.8, 1.4); scene.add(side);
  scene.add(new THREE.HemisphereLight(0xe9f5ee, 0x0a2b1e, 0.55));
  const items = {}, labels = [], grid = document.getElementById(spec.id + "-grid"), svg = document.getElementById(spec.id + "-ln");
  const v = new THREE.Vector3(), look = new THREE.Vector3();

  function build(imgs) {
    (spec.objects || []).forEach((o, n) => {
      const m = o.type === "trouser" ? trouser(o) : o.type === "card" ? card(o, imgs[n]) : solid(o);
      const g = new THREE.Group(); g.add(m); if (o.scale) m.scale.multiplyScalar(o.scale);
      scene.add(g); items[o.id] = { o, g };
      if (o.shadow) {
        const c = document.createElement("canvas"); c.width = c.height = 256; const x = c.getContext("2d"), r = x.createRadialGradient(128, 128, 8, 128, 128, 128);
        r.addColorStop(0, "rgba(0,0,0,.62)"); r.addColorStop(1, "rgba(0,0,0,0)"); x.fillStyle = r; x.fillRect(0, 0, 256, 256);
        const s = new THREE.Mesh(new THREE.PlaneGeometry(o.shadow[0], o.shadow[1]), new THREE.MeshBasicMaterial({ map: new THREE.CanvasTexture(c), transparent: true, depthWrite: false }));
        s.rotation.x = -Math.PI / 2; s.position.set(o.pos[0], (o.floor ?? o.pos[1]) + 0.002, o.pos[2]); scene.add(s);
      }
    });
    (spec.labels || []).forEach((L, n) => {
      const el = document.getElementById(spec.id + "-l" + n); if (!el || !svg) return;
      const line = document.createElementNS("http://www.w3.org/2000/svg", "line"); line.setAttribute("stroke", "#e3c47f"); line.setAttribute("stroke-width", "3"); line.setAttribute("stroke-dasharray", "2 10"); line.setAttribute("stroke-linecap", "round");
      const dot = document.createElementNS("http://www.w3.org/2000/svg", "circle"); dot.setAttribute("r", "8"); dot.setAttribute("fill", "#e3c47f");
      svg.appendChild(line); svg.appendChild(dot); labels.push({ L, el, line, dot, p: new THREE.Vector3(...L.p) });
    });
  }

  function renderAt(global) {
    const t = clamp(global - T0, 0, DUR), life = t / DUR;
    for (const id in items) {
      const { o, g } = items[id], p = track(o.pos || [0, 0, 0], o.move, t), r = track(o.rot || [0, 0, 0], o.turn, t);
      const a = o.t == null ? 1 : prog(t, o.t, 0.6, "out");                      // an object that enters: rises 12 cm and fades in on its time
      g.position.set(p[0], p[1] - 0.12 * (1 - a), p[2]); g.rotation.set(r[0], r[1], r[2]); g.visible = a > 0.001;
      g.traverse((m) => { if (m.material && o.t != null) { m.material.transparent = true; m.material.opacity = (m.material.userData.o ?? (m.material.userData.o = m.material.opacity)) * a; } });
    }
    const c0 = spec.cam[0], pos = track(c0.pos, spec.cam.slice(1).map((k) => ({ t: k.t, d: k.d, to: k.pos, ease: k.ease || "hand" })), t);
    const lk = track(c0.look, spec.cam.slice(1).map((k) => ({ t: k.t, d: k.d, to: k.look, ease: k.ease || "hand" })), t);
    look.set(lk[0], lk[1], lk[2]); camera.position.set(pos[0], pos[1], pos[2]);
    camera.position.lerp(look, 0.05 * life);                                     // never still: a slow push towards what it looks at, the whole life of the plate
    camera.lookAt(look); camera.updateMatrixWorld(); scene.updateMatrixWorld(true);
    renderer.render(scene, camera);
    if (grid) grid.style.transform = "translate(" + (-(camera.position.x * 60) - 28 * life).toFixed(2) + "px," + ((camera.position.y - c0.pos[1]) * 40 - 14 * life).toFixed(2) + "px)";   // the grid follows at a fraction of the camera: depth
    for (const { L, el, line, dot, p } of labels) {
      v.copy(p); if (L.obj && items[L.obj]) v.applyMatrix4(items[L.obj].g.matrixWorld); v.project(camera);
      const x = (v.x * 0.5 + 0.5) * W, y = (-v.y * 0.5 + 0.5) * H, k = prog(t, L.t, 0.5, "out") * (L.out == null ? 1 : 1 - prog(t, L.out, 0.35, "smooth"));
      const lx = x + L.dx, ly = y + L.dy + 18 * (1 - prog(t, L.t, 0.5, "out")), w = el.offsetWidth, h = el.offsetHeight;
      el.style.opacity = k; el.style.transform = "translate(" + lx.toFixed(1) + "px," + ly.toFixed(1) + "px)";
      const ex = L.dx > 0 ? lx : lx + w, ey = ly + h / 2, d = prog(t, L.t + 0.15, 0.45, "smooth");                 // the dashed link draws only after its label exists
      line.setAttribute("x1", x.toFixed(1)); line.setAttribute("y1", y.toFixed(1)); line.setAttribute("x2", lerp(x, ex, d).toFixed(1)); line.setAttribute("y2", lerp(y, ey, d).toFixed(1));
      line.setAttribute("opacity", k); dot.setAttribute("cx", x.toFixed(1)); dot.setAttribute("cy", y.toFixed(1)); dot.setAttribute("opacity", k);
    }
    for (const tx of spec.texts || []) {                                         // title and sub: in on their time
      const el = document.getElementById(tx.id); if (!el) continue; const k = prog(t, tx.t, 0.45, "out") * (tx.out == null ? 1 : 1 - prog(t, tx.out, 0.35, "smooth"));
      el.style.opacity = k; el.style.transform = "translateY(" + (14 * (1 - k)).toFixed(2) + "px)";
    }
  }

  let last = T0;
  const ready = Promise.all([document.fonts.load('800 40px "Inter"'), document.fonts.load('italic 500 40px "Playfair Display"'), document.fonts.ready,
    ...(spec.objects || []).map((o) => (o.type === "card" && o.img ? loadImage(o.img) : Promise.resolve(null)))])
    .then((r) => { build(r.slice(3)); return renderer.compileAsync(scene, camera); }).then(() => { window.__w3d[spec.id] = (g, p) => { last = p == null ? g : T0 + p * DUR; renderAt(last); }; renderAt(last); });
  window.__w3d = window.__w3d || {}; window.__w3d[spec.id] = (g, p) => { last = p == null ? g : T0 + p * DUR; };      // (globalTime) or (null, progress 0-1 of the plate)
  window.__hf = window.__hf || {}; window.__hf.buildReady = window.__hf.buildReady || {}; window.__hf.buildReady["w3d-" + spec.id] = ready;
  window.addEventListener("hf-seek", (e) => { window.__w3d[spec.id](e.detail.time); e.detail.waitUntil && e.detail.waitUntil(ready); });
}
