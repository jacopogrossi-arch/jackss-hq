// atelier-props.js: detailed hero props of the atelier (14/11/2026): a vintage sewing machine (extruded silhouette, enamel, chrome, gold decals with lettering), a dress form
// (turned body, linen weave, seams, pins, turned wooden stand on casters), a cutting mat, a button jar, a pincushion, a spool.
// Same conventions as atelier-kit.js: metres, y up, standing on y = 0, front = +z.
import * as THREE from "./three.module.min.js";
import { buildCut, CUTPROPS } from "./atelier-cut.js";
import { hash2, clothMat, canvasTex, tube, stitches, lerp, smooth, clamp, fabricMaps } from "./atelier-tex.js";

const M = (c, r = 0.5, m = 0) => new THREE.MeshStandardMaterial({ color: c, roughness: r, metalness: m });
const CHROME = () => new THREE.MeshStandardMaterial({ color: 0xdfe2e6, roughness: 0.18, metalness: 1.0 });
function add(g, geo, mat, x = 0, y = 0, z = 0, rx = 0, ry = 0, rz = 0) { const m = new THREE.Mesh(geo, mat); m.position.set(x, y, z); m.rotation.set(rx, ry, rz); g.add(m); return m; }
function scaleUV(geo, su, sv) { const uv = geo.attributes.uv; for (let i = 0; i < uv.count; i++) uv.setXY(i, uv.getX(i) * su, uv.getY(i) * sv); return geo; }
function rrect(w, h, r) { const s = new THREE.Shape(), x = -w / 2, y = -h / 2; s.moveTo(x + r, y); s.lineTo(x + w - r, y); s.quadraticCurveTo(x + w, y, x + w, y + r); s.lineTo(x + w, y + h - r); s.quadraticCurveTo(x + w, y + h, x + w - r, y + h); s.lineTo(x + r, y + h); s.quadraticCurveTo(x, y + h, x, y + h - r); s.lineTo(x, y + r); s.quadraticCurveTo(x, y, x + r, y); return s; }
function ext(shape, depth, bev = 0.004, seg = 16) { const g = new THREE.ExtrudeGeometry(shape, { depth, bevelEnabled: true, bevelThickness: bev, bevelSize: bev, bevelSegments: 4, curveSegments: seg }); g.translate(0, 0, -depth / 2); return g; }

