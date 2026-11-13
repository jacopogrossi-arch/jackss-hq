// atelier-studio.js (13/11/2026, Short #2 "tre significati"): the props of the Inverso STUDIO at night, a second world next to the atelier.
//   wordblocks  a row of letter cubes (INVERSO) that flip in a wave: upside down at first, upright after the first flip
//   seampanel   a trouser back panel on the table: the right side (welt pocket, seam) and the WRONG side (pressed-open seams, overlock, pocket bag,
//               waistband facing with the woven label). o.flip=[t0,t1] turns it over; o.flipped shows the wrong side from the start; o.dirty = the badly made one
//   fastrail    fast fashion: a rail of identical tees that races past over o.span and empties after o.clear
//   wallclock   a wall clock whose hands race over o.spin=[[t0,t1,turns],...]
//   shoeboxes   six shoe boxes with a 150 € tag; they pop in over o.show, all but one vanish at o.drop
//   sneaker     a plain low-top sneaker (no brand marks)
//   cityview    Rome at night: sky, domes, bell towers, umbrella pines, lit windows (a backdrop outside the window)
//   crittall    a black steel factory window: grid of panes, no glass glare
//   bookshelf   wooden shelves with books, magazines and a few objects
//   pinboard    a cork board with pinned swatches and sketches; o.cards=[{text, sub, t, x, y, rot}] pop in on their time
//   swatchwall  the brand palette painted as five tall strips with names and hex
//   axisline    the diagram on the floor: ostentazione <-> flexing, a puck that moves along it (o.puck=[[t, d, frac], ...])
//   crossmark   a rust X that pops on o.show
//   laptop      an open laptop whose screen shows the brand page
//   deskset     a mug, a notebook and a pencil cup
//   terrazzo    a terrazzo floor with chips in the brand colours
// Same conventions as atelier-kit.js: metres, y up, standing on y = 0, front = +z; deterministic (hash), animation = userData.update(t) pure in t.
import * as THREE from "./three.module.min.js";
import { clothMat, stitches, tube, lerp, clamp, smooth, hash2 } from "./atelier-tex.js";
import { drawLogo } from "./atelier-cut.js";

await Promise.all(['400 100px "Instrument Serif"', 'italic 400 100px "Instrument Serif"', '500 40px "IBM Plex Sans"', '600 40px "IBM Plex Sans"']
  .map((f) => document.fonts.load(f).catch(() => null)));

const SERIF = '"Instrument Serif", "Playfair Display", Georgia, serif', SANS = '"IBM Plex Sans", Inter, "Segoe UI", sans-serif';
const C = { gesso: "#EFE9DD", ink: "#1E1B18", bosco: "#2F3A2E", ruggine: "#8A4B2D", sabbia: "#B9AE98", red: "#b8432a" };
const M = (c, r = 0.6, m = 0) => new THREE.MeshStandardMaterial({ color: c, roughness: r, metalness: m });
function add(g, geo, mat, x = 0, y = 0, z = 0, rx = 0, ry = 0, rz = 0) { const m = new THREE.Mesh(geo, mat); m.position.set(x, y, z); m.rotation.set(rx, ry, rz); g.add(m); return m; }
const B = (w, h, d) => new THREE.BoxGeometry(w, h, d);
const CY = (r1, r2, h, s = 24) => new THREE.CylinderGeometry(r1, r2, h, s);
const cv = (w, h) => { const c = document.createElement("canvas"); c.width = w; c.height = h; return [c, c.getContext("2d")]; };
const tx = (c, rep, srgb = true) => { const t = new THREE.CanvasTexture(c); if (srgb) t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 16; if (rep) { t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(rep[0], rep[1]); } return t; };
const H = (a, b = 0, c = 0) => hash2(a, b, c);
const ease = (k) => { k = clamp(k); return k < 0.5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2; };
const outE = (k) => 1 - Math.pow(1 - clamp(k), 3);
function rrect(w, h, r) { const s = new THREE.Shape(), x = -w / 2, y = -h / 2; s.moveTo(x + r, y); s.lineTo(x + w - r, y); s.quadraticCurveTo(x + w, y, x + w, y + r); s.lineTo(x + w, y + h - r); s.quadraticCurveTo(x + w, y + h, x + w - r, y + h); s.lineTo(x + r, y + h); s.quadraticCurveTo(x, y + h, x, y + h - r); s.lineTo(x, y + r); s.quadraticCurveTo(x, y, x + r, y); return s; }
function grain(x, w, h, n, a, seed = 1) { for (let i = 0; i < n; i++) { const v = H(i, seed, 3); x.fillStyle = "rgba(" + (v > 0.5 ? "255,250,240" : "40,30,20") + "," + (a * (0.4 + 0.6 * H(i, seed, 5))).toFixed(3) + ")"; x.fillRect(H(i, seed, 1) * w, H(i, seed, 2) * h, 1 + 2 * H(i, seed, 4), 1 + 2 * H(i, seed, 6)); } }
const fadeable = (g) => { const mats = []; g.traverse((m) => { if (m.material) { const one = (x) => { x = x.clone(); x.transparent = true; x.userData.op = x.opacity; mats.push(x); return x; }; m.material = Array.isArray(m.material) ? m.material.map(one) : one(m.material); } }); return (k) => { for (const x of mats) x.opacity = x.userData.op * k; }; };

// ---------- letter cubes ----------------------------------------------------------------------------------------
function letterFace(ch, upside, face, ink) {
  const [c, x] = cv(512, 512); x.fillStyle = face; x.fillRect(0, 0, 512, 512); grain(x, 512, 512, 1600, 0.05, ch.charCodeAt(0));
  x.strokeStyle = "rgba(30,27,24,.22)"; x.lineWidth = 6; x.strokeRect(26, 26, 460, 460);
  const sh = x.createLinearGradient(0, 0, 0, 512); sh.addColorStop(0, "rgba(255,255,255,.08)"); sh.addColorStop(1, "rgba(0,0,0,.10)"); x.fillStyle = sh; x.fillRect(0, 0, 512, 512);
  x.save(); x.translate(256, 256); if (upside) x.rotate(Math.PI);
  x.fillStyle = ink; x.textAlign = "center"; x.textBaseline = "middle"; x.font = "400 400px " + SERIF; x.fillText(ch, 0, 30); x.restore();
  return tx(c);
}
function plainFace(col, mark) {
  const [c, x] = cv(256, 256); x.fillStyle = col; x.fillRect(0, 0, 256, 256); grain(x, 256, 256, 500, 0.06, 7);
  x.strokeStyle = "rgba(239,233,221,.35)"; x.lineWidth = 5; x.strokeRect(14, 14, 228, 228);
  if (mark) { x.fillStyle = "rgba(239,233,221,.8)"; x.fillRect(118, 70, 20, 116); x.fillRect(96, 64, 64, 8); x.fillRect(96, 184, 64, 8); }
  return tx(c);
}
function wordblocks(o) {                                    // a vertical totem: letter cubes on a steel rod, top to bottom; each spins about y (o.flips=[[t0, stagger, dur, angle]])
  const text = o.text || "INVERSO", n = text.length, e = (o.size && o.size[0]) || 0.3, gap = o.gap ?? 0.012, base = 0.14, g = new THREE.Group(), blocks = [];
  const face = o.face || C.gesso, ink = o.ink || C.ink, side = new THREE.MeshStandardMaterial({ map: plainFace(o.edge || C.ruggine, true), roughness: 0.6 }), cap = M(o.side || C.ink, 0.55);
  const geo = B(e, e, e), steel = M("#2a2a2a", 0.3, 0.85), Ht = base + n * (e + gap);
  add(g, B(e * 1.5, base - 0.01, e * 1.5), M(C.ink, 0.5), 0, (base - 0.01) / 2, 0); add(g, B(e * 1.56, 0.012, e * 1.56), M("#c9a24a", 0.3, 0.9), 0, base - 0.006, 0);
  add(g, CY(0.012, 0.012, Ht + 0.06, 12), steel, 0, (Ht + 0.06) / 2, 0); add(g, new THREE.SphereGeometry(0.03, 16, 12), M("#c9a24a", 0.3, 0.9), 0, Ht + 0.07, 0);
  for (let i = 0; i < n; i++) {
    const front = new THREE.MeshStandardMaterial({ map: letterFace(text[n - 1 - i], true, face, ink), roughness: 0.62 });
    const back = new THREE.MeshStandardMaterial({ map: letterFace(text[i], false, face, ink), roughness: 0.62 });
    const piv = new THREE.Group(); piv.position.set(0, Ht - (i + 0.5) * (e + gap), 0); g.add(piv);
    add(piv, geo, [side, side, cap, cap, front, back]); blocks.push(piv);
  }
  const flips = o.flips || [];
  g.userData.update = (t) => {
    for (let i = 0; i < n; i++) { let a = 0; for (const [t0, st, d, ang] of flips) a += ease((t - (t0 + i * st)) / d) * (ang ?? Math.PI); blocks[i].rotation.y = a; }
  };
  g.userData.update(-1); return g;
}

