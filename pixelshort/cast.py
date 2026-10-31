"""Original characters and effect sprites, authored as ASCII grids.

Each character keeps a small palette: base / shadow / highlight per colour
area, plus one or two accent colours that pop.

Cast:
  ZACK - dark skin, black hair, black suit, white shirt, red tie (accent).
  PIP  - a penguin who is almost always in a suit: royal-blue jacket,
         yellow bow tie and orange beak/feet as accents.
"""
from .sprite import Sprite


def mirror(left_half, swap=None):
    """Build symmetric rows from left halves. `swap` remaps keys on the right
    half so highlights on the lit (left) side become shadows on the right."""
    swap = swap or {}
    rows = []
    for r in left_half:
        right = "".join(swap.get(ch, ch) for ch in reversed(r))
        rows.append(r + right)
    return rows


# --------------------------------------------------------------------------
# ZACK - big head, black hair, dark skin, black suit. Faces 3/4 right.
# --------------------------------------------------------------------------
ZACK_PAL = {
    "h": "#26222e", "H": "#4c4662", "d": "#17131f",          # black hair
    "s": "#8a5638", "S": "#683e28", "x": "#a26a48",          # dark skin
    "e": "#120e22",                                          # eyes
    "m": "#3e1e16",                                          # mouth
    "j": "#2e2c3c", "J": "#1e1c2a", "K": "#4a4860",          # black suit
    "w": "#f4f2ea", "W": "#c8c4d0",                          # shirt
    "r": "#e23a48", "R": "#a42438",                          # tie (accent)
    "p": "#2e2c3c", "P": "#1e1c2a",                          # trousers
    "b": "#2c2632", "B": "#5a5470",                          # dress shoes
    "u": "#8fd8ff",                                          # sweat drop
}

_ZACK_HEAD_TOP = [
    "....hhhhhh....",
    "..hhHHHHhhhh..",
    ".hhHHhhhhhhhh.",
    ".hhhhhhhhhhhhh",
    "dhhhhhhhhhhhhh",
    "dhhhhhxxxxxxxx",
    "dhhSssssssssss",
]
# rows 7-11: the face. Expressions swap these rows whole, never morph.
ZACK_FACES = {
    "normal": [
        "dhSSsssesssess",
        "dSxSsssesssess",
        ".dSSssssssssss",
        "..SSSssssmmss.",
        "...SSSsssssss.",
    ],
    "blink": [
        "dhSSssssssssss",
        "dSxSsseesseess",
        ".dSSssssssssss",
        "..SSSssssmmss.",
        "...SSSsssssss.",
    ],
    "deadpan": [
        "dhSSssSSssSSss",
        "dSxSsseesseess",
        ".dSSssssssssss",
        "..SSSsssmmmss.",
        "...SSSsssssss.",
    ],
    "happy": [
        "dhSSsssesssess",
        "dSxSsseseseses",
        ".dSSssssssssss",
        "..SSSssmmmmss.",
        "...SSSsssssss.",
    ],
    "shock": [
        "dhSSsseesseess",
        "dSxSsseesseess",
        ".dSSssssssssuu",
        "..SSSssssmmsu.",
        "...SSSsssmmss.",
    ],
}

_ZACK_BODY = [
    "....SSSSSS....",
    "...jKwrRwKj...",
    "..JjjKwrRKjj..",
    "..JjjjKrRjjj..",
    "..JjjjjRjjKj..",
    "..sJjjjjjjJs..",
    "...JJJJJJJJ...",
    "...pppppppp...",
]
ZACK_LEGS = {
    "stand": [
        "...pPp..pPp...",
        "...pPp..pPp...",
        "...pPp..pPp...",
        "..bBbb.bBbbb..",
    ],
    "squash": [  # one row shorter: upper body dips 1 px (idle breath)
        "...pPp..pPp...",
        "...pPp..pPp...",
        "..bBbb.bBbbb..",
    ],
    "stride_a": [
        "...pPpppPpp...",
        "..pPp...pPp...",
        ".pPp.....pPp..",
        "bBbb.....bBbbb",
    ],
    "pass": [  # one row taller: upper body rises 1 px
        "....pPppPp....",
        "....pPppPp....",
        "....pPppPp....",
        "....pPppPp....",
        "....bBbbbbb...",
    ],
    "stride_b": [
        "...ppPpPpPp...",
        "..PpP...pPp...",
        ".PpP.....pPp..",
        "bbbb.....bBbbb",
    ],
}


