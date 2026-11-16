
// ---------- additions (demo-luce): a stylised Earth, glowing bodies, a dotted path
let _earth;
function earthTex() {
  if (_earth) return _earth;
  const W = 2048, H = 1024, c = document.createElement("canvas"); c.width = W; c.height = H; const g = c.getContext("2d");
  g.fillStyle = "#2478ad"; g.fillRect(0, 0, W, H);
  _earth = new THREE.CanvasTexture(c); _earth.colorSpace = THREE.SRGBColorSpace; return _earth;
}
function haloTex(color) {
  const c = document.createElement("canvas"); c.width = c.height = 256; const x = c.getContext("2d"), r = x.createRadialGradient(128, 128, 0, 128, 128, 128), k = new THREE.Color(color);
  const rgb = Math.round(k.r * 255) + "," + Math.round(k.g * 255) + "," + Math.round(k.b * 255);
  r.addColorStop(0, "rgba(" + rgb + ",.95)"); r.addColorStop(0.22, "rgba(" + rgb + ",.55)"); r.addColorStop(0.5, "rgba(" + rgb + ",.16)"); r.addColorStop(1, "rgba(" + rgb + ",0)");
  x.fillStyle = r; x.fillRect(0, 0, 256, 256); const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
}
function dots(o) {                                       // a row of small lit dots from pos to `to` (the dashed link of the flat plates, in space)
  const g = new THREE.Group(), n = o.n || 24, geo = new THREE.SphereGeometry((o.size && o.size[0] || 0.02) / 2, 12, 8), mat = new THREE.MeshBasicMaterial({ color: o.color || "#5EE6A8", toneMapped: false, transparent: true, opacity: o.alpha ?? 0.9 });
  for (let i = 0; i < n; i++) { const k = (i + 0.5) / n, m = new THREE.Mesh(geo, mat); m.position.set((o.to[0] - o.pos[0]) * k, (o.to[1] - o.pos[1]) * k, (o.to[2] - o.pos[2]) * k); g.add(m); }
  return g;
}

