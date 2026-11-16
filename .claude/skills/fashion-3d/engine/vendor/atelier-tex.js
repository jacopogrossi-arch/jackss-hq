// atelier-tex.js: procedural textures for the atelier kit (14/11/2026): woven cloth with a real normal map, metric UVs, stitches, pchip curves.
// Everything is drawn once on canvases (no files). Pure and deterministic.
import * as THREE from "./three.module.min.js";

export const hash2 = (x, y = 0, z = 0) => { const s = Math.sin(x * 127.1 + y * 311.7 + z * 74.7) * 43758.5453; return s - Math.floor(s); };
export const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
export const smooth = (k) => { k = clamp(k); return k * k * (3 - 2 * k); };
export const lerp = (a, b, k) => a + (b - a) * k;
export const wrap = (a) => { a = (a + Math.PI) % (Math.PI * 2); if (a < 0) a += Math.PI * 2; return a - Math.PI; };
export const groove = (a, at, w) => Math.exp(-Math.pow(wrap(a - at) / w, 2));
export const shade = (hex, k) => new THREE.Color(hex).multiplyScalar(k);

export function pchip(xs, ys) {                           // a smooth monotone curve through (xs, ys)
  const n = xs.length, d = [], m = new Array(n);
  for (let i = 0; i < n - 1; i++) d[i] = (ys[i + 1] - ys[i]) / (xs[i + 1] - xs[i]);
  m[0] = d[0]; m[n - 1] = d[n - 2];
  for (let i = 1; i < n - 1; i++) m[i] = d[i - 1] * d[i] <= 0 ? 0 : (d[i - 1] + d[i]) / 2;
  return (x) => {
    x = clamp(x, xs[0], xs[n - 1]); let k = 0; while (k < n - 2 && x > xs[k + 1]) k++;
    const h = xs[k + 1] - xs[k], t = (x - xs[k]) / h, t2 = t * t, t3 = t2 * t;
    return (2 * t3 - 3 * t2 + 1) * ys[k] + (t3 - 2 * t2 + t) * h * m[k] + (-2 * t3 + 3 * t2) * ys[k + 1] + (t3 - t2) * h * m[k + 1];
  };
}

const _cache = {};
// tileable cloth maps: kind "twill" (drill, diagonal ridges), "plain" (calico), "linen" (slubs). One tile = 512 px; use TILE metres per tile in the UVs.
export const TILE = 0.08;
export function fabricMaps(kind = "twill") {
  if (_cache[kind]) return _cache[kind];
  const N = 512, h = new Float32Array(N * N), P = kind === "twill" ? 32 : kind === "linen" ? 16 : 16;
  for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) {
    let v;
    if (kind === "twill") { const d = (((x - y) % P) + P) % P / P; v = Math.pow(0.5 + 0.5 * Math.sin(d * Math.PI * 2), 1.4) * 0.8 + (0.5 + 0.5 * Math.sin((x + y) * Math.PI * 2 / (P / 4))) * 0.2; }
    else { v = 0.5 + 0.5 * Math.sin(x * Math.PI * 2 / P) * Math.sin(y * Math.PI * 2 / P); if (kind === "linen") v *= 0.75 + 0.5 * hash2(Math.floor(y / 2), 3) * hash2(Math.floor(x / 5), 7) + 0.25 * hash2(Math.floor(x / 2), 9); }
    h[y * N + x] = v * (0.93 + 0.07 * hash2(x, y));
  }
  const cc = document.createElement("canvas"), nc = document.createElement("canvas"); cc.width = cc.height = nc.width = nc.height = N;
  const cx = cc.getContext("2d"), nx = nc.getContext("2d"), ci = cx.createImageData(N, N), ni = nx.createImageData(N, N), at = (x, y) => h[((y + N) % N) * N + ((x + N) % N)];
  for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) {
    const i = (y * N + x) * 4, v = h[y * N + x], g = Math.round(255 * (0.76 + 0.24 * v));
    ci.data[i] = ci.data[i + 1] = ci.data[i + 2] = g; ci.data[i + 3] = 255;
    const dx = (at(x - 1, y) - at(x + 1, y)) * 2.4, dy = (at(x, y - 1) - at(x, y + 1)) * 2.4, l = Math.hypot(dx, dy, 1);
    ni.data[i] = Math.round((dx / l * 0.5 + 0.5) * 255); ni.data[i + 1] = Math.round((dy / l * 0.5 + 0.5) * 255); ni.data[i + 2] = Math.round((1 / l * 0.5 + 0.5) * 255); ni.data[i + 3] = 255;
  }
  cx.putImageData(ci, 0, 0); nx.putImageData(ni, 0, 0);
  const mk = (c, srgb) => { const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.anisotropy = 16; if (srgb) t.colorSpace = THREE.SRGBColorSpace; return t; };
  return (_cache[kind] = { map: mk(cc, true), normal: mk(nc, false) });
}
export function clothMat(color, kind = "twill", o = {}) {
  const m = fabricMaps(kind);
  return new THREE.MeshStandardMaterial({ color, map: m.map, normalMap: m.normal, normalScale: new THREE.Vector2(o.n ?? 0.7, o.n ?? 0.7), roughness: o.rough ?? 0.92, metalness: 0, side: o.side ?? THREE.FrontSide });
}

