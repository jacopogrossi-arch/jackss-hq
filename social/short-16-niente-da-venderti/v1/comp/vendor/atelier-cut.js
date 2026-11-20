// atelier-cut.js (14/11/2026): the cutting-table story props, after Jacopo's note "le forbici si muovono a caso e si capisce poco".
//   patterncut: a real trouser FRONT pattern piece on pattern paper (outline, grain line, notches, pleat marks, writing), and tailor's shears that CUT ALONG
//               the outline over o.cut = [t0, t1] (plate seconds): blades open and close, the cut edge appears behind them. Size [w, d], the piece runs along z.
//   logoplate:  the Inverso logo (the real SVG paths) on an ink board hung by two cords. Size [w, h], faces +z, origin = board centre.
//   weight / chalk / lsquare: pattern weights, a tailor's chalk, a metal L-square.
// Same conventions as atelier-kit.js: metres, y up, lying on y = 0, front = +z.
import * as THREE from "./three.module.min.js";
import { lerp, clamp, smooth } from "./atelier-tex.js";

const M = (c, r = 0.5, m = 0) => new THREE.MeshStandardMaterial({ color: c, roughness: r, metalness: m });
function add(g, geo, mat, x = 0, y = 0, z = 0, rx = 0, ry = 0, rz = 0) { const m = new THREE.Mesh(geo, mat); m.position.set(x, y, z); m.rotation.set(rx, ry, rz); g.add(m); return m; }

// ---------- the pattern piece: normalised paper coords (u across, v along; v = 0 is the waist, far from the camera)
const OUTLINE = (() => {
  const P = [], seg = (pts, n = 10) => { for (let i = 0; i < pts.length - 1; i++) for (let k = 0; k < n; k++) { const f = k / n; P.push([lerp(pts[i][0], pts[i + 1][0], f), lerp(pts[i][1], pts[i + 1][1], f)]); } };
  const quad = (a, c, b, n = 16) => { for (let k = 0; k < n; k++) { const f = k / n, u = (1 - f) * (1 - f) * a[0] + 2 * f * (1 - f) * c[0] + f * f * b[0], v = (1 - f) * (1 - f) * a[1] + 2 * f * (1 - f) * c[1] + f * f * b[1]; P.push([u, v]); } };
  quad([0.64, 0.07], [0.70, 0.17], [0.685, 0.33], 14);          // side seam: waist -> hip curve
  seg([[0.685, 0.33], [0.655, 0.60], [0.635, 0.93]], 18);         // side seam -> hem (straight, a hint of taper)
  seg([[0.635, 0.93], [0.385, 0.93]], 14);                        // hem
  seg([[0.385, 0.93], [0.36, 0.60], [0.33, 0.43]], 18);           // inseam
  quad([0.33, 0.43], [0.27, 0.39], [0.215, 0.375], 12);           // crotch point
  quad([0.215, 0.375], [0.30, 0.34], [0.315, 0.22], 14);          // crotch curve
  seg([[0.315, 0.22], [0.32, 0.07], [0.64, 0.07]], 16);           // centre front -> waist
  P.push([0.64, 0.07]); return P;
})();
const CUT_END = OUTLINE.findIndex((p, i) => i > 60 && p[0] < 0.34 && p[1] < 0.44);   // the shears cut side seam + hem + inseam (the part the camera sees)

