// ---------- product kit v2: recognisable products, painted canvas textures (stylised 3D, like a Blender toon-ish scene)
const _tx = {};
function ctex(key, w, h, draw, rep) {
  if (_tx[key]) return _tx[key];
  const c = document.createElement("canvas"); c.width = w; c.height = h; const x = c.getContext("2d"); draw(x, w, h);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8;
  if (rep) t.wrapS = t.wrapT = THREE.RepeatWrapping;
  return (_tx[key] = t);
}
const rnd = (i) => hash(i * 0.731, i * 0.377 + 1.3, 2.9);
function speckle(x, w, h, n, cols, r0, r1, a0, a1, seed) {
  for (let i = 0; i < n; i++) {
    x.globalAlpha = a0 + (a1 - a0) * rnd(i * 5 + seed); x.fillStyle = cols[Math.floor(rnd(i * 7 + seed) * cols.length)];
    x.beginPath(); x.arc(rnd(i * 11 + seed) * w, rnd(i * 13 + seed) * h, r0 + (r1 - r0) * rnd(i * 3 + seed), 0, 7); x.fill();
  }
  x.globalAlpha = 1;
}
function rr(x, X, Y, W, H, R) { x.beginPath(); x.moveTo(X + R, Y); x.arcTo(X + W, Y, X + W, Y + H, R); x.arcTo(X + W, Y + H, X, Y + H, R); x.arcTo(X, Y + H, X, Y, R); x.arcTo(X, Y, X + W, Y, R); x.closePath(); }
function txt(x, s, X, Y, size, col, font, stroke) {
  x.font = font ? font.replace("#", size) : "900 " + size + "px Arial Black, Arial, sans-serif"; x.textAlign = "center"; x.textBaseline = "middle";
  if (stroke) { x.lineWidth = size * 0.16; x.strokeStyle = stroke; x.lineJoin = "round"; x.strokeText(s, X, Y); }
  x.fillStyle = col; x.fillText(s, X, Y);
}
const SERIF = "italic 700 #px Georgia, 'Times New Roman', serif";
function cookie(x, X, Y, R, kind) {                       // a painted biscuit
  const g = x.createRadialGradient(X - R * 0.3, Y - R * 0.3, R * 0.1, X, Y, R);
  g.addColorStop(0, kind === "cacao" ? "#7a4a2a" : "#f0c27a"); g.addColorStop(1, kind === "cacao" ? "#4a2a16" : "#c98a3e");
  x.fillStyle = g;
  if (kind === "fiore") { x.beginPath(); for (let k = 0; k < 8; k++) { const a = k / 8 * Math.PI * 2; x.arc(X + Math.cos(a) * R * 0.62, Y + Math.sin(a) * R * 0.62, R * 0.42, 0, 7); } x.fill(); x.fillStyle = "#e8b36a"; x.beginPath(); x.arc(X, Y, R * 0.28, 0, 7); x.fill(); x.fillStyle = "rgba(255,255,255,.85)"; speckle(x, 0, 0, 0, ["#fff"], 1, 2, 1, 1, 0); x.beginPath(); x.arc(X, Y, R * 0.12, 0, 7); x.fill(); return; }
  x.beginPath(); x.arc(X, Y, R, 0, 7); x.fill();
  x.strokeStyle = "rgba(90,50,20,.35)"; x.lineWidth = R * 0.08; x.beginPath(); x.arc(X, Y, R * 0.86, 0, 7); x.stroke();
  if (kind === "gocce") for (let k = 0; k < 7; k++) { x.fillStyle = "#3b2414"; x.beginPath(); x.arc(X + (rnd(k * 3 + X) - 0.5) * R * 1.3, Y + (rnd(k * 5 + Y) - 0.5) * R * 1.3, R * 0.11, 0, 7); x.fill(); }
  else if (kind === "cacao") { x.fillStyle = "#f6efe2"; x.beginPath(); x.arc(X, Y, R * 0.45, 0, 7); x.fill(); }
  else { x.fillStyle = "rgba(255,250,235,.9)"; for (let k = 0; k < 12; k++) { x.beginPath(); x.arc(X + (rnd(k * 3 + X) - 0.5) * R * 1.4, Y + (rnd(k * 5 + Y) - 0.5) * R * 1.4, R * 0.05, 0, 7); x.fill(); } }
}
// ---- textures
const TX = {
  salSkin: () => ctex("salSkin", 512, 512, (x, w, h) => {
    const g = x.createLinearGradient(0, 0, 0, h); g.addColorStop(0, "#6e2a1f"); g.addColorStop(0.5, "#86372a"); g.addColorStop(1, "#6e2a1f"); x.fillStyle = g; x.fillRect(0, 0, w, h);
    speckle(x, w, h, 900, ["#f1e7da", "#d9c8b4", "#ffffff"], 2, 9, 0.18, 0.5, 3);            // the white bloom of a cured salame
    speckle(x, w, h, 260, ["#4a1b13", "#5a2117"], 2, 6, 0.3, 0.6, 9);
    x.strokeStyle = "rgba(246,240,228,.95)"; x.lineWidth = 6;                                   // the string net
    for (let k = -8; k < 16; k++) { x.beginPath(); x.moveTo(k * 64, 0); x.lineTo(k * 64 + 256, h); x.stroke(); x.beginPath(); x.moveTo(k * 64 + 256, 0); x.lineTo(k * 64, h); x.stroke(); }
  }, true),
  salCut: () => ctex("salCut", 512, 512, (x, w, h) => {
    x.fillStyle = "#6a2419"; x.fillRect(0, 0, w, h); x.fillStyle = "#c23a44"; x.beginPath(); x.arc(256, 256, 236, 0, 7); x.fill();
    speckle(x, w, h, 1, ["#a82a35"], 1, 1, 1, 1, 0);
    for (let i = 0; i < 520; i++) { const a = rnd(i) * 7, r = Math.sqrt(rnd(i * 3 + 1)) * 222, s = 4 + rnd(i * 7) * 13; x.fillStyle = rnd(i * 9) < 0.72 ? "#f7e4dc" : "#8f1f2a"; x.globalAlpha = 0.9; x.beginPath(); x.arc(256 + Math.cos(a) * r, 256 + Math.sin(a) * r, s, 0, 7); x.fill(); }
    x.globalAlpha = 1; x.strokeStyle = "#e9ddcc"; x.lineWidth = 7; x.beginPath(); x.arc(256, 256, 238, 0, 7); x.stroke();
  }),
  parmSide: () => ctex("parmSide", 1024, 256, (x, w, h) => {
    const g = x.createLinearGradient(0, 0, 0, h); g.addColorStop(0, "#c9923f"); g.addColorStop(0.18, "#e6b55e"); g.addColorStop(0.82, "#e6b55e"); g.addColorStop(1, "#c08638"); x.fillStyle = g; x.fillRect(0, 0, w, h);
    speckle(x, w, h, 500, ["#b9832f", "#f2cb7d"], 1, 4, 0.2, 0.5, 21);
    x.fillStyle = "rgba(120,72,20,.7)"; x.font = "900 54px Arial Black, Arial"; x.textAlign = "center"; x.textBaseline = "middle";
    for (let r = 0; r < 2; r++) for (let k = 0; k < 4; k++) x.fillText(r ? "REGGIANO" : "PARMIGIANO", k * 256 + 128 + (r ? 64 : 0), 100 + r * 64);   // the pin-dot stamp, read as lettering
  }, true),
  parmTop: () => ctex("parmTop", 512, 512, (x, w, h) => {
    x.fillStyle = "#d8a24c"; x.fillRect(0, 0, w, h); const g = x.createRadialGradient(256, 256, 40, 256, 256, 250); g.addColorStop(0, "#f2d68f"); g.addColorStop(0.8, "#ecc877"); g.addColorStop(1, "#c98f3c");
    x.fillStyle = g; x.beginPath(); x.arc(256, 256, 250, 0, 7); x.fill(); speckle(x, w, h, 300, ["#f7e2a8", "#d9ad5c"], 2, 6, 0.2, 0.5, 33);
  }),
  wine: () => ctex("wine", 512, 256, (x, w, h) => {
    x.fillStyle = "#f3ead6"; x.fillRect(0, 0, w, h); x.strokeStyle = "#8a1c2b"; x.lineWidth = 6; x.strokeRect(150, 18, 212, 220);
    txt(x, "Chianti", 256, 100, 58, "#7a1626", SERIF); x.fillStyle = "#b08a3c"; x.fillRect(190, 140, 132, 4); txt(x, "RISERVA", 256, 178, 30, "#2b2b2b", "700 #px Georgia, serif");
  }, true),
  jar: () => ctex("jar", 512, 128, (x, w, h) => {
    x.fillStyle = "#f6f0e2"; x.fillRect(0, 0, w, h); x.fillStyle = "#2f7d3b"; x.fillRect(0, 0, w, 14); x.fillRect(0, h - 14, w, 14);
    txt(x, "Sugo", 150, 66, 50, "#b3261e", SERIF); x.fillStyle = "#d33a2c"; x.beginPath(); x.arc(330, 66, 26, 0, 7); x.fill(); x.fillStyle = "#3f8f3a"; x.beginPath(); x.ellipse(330, 38, 16, 7, 0, 0, 7); x.fill();
  }, true),
  gingham: () => ctex("gingham", 256, 256, (x, w, h) => {
    x.fillStyle = "#fbf7ef"; x.fillRect(0, 0, w, h); x.fillStyle = "rgba(200,30,40,.55)"; for (let k = 0; k < 8; k += 2) { x.fillRect(k * 32, 0, 32, h); x.fillRect(0, k * 32, w, 32); }
  }),
  pasta: () => ctex("pasta", 256, 448, (x, w, h) => {
    x.fillStyle = "#1c4fa0"; x.fillRect(0, 0, w, h); x.fillStyle = "#f7f2e6"; rr(x, 14, 18, 228, 96, 30); x.fill();
    txt(x, "Pasta", 128, 66, 58, "#1c4fa0", SERIF);
    x.fillStyle = "#f4e2a6"; rr(x, 30, 150, 196, 190, 24); x.fill();                           // the window with the penne
    for (let k = 0; k < 22; k++) { const X = 50 + rnd(k) * 156, Y = 170 + rnd(k * 3) * 150, a = rnd(k * 7) * 3; x.save(); x.translate(X, Y); x.rotate(a); x.fillStyle = "#e9b84d"; x.fillRect(-20, -7, 40, 14); x.strokeStyle = "#c58f2a"; x.lineWidth = 2; for (let j = -16; j < 20; j += 6) { x.beginPath(); x.moveTo(j, -7); x.lineTo(j + 4, 7); x.stroke(); } x.restore(); }
    txt(x, "PENNE RIGATE", 128, 386, 26, "#ffffff");
  }),
  biscotti: (v) => ctex("bisc" + v, 512, 384, (x, w, h) => {
    const P = [["#f4ead2", "#c8102e", "Frollini", "fiore"], ["#1f4e8c", "#ffd25a", "Gocciole", "gocce"], ["#7a1f2b", "#ffe9c7", "Cacao", "cacao"]][v];
    x.fillStyle = P[0]; x.fillRect(0, 0, w, h); x.fillStyle = P[1]; x.fillRect(0, 0, w, 18); x.fillRect(0, h - 18, w, 18);
    txt(x, P[2], 256, 80, 84, v === 0 ? "#c8102e" : P[1], SERIF, v === 0 ? "#fff" : "rgba(0,0,0,.25)");
    cookie(x, 150, 250, 72, P[3]); cookie(x, 300, 262, 64, P[3]); cookie(x, 410, 236, 52, P[3]);
    txt(x, "BISCOTTI", 256, 344, 28, v === 0 ? "#7a5a2e" : "#ffffff");
  }),
  panettone: (v) => ctex("pan" + v, 512, 640, (x, w, h) => {
    x.fillStyle = v ? "#a3141f" : "#16285a"; x.fillRect(0, 0, w, h);
    for (let k = 0; k < 40; k++) { x.fillStyle = "rgba(240,200,110," + (0.3 + rnd(k) * 0.6).toFixed(2) + ")"; const X = rnd(k * 3) * w, Y = rnd(k * 5) * h * 0.5, R = 4 + rnd(k * 7) * 9; x.beginPath(); for (let j = 0; j < 10; j++) { const a = j / 10 * Math.PI * 2, r = j % 2 ? R * 0.45 : R; x.lineTo(X + Math.cos(a) * r, Y + Math.sin(a) * r); } x.fill(); }
    if (v) {                                                          // pandoro: the eight-pointed star
      x.fillStyle = "#f2c35a"; x.beginPath(); for (let j = 0; j < 16; j++) { const a = j / 16 * Math.PI * 2, r = j % 2 ? 80 : 150; x.lineTo(256 + Math.cos(a) * r, 380 + Math.sin(a) * r * 0.75); } x.fill();
      x.fillStyle = "rgba(255,255,255,.9)"; speckle(x, 0, 0, 0, ["#fff"], 1, 1, 1, 1, 0); for (let k = 0; k < 60; k++) { x.beginPath(); x.arc(150 + rnd(k) * 212, 300 + rnd(k * 3) * 70, 4, 0, 7); x.fill(); }
    } else {                                                          // panettone: the dome, the paper band, the raisins
      x.fillStyle = "#7a3d14"; x.beginPath(); x.ellipse(256, 330, 150, 80, 0, Math.PI, 0); x.fill();
      x.fillStyle = "#f2c35a"; x.fillRect(106, 330, 300, 120); x.fillStyle = "#d9a441"; x.fillRect(106, 330, 300, 14);
      x.fillStyle = "#5a2a12"; for (let k = 0; k < 16; k++) { x.beginPath(); x.arc(120 + rnd(k) * 270, 350 + rnd(k * 3) * 90, 7, 0, 7); x.fill(); }
      x.fillStyle = "#c69a5a"; x.fillRect(100, 440, 312, 50); x.strokeStyle = "#a07840"; x.lineWidth = 3; for (let k = 104; k < 410; k += 12) { x.beginPath(); x.moveTo(k, 440); x.lineTo(k, 490); x.stroke(); }
    }
    txt(x, v ? "Pandoro" : "Panettone", 256, 560, 82, "#f2c35a", SERIF);
  }),
  prisma: () => ctex("prisma", 768, 1024, (x, w, h) => {
    x.fillStyle = "#f2c230"; x.fillRect(0, 0, w, h);
    for (let k = 0; k < 3; k++) { const X = k * 256; x.fillStyle = "#e0a915"; x.fillRect(X, 0, 10, h); x.save(); x.translate(X + 128, h / 2); x.rotate(Math.PI / 2);
      x.fillStyle = "#ffffff"; x.beginPath(); x.moveTo(-470, 70); x.lineTo(-400, -60); x.lineTo(-330, 70); x.fill(); x.fillStyle = "#cfd6dc"; x.beginPath(); x.moveTo(-400, -60); x.lineTo(-330, 70); x.lineTo(-375, 70); x.fill();
      txt(x, "CIOCCOLATO", 40, -18, 92, "#b3121c"); txt(x, "gigante · al latte e miele", 40, 62, 40, "#7a3b0c", SERIF); x.restore(); }
  }),
  latta: () => ctex("latta", 512, 512, (x, w, h) => {
    x.fillStyle = "#1d3f8f"; x.fillRect(0, 0, w, h); x.strokeStyle = "#f2d27a"; x.lineWidth = 10; x.beginPath(); x.arc(256, 256, 236, 0, 7); x.stroke();
    cookie(x, 190, 210, 70, "fiore"); cookie(x, 320, 200, 62, "gocce"); cookie(x, 255, 320, 66, "x"); txt(x, "Biscotti al burro", 256, 430, 40, "#f2d27a", SERIF);
  }),
  fur: () => ctex("fur", 256, 256, (x, w, h) => { x.fillStyle = "#ffffff"; x.fillRect(0, 0, w, h); speckle(x, w, h, 2200, ["#e6e0d6", "#ffffff", "#d6cfc3"], 0.6, 1.6, 0.2, 0.45, 41); }, true),
  ball: () => ctex("ball", 512, 256, (x, w, h) => { const C = ["#e63946", "#ffffff", "#ffb703", "#ffffff", "#219ebc", "#ffffff"]; C.forEach((c, k) => { x.fillStyle = c; x.fillRect(k * w / 6, 0, w / 6 + 1, h); }); x.fillStyle = "#ffffff"; x.fillRect(0, 0, w, 14); x.fillRect(0, h - 14, w, 14); }, true),
  gioco: (v) => ctex("gioco" + v, 512, 384, (x, w, h) => {
    x.fillStyle = ["#2a9d8f", "#6a4c93", "#fb8500"][v]; x.fillRect(0, 0, w, h);
    for (let k = 0; k < 14; k++) { x.fillStyle = ["#ffd166", "#ef476f", "#06d6a0", "#118ab2", "#ffffff"][k % 5]; x.globalAlpha = 0.85; x.beginPath(); x.arc(rnd(k + v) * w, rnd(k * 3 + v) * h, 14 + rnd(k * 5) * 26, 0, 7); x.fill(); }
    x.globalAlpha = 1; x.fillStyle = "#fff"; rr(x, 300, 170, 120, 120, 18); x.fill(); x.fillStyle = "#222"; for (const [a, b] of [[330, 200], [390, 200], [360, 230], [330, 260], [390, 260]]) { x.beginPath(); x.arc(a, b, 10, 0, 7); x.fill(); }
    txt(x, ["GIOCO", "PUZZLE", "COSTRUZIONI"][v], v === 2 ? 220 : 180, 90, v === 2 ? 64 : 92, "#ffffff", null, "rgba(0,0,0,.35)");
  }),
  blister: () => ctex("blister", 256, 320, (x, w, h) => {
    const g = x.createLinearGradient(0, 0, 0, h); g.addColorStop(0, "#d62828"); g.addColorStop(1, "#8f1515"); x.fillStyle = g; x.fillRect(0, 0, w, h);
    x.fillStyle = "#ffd166"; for (let k = 0; k < 6; k++) { x.save(); x.translate(128, 230); x.rotate(k * 0.5 - 1.3); x.fillRect(0, -6, 200, 12); x.restore(); }
    x.fillStyle = "#fff"; rr(x, 50, 18, 156, 18, 9); x.fill(); txt(x, "TURBO", 128, 64, 52, "#ffd166", null, "#5a0b0b");
  }),
  header: (label, col) => ctex("hdr" + label, 2048, 100, (x, w, h) => {
    x.fillStyle = col; x.fillRect(0, 0, w, h); x.fillStyle = "rgba(255,255,255,.18)"; x.fillRect(0, 0, w, 10);
    for (let k = 0; k < 3; k++) txt(x, label, (k + 0.5) * w / 3, 54, 62, "#ffffff", null, "rgba(0,0,0,.18)");
  }),
  peg: () => ctex("peg", 256, 256, (x, w, h) => { x.fillStyle = "#e9e6df"; x.fillRect(0, 0, w, h); x.fillStyle = "#c9c4b9"; for (let i = 0; i < 8; i++) for (let j = 0; j < 8; j++) { x.beginPath(); x.arc(16 + i * 32, 16 + j * 32, 4, 0, 7); x.fill(); } }, true),
  lolly: () => ctex("lolly", 256, 128, (x, w, h) => { x.fillStyle = "#fff"; x.fillRect(0, 0, w, h); x.fillStyle = "rgba(255,255,255,1)"; for (let k = 0; k < 8; k++) { x.fillStyle = k % 2 ? "#ffffff" : "#ff5d8f"; x.fillRect(k * 32, 0, 32, h); } }, true),
  gum: () => ctex("gum", 256, 192, (x, w, h) => { x.fillStyle = "#1fb5a8"; x.fillRect(0, 0, w, h); x.fillStyle = "#fff"; rr(x, 20, 40, 216, 110, 30); x.fill(); txt(x, "GOMME", 128, 96, 48, "#1fb5a8"); }),
};
// ---- materials and geometry helpers
const _mat = {};
function M(key, make) { return _mat[key] || (_mat[key] = make()); }
const std = (o) => new THREE.MeshStandardMaterial(Object.assign({ roughness: 0.6, metalness: 0 }, o));
const solidM = (c, r = 0.6, m = 0) => M("c" + c + r + m, () => std({ color: c, roughness: r, metalness: m }));
const texM = (t, r = 0.55, extra) => std(Object.assign({ map: t, roughness: r }, extra || {}));
function boxMats(front, side, top) { return [side, side, top || side, side, front, side]; }   // +x -x +y -y +z(front) -z
const sphere = (r, sx = 1, sy = 1, sz = 1) => { const g = new THREE.SphereGeometry(r, 18, 14); g.scale(sx, sy, sz); return g; };
const at3 = (g, x, y, z) => { g.translate(x, y, z); return g; };
// a product kind: { w, h, d, stack, parts: [{ geo, mat, tint }] }; geometry has its origin at the bottom centre, its face towards +z
const KINDS = {};
function K(name) {
  if (KINDS[name]) return KINDS[name];
  const k = { stack: 1, parts: [] }, P = (geo, mat, tint) => k.parts.push({ geo, mat, tint: !!tint });
  if (name === "salame") {                                   // a cut salame lying with its slice towards the aisle
    const r = 0.042, l = 0.2, g = new THREE.CylinderGeometry(r, r, l, 22); g.rotateX(Math.PI / 2); g.translate(0, r, 0);
    P(g, [texM(TX.salSkin(), 0.8), texM(TX.salCut(), 0.5), texM(TX.salCut(), 0.5)]);
    Object.assign(k, { w: 0.095, h: 0.084, d: l, stack: 3, pyramid: true });
  } else if (name === "salameIntero") {                      // whole, lying along the shelf
    const g = new THREE.CapsuleGeometry(0.045, 0.2, 8, 18); g.rotateZ(Math.PI / 2); g.translate(0, 0.045, 0); P(g, texM(TX.salSkin(), 0.85));
    Object.assign(k, { w: 0.31, h: 0.09, d: 0.09, stack: 3, pyramid: true });
  } else if (name === "parmigiano") {
    const g = new THREE.CylinderGeometry(0.16, 0.16, 0.11, 40); g.translate(0, 0.055, 0); P(g, [texM(TX.parmSide(), 0.75), texM(TX.parmTop(), 0.7), texM(TX.parmTop(), 0.7)]);
    Object.assign(k, { w: 0.33, h: 0.11, d: 0.32, stack: 2 });
  } else if (name === "vino") {
    const pts = [[0, 0], [0.036, 0], [0.038, 0.006], [0.038, 0.19], [0.035, 0.215], [0.017, 0.255], [0.0145, 0.3], [0.016, 0.305], [0.0, 0.305]].map((p) => new THREE.Vector2(p[0], p[1]));
    P(new THREE.LatheGeometry(pts, 22), std({ color: "#1d3a22", roughness: 0.12, metalness: 0.25 }));
    const lab = new THREE.CylinderGeometry(0.0388, 0.0388, 0.095, 22, 1, true); lab.translate(0, 0.105, 0); lab.rotateY(Math.PI); P(lab, texM(TX.wine(), 0.7), true);
    const cap = new THREE.CylinderGeometry(0.0158, 0.0158, 0.05, 14); cap.translate(0, 0.283, 0); P(cap, solidM("#6e1020", 0.35, 0.5));
    Object.assign(k, { w: 0.085, h: 0.305, d: 0.08 });
  } else if (name === "barattolo") {
    const b = new THREE.CylinderGeometry(0.043, 0.043, 0.1, 22); b.translate(0, 0.05, 0); P(b, std({ color: "#ffffff", roughness: 0.25 }), true);
    const lab = new THREE.CylinderGeometry(0.0438, 0.0438, 0.05, 22, 1, true); lab.translate(0, 0.05, 0); lab.rotateY(Math.PI); P(lab, texM(TX.jar(), 0.7));
    const lid = new THREE.CylinderGeometry(0.046, 0.046, 0.022, 22); lid.translate(0, 0.111, 0); P(lid, [texM(TX.gingham(), 0.7), texM(TX.gingham(), 0.7), solidM("#b5242c")]);
    Object.assign(k, { w: 0.1, h: 0.122, d: 0.09, stack: 2 });
  } else if (name === "pasta") {
    const g = new THREE.BoxGeometry(0.12, 0.21, 0.06); g.translate(0, 0.105, 0); P(g, boxMats(texM(TX.pasta(), 0.6), solidM("#1c4fa0", 0.6), solidM("#1c4fa0", 0.6)));
    Object.assign(k, { w: 0.13, h: 0.21, d: 0.06 });
  } else if (name.startsWith("biscotti")) {
    const v = +name.slice(-1), c = ["#f4ead2", "#1f4e8c", "#7a1f2b"][v], g = new THREE.BoxGeometry(0.2, 0.15, 0.07); g.translate(0, 0.075, 0);
    P(g, boxMats(texM(TX.biscotti(v), 0.5), solidM(c, 0.5)));
    Object.assign(k, { w: 0.21, h: 0.15, d: 0.07, stack: 2 });
  } else if (name === "panettone" || name === "pandoro") {
    const v = name === "pandoro" ? 1 : 0, t = texM(TX.panettone(v), 0.5), g = new THREE.BoxGeometry(0.21, 0.26, 0.21); g.translate(0, 0.13, 0);
    P(g, [t, t, solidM(v ? "#a3141f" : "#16285a", 0.5), t, t, t]);
    const rib = new THREE.BoxGeometry(0.215, 0.012, 0.215); rib.translate(0, 0.2, 0); P(rib, solidM("#d4a63c", 0.3, 0.6));
    Object.assign(k, { w: 0.23, h: 0.26, d: 0.21 });
  } else if (name === "prisma") {                             // the giant triangular chocolate bar
    const g = new THREE.CylinderGeometry(0.06, 0.06, 0.42, 3); g.rotateZ(Math.PI / 2); g.rotateX(-Math.PI / 2); g.translate(0, 0.03, 0);
    P(g, [texM(TX.prisma(), 0.45), solidM("#e0a915", 0.5), solidM("#e0a915", 0.5)]);
    Object.assign(k, { w: 0.44, h: 0.09, d: 0.11, stack: 3, pyramid: true });
  } else if (name === "latta") {
    const g = new THREE.CylinderGeometry(0.1, 0.1, 0.075, 36); g.rotateX(1.35); g.translate(0, 0.102, 0);
    P(g, [solidM("#1d3f8f", 0.3, 0.6), texM(TX.latta(), 0.35, { metalness: 0.3 }), solidM("#1d3f8f", 0.3, 0.6)]);
    Object.assign(k, { w: 0.21, h: 0.2, d: 0.1 });   // tins stand on their rim, lid towards you
  } else if (name === "orsetto") {
    const fur = texM(TX.fur(), 0.95);
    P(at3(sphere(0.068, 1, 1.12, 0.95), 0, 0.078, 0), fur, true); P(at3(sphere(0.056), 0, 0.19, 0.005), fur, true);
    for (const s of [-1, 1]) { P(at3(sphere(0.022, 1, 1, 0.6), s * 0.042, 0.238, 0), fur, true); P(at3(sphere(0.026, 0.8, 1.3, 0.8), s * 0.068, 0.095, 0.022), fur, true); P(at3(sphere(0.03, 1, 0.8, 1.3), s * 0.038, 0.024, 0.05), fur, true);
      P(at3(sphere(0.0075), s * 0.02, 0.205, 0.05), solidM("#111111", 0.2)); }
    P(at3(sphere(0.025, 1.1, 0.85, 0.9), 0, 0.177, 0.045), solidM("#f1e3cc", 0.9)); P(at3(sphere(0.0095, 1.3, 1, 1), 0, 0.186, 0.068), solidM("#1a1a1a", 0.25));
    for (const s of [-1, 1]) P(at3(sphere(0.014, 1.2, 0.85, 0.45), s * 0.016, 0.142, 0.052), solidM("#d62828", 0.5)); P(at3(sphere(0.007), 0, 0.142, 0.056), solidM("#b51d1d", 0.5));
    Object.assign(k, { w: 0.17, h: 0.25, d: 0.13 });
  } else if (name === "macchinina") {                        // a toy car in its blister pack
    const card = new THREE.BoxGeometry(0.15, 0.19, 0.012); card.translate(0, 0.095, -0.02); P(card, boxMats(texM(TX.blister(), 0.5), solidM("#8f1515")));
    const body = new THREE.BoxGeometry(0.11, 0.026, 0.045); body.translate(0, 0.055, 0.012); P(body, std({ color: "#ffffff", roughness: 0.25, metalness: 0.4 }), true);
    const cab = new THREE.BoxGeometry(0.05, 0.022, 0.04); cab.translate(-0.006, 0.078, 0.012); P(cab, solidM("#1b2630", 0.1, 0.5));
    for (const sx of [-0.035, 0.035]) { const wh = new THREE.CylinderGeometry(0.012, 0.012, 0.05, 12); wh.rotateX(Math.PI / 2); wh.translate(sx, 0.042, 0.012); P(wh, solidM("#151515", 0.8)); }
    const bub = new THREE.BoxGeometry(0.13, 0.08, 0.06); bub.translate(0, 0.064, 0.012); P(bub, std({ color: "#ffffff", roughness: 0.05, transparent: true, opacity: 0.18 }));
    Object.assign(k, { w: 0.16, h: 0.19, d: 0.07, stack: 2 });
  } else if (name === "palla") {
    const g = new THREE.SphereGeometry(0.075, 28, 18); g.rotateZ(0.5); g.translate(0, 0.075, 0); P(g, texM(TX.ball(), 0.35));
    Object.assign(k, { w: 0.16, h: 0.15, d: 0.15, stack: 2 });
  } else if (name.startsWith("gioco")) {
    const v = +name.slice(-1), c = ["#2a9d8f", "#6a4c93", "#fb8500"][v], g = new THREE.BoxGeometry(0.27, 0.2, 0.06); g.translate(0, 0.1, 0);
    P(g, boxMats(texM(TX.gioco(v), 0.45), solidM(c, 0.5)));
    Object.assign(k, { w: 0.28, h: 0.2, d: 0.06 });
  } else if (name === "lecca") {
    const s = sphere(0.022, 1, 1, 0.45); s.translate(0, 0.075, 0); P(s, texM(TX.lolly(), 0.3), true);
    const st = new THREE.CylinderGeometry(0.003, 0.003, 0.06, 6); st.translate(0, 0.03, 0); P(st, solidM("#ffffff", 0.5));
    Object.assign(k, { w: 0.05, h: 0.1, d: 0.03 });
  } else if (name === "gomme") {
    const g = new THREE.BoxGeometry(0.07, 0.05, 0.03); g.translate(0, 0.025, 0); P(g, boxMats(texM(TX.gum(), 0.5), solidM("#1fb5a8")));
    Object.assign(k, { w: 0.075, h: 0.05, d: 0.03, stack: 3 });
  }
  return (KINDS[name] = k);
}
// what goes on each shelf: per row (bottom -> top) the product kinds, in runs
const PLAN = {
  giocattoli: [["palla"], ["orsetto"], ["macchinina"], ["gioco0", "gioco1", "gioco2"]],
  tipici: [["parmigiano"], ["vino"], ["salame", "barattolo"], ["pasta", "salameIntero"]],
  dolci: [["panettone", "pandoro"], ["biscotti0", "biscotti1", "biscotti2"], ["prisma"], ["latta", "biscotti1"]],
  cassa: [["gomme"], ["lecca"]],
};
const TINT = { orsetto: ["#9a6a40", "#d9b58c", "#f2a7b8", "#f4efe6", "#7a8fd6"], macchinina: ["#e63946", "#219ebc", "#ffb703", "#2a9d8f"], vino: ["#f3ead6", "#ffffff", "#f6e2b8"],
  barattolo: ["#b8321f", "#5c7a2a", "#d06a1f"], lecca: ["#ffffff", "#ffd6e5", "#e0f4ff"] };
