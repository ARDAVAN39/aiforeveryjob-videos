"""Illustrated presenter, drawn as SVG layers and rendered to sprites.
One config per profession: change colours, hair, outfit, props and backdrop."""
import io, cairosvg, numpy as np
from PIL import Image

PW, PH = 440, 640

STUDENT = dict(
    skin="#EDBE98", skin_shade="#D9A27A", hair="#3B2A20", outfit="#F2B63D", outfit_shade="#D99A22",
    accent="#56CCF2", wall_top="#2A3D70", wall_bot="#141D3A",
)

STUDENT.update(room="study", outfit_style="hoodie", hair_style="bun", glasses=True)
MANAGER = dict(skin="#C8936C", skin_shade="#B07C58", hair="#1F1A1A", outfit="#2F4A7A", outfit_shade="#22375C",
    accent="#F4F1DE", wall_top="#34405F", wall_bot="#151B2E", room="office", outfit_style="blazer", hair_style="short", glasses=False)
TEACHER = dict(skin="#8D5A3B", skin_shade="#74452B", hair="#1A1210", outfit="#9C3D4E", outfit_shade="#7E2F3E",
    accent="#CFE3F5", wall_top="#5A4636", wall_bot="#2B2019", room="classroom", outfit_style="cardigan", hair_style="curly",
    glasses=False, beard=True)
PRESENTERS = {"student": STUDENT, "manager": MANAGER, "teacher": TEACHER}