function patterncut(o) {
  const [w, d] = o.size, [t0, t1] = o.cut || [0, 1], W = 1400, H = Math.round(W * d / w), g = new THREE.Group();
  const base = document.createElement("canvas"); base.width = W; base.height = H; const b = base.getContext("2d"), X = (u) => u * W, Yv = (v) => v * H;
  b.fillStyle = "#f2ede1"; b.fillRect(0, 0, W, H);
  b.fillStyle = "rgba(60,90,140,.22)"; for (let i = 20; i < W; i += 28) for (let j = 20; j < H; j += 28) b.fillRect(i, j, 3, 3);                  // dotted pattern paper
  b.fillStyle = "rgba(255,252,244,.55)"; b.beginPath(); OUTLINE.forEach((p, i) => (i ? b.lineTo(X(p[0]), Yv(p[1])) : b.moveTo(X(p[0]), Yv(p[1])))); b.fill();
  b.strokeStyle = "#26211c"; b.lineWidth = 4.5; b.lineJoin = "round"; b.beginPath(); OUTLINE.forEach((p, i) => (i ? b.lineTo(X(p[0]), Yv(p[1])) : b.moveTo(X(p[0]), Yv(p[1])))); b.stroke();
  b.strokeStyle = "rgba(38,33,28,.45)"; b.lineWidth = 2; b.setLineDash([10, 8]); b.beginPath();                                                // the 1 cm seam allowance, inside
  OUTLINE.forEach((p, i) => { const q = [lerp(p[0], 0.49, 0.045), lerp(p[1], 0.5, 0.03)]; i ? b.lineTo(X(q[0]), Yv(q[1])) : b.moveTo(X(q[0]), Yv(q[1])); }); b.stroke(); b.setLineDash([]);
  b.strokeStyle = "#26211c"; b.lineWidth = 4; b.beginPath(); b.moveTo(X(0.50), Yv(0.16)); b.lineTo(X(0.50), Yv(0.86)); b.stroke();               // grain line with arrows
  for (const [v, s] of [[0.16, 1], [0.86, -1]]) { b.beginPath(); b.moveTo(X(0.50), Yv(v)); b.lineTo(X(0.485), Yv(v + s * 0.03)); b.moveTo(X(0.50), Yv(v)); b.lineTo(X(0.515), Yv(v + s * 0.03)); b.stroke(); }
  b.lineWidth = 4; for (const [u, v] of [[0.69, 0.24], [0.664, 0.52], [0.367, 0.66]]) { const out = u > 0.5 ? 1 : -1; b.beginPath(); b.moveTo(X(u), Yv(v)); b.lineTo(X(u + out * 0.035), Yv(v)); b.stroke(); }   // notches
  for (const u of [0.42, 0.53]) { b.beginPath(); b.moveTo(X(u - 0.02), Yv(0.07)); b.lineTo(X(u), Yv(0.14)); b.lineTo(X(u + 0.02), Yv(0.07)); b.stroke(); }  // double pleat
  b.strokeStyle = "rgba(38,33,28,.6)"; b.lineWidth = 2.5; b.beginPath(); b.moveTo(X(0.33), Yv(0.43)); b.lineTo(X(0.685), Yv(0.33)); b.stroke();  // hip line
  b.beginPath(); b.moveTo(X(0.36), Yv(0.62)); b.lineTo(X(0.66), Yv(0.62)); b.stroke();                                                            // knee line
  b.save(); b.translate(X(0.555), Yv(0.70)); b.rotate(-Math.PI / 2); b.fillStyle = "#26211c"; b.font = "600 " + Math.round(W * 0.03) + "px Inter, sans-serif"; b.fillText("DAVANTI · TG 48", 0, 0);
  b.font = "italic 500 " + Math.round(W * 0.027) + "px 'Playfair Display', Georgia, serif"; b.fillStyle = "#8a4b2d"; b.fillText("taglia 2 · tela", 0, W * 0.04); b.restore();
  b.save(); b.translate(X(0.475), Yv(0.55)); b.rotate(-Math.PI / 2); b.font = "500 " + Math.round(W * 0.018) + "px Inter, sans-serif"; b.fillStyle = "#26211c"; b.fillText("drittofilo", 0, 0); b.restore();
  const cvs = document.createElement("canvas"); cvs.width = W; cvs.height = H; const cx = cvs.getContext("2d"), tx = new THREE.CanvasTexture(cvs); tx.colorSpace = THREE.SRGBColorSpace; tx.anisotropy = 16;
  const mesh = new THREE.Mesh(new THREE.PlaneGeometry(w, d), new THREE.MeshStandardMaterial({ map: tx, roughness: 0.92 })); mesh.rotation.x = -Math.PI / 2; mesh.position.y = 0.0015; mesh.receiveShadow = true; g.add(mesh);
  // the shears: two extruded blades on a screw, black and orange bows; local +x = the way the blades point
  const sh = new THREE.Group(), steel = M("#cfd3d8", 0.2, 1.0), blade = (side) => {
    const s = new THREE.Shape(); s.moveTo(-0.02, 0); s.lineTo(0.15, side * 0.002); s.quadraticCurveTo(0.165, side * 0.004, 0.15, side * 0.011); s.lineTo(0.0, side * 0.016); s.lineTo(-0.02, side * 0.008); s.closePath();
    const m = new THREE.Mesh(new THREE.ExtrudeGeometry(s, { depth: 0.0022, bevelEnabled: true, bevelThickness: 0.0006, bevelSize: 0.0006, bevelSegments: 2 }), steel); m.rotation.x = -Math.PI / 2; return m;
  };
  const armA = new THREE.Group(), armB = new THREE.Group(); armA.add(blade(1)); armB.add(blade(-1)); armB.position.y = 0.003;
  for (const [arm, col, r, side] of [[armA, "#1e1b18", 0.022, 1], [armB, "#c8501f", 0.026, -1]]) {
    const shank = add(arm, new THREE.BoxGeometry(0.07, 0.005, 0.009), steel, -0.05, 0.001, side * 0.006, 0, side * 0.18, 0);
    const bow = add(arm, new THREE.TorusGeometry(r, 0.0055, 10, 28), M(col, 0.45, 0.05), -0.085 - r * 0.6, 0.001, side * (0.016 + r * 0.55), Math.PI / 2, 0, 0); bow.scale.set(1, 0.72, 1);
  }
  add(sh, new THREE.CylinderGeometry(0.0045, 0.0045, 0.009, 16), steel, 0, 0.002, 0); sh.add(armA, armB); sh.position.y = 0.006; g.add(sh);
  const P = (i) => { const p = OUTLINE[Math.max(0, Math.min(OUTLINE.length - 1, i))]; return [(p[0] - 0.5) * w, (p[1] - 0.5) * d]; };
  let last = -1;
  const draw = (q) => {
    cx.drawImage(base, 0, 0); const n = Math.floor(q * CUT_END); if (n < 1) { tx.needsUpdate = true; return; }
    cx.lineJoin = "round"; cx.lineCap = "round";
    cx.strokeStyle = "rgba(20,16,12,.55)"; cx.lineWidth = 9; cx.beginPath(); for (let i = 0; i <= n; i++) { const p = OUTLINE[i]; i ? cx.lineTo(X(p[0]), Yv(p[1])) : cx.moveTo(X(p[0]), Yv(p[1])); } cx.stroke();     // the slit: a shadowed edge
    cx.strokeStyle = "rgba(255,255,255,.9)"; cx.lineWidth = 2.5; cx.beginPath(); for (let i = 0; i <= n; i++) { const p = OUTLINE[i]; i ? cx.lineTo(X(p[0]) + 4, Yv(p[1]) - 3) : cx.moveTo(X(p[0]) + 4, Yv(p[1]) - 3); } cx.stroke();
    tx.needsUpdate = true;
  };
  g.userData.update = (t) => {
    const q = smooth(clamp((t - t0) / (t1 - t0))), k = Math.round(q * 400);
    if (k !== last) { last = k; draw(k / 400); }
    const f = q * CUT_END, i = Math.floor(f), fr = f - i, c = P(i), c2 = P(i + 1);
    let dx = 0, dz = 0; for (let j = -8; j <= 8; j++) { const u = P(i + j), v = P(i + j + 1), w8 = 1 - Math.abs(j) / 9; dx += (v[0] - u[0]) * w8; dz += (v[1] - u[1]) * w8; }   // direction averaged over ±8 points: the shears turn round a corner, they don't snap 90°
    const L = Math.hypot(dx, dz) || 1;
    const px = lerp(c[0], c2[0], fr), pz = lerp(c[1], c2[1], fr);
    sh.position.x = px - (dx / L) * 0.05; sh.position.z = pz - (dz / L) * 0.05; sh.rotation.y = -Math.atan2(dz, dx);
    const cutting = t > t0 && t < t1, open = cutting ? 0.2 * (0.5 + 0.5 * Math.cos((t - t0) * Math.PI * 2 * 2.4)) : 0.05;
    armA.rotation.y = open; armB.rotation.y = -open;
  };
  g.userData.update(-1); return g;
}