// ---------- the trouser back panel: right side and wrong side ------------------------------------------------------
function overlockTex(base, thread, dirty, seed) {
  const [c, x] = cv(256, 1024); x.fillStyle = base; x.fillRect(0, 0, 256, 1024); grain(x, 256, 1024, 1400, 0.06, seed);
  if (!dirty) {
    x.strokeStyle = thread; x.lineWidth = 2.2; x.beginPath();
    for (let y = 0; y < 1024; y += 7) { x.moveTo(256, y); x.lineTo(186, y + 3.5); x.lineTo(256, y + 7); }
    x.stroke(); x.strokeStyle = "rgba(0,0,0,.25)"; x.lineWidth = 2; x.beginPath(); x.moveTo(184, 0); x.lineTo(184, 1024); x.stroke();
    x.fillStyle = thread; for (let y = 0; y < 1024; y += 6) x.fillRect(16, y, 3, 3.4);                         // the seam stitch at the inner edge
  } else {
    for (let i = 0; i < 260; i++) { const y = H(i, seed, 1) * 1024, l = 8 + 30 * H(i, seed, 2); x.strokeStyle = "rgba(60,62,40," + (0.4 + 0.5 * H(i, seed, 3)).toFixed(2) + ")"; x.lineWidth = 1.5; x.beginPath(); x.moveTo(256, y); x.lineTo(256 - l, y + (H(i, seed, 4) - 0.5) * 10); x.stroke(); }
    x.fillStyle = "#d6c9a8"; let px = 18; for (let y = 0; y < 1024; y += 6 + 9 * H(y, seed, 6)) { px = clamp(px + (H(y, seed, 7) - 0.5) * 10, 6, 40); x.fillRect(px, y, 3, 4); }
  }
  return tx(c);
}
function pocketingTex() {
  const [c, x] = cv(256, 256); x.fillStyle = "#e8e1d0"; x.fillRect(0, 0, 256, 256);
  for (let i = 0; i < 256; i += 8) { x.fillStyle = "rgba(47,58,46,.16)"; x.fillRect(i, 0, 2, 256); } grain(x, 256, 256, 600, 0.05, 4); return tx(c);
}
function labelTex(text) {
  const [c, x] = cv(512, 192); x.fillStyle = C.ink; x.fillRect(0, 0, 512, 192);
  for (let i = 0; i < 512; i += 4) { x.fillStyle = "rgba(255,255,255,.04)"; x.fillRect(i, 0, 1, 192); }
  x.strokeStyle = "rgba(185,174,152,.6)"; x.lineWidth = 4; x.strokeRect(12, 12, 488, 168);
  if (text === "logo" || text === "logo-m") { if (text === "logo-m") { x.translate(512, 0); x.scale(-1, 1); } drawLogo(x, 256, 96, 330, C.gesso); } else { x.fillStyle = C.gesso; x.font = "400 96px " + SERIF; x.textAlign = "center"; x.textBaseline = "middle"; x.fillText(text, 256, 100); }
  return tx(c);
}
function seampanel(o) {
  const [w, d] = o.size || [0.5, 0.62], col = o.color || "#6f7452", dirty = !!o.dirty, th = 0.004, g = new THREE.Group(), p = new THREE.Group(); g.add(p);
  const fr = clothMat(col, "twill", { n: 0.8 }), bk = clothMat(new THREE.Color(col).multiplyScalar(1.18).getStyle(), "twill", { n: 0.35, rough: 0.97 });
  fr.map = fr.map.clone(); fr.map.repeat.set(w / 0.08, d / 0.08); fr.map.needsUpdate = true; fr.normalMap = fr.normalMap.clone(); fr.normalMap.repeat.set(w / 0.08, d / 0.08); fr.normalMap.needsUpdate = true;
  bk.map = fr.map; bk.normalMap = fr.normalMap;
  const edge = M(new THREE.Color(col).multiplyScalar(0.8).getStyle(), 0.9);
  const slab = add(p, B(w, th, d), [edge, edge, fr, bk, edge, edge]);
  // right side (+y): the centre-back seam (a fine groove), a flush welt pocket with its button, the waistband
  const dark = M("#1d1f14", 0.95);
  add(p, B(0.003, 0.0012, d * 0.86), M(new THREE.Color(col).multiplyScalar(0.62).getStyle(), 0.95), w * 0.18, th / 2 + 0.0004, 0.045);
  const wb = add(p, B(w, 0.007, 0.06), clothMat(col, "twill", { n: 0.8 }), 0, th / 2 + 0.0025, -d / 2 + 0.03);
  add(p, B(w, 0.0012, 0.002), dark, 0, th / 2 + 0.0061, -d / 2 + 0.0605);
  const pz = -d / 2 + 0.17, px = -w * 0.08;
  add(p, B(0.15, 0.0014, 0.0045), dark, px, th / 2 + 0.0006, pz);                                          // the pocket mouth
  for (const s of [-1, 1]) add(p, B(0.152, 0.0028, 0.0055), clothMat(col, "twill", { n: 0.8 }), px, th / 2 + 0.0014, pz + s * 0.005);   // the two welts
  for (const s of [-1, 1]) add(p, B(0.003, 0.0034, 0.014), M(new THREE.Color(col).multiplyScalar(0.7).getStyle(), 0.9), px + s * 0.076, th / 2 + 0.0017, pz);
  add(p, CY(0.0085, 0.0085, 0.003, 20), M("#3b2a1c", 0.35, 0.1), px, th / 2 + 0.0035, pz + 0.022);         // horn button under the welt
  // wrong side (-y): built facing down, it faces up once the panel is turned over
  const wr = new THREE.Group(); wr.rotation.x = Math.PI; wr.position.y = -th / 2; p.add(wr);              // inside wr, +y points away from the slab's back
  const thread = o.thread || C.sabbia;
  for (const s of [-1, 1]) {                                                                               // seam allowances pressed open, overlocked
    const sw = dirty ? 0.026 + 0.01 * (s > 0 ? 1 : 0) : 0.028, mat = new THREE.MeshStandardMaterial({ map: overlockTex(new THREE.Color(col).multiplyScalar(1.12).getStyle(), thread, dirty, s > 0 ? 3 : 8), roughness: 0.95 });
    if (s < 0) { mat.map.center.set(0.5, 0.5); mat.map.rotation = Math.PI; }
    const a = add(wr, B(sw, 0.0022, d * 0.88), [edge, edge, mat, edge, edge, edge], w * 0.18 + s * (sw / 2 + 0.001), 0.0011, -0.045);
    if (dirty) a.rotation.y = s * 0.025;
  }
  const bag = add(wr, B(0.19, 0.0016, 0.25), new THREE.MeshStandardMaterial({ map: pocketingTex(), roughness: 0.9 }), px, 0.0008, d / 2 - 0.2);   // the pocket bag, under the welt
  if (dirty) { bag.rotation.y = 0.09; bag.position.x += 0.012; }
  wr.add(stitches(dirty ? [[px - 0.09, 0.0018, d / 2 - 0.08], [px - 0.1, 0.0018, d / 2 - 0.2], [px - 0.085, 0.0018, d / 2 - 0.33]] : [[px - 0.09, 0.0018, d / 2 - 0.075], [px - 0.09, 0.0018, d / 2 - 0.325], [px + 0.09, 0.0018, d / 2 - 0.325], [px + 0.09, 0.0018, d / 2 - 0.075]], dirty ? "#c9b98a" : "#cfc4a6", 0.006, 0.0036, 0.0007));
  const facing = add(wr, B(w, 0.0025, 0.055), M(dirty ? new THREE.Color(col).multiplyScalar(1.1).getStyle() : C.ruggine, 0.85), 0, 0.0013, d / 2 - 0.028);   // the waistband facing in rust
  if (!dirty) {
    add(wr, B(0.085, 0.0012, 0.03), new THREE.MeshStandardMaterial({ map: labelTex("logo-m"), roughness: 0.6 }), 0, 0.0032, d / 2 - 0.03, 0, 0, 0);   // the woven label
    wr.add(stitches([[-w / 2 + 0.01, 0.0028, d / 2 - 0.054], [w / 2 - 0.01, 0.0028, d / 2 - 0.054]], "#e7dcc4", 0.006, 0.0036, 0.0007));
  } else {
    const loose = M("#d8cba6", 0.8);                                                                      // loose thread tails
    for (let i = 0; i < 6; i++) {
      const x0 = w * 0.18 + (H(i, 2, 2) - 0.5) * 0.06, z0 = -d * 0.38 + H(i, 3, 3) * d * 0.8, pts = [];
      for (let k = 0; k < 7; k++) pts.push([x0 + Math.sin(k * 1.3 + i) * 0.02 + k * 0.006 * (i % 2 ? 1 : -1), 0.004 + 0.002 * Math.sin(k), z0 + k * 0.012 + Math.cos(k * 1.7 + i) * 0.01]);
      const tb = tube(pts, 0.0006, loose, 40); tb.userData.noshadow = true; wr.add(tb);
    }
  }
  const t0 = o.flip ? o.flip[0] : 0, t1 = o.flip ? o.flip[1] : 0, axis = o.axis || "z";
  g.userData.update = (t) => {
    const k = o.flipped ? 1 : (o.flip ? ease((t - t0) / Math.max(0.01, t1 - t0)) : 0), a = k * Math.PI;
    if (axis === "z") { p.rotation.z = a; p.position.set(-Math.sin(a) * 0 + (1 - Math.cos(a)) * 0, Math.sin(a) * w * 0.5 + th / 2, 0); }
    else { p.rotation.x = -a; p.position.set(0, Math.sin(a) * d * 0.5 + th / 2, 0); }
  };
  g.userData.update(-1); return g;
}

