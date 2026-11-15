"""Draws the channel profile photo (800x800) and banner (2560x1440, YouTube safe area 1546x423 centred)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pipeline"))
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from character import Presenter, PRESENTERS
import numpy as np
OUT = os.path.dirname(os.path.abspath(__file__))
F = "/usr/share/fonts/opentype/inter/"
def font(n, s): return ImageFont.truetype(F + n + ".otf", s)
BG = (11, 18, 38); INK = (240, 244, 255); ACC = (255, 196, 61); ACC2 = (86, 204, 242); MUTED = (150, 165, 200)
def glow(w, h, spots):
    g = Image.new("RGB", (w, h), BG); d = ImageDraw.Draw(g)
    for box, col in spots: d.ellipse(box, fill=col)
    return g.filter(ImageFilter.GaussianBlur(min(w, h) // 6))

S = 800; im = glow(S, S, [((350, -250, 1100, 500), (30, 56, 120)), ((-300, 450, 400, 1150), (22, 40, 90))]); d = ImageDraw.Draw(im)
f = font("InterDisplay-ExtraBold", 380); tw = d.textlength("AI", font=f)
d.text(((S - tw) / 2 + 20, 150), "AI", font=f, fill=INK)
d.rounded_rectangle(((S - tw) / 2 - 40, 205, (S - tw) / 2 - 2, 505), 14, fill=ACC)
f2 = font("InterDisplay-Bold", 62); t = "FOR EVERY JOB"; d.text(((S - d.textlength(t, font=f2)) / 2, 560), t, font=f2, fill=ACC)
im.save(OUT + "/profile.png")

W, H = 2560, 1440
b = glow(W, H, [((1500, -300, 2900, 900), (28, 52, 112)), ((-200, 700, 1100, 1800), (20, 38, 86))]); d = ImageDraw.Draw(b)
x0 = 560
d.rounded_rectangle((x0, 560, x0 + 22, 690), 8, fill=ACC)
d.text((x0 + 52, 540), "AI for Every Job", font=font("InterDisplay-ExtraBold", 128), fill=INK)
d.text((x0 + 56, 716), "Practical AI for your job, one profession at a time.", font=font("Inter-Medium", 40), fill=MUTED)
d.text((x0 + 56, 790), "New videos every day", font=font("Inter-SemiBold", 40), fill=ACC2)
px = 1640
for i, k in enumerate(["student", "manager"]):
    p = Presenter(PRESENTERS[k]); fr = Image.fromarray(p.frame(2 if i == 0 else 0, 0, 0).astype(np.uint8)).resize((176, 256))
    m = Image.new("L", fr.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, 175, 255), 26, fill=255)
    bx = px + i * 196; by = 600 if i == 0 else 640
    d.rounded_rectangle((bx - 4, by - 4, bx + 179, by + 259), 30, fill=ACC)
    b.paste(fr, (bx, by), m)
b.save(OUT + "/banner.png")
