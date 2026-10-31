"""Channel profile picture v2: Pip alone, big, on a glowing halo.

Avatars are shown tiny and in a circle, so: one character, one bold silhouette,
high contrast, centred. 144x144 native, x6 nearest-neighbour -> 864x864.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
from PIL import Image
from pixelshort import Canvas, cast, backgrounds as bg
from pixelshort.canvas import hex_rgb as H

N, SC = 144, 6
VOID = H("#150c2c")


def build():
    c = Canvas(N, N, fill=VOID)
    cx, cy = N / 2, 70
    yy, xx = np.mgrid[0:N, 0:N]
    d = np.sqrt((xx + 0.5 - cx) ** 2 + (yy + 0.5 - cy) ** 2)
    # flat concentric halo rings: no gradients, hard steps
    for r, col in ((80, "#232066"), (66, "#3a52b4"), (56, "#7a9cf0")):
        c.px[d <= r] = H(col)
    # single-pixel sparkles
    for x, y in ((14, 20), (126, 14), (24, 104), (122, 96), (70, 8), (8, 62), (136, 56), (104, 30), (40, 34)):
        c.pset(x, y, bg.SPARK)
        if (x + y) % 3 == 0:
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                c.pset(x + dx, y + dy, bg.SPARK_DIM)
    pip = cast.pip_closeup("angry", h=N - 12)
    c.blit(pip, (N - pip.w) // 2, 12)
    return c


def main(out="renders/channel_pfp.png"):
    c = build()
    img = Image.fromarray(c.upscale(SC))
    img.save(out)
    px = np.asarray(img).copy()
    yy, xx = np.mgrid[0:px.shape[0], 0:px.shape[1]]
    r = px.shape[0] / 2
    px[(xx + 0.5 - r) ** 2 + (yy + 0.5 - r) ** 2 > r * r] = (20, 14, 40)
    circ = Image.fromarray(px)
    circ.save(out.replace(".png", "_circle_preview.png"))
    # what it looks like at real avatar sizes (for checking only)
    strip = Image.new("RGB", (96 + 48 + 32 + 40, 100), (30, 30, 36))
    x = 10
    for s in (96, 48, 32):
        strip.paste(circ.resize((s, s), Image.LANCZOS), (x, (100 - s) // 2))
        x += s + 10
    strip.resize((strip.width * 3, strip.height * 3), Image.NEAREST).save("/tmp/pfp_small.png")
    print(out, img.size)


if __name__ == "__main__":
    main(*sys.argv[1:])
