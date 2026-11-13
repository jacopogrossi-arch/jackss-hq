// atelier-trouser.js: the high-detail trouser (14/11/2026). Two real legs that grow into the hips (no "skirt"), a waistband, pleats, slanted side pockets,
// back welt pockets with buttons, belt loops, fly, side adjusters, real top-stitching, turn-ups, and a hanger with a CLOSED hook and a cord.
// Metres, hem at y = 0, waist top at y = 1.08, front = +z. Used by atelier-kit.js (o.hi) .
import * as THREE from "./three.module.min.js";
import { pchip, smooth, groove, lerp, clamp, shade, clothMat, loftGeo, stitches, tube } from "./atelier-tex.js";

const Y = [0, 0.10, 0.5, 0.72, 0.80, 0.86, 0.92, 1.02, 1.06];
const CX = pchip(Y, [0.112, 0.113, 0.112, 0.105, 0.095, 0.080, 0.066, 0.048, 0.044]);
const RX = pchip(Y, [0.094, 0.095, 0.101, 0.100, 0.097, 0.115, 0.128, 0.126, 0.124]);
const RZ = pchip(Y, [0.097, 0.098, 0.106, 0.118, 0.130, 0.131, 0.130, 0.116, 0.112]);
const pl = (a, at, w) => (a > at ? Math.exp(-Math.pow((a - at) / 0.03, 2)) : Math.exp(-Math.pow((a - at) / w, 2)));   // a fold: sharp on the crease side, soft on the other
function relief(a, y) {
  let r = 0;
  r += 0.0035 * (groove(a, 0, 0.06) + 0.7 * groove(a, Math.PI, 0.06)) * clamp((0.80 - y) / 0.1) * (y > 0.03 ? 1 : 0.5);              // pressed crease, front and back
  const fp = 0.0155 * smooth((y - 0.80) / 0.1) * (1 - smooth((y - 1.0) / 0.03)) + 0.003 * smooth((y - 0.55) / 0.25) * (1 - smooth((y - 1.0) / 0.03));
  r += fp * (pl(a, -0.30, 0.12) + pl(a, -0.66, 0.12));                                                                              // double pleat, towards the fly
  r += 0.0022 * Math.sin(a * 3 + y * 70 + 1.3) * Math.exp(-Math.pow((y - 0.52) / 0.1, 2)) * groove(a, 0, 1.1);                      // knee creases
  r += 0.002 * Math.sin(a * 4 - y * 65) * Math.exp(-Math.pow((y - 0.5) / 0.08, 2)) * groove(a, Math.PI, 1.0);
  r += 0.0035 * Math.max(0, Math.sin(a * 5 + 1.7)) * Math.exp(-Math.pow((y - 0.74) / 0.07, 2)) * groove(a, 0, 1.3);                  // fan of folds under the crotch
  r += 0.0045 * groove(a, 0, 0.7) * smooth((0.10 - y) / 0.10);                                                                       // the break over the shoe
  r += 0.008 * groove(a, Math.PI, 0.9) * smooth((y - 0.80) / 0.1) * (1 - smooth((y - 1.0) / 0.03));                                  // the seat
  return r;
}
const legPoint = (s, y, a, off = 0) => { const r = relief(a, y) + off; return [s * (CX(y) + (RX(y) + r) * Math.sin(a)), y, (RZ(y) + r) * Math.cos(a) - 0.004 * smooth((y - 0.8) / 0.2)]; };
const legNormal = (s, y, a) => { const nx = Math.sin(a) / RX(y), nz = Math.cos(a) / RZ(y), l = Math.hypot(nx, nz); return [s * nx / l, nz / l]; };

