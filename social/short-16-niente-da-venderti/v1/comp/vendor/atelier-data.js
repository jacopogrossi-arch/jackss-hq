// atelier-data.js (16/11/2026): DATA AS OBJECTS for the "metaphor world" format (from the drillup.io reels studied at 8 fps: a dot grid where "1 in 10" lights up, a call to action written INSIDE the scene).
// Types: "dotgrid" (a grid of small rounded tiles; some light up, one after the other, on given times), "ctaplate" (a lit plate with words, standing in the world).
// Pure functions of time: the lit state and the pop-in come from t (plate seconds), nothing is stored between frames.
import * as THREE from "./three.module.min.js";

export const DATA = new Set(["dotgrid", "ctaplate"]);
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const backOut = (k, s = 1.7) => 1 + (s + 1) * Math.pow(k - 1, 3) + s * Math.pow(k - 1, 2);

// o: size=[width, height] (metres), cols, rows, lit=[[t, index], ...] (plate seconds; index counts row by row), color (off tiles), accent (lit tiles), pop=[t0, step] (tiles pop in staggered from t0, one every `step` seconds)
function dotgrid(o) {
  const g = new THREE.Group(), cols = o.cols || 10, rows = o.rows || 10, W = (o.size && o.size[0]) || 0.8, H = (o.size && o.size[1]) || 0.8, cw = W / cols, chh = H / rows;
  const off = new THREE.MeshStandardMaterial({ color: o.color || "#3a3530", roughness: 0.6 }), tiles = [];
  for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) {
    const m = new THREE.Mesh(new THREE.BoxGeometry(cw * 0.78, chh * 0.78, 0.018), off.clone()); m.position.set((c - (cols - 1) / 2) * cw, (rows - 1 - r - (rows - 1) / 2) * chh, 0);
    m.castShadow = true; m.receiveShadow = true; g.add(m); tiles.push(m);
  }
  const acc = new THREE.Color(o.accent || "#ffc23a"), base = new THREE.Color(o.color || "#3a3530"), pop = o.pop || [0, 0.012];
  g.userData.update = (t) => {
    tiles.forEach((m, i) => {
      const k = clamp((t - (pop[0] + i * pop[1])) / 0.25), s = k <= 0 ? 0.0001 : backOut(k);                    // staggered pop-in
      m.scale.set(s, s, s);
      let lit = 0; for (const [lt, li] of o.lit || []) if (li === i) lit = clamp((t - lt) / 0.2);
      m.material.color.copy(base).lerp(acc, lit); m.material.emissive.copy(acc).multiplyScalar(0.9 * lit); m.material.emissiveIntensity = 1;
      m.position.z = 0.012 * lit;
    });
  };
  g.userData.update(0); return g;
}

// o: size=[w, h], text="Scrivi *PANTALONE*" (the words between * are highlighted), color (plate), ink, accent
function ctaplate(o) {
  const W = (o.size && o.size[0]) || 0.7, H = (o.size && o.size[1]) || 0.28, cv = document.createElement("canvas"); cv.width = 1400; cv.height = Math.round(1400 * H / W);
  const x = cv.getContext("2d"); x.fillStyle = o.color || "#efe9dd"; x.beginPath(); x.roundRect(0, 0, cv.width, cv.height, 60); x.fill();
  const parts = String(o.text || "Scrivi *CIAO*").split("*"); let size = Math.round(cv.height * 0.34), widths; x.textBaseline = "middle";
  for (let k = 0; k < 12; k++) { x.font = "700 " + size + "px Inter, sans-serif"; widths = parts.map((p) => x.measureText(p).width); if (widths.reduce((a, b) => a + b, 0) <= cv.width * 0.86) break; size = Math.round(size * 0.92); }   // shrink to fit the plate
  let px = (cv.width - widths.reduce((a, b) => a + b, 0)) / 2;
  parts.forEach((p, i) => { x.fillStyle = i % 2 ? (o.accent || "#8a4b2d") : (o.ink || "#1e1b18"); x.fillText(p, px, cv.height / 2); px += widths[i]; });
  const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 8;
  const m = new THREE.Mesh(new THREE.PlaneGeometry(W, H), new THREE.MeshStandardMaterial({ map: tex, roughness: 0.55, emissive: 0xffffff, emissiveMap: tex, emissiveIntensity: 0.35, side: THREE.DoubleSide })); m.castShadow = true;
  const g = new THREE.Group(); g.add(m); g.position.y = 0; m.position.y = H / 2;
  return g;
}

export function buildData(o) { return o.type === "dotgrid" ? dotgrid(o) : ctaplate(o); }
