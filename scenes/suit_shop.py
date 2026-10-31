"""PIP'S SUITS - a ~22 second vertical short.

Zack walks into Pip's suit shop and makes one mistake.
All timing is in art frames at 12 fps ("on 2s" at 24 fps output).
"""
from pixelshort import cast, backgrounds as bg, effects as fx
from pixelshort.textbox import draw_box, WHITE, YELLOW
from pixelshort.font import draw_text
from pixelshort.canvas import hex_rgb

FEET_Y = 204
PIP_X, PIP_Y = 118, 118
ZACK_STOP_X = 56
RIM = hex_rgb("#b8c8ff")


class Sprites:
    """Pre-build every sprite once."""
    def __init__(self):
        self.zack = {(f, l): cast.zack(f, l) for f in cast.ZACK_FACES for l in cast.ZACK_LEGS}
        self.zack_rim = {l: cast.zack("deadpan", l, rim=RIM) for l in cast.ZACK_LEGS}
        self.pip = {f: cast.pip(f) for f in cast.PIP_FACES}
        self.pip_cu = cast.pip_closeup("angry")


S = None


def _zack(c, x, face, legs, flip=False, rim=False):
    spr = S.zack_rim[legs] if rim else S.zack[(face, legs)]
    c.blit(spr, x, FEET_Y - spr.h, flip=flip)


def _pip(c, face, bob=0):
    c.blit(S.pip[face], PIP_X, PIP_Y + bob)


def idle_legs(f):
    return cast.ZACK_IDLE[(f // 6) % 2]   # each pose held 6 art frames


def pip_idle(f, face="normal"):
    # blink for 2 frames every ~3 s; 1 px breathing bob held on 6s
    if face == "normal" and f % 36 in (30, 31):
        face = "blink"
    return face, (f // 6) % 2


def type_chars(f, start, cps=2):
    return max(0, (f - start) * cps)


# --------------------------------------------------------------------------
# shots: each is (length_in_art_frames, draw_fn(canvas_factory, f) -> canvas)
# --------------------------------------------------------------------------
def shot_walk_in(f):
    c = bg.shop()
    face, bob = pip_idle(f)
    _pip(c, face, bob)
    bg.draw_counter(c)
    x = -16 + f * 2 + (f // 2) % 1
    if x < ZACK_STOP_X:
        _zack(c, x, "normal", cast.ZACK_WALK[f % 4])
    else:
        _zack(c, ZACK_STOP_X, "normal", "stand")
    return c


def talk(speaker, line, zack_face="normal", pip_face="normal", color=WHITE, cps=2, start=2):
    def draw(f):
        c = bg.shop()
        pf, bob = pip_idle(f, pip_face)
        _pip(c, pf, bob)
        bg.draw_counter(c)
        _zack(c, ZACK_STOP_X, zack_face, idle_legs(f))
        if line:
            draw_box(c, speaker, line, chars=type_chars(f, start, cps), color=color, cursor_frame=f)
        return c
    return draw


def shot_closeup(f):
    """HARD CUT: Pip close-up. Red tint fades in, shake, steam, fire rising."""
    c = bg.closeup_wall()
    fx.fire_row(c, f, floor_y=214, height=min(1.0, f / 18), spacing=9, seed=5)
    c.blit(S.pip_cu, (c.w - S.pip_cu.w) // 2, 70)
    fx.steam_puffs(c, f, 58, 84)
    fx.steam_puffs(c, f + 5, 122, 84)
    c.tint(fx.ANGER_RED, fx.tint_ramp(f, 0, frames=6))
    if f >= 2:
        c.shake(*fx.shake_offset(f))
    draw_box(c, "PIP", "IT'S. A. SUIT.", chars=type_chars(f, 2, 1), color=YELLOW, cursor_frame=f)
    return c


def shot_fire_wide(f):
    """HARD CUT: the whole shop on fire, Zack backs out the door."""
    c = bg.shop()
    _pip(c, "angry", 0)
    fx.steam_puffs(c, f, PIP_X + 11, PIP_Y - 1)
    bg.draw_counter(c)
    # a short back row along the wall line, then the main fire at the front
    fx.fire_row(c, f, floor_y=bg.FLOOR_Y + 4, height=0.0, x0=0, x1=bg.COUNTER_X, spacing=11, seed=9)
    if f < 12:
        _zack(c, ZACK_STOP_X, "shock", idle_legs(f))
    else:
        x = ZACK_STOP_X - (f - 12) * 4
        _zack(c, x, "shock", cast.ZACK_WALK[f % 4], flip=True)
    fx.fire_row(c, f + 1, floor_y=FEET_Y + 12, height=min(1.0, 0.3 + f / 24), spacing=10, seed=4)
    c.tint(fx.ANGER_RED, 0.26)
    c.shake(*fx.shake_offset(f, amp=2, seed=23))
    draw_box(c, "PIP", "GET OUT OF MY SHOP.", chars=type_chars(f, 1, 2), color=YELLOW, cursor_frame=f)
    return c


def shot_void(f):
    """HARD CUT: the dark. Zack alone in a light beam, with a light rim."""
    c = bg.void()
    bg.sparkles(c, f)
    _zack(c, 90 - 9, "deadpan", idle_legs(f), rim=True)
    if f >= 6:
        draw_box(c, "ZACK", "...Guess I'm renting a tux.", chars=type_chars(f, 8, 2), cursor_frame=f)
    return c


def build_shots():
    global S
    S = Sprites()
    walk_len = (ZACK_STOP_X + 16) // 2 + 4
    return [
        (walk_len, shot_walk_in),
        (34, talk("ZACK", "Yo! Nice tux, little guy.", zack_face="happy")),
        (36, talk("PIP", "It is a SUIT. I sell suits.")),
        (10, talk(None, None, zack_face="deadpan")),                      # beat
        (38, talk("ZACK", "...You're a penguin. You were born in a tux.",
                  zack_face="deadpan")),
        (14, talk(None, None, zack_face="deadpan", pip_face="deadpan")),  # beat
        (36, shot_closeup),
        (34, shot_fire_wide),
        (44, shot_void),
        (10, lambda f: shot_walk_in(0)),  # hard cut to the opening frame: loops
    ]


def frames(watermark=None):
    for length, draw in build_shots():
        for f in range(length):
            c = draw(f)
            if watermark:
                draw_text(c, watermark, c.w - 4 - len(watermark) * 6, c.h - 14,
                          fill=hex_rgb("#c8c0e0"), border=hex_rgb("#1a1436"))
            yield c
