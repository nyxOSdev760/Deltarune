"""Tile-based rooms. Backgrounds are kept simpler and lower in contrast than
the characters so sprites pop."""
import random
from .canvas import Canvas, hex_rgb as H
from .font import draw_text, text_width

# ---- warm interior palette (orange / brown / tan) ---------------------------
WALL = H("#93502f")
WALL_LINE = H("#7c4127")
WALL_HI = H("#a05a36")
CEIL = H("#4e2a1c")
CEIL_BEAM = H("#5e3422")
RAIL = H("#5c301e")
WAIN = H("#7a4026")
WAIN_HI = H("#86482b")
FLOOR = H("#d6a06a")
FLOOR_LINE = H("#c48c58")
RUG = H("#c27140")
RUG_D = H("#a85a34")
RUG_EDGE = H("#8e4a2c")
DOOR = H("#5a2e1c")
DOOR_P = H("#6a3822")
DOOR_FRAME = H("#3e2014")
KNOB = H("#ffe066")
KNOB_HI = H("#fffbe0")
COUNTER_TOP = H("#c47c46")
COUNTER_HI = H("#dc9a5c")
COUNTER = H("#86482a")
COUNTER_LINE = H("#713c22")
SHELF = H("#5c301e")
LAMP = H("#ffe8a0")

FLOOR_Y = 168       # where the wall meets the floor
COUNTER_X = 100
COUNTER_Y = 146


def _diamond_rug(c, x, y, w, h):
    c.rect(x, y, w, h, RUG)
    c.rect(x, y, w, 1, RUG_EDGE)
    c.rect(x, y + h - 1, w, 1, RUG_EDGE)
    # repeated carpet diamonds, 8 px tile
    for ty in range(y + 2, y + h - 2):
        for tx in range(x, x + w):
            lx, ly = (tx - x) % 8, (ty - y - 2) % 8
            if abs(lx - 3.5) + abs(ly - 3.5) in (3.0,):
                c.pset(tx, ty, RUG_D)


