
// ---------- scenery v2: broadleaf trees and pines with irregular crowns, a deep wood, hills, hedges (instanced, deterministic)
function blobGeo(r, seed, detail) {                        // a lumpy ball of leaves: an icosphere pushed in and out by a smooth function of the direction
  const g = new THREE.IcosahedronGeometry(r, detail ?? 3), p = g.attributes.position, v = new THREE.Vector3();
  for (let i = 0; i < p.count; i++) {
    v.fromBufferAttribute(p, i); const n = v.clone().normalize();
    const k = 1 + 0.16 * Math.sin(n.x * 5.1 + seed) * Math.cos(n.y * 4.3 + seed * 1.7) + 0.08 * Math.sin(n.z * 9.7 + n.x * 7.3 + seed * 3.1) + 0.05 * Math.sin(n.y * 17.0 + n.z * 13.0 + seed);
    v.multiplyScalar(k); if (v.y < -r * 0.45) v.y = -r * 0.45 + (v.y + r * 0.45) * 0.35;      // crowns are flatter underneath
    p.setXYZ(i, v.x, v.y, v.z);
  }
  g.computeVertexNormals(); return g;
}
function jaggedCone(r, h, seed) {                          // a pine tier with a ragged, drooping rim
  const g = new THREE.ConeGeometry(r, h, 14, 3, true), p = g.attributes.position;
  for (let i = 0; i < p.count; i++) {
    const x = p.getX(i), y = p.getY(i), z = p.getZ(i), a = Math.atan2(z, x), k = 1 + 0.22 * Math.max(0, Math.sin(a * 7 + seed));
    p.setXYZ(i, x * k, y - (y < -h * 0.45 ? 0.12 * h * Math.abs(Math.sin(a * 7 + seed)) : 0), z * k);
  }
  g.computeVertexNormals(); return g;
}
const SCN = {};
function scn() {
  if (SCN.ok) return SCN;
  const leafT = ctex("leaf", 256, 256, (x, w, h) => { x.fillStyle = "#ffffff"; x.fillRect(0, 0, w, h); speckle(x, w, h, 2600, ["#c9d8b8", "#ffffff", "#9fb38a", "#e9f2dc"], 1.5, 4.5, 0.35, 0.8, 61); }, true);
  leafT.repeat.set(3, 3);
  const barkT = ctex("bark", 128, 256, (x, w, h) => { x.fillStyle = "#6a4e3a"; x.fillRect(0, 0, w, h); for (let i = 0; i < 60; i++) { x.strokeStyle = rnd(i) < 0.5 ? "#4a3427" : "#86664e"; x.lineWidth = 1 + rnd(i * 3) * 3; const X = rnd(i * 7) * w; x.beginPath(); x.moveTo(X, 0); x.bezierCurveTo(X + 6, h * 0.3, X - 6, h * 0.6, X + 3, h); x.stroke(); } }, true);
  SCN.leaf = new THREE.MeshStandardMaterial({ color: 0xffffff, map: leafT, roughness: 0.92, metalness: 0 });
  SCN.pine = new THREE.MeshStandardMaterial({ color: 0xffffff, map: leafT, roughness: 0.95, metalness: 0, side: THREE.DoubleSide });
  SCN.bark = new THREE.MeshStandardMaterial({ color: 0xffffff, map: barkT, roughness: 0.95 });
  SCN.blobs = [blobGeo(1, 1.3), blobGeo(1, 4.7), blobGeo(1, 8.1)];
  SCN.blobsLo = [blobGeo(1, 2.2, 2), blobGeo(1, 6.6, 2)];
  SCN.cones = [jaggedCone(1, 1, 0.7), jaggedCone(1, 1, 2.9)];
  const tr = new THREE.CylinderGeometry(0.6, 1, 1, 9); tr.translate(0, 0.5, 0); SCN.trunk = tr;
  const br = new THREE.CylinderGeometry(0.35, 0.6, 1, 6); br.translate(0, 0.5, 0); SCN.branch = br;
  SCN.ok = true; return SCN;
}
const LEAF = ["#4f7a3f", "#5d8a45", "#44693a", "#6b8f3e", "#3f6234", "#7a9a48"], PINE = ["#2f5232", "#36603a", "#2a4a2e"], AUTUMN = ["#b0782e", "#9c5a2a", "#c79a3a"];
// one tree as a list of [geometry, material, matrix, colour] parts: kind "leaf" (broadleaf) or "pine"
function treeParts(kind, h, seed, autumn) {
  const S = scn(), out = [], M4 = new THREE.Matrix4(), Q = new THREE.Quaternion(), E = new THREE.Euler(), V = new THREE.Vector3(), Sc = new THREE.Vector3();
  const put = (geo, mat, x, y, z, sx, sy, sz, rx, ry, rz, col) => { E.set(rx || 0, ry || 0, rz || 0); Q.setFromEuler(E); out.push([geo, mat, M4.compose(V.set(x, y, z), Q, Sc.set(sx, sy, sz)).clone(), col]); };
  const R = (i) => hash(seed * 1.31 + i, i * 0.7, seed);
  if (kind === "pine") {
    put(S.trunk, S.bark, 0, 0, 0, h * 0.035, h * 0.3, h * 0.035, 0, 0, 0, "#ffffff");
    const n = 5 + Math.floor(R(1) * 2);
    for (let k = 0; k < n; k++) {
      const f = k / n, r = h * (0.27 - 0.2 * f) * (0.9 + 0.2 * R(k + 3)), y = h * (0.22 + 0.68 * f) + h * 0.07;
      put(S.cones[k % 2], S.pine, 0, y, 0, r, h * 0.26, r, 0, R(k) * 6, 0, PINE[Math.floor(R(k + 9) * 3)]);
    }
    return out;
  }
  const th = h * (0.38 + 0.08 * R(2));
  put(S.trunk, S.bark, 0, 0, 0, h * 0.045, th, h * 0.045, 0, 0, (R(4) - 0.5) * 0.08, "#ffffff");
  for (let b = 0; b < 3; b++) { const a = b / 3 * 6.28 + R(b) * 1.5; put(S.branch, S.bark, 0, th * 0.75, 0, h * 0.022, h * 0.25, h * 0.022, Math.sin(a) * 0.7, 0, Math.cos(a) * 0.7, "#ffffff"); }
  const pal = autumn ? AUTUMN : LEAF, nb = 6 + Math.floor(R(5) * 4), cy = th + h * 0.2;
  for (let k = 0; k < nb; k++) {
    const a = R(k * 3 + 1) * 6.28, d = (k === 0 ? 0 : 0.18 + 0.18 * R(k * 5)) * h, r = h * (k === 0 ? 0.3 : 0.17 + 0.09 * R(k * 7));
    put(S.blobs[k % 3], S.leaf, Math.cos(a) * d, cy + (R(k * 11) - 0.35) * h * 0.25, Math.sin(a) * d, r, r * (0.85 + 0.2 * R(k)), r, 0, R(k * 13) * 6, 0, pal[Math.floor(R(k * 17) * pal.length)]);
  }
  return out;
}
function tree(o) {                                         // one hero tree (near the store): its own meshes, casts shadows
  const g = new THREE.Group(), h = o.size ? o.size[0] : 5, seed = Math.round((o.pos[0] * 7.1 + o.pos[2] * 3.3) * 10) / 10;
  for (const [geo, mat, m, col] of treeParts(o.kind || (hash(seed, 1, 2) < 0.3 ? "pine" : "leaf"), h, seed, o.autumn)) {
    const mesh = new THREE.Mesh(geo, col === "#ffffff" ? mat : mat.clone()); if (col !== "#ffffff") mesh.material.color.set(col); mesh.applyMatrix4(m); g.add(mesh);
  }
  return g;
}
function forest(o) {                                       // a wood: o.area [x0, z0, x1, z1] in world metres (the object sits at the origin), o.n trees, instanced
  const [x0, z0, x1, z1] = o.area, n = o.n || 200, seed = o.seed || 1, parts = new Map(), M = new THREE.Matrix4(), C = new THREE.Color();
  for (let i = 0; i < n; i++) {
    const x = x0 + hash(i, seed, 1) * (x1 - x0), z = z0 + hash(i, seed, 2) * (z1 - z0), h = (o.h || 7) * (0.7 + 0.6 * hash(i, seed, 3));
    const kind = hash(i, seed, 4) < (o.pines ?? 0.35) ? "pine" : "leaf", autumn = hash(i, seed, 5) < (o.autumn ?? 0.08);
    const T = new THREE.Matrix4().makeTranslation(x, 0, z);
    for (const [geo, mat, m, col] of treeParts(kind, h, i + seed * 100, autumn)) {
      const key = geo.uuid + mat.uuid; if (!parts.has(key)) parts.set(key, { geo, mat, list: [] });
      parts.get(key).list.push([M.multiplyMatrices(T, m).clone(), col]);
    }
  }
  const g = new THREE.Group();
  for (const { geo, mat, list } of parts.values()) {
    const im = new THREE.InstancedMesh(geo, mat, list.length);
    list.forEach(([m, col], i) => { im.setMatrixAt(i, m); C.set(col); C.multiplyScalar(0.88 + 0.24 * hash(i, 7, seed)); im.setColorAt(i, C); });
    im.instanceMatrix.needsUpdate = true; im.instanceColor.needsUpdate = true; g.add(im);
  }
  return g;
}
function hedge(o) {                                        // a row of bushes from pos to o.to
  const S = scn(), n = o.n || 20, g = new THREE.Group(), im = new THREE.InstancedMesh(S.blobsLo[0], S.leaf, n), M = new THREE.Matrix4(), C = new THREE.Color(), Q = new THREE.Quaternion();
  for (let i = 0; i < n; i++) {
    const k = (i + 0.5) / n, r = (o.r || 0.7) * (0.8 + 0.4 * hash(i, 3, 9));
    M.compose(new THREE.Vector3((o.to[0] - o.pos[0]) * k, r * 0.55, (o.to[2] - o.pos[2]) * k), Q, new THREE.Vector3(r, r * 0.8, r));
    im.setMatrixAt(i, M); C.set(LEAF[i % LEAF.length]); im.setColorAt(i, C);
  }
  im.instanceMatrix.needsUpdate = true; im.instanceColor.needsUpdate = true; g.add(im); return g;
}
function hills(o) {                                        // soft hills on the horizon (the fog tints them)
  const g = new THREE.Group(), geo = blobGeo(1, 3.3, 4), cols = o.colors || ["#2c4a3a", "#34543f", "#284236"];
  (o.list || []).forEach(([x, z, r, hgt], i) => { const m = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({ color: cols[i % cols.length], roughness: 1 })); m.position.set(x - o.pos[0], -r * 0.05, z - o.pos[2]); m.scale.set(r, hgt, r * 0.7); m.userData.floor = true; g.add(m); });
  return g;
}