def zack(face="normal", legs="stand", rim=None):
    rows = _ZACK_HEAD_TOP + ZACK_FACES[face] + _ZACK_BODY + ZACK_LEGS[legs]
    s = Sprite.from_rows(rows, ZACK_PAL)
    return s.rimmed(rim) if rim else s


ZACK_WALK = ["stride_a", "pass", "stride_b", "pass"]  # 4-frame walk cycle
ZACK_IDLE = ["stand", "squash"]                       # 2-pose breath


# --------------------------------------------------------------------------
# PIP - a penguin in a suit. Front-facing, drawn as left halves + mirror.
# --------------------------------------------------------------------------
PIP_PAL = {
    "b": "#2a2c48", "B": "#1c1c34", "v": "#4c5080",          # feathers
    "w": "#f4f4fa", "W": "#c8cce0",                          # white face/belly
    "o": "#ffa030", "O": "#d0701e",                          # beak & feet (accent)
    "e": "#10101e",                                          # eyes
    "u": "#3a5ad0", "U": "#28398e", "V": "#6e8ef2",          # blue suit jacket
    "y": "#ffd84a", "Y": "#d8962a",                          # bow tie (accent)
    "k": "#ffd84a",                                          # jacket button
    "z": "#8fd8ff",                                          # sweat
}
_PIP_SWAP = {"v": "B", "V": "U"}  # right half = shadow side

_PIP_TOP = [
    "......bbbb",
    "....bbbbbb",
    "...bvvbbbb",
    "..bvvbbbbb",
    "..bvbbbbww",
    ".bvbbwwwww",
]
PIP_FACES = {  # rows 6-10 (left halves)
    "normal": [
        ".bvbwwwwww",
        ".bbwwwewww",
        ".bbwwwewww",
        ".bbwwwwwoo",
        ".bbbwwwwOO",
    ],
    "blink": [
        ".bvbwwwwww",
        ".bbwwwwwww",
        ".bbwwweeww",
        ".bbwwwwwoo",
        ".bbbwwwwOO",
    ],
    "deadpan": [
        ".bvbwwwwww",
        ".bbwwbbbww",
        ".bbwwweeww",
        ".bbwwwwwoo",
        ".bbbwwwwOO",
    ],
    "smug": [
        ".bvbwwwwww",
        ".bbwwwewww",
        ".bbwweweww",
        ".bbwwwwwoo",
        ".bbbwwwwOO",
    ],
    "angry": [
        ".bvbeewwww",
        ".bbwwweeww",
        ".bbwwwewww",
        ".bbwwwwooo",
        ".bbbwwwOee",
    ],
}
_PIP_SUIT = [
    "..bbbwwwww",
    "..ubbbwwww",
    ".uVuubwyyy",
    ".uVuuuwyYY",
    "uuVuuuuwyy",
    "uVuuuuuwww",
    "uVuuuuuuww",
    "uVuuuuukww",
    "bVuuuuuuww",
    ".uuuuuuuww",
    ".uuuuuukww",
    ".UUUuuuuuw",
    "..UUUUUUUU",
    "..bbbbwwww",
    "...bbbwwww",
    "...oooOo..",
]


def pip(face="normal", suit=True):
    left = _PIP_TOP + PIP_FACES[face] + (_PIP_SUIT if suit else [
        r.replace("u", "b").replace("U", "B").replace("V", "v")
         .replace("y", "w").replace("Y", "w").replace("k", "w")
        for r in _PIP_SUIT])
    return Sprite.from_rows(mirror(left, _PIP_SWAP), PIP_PAL)


