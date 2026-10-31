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
    pal = dict(PIP_PAL, R="#e8404e")
    return Sprite.from_rows(G.rows(), pal)