function shelf2(o) {
  const [L, Hh, D] = o.size, g = new THREE.Group(), rows = o.rows || 4, rh = (Hh - 0.12) / rows, seed = o.seed || 1;
  const body = M("shelfBody", () => std({ color: "#f1efea", roughness: 0.5, metalness: 0.15 })), edge = M("shelfEdge", () => std({ color: "#8b8f94", roughness: 0.35, metalness: 0.7 }));
  const add = (w, h, d, x, y, z, m) => { const b = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), m || body); b.position.set(x, y, z); g.add(b); return b; };
  const Li = L - 0.08;                                     // the inner parts stop at the side panels: equal faces in one plane flicker (z-fighting)
  add(Li, 0.12, D, 0, 0.06, 0, edge);
  const peg = TX.peg().clone(); peg.needsUpdate = true; peg.repeat.set(L / 0.25, (Hh - 0.12) / 0.25);
  add(Li, Hh - 0.12, 0.04, 0, 0.12 + (Hh - 0.12) / 2, 0, std({ map: peg, roughness: 0.7 }));
  for (let r = 1; r <= rows; r++) { add(Li, 0.022, D, 0, 0.12 + r * rh - (r === rows ? 0 : 0.011), 0); if (r < rows) for (const s of [-1, 1]) add(Li, 0.035, 0.012, 0, 0.12 + r * rh - 0.02, s * (D / 2 + 0.006), edge); }
  add(0.04, Hh + 0.004, D + 0.03, -L / 2 + 0.02, Hh / 2 + 0.002, 0); add(0.04, Hh + 0.004, D + 0.03, L / 2 - 0.02, Hh / 2 + 0.002, 0);
  if (o.accent && o.label) { const t = texM(TX.header(o.label, o.accent), 0.5, { emissive: "#ffffff", emissiveMap: TX.header(o.label, o.accent), emissiveIntensity: 0.25 }); const hb = add(L, 0.3, 0.05, 0, Hh + 0.19, 0, [o.accent && solidM(o.accent), solidM(o.accent), solidM(o.accent), solidM(o.accent), t, t]); for (const s of [-1, 1]) add(0.03, 0.06, 0.03, s * (L / 2 - 0.3), Hh + 0.02, 0, edge); }
  // place the products
  const plan = PLAN[o.theme], items = {};
  const push = (name, mat) => (items[name] = items[name] || []).push(mat);
  const Q = new THREE.Quaternion(), E = new THREE.Euler(), P = new THREE.Vector3(), S = new THREE.Vector3(1, 1, 1), MX = new THREE.Matrix4();
  for (const s of [-1, 1]) for (let r = 0; r < rows && r < plan.length; r++) {
    const kinds = plan[r], y0 = 0.12 + r * rh + 0.011; let x = -L / 2 + 0.08, run = 0, cur = null, n = 0;
    while (true) {
      if (run <= 0) { cur = kinds[Math.floor(hash(n + seed, r, s) * kinds.length)]; run = 2 + Math.floor(hash(n * 3 + seed, r * 5, s) * 4); }
      const k = K(cur), gap = 0.012 + 0.012 * hash(n, r + seed, s);
      if (x + k.w > L / 2 - 0.08) break;
      const cx = x + k.w / 2, stack = Math.max(1, Math.min(k.stack, Math.floor((rh - 0.05) / k.h)));
      for (let j = 0; j < stack; j++) {
        if (k.pyramid && j > 0 && hash(n, j, r + s) < 0.25) continue;
        const yaw = (s > 0 ? 0 : Math.PI) + (hash(n * 7, r, j + s) - 0.5) * 0.12;
        E.set(0, yaw, 0, "YXZ"); Q.setFromEuler(E);
        P.set(cx, y0 + j * k.h, s * (D / 2 - 0.03 - k.d / 2));
        MX.compose(P, Q, S); push(cur, MX.clone());
      }
      x += k.w + gap; run--; n++;
    }
  }
  for (const name in items) {
    const k = K(name), list = items[name], tints = TINT[name];
    for (const p of k.parts) {
      const im = new THREE.InstancedMesh(p.geo, p.mat, list.length), C = new THREE.Color();
      list.forEach((m, i) => { im.setMatrixAt(i, m); if (p.tint && tints) { C.set(tints[Math.floor(hash(i * 1.7, 3, seed) * tints.length)]); im.setColorAt(i, C); } });
      im.instanceMatrix.needsUpdate = true; if (im.instanceColor) im.instanceColor.needsUpdate = true; g.add(im);
    }
  }
  // salami hanging from a bar above the shelf (the tipici shelf)
  if (o.hang) {
    const yb = Hh + 0.62; add(L - 0.3, 0.025, 0.025, 0, yb, 0, edge); for (const s of [-1, 1]) add(0.025, 0.62, 0.025, s * (L / 2 - 0.15), Hh + 0.31, 0, edge);
    const n = Math.floor((L - 0.5) / 0.13), sal = new THREE.CapsuleGeometry(0.042, 0.22, 8, 18), str = new THREE.CylinderGeometry(0.003, 0.003, 0.08, 5);
    const im = new THREE.InstancedMesh(sal, texM(TX.salSkin(), 0.85), n), is = new THREE.InstancedMesh(str, solidM("#efe6d6", 0.9), n);
    for (let i = 0; i < n; i++) { const xx = -L / 2 + 0.3 + i * 0.13, len = 0.85 + 0.3 * hash(i, 9, seed); E.set(0, 0, (hash(i, 4, seed) - 0.5) * 0.08); Q.setFromEuler(E);
      MX.compose(P.set(xx, yb - 0.08 - 0.155 * len, 0), Q, new THREE.Vector3(1, len, 1)); im.setMatrixAt(i, MX.clone()); MX.compose(P.set(xx, yb - 0.04, 0), Q, S); is.setMatrixAt(i, MX.clone()); }
    g.add(im); g.add(is);
  }
  return g;
}

function grassTex(size) {                                  // mown grass: blades and darker patches
  const t = ctex("grass", 512, 512, (x, w, h) => {
    x.fillStyle = "#6f8a4c"; x.fillRect(0, 0, w, h); speckle(x, w, h, 90, ["#5f7a3f", "#7e9a57"], 20, 60, 0.15, 0.35, 51);
    for (let i = 0; i < 5000; i++) { x.strokeStyle = ["#5a7538", "#86a35c", "#6b8746", "#94ad66"][i % 4]; x.globalAlpha = 0.5; x.lineWidth = 1.5; const X = rnd(i * 3 + 7) * w, Y = rnd(i * 5 + 7) * h; x.beginPath(); x.moveTo(X, Y); x.lineTo(X + (rnd(i) - 0.5) * 5, Y - 5 - rnd(i * 9) * 8); x.stroke(); }
    x.globalAlpha = 1;
  }, true);
  t.repeat.set(size[0] / 5, size[2] / 5); return t;
}
