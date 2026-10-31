"""Build large sprites from flat shapes on a character grid.

Used for close-ups: shapes write palette keys (not colours), the grid becomes
ASCII rows, and the result goes through the same Sprite pipeline (flat tones,
auto 1 px tinted outline) as the hand-drawn sprites.
"""
import numpy as np


class Grid:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.g = np.full((h, w), ".", dtype="<U1")
        yy, xx = np.mgrid[0:h, 0:w]
        self.x, self.y = xx + 0.5, yy + 0.5

    def ellipse_mask(self, cx, cy, rx, ry):
        return ((self.x - cx) / rx) ** 2 + ((self.y - cy) / ry) ** 2 <= 1.0

    def fill(self, mask, key):
        self.g[mask] = key

    def ellipse(self, cx, cy, rx, ry, key):
        self.fill(self.ellipse_mask(cx, cy, rx, ry), key)

    def rect(self, x, y, w, h, key):
        self.g[max(0, y):max(0, y + h), max(0, x):max(0, x + w)] = key

    def line(self, x0, y0, x1, y1, key, r=1):
        """Thick line with a square brush (keeps edges blocky)."""
        n = int(max(abs(x1 - x0), abs(y1 - y0))) + 1
        for i in range(n):
            t = i / max(1, n - 1)
            x = int(round(x0 + (x1 - x0) * t))
            y = int(round(y0 + (y1 - y0) * t))
            self.rect(x - r, y - r, 2 * r + 1, 2 * r + 1, key)

    def rows(self):
        return ["".join(r) for r in self.g]