// ---------- fast fashion rail -------------------------------------------------------------------------------------
function teeShape() {
  const s = new THREE.Shape(); s.moveTo(-0.075, 0); s.quadraticCurveTo(0, -0.03, 0.075, 0);                // neck at y = 0 (the hanger)
  s.lineTo(0.2, -0.035); s.lineTo(0.27, -0.2); s.lineTo(0.2, -0.235); s.lineTo(0.17, -0.17); s.lineTo(0.17, -0.66); s.lineTo(-0.17, -0.66); s.lineTo(-0.17, -0.17); s.lineTo(-0.2, -0.235); s.lineTo(-0.27, -0.2); s.lineTo(-0.2, -0.035); s.closePath(); return s;
}
function fastrail(o) {
  const [L, Hh] = o.size || [4, 1.75], g = new THREE.Group(), steel = M("#2a2a2a", 0.35, 0.8), sp = o.gap || 0.13, n = Math.floor(L / sp);
  add(g, CY(0.013, 0.013, L + 0.1, 12), steel, 0, Hh, 0, 0, 0, Math.PI / 2);
  for (const s of [-1, 1]) { add(g, CY(0.013, 0.013, Hh, 12), steel, s * L / 2, Hh / 2, 0); add(g, B(0.05, 0.03, 0.55), steel, s * L / 2, 0.015, 0); for (const z of [-0.24, 0.24]) add(g, new THREE.SphereGeometry(0.022, 10, 8), M("#111", 0.6), s * L / 2, 0.022, z); }
  const geo = new THREE.ExtrudeGeometry(teeShape(), { depth: 0.022, bevelEnabled: true, bevelThickness: 0.008, bevelSize: 0.008, bevelSegments: 2, curveSegments: 6 }); geo.translate(0, -0.03, -0.011);
  const tee = M(o.color || "#f3f0ea", 0.95), tagm = M(o.tag || C.red, 0.6), hang = M("#c7c9cc", 0.3, 0.7), hook = new THREE.TorusGeometry(0.018, 0.0028, 6, 16, Math.PI * 1.5);
  const hangerGeo = new THREE.CylinderGeometry(0.004, 0.004, 0.38, 6);
  const items = [];
  for (let i = 0; i < n; i++) {
    const piv = new THREE.Group(); g.add(piv); const sw = new THREE.Group(); piv.add(sw); sw.rotation.y = o.fan ?? -0.8;
    add(sw, hook, hang, 0, 0.012, 0, 0, Math.PI / 2, 0.6); add(sw, hangerGeo, hang, 0, -0.035, 0, 0, Math.PI / 2, Math.PI / 2 - 0.0).rotation.set(0, Math.PI / 2, Math.PI / 2);
    const body = add(sw, geo, tee, 0, -0.03, 0); body.rotation.y = Math.PI / 2;
    add(sw, B(0.004, 0.06, 0.035), tagm, 0.02, -0.12, 0.17, 0, Math.PI / 2, 0);
    items.push(piv);
  }
  const [t0, t1] = o.span || [0, 1], tc = o.clear ?? t1, vmax = o.speed || 3.2;
  const D = (t) => { if (t <= t0) return 0; const ta = 0.7, u = t - t0; return u < ta ? vmax * u * u / (2 * ta) : vmax * (ta / 2 + (u - ta)); };   // displacement: ramp up, then steady
  const vel = (t) => (t <= t0 ? 0 : Math.min(1, (t - t0) / 0.7) * vmax);
  g.userData.update = (t) => {
    const dc = D(Math.min(t, tc)), extra = D(t) - dc;
    for (let i = 0; i < n; i++) {
      let x = (((i * sp + dc) % L) + L) % L - L / 2;
      if (t > tc) x += extra;
      const it = items[i]; it.position.set(x, Hh, 0); it.visible = x < L / 2 - 0.02 && !(o.out != null && t > o.out);
      const v = vel(t) * (t > tc + 2 ? 0 : 1), acc = t > t0 && t < t0 + 0.7 ? 1 : 0;
      it.children[0].rotation.x = 0; it.rotation.z = -0.1 * (v / vmax) - 0.12 * acc + 0.02 * Math.sin(t * 9 + i);
    }
  };
  g.userData.update(-1); return g;
}