def shop(sign="PIP'S SUITS"):
    c = Canvas(fill=WALL)
    # ceiling band with beams
    c.rect(0, 0, c.w, 30, CEIL)
    for x in range(6, c.w, 24):
        c.rect(x, 0, 4, 30, CEIL_BEAM)
    c.hline(0, 30, c.w, RAIL)
    # wood panel wall
    for x in range(4, c.w, 12):
        c.vline(x, 31, FLOOR_Y - 31, WALL_LINE)
        c.vline(x + 1, 31, FLOOR_Y - 31, WALL_HI)
    # wainscot band (darker) under a rail
    c.rect(0, 128, c.w, FLOOR_Y - 128, WAIN)
    for x in range(0, c.w, 16):
        c.rect(x + 2, 132, 12, FLOOR_Y - 136, WAIN_HI)
        c.rect(x + 3, 133, 10, FLOOR_Y - 138, WAIN)
    c.rect(0, 126, c.w, 3, RAIL)
    # floor (lighter band) with board seams
    c.rect(0, FLOOR_Y, c.w, c.h - FLOOR_Y, FLOOR)
    c.hline(0, FLOOR_Y, c.w, RAIL)
    for y in range(FLOOR_Y + 6, c.h, 8):
        c.hline(0, y, c.w, FLOOR_LINE)
        off = 0 if (y // 8) % 2 else 14
        for x in range(off, c.w, 28):
            c.vline(x, y - 7, 7, FLOOR_LINE)
    _diamond_rug(c, 10, 182, 160, 26)
    # door with a single bright knob
    c.rect(8, 76, 30, FLOOR_Y - 76, DOOR_FRAME)
    c.rect(11, 79, 24, FLOOR_Y - 79, DOOR)
    c.rect(14, 83, 18, 30, DOOR_P)
    c.rect(14, 118, 18, 44, DOOR_P)
    c.rect(29, 120, 3, 3, KNOB)
    c.pset(29, 120, KNOB_HI)
    # hanging lamp
    c.vline(90, 31, 14, RAIL)
    c.rect(86, 45, 9, 3, RAIL)
    c.rect(87, 48, 7, 2, LAMP)
    # sign board
    tw = text_width(sign)
    bx = (c.w - tw) // 2 - 6
    c.rect(bx, 54, tw + 12, 17, DOOR_FRAME)
    c.rect(bx + 1, 55, tw + 10, 15, DOOR)
    draw_text(c, sign, bx + 6, 58, fill=H("#f2dcae"), border=DOOR_FRAME)
    # shelf of folded suits behind the counter (one bright accent stack)
    c.rect(108, 98, 66, 3, SHELF)
    stacks = [("#2e2c3c", "#4a4860"), ("#3a5ad0", "#6e8ef2"), ("#e8e0d0", "#ffffff"),
              ("#2e2c3c", "#4a4860"), ("#8a3040", "#b04a5a")]
    for i, (base, hi) in enumerate(stacks):
        x = 112 + i * 12
        for j in range(3):
            c.rect(x, 95 - j * 3, 9, 3, H(base))
            c.hline(x, 95 - j * 3, 9, H(hi))
        c.rect(x, 97, 9, 1, DOOR_FRAME)
    return c


def draw_counter(c):
    """Drawn after Mr. Kettle so he stands behind it."""
    c.rect(COUNTER_X, COUNTER_Y, c.w - COUNTER_X, 6, COUNTER_TOP)
    c.hline(COUNTER_X, COUNTER_Y, c.w - COUNTER_X, COUNTER_HI)
    c.hline(COUNTER_X, COUNTER_Y + 6, c.w - COUNTER_X, DOOR_FRAME)
    c.rect(COUNTER_X + 2, COUNTER_Y + 7, c.w - COUNTER_X - 2, 46, COUNTER)
    for x in range(COUNTER_X + 8, c.w, 14):
        c.vline(x, COUNTER_Y + 10, 40, COUNTER_LINE)
    c.vline(COUNTER_X + 2, COUNTER_Y + 7, 46, DOOR_FRAME)
    c.hline(COUNTER_X + 2, COUNTER_Y + 52, c.w - COUNTER_X - 2, DOOR_FRAME)


def closeup_wall():
    """Simplified, flatter wall for the close-up (bigger panels = closer)."""
    c = Canvas(fill=WALL)
    for x in range(10, c.w, 30):
        c.rect(x, 0, 2, c.h, WALL_LINE)
        c.rect(x + 2, 0, 1, c.h, WALL_HI)
    c.rect(0, 40, c.w, 6, RAIL)
    return c


# ---- dark / magical ---------------------------------------------------------
VOID_BANDS = [H("#120a24"), H("#170d2e"), H("#1d1138"), H("#221442")]
BEAM_OUT = H("#2a2a6c")
BEAM_MID = H("#34449a")
BEAM_IN = H("#4a64c0")
SPARK = H("#c8d8ff")
SPARK_DIM = H("#7a86d0")


def void(beam_cx=90):
    c = Canvas(fill=VOID_BANDS[0])
    # flat horizontal bands: deep purple at the top fading to violet
    band_h = c.h // len(VOID_BANDS)
    for i, col in enumerate(VOID_BANDS):
        c.rect(0, i * band_h, c.w, band_h + 1, col)
    # soft vertical light beam: flat bands, each edge softened by a
    # one-column checker of the band colour (still hard, square pixels)
    for half, col in ((26, BEAM_OUT), (18, BEAM_MID), (10, BEAM_IN)):
        c.rect(beam_cx - half, 0, half * 2, c.h, col)
        for y in range(0, c.h, 2):
            c.pset(beam_cx - half - 1, y, col)
            c.pset(beam_cx + half, y + 1, col)
    # floor glow under the beam
    c.rect(beam_cx - 20, 203, 40, 3, BEAM_IN)
    c.rect(beam_cx - 14, 202, 28, 1, H("#6a86e0"))
    return c


def sparkles(c, frame, seed=7, count=34):
    """Sparse single-pixel sparkles that twinkle; a few flash into tiny crosses."""
    rnd = random.Random(seed)
    for i in range(count):
        x, y = rnd.randrange(4, c.w - 4), rnd.randrange(34, 280)
        phase = rnd.randrange(6)
        t = (frame + phase) % 6
        if t in (0, 1):
            c.pset(x, y, SPARK)
            if i % 5 == 0 and t == 0:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    c.pset(x + dx, y + dy, SPARK_DIM)
        elif t in (2, 3):
            c.pset(x, y, SPARK_DIM)