// ---------- the sewing machine
function decalTex() {
  return canvasTex(2048, 512, (x, w, h) => {
    x.clearRect(0, 0, w, h); const gold = "#e3c47f"; x.strokeStyle = gold; x.fillStyle = gold; x.lineCap = "round";
    x.lineWidth = 7; x.beginPath(); x.moveTo(30, 60); x.lineTo(w - 30, 60); x.stroke(); x.lineWidth = 3; x.beginPath(); x.moveTo(30, 82); x.lineTo(w - 30, 82); x.stroke();
    x.lineWidth = 7; x.beginPath(); x.moveTo(30, h - 60); x.lineTo(w - 30, h - 60); x.stroke(); x.lineWidth = 3; x.beginPath(); x.moveTo(30, h - 82); x.lineTo(w - 30, h - 82); x.stroke();
    x.textBaseline = "middle"; x.textAlign = "center"; x.font = "italic 600 190px 'Playfair Display', Georgia, serif"; x.fillText("Inverso", w / 2, h * 0.46);
    x.font = "600 58px Inter, sans-serif"; x.letterSpacing = "10px"; x.fillText("ATELIER · MODELLO 1977 · ROMA", w / 2, h * 0.78);
    for (const sx of [150, w - 150]) { x.beginPath(); x.arc(sx, h * 0.46, 46, 0, Math.PI * 2); x.lineWidth = 5; x.stroke(); x.beginPath(); x.arc(sx, h * 0.46, 22, 0, Math.PI * 2); x.fill(); }
  }, true);
}
function sewing(o) {
  const g = new THREE.Group(), D = 0.105, enamel = new THREE.MeshPhysicalMaterial({ color: o.color || "#1f3a2e", roughness: 0.22, metalness: 0.15, clearcoat: 1.0, clearcoatRoughness: 0.08 }), chrome = CHROME(), black = M("#141210", 0.5, 0.2);
  // the silhouette: bed, pillar, arm and head in one extruded, bevelled piece
  const s = new THREE.Shape(); s.moveTo(-0.215, 0.0); s.lineTo(0.205, 0.0); s.quadraticCurveTo(0.218, 0.0, 0.218, 0.014); s.lineTo(0.218, 0.040); s.lineTo(0.19, 0.047);
  s.lineTo(0.19, 0.25); s.quadraticCurveTo(0.19, 0.305, 0.135, 0.308); s.lineTo(-0.115, 0.308); s.quadraticCurveTo(-0.165, 0.312, -0.19, 0.285); s.lineTo(-0.206, 0.215); s.quadraticCurveTo(-0.208, 0.178, -0.18, 0.178);
  s.lineTo(-0.135, 0.178); s.lineTo(-0.085, 0.192); s.lineTo(0.082, 0.192); s.quadraticCurveTo(0.098, 0.12, 0.098, 0.062); s.lineTo(0.092, 0.047); s.lineTo(-0.19, 0.047); s.lineTo(-0.215, 0.032); s.closePath();
  add(g, ext(s, D, 0.006), enamel, 0, 0, 0);
  // decals: the name and a double gold stripe on the arm, a small plaque on the pillar
  const dc = new THREE.MeshBasicMaterial({ map: decalTex(), transparent: true, toneMapped: false, depthWrite: false, polygonOffset: true, polygonOffsetFactor: -2 });
  const dp = add(g, new THREE.PlaneGeometry(0.205, 0.0512), dc, 0.04, 0.2505, D / 2 + 0.0064); dp.userData.noshadow = true;
  const dp2 = add(g, new THREE.PlaneGeometry(0.205, 0.0512), dc, 0.04, 0.2505, -D / 2 - 0.0064, 0, Math.PI, 0); dp2.userData.noshadow = true;
  // bed: chrome slide plates, needle plate with its slot, a drawer line
  add(g, new THREE.BoxGeometry(0.105, 0.003, 0.074), chrome, -0.115, 0.0485, 0.0); add(g, new THREE.BoxGeometry(0.035, 0.0012, 0.006), black, -0.15, 0.0504, 0.0);
  add(g, new THREE.BoxGeometry(0.052, 0.0025, 0.03), chrome, -0.14, 0.0515, 0.0); add(g, new THREE.BoxGeometry(0.012, 0.0013, 0.0045), black, -0.15, 0.0531, 0.0);
  // head: needle bar, presser bar and foot, needle, thread guides, tension dial, stitch lever
  const nx = -0.15; add(g, new THREE.CylinderGeometry(0.0034, 0.0034, 0.112, 12), chrome, nx, 0.112 + 0.001, 0.003); add(g, new THREE.CylinderGeometry(0.0053, 0.0053, 0.1, 12), chrome, nx - 0.019, 0.128, 0.0);
  add(g, new THREE.CylinderGeometry(0.0007, 0.0014, 0.032, 8), chrome, nx, 0.068, 0.003); add(g, new THREE.CylinderGeometry(0.0075, 0.0075, 0.012, 14), chrome, nx, 0.103, 0.003);
  const fs = new THREE.Shape(); fs.moveTo(0, 0); fs.lineTo(0.036, 0); fs.lineTo(0.040, 0.004); fs.lineTo(0.036, 0.008); fs.lineTo(0.008, 0.009); fs.lineTo(0.008, 0.032); fs.lineTo(0, 0.032); fs.closePath();
  const foot = add(g, ext(fs, 0.012, 0.0015, 6), chrome, nx - 0.019 - 0.004, 0.055, 0.0); foot.rotation.y = Math.PI / 2; foot.position.set(nx - 0.019, 0.056, 0.0); foot.scale.set(1, 1, 1);
  add(g, new THREE.CylinderGeometry(0.0165, 0.0165, 0.014, 28), chrome, nx - 0.002, 0.255, D / 2 + 0.0075, Math.PI / 2, 0, 0);                    // tension dial, knurled by a ring of ribs
  for (let k = 0; k < 24; k++) { const a = k / 24 * Math.PI * 2; add(g, new THREE.BoxGeometry(0.0016, 0.0016, 0.012), black, nx - 0.002 + Math.cos(a) * 0.0165, 0.255 + Math.sin(a) * 0.0165, D / 2 + 0.0075); }
  add(g, new THREE.CylinderGeometry(0.009, 0.009, 0.006, 20), black, nx - 0.002, 0.255, D / 2 + 0.017, Math.PI / 2, 0, 0);
  add(g, new THREE.BoxGeometry(0.06, 0.008, 0.01), chrome, 0.145, 0.12, D / 2 + 0.003); const lv = add(g, new THREE.BoxGeometry(0.008, 0.036, 0.008), black, 0.16, 0.13, D / 2 + 0.01); lv.rotation.z = 0.3;
  add(g, new THREE.CylinderGeometry(0.012, 0.012, 0.01, 18), chrome, 0.12, 0.235, D / 2 + 0.006, Math.PI / 2, 0, 0);
  // the handwheel (right end): chrome rim with ribs, enamel hub, black knob
  const hw = new THREE.Group(); hw.position.set(0.235, 0.255, 0);
  add(hw, new THREE.CylinderGeometry(0.052, 0.052, 0.014, 40), chrome, 0.0, 0, 0, 0, 0, Math.PI / 2); add(hw, new THREE.CylinderGeometry(0.043, 0.043, 0.018, 36), enamel, 0.004, 0, 0, 0, 0, Math.PI / 2);
  add(hw, new THREE.TorusGeometry(0.047, 0.0024, 8, 40), chrome, 0.006, 0, 0, 0, Math.PI / 2, 0); add(hw, new THREE.CylinderGeometry(0.012, 0.012, 0.024, 20), black, 0.014, 0, 0, 0, 0, Math.PI / 2); add(hw, new THREE.CylinderGeometry(0.006, 0.006, 0.01, 12), chrome, 0.028, 0, 0, 0, 0, Math.PI / 2);
  for (let k = 0; k < 5; k++) { const a = k / 5 * Math.PI * 2 + 0.3; add(hw, new THREE.BoxGeometry(0.006, 0.014, 0.006), chrome, 0.0, Math.cos(a) * 0.03, Math.sin(a) * 0.03, a, 0, 0); } g.add(hw);
  // the spool on its pin, with a thread that runs over the guides to the needle
  const spool = new THREE.Group(); spool.position.set(0.03, 0.308, 0);
  add(spool, new THREE.CylinderGeometry(0.0032, 0.0032, 0.05, 8), chrome, 0, 0.025, 0);
  const spl = new THREE.LatheGeometry([[0.004, 0], [0.0145, 0], [0.0145, 0.003], [0.007, 0.004], [0.007, 0.032], [0.0145, 0.033], [0.0145, 0.036], [0.004, 0.036]].map((p) => new THREE.Vector2(p[0], p[1])), 22);
  add(spool, spl, M("#c9a46a", 0.6), 0, 0.004, 0); add(spool, new THREE.CylinderGeometry(0.0121, 0.0121, 0.027, 22), clothMat(o.thread || "#8a4b2d", "plain", { n: 0.6 }), 0, 0.0195, 0); g.add(spool);
  const th = [[0.03, 0.34, 0.0], [0.0, 0.352, 0.004], [-0.05, 0.322, D / 2 + 0.004], [nx - 0.002, 0.30, D / 2 + 0.008], [nx - 0.002, 0.26, D / 2 + 0.016], [nx - 0.002, 0.205, D / 2 + 0.006], [nx, 0.12, 0.004], [nx, 0.068, 0.003]];
  g.add(tube(th, 0.0007, M(o.thread || "#8a4b2d", 0.8), 50));
  for (const p of [[-0.05, 0.322, D / 2 + 0.004], [nx - 0.002, 0.205, D / 2 + 0.006]]) { const e = new THREE.Mesh(new THREE.TorusGeometry(0.0038, 0.0009, 6, 14), chrome); e.position.set(...p); g.add(e); }
  // bobbin winder on the arm, the light under the head, the power cord
  add(g, new THREE.CylinderGeometry(0.008, 0.008, 0.018, 14), chrome, 0.15, 0.318, 0.02); add(g, new THREE.CylinderGeometry(0.014, 0.01, 0.022, 14), black, -0.15, 0.172, -0.03);
  const cord = [[0.19, 0.04, -0.02], [0.24, 0.03, -0.08], [0.30, 0.0, -0.16], [0.38, -0.2, -0.20]]; g.add(tube(cord, 0.0036, M("#1a1714", 0.7), 30));
  // a little cloth under the needle with a line of stitches
  const cloth = add(g, new THREE.BoxGeometry(0.15, 0.0035, 0.2), clothMat(o.cloth || "#e4dcc6", "plain"), nx + 0.0, 0.0555, 0.0, 0, 0.1, 0);
  const st = []; for (let k = 0; k <= 20; k++) st.push([nx + 0.0 + 0.0003 * k, 0.0576, lerp(0.095, -0.0, k / 20) * 1.0 - 0.0]); g.add(stitches(st, "#8a4b2d", 0.0045, 0.0028, 0.0007));
  g.rotation.y = 0; return g;
}