// ---------- wall clock --------------------------------------------------------------------------------------------
function wallclock(o) {
  const dia = (o.size && o.size[0]) || 0.42, g = new THREE.Group(), [c, x] = cv(512, 512);
  x.fillStyle = C.gesso; x.fillRect(0, 0, 512, 512); grain(x, 512, 512, 900, 0.04, 9); x.fillStyle = C.ink; x.translate(256, 256);
  for (let i = 0; i < 60; i++) { x.save(); x.rotate(i * Math.PI / 30); x.fillRect(-(i % 5 ? 2 : 5), -236, i % 5 ? 4 : 10, i % 5 ? 18 : 40); x.restore(); }
  x.font = "400 64px " + SERIF; x.textAlign = "center"; x.textBaseline = "middle"; for (let i = 1; i <= 12; i++) { const a = i * Math.PI / 6; x.fillText(String(i), Math.sin(a) * 166, -Math.cos(a) * 166 + 4); }
  x.font = "600 22px " + SANS; x.fillStyle = C.ruggine; x.fillText("ROMA", 0, 86);
  add(g, CY(dia / 2 + 0.02, dia / 2 + 0.02, 0.05, 48), M(C.ink, 0.4, 0.3), 0, 0, 0.025, Math.PI / 2, 0, 0);
  add(g, new THREE.CircleGeometry(dia / 2, 64), new THREE.MeshStandardMaterial({ map: tx(c), roughness: 0.6 }), 0, 0, 0.051);
  add(g, new THREE.TorusGeometry(dia / 2 + 0.012, 0.012, 10, 64), M("#c9a24a", 0.3, 0.9), 0, 0, 0.05);
  const mk = (len, wid, col, z) => { const h = new THREE.Group(); h.position.z = z; g.add(h); add(h, B(wid, len, 0.004), M(col, 0.4, 0.2), 0, len / 2 - 0.02, 0); h.children[0].userData.noshadow = true; return h; };
  const hh = mk(dia * 0.25, 0.014, C.ink, 0.056), mh = mk(dia * 0.38, 0.009, C.ink, 0.06), sh = mk(dia * 0.42, 0.003, C.red, 0.064);
  add(g, CY(0.012, 0.012, 0.012, 16), M(C.red, 0.4), 0, 0, 0.066, Math.PI / 2, 0, 0);
  const spin = o.spin || [];
  g.userData.update = (t) => {
    let turns = 0; for (const [a, b, n] of spin) turns += smooth((t - a) / Math.max(0.01, b - a)) * n;   // extra turns of the minute hand
    const m = 10 + 60 * turns + t / 60, hr = 10 + m / 60;
    mh.rotation.z = -m / 60 * Math.PI * 2; hh.rotation.z = -(hr % 12) / 12 * Math.PI * 2; sh.rotation.z = -(Math.floor(t) + smooth((t % 1) * 6)) / 60 * Math.PI * 2 - turns * 30;
  };
  g.userData.update(0); return g;
}

// ---------- shoe boxes and the sneaker --------------------------------------------------------------------------------
function boxEndTex(price) {
  const [c, x] = cv(512, 192); x.fillStyle = "#cdbf9f"; x.fillRect(0, 0, 512, 192); grain(x, 512, 192, 900, 0.07, 3);
  x.fillStyle = C.gesso; x.fillRect(300, 36, 180, 120); x.strokeStyle = "rgba(30,27,24,.35)"; x.lineWidth = 2; x.strokeRect(300, 36, 180, 120);
  x.fillStyle = C.ink; x.font = "600 50px " + SANS; x.textAlign = "center"; x.textBaseline = "middle"; x.fillText(price, 390, 98);
  x.fillStyle = "rgba(30,27,24,.55)"; x.font = "500 20px " + SANS; x.textAlign = "left"; x.fillText("EU 42", 40, 150); x.fillText("||| |||| || |||", 40, 122);
  return tx(c);
}
function shoeboxes(o) {
  const g = new THREE.Group(), [bw, bh, bd] = o.box || [0.34, 0.13, 0.22], gap = 0.012, n = o.n || 6, cols = o.cols || 3, keep = o.keep ?? 1;
  const endM = new THREE.MeshStandardMaterial({ map: boxEndTex(o.price || "150 €"), roughness: 0.8 }), kraft = M("#cdbf9f", 0.85), lid = M(o.lid || C.ink, 0.7);
  const boxes = [];
  for (let i = 0; i < n; i++) {
    const r = Math.floor(i / cols), k = i % cols, b = new THREE.Group();
    b.position.set((k - (cols - 1) / 2) * (bw + gap), r * (bh + 0.004), 0); g.add(b);
    const inner = new THREE.Group(); b.add(inner);
    add(inner, B(bw, bh * 0.82, bd), [kraft, kraft, kraft, kraft, endM, kraft], 0, bh * 0.41, 0);
    add(inner, B(bw + 0.008, bh * 0.24, bd + 0.008), lid, 0, bh * 0.88, 0);
    boxes.push({ b: inner, f: fadeable(inner), i, base: b.position.clone() });
  }
  const [s0, st] = o.show || [-1, 0], drop = o.drop ?? 1e9;
  g.userData.update = (t) => {
    for (const x of boxes) {
      const ki = clamp((t - (s0 + x.i * st)) / 0.3), kin = ki <= 0 ? 0 : outE(ki);
      let k = kin, dy = (1 - kin) * 0.06, dz = 0;
      if (x.i !== keep && t > drop) { const kd = clamp((t - drop - 0.07 * ((x.i * 7) % n)) / 0.45); k *= 1 - smooth(kd); dz = -0.25 * smooth(kd); dy += 0.08 * Math.sin(Math.PI * kd * 0.5); }
      x.b.visible = k > 0.002; x.b.position.set(0, dy, dz); x.b.scale.setScalar(0.85 + 0.15 * k); x.f(Math.min(1, k * 1.4));
    }
  };
  g.userData.update(-1); return g;
}
function sneakerMesh(col, sole, accent) {
  // a lofted low-top: footprint-shaped cupsole + an upper built from superellipse sections (heel high, collar dip, low toe), laces, tongue, side band, heel tab
  const g = new THREE.Group(), L = 0.28, base = 0.03, NS = 48, NA = 28;
  const hc = new THREE.CatmullRomCurve3([[0, 0.092], [0.1, 0.108], [0.24, 0.1], [0.34, 0.088], [0.46, 0.086], [0.62, 0.071], [0.8, 0.055], [0.93, 0.045], [1, 0.034]].map(([u, h]) => new THREE.Vector3(u, h, 0)));
  const tab = hc.getPoints(400); const hAt = (u) => { for (let i = 1; i < tab.length; i++) if (tab[i].x >= u) { const a = tab[i - 1], b = tab[i], k = (u - a.x) / Math.max(1e-6, b.x - a.x); return a.y + (b.y - a.y) * k; } return tab[tab.length - 1].y; };
  const wAt = (u) => { const prof = u < 0.25 ? 0.037 + 0.03 * u : u < 0.72 ? 0.0445 + 0.012 * Math.sin(Math.PI * (u - 0.25) / 0.94) : 0.05 - 0.01 * (u - 0.72) / 0.28; const c = 1 - Math.pow(Math.abs(u - 0.5) / 0.5, u < 0.5 ? 7 : 3.2); return prof * Math.sqrt(Math.max(0, c)); };
  const X = (u) => -L / 2 + u * L;
  // sole: the footprint, extruded up
  const fp = new THREE.Shape(), pts = [];
  for (let i = 0; i <= 60; i++) { const u = i / 60; pts.push([X(u), (wAt(u) + 0.006 * Math.sqrt(Math.max(0, 1 - Math.pow(2 * u - 1, 8)))) * 1.06]); }
  fp.moveTo(pts[0][0], 0); for (const [x, y] of pts) fp.lineTo(x, y); for (let i = pts.length - 1; i >= 0; i--) fp.lineTo(pts[i][0], -pts[i][1]); fp.closePath();
  const sg = new THREE.ExtrudeGeometry(fp, { depth: base - 0.006, bevelEnabled: true, bevelThickness: 0.003, bevelSize: 0.003, bevelSegments: 3, curveSegments: 4 }); sg.rotateX(-Math.PI / 2); sg.translate(0, 0.003, 0);
  add(g, sg, M(sole, 0.8));
  const fx = new THREE.ExtrudeGeometry(fp, { depth: 0.006, bevelEnabled: false }); fx.rotateX(-Math.PI / 2); fx.scale(1.005, 1, 1.02); add(g, fx, M(C.gesso, 0.6), 0, base - 0.009, 0);   // the foxing line
  // upper: rings of superellipse sections from heel (u=0) to toe (u=1)
  const pos = [], idx = [], A0 = -0.12, A1 = Math.PI + 0.12, ex = 0.62;
  for (let i = 0; i <= NS; i++) { const u = i / NS, w = Math.max(wAt(u), 0.0008), H = Math.max(hAt(u) - base, 0.002) * (u > 0.985 ? 0.6 : 1);
    for (let j = 0; j <= NA; j++) { const a = A0 + (A1 - A0) * j / NA, c = Math.cos(a), sn = Math.sin(a); pos.push(X(u), base - 0.004 + H * Math.sign(sn) * Math.pow(Math.abs(sn), ex) + (sn < 0 ? 0.004 * sn : 0), w * Math.sign(c) * Math.pow(Math.abs(c), ex)); } }
  for (let i = 0; i < NS; i++) for (let j = 0; j < NA; j++) { const a = i * (NA + 1) + j, b = a + NA + 1; idx.push(a, a + 1, b, b, a + 1, b + 1); }
  const ug = new THREE.BufferGeometry(); ug.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3)); ug.setIndex(idx); ug.computeVertexNormals();
  const um = M(col, 0.62); um.side = THREE.DoubleSide; add(g, ug, um);
  const surf = (u, a) => { const w = wAt(u), H = hAt(u) - base, c = Math.cos(a), sn = Math.sin(a); return new THREE.Vector3(X(u), base - 0.004 + H * Math.pow(Math.max(0, sn), ex), w * Math.sign(c) * Math.pow(Math.abs(c), ex)); };
  const band = (u0, u1, a, r, mat) => { const p = []; for (let k = 0; k <= 30; k++) { const v = surf(u0 + (u1 - u0) * k / 30, a), n = v.clone().setX(0).setY(v.y - base).normalize(); p.push(v.add(n.multiplyScalar(r * 0.6))); } const m = add(g, new THREE.TubeGeometry(new THREE.CatmullRomCurve3(p), 40, r, 6, false), mat); m.userData.noshadow = true; return m; };
  const acc = M(accent, 0.5);
  for (const s of [1, -1]) { const a = s > 0 ? 0.42 : Math.PI - 0.42; band(0.06, 0.74, a, 0.0035, acc); band(0.44, 0.74, s > 0 ? 1.05 : Math.PI - 1.05, 0.0028, M(col, 0.5)); }   // side band + eyestay edge
  // collar: a dark opening ringed by a padded edge
  const cu = 0.27, cy = hAt(cu) + 0.002, op = add(g, new THREE.CircleGeometry(1, 40), M("#221e1a", 0.95), X(cu), cy, 0, -Math.PI / 2 + 0.12, 0, 0); op.scale.set(0.07, 0.034, 1); op.userData.noshadow = true;
  const ring = add(g, new THREE.TorusGeometry(1, 0.06, 10, 40), M(col, 0.55), X(cu), cy - 0.001, 0, -Math.PI / 2 + 0.12, 0, 0); ring.scale.set(0.071, 0.036, 0.05); ring.userData.noshadow = true;
  // tongue + laces
  const tg = add(g, B(0.05, 0.006, 0.05), M(col, 0.7), X(0.41), hAt(0.41) + 0.012, 0, 0, 0, 0.32); tg.userData.noshadow = true;
  for (let i = 0; i < 5; i++) { const u = 0.47 + i * 0.055, y = hAt(u) + 0.0035, sl = (hAt(u + 0.01) - hAt(u - 0.01)) / (0.02 * L), w = wAt(u) * 1.25;
    for (const s of [1, -1]) { const l = add(g, CY(0.0022, 0.0022, w, 6), M(C.gesso, 0.85), X(u), y, 0, Math.PI / 2, s * 0.28, Math.atan(sl)); l.userData.noshadow = true; } }
  const ht = add(g, B(0.007, 0.04, 0.02), acc, X(0.012), hAt(0.03) - 0.02, 0, 0, 0, -0.18); ht.userData.noshadow = true;   // heel tab
  return g;
}
function sneaker(o) { const g = new THREE.Group(), a = sneakerMesh(o.color || "#f2eee6", o.sole || "#c9a77a", o.accent || C.bosco); g.add(a); if (o.pair) { const b = sneakerMesh(o.color || "#f2eee6", o.sole || "#c9a77a", o.accent || C.bosco); b.position.set(0.02, 0, 0.12); b.rotation.y = 0.12; g.add(b); } return g; }

