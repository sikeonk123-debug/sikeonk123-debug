#!/usr/bin/env python3
"""Draw entry.png: a one-page newspaper front page summing up 19 Nov 2026.

v1: built from the stories verified on the morning of 19 Nov 2026 (UTC).
Regenerate after the day ends with the final story list before submitting.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (248, 245, 238)
INK = (20, 20, 20)
MUTED = (90, 86, 78)
RED = (166, 27, 27)
NAVY = (18, 34, 64)
RULE = (180, 174, 162)
CARD = (255, 255, 255)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = f"{cur} {w}".strip()
        if draw.textlength(t, font=fnt) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def draw_wrapped(draw, xy, text, fnt, width, fill, spacing=6):
    x, y = xy
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
M = 36  # margin

# ---- masthead ----
d.rectangle([M, M, W - M, 186], fill=NAVY)
d.text((M + 24, M + 14), "THE WORLD IN ONE DAY", font=font(SANS_B, 24), fill=(255, 255, 255))
d.text((M + 24, M + 44), "19 NOVEMBER 2026", font=font(SERIF_B, 62), fill=(255, 255, 255))
d.text((M + 24, M + 124), "THURSDAY  •  THE DAY'S NEWS IN ONE IMAGE",
       font=font(SANS_B, 20), fill=(255, 214, 90))

# ---- lead story ----
y = 206
d.text((M, y), "UNITED STATES", font=font(SANS_B, 20), fill=RED)
y += 28
y = draw_wrapped(d, (M, y), "Democrats nominate Jeffries for Speaker",
                 font(SERIF_B, 52), W - 2 * M, INK, spacing=4)
y += 6
y = draw_wrapped(d, (M, y),
                 "House Democrats pick Hakeem Jeffries 251\u201311. He is in line to become the "
                 "first Black Speaker when the new Congress convenes on 3 January 2027.",
                 font(SANS, 26), W - 2 * M, MUTED, spacing=4)
y += 10
d.line([M, y, W - M, y], fill=RULE, width=2)

# ---- 2x2 grid ----
stories = [
    ("DIPLOMACY", "Trump, Xi and Putin due to meet in Shenzhen",
     "The three leaders are set for a first trilateral meeting on the sidelines of the APEC summit in China."),
    ("MIDDLE EAST", "US and Iran trade fire",
     "Washington struck a missile site on Qeshm Island; Tehran hit US bases in Bahrain and Kuwait."),
    ("INDIA", "Cyclone Akvan nears the coast",
     "The severe cyclone closes on Andhra Pradesh and Odisha, with red alerts in place."),
    ("TECHNOLOGY", "GTA VI launches worldwide",
     "After 13 years, Rockstar's sequel begins its global rollout \u2014 scoring 99 on Metacritic."),
]
gx, gy = M, y + 18
cw, ch, gap = 460, 196, 32
for i, (tag, head, body) in enumerate(stories):
    x = gx + (i % 2) * (cw + gap)
    yy = gy + (i // 2) * (ch + 18)
    d.rectangle([x, yy, x + cw, yy + ch], fill=CARD, outline=RULE, width=1)
    d.text((x + 16, yy + 12), tag, font=font(SANS_B, 18), fill=RED)
    y2 = draw_wrapped(d, (x + 16, yy + 40), head, font(SERIF_B, 27), cw - 32, INK, spacing=2)
    draw_wrapped(d, (x + 16, y2 + 6), body, font(SANS, 21), cw - 32, MUTED, spacing=3)

# ---- footer strip ----
fy = gy + 2 * ch + 18 + 14
d.rectangle([M, fy, W - M, fy + 96], fill=NAVY)
d.text((M + 20, fy + 12), "ALSO TODAY", font=font(SANS_B, 20), fill=(255, 214, 90))
draw_wrapped(d, (M + 20, fy + 40),
             "Voyager 1 reaches one light-day from Earth  \u2022  EU proposes a \u20ac45bn loan "
             "for Ukraine  \u2022  Pew: Islam on track to be the world's largest religion by 2035",
             font(SANS, 20), W - 2 * M - 40, (255, 255, 255), spacing=3)

d.text((M, H - 34), "Compiled from wire reports  \u2022  19 November 2026",
       font=font(SANS, 16), fill=MUTED)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
import os
print("bytes:", os.path.getsize("entry.png"))
