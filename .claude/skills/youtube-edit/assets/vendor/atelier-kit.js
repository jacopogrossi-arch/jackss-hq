// atelier-kit.js: the props of a tailor's atelier for world3d (14/11/2026, from the "autogrill" reference: a dense, readable, cartoon-but-real room).
// build(o, H) -> a THREE.Group for kit types, or null for any other type. H = { fabric, shade } from world3d.js. Everything is deterministic (hash, no random).
// Units are metres, y up, every prop stands on y = 0 (a prop that hangs says so). Meshes that must not cast a shadow carry userData.noshadow.
import * as THREE from "./three.module.min.js";
import { trouserHi } from "./atelier-trouser.js";
import { buildProp, PROPS } from "./atelier-props.js";
import { fabricMaps } from "./atelier-tex.js";

const hash = (a, b = 0, c = 0) => { const x = Math.sin(a * 127.1 + b * 311.7 + c * 74.7) * 43758.5453; return x - Math.floor(x); };
export const PAL = ["#2f3a2e", "#8a4b2d", "#b9ae98", "#efe9dd", "#3b4f6b", "#6f7452", "#c9a24a", "#7a2f2f", "#4d6b5c", "#1e1b18", "#a58a6a", "#5d6b7a"];
const WOOD = "#b98a5a", WOOD_D = "#6b4a30";
const std = (c, r = 0.7, m = 0) => new THREE.MeshStandardMaterial({ color: c, roughness: r, metalness: m });
const B = (w, h, d) => new THREE.BoxGeometry(w, h, d);
const CY = (r1, r2, h, s = 20) => new THREE.CylinderGeometry(r1, r2, h, s);
function add(g, geo, mat, x = 0, y = 0, z = 0, rx = 0, ry = 0, rz = 0) { const m = new THREE.Mesh(geo, mat); m.position.set(x, y, z); m.rotation.set(rx, ry, rz); g.add(m); return m; }
const tex = (c, rep) => { const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; if (rep) { t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(rep[0], rep[1]); } return t; };
const cv = (w, h) => { const c = document.createElement("canvas"); c.width = w; c.height = h; return [c, c.getContext("2d")]; };
function halo(color, op = 0.8) {
  const [c, x] = cv(256, 256), k = new THREE.Color(color), rgb = Math.round(k.r * 255) + "," + Math.round(k.g * 255) + "," + Math.round(k.b * 255), r = x.createRadialGradient(128, 128, 0, 128, 128, 128);
  r.addColorStop(0, "rgba(" + rgb + ",.95)"); r.addColorStop(0.25, "rgba(" + rgb + ",.5)"); r.addColorStop(0.55, "rgba(" + rgb + ",.14)"); r.addColorStop(1, "rgba(" + rgb + ",0)"); x.fillStyle = r; x.fillRect(0, 0, 256, 256);
  const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: tex(c), blending: THREE.AdditiveBlending, depthWrite: false, transparent: true, opacity: op })); return s;
}
const noShadow = (g) => g.traverse((m) => { if (m.isMesh) m.userData.noshadow = true; });