// ---------- Rome at night ------------------------------------------------------------------------------------------
function cityview(o) {
  const [w, h] = o.size || [8, 4], [c, x] = cv(2048, 1024), W = 2048, Hh = 1024;
  const sky = x.createLinearGradient(0, 0, 0, Hh); sky.addColorStop(0, "#0b1424"); sky.addColorStop(0.55, "#1c2a44"); sky.addColorStop(0.78, "#4a3f52"); sky.addColorStop(0.9, "#c47a4e"); sky.addColorStop(1, "#e3a066"); x.fillStyle = sky; x.fillRect(0, 0, W, Hh);
  for (let i = 0; i < 260; i++) { const a = H(i, 1, 9); x.fillStyle = "rgba(255,248,230," + (0.25 + 0.6 * a * a).toFixed(2) + ")"; const r = a > 0.92 ? 2.2 : 1.1; x.fillRect(H(i, 2, 9) * W, H(i, 3, 9) * Hh * 0.55, r, r); }
  const mg = x.createRadialGradient(1620, 210, 0, 1620, 210, 140); mg.addColorStop(0, "rgba(255,246,220,.9)"); mg.addColorStop(0.18, "rgba(255,246,220,.85)"); mg.addColorStop(0.2, "rgba(255,240,210,.18)"); mg.addColorStop(1, "rgba(255,240,210,0)"); x.fillStyle = mg; x.fillRect(1460, 60, 320, 320);
  const layer = (base, col, seed, lit, scale) => {
    x.fillStyle = col; x.beginPath(); x.moveTo(0, Hh); let px = 0;
    const win = [];
    while (px < W) {
      const bw = (60 + 140 * H(px, seed, 1)) * scale, bh = (40 + 150 * H(px, seed, 2)) * scale, y = base - bh, kind = H(px, seed, 3);
      x.lineTo(px, y);
      if (kind > 0.93) { x.lineTo(px + bw * 0.2, y); x.arc(px + bw * 0.5, y - 10 * scale, bw * 0.32, Math.PI, 0); x.lineTo(px + bw * 0.8, y); x.lineTo(px + bw * 0.5 + 4, y - bw * 0.36 - 10 * scale); }   // a dome
      else if (kind > 0.87) { x.lineTo(px + bw * 0.35, y); x.lineTo(px + bw * 0.35, y - 120 * scale); x.lineTo(px + bw * 0.5, y - 150 * scale); x.lineTo(px + bw * 0.65, y - 120 * scale); x.lineTo(px + bw * 0.65, y); }   // a bell tower
      else if (kind < 0.07) { x.lineTo(px + bw * 0.45, y); x.lineTo(px + bw * 0.45, y - 70 * scale); x.ellipse(px + bw * 0.5, y - 85 * scale, bw * 0.55, 26 * scale, 0, Math.PI, 0); x.lineTo(px + bw * 0.55, y); }   // an umbrella pine
      else { x.lineTo(px + bw * 0.1, y - 10 * scale * H(px, seed, 5)); }
      x.lineTo(px + bw, y);
      if (lit) for (let r = y + 14 * scale; r < base - 6; r += 22 * scale) for (let q = px + 10 * scale; q < px + bw - 10; q += 18 * scale) if (H(q, r, seed) > 0.72) win.push([q, r]);
      px += bw;
    }
    x.lineTo(W, Hh); x.closePath(); x.fill();
    for (const [q, r] of win) { x.fillStyle = "rgba(255," + (190 + Math.floor(40 * H(q, r, 4))) + ",110," + (0.55 + 0.4 * H(q, r, 5)).toFixed(2) + ")"; x.fillRect(q, r, 6 * scale, 9 * scale); }
  };
  layer(Hh * 0.8, "#1d2232", 11, true, 0.6); layer(Hh * 0.88, "#151826", 23, true, 0.85); layer(Hh * 1.0, "#0d0f17", 37, true, 1.1);
  const haze = x.createLinearGradient(0, Hh * 0.6, 0, Hh); haze.addColorStop(0, "rgba(230,150,90,0)"); haze.addColorStop(1, "rgba(230,150,90,.12)"); x.fillStyle = haze; x.fillRect(0, Hh * 0.6, W, Hh * 0.4);
  const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ map: tx(c), toneMapped: false, fog: false, color: new THREE.Color(o.dim ?? 0.85, o.dim ?? 0.85, o.dim ?? 0.85) }));
  m.position.y = h / 2; m.userData.noshadow = true; const g = new THREE.Group(); g.add(m); return g;
}
function crittall(o) {                                     // origin = the middle of the opening; size [w, h]; cols x rows panes
  const [w, h] = o.size, g = new THREE.Group(), st = M("#16171a", 0.45, 0.6), f = 0.05, d = 0.07, cols = o.cols || 6, rows = o.rows || 4;
  add(g, B(w + 2 * f, f, d), st, 0, h / 2 + f / 2, 0); add(g, B(w + 2 * f, f, d), st, 0, -h / 2 - f / 2, 0); add(g, B(f, h, d), st, -w / 2 - f / 2, 0, 0); add(g, B(f, h, d), st, w / 2 + f / 2, 0, 0);
  for (let i = 1; i < cols; i++) add(g, B(0.018, h, 0.04), st, -w / 2 + i * w / cols, 0, 0);
  for (let j = 1; j < rows; j++) add(g, B(w, 0.018, 0.04), st, 0, -h / 2 + j * h / rows, 0);
  add(g, B(w + 0.2, 0.04, 0.24), M("#d9cfbd", 0.5), 0, -h / 2 - f - 0.02, 0.1);                         // a stone sill
  const gl = add(g, new THREE.PlaneGeometry(w, h), new THREE.MeshStandardMaterial({ color: "#9fb2cf", roughness: 0.05, metalness: 0.9, transparent: true, opacity: 0.08 }), 0, 0, -0.01); gl.userData.noshadow = true;
  return g;
}