// ---------- the dress form
function mannequin(o) {
  const g = new THREE.Group(), lin = o.linen || "#d8ccb0", mat = clothMat(lin, "linen", { n: 0.9, rough: 0.95, side: THREE.DoubleSide }), wood = M("#4a3322", 0.45, 0.1), brass = M("#c9a24a", 0.3, 0.9), steel = CHROME();
  const prof = [[0.001, 0.0], [0.12, 0.004], [0.152, 0.04], [0.172, 0.10], [0.170, 0.17], [0.150, 0.27], [0.138, 0.33], [0.147, 0.40], [0.166, 0.47], [0.176, 0.53], [0.168, 0.60], [0.148, 0.655], [0.120, 0.695], [0.080, 0.722], [0.052, 0.742], [0.043, 0.78], [0.038, 0.82], [0.001, 0.832]];
  const TY = 0.84, torso = new THREE.Group(); torso.position.y = TY;
  const lg = scaleUV(new THREE.LatheGeometry(prof.map((p) => new THREE.Vector2(p[0], p[1])), 64), 12, 11), body = new THREE.Mesh(lg, mat); body.scale.set(1.2, 1, 0.74); torso.add(body);
  for (const sx of [-1, 1]) { const cap = new THREE.Mesh(scaleUV(new THREE.SphereGeometry(1, 20, 14), 3, 3), mat); cap.position.set(sx * 0.178, 0.648, 0.0); cap.scale.set(0.042, 0.05, 0.066); cap.rotation.z = sx * 0.55; torso.add(cap); }
  add(torso, new THREE.TorusGeometry(0.046, 0.005, 8, 28), brass, 0, 0.775, 0, Math.PI / 2, 0, 0);                                             // brass collar at the neck
  add(torso, new THREE.SphereGeometry(0.036, 18, 12), M("#4a3322", 0.4, 0.1), 0, 0.86, 0); add(torso, new THREE.CylinderGeometry(0.012, 0.018, 0.03, 14), wood, 0, 0.83, 0);   // the turned knob on top
  // seams: centre front, princess seams, side seams, a waist tape
  const pr = (y, rfac = 1) => { let i = 0; while (i < prof.length - 2 && y > prof[i + 1][1]) i++; const a = prof[i], b = prof[i + 1], k = clamp((y - a[1]) / (b[1] - a[1])); return lerp(a[0], b[0], k) * rfac; };
  const seam = (a0, a1, y0, y1, n = 24) => { const p = []; for (let k = 0; k <= n; k++) { const u = k / n, y = lerp(y0, y1, u), a = lerp(a0, a1, smooth(u)), r = pr(y) + 0.0012; p.push([r * 1.2 * Math.sin(a), y, r * 0.74 * Math.cos(a)]); } return tube(p, 0.0013, M("#8a7a5a", 0.9), 40); };
  for (const sx of [-1, 1]) { torso.add(seam(0.0, 0.0, 0.01, 0.735)); torso.add(seam(sx * 0.62, sx * 0.40, 0.66, 0.06)); torso.add(seam(sx * 1.45, sx * 1.55, 0.64, 0.02)); torso.add(seam(sx * 2.8, sx * 3.0, 0.64, 0.02)); }
  const tape = add(torso, new THREE.TorusGeometry(1, 0.0045, 6, 56), M("#f0c93a", 0.6), 0, 0.33, 0, Math.PI / 2, 0, 0); tape.scale.set(0.141 * 1.2, 0.141 * 0.74, 1);
  for (let k = 0; k < 9; k++) { const a = -0.5 + k * 0.13, y = 0.52 + 0.01 * Math.sin(k * 2.3), r = pr(y) + 0.001; const pn = new THREE.Group(); const sh = new THREE.Mesh(new THREE.CylinderGeometry(0.0006, 0.0006, 0.03, 5), steel), hd = new THREE.Mesh(new THREE.SphereGeometry(0.002, 8, 6), M(["#d1432f", "#e6c24a", "#f4efe6"][k % 3], 0.4)); hd.position.y = 0.0165; pn.add(sh, hd); pn.position.set(r * 1.2 * Math.sin(a), y, r * 0.74 * Math.cos(a)); pn.rotation.set(1.35, a * 0.5, -a * 0.6); torso.add(pn); }
  g.add(torso);
  // the stand: a turned pole with rings, a brass adjuster, a hub and three bevelled legs on casters
  const pole = [[0.017, 0], [0.017, 0.12], [0.022, 0.125], [0.022, 0.14], [0.017, 0.145], [0.017, 0.40], [0.020, 0.405], [0.020, 0.42], [0.017, 0.425], [0.017, 0.82], [0.001, 0.82]];
  add(g, new THREE.LatheGeometry(pole.map((p) => new THREE.Vector2(p[0], p[1])), 20), wood, 0, 0.05, 0); add(g, new THREE.CylinderGeometry(0.03, 0.03, 0.07, 20), brass, 0, 0.58, 0); add(g, new THREE.CylinderGeometry(0.036, 0.036, 0.012, 20), brass, 0, 0.625, 0);
  const wing = add(g, new THREE.BoxGeometry(0.05, 0.012, 0.012), brass, 0.04, 0.58, 0); wing.rotation.z = 0.0;
  add(g, new THREE.CylinderGeometry(0.075, 0.09, 0.05, 6), wood, 0, 0.055, 0); add(g, new THREE.CylinderGeometry(0.03, 0.03, 0.008, 18), brass, 0, 0.082, 0);
  const lg2 = new THREE.Shape(); lg2.moveTo(0, -0.022); lg2.lineTo(0.30, -0.016); lg2.quadraticCurveTo(0.335, 0, 0.30, 0.016); lg2.lineTo(0, 0.022); lg2.closePath();
  for (let i = 0; i < 3; i++) { const a = i * Math.PI * 2 / 3 + 0.5, leg = new THREE.Group(); leg.rotation.y = -a;
    const lm = new THREE.Mesh(new THREE.ExtrudeGeometry(lg2, { depth: 0.034, bevelEnabled: true, bevelThickness: 0.004, bevelSize: 0.004, bevelSegments: 3, curveSegments: 8 }), wood); lm.rotation.x = Math.PI / 2; lm.position.set(0.04, 0.054, 0.0); lm.rotation.set(Math.PI / 2, 0, 0); lm.position.y = 0.05; lm.position.z = 0.017; leg.add(lm);
    const cs = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, 0.014, 14), M("#1a1714", 0.7)); cs.position.set(0.32, 0.01, 0); leg.add(cs); const cw = new THREE.Mesh(new THREE.CylinderGeometry(0.007, 0.007, 0.034, 12), brass); cw.rotation.x = Math.PI / 2; cw.position.set(0.32, 0.02, 0); leg.add(cw);
    const fork = new THREE.Mesh(new THREE.BoxGeometry(0.026, 0.026, 0.036), brass); fork.position.set(0.32, 0.035, 0); leg.add(fork); const wh = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, 0.01, 14), M("#1a1714", 0.7)); wh.rotation.x = Math.PI / 2; wh.position.set(0.32, 0.012, 0); leg.add(wh);
    g.add(leg); }
  return g;
}

