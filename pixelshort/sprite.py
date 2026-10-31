"""Sprites authored as ASCII grids.

Each character maps to a palette colour; '.' is transparent. Outlines are
generated automatically: every transparent pixel touching the sprite becomes a
1 px outline whose colour is the neighbouring fill colour pushed hard toward a
dark navy - so hair gets a dark-brown edge, a green sweater a dark-green edge,
and nothing is ever pure black.
"""
import numpy as np
from .canvas import hex_rgb

OUTLINE_BASE = (22, 16, 40)  # dark navy the outline is pulled toward


def _parse(rows, palette):
    width = max(len(r) for r in rows)
    for i, r in enumerate(rows):
        if len(r) != width:
            raise ValueError(f"row {i} is {len(r)} wide, expected {width}: {r!r}")
    h = len(rows)
    rgb = np.zeros((h, width, 3), dtype=np.uint8)
    mask = np.zeros((h, width), dtype=bool)
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch in ". ":
                continue
            if ch not in palette:
                raise KeyError(f"no palette entry for {ch!r} at {x},{y}")
            rgb[y, x] = palette[ch]
            mask[y, x] = True
    return rgb, mask


def outline_tone(c, strength=0.72):
    c = np.asarray(c, dtype=np.float32)
    base = np.array(OUTLINE_BASE, dtype=np.float32)
    return np.round(c * (1 - strength) + base * strength).astype(np.uint8)


class Sprite:
    def __init__(self, rgb, mask):
        self.rgb, self.mask = rgb, mask

    @property
    def w(self):
        return self.mask.shape[1]

    @property
    def h(self):
        return self.mask.shape[0]

    @classmethod
    def from_rows(cls, rows, palette, outline=True, outline_color=None):
        pal = {k: (hex_rgb(v) if isinstance(v, str) else v) for k, v in palette.items()}
        rgb, mask = _parse(rows, pal)
        s = cls(rgb, mask)
        if outline:
            s = s.outlined(outline_color)
        return s

    def outlined(self, color=None):
        """Add a 1 px outline (4-connected) around the sprite."""
        rgb = np.pad(self.rgb, ((1, 1), (1, 1), (0, 0)))
        m = np.pad(self.mask, 1)
        h, w = m.shape
        edge = np.zeros_like(m)
        out = rgb.copy()
        # walk the 4 neighbours; first neighbour found decides the tint
        for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            sm = np.zeros_like(m)
            sc = np.zeros_like(rgb)
            ys = slice(max(0, dy), h + min(0, dy))
            yd = slice(max(0, -dy), h + min(0, -dy))
            xs = slice(max(0, dx), w + min(0, dx))
            xd = slice(max(0, -dx), w + min(0, -dx))
            sm[yd, xd] = m[ys, xs]
            sc[yd, xd] = rgb[ys, xs]
            new = sm & ~m & ~edge
            if color is None:
                out[new] = outline_tone(sc[new]) if new.any() else out[new]
            else:
                out[new] = hex_rgb(color) if isinstance(color, str) else color
            edge |= new
        return Sprite(out, m | edge)

    def rimmed(self, color):
        """Extra light rim outside the dark outline, for dark backgrounds."""
        return self.outlined(color)

    def flipped(self):
        return Sprite(self.rgb[:, ::-1].copy(), self.mask[:, ::-1].copy())

    @staticmethod
    def stack(top_rows, bottom_rows):
        return list(top_rows) + list(bottom_rows)
