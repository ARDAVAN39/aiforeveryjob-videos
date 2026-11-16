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
DOCTOR = dict(skin="#E3B48E", skin_shade="#C99670", hair="#2A1F2E", outfit="#F7F9FB", outfit_shade="#D5DEE6",
    accent="#2A9D8F", wall_top="#DCEBEA", wall_bot="#9FC3C4", room="clinic", outfit_style="coat", hair_style="bob",
    glasses=False)
DEVELOPER = dict(skin="#F5D5BC", skin_shade="#E2B497", hair="#B4532A", outfit="#3B4252", outfit_shade="#2A2F3B",
    accent="#7EE787", tee="#E9EEF3", wall_top="#2E2A4A", wall_bot="#14121F", room="devroom", outfit_style="zip_hoodie",
    hair_style="quiff", glasses="square")
SHOPOWNER = dict(skin="#6B4430", skin_shade="#553423", hair="#17110E", outfit="#E9DCC6", outfit_shade="#C9B79B",
    accent="#E07A3F", apron="#2F6F68", apron_shade="#235650", wall_top="#F3E3C8", wall_bot="#D9BE95", room="shop", outfit_style="apron",
    hair_style="waves", glasses=False)
DENTIST = dict(skin="#A8714D", skin_shade="#8E5C3B", hair="#18161C", outfit="#5B8DC9", outfit_shade="#4673AD",
    accent="#7FD1C1", mask="#BFE3F2", wall_top="#FCEFE3", wall_bot="#F0CDB6", room="dental", outfit_style="scrubs",
    hair_style="side_part", glasses=False)
LAWYER = dict(skin="#E9C2A0", skin_shade="#D3A47F", hair="#141218", outfit="#3B3F4C", outfit_shade="#2A2D37",
    accent="#C9A227", blouse="#F6F2EA", wall_top="#6B4A3A", wall_bot="#3A251C", room="law_office", outfit_style="suit",
    hair_style="long_straight", glasses="thin")
NURSE = dict(skin="#D9A47A", skin_shade="#BF8A60", hair="#1C1714", outfit="#7A2E4A", outfit_shade="#5E2238",
    accent="#F2B63D", undershirt="#2B2F3A", wall_top="#E8EAF4", wall_bot="#C3C9E0", room="ward", outfit_style="nurse_scrubs",
    hair_style="buzz", glasses=True)
MARKETER = dict(skin="#F0C7A0", skin_shade="#D9A982", hair="#121014", outfit="#4A6FA5", outfit_shade="#38578A",
    accent="#FF6B6B", tee="#F4F1DE", wall_top="#FFE2CF", wall_bot="#F6B99B", room="agency", outfit_style="denim_shirt",
    hair_style="fringe", glasses=False)
ACCOUNTANT = dict(skin="#B9825C", skin_shade="#9F6A46", hair="#1A1414", outfit="#2F5D50", outfit_shade="#234A3F",
    accent="#E9A23B", shirt="#F6F1E7", wall_top="#E3ECDD", wall_bot="#B8CDB1", room="ledger_office", outfit_style="sweater_vest",
    hair_style="ponytail", glasses="thin")
DESIGNER = dict(skin="#5C3A24", skin_shade="#47291A", hair="#141010", outfit="#E4B33C", outfit_shade="#C69524",
    accent="#7B5CE0", wall_top="#F4EFE6", wall_bot="#DCD3C4", room="design_studio", outfit_style="turtleneck",
    hair_style="afro", glasses=False, earrings="#E4B33C")
SALES = dict(skin="#B9835A", skin_shade="#9E6A44", hair="#1E1612", outfit="#CFE0F2", outfit_shade="#A9C3DE",
    accent="#F25F4C", tie="#1F3A5F", wall_top="#E6EEF6", wall_bot="#BFD0E2", room="sales_floor", outfit_style="oxford_tie",
    hair_style="slick_back", glasses=False, stubble=True)
HR = dict(skin="#E0B48C", skin_shade="#C8976E", hair="#C9C6C2", outfit="#E9735A", outfit_shade="#C95A43",
    accent="#2B7A78", scarf="#2B7A78", scarf_dot="#F6D365", wall_top="#F1EAF4", wall_bot="#D3C6DC", room="people_office", outfit_style="blouse_scarf",
    hair_style="pixie", glasses="cat_eye", earrings_stud="#F6D365")
REALTOR = dict(skin="#D8A27C", skin_shade="#BE875F", hair="#8A3B22", outfit="#5B3A8C", outfit_shade="#46296F",
    accent="#F2A541", top="#FBF4E6", gold="#E0A526", wall_top="#FFF7DA", wall_bot="#F1DDA4", room="open_house", outfit_style="open_blazer",
    hair_style="long_curly", glasses=False, earrings_stud="#E0A526")
RESEARCHER = dict(skin="#C99872", skin_shade="#AE7D58", hair="#B9B4AC", outfit="#F7F8FA", outfit_shade="#D3DAE2",
    accent="#3A7CA5", sweater="#3B5B4A", sweater_shade="#2C4638", wall_top="#E4EEF0", wall_bot="#B9CDD2", room="lab", outfit_style="lab_coat",
    hair_style="receding", glasses=True, beard=True)
SUPPORT = dict(skin="#D6A27A", skin_shade="#BC875F", hair="#1A1418", outfit="#3157C9", outfit_shade="#2443A3",
    accent="#FFC857", wall_top="#E3F4EF", wall_bot="#B7DCD1", room="support_desk", outfit_style="polo",
    hair_style="space_buns", glasses=False, headset="#2B2F3A")
JOURNALIST = dict(skin="#C68E62", skin_shade="#AA7349", hair="#2A1E18", outfit="#5E6B3F", outfit_shade="#485330",
    accent="#E63946", tee="#D5D9DE", tee_shade="#B4BAC2", wall_top="#3A4658", wall_bot="#1E2532", room="newsroom", outfit_style="field_jacket",
    hair_style="tousled", glasses=False, stubble=True, mustache=True)
PRESENTERS = {"journalist": JOURNALIST, "support": SUPPORT, "researcher": RESEARCHER, "realtor": REALTOR, "hr": HR, "sales": SALES, "designer": DESIGNER, "accountant": ACCOUNTANT, "marketer": MARKETER, "nurse": NURSE, "lawyer": LAWYER, "dentist": DENTIST, "shopowner": SHOPOWNER, "student": STUDENT, "manager": MANAGER, "teacher": TEACHER, "doctor": DOCTOR, "developer": DEVELOPER}