// ---------- store kit (autogrill): gondola shelves with products, tiled floor, gates
const hash = (a, b, c) => { const x = Math.sin(a * 127.1 + b * 311.7 + c * 74.7) * 43758.5453; return x - Math.floor(x); };
const PALS = {
  plastico: { body: "#f4efe6", prod: ["#e3c47f", "#f4efe6", "#5EE6A8", "#c9703f", "#d8c9a3", "#2f8f6a", "#e9e2d2"] },
  reale: { body: "#f3f3f0", prod: ["#e63946", "#ffb703", "#219ebc", "#8ecae6", "#fb8500", "#2a9d8f", "#f4f1de", "#d62828", "#6a4c93", "#90be6d", "#f28482"] },
};
function shelf(o) {
  if (o.theme) return shelf2(o);                         // v2: real products
  // size [length, height, depth]; products on both faces; o.accent = the colour of its header strip
  const [L, Hh, D] = o.size, look = PALS[o.look || "plastico"], g = new THREE.Group();
  const body = new THREE.MeshStandardMaterial({ color: o.color || look.body, roughness: 0.7, metalness: 0 });
  const add = (w, h, d, x, y, z, m) => { const b = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), m || body); b.position.set(x, y, z); g.add(b); return b; };
  add(L, 0.12, D, 0, 0.06, 0); add(L, Hh - 0.12, 0.04, 0, 0.12 + (Hh - 0.12) / 2, 0);
  const rows = o.rows || 4, rh = (Hh - 0.12) / rows;
  for (let r = 1; r <= rows; r++) add(L, 0.022, D, 0, 0.12 + r * rh - (r === rows ? 0 : 0.011), 0);
  add(0.04, Hh, D, -L / 2 + 0.02, Hh / 2, 0); add(0.04, Hh, D, L / 2 - 0.02, Hh / 2, 0);
  if (o.accent) add(L, 0.16, 0.05, 0, Hh + 0.1, 0, new THREE.MeshStandardMaterial({ color: o.accent, roughness: 0.5, emissive: o.accent, emissiveIntensity: 0.3 }));
  const pal = o.palette || look.prod, n = Math.max(1, Math.floor((L - 0.1) / (o.pw || 0.19))), step = (L - 0.1) / n, seed = o.seed || 1;
  const im = new THREE.InstancedMesh(new THREE.BoxGeometry(1, 1, 1), new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.55, metalness: 0 }), n * rows * 2);
  const M = new THREE.Matrix4(), q = new THREE.Quaternion(), P = new THREE.Vector3(), S = new THREE.Vector3(), C = new THREE.Color(); let k = 0;
  for (let s = -1; s <= 1; s += 2) for (let r = 0; r < rows; r++) for (let i = 0; i < n; i++) {
    const h1 = hash(i + seed, r, s), h2 = hash(i * 3 + seed, r * 7, s * 5), run = Math.floor(i / (2 + Math.floor(hash(r, s, seed) * 3)));     // products come in runs of one colour, like facings
    const ph = (rh - 0.05) * (0.55 + 0.4 * hash(run + seed, r, s)), pw = step * (0.78 + 0.14 * h2);
    P.set(-L / 2 + 0.05 + (i + 0.5) * step, 0.12 + r * rh + 0.011 + ph / 2, s * (0.02 + (D / 2 - 0.02) / 2)); S.set(pw, ph, D / 2 - 0.06);
    M.compose(P, q, S); im.setMatrixAt(k, M); C.set(pal[Math.floor(hash(run * 13 + seed, r * 3, s) * pal.length)]); C.multiplyScalar(0.85 + 0.15 * h1); im.setColorAt(k, C); k++;
  }
  im.instanceMatrix.needsUpdate = true; im.instanceColor.needsUpdate = true; g.add(im); return g;
}
function floorTex(look) {
  const c = document.createElement("canvas"); c.width = c.height = 512; const x = c.getContext("2d");
  if (look === "reale") { x.fillStyle = "#bdb8ac"; x.fillRect(0, 0, 512, 512); for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) { x.fillStyle = (i + j) % 2 ? "#e6e2d8" : "#d3cec2"; x.fillRect(i * 128 + 2, j * 128 + 2, 124, 124); } }
  else { x.fillStyle = "#0d3524"; x.fillRect(0, 0, 512, 512); x.strokeStyle = "rgba(120,235,180,.35)"; x.lineWidth = 3; for (let i = 0; i <= 4; i++) { x.beginPath(); x.moveTo(i * 128, 0); x.lineTo(i * 128, 512); x.stroke(); x.beginPath(); x.moveTo(0, i * 128); x.lineTo(512, i * 128); x.stroke(); } }
  const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; return t;
}
function floor(o) {                                      // size [x, z]: a slab of tiles, its top at y = 0
  const t = floorTex(o.look); t.repeat.set(o.size[0] / 2.4, o.size[1] / 2.4);
  const m = new THREE.Mesh(new THREE.BoxGeometry(o.size[0], 0.08, o.size[1]), new THREE.MeshStandardMaterial({ map: t, roughness: o.look === "reale" ? 0.45 : 0.85, metalness: 0 }));
  m.position.y = -0.04; m.userData.floor = true; const g = new THREE.Group(); g.add(m);
  if (o.look !== "reale") { const e = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(o.size[0], 0.08, o.size[1])), new THREE.LineBasicMaterial({ color: 0x5EE6A8 })); e.position.y = -0.04; g.add(e); }
  return g;
}
function gate(o) {                                       // a doorway: two posts, a lit lintel and a lit mat; size [width, height]
  const [w, h] = o.size, g = new THREE.Group(), post = new THREE.MeshStandardMaterial({ color: o.look === "reale" ? "#8b8f94" : "#f4efe6", roughness: 0.4, metalness: o.look === "reale" ? 0.7 : 0 });
  const lit = new THREE.MeshBasicMaterial({ color: o.color || "#5EE6A8", toneMapped: false });
  for (const s of [-1, 1]) { const p = new THREE.Mesh(new THREE.BoxGeometry(0.1, h, 0.1), post); p.position.set(s * w / 2, h / 2, 0); g.add(p); }
  const l = new THREE.Mesh(new THREE.BoxGeometry(w + 0.1, 0.16, 0.12), lit); l.position.set(0, h + 0.08, 0); g.add(l);
  const mat = new THREE.Mesh(new THREE.BoxGeometry(w, 0.012, 0.9), new THREE.MeshBasicMaterial({ color: o.color || "#5EE6A8", toneMapped: false, transparent: true, opacity: 0.35 })); mat.position.set(0, 0.008, 0); g.add(mat);
  return g;
}

