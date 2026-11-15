import sys, os, json, subprocess, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib
# Usage: EP=<slug> python3 build.py preview|tts|plan|render [scene numbers]
# The episode module pipeline/episodes/<slug>.py defines CHANNEL, EPISODE, SCENES, PRESENTER (key in character.PRESENTERS), VOICE (Kokoro voice id).
EP = os.environ.get("EP", "students")
_c = importlib.import_module("episodes." + EP)
SCENES, CHANNEL, EPISODE = _c.SCENES, _c.CHANNEL, _c.EPISODE
PRESENTER_KEY, VOICE = _c.PRESENTER, _c.VOICE
TTS_DIR = os.environ.get("TTS_DIR", os.path.expanduser("~/tts"))

W, H, FPS = 1920, 1080, 30
OUT = os.environ.get("WORK_DIR", os.path.expanduser("~/work")) + "/" + EP; os.makedirs(OUT, exist_ok=True)
F = "/usr/share/fonts/opentype/inter/"
def font(name, size): return ImageFont.truetype(F + name + ".otf", size)

BG = (11, 18, 38); PANEL = (22, 33, 62); INK = (240, 244, 255); MUTED = (150, 165, 200)
ACC = (255, 196, 61); ACC2 = (86, 204, 242)

def base():
    im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
    # soft diagonal glow
    g = Image.new("RGB", (W, H), BG); gd = ImageDraw.Draw(g)
    gd.ellipse((1150, -500, 2350, 700), fill=(24, 44, 92))
    gd.ellipse((-600, 700, 500, 1700), fill=(18, 34, 74))
    from PIL import ImageFilter
    g = g.filter(ImageFilter.GaussianBlur(180))
    return g

BASE = base()

PX, PY, PW, PH = 1400, 250, 440, 640
def brand(d):
    d.rounded_rectangle((PX - 5, PY - 5, PX + PW + 4, PY + PH + 4), 40, fill=ACC)
    d.rounded_rectangle((80, 56, 96, 92), 4, fill=ACC)
    d.text((112, 54), CHANNEL, font=font("Inter-SemiBold", 30), fill=INK)
    tw = d.textlength(EPISODE, font=font("Inter-Medium", 28))
    d.text((W - 80 - tw, 56), EPISODE, font=font("Inter-Medium", 28), fill=MUTED)

def fit(d, text, name, size, maxw):
    while d.textlength(text, font=font(name, size)) > maxw and size > 20: size -= 2
    return font(name, size)

def draw_title(sc):
    im = BASE.copy(); d = ImageDraw.Draw(im); brand(d)
    f = fit(d, sc["title"], "InterDisplay-ExtraBold", 150, 1180)
    y = 330
    d.text((160, y), sc["title"], font=f, fill=INK)
    if sc.get("year"):
        d.text((160, y + 170), "in " + sc["year"], font=font("InterDisplay-ExtraBold", 150), fill=ACC)
        y += 170
    d.rounded_rectangle((160, y + 215, 400, y + 223), 4, fill=ACC2)
    d.text((160, y + 260), sc["sub"], font=fit(d, sc["sub"], "Inter-Medium", 46, 1180), fill=MUTED)
    return im

def draw_cards(sc, n_items):
    """n_items: how many card/tip items are visible."""
    im = BASE.copy(); d = ImageDraw.Draw(im); brand(d)
    d.text((160, 168), sc["num"], font=font("InterDisplay-ExtraBold", 96), fill=ACC)
    nw = d.textlength(sc["num"], font=font("InterDisplay-ExtraBold", 96))
    d.text((160 + nw + 36, 180), sc["title"], font=font("InterDisplay-Bold", 80), fill=INK)
    items = [b for b in sc["beats"] if "card" in b or "tip" in b][:n_items]
    y = 330
    for i, b in enumerate(items):
        if "card" in b:
            name, desc = b["card"]
            d.rounded_rectangle((160, y, 1330, y + 144), 22, fill=PANEL)
            d.rounded_rectangle((160, y, 172, y + 144), 6, fill=ACC2)
            d.text((216, y + 22), name, font=fit(d, name, "Inter-Bold", 46, 1060), fill=INK)
            d.text((216, y + 84), desc, font=fit(d, desc, "Inter-Regular", 34, 1060), fill=MUTED)
        else:
            d.rounded_rectangle((160, y, 1330, y + 144), 22, fill=(52, 44, 20), outline=ACC, width=3)
            d.text((216, y + 16), "REMEMBER", font=font("Inter-Bold", 22), fill=ACC)
            f = font("Inter-SemiBold", 34); words = b["tip"].split(); lines = [""]
            for w in words:
                t = (lines[-1] + " " + w).strip()
                if d.textlength(t, font=f) > 1060: lines.append(w)
                else: lines[-1] = t
            ty = y + 76 - 21 * len(lines) + 12
            for ln in lines:
                d.text((216, ty), ln, font=f, fill=INK); ty += 42
        y += 166
    return im

def states(sc):
    """One image per beat."""
    if sc["kind"] == "title": return [draw_title(sc)] * len(sc["beats"])
    out, n = [], 0
    for b in sc["beats"]:
        if "card" in b or "tip" in b: n += 1
        out.append(draw_cards(sc, n))
    return out