// ---------- surfaces
function woodTex() {
  const [c, x] = cv(512, 512), n = 16, pw = 512 / n;
  for (let i = 0; i < n; i++) {
    const base = 0.86 + 0.22 * hash(i, 1, 2); x.fillStyle = "rgb(" + Math.round(176 * base) + "," + Math.round(120 * base) + "," + Math.round(76 * base) + ")"; x.fillRect(0, i * pw, 512, pw);
    for (let k = 0; k < 14; k++) { x.strokeStyle = "rgba(60,32,14," + (0.05 + 0.07 * hash(i, k, 3)).toFixed(3) + ")"; x.lineWidth = 1; const y = i * pw + hash(i, k, 4) * pw; x.beginPath(); x.moveTo(0, y); x.bezierCurveTo(170, y + 2 * hash(i, k, 5), 340, y - 2, 512, y + 1); x.stroke(); }
    const j = hash(i, 9, 9) * 512; x.fillStyle = "rgba(40,22,10,.55)"; x.fillRect(j, i * pw, 2, pw);
    x.fillStyle = "rgba(40,22,10,.6)"; x.fillRect(0, i * pw, 512, 1.5);
  }
  return tex(c, [1, 1]);
}
function floorBoards(o) {
  const [sx, sz] = o.size, t = woodTex(); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(sx / 2.0, sz / 2.0);
  const m = new THREE.Mesh(new THREE.PlaneGeometry(sx, sz), new THREE.MeshStandardMaterial({ map: t, roughness: o.rough ?? 0.5, metalness: 0, color: o.color || "#ffffff" })); m.rotation.x = -Math.PI / 2; m.userData.floor = true;
  const g = new THREE.Group(); g.add(m); return g;
}
function wallPanel(o) {                                  // size [length, height, thickness]; hole [cx, cy, w, h] (cx from the wall's centre, cy from the floor) leaves a window opening
  const [L, Hh, T] = o.size, mat = std(o.color || "#dccfb6", 0.95), g = new THREE.Group();
  if (!o.hole) add(g, B(L, Hh, T), mat, 0, Hh / 2, 0);
  else {
    const [cx, cy, w, h] = o.hole, l = cx - w / 2 + L / 2, r = L / 2 - (cx + w / 2);
    add(g, B(l, Hh, T), mat, -L / 2 + l / 2, Hh / 2, 0); add(g, B(r, Hh, T), mat, L / 2 - r / 2, Hh / 2, 0);
    add(g, B(w, cy - h / 2, T), mat, cx, (cy - h / 2) / 2, 0); add(g, B(w, Hh - cy - h / 2, T), mat, cx, Hh - (Hh - cy - h / 2) / 2, 0);
  }
  add(g, B(L, 0.14, T + 0.03), std(o.base || WOOD_D, 0.6), 0, 0.07, 0);                                    // skirting
  if (o.rail !== false) add(g, B(L, 0.05, T + 0.02), std(o.base || WOOD_D, 0.6), 0, 1.05, 0);                  // a dado rail: the wall is not a flat slab
  return g;
}
function windowFrame(o) {                                // size [w, h]; its local origin is the middle of the opening; light comes through its glass
  const [w, h] = o.size, g = new THREE.Group(), fr = std("#f1ece0", 0.55), d = 0.1, f = 0.06;
  add(g, B(w + 2 * f, f, d), fr, 0, h / 2 + f / 2, 0); add(g, B(w + 2 * f, f, d), fr, 0, -h / 2 - f / 2, 0); add(g, B(f, h, d), fr, -w / 2 - f / 2, 0, 0); add(g, B(f, h, d), fr, w / 2 + f / 2, 0, 0);
  add(g, B(0.035, h, 0.05), fr, 0, 0, 0); add(g, B(w, 0.035, 0.05), fr, 0, h * 0.18, 0);                       // the cross: the only shadow the window makes
  add(g, B(w + 0.24, 0.05, 0.22), fr, 0, -h / 2 - f - 0.025, 0.08);                                           // sill
  const [c, x] = cv(4, 256), gr = x.createLinearGradient(0, 0, 0, 256); gr.addColorStop(0, "#dfe9f2"); gr.addColorStop(0.55, "#fff6e2"); gr.addColorStop(1, "#ffe2b0"); x.fillStyle = gr; x.fillRect(0, 0, 4, 256);
  const gl = add(g, new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ map: tex(c), toneMapped: false }), 0, 0, -0.02); gl.userData.noshadow = true;
  const hl = halo("#fff0cf", o.glow ?? 0.55); hl.scale.set(w * 2.4, h * 2.2, 1); hl.position.set(0, 0, 0.25); g.add(hl);
  return g;
}

