"""Render frames and pipe them to ffmpeg.

Animation runs at ANIM_FPS (12 = "on 2s"); every art frame is held for
OUT_FPS / ANIM_FPS output frames, so the 24 fps MP4 keeps a choppy pixel feel.
Upscaling is done here with nearest-neighbour; ffmpeg only encodes.
"""
import subprocess
from .canvas import SCALE, NATIVE_W, NATIVE_H

ANIM_FPS = 12
OUT_FPS = 24


def encode(frames, path, out_fps=OUT_FPS, anim_fps=ANIM_FPS, scale=SCALE, crf=14):
    hold = out_fps // anim_fps
    w, h = NATIVE_W * scale, NATIVE_H * scale
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}", "-r", str(out_fps), "-i", "-",
        "-c:v", "libx264", "-preset", "slow", "-crf", str(crf), "-tune", "animation",
        # 6x6 art pixels on even boundaries: 4:2:0 chroma never crosses a pixel
        "-pix_fmt", "yuv420p", "-movflags", "+faststart", path,
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    n = 0
    for canvas in frames:
        buf = canvas.upscale(scale).tobytes()
        for _ in range(hold):
            proc.stdin.write(buf)
            n += 1
    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError("ffmpeg failed")
    return n
