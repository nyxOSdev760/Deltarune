"""Frame effects: fire, steam, screen shake, anger tint."""
import random
from .cast import flames, steam
from .canvas import hex_rgb

_FLAMES = flames()
_STEAM = steam()
ANGER_RED = hex_rgb("#e01c28")
EMBER = hex_rgb("#ffb040")


def fire_row(c, frame, floor_y, height=1.0, x0=0, x1=None, spacing=10, seed=3):
    """A loop of flickering flames along the floor that grows upward.

    height 0..1 controls how far the fire has risen: extra rows of flames
    stack above the floor row as it grows, and embers drift up.
    """
    x1 = c.w if x1 is None else x1
    rnd = random.Random(seed)
    rows = 1 + int(round(height * 3))
    for r in range(rows):
        y = floor_y - 10 - r * 7
        off = (r * 5) % spacing
        for x in range(x0 - 4 + off, x1, spacing):
            ph = rnd.randrange(3)
            # 3-frame flicker, each flame on its own phase
            spr = _FLAMES[(frame + ph) % 3]
            bob = (frame + ph) % 2
            c.blit(spr, x, y - bob, flip=bool((x // spacing + frame) % 2))
    # rising embers, looping upward
    for i in range(int(14 * height)):
        ex = rnd.randrange(x0, x1)
        speed = 2 + rnd.randrange(2)
        span = 60 + rnd.randrange(40)
        ey = floor_y - 14 - ((frame * speed + rnd.randrange(span)) % span)
        c.pset(ex + ((frame + i) // 3) % 2, ey, EMBER)


def steam_puffs(c, frame, x, y, count=3):
    """Steam puffs that rise and grow from a point (spout or lid)."""
    for i in range(count):
        t = (frame + i * 4) % 12
        spr = _STEAM[min(2, t // 4)]
        c.blit(spr, x - spr.w // 2 + (i % 2) * 2 - 1, y - t * 2 - spr.h)


def shake_offset(frame, amp=2, seed=11):
    """Random 1-2 px jitter per frame, no easing."""
    rnd = random.Random(seed * 1000 + frame)
    dx = rnd.choice([-amp, -1, 1, amp])
    dy = rnd.choice([-1, 0, 1])
    return dx, dy


def tint_ramp(frame, start, frames=6, peak=0.26):
    """Anger tint fading in over several frames in flat steps."""
    if frame < start:
        return 0.0
    k = min(frames, frame - start + 1)
    return peak * k / frames
