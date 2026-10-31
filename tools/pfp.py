"""Channel profile picture: Zack (smug) and Pip (angry), fire at the bottom.

224x224 native, upscaled x4 with nearest-neighbour -> 896x896 PNG. Platforms
show avatars in a circle, so the faces are kept near the centre and a circle-
masked preview is written next to it.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
from PIL import Image
from pixelshort import Canvas, cast, backgrounds as bg, effects as fx

N, SC = 224, 4


def build(frame=0):
    c = Canvas(N, N, fill=bg.WALL)
    for x in range(10, N, 30):                       # same wall panels as the shorts
        c.rect(x, 0, 2, N, bg.WALL_LINE)
        c.rect(x + 2, 0, 1, N, bg.WALL_HI)
    zack = cast.zack_closeup("smug", h=184)
    pip = cast.pip_closeup("angry", h=184)
    c.blit(zack, 2, 40)
    c.blit(pip, 94, 40)
    # fire in front, drawn on a key-colour layer so stray embers can be kept
    # off the faces: only the bottom band is composited
    key = (255, 0, 255)
    layer = Canvas(N, N, fill=key)
    fx.fire_row(layer, frame, floor_y=214, height=0.7, spacing=9, seed=5)
    band = layer.px[184:]
    keep = ~np.all(band == key, axis=-1)
    c.px[184:][keep] = band[keep]
    return c


def main(out="renders/channel_pfp.png"):
    c = build()
    img = Image.fromarray(c.upscale(SC))
    img.save(out)
    # circle preview (what the platform shows)
    px = np.asarray(img).copy()
    yy, xx = np.mgrid[0:px.shape[0], 0:px.shape[1]]
    r = px.shape[0] / 2
    outside = (xx + 0.5 - r) ** 2 + (yy + 0.5 - r) ** 2 > r * r
    px[outside] = (20, 14, 40)
    Image.fromarray(px).save(out.replace(".png", "_circle_preview.png"))
    print(out, img.size)


if __name__ == "__main__":
    main(*sys.argv[1:])
