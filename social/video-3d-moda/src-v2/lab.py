import os, sys
SK = "D:/ClaudeCodeTest/.claude/skills/youtube-edit"
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SK + "/formats"); sys.path.insert(0, HERE)
from world3d import World3D
from room import furnish
w = World3D("r", 0.0, 12.0, fov=34)
furnish(w)
w.trouser("hero", pos=(0.3, 0.55, 0.4), rot_y=-0.4, color="#6f7452", hang=2.0, turn=[(0, 12, 0.4, "smooth")])
w.trouser("toile", pos=(3.1, 1.0, 1.4), rot_y=0.3, color="#e8e0cc", hang=0.0)
w.cam((0.9, 1.15, 2.0), look=(0.3, 1.0, 0.4))
w.cam((1.0, 1.5, 3.2), look=(-1.2, 1.0, 0.3), t=3.0, d=3.0, ease="glide")
w.cam((0.9, 1.15, 1.6), look=(0.3, 1.1, 0.4), t=7.0, d=2.5, ease="glide")
print(World3D.page(HERE + "/lab", [w]))
