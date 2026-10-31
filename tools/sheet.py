"""Export a sprite sheet PNG (nearest-neighbour scaled) for review."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from PIL import Image
from pixelshort import Canvas
from pixelshort import cast


def main(out="renders/sprite_sheet.png", scale=6):
    items = []
    for f in cast.ZACK_FACES:
        items.append(cast.zack(face=f))
    for l in cast.ZACK_LEGS:
        items.append(cast.zack(legs=l))
    items.append(cast.zack(face="deadpan", rim="#b8c8ff"))
    for f in cast.PIP_FACES:
        items.append(cast.pip(f))
    items.append(cast.pip("normal", suit=False))
    items += cast.flames() + cast.steam()
    items.append(cast.pip_closeup())
    W = sum(s.w + 4 for s in items) + 4
    H = max(s.h for s in items) + 8
    c = Canvas(W, H, fill=(147, 80, 47))
    x = 4
    for s in items:
        c.blit(s, x, H - 4 - s.h)
        x += s.w + 4
    Image.fromarray(c.upscale(scale)).save(out)
    print(out, c.w, c.h)


if __name__ == "__main__":
    main(*sys.argv[1:])
