"""make_engine.py: world3d.js della skill youtube-edit + le aggiunte di questo progetto (la skill non viene toccata).
Dalla demo "luce": texture "earth", materiale luminoso con alone, "dots", uscita `out`.
Nuovo qui (kit dello store): "shelf" (gondola con prodotti), "floor" (pavimento a piastrelle), "gate" (varco), ombre vere, luce da negozio."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SK = "D:/ClaudeCodeTest/.claude/skills/youtube-edit"
src = open(os.path.join(HERE, "base-world3d.js"), encoding="utf-8").read()   # il motore della skill al 10/11, fissato qui


def sub(a, b):
    global src
    assert src.count(a) == 1, "non trovo (o trovo due volte): " + a[:70]
    src = src.replace(a, b)


EXTRA = open(os.path.join(HERE, "engine-extra.js"), encoding="utf-8").read() + chr(10) + open(os.path.join(HERE, "products.js"), encoding="utf-8").read() + open(os.path.join(HERE, "scenery.js"), encoding="utf-8").read()
sub("const loadImage =", EXTRA + "\nconst loadImage =")
sub('''function solid(o) {
  const mat = o.fabric ?''', '''function solid(o) {
  if (o.type === "dots") return dots(o);
  if (o.type === "shelf") return shelf(o);
  if (o.type === "floor") return floor(o);
  if (o.type === "gate") return gate(o);
  if (o.type === "road") return road(o);
  if (o.type === "car") return car(o);
  if (o.type === "tree") return tree(o);
  if (o.type === "forest") return forest(o);
  if (o.type === "hedge") return hedge(o);
  if (o.type === "hills") return hills(o);
  if (o.type === "lamp") return lamp(o);
  const mat = o.emissive ? new THREE.MeshBasicMaterial({ color: o.emissive, toneMapped: false }) : o.tex === "earth" ? new THREE.MeshStandardMaterial({ map: earthTex(), roughness: 0.75, metalness: 0 }) : o.tex === "grass" ? new THREE.MeshStandardMaterial({ map: grassTex(o.size), roughness: 1, metalness: 0 }) : o.fabric ?''')
sub("  return new THREE.Mesh(geo, mat);\n}", '''  const mesh = new THREE.Mesh(geo, mat);
  if (o.alpha != null) { mat.transparent = true; mat.opacity = o.alpha; }
  if (!o.glow) return mesh;
  const grp = new THREE.Group(), sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: haloTex(o.glow[1] || "#ffd98a"), blending: THREE.AdditiveBlending, depthWrite: false, transparent: true, opacity: o.glow[2] ?? 1 }));
  sp.scale.set(o.glow[0], o.glow[0], 1); grp.add(sp); grp.add(mesh);
  if (o.core) { const c = new THREE.Sprite(new THREE.SpriteMaterial({ map: haloTex(o.core[1]), blending: THREE.AdditiveBlending, depthWrite: false, depthTest: false, transparent: true, opacity: o.core[2] ?? 1 })); c.scale.set(o.core[0], o.core[0], 1); c.renderOrder = 5; grp.add(c); }
  return grp;
}''')
sub('''      const a = o.t == null ? 1 : prog(t, o.t, 0.6, "out");''', '''      const ain = o.t == null ? 1 : prog(t, o.t, o.tin ?? 0.6, "out"), a = ain * (o.out == null ? 1 : 1 - prog(t, o.out, 0.4, "smooth"));''')
sub("g.position.set(p[0], p[1] - 0.12 * (1 - a), p[2]);", "g.position.set(p[0], p[1] - (o.rise ?? 0.12) * (1 - ain), p[2]);")
sub("if (m.material && o.t != null) {", "if (m.material && (o.t != null || o.out != null)) {")
# a whole room: shadows, shop light, far plane
sub("key.position.set(1.6, 2.4, 2.2); scene.add(key);", """key.position.set(1.6, 2.4, 2.2); scene.add(key);
  if (spec.fog) scene.fog = new THREE.Fog(spec.fog[0], spec.fog[1], spec.fog[2]);
  if (spec.far) { camera.far = spec.far; camera.updateProjectionMatrix(); }
  if (spec.shadows) { renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap; key.position.set(...(spec.keyPos || [5.5, 11, 6.5])); key.castShadow = true; key.shadow.mapSize.set(4096, 4096);
    const sc = key.shadow.camera; const sb = spec.shadowBox || [11, 9, 40]; sc.left = -sb[0]; sc.right = sb[0]; sc.top = sb[1]; sc.bottom = -sb[1]; sc.near = 1; sc.far = sb[2]; sc.updateProjectionMatrix(); key.shadow.bias = -0.0006; key.shadow.normalBias = 0.04; key.shadow.radius = 5; }""")
sub("scene.add(new THREE.HemisphereLight(0xe9f5ee, 0x0a2b1e, 0.55));", """scene.add(new THREE.HemisphereLight(0xe9f5ee, 0x0a2b1e, 0.55));
  if (spec.light === "store") { key.color.set(0xfff6e8); key.intensity = 2.3; rim.color.set(0xdfe9ff); rim.intensity = 0.9; scene.add(new THREE.AmbientLight(0xffffff, 0.75)); }""")
sub("scene.add(g); items[o.id] = { o, g };", """scene.add(g); items[o.id] = { o, g };
      if (spec.shadows) g.traverse((x) => { if (x.isMesh && x.material && !x.material.isMeshBasicMaterial) { x.receiveShadow = true; x.castShadow = !x.userData.floor && !(x.material.transparent && x.material.opacity < 0.9); } });""")
open(os.path.join(HERE, "vendor", "world3d.js"), "w", encoding="utf-8", newline="\n").write(src)
print("engine ok", len(src))
