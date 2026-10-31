"""SIBLINGS BE LIKE - 12 s vertical loop.

0:00-0:01  caption, Zack and Pip at a table, paper between them
0:01-0:04  paper insert: X and O traded with snappy moves
0:04-0:06  Pip (O) has a fork. Zack pauses, eyes slide off to the side
0:06-0:08  Zack draws a BIG X in the margin, writes WIN!, points. Held.
0:08-0:10  Pip close-up: blank... then angry. Shake, red tint, fire.
0:10-0:12  hard cut to the opening frame (loops)

Art runs at 12 fps; 1 s = 12 art frames.
"""
from pixelshort import cast, backgrounds as bg, effects as fx
from pixelshort.canvas import hex_rgb as H, stroke, ring
from pixelshort.font import draw_text, text_width
from pixelshort import audio as au

CAPTION = "siblings be like"
SECONDS = 12
X_RED, X_RED_D = H("#e23a48"), H("#8e1e30")
O_BLUE = H("#3a5ad0")
CAP_FILL, CAP_BORDER = H("#ffffff"), H("#141026")

# Pip (O) goes first. After 5 moves O has a fork: column 0 and row 1.
#   O X .
#   O O .
#   . . X
MOVES = [("O", 0, 0), ("X", 0, 1), ("O", 1, 1), ("X", 2, 2), ("O", 1, 0)]
MOVE_START = [13, 20, 27, 34, 41]          # art frames
MOVE_LEN = 7

# ---------------------------------------------------------------------------
# timeline (art frames)
SHOTS = [
    ("wide_open", 0, 12),
    ("game", 12, 48),
    ("wide_fork", 48, 57),
    ("zack_cu", 57, 72),
    ("margin", 72, 96),
    ("pip_cu", 96, 120),
    ("wide_open", 120, 144),
]
ANGRY_AT = 108


class Art:
    def __init__(self):
        self.zack = {f: cast.zack(f) for f in ("normal", "deadpan")}
        self.zack_squash = {f: cast.zack(f, "squash") for f in ("normal", "deadpan")}
        self.pip = {f: cast.pip(f) for f in cast.PIP_FACES}
        self.zack_cu = {f: cast.zack_closeup(f, h=240) for f in ("normal", "side1", "side2", "whistle")}
        self.pip_cu = {f: cast.pip_closeup(f, h=240) for f in ("blank", "angry")}
        self.arm_zack_pen = cast.arm("zack", "pen", 240)
        self.arm_zack_point = cast.arm("zack", "point", 240)
        self.arm_pip_pen = cast.arm("pip", "pen", 240)


A = None