# --------------------------------------------------------------------------
# EFFECTS
# --------------------------------------------------------------------------
FIRE_PAL = {"c": "#fff4b8", "o": "#ff9a2a", "r": "#e2342c"}
FLAME_FRAMES = [
    [
        "....r....",
        "...rr....",
        "...ror...",
        "..roor...",
        "..rooor..",
        ".roocoor.",
        ".roccoor.",
        "roocccoor",
        "roccccorr",
        ".roccorr.",
    ],
    [
        ".....r...",
        ".....rr..",
        "....ror..",
        "...roor..",
        "..rooor..",
        "..rocoor.",
        ".roccoor.",
        ".rocccorr",
        "roccccor.",
        ".rocccor.",
    ],
    [
        "...r.....",
        "..rr..r..",
        "..ror.rr.",
        ".roorror.",
        ".rooooor.",
        ".roocoor.",
        "rooccoor.",
        "roccccor.",
        "roccccorr",
        ".roccor..",
    ],
]


def flames():
    out = []
    for rows in FLAME_FRAMES:
        w = max(len(r) for r in rows)
        rows = [r.ljust(w, ".") for r in rows]
        out.append(Sprite.from_rows(rows, FIRE_PAL, outline=False))
    return out


STEAM_PAL = {"w": "#f4f4ff", "W": "#c4c8e8"}
STEAM_FRAMES = [
    [".ww.", "wwwW", ".WW."],
    ["..ww..", ".wwwww", "wwwwWW", ".WWWW."],
    ["..w.w.", ".w...w", "W.....", ".W..W."],
]


def steam():
    out = []
    for rows in STEAM_FRAMES:
        w = max(len(r) for r in rows)
        rows = [r.ljust(w, ".") for r in rows]
        out.append(Sprite.from_rows(rows, STEAM_PAL, outline=False))
    return out