// ---------- shelves, cork board, palette ---------------------------------------------------------------------------
function bookshelf(o) {
  const [w, h, d] = o.size || [1.4, 2.1, 0.32], g = new THREE.Group(), wood = M(o.wood || "#5a3d28", 0.55), sh = o.shelves || 5;
  add(g, B(0.025, h, d), wood, -w / 2, h / 2, 0); add(g, B(0.025, h, d), wood, w / 2, h / 2, 0); add(g, B(w, h, 0.012), M("#24201c", 0.9), 0, h / 2, -d / 2 + 0.006);
  const pal = ["#2f3a2e", "#8a4b2d", "#b9ae98", "#efe9dd", "#1e1b18", "#6f7452", "#c9a24a", "#3b4f6b", "#7a2f2f", "#a58a6a", "#d8cfc0"];
  for (let s = 0; s <= sh; s++) {
    const y = 0.06 + s * (h - 0.08) / sh; add(g, B(w, 0.025, d), wood, 0, y, 0);
    if (s === sh) break;
    let x = -w / 2 + 0.03; const top = (h - 0.08) / sh - 0.04; let k = 0;
    while (x < w / 2 - 0.06) {
      const r = H(s, k, o.seed || 2), kind = H(k, s, 9);
      if (kind > 0.9 && x < w / 2 - 0.3) {                                                               // a stack of magazines lying flat
        for (let m = 0; m < 5; m++) add(g, B(0.22, 0.012, 0.24), M(pal[(s + m * 3) % pal.length], 0.8), x + 0.11 + 0.006 * Math.sin(m), y + 0.0185 + m * 0.013, 0, 0, 0.04 * Math.sin(m * 2), 0);
        x += 0.26; k++; continue;
      }
      if (kind < 0.07 && x < w / 2 - 0.15) { add(g, CY(0.045, 0.06, 0.16, 18), M(pal[(k + s) % 3 === 0 ? 1 : 3], 0.35), x + 0.07, y + 0.0925, 0); x += 0.16; k++; continue; }   // a vase
      const bw = 0.022 + 0.03 * r, bh = top * (0.62 + 0.36 * H(k, s, 4)), col = pal[Math.floor(H(k, s, 5) * pal.length)], lean = x > w / 2 - 0.12 ? 0 : (H(k, s, 6) > 0.95 ? 0.22 : 0);
      const b = add(g, B(bw, bh, d * 0.78), M(col, 0.8), x + bw / 2, y + 0.0125 + bh / 2, 0.01, 0, 0, lean);
      if (H(k, s, 7) > 0.5) add(g, B(bw * 1.01, 0.012, d * 0.785), M("#c9a24a", 0.4, 0.5), x + bw / 2, y + 0.0125 + bh * 0.8, 0.01).userData.noshadow = true;
      x += bw + 0.002 + (lean ? 0.06 : 0); k++;
    }
  }
  return g;
}
function cardTex(cd, w, h) {
  const W = 512, Hh = Math.round(W * h / w), [c, x] = cv(W, Hh); x.fillStyle = cd.bg || C.gesso; x.fillRect(0, 0, W, Hh); grain(x, W, Hh, 900, 0.05, 5);
  x.fillStyle = cd.ink || C.ink; x.textAlign = "center"; x.textBaseline = "middle";
  if (cd.big) { x.font = "400 " + Math.round(Hh * 0.34) + "px " + SERIF; x.fillText(cd.big, W / 2, Hh * 0.42); }
  x.font = "italic 400 " + Math.round(Hh * (cd.big ? 0.15 : 0.2)) + "px " + SERIF; x.fillText((cd.text || "").replace(/\*/g, ""), W / 2, Hh * (cd.big ? 0.72 : 0.42));
  if (cd.sub) { x.font = "500 " + Math.round(Hh * 0.075) + "px " + SANS; x.fillStyle = "rgba(30,27,24,.6)"; x.fillText(cd.sub.toUpperCase(), W / 2, Hh * (cd.big ? 0.88 : 0.68)); }
  if (cd.lines) { x.strokeStyle = "rgba(30,27,24,.35)"; x.lineWidth = 3; for (let i = 0; i < 4; i++) { x.beginPath(); x.moveTo(60, Hh * 0.62 + i * 26); x.lineTo(W - 60 - 80 * H(i, 3, 3), Hh * 0.62 + i * 26); x.stroke(); } }
  if (cd.strike) { x.strokeStyle = C.red; x.lineWidth = 9; x.beginPath(); x.moveTo(70, Hh * 0.5); x.lineTo(W - 70, Hh * 0.36); x.stroke(); }
  return tx(c);
}
function pinboard(o) {
  const [w, h] = o.size || [1.6, 1.0], g = new THREE.Group(), [c, x] = cv(1024, 640);
  x.fillStyle = "#b48a5c"; x.fillRect(0, 0, 1024, 640); for (let i = 0; i < 9000; i++) { x.fillStyle = "rgba(" + (H(i, 1, 1) > 0.5 ? "90,55,25" : "220,180,130") + "," + (0.25 * H(i, 2, 2)).toFixed(2) + ")"; x.fillRect(H(i, 3, 3) * 1024, H(i, 4, 4) * 640, 2, 2); }
  add(g, B(w, h, 0.02), [M("#3a2a1c"), M("#3a2a1c"), M("#3a2a1c"), M("#3a2a1c"), new THREE.MeshStandardMaterial({ map: tx(c), roughness: 0.95 }), M("#3a2a1c")], 0, 0, 0.01);
  const fr = M(o.frame || C.ink, 0.5); add(g, B(w + 0.06, 0.03, 0.04), fr, 0, h / 2 + 0.015, 0.02); add(g, B(w + 0.06, 0.03, 0.04), fr, 0, -h / 2 - 0.015, 0.02); add(g, B(0.03, h, 0.04), fr, -w / 2 - 0.015, 0, 0.02); add(g, B(0.03, h, 0.04), fr, w / 2 + 0.015, 0, 0.02);
  const pin = new THREE.SphereGeometry(0.009, 12, 8), pinM = M(C.red, 0.35), anim = [];
  const put = (cd, i) => {
    const cw = cd.w || 0.3, ch = cd.h || 0.21, q = new THREE.Group(); q.position.set(cd.x * w / 2, cd.y * h / 2, 0.024); q.rotation.z = cd.rot || 0; g.add(q);
    const inner = new THREE.Group(); q.add(inner);
    if (cd.swatch) { add(inner, B(cw, ch, 0.003), clothMat(cd.swatch, cd.kind || "twill", { n: 0.6 })); }
    else add(inner, new THREE.PlaneGeometry(cw, ch), new THREE.MeshStandardMaterial({ map: cardTex(cd, cw, ch), roughness: 0.85 }), 0, 0, 0.002);
    add(inner, pin, pinM, 0, ch / 2 - 0.02, 0.01); add(inner, CY(0.0015, 0.0015, 0.02, 6), M("#999", 0.3, 0.8), 0, ch / 2 - 0.02, 0.0, Math.PI / 2, 0, 0);
    if (cd.t != null) anim.push({ q: inner, t: cd.t, f: fadeable(inner) });
  };
  (o.items || []).forEach(put); (o.cards || []).forEach(put);
  g.userData.update = (t) => { for (const a of anim) { const k = clamp((t - a.t) / 0.35), e = outE(k); a.q.visible = k > 0; a.q.position.set(0, (1 - e) * 0.05, (1 - e) * 0.12); a.q.rotation.z = (1 - e) * 0.25; a.f(Math.min(1, k * 1.5)); } };
  g.userData.update(-1); return g;
}
function swatchwall(o) {
  const [w, h] = o.size || [1.2, 1.6], [c, x] = cv(1200, 1600), S = o.colors || [["gesso", C.gesso], ["inchiostro", C.ink], ["bosco", C.bosco], ["ruggine", C.ruggine], ["sabbia", C.sabbia]];
  x.fillStyle = "#e9e3d6"; x.fillRect(0, 0, 1200, 1600);
  S.forEach(([nm, col], i) => {
    const x0 = 40 + i * 228; x.fillStyle = col; x.fillRect(x0, 40, 200, 1300);
    x.strokeStyle = "rgba(30,27,24,.25)"; x.lineWidth = 2; x.strokeRect(x0, 40, 200, 1300);
    x.fillStyle = C.ink; x.font = "italic 400 58px " + SERIF; x.textAlign = "left"; x.fillText(nm, x0 + 4, 1420); x.font = "500 26px " + SANS; x.fillStyle = "rgba(30,27,24,.7)"; x.fillText(col.toUpperCase(), x0 + 6, 1470);
  });
  const g = new THREE.Group(); add(g, B(w, h, 0.012), [M("#ddd"), M("#ddd"), M("#ddd"), M("#ddd"), new THREE.MeshStandardMaterial({ map: tx(c), roughness: 0.8 }), M("#ddd")], 0, 0, 0.006); return g;
}