// ---------- the Inverso logo: the real paths of inverso/logo/inverso-logo.svg (10/11/2026)
const LOGO = [
  [59.5, "M101 288H163V289C148 291 144 300 144 315V407C144 423 148 431 163 433V435H101V433C115 431 119 423 119 407V315C119 300 115 291 101 289Z"],
  [33.5, "M209 288H249L344 397V319C344 300 338 291 322 289V288H369V289C353 292 348 300 348 319V437H343L234 310V404C234 424 240 431 256 433V435H209V433C225 431 230 423 230 404V315C230 301 222 292 209 289Z"],
  [16.5, "M406 288H469V289C455 292 451 299 456 312L495 405L530 315C536 299 532 292 517 289V288H565V289C552 293 546 302 539 318L488 437H483L432 315C426 301 420 292 406 289Z"],
  [-1.5, "M603 288H715L720 325H718C712 302 696 292 673 292H646V357H666C686 357 695 350 698 335H700V383H698C695 367 686 360 666 360H646V415C646 428 649 431 664 431H676C700 431 718 416 726 394H728L721 435H603V433C617 431 621 423 621 408V315C621 300 617 292 603 289Z"],
  [-24.5, "M771 288H828C864 288 886 302 886 327C886 347 873 359 852 365L884 413C893 426 900 431 912 433V435H868L825 368H813V408C813 423 817 431 831 433V435H771V433C785 431 789 423 789 408V315C789 300 785 292 771 289ZM813 292V365H826C849 365 861 352 861 328C861 304 849 292 826 292Z"],
  [-40.5, "M1039 294L1040 329H1038C1033 303 1019 289 998 289C980 289 969 300 969 315C969 332 982 340 1003 350C1031 363 1047 375 1047 399C1047 424 1027 438 998 438C978 438 962 432 949 425L948 386H950C957 417 974 434 997 434C1017 434 1029 423 1029 406C1029 389 1016 380 993 369C967 356 952 345 952 322C952 299 972 285 998 285C1014 285 1027 289 1039 294Z"],
  [-58.5, "M1164 285C1209 285 1242 317 1242 361C1242 406 1209 438 1164 438C1119 438 1085 406 1085 361C1085 317 1119 285 1164 285ZM1164 289C1131 289 1113 317 1113 361C1113 406 1131 434 1164 434C1196 434 1214 406 1214 361C1214 317 1196 289 1164 289Z"],
];
export function drawLogo(x, cxp, cyp, width, color = "#EDE6D6") {   // draws the logo centred on (cxp, cyp), `width` px wide
  const x0 = 150, x1 = 1186, y0 = 273, y1 = 450, s = width / (x1 - x0);
  x.save(); x.translate(cxp - width / 2, cyp - ((y1 - y0) * s) / 2); x.scale(s, s); x.translate(-x0, -y0); x.fillStyle = color;
  for (const [dx, d] of LOGO) { x.save(); x.translate(dx, 0); x.fill(new Path2D(d), "evenodd"); x.restore(); }
  x.fillRect(153.5, 273, 76, 5); x.fillRect(153.5, 445, 76, 5); x.restore();
}
function logoplate(o) {
  const [w, h] = o.size, g = new THREE.Group(), W = 2048, H = Math.round(W * h / w), c = document.createElement("canvas"); c.width = W; c.height = H; const x = c.getContext("2d");
  x.fillStyle = "#1E1B18"; x.fillRect(0, 0, W, H);
  for (let i = 0; i < 2600; i++) { const v = Math.sin(i * 12.9898) * 43758.5453; x.fillStyle = "rgba(255,240,220," + (0.012 + 0.02 * (v - Math.floor(v))).toFixed(3) + ")"; x.fillRect(((v * 7) % 1) * W, (((v * 13) % 1 + 1) % 1) * H, 2, 2); }
  x.strokeStyle = "rgba(185,174,152,.55)"; x.lineWidth = 6; x.strokeRect(46, 46, W - 92, H - 92);
  drawLogo(x, W / 2, H * (o.sub ? 0.45 : 0.5), W * 0.66);
  if (o.sub) { x.fillStyle = "#B9AE98"; x.font = "500 " + Math.round(H * 0.075) + "px 'IBM Plex Sans', Inter, sans-serif"; x.textAlign = "center"; x.fillText(o.sub, W / 2, H * 0.78); }
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 16;
  const face = new THREE.MeshStandardMaterial({ map: t, roughness: 0.55, emissive: 0xffffff, emissiveMap: t, emissiveIntensity: 0.22 }), edge = M("#14110e", 0.6);
  add(g, new THREE.BoxGeometry(w, h, 0.03), [edge, edge, edge, edge, face, edge]);
  const brass = M("#c9a24a", 0.3, 0.9), cord = M("#1e1b18", 0.9);
  for (const s of [-1, 1]) { add(g, new THREE.CylinderGeometry(0.004, 0.004, 3, 6), cord, s * w * 0.38, h / 2 + 1.5, 0).userData.noshadow = true; add(g, new THREE.TorusGeometry(0.012, 0.003, 8, 18), brass, s * w * 0.38, h / 2 + 0.006, 0); }
  return g;
}