def pip_closeup(face="angry", w=128, h=150):
    """Big Pip head and shoulders for close-ups, built from flat shapes but
    run through the same palette + auto-outline pipeline as every sprite."""
    from .shapes import Grid
    G = Grid(w, h)
    cx = 64
    # shoulders: blue suit jacket, white shirt, yellow bow tie
    jacket = G.ellipse_mask(cx, 128, 58, 26) | ((G.y > 128) & (abs(G.x - cx) < 58))
    G.fill(jacket & (G.y > 96), "u")
    G.fill(jacket & (G.y > 96) & (G.x < cx - 46), "V")
    G.fill(jacket & (G.y > 96) & (G.x > cx + 46), "U")
    shirt = (G.y > 100) & (abs(G.x - cx) < 22 - (G.y - 100) * 0.25)
    G.fill(shirt, "w")
    for i in range(12):  # bow tie: two flat triangles and a knot
        hgt = 6 + i
        G.rect(cx - 6 - i, 110 - hgt // 2, 1, hgt, "y")
        G.rect(cx + 5 + i, 110 - hgt // 2, 1, hgt, "y")
    G.rect(cx - 17, 110 - 8, 2, 17, "Y")
    G.rect(cx + 15, 110 - 8, 2, 17, "Y")
    G.rect(cx - 5, 105, 10, 10, "Y")
    G.rect(cx - 1, 128, 3, 3, "k")
    G.rect(cx - 1, 140, 3, 3, "k")
    # head: dark round head, highlight upper-left, shadow lower-right
    head = G.ellipse_mask(cx, 58, 50, 46)
    G.fill(head, "b")
    G.fill(head & ~G.ellipse_mask(cx - 6, 52, 50, 46), "B")
    G.ellipse(34, 30, 10, 6, "v")
    G.ellipse(26, 42, 3, 5, "v")
    # white face mask: two lobes meeting under the beak
    mask = (G.ellipse_mask(cx - 16, 66, 22, 28) | G.ellipse_mask(cx + 16, 66, 22, 28)) & head
    G.fill(mask, "w")
    G.fill(mask & (G.x > cx + 30) & (G.y > 70), "W")
    if face == "angry":
        G.line(30, 44, 52, 56, "e", r=2)            # brows slam down
        G.line(98, 44, 76, 56, "e", r=2)
        G.rect(40, 58, 10, 12, "e")                 # eyes with a shine
        G.rect(78, 58, 10, 12, "e")
        G.rect(41, 59, 3, 3, "w")
        G.rect(79, 59, 3, 3, "w")
        # open beak, yelling
        G.ellipse(cx, 80, 16, 6, "o")
        G.rect(cx - 16, 80, 32, 2, "O")
        G.ellipse(cx, 88, 12, 6, "e")
        G.ellipse(cx, 92, 10, 3, "O")
        G.ellipse(cx, 96, 14, 4, "o")
        # anger mark: four little corner brackets
        mx, my = 92, 26
        for sx in (-1, 1):
            for sy in (-1, 1):
                G.rect(mx + (sx > 0) * 3 - (sx < 0) * 6, my + sy * 2 - (sy < 0) * 1, 5, 2, "R")
                G.rect(mx + sx * 2 - (sx < 0) * 1, my + (sy > 0) * 3 - (sy < 0) * 6, 2, 5, "R")
    elif face == "blank":
        # nothing behind the eyes: two dots, beak shut
        G.rect(44, 62, 6, 6, "e")
        G.rect(78, 62, 6, 6, "e")
        G.ellipse(cx, 82, 14, 5, "o")
        G.rect(cx - 12, 83, 24, 1, "O")
    pal = dict(PIP_PAL, R="#e8404e")
    return Sprite.from_rows(G.rows(), pal)


def zack_closeup(face="normal", w=128, h=150):
    """Big Zack head and shoulders. Eyes have whites so a sideways glance
    reads from across the room. Faces: normal, side1, side2, whistle, smug.
    Pair "smug" with zack_l_hand() for the L on the forehead."""
    from .shapes import Grid
    G = Grid(w, h)
    cx = 64
    # black suit, white shirt, red tie
    jacket = G.ellipse_mask(cx, 132, 58, 26) | ((G.y > 132) & (abs(G.x - cx) < 58))
    G.fill(jacket & (G.y > 104), "j")
    G.fill(jacket & (G.y > 104) & (G.x < cx - 46), "K")
    G.fill(jacket & (G.y > 104) & (G.x > cx + 46), "J")
    shirt = (G.y > 106) & (abs(G.x - cx) < 18 - (G.y - 106) * 0.3)
    G.fill(shirt, "w")
    G.rect(cx - 4, 110, 8, 6, "R")
    tie = (G.y > 115) & (abs(G.x - cx) < 3 + (G.y - 115) * 0.15)
    G.fill(tie & shirt, "r")
    G.rect(cx - 9, 100, 18, 10, "S")                     # neck
    # ears, head, shading
    G.ellipse(27, 70, 7, 10, "s")
    G.ellipse(101, 70, 7, 10, "S")
    G.ellipse(27, 70, 3, 5, "S")
    head = G.ellipse_mask(cx, 66, 38, 42)
    G.fill(head, "s")
    G.fill(head & ~G.ellipse_mask(cx - 6, 61, 38, 42), "S")
    G.ellipse(44, 52, 6, 3, "x")
    # short black hair with a hairline and faded sides
    hair = G.ellipse_mask(cx, 44, 42, 28) & (G.y < 44 - 0.004 * (G.x - cx) ** 2 + 6)
    G.fill(hair, "h")
    G.fill(hair & (G.y < 30) & (G.x < cx - 4) & (G.x > cx - 30), "H")
    G.fill(G.ellipse_mask(cx, 44, 42, 28) & ~hair & (abs(G.x - cx) > 30) & (G.y < 60), "d")
    G.fill(hair & ~G.ellipse_mask(cx - 4, 40, 42, 28), "d")
    # brows
    G.rect(38, 54, 14, 3, "h")
    G.rect(76, 54, 14, 3, "h")
    # eyes: whites + pupils that slide
    look = {"normal": 0, "side1": -3, "side2": -6, "whistle": -6, "smug": 4}[face]
    for ex in (39, 75):
        G.rect(ex, 62, 14, 11, "w")
        G.rect(ex + 5 + look, 63, 5, 9, "e")
        if face == "smug":                       # heavy half-closed lids
            G.rect(ex - 1, 61, 16, 5, "S")
            G.rect(ex - 1, 65, 16, 1, "m")
    if face == "smug":
        G.rect(38, 56, 14, 3, "h")               # brows relaxed, lower
        G.rect(76, 55, 14, 3, "h")
        G.rect(cx - 6, 89, 13, 2, "m")           # one-sided smirk
        G.rect(cx + 6, 86, 3, 3, "m")
    elif face == "whistle":
        G.ellipse(cx + 2, 88, 4, 4, "m")
        G.ellipse(cx + 2, 88, 2, 2, "S")
        G.rect(38, 53, 14, 3, "h")
    else:
        G.rect(cx - 8, 88, 16, 2, "m")
    return Sprite.from_rows(G.rows(), ZACK_PAL)


def arm(who="zack", tool="pen", length=120):
    """A sleeve reaching in from the bottom corner with a pen (or pointing
    finger) at its tip. Returns (sprite, (tip_x, tip_y)) inside the sprite.
    Zack reaches in from the left, Pip from the right."""
    from .shapes import Grid
    n = length
    G = Grid(n, n)
    tx, ty = n - 4, 3

    def at(d):
        k = d / 1.4142
        return tx - k, ty + k

    if who == "zack":
        sleeve, cuff, hand, pal = "j", "w", "s", ZACK_PAL
        pen_body, pen_shade, pen_tip = "r", "R", "R"
    else:
        sleeve, cuff, hand, pal = "u", "w", "b", PIP_PAL
        pen_body, pen_shade, pen_tip = "w", "U", "U"
    G.line(*at(24), *at(n * 1.5), sleeve, r=6)
    G.line(*at(20), *at(24), cuff, r=5)
    if tool == "pen":
        G.line(*at(3), *at(16), pen_body, r=1)
        G.line(*at(3), *at(16), pen_shade, r=0)
        G.line(*at(0), *at(3), pen_tip, r=0)
        hx, hy = at(15)
        G.ellipse(hx, hy, 5, 5, hand)
    else:  # pointing
        G.line(*at(0), *at(9), hand, r=1)
        hx, hy = at(14)
        G.ellipse(hx, hy, 6, 6, hand)
    rows = G.rows()
    if who != "zack":
        rows = [r[::-1] for r in rows]
        tx = n - 1 - tx
    s = Sprite.from_rows(rows, pal)
    return s, (tx + 1, ty + 1)   # +1 for the outline border


def zack_l_hand(w=128, h=240):
    """Zack's arm making an "L" on his forehead: index finger straight up,
    thumb out. A separate sprite (blit at the close-up's origin) so it gets
    its own dark outline where it crosses his face."""
    from .shapes import Grid
    G = Grid(w, h)
    G.line(-8, 160, 24, 70, "j", r=8)        # sleeve from off-frame
    G.line(-8, 160, 18, 84, "K", r=2)
    G.line(24, 70, 29, 60, "w", r=7)         # cuff
    G.ellipse(36, 50, 10, 9, "s")            # back of the hand
    G.ellipse(33, 47, 5, 4, "x")
    G.rect(29, 4, 8, 46, "s")                # index finger: the tall stroke
    G.rect(29, 4, 3, 46, "x")
    G.rect(29, 24, 8, 1, "S")                # knuckle creases
    G.rect(29, 36, 8, 1, "S")
    G.rect(40, 50, 30, 8, "s")               # thumb: the foot of the L
    G.rect(40, 50, 30, 3, "x")
    G.rect(56, 50, 1, 8, "S")
    G.rect(30, 58, 14, 2, "S")               # curled fingers under the palm
    return Sprite.from_rows(G.rows(), ZACK_PAL)