if sys.argv[1] == "preview":
    for i in (0, 1, 2, len(SCENES) - 2):
        states(SCENES[i])[-1].save(f"{OUT}/preview_{i}.png")
    sys.exit()

# ---------- narration ----------
import soundfile as sf
SR = 24000
AUD = f"{OUT}/audio"; os.makedirs(AUD, exist_ok=True)
if sys.argv[1] == "tts":
    from kokoro_onnx import Kokoro
    k = Kokoro(TTS_DIR + "/kokoro-v1.0.onnx", TTS_DIR + "/voices-v1.0.bin")
    for si, sc in enumerate(SCENES):
        for bi, b in enumerate(sc["beats"]):
            p = f"{AUD}/{si:02d}_{bi:02d}.wav"
            if os.path.exists(p): continue
            s, sr = k.create(b.get("tts", b["say"]), voice=VOICE, speed=1.0, lang="en-us")
            sf.write(p, s, sr)
        print("scene", si, flush=True)
    sys.exit()

# ---------- render ----------
PAUSE, SCENE_END, FADE = 0.35, 0.7, 10
plan, total = [], 0
for si, sc in enumerate(SCENES):
    beats = []
    for bi, b in enumerate(sc["beats"]):
        a, sr = sf.read(f"{AUD}/{si:02d}_{bi:02d}.wav", dtype="float32"); assert sr == SR
        tail = SCENE_END if bi == len(sc["beats"]) - 1 else PAUSE
        nf = math.ceil((len(a) / SR + tail) * FPS)
        beats.append((a, nf)); total += nf
    plan.append(beats)
print("total seconds", total / FPS, flush=True)
if sys.argv[1] == "plan": sys.exit()

only = [int(x) for x in sys.argv[2:]] or range(len(SCENES))
bgarr = np.asarray(BASE, dtype=np.float32)
from character import Presenter, PRESENTERS
PRES = Presenter(PRESENTERS[PRESENTER_KEY])
_m = Image.new("L", (PW, PH), 0); ImageDraw.Draw(_m).rounded_rectangle((0, 0, PW - 1, PH - 1), 36, fill=255)
RM = (np.asarray(_m, dtype=np.float32) / 255)[..., None]
import random; random.seed(7)
gf = 0
for si, sc in enumerate(SCENES):
    nframes = sum(nf for _, nf in plan[si])
    if si not in only: gf += nframes; continue
    sts = [np.asarray(s, dtype=np.uint8) for s in states(sc)]
    tmp, fin = f"{OUT}/scene_{si:02d}.tmp.mp4", f"{OUT}/scene_{si:02d}.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "18", "-preset", "veryfast",
                          "-pix_fmt", "yuv420p", "-r", str(FPS), tmp], stdin=subprocess.PIPE)
    prev = bgarr
    audio = []
    for a, nf in plan[si]:
        buf = np.zeros(round(nf * SR / FPS), dtype=np.float32); buf[:len(a)] = a[:len(buf)]
        audio.append(buf)
    aud = np.concatenate(audio); spf = SR // FPS
    rms = np.array([np.sqrt(np.mean(aud[i * spf:(i + 1) * spf] ** 2) + 1e-12) for i in range(nframes)])
    rms = rms / (np.percentile(rms, 95) + 1e-9)
    lf = 0; mouth = 0; blink_at = random.randint(40, 110); blink_left = 0
    for bi, (a, nf) in enumerate(plan[si]):
        cur = sts[bi]; curf = cur.astype(np.float32)
        changed = bi == 0 or not np.array_equal(cur, sts[bi - 1])
        for j in range(nf):
            if changed and j < FADE:
                t = (j + 1) / (FADE + 1); t = t * t * (3 - 2 * t)
                fr = (prev * (1 - t) + curf * t).astype(np.uint8)
            else:
                fr = cur.copy()
            # presenter: mouth shape every 2 frames from loudness, blinks, gentle head bob
            if lf % 2 == 0:
                v = float(rms[lf:lf + 2].max())
                new = 0 if v < 0.08 else 1 if v < 0.3 else 2 if v < 0.62 else 3
                if new == 2 and mouth == 2 and random.random() < 0.35: new = 4
                mouth = new
            if lf == blink_at: blink_left = 4; blink_at = lf + random.randint(70, 150)
            blink = 1 if blink_left > 0 else 0; blink_left -= 1
            dy = int(round(2 * math.sin(2 * math.pi * gf / 95))) + (1 if mouth >= 2 else 0)
            pf = PRES.frame(mouth, blink, dy)
            reg = fr[PY:PY + PH, PX:PX + PW].astype(np.float32)
            fr[PY:PY + PH, PX:PX + PW] = (pf * RM + reg * (1 - RM)).astype(np.uint8)
            x = int(W * (gf + 1) / total)
            fr[H - 8:H, :x] = ACC; fr[H - 8:H, x:] = (30, 42, 76)
            p.stdin.write(fr.tobytes()); gf += 1; lf += 1
        prev = curf
    p.stdin.close(); assert p.wait() == 0
    os.replace(tmp, fin)
    sf.write(f"{OUT}/scene_{si:02d}.wav", np.concatenate(audio), SR)
    print("rendered", si, nframes / FPS, flush=True)