// ---------- fabric stock
function rollRack(o) {                                   // size [length, height, depth]: cubbies each holding a roll of cloth lying on its side, or a folded stack
  const [L, Hh, D] = o.size, g = new THREE.Group(), wood = std(o.wood || WOOD, 0.7), cols = o.cols || Math.max(2, Math.round(L / 0.36)), rows = o.rows || Math.max(2, Math.round(Hh / 0.38)), cw = L / cols, rh = Hh / rows;
  const pal = o.palette || PAL;
  add(g, B(L, Hh, 0.03), std(WOOD_D, 0.8), 0, Hh / 2, -D / 2 + 0.015);
  for (let i = 0; i <= cols; i++) add(g, B(0.03, Hh, D), wood, -L / 2 + i * cw, Hh / 2, 0);
  for (let r = 0; r <= rows; r++) add(g, B(L, 0.03, D), wood, 0, r * rh, 0);
  const rolls = [], stacks = [];
  for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) {
    const h1 = hash(c, r, o.seed || 1), x = -L / 2 + (c + 0.5) * cw, y = r * rh;
    if (h1 < 0.62) { const rad = Math.min(cw, rh) * (0.3 + 0.12 * hash(c, r, 7)); rolls.push([x, y + 0.015 + rad, 0.02, rad, pal[Math.floor(hash(c, r, 3) * pal.length)], D * 0.86]); }
    else if (h1 < 0.9) { const n = 3 + Math.floor(hash(c, r, 5) * 3); for (let k = 0; k < n; k++) stacks.push([x, y + 0.015 + 0.035 + k * 0.058, 0.02, cw - 0.07, 0.054, D * 0.8, pal[Math.floor(hash(c, r, 11 + k) * pal.length)]]); }
  }
  const fm = fabricMaps("plain"), cm = () => new THREE.MeshStandardMaterial({ color: "#ffffff", roughness: 0.95, map: fm.map, normalMap: fm.normal }), sUV = (geo, u, v) => { const uv = geo.attributes.uv; for (let i = 0; i < uv.count; i++) uv.setXY(i, uv.getX(i) * u, uv.getY(i) * v); return geo; };
  const mkI = (geo, n) => new THREE.InstancedMesh(geo, cm(), Math.max(1, n)), M = new THREE.Matrix4(), q = new THREE.Quaternion(), P = new THREE.Vector3(), S = new THREE.Vector3(), Cc = new THREE.Color();
  const ri = mkI(sUV(CY(1, 1, 1, 24), 9, 5), rolls.length); q.setFromEuler(new THREE.Euler(Math.PI / 2, 0, 0));
  rolls.forEach((a, i) => { P.set(a[0], a[1], a[2]); S.set(a[3], a[5], a[3]); M.compose(P, q, S); ri.setMatrixAt(i, M); ri.setColorAt(i, Cc.set(a[4]).multiplyScalar(0.9 + 0.1 * hash(i, 1, 1))); }); ri.count = rolls.length;
  const si = mkI(sUV(B(1, 1, 1), 5, 1), stacks.length); q.identity();
  stacks.forEach((a, i) => { P.set(a[0], a[1], a[2]); S.set(a[3], a[4], a[5]); M.compose(P, q, S); si.setMatrixAt(i, M); si.setColorAt(i, Cc.set(a[6]).multiplyScalar(0.92)); }); si.count = stacks.length;
  g.add(ri); g.add(si); return g;
}
function bolts(o) {                                      // a pile of folded cloth: size [w, d]; n layers, each a woven slab with a rolled fold on the front edge
  const [w, d] = o.size, g = new THREE.Group(), n = o.n || 5, pal = o.palette || PAL, fm = fabricMaps("plain"), th = 0.06;
  for (let k = 0; k < n; k++) {
    const col = pal[Math.floor(hash(k, o.seed || 2, 8) * pal.length)], mat = new THREE.MeshStandardMaterial({ color: col, roughness: 0.95, map: fm.map, normalMap: fm.normal }), ww = w * (0.96 - 0.02 * (k % 3)), dd = d * (0.96 - 0.03 * (k % 2));
    const L = new THREE.Group(); L.position.set(0.012 * Math.sin(k * 2.3), 0.032 + k * (th + 0.004), 0.01 * Math.cos(k * 1.7)); L.rotation.y = 0.05 * Math.sin(k * 2.1); g.add(L);
    const geo = B(ww, th * 0.9, dd - th), uv = geo.attributes.uv; for (let i = 0; i < uv.count; i++) uv.setXY(i, uv.getX(i) * ww / 0.08, uv.getY(i) * dd / 0.08); add(L, geo, mat, 0, 0, -th / 2);
    const fold = CY(th / 2, th / 2, ww, 20), fu = fold.attributes.uv; for (let i = 0; i < fu.count; i++) fu.setXY(i, fu.getX(i) * 3, fu.getY(i) * ww / 0.08); add(L, fold, mat, 0, 0, dd / 2 - th, 0, 0, Math.PI / 2);
  }
  return g;
}
function spoolWall(o) {                                  // size [w, h]: a wall rack of shelves with thread spools standing upright (coloured thread between two wooden flanges)
  const [W, Hh] = o.size, g = new THREE.Group(), pal = o.palette || PAL; add(g, B(W, Hh, 0.03), std(o.color || "#c9ae82", 0.9), 0, Hh / 2, 0);
  const rows = Math.floor(Hh / 0.13), cols = Math.floor(W / 0.062), n = rows * cols, thr = new THREE.InstancedMesh(CY(1, 1, 1, 18), std("#ffffff", 0.75), n), fl = new THREE.InstancedMesh(CY(1, 1, 1, 18), std("#d9b98a", 0.55), n * 2);
  const M = new THREE.Matrix4(), q = new THREE.Quaternion(), P = new THREE.Vector3(), S = new THREE.Vector3(), Cc = new THREE.Color(); let k = 0, f = 0;
  for (let r = 0; r < rows; r++) { const sy = 0.07 + r * 0.13; add(g, B(W - 0.04, 0.012, 0.07), std("#8a6a44", 0.8), 0, sy, 0.05);
    for (let c = 0; c < cols; c++) { const x = -W / 2 + 0.04 + c * ((W - 0.08) / Math.max(1, cols - 1)), run = Math.floor(c / (2 + Math.floor(hash(r, 1, 1) * 3))), hgt = 0.05 + 0.012 * hash(c, r, 9), base = sy + 0.006, z = 0.05 + 0.006 * (hash(c, r, 2) - 0.5);
      P.set(x, base + hgt / 2, z); S.set(0.019, hgt - 0.008, 0.019); M.compose(P, q, S); thr.setMatrixAt(k, M); thr.setColorAt(k, Cc.set(pal[Math.floor(hash(run, r, 4) * pal.length)]).multiplyScalar(0.8 + 0.25 * hash(c, r, 6))); k++;
      for (const yy of [base + 0.002, base + hgt - 0.002]) { P.set(x, yy, z); S.set(0.024, 0.004, 0.024); M.compose(P, q, S); fl.setMatrixAt(f++, M); } } }
  thr.count = k; fl.count = f; g.add(thr); g.add(fl); return g;
}