// a lofted surface of revolution-like tubes with METRIC uvs (tile = TILE metres) so the weave has the same size on every part
export function loftGeo(f, y0, y1, seg = 144, steps = 120, flip = false) {   // f(y, a) -> [x, y, z]
  const pos = [], uv = [], idx = [];
  let prev = null;
  for (let j = 0; j <= steps; j++) {
    const y = lerp(y0, y1, j / steps);
    for (let i = 0; i <= seg; i++) {
      const a = (i / seg) * Math.PI * 2, p = f(y, a); pos.push(p[0], p[1], p[2]);
      const r = Math.hypot(p[0], p[2]); uv.push(i / seg * Math.PI * 2 * Math.max(0.05, f.rad ? f.rad(y) : r) / TILE, y / TILE);
    }
  }
  for (let j = 0; j < steps; j++) for (let i = 0; i < seg; i++) { const p = j * (seg + 1) + i; if (flip) idx.push(p, p + seg + 1, p + 1, p + 1, p + seg + 1, p + seg + 2); else idx.push(p, p + 1, p + seg + 1, p + 1, p + seg + 2, p + seg + 1); }
  const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3)); g.setAttribute("uv", new THREE.Float32BufferAttribute(uv, 2)); g.setIndex(idx); g.computeVertexNormals(); return g;
}

// stitches: little capsules every `gap` metres along a polyline (instanced, no shadows)
export function stitches(points, color, gap = 0.0055, len = 0.0034, r = 0.00085) {
  const segs = []; let total = 0;
  for (let i = 0; i < points.length - 1; i++) { const a = new THREE.Vector3(...points[i]), b = new THREE.Vector3(...points[i + 1]), l = a.distanceTo(b); segs.push([a, b, l, total]); total += l; }
  const n = Math.max(1, Math.floor(total / gap)), geo = new THREE.CapsuleGeometry(r, len, 2, 5), im = new THREE.InstancedMesh(geo, new THREE.MeshStandardMaterial({ color, roughness: 0.7 }), n);
  const M = new THREE.Matrix4(), q = new THREE.Quaternion(), P = new THREE.Vector3(), S = new THREE.Vector3(1, 1, 1), up = new THREE.Vector3(0, 1, 0); let k = 0;
  for (let i = 0; i < n; i++) {
    const d = (i + 0.5) * gap; let s = segs.find((e) => d >= e[3] && d <= e[3] + e[2]); if (!s) s = segs[segs.length - 1];
    const t = clamp((d - s[3]) / Math.max(1e-6, s[2])), dir = s[1].clone().sub(s[0]).normalize(); P.copy(s[0]).lerp(s[1], t); q.setFromUnitVectors(up, dir); M.compose(P, q, S); im.setMatrixAt(k++, M);
  }
  im.count = k; im.userData.noshadow = true; im.castShadow = false; return im;
}
export function tube(points, r, mat, seg = 24) { return new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(points.map((p) => new THREE.Vector3(...p))), seg, r, 5, false), mat); }

// plain canvas textures used all over the room
export function canvasTex(w, h, draw, srgb = true, rep) {
  const c = document.createElement("canvas"); c.width = w; c.height = h; draw(c.getContext("2d"), w, h);
  const t = new THREE.CanvasTexture(c); t.anisotropy = 16; if (srgb) t.colorSpace = THREE.SRGBColorSpace; if (rep) { t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(rep[0], rep[1]); } return t;
}