// ---------- outdoor kit: asphalt with markings, cars, trees, lamps
function roadTex(kind) {
  const c = document.createElement("canvas"); c.width = 512; c.height = 512; const x = c.getContext("2d");
  x.fillStyle = "#3a3c41"; x.fillRect(0, 0, 512, 512);
  for (let i = 0; i < 900; i++) { x.fillStyle = "rgba(255,255,255," + (0.02 + 0.03 * hash(i, 1, 2)).toFixed(3) + ")"; x.fillRect(hash(i, 3, 4) * 512, hash(i, 5, 6) * 512, 2, 2); }
  x.fillStyle = "#f2f0e8";
  if (kind === "parking") { for (let i = 0; i <= 4; i++) x.fillRect(i * 128 - 3, 60, 6, 250); }                         // bays: u = along the row
  else { x.fillRect(0, 18, 512, 8); x.fillRect(0, 486, 512, 8); x.fillRect(0, 250, 512, 12); x.fillRect(40, 132, 200, 7); x.fillRect(40, 372, 200, 7); }   // edges, median, dashes
  const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; return t;
}
function road(o) {                                       // size [length along x, width along z]; kind "road" (two carriageways) or "parking"
  const t = roadTex(o.rk); t.repeat.set(o.size[0] / (o.rk === "parking" ? 10.4 : 12), 1);
  const m = new THREE.Mesh(new THREE.BoxGeometry(o.size[0], 0.06, o.size[1]), new THREE.MeshStandardMaterial({ map: t, roughness: 0.9, metalness: 0 })); m.userData.floor = true; return m;
}
function car(o) {                                        // 4.2 m long along x, nose towards +x, wheels on y = 0: a rounded hatchback with a glass cabin
  const g = new THREE.Group(), paint = new THREE.MeshPhysicalMaterial({ color: o.color || "#c0392b", roughness: 0.3, metalness: 0.35, clearcoat: 1, clearcoatRoughness: 0.08 });
  const glass = new THREE.MeshStandardMaterial({ color: "#16212a", roughness: 0.06, metalness: 0.7 }), dark = new THREE.MeshStandardMaterial({ color: "#232326", roughness: 0.6 });
  const chrome = new THREE.MeshStandardMaterial({ color: "#d9dde2", roughness: 0.2, metalness: 1 }), tyre = new THREE.MeshStandardMaterial({ color: "#151515", roughness: 0.9 });
  const add = (geo, m, x, y, z) => { const b = new THREE.Mesh(geo, m); b.position.set(x, y, z); g.add(b); return b; };
  const s = new THREE.Shape();                                   // side profile, wheel arches cut in
  s.moveTo(-2.06, 0.3); s.lineTo(-1.74, 0.3); s.absarc(-1.3, 0.3, 0.44, Math.PI, 0, true); s.lineTo(0.86, 0.3); s.absarc(1.3, 0.3, 0.44, Math.PI, 0, true); s.lineTo(2.02, 0.3);
  s.quadraticCurveTo(2.17, 0.32, 2.16, 0.55); s.quadraticCurveTo(2.12, 0.8, 1.7, 0.85); s.lineTo(0.78, 0.93); s.lineTo(-1.72, 0.97); s.quadraticCurveTo(-2.1, 0.96, -2.13, 0.72); s.quadraticCurveTo(-2.15, 0.32, -2.06, 0.3);
  const body = new THREE.ExtrudeGeometry(s, { depth: 1.64, bevelEnabled: true, bevelThickness: 0.07, bevelSize: 0.06, bevelSegments: 4, curveSegments: 18 }); body.translate(0, 0, -0.82); add(body, paint, 0, 0, 0);
  const c = new THREE.Shape(); c.moveTo(0.86, 0.9); c.lineTo(0.14, 1.38); c.quadraticCurveTo(0.02, 1.47, -0.16, 1.47); c.lineTo(-1.12, 1.47); c.quadraticCurveTo(-1.3, 1.47, -1.42, 1.36); c.lineTo(-1.8, 0.93); c.lineTo(0.86, 0.9);
  const cab = new THREE.ExtrudeGeometry(c, { depth: 1.4, bevelEnabled: true, bevelThickness: 0.05, bevelSize: 0.05, bevelSegments: 3, curveSegments: 10 }); cab.translate(0, 0, -0.7); add(cab, glass, 0, 0, 0);
  add(new THREE.BoxGeometry(1.3, 0.06, 1.48), paint, -0.62, 1.5, 0);                         // roof
  for (const x of [-0.42]) add(new THREE.BoxGeometry(0.09, 0.5, 1.53), paint, x, 1.2, 0);      // B pillar
  for (const sz of [-1, 1]) { add(new THREE.BoxGeometry(2.5, 0.025, 0.02), chrome, -0.45, 0.98, sz * 0.88); add(new THREE.BoxGeometry(0.16, 0.09, 0.12), paint, 0.66, 1.02, sz * 0.93);
    add(new THREE.BoxGeometry(0.14, 0.025, 0.02), chrome, 0.15, 0.82, sz * 0.9); add(new THREE.BoxGeometry(0.14, 0.025, 0.02), chrome, -0.9, 0.82, sz * 0.9); }
  for (const x of [2.18, -2.18]) add(new THREE.BoxGeometry(0.12, 0.14, 1.72), dark, x * 0.985, 0.36, 0);   // bumpers
  add(new THREE.BoxGeometry(0.05, 0.16, 0.8), dark, 2.17, 0.56, 0); add(new THREE.BoxGeometry(0.03, 0.11, 0.4), new THREE.MeshStandardMaterial({ color: "#f5f5f0", roughness: 0.5 }), 2.25, 0.36, 0);
  for (const sx of [-1.3, 1.3]) for (const sz of [-0.8, 0.8]) {
    const w = add(new THREE.CylinderGeometry(0.35, 0.35, 0.24, 28), tyre, sx, 0.35, sz); w.rotation.x = Math.PI / 2;
    const r = add(new THREE.CylinderGeometry(0.21, 0.21, 0.25, 20), chrome, sx, 0.35, sz); r.rotation.x = Math.PI / 2;
    const h = add(new THREE.CylinderGeometry(0.08, 0.08, 0.26, 12), dark, sx, 0.35, sz); h.rotation.x = Math.PI / 2;
    for (let k = 0; k < 5; k++) { const sp = add(new THREE.BoxGeometry(0.05, 0.3, 0.02), dark, sx, 0.35, sz + Math.sign(sz) * 0.126); sp.rotation.z = k / 5 * Math.PI; }
  }
  const hl = new THREE.MeshBasicMaterial({ color: "#fff6d6", toneMapped: false }), tl = new THREE.MeshBasicMaterial({ color: "#ff2a1f", toneMapped: false });
  for (const sz of [-0.6, 0.6]) { const h = add(new THREE.CylinderGeometry(0.11, 0.11, 0.06, 18), hl, 2.13, 0.64, sz); h.rotation.z = Math.PI / 2; h.scale.set(1, 1, 1.7);
    add(new THREE.BoxGeometry(0.05, 0.12, 0.36), tl, -2.16, 0.74, sz);
    const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: haloTex("#ffe6a8"), blending: THREE.AdditiveBlending, depthWrite: false, transparent: true, opacity: 0.8 })); sp.scale.set(1.5, 1.5, 1); sp.position.set(2.25, 0.64, sz); g.add(sp); }
  return g;
}
function treeV1(o) {
  const g = new THREE.Group(), h = o.size ? o.size[0] : 5, leaf = new THREE.MeshStandardMaterial({ color: o.color || "#4f7a3f", roughness: 0.9 });
  const tr = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.22, h * 0.35, 10), new THREE.MeshStandardMaterial({ color: "#5a4030", roughness: 0.9 })); tr.position.y = h * 0.175; g.add(tr);
  for (let k = 0; k < 3; k++) { const c = new THREE.Mesh(new THREE.ConeGeometry(h * (0.3 - 0.06 * k), h * 0.42, 14), leaf); c.position.y = h * (0.45 + 0.2 * k); g.add(c); }
  return g;
}
function lamp(o) {
  const g = new THREE.Group(), h = o.size ? o.size[0] : 7, steel = new THREE.MeshStandardMaterial({ color: "#8b8f94", roughness: 0.4, metalness: 0.7 });
  const p = new THREE.Mesh(new THREE.CylinderGeometry(0.07, 0.1, h, 10), steel); p.position.y = h / 2; g.add(p);
  const head = new THREE.Mesh(new THREE.BoxGeometry(0.9, 0.12, 0.3), new THREE.MeshBasicMaterial({ color: "#fff1c9", toneMapped: false })); head.position.set(0.4, h, 0); g.add(head);
  const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: haloTex("#ffd98a"), blending: THREE.AdditiveBlending, depthWrite: false, transparent: true, opacity: 0.9 })); sp.scale.set(3.4, 3.4, 1); sp.position.set(0.4, h - 0.1, 0); g.add(sp);
  return g;
}