// ---------- the workshop furniture
function table(o) {                                      // size [length, height, depth]: a cutting table, wooden top, a lower shelf
  const [L, Hh, D] = o.size, g = new THREE.Group(), wood = std(o.color || WOOD, 0.55), dark = std(WOOD_D, 0.7);
  add(g, B(L, 0.05, D), wood, 0, Hh - 0.025, 0); add(g, B(L - 0.1, 0.08, D - 0.1), dark, 0, Hh - 0.09, 0);
  for (const sx of [-1, 1]) for (const sz of [-1, 1]) add(g, B(0.07, Hh - 0.05, 0.07), dark, sx * (L / 2 - 0.07), (Hh - 0.05) / 2, sz * (D / 2 - 0.07));
  add(g, B(L - 0.14, 0.03, D - 0.14), dark, 0, 0.22, 0);
  if (o.shelfstuff !== false) { for (let i = 0; i < 4; i++) add(g, B(0.4, 0.07, 0.3), std(PAL[(i * 3) % PAL.length], 0.95), -L / 2 + 0.35 + i * 0.5, 0.275 + 0.035, 0.0); }
  return g;
}
function drawBoard(kind, w, h) {
  const [c, x] = cv(2048, Math.round(2048 * h / w));
  x.scale(2, 2);
  const W = 1024, Hh = c.height / 2;
  if (kind === "pattern") {                              // kraft paper with the pieces of a trouser pattern: outlines, grain arrows, notches
    x.fillStyle = "#c8a878"; x.fillRect(0, 0, W, Hh);
    for (let i = 0; i < 900; i++) { x.fillStyle = "rgba(90,60,30," + (0.03 + 0.05 * hash(i, 1, 1)).toFixed(3) + ")"; x.fillRect(hash(i, 2, 2) * W, hash(i, 3, 3) * Hh, 2 + 6 * hash(i, 4, 4), 1); }
    x.strokeStyle = "#241a12"; x.lineWidth = 5; x.lineJoin = "round"; x.fillStyle = "rgba(255,250,235,.28)";
    const piece = (ox, oy, k) => { x.beginPath(); x.moveTo(ox + 0.04 * W, oy); x.lineTo(ox + 0.34 * W, oy); x.lineTo(ox + 0.36 * W, oy + 0.08 * Hh); x.quadraticCurveTo(ox + 0.33 * W, oy + 0.22 * Hh, ox + 0.31 * W, oy + 0.44 * Hh); x.lineTo(ox + 0.29 * W, oy + 0.9 * Hh); x.lineTo(ox + 0.06 * W, oy + 0.9 * Hh); x.lineTo(ox + 0.04 * W * k, oy + 0.4 * Hh); x.quadraticCurveTo(ox + 0.0, oy + 0.18 * Hh, ox + 0.04 * W, oy); x.closePath(); x.fill(); x.stroke();
      x.setLineDash([14, 12]); x.lineWidth = 3; x.beginPath(); x.moveTo(ox + 0.18 * W, oy + 0.1 * Hh); x.lineTo(ox + 0.18 * W, oy + 0.82 * Hh); x.stroke(); x.setLineDash([]); x.lineWidth = 5;
      x.beginPath(); x.moveTo(ox + 0.18 * W, oy + 0.1 * Hh); x.lineTo(ox + 0.165 * W, oy + 0.15 * Hh); x.moveTo(ox + 0.18 * W, oy + 0.1 * Hh); x.lineTo(ox + 0.195 * W, oy + 0.15 * Hh); x.stroke();
      for (const ny of [0.3, 0.52, 0.74]) { x.beginPath(); x.moveTo(ox + 0.31 * W, oy + ny * Hh); x.lineTo(ox + 0.335 * W, oy + ny * Hh); x.stroke(); } };
    piece(0.04 * W, 0.04 * Hh, 1); piece(0.40 * W, 0.04 * Hh, 0.2);
    x.fillStyle = "#241a12"; x.font = "italic 500 " + Math.round(W * 0.05) + 'px "Playfair Display", Georgia, serif'; x.fillText("davanti", 0.1 * W, 0.97 * Hh); x.fillText("dietro", 0.46 * W, 0.97 * Hh);
    x.strokeStyle = "#241a12"; x.lineWidth = 5; x.beginPath(); x.moveTo(0.78 * W, 0.15 * Hh); x.lineTo(0.96 * W, 0.15 * Hh); x.lineTo(0.96 * W, 0.7 * Hh); x.stroke();
  } else if (kind === "sketch") {                        // a croquis of the Drop 1 trouser on cream paper (front, technical line)
    x.fillStyle = "#f3ede0"; x.fillRect(0, 0, W, Hh); x.strokeStyle = "rgba(30,27,24,.1)"; x.lineWidth = 1; for (let i = 0; i < W; i += 32) { x.beginPath(); x.moveTo(i, 0); x.lineTo(i, Hh); x.stroke(); } for (let j = 0; j < Hh; j += 32) { x.beginPath(); x.moveTo(0, j); x.lineTo(W, j); x.stroke(); }
    x.strokeStyle = "#1e1b18"; x.lineWidth = 6; x.lineJoin = "round"; x.lineCap = "round"; const cx = W / 2, t = 0.08 * Hh, b = 0.92 * Hh;
    x.beginPath(); x.moveTo(cx - 0.2 * W, t); x.lineTo(cx + 0.2 * W, t); x.lineTo(cx + 0.21 * W, t + 0.07 * Hh); x.lineTo(cx + 0.23 * W, b); x.lineTo(cx + 0.03 * W, b); x.lineTo(cx, t + 0.5 * Hh); x.lineTo(cx - 0.03 * W, b); x.lineTo(cx - 0.23 * W, b); x.lineTo(cx - 0.21 * W, t + 0.07 * Hh); x.closePath(); x.stroke();
    x.lineWidth = 4; for (const s of [-1, 1]) { x.beginPath(); x.moveTo(cx + s * 0.09 * W, t + 0.07 * Hh); x.lineTo(cx + s * 0.085 * W, t + 0.2 * Hh); x.moveTo(cx + s * 0.13 * W, t + 0.07 * Hh); x.lineTo(cx + s * 0.125 * W, t + 0.19 * Hh); x.stroke(); x.beginPath(); x.moveTo(cx + s * 0.2 * W, t + 0.1 * Hh); x.quadraticCurveTo(cx + s * 0.17 * W, t + 0.17 * Hh, cx + s * 0.16 * W, t + 0.22 * Hh); x.stroke(); }
    x.beginPath(); x.moveTo(cx - 0.2 * W, t + 0.07 * Hh); x.lineTo(cx + 0.21 * W, t + 0.07 * Hh); x.stroke();
    x.fillStyle = "#8a4b2d"; x.font = "italic 500 " + Math.round(W * 0.06) + 'px "Playfair Display", Georgia, serif'; x.fillText("Drop 1", 0.06 * W, 0.08 * Hh); x.fillStyle = "#1e1b18"; x.font = "500 " + Math.round(W * 0.03) + "px Inter, sans-serif"; x.fillText("doppia piega · vita naturale", 0.06 * W, 0.13 * Hh);
  } else if (kind === "swatch") {                        // a board of cloth swatches
    x.fillStyle = "#efe9dd"; x.fillRect(0, 0, W, Hh); const nx = 4, ny = Math.max(2, Math.round(4 * h / w)), gw = W / nx, gh = Hh / ny;
    for (let i = 0; i < nx; i++) for (let j = 0; j < ny; j++) { x.fillStyle = PAL[(i * 3 + j * 5 + 1) % PAL.length]; x.fillRect(i * gw + gw * 0.08, j * gh + gh * 0.08, gw * 0.84, gh * 0.84); x.fillStyle = "rgba(255,255,255,.10)"; for (let k = 0; k < gh * 0.84; k += 8) x.fillRect(i * gw + gw * 0.08, j * gh + gh * 0.08 + k, gw * 0.84, 3); }
  } else {                                               // "lines": a moodboard of simple shapes
    x.fillStyle = "#efe9dd"; x.fillRect(0, 0, W, Hh); for (let i = 0; i < 5; i++) { x.fillStyle = PAL[(i * 2 + 1) % PAL.length]; x.fillRect(W * (0.06 + 0.18 * i), Hh * (0.12 + 0.3 * hash(i, 1, 1)), W * 0.14, Hh * (0.3 + 0.3 * hash(i, 2, 2))); }
  }
  return tex(c);
}
function paper(o) {                                      // a sheet lying flat on a surface: size [w, d], kind "pattern" | "sketch" | "swatch" | "lines"
  const [w, d] = o.size, m = new THREE.Mesh(new THREE.PlaneGeometry(w, d), new THREE.MeshStandardMaterial({ map: drawBoard(o.kind || "pattern", w, d), roughness: 0.92, side: THREE.DoubleSide })); m.rotation.x = -Math.PI / 2; m.position.y = 0.002;
  const g = new THREE.Group(); g.add(m); return g;
}
function frame(o) {                                      // a framed picture on a wall: size [w, h]; kind as paper; local origin = its centre, facing +z
  const [w, h] = o.size, g = new THREE.Group(), fr = std(o.color || "#1e1b18", 0.5), t = 0.035;
  add(g, B(w, t, 0.04), fr, 0, h / 2 - t / 2, 0); add(g, B(w, t, 0.04), fr, 0, -h / 2 + t / 2, 0); add(g, B(t, h, 0.04), fr, -w / 2 + t / 2, 0, 0); add(g, B(t, h, 0.04), fr, w / 2 - t / 2, 0, 0);
  add(g, new THREE.PlaneGeometry(w - 2 * t, h - 2 * t), new THREE.MeshStandardMaterial({ map: drawBoard(o.kind || "sketch", w, h), roughness: 0.9 }), 0, 0, 0.005); return g;
}
function ruler(o) {                                      // a flat strip with ticks: a ruler or a tape measure; size [length, width]
  const [L, Wd] = o.size, [c, x] = cv(1024, 64); x.fillStyle = o.color || "#f0c93a"; x.fillRect(0, 0, 1024, 64); x.fillStyle = "#1e1b18";
  for (let i = 0; i <= 50; i++) x.fillRect(i * 20.4, 0, 2, i % 5 === 0 ? 30 : 16); x.font = "600 18px Inter, sans-serif"; for (let i = 0; i < 10; i++) x.fillText(String(i * 10), i * 102 + 6, 54);
  const m = new THREE.Mesh(new THREE.PlaneGeometry(L, Wd), new THREE.MeshStandardMaterial({ map: tex(c), roughness: 0.6, side: THREE.DoubleSide })); m.rotation.x = -Math.PI / 2; m.position.y = 0.003; const g = new THREE.Group(); g.add(m); return g;
}
function shears(o) {                                     // tailor's shears lying flat; ~25 cm long, blades along +x
  const g = new THREE.Group(), steel = std("#c9ccd1", 0.25, 0.9), blk = std("#1e1b18", 0.5, 0.1), org = std("#c8501f", 0.5, 0.1);
  add(g, B(0.2, 0.006, 0.026), steel, 0.12, 0.014, 0.008, 0, -0.05, 0); add(g, B(0.2, 0.006, 0.026), steel, 0.12, 0.022, -0.008, 0, 0.05, 0);
  const t1 = add(g, new THREE.TorusGeometry(0.03, 0.007, 8, 22), blk, -0.055, 0.016, 0.03, Math.PI / 2, 0, 0), t2 = add(g, new THREE.TorusGeometry(0.036, 0.008, 8, 22), org, -0.058, 0.016, -0.03, Math.PI / 2, 0, 0);
  add(g, B(0.1, 0.008, 0.012), steel, -0.0, 0.016, 0.01, 0, 0.35, 0); add(g, B(0.1, 0.008, 0.012), steel, -0.0, 0.02, -0.01, 0, -0.35, 0); return g;
}
function sewingMachine(o) {                              // ~40 cm, facing +z, standing on y = 0
  const g = new THREE.Group(), body = std(o.color || "#efe9dd", 0.35, 0.1), accent = std("#2f3a2e", 0.4, 0.2), steel = std("#c9ccd1", 0.25, 0.9);
  add(g, B(0.46, 0.035, 0.22), accent, 0, 0.018, 0); add(g, B(0.075, 0.27, 0.12), body, 0.17, 0.155, 0); add(g, B(0.38, 0.08, 0.12), body, -0.01, 0.285, 0); add(g, B(0.11, 0.14, 0.125), body, -0.17, 0.26, 0);
  add(g, CY(0.006, 0.006, 0.11, 8), steel, -0.17, 0.12, 0.0); add(g, B(0.1, 0.012, 0.09), steel, -0.17, 0.04, 0);
  add(g, CY(0.055, 0.055, 0.025, 28), accent, 0.225, 0.285, 0, Math.PI / 2, 0, 0); add(g, CY(0.02, 0.02, 0.07, 14), std("#8a4b2d", 0.6), 0.0, 0.355, 0); add(g, CY(0.004, 0.004, 0.05, 6), steel, 0.0, 0.4, 0);
  add(g, CY(0.025, 0.025, 0.02, 20), steel, 0.12, 0.34, 0, Math.PI / 2, 0, 0); return g;
}
function mannequin(o) {                                  // a dress form on a stand: ~1.6 m tall; o.tape draws a measuring tape round the chest
  const g = new THREE.Group(), lin = o.linen || "#d8ccb0", pts = [[0.001, 0.0], [0.13, 0.005], [0.16, 0.07], [0.18, 0.17], [0.165, 0.27], [0.15, 0.33], [0.17, 0.43], [0.188, 0.52], [0.18, 0.6], [0.15, 0.66], [0.09, 0.7], [0.05, 0.725], [0.035, 0.78], [0.001, 0.78]];
  const geo = new THREE.LatheGeometry(pts.map((p) => new THREE.Vector2(p[0], p[1])), 32), tors = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({ color: lin, roughness: 0.95, side: THREE.DoubleSide, map: null }));
  tors.position.y = 0.84; tors.scale.set(1, 1, 0.72); g.add(tors);
  add(g, CY(0.018, 0.018, 0.84, 10), std("#2b2118", 0.5, 0.2), 0, 0.42, 0); add(g, new THREE.SphereGeometry(0.028, 14, 10), std(WOOD_D, 0.5), 0, 1.66, 0);
  add(g, CY(0.14, 0.14, 0.012, 20), std("#a58a6a", 0.6, 0.4), 0, 0.84, 0);
  for (let i = 0; i < 3; i++) { const a = i * Math.PI * 2 / 3 + 0.4, b = add(g, B(0.34, 0.035, 0.05), std(WOOD_D, 0.6), 0.17 * Math.cos(a), 0.02, 0.17 * Math.sin(a)); b.rotation.y = -a; add(g, CY(0.02, 0.02, 0.03, 10), std("#1e1b18", 0.8), 0.33 * Math.cos(a), 0.015, 0.33 * Math.sin(a)); }
  if (o.tape !== false) { const tp = add(g, new THREE.TorusGeometry(0.19, 0.006, 6, 40), std("#f0c93a", 0.6), 0, 1.38, 0, Math.PI / 2, 0, 0); tp.scale.set(1, 0.72, 1); tp.rotation.x = Math.PI / 2; }
  return g;
}
function pendant(o) {                                    // a hanging lamp: the origin is where the shade hangs; the cord runs up out of frame
  const [cord] = o.size || [2], g = new THREE.Group(), col = o.color || "#8a4b2d";
  add(g, CY(0.004, 0.004, cord, 6), std("#1e1b18", 0.9), 0, 0.2 + cord / 2, 0);
  add(g, new THREE.CylinderGeometry(0.05, 0.25, 0.2, 28, 1, true), new THREE.MeshStandardMaterial({ color: col, roughness: 0.35, metalness: 0.3, side: THREE.DoubleSide }), 0, 0.1, 0).userData.noshadow = true;
  add(g, new THREE.SphereGeometry(0.05, 14, 10), new THREE.MeshBasicMaterial({ color: "#fff1c8", toneMapped: false }), 0, 0.02, 0).userData.noshadow = true;
  const h = halo(o.glowColor || "#ffd98a", o.glow ?? 0.9); h.scale.set(1.5, 1.5, 1); h.position.set(0, -0.05, 0); g.add(h);
  if (o.light) { const pl = new THREE.PointLight(o.glowColor || "#ffd7a0", o.light, 5, 1.6); pl.position.set(0, -0.12, 0); g.add(pl); }
  return g;
}
function deskLamp(o) {                                   // an articulated desk lamp, ~45 cm
  const g = new THREE.Group(), m = std(o.color || "#2f3a2e", 0.4, 0.3);
  add(g, CY(0.07, 0.08, 0.02, 20), m, 0, 0.01, 0); add(g, CY(0.008, 0.008, 0.3, 8), m, 0, 0.17, 0, 0, 0, 0.3); add(g, CY(0.008, 0.008, 0.28, 8), m, 0.1, 0.4, 0, 0, 0, -0.9);
  add(g, new THREE.ConeGeometry(0.06, 0.1, 18, 1, true), new THREE.MeshStandardMaterial({ color: m.color, roughness: 0.4, metalness: 0.3, side: THREE.DoubleSide }), 0.24, 0.5, 0, 0, 0, -2.2).userData.noshadow = true;
  const h = halo("#ffd98a", 0.7); h.scale.set(0.6, 0.6, 1); h.position.set(0.28, 0.43, 0); g.add(h); return g;
}
function plant(o) {                                      // a potted rubber plant: a trunk, branches, and each leaf on its own stalk (no floating leaves)
  const hgt = (o.size && o.size[0]) || 1.1, g = new THREE.Group(); add(g, CY(0.16, 0.12, 0.3, 20), std("#a95f3b", 0.8), 0, 0.15, 0); add(g, CY(0.145, 0.145, 0.02, 20), std("#3a2a1c", 1), 0, 0.29, 0);
  const bark = std("#5a4030", 0.9), lc = ["#3f6a35", "#4d7a3f", "#3a5f31", "#5b8a48"]; add(g, CY(0.011, 0.017, hgt * 0.85, 8), bark, 0, 0.3 + hgt * 0.425, 0);
  for (let i = 0; i < 14; i++) {
    const a = i * 2.39996, y = 0.42 + hgt * 0.8 * (i / 14) + 0.03 * hash(i, 2, 2), r = 0.05 + 0.05 * hash(i, 1, 1), L = 0.17 + 0.06 * hash(i, 3, 3), up = 0.35 + 0.3 * hash(i, 4, 4);
    const arm = new THREE.Group(); arm.position.set(0, y, 0); arm.rotation.y = -a; g.add(arm);
    const tilt = new THREE.Group(); tilt.rotation.z = up; arm.add(tilt);
    add(tilt, CY(0.0035, 0.0045, r, 6), bark, r / 2, 0, 0, 0, 0, Math.PI / 2);
    const leaf = add(tilt, new THREE.SphereGeometry(1, 16, 10), std(lc[i % 4], 0.55), r + L / 2, 0, 0, 0, 0, -up - 0.25 * hash(i, 5, 5)); leaf.scale.set(L / 2, 0.006, 0.055 + 0.02 * hash(i, 6, 6));
  }
  return g;
}
function rail(o) {                                       // a garment rail: size [length, height]; a row of coats and shirts on hangers (the bar is at `height`)
  const [L, Hh] = o.size, g = new THREE.Group(), steel = std("#8b8f94", 0.35, 0.7), n = o.n || Math.floor(L / 0.095);
  add(g, CY(0.011, 0.011, L, 10), steel, 0, Hh, 0, 0, 0, Math.PI / 2);
  for (const s of [-1, 1]) { add(g, CY(0.011, 0.011, Hh, 10), steel, s * (L / 2 - 0.02), Hh / 2, 0); add(g, B(0.06, 0.03, 0.6), std("#1e1b18", 0.7), s * (L / 2 - 0.02), 0.015, 0); }
  const pal = o.palette || PAL;
  for (let i = 0; i < n; i++) {
    const x = -L / 2 + 0.1 + i * ((L - 0.2) / Math.max(1, n - 1)), col = pal[Math.floor(hash(i, o.seed || 3, 2) * pal.length)], len = 0.6 + 0.5 * hash(i, 4, 4), mat = std(col, 0.92), gg = new THREE.Group();
    add(gg, B(0.44, len, 0.07), mat, 0, -len / 2 - 0.05, 0); add(gg, B(0.13, len * 0.82, 0.075), mat, -0.28, -len * 0.45, 0, 0, 0, -0.06); add(gg, B(0.13, len * 0.82, 0.075), mat, 0.28, -len * 0.45, 0, 0, 0, 0.06);
    add(gg, B(0.2, 0.05, 0.08), std("#efe9dd", 0.9), 0, -0.06, 0.01); add(gg, new THREE.TorusGeometry(0.012, 0.0025, 6, 14, Math.PI * 1.6), steel, 0, 0.0, 0, 0, 0, 1.2);
    gg.position.set(x, Hh - 0.02, (hash(i, 5, 5) - 0.5) * 0.05); gg.rotation.y = 0.25 * (hash(i, 6, 6) - 0.5) + 1.0; g.add(gg);
  }
  return g;
}
function rug(o) {                                        // size [w, d]: a striped flat rug
  const [w, d] = o.size, [c, x] = cv(512, 512); x.fillStyle = o.color || "#b9ae98"; x.fillRect(0, 0, 512, 512);
  const cols = ["#8a4b2d", "#2f3a2e", "#efe9dd", "#1e1b18"]; for (let i = 0; i < 9; i++) { x.fillStyle = cols[i % cols.length]; x.fillRect(0, 30 + i * 52, 512, i % 3 === 0 ? 20 : 8); } x.strokeStyle = "#1e1b18"; x.lineWidth = 14; x.strokeRect(7, 7, 498, 498);
  const m = new THREE.Mesh(B(w, 0.012, d), new THREE.MeshStandardMaterial({ map: tex(c), roughness: 1 })); m.position.y = 0.006; const g = new THREE.Group(); g.add(m); return g;
}
function clothSheet(o) {                                 // cloth laid on a table with gentle folds: size [w, d], amp = fold height
  const [w, d] = o.size, geo = new THREE.PlaneGeometry(w, d, 48, 24), p = geo.attributes.position, amp = o.amp ?? 0.012;
  for (let i = 0; i < p.count; i++) { const x = p.getX(i), y = p.getY(i); p.setZ(i, amp * Math.sin(x * 14 + 0.8 * Math.sin(y * 5)) * (0.6 + 0.4 * Math.sin(y * 9 + 1)) + 0.5 * amp * Math.sin(y * 7 + x * 3)); } geo.computeVertexNormals();
  const m = new THREE.Mesh(geo, o.mat); m.rotation.x = -Math.PI / 2; m.position.y = 0.004; const g = new THREE.Group(); g.add(m); return g;
}

