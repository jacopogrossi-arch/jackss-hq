// world3d.js: the engine of the 3D motion plates (formats/world3d.py writes the spec, this draws it with three.js).
// Everything on screen is a pure function of time: HyperFrames renders frames out of order, so nothing here keeps state between frames.
// mount(spec) -> draws spec.id's world on <canvas id="<id>-gl">, moves the DOM labels <div id="<id>-l<n>"> onto their 3D points, and registers
// window.__w3d[<id>](globalTime) so a GSAP proxy can drive it too. Spec: see formats/world3d.py.
import * as THREE from "./three.module.min.js";
import { build as kitBuild, KIT } from "./atelier-kit.js";

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
      (a, y) => 0.005 * groove(a, 0, 0.07) * smooth((0.80 - y) / 0.25) + 0.004 * groove(a, Math.PI, 0.07) - 0.003 * Math.max(0, Math.sin(a * 5 + y * 40 + s)) * smooth((0.25 - y) / 0.25)
        + 0.0024 * Math.sin(a * 3 + y * 75 + s) * Math.exp(-Math.pow((y - 0.55) / 0.11, 2)) * groove(a, 0, 1.0) + 0.0045 * groove(a, 0, 0.7) * smooth((0.1 - y) / 0.1)), cloth));       // knee creases, a slight break over the shoe
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
  // ---- details (14/11/2026: the first trouser read as two tubes): slanted side pockets, back welt pockets, belt loops, the fly, knee creases, an optional hanger
  const darkM = fabric(shade(color, 0.62)), bodyR = (y, a) => {         // radius of the hip body at height y and angle a (same recipe as the loop above, without the pleats)
    let i0 = 0; while (i0 < keys.length - 2 && y > keys[i0 + 1].y) i0++;
    const k0 = keys[i0], k1 = keys[i0 + 1], kk = smooth((y - k0.y) / (k1.y - k0.y)), rx = lerp(k0.rx, k1.rx, kk), rz = lerp(k0.rz, k1.rz, kk), sn = Math.sin(a), co = Math.cos(a), ell = 1 / Math.sqrt(sn * sn / (rx * rx) + co * co / (rz * rz));
    return lerp(softmax(outline(a), ell * 0.84), ell, smooth((y - CROTCH) / 0.13));
  };
  const seam = (pts, r = 0.0022, mat = darkM) => g.add(new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts.map((p) => new THREE.Vector3(...p))), 20, r, 5, false), mat));
  const onBody = (y, a, off = 0.0026) => { const r = bodyR(y, a) + off; return [r * Math.sin(a), y, r * Math.cos(a)]; };
  for (const s of [-1, 1]) {
    const pk = []; for (let k = 0; k <= 8; k++) { const u = k / 8; pk.push(onBody(lerp(1.025, 0.865, u), s * lerp(1.12, 0.80, Math.pow(u, 1.2)))); } seam(pk, 0.0026);       // the slanted pocket opening
    if (o.pockets !== false) { const bw = []; for (let k = 0; k <= 5; k++) bw.push(onBody(1.0, s * lerp(Math.PI - 0.62, Math.PI - 0.26, k / 5), 0.0016)); seam(bw, 0.0028); const bw2 = []; for (let k = 0; k <= 5; k++) bw2.push(onBody(0.975, s * lerp(Math.PI - 0.62, Math.PI - 0.26, k / 5), 0.0016)); seam(bw2, 0.0028); }
  }
  { const f = []; for (let k = 0; k <= 8; k++) { const u = k / 8; f.push([0.012 * smooth((u - 0.65) / 0.35), lerp(1.04, 0.845, u), bodyR(lerp(1.04, 0.845, u), 0.03 * smooth((u - 0.65) / 0.35)) + 0.0024]); } seam(f, 0.0016); }
  for (const a of [-1.38, -0.92, -0.5, 0.5, 0.92, 1.38, Math.PI - 0.25, Math.PI + 0.25]) {                     // belt loops on the waistband
    const r = 1 / Math.sqrt(Math.sin(a) ** 2 / (0.19 * 0.19) + Math.cos(a) ** 2 / (0.117 * 0.117)) + 0.002, lp = new THREE.Mesh(new THREE.BoxGeometry(0.015, 0.05, 0.006), dark); lp.position.set(r * Math.sin(a), 1.062, r * Math.cos(a)); lp.rotation.y = a; g.add(lp);
  }
  const body = new THREE.Group(); g.scale.set(0.9, 1, 0.94); body.add(g);
  if (o.hang != null) {                                                  // hung from a wooden trouser hanger on a cord that runs up out of frame
    const wood = new THREE.MeshStandardMaterial({ color: 0xb98a5a, roughness: 0.55 }), steel = new THREE.MeshStandardMaterial({ color: 0xc9ccd1, roughness: 0.3, metalness: 0.9 });
    const bar = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.016, 0.03), wood); bar.position.set(0, 1.108, 0); body.add(bar);
    for (const sx of [-0.15, 0.15]) { const c = new THREE.Mesh(new THREE.BoxGeometry(0.028, 0.05, 0.16), steel); c.position.set(sx, 1.085, 0); body.add(c); }
    const hk = new THREE.Mesh(new THREE.TorusGeometry(0.02, 0.0028, 8, 18, Math.PI * 1.5), steel); hk.position.set(0, 1.145, 0); hk.rotation.z = Math.PI * 0.75; body.add(hk);
    const cord = new THREE.Mesh(new THREE.CylinderGeometry(0.0025, 0.0025, o.hang, 6), new THREE.MeshStandardMaterial({ color: 0x1e1b18, roughness: 0.9 })); cord.position.set(0, 1.165 + o.hang / 2, 0); cord.userData.noshadow = true; body.add(cord);
  }
  return body;
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
  const tex = cardTexture(o, img), m = new THREE.Mesh(roundRect(o.w, o.h, o.radius ?? Math.min(o.w, o.h) * 0.07), o.flat ? new THREE.MeshBasicMaterial({ map: tex, toneMapped: false, side: THREE.DoubleSide }) : new THREE.MeshStandardMaterial({ map: tex, roughness: 0.82, metalness: 0, side: THREE.DoubleSide }));
  m.userData.flat = !!o.flat;
  const back = new THREE.Mesh(roundRect(o.w, o.h, o.radius ?? Math.min(o.w, o.h) * 0.07), new THREE.MeshBasicMaterial({ color: 0x000000, transparent: true, opacity: 0.28 }));
  back.position.set(0.012, -0.018, -0.02); const g = new THREE.Group(); g.add(back); g.add(m); return g;
}
function solid(o) {
  if (KIT.has(o.type)) return kitBuild(o, { fabric, shade });
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

// ---------- looks for the render passes (13/11/2026, from the @holcdenis teardown): "final" (lit), "clay" (flat grey, no stripes) and "ink" (paper + black outlines).
const PAPER = 0xefe9dd, CLAY = 0xc4bdaf, INK = new THREE.Color(0x1e1b18);
const hullMat = new THREE.ShaderMaterial({                // inverted hull: the back faces pushed out along the normal, in view space, scaled by distance (constant line width)
  side: THREE.BackSide, uniforms: { w: { value: 0.0045 } }, toneMapped: false,
  vertexShader: "uniform float w; void main(){ vec4 p = modelViewMatrix * vec4(position, 1.0); vec3 n = normalize(normalMatrix * normal); p.xyz += n * w * (-p.z); gl_Position = projectionMatrix * p; }",
  fragmentShader: "void main(){ gl_FragColor = vec4(0.118, 0.106, 0.094, 1.0); }" });
const lineMat = new THREE.LineBasicMaterial({ color: 0x1e1b18, toneMapped: false });
const inkFill = new THREE.MeshBasicMaterial({ color: PAPER, toneMapped: false, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1, side: THREE.DoubleSide });
const hash = (i) => { const s = Math.sin(i * 12.9898 + 78.233) * 43758.5453; return s - Math.floor(s); };

export function mount(spec) {
  const W = spec.w || 1920, H = spec.h || 1080, DUR = spec.dur, LOOK = spec.look || null, ROOM = spec.room || null;
  const host = document.getElementById("host-" + spec.id);
  const T0 = host && host.dataset.start != null ? parseFloat(host.dataset.start) : (spec.t_in || 0);     // the host's data-start wins: a recut moves it, the spec does not know
  const canvas = document.getElementById(spec.id + "-gl");
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, preserveDrawingBuffer: true });
  const PR = Math.max(1, Math.min(2, window.devicePixelRatio || 1)); renderer.setPixelRatio(PR); renderer.setSize(W, H, false); renderer.outputColorSpace = THREE.SRGBColorSpace; renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = spec.exposure || 1.3;
  const scene = new THREE.Scene(), camera = new THREE.PerspectiveCamera(spec.fov || 32, W / H, 0.05, 60);
  const key = new THREE.DirectionalLight(0xfff1de, 2.7); key.position.set(1.6, 2.4, 2.2); scene.add(key);          // warm key, cool rim in the preset's mint, a low fill
  const rim = new THREE.DirectionalLight(0x8fe8c4, 2.0); rim.position.set(-2.0, 1.6, -2.2); scene.add(rim);
  const side = new THREE.DirectionalLight(0xfff4e0, 0.7); side.position.set(-2.2, 0.8, 1.4); scene.add(side);
  const hemi = new THREE.HemisphereLight(0xe9f5ee, 0x0a2b1e, 0.55); scene.add(hemi);
  const items = {}, labels = [], grid = document.getElementById(spec.id + "-grid"), svg = document.getElementById(spec.id + "-ln");
  const v = new THREE.Vector3(), look = new THREE.Vector3();
  const mb = document.getElementById(spec.id + "-mb"), mbx = mb ? mb.getContext("2d") : null, bar = document.getElementById(spec.id + "-bar"), bart = document.getElementById(spec.id + "-bart");
  if (mb) { mb.width = Math.round(W * PR); mb.height = Math.round(H * PR); }
  // the three looks and what each one does to the scene
  const dressed = [], inkOnly = [], onlyFinal = [], notInk = [], clayMats = new Map(); let slats = null, dust = null, mode = null;
  const LIGHTS = ROOM ? { final: [ROOM.key_i ?? 3.2, ROOM.rim_i ?? 0.5, ROOM.side_i ?? 0, ROOM.hemi_i ?? 0.9], clay: [1.5, 0, 0.5, 1.0] } : LOOK ? { final: [4.6, 0, 1.2, 1.5], clay: [2.4, 0, 0.5, 0.8] } : { final: [2.7, 2.0, 0.7, 0.55], clay: [1.5, 0, 0.5, 1.0] };   // key, rim, side, hemisphere
  if (LOOK) {                                                  // an atelier: one warm key through blinds, a dark room, a floor that catches the stripes
    renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap; if (spec.exposure == null) renderer.toneMappingExposure = 1.45; side.position.set(2.2, 0.9, 1.8);
    const d = LOOK.dir || [-2.4, 1.5, 1.7]; key.color.set(LOOK.key || "#ffc98a"); key.position.set(d[0], d[1], d[2]); key.target.position.set(0, 0.65, 0); scene.add(key.target);
    key.castShadow = true; key.shadow.mapSize.set(2048, 2048); key.shadow.bias = -0.0004; key.shadow.normalBias = 0.02; key.shadow.radius = 3;
    Object.assign(key.shadow.camera, { left: -2.2, right: 2.2, top: 2.2, bottom: -2.2, near: 0.3, far: 9 }); key.shadow.camera.updateProjectionMatrix();
    hemi.color.set(0x5a4332); hemi.groundColor.set(0x120c08); side.color.set(0x7fa08a);
    slats = new THREE.Group(); const n = LOOK.slats ?? 9, gap = LOOK.gap ?? 0.30, th = LOOK.thick ?? 0.09, nm = new THREE.MeshBasicMaterial({ colorWrite: false, depthWrite: false });
    for (let i = 0; i < n; i++) { const b = new THREE.Mesh(new THREE.BoxGeometry(3.6, th, 0.012), nm); b.position.y = (i - (n - 1) / 2) * gap; b.castShadow = true; b.userData.y0 = b.position.y; slats.add(b); }
    slats.position.copy(key.target.position).addScaledVector(key.position.clone().sub(key.target.position).normalize(), 1.3); slats.lookAt(key.target.position); scene.add(slats);
    if (LOOK.dust !== false) {                                 // dust in the light: a pure function of time (positions from a hash, no random)
      const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.Float32BufferAttribute(new Float32Array(360), 3));
      dust = new THREE.Points(g, new THREE.PointsMaterial({ color: 0xffe2b0, size: 0.011, transparent: true, opacity: 0.55, depthWrite: false, blending: THREE.AdditiveBlending })); dust.frustumCulled = false; scene.add(dust);
    }
  }
  if (ROOM) {                                                  // a lit room (14/11/2026): daylight through the window as the key, real shadows, a warm ambient, fog; props come from atelier-kit.js
    renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap; renderer.toneMappingExposure = spec.exposure ?? 1.15;
    const d = ROOM.dir || [-6, 5, 2.5], sb = ROOM.box || [6, 5, 30]; key.color.set(ROOM.key || "#fff0d8"); key.position.set(d[0], d[1], d[2]); key.target.position.set(...(ROOM.aim || [0, 0.8, 0])); scene.add(key.target);
    key.castShadow = true; key.shadow.mapSize.set(ROOM.map || 4096, ROOM.map || 4096); key.shadow.bias = -0.0004; key.shadow.normalBias = 0.025; key.shadow.radius = ROOM.soft ?? 4;
    Object.assign(key.shadow.camera, { left: -sb[0], right: sb[0], top: sb[1], bottom: -sb[1], near: 0.5, far: sb[2] }); key.shadow.camera.updateProjectionMatrix();
    rim.color.set(ROOM.rim || "#a9bfe8"); rim.position.set(ROOM.rim_dir ? ROOM.rim_dir[0] : 3, ROOM.rim_dir ? ROOM.rim_dir[1] : 3, ROOM.rim_dir ? ROOM.rim_dir[2] : -4); side.color.set(ROOM.side || "#ffe9cf"); side.position.set(2.5, 1.5, 3.5);
    hemi.color.set(ROOM.hemi ? ROOM.hemi[0] : "#fff0dd"); hemi.groundColor.set(ROOM.hemi ? ROOM.hemi[1] : "#6b4a30");
    if (ROOM.fog) scene.fog = new THREE.Fog(ROOM.fog[0], ROOM.fog[1], ROOM.fog[2]);
    camera.far = ROOM.far || 80; camera.updateProjectionMatrix();
  }
  function dressMesh(mesh, m) {                                 // one mesh in one look (an object can carry its own look: o.pass_mode)
    if (m === "final") mesh.material = mesh.userData.orig;
    else if (m === "ink") mesh.material = inkFill;
    else { const o = mesh.userData.orig, k = o.color ? o.color.getHex() : CLAY; if (!clayMats.has(k)) clayMats.set(k, new THREE.MeshLambertMaterial({ color: new THREE.Color(k).lerp(new THREE.Color(CLAY), 0.7), side: THREE.DoubleSide })); mesh.material = clayMats.get(k); }
  }
  function setMode(m) {
    if (m === mode) return; mode = m; const f = m === "final", c = m === "clay";
    for (const mesh of dressed) dressMesh(mesh, mesh.userData.pass || m);
    for (const h of inkOnly) h.visible = (h.userData.mesh.userData.pass || m) === "ink";
    for (const h of onlyFinal) h.visible = f;
    for (const h of notInk) h.visible = m !== "ink";
    if (slats) slats.visible = f; if (dust) dust.visible = f;
    const L = LIGHTS[f ? "final" : "clay"]; key.intensity = L[0]; rim.intensity = L[1]; side.intensity = L[2]; hemi.intensity = L[3];
    if (LOOK) {                                                  // the clay pass is neutral and shadowless: no warm light, no stripes, no cast shadows
      key.color.set(f ? (LOOK.key || "#ffc98a") : "#ffffff"); side.color.set(f ? 0x7fa08a : 0xffffff); key.castShadow = f;
      hemi.color.set(f ? 0x5a4332 : 0xffffff); hemi.groundColor.set(f ? 0x120c08 : 0x9a9388);
    }
    renderer.setClearColor(m === "ink" ? PAPER : c ? CLAY : (ROOM ? new THREE.Color(ROOM.bg || "#1b1511") : LOOK ? new THREE.Color(LOOK.bg || "#14100c") : 0x000000), f && !LOOK && !ROOM ? 0 : 1);
  }
  const passState = (t) => {                                    // the wipe bar: what is under it, what is coming in, where the edge is
    let cur = spec.base || "final";
    for (const e of spec.passes || []) { const p = prog(t, e.t, e.d ?? 0.7, "hand"); if (p < 0.0005) break; if (p < 0.9995) return { a: cur, b: e.to, edge: p * W, p }; cur = e.to; }   // thresholds: the bezier never returns exactly 0 or 1
    return { a: cur };
  };

  function build(imgs) {
    (spec.objects || []).forEach((o, n) => {
      const m = o.type === "trouser" ? (o.hi ? kitBuild(o, { fabric, shade }) : trouser(o)) : o.type === "card" ? card(o, imgs[n]) : solid(o);
      const g = new THREE.Group(); g.add(m); if (o.scale) m.scale.multiplyScalar(o.scale);
      scene.add(g); items[o.id] = { o, g };
      const meshes = []; g.traverse((x) => { if (x.isMesh) meshes.push(x); });                      // dress it for the passes: ink outlines (hull for round things, edge lines for boxes and sheets)
      for (const x of meshes) {
        if (x.material.type === "MeshBasicMaterial" && x.material.transparent) { notInk.push(x); onlyFinal.push(x); continue; }   // the card's soft back plate
        x.userData.orig = x.material; x.userData.pass = o.pass_mode || null;
        if (LOOK || ROOM) { const ns = x.userData.flat || x.userData.noshadow || x.material.isMeshBasicMaterial; x.castShadow = !ns && !x.userData.floor; x.receiveShadow = !x.userData.flat; }
        if (KIT.has(o.type) || o.hi) continue;                                 // props live in one look: no ink/clay dressing (saves a hull mesh per mesh)
        dressed.push(x);
        if (o.type === "box" || o.type === "card") { const e = new THREE.LineSegments(new THREE.EdgesGeometry(x.geometry, 30), lineMat); e.userData.mesh = x; e.visible = false; x.add(e); inkOnly.push(e); }
        else { const h = new THREE.Mesh(x.geometry, hullMat); h.userData.mesh = x; h.visible = false; x.add(h); inkOnly.push(h); }
      }
      if (o.shadow && !LOOK && !ROOM) {
        const c = document.createElement("canvas"); c.width = c.height = 256; const x = c.getContext("2d"), r = x.createRadialGradient(128, 128, 8, 128, 128, 128);
        r.addColorStop(0, "rgba(0,0,0,.62)"); r.addColorStop(1, "rgba(0,0,0,0)"); x.fillStyle = r; x.fillRect(0, 0, 256, 256);
        const s = new THREE.Mesh(new THREE.PlaneGeometry(o.shadow[0], o.shadow[1]), new THREE.MeshBasicMaterial({ map: new THREE.CanvasTexture(c), transparent: true, depthWrite: false }));
        s.rotation.x = -Math.PI / 2; s.position.set(o.pos[0], (o.floor ?? o.pos[1]) + 0.002, o.pos[2]); scene.add(s);
      }
    });
    if (LOOK) {                                                  // the floor that catches the stripes (hidden in the ink pass: the paper is the floor)
      const fl = new THREE.Mesh(new THREE.PlaneGeometry(14, 14), new THREE.MeshStandardMaterial({ color: LOOK.floor || "#2b1d13", roughness: 0.92, metalness: 0 }));
      fl.rotation.x = -Math.PI / 2; fl.position.y = LOOK.floor_y ?? 0; fl.receiveShadow = true; fl.userData.orig = fl.material; scene.add(fl); dressed.push(fl); notInk.push(fl);
      if (LOOK.wall !== false) {                                 // a back wall: it catches the stripes too, and gives the room a depth
        const wl = new THREE.Mesh(new THREE.PlaneGeometry(14, 6), new THREE.MeshStandardMaterial({ color: LOOK.wall || "#3b2b20", roughness: 0.95, metalness: 0 }));
        wl.position.set(0, 3, LOOK.wall_z ?? -1.7); wl.receiveShadow = true; wl.userData.orig = wl.material; scene.add(wl); dressed.push(wl); notInk.push(wl);
      }
    }
    (spec.labels || []).forEach((L, n) => {
      const el = document.getElementById(spec.id + "-l" + n); if (!el || !svg) return;
      const line = document.createElementNS("http://www.w3.org/2000/svg", "line"); line.setAttribute("stroke", "#e3c47f"); line.setAttribute("stroke-width", "3"); line.setAttribute("stroke-dasharray", "2 10"); line.setAttribute("stroke-linecap", "round");
      const dot = document.createElementNS("http://www.w3.org/2000/svg", "circle"); dot.setAttribute("r", "8"); dot.setAttribute("fill", "#e3c47f");
      svg.appendChild(line); svg.appendChild(dot); labels.push({ L, el, line, dot, p: new THREE.Vector3(...L.p) });
    });
  }

  const c0 = spec.cam[0], camP = spec.cam.slice(1).map((k) => ({ t: k.t, d: k.d, to: k.pos, ease: k.ease || "hand" })), camL = spec.cam.slice(1).map((k) => ({ t: k.t, d: k.d, to: k.look, ease: k.ease || "hand" }));
  function poseObjects(t) {
    for (const id in items) {
      const { o, g } = items[id], p = track(o.pos || [0, 0, 0], o.move, t), r = track(o.rot || [0, 0, 0], o.turn, t);
      const a = o.t == null ? 1 : prog(t, o.t, 0.6, "out");                      // an object that enters: rises 12 cm and fades in on its time
      g.position.set(p[0], p[1] - 0.12 * (1 - a), p[2]); g.rotation.set(r[0], r[1], r[2]); g.visible = a > 0.001;
      g.traverse((m) => { if (m.material && o.t != null && m.userData.orig === m.material) { m.material.transparent = true; m.material.opacity = (m.material.userData.o ?? (m.material.userData.o = m.material.opacity)) * a; } });
    }
    if (slats) for (const b of slats.children) b.position.y = b.userData.y0 + 0.012 * t;      // the sun creeps: the stripes drift across the room
  }
  function aimCamera(t) {                                                       // camera pose at time t (clamped), without any jitter
    t = clamp(t, 0, DUR); const pos = track(c0.pos, camP, t), lk = track(c0.look, camL, t);
    look.set(lk[0], lk[1], lk[2]); camera.position.set(pos[0], pos[1], pos[2]);
    camera.position.lerp(look, 0.05 * (t / DUR));                                // never still: a slow push towards what it looks at, the whole life of the plate
    camera.lookAt(look); camera.updateMatrixWorld();
  }
  const camSpeed = (t) => { const h = 0.02; aimCamera(t - h); const a = camera.position.clone(), la = look.clone(); aimCamera(t + h); return (camera.position.distanceTo(a) + 0.5 * look.distanceTo(la)) / (2 * h); };   // m/s
  const dofAt = (t) => { let ap = 0; for (const e of spec.dof || []) { const k = prog(t, e.t, 0.35, "smooth") * (1 - prog(t, e.t + e.d - 0.35, 0.35, "smooth")); ap = Math.max(ap, e.ap * k); } return ap; };
  const rgt = new THREE.Vector3(), upv = new THREE.Vector3();

  function renderAt(global) {
    const t = clamp(global - T0, 0, DUR), life = t / DUR;
    if (dust) { const a = dust.geometry.attributes.position; for (let i = 0; i < 120; i++) { const h1 = hash(i), h2 = hash(i + 500), h3 = hash(i + 900), y = ((h2 * 2.2 + t * (0.03 + 0.05 * h3)) % 2.2); a.setXYZ(i, -1.3 + h1 * 2.6 + 0.06 * Math.sin(t * 0.6 + i), y, -1.0 + h3 * 2.0 + 0.05 * Math.cos(t * 0.5 + i * 1.7)); } a.needsUpdate = true; }
    // motion blur and depth of field: several renders of the same instant (shutter spread over time, lens spread over a disc) averaged on a 2D canvas. Pure function of t.
    const shutter = (spec.shutter ?? 0.8) / 30, sp = shutter > 0 ? camSpeed(t) : 0, ap = dofAt(t);
    let N = sp > 0.6 ? clamp(Math.round(sp * 3), 2, 10) : 1; if (ap > 0) N = Math.max(N, 12);
    for (let i = 0; i < N; i++) {
      const ts = N > 1 && sp > 0.6 ? t + ((i + 0.5) / N - 0.5) * shutter : t;
      poseObjects(ts); aimCamera(ts); scene.updateMatrixWorld(true);
      if (ap > 0) { const fx = look.clone(), r = ap * Math.sqrt((i + 0.5) / N), th = i * 2.39996; rgt.setFromMatrixColumn(camera.matrixWorld, 0); upv.setFromMatrixColumn(camera.matrixWorld, 1); camera.position.addScaledVector(rgt, r * Math.cos(th)).addScaledVector(upv, r * Math.sin(th)); camera.lookAt(fx); camera.updateMatrixWorld(); }
      const ps = passState(ts); setMode(ps.a); renderer.setScissorTest(false); renderer.render(scene, camera);
      if (ps.b) { setMode(ps.b); renderer.setScissorTest(true); renderer.setScissor(0, 0, ps.edge, H); renderer.render(scene, camera); renderer.setScissorTest(false); }
      if (N > 1 && mbx) { if (i === 0) mbx.clearRect(0, 0, mb.width, mb.height); mbx.globalAlpha = 1 / (i + 1); mbx.drawImage(canvas, 0, 0); mbx.globalAlpha = 1; }
    }
    if (mb) { mb.style.display = N > 1 ? "block" : "none"; canvas.style.visibility = N > 1 ? "hidden" : "visible"; }
    if (bar) { const ps = passState(t), on = ps.b != null; bar.style.opacity = on ? 1 : 0; if (on) { bar.style.transform = "translateX(" + (ps.edge - 3).toFixed(1) + "px)"; if (bart) bart.textContent = "FRAME " + String(Math.round(t * 30)).padStart(4, "0") + " · PASS: " + ps.b.toUpperCase(); } }
    poseObjects(t); aimCamera(t); scene.updateMatrixWorld(true);                 // the labels project from the exact instant, not from a sub-sample
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