def _svg(body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{PW*2}" height="{PH*2}" viewBox="0 0 {PW} {PH}">{body}</svg>'

def _render(body):
    png = cairosvg.svg2png(bytestring=_svg(body).encode())
    return Image.open(io.BytesIO(png)).convert("RGBA").resize((PW, PH), Image.LANCZOS)

def backdrop(c):
    if c["room"] == "classroom":
        chalk = 'stroke="#EEF3E8" stroke-width="3" fill="none" stroke-linecap="round" opacity="0.85"'
        return f'''<defs><linearGradient id="w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c["wall_top"]}"/><stop offset="1" stop-color="{c["wall_bot"]}"/></linearGradient></defs>
        <rect width="{PW}" height="{PH}" fill="url(#w)"/>
        <rect x="10" y="34" width="420" height="200" rx="8" fill="#B07A45"/><rect x="20" y="44" width="400" height="180" rx="4" fill="#2F5D4A"/>
        <rect x="14" y="226" width="412" height="10" rx="3" fill="#8A5A30"/><rect x="60" y="220" width="20" height="6" rx="2" fill="#F4F1DE"/><rect x="350" y="220" width="26" height="6" rx="2" fill="#F2B63D"/>
        <text x="34" y="96" font-family="Inter" font-weight="600" font-size="30" fill="#EEF3E8" opacity="0.85">a+b</text>
        <path d="M36 120 L104 120" {chalk}/>
        <text x="34" y="160" font-family="Inter" font-weight="600" font-size="26" fill="#EEF3E8" opacity="0.85">2×3=6</text>
        <path d="M44 188 L60 204 L92 176" {chalk}/>
        <text x="334" y="96" font-family="Inter" font-weight="700" font-size="32" fill="#EEF3E8" opacity="0.85">ABC</text>
        <circle cx="378" cy="150" r="26" {chalk}/><path d="M352 150 L404 150 M378 124 C364 138 364 162 378 176 C392 162 392 138 378 124" {chalk}/>
        <rect x="24" y="304" width="88" height="16" rx="3" fill="#56CCF2"/><rect x="30" y="288" width="78" height="16" rx="3" fill="#F2B63D"/><rect x="22" y="320" width="94" height="16" rx="3" fill="#E76F51"/>
        <circle cx="70" cy="270" r="17" fill="#D64545"/><path d="M70 254 Q72 246 78 242" stroke="#5B3A1E" stroke-width="3" fill="none"/><ellipse cx="80" cy="248" rx="8" ry="4" fill="#5FAF5A" transform="rotate(-25 80 248)"/>
        <circle cx="378" cy="292" r="30" fill="#F4F1DE"/><circle cx="378" cy="292" r="25" fill="#FFFFFF" stroke="#1B2A4A" stroke-width="3"/>
        <path d="M378 292 L378 274 M378 292 L390 298" stroke="#1B2A4A" stroke-width="3.5" stroke-linecap="round"/>'''
    if c["room"] == "office":
        b = f'''<defs><linearGradient id="w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c["wall_top"]}"/><stop offset="1" stop-color="{c["wall_bot"]}"/></linearGradient>
        <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8FD3F4"/><stop offset="1" stop-color="#FCE8B8"/></linearGradient></defs>
        <rect width="{PW}" height="{PH}" fill="url(#w)"/>
        <rect x="22" y="56" width="150" height="170" rx="8" fill="#0E1426"/><rect x="30" y="64" width="134" height="154" rx="4" fill="url(#sky)"/>
        <rect x="42" y="150" width="24" height="68" fill="#5B7BB0"/><rect x="70" y="120" width="30" height="98" fill="#40598A"/><rect x="104" y="140" width="22" height="78" fill="#6C8CC0"/><rect x="130" y="166" width="28" height="52" fill="#40598A"/>
        <rect x="95" y="64" width="5" height="154" fill="#0E1426"/><rect x="30" y="136" width="134" height="5" fill="#0E1426"/>
        <rect x="290" y="66" width="130" height="120" rx="8" fill="#F4F1DE"/>
        <rect x="308" y="130" width="18" height="40" rx="3" fill="#56CCF2"/><rect x="334" y="108" width="18" height="62" rx="3" fill="#F2B63D"/><rect x="360" y="120" width="18" height="50" rx="3" fill="#E76F51"/><rect x="386" y="90" width="18" height="80" rx="3" fill="#2A9D8F"/>
        <path d="M306 100 L338 88 L366 96 L402 76" stroke="#1B2A4A" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
        <rect x="352" y="232" width="62" height="54" rx="5" fill="#F2B63D" opacity="0.9" transform="rotate(5 383 259)"/>'''
        return b
    books_l = [(24, 22, "#E76F51"), (48, 16, "#56CCF2"), (66, 24, "#F2B63D"), (92, 14, "#8E7CC3"), (108, 20, "#2A9D8F")]
    books_r = [(312, 18, "#8E7CC3"), (332, 24, "#E76F51"), (358, 14, "#F4F1DE"), (374, 22, "#2A9D8F"), (398, 18, "#56CCF2")]
    b = f'''<defs><linearGradient id="w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c["wall_top"]}"/><stop offset="1" stop-color="{c["wall_bot"]}"/></linearGradient>
    <radialGradient id="g" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#FFE9A8" stop-opacity="0.55"/><stop offset="1" stop-color="#FFE9A8" stop-opacity="0"/></radialGradient></defs>
    <rect width="{PW}" height="{PH}" fill="url(#w)"/>
    <circle cx="372" cy="70" r="150" fill="url(#g)"/>'''
    for x, w, col in books_l + books_r:
        h = 70 + (x * 7) % 34
        b += f'<rect x="{x}" y="{196-h}" width="{w}" height="{h}" rx="3" fill="{col}"/>'
    b += '<rect x="10" y="196" width="130" height="9" rx="3" fill="#0E1630"/><rect x="300" y="196" width="130" height="9" rx="3" fill="#0E1630"/>'
    # pinned notes
    b += '<rect x="34" y="250" width="54" height="54" rx="4" fill="#F2B63D" opacity="0.9" transform="rotate(-6 61 277)"/><rect x="356" y="262" width="50" height="50" rx="4" fill="#56CCF2" opacity="0.85" transform="rotate(7 381 287)"/>'
    return b

def body(c):
    if c["outfit_style"] == "cardigan":
        return f'''
    <rect x="190" y="372" width="60" height="90" rx="22" fill="{c["skin_shade"]}"/>
    <path d="M36 640 C36 524 88 464 172 446 L220 482 L268 446 C352 464 404 524 404 640 Z" fill="{c["outfit"]}"/>
    <path d="M168 446 L220 640 L272 446 L220 470 Z" fill="{c["accent"]}"/>
    <path d="M184 436 L220 470 L200 492 L170 450 Z" fill="#FFFFFF"/><path d="M256 436 L220 470 L240 492 L270 450 Z" fill="#FFFFFF"/>
    <path d="M168 446 L220 640" stroke="{c["outfit_shade"]}" stroke-width="10"/><path d="M272 446 L220 640" stroke="{c["outfit_shade"]}" stroke-width="10"/>
    <circle cx="190" cy="540" r="5" fill="#F4F1DE"/><circle cx="198" cy="580" r="5" fill="#F4F1DE"/><circle cx="206" cy="620" r="5" fill="#F4F1DE"/>
    <path d="M76 640 C78 580 92 548 112 528" stroke="{c["outfit_shade"]}" stroke-width="5" fill="none" stroke-linecap="round"/>
    <path d="M364 640 C362 580 348 548 328 528" stroke="{c["outfit_shade"]}" stroke-width="5" fill="none" stroke-linecap="round"/>
    <rect x="276" y="548" width="58" height="50" rx="8" fill="{c["outfit_shade"]}"/>
    <rect x="290" y="522" width="8" height="40" rx="2" fill="#F2B63D"/><path d="M290 522 L294 512 L298 522 Z" fill="#E9C9A0"/>
    <rect x="304" y="528" width="7" height="34" rx="2" fill="#56CCF2"/>'''
    if c["outfit_style"] == "blazer":
        return f'''
    <rect x="190" y="372" width="60" height="90" rx="22" fill="{c["skin_shade"]}"/>
    <path d="M36 640 C36 524 88 464 172 446 L220 482 L268 446 C352 464 404 524 404 640 Z" fill="{c["outfit"]}"/>
    <path d="M176 446 L220 600 L264 446 L220 474 Z" fill="{c["accent"]}"/>
    <path d="M186 432 L220 476 L196 500 L172 448 Z" fill="#FFFFFF"/><path d="M254 432 L220 476 L244 500 L268 448 Z" fill="#FFFFFF"/>
    <path d="M172 446 L146 512 L190 548 L214 640 L170 640 L120 520 Z" fill="{c["outfit_shade"]}"/>
    <path d="M268 446 L294 512 L250 548 L226 640 L270 640 L320 520 Z" fill="{c["outfit_shade"]}"/>
    <path d="M172 446 L146 512 L190 548 L220 600 L176 448 Z" fill="{c["outfit"]}" stroke="{c["outfit_shade"]}" stroke-width="3"/>
    <path d="M268 446 L294 512 L250 548 L220 600 L264 448 Z" fill="{c["outfit"]}" stroke="{c["outfit_shade"]}" stroke-width="3"/>
    <rect x="286" y="560" width="46" height="8" rx="3" fill="{c["accent"]}"/>'''
    return f'''
    <path d="M118 250 C96 330 104 420 128 470 L312 470 C336 420 344 330 322 250 Z" fill="{c["hair"]}"/>
    <ellipse cx="220" cy="452" rx="128" ry="52" fill="{c["outfit_shade"]}"/>
    <rect x="192" y="372" width="56" height="86" rx="22" fill="{c["skin_shade"]}"/>
    <path d="M36 640 C36 524 88 464 172 446 L220 482 L268 446 C352 464 404 524 404 640 Z" fill="{c["outfit"]}"/>
    <path d="M172 446 L220 482 L268 446 L256 440 L220 466 L184 440 Z" fill="{c["outfit_shade"]}"/>
    <path d="M204 478 L200 548" stroke="#FFF6DD" stroke-width="5" stroke-linecap="round"/><path d="M236 478 L240 548" stroke="#FFF6DD" stroke-width="5" stroke-linecap="round"/>
    <circle cx="200" cy="552" r="5" fill="#FFF6DD"/><circle cx="240" cy="552" r="5" fill="#FFF6DD"/>
    <path d="M146 452 C150 520 290 520 294 452" stroke="{c["accent"]}" stroke-width="13" fill="none" stroke-linecap="round"/>
    <rect x="128" y="414" width="34" height="58" rx="14" fill="#1B2A4A"/><rect x="278" y="414" width="34" height="58" rx="14" fill="#1B2A4A"/>
    <rect x="134" y="424" width="22" height="38" rx="9" fill="{c["accent"]}"/><rect x="284" y="424" width="22" height="38" rx="9" fill="{c["accent"]}"/>
    <path d="M70 640 C74 590 86 560 104 540" stroke="{c["outfit_shade"]}" stroke-width="5" fill="none" stroke-linecap="round"/>
    <path d="M370 640 C366 590 354 560 336 540" stroke="{c["outfit_shade"]}" stroke-width="5" fill="none" stroke-linecap="round"/>'''

MOUTHS = [
    '<path d="M198 350 Q220 366 242 350" stroke="#8A3B3B" stroke-width="5" fill="none" stroke-linecap="round"/>',
    '<path d="M199 349 Q220 374 241 349 Q220 357 199 349 Z" fill="#6B252B" stroke="#6B252B" stroke-width="2" stroke-linejoin="round"/>',
    '<path d="M198 347 Q220 343 242 347 Q238 381 220 381 Q202 381 198 347 Z" fill="#5E1F24"/><path d="M203 348 Q220 345 237 348 L235 356 Q220 353 205 356 Z" fill="#FFFFFF"/><ellipse cx="220" cy="373" rx="11" ry="6" fill="#E2707A"/>',
    '<path d="M196 346 Q220 341 244 346 Q240 394 220 394 Q200 394 196 346 Z" fill="#5E1F24"/><path d="M202 347 Q220 344 238 347 L236 357 Q220 354 204 357 Z" fill="#FFFFFF"/><ellipse cx="220" cy="384" rx="13" ry="7" fill="#E2707A"/>',
    '<ellipse cx="220" cy="361" rx="12" ry="15" fill="#5E1F24"/><ellipse cx="220" cy="370" rx="7" ry="5" fill="#E2707A"/>',
]

def head(c, mouth, blink):
    if blink:
        eyes = '<path d="M163 294 Q178 305 193 294" stroke="#2E1F18" stroke-width="5" fill="none" stroke-linecap="round"/><path d="M247 294 Q262 305 277 294" stroke="#2E1F18" stroke-width="5" fill="none" stroke-linecap="round"/>'
    else:
        eyes = ''.join(f'<ellipse cx="{x}" cy="292" rx="15" ry="17" fill="#FFFFFF"/><circle cx="{x+1}" cy="294" r="9.5" fill="#2E1F18"/><circle cx="{x+4}" cy="290" r="3.2" fill="#FFFFFF"/>' for x in (178, 262))
    if c["hair_style"] == "curly":
        import math
        hair = f'<path d="M122 286 C104 176 184 140 222 144 C300 140 340 204 318 288 C312 246 298 222 272 210 C232 222 180 222 150 214 C134 234 126 260 122 286 Z" fill="{c["hair"]}"/>'
        for i in range(13):
            a = math.pi * (1.05 - 1.1 * i / 12)
            x, y = 220 + 104 * math.cos(a), 250 - 100 * math.sin(a)
            hair += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{27 if 2 < i < 10 else 22}" fill="{c["hair"]}"/>'
    elif c["hair_style"] == "short":
        hair = f'<path d="M122 282 C106 172 182 146 222 150 C298 144 338 204 318 284 C312 244 300 216 272 204 C232 216 180 216 150 208 C134 228 126 254 122 282 Z" fill="{c["hair"]}"/>'
    else:
        hair = f'<circle cx="220" cy="146" r="38" fill="{c["hair"]}"/><path d="M119 286 C104 176 188 150 228 160 C300 148 344 210 321 292 C312 250 292 226 262 216 C230 242 172 246 140 236 C128 250 122 268 119 286 Z" fill="{c["hair"]}"/>'
    glasses = '<circle cx="178" cy="293" r="27" fill="none" stroke="#1B2A4A" stroke-width="4.5"/><circle cx="262" cy="293" r="27" fill="none" stroke="#1B2A4A" stroke-width="4.5"/><path d="M205 290 Q220 283 235 290" stroke="#1B2A4A" stroke-width="4.5" fill="none"/>' if c["glasses"] else ''
    beard = ''
    if c.get("beard"):
        beard = f'<path d="M126 300 C128 372 170 414 220 416 C270 414 312 372 314 300 C304 340 286 356 264 352 Q220 338 176 352 C154 356 136 340 126 300 Z" fill="{c["hair"]}"/><path d="M190 340 Q205 330 220 336 Q235 330 250 340 Q236 346 220 342 Q204 346 190 340 Z" fill="{c["hair"]}"/>'
    blush = '0.5' if c["glasses"] else '0.25'
    return f'''
    <circle cx="124" cy="302" r="16" fill="{c["skin_shade"]}"/><circle cx="316" cy="302" r="16" fill="{c["skin_shade"]}"/>
    <ellipse cx="220" cy="290" rx="96" ry="108" fill="{c["skin"]}"/>
    {hair}
    <path d="M160 262 Q178 251 196 259" stroke="{c["hair"]}" stroke-width="6" fill="none" stroke-linecap="round"/><path d="M244 259 Q262 251 280 262" stroke="{c["hair"]}" stroke-width="6" fill="none" stroke-linecap="round"/>
    {beard}
    {eyes}
    {glasses}
    <path d="M216 320 Q222 328 229 321" stroke="{c["skin_shade"]}" stroke-width="3.5" fill="none" stroke-linecap="round"/>
    <ellipse cx="150" cy="334" rx="14" ry="8" fill="#F29B8E" opacity="{blush}"/><ellipse cx="290" cy="334" rx="14" ry="8" fill="#F29B8E" opacity="{blush}"/>
    {MOUTHS[mouth]}'''

class Presenter:
    def __init__(self, cfg=STUDENT):
        self.bg = _render(backdrop(cfg)).convert("RGB")
        self.body = _render(body(cfg))
        self.heads = {(m, b): _render(head(cfg, m, b)) for m in range(5) for b in (0, 1)}
        self.cache = {}
    def frame(self, mouth, blink, dy):
        k = (mouth, blink, dy)
        if k not in self.cache:
            im = self.bg.copy()
            im.paste(self.body, (0, max(0, dy // 2)), self.body)
            h = self.heads[(mouth, blink)]
            im.paste(h, (0, dy), h)
            self.cache[k] = np.asarray(im, dtype=np.float32)
        return self.cache[k]

if __name__ == "__main__":
    import sys
    p = Presenter(PRESENTERS[sys.argv[1]])
    sheet = Image.new("RGB", (PW * 5, PH))
    for i, (m, b) in enumerate([(0, 0), (1, 0), (2, 0), (3, 0), (4, 1)]):
        sheet.paste(Image.fromarray(p.frame(m, b, 0).astype(np.uint8)), (i * PW, 0))
    import os; d = os.path.expanduser("~/work"); os.makedirs(d, exist_ok=True); sheet.save(d + "/character_sheet_" + sys.argv[1] + ".png"); print(d + "/character_sheet_" + sys.argv[1] + ".png")