export const KIT = new Set(["woodfloor", "wall", "window", "rollrack", "bolts", "spoolwall", "table", "paper", "frame", "ruler", "shears", "sewing", "mannequin", "pendant", "desklamp", "plant", "rail", "rug", "cloth", "cuttingmat", "buttonjar", "pincushion", "spool", "hoop", "sketchdraw", "patterncut", "logoplate", "weight", "chalk", "lsquare", "pathdots", "floorbadge"]);
export function build(o, H) {
  if (PROPS.has(o.type)) return buildProp(o);
  switch (o.type) {
    case "trouser": return trouserHi(o);
    case "woodfloor": return floorBoards(o);
    case "wall": return wallPanel(o);
    case "window": return windowFrame(o);
    case "rollrack": return rollRack(o);
    case "bolts": return bolts(o);
    case "spoolwall": return spoolWall(o);
    case "table": return table(o);
    case "paper": return paper(o);
    case "frame": return frame(o);
    case "ruler": return ruler(o);
    case "shears": return shears(o);
    case "sewing": return sewingMachine(o);
    case "mannequin": return mannequin(o);
    case "pendant": return pendant(o);
    case "desklamp": return deskLamp(o);
    case "plant": return plant(o);
    case "rail": return rail(o);
    case "rug": return rug(o);
    case "cloth": return clothSheet({ ...o, mat: H.fabric(o.color || "#7b7d5a") });
    default: return null;
  }
}