// ---------- small things on the cutting table
function weight(o) {                                       // a cast-iron pattern weight with a brass knob
  const g = new THREE.Group(); add(g, new THREE.CylinderGeometry(0.045, 0.048, 0.03, 32), M("#3a3734", 0.55, 0.6), 0, 0.015, 0); add(g, new THREE.CylinderGeometry(0.012, 0.016, 0.03, 18), M("#c9a24a", 0.3, 0.9), 0, 0.045, 0);
  add(g, new THREE.SphereGeometry(0.014, 16, 10), M("#c9a24a", 0.3, 0.9), 0, 0.064, 0); return g;
}
function chalk(o) {                                        // a tailor's chalk: a flat triangle with rounded edges
  const s = new THREE.Shape(); s.moveTo(-0.025, -0.02); s.lineTo(0.025, -0.02); s.lineTo(0, 0.025); s.closePath();
  const g = new THREE.Group(), m = new THREE.Mesh(new THREE.ExtrudeGeometry(s, { depth: 0.005, bevelEnabled: true, bevelThickness: 0.0015, bevelSize: 0.003, bevelSegments: 3 }), M(o.color || "#efe9dd", 0.95)); m.rotation.x = -Math.PI / 2; m.position.y = 0.002; g.add(m); return g;
}
function lsquare(o) {                                      // a metal L-square with ticks: arms o.size = [a, b]
  const [a, b] = o.size || [0.6, 0.35], g = new THREE.Group(), c = document.createElement("canvas"); c.width = 1024; c.height = 48; const x = c.getContext("2d");
  x.fillStyle = "#cfd3d8"; x.fillRect(0, 0, 1024, 48); x.fillStyle = "#26211c"; for (let i = 0; i <= 120; i++) x.fillRect(i * 8.5, 0, 1.5, i % 10 === 0 ? 22 : i % 5 === 0 ? 15 : 9);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; const mat = new THREE.MeshStandardMaterial({ map: t, roughness: 0.3, metalness: 0.7 });
  add(g, new THREE.BoxGeometry(a, 0.003, 0.04), mat, a / 2, 0.0015, 0); add(g, new THREE.BoxGeometry(0.04, 0.003, b), mat, 0, 0.0015, -b / 2 + 0.02); return g;
}

