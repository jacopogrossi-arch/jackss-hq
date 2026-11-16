"""Shim: the 3D engine moved to the `fashion-3d` skill on 16/11/2026 (fashion-3d/engine/world3d.py).
Old imports (`from world3d import World3D` with this folder on sys.path) keep working: the real file is run inside this module."""
import os
_real = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "fashion-3d", "engine", "world3d.py"))
__file__ = _real
exec(compile(open(_real, encoding="utf-8").read(), _real, "exec"), globals())
