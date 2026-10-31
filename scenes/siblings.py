"""SIBLINGS BE LIKE - 16.5 s vertical loop.

0:00-0:01  caption, Zack and Pip at a table, paper between them
0:01-0:04  paper insert: X and O traded with snappy moves. Pip (O) forks.
0:04-0:06  Pip smug. Zack pauses, eyes slide off to the side.
0:06-0:08  Zack draws an X in the margin, lined up with his two Xs on the
           bottom row -> "three in a row", and strikes the winning line.
0:08-0:10  Zack: "ez" + the L on his forehead.
0:10-0:12  Pip close-up: blank... then furious.
0:12-0:15  Pip sets the whole room on fire.
0:15-0:16  hard cut to the opening frame (loops).

Art runs at 12 fps; 1 s = 12 art frames.
"""
from pixelshort import cast, backgrounds as bg, effects as fx
from pixelshort.canvas import hex_rgb as H, stroke, ring
from pixelshort.font import draw_text, text_width
from pixelshort import audio as au
from pathlib import Path

ASSETS = Path(__file__).resolve().parents[1] / "assets" / "audio"
CAPTION = "siblings be like"
X_RED, X_RED_D = H("#e23a48"), H("#8e1e30")
O_BLUE = H("#3a5ad0")
CAP_FILL, CAP_BORDER = H("#ffffff"), H("#141026")

# Pip (O) goes first. After 5 moves O has a fork (diagonal and column 2) and
# X's only line - the bottom row - is blocked by an O. Unless...
#   . . O
#   . O .
#   X X O        <- X X X if you count the margin
MOVES = [("O", 1, 1), ("X", 2, 0), ("O", 0, 2), ("X", 2, 1), ("O", 2, 2)]
MOVE_START = [13, 20, 27, 34, 41]          # art frames
MOVE_LEN = 7

SHOTS = [
    ("wide_open", 0, 12),
    ("game", 12, 48),
    ("wide_fork", 48, 57),
    ("zack_cu", 57, 72),
    ("margin", 72, 102),
    ("zack_ez", 102, 126),
    ("pip_cu", 126, 150),
    ("room_fire", 150, 186),
    ("wide_open", 186, 198),
]
TOTAL = SHOTS[-1][2]
SECONDS = TOTAL / 12
EZ_AT = 104
ANGRY_AT = 138
FIRE_AT = 150