// ---------- the story path (14/11/2026, the Autogrill "serpentone" device): dots that draw themselves along a polyline over o.span = [t0, t1], newest dot pops in.
//   o.pts = [[x, y, z], ...] relative to the prop origin; o.gap = spacing (m); o.r = dot radius; o.color; o.out = time it fades away (optional).
function pathdots(o) {
  const pts = o.pts || [[0, 0, 0], [1, 0, 0]], gap = o.gap || 0.12, r = o.r || 0.028, [t0, t1] = o.span || [0, 1], out = o.out == null ? 1e9 : o.out, g = new THREE.Group();
  const D = [];
  for (let i = 0; i < pts.length - 1; i++) {
    const a = pts[i], b = pts[i + 1], L = Math.hypot(b[0] - a[0], b[1] - a[1], b[2] - a[2]), n = Math.max(1, Math.round(L / gap));
    for (let k = 0; k < n; k++) { const f = k / n; D.push([lerp(a[0], b[0], f), lerp(a[1], b[1], f), lerp(a[2], b[2], f)]); }
  }
  D.push(pts[pts.length - 1]);
  const geo = new THREE.SphereGeometry(r, 14, 10); geo.scale(1, o.flat ? 0.35 : 1, 1);
  const mat = new THREE.MeshStandardMaterial({ color: o.color || "#c0392b", roughness: 0.45, emissive: o.color || "#c0392b", emissiveIntensity: o.glow == null ? 0.35 : o.glow });
  const im = new THREE.InstancedMesh(geo, mat, D.length), m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), sc = new THREE.Vector3(), ps = new THREE.Vector3();
  im.castShadow = false; im.receiveShadow = false; g.add(im);
  g.userData.update = (t) => {
    const fo = t >= out ? clamp(1 - (t - out) / 0.35) : 1, shown = clamp((t - t0) / Math.max(0.01, t1 - t0)) * D.length;
    for (let i = 0; i < D.length; i++) {
      const k = clamp(shown - i), s = (k <= 0 ? 0 : (k < 1 ? 1.35 * Math.sin(k * Math.PI * 0.5) + (k > 0.6 ? (1 - k) * 0.6 : 0) : 1)) * fo;
      ps.set(D[i][0], D[i][1], D[i][2]); sc.set(s || 1e-4, s || 1e-4, s || 1e-4); m4.compose(ps, q, sc); im.setMatrixAt(i, m4);
    }
    im.instanceMatrix.needsUpdate = true;
  };
  g.userData.update(-1); return g;
}

