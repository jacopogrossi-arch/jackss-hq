import sys
sys.path.insert(0, "D:/ClaudeCodeTest/.claude/skills/fashion-3d/engine")
from world3d import World3D
GLB = "D:/ClaudeCodeTest/videos/_bench/fashion3d/blender/trouser10b.glb"
w = World3D("w1", 0.0, 3.0, fov=34, w=1080, h=1920)
w.room(bg="#120d09", key="#ffc48a", dir=(-3, 2.2, 2.5), key_i=4.2, hemi=("#ffd8b0", "#2a1a10"), hemi_i=0.30, rim_i=0.15, aim=(0, 0.55, 0)).photo()
w.soft(n=10, area=0.12, sky=0.3)
w.prop("woodfloor", "fl", (0, 0, 0), (8, 8)); w.prop("wall", "wl", (0, 0, -1.3), (4, 3, 0.1), color="#3b2b20")
w.prop("table", "tb", (-0.2, 0, -0.9), (2.4, 0.78, 0.7)); w.prop("bookshelf", "bs", (0.95, 0, -1.2)); w.prop("desklamp", "lp", (-0.65, 0.9, -0.6))
w.solid("pole", "cyl", (0, 0.15, 0), (0.025, 0.30), color="#3a3a3c", metal=0.8, rough=0.4); w.solid("base", "cyl", (0, 0.01, 0), (0.55, 0.025), color="#26262a", metal=0.5, rough=0.5)
w.glb("tr", GLB, fit=1.18, pos=(0, 0.14, 0), rot_y=-0.45, double=True, fabric=True)
w.cam((0.28, 0.66, 3.2), look=(-0.01, 0.62, 0)); w.dof(0.0, 3.0, aperture=0.035)
World3D.page("D:/ClaudeCodeTest/videos/_bench/fashion3d/lab_merge2", [w], duration=3.0)
print("built")