export function trouserHi(o) {
  const color = o.color || "#6f7452", toile = !!o.toile, kind = toile ? "plain" : "twill";
  const cloth = clothMat(color, kind), dark = clothMat(shade(color, 0.8), kind), body = new THREE.Group(), g = new THREE.Group(); body.add(g);
  const thread = toile ? "#d8cdb2" : new THREE.Color(color).lerp(new THREE.Color("#efe3c4"), 0.55).getStyle();
  const gold = new THREE.MeshStandardMaterial({ color: 0xe3c47f, roughness: 0.32, metalness: 0.95 }), horn = new THREE.MeshStandardMaterial({ color: 0x2b2118, roughness: 0.35, metalness: 0.1 });
  const seamM = clothMat(shade(color, 0.72), kind);
  // --- the two legs
  for (const s of [-1, 1]) {
    const f = (y, a) => legPoint(s, y, a); f.rad = (y) => (RX(y) + RZ(y)) / 2;
    g.add(new THREE.Mesh(loftGeo(f, 0, 1.045, 160, 150, s < 0), cloth));
    const seamOuter = [], seamIn = [], hem = [], hem2 = [];
    for (let k = 0; k <= 40; k++) { const y = lerp(0.045, 1.0, k / 40); seamOuter.push(legPoint(s, y, Math.PI / 2, 0.0012)); seamIn.push(legPoint(s, y, -Math.PI / 2, 0.0012)); }
    g.add(tube(seamOuter, 0.0018, seamM, 60)); g.add(tube(seamIn.filter((_, i) => i < 26), 0.0016, seamM, 40));
    for (const sd of [-0.03, 0.03]) { const p = [], q = []; for (let k = 0; k <= 40; k++) { const y = lerp(0.045, 1.0, k / 40); p.push(legPoint(s, y, Math.PI / 2 + sd, 0.0014)); if (k < 26) q.push(legPoint(s, y, -Math.PI / 2 + sd, 0.0014)); } g.add(stitches(p, thread)); g.add(stitches(q, thread)); }
    for (let k = 0; k <= 72; k++) { const a = (k / 72) * Math.PI * 2; hem.push(legPoint(s, 0.040, a, 0.0014)); }
    g.add(stitches(hem, thread));                                                                                                      // hem stitching
    // turn-up (cuff): a slightly wider ring with a rolled fold and its own stitches
    const cuff = (y, a) => { const p = legPoint(s, 0.0, a, 0.004 + 0.0035 * Math.sin(Math.min(1, y / 0.045) * Math.PI)); return [p[0], y, p[2]]; }; cuff.rad = () => 0.1;
    g.add(new THREE.Mesh(loftGeo(cuff, 0.0, 0.046, 160, 10, s < 0), dark));
    const cs = []; for (let k = 0; k <= 72; k++) cs.push(legPoint(s, 0.0, (k / 72) * Math.PI * 2, 0.0075)), cs[cs.length - 1][1] = 0.032; g.add(stitches(cs.map((p) => [p[0], 0.032, p[2]]), thread, 0.007));
    // slanted side pocket: opening seam, lining lip, stitches
    const po = [], pi = [], ps = []; for (let k = 0; k <= 14; k++) { const u = k / 14, y = lerp(1.012, 0.86, Math.pow(u, 0.95)), a = lerp(1.30, 0.72, Math.pow(u, 1.15)); po.push(legPoint(s, y, a, 0.0018)); pi.push(legPoint(s, y, a - 0.035, 0.0012)); ps.push(legPoint(s, y, a - 0.07, 0.0013)); }
    g.add(tube(po, 0.0024, new THREE.MeshStandardMaterial({ color: toile ? "#e8e0cc" : shade(color, 0.62), roughness: 0.9 }), 40)); g.add(stitches(ps, thread, 0.0058)); g.add(tube(pi, 0.0012, seamM, 30));
    // back welt pocket: two welts, a button, stitches
    const bpA = Math.PI + s * 0.38;
    for (const yy of [0.968, 0.944]) {
      const c = legPoint(s, yy, bpA, 0.002), n = legNormal(s, yy, bpA), w = new THREE.Mesh(new THREE.BoxGeometry(0.105, 0.0095, 0.0045), seamM);
      w.position.set(c[0], c[1], c[2]); w.rotation.y = Math.atan2(n[0], n[1]); g.add(w);
      const pts = []; for (let k = 0; k <= 10; k++) pts.push(legPoint(s, yy - 0.0075, bpA + (k / 10 - 0.5) * 0.85 * (s < 0 ? -1 : 1) * (0.105 / 0.20), 0.0032)); g.add(stitches(pts, thread, 0.0052));
    }
    { const c = legPoint(s, 0.952, bpA, 0.0034), n = legNormal(s, 0.952, bpA), b = new THREE.Mesh(new THREE.CylinderGeometry(0.0066, 0.0066, 0.0028, 20), horn);
      b.position.set(c[0], c[1], c[2]); b.rotation.set(Math.PI / 2, 0, 0); const holder = new THREE.Group(); holder.position.copy(b.position); b.position.set(0, 0, 0); holder.rotation.y = Math.atan2(n[0], n[1]); holder.add(b);
      for (const [hx, hy] of [[-0.002, -0.002], [0.002, 0.002], [-0.002, 0.002], [0.002, -0.002]]) { const hole = new THREE.Mesh(new THREE.SphereGeometry(0.0007, 6, 4), new THREE.MeshBasicMaterial({ color: 0x0a0806 })); hole.position.set(hx, hy, 0.0016); holder.add(hole); }
      g.add(holder); }
  }
  // --- the waistband and its details
  const wb = (y, a) => { const e = smooth((y - 1.015) / 0.01) * (1 - smooth((y - 1.075) / 0.008)); const r = 0.003 * e; return [(0.175 + r) * Math.sin(a), y, (0.112 + r) * Math.cos(a)]; }; wb.rad = () => 0.14;
  g.add(new THREE.Mesh(loftGeo(wb, 1.012, 1.08, 160, 16), dark));
  for (const yy of [1.0215, 1.0735]) { const p = []; for (let k = 0; k <= 160; k++) { const a = (k / 160) * Math.PI * 2; p.push([(0.1785) * Math.sin(a), yy, (0.1155) * Math.cos(a)]); } g.add(stitches(p, thread, 0.0058)); }
  const wl = (hx, hy, hz, ry = 0) => { const m = new THREE.Mesh(new THREE.BoxGeometry(hx, hy, hz), dark); m.rotation.y = ry; return m; };
  for (const a of [-1.32, -0.88, -0.46, 0.46, 0.88, 1.32, Math.PI - 0.3, Math.PI + 0.3, Math.PI]) {                                       // belt loops
    const r = 0.001 + 1 / Math.sqrt(Math.sin(a) ** 2 / (0.1805 ** 2) + Math.cos(a) ** 2 / (0.1175 ** 2)), lp = wl(0.014, 0.058, 0.0055, a); lp.position.set(r * Math.sin(a), 1.047, r * Math.cos(a)); g.add(lp);
    const st = []; for (const yy of [1.02, 1.074]) st.push([r * Math.sin(a), yy, r * Math.cos(a)]); const sp = new THREE.Mesh(new THREE.SphereGeometry(0.0009, 5, 4), new THREE.MeshStandardMaterial({ color: thread })); sp.position.set(st[0][0], st[0][1], st[0][2] + 0.0035 * Math.cos(a)); g.add(sp);
  }
  { const tab = new THREE.Mesh(new THREE.BoxGeometry(0.052, 0.062, 0.0058), dark); tab.position.set(-0.024, 1.047, 0.1215); g.add(tab);       // the extension tab of the front closure, with its button
    const bt = new THREE.Mesh(new THREE.CylinderGeometry(0.0095, 0.0095, 0.004, 28), horn); bt.rotation.x = Math.PI / 2; bt.position.set(-0.036, 1.047, 0.1262); g.add(bt);
    const rim = new THREE.Mesh(new THREE.TorusGeometry(0.0072, 0.0009, 6, 22), new THREE.MeshStandardMaterial({ color: 0x120d09, roughness: 0.4 })); rim.position.copy(bt.position); rim.position.z += 0.0022; g.add(rim);
    for (const [hx, hy] of [[-0.0025, -0.0025], [0.0025, 0.0025], [-0.0025, 0.0025], [0.0025, -0.0025]]) { const hole = new THREE.Mesh(new THREE.SphereGeometry(0.0009, 6, 4), new THREE.MeshBasicMaterial({ color: 0x050302 })); hole.position.set(-0.036 + hx, 1.047 + hy, 0.1285); g.add(hole); } }
  // fly: a J of stitches and a seam line at the centre front
  { const fl = [], fs = []; for (let k = 0; k <= 22; k++) { const u = k / 22, y = lerp(1.012, 0.815, u), x = 0.024 * (1 - smooth((u - 0.55) / 0.45)); const a = Math.asin(clamp((x - CX(y)) / RX(y), -1, 1)); const p = legPoint(1, y, a, 0.0022); fl.push([x, y, p[2]]); const a2 = Math.asin(clamp((x + 0.007 - CX(y)) / RX(y), -1, 1)), p2 = legPoint(1, y, a2, 0.0022); fs.push([x + 0.007, y, p2[2]]); }
    g.add(tube(fl, 0.0016, seamM, 40)); g.add(stitches(fs, thread, 0.0055)); }
  // the side adjusters: a tab with a double-prong buckle on each side seam
  for (const s of [-1, 1]) {
    const tb = new THREE.Mesh(new THREE.BoxGeometry(0.008, 0.032, 0.085), dark); tb.position.set(s * 0.1815, 1.046, -0.012); g.add(tb);
    const bk = new THREE.Mesh(new THREE.BoxGeometry(0.0035, 0.036, 0.030), gold); bk.position.set(s * 0.1865, 1.047, 0.030); g.add(bk);
    for (const dz of [-0.008, 0.008]) { const slot = new THREE.Mesh(new THREE.BoxGeometry(0.004, 0.026, 0.0035), horn); slot.position.set(s * 0.1868, 1.047, 0.030 + dz); g.add(slot); }
    const bar = new THREE.Mesh(new THREE.CylinderGeometry(0.0022, 0.0022, 0.030, 8), gold); bar.rotation.x = Math.PI / 2; bar.position.set(s * 0.188, 1.032, 0.030); g.add(bar);
    for (let k = 0; k < 3; k++) { const e = new THREE.Mesh(new THREE.TorusGeometry(0.0035, 0.0009, 5, 12), horn); e.rotation.y = Math.PI / 2; e.position.set(s * 0.1865, 1.047, -0.008 - k * 0.016); g.add(e); }
  }
  if (toile) {                                                                                                                          // a toile is marked: chalk lines, basting threads, pins
    const chalk = new THREE.MeshStandardMaterial({ color: "#b9402c", roughness: 1 }), pencil = new THREE.MeshStandardMaterial({ color: "#59534a", roughness: 1 });
    for (const s of [-1, 1]) {
      const l1 = [], l2 = [], l3 = []; for (let k = 0; k <= 12; k++) { const u = k / 12; l1.push(legPoint(s, lerp(0.90, 0.80, u), lerp(0.2, 0.9, u) * 1, 0.0015)); l2.push(legPoint(s, 0.55, lerp(-0.7, 0.7, u), 0.0015)); l3.push(legPoint(s, lerp(0.2, 0.7, u), -0.45 * 1 + 0.0 * u, 0.0015)); }
      g.add(tube(l1, 0.0011, chalk, 20)); g.add(tube(l2, 0.0011, pencil, 20)); g.add(tube(l3, 0.0011, chalk, 20));
      const bs = []; for (let k = 0; k <= 30; k++) bs.push(legPoint(s, lerp(0.07, 0.98, k / 30), Math.PI / 2 + 0.07, 0.0016)); g.add(stitches(bs, "#b9402c", 0.014, 0.009, 0.0011));      // red basting along the side seam
    }
    for (let k = 0; k < 7; k++) { const a = -0.5 + k * 0.18, y = 0.88 + 0.015 * Math.sin(k * 2.1), p = legPoint(1, y, a, 0.0012), pin = new THREE.Group(), st = new THREE.Mesh(new THREE.CylinderGeometry(0.0006, 0.0006, 0.032, 5), new THREE.MeshStandardMaterial({ color: 0xd8dbe0, metalness: 0.9, roughness: 0.3 }));
      const hd = new THREE.Mesh(new THREE.SphereGeometry(0.0021, 8, 6), new THREE.MeshStandardMaterial({ color: ["#d1432f", "#e6c24a", "#2f8f6a"][k % 3], roughness: 0.4 })); hd.position.y = 0.017; pin.add(st); pin.add(hd);
      pin.position.set(p[0], p[1], p[2]); pin.rotation.set(1.2, 0, -0.3 + 0.1 * k); g.add(pin); }
  }
  // --- the hanger: shaped wooden body, two spring clips on the waistband, a neck, and a CLOSED eye that the cord is tied through
  if (o.hang != null) {
    const wood = new THREE.MeshStandardMaterial({ color: 0xa8743f, roughness: 0.42 }), steel = new THREE.MeshStandardMaterial({ color: 0xd0d3d8, roughness: 0.22, metalness: 1.0 });
    const sh = new THREE.Shape(); sh.moveTo(-0.215, 0); sh.quadraticCurveTo(-0.215, 0.012, -0.19, 0.013); sh.lineTo(-0.03, 0.036); sh.quadraticCurveTo(0, 0.043, 0.03, 0.036); sh.lineTo(0.19, 0.013); sh.quadraticCurveTo(0.215, 0.012, 0.215, 0); sh.lineTo(0.205, -0.01); sh.lineTo(-0.205, -0.01); sh.closePath();
    const hb = new THREE.Mesh(new THREE.ExtrudeGeometry(sh, { depth: 0.016, bevelEnabled: true, bevelThickness: 0.004, bevelSize: 0.004, bevelSegments: 4, curveSegments: 14 }), wood); hb.position.set(0, 1.088, -0.008); body.add(hb);
    for (const sx of [-1, 1]) {
      const cl = new THREE.Group(), fr = new THREE.Mesh(new THREE.BoxGeometry(0.036, 0.05, 0.0035), steel), bk = fr.clone(), top = new THREE.Mesh(new THREE.BoxGeometry(0.036, 0.006, 0.17), steel);
      fr.position.set(0, -0.026, 0.0875); bk.position.set(0, -0.026, -0.0875); top.position.set(0, 0.002, 0);
      const pad = new THREE.MeshStandardMaterial({ color: 0x1e1b18, roughness: 0.9 }), pf = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.04, 0.002), pad); pf.position.set(0, -0.028, 0.0845); const pb = pf.clone(); pb.position.z = -0.0845;
      const spr = new THREE.Mesh(new THREE.TorusGeometry(0.007, 0.0014, 6, 14), steel); spr.rotation.y = Math.PI / 2; spr.position.set(0.0, 0.01, 0.0);
      cl.add(fr, bk, top, pf, pb, spr); cl.position.set(sx * 0.12, 1.08, 0); body.add(cl);
    }
    const eye = new THREE.Mesh(new THREE.TorusGeometry(0.014, 0.0026, 10, 28), steel); eye.position.set(0, 1.162, 0); eye.rotation.y = Math.PI / 2; body.add(eye);   // a full ring: closed
    const neck = []; for (let k = 0; k <= 12; k++) { const u = k / 12; neck.push([0, 1.12 + 0.034 * u, 0.0 * u]); } body.add(tube(neck, 0.0042, steel, 12));
    const cap = new THREE.Mesh(new THREE.CylinderGeometry(0.0085, 0.0085, 0.008, 18), steel); cap.position.set(0, 1.122, 0); body.add(cap);
    const cord = new THREE.Mesh(new THREE.CylinderGeometry(0.0022, 0.0022, o.hang, 8), new THREE.MeshStandardMaterial({ color: 0xe8dcc0, roughness: 0.9 })); cord.position.set(0, 1.176 + o.hang / 2, 0); cord.userData.noshadow = true; body.add(cord);
    const knot = new THREE.Mesh(new THREE.SphereGeometry(0.005, 10, 8), new THREE.MeshStandardMaterial({ color: 0xe8dcc0, roughness: 0.9 })); knot.position.set(0, 1.176, 0); body.add(knot);
  }
  return body;
}
