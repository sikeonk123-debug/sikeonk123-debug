#!/usr/bin/env python3
"""Draw entry.png: a one-page newspaper front page summing up 19 Nov 2026.

v2: final story list, researched after the day ended (20 Nov 2026, UTC).
Lead is the first-ever Trump-Xi-Putin trilateral in Shenzhen and its
Declaration Towards Peace; the grid adds the ICJ's Myanmar genocide ruling.
Card headlines are kept to one line so the body fits the 196px card.
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
d.text((M + 24, M + 124), "THURSDAY  \u2022  THE DAY'S NEWS IN ONE IMAGE",
       font=font(SANS_B, 20), fill=(255, 214, 90))

# ---- lead story ----
y = 206
d.text((M, y), "DIPLOMACY", font=font(SANS_B, 20), fill=RED)
y += 28
y = draw_wrapped(d, (M, y), "Trump, Xi and Putin issue a \u2018Declaration Towards Peace\u2019",
                 font(SERIF_B, 52), W - 2 * M, INK, spacing=4)
y += 6
y = draw_wrapped(d, (M, y),
                 "In a first three-way summit in Shenzhen, the US, Chinese and Russian "
                 "leaders pledge nuclear-risk talks, more oil supply, UN reform and ICC "
                 "limits \u2014 but no deal on Ukraine, Iran or arms.",
                 font(SANS, 26), W - 2 * M, MUTED, spacing=4)
y += 10
d.line([M, y, W - M, y], fill=RULE, width=2)

# ---- 2x2 grid ----
stories = [
    ("UNITED STATES", "Democrats nominate Jeffries",
     "House Democrats pick Hakeem Jeffries 251\u201311, in line to be the first "
     "Black Speaker on 3 January 2027."),
    ("JUSTICE", "Myanmar committed genocide",
     "The ICJ finds Myanmar committed genocide against the Rohingya, the first "
     "such verdict against a state."),
    ("MIDDLE EAST", "US and Iran trade fire",
     "Washington struck a missile site on Qeshm Island; Tehran hit US bases in Bahrain and Kuwait."),
    ("INDIA", "Cyclone Akvan nears coast",
     "Severe Cyclone Akvan closes on Andhra Pradesh and Odisha, due to make "
     "landfall by Friday noon near Gopalpur, winds 90\u2013100 km/h, red alerts in place."),
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
             "GTA VI launches, scoring 99 on Metacritic  \u2022  Anthropic\u2019s record $81bn IPO  "
             "\u2022  Voyager 1 reaches one light-day from Earth  \u2022  EU proposes a \u20ac45bn loan for Ukraine",
             font(SANS, 20), W - 2 * M - 40, (255, 255, 255), spacing=3)

d.text((M, H - 34), "Compiled from wire reports  \u2022  19 November 2026",
       font=font(SANS, 16), fill=MUTED)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
import os
print("bytes:", os.path.getsize("entry.png"))
