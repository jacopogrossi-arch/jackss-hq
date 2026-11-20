// atelier-mascot.js (16/11/2026): "Jacopino", the channel's 3D mascot = a small stylised Jacopo (personal brand: the character is the person, never a spool or a generic thing).
// Built from his real style (memory style_jacopo): wavy medium-short brown hair, light stubble, Mediterranean skin, slim black tee, dark-indigo boot-cut selvage jeans, black Texan boots with a heel,
// belt, optional glasses and an olive vest over the shoulder. Chibi proportions (head about 36 % of the height) so he reads on a phone. VERSION 1: primitives; a Blender-modelled version can replace it
// through w.glb() later. Everything is a pure function of time (blink, breathing, walk, wave, hop come from t, no state).
// build: buildMascot(o) -> THREE.Group standing on y = 0, facing +z. o: size[0] = height in metres (default 0.55), glasses, vest, walk=[[t0,t1],...], wave=[[t0,t1],...], hop=[t,...] (plate seconds).
import * as THREE from "./three.module.min.js";

export const MASCOT = new Set(["jacopino"]);
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const hash = (n) => { const s = Math.sin(n * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
const std = (c, r = 0.7, m = 0) => new THREE.MeshStandardMaterial({ color: c, roughness: r, metalness: m });
const mesh = (geo, mat, x = 0, y = 0, z = 0) => { const m = new THREE.Mesh(geo, mat); m.position.set(x, y, z); m.castShadow = true; m.receiveShadow = true; return m; };
const inAny = (t, L) => { for (const [a, b] of L || []) if (t >= a && t <= b) return [a, b]; return null; };

export function buildMascot(o) {
  const g = new THREE.Group(), s = ((o.size && o.size[0]) || 0.55) / 0.55, body = new THREE.Group(); g.add(body);
  const SKIN = std("#d3996f", 0.62), TEE = std("#1e1b18", 0.85), JEAN = std("#2a3a58", 0.9), BOOT = std("#17120f", 0.45, 0.1), HAIR = std("#4a3223", 0.8), BELT = std("#3a2a1c", 0.6), EYE = std("#14100c", 0.3);
  // ---- legs (pivot at the hip): boot-cut jeans with a red selvage line, a Texan boot with a pointed toe and a heel
  const mkLeg = (side) => {
    const pv = new THREE.Group(); pv.position.set(side * 0.034, 0.205, 0); body.add(pv);
    pv.add(mesh(new THREE.CylinderGeometry(0.03, 0.043, 0.125, 20), JEAN, 0, -0.0625, 0));
    pv.add(mesh(new THREE.CylinderGeometry(0.038, 0.04, 0.05, 20), BOOT, 0, -0.1475, 0));                                           // boot shaft
    const toe = mesh(new THREE.SphereGeometry(1, 24, 16), BOOT, 0, -0.18, 0.026); toe.scale.set(0.034, 0.03, 0.074); pv.add(toe);   // elongated, pointed toe
    pv.add(mesh(new THREE.BoxGeometry(0.036, 0.03, 0.03), BOOT, 0, -0.19, -0.026));                                                  // heel
    return pv;
  };
  const legL = mkLeg(-1), legR = mkLeg(1);
  // ---- torso: a slim black tee on an athletic frame, belt with a silver buckle
  const torso = mesh(new THREE.CapsuleGeometry(0.052, 0.1, 8, 20), TEE, 0, 0.29, 0); torso.scale.set(1.12, 1, 0.82); body.add(torso);
  const belt = mesh(new THREE.CylinderGeometry(0.0565, 0.0565, 0.012, 24), BELT, 0, 0.212, 0); belt.scale.set(1.12, 1, 0.82); body.add(belt);
  body.add(mesh(new THREE.BoxGeometry(0.014, 0.011, 0.004), std("#c9ccd2", 0.25, 0.9), 0, 0.212, 0.0475));
  // ---- arms (pivot at the shoulder): short sleeve, skin forearm, a hand
  const mkArm = (side) => {
    const pv = new THREE.Group(); pv.position.set(side * 0.074, 0.335, 0); body.add(pv);
    pv.add(mesh(new THREE.CylinderGeometry(0.024, 0.026, 0.05, 16), TEE, 0, -0.025, 0));
    pv.add(mesh(new THREE.CapsuleGeometry(0.0185, 0.06, 6, 14), SKIN, 0, -0.085, 0));
    pv.add(mesh(new THREE.SphereGeometry(0.021, 14, 10), SKIN, 0, -0.13, 0));
    pv.rotation.z = side * 0.14; return pv;
  };
  const armL = mkArm(-1), armR = mkArm(1);
  // ---- head: skin, ears, nose, eyes with a glint, brows, a smile, light stubble, wavy brown hair
  const head = new THREE.Group(); head.position.set(0, 0.455, 0); body.add(head);
  const skull = mesh(new THREE.SphereGeometry(0.1, 36, 24), SKIN); skull.scale.set(1, 1.03, 0.97); head.add(skull);
  for (const sd of [-1, 1]) { head.add(mesh(new THREE.SphereGeometry(0.019, 12, 8), SKIN, sd * 0.099, -0.005, 0)); }
  head.add(mesh(new THREE.SphereGeometry(0.016, 14, 10), SKIN, 0, -0.012, 0.099));
  const eyes = [];
  for (const sd of [-1, 1]) {
    const e = mesh(new THREE.SphereGeometry(1, 16, 12), EYE, sd * 0.036, 0.012, 0.092); e.scale.set(0.0115, 0.017, 0.007); head.add(e); eyes.push(e);
    head.add(mesh(new THREE.SphereGeometry(0.0033, 8, 6), std("#ffffff", 0.2), sd * 0.0385, 0.019, 0.0985));
    const br = mesh(new THREE.BoxGeometry(0.03, 0.0065, 0.006), HAIR, sd * 0.036, 0.047, 0.093); br.rotation.z = sd * -0.12; head.add(br);
  }
  const smile = mesh(new THREE.TorusGeometry(0.02, 0.0032, 6, 20, Math.PI), std("#7a3b2e", 0.5), 0, -0.036, 0.094); smile.rotation.z = Math.PI; head.add(smile);
  const stub = new THREE.Mesh(new THREE.SphereGeometry(0.1008, 28, 14, 0, Math.PI * 2, 2.3, 0.84), new THREE.MeshStandardMaterial({ color: "#3a2c22", roughness: 1, transparent: true, opacity: 0.3, depthWrite: false })); stub.scale.set(1, 1.03, 0.97); head.add(stub);
  const cap = mesh(new THREE.SphereGeometry(0.106, 32, 18, 0, Math.PI * 2, 0, 1.28), HAIR, 0, 0.012, -0.01); cap.rotation.x = -0.28; head.add(cap);       // hair swept a little back
  for (let i = 0; i < 9; i++) { const a = -1.2 + i * 0.3, r = 0.012 + 0.006 * hash(i), c = mesh(new THREE.SphereGeometry(r + 0.012, 10, 8), HAIR, Math.sin(a) * 0.085, 0.09 + 0.012 * hash(i + 3), Math.cos(a) * 0.04 + 0.02 - 0.03 * hash(i + 6)); head.add(c); }   // the wave on top
  if (o.glasses) { for (const sd of [-1, 1]) head.add(mesh(new THREE.TorusGeometry(0.029, 0.0024, 8, 28), std("#101010", 0.3, 0.4), sd * 0.036, 0.013, 0.1)); head.add(mesh(new THREE.BoxGeometry(0.018, 0.0024, 0.0024), std("#101010", 0.3, 0.4), 0, 0.017, 0.1)); }
  if (o.vest) { const v = mesh(new THREE.BoxGeometry(0.05, 0.1, 0.012), std("#6f7452", 0.95), -0.085, 0.31, 0.044); v.rotation.z = 0.12; v.rotation.y = 0.18; body.add(v); const v2 = mesh(new THREE.BoxGeometry(0.03, 0.08, 0.012), std("#5f6446", 0.95), -0.075, 0.295, -0.04); v2.rotation.z = 0.12; body.add(v2); }   // an olive vest slung over the shoulder
  g.scale.setScalar(s);
  // ---- life: a pure function of t (plate seconds)
  g.userData.update = (t) => {
    const w = inAny(t, o.walk), wv = inAny(t, o.wave);
    let swing = 0, bob = 0.004 * Math.sin(t * 2.6);                                              // breathing
    if (w) { const k = Math.min(clamp((t - w[0]) / 0.25), clamp((w[1] - t) / 0.25)); swing = 0.55 * k * Math.sin((t - w[0]) * Math.PI * 2 * 1.7); bob += 0.012 * k * Math.abs(Math.sin((t - w[0]) * Math.PI * 2 * 1.7)); }
    legL.rotation.x = swing; legR.rotation.x = -swing; armL.rotation.x = -swing * 0.8; armR.rotation.x = swing * 0.8;
    armR.rotation.z = 0.14; if (wv) { const k = Math.min(clamp((t - wv[0]) / 0.3), clamp((wv[1] - t) / 0.3)); armR.rotation.z = 0.14 + k * (2.5 - 0.14) + 0.28 * k * Math.sin((t - wv[0]) * 11); armR.rotation.x = 0; }
    let hop = 0, sq = 0; for (const h of o.hop || []) { const k = (t - h) / 0.5; if (k >= 0 && k <= 1) { hop = 0.09 * Math.sin(Math.PI * k); sq = -0.06 * Math.exp(-k * 14); } else if (k > -0.12 && k < 0) sq = 0.07 * (1 + k / 0.12); }
    body.position.y = bob + hop; body.scale.set(1 - sq * 0.4, 1 + sq, 1 - sq * 0.4);               // squash and stretch, volume kept
    head.rotation.y = 0.12 * Math.sin(t * 0.9); head.rotation.x = 0.02 * Math.sin(t * 1.7);
    const ph = (t % 3.4), blink = ph < 0.11 ? Math.sin(Math.PI * ph / 0.11) : 0; for (const e of eyes) e.scale.y = 0.017 * (1 - 0.9 * blink);
  };
  g.userData.update(0);
  return g;
}