// ---------- small things for the tables
function cuttingMat(o) {                                  // size [w, d]: a green self-healing mat with a white grid and numbers
  const [w, d] = o.size, g = new THREE.Group(), t = canvasTex(2048, Math.round(2048 * d / w), (x, W, H) => {
    x.fillStyle = "#2c5a43"; x.fillRect(0, 0, W, H); x.strokeStyle = "rgba(255,255,255,.55)"; x.fillStyle = "rgba(255,255,255,.75)"; x.font = "600 38px Inter, sans-serif";
    const nx = Math.round(w / 0.025), ny = Math.round(d / 0.025);
    for (let i = 0; i <= nx; i++) { x.lineWidth = i % 4 === 0 ? 3 : 1; x.beginPath(); x.moveTo(i * W / nx, 0); x.lineTo(i * W / nx, H); x.stroke(); if (i % 4 === 0 && i > 0 && i < nx) x.fillText(String(i * 2.5 | 0), i * W / nx + 6, 44); }
    for (let j = 0; j <= ny; j++) { x.lineWidth = j % 4 === 0 ? 3 : 1; x.beginPath(); x.moveTo(0, j * H / ny); x.lineTo(W, j * H / ny); x.stroke(); }
    x.strokeStyle = "rgba(255,255,255,.4)"; x.lineWidth = 2; for (let a = 15; a <= 75; a += 15) { x.beginPath(); x.moveTo(0, H); x.lineTo(W, H - Math.tan(a * Math.PI / 180) * W * 0.5); x.stroke(); }
    x.fillStyle = "rgba(255,255,255,.55)"; x.font = "italic 600 54px 'Playfair Display', Georgia, serif"; x.fillText("Inverso · taglio", W * 0.64, H * 0.94);
  });
  const m = add(g, new THREE.BoxGeometry(w, 0.004, d), new THREE.MeshStandardMaterial({ map: t, roughness: 0.55 }), 0, 0.002, 0); return g;
}
function buttonJar(o) {
  const g = new THREE.Group(), glass = new THREE.MeshPhysicalMaterial({ color: 0xeaf2f0, roughness: 0.05, metalness: 0, transparent: true, opacity: 0.28, side: THREE.DoubleSide }), n = 90, pal = ["#2f3a2e", "#8a4b2d", "#efe9dd", "#c9a24a", "#3b4f6b", "#1e1b18", "#7a2f2f"];
  const im = new THREE.InstancedMesh(new THREE.CylinderGeometry(0.0085, 0.0085, 0.0026, 14), M("#ffffff", 0.4), n), mx = new THREE.Matrix4(), q = new THREE.Quaternion(), P = new THREE.Vector3(), S = new THREE.Vector3(1, 1, 1), C = new THREE.Color();
  for (let i = 0; i < n; i++) { const a = hash2(i, 1) * 6.28, r = Math.sqrt(hash2(i, 2)) * 0.034, y = 0.01 + hash2(i, 3) * 0.075 * (1 - 0.25 * r / 0.034); P.set(Math.cos(a) * r, y, Math.sin(a) * r); q.setFromEuler(new THREE.Euler(hash2(i, 4) * 3, hash2(i, 5) * 6, hash2(i, 6) * 3)); mx.compose(P, q, S); im.setMatrixAt(i, mx); im.setColorAt(i, C.set(pal[Math.floor(hash2(i, 7) * pal.length)])); }
  g.add(im); const jar = add(g, new THREE.CylinderGeometry(0.044, 0.044, 0.11, 28, 1, true), glass, 0, 0.055, 0); jar.userData.noshadow = true; add(g, new THREE.CylinderGeometry(0.044, 0.044, 0.004, 28), glass, 0, 0.002, 0).userData.noshadow = true;
  add(g, new THREE.CylinderGeometry(0.046, 0.046, 0.016, 28), M("#c9a24a", 0.35, 0.8), 0, 0.118, 0); return g;
}
function pincushion(o) {
  const g = new THREE.Group(); const lat = new THREE.LatheGeometry([[0.001, 0], [0.034, 0.002], [0.040, 0.012], [0.034, 0.026], [0.012, 0.032], [0.001, 0.03]].map((p) => new THREE.Vector2(p[0], p[1])), 24);
  add(g, lat, clothMat("#b8342a", "plain", { n: 0.7, side: THREE.DoubleSide }), 0, 0, 0);
  for (let k = 0; k < 26; k++) { const a = hash2(k, 1) * 6.28, r = Math.sqrt(hash2(k, 2)) * 0.03, pn = new THREE.Group(), sh = new THREE.Mesh(new THREE.CylinderGeometry(0.0006, 0.0006, 0.03, 5), CHROME()), hd = new THREE.Mesh(new THREE.SphereGeometry(0.0021, 8, 6), M(["#d1432f", "#e6c24a", "#f4efe6", "#3b4f6b"][k % 4], 0.4)); hd.position.y = 0.0165; pn.add(sh, hd); pn.position.set(Math.cos(a) * r, 0.028, Math.sin(a) * r); pn.rotation.set(Math.sin(a) * 0.6, 0, -Math.cos(a) * 0.6); g.add(pn); }
  return g;
}
function spoolLying(o) {                                  // a wooden spool of thread, standing on y = 0 on its side
  const g = new THREE.Group(), r = 0.014, lat = new THREE.LatheGeometry([[0.004, 0], [r, 0], [r, 0.003], [0.0072, 0.004], [0.0072, 0.032], [r, 0.033], [r, 0.036], [0.004, 0.036]].map((p) => new THREE.Vector2(p[0], p[1])), 20);
  add(g, lat, M("#c9a46a", 0.6), 0, 0, 0); add(g, new THREE.CylinderGeometry(0.0125, 0.0125, 0.028, 20), clothMat(o.color || "#8a4b2d", "plain", { n: 0.5 }), 0, 0.018, 0); g.rotation.z = Math.PI / 2; g.position.y = 0.014; const w = new THREE.Group(); w.add(g); return w;
}