// ---------- the diagram on the floor --------------------------------------------------------------------------------
function axisline(o) {
  const L = (o.size && o.size[0]) || 4, g = new THREE.Group(), [c, x] = cv(2048, 64);
  x.fillStyle = C.gesso; x.fillRect(0, 0, 2048, 64); x.fillStyle = C.ink; for (let i = 0; i <= 40; i++) x.fillRect(i * 2048 / 40 - (i === 40 ? 4 : 0), 0, 4, i % 10 === 0 ? 64 : i % 5 === 0 ? 40 : 22);
  const strip = add(g, new THREE.PlaneGeometry(L, 0.07), new THREE.MeshStandardMaterial({ map: tx(c), roughness: 0.7, polygonOffset: true, polygonOffsetFactor: -4 }), 0, 0.006, 0, -Math.PI / 2, 0, 0);
  const end = (word, sgn, col) => {
    const [cc, xx] = cv(512, 512); xx.fillStyle = col; xx.beginPath(); xx.arc(256, 256, 250, 0, Math.PI * 2); xx.fill(); xx.fillStyle = C.gesso; xx.beginPath(); xx.arc(256, 256, 222, 0, Math.PI * 2); xx.fill();
    xx.fillStyle = C.ink; xx.textAlign = "center"; xx.textBaseline = "middle"; xx.font = "italic 400 " + (word.length > 9 ? 78 : 96) + "px " + SERIF; xx.fillText(word, 256, 256);
    const m = add(g, new THREE.CircleGeometry(0.33, 64), new THREE.MeshStandardMaterial({ map: tx(cc), roughness: 0.8, polygonOffset: true, polygonOffsetFactor: -5 }), sgn * (L / 2 + 0.3), 0.007, 0, -Math.PI / 2, 0, o.tspin || 0); return m;
  };
  const left = end(o.left || "ostentazione", -1, o.lcol || C.ruggine), right = end(o.right || "flexing", 1, o.rcol || C.ruggine);
  const puck = new THREE.Group(); g.add(puck); const pin = new THREE.Group(); pin.rotation.y = o.pspin || 0; puck.add(pin); const [pc, px] = cv(512, 512); px.fillStyle = C.ink; px.fillRect(0, 0, 512, 512); drawLogo(px, 256, 256, 400, C.gesso);
  add(pin, CY(0.2, 0.2, 0.05, 48), [M(C.red, 0.4), new THREE.MeshStandardMaterial({ map: tx(pc), roughness: 0.5 }), M(C.red, 0.4)], 0, 0.025, 0);
  const ring = add(puck, new THREE.RingGeometry(0.22, 0.25, 48), new THREE.MeshBasicMaterial({ color: C.red, transparent: true, opacity: 0, toneMapped: false }), 0, 0.009, 0, -Math.PI / 2, 0, 0); ring.userData.noshadow = true;
  const [d0, d1] = o.draw || [-1, 0], lt = o.lt ?? -1, rt = o.rt ?? -1, keys = o.puck || [];
  g.userData.update = (t) => {
    const k = ease((t - d0) / Math.max(0.01, d1 - d0)); strip.scale.set(Math.max(1e-3, k), 1, 1); strip.visible = k > 0.001;
    const pop = (m, t0) => { const q = clamp((t - t0) / 0.35), s = q <= 0 ? 1e-3 : q < 1 ? outE(q) * (1 + 0.12 * Math.sin(Math.PI * q)) : 1; m.scale.set(s, s, s); m.visible = q > 0; };
    pop(left, lt); pop(right, rt);
    let f = keys.length ? keys[0][2] : 0.5; for (const [a, d, to] of keys) { const p = ease((t - a) / d); if (p <= 0) break; f = lerp(f, to, p); }
    const vis = keys.length && t >= keys[0][0] - 0.3; puck.visible = !!vis; const q = vis ? outE((t - keys[0][0] + 0.3) / 0.3) : 0;
    puck.position.set((f - 0.5) * L, 0, 0); puck.scale.setScalar(Math.max(1e-3, q));
    const last = keys.length ? keys[keys.length - 1] : null; const rk = last ? clamp((t - last[0] - last[1]) / 0.6) : 0;
    ring.material.opacity = rk > 0 && rk < 1 ? 1 - rk : 0; ring.scale.setScalar(1 + rk * 1.6);
  };
  g.userData.update(-1); return g;
}
function crossmark(o) {
  const s = (o.size && o.size[0]) || 0.2, g = new THREE.Group(), inner = new THREE.Group(), m = M(C.red, 0.45); g.add(inner);
  for (const a of [Math.PI / 4, -Math.PI / 4]) { const b = add(inner, B(s, 0.006, s * 0.16), m, 0, 0.003, 0, 0, a, 0); b.userData.noshadow = true; }
  m.emissive = new THREE.Color(C.red); m.emissiveIntensity = 0.35;
  const t0 = o.show ?? -1, out = o.out ?? 1e9;
  g.userData.update = (t) => { const k = clamp((t - t0) / 0.3), ko = t > out ? 1 - clamp((t - out) / 0.3) : 1, sc = (k <= 0 ? 1e-3 : outE(k) * (1 + 0.18 * Math.sin(Math.PI * k))) * ko; inner.scale.set(sc, 1, sc); inner.visible = k > 0 && ko > 0; };
  g.userData.update(-1); return g;
}