def _svg(body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{PW*2}" height="{PH*2}" viewBox="0 0 {PW} {PH}">{body}</svg>'

def _render(body):
    png = cairosvg.svg2png(bytestring=_svg(body).encode())
    return Image.open(io.BytesIO(png)).convert("RGBA").resize((PW, PH), Image.LANCZOS)

def _monitor(x, y, w, h, seed):
    """Monitor with coloured code lines on a dark editor theme, stand down to the desk at y+h+30."""
    cols = ["#C792EA", "#82AAFF", "#7EE787", "#F78C6C", "#FFCB6B", "#89DDFF"]
    m = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="#0B0D14"/><rect x="{x+5}" y="{y+5}" width="{w-10}" height="{h-12}" rx="3" fill="#1E2233"/>'
    m += f'<rect x="{x+5}" y="{y+5}" width="{w-10}" height="7" fill="#2C3148"/>'
    m += ''.join(f'<circle cx="{x+11+i*7}" cy="{y+8.5}" r="2" fill="{c}"/>' for i, c in enumerate(["#FF5F57", "#FEBC2E", "#28C840"]))
    ly, i = y + 20, 0
    while ly < y + h - 12:
        ind = [0, 8, 8, 16, 8, 0, 8, 16][(i + seed) % 8]
        lx = x + 11 + ind
        for k in range(1 + (i + seed) % 3):
            lw = 8 + ((i * 7 + k * 5 + seed * 3) % 5) * 5
            if lx + lw > x + w - 10: break
            m += f'<rect x="{lx}" y="{ly}" width="{lw}" height="4" rx="2" fill="{cols[(i * 2 + k + seed) % 6]}"/>'
            lx += lw + 4
        ly += 8; i += 1
    cx = x + w // 2
    m += f'<rect x="{cx-6}" y="{y+h}" width="12" height="24" fill="#0B0D14"/><rect x="{cx-17}" y="{y+h+22}" width="34" height="8" rx="3" fill="#0B0D14"/>'
    return m

def _tooth(cx, cy, k, fill, stroke="none", sw=0):
    """Generic molar outline centred at (cx, cy), scaled by k."""
    d = "M-20 -18 Q-22 -32 -10 -31 Q0 -26 10 -31 Q22 -32 20 -18 Q20 0 14 6 L10 30 Q6 35 3 28 L0 12 L-3 28 Q-6 35 -10 30 L-14 6 Q-20 0 -20 -18 Z"
    return f'<path d="{d}" transform="translate({cx} {cy}) scale({k})" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>'

def backdrop(c):
    if c["room"] == "newsroom":
        clocks = ''
        for x, lab, ang in [(32, "NYC", 300), (78, "LDN", 60)]:
            import math
            hx, hy = x + 11 * math.sin(math.radians(ang)), 184 - 11 * math.cos(math.radians(ang))
            clocks += f'<circle cx="{x}" cy="184" r="17" fill="#F4F1DE" stroke="#0F141C" stroke-width="3"/><path d="M{x} 184 L{x} 172 M{x} 184 L{hx:.0f} {hy:.0f}" stroke="#0F141C" stroke-width="2.5" stroke-linecap="round"/><text x="{x}" y="216" font-family="Inter" font-weight="800" font-size="9" fill="#C9D2DE" text-anchor="middle">{lab}</text>'
        clips = ''
        for x, y, w, h, r in [(326, 70, 40, 50, -4), (374, 66, 42, 36, 3), (330, 132, 36, 44, 2), (378, 114, 38, 54, -3)]:
            lines = ''.join(f'<rect x="{x+5}" y="{y+12+k*7}" width="{w-10 if k % 2 == 0 else w-18}" height="3" rx="1" fill="#9AA6B2"/>' for k in range(int((h-16)/7)))
            clips += f'<g transform="rotate({r} {x+w/2} {y+h/2})"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#FBFAF5"/><rect x="{x+5}" y="{y+5}" width="{w-10}" height="4" rx="1" fill="#2B3A42"/>{lines}</g>'
        pins = [(346, 72), (395, 68), (348, 134), (397, 116)]
        string = '<path d="M346 72 L397 116 L348 134 L395 68" stroke="#E63946" stroke-width="1.8" fill="none"/>'
        pin_dots = ''.join(f'<circle cx="{x}" cy="{y}" r="4" fill="#E63946"/>' for x, y in pins)
        return f'''<defs><linearGradient id="w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c["wall_top"]}"/><stop offset="1" stop-color="{c["wall_bot"]}"/></linearGradient></defs>
        <rect width="{PW}" height="{PH}" fill="url(#w)"/>
        <rect x="12" y="44" width="148" height="104" rx="6" fill="#0F141C"/><rect x="18" y="50" width="136" height="80" rx="3" fill="#24476B"/>
        <rect x="18" y="50" width="136" height="80" rx="3" fill="#3B6FA0" opacity="0.5"/><circle cx="118" cy="82" r="20" fill="#7FB3E0" opacity="0.5"/>
        <rect x="24" y="56" width="30" height="12" rx="2" fill="#E63946"/><text x="39" y="65.5" font-family="Inter" font-weight="800" font-size="8" fill="#FFFFFF" text-anchor="middle">LIVE</text>
        <rect x="18" y="104" width="136" height="16" fill="#F4F1DE"/><rect x="24" y="109" width="78" height="6" rx="2" fill="#1E2532"/>
        <rect x="18" y="120" width="136" height="10" fill="#E63946"/><rect x="24" y="123.5" width="40" height="3" rx="1" fill="#FFFFFF"/><rect x="70" y="123.5" width="30" height="3" rx="1" fill="#FFFFFF"/><rect x="106" y="123.5" width="42" height="3" rx="1" fill="#FFFFFF"/>
        <rect x="80" y="148" width="12" height="8" fill="#0F141C"/>{clocks}
        <rect x="312" y="54" width="118" height="140" rx="4" fill="#B98B5E" stroke="#6E4E31" stroke-width="5"/>{clips}{string}{pin_dots}
        <rect x="0" y="292" width="{PW}" height="348" fill="#5A4636"/><rect x="0" y="286" width="{PW}" height="8" fill="#3B2C21"/>
        <path d="M20 286 L32 246 L104 246 L96 286 Z" fill="#2B3A42"/><path d="M28 280 L38 252 L98 252 L92 280 Z" fill="#7FB3E0" opacity="0.7"/><rect x="14" y="284" width="96" height="5" rx="2" fill="#1B232B"/>
        
        <rect x="336" y="262" width="56" height="24" rx="2" fill="#FBF3C2" transform="rotate(-6 364 274)"/><path d="M342 266 L384 262 M342 273 L380 269 M343 280 L372 277" stroke="#9AA6B2" stroke-width="2" transform="rotate(-6 364 274)"/>
        <path d="M352 284 L396 252" stroke="#2B3A42" stroke-width="4" stroke-linecap="round"/>
        <rect x="402" y="246" width="20" height="40" rx="5" fill="#1B232B"/><circle cx="412" cy="258" r="5" fill="#56707A"/><circle cx="412" cy="276" r="3" fill="#E63946"/>'''
    if c["room"] == "support_desk":
        cols = [("NEW", 22, "#E76F51", 3), ("OPEN", 66, "#FFC857", 2), ("SOLVED", 110, "#2A9D8F", 3)]
        board = ''
        for name, x, col, n in cols:
            board += f'<text x="{x+19}" y="76" font-family="Inter" font-weight="800" font-size="9" fill="#2B3A42" text-anchor="middle">{name}</text>'
            for k in range(n):
                y = 84 + k * 32
                board += f'<rect x="{x}" y="{y}" width="38" height="26" rx="3" fill="#FFFFFF" stroke="#C9D6D2" stroke-width="1.5"/><rect x="{x}" y="{y}" width="5" height="26" rx="2" fill="{col}"/><rect x="{x+9}" y="{y+6}" width="24" height="4" rx="2" fill="#2B3A42" opacity="0.6"/><rect x="{x+9}" y="{y+15}" width="16" height="4" rx="2" fill="#9AA6B2"/>'
        board += '<path d="M120 200 L124 205 L132 196" stroke="#2A9D8F" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
        return f'''<defs><linearGradient id="w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c["wall_top"]}"/><stop offset="1" stop-color="{c["wall_bot"]}"/></linearGradient></defs>
        <rect width="{PW}" height="{PH}" fill="url(#w)"/>
        <rect x="12" y="56" width="148" height="160" rx="6" fill="#F7FBFA" stroke="#56707A" stroke-width="3"/>
        <path d="M60 64 L60 210 M104 64 L104 210" stroke="#C9D6D2" stroke-width="2"/>{board}
        <path d="M326 64 L414 64 Q424 64 424 74 L424 116 Q424 126 414 126 L360 126 L344 142 L346 126 L326 126 Q316 126 316 116 L316 74 Q316 64 326 64 Z" fill="{c["outfit"]}"/>
        <circle cx="348" cy="95" r="6" fill="#FFFFFF"/><circle cx="370" cy="95" r="6" fill="#FFFFFF"/><circle cx="392" cy="95" r="6" fill="#FFFFFF"/>
        <path d="M344 152 L404 152 Q414 152 414 162 L414 192 Q414 202 404 202 L394 202 L396 216 L380 202 L344 202 Q334 202 334 192 L334 162 Q334 152 344 152 Z" fill="{c["accent"]}"/>
        <path d="M374 166 Q368 158 362 164 Q358 170 374 184 Q390 170 386 164 Q380 158 374 166 Z" fill="#E76F51"/>
        <rect x="0" y="292" width="{PW}" height="348" fill="#56707A"/><rect x="0" y="286" width="{PW}" height="8" fill="#3A4E57"/>
        <rect x="16" y="214" width="90" height="62" rx="5" fill="#1E2838"/><rect x="21" y="219" width="80" height="50" rx="2" fill="#F7FBFA"/>
        <rect x="26" y="225" width="40" height="9" rx="4" fill="#DCE6EA"/><rect x="54" y="238" width="42" height="9" rx="4" fill="{c["outfit"]}"/><rect x="26" y="251" width="34" height="9" rx="4" fill="#DCE6EA"/>
        <rect x="54" y="276" width="14" height="10" fill="#1E2838"/><rect x="42" y="282" width="38" height="6" rx="2" fill="#1E2838"/>
        <rect x="360" y="258" width="28" height="30" rx="4" fill="{c["accent"]}"/><path d="M388 265 Q400 265 400 273 Q400 281 388 281" stroke="{c["accent"]}" stroke-width="4" fill="none"/>
        <path d="M368 252 Q372 244 368 236 M378 252 Q382 244 378 236" stroke="#FFFFFF" stroke-width="2.5" fill="none" opacity="0.8" stroke-linecap="round"/>
        <path d="M408 288 L404 268 L428 268 L424 288 Z" fill="#E76F51"/><ellipse cx="416" cy="262" rx="9" ry="7" fill="#5FAF5A"/><ellipse cx="408" cy="256" rx="6" ry="5" fill="#4E9F6A"/><ellipse cx="423" cy="255" rx="6" ry="5" fill="#4E9F6A"/>'''
    if c["room"] == "lab":
        pts = [(36, 160), (48, 150), (58, 152), (66, 138), (78, 132), (88, 128), (96, 116), (108, 110), (118, 100), (128, 96), (52, 140), (100, 124), (72, 146), (122, 112)]
        dots = ''.join(f'<circle cx="{x}" cy="{y}" r="3.5" fill="{"#E76F51" if i % 4 == 0 else "#3A7CA5"}"/>' for i, (x, y) in enumerate(pts))
        flasks = ''
        for x, col, h in [(326, "#2EC4B6", 30), (360, "#F2B63D", 22), (394, "#E76F51", 26)]:
            flasks += f'<path d="M{x+8} 96 L{x+8} 114 L{x-4} 140 Q{x-6} 146 {x} 146 L{x+24} 146 Q{x+30} 146 {x+28} 140 L{x+16} 114 L{x+16} 96 Z" fill="#FFFFFF" opacity="0.85" stroke="#56707A" stroke-width="2"/>'
            flasks += f'<path d="M{x-1} {146-h*0.55:.0f} L{x+25} {146-h*0.55:.0f} L{x+28} 140 Q{x+30} 146 {x+24} 146 L{x} 146 Q{x-6} 146 {x-4} 140 Z" fill="{col}"/>'
        journals = ''.join(f'<rect x="{x}" y="{196-h}" width="{w}" height="{h}" rx="2" fill="{col}"/>' for x, w, h, col in [(322, 14, 40, "#3A7CA5"), (338, 12, 46, "#3B5B4A"), (352, 16, 38, "#C8553D"), (370, 12, 44, "#F2B63D"), (384, 14, 40, "#56707A")])
        return f'''<defs><linearGradient id="w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c["wall_top"]}"/><stop offset="1" stop-color="{c["wall_bot"]}"/></linearGradient></defs>
        <rect width="{PW}" height="{PH}" fill="url(#w)"/>
        <rect x="16" y="52" width="136" height="146" rx="6" fill="#FFFFFF" stroke="#56707A" stroke-width="3"/>
        <path d="M30 70 L30 176 L142 176" stroke="#2B3A42" stroke-width="2.5" fill="none"/>
        <path d="M32 166 L140 92" stroke="#E76F51" stroke-width="2.5" stroke-dasharray="6 4"/>{dots}
        <rect x="30" y="184" width="50" height="5" rx="2" fill="#2B3A42" opacity="0.5"/>
        <rect x="312" y="146" width="116" height="7" rx="2" fill="#56707A"/>{flasks}
        <rect x="312" y="196" width="116" height="7" rx="2" fill="#56707A"/>{journals}
        <path d="M404 196 L418 160" stroke="#3A7CA5" stroke-width="9" stroke-linecap="round"/>
        <rect x="0" y="292" width="{PW}" height="348" fill="#3E4E56"/><rect x="0" y="286" width="{PW}" height="8" fill="#26323A"/>
        <rect x="18" y="270" width="70" height="8" rx="1" fill="#FFFFFF"/><rect x="22" y="262" width="66" height="8" rx="1" fill="#F4F1DE"/><rect x="16" y="278" width="74" height="8" rx="1" fill="#FFFFFF"/>
        <rect x="30" y="250" width="44" height="12" rx="2" fill="#3B5B4A" transform="rotate(-4 52 256)"/>
        <rect x="104" y="258" width="18" height="28" rx="3" fill="#FFFFFF" opacity="0.85" stroke="#56707A" stroke-width="1.5"/><rect x="106" y="272" width="14" height="12" rx="2" fill="#7EC8E3"/>
        <rect x="350" y="276" width="56" height="10" rx="3" fill="#2B3A42"/><path d="M394 276 L394 222 Q394 214 386 214" stroke="#2B3A42" stroke-width="10" fill="none" stroke-linecap="round"/>
        <rect x="360" y="206" width="14" height="40" rx="4" fill="#E6ECF1" stroke="#2B3A42" stroke-width="3" transform="rotate(-20 367 226)"/>
        <rect x="356" y="252" width="34" height="6" rx="2" fill="#2B3A42"/><circle cx="398" cy="244" r="6" fill="#56707A"/>
        <path d="M366 248 L368 262" stroke="#2B3A42" stroke-width="4"/>'''
    if c["room"] == "open_house":
        keys = ''.join(f'<circle cx="{x}" cy="212" r="3.5" fill="#6A5242"/><path d="M{x} 214 L{x} 224" stroke="#8A8F98" stroke-width="2"/><circle cx="{x}" cy="230" r="6.5" fill="none" stroke="{col}" stroke-width="3.5"/><path d="M{x} 237 L{x} 256 M{x} 248 L{x+5} 248 M{x} 254 L{x+5} 254" stroke="{col}" stroke-width="3.5" stroke-linecap="round"/>' for x, col in [(372, "#E0A526"), (394, "#9AA6B2"), (416, "#E0A526")])
        return f'''<defs><linearGradient id="w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c["wall_top"]}"/><stop offset="1" stop-color="{c["wall_bot"]}"/></linearGradient>
        <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9FD3F2"/><stop offset="1" stop-color="#DDF1FB"/></linearGradient><clipPath id="win"><rect x="18" y="50" width="134" height="150" rx="4"/></clipPath></defs>
        <rect width="{PW}" height="{PH}" fill="url(#w)"/>
        <rect x="12" y="44" width="146" height="162" rx="7" fill="#FFFFFF" stroke="#8C6E5A" stroke-width="3"/>
        <g clip-path="url(#win)"><rect x="18" y="50" width="134" height="150" fill="url(#sky)"/>
        <ellipse cx="50" cy="78" rx="20" ry="8" fill="#FFFFFF" opacity="0.9"/><ellipse cx="66" cy="72" rx="14" ry="8" fill="#FFFFFF" opacity="0.9"/>
        <path d="M18 172 Q70 150 152 166 L152 200 L18 200 Z" fill="#7FBF6A"/>
        <rect x="34" y="128" width="54" height="44" fill="#F6EBD8"/><path d="M28 130 L61 104 L94 130 Z" fill="#C4563E"/><rect x="54" y="148" width="14" height="24" rx="2" fill="#5B3A8C"/><rect x="40" y="138" width="10" height="10" fill="#9FD3F2" stroke="#8C6E5A" stroke-width="1.5"/><rect x="72" y="138" width="10" height="10" fill="#9FD3F2" stroke="#8C6E5A" stroke-width="1.5"/>
        <g transform="translate(-4,8)"><rect x="118" y="118" width="5" height="76" fill="#6A5242"/><rect x="100" y="120" width="23" height="4" fill="#6A5242"/>
        <rect x="98" y="126" width="40" height="30" rx="3" fill="#C4563E"/><text x="118" y="139" font-family="Inter" font-weight="800" font-size="9" fill="#FFFFFF" text-anchor="middle">FOR</text><text x="118" y="151" font-family="Inter" font-weight="800" font-size="9" fill="#FFFFFF" text-anchor="middle">SALE</text></g></g>
        <path d="M85 50 L85 200 M18 122 L152 122" stroke="#FFFFFF" stroke-width="5"/>
        <rect x="6" y="204" width="158" height="9" rx="3" fill="#FFFFFF" stroke="#8C6E5A" stroke-width="2.5"/>
        <rect x="316" y="48" width="110" height="132" rx="5" fill="#FFFFFF" stroke="#8C6E5A" stroke-width="3"/>
        <path d="M330 64 L412 64 L412 164 L330 164 Z M330 108 L366 108 M378 108 L412 108 M372 64 L372 96 M372 120 L372 164 M330 138 L350 138" stroke="#3D3552" stroke-width="3" fill="none" stroke-linejoin="round"/>
        <path d="M350 138 A14 14 0 0 1 364 152" stroke="{c["accent"]}" stroke-width="2.5" fill="none"/><rect x="338" y="72" width="22" height="14" rx="2" fill="#DCD3E4"/><rect x="384" y="130" width="20" height="26" rx="2" fill="#CFE6D2"/><circle cx="392" cy="84" r="8" fill="#F6D9A8"/>
        <rect x="358" y="204" width="72" height="10" rx="4" fill="#8C6E5A"/>{keys}
        <rect x="0" y="292" width="{PW}" height="348" fill="#B98A5E"/><rect x="0" y="288" width="{PW}" height="8" fill="#8C6440"/>
        <path d="M14 288 L26 240 L68 240 L80 288 Z" fill="#FFFFFF" stroke="#8C6E5A" stroke-width="2.5" stroke-linejoin="round"/><text x="47" y="261" font-family="Inter" font-weight="800" font-size="11" fill="{c["outfit"]}" text-anchor="middle">OPEN</text><text x="47" y="277" font-family="Inter" font-weight="800" font-size="11" fill="#C4563E" text-anchor="middle">HOUSE</text>
        <rect x="366" y="272" width="64" height="16" rx="2" fill="#FFFFFF" stroke="#8C6E5A" stroke-width="2"/><rect x="370" y="262" width="58" height="10" rx="2" fill="{c["accent"]}"/><rect x="374" y="277" width="28" height="4" rx="2" fill="#3D3552" opacity="0.5"/>'''
    if c["room"] == "people_office":
        nodes = [(84, 70, "#2B7A78"), (46, 118, "#E9735A"), (84, 118, "#F6D365"), (122, 118, "#7B6BB0"), (32, 166, "#7B6BB0"), (60, 166, "#2B7A78"), (108, 166, "#E9735A"), (136, 166, "#2B7A78")]
        lines = '<path d="M84 70 L84 94 M46 94 L122 94 M46 94 L46 118 M84 94 L84 118 M122 94 L122 118 M46 118 L46 142 M32 142 L60 142 M32 142 L32 166 M60 142 L60 166 M122 118 L122 142 M108 142 L136 142 M108 142 L108 166 M136 142 L136 166" stroke="#5A4E66" stroke-width="2.5" fill="none"/>'
        people = ''.join(f'<circle cx="{x}" cy="{y}" r="11" fill="{col}"/><circle cx="{x}" cy="{y-3}" r="4" fill="#FFFFFF" opacity="0.9"/><path d="M{x-6} {y+7} Q{x} {y} {x+6} {y+7}" fill="#FFFFFF" opacity="0.9"/>' for x, y, col in nodes)
        cal = ''.join(f'<rect x="{332+(i%4)*21}" y="{116+(i//4)*16}" width="16" height="11" rx="2" fill="{["#F6D365","#DCD3E4","#E9735A","#DCD3E4"][i%4] if i in (2, 5, 11) else "#DCD3E4"}"/>' for i in range(12))
        return f'''<defs><linearGradient id="w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c["wall_top"]}"/><stop offset="1" stop-color="{c["wall_bot"]}"/></linearGradient></defs>
        <rect width="{PW}" height="{PH}" fill="url(#w)"/>
        <rect x="14" y="50" width="142" height="138" rx="6" fill="#FFFFFF" stroke="#5A4E66" stroke-width="3"/>
        {lines}{people}
        <rect x="316" y="52" width="108" height="150" rx="6" fill="#FFFFFF" stroke="#5A4E66" stroke-width="3"/>
        <rect x="316" y="52" width="108" height="36" rx="6" fill="#2B7A78"/><rect x="316" y="76" width="108" height="12" fill="#2B7A78"/>
        <text x="370" y="76" font-family="Inter" font-weight="800" font-size="15" fill="#FFFFFF" text-anchor="middle">WELCOME</text>
        <rect x="332" y="98" width="56" height="7" rx="3" fill="#5A4E66" opacity="0.6"/>{cal}
        <path d="M338 178 L346 186 L360 172" stroke="#2B7A78" stroke-width="3.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/><rect x="366" y="176" width="44" height="6" rx="3" fill="#5A4E66" opacity="0.45"/>
        <rect x="0" y="292" width="{PW}" height="348" fill="#8C6E5A"/><rect x="0" y="288" width="{PW}" height="8" fill="#6A5242"/>
        <rect x="20" y="262" width="62" height="10" rx="2" fill="#E9735A"/><rect x="24" y="252" width="56" height="10" rx="2" fill="#F6D365"/><rect x="18" y="272" width="66" height="16" rx="2" fill="#7B6BB0"/>
        <rect x="26" y="276" width="20" height="4" rx="2" fill="#FFFFFF" opacity="0.7"/>
        <path d="M104 288 L100 262 L132 262 L128 288 Z" fill="#2B7A78"/><path d="M116 262 Q104 236 110 222 Q120 240 118 262 Z" fill="#4E9F6A"/><path d="M118 262 Q126 234 142 228 Q136 250 122 262 Z" fill="#5FAF5A"/><path d="M112 262 Q96 248 94 236 Q108 244 116 262 Z" fill="#5FAF5A"/>
        <rect x="352" y="256" width="28" height="32" rx="4" fill="#F1EAF4" stroke="#7B6BB0" stroke-width="2"/><path d="M380 264 Q392 264 392 273 Q392 282 380 282" stroke="#7B6BB0" stroke-width="4" fill="none"/>
        <path d="M361 266 Q366 262 371 266 Q371 272 366 276 Q361 272 361 266 Z" fill="#E9735A"/>
        <path d="M360 250 Q364 242 360 234 M370 250 Q374 242 370 234" stroke="#FFFFFF" stroke-width="2.5" fill="none" opacity="0.7" stroke-linecap="round"/>'''
    if c["room"] == "sales_floor":
        cols = [("#7A8CA8", 3), ("#3D7BD9", 3), ("#F2B63D", 2), ("#2EAD6B", 2)]
        board = ''.join(f'<rect x="{28+i*31}" y="80" width="27" height="6" rx="3" fill="{col}"/>' + ''.join(f'<rect x="{28+i*31}" y="{92+j*26}" width="27" height="21" rx="3" fill="#FFFFFF" stroke="{col}" stroke-width="2"/><rect x="{32+i*31}" y="{98+j*26}" width="17" height="3" rx="1.5" fill="#55657E"/><rect x="{32+i*31}" y="{104+j*26}" width="11" height="3" rx="1.5" fill="#9AA6B8"/>' for j in range(n)) for i, (col, n) in enumerate(cols))
        return f'''<defs><linearGradient id="w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c["wall_top"]}"/><stop offset="1" stop-color="{c["wall_bot"]}"/></linearGradient>
        <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9ED2F0"/><stop offset="1" stop-color="#E8F3FA"/></linearGradient></defs>
        <rect width="{PW}" height="{PH}" fill="url(#w)"/>
        <rect x="18" y="54" width="140" height="160" rx="6" fill="#FFFFFF" stroke="#2B3A52" stroke-width="3"/>
        <rect x="28" y="62" width="70" height="8" rx="4" fill="#2B3A52" opacity="0.75"/>{board}
        <rect x="312" y="54" width="110" height="122" rx="6" fill="#2B3A52"/><rect x="319" y="61" width="96" height="108" rx="3" fill="url(#sky)"/>
        <rect x="326" y="118" width="18" height="51" fill="#8FA9C8"/><rect x="348" y="98" width="22" height="71" fill="#6F8DB3"/><rect x="374" y="128" width="16" height="41" fill="#8FA9C8"/><rect x="394" y="108" width="18" height="61" fill="#6F8DB3"/>
        <rect x="365" y="61" width="4" height="108" fill="#2B3A52"/>
        <rect x="352" y="188" width="58" height="8" rx="3" fill="#6B4A32"/><rect x="378" y="180" width="6" height="14" fill="#6B4A32"/>
        <path d="M366 214 Q366 196 381 196 Q396 196 396 214 L400 222 L362 222 Z" fill="#E2B13C" stroke="#B8891F" stroke-width="2"/><circle cx="381" cy="226" r="4" fill="#B8891F"/>
        <path d="M381 196 L381 192" stroke="#6B4A32" stroke-width="4"/>
        <rect x="0" y="292" width="{PW}" height="348" fill="#5D6B80"/><rect x="0" y="288" width="{PW}" height="8" fill="#3F4A5A"/>
        <rect x="24" y="252" width="76" height="40" rx="4" fill="#2B3A52"/><rect x="29" y="256" width="66" height="30" rx="2" fill="#DDE7F2"/>
        <path d="M34 280 L48 270 L60 274 L74 262 L88 266" stroke="{c["accent"]}" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
        <rect x="14" y="288" width="96" height="5" rx="2" fill="#1E2838"/>
        
        <rect x="350" y="252" width="30" height="36" rx="4" fill="{c["accent"]}"/><path d="M380 262 Q394 262 394 272 Q394 282 380 282" stroke="{c["accent"]}" stroke-width="5" fill="none"/>
        <path d="M358 246 Q362 238 358 230 M368 246 Q372 238 368 230" stroke="#FFFFFF" stroke-width="2.5" fill="none" opacity="0.7" stroke-linecap="round"/>'''
    if c["room"] == "design_studio":
        wheel = ''.join(f'<path d="M370 120 L{370+44*__import__("math").cos(__import__("math").radians(i*30)):.1f} {120+44*__import__("math").sin(__import__("math").radians(i*30)):.1f} A44 44 0 0 1 {370+44*__import__("math").cos(__import__("math").radians(i*30+30)):.1f} {120+44*__import__("math").sin(__import__("math").radians(i*30+30)):.1f} Z" fill="{["#E5484D","#F06A3B","#F5A524","#F2D03B","#A3D04C","#46B86A","#2EC4B6","#3AA0E0","#3D6FE0","#7B5CE0","#B04FD0","#E0499B"][i]}"/>' for i in range(12))
        cards = ''.join(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{col}" transform="rotate({r} {x+w/2} {y+h/2})"/>' for x, y, w, h, col, r in [(30, 66, 52, 40, "#7B5CE0", -4), (90, 62, 44, 56, "#F28C6B", 3), (34, 116, 40, 40, "#2EC4B6", 2), (82, 126, 58, 34, "#1B1B2F", -2), (40, 166, 96, 18, "#E4B33C", 1)])
        pins = ''.join(f'<circle cx="{x}" cy="{y}" r="3" fill="#C8553D"/>' for x, y in [(56, 64), (112, 60), (54, 114), (111, 124), (88, 164)])
        sw = ''.join(f'<rect x="{336+i*16}" y="178" width="12" height="12" rx="2" fill="{col}"/>' for i, col in enumerate(["#7B5CE0", "#E4B33C", "#2EC4B6", "#F28C6B", "#1B1B2F"]))
        return f'''<defs><linearGradient id="w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c["wall_top"]}"/><stop offset="1" stop-color="{c["wall_bot"]}"/></linearGradient></defs>
        <rect width="{PW}" height="{PH}" fill="url(#w)"/>
        <rect x="18" y="52" width="134" height="144" rx="4" fill="#C9A77C" stroke="#9C7B53" stroke-width="3"/>
        {cards}{pins}
        <circle cx="370" cy="120" r="50" fill="#FFFFFF"/>{wheel}<circle cx="370" cy="120" r="16" fill="#FFFFFF"/>
        {sw}
        <rect x="0" y="292" width="{PW}" height="348" fill="#E9E2D6"/><rect x="0" y="288" width="{PW}" height="8" fill="#BFB5A4"/>
        <path d="M44 288 L60 236 L52 228" stroke="#2B2B33" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M60 236 L92 206" stroke="#2B2B33" stroke-width="5" stroke-linecap="round"/>
        <path d="M84 196 L112 214 L100 226 Z" fill="#7B5CE0"/><circle cx="60" cy="236" r="5" fill="#2B2B33"/>
        <rect x="30" y="284" width="36" height="6" rx="3" fill="#2B2B33"/>
        <rect x="334" y="262" width="80" height="26" rx="4" fill="#2B2B33"/><rect x="340" y="266" width="68" height="18" rx="2" fill="#3C3C48"/>
        <path d="M372 262 L404 222" stroke="#2B2B33" stroke-width="4" stroke-linecap="round"/><path d="M404 222 L408 216" stroke="#7B5CE0" stroke-width="4" stroke-linecap="round"/>
        <rect x="300" y="268" width="22" height="20" rx="3" fill="#F28C6B"/>
        <path d="M304 268 L300 240 M311 268 L314 236 M317 268 L324 244" stroke="#2B2B33" stroke-width="3" stroke-linecap="round"/>'''
    if c["room"] == "ledger_office":
        bars = ''.join(f'<rect x="{36+i*22}" y="{170-h}" width="14" height="{h}" rx="2" fill="{col}"/>' for i, (h, col) in enumerate([(44, "#2F5D50"), (62, "#2F5D50"), (52, "#2F5D50"), (78, "#E9A23B"), (70, "#2F5D50")]))
        cal = ''.join(f'<rect x="{326+(i%5)*18}" y="{100+(i//5)*16}" width="13" height="11" rx="2" fill="{"#E9A23B" if i == 19 else "#DCE3D6"}"/>' for i in range(20))
        binders = ''.join(f'<rect x="{x}" y="{y}" width="20" height="{h}" rx="2" fill="{col}"/><rect x="{x+4}" y="{y+10}" width="12" height="8" rx="1" fill="#FFFFFF" opacity="0.8"/>' for x, y, h, col in [(28, 226, 62, "#2F5D50"), (50, 232, 56, "#C8553D"), (72, 222, 66, "#3D5A80"), (94, 230, 58, "#E9A23B")])
        return f'''<defs><linearGradient id="w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c["wall_top"]}"/><stop offset="1" stop-color="{c["wall_bot"]}"/></linearGradient></defs>
        <rect width="{PW}" height="{PH}" fill="url(#w)"/>
        <rect x="20" y="62" width="128" height="126" rx="6" fill="#FFFFFF" stroke="#4A5A48" stroke-width="3"/>
        <rect x="32" y="74" width="60" height="7" rx="3" fill="#4A5A48" opacity="0.7"/>
        <path d="M30 172 L140 172" stroke="#4A5A48" stroke-width="2"/>{bars}
        <path d="M42 120 L64 104 L86 112 L108 86 L130 94" stroke="#C8553D" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
        <rect x="316" y="58" width="104" height="138" rx="6" fill="#FFFFFF" stroke="#4A5A48" stroke-width="3"/>
        <rect x="316" y="58" width="104" height="30" rx="6" fill="#2F5D50"/><rect x="316" y="78" width="104" height="10" fill="#2F5D50"/>
        <rect x="340" y="68" width="56" height="8" rx="4" fill="#FFFFFF" opacity="0.85"/>{cal}
        <circle cx="398" cy="165" r="11" fill="none" stroke="#C8553D" stroke-width="3"/>
        <rect x="0" y="292" width="{PW}" height="348" fill="#6B5444"/><rect x="0" y="288" width="{PW}" height="8" fill="#4E3C31"/>
        {binders}
        <rect x="350" y="250" width="58" height="40" rx="5" fill="#3B3F4C"/><rect x="356" y="255" width="46" height="10" rx="2" fill="#B9D3A8"/>
        {''.join(f'<rect x="{357+(i%4)*11}" y="{269+(i//4)*7}" width="8" height="5" rx="1.5" fill="{"#E9A23B" if i % 4 == 3 else "#DCE3D6"}"/>' for i in range(12))}
        <path d="M362 250 L362 218 Q370 208 384 214 L392 250" fill="#FFFFFF" stroke="#C9CED6" stroke-width="1.5"/>
        <path d="M368 226 L384 226 M368 234 L386 234 M368 242 L382 242" stroke="#9AA6B2" stroke-width="2"/>'''
    if c["room"] == "agency":
        sw = ''.join(f'<rect x="{30+i*24}" y="72" width="20" height="30" rx="3" fill="{col}"/>' for i, col in enumerate(["#FF6B6B", "#FFB84C", "#2EC4B6", "#3D5A80", "#1B1B2F"]))
        notes = ''.join(f'<rect x="{x}" y="{y}" width="30" height="30" rx="2" fill="{col}" transform="rotate({r} {x+15} {y+15})"/><rect x="{x+5}" y="{y+9}" width="18" height="3" rx="1.5" fill="#1B1B2F" opacity="0.45" transform="rotate({r} {x+15} {y+15})"/><rect x="{x+5}" y="{y+16}" width="12" height="3" rx="1.5" fill="#1B1B2F" opacity="0.45" transform="rotate({r} {x+15} {y+15})"/>'
                        for x, y, col, r in [(32, 120, "#FFE066", -6), (70, 124, "#FF9F9F", 4), (108, 118, "#9FE2D6", -3), (48, 164, "#B9C8FF", 5), (90, 166, "#FFE066", -4)])
        funnel = ''.join(f'<path d="M{330+i*10} {70+i*30} L{410-i*10} {70+i*30} L{404-i*10} {96+i*30} L{336+i*10} {96+i*30} Z" fill="{col}"/>' for i, col in enumerate(["#FF6B6B", "#FFB84C", "#2EC4B6", "#3D5A80"]))
        return f'''<defs><linearGradient id="w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c["wall_top"]}"/><stop offset="1" stop-color="{c["wall_bot"]}"/></linearGradient></defs>
        <rect width="{PW}" height="{PH}" fill="url(#w)"/>
        <rect x="18" y="52" width="136" height="160" rx="6" fill="#FFFFFF" stroke="#1B1B2F" stroke-width="3"/>
        {sw}{notes}
        <rect x="316" y="52" width="108" height="150" rx="6" fill="#1B1B2F"/>
        {funnel}
        <rect x="336" y="190" width="68" height="4" rx="2" fill="#FFFFFF" opacity="0.4"/>
        <rect x="0" y="292" width="{PW}" height="348" fill="#3D2C2E"/><rect x="0" y="288" width="{PW}" height="8" fill="#2A1E20"/>
        <path d="M30 288 L36 252 L74 252 L80 288 Z" fill="#2EC4B6"/><path d="M48 252 Q38 222 46 206 Q56 226 54 252 Z" fill="#4E9F6A"/><path d="M54 252 Q62 220 78 214 Q72 238 58 252 Z" fill="#5FAF5A"/><path d="M50 252 Q30 236 28 222 Q44 232 52 252 Z" fill="#5FAF5A"/>
        <path d="M352 286 L352 262 L396 248 L396 286 Z" fill="#FF6B6B"/><rect x="396" y="244" width="10" height="46" rx="4" fill="#FF6B6B"/><rect x="340" y="262" width="14" height="22" rx="3" fill="#E85555"/>
        <path d="M412 252 Q422 246 426 236 M412 266 L428 266 M412 280 Q422 286 426 296" stroke="#FF6B6B" stroke-width="3" fill="none" stroke-linecap="round"/>'''
    if c["room"] == "ward":
        import math
        ticks = ''.join(f'<path d="M{368+30*math.sin(math.radians(a)):.1f} {78-30*math.cos(math.radians(a)):.1f} L{368+25*math.sin(math.radians(a)):.1f} {78-25*math.cos(math.radians(a)):.1f}" stroke="#1B2A4A" stroke-width="{3 if a % 90 == 0 else 1.6}" stroke-linecap="round"/>' for a in range(0, 360, 30))
        rows = ''.join(f'<circle cx="{38}" cy="{y}" r="5" fill="{col}"/><rect x="50" y="{y-3}" width="{w}" height="6" rx="3" fill="#5A6380" opacity="0.75"/>' for y, col, w in [(110, "#E76F51", 70), (130, "#2A9D8F", 54), (150, "#F2B63D", 78), (170, "#8E7CC3", 46)])
        return f"""<defs><linearGradient id="w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c["wall_top"]}"/><stop offset="1" stop-color="{c["wall_bot"]}"/></linearGradient></defs>
        <rect width="{PW}" height="{PH}" fill="url(#w)"/>
        <rect x="0" y="244" width="{PW}" height="14" fill="#9AA3C2" opacity="0.6"/><rect x="0" y="250" width="{PW}" height="3" fill="#FFFFFF" opacity="0.7"/>
        <rect x="16" y="54" width="132" height="140" rx="6" fill="#B9C0D4"/><rect x="22" y="60" width="120" height="128" rx="3" fill="#FFFFFF"/>
        <rect x="30" y="72" width="70" height="9" rx="3" fill="{c["outfit"]}"/><rect x="104" y="72" width="30" height="9" rx="3" fill="#C3C9E0"/>
        <path d="M30 92 L134 92" stroke="#C3C9E0" stroke-width="2"/>{rows}
        <rect x="40" y="190" width="40" height="5" rx="2" fill="#56CCF2"/><rect x="88" y="190" width="28" height="5" rx="2" fill="#E76F51"/>
        <circle cx="368" cy="78" r="38" fill="#1B2A4A"/><circle cx="368" cy="78" r="33" fill="#FFFFFF"/>{ticks}
        <path d="M368 78 L368 56 M368 78 L384 86" stroke="#1B2A4A" stroke-width="4" stroke-linecap="round"/><path d="M368 78 L352 102" stroke="#E76F51" stroke-width="2" stroke-linecap="round"/><circle cx="368" cy="78" r="3.5" fill="#1B2A4A"/>
        <rect x="408" y="150" width="6" height="320" fill="#9AA6B2"/><path d="M392 150 L430 150" stroke="#9AA6B2" stroke-width="5" stroke-linecap="round"/>
        <path d="M398 152 L398 160 M424 152 L424 160" stroke="#9AA6B2" stroke-width="3"/>
        <rect x="388" y="160" width="22" height="40" rx="8" fill="#DFF3FB" stroke="#7FB8D0" stroke-width="2"/><rect x="392" y="178" width="14" height="18" rx="5" fill="#9ED6EE"/>
        <path d="M399 200 L399 214 Q399 230 410 236" stroke="#7FB8D0" stroke-width="2.5" fill="none"/>
        <rect x="318" y="150" width="54" height="70" rx="6" fill="#FFFFFF" stroke="#9AA6B2" stroke-width="2"/><rect x="328" y="160" width="34" height="22" rx="3" fill="#2A9D8F" opacity="0.85"/>
        <path d="M345 182 L345 196" stroke="#9AA6B2" stroke-width="5"/><rect x="336" y="196" width="18" height="10" rx="3" fill="#9AA6B2"/><circle cx="345" cy="214" r="2.5" fill="#2A9D8F"/>
        <rect x="0" y="300" width="{PW}" height="340" fill="#DCE0EE"/><rect x="0" y="296" width="{PW}" height="8" fill="#A8B0CC"/>
        <rect x="14" y="262" width="78" height="34" rx="4" fill="#FFFFFF" stroke="#A8B0CC" stroke-width="2"/><rect x="22" y="270" width="40" height="5" rx="2" fill="#5A6380"/><rect x="22" y="281" width="56" height="5" rx="2" fill="#A8B0CC"/>
        <rect x="352" y="270" width="22" height="26" rx="5" fill="#E76F51"/><rect x="355" y="262" width="16" height="9" rx="2" fill="#F4F1DE"/>"""
    if c["room"] == "law_office":
        cols = ["#7A2E2E", "#2F5446", "#5A3A22", "#7A2E2E", "#2B3A5C", "#5A3A22", "#2F5446"]
        books = ''
        for side, x0 in (("l", 10), ("r", 316)):
            for shelf_y in (118, 216):
                x = x0
                for i in range(7):
                    w = 14 + (i * 5 + shelf_y + x0) % 6
                    h = 66 + (i * 11 + shelf_y) % 14
                    col = cols[(i + shelf_y // 98 + (x0 > 100)) % len(cols)]
                    books += f'<rect x="{x}" y="{shelf_y-h}" width="{w}" height="{h}" rx="2" fill="{col}"/>'
                    books += f'<rect x="{x}" y="{shelf_y-h+10}" width="{w}" height="3" fill="#C9A227" opacity="0.8"/><rect x="{x}" y="{shelf_y-14}" width="{w}" height="3" fill="#C9A227" opacity="0.8"/>'
                    x += w + 2
                    if x > x0 + 104: break
                books += f'<rect x="{x0-6}" y="{shelf_y}" width="124" height="9" rx="2" fill="#2A1A12"/>'
        return f'''<defs><linearGradient id="w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c["wall_top"]}"/><stop offset="1" stop-color="{c["wall_bot"]}"/></linearGradient>
        <radialGradient id="lampglow" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#FFE7A3" stop-opacity="0.55"/><stop offset="1" stop-color="#FFE7A3" stop-opacity="0"/></radialGradient></defs>
        <rect width="{PW}" height="{PH}" fill="url(#w)"/>
        <rect x="0" y="0" width="134" height="240" fill="#3A251C"/><rect x="310" y="0" width="130" height="240" fill="#3A251C"/>
        {books}
        <rect x="170" y="26" width="100" height="72" rx="3" fill="#C9A227"/><rect x="176" y="32" width="88" height="60" fill="#F6F2EA"/>
        <rect x="190" y="44" width="60" height="5" rx="2" fill="#3A251C" opacity="0.7"/><rect x="198" y="56" width="44" height="4" rx="2" fill="#3A251C" opacity="0.45"/><rect x="194" y="66" width="52" height="4" rx="2" fill="#3A251C" opacity="0.45"/>
        <circle cx="244" cy="82" r="6" fill="#B23A3A"/>
        <rect x="0" y="300" width="{PW}" height="340" fill="#4A2E20"/><rect x="0" y="300" width="{PW}" height="10" fill="#2A1A12"/>
        <ellipse cx="56" cy="262" rx="64" ry="46" fill="url(#lampglow)"/>
        <rect x="46" y="262" width="8" height="38" fill="#C9A227"/><rect x="26" y="294" width="48" height="8" rx="3" fill="#C9A227"/>
        <path d="M14 262 Q50 228 88 262 Z" fill="#2F6B4F"/><rect x="14" y="260" width="74" height="5" rx="2" fill="#C9A227"/>
        <rect x="378" y="232" width="6" height="66" fill="#C9A227"/><rect x="362" y="294" width="38" height="7" rx="3" fill="#C9A227"/>
        <path d="M344 240 L418 240" stroke="#C9A227" stroke-width="4" stroke-linecap="round"/><circle cx="381" cy="230" r="5" fill="#C9A227"/>
        <path d="M350 240 L340 266 M350 240 L360 266 M412 240 L402 266 M412 240 L422 266" stroke="#C9A227" stroke-width="1.6"/>
        <path d="M336 266 Q350 278 364 266 Z" fill="#C9A227"/><path d="M398 266 Q412 278 426 266 Z" fill="#C9A227"/>
        '''
    if c["room"] == "dental":
        brushes = ''.join(f'<rect x="{x}" y="{y}" width="5" height="34" rx="2" fill="{col}" transform="rotate({r} {x+2} {y+34})"/><rect x="{x-1}" y="{y-2}" width="7" height="10" rx="2" fill="#FFFFFF" transform="rotate({r} {x+2} {y+34})"/>'
                          for x, y, col, r in [(362, 196, "#E76F51", -12), (370, 192, "#5B8DC9", 0), (378, 196, "#F2B63D", 12)])
        return f'''<defs><linearGradient id="w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c["wall_top"]}"/><stop offset="1" stop-color="{c["wall_bot"]}"/></linearGradient>
        <radialGradient id="lamp" cx="0.5" cy="0.2" r="0.6"><stop offset="0" stop-color="#FFF7D6" stop-opacity="0.9"/><stop offset="1" stop-color="#FFF7D6" stop-opacity="0"/></radialGradient></defs>
        <rect width="{PW}" height="{PH}" fill="url(#w)"/>
        <rect x="0" y="240" width="{PW}" height="6" fill="#FFFFFF" opacity="0.7"/>
        <path d="M0 26 L64 26 L84 50" stroke="#9AA6B2" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
        <ellipse cx="70" cy="120" rx="70" ry="44" fill="url(#lamp)"/>
        <rect x="40" y="48" width="84" height="40" rx="20" fill="#E6ECF1" stroke="#9AA6B2" stroke-width="3"/>
        <rect x="52" y="78" width="60" height="12" rx="6" fill="#FFF3B0"/>
        <rect x="18" y="140" width="96" height="84" rx="6" fill="#DDE4EA"/><rect x="24" y="146" width="84" height="72" rx="3" fill="#1C2D44"/>
        {_tooth(48, 182, 0.75, "none", "#E9F1F7", 3)}{_tooth(84, 182, 0.75, "none", "#E9F1F7", 3)}
        <rect x="318" y="44" width="104" height="132" rx="8" fill="{c["accent"]}"/><rect x="326" y="52" width="88" height="116" rx="5" fill="#FFFFFF" opacity="0.35"/>
        {_tooth(370, 98, 1.3, "#FFFFFF", "#2E5E66", 3)}
        <path d="M352 92 Q356 86 362 88" stroke="#2E5E66" stroke-width="2.5" fill="none" stroke-linecap="round"/>
        <text x="370" y="158" font-family="Inter" font-weight="800" font-size="16" fill="#2E5E66" text-anchor="middle">SMILE</text>
        <rect x="330" y="230" width="98" height="8" rx="3" fill="#B98B6A"/>
        <path d="M358 230 L356 206 L388 206 L386 230 Z" fill="#7FD1C1"/>{brushes}
        <rect x="398" y="210" width="22" height="20" rx="3" fill="#FFFFFF"/><rect x="401" y="204" width="16" height="7" rx="2" fill="#5B8DC9"/>
        <rect x="0" y="330" width="96" height="310" fill="#FFFFFF"/><rect x="0" y="322" width="102" height="12" rx="3" fill="#D9E2E8"/>
        <rect x="10" y="350" width="76" height="40" rx="4" fill="#EEF2F5"/><rect x="36" y="366" width="24" height="5" rx="2.5" fill="#9AA6B2"/>
        <rect x="10" y="400" width="76" height="40" rx="4" fill="#EEF2F5"/><rect x="36" y="416" width="24" height="5" rx="2.5" fill="#9AA6B2"/>
        <path d="M30 322 Q26 290 40 272 Q46 300 40 322 Z" fill="#4E9F6A"/><path d="M40 322 Q48 286 70 276 Q62 304 52 322 Z" fill="#5FAF5A"/>
        <rect x="24" y="300" width="40" height="22" rx="4" fill="#F2B63D"/>'''
    if c["room"] == "shop":
        awn = ''.join(f'<path d="M{x} 0 L{x+44} 0 L{x+44} 30 Q{x+22} 44 {x} 30 Z" fill="{col}"/>' for x, col in zip(range(0, 440, 44), ["#E07A3F", "#FFF6E8"] * 5))
        jars = ''
        for i, (x, col) in enumerate([(22, "#E9B44C"), (52, "#B5523B"), (82, "#7FA36B"), (112, "#E9B44C")]):
            jars += f'<rect x="{x}" y="96" width="24" height="34" rx="5" fill="{col}" opacity="0.9"/><rect x="{x+2}" y="90" width="20" height="8" rx="2" fill="#6E4B32"/><rect x="{x+4}" y="108" width="16" height="10" rx="2" fill="#FFF6E8"/>'
        for i, (x, w, col) in enumerate([(22, 30, "#2F6F68"), (56, 22, "#E07A3F"), (82, 34, "#F3E3C8"), (120, 24, "#B5523B")]):
            jars += f'<rect x="{x}" y="{176-28-(i%2)*8}" width="{w}" height="{28+(i%2)*8}" rx="4" fill="{col}"/>'
        return f'''<defs><linearGradient id="w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c["wall_top"]}"/><stop offset="1" stop-color="{c["wall_bot"]}"/></linearGradient></defs>
        <rect width="{PW}" height="{PH}" fill="url(#w)"/>
                {awn}
        <rect x="10" y="130" width="140" height="8" rx="3" fill="#6E4B32"/><rect x="10" y="176" width="140" height="8" rx="3" fill="#6E4B32"/>
        {jars}
        <path d="M352 52 L330 84 M352 52 L404 84" stroke="#6E4B32" stroke-width="2.5"/><circle cx="352" cy="52" r="4" fill="#6E4B32"/>
        <rect x="318" y="84" width="100" height="44" rx="8" fill="#2F6F68"/><text x="368" y="115" font-family="Inter" font-weight="800" font-size="22" fill="#FFF6E8" text-anchor="middle">OPEN</text>
        <rect x="326" y="142" width="96" height="80" rx="6" fill="#6E4B32"/><rect x="332" y="148" width="84" height="68" rx="3" fill="#2B2B2B"/>
        <rect x="342" y="160" width="44" height="5" rx="2" fill="#FFF6E8" opacity="0.85"/><rect x="342" y="174" width="60" height="5" rx="2" fill="#FFF6E8" opacity="0.7"/><rect x="342" y="188" width="36" height="5" rx="2" fill="#E9B44C" opacity="0.9"/><rect x="342" y="202" width="52" height="5" rx="2" fill="#FFF6E8" opacity="0.7"/>
        <rect x="0" y="300" width="{PW}" height="340" fill="#8A5E3C"/><rect x="0" y="300" width="{PW}" height="12" fill="#6E4B32"/>
        <rect x="16" y="252" width="64" height="48" rx="6" fill="#3A3F47"/><rect x="24" y="258" width="48" height="18" rx="3" fill="#9FD8CB"/><rect x="24" y="282" width="10" height="8" rx="2" fill="#C9CED6"/><rect x="38" y="282" width="10" height="8" rx="2" fill="#C9CED6"/><rect x="52" y="282" width="10" height="8" rx="2" fill="#E07A3F"/>
        <path d="M376 300 L372 270 L412 270 L408 300 Z" fill="#E07A3F"/><path d="M392 270 Q378 240 386 226 Q396 244 394 270 Z" fill="#4E9F6A"/><path d="M394 270 Q404 238 420 232 Q414 254 398 270 Z" fill="#5FAF5A"/><path d="M388 270 Q370 252 368 240 Q384 248 392 270 Z" fill="#5FAF5A"/>
        <rect x="104" y="276" width="38" height="24" rx="4" fill="#FFF6E8"/><path d="M142 282 Q152 282 152 290 Q152 296 142 296" stroke="#FFF6E8" stroke-width="4" fill="none"/>'''
    if c["room"] == "devroom":
        return f'''<defs><linearGradient id="w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c["wall_top"]}"/><stop offset="1" stop-color="{c["wall_bot"]}"/></linearGradient>
        <radialGradient id="neon" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="{c["accent"]}" stop-opacity="0.35"/><stop offset="1" stop-color="{c["accent"]}" stop-opacity="0"/></radialGradient></defs>
        <rect width="{PW}" height="{PH}" fill="url(#w)"/>
        <ellipse cx="74" cy="72" rx="80" ry="54" fill="url(#neon)"/>
        <text x="74" y="90" font-family="Inter" font-weight="700" font-size="46" fill="none" stroke="{c["accent"]}" stroke-width="3" text-anchor="middle">&lt;/&gt;</text>
        <rect x="300" y="104" width="128" height="8" rx="3" fill="#0B0D14"/>
        <rect x="312" y="62" width="12" height="42" rx="2" fill="#82AAFF"/><rect x="326" y="70" width="10" height="34" rx="2" fill="#F78C6C"/><rect x="338" y="58" width="14" height="46" rx="2" fill="#FFCB6B"/>
        <path d="M376 104 Q368 104 368 94 Q368 84 380 84 Q378 74 388 72 Q398 72 398 82 L408 82 Q404 88 397 88 Q408 92 406 100 Q404 104 396 104 Z" fill="#FFD43B"/>
        <circle cx="391" cy="79" r="1.8" fill="#1B2A4A"/><path d="M398 82 L408 82 Q404 88 397 88 Z" fill="#F78C6C"/>
        <rect x="0" y="252" width="{PW}" height="12" fill="#5B4636"/><rect x="0" y="264" width="{PW}" height="6" fill="#3E2F24"/>
        {_monitor(14, 150, 104, 72, 0)}
        {_monitor(334, 150, 94, 72, 3)}
        <rect x="18" y="232" width="20" height="20" rx="4" fill="#E76F51"/><path d="M38 237 Q47 237 47 243 Q47 249 38 248" stroke="#E76F51" stroke-width="3.5" fill="none"/>
        <path d="M23 228 Q20 222 24 216 M31 228 Q28 222 32 216" stroke="#FFFFFF" stroke-width="2" fill="none" opacity="0.5" stroke-linecap="round"/>
        <path d="M410 234 Q404 216 414 206 Q418 222 414 234 Z" fill="#4E9F6A"/><path d="M414 234 Q420 214 432 210 Q428 226 418 236 Z" fill="#5FAF5A"/><path d="M406 236 Q394 224 396 214 Q408 222 410 236 Z" fill="#5FAF5A"/>
        <path d="M404 236 L426 236 L423 252 L407 252 Z" fill="#C97B5A"/>
        <rect x="18" y="300" width="70" height="44" rx="5" fill="{c["accent"]}" opacity="0.85" transform="rotate(-5 53 322)"/><rect x="28" y="314" width="40" height="5" rx="2" fill="#14121F" opacity="0.6" transform="rotate(-5 53 322)"/><rect x="28" y="326" width="28" height="5" rx="2" fill="#14121F" opacity="0.6" transform="rotate(-5 53 322)"/>'''
    if c["room"] == "clinic":
        return f'''<defs><linearGradient id="w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c["wall_top"]}"/><stop offset="1" stop-color="{c["wall_bot"]}"/></linearGradient></defs>
        <rect width="{PW}" height="{PH}" fill="url(#w)"/>
        <rect x="0" y="236" width="{PW}" height="8" fill="#FFFFFF" opacity="0.6"/>
        <rect x="24" y="52" width="132" height="94" rx="8" fill="#1B2A4A"/><rect x="31" y="59" width="118" height="80" rx="4" fill="#0F2233"/>
        <path d="M38 104 L64 104 L72 88 L80 122 L90 76 L98 112 L104 104 L142 104" stroke="#5FE0B7" stroke-width="3" fill="none" stroke-linejoin="round" stroke-linecap="round"/>
        <rect x="80" y="146" width="20" height="18" fill="#1B2A4A"/><rect x="62" y="162" width="56" height="7" rx="3" fill="#1B2A4A"/>
        <rect x="34" y="186" width="96" height="44" rx="6" fill="#FFFFFF" opacity="0.85"/><rect x="44" y="198" width="54" height="6" rx="3" fill="#9FC3C4"/><rect x="44" y="212" width="72" height="6" rx="3" fill="#9FC3C4"/>
        <rect x="318" y="48" width="98" height="132" rx="6" fill="#FFFFFF"/>
        <text x="367" y="86" font-family="Inter" font-weight="700" font-size="30" fill="#1B2A4A" text-anchor="middle">E</text>
        <text x="367" y="114" font-family="Inter" font-weight="700" font-size="20" fill="#1B2A4A" text-anchor="middle">F P</text>
        <text x="367" y="136" font-family="Inter" font-weight="700" font-size="14" fill="#1B2A4A" text-anchor="middle">T O Z</text>
        <text x="367" y="154" font-family="Inter" font-weight="700" font-size="10" fill="#1B2A4A" text-anchor="middle">L P E D</text>
        <rect x="350" y="200" width="40" height="40" rx="6" fill="#2A9D8F"/><path d="M370 208 L370 232 M358 220 L382 220" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round"/>
        <path d="M26 330 Q22 286 44 262 Q48 300 40 330 Z" fill="#4E9F6A"/><path d="M40 330 Q46 280 78 266 Q66 304 54 330 Z" fill="#5FAF5A"/>
        <rect x="24" y="326" width="42" height="40" rx="6" fill="#F4F1DE"/>
        <rect x="380" y="296" width="30" height="62" rx="6" fill="#FFFFFF"/><rect x="386" y="282" width="18" height="16" rx="3" fill="#56CCF2"/><rect x="384" y="316" width="22" height="18" rx="2" fill="#56CCF2" opacity="0.6"/>'''
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
    if c["outfit_style"] == "field_jacket":
        a = c["accent"]
        return f"""
    <rect x="190" y="372" width="60" height="90" rx="22" fill="{c["skin_shade"]}"/>
    <path d="M36 640 C36 524 88 464 172 446 L220 470 L268 446 C352 464 404 524 404 640 Z" fill="{c["tee"]}"/>
    <path d="M180 446 Q220 492 260 446" stroke="{c["tee_shade"]}" stroke-width="7" fill="none"/>
    <rect x="212" y="468" width="16" height="48" rx="3" fill="{c["tee_shade"]}"/><circle cx="220" cy="482" r="3" fill="#FFFFFF"/><circle cx="220" cy="502" r="3" fill="#FFFFFF"/>
    <path d="M36 640 C36 524 88 464 172 446 L184 474 L194 640 Z" fill="{c["outfit"]}"/>
    <path d="M404 640 C404 524 352 464 268 446 L256 474 L246 640 Z" fill="{c["outfit"]}"/>
    <path d="M172 442 L146 446 L150 488 L188 480 Z" fill="{c["outfit_shade"]}"/><path d="M268 442 L294 446 L290 488 L252 480 Z" fill="{c["outfit_shade"]}"/>
    <rect x="98" y="528" width="60" height="58" rx="6" fill="{c["outfit_shade"]}" opacity="0.55"/><path d="M96 528 L160 528 L156 546 L100 546 Z" fill="{c["outfit_shade"]}"/><circle cx="128" cy="540" r="3.5" fill="#2B2F22"/>
    <rect x="282" y="528" width="60" height="58" rx="6" fill="{c["outfit_shade"]}" opacity="0.55"/><path d="M280 528 L344 528 L340 546 L284 546 Z" fill="{c["outfit_shade"]}"/><circle cx="312" cy="540" r="3.5" fill="#2B2F22"/>
    <rect x="114" y="512" width="5" height="22" rx="2" fill="#1B2A4A"/><rect x="113" y="510" width="7" height="6" rx="2" fill="{a}"/>
    <path d="M186 452 L206 560 M254 452 L234 560" stroke="{a}" stroke-width="6" stroke-linecap="round"/>
    <rect x="194" y="556" width="52" height="64" rx="5" fill="#FFFFFF" stroke="#C9CED6" stroke-width="2"/><rect x="194" y="556" width="52" height="16" rx="5" fill="{a}"/><rect x="194" y="566" width="52" height="6" fill="{a}"/>
    <text x="220" y="568" font-family="Inter" font-weight="800" font-size="10" fill="#FFFFFF" text-anchor="middle">PRESS</text>
    <rect x="202" y="580" width="16" height="20" rx="2" fill="#9AA6B2"/><rect x="222" y="582" width="18" height="4" rx="2" fill="#3D3552"/><rect x="222" y="592" width="14" height="4" rx="2" fill="#9AA6B2"/>
    <path d="M70 640 C74 590 86 560 104 540" stroke="{c["outfit_shade"]}" stroke-width="5" fill="none" stroke-linecap="round"/>
    <path d="M370 640 C366 590 354 560 336 540" stroke="{c["outfit_shade"]}" stroke-width="5" fill="none" stroke-linecap="round"/>"""
    if c["outfit_style"] == "polo":
        return f"""
    <rect x="190" y="372" width="60" height="90" rx="22" fill="{c["skin_shade"]}"/>
    <path d="M36 640 C36 524 88 464 172 446 L220 476 L268 446 C352 464 404 524 404 640 Z" fill="{c["outfit"]}"/>
    <path d="M206 470 L234 470 L234 548 L206 548 Z" fill="{c["outfit_shade"]}"/>
    <circle cx="220" cy="496" r="4" fill="#FFFFFF"/><circle cx="220" cy="524" r="4" fill="#FFFFFF"/>
    <path d="M172 440 L220 472 L196 500 L160 456 Z" fill="{c["outfit"]}" stroke="{c["outfit_shade"]}" stroke-width="3" stroke-linejoin="round"/>
    <path d="M268 440 L220 472 L244 500 L280 456 Z" fill="{c["outfit"]}" stroke="{c["outfit_shade"]}" stroke-width="3" stroke-linejoin="round"/>
    <path d="M276 536 L310 536 Q316 536 316 542 L316 560 Q316 566 310 566 L292 566 L284 574 L285 566 L276 566 Q270 566 270 560 L270 542 Q270 536 276 536 Z" fill="{c["accent"]}"/>
    <circle cx="283" cy="551" r="2.5" fill="{c["outfit_shade"]}"/><circle cx="293" cy="551" r="2.5" fill="{c["outfit_shade"]}"/><circle cx="303" cy="551" r="2.5" fill="{c["outfit_shade"]}"/>
    <path d="M70 640 C74 590 86 560 104 540" stroke="{c["outfit_shade"]}" stroke-width="5" fill="none" stroke-linecap="round"/>
    <path d="M370 640 C366 590 354 560 336 540" stroke="{c["outfit_shade"]}" stroke-width="5" fill="none" stroke-linecap="round"/>"""
    pony = ''
    if c["hair_style"] == "ponytail":
        pony = f'<path d="M300 226 C352 236 360 300 340 360 C330 392 338 420 350 440 C318 430 304 392 312 350 C320 300 312 262 290 240 Z" fill="{c["hair"]}"/><path d="M318 268 C332 300 330 340 322 372" stroke="#FFFFFF" stroke-width="3" fill="none" opacity="0.15" stroke-linecap="round"/>'
    if c["outfit_style"] == "open_blazer":
        g = c["gold"]
        return f"""
    <rect x="190" y="372" width="60" height="90" rx="22" fill="{c["skin_shade"]}"/>
    <path d="M36 640 C36 524 88 464 172 446 L220 470 L268 446 C352 464 404 524 404 640 Z" fill="{c["top"]}"/>
    <path d="M178 444 Q220 512 262 444 L250 440 L220 458 L190 440 Z" fill="{c["skin_shade"]}"/>
    <path d="M184 450 Q220 506 256 450" stroke="#E4D8C0" stroke-width="4" fill="none"/>
    <path d="M192 452 Q220 524 248 452" stroke="{g}" stroke-width="2.5" fill="none"/>
    <circle cx="220" cy="498" r="7.5" fill="none" stroke="{g}" stroke-width="4"/><path d="M220 506 L220 532 M220 520 L228 520 M220 529 L228 529" stroke="{g}" stroke-width="4" stroke-linecap="round"/>
    <path d="M36 640 C36 524 88 464 172 446 L190 520 L204 640 Z" fill="{c["outfit"]}"/>
    <path d="M404 640 C404 524 352 464 268 446 L250 520 L236 640 Z" fill="{c["outfit"]}"/>
    <path d="M172 446 L146 502 L174 512 L162 534 L204 640 L190 520 Z" fill="{c["outfit_shade"]}"/>
    <path d="M268 446 L294 502 L266 512 L278 534 L236 640 L250 520 Z" fill="{c["outfit_shade"]}"/>
    <g transform="translate(-12,22)"><rect x="296" y="548" width="58" height="26" rx="5" fill="#FFFFFF" stroke="#C9CED6" stroke-width="2"/>
    <path d="M304 566 L304 559 L311 553 L318 559 L318 566 Z" fill="{c["accent"]}"/><rect x="324" y="556" width="24" height="4" rx="2" fill="#3D3552"/><rect x="324" y="564" width="16" height="4" rx="2" fill="#9AA6B2"/></g>
    <path d="M70 640 C74 590 86 560 104 540" stroke="{c["outfit_shade"]}" stroke-width="5" fill="none" stroke-linecap="round"/>
    <path d="M370 640 C366 590 354 560 336 540" stroke="{c["outfit_shade"]}" stroke-width="5" fill="none" stroke-linecap="round"/>"""
    if c["outfit_style"] == "lab_coat":
        return f"""
    <rect x="190" y="372" width="60" height="90" rx="22" fill="{c["skin_shade"]}"/>
    <path d="M36 640 C36 524 88 464 172 446 L220 482 L268 446 C352 464 404 524 404 640 Z" fill="{c["outfit"]}"/>
    <path d="M176 444 L220 600 L264 444 Q220 474 176 444 Z" fill="{c["sweater"]}"/>
    <path d="M182 444 Q220 478 258 444" stroke="{c["sweater_shade"]}" stroke-width="7" fill="none"/>
    <path d="M190 446 Q220 470 250 446 L246 440 Q220 460 194 440 Z" fill="#FFFFFF"/>
    <path d="M172 446 L146 516 L188 550 L212 640 L172 640 L122 524 Z" fill="{c["outfit_shade"]}"/>
    <path d="M268 446 L294 516 L252 550 L228 640 L268 640 L318 524 Z" fill="{c["outfit_shade"]}"/>
    <path d="M172 446 L146 516 L188 550 L220 604 L178 448 Z" fill="{c["outfit"]}" stroke="{c["outfit_shade"]}" stroke-width="3"/>
    <path d="M268 446 L294 516 L252 550 L220 604 L262 448 Z" fill="{c["outfit"]}" stroke="{c["outfit_shade"]}" stroke-width="3"/>
    <rect x="276" y="566" width="50" height="44" rx="4" fill="none" stroke="{c["outfit_shade"]}" stroke-width="3"/>
    <rect x="286" y="544" width="7" height="32" rx="2" fill="{c["accent"]}"/><rect x="297" y="548" width="7" height="28" rx="2" fill="#E76F51"/><rect x="308" y="550" width="7" height="26" rx="2" fill="#2B3A42"/>
    <rect x="112" y="556" width="50" height="34" rx="4" fill="#FFFFFF" stroke="#9AA6B2" stroke-width="1.5"/>
    <rect x="112" y="556" width="50" height="9" rx="4" fill="{c["accent"]}"/><rect x="112" y="561" width="50" height="4" fill="{c["accent"]}"/>
    <circle cx="125" cy="577" r="6" fill="#DCE3E8"/><rect x="135" y="572" width="20" height="4" rx="2" fill="#2B3A42"/><rect x="135" y="580" width="14" height="4" rx="2" fill="#9AA6B2"/>
    <path d="M70 640 C74 590 86 560 104 540" stroke="{c["outfit_shade"]}" stroke-width="5" fill="none" stroke-linecap="round"/>
    <path d="M370 640 C366 590 354 560 336 540" stroke="{c["outfit_shade"]}" stroke-width="5" fill="none" stroke-linecap="round"/>"""
    if c["outfit_style"] == "blouse_scarf":
        dots = ''.join(f'<circle cx="{x}" cy="{y}" r="3" fill="{c["scarf_dot"]}"/>' for x, y in [(190, 452), (206, 462), (234, 462), (250, 452), (212, 488), (226, 500), (218, 520)])
        return f"""
    <rect x="190" y="372" width="60" height="90" rx="22" fill="{c["skin_shade"]}"/>
    <path d="M36 640 C36 524 88 464 172 446 L220 470 L268 446 C352 464 404 524 404 640 Z" fill="{c["outfit"]}"/>
    {''.join(f'<path d="M{x} 520 Q{x+6} 580 {x} 640" stroke="{c["outfit_shade"]}" stroke-width="2.5" fill="none" opacity="0.5"/>' for x in (110, 140, 300, 330))}
    <path d="M176 444 Q220 482 264 444 L258 470 Q220 498 182 470 Z" fill="{c["scarf"]}"/>
    <path d="M210 476 L196 540 L214 546 L222 488 Z" fill="{c["scarf"]}"/><path d="M226 480 L242 530 L226 538 L216 488 Z" fill="{c["scarf"]}" opacity="0.92"/>
    <ellipse cx="220" cy="482" rx="12" ry="9" fill="{c["scarf"]}" stroke="#1F5B59" stroke-width="2"/>{dots}
    <path d="M168 452 C164 520 186 566 248 586" stroke="#3D3552" stroke-width="5" fill="none" stroke-linecap="round"/>
    <path d="M272 452 C278 520 268 560 252 586" stroke="#3D3552" stroke-width="5" fill="none" stroke-linecap="round"/>
    <rect x="243" y="582" width="18" height="10" rx="3" fill="#9AA6B2"/>
    <rect x="226" y="590" width="52" height="40" rx="5" fill="#FFFFFF" stroke="#C9CED6" stroke-width="2"/>
    <rect x="226" y="590" width="52" height="10" rx="5" fill="{c["accent"]}"/><rect x="226" y="596" width="52" height="4" fill="{c["accent"]}"/>
    <circle cx="240" cy="614" r="7" fill="#DCD3E4"/><rect x="252" y="609" width="20" height="4" rx="2" fill="#3D3552"/><rect x="252" y="617" width="14" height="4" rx="2" fill="#9AA6B2"/>
    <path d="M70 640 C74 590 86 560 104 540" stroke="{c["outfit_shade"]}" stroke-width="5" fill="none" stroke-linecap="round"/>
    <path d="M370 640 C366 590 354 560 336 540" stroke="{c["outfit_shade"]}" stroke-width="5" fill="none" stroke-linecap="round"/>"""
    if c["outfit_style"] == "oxford_tie":
        return f"""
    <rect x="190" y="372" width="60" height="90" rx="22" fill="{c["skin_shade"]}"/>
    <path d="M36 640 C36 524 88 464 172 446 L220 482 L268 446 C352 464 404 524 404 640 Z" fill="{c["outfit"]}"/>
    {''.join(f'<path d="M{x} 500 L{x} 640" stroke="{c["outfit_shade"]}" stroke-width="2" opacity="0.6"/>' for x in range(96, 350, 18) if abs(x - 220) > 20)}
    <path d="M208 474 L232 474 L228 492 L212 492 Z" fill="{c["tie"]}"/>
    <path d="M212 490 L228 490 L238 600 L220 622 L202 600 Z" fill="{c["tie"]}"/>
    <path d="M206 528 L232 528" stroke="{c["accent"]}" stroke-width="4" stroke-linecap="round"/>
    <path d="M174 440 L220 478 L198 508 L166 452 Z" fill="{c["outfit"]}" stroke="{c["outfit_shade"]}" stroke-width="3" stroke-linejoin="round"/>
    <path d="M266 440 L220 478 L242 508 L274 452 Z" fill="{c["outfit"]}" stroke="{c["outfit_shade"]}" stroke-width="3" stroke-linejoin="round"/>
    <path d="M250 500 L250 640" stroke="{c["outfit_shade"]}" stroke-width="3"/><circle cx="256" cy="560" r="3.5" fill="#FFFFFF" stroke="{c["outfit_shade"]}"/><circle cx="256" cy="606" r="3.5" fill="#FFFFFF" stroke="{c["outfit_shade"]}"/>
    <rect x="270" y="536" width="52" height="46" rx="4" fill="none" stroke="{c["outfit_shade"]}" stroke-width="3"/>
    <rect x="280" y="512" width="22" height="38" rx="4" fill="#1E2838"/><rect x="283" y="516" width="16" height="22" rx="2" fill="#5D8FD9"/>
    <path d="M70 640 C74 590 86 560 104 540" stroke="{c["outfit_shade"]}" stroke-width="5" fill="none" stroke-linecap="round"/>
    <path d="M370 640 C366 590 354 560 336 540" stroke="{c["outfit_shade"]}" stroke-width="5" fill="none" stroke-linecap="round"/>"""
    if c["outfit_style"] == "turtleneck":
        return f"""
    <rect x="190" y="372" width="60" height="90" rx="22" fill="{c["skin_shade"]}"/>
    <path d="M36 640 C36 524 88 464 172 446 L268 446 C352 464 404 524 404 640 Z" fill="{c["outfit"]}"/>
    {''.join(f'<path d="M{x} 470 L{x} 640" stroke="{c["outfit_shade"]}" stroke-width="2.5" opacity="0.55"/>' for x in range(110, 340, 16))}
    <rect x="178" y="420" width="84" height="46" rx="18" fill="{c["outfit_shade"]}"/>
    <path d="M186 436 L254 436 M186 448 L254 448" stroke="{c["outfit"]}" stroke-width="3" opacity="0.6"/>
    <path d="M70 640 C74 590 86 560 104 540" stroke="{c["outfit_shade"]}" stroke-width="5" fill="none" stroke-linecap="round"/>
    <path d="M370 640 C366 590 354 560 336 540" stroke="{c["outfit_shade"]}" stroke-width="5" fill="none" stroke-linecap="round"/>
    <circle cx="160" cy="530" r="13" fill="#FFFFFF"/><path d="M160 520 L166 532 L160 542 L154 532 Z" fill="{c["accent"]}"/><circle cx="160" cy="532" r="2" fill="#FFFFFF"/>"""
    if c["outfit_style"] == "sweater_vest":
        return pony + f"""
    <rect x="190" y="372" width="60" height="90" rx="22" fill="{c["skin_shade"]}"/>
    <path d="M36 640 C36 524 88 464 172 446 L220 482 L268 446 C352 464 404 524 404 640 Z" fill="{c["shirt"]}"/>
    <path d="M176 440 L220 480 L200 506 L168 452 Z" fill="#FFFFFF" stroke="#D8D0C0" stroke-width="2"/><path d="M264 440 L220 480 L240 506 L272 452 Z" fill="#FFFFFF" stroke="#D8D0C0" stroke-width="2"/>
    <path d="M96 640 C100 560 118 500 156 470 L220 560 L284 470 C322 500 340 560 344 640 Z" fill="{c["outfit"]}"/>
    <path d="M156 470 L220 560 L284 470" stroke="{c["outfit_shade"]}" stroke-width="9" fill="none" stroke-linejoin="round"/>
    {''.join(f'<path d="M{x} 580 L{x} 636" stroke="{c["outfit_shade"]}" stroke-width="3" opacity="0.7"/>' for x in range(124, 330, 14) if abs(x - 220) > 10)}
    <path d="M100 630 L340 630" stroke="{c["outfit_shade"]}" stroke-width="8"/>
    <path d="M220 560 L220 640" stroke="{c["outfit_shade"]}" stroke-width="3" opacity="0.6"/>
    <path d="M58 640 C62 590 74 560 92 540" stroke="#D8D0C0" stroke-width="4" fill="none" stroke-linecap="round"/>
    <path d="M382 640 C378 590 366 560 348 540" stroke="#D8D0C0" stroke-width="4" fill="none" stroke-linecap="round"/>
    <rect x="262" y="540" width="44" height="40" rx="4" fill="{c["outfit_shade"]}"/>
    <rect x="270" y="512" width="7" height="36" rx="2" fill="{c["accent"]}"/><path d="M270 512 L273.5 503 L277 512 Z" fill="#3B3F4C"/>
    <rect x="282" y="518" width="6" height="30" rx="2" fill="#3B3F4C"/>"""
    if c["outfit_style"] == "denim_shirt":
        return f"""
    <rect x="190" y="372" width="60" height="90" rx="22" fill="{c["skin_shade"]}"/>
    <path d="M36 640 C36 524 88 464 172 446 L220 482 L268 446 C352 464 404 524 404 640 Z" fill="{c["outfit"]}"/>
    <path d="M182 446 Q220 490 258 446 L250 640 L190 640 Z" fill="{c["tee"]}"/>
    <path d="M190 448 Q220 480 250 448" stroke="#D9D3BC" stroke-width="5" fill="none"/>
    <circle cx="220" cy="560" r="22" fill="{c["accent"]}"/><path d="M213 549 L231 560 L213 571 Z" fill="#F4F1DE" stroke="#F4F1DE" stroke-width="2" stroke-linejoin="round"/>
    <path d="M172 446 L150 500 L188 520 L190 640" stroke="{c["outfit_shade"]}" stroke-width="7" fill="none" stroke-linejoin="round"/>
    <path d="M268 446 L290 500 L252 520 L250 640" stroke="{c["outfit_shade"]}" stroke-width="7" fill="none" stroke-linejoin="round"/>
    <path d="M172 446 L150 500 L188 520 L182 448 Z" fill="{c["outfit"]}"/><path d="M268 446 L290 500 L252 520 L258 448 Z" fill="{c["outfit"]}"/>
    <path d="M176 452 L156 498 L186 514" stroke="#E8C66A" stroke-width="2" stroke-dasharray="4 3" fill="none"/><path d="M264 452 L284 498 L254 514" stroke="#E8C66A" stroke-width="2" stroke-dasharray="4 3" fill="none"/>
    <circle cx="186" cy="560" r="4" fill="#E8C66A"/><circle cx="188" cy="604" r="4" fill="#E8C66A"/>
    <rect x="112" y="540" width="56" height="44" rx="4" fill="{c["outfit_shade"]}"/><path d="M112 540 L168 540 L168 556 L140 560 L112 556 Z" fill="{c["outfit"]}" stroke="#E8C66A" stroke-width="1.5" stroke-dasharray="4 3"/>
    <rect x="124" y="522" width="7" height="26" rx="2" fill="#1B1B2F"/><rect x="134" y="526" width="18" height="18" rx="2" fill="#FFE066" transform="rotate(8 143 535)"/>
    <rect x="272" y="540" width="56" height="44" rx="4" fill="{c["outfit_shade"]}"/><path d="M272 540 L328 540 L328 556 L300 560 L272 556 Z" fill="{c["outfit"]}" stroke="#E8C66A" stroke-width="1.5" stroke-dasharray="4 3"/>
    <path d="M70 640 C74 590 86 560 104 540" stroke="{c["outfit_shade"]}" stroke-width="5" fill="none" stroke-linecap="round"/>
    <path d="M370 640 C366 590 354 560 336 540" stroke="{c["outfit_shade"]}" stroke-width="5" fill="none" stroke-linecap="round"/>"""
    if c["outfit_style"] == "nurse_scrubs":
        return f"""
    <rect x="190" y="372" width="60" height="90" rx="22" fill="{c["skin_shade"]}"/>
    <path d="M182 446 Q220 474 258 446 L254 440 Q220 462 186 440 Z" fill="{c["undershirt"]}"/>
    <path d="M36 640 C36 524 88 464 172 446 L220 482 L268 446 C352 464 404 524 404 640 Z" fill="{c["outfit"]}"/>
    <path d="M36 640 C36 560 52 512 82 488 L96 640 Z" fill="{c["undershirt"]}"/><path d="M404 640 C404 560 388 512 358 488 L344 640 Z" fill="{c["undershirt"]}"/>
    <path d="M82 488 L96 640" stroke="{c["outfit_shade"]}" stroke-width="5"/><path d="M358 488 L344 640" stroke="{c["outfit_shade"]}" stroke-width="5"/>
    <path d="M180 446 L220 520 L260 446 Z" fill="{c["undershirt"]}"/>
    <path d="M180 446 L220 520 L260 446" stroke="{c["outfit_shade"]}" stroke-width="8" fill="none" stroke-linejoin="round"/>
    <path d="M168 452 C150 510 162 556 190 566" stroke="#1B2A4A" stroke-width="6" fill="none" stroke-linecap="round"/>
    <path d="M272 452 C290 500 284 536 272 552" stroke="#1B2A4A" stroke-width="6" fill="none" stroke-linecap="round"/>
    <path d="M190 566 C200 576 214 574 222 564" stroke="#1B2A4A" stroke-width="5" fill="none" stroke-linecap="round"/>
    <circle cx="272" cy="560" r="11" fill="#C9CED6" stroke="#1B2A4A" stroke-width="4"/><circle cx="272" cy="560" r="4.5" fill="#EEF2F5"/>
    <path d="M150 540 L150 586" stroke="{c["accent"]}" stroke-width="3"/><circle cx="150" cy="590" r="6" fill="#1B2A4A"/>
    <rect x="132" y="596" width="36" height="40" rx="4" fill="#FFFFFF" stroke="#9AA6B2" stroke-width="1.5"/><rect x="138" y="602" width="24" height="12" rx="2" fill="#56CCF2"/><rect x="138" y="618" width="20" height="3" rx="1.5" fill="#1B2A4A"/><rect x="138" y="625" width="14" height="3" rx="1.5" fill="#9AA6B2"/>
    <rect x="292" y="560" width="52" height="46" rx="5" fill="{c["outfit_shade"]}"/>
    <rect x="300" y="538" width="7" height="32" rx="2" fill="#1B2A4A"/><rect x="311" y="544" width="9" height="26" rx="2" fill="#C9CED6"/><rect x="311" y="544" width="9" height="5" rx="1" fill="#F4F1DE"/><rect x="324" y="540" width="7" height="30" rx="2" fill="#E76F51"/>"""
    if c["outfit_style"] == "suit":
        return f'''
    <path d="M112 300 C100 360 104 420 120 470 L320 470 C336 420 340 360 328 300 Z" fill="{c["hair"]}"/>
    <rect x="190" y="372" width="60" height="90" rx="22" fill="{c["skin_shade"]}"/>
    <path d="M36 640 C36 524 88 464 172 446 L220 482 L268 446 C352 464 404 524 404 640 Z" fill="{c["outfit"]}"/>
    <path d="M178 446 L220 610 L262 446 L220 476 Z" fill="{c["blouse"]}"/>
    <path d="M190 446 L220 482 L250 446 L220 466 Z" fill="{c["skin_shade"]}"/>
    <path d="M196 470 Q220 494 244 470" stroke="#F3EBDD" stroke-width="3" fill="none"/>
    <circle cx="202" cy="484" r="3.5" fill="#FFFFFF"/><circle cx="212" cy="492" r="3.5" fill="#FFFFFF"/><circle cx="220" cy="494" r="3.5" fill="#FFFFFF"/><circle cx="228" cy="492" r="3.5" fill="#FFFFFF"/><circle cx="238" cy="484" r="3.5" fill="#FFFFFF"/>
    <path d="M172 446 L144 516 L186 550 L212 640 L172 640 L122 524 Z" fill="{c["outfit_shade"]}"/>
    <path d="M268 446 L296 516 L254 550 L228 640 L268 640 L318 524 Z" fill="{c["outfit_shade"]}"/>
    <path d="M172 446 L144 516 L186 550 L220 610 L178 448 Z" fill="{c["outfit"]}" stroke="{c["outfit_shade"]}" stroke-width="3"/>
    <path d="M268 446 L296 516 L254 550 L220 610 L262 448 Z" fill="{c["outfit"]}" stroke="{c["outfit_shade"]}" stroke-width="3"/>
    <circle cx="160" cy="512" r="6" fill="{c["accent"]}"/><path d="M156 512 L164 512 M160 508 L160 516" stroke="#7A5E10" stroke-width="1.5"/>
    <circle cx="214" cy="600" r="4" fill="{c["outfit_shade"]}"/>
    <path d="M70 640 C74 590 86 560 104 540" stroke="{c["outfit_shade"]}" stroke-width="5" fill="none" stroke-linecap="round"/>
    <path d="M370 640 C366 590 354 560 336 540" stroke="{c["outfit_shade"]}" stroke-width="5" fill="none" stroke-linecap="round"/>
    <rect x="288" y="566" width="44" height="6" rx="3" fill="{c["blouse"]}" opacity="0.8"/>'''
    if c["outfit_style"] == "scrubs":
        return f'''
    <rect x="190" y="372" width="60" height="90" rx="22" fill="{c["skin_shade"]}"/>
    <path d="M36 640 C36 524 88 464 172 446 L220 482 L268 446 C352 464 404 524 404 640 Z" fill="{c["outfit"]}"/>
    <path d="M176 446 L220 528 L264 446 Z" fill="{c["skin_shade"]}"/>
    <path d="M176 446 L220 528 L264 446" stroke="{c["outfit_shade"]}" stroke-width="9" fill="none" stroke-linejoin="round"/>
    <path d="M186 430 Q220 462 254 430 L250 448 Q220 474 190 448 Z" fill="{c["mask"]}"/>
    <path d="M192 440 Q220 462 248 440" stroke="#93C4D8" stroke-width="2" fill="none"/>
    <rect x="268" y="530" width="54" height="48" rx="5" fill="{c["outfit_shade"]}"/>
    <rect x="280" y="510" width="7" height="30" rx="2" fill="#1B2A4A"/><rect x="292" y="514" width="7" height="26" rx="2" fill="{c["accent"]}"/>
    <rect x="124" y="532" width="48" height="30" rx="5" fill="#FFFFFF" stroke="{c["outfit_shade"]}" stroke-width="2"/>
    {_tooth(138, 547, 0.32, c["accent"])}<rect x="148" y="540" width="18" height="4" rx="2" fill="#1B2A4A"/><rect x="148" y="549" width="12" height="4" rx="2" fill="#9AA6B2"/>
    <path d="M70 640 C74 590 86 560 104 540" stroke="{c["outfit_shade"]}" stroke-width="5" fill="none" stroke-linecap="round"/>
    <path d="M370 640 C366 590 354 560 336 540" stroke="{c["outfit_shade"]}" stroke-width="5" fill="none" stroke-linecap="round"/>'''
    if c["outfit_style"] == "apron":
        stripes = ''.join(f'<path d="M{x} 470 L{x-10} 640" stroke="{c["outfit_shade"]}" stroke-width="5"/>' for x in range(70, 400, 22))
        return f'''
    <rect x="190" y="372" width="60" height="90" rx="22" fill="{c["skin_shade"]}"/>
    <path d="M36 640 C36 524 88 464 172 446 L220 482 L268 446 C352 464 404 524 404 640 Z" fill="{c["outfit"]}"/>
    <clipPath id="tor"><path d="M36 640 C36 524 88 464 172 446 L220 482 L268 446 C352 464 404 524 404 640 Z"/></clipPath>
    <g clip-path="url(#tor)" opacity="0.55">{stripes}</g>
    <path d="M172 446 L220 482 L268 446 L258 440 L220 470 L182 440 Z" fill="{c["outfit_shade"]}"/>
    <path d="M168 452 L184 520" stroke="{c["apron_shade"]}" stroke-width="9" stroke-linecap="round"/><path d="M272 452 L256 520" stroke="{c["apron_shade"]}" stroke-width="9" stroke-linecap="round"/>
    <path d="M160 520 L280 520 L300 640 L140 640 Z" fill="{c["apron"]}"/>
    <path d="M160 520 L280 520" stroke="{c["apron_shade"]}" stroke-width="5"/>
    <rect x="182" y="566" width="76" height="46" rx="6" fill="{c["apron_shade"]}"/>
    <rect x="196" y="548" width="7" height="32" rx="2" fill="{c["accent"]}"/><path d="M196 548 L199.5 540 L203 548 Z" fill="#F3E3C8"/>
    <rect x="210" y="552" width="30" height="26" rx="2" fill="#FFF6E8"/><rect x="214" y="558" width="20" height="3" rx="1.5" fill="#9AA6B2"/><rect x="214" y="565" width="14" height="3" rx="1.5" fill="#9AA6B2"/>
    <text x="220" y="598" font-family="Inter" font-weight="800" font-size="12" fill="#F3E3C8" text-anchor="middle" opacity="0.9">EST. 2019</text>
    <path d="M70 640 C74 590 86 560 104 540" stroke="{c["outfit_shade"]}" stroke-width="5" fill="none" stroke-linecap="round"/>
    <path d="M370 640 C366 590 354 560 336 540" stroke="{c["outfit_shade"]}" stroke-width="5" fill="none" stroke-linecap="round"/>'''
    if c["outfit_style"] == "zip_hoodie":
        return f'''
    <ellipse cx="220" cy="452" rx="122" ry="50" fill="{c["outfit"]}"/><ellipse cx="220" cy="448" rx="94" ry="36" fill="{c["outfit_shade"]}"/>
    <rect x="190" y="372" width="60" height="90" rx="22" fill="{c["skin_shade"]}"/>
    <path d="M36 640 C36 524 88 464 172 446 L220 482 L268 446 C352 464 404 524 404 640 Z" fill="{c["outfit"]}"/>
    <path d="M184 446 Q220 486 256 446 L248 640 L192 640 Z" fill="{c["tee"]}"/>
    <path d="M192 448 Q220 478 248 448" stroke="#C9D2DB" stroke-width="5" fill="none"/>
    <text x="220" y="566" font-family="Inter" font-weight="800" font-size="20" fill="#2A2F3B" text-anchor="middle">&lt;/&gt;</text>
    <path d="M182 446 L194 640" stroke="{c["outfit_shade"]}" stroke-width="7"/><path d="M258 446 L246 640" stroke="{c["outfit_shade"]}" stroke-width="7"/>
    <path d="M185 452 L196 640" stroke="#AEB8C2" stroke-width="2.5" stroke-dasharray="3 3"/><path d="M255 452 L244 640" stroke="#AEB8C2" stroke-width="2.5" stroke-dasharray="3 3"/>
    <path d="M176 456 L168 534" stroke="{c["accent"]}" stroke-width="4.5" stroke-linecap="round"/><path d="M262 456 L270 534" stroke="{c["accent"]}" stroke-width="4.5" stroke-linecap="round"/>
    <rect x="164" y="532" width="8" height="12" rx="2" fill="#AEB8C2"/><rect x="266" y="532" width="8" height="12" rx="2" fill="#AEB8C2"/>
    <path d="M70 640 C74 590 86 560 104 540" stroke="{c["outfit_shade"]}" stroke-width="5" fill="none" stroke-linecap="round"/>
    <path d="M370 640 C366 590 354 560 336 540" stroke="{c["outfit_shade"]}" stroke-width="5" fill="none" stroke-linecap="round"/>
    <path d="M128 640 L142 602 L188 602" stroke="{c["outfit_shade"]}" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M312 640 L298 602 L252 602" stroke="{c["outfit_shade"]}" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
    <rect x="290" y="500" width="36" height="36" rx="18" fill="#FFFFFF" opacity="0.92"/><text x="308" y="524" font-family="Inter" font-weight="800" font-size="14" fill="#2A2F3B" text-anchor="middle">{{ }}</text>'''
    if c["outfit_style"] == "coat":
        return f'''
    <rect x="190" y="372" width="60" height="90" rx="22" fill="{c["skin_shade"]}"/>
    <path d="M36 640 C36 524 88 464 172 446 L220 482 L268 446 C352 464 404 524 404 640 Z" fill="{c["outfit"]}"/>
    <path d="M178 446 L220 600 L262 446 L220 478 Z" fill="{c["accent"]}"/>
    <path d="M190 446 L220 486 L250 446 L220 470 Z" fill="{c["skin_shade"]}"/>
    <path d="M172 446 L144 520 L184 552 L208 640 L172 640 L122 524 Z" fill="{c["outfit_shade"]}"/>
    <path d="M268 446 L296 520 L256 552 L232 640 L268 640 L318 524 Z" fill="{c["outfit_shade"]}"/>
    <path d="M172 446 L144 520 L184 552 L220 604 L178 448 Z" fill="{c["outfit"]}" stroke="{c["outfit_shade"]}" stroke-width="3"/>
    <path d="M268 446 L296 520 L256 552 L220 604 L262 448 Z" fill="{c["outfit"]}" stroke="{c["outfit_shade"]}" stroke-width="3"/>
    <path d="M186 452 C170 500 172 540 196 560" stroke="#1B2A4A" stroke-width="6" fill="none" stroke-linecap="round"/>
    <path d="M254 452 C270 500 268 528 254 546" stroke="#1B2A4A" stroke-width="6" fill="none" stroke-linecap="round"/>
    <path d="M196 560 C206 572 222 572 232 562" stroke="#1B2A4A" stroke-width="5" fill="none" stroke-linecap="round"/>
    <circle cx="254" cy="552" r="12" fill="#AEB8C2" stroke="#1B2A4A" stroke-width="4"/><circle cx="254" cy="552" r="5" fill="#E6ECF1"/>
    <rect x="286" y="560" width="50" height="40" rx="5" fill="{c["outfit_shade"]}"/>
    <rect x="296" y="540" width="7" height="30" rx="2" fill="#1B2A4A"/><rect x="308" y="544" width="7" height="26" rx="2" fill="{c["accent"]}"/>
    <rect x="104" y="548" width="56" height="30" rx="4" fill="#FFFFFF" stroke="{c["outfit_shade"]}" stroke-width="2"/>
    <rect x="110" y="556" width="18" height="14" rx="2" fill="{c["accent"]}"/><rect x="132" y="557" width="22" height="4" rx="2" fill="#1B2A4A"/><rect x="132" y="565" width="16" height="4" rx="2" fill="#9AA6B2"/>'''
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
    if c["hair_style"] == "tousled":
        hair = (f'<path d="M122 282 C106 172 182 146 222 150 C298 144 338 204 318 284 C312 244 300 216 272 204 C232 216 180 216 150 208 C134 228 126 254 122 282 Z" fill="{c["hair"]}"/>'
                f'<path d="M136 216 C120 166 160 128 206 126 L196 112 L226 124 C240 112 262 110 280 118 L272 128 C306 138 324 170 312 214 C300 202 290 198 280 206 C274 190 260 184 248 198 C240 182 224 180 214 196 C204 182 188 184 180 200 C170 188 152 192 136 216 Z" fill="{c["hair"]}"/>'
                f'<path d="M208 194 C200 212 204 228 216 236 C212 222 214 208 222 198 Z" fill="{c["hair"]}"/>'
                f'<path d="M172 158 C196 140 240 134 280 150 M190 178 C214 160 252 158 290 172" stroke="#FFFFFF" stroke-width="3.5" fill="none" opacity="0.14" stroke-linecap="round"/>')
    elif c["hair_style"] == "space_buns":
        hair = (f'<path d="M122 286 C104 178 172 142 222 142 C290 140 342 190 318 288 C314 248 302 222 284 208 C250 198 198 198 160 206 C140 224 126 254 122 286 Z" fill="{c["hair"]}"/>'
                f'<path d="M222 146 L222 196" stroke="#000000" stroke-width="2" opacity="0.35"/>'
                f'<path d="M168 166 C186 154 208 150 216 154 M230 154 C254 150 280 160 296 178" stroke="#FFFFFF" stroke-width="4" fill="none" opacity="0.15" stroke-linecap="round"/>')
    elif c["hair_style"] == "long_curly":
        hair = (f'<path d="M122 292 C102 176 176 138 224 140 C294 138 346 190 318 292 C316 250 306 224 288 208 C258 212 216 206 192 190 C176 214 150 232 136 246 C128 260 124 276 122 292 Z" fill="{c["hair"]}"/>'
                f'<path d="M190 150 C196 170 196 182 192 192" stroke="#000000" stroke-width="2" opacity="0.25" fill="none"/>'
                f'<path d="M214 152 C250 146 288 162 302 190 M150 196 C158 180 170 166 184 158" stroke="#FFFFFF" stroke-width="4" fill="none" opacity="0.2" stroke-linecap="round"/>')
    elif c["hair_style"] == "receding":
        hair = (f'<path d="M124 282 C112 226 126 196 150 182 C152 210 150 236 144 262 C136 268 128 274 124 282 Z" fill="{c["hair"]}"/>'
                f'<path d="M316 282 C328 226 314 196 290 182 C288 210 290 236 296 262 C304 268 312 274 316 282 Z" fill="{c["hair"]}"/>'
                f'<path d="M150 182 C176 164 200 170 206 176 C190 176 168 182 152 196 Z" fill="{c["hair"]}"/><path d="M290 182 C264 164 240 170 234 176 C250 176 272 182 288 196 Z" fill="{c["hair"]}"/>'
                f'<path d="M136 230 C134 250 134 266 138 280 M304 230 C306 250 306 266 302 280" stroke="#8E8A86" stroke-width="2" fill="none" opacity="0.6" stroke-linecap="round"/>')
    elif c["hair_style"] == "pixie":
        hair = (f'<path d="M124 278 C110 184 170 146 222 146 C284 144 334 190 318 278 C314 244 304 222 290 210 C262 214 236 206 220 196 C196 214 166 222 148 216 C136 232 128 254 124 278 Z" fill="{c["hair"]}"/>'
                f'<path d="M150 218 C140 170 178 138 228 138 C280 138 312 170 306 214 C290 196 266 190 244 194 C226 206 188 222 150 218 Z" fill="{c["hair"]}"/>'
                f'<path d="M168 196 C190 168 236 156 276 166 M196 208 C220 186 252 180 288 188" stroke="#8E8A86" stroke-width="3" fill="none" opacity="0.55" stroke-linecap="round"/>'
                f'<path d="M180 158 C206 146 244 146 270 156" stroke="#FFFFFF" stroke-width="4" fill="none" opacity="0.35" stroke-linecap="round"/>')
    elif c["hair_style"] == "afro":
        hair = (f'<path d="M128 262 C124 200 168 168 222 168 C276 168 318 200 314 262 C304 226 286 206 262 200 C236 210 204 210 178 200 C154 208 136 230 128 262 Z" fill="{c["hair"]}"/>'
                f'<path d="M150 188 C180 166 260 164 292 188" stroke="{c["accent"]}" stroke-width="10" fill="none" stroke-linecap="round"/>')
    elif c["hair_style"] == "ponytail":
        hair = (f'<path d="M122 286 C104 178 174 142 222 142 C290 140 342 190 318 288 C314 246 300 218 280 204 C252 190 196 190 164 204 C140 222 126 252 122 286 Z" fill="{c["hair"]}"/>'
                f'<path d="M170 196 C196 182 250 180 278 194" stroke="#FFFFFF" stroke-width="3" fill="none" opacity="0.15" stroke-linecap="round"/>'
                f'<path d="M180 160 C204 148 244 148 268 158" stroke="#FFFFFF" stroke-width="4" fill="none" opacity="0.15" stroke-linecap="round"/>'
                f'<rect x="296" y="214" width="20" height="14" rx="6" fill="{c["accent"]}" transform="rotate(30 306 221)"/>')
    elif c["hair_style"] == "fringe":
        hair = (f'<path d="M122 284 C104 180 168 142 222 144 C290 140 340 196 318 286 C314 250 304 228 290 214 L130 214 C126 236 122 260 122 284 Z" fill="{c["hair"]}"/>'
                f'<path d="M132 222 C128 170 172 136 226 136 C286 134 320 172 312 222 C300 212 290 214 280 222 C272 210 258 210 248 224 C238 210 222 212 212 226 C202 212 186 212 176 226 C166 212 150 212 132 222 Z" fill="{c["hair"]}"/>'
                f'<path d="M170 160 C200 146 250 144 282 158" stroke="#FFFFFF" stroke-width="4" fill="none" opacity="0.14" stroke-linecap="round"/>')
    elif c["hair_style"] == "curly":
        import math
        hair = f'<path d="M122 286 C104 176 184 140 222 144 C300 140 340 204 318 288 C312 246 298 222 272 210 C232 222 180 222 150 214 C134 234 126 260 122 286 Z" fill="{c["hair"]}"/>'
        for i in range(13):
            a = math.pi * (1.05 - 1.1 * i / 12)
            x, y = 220 + 104 * math.cos(a), 250 - 100 * math.sin(a)
            hair += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{27 if 2 < i < 10 else 22}" fill="{c["hair"]}"/>'
    elif c["hair_style"] == "waves":
        hair = (f'<path d="M108 420 C80 360 96 300 104 250 C112 176 170 140 222 142 C286 140 344 186 338 260 C346 310 362 360 330 420 C316 380 318 340 316 300 C314 250 300 224 282 212 C250 232 194 230 160 206 C138 236 126 270 126 310 C124 350 126 386 108 420 Z" fill="{c["hair"]}"/>'
                f'<path d="M130 196 C170 160 270 156 312 196" stroke="{c["accent"]}" stroke-width="12" fill="none" stroke-linecap="round"/>'
                f'<path d="M114 330 Q104 360 116 392 M326 330 Q338 360 326 392" stroke="#FFFFFF" stroke-width="3" fill="none" opacity="0.15" stroke-linecap="round"/>')
    elif c["hair_style"] == "long_straight":
        hair = (f'<path d="M124 290 C104 176 176 140 222 142 C292 140 344 190 318 290 C314 248 300 222 276 206 C262 220 236 226 222 214 C206 228 176 226 158 212 C138 232 128 260 124 290 Z" fill="{c["hair"]}"/>'
                f'<path d="M222 150 L222 212" stroke="#000000" stroke-width="2" opacity="0.35"/>'
                f'<path d="M170 168 C190 154 214 152 218 160" stroke="#FFFFFF" stroke-width="4" fill="none" opacity="0.18" stroke-linecap="round"/>'
                f'<path d="M262 160 C286 164 304 182 310 204" stroke="#FFFFFF" stroke-width="4" fill="none" opacity="0.14" stroke-linecap="round"/>')
    elif c["hair_style"] == "side_part":
        hair = (f'<path d="M122 284 C104 172 178 140 226 144 C300 140 342 206 318 286 C314 246 302 220 282 206 C252 210 214 208 190 200 C170 214 150 224 140 238 C130 252 124 268 122 284 Z" fill="{c["hair"]}"/>'
                f'<path d="M176 150 C222 128 296 146 312 204 C282 186 236 186 196 208 C184 190 178 172 176 150 Z" fill="{c["hair"]}"/>'
                f'<path d="M178 154 C182 176 188 192 196 206" stroke="#FFFFFF" stroke-width="3" fill="none" opacity="0.25" stroke-linecap="round"/>'
                f'<path d="M214 150 C250 144 286 160 300 186" stroke="#FFFFFF" stroke-width="4" fill="none" opacity="0.15" stroke-linecap="round"/>')
    elif c["hair_style"] == "bob":
        hair = f'<path d="M112 330 C92 190 168 140 222 144 C290 140 352 190 330 330 L304 336 C314 280 304 236 286 216 C252 236 196 234 160 210 C140 240 130 280 138 336 Z" fill="{c["hair"]}"/>'
    elif c["hair_style"] == "quiff":
        hair = (f'<path d="M124 280 C110 196 150 160 196 152 L250 154 C300 156 336 206 316 282 C312 246 302 222 282 210 C240 214 186 216 150 210 C136 230 128 254 124 280 Z" fill="{c["hair"]}"/>'
                f'<path d="M146 212 C130 158 170 112 232 108 C284 104 318 128 314 168 C302 152 282 146 262 150 C288 162 304 184 302 204 C272 192 238 198 210 210 C188 218 164 220 146 212 Z" fill="{c["hair"]}"/>'
                f'<path d="M178 150 C204 128 246 120 290 130" stroke="#FFFFFF" stroke-width="4" fill="none" stroke-linecap="round" opacity="0.18"/>')
    elif c["hair_style"] == "buzz":
        hair = (f'<path d="M126 268 C114 186 176 150 222 150 C276 148 330 188 316 268 C310 236 300 214 284 202 C250 212 192 212 158 202 C140 216 130 240 126 268 Z" fill="{c["hair"]}"/>'
                f'<path d="M126 268 C114 186 176 150 222 150 C276 148 330 188 316 268" stroke="{c["hair"]}" stroke-width="3" fill="none" opacity="0.6"/>'
                f'<path d="M134 244 C130 270 128 290 132 304 M308 244 C312 270 312 290 308 304" stroke="{c["hair"]}" stroke-width="8" fill="none" stroke-linecap="round" opacity="0.85"/>'
                f'<path d="M176 168 C204 156 246 156 272 166" stroke="#FFFFFF" stroke-width="4" fill="none" opacity="0.12" stroke-linecap="round"/>')
    elif c["hair_style"] == "slick_back":
        hair = (f'<path d="M122 280 C108 184 168 140 222 140 C286 138 336 186 318 282 C314 246 304 222 288 208 C252 196 192 196 156 208 C140 224 128 250 122 280 Z" fill="{c["hair"]}"/>'
                f'<path d="M156 208 C150 172 182 138 226 136 C276 134 304 160 300 200 C270 186 214 186 156 208 Z" fill="{c["hair"]}"/>'
                f'<path d="M172 190 C196 160 248 152 286 166 M180 204 C206 178 250 172 292 184" stroke="#FFFFFF" stroke-width="3" fill="none" opacity="0.16" stroke-linecap="round"/>')
    elif c["hair_style"] == "short":
        hair = f'<path d="M122 282 C106 172 182 146 222 150 C298 144 338 204 318 284 C312 244 300 216 272 204 C232 216 180 216 150 208 C134 228 126 254 122 282 Z" fill="{c["hair"]}"/>'
    else:
        hair = f'<circle cx="220" cy="146" r="38" fill="{c["hair"]}"/><path d="M119 286 C104 176 188 150 228 160 C300 148 344 210 321 292 C312 250 292 226 262 216 C230 242 172 246 140 236 C128 250 122 268 119 286 Z" fill="{c["hair"]}"/>'
    glasses = '<rect x="149" y="272" width="58" height="42" rx="10" fill="none" stroke="#1B2A4A" stroke-width="5"/><rect x="233" y="272" width="58" height="42" rx="10" fill="none" stroke="#1B2A4A" stroke-width="5"/><path d="M207 289 Q220 282 233 289" stroke="#1B2A4A" stroke-width="4.5" fill="none"/><path d="M149 284 L128 280 M291 284 L312 280" stroke="#1B2A4A" stroke-width="4.5" stroke-linecap="round"/>' if c["glasses"] == "square" else '<rect x="152" y="278" width="52" height="34" rx="12" fill="none" stroke="#7A5E10" stroke-width="3"/><rect x="236" y="278" width="52" height="34" rx="12" fill="none" stroke="#7A5E10" stroke-width="3"/><path d="M204 292 Q220 286 236 292" stroke="#7A5E10" stroke-width="3" fill="none"/><path d="M152 290 L128 284 M288 290 L312 284" stroke="#7A5E10" stroke-width="3" stroke-linecap="round"/>' if c["glasses"] == "thin" else '<circle cx="178" cy="293" r="27" fill="none" stroke="#1B2A4A" stroke-width="4.5"/><circle cx="262" cy="293" r="27" fill="none" stroke="#1B2A4A" stroke-width="4.5"/><path d="M205 290 Q220 283 235 290" stroke="#1B2A4A" stroke-width="4.5" fill="none"/>' if c["glasses"] else ''
    if c["glasses"] == "cat_eye":
        glasses = '<path d="M148 284 Q150 274 166 274 L196 276 Q206 278 204 292 Q200 312 178 312 Q154 312 150 296 Z" fill="none" stroke="#5A2E4A" stroke-width="4.5" stroke-linejoin="round"/><path d="M292 284 Q290 274 274 274 L244 276 Q234 278 236 292 Q240 312 262 312 Q286 312 290 296 Z" fill="none" stroke="#5A2E4A" stroke-width="4.5" stroke-linejoin="round"/><path d="M204 288 Q220 281 236 288" stroke="#5A2E4A" stroke-width="4" fill="none"/><path d="M148 282 L130 276 M292 282 L310 276" stroke="#5A2E4A" stroke-width="4" stroke-linecap="round"/><path d="M146 282 L140 272 M294 282 L300 272" stroke="#5A2E4A" stroke-width="5" stroke-linecap="round"/>'
    if c.get("headset"):
        hc = c["headset"]
        glasses += (f'<path d="M112 300 C104 196 160 128 220 126 C280 128 336 196 328 300" stroke="{hc}" stroke-width="9" fill="none" stroke-linecap="round"/>'
                    f'<rect x="104" y="280" width="30" height="48" rx="12" fill="{hc}"/><rect x="306" y="280" width="30" height="48" rx="12" fill="{hc}"/>'
                    f'<rect x="110" y="290" width="10" height="28" rx="5" fill="{c["accent"]}"/><rect x="320" y="290" width="10" height="28" rx="5" fill="{c["accent"]}"/>'
                    f'<path d="M124 322 C130 360 150 376 182 380" stroke="{hc}" stroke-width="5" fill="none" stroke-linecap="round"/>'
                    f'<rect x="178" y="372" width="18" height="12" rx="6" fill="{hc}"/>')
    beard = ''
    if c.get("stubble"):
        beard = f'<path d="M132 318 C140 380 178 410 220 412 C262 410 300 380 308 318 C298 352 280 368 258 366 Q220 356 182 366 C160 368 142 352 132 318 Z" fill="{c["hair"]}" opacity="0.35"/><path d="M198 337 Q220 330 242 337 Q232 341 220 339 Q208 341 198 337 Z" fill="{c["hair"]}" opacity="0.55"/>'
    if c.get("beard"):
        beard = f'<path d="M126 300 C128 372 170 414 220 416 C270 414 312 372 314 300 C304 340 286 356 264 352 Q220 338 176 352 C154 356 136 340 126 300 Z" fill="{c["hair"]}"/><path d="M190 340 Q205 330 220 336 Q235 330 250 340 Q236 346 220 342 Q204 346 190 340 Z" fill="{c["hair"]}"/>'
    if c.get("mustache"):
        beard += f'<path d="M188 340 Q202 324 220 332 Q238 324 252 340 Q238 346 220 340 Q202 346 188 340 Z" fill="{c["hair"]}"/>'
    blush = '0.5' if c["glasses"] else '0.25'
    back = ''
    if c["hair_style"] == "afro":
        import math
        back = f'<ellipse cx="220" cy="218" rx="136" ry="114" fill="{c["hair"]}"/>' + ''.join(f'<circle cx="{220+130*math.cos(math.radians(a)):.0f}" cy="{218-110*math.sin(math.radians(a)):.0f}" r="22" fill="{c["hair"]}"/>' for a in range(-20, 201, 20))
    if c["hair_style"] == "space_buns":
        back = ''.join(f'<circle cx="{x}" cy="150" r="40" fill="{c["hair"]}"/><path d="M{x-24} 136 Q{x} 118 {x+24} 136" stroke="#FFFFFF" stroke-width="4" fill="none" opacity="0.15" stroke-linecap="round"/><path d="M{x-30} 176 Q{x} 190 {x+30} 176" stroke="{c["accent"]}" stroke-width="7" fill="none" stroke-linecap="round"/>' for x in (150, 290))
    if c["hair_style"] == "long_curly":
        pts = [(118, 232, 24), (110, 272, 24), (106, 314, 24), (108, 356, 24), (118, 394, 23), (322, 232, 24), (330, 272, 24), (334, 314, 24), (332, 356, 24), (322, 394, 23), (146, 194, 28), (294, 194, 28), (220, 178, 56)]
        back = ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c["hair"]}"/>' for x, y, r in pts) + f'<path d="M112 220 L328 220 L330 380 Q300 404 270 392 L170 392 Q140 404 110 380 Z" fill="{c["hair"]}"/>' + ''.join(f'<path d="M{x-12} {y-6} Q{x} {y+10} {x+12} {y-4}" stroke="#FFFFFF" stroke-width="3" fill="none" opacity="0.16" stroke-linecap="round"/>' for x, y, r in pts[:10])
    ear = f'<circle cx="122" cy="324" r="10" fill="none" stroke="{c["earrings"]}" stroke-width="4"/><circle cx="318" cy="324" r="10" fill="none" stroke="{c["earrings"]}" stroke-width="4"/>' if c.get("earrings") else ''
    if c.get("earrings_stud"): ear = f'<circle cx="122" cy="322" r="5" fill="{c["earrings_stud"]}"/><circle cx="318" cy="322" r="5" fill="{c["earrings_stud"]}"/>'
    return f'''{back}
    <circle cx="124" cy="302" r="16" fill="{c["skin_shade"]}"/><circle cx="316" cy="302" r="16" fill="{c["skin_shade"]}"/>
    <ellipse cx="220" cy="290" rx="96" ry="108" fill="{c["skin"]}"/>
    {hair}{ear}
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