// ---------- a croquis that draws itself: strokes revealed over [t0, t1] (plate seconds), a 3D pencil riding the tip
const SKETCH = (() => {
  const L = [];
  const poly = (...p) => L.push(p);
  poly([0.30, 0.08], [0.70, 0.08], [0.71, 0.15], [0.73, 0.92], [0.535, 0.92], [0.50, 0.58], [0.465, 0.92], [0.27, 0.92], [0.29, 0.15], [0.30, 0.08]);
  poly([0.29, 0.15], [0.71, 0.15]);
  for (const s of [-1, 1]) { poly([0.5 + s * 0.09, 0.15], [0.5 + s * 0.085, 0.28]); poly([0.5 + s * 0.13, 0.15], [0.5 + s * 0.125, 0.27]); poly([0.5 + s * 0.20, 0.17], [0.5 + s * 0.18, 0.23], [0.5 + s * 0.16, 0.30]); }
  poly([0.40, 0.32], [0.40, 0.91]); poly([0.60, 0.32], [0.60, 0.91]);
  poly([0.27, 0.90], [0.535, 0.90]);
  return L;
})();
function sketchReveal(o) {
  const [w, d] = o.size, [t0, t1] = o.reveal, W = 1536, H = Math.round(W * d / w), g = new THREE.Group();
  const base = document.createElement("canvas"); base.width = W; base.height = H; const bx = base.getContext("2d");
  bx.fillStyle = "#f3ede0"; bx.fillRect(0, 0, W, H); bx.strokeStyle = "rgba(30,27,24,.10)"; bx.lineWidth = 1; for (let i = 0; i < W; i += 48) { bx.beginPath(); bx.moveTo(i, 0); bx.lineTo(i, H); bx.stroke(); } for (let j = 0; j < H; j += 48) { bx.beginPath(); bx.moveTo(0, j); bx.lineTo(W, j); bx.stroke(); }
  const cvs = document.createElement("canvas"); cvs.width = W; cvs.height = H; const cx = cvs.getContext("2d"), tx = new THREE.CanvasTexture(cvs); tx.colorSpace = THREE.SRGBColorSpace; tx.anisotropy = 16;
  const pts = SKETCH.map((pl) => pl.map((p) => [p[0] * W, p[1] * H])), lens = pts.map((pl) => { let s = 0; for (let i = 1; i < pl.length; i++) s += Math.hypot(pl[i][0] - pl[i - 1][0], pl[i][1] - pl[i - 1][1]); return s; }), total = lens.reduce((a, b) => a + b, 0);
  const mesh = new THREE.Mesh(new THREE.PlaneGeometry(w, d), new THREE.MeshStandardMaterial({ map: tx, roughness: 0.9 })); mesh.rotation.x = -Math.PI / 2; mesh.position.y = 0.002; g.add(mesh);
  const pen = new THREE.Group(), body = new THREE.Mesh(new THREE.CylinderGeometry(0.0042, 0.0042, 0.15, 6), M("#e0a82e", 0.5)); body.position.y = 0.083; pen.add(body);
  const cone = new THREE.Mesh(new THREE.CylinderGeometry(0.0042, 0.0008, 0.016, 6), M("#d9b98a", 0.7)); cone.position.y = 0.0075; pen.add(cone);
  const lead = new THREE.Mesh(new THREE.CylinderGeometry(0.0009, 0.0003, 0.004, 6), M("#1e1b18", 0.4)); lead.position.y = 0.0015; pen.add(lead);
  const era = new THREE.Mesh(new THREE.CylinderGeometry(0.0044, 0.0044, 0.012, 6), M("#c9503a", 0.7)); era.position.y = 0.164; pen.add(era);
  pen.rotation.set(-0.9, 0.25, 0.1); g.add(pen); let last = -1;
  const draw = (p) => {
    cx.drawImage(base, 0, 0); cx.strokeStyle = "#2a2623"; cx.lineWidth = 6; cx.lineCap = "round"; cx.lineJoin = "round"; let left = p * total, tip = pts[0][0];
    for (let k = 0; k < pts.length && left > 0; k++) {
      const pl = pts[k]; cx.beginPath(); cx.moveTo(pl[0][0], pl[0][1]); tip = pl[0];
      for (let i = 1; i < pl.length && left > 0; i++) { const a = pl[i - 1], b = pl[i], sl = Math.hypot(b[0] - a[0], b[1] - a[1]), f = Math.min(1, left / sl); tip = [a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f]; cx.lineTo(tip[0], tip[1]); left -= sl; }
      cx.stroke();
    }
    if (p >= 1) { cx.fillStyle = "#8a4b2d"; cx.font = "italic 500 92px 'Playfair Display', Georgia, serif"; cx.fillText("Drop 1", W * 0.06, H * 0.07); cx.fillStyle = "#1e1b18"; cx.font = "500 40px Inter, sans-serif"; cx.fillText("vita alta · doppia piega", W * 0.06, H * 0.115); }
    tx.needsUpdate = true; return tip;
  };
  g.userData.update = (t) => {
    const p = Math.max(0, Math.min(1, (t - t0) / (t1 - t0))), q = Math.round(p * 600);
    if (q !== last) { last = q; const tip = draw(q / 600); pen.position.set((tip[0] / W - 0.5) * w, 0.002, (tip[1] / H - 0.5) * d); }
    pen.visible = p > 0 && p < 1;
  };
  g.userData.update(-1); return g;
}
function hoop(o) {                                         // a flat measuring-tape ring round something: size [rx, rz]; stands in the XZ plane at its local y = 0
  const [rx, rz] = o.size, g = new THREE.Group(), [c, x] = (() => { const cc = document.createElement("canvas"); cc.width = 1024; cc.height = 32; return [cc, cc.getContext("2d")]; })();
  x.fillStyle = "#f0c93a"; x.fillRect(0, 0, 1024, 32); x.fillStyle = "#1e1b18"; for (let i = 0; i < 100; i++) x.fillRect(i * 10.24, 0, 2, i % 5 === 0 ? 18 : 9);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.wrapS = THREE.RepeatWrapping; t.repeat.set(2, 1);
  const geo = new THREE.CylinderGeometry(1, 1, 0.016, 96, 1, true), m = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({ map: t, roughness: 0.55, side: THREE.DoubleSide })); m.scale.set(rx, 1, rz); g.add(m); return g;
}

export function buildProp(o) {
  switch (o.type) {
    case "sewing": return sewing(o);
    case "sketchdraw": return sketchReveal(o);
    case "mannequin": return mannequin(o);
    case "cuttingmat": return cuttingMat(o);
    case "buttonjar": return buttonJar(o);
    case "pincushion": return pincushion(o);
    case "spool": return spoolLying(o);
    case "hoop": return hoop(o);
    default: return buildCut(o);
  }
}
export const PROPS = new Set(["sewing", "mannequin", "cuttingmat", "buttonjar", "pincushion", "spool", "hoop", "sketchdraw", ...CUTPROPS]);