// ---------- desk things -------------------------------------------------------------------------------------------
function laptop(o) {
  const g = new THREE.Group(), al = M("#b8b9bb", 0.35, 0.8), w = 0.34, d = 0.235;
  add(g, B(w, 0.012, d), al, 0, 0.006, 0); add(g, B(w * 0.86, 0.001, d * 0.42), M("#1b1b1d", 0.8), 0, 0.0125, -0.02); add(g, B(w * 0.3, 0.001, d * 0.2), M("#a5a6a8", 0.4, 0.6), 0, 0.0125, d * 0.28);
  const lid = new THREE.Group(); lid.position.set(0, 0.012, -d / 2); lid.rotation.x = -0.32; g.add(lid);
  add(lid, B(w, d, 0.008), al, 0, d / 2, -0.004);
  const [c, x] = cv(1024, 680); x.fillStyle = C.gesso; x.fillRect(0, 0, 1024, 680);
  x.fillStyle = C.ink; x.fillRect(0, 0, 1024, 70); drawLogo(x, 120, 35, 150, C.gesso);
  x.fillStyle = C.ink; x.font = "400 92px " + SERIF; x.fillText("Il mondo di", 60, 190); x.font = "italic 400 92px " + SERIF; x.fillStyle = C.ruggine; x.fillText("Inverso", 520, 190);
  [C.gesso, C.ink, C.bosco, C.ruggine, C.sabbia].forEach((col, i) => { x.fillStyle = col; x.fillRect(60 + i * 180, 260, 160, 240); x.strokeStyle = "rgba(30,27,24,.3)"; x.strokeRect(60 + i * 180, 260, 160, 240); });
  x.fillStyle = "rgba(30,27,24,.55)"; x.font = "500 26px " + SANS; ["GESSO", "INCHIOSTRO", "BOSCO", "RUGGINE", "SABBIA"].forEach((nm, i) => x.fillText(nm, 64 + i * 180, 540));
  add(lid, new THREE.PlaneGeometry(w * 0.92, d * 0.86), new THREE.MeshBasicMaterial({ map: tx(c), toneMapped: false, color: new THREE.Color(0.75, 0.75, 0.75) }), 0, d / 2, 0.0005).userData.noshadow = true;
  return g;
}
function deskset(o) {
  const g = new THREE.Group();
  const mug = new THREE.Group(); mug.position.set(0.2, 0, 0.05); g.add(mug);
  add(mug, CY(0.042, 0.038, 0.095, 28), M(C.gesso, 0.3), 0, 0.0475, 0); add(mug, CY(0.037, 0.037, 0.002, 24), M("#3b2414", 0.2), 0, 0.085, 0); add(mug, new THREE.TorusGeometry(0.025, 0.007, 10, 20), M(C.gesso, 0.3), 0.045, 0.05, 0, 0, 0, 0);
  const nb = add(g, B(0.15, 0.018, 0.21), M(C.bosco, 0.7), -0.05, 0.009, 0.02, 0, 0.25, 0); add(g, B(0.006, 0.019, 0.212), M(C.ruggine, 0.6), -0.05 + 0.06 * Math.cos(0.25), 0.0095, 0.02 - 0.06 * Math.sin(0.25), 0, 0.25, 0);
  const cup = new THREE.Group(); cup.position.set(-0.22, 0, -0.08); g.add(cup); add(cup, CY(0.035, 0.035, 0.1, 20, 1), M(C.ruggine, 0.6), 0, 0.05, 0);
  for (let i = 0; i < 5; i++) { const a = i * 1.3; add(cup, CY(0.0035, 0.0035, 0.17, 6), M(["#c9a24a", C.ink, "#3b4f6b", "#c9a24a", C.red][i], 0.5), Math.cos(a) * 0.015, 0.12, Math.sin(a) * 0.015, Math.sin(a) * 0.15, 0, Math.cos(a) * 0.15); }
  return g;
}
function terrazzo(o) {
  const [sx, sz] = o.size, [c, x] = cv(1024, 1024); x.fillStyle = o.base || "#cfc6b6"; x.fillRect(0, 0, 1024, 1024);
  const cols = ["#2f3a2e", "#8a4b2d", "#b9ae98", "#efe9dd", "#1e1b18", "#a58a6a", "#6f7452", "#e6dccb"];
  for (let i = 0; i < 2600; i++) {
    const r = 2 + 9 * Math.pow(H(i, 1, 7), 2.4), px = H(i, 2, 7) * 1024, py = H(i, 3, 7) * 1024; x.fillStyle = cols[Math.floor(H(i, 4, 7) * cols.length)];
    x.beginPath(); for (let k = 0; k < 6; k++) { const a = k * Math.PI / 3 + H(i, k, 8), rr = r * (0.6 + 0.6 * H(i, k, 9)); x.lineTo(px + Math.cos(a) * rr, py + Math.sin(a) * rr); } x.closePath(); x.fill();
  }
  grain(x, 1024, 1024, 4000, 0.05, 2);
  const t = tx(c, [sx / 1.6, sz / 1.6]); const m = add(new THREE.Group(), new THREE.PlaneGeometry(sx, sz), new THREE.MeshStandardMaterial({ map: t, roughness: o.rough ?? 0.32, metalness: 0.02 }), 0, 0, 0, -Math.PI / 2, 0, 0);
  m.userData.floor = true; return m.parent;
}

export const STUDIO = new Set(["wordblocks", "seampanel", "fastrail", "wallclock", "shoeboxes", "sneaker", "cityview", "crittall", "bookshelf", "pinboard", "swatchwall", "axisline", "crossmark", "laptop", "deskset", "terrazzo"]);
export function buildStudio(o) {
  switch (o.type) {
    case "wordblocks": return wordblocks(o);
    case "seampanel": return seampanel(o);
    case "fastrail": return fastrail(o);
    case "wallclock": return wallclock(o);
    case "shoeboxes": return shoeboxes(o);
    case "sneaker": return sneaker(o);
    case "cityview": return cityview(o);
    case "crittall": return crittall(o);
    case "bookshelf": return bookshelf(o);
    case "pinboard": return pinboard(o);
    case "swatchwall": return swatchwall(o);
    case "axisline": return axisline(o);
    case "crossmark": return crossmark(o);
    case "laptop": return laptop(o);
    case "deskset": return deskset(o);
    case "terrazzo": return terrazzo(o);
    default: return null;
  }
}