def caption(c):
    draw_text(c, CAPTION, (c.w - text_width(CAPTION)) // 2, 40, fill=CAP_FILL, border=CAP_BORDER)


# ---------------------------------------------------------------------------
# board state
def move_progress(i, f):
    """0..1 drawing progress of move i at art frame f (snappy: 4 frames)."""
    s = MOVE_START[i]
    return max(0.0, min(1.0, (f - s) / 4.0))


def board_at(f):
    if f >= MOVE_START[-1] + MOVE_LEN:
        return [(m, 1.0) for m in MOVES]
    return [(m, move_progress(i, f)) for i, m in enumerate(MOVES) if f > MOVE_START[i]]


# ---------------------------------------------------------------------------
# paper insert (top-down, close)
GX, GY, CELL = 70, 100, 28
MARGIN_X = 58
MX, MY, MH = 36, 142, 14     # big margin X: centre and half-size


def cell_center(r, col):
    return GX + CELL // 2 + CELL * col, GY + CELL // 2 + CELL * r


def draw_paper(c):
    shadow = H("#a8643a")
    c.rect(16, 55, 152, 220, shadow)
    c.rect(14, 52, 152, 220, bg.PAPER)
    for y in range(70, 270, 10):
        c.hline(14, y, 152, bg.PAPER_RULE)
    c.rect(MARGIN_X, 52, 2, 220, bg.PAPER_MARGIN)
    for hy in (78, 160, 242):           # punch holes
        c.rect(20, hy, 5, 5, bg.TABLE_TOP)
        c.rect(20, hy, 5, 1, bg.TABLE_GRAIN)
    for k in (1, 2):                    # pencil grid
        c.rect(GX + CELL * k - 1, GY + 2, 2, CELL * 3 - 4, bg.PENCIL)
        c.rect(GX + 2, GY + CELL * k - 1, CELL * 3 - 4, 2, bg.PENCIL)


def x_mark(c, cx, cy, half, p, r=1, under=None):
    """Two strokes; returns the pen tip position."""
    p1, p2 = min(1, p * 2), max(0, p * 2 - 1)
    for col, rr in ((under, r + 1), (X_RED, r)):
        if col is None:
            continue
        stroke(c, cx - half, cy - half, cx + half, cy + half, col, rr, p1)
        if p2 > 0:
            stroke(c, cx + half, cy - half, cx - half, cy + half, col, rr, p2)
    if p2 > 0:
        return (int(cx + half - 2 * half * p2), int(cy - half + 2 * half * p2))
    return (int(cx - half + 2 * half * p1), int(cy - half + 2 * half * p1))


def o_mark(c, cx, cy, p):
    import math
    ring(c, cx, cy, 10.5, 7, O_BLUE, p)
    a = math.radians(-90 + 360 * p)
    return (int(cx + 9 * math.cos(a)), int(cy + 9 * math.sin(a)))


# "WIN!" hand-lettered in the same marker strokes as the X: big and readable
WIN_STROKES = [
    [(0, 0), (2, 13), (5, 5), (8, 13), (10, 0)],     # W
    [(15, 0), (15, 13)],                               # I
    [(20, 13), (20, 0), (28, 13), (28, 0)],            # N
    [(33, 0), (33, 8)], [(33, 12), (33, 13)],          # !
]


def hand_win(c, x, y, p):
    segs = [(a, b) for poly in WIN_STROKES for a, b in zip(poly, poly[1:])]
    k = int(round(len(segs) * p))
    for col, r in ((X_RED_D, 2), (X_RED, 1)):
        for (x0, y0), (x1, y1) in segs[:k]:
            stroke(c, x + x0, y + y0, x + x1, y + y1, col, r)


def blit_arm(c, arm, tip, out=0, flip_side=1):
    spr, (tx, ty) = arm
    c.blit(spr, tip[0] - tx - out * flip_side, tip[1] - ty + out)


def shot_game(f):
    c = bg.table_top_closeup()
    draw_paper(c)
    tip, who = None, None
    for i, ((m, r, col), p) in enumerate(board_at(f)):
        cx, cy = cell_center(r, col)
        t = x_mark(c, cx, cy, 8, p) if m == "X" else o_mark(c, cx, cy, p)
        s = MOVE_START[i]
        if s < f <= s + 5:
            tip, who, out = t, m, (0 if f <= s + 4 else 70)   # snap away
    if tip:
        if who == "X":
            blit_arm(c, A.arm_zack_pen, tip, out, 1)
        else:
            blit_arm(c, A.arm_pip_pen, tip, out, -1)
    caption(c)
    return c


def shot_margin(f):
    c = bg.table_top_closeup()
    draw_paper(c)
    for (m, r, col), _ in board_at(f):
        cx, cy = cell_center(r, col)
        x_mark(c, cx, cy, 8, 1) if m == "X" else o_mark(c, cx, cy, 1)
    p = max(0.0, min(1.0, (f - 73) / 8.0))           # deliberate: 8 frames
    tip = x_mark(c, MX, MY, MH, p, r=2, under=X_RED_D) if p > 0 else (MX - MH, MY - MH)
    if f >= 80:
        hand_win(c, 20, MY - MH - 22, 1.0 if f >= 81 else 0.5)
    if f < 82:
        blit_arm(c, A.arm_zack_pen, tip if f >= 73 else (MX - MH + 6, MY - MH + 30))
    else:
        bob = (f // 3) % 2                               # proud point, held
        blit_arm(c, A.arm_zack_point, (MX + MH + 3 + bob, MY + MH + 3 + bob))
    caption(c)
    return c


# ---------------------------------------------------------------------------
# wide shots
ZACK_X, ZACK_Y = 30, 133
PIP_X, PIP_Y = 128, 131


def mini_board(c, f, final=False):
    ty = bg.TABLE_Y + 4
    c.rect(66, ty, 48, 22, bg.PAPER)
    c.vline(76, ty, 22, bg.PAPER_MARGIN)
    for x in (90, 98):
        c.vline(x, ty + 2, 18, bg.PENCIL)
    for y in (ty + 8, ty + 14):
        c.hline(82, y, 24, bg.PENCIL)
    moves = MOVES if final else [m for (m, p) in board_at(f) if p >= 1]
    for m, r, col in moves:
        x, y = 85 + 8 * col, ty + 4 + 6 * r
        if m == "X":
            for k in range(3):
                c.pset(x + k, y + k, X_RED)
                c.pset(x + 2 - k, y + k, X_RED)
        else:
            c.rect(x, y, 3, 3, O_BLUE)
            c.pset(x + 1, y + 1, bg.PAPER)


def wide(f, pip_face="normal", zack_face="normal", board_final=False, blank=False):
    c = bg.home()
    bg.chair_back(c, ZACK_X + 8)
    bg.chair_back(c, PIP_X + 11)
    breath = (f // 6) % 2
    z = A.zack_squash[zack_face] if breath else A.zack[zack_face]
    c.blit(z, ZACK_X, ZACK_Y + breath)
    pf = pip_face
    if pf == "normal" and f % 36 in (30, 31):
        pf = "blink"
    c.blit(A.pip[pf], PIP_X, PIP_Y + (1 - breath))
    bg.table(c)
    if blank:
        mini_board(c, -1)
    else:
        mini_board(c, f, final=board_final)
    caption(c)
    return c


def shot_wide_open(f):
    return wide(f, blank=True)


def shot_wide_fork(f):
    return wide(f, pip_face="smug", board_final=True)


def shot_zack_cu(f):
    c = bg.closeup_wall()
    face = "normal" if f < 63 else "side1" if f < 65 else "side2" if f < 68 else "whistle"
    spr = A.zack_cu[face]
    c.blit(spr, (c.w - spr.w) // 2, 92)
    caption(c)
    return c


def shot_pip_cu(f):
    c = bg.closeup_wall()
    angry = f >= ANGRY_AT
    spr = A.pip_cu["angry" if angry else "blank"]
    c.blit(spr, (c.w - spr.w) // 2, 92)
    if angry:
        # optional payoff from the last short: fire rising in front of him
        fx.fire_row(c, f, floor_y=304, height=min(1.0, (f - ANGRY_AT) / 8), spacing=9, seed=5)
        fx.steam_puffs(c, f, 58, 104)
        fx.steam_puffs(c, f + 5, 122, 104)
        c.tint(fx.ANGER_RED, fx.tint_ramp(f, ANGRY_AT, frames=6))
        c.shake(*fx.shake_offset(f))
    caption(c)
    return c


DRAW = {
    "wide_open": lambda f, s: shot_wide_open(f - s),
    "game": lambda f, s: shot_game(f),
    "wide_fork": lambda f, s: shot_wide_fork(f),
    "zack_cu": lambda f, s: shot_zack_cu(f),
    "margin": lambda f, s: shot_margin(f),
    "pip_cu": lambda f, s: shot_pip_cu(f),
}


def frames(watermark=None):
    global A
    A = Art()
    for name, start, end in SHOTS:
        for f in range(start, end):
            c = DRAW[name](f, start)
            if watermark:
                draw_text(c, watermark, c.w - 4 - text_width(watermark), c.h - 14,
                          fill=H("#c8c0e0"), border=H("#1a1436"))
            yield c


# ---------------------------------------------------------------------------
# audio
def T(frame):
    return frame / 12.0


def soundtrack(path):
    tr = au.Track(SECONDS)

    # -- music: 120 bpm, 2 s bars. A at 0-2, B at 2-4, B again at 10-12 so the
    #    loop runs B -> A seamlessly.
    bars = {
        "A": (["E5", "G5", "E5", "C5", "D5", "E5", "G5", None],
              ["C3", "G2", "C3", "G2"]),
        "B": (["A5", "G5", "E5", "C5", "D5", "B4", "C5", None],
              ["F2", "C3", "G2", "G2"]),
    }

    def bar(t0, name):
        lead, bass = bars[name]
        for i, n in enumerate(lead):
            if n:
                tr.add(t0 + i * 0.25, au.square(au.hz(n), 0.2, duty=0.25, vol=0.07),
                       au.env(int(au.SR * 0.2), release=0.05))
        for i, n in enumerate(bass):
            tr.add(t0 + i * 0.5, au.tri(au.hz(n), 0.42, vol=0.2))
        for i in range(8):
            tr.add(t0 + i * 0.25, au.noise(0.025, vol=0.035, seed=i), au.env(int(au.SR * 0.025), 0.001, 0.02))
        for i in (0, 2):
            tr.add(t0 + i * 0.5, au.sine(110, 0.12, vol=0.3, slide_to=45))

    bar(0, "A")
    bar(2, "B")
    bar(10, "B")

    # -- pen strokes: scribble while drawing, pop when a mark lands
    def scribble(t, dur, rate, vol, seed, lp=None):
        n = au.noise(dur, vol=vol, seed=seed, lowpass=lp)
        am = (0.5 + 0.5 * __import__("numpy").sign(__import__("numpy").sin(
            2 * 3.14159 * rate * au._t(dur)))).astype("float32")
        tr.add(t, n * am, au.env(len(n), 0.005, 0.02))

    for i, (m, _, _) in enumerate(MOVES):
        s = MOVE_START[i]
        if m == "X":
            scribble(T(s + 1), 0.15, 16, 0.16, i, lp=2500)
            scribble(T(s + 3), 0.15, 16, 0.16, i + 10, lp=2500)
        else:
            scribble(T(s + 1), 0.3, 26, 0.12, i, lp=1800)
        tr.add(T(s + 5), au.square(au.hz("C6") if m == "X" else au.hz("G5"), 0.05, vol=0.07))

    # -- 0:04 record scratch, music stops; Pip's smug "heh heh"
    tr.add(T(48), au.square(700, 0.22, duty=0.3, vol=0.12, slide_to=120) + au.noise(0.22, vol=0.12, seed=3))
    for k in range(2):
        tr.add(T(50) + k * 0.16, au.square(au.hz("E6"), 0.06, duty=0.25, vol=0.07))
        tr.add(T(50) + k * 0.16 + 0.07, au.square(au.hz("C6"), 0.06, duty=0.25, vol=0.07))

    # -- awkward silence: crickets, eyes slide, innocent whistle
    import numpy as np
    for t0 in (T(58), T(61)):
        for k in range(3):
            chirp = au.sine(4300, 0.03, vol=0.06)
            tr.add(t0 + k * 0.055, chirp, au.env(len(chirp), 0.003, 0.01))
    tr.add(T(63), au.tri(700, 0.18, vol=0.12, slide_to=380))
    for k, (n, d) in enumerate((("E6", 0.12), ("G6", 0.12), ("E6", 0.22))):
        tr.add(T(68) + [0, 0.13, 0.26][k], au.sine(au.hz(n), d, vol=0.12, vibrato=0.012),
               au.env(int(au.SR * d), 0.02, 0.04))

    # -- 0:06 the margin X: two big deliberate strokes, then ta-da
    scribble(T(73), 0.33, 11, 0.22, 40, lp=1500)
    scribble(T(77), 0.33, 11, 0.22, 41, lp=1500)
    for k, n in enumerate(("C5", "E5", "G5")):
        tr.add(T(81) + k * 0.07, au.square(au.hz(n), 0.07, duty=0.25, vol=0.1))
    for n in ("C6", "G5", "E5"):
        tr.add(T(81) + 0.21, au.square(au.hz(n), 0.5, duty=0.25, vol=0.06),
               au.env(int(au.SR * 0.5), release=0.25))

    # -- 0:08 blank stare (silence, one blink tick) then 0:09 anger
    tr.add(T(102), au.noise(0.02, vol=0.08, seed=9))
    tr.add(T(ANGRY_AT), au.sine(150, 0.6, vol=0.55, slide_to=32))
    tr.add(T(ANGRY_AT), au.noise(0.5, vol=0.35, seed=5, lowpass=500))
    tr.add(T(ANGRY_AT) + 0.05, au.square(230, 0.85, duty=0.3, vol=0.1, slide_to=120, vibrato=0.05),
           au.env(int(au.SR * 0.85), 0.01, 0.2))
    rumble = au.noise(0.95, vol=0.22, seed=6, lowpass=160)
    tr.add(T(ANGRY_AT) + 0.05, rumble, au.env(len(rumble), 0.05, 0.3))
    rnd = np.random.default_rng(1)
    for k in range(10):   # fire crackle
        tr.add(T(ANGRY_AT) + 0.1 + rnd.uniform(0, 0.85), au.noise(0.015, vol=0.12, seed=20 + k))

    tr.write(path)
