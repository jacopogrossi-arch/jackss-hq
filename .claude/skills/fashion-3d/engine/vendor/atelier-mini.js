// atelier-mini.js (17/11/2026): "mini-me", a toy-figure (Lego-like) Jacopo: round glasses, swept-up brown hair with a quiff, black tee, indigo selvage jeans with a red selvage line, Texan boots.
// Made to RESEMBLE him (Jacopo's note of 17/11: not three solids stacked, not a cardboard cut-out). Bevelled boxes and extrusions instead of spheres; a painted face (eyes, brows, a mouth that opens while he talks, blinks).
// build: buildMini(o) -> THREE.Group standing on y = 0, facing +z. o: size[0] = height in metres (default 0.5), talk = [[t0,t1],...] (plate seconds: mouth + head + right hand move), glasses (default true).
import * as THREE from "./three.module.min.js";
import { RoundedBoxGeometry } from "./RoundedBoxGeometry.js";

export const MINI = new Set(["minime"]);
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const hash = (n) => { const s = Math.sin(n * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
const plastic = (c, r = 0.5, cc = 0.35) => new THREE.MeshPhysicalMaterial({ color: c, roughness: r, metalness: 0, clearcoat: cc, clearcoatRoughness: 0.35 });
const mesh = (geo, mat, x = 0, y = 0, z = 0) => { const m = new THREE.Mesh(geo, mat); m.position.set(x, y, z); m.castShadow = true; m.receiveShadow = true; return m; };
const rbox = (w, h, d, r = 0.006) => new RoundedBoxGeometry(w, h, d, 3, r);
const inAny = (t, L) => { for (const [a, b] of L || []) if (t >= a && t <= b) return [a, b]; return null; };

// ---- the painted face (canvas): variants = [eyes open|closed] x [mouth closed|open]
function faceTexture(eyesClosed, mouthOpen) {
  const W = 768, H = 512, c = document.createElement("canvas"); c.width = W; c.height = H; const g = c.getContext("2d");
  const grad = g.createLinearGradient(0, 0, 0, H); grad.addColorStop(0, "#e6b790"); grad.addColorStop(1, "#d9a37d"); g.fillStyle = grad; g.fillRect(0, 0, W, H);
  // face x (metres from the centre) -> canvas x. arc = 150 deg on r = 0.05
  const R = 0.05, ARC = (150 * Math.PI) / 180, X = (m) => (0.5 + Math.asin(Math.max(-0.99, Math.min(0.99, m / R))) / ARC) * W, Y = (m) => (0.5 - m / 0.085) * H;
  // light stubble on the jaw and upper lip
  g.fillStyle = "rgba(70,50,38,0.12)"; for (let i = 0; i < 1400; i++) { const x = Math.random() * W, y = H * (0.62 + Math.random() * 0.38); const k = Math.abs(x / W - 0.5) * 2; if (y > H * (0.78 - 0.1 * (1 - k)) || (y > H * 0.66 && Math.abs(x - W / 2) < W * 0.12)) g.fillRect(x, y, 3, 3); }
  g.fillStyle = "rgba(210,110,100,0.18)"; for (const sd of [-1, 1]) { g.beginPath(); g.ellipse(X(sd * 0.032), Y(-0.012), 46, 30, 0, 0, 7); g.fill(); }            // cheeks
  for (const sd of [-1, 1]) {
    const ex = X(sd * 0.0215), ey = Y(0.006);
    // eyebrows: thick, slightly arched, dark brown
    g.strokeStyle = "#3d291b"; g.lineCap = "round"; g.lineWidth = 17; g.beginPath(); g.moveTo(ex - sd * 52, Y(0.0225) + 5); g.quadraticCurveTo(ex, Y(0.0275), ex + sd * 52, Y(0.0235) - 5); g.stroke();
    if (eyesClosed) { g.strokeStyle = "#3a2618"; g.lineWidth = 7; g.beginPath(); g.moveTo(ex - 28, ey + 4); g.quadraticCurveTo(ex, ey + 16, ex + 28, ey + 4); g.stroke(); continue; }
    g.fillStyle = "#fbf9f4"; g.beginPath(); g.ellipse(ex, ey, 31, 24, 0, 0, 7); g.fill();                                     // sclera
    g.fillStyle = "#6c8a58"; g.beginPath(); g.arc(ex + sd * 2, ey + 1, 17, 0, 7); g.fill();                                  // green iris
    g.fillStyle = "#1a2418"; g.beginPath(); g.arc(ex + sd * 2, ey + 1, 8, 0, 7); g.fill();                                    // pupil
    g.fillStyle = "#fff"; g.beginPath(); g.arc(ex + sd * 2 + 6, ey - 6, 4.2, 0, 7); g.fill();                                  // glint
    g.strokeStyle = "#3a2618"; g.lineWidth = 6; g.beginPath(); g.ellipse(ex, ey, 31, 24, 0, Math.PI * 1.06, Math.PI * 1.94); g.stroke();   // upper lid line
  }
  // mouth
  const mx = W / 2, my = Y(-0.0255);
  if (mouthOpen) { g.fillStyle = "#6a2a24"; g.beginPath(); g.ellipse(mx, my + 6, 36, 19, 0, 0, 7); g.fill(); g.fillStyle = "#f3efe6"; g.beginPath(); g.ellipse(mx, my - 6, 28, 7, 0, Math.PI, 0); g.fill(); g.fillStyle = "#c0605c"; g.beginPath(); g.ellipse(mx, my + 14, 17, 6, 0, 0, 7); g.fill(); }
  else { g.strokeStyle = "#8a3b30"; g.lineWidth = 8; g.lineCap = "round"; g.beginPath(); g.moveTo(mx - 38, my - 2); g.quadraticCurveTo(mx, my + 20, mx + 38, my - 2); g.stroke(); }
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; return t;
}

export function buildMini(o) {
  const g = new THREE.Group(), s = ((o.size && o.size[0]) || 0.5) / 0.5, body = new THREE.Group(); g.add(body);
  const SKIN = plastic("#dfa97f", 0.55, 0.25), TEE = plastic("#1b1a19", 0.6, 0.3), JEAN = plastic("#2b3c66", 0.7, 0.2), BOOT = plastic("#4a2f1d", 0.4, 0.5), SOLE = plastic("#171311", 0.6, 0.2);
  const HAIR = plastic("#47301f", 0.7, 0.12), HAIR2 = plastic("#5c3d28", 0.7, 0.12), HAIR3 = plastic("#3a2517", 0.75, 0.1), BELT = plastic("#2d1f15", 0.5, 0.4), SILVER = new THREE.MeshStandardMaterial({ color: "#cfd3da", roughness: 0.25, metalness: 0.9 });
  // ---- boots: a real side profile (shaft, instep, a pointed toe, a stacked heel), extruded across the width
  const bootGeo = (() => {
    const p = new THREE.Shape();
    p.moveTo(-0.026, 0.0); p.lineTo(-0.026, 0.016); p.lineTo(-0.016, 0.016); p.lineTo(-0.012, 0.0); p.lineTo(0.03, 0.0);      // heel stack and sole
    p.quadraticCurveTo(0.062, 0.0, 0.066, 0.011); p.quadraticCurveTo(0.066, 0.02, 0.046, 0.026);                                     // pointed toe
    p.lineTo(0.022, 0.034); p.lineTo(0.02, 0.07); p.lineTo(-0.026, 0.07); p.lineTo(-0.026, 0.0);
    const e = new THREE.ExtrudeGeometry(p, { depth: 0.034, bevelEnabled: true, bevelSize: 0.004, bevelThickness: 0.004, bevelSegments: 3, curveSegments: 10 }); e.translate(0, 0, -0.017); e.rotateY(-Math.PI / 2); return e;
  })();
  const mkLeg = (side) => {
    const pv = new THREE.Group(); pv.position.set(side * 0.026, 0.225, 0); body.add(pv);
    pv.add(mesh(rbox(0.046, 0.15, 0.052, 0.008), JEAN, 0, -0.075, 0));
    const sel = mesh(new THREE.BoxGeometry(0.0022, 0.146, 0.0022), plastic("#b8432a", 0.6, 0.1), side * 0.0232, -0.075, 0.012); pv.add(sel);   // red selvage line on the outer seam
    pv.add(mesh(rbox(0.05, 0.012, 0.056, 0.005), JEAN, 0, -0.146, 0));                                                              // the hem, a bit wider (boot cut)
    const boot = mesh(bootGeo, BOOT, 0, -0.225, 0.0); boot.position.y = -0.225; pv.add(boot);
    pv.add(mesh(new THREE.BoxGeometry(0.036, 0.004, 0.088), SOLE, 0, -0.2235, 0.008));
    return pv;
  };
  const legL = mkLeg(-1), legR = mkLeg(1);
  // ---- hips + belt
  body.add(mesh(rbox(0.1, 0.034, 0.056, 0.008), JEAN, 0, 0.234, 0));
  body.add(mesh(rbox(0.104, 0.011, 0.059, 0.004), BELT, 0, 0.245, 0));
  body.add(mesh(rbox(0.016, 0.012, 0.004, 0.002), SILVER, 0, 0.245, 0.0305));
  // ---- torso: a trapezoid (shoulders wider than the waist), black tee, a round collar
  const tshape = new THREE.Shape(); tshape.moveTo(-0.05, 0); tshape.lineTo(0.05, 0); tshape.lineTo(0.062, 0.115); tshape.quadraticCurveTo(0.062, 0.125, 0.052, 0.125); tshape.lineTo(-0.052, 0.125); tshape.quadraticCurveTo(-0.062, 0.125, -0.062, 0.115); tshape.lineTo(-0.05, 0);
  const tg = new THREE.ExtrudeGeometry(tshape, { depth: 0.04, bevelEnabled: true, bevelSize: 0.006, bevelThickness: 0.006, bevelSegments: 4 }); tg.translate(0, 0, -0.02);
  body.add(mesh(tg, TEE, 0, 0.25, 0));
  const collar = mesh(new THREE.TorusGeometry(0.02, 0.0045, 10, 28), plastic("#262524", 0.6, 0.3), 0, 0.376, 0.004); collar.rotation.x = Math.PI / 2 - 0.2; body.add(collar);
  body.add(mesh(new THREE.CylinderGeometry(0.0155, 0.0175, 0.022, 20), SKIN, 0, 0.388, 0));                                           // neck
  // ---- arms (pivot at the shoulder): tee sleeve, skin forearm, a hand
  const mkArm = (side) => {
    const pv = new THREE.Group(); pv.position.set(side * 0.0745, 0.366, 0); body.add(pv);
    pv.add(mesh(rbox(0.03, 0.052, 0.034, 0.01), TEE, 0, -0.022, 0));
    pv.add(mesh(rbox(0.024, 0.058, 0.026, 0.009), SKIN, 0, -0.07, 0));
    pv.add(mesh(rbox(0.031, 0.03, 0.028, 0.012), SKIN, 0, -0.115, 0.002));
    pv.rotation.z = side * 0.1; return pv;
  };
  const armL = mkArm(-1), armR = mkArm(1);
  // ---- head: a toy-brick cylinder with rounded edges, a painted face, ears, a nose
  const head = new THREE.Group(); head.position.set(0, 0.445, 0); body.add(head);
  const lathe = (() => { const pts = [], hh = 0.0435, r = 0.05, f = 0.012, rb = 0.0455; pts.push(new THREE.Vector2(0, -hh)); for (let i = 0; i <= 6; i++) { const a = -Math.PI / 2 + (i / 6) * (Math.PI / 2); pts.push(new THREE.Vector2(rb - f + Math.cos(a) * f, -hh + f + Math.sin(a) * f)); } for (let i = 0; i <= 6; i++) { const a = (i / 6) * (Math.PI / 2); pts.push(new THREE.Vector2(r - f + Math.cos(a) * f, hh - f + Math.sin(a) * f)); } pts.push(new THREE.Vector2(0, hh)); return new THREE.LatheGeometry(pts, 56); })();
  head.add(mesh(lathe, SKIN));
  const faceMats = {}; const fm = (ec, mo) => { const k = (ec ? 1 : 0) + (mo ? 2 : 0); if (!faceMats[k]) faceMats[k] = faceTexture(ec, mo); return faceMats[k]; };
  const faceMat = new THREE.MeshPhysicalMaterial({ map: fm(false, false), roughness: 0.55, clearcoat: 0.2, polygonOffset: true, polygonOffsetFactor: -2, polygonOffsetUnits: -2 });
  const ARC = (150 * Math.PI) / 180, face = new THREE.Mesh(new THREE.CylinderGeometry(0.0504, 0.0504, 0.0852, 56, 1, true, -ARC / 2, ARC), faceMat); face.castShadow = false; head.add(face);
  for (const sd of [-1, 1]) head.add(mesh(rbox(0.01, 0.022, 0.016, 0.004), SKIN, sd * 0.0505, -0.002, -0.004));                      // ears
  head.add(mesh(rbox(0.012, 0.016, 0.012, 0.005), plastic("#d49a72", 0.55, 0.2), 0, -0.007, 0.0525));                                // nose
  // ---- glasses: round frames, a bridge, temples to the ears, faint lenses
  if (o.glasses !== false) {
    const FR = plastic("#121212", 0.35, 0.6);
    const ring = new THREE.Shape(); ring.absarc(0, 0, 0.0158, 0, Math.PI * 2, false); const hole = new THREE.Path(); hole.absarc(0, 0, 0.0136, 0, Math.PI * 2, true); ring.holes.push(hole);
    const rg = new THREE.ExtrudeGeometry(ring, { depth: 0.004, bevelEnabled: true, bevelSize: 0.0006, bevelThickness: 0.0006, bevelSegments: 2, curveSegments: 28 });
    for (const sd of [-1, 1]) {
      head.add(mesh(rg, FR, sd * 0.0215, 0.006, 0.0516));
      const lens = new THREE.Mesh(new THREE.CircleGeometry(0.0136, 28), new THREE.MeshPhysicalMaterial({ color: "#cfe4ff", roughness: 0.05, transparent: true, opacity: 0.13, depthWrite: false })); lens.position.set(sd * 0.0215, 0.006, 0.0538); head.add(lens);
      const tp = mesh(new THREE.BoxGeometry(0.0022, 0.0026, 0.05), FR, sd * 0.0412, 0.0085, 0.0285); tp.rotation.y = sd * -0.1; head.add(tp);        // temple arm back to the ear
    }
    head.add(mesh(new THREE.BoxGeometry(0.01, 0.0026, 0.003), FR, 0, 0.0095, 0.0535));                                                // bridge
  }
  // ---- hair: a dome above the eyebrows, a shell round the back and sides, and a combed-up quiff of tapered locks (straight, standing up, fanned from the hairline back)
  const HAIRDS = new THREE.MeshPhysicalMaterial({ color: "#3d2718", roughness: 0.75, clearcoat: 0.1, side: THREE.DoubleSide });
  const cap = mesh(new THREE.SphereGeometry(0.0535, 48, 28, 0, Math.PI * 2, 0, Math.PI * 0.5), HAIR, 0, 0.034, -0.002); cap.scale.set(1.0, 0.85, 1.04); head.add(cap);
  const shell = mesh(new THREE.CylinderGeometry(0.0516, 0.0478, 0.058, 44, 1, true, ARC / 2, Math.PI * 2 - ARC), HAIRDS, 0, 0.005, 0); head.add(shell);        // back and sides, down to the nape
  const lock = (len, r, mat) => { const pts = [new THREE.Vector2(r, -len / 2), new THREE.Vector2(r * 0.96, -len * 0.2), new THREE.Vector2(r * 0.78, len * 0.12), new THREE.Vector2(r * 0.45, len * 0.34), new THREE.Vector2(r * 0.15, len * 0.47), new THREE.Vector2(0, len / 2)]; return new THREE.Mesh(new THREE.LatheGeometry(pts, 10), mat); };
  const rows = [{ z: 0.034, y: 0.058, n: 7, spread: 0.034, len: 0.034, r: 0.0088, tilt: 1.0 }, { z: 0.016, y: 0.07, n: 7, spread: 0.04, len: 0.044, r: 0.0098, tilt: 0.7 }, { z: -0.004, y: 0.073, n: 6, spread: 0.038, len: 0.042, r: 0.0098, tilt: 0.42 }, { z: -0.024, y: 0.064, n: 5, spread: 0.032, len: 0.034, r: 0.0098, tilt: 0.12 }];
  let li = 0;
  for (const rw of rows) for (let i = 0; i < rw.n; i++, li++) {
    const u = rw.n === 1 ? 0 : (i / (rw.n - 1)) * 2 - 1, mat = li % 3 === 0 ? HAIR2 : li % 3 === 1 ? HAIR : HAIR3, m = lock(rw.len * (0.9 + 0.2 * hash(li)), rw.r, mat);
    m.castShadow = true; m.receiveShadow = true; m.position.set(u * rw.spread, rw.y + 0.004 * hash(li + 5), rw.z - 0.003 * Math.abs(u));
    m.rotation.x = rw.tilt + 0.12 * (hash(li + 9) - 0.5); m.rotation.z = -u * 0.28; head.add(m);
  }
  g.scale.setScalar(s);
  // ---- life, a pure function of t: breathing, blinking, and while he talks the mouth opens and shuts, the head nods and the right hand gestures
  g.userData.update = (t) => {
    const tk = inAny(t, o.talk); let bob = 0.0025 * Math.sin(t * 2.4), nod = 0, mouth = false, arm = 0;
    if (tk) { const k = Math.min(clamp((t - tk[0]) / 0.18), clamp((tk[1] - t) / 0.18)); mouth = Math.sin(t * 26) > -0.15; nod = k * 0.05 * Math.sin(t * 7.5); arm = k * (0.35 + 0.35 * Math.sin(t * 4.3)); bob += k * 0.0025 * Math.abs(Math.sin(t * 7.5)); }
    const ph = (t + 0.9 * hash(Math.floor(t / 3.1))) % 3.1, blink = ph < 0.13;
    faceMat.map = fm(blink, mouth);
    body.position.y = bob; head.rotation.x = nod; head.rotation.y = 0.1 * Math.sin(t * 0.8) + (tk ? 0.08 * Math.sin(t * 3.1) : 0);
    armR.rotation.z = 0.1 + arm * 0.6; armR.rotation.x = -arm * 0.9; armL.rotation.z = -0.1; armL.rotation.x = 0.04 * Math.sin(t * 1.3);
  };
  g.userData.update(0);
  return g;
}