class Art:
    def __init__(self):
        self.zack = {f: cast.zack(f) for f in ("normal", "deadpan")}
        self.zack_squash = {f: cast.zack(f, "squash") for f in ("normal", "deadpan")}
        self.pip = {f: cast.pip(f) for f in cast.PIP_FACES}
        self.zack_cu = {f: cast.zack_closeup(f, h=240) for f in ("normal", "side1", "side2", "smug")}
        self.zack_l = cast.zack_l_hand(h=240)
        self.zack_shock = cast.zack("shock")
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
MX, MY, MH = 36, GY + CELL // 2 + CELL * 2, 12   # margin X, on the bottom row


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
    # 1) the X in the margin, lined up with his two Xs: deliberate, 8 frames
    p = max(0.0, min(1.0, (f - 73) / 8.0))
    tip = x_mark(c, MX, MY, MH, p, r=2, under=X_RED_D) if p > 0 else (MX - MH, MY - MH)
    # 2) the "winning" line straight through all three
    q = max(0.0, min(1.0, (f - 83) / 4.0))
    x0, x1 = MX - MH - 6, cell_center(2, 1)[0] + 12
    if q > 0:
        stroke(c, x0, MY, x1, MY, X_RED_D, 2, q)
        stroke(c, x0, MY, x1, MY, X_RED, 1, q)
        tip = (int(x0 + (x1 - x0) * q), MY)
    if f < 73:
        blit_arm(c, A.arm_zack_pen, (MX - MH + 6, MY - MH + 30))
    elif f <= 88:
        blit_arm(c, A.arm_zack_pen, tip)
    elif f <= 89:
        blit_arm(c, A.arm_zack_pen, tip, out=70)   # snap away, then hold the board
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
    face = "normal" if f < 63 else "side1" if f < 66 else "side2"
    spr = A.zack_cu[face]
    c.blit(spr, (c.w - spr.w) // 2, 92)
    caption(c)
    return c


def shot_zack_ez(f):
    c = bg.closeup_wall()
    x, y = (c.w - A.zack_cu["smug"].w) // 2, 92
    c.blit(A.zack_cu["smug"], x, y + ((f // 6) % 2))
    c.blit(A.zack_l, x, y + ((f // 6) % 2))
    if f >= EZ_AT:
        ez_bubble(c, 100, 52, pop=(f == EZ_AT))
    caption(c)
    return c


# big hand-lettered "ez" in a speech bubble: reads instantly on a phone
EZ_STROKES = [
    [(0, 9), (13, 9), (13, 4), (10, 0), (3, 0), (0, 4), (0, 13), (3, 17), (13, 17)],   # e
    [(19, 0), (32, 0), (19, 17), (32, 17)],                                           # z
]
BUBBLE, BUBBLE_EDGE, INK = H("#ffffff"), H("#141026"), H("#1e1a3a")


def ez_bubble(c, x, y, pop=False):
    g = 2 if pop else 0                                   # 1-frame pop-in
    w, h = 64 + g * 2, 38 + g * 2
    x, y = x - g, y - g
    c.rect(x + 2, y, w - 4, h, BUBBLE_EDGE)
    c.rect(x, y + 2, w, h - 4, BUBBLE_EDGE)
    c.rect(x + 3, y + 1, w - 6, h - 2, BUBBLE)
    c.rect(x + 1, y + 3, w - 2, h - 6, BUBBLE)
    for i in range(8):                                    # tail toward his head
        c.rect(x + 10 - i, y + h - 1 + i, 3 + (7 - i) // 2, 1, BUBBLE)
        c.pset(x + 9 - i, y + h - 1 + i, BUBBLE_EDGE)
        c.pset(x + 13 - i + (7 - i) // 2, y + h - 1 + i, BUBBLE_EDGE)
    ox, oy = x + 15 + g, y + 10 + g
    for poly in EZ_STROKES:
        for (x0, y0), (x1, y1) in zip(poly, poly[1:]):
            stroke(c, ox + x0, oy + y0, ox + x1, oy + y1, INK, 2)


def shot_room_fire(f):
    """Pip sets the room on fire: it bursts out from him and spreads to the
    floor, the table, the curtains and up the walls."""
    t = f - FIRE_AT
    spread = min(1.0, t / 10)                      # 0 -> 1 over ~0.8 s
    c = bg.home()
    pcx = PIP_X + 11
    reach = int(20 + spread * 180)
    # back wall line, curtains and wall climbing flames
    fx.fire_row(c, f, floor_y=bg.FLOOR_Y + 2, height=spread, x0=max(0, pcx - reach),
                x1=min(c.w, pcx + reach), spacing=10, seed=2)
    if t >= 4:
        for cx0 in (58, 113):
            fx.fire_row(c, f + cx0, floor_y=112, height=min(1.0, (t - 4) / 8), x0=cx0,
                        x1=cx0 + 9, spacing=9, seed=cx0)
    bg.chair_back(c, ZACK_X + 8)
    bg.chair_back(c, PIP_X + 11)
    c.blit(A.zack_shock, ZACK_X - min(8, t // 2), ZACK_Y)
    c.blit(A.pip["angry"], PIP_X, PIP_Y)
    fx.steam_puffs(c, f, pcx, PIP_Y - 1)
    bg.table(c)
    mini_board(c, f, final=True)
    # flames on the table top, then the floor in front, rising
    fx.fire_row(c, f + 2, floor_y=bg.TABLE_Y + 14, height=min(1.0, t / 8) * 0.7,
                x0=max(10, pcx - reach // 2), x1=min(170, pcx + reach // 2), spacing=12, seed=6)
    for i, fy in enumerate((240, 292)):
        if t >= 2 + i * 3:
            fx.fire_row(c, f + i, floor_y=fy, height=min(1.0, (t - 2 - i * 3) / 8) * 0.67,
                        spacing=11, seed=10 + i)
    c.tint(fx.ANGER_RED, 0.26)
    c.shake(*fx.shake_offset(f, amp=2, seed=31))
    caption(c)
    return c


def shot_pip_cu(f):
    c = bg.closeup_wall()
    angry = f >= ANGRY_AT
    spr = A.pip_cu["angry" if angry else "blank"]
    c.blit(spr, (c.w - spr.w) // 2, 92)
    if angry:   # the fire starts: flames lick up from the bottom of frame
        fx.fire_row(c, f, floor_y=304, height=min(1.0, (f - ANGRY_AT) / 10) * 0.6, spacing=9, seed=5)
        fx.steam_puffs(c, f, 58, 104)
        fx.steam_puffs(c, f + 5, 122, 104)
        c.tint(fx.ANGER_RED, fx.tint_ramp(f, ANGRY_AT, frames=6))
        c.shake(*fx.shake_offset(f))
    caption(c)
    return c


DRAW = {
    "wide_open": lambda f, s: shot_wide_open(f - s if s == 0 else f - s + 12),
    "game": lambda f, s: shot_game(f),
    "wide_fork": lambda f, s: shot_wide_fork(f),
    "zack_cu": lambda f, s: shot_zack_cu(f),
    "margin": lambda f, s: shot_margin(f),
    "pip_cu": lambda f, s: shot_pip_cu(f),
    "zack_ez": lambda f, s: shot_zack_ez(f),
    "room_fire": lambda f, s: shot_room_fire(f),
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


# Music: two generated chiptune tracks (assets/audio/README.md).
PLAYFUL_IN = 2.0     # where the playful track is cued from
RAGE_IN = 9.0        # the rage track's full-intensity section


def soundtrack(path):
    import numpy as np
    tr = au.Track(SECONDS)
    playful = au.load(str(ASSETS / "music_playful_chiptune.wav"))
    rage = au.load(str(ASSETS / "music_rage_chiptune.wav"))

    # -- playful music. The closing second (reset to the opening frame) plays
    #    PLAYFUL_IN..+1 s, and 0:00 picks up exactly where that leaves off, so
    #    the loop point is seamless. Hard stop at 0:04 with a record scratch.
    tail = T(TOTAL) - T(SHOTS[-1][1])
    tr.add(T(SHOTS[-1][1]), au.clip(playful, PLAYFUL_IN, tail, fade_in=0.02, fade_out=0.0),
           np.ones(int(tail * au.SR), dtype="float32"), gain=0.8)
    tr.add(0, au.clip(playful, PLAYFUL_IN + tail, 4.0, fade_out=0.03),
           np.ones(int(4.0 * au.SR), dtype="float32"), gain=0.8)

    # -- pen strokes: scribble while drawing, pop when a mark lands
    def scribble(t, dur, rate, vol, seed, lp=None):
        n = au.noise(dur, vol=vol, seed=seed, lowpass=lp)
        am = (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * rate * au._t(dur)))).astype("float32")
        tr.add(t, n * am, au.env(len(n), 0.005, 0.02))

    for i, (m, _, _) in enumerate(MOVES):
        s = MOVE_START[i]
        if m == "X":
            scribble(T(s + 1), 0.15, 16, 0.16, i, lp=2500)
            scribble(T(s + 3), 0.15, 16, 0.16, i + 10, lp=2500)
        else:
            scribble(T(s + 1), 0.3, 26, 0.12, i, lp=1800)
        tr.add(T(s + 5), au.square(au.hz("C6") if m == "X" else au.hz("G5"), 0.05, vol=0.06))

    # -- 0:04 record scratch, music stops; Pip's smug "heh heh"
    tr.add(T(48), au.square(700, 0.22, duty=0.3, vol=0.12, slide_to=120) + au.noise(0.22, vol=0.12, seed=3))
    for k in range(2):
        tr.add(T(50) + k * 0.16, au.square(au.hz("E6"), 0.06, duty=0.25, vol=0.07))
        tr.add(T(50) + k * 0.16 + 0.07, au.square(au.hz("C6"), 0.06, duty=0.25, vol=0.07))

    # -- awkward silence: crickets, eyes slide
    for t0 in (T(58), T(62), T(67)):
        for k in range(3):
            chirp = au.sine(4300, 0.03, vol=0.06)
            tr.add(t0 + k * 0.055, chirp, au.env(len(chirp), 0.003, 0.01))
    tr.add(T(63), au.tri(700, 0.25, vol=0.12, slide_to=380))

    # -- 0:06 margin X (two slow strokes), the winning line, a win jingle
    scribble(T(73), 0.33, 11, 0.22, 40, lp=1500)
    scribble(T(77), 0.33, 11, 0.22, 41, lp=1500)
    swoosh = au.noise(0.33, vol=0.25, seed=42, lowpass=3000)
    tr.add(T(83), swoosh, au.env(len(swoosh), 0.01, 0.15))
    for k, n in enumerate(("C5", "E5", "G5")):
        tr.add(T(88) + k * 0.07, au.square(au.hz(n), 0.07, duty=0.25, vol=0.1))
    for n in ("C6", "G5", "E5"):
        tr.add(T(88) + 0.21, au.square(au.hz(n), 0.5, duty=0.25, vol=0.06),
               au.env(int(au.SR * 0.5), release=0.25))

    # -- 0:08 "ez": two 8-bit talk blips as the bubble pops, then a smug sting
    for k, n in enumerate(("A5", "E5")):
        tr.add(T(EZ_AT) + k * 0.11, au.square(au.hz(n), 0.07, duty=0.25, vol=0.12))
    tr.add(T(EZ_AT) + 0.9, au.square(au.hz("G5"), 0.08, duty=0.25, vol=0.06))
    tr.add(T(EZ_AT) + 1.0, au.square(au.hz("C6"), 0.18, duty=0.25, vol=0.06))

    # -- 0:10 blank stare (dead silence, one blink tick), then rage
    tr.add(T(132), au.noise(0.02, vol=0.08, seed=9))
    tr.add(T(ANGRY_AT), au.sine(150, 0.6, vol=0.55, slide_to=32))
    tr.add(T(ANGRY_AT), au.noise(0.5, vol=0.35, seed=5, lowpass=500))
    rage_len = T(SHOTS[-1][1]) - T(ANGRY_AT)
    tr.add(T(ANGRY_AT) + 0.1, au.clip(rage, RAGE_IN, rage_len - 0.1, fade_in=0.01, fade_out=0.02),
           np.ones(int((rage_len - 0.1) * au.SR), dtype="float32"), gain=0.9)
    # -- 0:12 the room goes up: whoosh + crackle under the music
    whoosh = au.noise(0.8, vol=0.4, seed=7, lowpass=900)
    tr.add(T(FIRE_AT), whoosh, au.env(len(whoosh), 0.02, 0.5))
    rnd = np.random.default_rng(1)
    for k in range(40):
        tr.add(T(FIRE_AT) + rnd.uniform(0, 2.9), au.noise(0.015, vol=0.14, seed=20 + k))

    tr.write(path)
