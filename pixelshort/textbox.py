"""Dialogue box: dark box, double light border, typewriter pixel text."""
from .canvas import hex_rgb as H
from .font import draw_text, wrap, LINE_H

BOX_BG = H("#0e0a1e")
BOX_BORDER = H("#f4f4ff")
BOX_INNER = H("#5a5288")
WHITE = H("#ffffff")
YELLOW = H("#ffe14a")
TEXT_BORDER = H("#1a1436")

BOX_X, BOX_Y, BOX_W, BOX_H = 6, 216, 168, 70   # inside the 10% safe margins


def draw_box(c, speaker, text, chars=None, color=WHITE, y=BOX_Y, cursor_frame=None):
    c.rect(BOX_X, y, BOX_W, BOX_H, BOX_BORDER)
    c.rect(BOX_X + 2, y + 2, BOX_W - 4, BOX_H - 4, BOX_BG)
    c.rect(BOX_X + 3, y + 3, BOX_W - 6, 1, BOX_INNER)
    c.rect(BOX_X + 3, y + BOX_H - 4, BOX_W - 6, 1, BOX_INNER)
    tx = BOX_X + 9
    ty = y + 8
    if speaker:
        draw_text(c, speaker, tx, ty, fill=YELLOW, border=TEXT_BORDER)
        ty += LINE_H + 1
    lines = wrap(text, BOX_W - 20)
    remaining = len(text) if chars is None else chars
    for line in lines:
        if remaining <= 0:
            break
        draw_text(c, line[:remaining], tx, ty, fill=color, border=TEXT_BORDER)
        remaining -= len(line) + 1
        ty += LINE_H
    # blinking "next" arrow once the line is fully typed
    if cursor_frame is not None and (chars is None or chars >= len(text)) and (cursor_frame // 3) % 2 == 0:
        ax, ay = BOX_X + BOX_W - 14, y + BOX_H - 10
        for i, w in enumerate((5, 3, 1)):
            c.rect(ax + i, ay + i, w, 1, YELLOW)
