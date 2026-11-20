#!/usr/bin/env python3
"""Draw entry.png: a newspaper-poster summary of world news, 19 Nov 2026.

Deterministic: fixed palette, fixed fonts, no randomness, no network,
no timestamps. Run: python3 gen_image.py  (writes entry.png next to this file)
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (246, 241, 231)          # warm paper
INK = (26, 26, 46)            # near-black navy
RED = (192, 57, 43)           # newspaper red accent
PANEL = (255, 255, 255)
BORDER = (200, 192, 172)
MUTED = (90, 86, 76)
TICKER_BG = (26, 26, 46)
TICKER_FG = (246, 241, 231)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
F_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
F_REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def center_text(draw, y, text, fnt, fill, x0=0, x1=W):
    w = draw.textlength(text, font=fnt)
    draw.text(((x0 + x1 - w) / 2, y), text, font=fnt, fill=fill)


# ---------------------------------------------------------------- illustrations
def ill_summit(d, x, y, w, h):
    """Three flags behind a table."""
    cy = y + h - 26
    d.rectangle([x + 8, cy, x + w - 8, cy + 8], fill=(120, 72, 48))  # table
    d.rectangle([x + 8, cy + 8, x + w - 8, cy + 12], fill=(90, 54, 36))
    cols = [(192, 57, 43), (52, 120, 180), (60, 140, 90)]  # red, blue, green
    for i, c in enumerate(cols):
        px = x + 60 + i * (w - 120) // 2
        d.line([px, y + 8, px, cy], fill=INK, width=4)
        d.polygon([(px, y + 8), (px + 46, y + 18), (px, y + 28)], fill=c)
    d.ellipse([x + w // 2 - 14, cy - 30, x + w // 2 + 14, cy - 2],
              fill=(240, 200, 90))  # sun / globe accent


def ill_court(d, x, y, w, h):
    """Courthouse pediment, columns, scales."""
    base = y + h - 18
    d.polygon([(x + 20, y + 34), (x + w // 2, y + 6), (x + w - 20, y + 34)],
              fill=(52, 90, 140))
    d.rectangle([x + 20, y + 34, x + w - 20, y + 42], fill=(40, 70, 110))
    for i in range(4):
        cx = x + 52 + i * (w - 104) // 3
        d.rectangle([cx - 7, y + 42, cx + 7, base - 8], fill=(230, 225, 210),
                    outline=(120, 110, 90))
    d.rectangle([x + 16, base - 8, x + w - 16, base], fill=(40, 70, 110))
    # scales of justice in the middle, above the base
    mx = x + w // 2
    d.line([mx, y + 52, mx, y + 84], fill=INK, width=4)
    d.line([mx - 26, y + 56, mx + 26, y + 56], fill=INK, width=4)
    d.polygon([(mx - 34, y + 60), (mx - 18, y + 60), (mx - 26, y + 74)],
              fill=(240, 200, 90))
    d.polygon([(mx + 18, y + 60), (mx + 34, y + 60), (mx + 26, y + 74)],
              fill=(240, 200, 90))


def ill_tanker(d, x, y, w, h):
    """Tanker ship with a flame, on waves."""
    hull_y = y + h - 46
    d.polygon([(x + 30, hull_y), (x + w - 30, hull_y), (x + w - 52, hull_y + 26),
               (x + 52, hull_y + 26)], fill=(150, 40, 36))
    d.rectangle([x + 60, hull_y - 26, x + w - 110, hull_y], fill=(52, 90, 140))
    d.rectangle([x + 70, hull_y - 20, x + w - 120, hull_y - 6], fill=(240, 200, 90))
    # flame above the bow
    fx = x + w - 78
    d.polygon([(fx - 16, hull_y - 30), (fx - 4, hull_y - 62), (fx + 4, hull_y - 40),
               (fx + 14, hull_y - 66), (fx + 20, hull_y - 30)], fill=(240, 120, 30))
    d.polygon([(fx - 8, hull_y - 30), (fx, hull_y - 50), (fx + 10, hull_y - 30)],
              fill=(250, 200, 40))
    for wy in (hull_y + 34, hull_y + 44):
        d.arc([x + 20, wy - 8, x + w - 20, wy + 8], 0, 180, fill=(52, 120, 180),
              width=4)


def ill_globe(d, x, y, w, h):
    """Globe with a leaf."""
    cx, cy, r = x + w // 2 - 20, y + h // 2 + 4, 44
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 180, 220),
              outline=(52, 90, 140), width=3)
    d.ellipse([cx - 26, cy - 22, cx - 2, cy + 2], fill=(90, 170, 90))
    d.ellipse([cx + 2, cy + 6, cx + 26, cy + 28], fill=(90, 170, 90))
    d.ellipse([cx + 8, cy - 30, cx + 30, cy - 8], fill=(90, 170, 90))
    # leaf
    lx, ly = x + w - 66, y + 16
    d.polygon([(lx, ly + 26), (lx + 8, ly), (lx + 34, ly + 10), (lx + 26, ly + 34),
               (lx + 6, ly + 36)], fill=(60, 140, 90))
    d.line([lx + 6, ly + 32, lx + 28, ly + 8], fill=(30, 100, 60), width=3)


def ill_bangladesh(d, x, y, w, h):
    """Flames over a map outline."""
    base = y + h - 20
    d.polygon([(x + 40, base), (x + 70, y + 44), (x + 110, y + 30),
               (x + 150, y + 52), (x + 190, y + 40), (x + w - 50, y + 60),
               (x + w - 40, base)], fill=(220, 205, 170), outline=(150, 120, 80))
    for fx, fh in ((x + 84, 52), (x + w // 2, 66), (x + w - 96, 48)):
        d.polygon([(fx - 18, base - 6), (fx - 6, base - fh), (fx + 2, base - fh + 18),
                   (fx + 10, base - fh - 8), (fx + 20, base - 6)], fill=(240, 120, 30))
        d.polygon([(fx - 9, base - 6), (fx, base - fh + 16), (fx + 10, base - 6)],
                  fill=(250, 200, 40))


def ill_bank(d, x, y, w, h):
    """Bank building with a rising chart arrow."""
    base = y + h - 18
    d.polygon([(x + 30, y + 30), (x + w // 2 - 40, y + 8), (x + w - 90, y + 30)],
              fill=(52, 90, 140))
    d.rectangle([x + 30, y + 30, x + w - 90, y + 38], fill=(40, 70, 110))
    for i in range(3):
        cx = x + 62 + i * (w - 170) // 2
        d.rectangle([cx - 7, y + 38, cx + 7, base - 8], fill=(230, 225, 210),
                    outline=(120, 110, 90))
    d.rectangle([x + 26, base - 8, x + w - 86, base], fill=(40, 70, 110))
    # rising chart
    ax, ay = x + w - 84, y + h - 22
    pts = [(ax, ay - 6), (ax + 16, ay - 22), (ax + 30, ay - 16),
           (ax + 46, ay - 38), (ax + 62, ay - 46)]
    d.line(pts, fill=(192, 57, 43), width=5, joint="curve")
    d.polygon([(ax + 62, ay - 46), (ax + 50, ay - 46), (ax + 62, ay - 34)],
              fill=(192, 57, 43))


PANELS = [
    ("PEACE DECLARATION IN SHENZHEN",
     "Trump, Xi and Putin sign joint declaration", ill_summit),
    ("WORLD COURT: MYANMAR GUILTY OF GENOCIDE",
     "ICJ rules on the Rohingya, 9-6", ill_court),
    ("TANKERS HIT IN STRAIT OF HORMUZ",
     "11 crew hurt, 1 missing as strikes escalate", ill_tanker),
    ("COP31 RACE TO UNBLOCK CLIMATE TALKS",
     "Ministers push for a final text in Antalya", ill_globe),
    ("BANGLADESH IN TURMOIL",
     "Violence in 28 districts; Yunus home torched", ill_bangladesh),
    ("INDONESIA LIFTS RATE TO 6%",
     "Rupiah at record low; central bank acts", ill_bank),
]

TICKER = ("ALSO: US Senate rejects Iran war-powers bid 51-48  \u2022  "
          "EU proposes 45bn euro loan to Ukraine  \u2022  "
          "Van Gogh sells for $190.4m, artist record")


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- header ----
    date_f = font(F_BOLD, 34)
    head_f = font(F_BOLD, 50)
    center_text(d, 26, "THURSDAY 19 NOVEMBER 2026", date_f, RED)
    center_text(d, 74, "THE WORLD IN ONE PICTURE", head_f, INK)
    d.rectangle([32, 142, W - 32, 146], fill=RED)
    d.rectangle([32, 150, W - 32, 152], fill=INK)

    # ---- story grid: 2 cols x 3 rows ----
    margin, gap = 32, 16
    pw = (W - 2 * margin - gap) // 2
    ph = 232
    top = 168
    h_f = font(F_BOLD, 21)
    c_f = font(F_REG, 17)
    for i, (headline, caption, ill) in enumerate(PANELS):
        col, row = i % 2, i // 2
        x = margin + col * (pw + gap)
        y = top + row * (ph + gap)
        d.rectangle([x, y, x + pw, y + ph], fill=PANEL, outline=BORDER, width=2)
        d.rectangle([x, y, x + pw, y + 5], fill=RED)
        ill(d, x + 12, y + 12, pw - 24, 104)
        # Vertically centre the headline + caption block in the space
        # below the illustration, so one-line and two-line headlines
        # sit at the same visual height across panels.
        lines = wrap(d, headline, h_f, pw - 28)[:2]
        clines = wrap(d, caption, c_f, pw - 28)[:2]
        block_h = 26 * len(lines) + 10 + 21 * len(clines)
        ty = y + 122 + (ph - 122 - 10 - block_h) // 2
        for ln in lines:
            center_text(d, ty, ln, h_f, INK, x + 14, x + pw - 14)
            ty += 26
        ty += 10
        for ln in clines:
            center_text(d, ty, ln, c_f, MUTED, x + 14, x + pw - 14)
            ty += 21

    # ---- ticker ----
    ty0 = top + 3 * ph + 2 * gap + 22
    d.rectangle([32, ty0, W - 32, ty0 + 62], fill=TICKER_BG)
    t_f = font(F_REG, 17)
    tlines = wrap(d, TICKER, t_f, W - 2 * 32 - 24)
    ty = ty0 + 31 - 10 * len(tlines)
    for ln in tlines:
        center_text(d, ty, ln, t_f, TICKER_FG, 44, W - 44)
        ty += 20

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
