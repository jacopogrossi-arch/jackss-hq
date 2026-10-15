"""Rigenera i fotogrammi di grana (non salvati nel repo, 12 MB): python3 grain.py"""
import numpy as np
from PIL import Image
rng = np.random.default_rng(7)
for i in range(8):
    n = rng.normal(128, 40, (540, 960)).clip(0, 255).astype(np.uint8)
    Image.fromarray(n, 'L').resize((1920, 1080), Image.BILINEAR).save(f'assets/grain{i}.png')
