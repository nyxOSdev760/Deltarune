"""Native-resolution canvas. Flat colours only - no smoothing anywhere."""
import numpy as np

# 180x320 is "about 160x284" and is the only nearby 9:16 size that scales to
# 1080x1920 by a whole number (x6). A whole-number scale keeps every art
# pixel exactly 6x6 output pixels, so nothing is ever stretched unevenly.
NATIVE_W, NATIVE_H = 180, 320
SCALE = 6
SAFE_MARGIN = NATIVE_H // 10  # 32 px top and bottom kept clear for platform UI


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


class Canvas:
    def __init__(self, w=NATIVE_W, h=NATIVE_H, fill=(0, 0, 0)):
        self.w, self.h = w, h
        self.px = np.zeros((h, w, 3), dtype=np.uint8)
        self.px[:] = fill

    def copy(self):
        c = Canvas(self.w, self.h)
        c.px = self.px.copy()
        return c

    # -- primitives -------------------------------------------------------
    def rect(self, x, y, w, h, color):
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + w), min(self.h, y + h)
        if x1 > x0 and y1 > y0:
            self.px[y0:y1, x0:x1] = color

    def hline(self, x, y, w, color):
        self.rect(x, y, w, 1, color)

    def vline(self, x, y, h, color):
        self.rect(x, y, 1, h, color)

    def pset(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.px[y, x] = color

    def blit(self, sprite, x, y, flip=False):
        """Paste a Sprite with its top-left at (x, y). Hard alpha only."""
        rgb, mask = (sprite.rgb, sprite.mask)
        if flip:
            rgb, mask = rgb[:, ::-1], mask[:, ::-1]
        sh, sw = mask.shape
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + sw), min(self.h, y + sh)
        if x1 <= x0 or y1 <= y0:
            return
        sub_m = mask[y0 - y:y1 - y, x0 - x:x1 - x]
        sub_c = rgb[y0 - y:y1 - y, x0 - x:x1 - x]
        dst = self.px[y0:y1, x0:x1]
        dst[sub_m] = sub_c[sub_m]

    # -- full-frame effects -------------------------------------------------
    def tint(self, color, alpha):
        """Flat colour overlay (e.g. red anger tint at 0.2-0.3)."""
        if alpha <= 0:
            return
        c = np.array(color, dtype=np.float32)
        out = self.px.astype(np.float32) * (1 - alpha) + c * alpha
        self.px = np.round(out).astype(np.uint8)

    def shake(self, dx, dy):
        """Whole-pixel jitter; edges repeat so no black seams appear."""
        if dx == 0 and dy == 0:
            return
        p = np.pad(self.px, ((2, 2), (2, 2), (0, 0)), mode="edge")
        self.px = p[2 - dy:2 - dy + self.h, 2 - dx:2 - dx + self.w].copy()

    def upscale(self, factor=SCALE):
        """Nearest-neighbour only: each art pixel becomes a factor x factor block."""
        return np.repeat(np.repeat(self.px, factor, axis=0), factor, axis=1)


def line_points(x0, y0, x1, y1):
    n = int(max(abs(x1 - x0), abs(y1 - y0))) + 1
    return [(int(round(x0 + (x1 - x0) * i / max(1, n - 1))),
             int(round(y0 + (y1 - y0) * i / max(1, n - 1)))) for i in range(n)]


def stroke(c, x0, y0, x1, y1, color, r=1, progress=1.0):
    """Square-brush line, optionally only the first `progress` of it (for
    drawing-on animation). Hard edges, no anti-aliasing."""
    pts = line_points(x0, y0, x1, y1)
    k = int(round(len(pts) * max(0.0, min(1.0, progress))))
    for x, y in pts[:k]:
        c.rect(x - r, y - r, 2 * r + 1, 2 * r + 1, color)


def ring(c, cx, cy, r_out, r_in, color, progress=1.0, start_deg=-90):
    """Annulus revealed clockwise from the top as progress goes 0 -> 1."""
    import math
    for y in range(int(cy - r_out) - 1, int(cy + r_out) + 2):
        for x in range(int(cx - r_out) - 1, int(cx + r_out) + 2):
            dx, dy = x + 0.5 - cx, y + 0.5 - cy
            d2 = dx * dx + dy * dy
            if r_in * r_in <= d2 <= r_out * r_out:
                a = (math.degrees(math.atan2(dy, dx)) - start_deg) % 360
                if a <= 360 * progress:
                    c.pset(x, y, color)
