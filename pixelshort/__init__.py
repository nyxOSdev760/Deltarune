"""pixelshort - a tiny engine for low-res, nearest-neighbor pixel-art shorts.

Everything is drawn on a small native canvas (default 180x320, 9:16) using
flat colours only, then upscaled by an integer factor with nearest-neighbour
so every art pixel lands on the output as a crisp square block.
"""
from .canvas import Canvas, NATIVE_W, NATIVE_H, SCALE
from .sprite import Sprite