// ---------- a numbered station disc on the floor (seen from above): ink ring, cream face, a big number and a word. o.size = [diameter], o.n, o.word, o.show (appear) / o.out
function floorbadge(o) {
  const d = (o.size || [0.7])[0], c = document.createElement("canvas"); c.width = c.height = 512; const x = c.getContext("2d");
  x.fillStyle = o.ring || "#8A4B2D"; x.beginPath(); x.arc(256, 256, 250, 0, Math.PI * 2); x.fill();
  x.fillStyle = o.face || "#EFE9DD"; x.beginPath(); x.arc(256, 256, 222, 0, Math.PI * 2); x.fill();
  x.fillStyle = o.ink || "#1E1B18"; x.textAlign = "center"; x.textBaseline = "middle";
  x.font = "italic 230px 'Instrument Serif', 'Playfair Display', Georgia, serif"; x.fillText(String(o.n || 1), 256, o.word ? 220 : 262);
  if (o.word) { x.font = "600 54px 'IBM Plex Sans', Inter, sans-serif"; x.fillText(o.word.toUpperCase(), 256, 380); }
  const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace; tx.anisotropy = 8;
  const m = new THREE.Mesh(new THREE.CircleGeometry(d / 2, 64), new THREE.MeshStandardMaterial({ map: tx, roughness: 0.8, transparent: true, polygonOffset: true, polygonOffsetFactor: -4 }));
  m.rotation.x = -Math.PI / 2; m.position.y = 0.004; const g = new THREE.Group(); g.add(m);
  const t0 = o.show == null ? -1 : o.show, out = o.out == null ? 1e9 : o.out;
  g.userData.update = (t) => { const k = t < t0 ? 0 : t >= out ? clamp(1 - (t - out) / 0.3) : clamp((t - t0) / 0.3); const s = k <= 0 ? 1e-4 : (k < 1 ? 1 + 0.15 * Math.sin(k * Math.PI) : 1) * k; m.scale.set(s, s, s); m.material.opacity = k; };
  g.userData.update(-1); return g;
}

export const CUTPROPS = new Set(["patterncut", "logoplate", "weight", "chalk", "lsquare", "pathdots", "floorbadge"]);
export function buildCut(o) {
  switch (o.type) {
    case "patterncut": return patterncut(o);
    case "logoplate": return logoplate(o);
    case "weight": return weight(o);
    case "chalk": return chalk(o);
    case "lsquare": return lsquare(o);
    case "pathdots": return pathdots(o);
    case "floorbadge": return floorbadge(o);
    default: return null;
  }
}
