import os, sys
sys.path.insert(0, "D:/ClaudeCodeTest/.claude/skills/fashion-3d/engine"); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from world3d import World3D
import room
w = World3D("s", 0.0, 3.0, fov=42, w=1080, h=1920, fade=0.1)
room.furnish(w, trouser="D:/ClaudeCodeTest/videos/_bench/assets3d/finali/pantalone.glb")
w.cam((0.5, 1.3, 7.0), (0.5, 1.5, -2.0))
w.cam((0.3, 1.3, 4.0), (0.5, 1.3, -2.0), t=1.0, d=1.0)
print(World3D.page(os.path.join(os.path.dirname(os.path.abspath(__file__)), "comp_test"), [w], duration=3.0))
