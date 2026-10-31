#!/usr/bin/env python3
"""Render a short to a 1080x1920 MP4 (plus optional preview stills).

    python3 render.py siblings              # renders/siblings.mp4 (with audio)
    python3 render.py suit_shop             # renders/suit_shop.mp4
    python3 render.py --stills 0,40,200     # also dump those art frames as PNG
    python3 render.py --watermark @you      # small corner watermark
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from PIL import Image
from pixelshort.encode import encode, ANIM_FPS, OUT_FPS
import importlib
import tempfile


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("scene", nargs="?", default="siblings", help="module in scenes/")
    ap.add_argument("--out", default=None)
    ap.add_argument("--watermark", default=None)
    ap.add_argument("--stills", default="", help="comma list of art-frame indices to save as PNG")
    args = ap.parse_args()

    scene = importlib.import_module(f"scenes.{args.scene}")
    args.out = args.out or f"renders/{args.scene}.mp4"
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    want = {int(s) for s in args.stills.split(",") if s.strip()}
    saved = []

    def tap(it):
        for i, c in enumerate(it):
            if i in want:
                p = Path(args.out).with_name(f"still_{args.scene}_{i:03d}.png")
                Image.fromarray(c.upscale()).save(p)
                saved.append(p)
            yield c

    wav = None
    if hasattr(scene, "soundtrack"):
        wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
        scene.soundtrack(wav)
    n = encode(tap(scene.frames(args.watermark)), args.out, audio=wav)
    print(f"{args.out}: {n} frames @ {OUT_FPS} fps = {n / OUT_FPS:.1f}s "
          f"(art at {ANIM_FPS} fps)")
    for p in saved:
        print("still:", p)


if __name__ == "__main__":
    main()
