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
ARCHITECT = dict(skin="#F1CDA8", skin_shade="#DCAE86", hair="#121216", outfit="#B5543A", outfit_shade="#93412B",
    accent="#F2C14E", tee="#26282E", tee_shade="#17181C", wall_top="#E9E5DE", wall_bot="#C9C2B6", room="drafting_studio", outfit_style="overshirt",
    hair_style="asym_bob", glasses="round_thick", earrings_stud="#D9DDE2")
PHARMACIST = dict(skin="#7A4A2E", skin_shade="#633A22", hair="#141012", outfit="#F5F7F8", outfit_shade="#D2DBE0",
    accent="#1F8A7A", wall_top="#EAF4EF", wall_bot="#C2DDD2", room="pharmacy", outfit_style="pharmacy_tunic",
    hair_style="flat_fade", glasses="browline", goatee=True, mustache=True)
ELECTRICIAN = dict(skin="#C48A62", skin_shade="#A87048", hair="#3A1F1A", outfit="#2E3E5C", outfit_shade="#223049",
    accent="#F2C230", tee="#E07B39", tee_shade="#BF6328", wall_top="#E3E8EE", wall_bot="#B9C3CF", room="workshop", outfit_style="bib_overalls",
    hair_style="side_braid", glasses=False, safety_glasses=True, earrings_stud="#F2C230")
FREELANCER = dict(skin="#A86B47", skin_shade="#8E5636", hair="#1A1412", outfit="#B23A3A", outfit_shade="#8A2A2C",
    accent="#F4C95D", tee="#F2E6CF", tee_shade="#D6C6A8", wall_top="#2F4E57", wall_bot="#1C3038", room="home_studio", outfit_style="flannel",
    hair_style="man_bun", glasses=False, beard=True, headphones="#2B2F3A")
CHEF = dict(skin="#9C6B4A", skin_shade="#82563A", hair="#17110F", outfit="#FAFAF7", outfit_shade="#D9DCD8",
    accent="#C8352E", cap="#22262E", cap_shade="#14171C", wall_top="#F4F1EA", wall_bot="#D9D3C6", room="kitchen", outfit_style="chef_jacket",
    hair_style="skull_cap", glasses=False, beard=True)
JOB_SEEKER = dict(skin="#C99A78", skin_shade="#AE7F5E", hair="#2A1E1A", outfit="#7FA38A", outfit_shade="#628A70",
    accent="#F2B84B", hijab="#7A3E5C", hijab_shade="#5E2E46", strap="#8A5A3C", wall_top="#35554A", wall_bot="#1E3530", room="library_nook",
    outfit_style="knit_sweater", hair_style="hijab", glasses=False)
ANALYST = dict(skin="#B57E57", skin_shade="#9A6542", hair="#16120F", outfit="#5E8C6A", outfit_shade="#4A7356",
    accent="#F2A541", shirt="#EEF2F6", shirt_shade="#C9D3DC", wall_top="#1F3B45", wall_bot="#0F2128", room="data_desk", outfit_style="quarter_zip",
    hair_style="swoop", glasses="tortoise", stubble=True)
PROJECT_MANAGER = dict(skin="#6E4430", skin_shade="#58331F", hair="#1A1210", outfit="#1F7A74", outfit_shade="#17605B",
    accent="#F2B84B", wall_top="#3B2E4A", wall_bot="#1F1828", room="pm_office", outfit_style="wrap_top",
    hair_style="locs_bun", glasses=False, earrings="#F2B84B")
SOCIAL_WORKER = dict(skin="#E6BE98", skin_shade="#CDA07A", hair="#17161A", grey="#9C9AA0", outfit="#2F5E4E", outfit_shade="#224739",
    accent="#E8735A", shirt="#A9C4DE", shirt_shade="#86A6C4", wall_top="#F3E6D6", wall_bot="#DCC4A8", room="community_office",
    outfit_style="fleece_vest", hair_style="crew_grey", glasses=False)
PHOTOGRAPHER = dict(skin="#F3D2B8", skin_shade="#DEB296", hair="#9A4A26", outfit="#2B2E35", outfit_shade="#1D1F24",
    accent="#E9B949", beanie="#D98E3A", beanie_shade="#B8722A", strap="#2F6F7A", wall_top="#3A3F47", wall_bot="#1E2126", room="photo_studio",
    outfit_style="camera_tee", hair_style="beanie_waves", glasses=False, freckles=True, earrings_stud="#E9B949")
TRANSLATOR = dict(skin="#C9A07C", skin_shade="#AF865F", hair="#8F8A84", hair_dark="#4A4440", outfit="#5A2E46", outfit_shade="#431F33",
    accent="#3FA7A0", shirt="#E9EEF2", shirt_shade="#C3CDD6", neck_headset="#24272E", wall_top="#E8E1D6", wall_bot="#C9BCA6", room="interp_booth",
    outfit_style="shawl_cardigan", hair_style="silver_swept", glasses="wire_round", beard=True)
VET = dict(skin="#A8704A", skin_shade="#8E5A37", hair="#1C1310", outfit="#3E9C9A", outfit_shade="#2F7E7C",
    accent="#F28C5A", under="#2E3A52", under_shade="#222C40", steth="#2B2F3A", wall_top="#EAF3F1", wall_bot="#C6DFDA", room="vet_exam",
    outfit_style="vet_scrubs", hair_style="curly_pony", glasses=False, earrings_stud="#F28C5A")
FARMER = dict(skin="#B07A52", skin_shade="#95633F", hair="#1E1814", grey="#8E8984", outfit="#B98A47", outfit_shade="#9A7036",
    accent="#3E6B3A", collar="#5A3A26", henley="#8E3B2F", henley_shade="#722C23", cap="#3E6B3A", cap_shade="#2E5229", mesh="#EFE6D2",
    wall_top="#C89A6A", wall_bot="#9C6E45", room="farm_office", outfit_style="chore_coat", hair_style="trucker_cap", glasses=False,
    stubble=True, mustache=True)
FITNESS = dict(skin="#E9B994", skin_shade="#D29C76", hair="#B8893E", hair_dark="#9C7436", outfit="#2350B8", outfit_shade="#1A3E92",
    accent="#C6F24E", tee="#C6F24E", tee_shade="#A4CE34", stripe="#F4F6FA", wall_top="#F0F2F4", wall_bot="#CBD2DA", room="gym_studio",
    outfit_style="track_jacket", hair_style="faux_hawk", glasses=False, beard=True)
LOGISTICS = dict(skin="#6E4530", skin_shade="#5A3624", hair="#16110F", outfit="#22304F", outfit_shade="#18233B",
    accent="#FF7A1A", vest="#FF7A1A", vest_shade="#DB5F0A", reflect="#E3E8EE", wall_top="#7C8A99", wall_bot="#4C5866",
    room="loading_dock", outfit_style="hi_vis_vest", hair_style="twists", glasses=False, beard=True)
INTERVIEWEE = dict(skin="#D9A882", skin_shade="#C08B64", hair="#2B1D16", hair_dark="#1A110C", outfit="#2C3A52", outfit_shade="#1F2A3D",
    accent="#B8423A", shirt="#DCE8F5", shirt_shade="#B7C9DD", wall_top="#E7ECEA", wall_bot="#B9C7C4", room="lobby",
    outfit_style="interview_suit", hair_style="textured_crop", glasses=False)
PRODUCT_MANAGER = dict(skin="#CF9C74", skin_shade="#B58158", hair="#221714", outfit="#C97B8E", outfit_shade="#A9617A",
    accent="#2F6FDB", tee="#F7F4EE", tee_shade="#D9D3C8", rib="#24324D", rib_stripe="#F2C14E", wall_top="#E4ECE3", wall_bot="#BACDBB",
    room="product_lab", outfit_style="bomber", hair_style="curtain_lob", glasses=False, earrings_stud="#F2C14E")
CONSULTANT = dict(skin="#6A3F28", skin_shade="#55301D", hair="#1A1311", outfit="#2E5A4C", outfit_shade="#22463A",
    accent="#D9A441", shell="#F4EEE3", shell_shade="#D8CFC0", wall_top="#DDE3E8", wall_bot="#AEB9C4", room="war_room",
    outfit_style="double_breasted", hair_style="box_braids", glasses="rect_gold", earrings="#D9A441")
EVENT_PLANNER = dict(skin="#B9825A", skin_shade="#9E6A44", hair="#2A1C15", hair_dark="#160F0B", outfit="#1E6B6B", outfit_shade="#155252",
    accent="#FF6B5A", tee="#23262D", tee_shade="#15171C", wall_top="#3A2D4F", wall_bot="#1C1630", room="event_venue",
    outfit_style="event_blazer", hair_style="curly_top", glasses=False, stubble=True, earpiece="#1E2026")
PRESENTERS = {"event_planner": EVENT_PLANNER, "consultant": CONSULTANT, "product_manager": PRODUCT_MANAGER, "interviewee": INTERVIEWEE, "logistics": LOGISTICS, "fitness_trainer": FITNESS, "farmer": FARMER, "veterinarian": VET, "translator": TRANSLATOR, "photographer": PHOTOGRAPHER, "social_worker": SOCIAL_WORKER, "project_manager": PROJECT_MANAGER, "analyst": ANALYST, "job_seeker": JOB_SEEKER, "chef": CHEF, "freelancer": FREELANCER, "electrician": ELECTRICIAN, "pharmacist": PHARMACIST, "architect": ARCHITECT, "journalist": JOURNALIST, "support": SUPPORT, "researcher": RESEARCHER, "realtor": REALTOR, "hr": HR, "sales": SALES, "designer": DESIGNER, "accountant": ACCOUNTANT, "marketer": MARKETER, "nurse": NURSE, "lawyer": LAWYER, "dentist": DENTIST, "shopowner": SHOPOWNER, "student": STUDENT, "manager": MANAGER, "teacher": TEACHER, "doctor": DOCTOR, "developer": DEVELOPER}

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
    if c["room"] == "war_room":
        a = c["accent"]
        # glass whiteboard with a hand-drawn issue tree, left
        wb = ('<rect x="8" y="22" width="150" height="176" rx="4" fill="#F7FAFB" opacity="0.95"/><rect x="8" y="22" width="150" height="176" rx="4" fill="none" stroke="#8A97A3" stroke-width="3"/>'
              '<text x="83" y="40" font-family="Inter" font-weight="800" font-size="9" fill="#2B3440" text-anchor="middle" letter-spacing="1.2">WHY LATE?</text>'
              '<rect x="54" y="48" width="58" height="18" rx="3" fill="none" stroke="#2B3440" stroke-width="2"/><rect x="62" y="55" width="42" height="3" rx="1.5" fill="#2B3440"/>')
        mids = [(30, 96), (83, 96), (136, 96)]
        for x, y in mids:
            wb += f'<path d="M83 66 L83 76 L{x} 76 L{x} {y-8}" stroke="#2B3440" stroke-width="1.8" fill="none"/>'
            wb += f'<rect x="{x-22}" y="{y-8}" width="44" height="16" rx="3" fill="none" stroke="{"#C0392B" if x == 83 else "#2B3440"}" stroke-width="2"/><rect x="{x-14}" y="{y-2}" width="28" height="3" rx="1.5" fill="#5A6672"/>'
            for dx in (-12, 12):
                wb += f'<path d="M{x} {y+8} L{x} {y+18} L{x+dx} {y+18} L{x+dx} {y+26}" stroke="#5A6672" stroke-width="1.5" fill="none"/><rect x="{x+dx-9}" y="{y+26}" width="18" height="12" rx="2" fill="none" stroke="#5A6672" stroke-width="1.5"/>'
        wb += '<ellipse cx="83" cy="88" rx="30" ry="15" fill="none" stroke="#C0392B" stroke-width="2" transform="rotate(-4 83 88)" opacity="0.0"/>'
        for i, (x, y, col) in enumerate([(14, 152, "#F6D365"), (46, 158, "#9FE2BF"), (78, 150, "#F7A8B8"), (112, 156, "#9FC9F2")]):
            r = (-5, 3, -2, 4)[i]
            wb += (f'<g transform="rotate({r} {x+14} {y+14})"><rect x="{x}" y="{y}" width="28" height="28" rx="1.5" fill="{col}"/>'
                   f'<rect x="{x+5}" y="{y+8}" width="18" height="2.5" rx="1" fill="#3A3226" opacity="0.5"/><rect x="{x+5}" y="{y+15}" width="13" height="2.5" rx="1" fill="#3A3226" opacity="0.5"/></g>')
        # wall screen with a slide: action title bar and a bar chart, right
        scr = ('<rect x="300" y="20" width="132" height="92" rx="5" fill="#1E2630"/><rect x="306" y="26" width="120" height="76" fill="#FFFFFF"/>'
               f'<rect x="312" y="32" width="96" height="5" rx="2.5" fill="#1E2630"/><rect x="312" y="41" width="70" height="3" rx="1.5" fill="#9AA6B2"/>'
               '<path d="M314 94 L420 94" stroke="#9AA6B2" stroke-width="1.5"/>')
        for i, h in enumerate((22, 30, 16, 38, 44)):
            scr += f'<rect x="{318 + i*20}" y="{94-h}" width="13" height="{h}" fill="{a if i == 4 else "#7D8FA3"}"/>'
        scr += '<rect x="360" y="112" width="12" height="10" fill="#1E2630"/><rect x="346" y="120" width="40" height="5" rx="2.5" fill="#1E2630"/>'
        # printed deck pinned on the wall below the screen
        deck = ('<g transform="rotate(-3 366 170)"><rect x="330" y="138" width="78" height="56" rx="2" fill="#FFFFFF" stroke="#AEB9C4" stroke-width="1.5"/>'
                f'<rect x="336" y="144" width="66" height="4" rx="2" fill="#2B3440"/><rect x="336" y="154" width="30" height="30" rx="2" fill="#E8EEF2"/>'
                f'<path d="M340 178 L348 170 L354 174 L362 162" stroke="{a}" stroke-width="2.5" fill="none" stroke-linecap="round"/>'
                '<rect x="370" y="156" width="28" height="3" rx="1.5" fill="#9AA6B2"/><rect x="370" y="164" width="24" height="3" rx="1.5" fill="#9AA6B2"/><rect x="370" y="172" width="26" height="3" rx="1.5" fill="#9AA6B2"/>'
                '<circle cx="369" cy="140" r="3.5" fill="#C0392B"/></g>')
        # pendant lights
        lamp = ''.join(f'<path d="M{x} 0 L{x} 14" stroke="#2B3440" stroke-width="2.5"/><path d="M{x-14} 28 Q{x-12} 14 {x} 14 Q{x+12} 14 {x+14} 28 Z" fill="#2B3440"/><ellipse cx="{x}" cy="28" rx="13" ry="3.5" fill="#FFE7A8"/>' for x in (200, 244))
        # window mullions behind (glass office wall)
        glass = ''.join(f'<path d="M{x} 0 L{x} 286" stroke="#FFFFFF" stroke-width="3" opacity="0.35"/>' for x in (170, 290))
        table = (f'<rect x="0" y="292" width="{PW}" height="348" fill="#3E4A56"/><rect x="0" y="286" width="{PW}" height="8" fill="#56636F"/><rect x="0" y="294" width="{PW}" height="4" fill="#2A333C"/>'
                 # stack of printed decks and a pen, left
                 '<rect x="18" y="274" width="62" height="6" rx="1" fill="#FFFFFF"/><rect x="20" y="268" width="62" height="6" rx="1" fill="#EEF2F5"/><rect x="16" y="280" width="64" height="6" rx="1" fill="#FFFFFF"/>'
                 f'<rect x="22" y="262" width="58" height="6" rx="1" fill="#FFFFFF"/><rect x="22" y="262" width="58" height="2" fill="{a}"/>'
                 '<path d="M30 258 L76 250" stroke="#1E2630" stroke-width="3" stroke-linecap="round"/>'
                 # coffee cup and croissant on a napkin (the bakery client)
                 '<path d="M92 262 L96 288 L114 288 L118 262 Z" fill="#FFFFFF"/><rect x="90" y="258" width="30" height="6" rx="2" fill="#2E5A4C"/>'
                 '<rect x="360" y="282" width="62" height="6" rx="1" fill="#FFFFFF" opacity="0.9"/>'
                 '<path d="M366 282 Q370 262 391 260 Q412 262 416 282 Z" fill="#D99A4E"/><path d="M378 280 Q382 268 386 264 M392 280 Q393 268 394 262 M404 280 Q402 268 398 264" stroke="#A86A2C" stroke-width="2.5" fill="none" stroke-linecap="round"/>'
                 '<path d="M372 270 Q380 266 384 270" stroke="#F2C98C" stroke-width="2" fill="none" opacity="0.7"/>'
                 # laptop, right-centre
                 '<path d="M282 286 L290 250 L350 250 L344 286 Z" fill="#B8C0C8"/><path d="M286 282 L293 254 L346 254 L340 282 Z" fill="#1F2A3A"/>'
                 f'<rect x="298" y="260" width="34" height="4" rx="2" fill="{a}"/><rect x="297" y="268" width="26" height="3" rx="1.5" fill="#8A97A3"/><rect x="296" y="274" width="30" height="3" rx="1.5" fill="#8A97A3"/>')
        return f'''<defs><linearGradient id="w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c["wall_top"]}"/><stop offset="1" stop-color="{c["wall_bot"]}"/></linearGradient>
        <radialGradient id="g" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#FFF3C9" stop-opacity="0.35"/><stop offset="1" stop-color="#FFF3C9" stop-opacity="0"/></radialGradient></defs>
        <rect width="{PW}" height="{PH}" fill="url(#w)"/>{glass}<circle cx="222" cy="110" r="150" fill="url(#g)"/>
        {wb}{scr}{deck}{lamp}{table}'''
    if c["room"] == "event_venue":
        a = c["accent"]
        import math
        # string lights: two swags across the top, warm bulbs with glow
        lights = ''
        for (x0, x1, y0, sag) in [(-10, 220, 14, 34), (220, 450, 14, 36)]:
            lights += f'<path d="M{x0} {y0} Q{(x0+x1)/2} {y0+2*sag} {x1} {y0}" stroke="#141020" stroke-width="2" fill="none"/>'
            for i in range(1, 8):
                t = i / 8; x = (1-t)**2*x0 + 2*(1-t)*t*(x0+x1)/2 + t*t*x1; y = (1-t)**2*y0 + 2*(1-t)*t*(y0+2*sag) + t*t*y0
                lights += f'<circle cx="{x:.0f}" cy="{y+7:.0f}" r="11" fill="#FFD98A" opacity="0.18"/><rect x="{x-2.5:.0f}" y="{y:.0f}" width="5" height="4" fill="#3A3346"/><ellipse cx="{x:.0f}" cy="{y+8:.0f}" rx="4.5" ry="5.5" fill="#FFE3A3"/>'
        # welcome easel sign, left
        easel = ('<path d="M40 236 L58 150 M118 236 L100 150 M79 236 L79 160" stroke="#8A6A48" stroke-width="5" stroke-linecap="round"/>'
                 '<rect x="16" y="86" width="126" height="118" rx="6" fill="#F7F1E6" stroke="#C9A86A" stroke-width="4"/>'
                 '<text x="79" y="112" font-family="Inter" font-weight="800" font-size="11" fill="#5A4A3A" text-anchor="middle" letter-spacing="2">WELCOME</text>'
                 f'<path d="M36 120 L122 120" stroke="{a}" stroke-width="2"/>'
                 '<text x="79" y="142" font-family="Inter" font-weight="800" font-size="17" fill="#1E6B6B" text-anchor="middle">FERNHILL</text>'
                 '<text x="79" y="160" font-family="Inter" font-weight="600" font-size="10" fill="#5A4A3A" text-anchor="middle" letter-spacing="1.5">TEAM OFFSITE</text>'
                 '<path d="M50 176 Q60 168 70 176 Q79 168 88 176 Q98 168 108 176" stroke="#7FA88A" stroke-width="2.5" fill="none"/>'
                 '<text x="79" y="194" font-family="Inter" font-weight="600" font-size="9" fill="#8A7A6A" text-anchor="middle">DAY 1 · 09:00</text>')
        # tall window onto the lake, right
        win = ('<rect x="318" y="76" width="114" height="160" rx="6" fill="#2A2238"/>'
               '<rect x="326" y="84" width="98" height="144" fill="#F4B98A"/><rect x="326" y="84" width="98" height="60" fill="#E9906E" opacity="0.55"/>'
               '<circle cx="392" cy="150" r="14" fill="#FFE1A6"/>'
               '<path d="M326 160 L350 136 L370 152 L394 128 L424 156 L424 168 L326 168 Z" fill="#6E5A7A"/>'
               '<rect x="326" y="166" width="98" height="62" fill="#4E6E8E"/><path d="M380 172 L404 172 M372 184 L412 184 M386 196 L400 196" stroke="#FFE1A6" stroke-width="2.5" opacity="0.8"/>'
               + ''.join(f'<path d="M{x} {y} L{x-9} {y+26} L{x+9} {y+26} Z" fill="#2E4A3A"/><path d="M{x} {y+8} L{x-11} {y+36} L{x+11} {y+36} Z" fill="#2E4A3A"/>' for x, y in [(336, 168), (352, 178)])
               + '<path d="M375 84 L375 228 M326 156 L424 156" stroke="#2A2238" stroke-width="5"/>'
               '<path d="M318 236 L432 236" stroke="#1A1424" stroke-width="6"/>')
        # registration table with white cloth, badges, a walkie-talkie and a table-number card
        table = (f'<rect x="0" y="292" width="{PW}" height="348" fill="#EDE8F0"/><rect x="0" y="286" width="{PW}" height="10" fill="#FFFFFF"/>'
                 + ''.join(f'<path d="M{x} 300 L{x} 640" stroke="#D6CEDD" stroke-width="3"/>' for x in range(20, 440, 40))
                 + f'<rect x="0" y="296" width="{PW}" height="6" fill="{a}" opacity="0.85"/>'
                 # name badges laid out in rows, left
                 + ''.join(f'<rect x="{x}" y="{y}" width="26" height="18" rx="2" fill="#FFFFFF" stroke="#B9AFC6" stroke-width="1.5"/><rect x="{x}" y="{y}" width="26" height="5" rx="1" fill="{col}"/><rect x="{x+4}" y="{y+9}" width="16" height="2.5" rx="1" fill="#6A6276"/>'
                         for (x, y, col) in [(10, 250, "#1E6B6B"), (40, 250, a), (70, 250, "#1E6B6B"), (10, 268, a), (40, 268, "#1E6B6B"), (70, 268, a)])
                 # walkie-talkie
                 + '<rect x="354" y="236" width="24" height="50" rx="5" fill="#2B2F3A"/><rect x="370" y="216" width="5" height="24" rx="2" fill="#2B2F3A"/>'
                 '<rect x="358" y="244" width="16" height="12" rx="2" fill="#9FE2BF"/>' + ''.join(f'<path d="M359 {y} L373 {y}" stroke="#555B68" stroke-width="2"/>' for y in (264, 270, 276))
                 # table number tent card
                 + '<path d="M392 286 L404 246 L428 246 L436 286 Z" fill="#FFFFFF" stroke="#C9A86A" stroke-width="2"/>'
                 '<text x="416" y="276" font-family="Inter" font-weight="800" font-size="20" fill="#1E6B6B" text-anchor="middle">7</text>')
        return f'''<defs><linearGradient id="w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c["wall_top"]}"/><stop offset="1" stop-color="{c["wall_bot"]}"/></linearGradient>
        <radialGradient id="g" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#FFD98A" stop-opacity="0.25"/><stop offset="1" stop-color="#FFD98A" stop-opacity="0"/></radialGradient></defs>
        <rect width="{PW}" height="{PH}" fill="url(#w)"/><circle cx="220" cy="120" r="170" fill="url(#g)"/>
        {lights}{easel}{win}{table}'''
    if c["room"] == "product_lab":
        a = c["accent"]
        # customer journey map on the left wall: five stages, a feelings line with faces, sticky notes
        jm = ('<rect x="8" y="24" width="142" height="144" rx="6" fill="#FBFAF6"/><rect x="8" y="24" width="142" height="144" rx="6" fill="none" stroke="#8E9C90" stroke-width="3"/>'
              f'<rect x="8" y="24" width="142" height="20" rx="6" fill="{a}"/><rect x="8" y="36" width="142" height="8" fill="{a}"/>'
              '<text x="79" y="38" font-family="Inter" font-weight="800" font-size="9.5" fill="#FFFFFF" text-anchor="middle" letter-spacing="1.5">JOURNEY MAP</text>'
              + ''.join(f'<path d="M{x} 52 L{x} 162" stroke="#E2DED4" stroke-width="1.5"/>' for x in (36, 64, 92, 120)))
        pts = [(22, 94), (50, 76), (78, 112), (106, 86), (134, 66)]
        jm += '<path d="M' + ' L'.join(f'{x} {y}' for x, y in pts) + '" stroke="#8E9C90" stroke-width="2.5" fill="none" stroke-dasharray="5 4"/>'
        for i, (x, y) in enumerate(pts):
            sad = i == 2
            jm += (f'<circle cx="{x}" cy="{y}" r="9" fill="{"#F7A8B8" if sad else "#F6D365"}" stroke="#4A3E2A" stroke-width="1.5"/>'
                   f'<circle cx="{x-3}" cy="{y-2}" r="1.4" fill="#4A3E2A"/><circle cx="{x+3}" cy="{y-2}" r="1.4" fill="#4A3E2A"/>'
                   + (f'<path d="M{x-4} {y+5} Q{x} {y+1} {x+4} {y+5}" stroke="#4A3E2A" stroke-width="1.5" fill="none"/>' if sad else f'<path d="M{x-4} {y+2} Q{x} {y+6} {x+4} {y+2}" stroke="#4A3E2A" stroke-width="1.5" fill="none"/>'))
            jm += f'<rect x="{x-10}" y="54" width="20" height="6" rx="3" fill="#C9D3CB"/>'
        for i, (x, y, col) in enumerate([(12, 130, "#F6D365"), (40, 136, "#9FE2BF"), (68, 128, "#F7A8B8"), (96, 136, "#9FC9F2"), (124, 130, "#F6D365")]):
            r = (-4, 3, -2, 4, -3)[i]
            jm += (f'<g transform="rotate({r} {x+11} {y+11})"><rect x="{x}" y="{y}" width="22" height="22" rx="1.5" fill="{col}"/>'
                   f'<rect x="{x+4}" y="{y+6}" width="14" height="2.5" rx="1" fill="#4A3E2A" opacity="0.5"/><rect x="{x+4}" y="{y+12}" width="10" height="2.5" rx="1" fill="#4A3E2A" opacity="0.5"/></g>')
        # lit WHY? sign, top right
        sign = ('<rect x="326" y="24" width="104" height="54" rx="10" fill="#1F2A3A"/>'
                f'<text x="378" y="62" font-family="Inter" font-weight="800" font-size="30" fill="none" stroke="{a}" stroke-width="5" opacity="0.35" text-anchor="middle">WHY?</text>'
                '<text x="378" y="62" font-family="Inter" font-weight="800" font-size="30" fill="#F2C14E" text-anchor="middle">WHY?</text>'
                '<path d="M350 24 L346 8 M406 24 L410 8" stroke="#1F2A3A" stroke-width="2"/>')
        # persona card pinned below it
        card = ('<g transform="rotate(2 378 148)"><rect x="328" y="92" width="102" height="112" rx="5" fill="#FFFFFF" stroke="#9AA79B" stroke-width="2"/>'
                f'<rect x="328" y="92" width="102" height="18" rx="5" fill="#E5684C"/><rect x="328" y="104" width="102" height="6" fill="#E5684C"/>'
                '<text x="379" y="105" font-family="Inter" font-weight="800" font-size="9" fill="#FFFFFF" text-anchor="middle" letter-spacing="1.5">PERSONA</text>'
                '<circle cx="352" cy="134" r="15" fill="#F6E3CF"/><circle cx="352" cy="130" r="6" fill="#8A5A3C"/><path d="M341 145 Q352 133 363 145 Z" fill="#8A5A3C"/>'
                '<rect x="373" y="122" width="48" height="5" rx="2.5" fill="#2B2F3A"/><rect x="373" y="132" width="38" height="3" rx="1.5" fill="#9AA6A4"/><rect x="373" y="139" width="44" height="3" rx="1.5" fill="#9AA6A4"/>'
                '<rect x="338" y="158" width="82" height="3" rx="1.5" fill="#9AA6A4"/><rect x="338" y="166" width="70" height="3" rx="1.5" fill="#9AA6A4"/>'
                f'<rect x="338" y="178" width="30" height="12" rx="6" fill="{a}" opacity="0.85"/><rect x="372" y="178" width="38" height="12" rx="6" fill="#9FE2BF"/>'
                '<circle cx="379" cy="94" r="4" fill="#E5684C" stroke="#8E2F1F" stroke-width="1"/></g>')
        lamp = '<path d="M232 0 L232 22" stroke="#1F2A3A" stroke-width="3"/><path d="M214 42 Q216 22 232 22 Q248 22 250 42 Z" fill="#2F6F5A"/><ellipse cx="232" cy="42" rx="18" ry="4" fill="#FFE7A8"/>'
        desk = (f'<rect x="0" y="292" width="{PW}" height="348" fill="#C7AE8A"/><rect x="0" y="286" width="{PW}" height="8" fill="#DCC6A2"/><rect x="0" y="294" width="{PW}" height="4" fill="#9C8462"/>'
                # laptop with a rising usage chart, right
                '<path d="M330 286 L340 244 L422 244 L414 286 Z" fill="#B8C0C8"/><path d="M335 282 L344 248 L417 248 L409 282 Z" fill="#1F2A3A"/>'
                f'<path d="M348 274 L362 268 L374 271 L388 260 L404 254" stroke="{a}" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
                '<path d="M348 276 L404 276" stroke="#5A6578" stroke-width="1.5"/><circle cx="404" cy="254" r="3" fill="#F2C14E"/>'
                '<rect x="322" y="284" width="100" height="6" rx="3" fill="#D3D9DE"/>'
                # sticky-note pads and a marker, left
                '<rect x="18" y="268" width="34" height="18" rx="2" fill="#F6D365"/><rect x="18" y="264" width="34" height="6" fill="#E9C24F"/>'
                '<rect x="20" y="256" width="30" height="10" rx="2" fill="#F7A8B8" transform="rotate(-6 35 261)"/>'
                
                # mug
                '<rect x="64" y="252" width="26" height="34" rx="5" fill="#FFFFFF"/><path d="M90 260 Q104 262 102 272 Q100 280 90 278" stroke="#FFFFFF" stroke-width="5" fill="none"/>'
                f'<text x="77" y="276" font-family="Inter" font-weight="800" font-size="16" fill="{a}" text-anchor="middle">?</text>')
        return f'''<defs><linearGradient id="w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c["wall_top"]}"/><stop offset="1" stop-color="{c["wall_bot"]}"/></linearGradient>
        <radialGradient id="g" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#FFF3C9" stop-opacity="0.4"/><stop offset="1" stop-color="#FFF3C9" stop-opacity="0"/></radialGradient></defs>
        <rect width="{PW}" height="{PH}" fill="url(#w)"/><circle cx="232" cy="96" r="150" fill="url(#g)"/>
        {jm}{sign}{card}{lamp}{desk}'''
    if c["room"] == "lobby":
        import math
        a = c["accent"]
        # panelled lower wall
        wall = ('<rect x="0" y="200" width="440" height="92" fill="#8FA19E"/>'
                + ''.join(f'<path d="M{x} 200 L{x} 292" stroke="#7B8D8A" stroke-width="2"/>' for x in range(36, 440, 52))
                + '<rect x="0" y="196" width="440" height="6" fill="#6E807D"/>')
        # tall window onto a city skyline, left
        win = '<rect x="8" y="16" width="118" height="180" rx="3" fill="#3C4A5C"/><rect x="14" y="22" width="106" height="168" fill="#BFDDEE"/>'
        win += '<rect x="14" y="120" width="106" height="70" fill="#D9ECF5"/>'
        for x, w, h, col in [(16, 20, 92, "#7C93AE"), (38, 16, 64, "#93A9C2"), (56, 24, 112, "#6C83A0"), (82, 14, 76, "#8AA1BB"), (98, 20, 100, "#7890AB")]:
            win += f'<rect x="{x}" y="{190-h}" width="{w}" height="{h}" fill="{col}"/>'
            win += ''.join(f'<rect x="{x+3+j*6}" y="{194-h+i*10}" width="3" height="5" fill="#E8F2F8" opacity="0.8"/>' for i in range(h//10 - 1) for j in range(max(1, (w-4)//6)))
        win += '<path d="M67 22 L67 190 M14 106 L120 106" stroke="#3C4A5C" stroke-width="4"/>'
        # plant on the floor beside the window
        plant = ('<path d="M18 288 L24 250 L58 250 L64 288 Z" fill="#E8E2D6"/><rect x="20" y="246" width="42" height="7" rx="2" fill="#D3CBBB"/>'
                 + ''.join(f'<path d="M41 248 Q{41+dx} {200+abs(dx)//2} {41+dx*1.4:.0f} {178+abs(dx)}" stroke="#3E7D5A" stroke-width="7" fill="none" stroke-linecap="round"/>' for dx in (-22, -10, 0, 12, 24)))
        # wall clock, top right of centre
        clock = ('<circle cx="370" cy="40" r="24" fill="#FFFFFF" stroke="#2B2F3A" stroke-width="4"/>'
                 + ''.join(f'<path d="M{370+17*math.cos(t*0.5236):.1f} {40+17*math.sin(t*0.5236):.1f} L{370+21*math.cos(t*0.5236):.1f} {40+21*math.sin(t*0.5236):.1f}" stroke="#2B2F3A" stroke-width="2"/>' for t in range(12))
                 + f'<path d="M370 40 L370 24 M370 40 L360 34" stroke="#2B2F3A" stroke-width="3" stroke-linecap="round"/><circle cx="370" cy="40" r="2.5" fill="{a}"/>')
        # countdown calendar with crossed-off days and the interview day circled, right
        cal = (f'<rect x="330" y="78" width="100" height="104" rx="4" fill="#FFFFFF" stroke="#9AA6A4" stroke-width="2"/><rect x="330" y="78" width="100" height="20" rx="4" fill="{a}"/>'
               '<text x="380" y="93" font-family="Inter" font-weight="800" font-size="10" fill="#FFFFFF" text-anchor="middle">THIS WEEK</text>')
        for i in range(12):
            x = 340 + (i % 4) * 22; y = 106 + (i // 4) * 24
            cal += f'<rect x="{x}" y="{y}" width="16" height="16" rx="2" fill="#EEF2F1"/>'
            if i < 6:
                cal += f'<path d="M{x+3} {y+3} L{x+13} {y+13} M{x+13} {y+3} L{x+3} {y+13}" stroke="#7B8D8A" stroke-width="2" stroke-linecap="round"/>'
        cal += f'<circle cx="{340+2*22+8}" cy="{106+24+8}" r="11" fill="none" stroke="{a}" stroke-width="3"/>'
        cal += f'<text x="380" y="178" font-family="Inter" font-weight="800" font-size="7.5" fill="{a}" text-anchor="middle">INTERVIEW</text>'
        # welcome sign above the lower wall, right
        sign = ('<rect x="330" y="200" width="100" height="26" rx="3" fill="#2B2F3A"/>'
                '<circle cx="346" cy="213" r="7" fill="none" stroke="#E7ECEA" stroke-width="2.5"/><path d="M342 213 L346 217 L351 209" stroke="#E7ECEA" stroke-width="2" fill="none" stroke-linecap="round"/>'
                '<text x="392" y="217" font-family="Inter" font-weight="700" font-size="10" fill="#E7ECEA" text-anchor="middle">WELCOME</text>')
        desk = (f'<rect x="0" y="292" width="{PW}" height="348" fill="#5C4A3D"/><rect x="0" y="286" width="{PW}" height="8" fill="#7A6455"/><rect x="0" y="294" width="{PW}" height="4" fill="#3E3129"/>'
                # coffee cup, left
                '<path d="M82 262 L86 288 L104 288 L108 262 Z" fill="#FFFFFF"/><rect x="80" y="258" width="30" height="6" rx="2" fill="#2B2F3A"/><rect x="84" y="270" width="22" height="8" fill="#B8A27A"/>'
                # portfolio with CV and a printed question list, right
                '<rect x="332" y="246" width="98" height="42" rx="3" fill="#2B2F3A"/><rect x="340" y="238" width="58" height="48" fill="#FFFFFF" transform="rotate(-6 369 262)"/>'
                + ''.join(f'<rect x="{346}" y="{248 + i*7}" width="{40 - (i % 3) * 8}" height="3" fill="#9AA6A4" transform="rotate(-6 369 262)"/>' for i in range(5))
                + f'<text x="352" y="246" font-family="Inter" font-weight="800" font-size="7" fill="{a}" transform="rotate(-6 369 262)">CV</text>'
                '<rect x="398" y="252" width="26" height="34" rx="2" fill="#F6E7A8"/><path d="M402 260 L420 260 M402 266 L418 266 M402 272 L420 272" stroke="#8A7A40" stroke-width="2"/>'
                '<text x="404" y="282" font-family="Inter" font-weight="800" font-size="7" fill="#8A7A40">Q&amp;A</text>')
        return f'''<defs><linearGradient id="w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c["wall_top"]}"/><stop offset="1" stop-color="{c["wall_bot"]}"/></linearGradient>
        <radialGradient id="g" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0.45"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></radialGradient></defs>
        <rect width="{PW}" height="{PH}" fill="url(#w)"/><circle cx="220" cy="150" r="170" fill="url(#g)"/>
        {wall}{win}{plant}{clock}{cal}{sign}{desk}'''
    if c["room"] == "loading_dock":
        a = c["accent"]
        # corrugated warehouse wall and a hazard-striped kick rail
        wall = (''.join(f'<path d="M{x} 0 L{x} 286" stroke="#FFFFFF" stroke-width="3" opacity="0.06"/><path d="M{x+6} 0 L{x+6} 286" stroke="#000000" stroke-width="2" opacity="0.08"/>' for x in range(0, 440, 16))
                + '<rect x="0" y="262" width="440" height="24" fill="#2B2F36"/>'
                + '<defs><clipPath id="hz"><rect x="0" y="266" width="440" height="16"/></clipPath></defs><g clip-path="url(#hz)">'
                + ''.join(f'<path d="M{x} 282 L{x+12} 266 L{x+24} 266 L{x+12} 282 Z" fill="#F2C230"/>' for x in range(-20, 460, 24)) + '</g>')
        # roll-up dock door, half open, a delivery van backed up to it (left)
        door = ('<rect x="6" y="34" width="124" height="174" fill="#2B2F36"/>'
                '<rect x="14" y="42" width="108" height="166" fill="#D6E9F2"/><rect x="14" y="150" width="108" height="58" fill="#9AA6B2"/>'
                # van rear
                '<rect x="20" y="104" width="96" height="100" rx="6" fill="#F4F6F8"/><path d="M68 108 L68 200" stroke="#B9C2CC" stroke-width="2"/>'
                '<rect x="28" y="114" width="32" height="26" rx="3" fill="#5B6B7C"/><rect x="76" y="114" width="32" height="26" rx="3" fill="#5B6B7C"/>'
                '<rect x="22" y="170" width="8" height="18" rx="2" fill="#E0503A"/><rect x="106" y="170" width="8" height="18" rx="2" fill="#E0503A"/>'
                f'<rect x="40" y="150" width="56" height="10" rx="2" fill="{a}"/>'
                # shutter slats
                + '<rect x="14" y="42" width="108" height="62" fill="#AEB7C1"/>'
                + ''.join(f'<path d="M14 {y} L122 {y}" stroke="#7F8994" stroke-width="2"/>' for y in range(50, 104, 8))
                + '<rect x="14" y="100" width="108" height="6" fill="#5B6570"/><rect x="58" y="104" width="20" height="6" rx="2" fill="#2B2F36"/>'
                # dock sign
                f'<rect x="38" y="10" width="60" height="20" rx="3" fill="{a}"/><text x="68" y="25" font-family="Inter" font-weight="800" font-size="13" fill="#1A1D24" text-anchor="middle">DOCK 4</text>')
        # pallet racking with parcels (right)
        rack = ('<rect x="330" y="14" width="8" height="250" fill="#2E5FA8"/><rect x="424" y="14" width="8" height="250" fill="#2E5FA8"/>'
                f'<rect x="330" y="96" width="102" height="8" fill="{a}"/><rect x="330" y="182" width="102" height="8" fill="{a}"/>')
        for x, y, w, h, col in [(342, 54, 36, 42, "#C8955C"), (380, 64, 40, 32, "#B9844C"), (340, 140, 44, 42, "#B9844C"), (386, 150, 34, 32, "#D2A46C"),
                                (344, 226, 30, 36, "#C8955C"), (378, 236, 44, 26, "#B9844C")]:
            rack += (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{col}"/><rect x="{x + w//2 - 3}" y="{y}" width="6" height="{h}" fill="#E8D3A8" opacity="0.7"/>'
                     f'<rect x="{x+4}" y="{y+h-14}" width="14" height="10" fill="#FFFFFF"/>')
        desk = (f'<rect x="0" y="292" width="{PW}" height="348" fill="#3A3F48"/><rect x="0" y="286" width="{PW}" height="8" fill="#5A616C"/><rect x="0" y="294" width="{PW}" height="4" fill="#23272E"/>'
                # parcels on the bench, left
                '<rect x="12" y="232" width="62" height="56" fill="#C8955C"/><rect x="40" y="232" width="8" height="56" fill="#E8D3A8" opacity="0.75"/>'
                '<rect x="16" y="252" width="22" height="26" fill="#FFFFFF"/>'
                + ''.join(f'<rect x="{18 + i*3}" y="266" width="{1 + (i % 2)}" height="10" fill="#1A1D24"/>' for i in range(6))
                + '<rect x="19" y="256" width="16" height="3" fill="#5B6570"/><rect x="19" y="261" width="12" height="2" fill="#5B6570"/>'
                '<rect x="76" y="252" width="38" height="36" fill="#B9844C"/><rect x="92" y="252" width="6" height="36" fill="#E8D3A8" opacity="0.75"/>'
                # tablet with a route map, right
                '<rect x="334" y="232" width="96" height="58" rx="6" fill="#1A1D24"/><rect x="339" y="237" width="86" height="48" rx="2" fill="#E9F0E4"/>'
                '<path d="M339 262 L425 254 M372 237 L366 285 M400 237 L408 285" stroke="#FFFFFF" stroke-width="4"/>'
                f'<path d="M348 276 L362 258 L384 266 L398 246 L416 250" stroke="{a}" stroke-width="3" fill="none" stroke-linejoin="round" stroke-linecap="round"/>'
                + ''.join(f'<circle cx="{x}" cy="{y}" r="3.5" fill="#2E5FA8" stroke="#FFFFFF" stroke-width="1.5"/>' for x, y in [(348, 276), (362, 258), (384, 266), (398, 246), (416, 250)]))
        return f'''<defs><linearGradient id="w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c["wall_top"]}"/><stop offset="1" stop-color="{c["wall_bot"]}"/></linearGradient>
        <radialGradient id="g" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0.35"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></radialGradient></defs>
        <rect width="{PW}" height="{PH}" fill="url(#w)"/><circle cx="220" cy="150" r="170" fill="url(#g)"/>
        {wall}{door}{rack}{desk}'''
    if c["room"] == "gym_studio":
        a = c["accent"]
        # wall: lower rubber-panel wainscot and a wide mirror strip
        wall = ('<rect x="0" y="196" width="440" height="96" fill="#3A4150"/>'
                + ''.join(f'<path d="M{x} 196 L{x} 292" stroke="#2C323E" stroke-width="2"/>' for x in range(40, 440, 60))
                + f'<rect x="0" y="190" width="440" height="7" fill="{a}"/>')
        # whiteboard with the week's sessions, top left
        board = ('<rect x="12" y="20" width="114" height="112" rx="4" fill="#FFFFFF" stroke="#9AA4B0" stroke-width="3"/>'
                 '<text x="69" y="38" font-family="Inter" font-weight="800" font-size="10" fill="#1A3E92" text-anchor="middle">THIS WEEK</text>'
                 '<path d="M22 44 L116 44" stroke="#C9D0D8" stroke-width="1.5"/>')
        for i, (d, col, w) in enumerate([("MON", "#2350B8", 52), ("TUE", "#E0503A", 38), ("WED", "#2350B8", 58), ("THU", "#3E9C5A", 44), ("FRI", "#E0503A", 50)]):
            y = 54 + i * 15
            board += (f'<text x="22" y="{y+7}" font-family="Inter" font-weight="700" font-size="7.5" fill="#4A5260">{d}</text>'
                      f'<rect x="46" y="{y}" width="{w}" height="7" rx="3.5" fill="{col}" opacity="0.8"/>')
        board += '<path d="M104 118 L110 124 L120 110" stroke="#3E9C5A" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/><rect x="18" y="132" width="102" height="6" rx="2" fill="#9AA4B0"/><rect x="30" y="130" width="14" height="4" rx="2" fill="#E0503A"/>'
        # wall clock, top centre-right
        clock = ('<circle cx="356" cy="40" r="22" fill="#FFFFFF" stroke="#2B2F3A" stroke-width="4"/>'
                 + ''.join(f'<path d="M{356+16*__import__("math").cos(t*0.5236):.1f} {40+16*__import__("math").sin(t*0.5236):.1f} L{356+19*__import__("math").cos(t*0.5236):.1f} {40+19*__import__("math").sin(t*0.5236):.1f}" stroke="#2B2F3A" stroke-width="2"/>' for t in range(12))
                 + '<path d="M356 40 L356 27 M356 40 L366 45" stroke="#2B2F3A" stroke-width="3" stroke-linecap="round"/><circle cx="356" cy="40" r="2.5" fill="#E0503A"/>')
        # resistance bands on hooks, right
        bands = '<rect x="332" y="78" width="96" height="7" rx="3" fill="#8A929B"/>'
        for x, col in [(346, "#E0503A"), (370, "#F2B63D"), (394, "#2350B8"), (416, "#3E9C5A")]:
            bands += f'<circle cx="{x}" cy="88" r="3" fill="#4A5260"/><path d="M{x-6} 90 Q{x-9} 130 {x} 150 Q{x+9} 130 {x+6} 90" stroke="{col}" stroke-width="5" fill="none" stroke-linecap="round"/>'
        # dumbbell rack, right on the wainscot
        rack = '<rect x="330" y="232" width="104" height="6" rx="2" fill="#20242C"/>'
        for i, (x, r, col) in enumerate([(346, 9, "#E0503A"), (372, 10, "#F2B63D"), (400, 11, "#2350B8")]):
            rack += (f'<rect x="{x-4}" y="{224-r}" width="8" height="{2*r}" rx="2" fill="{col}"/><rect x="{x+16}" y="{224-r}" width="8" height="{2*r}" rx="2" fill="{col}"/>'
                     f'<rect x="{x+4}" y="221" width="12" height="6" rx="2" fill="#8A929B"/>')
        # kettlebells, left on the wainscot
        kb = ''
        for x, r, col in [(68, 15, "#2B2F3A"), (102, 12, "#E0503A")]:
            kb += (f'<path d="M{x-r*0.6:.0f} {286-2*r:.0f} Q{x} {286-3.3*r:.0f} {x+r*0.6:.0f} {286-2*r:.0f}" stroke="{col}" stroke-width="5" fill="none"/>'
                   f'<circle cx="{x}" cy="{286-r}" r="{r}" fill="{col}"/><circle cx="{x-r*0.35:.0f}" cy="{286-r*1.3:.0f}" r="{r*0.25:.0f}" fill="#FFFFFF" opacity="0.25"/>')
        # plant, upper left beside the board
        desk = (f'<rect x="0" y="292" width="{PW}" height="348" fill="#2B2F3A"/><rect x="0" y="286" width="{PW}" height="8" fill="#4A5260"/><rect x="0" y="294" width="{PW}" height="4" fill="#1A1D24"/>'
                # water bottle and a folded towel, left
                f'<rect x="20" y="226" width="26" height="62" rx="8" fill="#5BC0EB" opacity="0.9"/><rect x="24" y="214" width="18" height="14" rx="4" fill="#20242C"/><rect x="20" y="246" width="26" height="10" fill="#FFFFFF" opacity="0.35"/>'
                # tablet with a booking calendar, right
                '<rect x="334" y="236" width="94" height="54" rx="6" fill="#20242C"/><rect x="339" y="241" width="84" height="44" rx="2" fill="#F4F7FA"/><rect x="339" y="241" width="84" height="8" fill="#2350B8"/>'
                + ''.join(f'<rect x="{343 + j*16}" y="{253 + i*10}" width="12" height="7" rx="1.5" fill="{["#DCE4F2", "#C6F24E", "#DCE4F2", "#F6C9A0", "#DCE4F2"][(i*2+j) % 5]}"/>' for i in range(3) for j in range(5))
                )
        return f'''<defs><linearGradient id="w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c["wall_top"]}"/><stop offset="1" stop-color="{c["wall_bot"]}"/></linearGradient>
        <radialGradient id="g" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0.45"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></radialGradient></defs>
        <rect width="{PW}" height="{PH}" fill="url(#w)"/><circle cx="220" cy="150" r="170" fill="url(#g)"/>
        {wall}{board}{clock}{bands}{rack}{kb}{desk}'''
    if c["room"] == "farm_office":
        a = c["accent"]
        planks = ''.join(f'<path d="M0 {y} L{PW} {y}" stroke="#7E5532" stroke-width="2" opacity="0.45"/>' for y in range(26, 292, 26))
        planks += ''.join(f'<path d="M{x} {y} L{x} {y+26}" stroke="#7E5532" stroke-width="2" opacity="0.35"/>' for i, y in enumerate(range(0, 286, 26)) for x in ([60, 210, 360] if i % 2 else [130, 290, 420]))
        # window over the fields with a red barn and a small tractor, top left
        win = ('<rect x="10" y="16" width="112" height="132" rx="4" fill="#F4ECDD"/><rect x="17" y="23" width="98" height="118" fill="#BFE0F2"/>'
               '<circle cx="98" cy="40" r="9" fill="#FCE7A2"/>'
               '<path d="M17 92 Q50 76 80 86 Q100 80 115 84 L115 141 L17 141 Z" fill="#8DBF6E"/><path d="M17 104 Q60 92 115 100 L115 141 L17 141 Z" fill="#C9B062"/>'
               + ''.join(f'<path d="M{x} 141 L{66 + (x-66)*0.35:.0f} 104" stroke="#A58E45" stroke-width="2"/>' for x in range(14, 124, 12))
               + '<rect x="30" y="72" width="26" height="20" fill="#B83A2E"/><path d="M27 73 L43 60 L59 73 Z" fill="#8E2A22"/><rect x="38" y="80" width="10" height="12" fill="#F4ECDD"/><path d="M38 80 L48 92 M48 80 L38 92" stroke="#B83A2E" stroke-width="1.5"/>'
               '<rect x="60" y="68" width="8" height="24" rx="3" fill="#D9D3C6"/><path d="M60 68 Q64 62 68 68 Z" fill="#9A9488"/>'
               '<g transform="translate(84 86)"><rect x="0" y="0" width="16" height="9" rx="1.5" fill="#3E7A3A"/><rect x="9" y="-7" width="8" height="8" fill="#3E7A3A"/><rect x="10.5" y="-5.5" width="5" height="5" fill="#BFE0F2"/>'
               '<circle cx="4" cy="10" r="4" fill="#2B2F3A"/><circle cx="14" cy="9" r="6" fill="#2B2F3A"/><circle cx="14" cy="9" r="2" fill="#F2C14E"/></g>'
               '<path d="M66 23 L66 141 M17 82 L115 82" stroke="#F4ECDD" stroke-width="4"/>')
        # season planner calendar, top right
        cal = ('<rect x="324" y="18" width="104" height="108" rx="5" fill="#FBF6EA" stroke="#D8C8A8" stroke-width="2"/><rect x="324" y="18" width="104" height="18" rx="5" fill="#3E6B3A"/>'
               '<text x="376" y="31" font-family="Inter" font-weight="800" font-size="9" fill="#FFFFFF" text-anchor="middle">FARM YEAR</text>'
               '<circle cx="350" cy="16" r="3" fill="#7E5532"/><circle cx="402" cy="16" r="3" fill="#7E5532"/>')
        for i, (lab, col) in enumerate([("WINTER", "#CFE3F2"), ("SPRING", "#CDE8C2"), ("SUMMER", "#FCE7A2"), ("HARVEST", "#F6C9A0")]):
            x = 330 + (i % 2) * 48; y = 42 + (i // 2) * 41
            cal += f'<rect x="{x}" y="{y}" width="44" height="37" rx="3" fill="{col}"/><text x="{x+22}" y="{y+33}" font-family="Inter" font-weight="800" font-size="6.5" fill="#3A2E22" text-anchor="middle">{lab}</text>'
        cal += ('<path d="M352 50 L352 68 M344 54 L360 64 M360 54 L344 64" stroke="#5A7FA0" stroke-width="2" stroke-linecap="round"/>'
                '<path d="M400 68 L400 56 M400 60 Q392 52 388 56 Q394 62 400 60 M400 58 Q408 50 412 54 Q406 60 400 58" stroke="#3E7A3A" stroke-width="2" fill="#6FAE5A" stroke-linejoin="round"/>'
                '<circle cx="352" cy="99" r="7" fill="#F2B63D"/>' + ''.join(f'<path d="M{352+11*__import__("math").cos(t*0.785):.1f} {99+11*__import__("math").sin(t*0.785):.1f} L{352+14*__import__("math").cos(t*0.785):.1f} {99+14*__import__("math").sin(t*0.785):.1f}" stroke="#F2B63D" stroke-width="2" stroke-linecap="round"/>' for t in range(8))
                + '<ellipse cx="400" cy="101" rx="10" ry="8" fill="#E07B39"/><path d="M394 95 Q394 101 395 108 M400 93 L400 109 M406 95 Q406 101 405 108" stroke="#C0612A" stroke-width="1.2" fill="none"/><rect x="398.5" y="89" width="3" height="5" rx="1" fill="#5A7A2E"/>'
                )
        # corkboard with seed packets and a delivery note, right
        cork = '<rect x="330" y="138" width="96" height="88" rx="4" fill="#C49A62" stroke="#8C6A40" stroke-width="3"/>'
        for x, y, ang, col, ic in [(338, 146, -4, "#F4E4B8", "#E0503A"), (366, 150, 3, "#DDEBC8", "#E07B39"), (394, 146, -2, "#F6D9C9", "#6FAE5A")]:
            cork += (f'<g transform="rotate({ang} {x+12} {y+18})"><rect x="{x}" y="{y}" width="24" height="34" rx="2" fill="{col}"/><circle cx="{x+12}" cy="{y+14}" r="6" fill="{ic}"/>'
                     f'<rect x="{x+4}" y="{y+25}" width="16" height="3" rx="1.5" fill="#6A5A48"/><circle cx="{x+12}" cy="{y+2}" r="2.2" fill="#C8352E"/></g>')
        cork += ('<rect x="344" y="190" width="62" height="30" rx="2" fill="#FFFFFF" transform="rotate(2 375 205)"/><circle cx="375" cy="192" r="2.2" fill="#2F6F9A"/>'
                 '<rect x="350" y="199" width="42" height="3" rx="1.5" fill="#8A929B"/><rect x="350" y="206" width="48" height="3" rx="1.5" fill="#8A929B"/><rect x="350" y="213" width="30" height="3" rx="1.5" fill="#8A929B"/>')
        # hooks with a coiled rope and a hanging lantern, left
        hooks = ('<rect x="14" y="162" width="104" height="8" rx="3" fill="#6E4A2C"/><circle cx="36" cy="172" r="3" fill="#3A3A3A"/><circle cx="92" cy="172" r="3" fill="#3A3A3A"/>'
                 '<ellipse cx="36" cy="198" rx="16" ry="22" fill="none" stroke="#C9A86A" stroke-width="5"/><ellipse cx="36" cy="198" rx="10" ry="15" fill="none" stroke="#B8955A" stroke-width="4"/>'
                 '<path d="M92 174 L92 186" stroke="#3A3A3A" stroke-width="2"/><rect x="82" y="186" width="20" height="5" rx="2" fill="#3A3A3A"/><rect x="84" y="191" width="16" height="24" rx="4" fill="#FCE7A2" stroke="#3A3A3A" stroke-width="2.5"/><rect x="82" y="214" width="20" height="5" rx="2" fill="#3A3A3A"/>')
        desk = (f'<rect x="0" y="292" width="{PW}" height="348" fill="#6B4A2E"/><rect x="0" y="286" width="{PW}" height="8" fill="#8C6440"/><rect x="0" y="294" width="{PW}" height="4" fill="#4A321E"/>'
                # crate of vegetables, left
                '<path d="M14 250 L22 228 Q34 214 44 230 Z" fill="#5E9A3E"/><ellipse cx="34" cy="246" rx="22" ry="17" fill="#E07B39"/><path d="M22 236 Q20 246 24 258 M34 230 L34 262 M46 236 Q48 246 44 258" stroke="#C0612A" stroke-width="1.8" fill="none"/><rect x="32" y="224" width="5" height="9" rx="2" fill="#5A7A2E"/>'
                + ''.join(f'<path d="M{x} 260 L{x+6} 232 L{x+12} 260 Z" fill="#E8792E"/><path d="M{x+6} 232 L{x+2} 220 M{x+6} 232 L{x+6} 218 M{x+6} 232 L{x+10} 220" stroke="#5E9A3E" stroke-width="2.5" stroke-linecap="round"/>' for x in (58, 72))
                + '<circle cx="98" cy="250" r="11" fill="#C8352E"/><circle cx="94" cy="246" r="3" fill="#FFFFFF" opacity="0.35"/><path d="M98 239 L101 234" stroke="#5E9A3E" stroke-width="2.5" stroke-linecap="round"/>'
                '<rect x="8" y="254" width="110" height="34" rx="2" fill="#C9A06A"/><rect x="8" y="254" width="110" height="5" fill="#A87E4C"/><path d="M8 271 L118 271" stroke="#A87E4C" stroke-width="2"/><path d="M30 254 L30 288 M96 254 L96 288" stroke="#A87E4C" stroke-width="2.5"/>'
                # tablet with a planting spreadsheet and a mug, right
                '<rect x="334" y="232" width="92" height="56" rx="6" fill="#23262C"/><rect x="339" y="237" width="82" height="46" rx="2" fill="#F4F7F2"/><rect x="339" y="237" width="82" height="8" fill="' + a + '"/>'
                + ''.join(f'<rect x="{343 + j*20}" y="{249 + i*8}" width="16" height="5" rx="1" fill="{["#CDE8C2", "#E9EEF2", "#FCE7A2"][(i+j) % 3]}"/>' for i in range(4) for j in range(4))
                )
        return f'''<defs><linearGradient id="w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c["wall_top"]}"/><stop offset="1" stop-color="{c["wall_bot"]}"/></linearGradient>
        <radialGradient id="g" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#FFF4D6" stop-opacity="0.35"/><stop offset="1" stop-color="#FFF4D6" stop-opacity="0"/></radialGradient></defs>
        <rect width="{PW}" height="{PH}" fill="url(#w)"/>{planks}<circle cx="220" cy="150" r="170" fill="url(#g)"/>
        {win}{cal}{cork}{hooks}{desk}'''
    if c["room"] == "vet_exam":
        a = c["accent"]
        # window with a tree and a fence, top left
        win = ('<rect x="14" y="18" width="104" height="120" rx="4" fill="#FFFFFF"/><rect x="20" y="24" width="92" height="108" fill="#BFE3F0"/>'
               '<rect x="20" y="100" width="92" height="32" fill="#9BCB8A"/><circle cx="54" cy="70" r="24" fill="#5FA86A"/><circle cx="74" cy="60" r="18" fill="#6FB878"/><rect x="58" y="82" width="7" height="22" fill="#7A5A3C"/>'
               + ''.join(f'<rect x="{x}" y="96" width="5" height="18" fill="#F4F1EA"/>' for x in range(24, 110, 12))
               + '<rect x="20" y="102" width="92" height="3" fill="#F4F1EA"/><path d="M66 24 L66 132 M20 78 L112 78" stroke="#FFFFFF" stroke-width="4"/>')
        # paw-print poster and appointment board, top right
        paws = ''
        for (px, py, s) in [(352, 52, 1.0), (392, 84, 0.8)]:
            paws += (f'<g transform="translate({px} {py}) scale({s})"><ellipse cx="0" cy="8" rx="11" ry="9" fill="{a}"/>'
                     f'<circle cx="-11" cy="-6" r="4.5" fill="{a}"/><circle cx="-4" cy="-12" r="4.5" fill="{a}"/><circle cx="4" cy="-12" r="4.5" fill="{a}"/><circle cx="11" cy="-6" r="4.5" fill="{a}"/></g>')
        poster = (f'<rect x="326" y="20" width="98" height="96" rx="6" fill="#FFF8EC" stroke="#D8CDB8" stroke-width="2"/>{paws}'
                  '<text x="375" y="108" font-family="Inter" font-weight="800" font-size="10" fill="#2B4A48" text-anchor="middle">WELCOME!</text>')
        board = ('<rect x="330" y="132" width="94" height="96" rx="4" fill="#FFFFFF" stroke="#B9CFCB" stroke-width="2"/><rect x="330" y="132" width="94" height="16" rx="4" fill="#2F7E7C"/>'
                 '<text x="377" y="144" font-family="Inter" font-weight="800" font-size="9" fill="#FFFFFF" text-anchor="middle">TODAY</text>')
        for i, (t, col) in enumerate([("9:00", "#8A929B"), ("10:30", a), ("11:15", "#8A929B"), ("2:00", "#8A929B")]):
            y = 160 + i * 17
            board += (f'<text x="338" y="{y+4}" font-family="Inter" font-weight="700" font-size="8" fill="#2B2F3A">{t}</text>'
                      f'<rect x="366" y="{y-3}" width="{48 if i != 1 else 50}" height="8" rx="3" fill="{col}" opacity="{1 if i == 1 else 0.5}"/>')
        board += '<text x="391" y="181" font-family="Inter" font-weight="800" font-size="6.5" fill="#FFFFFF" text-anchor="middle">BISCUIT</text>'
        shelf = ('<rect x="14" y="160" width="104" height="6" rx="2" fill="#B98A5A"/>'
                 '<rect x="20" y="128" width="0" height="0"/>'
                 '<rect x="22" y="140" width="26" height="20" rx="4" fill="#E9F2F1" stroke="#9FB8B4" stroke-width="1.5"/><rect x="22" y="136" width="26" height="6" rx="2" fill="#F28C5A"/>'
                 '<circle cx="30" cy="152" r="3" fill="#B97A4A"/><circle cx="39" cy="150" r="3" fill="#B97A4A"/><circle cx="34" cy="156" r="3" fill="#B97A4A"/>'
                 '<rect x="56" y="138" width="24" height="22" rx="3" fill="#FFFFFF" stroke="#9FB8B4" stroke-width="1.5"/><rect x="60" y="144" width="16" height="3" rx="1" fill="#2F7E7C"/><rect x="60" y="150" width="12" height="3" rx="1" fill="#8A929B"/>'
                 '<path d="M90 160 L90 146 Q90 138 98 138 L104 138 Q112 138 112 146 L112 160 Z" fill="#7FB8D8"/><rect x="94" y="132" width="14" height="8" rx="2" fill="#2F5E7A"/>')
        # beagle "Biscuit" sitting on the exam table, left
        dog = ('<g transform="translate(58 242)">'
               '<ellipse cx="0" cy="26" rx="34" ry="22" fill="#C98A4A"/><ellipse cx="4" cy="20" rx="20" ry="14" fill="#2B211C"/>'
               '<ellipse cx="-6" cy="38" rx="16" ry="10" fill="#FFFFFF"/><rect x="-22" y="34" width="10" height="14" rx="5" fill="#FFFFFF"/><rect x="8" y="34" width="10" height="14" rx="5" fill="#FFFFFF"/>'
               '<path d="M30 20 Q46 4 40 -8" stroke="#C98A4A" stroke-width="7" fill="none" stroke-linecap="round"/><path d="M40 -8 L42 -14" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round"/>'
               '<ellipse cx="-14" cy="-6" rx="22" ry="20" fill="#C98A4A"/><path d="M-14 -24 L-14 6" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round"/>'
               '<ellipse cx="-16" cy="6" rx="14" ry="10" fill="#FFFFFF"/><ellipse cx="-16" cy="0" rx="5" ry="3.5" fill="#2B211C"/>'
               '<path d="M-34 -14 Q-46 6 -36 22 Q-30 12 -28 -8 Z" fill="#8A5A30"/><path d="M6 -14 Q18 6 8 22 Q2 12 0 -8 Z" fill="#8A5A30"/>'
               '<circle cx="-23" cy="-10" r="3.2" fill="#2B211C"/><circle cx="-5" cy="-10" r="3.2" fill="#2B211C"/><circle cx="-22" cy="-11" r="1" fill="#FFFFFF"/><circle cx="-4" cy="-11" r="1" fill="#FFFFFF"/>'
               f'<path d="M-30 14 Q-16 22 -2 14" stroke="{a}" stroke-width="5" fill="none" stroke-linecap="round"/><circle cx="-16" cy="20" r="3.5" fill="#F2C14E"/>'
               '</g>')
        desk = (f'<rect x="0" y="292" width="{PW}" height="348" fill="#B7C4C9"/><rect x="0" y="286" width="{PW}" height="8" fill="#D9E2E5"/><rect x="0" y="294" width="{PW}" height="4" fill="#8E9CA2"/>'
                '<rect x="6" y="276" width="114" height="12" rx="4" fill="#4E8A86"/>'
                # monitor with a SOAP note on the right
                '<rect x="330" y="236" width="96" height="50" rx="5" fill="#1E2328"/><rect x="335" y="241" width="86" height="40" rx="2" fill="#F4F7F8"/>'
                '<text x="341" y="251" font-family="Inter" font-weight="800" font-size="7" fill="#2F7E7C">SOAP</text>'
                '<rect x="341" y="256" width="60" height="3" rx="1.5" fill="#8A929B"/><rect x="341" y="263" width="70" height="3" rx="1.5" fill="#8A929B"/><rect x="341" y="270" width="50" height="3" rx="1.5" fill="#8A929B"/>'
                '<rect x="372" y="286" width="12" height="6" fill="#1E2328"/>'
                # mug
                '<rect x="300" y="262" width="20" height="24" rx="3" fill="#F28C5A"/><path d="M320 268 Q328 270 320 280" stroke="#F28C5A" stroke-width="3" fill="none"/>')
        return f'''<defs><linearGradient id="w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c["wall_top"]}"/><stop offset="1" stop-color="{c["wall_bot"]}"/></linearGradient>
        <radialGradient id="g" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#FFF4D6" stop-opacity="0.3"/><stop offset="1" stop-color="#FFF4D6" stop-opacity="0"/></radialGradient></defs>
        <rect width="{PW}" height="{PH}" fill="url(#w)"/><rect x="0" y="200" width="{PW}" height="8" fill="#FFFFFF" opacity="0.5"/><circle cx="220" cy="140" r="160" fill="url(#g)"/>
        {win}{shelf}{poster}{board}{desk}{dog}'''
    if c["room"] == "interp_booth":
        a = c["accent"]
        # booth glass looking out over a conference hall
        hall = ('<rect x="8" y="16" width="424" height="196" rx="6" fill="#3A332E"/><rect x="16" y="24" width="408" height="180" rx="3" fill="#1F2A36"/>'
                '<rect x="16" y="24" width="408" height="70" fill="#27384A"/><rect x="16" y="94" width="408" height="10" fill="#32475C"/>'
                '<rect x="330" y="36" width="84" height="50" rx="3" fill="#E9EEF2"/><rect x="336" y="42" width="72" height="8" rx="2" fill="' + a + '"/>'
                '<rect x="338" y="56" width="50" height="4" rx="2" fill="#7A8A99"/><rect x="338" y="64" width="62" height="4" rx="2" fill="#7A8A99"/><rect x="338" y="72" width="40" height="4" rx="2" fill="#7A8A99"/>'
                '<rect x="52" y="56" width="30" height="40" rx="2" fill="#6B4A36"/><rect x="48" y="52" width="38" height="7" rx="2" fill="#8A6248"/><circle cx="67" cy="44" r="7" fill="#C9A07C"/><path d="M58 56 Q67 48 76 56 Z" fill="#2F3E66"/>'
                '<path d="M67 52 L67 46" stroke="#AAB4BE" stroke-width="1.5"/>')
        seats = ''
        for r, (y, rr) in enumerate([(118, 9), (142, 10), (168, 11)]):
            for i, x in enumerate(range(24 + r * 8, 424, 26)):
                col = ["#3C4A5A", "#4A3E52", "#3E5048", "#56463C"][(i + r) % 4]
                seats += f'<circle cx="{x}" cy="{y}" r="{rr}" fill="{col}"/><path d="M{x-rr-3} {y+rr+12} Q{x} {y+rr-4} {x+rr+3} {y+rr+12} Z" fill="{col}"/>'
        seats = f'<g clip-path="url(#hallclip)">{seats}</g>'
        glass = ('<path d="M16 24 L120 24 L40 204 L16 204 Z" fill="#FFFFFF" opacity="0.05"/><path d="M380 24 L424 24 L424 90 Z" fill="#FFFFFF" opacity="0.05"/>'
                 '<path d="M220 24 L220 204" stroke="#3A332E" stroke-width="6"/>')
        notes = ''
        for x, y, ang, col, t in [(22, 150, -4, "#FCE7A2", "EN→FR"), (74, 158, 3, "#BFE6E2", "TERMS"), (360, 146, 4, "#F6C9C0", "Q&amp;A")]:
            notes += (f'<g transform="rotate({ang} {x+24} {y+22})"><rect x="{x}" y="{y}" width="48" height="44" fill="{col}"/>'
                      f'<text x="{x+24}" y="{y+15}" font-family="Inter" font-weight="800" font-size="9" fill="#2B2F3A" text-anchor="middle">{t}</text>'
                      f'<rect x="{x+6}" y="{y+22}" width="34" height="3" rx="1.5" fill="#6A6F78"/><rect x="{x+6}" y="{y+29}" width="28" height="3" rx="1.5" fill="#6A6F78"/><rect x="{x+6}" y="{y+36}" width="32" height="3" rx="1.5" fill="#6A6F78"/></g>')
        desk = (f'<rect x="0" y="292" width="{PW}" height="348" fill="#6E5A48"/><rect x="0" y="286" width="{PW}" height="8" fill="#8C735C"/><rect x="0" y="294" width="{PW}" height="4" fill="#4E3F33"/>'
                # interpreter console with channel buttons and a gooseneck mic, left
                '<rect x="10" y="252" width="96" height="36" rx="5" fill="#2A2D33"/><rect x="16" y="258" width="38" height="12" rx="2" fill="#0F2A24"/>'
                f'<text x="35" y="267.5" font-family="Inter" font-weight="800" font-size="8" fill="{a}" text-anchor="middle">CH 2</text>'
                '<circle cx="66" cy="264" r="5" fill="#4A4F58"/><circle cx="82" cy="264" r="5" fill="#4A4F58"/><rect x="60" y="275" width="40" height="8" rx="4" fill="#C8352E"/>'
                '<rect x="16" y="276" width="10" height="7" rx="2" fill="#4A4F58"/><rect x="30" y="276" width="10" height="7" rx="2" fill="#4A4F58"/><rect x="44" y="276" width="10" height="7" rx="2" fill="#4A4F58"/>'
                '<path d="M92 254 C92 228 82 214 100 198" stroke="#2A2D33" stroke-width="4" fill="none"/><rect x="96" y="186" width="10" height="16" rx="4" fill="#2A2D33" transform="rotate(30 101 194)"/>'
                '<circle cx="97" cy="210" r="2.6" fill="#E84A3F"/>'
                # stacked dictionaries, right
                '<rect x="356" y="268" width="76" height="18" rx="2" fill="#2F5E7A"/><rect x="356" y="268" width="6" height="18" fill="#22465C"/><rect x="380" y="274" width="34" height="5" rx="1" fill="#E3C46E"/>'
                '<rect x="362" y="252" width="66" height="16" rx="2" fill="#8E3A2E"/><rect x="362" y="252" width="6" height="16" fill="#6E2A20"/><rect x="384" y="257" width="28" height="5" rx="1" fill="#E3C46E"/>'
                '<rect x="352" y="238" width="72" height="14" rx="2" fill="#3E6A4A"/><rect x="352" y="238" width="6" height="14" fill="#2C4E36"/><rect x="376" y="242" width="30" height="5" rx="1" fill="#E3C46E"/>'
                # water glass
                '<path d="M326 252 L346 252 L343 286 L329 286 Z" fill="#CFE6F0" opacity="0.7"/><path d="M328 264 L344 264 L343 286 L329 286 Z" fill="#9FCDE0" opacity="0.7"/>')
        return f'''<defs><linearGradient id="w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c["wall_top"]}"/><stop offset="1" stop-color="{c["wall_bot"]}"/></linearGradient>
        <clipPath id="hallclip"><rect x="16" y="24" width="408" height="180"/></clipPath>
        <radialGradient id="g" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#FFE6B0" stop-opacity="0.18"/><stop offset="1" stop-color="#FFE6B0" stop-opacity="0"/></radialGradient></defs>
        <rect width="{PW}" height="{PH}" fill="url(#w)"/>
        {hall}{seats}{glass}<circle cx="220" cy="120" r="150" fill="url(#g)"/>{notes}{desk}'''
    if c["room"] == "photo_studio":
        a = c["accent"]
        # seamless paper roll on a crossbar, top left
        roll = ('<path d="M14 18 L186 18" stroke="#15171B" stroke-width="5"/><rect x="18" y="10" width="164" height="18" rx="9" fill="#C9CFD6"/>'
                '<path d="M24 28 L176 28 L176 150 Q100 170 24 150 Z" fill="#B7BEC6"/><path d="M24 28 L176 28 L176 60 L24 60 Z" fill="#A9B0B9" opacity="0.6"/>'
                '<path d="M10 14 L10 290 M190 14 L190 290" stroke="#15171B" stroke-width="5"/>'
                '<path d="M10 290 L-6 300 M10 290 L24 300 M190 290 L174 300 M190 290 L206 300" stroke="#15171B" stroke-width="4"/>')
        # softbox on a stand, right
        soft = ('<path d="M360 30 L430 52 L430 160 L360 182 Z" fill="#101215"/><path d="M366 40 L424 58 L424 154 L366 172 Z" fill="#FFF6E2"/>'
                '<path d="M366 40 L424 58 L424 154 L366 172 Z" fill="url(#sb)"/><rect x="342" y="94" width="20" height="24" rx="3" fill="#2A2D33"/>'
                '<path d="M352 118 L352 284 M352 284 L332 296 M352 284 L372 296 M352 284 L352 298" stroke="#15171B" stroke-width="4"/>')
        # contact sheet with grease-pencil marks, pinned centre-left below roll
        cs = '<rect x="14" y="146" width="106" height="98" rx="2" fill="#F4F1EA" transform="rotate(-2 67 195)"/>'
        tones = ["#6E7A88", "#8A6E5A", "#5E7064", "#9A8A70", "#4E5A6A", "#7C6A7E", "#6A7E70", "#8C7A62", "#5A6676"]
        g = ''
        for i, col in enumerate(tones):
            x, y = 21 + (i % 3) * 32, 154 + (i // 3) * 29
            g += f'<rect x="{x}" y="{y}" width="28" height="22" fill="{col}"/><circle cx="{x+14}" cy="{y+9}" r="4" fill="#E9D8C2" opacity="0.7"/><path d="M{x} {y+22} L{x+8} {y+14} L{x+16} {y+19} L{x+28} {y+10} L{x+28} {y+22} Z" fill="#000" opacity="0.25"/>'
        g += '<ellipse cx="67" cy="194" rx="19" ry="15" fill="none" stroke="#D43A2F" stroke-width="2.5"/><path d="M23 214 L47 234 M47 214 L23 234" stroke="#D43A2F" stroke-width="2.5"/>'
        cs += f'<g transform="rotate(-2 67 195)">{g}</g><circle cx="67" cy="148" r="4" fill="{a}"/>'
        lamp = '<path d="M232 0 L232 22" stroke="#15171B" stroke-width="3"/><path d="M212 42 Q214 22 232 22 Q250 22 252 42 Z" fill="#2F6F7A"/><ellipse cx="232" cy="42" rx="20" ry="4" fill="#FFE6B0"/>'
        desk = (f'<rect x="0" y="292" width="{PW}" height="348" fill="#5C4A3C"/><rect x="0" y="286" width="{PW}" height="8" fill="#7A6250"/><rect x="0" y="294" width="{PW}" height="4" fill="#3E3128"/>'
                # laptop with an edit on screen, right
                '<path d="M318 286 L328 236 L428 236 L420 286 Z" fill="#B8C0C8"/><path d="M323 282 L332 240 L423 240 L415 282 Z" fill="#14161A"/>'
                '<path d="M334 276 L340 248 L392 248 L386 276 Z" fill="#6E8AA0"/><path d="M334 276 L350 260 L362 268 L378 254 L386 276 Z" fill="#3E5A44"/><circle cx="375" cy="254" r="3.5" fill="#F6D58A"/>'
                f'<rect x="396" y="250" width="20" height="3" rx="1.5" fill="{a}"/><rect x="396" y="258" width="16" height="3" rx="1.5" fill="#8A929B"/><rect x="396" y="266" width="18" height="3" rx="1.5" fill="#8A929B"/>'
                '<rect x="310" y="284" width="118" height="6" rx="3" fill="#D3D9DE"/>'
                # lens on the desk, left
                '<rect x="40" y="250" width="34" height="38" rx="5" fill="#1E2025"/><rect x="40" y="256" width="34" height="5" fill="#3A3D44"/><rect x="40" y="268" width="34" height="3" fill="#D43A2F"/>'
                '<ellipse cx="57" cy="250" rx="17" ry="5" fill="#2E3138"/><ellipse cx="57" cy="250" rx="11" ry="3" fill="#4C6A86"/>'
                # SD cards
                '<path d="M92 278 L110 278 L114 282 L114 290 L92 290 Z" fill="#2A5DB0" transform="rotate(-8 103 284)"/><path d="M106 280 L124 280 L128 284 L128 292 L106 292 Z" fill="#D43A2F" transform="rotate(6 117 286)"/>')
        return f'''<defs><linearGradient id="w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c["wall_top"]}"/><stop offset="1" stop-color="{c["wall_bot"]}"/></linearGradient>
        <linearGradient id="sb" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0.6"/><stop offset="1" stop-color="#FFE3A8" stop-opacity="0"/></linearGradient>
        <radialGradient id="g" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#FFE6B0" stop-opacity="0.22"/><stop offset="1" stop-color="#FFE6B0" stop-opacity="0"/></radialGradient></defs>
        <rect width="{PW}" height="{PH}" fill="url(#w)"/><circle cx="232" cy="80" r="150" fill="url(#g)"/>
        {roll}{soft}{cs}{lamp}{desk}'''
    if c["room"] == "community_office":
        a = c["accent"]
        board = ('<rect x="10" y="28" width="168" height="190" rx="5" fill="#7A5A3E"/><rect x="16" y="34" width="156" height="178" rx="3" fill="#C9A57A"/>'
                 '<rect x="40" y="40" width="108" height="18" rx="3" fill="#2F5E4E"/><text x="94" y="53" font-family="Inter" font-weight="800" font-size="10" fill="#FFF4E6" text-anchor="middle" letter-spacing="1.5">RESOURCES</text>')
        flyers = [(24, 66, -3, "#FFFDF4", "#E8735A"), (96, 64, 2, "#DDEBF5", "#3D7DD8"), (22, 140, 3, "#E4F1E0", "#5FA36B"), (98, 138, -2, "#FCE7B2", "#B5843A")]
        for i, (x, y, ang, col, hd) in enumerate(flyers):
            tabs = ''.join(f'<rect x="{x+4+j*9}" y="{y+52}" width="7" height="11" fill="{col}" stroke="#B9A88A" stroke-width="0.6"/>' for j in range(6) if i % 2 == 0 and j != 3)
            board += (f'<g transform="rotate({ang} {x+33} {y+28})"><rect x="{x}" y="{y}" width="66" height="54" fill="{col}" stroke="#B9A88A" stroke-width="0.8"/>'
                      f'<rect x="{x}" y="{y}" width="66" height="12" fill="{hd}"/><rect x="{x+6}" y="{y+18}" width="40" height="4" rx="2" fill="#2B2F3A"/>'
                      f'<rect x="{x+6}" y="{y+27}" width="52" height="3" rx="1.5" fill="#8A929B"/><rect x="{x+6}" y="{y+34}" width="46" height="3" rx="1.5" fill="#8A929B"/><rect x="{x+6}" y="{y+41}" width="30" height="3" rx="1.5" fill="#8A929B"/>{tabs}</g>'
                      f'<circle cx="{x+33}" cy="{y+3}" r="3.2" fill="{["#E8735A", "#2F5E4E", "#3D7DD8", "#E8735A"][i]}"/>')
        win = ('<rect x="300" y="30" width="126" height="130" rx="4" fill="#F8F2EA"/><rect x="306" y="36" width="114" height="118" fill="#BFDDEB"/>'
               '<path d="M306 120 Q340 96 372 112 Q396 100 420 110 L420 154 L306 154 Z" fill="#9CC59A"/><path d="M306 134 Q350 118 420 132 L420 154 L306 154 Z" fill="#7FB07D"/>'
               '<rect x="324" y="96" width="26" height="30" fill="#E9D8C2"/><path d="M320 98 L337 82 L354 98 Z" fill="#C46A4E"/><rect x="333" y="110" width="8" height="16" fill="#8A6A4C"/>'
               '<path d="M363 36 L363 154 M306 95 L420 95" stroke="#F8F2EA" stroke-width="6"/><rect x="296" y="156" width="134" height="8" rx="2" fill="#E9DCCB"/>')
        plant = ('<path d="M398 156 Q382 120 392 100 M404 156 Q404 116 418 102 M400 156 Q410 128 426 124" stroke="#3F7A50" stroke-width="3" fill="none"/>'
                 '<ellipse cx="390" cy="102" rx="9" ry="5" fill="#4E9A62" transform="rotate(-50 390 102)"/><ellipse cx="418" cy="104" rx="9" ry="5" fill="#4E9A62" transform="rotate(30 418 104)"/>'
                 '<ellipse cx="424" cy="124" rx="9" ry="5" fill="#5FAF72" transform="rotate(10 424 124)"/><ellipse cx="386" cy="126" rx="8" ry="4.5" fill="#5FAF72" transform="rotate(-70 386 126)"/>'
                 f'<path d="M388 140 L412 140 L408 160 L392 160 Z" fill="{a}"/>')
        cab = ('<rect x="330" y="186" width="96" height="104" rx="4" fill="#8E9AA6"/><rect x="336" y="192" width="84" height="44" rx="2" fill="#A7B2BC"/><rect x="336" y="242" width="84" height="44" rx="2" fill="#A7B2BC"/>'
               '<rect x="366" y="208" width="24" height="6" rx="3" fill="#5A6470"/><rect x="366" y="258" width="24" height="6" rx="3" fill="#5A6470"/>'
               '<rect x="364" y="196" width="28" height="9" fill="#FFFDF4" stroke="#5A6470" stroke-width="0.8"/><rect x="364" y="246" width="28" height="9" fill="#FFFDF4" stroke="#5A6470" stroke-width="0.8"/>')
        lamp = '<path d="M232 0 L232 26" stroke="#3A2E24" stroke-width="2.5"/><path d="M210 48 Q212 26 232 26 Q252 26 254 48 Z" fill="#2F5E4E"/><ellipse cx="232" cy="48" rx="22" ry="4" fill="#FFE6B0"/>'
        desk = (f'<rect x="0" y="292" width="{PW}" height="348" fill="#A9825E"/><rect x="0" y="286" width="{PW}" height="8" fill="#C49C74"/><rect x="0" y="294" width="{PW}" height="4" fill="#7E5E42"/>'
                '<rect x="10" y="276" width="74" height="10" rx="2" fill="#E8B04A"/><rect x="14" y="266" width="70" height="10" rx="2" fill="#6FA0C8"/><rect x="8" y="256" width="72" height="10" rx="2" fill="#E8735A"/><rect x="12" y="246" width="66" height="10" rx="2" fill="#F4ECDD"/>'
                '<rect x="80" y="244" width="8" height="10" rx="1" fill="#2F5E4E"/>'
                '<rect x="96" y="254" width="22" height="32" rx="5" fill="#F4ECDD"/><path d="M118 262 Q130 263 128 273 Q126 281 118 279" stroke="#F4ECDD" stroke-width="4" fill="none"/>'
                f'<path d="M100 266 Q107 260 114 266" stroke="{a}" stroke-width="3" fill="none"/><path d="M104 246 Q100 240 105 234" stroke="#FFFFFF" stroke-width="2" fill="none" opacity="0.45" stroke-linecap="round"/>')
        return f'''<defs><linearGradient id="w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c["wall_top"]}"/><stop offset="1" stop-color="{c["wall_bot"]}"/></linearGradient>
        <radialGradient id="g" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#FFE6B0" stop-opacity="0.3"/><stop offset="1" stop-color="#FFE6B0" stop-opacity="0"/></radialGradient></defs>
        <rect width="{PW}" height="{PH}" fill="url(#w)"/><circle cx="232" cy="80" r="150" fill="url(#g)"/>
        {board}{win}{plant}{cab}{lamp}{desk}'''
    if c["room"] == "pm_office":
        a = c["accent"]
        cols = [("TO DO", 22), ("DOING", 72), ("DONE", 122)]
        kb = ('<rect x="10" y="26" width="176" height="200" rx="6" fill="#F4F1EA"/><rect x="10" y="26" width="176" height="200" rx="6" fill="none" stroke="#8C8496" stroke-width="3"/>'
              '<path d="M68 40 L68 216 M126 40 L126 216" stroke="#C9C2B6" stroke-width="2"/>')
        for t, x in cols:
            kb += f'<text x="{x+22}" y="46" font-family="Inter" font-weight="800" font-size="9" fill="#3B2E4A" text-anchor="middle" letter-spacing="1">{t}</text>'
        cards = [(18, 56, "#F6D365"), (18, 92, "#9FE2BF"), (18, 128, "#F7A8B8"), (18, 164, "#F6D365"),
                 (76, 56, "#9FC9F2"), (76, 92, "#F6D365"), (134, 56, "#9FE2BF"), (134, 92, "#9FE2BF"), (134, 128, "#9FC9F2")]
        for i, (x, y, col) in enumerate(cards):
            r = (-3, 2, -1, 3, 1, -2, 2, -3, 1)[i]
            kb += (f'<g transform="rotate({r} {x+22} {y+14})"><rect x="{x}" y="{y}" width="44" height="28" rx="2" fill="{col}"/>'
                   f'<rect x="{x+5}" y="{y+7}" width="30" height="3" rx="1.5" fill="#4A3E2A" opacity="0.6"/><rect x="{x+5}" y="{y+14}" width="22" height="3" rx="1.5" fill="#4A3E2A" opacity="0.6"/>'
                   + (f'<path d="M{x+30} {y+20} L{x+34} {y+24} L{x+40} {y+16}" stroke="#2F7A4A" stroke-width="2.5" fill="none" stroke-linecap="round"/>' if x == 134 else '') + '</g>')
        kb += f'<circle cx="88" cy="140" r="7" fill="{a}"/><circle cx="88" cy="140" r="2.5" fill="#3B2E4A"/>'
        gantt = ('<rect x="284" y="30" width="146" height="112" rx="5" fill="#14101C"/><rect x="290" y="36" width="134" height="100" rx="3" fill="#251E33"/>'
                 '<rect x="298" y="44" width="50" height="5" rx="2.5" fill="#C9C2D6"/>'
                 + ''.join(f'<path d="M{x} 56 L{x} 130" stroke="#3A3148" stroke-width="1"/>' for x in range(300, 424, 18)))
        for i, (x, w, col) in enumerate([(300, 40, "#4FB3BF"), (330, 34, "#4FB3BF"), (352, 30, "#9FE2BF"), (370, 26, "#F7A8B8"), (388, 30, a)]):
            y = 62 + i * 13
            gantt += f'<rect x="{x}" y="{y}" width="{w}" height="8" rx="3" fill="{col}"/>'
        gantt += f'<path d="M340 66 L340 74 L352 75" stroke="#C9C2D6" stroke-width="1.5" fill="none"/><path d="M412 122 L418 128 L412 134 L406 128 Z" fill="{a}"/><path d="M404 56 L404 136" stroke="#E5684C" stroke-width="1.5" stroke-dasharray="3 3"/>'
        gantt += '<rect x="352" y="142" width="12" height="14" fill="#14101C"/><rect x="336" y="154" width="44" height="6" rx="3" fill="#14101C"/>'
        cal = ('<rect x="314" y="172" width="96" height="92" rx="4" fill="#F4F1EA"/><rect x="314" y="172" width="96" height="20" rx="4" fill="#E5684C"/>'
               '<text x="362" y="186" font-family="Inter" font-weight="800" font-size="10" fill="#FFFFFF" text-anchor="middle" letter-spacing="1.5">LAUNCH</text>')
        for r in range(4):
            for k in range(6):
                x, y = 320 + k * 15, 198 + r * 16
                cal += f'<rect x="{x}" y="{y}" width="11" height="11" rx="2" fill="{"#E5684C" if (r, k) == (2, 4) else "#DCD5C8"}"/>'
        cal += '<path d="M380 230 L392 244 M392 230 L380 244" stroke="#FFFFFF" stroke-width="0"/><path d="M386 228 L386 212 L398 216 L386 220" stroke="#3B2E4A" stroke-width="2" fill="#F2B84B"/>'
        lamp = '<path d="M232 0 L232 24" stroke="#14101C" stroke-width="3"/><path d="M212 44 Q214 24 232 24 Q250 24 252 44 Z" fill="#7A5C8E"/><ellipse cx="232" cy="44" rx="20" ry="4" fill="#FFE3A3"/>'
        desk = (f'<rect x="0" y="292" width="{PW}" height="348" fill="#B89C74"/><rect x="0" y="286" width="{PW}" height="8" fill="#D2B98E"/><rect x="0" y="294" width="{PW}" height="4" fill="#8E7454"/>'
                '<path d="M330 286 L340 246 L420 246 L412 286 Z" fill="#B8C0C8"/><path d="M335 282 L344 250 L415 250 L407 282 Z" fill="#251E33"/>'
                '<rect x="348" y="258" width="22" height="4" rx="2" fill="#4FB3BF"/><rect x="356" y="266" width="28" height="4" rx="2" fill="#9FE2BF"/><rect x="368" y="274" width="30" height="4" rx="2" fill="#F2B84B"/>'
                '<rect x="322" y="284" width="100" height="6" rx="3" fill="#D3D9DE"/>'
                f'<rect x="36" y="252" width="28" height="34" rx="5" fill="#F4F1EA"/><path d="M64 260 Q78 262 76 272 Q74 280 64 278" stroke="#F4F1EA" stroke-width="5" fill="none"/><rect x="36" y="262" width="28" height="8" fill="{c["outfit"]}"/>'
                '<path d="M50 242 Q44 234 50 226" stroke="#FFFFFF" stroke-width="2" fill="none" opacity="0.4" stroke-linecap="round"/>'
                '<rect x="86" y="270" width="54" height="16" rx="3" fill="#F4F1EA" transform="rotate(-4 113 278)"/><rect x="90" y="266" width="54" height="14" rx="3" fill="#E9A23B" transform="rotate(3 117 273)"/>')
        return f'''<defs><linearGradient id="w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c["wall_top"]}"/><stop offset="1" stop-color="{c["wall_bot"]}"/></linearGradient>
        <radialGradient id="g" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#FFE3A3" stop-opacity="0.26"/><stop offset="1" stop-color="#FFE3A3" stop-opacity="0"/></radialGradient></defs>
        <rect width="{PW}" height="{PH}" fill="url(#w)"/><circle cx="232" cy="74" r="140" fill="url(#g)"/>
        {kb}{gantt}{cal}{lamp}{desk}'''
    if c["room"] == "library_nook":
        books = ''
        cols = ["#C8553D", "#F2B84B", "#3D7DD8", "#E9E2D0", "#8AB17D", "#7A3E5C", "#2B2F3A", "#E07A5F", "#5FA3A3"]
        for si, y in enumerate((96, 172, 248)):
            x, k = 18, si * 3
            while x < 150:
                w = 9 + (k * 5) % 8; h = 50 + (k * 7) % 18; lean = 8 if (k % 7 == 5) else 0
                col = cols[k % len(cols)]
                books += f'<rect x="{x}" y="{y-h}" width="{w}" height="{h}" rx="1.5" fill="{col}" transform="rotate({lean} {x+w} {y})"/><rect x="{x+2}" y="{y-h+8}" width="{w-4}" height="3" fill="#FFFFFF" opacity="0.35" transform="rotate({lean} {x+w} {y})"/>'
                x += w + 2 + (6 if lean else 0); k += 1
        shelf = ('<rect x="8" y="20" width="166" height="268" rx="4" fill="#5A3B28"/><rect x="14" y="26" width="154" height="256" fill="#3A2618"/>'
                 + ''.join(f'<rect x="10" y="{y}" width="162" height="8" rx="2" fill="#7A5236"/>' for y in (96, 172, 248)) + books)
        board = ('<rect x="290" y="30" width="138" height="150" rx="5" fill="#8A5A3C"/><rect x="296" y="36" width="126" height="138" rx="3" fill="#C9A57A"/>'
                 '<rect x="318" y="42" width="82" height="16" rx="3" fill="#2B2F3A"/><text x="359" y="54" font-family="Inter" font-weight="800" font-size="10" fill="#F2B84B" text-anchor="middle" letter-spacing="1.5">JOBS BOARD</text>')
        for i, (x, y, ang, col) in enumerate([(302, 66, -4, "#FFFDF4"), (362, 64, 3, "#FCE7B2"), (304, 120, 2, "#DDEFE4"), (364, 118, -3, "#FFFDF4")]):
            tabs = ''.join(f'<rect x="{x+3+j*9}" y="{y+40}" width="7" height="12" fill="{col}" stroke="#B9A88A" stroke-width="0.6"/>' for j in range(6) if not (i == 1 and j == 2))
            board += (f'<g transform="rotate({ang} {x+27} {y+24})"><rect x="{x}" y="{y}" width="56" height="40" fill="{col}" stroke="#B9A88A" stroke-width="0.8"/>'
                      f'<rect x="{x+6}" y="{y+6}" width="30" height="5" rx="2" fill="#2B2F3A"/><rect x="{x+6}" y="{y+16}" width="42" height="3" rx="1.5" fill="#8A929B"/>'
                      f'<rect x="{x+6}" y="{y+23}" width="36" height="3" rx="1.5" fill="#8A929B"/><rect x="{x+6}" y="{y+30}" width="16" height="5" rx="2" fill="{["#C8553D", "#3D7DD8", "#5FA36B", "#7A3E5C"][i]}"/>{tabs}</g>'
                      f'<circle cx="{x+28}" cy="{y+3}" r="3" fill="#C8553D"/>')
        lamp = ('<path d="M232 0 L232 30" stroke="#1A2A24" stroke-width="2.5"/><path d="M208 52 Q210 30 232 30 Q254 30 256 52 Z" fill="#2F6F5A"/>'
                '<ellipse cx="232" cy="52" rx="24" ry="4" fill="#FFE7A8"/>')
        clock = ('<circle cx="392" cy="214" r="24" fill="#F4F1E6" stroke="#2B2F3A" stroke-width="4"/>'
                 '<path d="M392 214 L392 199 M392 214 L402 220" stroke="#2B2F3A" stroke-width="3" stroke-linecap="round"/><circle cx="392" cy="214" r="2.5" fill="#C8553D"/>')
        desk = (f'<rect x="0" y="292" width="{PW}" height="348" fill="#8A6244"/><rect x="0" y="286" width="{PW}" height="8" fill="#A87C58"/><rect x="0" y="294" width="{PW}" height="4" fill="#5E4230"/>'
                '<rect x="8" y="268" width="62" height="10" rx="2" fill="#3D7DD8"/><rect x="12" y="258" width="54" height="10" rx="2" fill="#E9E2D0"/><rect x="6" y="278" width="68" height="10" rx="2" fill="#C8553D"/>'
                '<rect x="74" y="256" width="20" height="30" rx="4" fill="#F4F1E6"/><path d="M74 262 Q65 262 66 271 Q67 279 74 278" stroke="#F4F1E6" stroke-width="3.5" fill="none"/>'
                '<rect x="74" y="262" width="20" height="7" fill="#7FA38A"/><path d="M80 250 Q77 244 82 238 M88 250 Q85 244 90 238" stroke="#FFFFFF" stroke-width="2" fill="none" opacity="0.5" stroke-linecap="round"/>'
                '<path d="M332 286 L344 244 L422 244 L414 286 Z" fill="#B8C0C8"/><path d="M337 282 L347 248 L417 248 L410 282 Z" fill="#F7F7F4"/>'
                '<rect x="352" y="254" width="12" height="12" rx="2" fill="#7A3E5C"/><rect x="368" y="255" width="30" height="4" rx="2" fill="#2B2F3A"/><rect x="368" y="262" width="22" height="2.5" rx="1" fill="#8A929B"/>'
                '<rect x="350" y="270" width="52" height="2.5" rx="1" fill="#8A929B"/><rect x="349" y="276" width="44" height="2.5" rx="1" fill="#8A929B"/>'
                '<rect x="324" y="284" width="98" height="6" rx="3" fill="#D3D9DE"/>')
        return f'''<defs><linearGradient id="w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c["wall_top"]}"/><stop offset="1" stop-color="{c["wall_bot"]}"/></linearGradient>
        <radialGradient id="g" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#FFE7A8" stop-opacity="0.32"/><stop offset="1" stop-color="#FFE7A8" stop-opacity="0"/></radialGradient></defs>
        <rect width="{PW}" height="{PH}" fill="url(#w)"/><circle cx="232" cy="90" r="150" fill="url(#g)"/>
        {shelf}{board}{clock}{lamp}{desk}'''
    if c["room"] == "data_desk":
        a = c["accent"]
        scr = ('<rect x="14" y="34" width="176" height="118" rx="6" fill="#0A1418"/><rect x="20" y="40" width="164" height="104" rx="3" fill="#13262E"/>'
               '<rect x="28" y="48" width="44" height="5" rx="2.5" fill="#9FC9D6"/><rect x="28" y="58" width="28" height="3" rx="1.5" fill="#4E6F7A"/>')
        for i, h in enumerate([34, 46, 40, 58, 52, 30, 44]):
            scr += f'<rect x="{30 + i*14}" y="{132 - h}" width="9" height="{h}" rx="1.5" fill="{"#E5684C" if i == 5 else "#4FB3BF"}"/>'
        scr += f'<path d="M132 120 L144 104 L156 110 L168 86 L178 92" stroke="{a}" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
        scr += ''.join(f'<circle cx="{x}" cy="{y}" r="2.5" fill="{a}"/>' for x, y in [(132, 120), (144, 104), (156, 110), (168, 86), (178, 92)])
        scr += '<rect x="132" y="50" width="44" height="22" rx="3" fill="#1D3640"/><rect x="137" y="55" width="20" height="4" rx="2" fill="#9FC9D6"/><rect x="137" y="63" width="30" height="5" rx="2" fill="#7EE0A1"/>'
        scr += '<rect x="96" y="152" width="12" height="16" fill="#0A1418"/><rect x="80" y="166" width="44" height="6" rx="3" fill="#0A1418"/>'
        wb = ('<rect x="290" y="30" width="138" height="112" rx="5" fill="#E9EEF0"/><rect x="290" y="30" width="138" height="112" rx="5" fill="none" stroke="#9AA9B2" stroke-width="3"/>'
              '<path d="M304 50 L360 50 L352 64 L312 64 Z M314 70 L350 70 L344 84 L320 84 Z M322 90 L342 90 L338 104 L326 104 Z" fill="#4FB3BF" opacity="0.85"/>'
              '<text x="372" y="62" font-family="Inter" font-weight="700" font-size="11" fill="#2B3A44">visit</text>'
              '<text x="364" y="82" font-family="Inter" font-weight="700" font-size="11" fill="#2B3A44">form</text>'
              '<text x="352" y="102" font-family="Inter" font-weight="700" font-size="11" fill="#E5684C">sign-up ?</text>'
              '<path d="M304 120 L412 120 M304 130 L380 130" stroke="#7A8A94" stroke-width="2.5" stroke-linecap="round"/>'
              '<rect x="290" y="142" width="138" height="5" fill="#9AA9B2"/>')
        notes = ''.join(f'<rect x="{x}" y="{y}" width="30" height="30" fill="{col}" transform="rotate({r} {x+15} {y+15})"/><path d="M{x+5} {y+11} L{x+24} {y+11} M{x+5} {y+18} L{x+20} {y+18}" stroke="#5A4A2A" stroke-width="2" opacity="0.6" transform="rotate({r} {x+15} {y+15})"/>' for x, y, col, r in [(316, 170, "#F6D365", -4), (354, 176, "#9FE2BF", 3), (392, 168, "#F7A8B8", -2)])
        lamp = '<path d="M232 0 L232 20" stroke="#0A1418" stroke-width="3"/><path d="M210 40 L218 20 L246 20 L254 40 Z" fill="#2F4F5A"/><ellipse cx="232" cy="41" rx="22" ry="4" fill="#FFE3A3"/>'
        desk = (f'<rect x="0" y="292" width="{PW}" height="348" fill="#3A4A52"/><rect x="0" y="286" width="{PW}" height="8" fill="#5C6F78"/><rect x="0" y="294" width="{PW}" height="4" fill="#26333A"/>'
                '<path d="M326 286 L336 244 L418 244 L410 286 Z" fill="#B8C0C8"/><path d="M331 282 L340 248 L413 248 L405 282 Z" fill="#13262E"/>'
                '<rect x="346" y="256" width="40" height="4" rx="2" fill="#7EE0A1"/><rect x="344" y="264" width="52" height="3" rx="1.5" fill="#4FB3BF"/><rect x="342" y="271" width="34" height="3" rx="1.5" fill="#9FC9D6"/>'
                '<rect x="318" y="284" width="100" height="6" rx="3" fill="#D3D9DE"/>'
                f'<rect x="34" y="250" width="30" height="36" rx="5" fill="{a}"/><path d="M64 258 Q78 260 76 272 Q74 280 64 278" stroke="{a}" stroke-width="5" fill="none"/><ellipse cx="49" cy="252" rx="13" ry="3" fill="#5A3A22"/>'
                '<path d="M52 240 Q46 232 52 224 M44 240 Q38 232 44 224" stroke="#FFFFFF" stroke-width="2" fill="none" opacity="0.4" stroke-linecap="round"/>'
                '<path d="M96 286 L92 262 L118 262 L114 286 Z" fill="#D9D3C6"/><path d="M105 262 Q92 236 82 234 Q92 250 102 262 M105 262 Q108 230 118 218 Q116 244 108 262 M105 262 Q124 244 134 246 Q120 256 110 262" fill="#5FA36B"/>')
        return f'''<defs><linearGradient id="w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c["wall_top"]}"/><stop offset="1" stop-color="{c["wall_bot"]}"/></linearGradient>
        <radialGradient id="g" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#FFE3A3" stop-opacity="0.28"/><stop offset="1" stop-color="#FFE3A3" stop-opacity="0"/></radialGradient></defs>
        <rect width="{PW}" height="{PH}" fill="url(#w)"/><circle cx="232" cy="70" r="140" fill="url(#g)"/>
        {scr}{wb}{notes}{lamp}{desk}'''
    if c["room"] == "kitchen":
        tiles = ''.join(f'<rect x="{x + (14 if (y//20) % 2 else 0)}" y="{y}" width="26" height="18" rx="2" fill="#FFFFFF" opacity="0.55"/>' for y in range(0, 290, 20) for x in range(-14, 440, 28))
        rail = '<rect x="12" y="38" width="168" height="6" rx="3" fill="#8A929B"/>'
        pans = ''
        for x, r, col in [(40, 22, "#B8BEC5"), (98, 28, "#2B2F36"), (154, 18, "#C98A4B")]:
            pans += (f'<path d="M{x} 44 L{x} 58" stroke="#5A626C" stroke-width="2.5"/><rect x="{x-3}" y="56" width="6" height="34" rx="3" fill="#3D4652"/>'
                     f'<circle cx="{x}" cy="{90+r}" r="{r}" fill="{col}"/><circle cx="{x}" cy="{90+r}" r="{r-5}" fill="#000000" opacity="0.12"/>'
                     f'<path d="M{x-r*0.5:.0f} {90+r*0.5:.0f} Q{x} {90+r*0.2:.0f} {x+r*0.4:.0f} {90+r*0.45:.0f}" stroke="#FFFFFF" stroke-width="2.5" fill="none" opacity="0.4" stroke-linecap="round"/>')
        shelf = '<rect x="12" y="196" width="150" height="7" rx="2" fill="#9AA3AD"/>'
        for i, (col, lid) in enumerate([("#E9C46A", "#C8352E"), ("#F4A261", "#2B2F36"), ("#8AB17D", "#C8352E"), ("#E76F51", "#2B2F36"), ("#F1E3C8", "#C8352E")]):
            x = 18 + i * 29
            shelf += f'<rect x="{x}" y="164" width="24" height="32" rx="4" fill="#FFFFFF" opacity="0.85"/><rect x="{x+3}" y="174" width="18" height="20" rx="2" fill="{col}"/><rect x="{x-1}" y="160" width="26" height="7" rx="2" fill="{lid}"/>'
        tickets = '<rect x="292" y="36" width="140" height="7" rx="3" fill="#8A929B"/>'
        for i, ang in enumerate([-3, 2, -2, 4]):
            x = 298 + i * 34
            tickets += (f'<g transform="rotate({ang} {x+14} 44)"><rect x="{x}" y="42" width="28" height="56" fill="#FFFDF4" stroke="#D6CFBF" stroke-width="1"/>'
                        f'<rect x="{x+4}" y="50" width="18" height="3" rx="1.5" fill="#3D3552"/><rect x="{x+4}" y="58" width="14" height="2.5" rx="1" fill="#9AA6B2"/>'
                        f'<rect x="{x+4}" y="64" width="20" height="2.5" rx="1" fill="#9AA6B2"/><rect x="{x+4}" y="70" width="12" height="2.5" rx="1" fill="#9AA6B2"/>'
                        f'<rect x="{x+4}" y="82" width="10" height="5" rx="2" fill="{"#C8352E" if i % 2 else "#2A9D8F"}"/></g>')
        board = ('<rect x="300" y="128" width="128" height="96" rx="5" fill="#2B2F36"/><rect x="306" y="134" width="116" height="84" rx="3" fill="#353B44"/>'
                 '<text x="364" y="154" font-family="Inter" font-weight="800" font-size="12" fill="#F4F1EA" text-anchor="middle">SPECIALS</text>'
                 '<path d="M318 166 L404 166 M318 180 L392 180 M318 194 L408 194 M318 208 L384 208" stroke="#F4F1EA" stroke-width="2.5" opacity="0.55" stroke-linecap="round"/>'
                 '<circle cx="410" cy="180" r="4" fill="#F4A261"/>')
        lamp = '<path d="M232 0 L232 22" stroke="#5A626C" stroke-width="3"/><path d="M206 44 L216 22 L248 22 L258 44 Z" fill="#C8352E"/><ellipse cx="232" cy="45" rx="26" ry="4" fill="#FFD27A"/>'
        counter = (f'<rect x="0" y="292" width="{PW}" height="348" fill="#7D858E"/><rect x="0" y="284" width="{PW}" height="10" rx="2" fill="#C9CFD5"/><rect x="0" y="294" width="{PW}" height="4" fill="#5C646C"/>'
                   '<rect x="18" y="268" width="96" height="18" rx="4" fill="#C9965E"/><rect x="18" y="268" width="96" height="5" rx="2" fill="#DDB07A"/>'
                   '<ellipse cx="54" cy="258" rx="22" ry="14" fill="#E9A23B"/><path d="M36 254 Q54 246 72 254" stroke="#C47F1E" stroke-width="2" fill="none"/><path d="M54 244 Q52 236 58 232" stroke="#5FA36B" stroke-width="3" fill="none" stroke-linecap="round"/>'
                   '<path d="M84 262 L110 252" stroke="#B8BEC5" stroke-width="5" stroke-linecap="round"/><path d="M76 265 L86 261" stroke="#2B2F36" stroke-width="6" stroke-linecap="round"/>'
                   '<rect x="342" y="240" width="70" height="46" rx="6" fill="#2B2F36" transform="rotate(-6 377 263)"/><rect x="347" y="245" width="60" height="36" rx="3" fill="#F4F8FA" transform="rotate(-6 377 263)"/>'
                   '<g transform="rotate(-6 377 263)"><rect x="353" y="251" width="26" height="4" rx="2" fill="#3D4652"/><rect x="353" y="260" width="44" height="3" rx="1.5" fill="#9AA6B2"/><rect x="353" y="268" width="36" height="3" rx="1.5" fill="#9AA6B2"/><rect x="385" y="250" width="16" height="7" rx="3" fill="#C8352E"/></g>')
        return f'''<defs><linearGradient id="w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c["wall_top"]}"/><stop offset="1" stop-color="{c["wall_bot"]}"/></linearGradient>
        <radialGradient id="g" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#FFD27A" stop-opacity="0.35"/><stop offset="1" stop-color="#FFD27A" stop-opacity="0"/></radialGradient></defs>
        <rect width="{PW}" height="{PH}" fill="url(#w)"/>{tiles}<circle cx="232" cy="80" r="120" fill="url(#g)"/>
        {rail}{pans}{shelf}{tickets}{board}{lamp}{counter}'''
    if c["room"] == "home_studio":
        win = ('<rect x="18" y="40" width="140" height="150" rx="6" fill="#0F1E24"/>'
               '<defs><linearGradient id="dusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F6B26B"/><stop offset="0.6" stop-color="#E9806E"/><stop offset="1" stop-color="#6A5A8C"/></linearGradient></defs>'
               '<rect x="26" y="48" width="124" height="134" rx="3" fill="url(#dusk)"/>'
               '<path d="M26 150 L48 132 L66 144 L92 120 L118 140 L150 124 L150 182 L26 182 Z" fill="#4B3F6B" opacity="0.8"/>'
               '<circle cx="118" cy="82" r="14" fill="#FFE3A3" opacity="0.9"/>'
               '<rect x="85" y="48" width="5" height="134" fill="#0F1E24"/><rect x="26" y="112" width="124" height="5" fill="#0F1E24"/>'
               '<rect x="12" y="188" width="152" height="9" rx="3" fill="#C9A77A"/>')
        plant = ('<path d="M44 188 L40 160 L72 160 L68 188 Z" fill="#D8734C"/>'
                 '<path d="M56 160 Q40 130 26 128 Q38 146 54 160 M56 160 Q58 124 70 108 Q68 136 60 160 M56 160 Q80 136 96 138 Q78 150 62 160" fill="#5FA36B"/>'
                 '<rect x="112" y="166" width="22" height="22" rx="4" fill="#F2E6CF"/><path d="M134 172 Q144 172 142 180 Q140 186 134 184" stroke="#F2E6CF" stroke-width="3" fill="none"/>')
        board = '<rect x="292" y="34" width="136" height="104" rx="5" fill="#C9A77A"/><rect x="298" y="40" width="124" height="92" rx="3" fill="#D9BC92"/>'
        board += ('<rect x="306" y="48" width="40" height="32" fill="#FFFFFF" transform="rotate(-5 326 64)"/><path d="M312 72 Q320 54 330 66 Q336 58 340 72" stroke="#3D5A80" stroke-width="2" fill="none" transform="rotate(-5 326 64)"/>'
                  '<rect x="354" y="46" width="34" height="34" fill="#F4C95D" transform="rotate(4 371 63)"/><path d="M360 56 L382 56 M360 63 L378 63 M360 70 L380 70" stroke="#6B5B2E" stroke-width="2" transform="rotate(4 371 63)"/>'
                  '<rect x="394" y="50" width="22" height="26" fill="#9FD3C7" transform="rotate(-3 405 63)"/>'
                  '<rect x="306" y="90" width="52" height="36" fill="#FFFFFF" transform="rotate(3 332 108)"/><circle cx="320" cy="106" r="7" fill="#E9806E" transform="rotate(3 332 108)"/><path d="M332 116 L348 98" stroke="#2B2F3A" stroke-width="2" transform="rotate(3 332 108)"/>'
                  '<rect x="368" y="90" width="48" height="36" fill="#F2E6CF" transform="rotate(-4 392 108)"/><path d="M374 100 L410 100 M374 108 L404 108 M374 116 L408 116" stroke="#8E7C64" stroke-width="2" transform="rotate(-4 392 108)"/>')
        board += ''.join(f'<circle cx="{x}" cy="{y}" r="3" fill="{col}"/>' for x, y, col in [(326, 48, "#E0453A"), (371, 46, "#3D7DD8"), (405, 50, "#E0453A"), (332, 90, "#3D7DD8"), (392, 90, "#F4C95D")])
        cal = ('<rect x="330" y="154" width="92" height="84" rx="4" fill="#F7F3EA"/><rect x="330" y="154" width="92" height="18" rx="4" fill="#E9806E"/><rect x="330" y="166" width="92" height="6" fill="#E9806E"/>'
               + ''.join(f'<rect x="{336+i*12}" y="{178+j*12}" width="9" height="9" rx="1.5" fill="{"#5FA36B" if (i+j*7) in (3, 9, 16, 24) else "#DDD5C6"}"/>' for i in range(7) for j in range(5)))
        lamp = '<path d="M232 0 L232 26" stroke="#0F1E24" stroke-width="2"/><path d="M212 44 Q232 18 252 44 Z" fill="#F4C95D"/><ellipse cx="232" cy="45" rx="9" ry="3" fill="#FFF1C8"/>'
        laptop = ('<path d="M332 286 L344 246 L420 246 L412 286 Z" fill="#B8C0C8"/><path d="M337 282 L347 250 L415 250 L408 282 Z" fill="#26323A"/>'
                  '<rect x="352" y="258" width="32" height="4" rx="2" fill="#9FD3C7"/><rect x="350" y="267" width="44" height="3" rx="1.5" fill="#8A99A6"/><rect x="348" y="274" width="38" height="3" rx="1.5" fill="#8A99A6"/>'
                  '<circle cx="404" cy="258" r="4" fill="#F4C95D"/><rect x="324" y="284" width="96" height="6" rx="3" fill="#D3D9DE"/>')
        tablet = ('<rect x="22" y="262" width="84" height="26" rx="5" fill="#2B2F3A" transform="rotate(-4 64 275)"/><rect x="28" y="266" width="66" height="18" rx="2" fill="#3E4A55" transform="rotate(-4 64 275)"/>'
                  '<path d="M40 280 Q56 268 70 276 Q78 270 88 272" stroke="#F4C95D" stroke-width="2" fill="none" transform="rotate(-4 64 275)"/>'
                  '<path d="M100 286 L124 252" stroke="#E9EDF1" stroke-width="4" stroke-linecap="round"/>')
        return f'''<defs><linearGradient id="w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c["wall_top"]}"/><stop offset="1" stop-color="{c["wall_bot"]}"/></linearGradient>
        <radialGradient id="g" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#FFE3A3" stop-opacity="0.35"/><stop offset="1" stop-color="#FFE3A3" stop-opacity="0"/></radialGradient></defs>
        <rect width="{PW}" height="{PH}" fill="url(#w)"/><circle cx="232" cy="60" r="140" fill="url(#g)"/>
        {win}{plant}{board}{cal}{lamp}
        <rect x="0" y="292" width="{PW}" height="348" fill="#7A5B3E"/><rect x="0" y="286" width="{PW}" height="8" fill="#9C7A55"/><rect x="0" y="294" width="{PW}" height="4" fill="#5A4230"/>
        {tablet}{laptop}'''
    if c["room"] == "workshop":
        board = '<rect x="10" y="30" width="150" height="190" rx="4" fill="#C9A77A"/>' + ''.join(f'<circle cx="{x}" cy="{y}" r="1.8" fill="#8E6E48"/>' for x in range(22, 156, 14) for y in range(42, 216, 14))
        tools = ('<path d="M34 60 L34 120" stroke="#E0453A" stroke-width="9" stroke-linecap="round"/><path d="M34 120 L34 158" stroke="#9AA3AD" stroke-width="3.5"/>'
                 '<path d="M58 60 L58 116" stroke="#F2C230" stroke-width="9" stroke-linecap="round"/><path d="M58 116 L58 150" stroke="#9AA3AD" stroke-width="3.5"/>'
                 '<path d="M90 62 L84 112 Q82 124 90 126 M108 62 L114 112 Q116 124 108 126" stroke="#E0453A" stroke-width="8" fill="none" stroke-linecap="round"/>'
                 '<path d="M90 126 L98 150 L108 126" stroke="#7D8690" stroke-width="5" fill="none" stroke-linejoin="round"/><circle cx="99" cy="130" r="3" fill="#5A626C"/>'
                 '<rect x="124" y="58" width="26" height="44" rx="5" fill="#F2C230"/><rect x="128" y="64" width="18" height="12" rx="2" fill="#2B3A2E"/>'
                 '<circle cx="132" cy="88" r="3" fill="#2B2F3A"/><circle cx="142" cy="88" r="3" fill="#E0453A"/><path d="M132 102 Q128 130 120 150 M142 102 Q146 130 152 150" stroke="#2B2F3A" stroke-width="2.5" fill="none"/>'
                 '<circle cx="48" cy="190" r="20" fill="none" stroke="#3D4652" stroke-width="7"/><circle cx="48" cy="190" r="8" fill="#C9A77A" stroke="#3D4652" stroke-width="3"/>'
                 '<rect x="88" y="172" width="58" height="36" rx="6" fill="#E9EDF1" stroke="#7D8690" stroke-width="2"/><path d="M96 184 L138 184 M96 194 L130 194" stroke="#9AA3AD" stroke-width="3" stroke-linecap="round"/>')
        def reel(cx, cy, col):
            return (f'<circle cx="{cx}" cy="{cy}" r="30" fill="#3D4652"/><circle cx="{cx}" cy="{cy}" r="25" fill="{col}"/>'
                    + ''.join(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#000000" stroke-width="1" opacity="0.18"/>' for r in (21, 17, 13))
                    + f'<circle cx="{cx}" cy="{cy}" r="8" fill="#D7DCE2"/><circle cx="{cx}" cy="{cy}" r="3" fill="#3D4652"/>')
        shelf = ('<rect x="300" y="128" width="136" height="8" rx="2" fill="#7A5B3E"/>'
                 '<path d="M318 128 Q318 96 346 94 Q374 96 374 128 Z" fill="#F2C230"/><rect x="310" y="122" width="72" height="8" rx="4" fill="#E0B020"/><path d="M346 94 L346 126" stroke="#E0B020" stroke-width="5"/>'
                 '<rect x="392" y="96" width="34" height="32" rx="3" fill="#E07B39"/><rect x="392" y="104" width="34" height="6" fill="#BF6328"/>'
                 '<rect x="300" y="214" width="136" height="8" rx="2" fill="#7A5B3E"/>')
        van = ('<rect x="320" y="24" width="102" height="58" rx="4" fill="#FFFFFF" stroke="#9AA3AD" stroke-width="2"/>'
               '<path d="M332 40 L370 40 M332 52 L362 52 M332 64 L374 64" stroke="#9AA3AD" stroke-width="3" stroke-linecap="round"/>'
               '<rect x="384" y="34" width="28" height="18" rx="3" fill="#F2C230"/><rect x="384" y="58" width="28" height="16" rx="3" fill="#56B4E9"/>')
        return f'''<defs><linearGradient id="w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c["wall_top"]}"/><stop offset="1" stop-color="{c["wall_bot"]}"/></linearGradient></defs>
        <rect width="{PW}" height="{PH}" fill="url(#w)"/>
        {board}{tools}{van}{shelf}{reel(334, 182, "#E0453A")}{reel(398, 182, "#3D7DD8")}
        <rect x="0" y="292" width="{PW}" height="348" fill="#5A4632"/><rect x="0" y="284" width="{PW}" height="10" rx="2" fill="#9C7A55"/><rect x="0" y="294" width="{PW}" height="5" fill="#3F3022"/>
        <rect x="20" y="246" width="70" height="38" rx="6" fill="#E0453A"/><rect x="30" y="236" width="50" height="12" rx="5" fill="none" stroke="#2B2F3A" stroke-width="5"/><rect x="20" y="258" width="70" height="5" fill="#B8352C"/>
        <rect x="348" y="244" width="70" height="44" rx="6" fill="#2B2F3A" transform="rotate(-6 383 266)"/><rect x="353" y="249" width="60" height="34" rx="3" fill="#F4F8FA" transform="rotate(-6 383 266)"/>
        <g transform="rotate(-6 383 266)"><rect x="359" y="255" width="26" height="4" rx="2" fill="#3D4652"/><rect x="359" y="264" width="44" height="3" rx="1.5" fill="#9AA6B2"/><rect x="359" y="272" width="36" height="3" rx="1.5" fill="#9AA6B2"/><rect x="391" y="254" width="16" height="7" rx="3" fill="#F2C230"/></g>'''
    if c["room"] == "pharmacy":
        cols = ["#F2B63D", "#E07A5F", "#81B29A", "#3D85C6", "#F4F1DE", "#B388EB", "#56CCF2"]
        def shelf(x0, x1, ys, seed):
            out = ''
            for j, y in enumerate(ys):
                out += f'<rect x="{x0-4}" y="{y}" width="{x1-x0+8}" height="7" rx="2" fill="#B8977A"/>'
                x, k = x0, 0
                while True:
                    w = 14 + ((k * 7 + j * 5 + seed) % 4) * 5; h = 24 + ((k * 3 + j + seed) % 3) * 8
                    if x + w > x1: break
                    col = cols[(k + j * 2 + seed) % len(cols)]
                    out += f'<rect x="{x}" y="{y-h}" width="{w}" height="{h}" rx="2" fill="{col}"/><rect x="{x+3}" y="{y-h+6}" width="{w-6}" height="4" rx="1" fill="#FFFFFF" opacity="0.7"/>'
                    x += w + 3; k += 1
            return out
        cross = ('<rect x="20" y="22" width="78" height="78" rx="14" fill="#FFFFFF" opacity="0.9"/>'
                 '<path d="M47 32 L71 32 L71 49 L88 49 L88 73 L71 73 L71 90 L47 90 L47 73 L30 73 L30 49 L47 49 Z" fill="#2BA84A"/>')
        tablet = ('<rect x="338" y="250" width="72" height="44" rx="6" fill="#2B2F3A" transform="rotate(-8 374 272)"/>'
                  '<rect x="343" y="255" width="62" height="34" rx="3" fill="#F4F8F7" transform="rotate(-8 374 272)"/>'
                  '<g transform="rotate(-8 374 272)"><path d="M349 263 l3 3 l5 -6 M349 273 l3 3 l5 -6 M349 283 l3 3 l5 -6" stroke="#1F8A7A" stroke-width="2" fill="none"/>'
                  '<rect x="362" y="262" width="34" height="3" rx="1.5" fill="#9AA6B2"/><rect x="362" y="272" width="28" height="3" rx="1.5" fill="#9AA6B2"/><rect x="362" y="282" width="32" height="3" rx="1.5" fill="#9AA6B2"/></g>')
        basket = ('<rect x="22" y="258" width="76" height="34" rx="6" fill="#E9E2D6" stroke="#B8A890" stroke-width="2"/>'
                  '<rect x="30" y="246" width="18" height="16" rx="2" fill="#81B29A"/><rect x="52" y="242" width="16" height="20" rx="2" fill="#F4F1DE"/><rect x="72" y="248" width="18" height="14" rx="2" fill="#3D85C6"/>'
                  '<path d="M22 270 L98 270" stroke="#B8A890" stroke-width="1.5"/>')
        return f'''<defs><linearGradient id="w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c["wall_top"]}"/><stop offset="1" stop-color="{c["wall_bot"]}"/></linearGradient></defs>
        <rect width="{PW}" height="{PH}" fill="url(#w)"/>
        {cross}
        <rect x="8" y="112" width="142" height="160" fill="#E2D2C0" opacity="0.6"/>{shelf(12, 146, [160, 214, 268], 1)}
        <rect x="292" y="14" width="146" height="258" fill="#E2D2C0" opacity="0.6"/>{shelf(296, 434, [74, 128, 182, 236], 4)}
        <rect x="0" y="292" width="{PW}" height="348" fill="#3F6F68"/><rect x="0" y="284" width="{PW}" height="12" rx="3" fill="#F2EEE6"/><rect x="0" y="296" width="{PW}" height="5" fill="#2E534D"/>
        {basket}{tablet}'''
    if c["room"] == "drafting_studio":
        bp = "#1F4E79"; ln = "#DCE9F5"
        plan = (f'<rect x="14" y="46" width="146" height="112" fill="{bp}"/>'
                f'<rect x="28" y="60" width="118" height="84" fill="none" stroke="{ln}" stroke-width="3"/>'
                f'<path d="M84 60 L84 102 M28 102 L70 102 M98 102 L146 102 M112 102 L112 144" stroke="{ln}" stroke-width="2.2" fill="none"/>'
                f'<path d="M70 102 A14 14 0 0 1 84 88" stroke="{ln}" stroke-width="1.4" fill="none"/>'
                f'<rect x="40" y="70" width="30" height="18" fill="none" stroke="{ln}" stroke-width="1.2" opacity="0.7"/><circle cx="128" cy="124" r="7" fill="none" stroke="{ln}" stroke-width="1.2" opacity="0.7"/>'
                f'<rect x="106" y="146" width="48" height="8" fill="{ln}" opacity="0.85"/>'
                f'<circle cx="22" cy="52" r="3.5" fill="#E05A47"/><circle cx="152" cy="52" r="3.5" fill="#E05A47"/>')
        elev = (f'<rect x="330" y="40" width="94" height="72" fill="#FBF8F1" transform="rotate(3 377 76)"/>'
                f'<g transform="rotate(3 377 76)"><path d="M344 100 L344 74 L366 58 L388 74 L388 100 Z M388 100 L388 80 L412 80 L412 100 Z" fill="none" stroke="#4A4F5A" stroke-width="2"/>'
                f'<rect x="352" y="82" width="10" height="12" fill="none" stroke="#4A4F5A" stroke-width="1.5"/><rect x="396" y="86" width="10" height="14" fill="#9DB7CF"/>'
                f'<path d="M338 101 L418 101" stroke="#4A4F5A" stroke-width="1.5"/><circle cx="377" cy="44" r="3.5" fill="#E05A47"/></g>')
        model = (f'<rect x="316" y="180" width="118" height="7" fill="#7A5B3E"/>'
                 f'<rect x="324" y="168" width="96" height="12" fill="#D9CBB2"/>'
                 f'<rect x="334" y="128" width="34" height="40" fill="#FFFFFF" stroke="#C8C2B8" stroke-width="1.5"/><rect x="368" y="144" width="40" height="24" fill="#F1EEE8" stroke="#C8C2B8" stroke-width="1.5"/>'
                 f'<path d="M334 128 L346 118 L380 118 L368 128 Z" fill="#E6E1D8" stroke="#C8C2B8" stroke-width="1.5"/>'
                 f'<path d="M340 138 L362 138 M340 148 L362 148 M340 158 L362 158" stroke="#C8C2B8" stroke-width="1.5"/>'
                 f'<circle cx="414" cy="158" r="8" fill="#7FA36B"/><rect x="413" y="162" width="2" height="6" fill="#6B4E36"/>')
        lamp = ('<path d="M150 0 L150 22" stroke="#2C2D33" stroke-width="2"/><path d="M128 40 Q150 16 172 40 Z" fill="#2C2D33"/><ellipse cx="150" cy="41" rx="10" ry="3" fill="#FFE7A8"/>')
        return f'''<defs><linearGradient id="w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c["wall_top"]}"/><stop offset="1" stop-color="{c["wall_bot"]}"/></linearGradient></defs>
        <rect width="{PW}" height="{PH}" fill="url(#w)"/>
        {plan}{elev}{model}
        <rect x="18" y="190" width="40" height="70" rx="4" fill="#5C6470"/><rect x="24" y="166" width="9" height="40" rx="4" fill="#F4EFE4"/><rect x="36" y="160" width="9" height="46" rx="4" fill="#DCE9F5"/><rect x="47" y="172" width="8" height="34" rx="4" fill="#F4EFE4"/>
        <rect x="0" y="292" width="{PW}" height="348" fill="#8A6A4C"/><rect x="0" y="286" width="{PW}" height="8" fill="#5E4630"/>
        <path d="M66 284 L66 238 L112 284 Z M74 276 L74 258 L92 276 Z" fill="#9FD3C7" opacity="0.85" fill-rule="evenodd"/>
        <rect x="16" y="270" width="44" height="14" rx="7" fill="#F7F1E0"/><ellipse cx="60" cy="277" rx="4" ry="7" fill="#E4DCC6"/>
        <rect x="372" y="280" width="40" height="7" rx="3" fill="#2C2D33"/><path d="M392 280 L374 240 L404 214" stroke="#2C2D33" stroke-width="5" fill="none" stroke-linecap="round"/>
        <path d="M396 204 L424 222 L412 236 Z" fill="#2C2D33"/><path d="M412 236 L424 222" stroke="#FFE7A8" stroke-width="3"/>'''
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
    if c["outfit_style"] == "double_breasted":
        o = c["outfit"]; sh = c["outfit_shade"]; a = c["accent"]; sl = c["shell"]; ss = c["shell_shade"]
        return f"""
    <rect x="190" y="372" width="60" height="90" rx="22" fill="{c["skin_shade"]}"/>
    <path d="M36 640 C36 524 88 464 172 446 L220 470 L268 446 C352 464 404 524 404 640 Z" fill="{o}"/>
    <path d="M174 446 Q220 486 266 446 L252 560 L188 560 Z" fill="{sl}"/>
    <path d="M178 450 Q220 488 262 450" stroke="{ss}" stroke-width="4" fill="none"/>
    <path d="M196 470 Q220 488 244 470" stroke="{a}" stroke-width="2.5" fill="none"/><rect x="212" y="480" width="16" height="6" rx="3" fill="{a}"/>
    <path d="M172 446 L140 512 L178 540 L236 640 L180 640 L118 520 Z" fill="{sh}"/>
    <path d="M268 446 L300 512 L262 540 L250 600 L262 640 L322 520 Z" fill="{sh}"/>
    <path d="M172 446 L140 512 L178 540 L240 640 L250 640 L258 560 L188 548 Z" fill="{o}" stroke="{sh}" stroke-width="3" stroke-linejoin="round"/>
    <path d="M268 446 L300 512 L262 540 L258 560 L268 452 Z" fill="{o}" stroke="{sh}" stroke-width="3" stroke-linejoin="round"/>
    <path d="M188 548 L258 560 L240 640" stroke="{sh}" stroke-width="3" fill="none"/>
    """ + "".join(f'<circle cx="{x}" cy="{y}" r="6" fill="{a}"/><circle cx="{x}" cy="{y}" r="2.2" fill="#8A6420"/>' for x, y in [(206, 580), (270, 580), (206, 618), (270, 618)]) + f"""
    <path d="M300 540 L340 534" stroke="{sh}" stroke-width="4" stroke-linecap="round"/>
    <path d="M100 560 L138 552" stroke="{sh}" stroke-width="4" stroke-linecap="round"/>
    <path d="M70 640 C74 590 86 560 104 540" stroke="{sh}" stroke-width="5" fill="none" stroke-linecap="round"/>
    <path d="M370 640 C366 590 354 560 336 540" stroke="{sh}" stroke-width="5" fill="none" stroke-linecap="round"/>"""
    if c["outfit_style"] == "event_blazer":
        o = c["outfit"]; sh = c["outfit_shade"]; a = c["accent"]; t = c["tee"]; ts = c["tee_shade"]
        return f"""
    <rect x="190" y="372" width="60" height="90" rx="22" fill="{c["skin_shade"]}"/>
    <path d="M36 640 C36 524 88 464 172 446 Q220 470 268 446 C352 464 404 524 404 640 Z" fill="{t}"/>
    <path d="M178 448 Q220 478 262 448" stroke="{ts}" stroke-width="7" fill="none" stroke-linecap="round"/>
    <path d="M36 640 C36 524 88 464 166 444 L196 540 L186 640 Z" fill="{o}"/>
    <path d="M404 640 C404 524 352 464 274 444 L244 540 L254 640 Z" fill="{o}"/>
    <path d="M166 444 L150 476 L176 486 L160 500 L196 548 Z" fill="{sh}"/>
    <path d="M274 444 L290 476 L264 486 L280 500 L244 548 Z" fill="{sh}"/>
    <path d="M166 444 L196 548 M274 444 L244 548" stroke="#0F3A3A" stroke-width="2" opacity="0.6"/>
    <path d="M104 540 C88 566 76 600 72 640 M336 540 C352 566 364 600 368 640" stroke="{sh}" stroke-width="5" fill="none" stroke-linecap="round"/>
    <path d="M300 520 L340 512 L342 518 L302 526 Z" fill="{sh}"/><path d="M306 516 L314 504 L320 515 L328 503 L334 514" fill="#F7F1E6" stroke="#F7F1E6" stroke-width="2"/>
    <circle cx="186" cy="600" r="5" fill="#0F3A3A"/>
    <path d="M180 452 L210 552 M260 452 L230 552" stroke="{a}" stroke-width="7" fill="none" stroke-linecap="round"/>
    <rect x="200" y="548" width="40" height="8" rx="3" fill="#B8BEC8"/>
    <rect x="190" y="554" width="60" height="78" rx="7" fill="#FFFFFF" stroke="#D5D9E0" stroke-width="2"/>
    <rect x="190" y="554" width="60" height="20" rx="7" fill="{a}"/><rect x="190" y="566" width="60" height="8" fill="{a}"/>
    <text x="220" y="569" font-family="Inter" font-weight="800" font-size="10" fill="#FFFFFF" text-anchor="middle" letter-spacing="1.5">CREW</text>
    <circle cx="220" cy="592" r="11" fill="{c["skin"]}"/><path d="M206 616 Q220 600 234 616 Z" fill="{o}"/>
    <rect x="202" y="620" width="36" height="4" rx="2" fill="#6A6276"/>
    <g transform="rotate(-7 116 600)"><rect x="70" y="548" width="92" height="100" rx="8" fill="#2B2F3A"/><rect x="76" y="554" width="80" height="88" rx="3" fill="#F7F7FA"/>
    <rect x="80" y="558" width="72" height="12" rx="2" fill="{o}"/><text x="116" y="567" font-family="Inter" font-weight="800" font-size="7.5" fill="#FFFFFF" text-anchor="middle" letter-spacing="1">RUN OF SHOW</text>
    """ + "".join(f'<text x="82" y="{582 + i*13}" font-family="Inter" font-weight="700" font-size="7" fill="#4A4458">{tm}</text><rect x="106" y="{577 + i*13}" width="{w}" height="4" rx="2" fill="{col}"/>'
                  for i, (tm, w, col) in enumerate([("09:00", 40, "#9AA6A4"), ("10:30", 32, a), ("12:30", 44, "#9AA6A4"), ("14:00", 36, "#9AA6A4"), ("17:00", 28, "#9AA6A4")])) + """
    <path d="M80 588 L152 588" stroke="#E4E0EA" stroke-width="0.8"/></g>"""
    if c["outfit_style"] == "bomber":
        o = c["outfit"]; sh = c["outfit_shade"]; a = c["accent"]; rb = c["rib"]; rs = c["rib_stripe"]
        return f"""
    <rect x="190" y="372" width="60" height="90" rx="22" fill="{c["skin_shade"]}"/>
    <path d="M36 640 C36 524 88 464 172 446 L220 470 L268 446 C352 464 404 524 404 640 Z" fill="{c["tee"]}"/>
    <path d="M176 450 Q220 492 264 450" stroke="{c["tee_shade"]}" stroke-width="7" fill="none" stroke-linecap="round"/>
    <rect x="202" y="560" width="36" height="36" rx="10" fill="{a}"/><path d="M212 572 Q212 566 220 566 Q228 566 228 573 Q228 578 220 580 L220 585" stroke="#FFFFFF" stroke-width="3.5" fill="none" stroke-linecap="round"/><circle cx="220" cy="590" r="2.2" fill="#FFFFFF"/>
    <path d="M36 640 C36 524 88 464 166 444 L182 452 C190 500 194 560 192 640 Z" fill="{o}"/>
    <path d="M404 640 C404 524 352 464 274 444 L258 452 C250 500 246 560 248 640 Z" fill="{o}"/>
    <path d="M150 470 C160 520 168 580 170 640" stroke="{sh}" stroke-width="5" fill="none" opacity="0.7" stroke-linecap="round"/>
    <path d="M290 470 C280 520 272 580 270 640" stroke="{sh}" stroke-width="5" fill="none" opacity="0.7" stroke-linecap="round"/>
    <path d="M104 540 C88 566 76 600 72 640 M336 540 C352 566 364 600 368 640" stroke="{sh}" stroke-width="5" fill="none" stroke-linecap="round"/>
    <path d="M190 456 C194 520 196 580 194 640 M250 456 C246 520 244 580 246 640" stroke="#C9CED6" stroke-width="3" fill="none" stroke-dasharray="3 3"/>
    <path d="M150 446 Q178 444 192 462" stroke="{rb}" stroke-width="13" fill="none" stroke-linecap="round"/>
    <path d="M290 446 Q262 444 248 462" stroke="{rb}" stroke-width="13" fill="none" stroke-linecap="round"/>
    <path d="M152 446 Q178 444 191 461 M288 446 Q262 444 249 461" stroke="{rs}" stroke-width="2.5" fill="none"/>
    <path d="M110 520 L150 512 L152 528 L112 536 Z" fill="{sh}" opacity="0.9"/><path d="M114 522 L146 516" stroke="{rs}" stroke-width="2"/>
    <g transform="rotate(8 306 598)"><rect x="282" y="556" width="48" height="86" rx="9" fill="#1F2A3A"/><rect x="287" y="566" width="38" height="70" rx="3" fill="#FFFFFF"/>
    <rect x="291" y="570" width="30" height="7" rx="2" fill="{a}"/>
    <rect x="292" y="583" width="6" height="6" rx="1.5" fill="none" stroke="#2F7A4A" stroke-width="1.5"/><path d="M293 586 L295 588 L298 584" stroke="#2F7A4A" stroke-width="1.5" fill="none"/><rect x="301" y="584" width="18" height="3" rx="1.5" fill="#9AA6A4"/>
    <rect x="292" y="594" width="6" height="6" rx="1.5" fill="none" stroke="#9AA6A4" stroke-width="1.5"/><rect x="301" y="595" width="14" height="3" rx="1.5" fill="#9AA6A4"/>
    <rect x="292" y="605" width="6" height="6" rx="1.5" fill="none" stroke="#9AA6A4" stroke-width="1.5"/><rect x="301" y="606" width="16" height="3" rx="1.5" fill="#9AA6A4"/>
    <circle cx="316" cy="626" r="5" fill="{rs}"/><circle cx="306" cy="626" r="5" fill="#9FE2BF"/></g>"""
    if c["outfit_style"] == "interview_suit":
        a = c["accent"]; o = c["outfit"]; sh = c["outfit_shade"]; sr = c["shirt"]; ss = c["shirt_shade"]
        return f"""
    <rect x="190" y="372" width="60" height="90" rx="22" fill="{c["skin_shade"]}"/>
    <path d="M36 640 C36 524 88 464 172 446 L220 470 L268 446 C352 464 404 524 404 640 Z" fill="{o}"/>
    <path d="M176 444 L220 640 L264 444 L220 468 Z" fill="{sr}"/>
    <path d="M180 440 L220 468 L204 492 L174 452 Z" fill="{sr}" stroke="{ss}" stroke-width="2"/><path d="M260 440 L220 468 L236 492 L266 452 Z" fill="{sr}" stroke="{ss}" stroke-width="2"/>
    <path d="M210 468 L230 468 L226 482 L214 482 Z" fill="{a}"/>
    <path d="M214 482 L226 482 L234 590 L220 606 L206 590 Z" fill="{a}"/>
    """ + "".join(f'<path d="M{214 - i*0.4:.1f} {492 + i*12} L{226 + i*0.4:.1f} {492 + i*12}" stroke="#000000" stroke-width="1.5" opacity="0.18"/>' for i in range(9)) + f"""
    <path d="M172 446 L144 514 L186 548 L212 640 L168 640 L118 520 Z" fill="{sh}"/>
    <path d="M268 446 L296 514 L254 548 L228 640 L272 640 L322 520 Z" fill="{sh}"/>
    <path d="M172 446 L144 514 L186 548 L214 610 L178 452 Z" fill="{o}" stroke="{sh}" stroke-width="3"/>
    <path d="M268 446 L296 514 L254 548 L226 610 L262 452 Z" fill="{o}" stroke="{sh}" stroke-width="3"/>
    <circle cx="220" cy="624" r="5" fill="{sh}"/>
    <path d="M282 556 L330 552" stroke="{sh}" stroke-width="4" stroke-linecap="round"/>
    <path d="M290 556 L298 540 L306 548 L314 538 L322 554 Z" fill="#FFFFFF"/>
    <rect x="160" y="500" width="12" height="4" rx="2" fill="#C9A227" transform="rotate(-24 166 502)"/>
    <path d="M70 640 C74 590 86 560 104 540" stroke="{sh}" stroke-width="5" fill="none" stroke-linecap="round"/>
    <path d="M370 640 C366 590 354 560 336 540" stroke="{sh}" stroke-width="5" fill="none" stroke-linecap="round"/>"""
    if c["outfit_style"] == "hi_vis_vest":
        o = c["outfit"]; sh = c["outfit_shade"]; v = c["vest"]; vs = c["vest_shade"]; rf = c["reflect"]
        L = "M150 452 L194 470 L204 640 L94 640 C98 560 112 500 150 452 Z"
        R = "M290 452 L246 470 L236 640 L346 640 C342 560 328 500 290 452 Z"
        return f"""
    <defs><clipPath id="hv"><path d="{L} {R}"/></clipPath></defs>
    <rect x="190" y="372" width="60" height="90" rx="22" fill="{c["skin_shade"]}"/>
    <path d="M36 640 C36 524 88 464 172 446 L220 470 L268 446 C352 464 404 524 404 640 Z" fill="{o}"/>
    <path d="M182 448 Q220 486 258 448 Q252 470 220 482 Q188 470 182 448 Z" fill="{sh}"/>
    <path d="M70 640 C74 590 86 560 104 540" stroke="{sh}" stroke-width="5" fill="none" stroke-linecap="round"/>
    <path d="M370 640 C366 590 354 560 336 540" stroke="{sh}" stroke-width="5" fill="none" stroke-linecap="round"/>
    <path d="{L}" fill="{v}"/><path d="{R}" fill="{v}"/>
    <g clip-path="url(#hv)">
      <rect x="80" y="548" width="280" height="16" fill="{rf}"/><rect x="80" y="596" width="280" height="16" fill="{rf}"/>
      <rect x="80" y="554" width="280" height="3" fill="#FFFFFF" opacity="0.7"/><rect x="80" y="602" width="280" height="3" fill="#FFFFFF" opacity="0.7"/>
      <path d="M150 452 L164 458 L150 548 L134 548 Z M290 452 L276 458 L290 548 L306 548 Z" fill="{rf}" opacity="0.9"/>
    </g>
    <path d="M194 470 L204 640 M246 470 L236 640" stroke="{vs}" stroke-width="4"/>
    <path d="M150 452 C112 500 98 560 94 640 M290 452 C328 500 342 560 346 640" stroke="{vs}" stroke-width="4" fill="none"/>
    <rect x="200" y="500" width="6" height="12" rx="2" fill="#8A929B"/>
    <rect x="252" y="496" width="44" height="40" rx="4" fill="{vs}"/>
    <rect x="262" y="470" width="24" height="40" rx="5" fill="#2B2F36"/><rect x="265" y="474" width="18" height="12" rx="2" fill="#5BC0EB"/><rect x="264" y="466" width="20" height="6" rx="2" fill="#E0503A"/>
    <rect x="252" y="496" width="44" height="8" fill="{v}"/>
    <rect x="164" y="508" width="34" height="44" rx="4" fill="#FFFFFF" stroke="#C9D0D8" stroke-width="1.5"/>
    <rect x="164" y="508" width="34" height="9" rx="3" fill="#2E5FA8"/>
    <rect x="170" y="521" width="12" height="14" rx="2" fill="#C8A58A"/><rect x="185" y="523" width="9" height="3" fill="#5B6570"/><rect x="185" y="529" width="7" height="3" fill="#5B6570"/>
    """ + "".join(f'<rect x="{169 + i*3}" y="540" width="{1 + (i % 2)}" height="8" fill="#1A1D24"/>' for i in range(8)) + f"""
    <rect x="178" y="500" width="6" height="10" rx="2" fill="#8A929B"/>"""
    if c["outfit_style"] == "track_jacket":
        a = c["accent"]; o = c["outfit"]; sh = c["outfit_shade"]; t = c["tee"]; ts = c["tee_shade"]; st = c["stripe"]
        return f"""
    <defs><clipPath id="tj"><path d="M36 640 C36 524 88 464 172 446 L220 470 L268 446 C352 464 404 524 404 640 Z"/></clipPath></defs>
    <rect x="190" y="372" width="60" height="90" rx="22" fill="{c["skin_shade"]}"/>
    <path d="M36 640 C36 524 88 464 172 446 L220 470 L268 446 C352 464 404 524 404 640 Z" fill="{o}"/>
    <g clip-path="url(#tj)">
      <path d="M150 452 C110 470 80 520 66 640" stroke="{st}" stroke-width="7" fill="none"/>
      <path d="M164 450 C124 470 96 524 84 640" stroke="{st}" stroke-width="7" fill="none"/>
      <path d="M290 452 C330 470 360 520 374 640" stroke="{st}" stroke-width="7" fill="none"/>
      <path d="M276 450 C316 470 344 524 356 640" stroke="{st}" stroke-width="7" fill="none"/>
    </g>
    <path d="M186 452 L220 478 L254 452 L248 640 L192 640 Z" fill="{t}"/>
    <path d="M194 450 Q220 474 246 450 Q242 462 220 478 Q198 462 194 450 Z" fill="{ts}"/>
    <path d="M186 452 L192 640 L180 640 C174 580 172 520 172 450 Z" fill="{sh}"/>
    <path d="M254 452 L248 640 L260 640 C266 580 268 520 268 450 Z" fill="{sh}"/>
    <path d="M160 438 L186 448 L200 490 L176 498 Z" fill="{sh}"/><path d="M280 438 L254 448 L240 490 L264 498 Z" fill="{sh}"/>
    <path d="M186 452 L192 640 M254 452 L248 640" stroke="#D9DDE2" stroke-width="2.5"/>
    <rect x="243" y="498" width="7" height="16" rx="2" fill="#D9DDE2"/>
    <path d="M200 470 C204 500 212 520 220 534 M240 470 C236 500 228 520 220 534" stroke="#20242C" stroke-width="3" fill="none"/>
    <circle cx="220" cy="552" r="17" fill="#20242C"/><circle cx="220" cy="552" r="12" fill="#E9EEF2"/><rect x="216" y="530" width="8" height="6" rx="2" fill="#20242C"/>
    <path d="M220 552 L220 544 M220 552 L226 555" stroke="#E0503A" stroke-width="2" stroke-linecap="round"/>
    <path d="M110 520 L134 516 L136 528 L112 532 Z" fill="{a}"/>
    <path d="M70 640 C74 590 86 560 104 540" stroke="{sh}" stroke-width="5" fill="none" stroke-linecap="round"/>
    <path d="M370 640 C366 590 354 560 336 540" stroke="{sh}" stroke-width="5" fill="none" stroke-linecap="round"/>"""
    if c["outfit_style"] == "chore_coat":
        a = c["accent"]; o = c["outfit"]; sh = c["outfit_shade"]; co = c["collar"]; hn = c["henley"]; hs = c["henley_shade"]
        stitch = ''.join(f'<path d="M{x} 470 L{x} 640" stroke="{sh}" stroke-width="1.5" opacity="0.35"/>' for x in list(range(64, 176, 16)) + list(range(270, 388, 16)))
        cord = ''.join(f'<path d="M{150+i*5} {438+i*1.2:.0f} L{176+i*4} {500+i*2}" stroke="#3E2818" stroke-width="1.5" opacity="0.5"/>' for i in range(6))
        cord += ''.join(f'<path d="M{290-i*5} {438+i*1.2:.0f} L{264-i*4} {500+i*2}" stroke="#3E2818" stroke-width="1.5" opacity="0.5"/>' for i in range(6))
        return f"""
    <defs><clipPath id="cc"><path d="M36 640 C36 524 88 464 172 446 L220 470 L268 446 C352 464 404 524 404 640 Z"/></clipPath></defs>
    <rect x="190" y="372" width="60" height="90" rx="22" fill="{c["skin_shade"]}"/>
    <path d="M36 640 C36 524 88 464 172 446 L220 470 L268 446 C352 464 404 524 404 640 Z" fill="{o}"/>
    <g clip-path="url(#cc)">{stitch}</g>
    <path d="M180 448 L220 476 L260 448 L256 640 L184 640 Z" fill="{hn}"/>
    <path d="M190 446 Q220 470 250 446 Q246 460 220 474 Q194 460 190 446 Z" fill="{hs}"/>
    <path d="M208 472 L208 540 L232 540 L232 472" stroke="{hs}" stroke-width="2.5" fill="none"/>
    <circle cx="220" cy="490" r="3" fill="#E9DCC6"/><circle cx="220" cy="508" r="3" fill="#E9DCC6"/><circle cx="220" cy="526" r="3" fill="#E9DCC6"/>
    <path d="M184 452 C176 520 182 590 190 640 L174 640 C164 580 160 520 168 452 Z" fill="{sh}"/>
    <path d="M256 452 C264 520 258 590 250 640 L266 640 C276 580 280 520 272 452 Z" fill="{sh}"/>
    <path d="M146 438 L184 446 L198 506 L170 512 Z" fill="{co}"/><path d="M294 438 L256 446 L242 506 L270 512 Z" fill="{co}"/>
    {cord}
    <rect x="96" y="540" width="56" height="52" rx="4" fill="{sh}"/><path d="M94 534 L154 534 L152 556 L96 556 Z" fill="{o}" stroke="{sh}" stroke-width="2"/>
    <circle cx="124" cy="550" r="3.5" fill="#5A3A26"/>
    <rect x="288" y="540" width="56" height="52" rx="4" fill="{sh}"/><path d="M286 534 L346 534 L344 556 L288 556 Z" fill="{o}" stroke="{sh}" stroke-width="2"/>
    <circle cx="316" cy="550" r="3.5" fill="#5A3A26"/>
    <rect x="302" y="512" width="6" height="30" rx="2" fill="#F2C14E"/><path d="M302 512 L305 504 L308 512 Z" fill="#E9C9A0"/>
    <rect x="314" y="516" width="22" height="26" rx="2" fill="#F4ECDD"/><rect x="314" y="516" width="22" height="5" fill="{a}"/><rect x="318" y="526" width="14" height="2" rx="1" fill="#8A929B"/>
    <circle cx="248" cy="568" r="4.5" fill="#5A3A26"/><circle cx="248" cy="612" r="4.5" fill="#5A3A26"/>
    <path d="M70 640 C74 590 86 560 104 540" stroke="{sh}" stroke-width="5" fill="none" stroke-linecap="round"/>
    <path d="M370 640 C366 590 354 560 336 540" stroke="{sh}" stroke-width="5" fill="none" stroke-linecap="round"/>"""
    if c["outfit_style"] == "vet_scrubs":
        a = c["accent"]; o = c["outfit"]; sh = c["outfit_shade"]; u = c["under"]; us = c["under_shade"]; st = c["steth"]
        return f"""
    <rect x="190" y="372" width="60" height="90" rx="22" fill="{c["skin_shade"]}"/>
    <path d="M36 640 C36 540 70 480 120 462 L120 640 Z M404 640 C404 540 370 480 320 462 L320 640 Z" fill="{u}"/>
    <path d="M70 640 C74 600 82 570 96 548 M370 640 C366 600 358 570 344 548" stroke="{us}" stroke-width="4" fill="none" stroke-linecap="round"/>
    <path d="M60 640 C66 540 100 478 172 450 L220 470 L268 450 C340 478 374 540 380 640 Z" fill="{o}"/>
    <path d="M176 450 L220 530 L264 450 L254 446 L220 508 L186 446 Z" fill="{sh}"/>
    <path d="M186 446 L220 508 L254 446 Z" fill="{c["skin_shade"]}"/>
    <path d="M300 560 L352 560 L350 616 L302 616 Z" fill="{sh}"/><path d="M300 560 L352 560" stroke="{o}" stroke-width="3"/>
    <rect x="312" y="540" width="5" height="26" rx="2" fill="#2B2F3A"/><rect x="322" y="544" width="5" height="22" rx="2" fill="{a}"/>
    <path d="M156 456 C140 500 150 540 178 552" stroke="{st}" stroke-width="7" fill="none" stroke-linecap="round"/>
    <path d="M284 456 C300 500 290 540 262 552" stroke="{st}" stroke-width="7" fill="none" stroke-linecap="round"/>
    <path d="M178 552 Q200 566 214 586 M262 552 Q240 566 226 586" stroke="{st}" stroke-width="6" fill="none" stroke-linecap="round"/>
    <path d="M220 590 L220 606" stroke="{st}" stroke-width="6" stroke-linecap="round"/>
    <circle cx="220" cy="618" r="14" fill="#C9D1D6" stroke="{st}" stroke-width="4"/><circle cx="220" cy="618" r="7" fill="#9AA6AE"/>
    <circle cx="214" cy="588" r="5" fill="#C9D1D6"/><circle cx="226" cy="588" r="5" fill="#C9D1D6"/>
    <path d="M118 540 L118 568" stroke="#5A6A72" stroke-width="2"/><circle cx="118" cy="534" r="9" fill="{a}"/>
    <ellipse cx="118" cy="537" rx="3.5" ry="3" fill="#FFFFFF"/><circle cx="113.5" cy="531.5" r="1.6" fill="#FFFFFF"/><circle cx="116.5" cy="529.5" r="1.6" fill="#FFFFFF"/><circle cx="119.5" cy="529.5" r="1.6" fill="#FFFFFF"/><circle cx="122.5" cy="531.5" r="1.6" fill="#FFFFFF"/>
    <rect x="100" y="566" width="36" height="48" rx="5" fill="#FFFFFF" stroke="#9FB8B4" stroke-width="1.5"/><rect x="100" y="566" width="36" height="12" rx="4" fill="{sh}"/>
    <circle cx="118" cy="590" r="7" fill="{c["skin"]}"/><path d="M111 586 Q118 579 125 586" stroke="{c["hair"]}" stroke-width="4" fill="none"/><rect x="106" y="602" width="24" height="3" rx="1.5" fill="#2B2F3A"/>
    <path d="M150 640 L150 590 M290 640 L290 590" stroke="{sh}" stroke-width="3" opacity="0.6"/>"""
    if c["outfit_style"] == "shawl_cardigan":
        a = c["accent"]; o = c["outfit"]; sh = c["outfit_shade"]; sc = c["shirt"]; ss = c["shirt_shade"]; hc = c["neck_headset"]
        rib = ''.join(f'<path d="M{x} 470 L{x} 640" stroke="{sh}" stroke-width="2" opacity="0.4"/>' for x in list(range(60, 176, 12)) + list(range(268, 390, 12)))
        return f"""
    <defs><clipPath id="sc"><path d="M36 640 C36 524 88 464 172 446 L220 470 L268 446 C352 464 404 524 404 640 Z"/></clipPath></defs>
    <rect x="190" y="372" width="60" height="90" rx="22" fill="{c["skin_shade"]}"/>
    <path d="M36 640 C36 524 88 464 172 446 L220 470 L268 446 C352 464 404 524 404 640 Z" fill="{o}"/>
    <g clip-path="url(#sc)">{rib}</g>
    <path d="M182 448 L220 500 L258 448 L258 640 L182 640 Z" fill="{sc}"/>
    <path d="M190 446 L220 492 L250 446 Z" fill="{c["skin_shade"]}"/>
    <path d="M186 444 L206 484 L220 474 Z M254 444 L234 484 L220 474 Z" fill="{sc}" stroke="{ss}" stroke-width="2.5" stroke-linejoin="round"/>
    <path d="M220 480 L220 640" stroke="{ss}" stroke-width="2"/><circle cx="220" cy="530" r="3" fill="{ss}"/><circle cx="220" cy="580" r="3" fill="{ss}"/><circle cx="220" cy="626" r="3" fill="{ss}"/>
    <path d="M166 440 C150 470 160 540 196 640 L176 640 C140 560 128 480 150 446 Z" fill="{sh}"/>
    <path d="M274 440 C290 470 280 540 244 640 L264 640 C300 560 312 480 290 446 Z" fill="{sh}"/>
    <path d="M168 444 C156 476 166 540 200 640" stroke="{o}" stroke-width="4" fill="none" opacity="0.6"/>
    <path d="M272 444 C284 476 274 540 240 640" stroke="{o}" stroke-width="4" fill="none" opacity="0.6"/>
    <circle cx="250" cy="600" r="5" fill="#D8C9A8"/><circle cx="250" cy="628" r="5" fill="#D8C9A8"/>
    <rect x="128" y="534" width="40" height="5" rx="2" fill="{sh}"/><rect x="146" y="514" width="6" height="26" rx="3" fill="#2B2F3A"/><rect x="146" y="512" width="6" height="5" rx="2" fill="#C9A227"/>
    <path d="M150 474 C150 506 176 520 220 520 C264 520 290 506 290 474" stroke="{hc}" stroke-width="8" fill="none" stroke-linecap="round"/>
    <rect x="132" y="456" width="34" height="42" rx="13" fill="{hc}"/><rect x="274" y="456" width="34" height="42" rx="13" fill="{hc}"/>
    <rect x="140" y="464" width="18" height="26" rx="8" fill="{a}"/><rect x="282" y="464" width="18" height="26" rx="8" fill="{a}"/>
    <path d="M70 640 C74 590 86 560 104 540" stroke="{sh}" stroke-width="5" fill="none" stroke-linecap="round"/>
    <path d="M370 640 C366 590 354 560 336 540" stroke="{sh}" stroke-width="5" fill="none" stroke-linecap="round"/>"""
    if c["outfit_style"] == "camera_tee":
        a = c["accent"]; o = c["outfit"]; sh = c["outfit_shade"]; st = c["strap"]
        zig = ''.join(f'<path d="M{x} 0 L{x+6} 6 L{x+12} 0" stroke="{a}" stroke-width="2" fill="none"/>' for x in range(0, 168, 12))
        return f"""
    <rect x="190" y="372" width="60" height="90" rx="22" fill="{c["skin_shade"]}"/>
    <path d="M36 640 C36 524 88 464 172 446 L220 470 L268 446 C352 464 404 524 404 640 Z" fill="{o}"/>
    <path d="M176 446 Q220 486 264 446" stroke="{sh}" stroke-width="9" fill="none" stroke-linecap="round"/>
    <path d="M70 640 C74 590 86 560 104 540" stroke="{sh}" stroke-width="5" fill="none" stroke-linecap="round"/>
    <path d="M370 640 C366 590 354 560 336 540" stroke="{sh}" stroke-width="5" fill="none" stroke-linecap="round"/>
    <path d="M160 452 C150 500 158 540 176 560" stroke="{st}" stroke-width="16" fill="none" stroke-linecap="round"/>
    <path d="M280 452 C290 500 282 540 264 560" stroke="{st}" stroke-width="16" fill="none" stroke-linecap="round"/>
    <path d="M160 452 C150 500 158 540 176 560 M280 452 C290 500 282 540 264 560" stroke="{a}" stroke-width="2" fill="none" stroke-dasharray="5 5"/>
    <rect x="160" y="548" width="120" height="76" rx="12" fill="#1E2025"/>
    <rect x="160" y="548" width="120" height="16" rx="8" fill="#2E3138"/>
    <rect x="178" y="538" width="30" height="14" rx="3" fill="#2E3138"/><rect x="246" y="540" width="18" height="10" rx="2" fill="#3A3D44"/>
    <rect x="166" y="566" width="20" height="54" rx="6" fill="#3A3D44"/>
    <circle cx="228" cy="590" r="30" fill="#2E3138"/><circle cx="228" cy="590" r="23" fill="#14161A"/><circle cx="228" cy="590" r="15" fill="#2E4A66"/>
    <circle cx="228" cy="590" r="23" fill="none" stroke="#D43A2F" stroke-width="2"/>
    <circle cx="222" cy="584" r="5" fill="#FFFFFF" opacity="0.55"/><circle cx="233" cy="595" r="2" fill="#FFFFFF" opacity="0.4"/>
    <circle cx="266" cy="560" r="4" fill="#D43A2F"/>"""
    if c["outfit_style"] == "fleece_vest":
        a = c["accent"]; o = c["outfit"]; sh = c["outfit_shade"]; sc = c["shirt"]; ss = c["shirt_shade"]
        quilt = ''.join(f'<path d="M40 {y} Q120 {y-6} 196 {y} M244 {y} Q320 {y-6} 400 {y}" stroke="{sh}" stroke-width="2.5" fill="none" opacity="0.7"/>' for y in range(540, 640, 26))
        return f"""
    <defs><clipPath id="fv"><path d="M36 640 C36 524 88 464 172 446 L220 470 L268 446 C352 464 404 524 404 640 Z"/></clipPath></defs>
    <rect x="190" y="372" width="60" height="90" rx="22" fill="{c["skin_shade"]}"/>
    <path d="M36 640 C36 524 88 464 172 446 L220 470 L268 446 C352 464 404 524 404 640 Z" fill="{sc}"/>
    <g clip-path="url(#fv)">
    <path d="M36 640 L36 560 C40 520 70 492 104 480 L120 640 Z M404 640 L404 560 C400 520 370 492 336 480 L320 640 Z" fill="{ss}"/>
    <path d="M110 470 C140 452 168 446 182 446 L210 520 L210 640 L104 640 C108 600 110 540 110 470 Z" fill="{o}"/>
    <path d="M330 470 C300 452 272 446 258 446 L230 520 L230 640 L336 640 C332 600 330 540 330 470 Z" fill="{o}"/>
    </g>
    <defs><clipPath id="fvp"><path d="M110 470 C140 452 168 446 182 446 L210 520 L210 640 L104 640 C108 600 110 540 110 470 Z M330 470 C300 452 272 446 258 446 L230 520 L230 640 L336 640 C332 600 330 540 330 470 Z"/></clipPath></defs>
    <g clip-path="url(#fvp)">{quilt}</g>
    <path d="M190 446 L220 488 L250 446 Z" fill="{c["skin_shade"]}"/>
    <path d="M186 444 L206 486 L220 470 Z M254 444 L234 486 L220 470 Z" fill="{sc}" stroke="{ss}" stroke-width="2.5" stroke-linejoin="round"/>
    <path d="M220 476 L220 640" stroke="{ss}" stroke-width="2"/>
    <circle cx="220" cy="520" r="3" fill="#F4F6F8"/><circle cx="220" cy="560" r="3" fill="#F4F6F8"/><circle cx="220" cy="600" r="3" fill="#F4F6F8"/>
    <path d="M182 446 L210 520 L210 640" stroke="{sh}" stroke-width="5" fill="none"/><path d="M258 446 L230 520 L230 640" stroke="{sh}" stroke-width="5" fill="none"/>
    <path d="M206 520 L206 640" stroke="#C9CED4" stroke-width="2" stroke-dasharray="2 2"/>
    <path d="M178 446 Q172 470 176 486 M262 446 Q268 470 264 486" stroke="{sh}" stroke-width="6" fill="none" stroke-linecap="round"/>
    <path d="M196 452 L178 540 M244 452 L262 540" stroke="{a}" stroke-width="4" fill="none"/>
    <rect x="248" y="536" width="42" height="56" rx="5" fill="#FFFFFF" stroke="#8A929B" stroke-width="1.5"/><rect x="248" y="536" width="42" height="12" rx="4" fill="{a}"/>
    <circle cx="269" cy="562" r="8" fill="{c["skin"]}"/><path d="M262 557 Q269 550 276 557" stroke="{c["hair"]}" stroke-width="4" fill="none"/><rect x="256" y="575" width="26" height="3" rx="1.5" fill="#2B2F3A"/><rect x="259" y="582" width="20" height="2.5" rx="1" fill="#8A929B"/>
    <rect x="140" y="498" width="7" height="30" rx="3" fill="#2B2F3A"/><rect x="140" y="496" width="7" height="6" rx="2" fill="#C9A227"/><path d="M128 520 L172 520 L170 528 L130 528 Z" fill="{sh}"/>
    <path d="M70 640 C74 590 86 560 104 540" stroke="{ss}" stroke-width="4" fill="none" stroke-linecap="round"/>
    <path d="M370 640 C366 590 354 560 336 540" stroke="{ss}" stroke-width="4" fill="none" stroke-linecap="round"/>"""
    if c["outfit_style"] == "wrap_top":
        a = c["accent"]; o = c["outfit"]; sh = c["outfit_shade"]
        return f"""
    <defs><clipPath id="wt"><path d="M36 640 C36 524 88 464 172 446 L220 470 L268 446 C352 464 404 524 404 640 Z"/></clipPath></defs>
    <rect x="190" y="372" width="60" height="90" rx="22" fill="{c["skin_shade"]}"/>
    <path d="M36 640 C36 524 88 464 172 446 L220 470 L268 446 C352 464 404 524 404 640 Z" fill="{o}"/>
    <path d="M170 446 Q200 446 220 470 Q240 446 270 446 L262 460 L222 540 L178 460 Z" fill="{c["skin_shade"]}"/>
    <g clip-path="url(#wt)">
    <path d="M164 444 L232 546 L360 640 L404 640 L404 600 L280 520 L272 446 Z" fill="{sh}" opacity="0.55"/>
    <path d="M168 446 L224 540 L340 640" stroke="{sh}" stroke-width="6" fill="none" stroke-linecap="round"/>
    <path d="M272 446 L234 520" stroke="{sh}" stroke-width="5" fill="none" stroke-linecap="round"/>
    </g>
    <path d="M194 452 Q220 492 246 452" stroke="{a}" stroke-width="2.5" fill="none"/><circle cx="220" cy="484" r="7" fill="{a}"/><circle cx="218" cy="482" r="2" fill="#FFFFFF" opacity="0.6"/>
    <path d="M70 640 C74 590 86 560 104 540" stroke="{sh}" stroke-width="5" fill="none" stroke-linecap="round"/>
    <path d="M370 640 C366 590 354 560 336 540" stroke="{sh}" stroke-width="5" fill="none" stroke-linecap="round"/>
    <rect x="96" y="560" width="62" height="80" rx="6" fill="#B98A5A" transform="rotate(-8 127 600)"/><rect x="102" y="574" width="50" height="66" rx="2" fill="#F7F5EF" transform="rotate(-8 127 600)"/>
    <rect x="114" y="554" width="26" height="12" rx="3" fill="#8C8496" transform="rotate(-8 127 600)"/>
    <g transform="rotate(-8 127 600)"><path d="M108 588 L112 592 L118 584 M108 604 L112 608 L118 600" stroke="#2F7A4A" stroke-width="2.5" fill="none" stroke-linecap="round"/>
    <rect x="124" y="587" width="22" height="3" rx="1.5" fill="#8A929B"/><rect x="124" y="603" width="18" height="3" rx="1.5" fill="#8A929B"/><rect x="108" y="618" width="10" height="10" rx="2" fill="none" stroke="#8A929B" stroke-width="2"/><rect x="124" y="621" width="20" height="3" rx="1.5" fill="#8A929B"/></g>"""
    if c["outfit_style"] == "knit_sweater":
        o = c["outfit"]; sh = c["outfit_shade"]; a = c["accent"]
        knit = ''.join(f'<path d="M{x} 520 Q{x+6} 528 {x} 536 Q{x-6} 544 {x} 552 Q{x+6} 560 {x} 568 Q{x-6} 576 {x} 584 Q{x+6} 592 {x} 600 Q{x-6} 608 {x} 616 Q{x+6} 624 {x} 632" stroke="{sh}" stroke-width="3" fill="none" opacity="0.8"/>' for x in (176, 220, 264))
        return f"""
    <rect x="190" y="372" width="60" height="90" rx="22" fill="{c["skin_shade"]}"/>
    <path d="M36 640 C36 524 88 464 172 446 L220 470 L268 446 C352 464 404 524 404 640 Z" fill="{o}"/>
    {knit}
    <path d="M150 520 L150 640 M290 520 L290 640" stroke="{sh}" stroke-width="2.5" opacity="0.6" stroke-dasharray="4 4"/>
    <path d="M70 640 C74 590 86 560 104 540" stroke="{sh}" stroke-width="5" fill="none" stroke-linecap="round"/>
    <path d="M370 640 C366 590 354 560 336 540" stroke="{sh}" stroke-width="5" fill="none" stroke-linecap="round"/>
    <path d="M300 470 C332 520 344 580 340 640" stroke="{c["strap"]}" stroke-width="16" fill="none"/><path d="M300 470 C332 520 344 580 340 640" stroke="#FFFFFF" stroke-width="2" fill="none" opacity="0.18" stroke-dasharray="6 6"/>
    <circle cx="132" cy="540" r="11" fill="{a}"/><circle cx="132" cy="540" r="7" fill="none" stroke="#FFFFFF" stroke-width="2"/><path d="M128 540 L131 543 L137 536" stroke="#FFFFFF" stroke-width="2" fill="none" stroke-linecap="round"/>"""
    if c["outfit_style"] == "quarter_zip":
        a = c["accent"]; o = c["outfit"]; sh = c["outfit_shade"]
        knit = ''.join(f'<path d="M{x} 520 L{x} 640" stroke="{sh}" stroke-width="2" opacity="0.35"/>' for x in range(64, 390, 14))
        return f"""
    <defs><clipPath id="qz"><path d="M36 640 C36 524 88 464 172 446 L220 470 L268 446 C352 464 404 524 404 640 Z"/></clipPath></defs>
    <rect x="190" y="372" width="60" height="90" rx="22" fill="{c["skin_shade"]}"/>
    <path d="M36 640 C36 524 88 464 172 446 L220 470 L268 446 C352 464 404 524 404 640 Z" fill="{o}"/>
    <g clip-path="url(#qz)">{knit}<rect x="0" y="618" width="440" height="22" fill="{sh}"/></g>
    <path d="M190 446 L220 500 L250 446 Z" fill="{c["shirt"]}"/>
    <path d="M190 446 L204 476 L218 470 L208 446 Z M250 446 L236 476 L222 470 L232 446 Z" fill="{c["shirt"]}" stroke="{c["shirt_shade"]}" stroke-width="2" stroke-linejoin="round"/>
    <path d="M172 440 Q220 462 268 440 L272 456 Q246 470 230 470 L220 520 L210 470 Q194 470 168 456 Z" fill="{sh}"/>
    <path d="M220 470 L220 560" stroke="#2B3A44" stroke-width="3"/>
    <rect x="215" y="540" width="10" height="18" rx="3" fill="#C9D3DC"/><circle cx="220" cy="556" r="2" fill="#2B3A44"/>
    <path d="M150 470 Q166 520 178 560" stroke="{a}" stroke-width="5" fill="none" stroke-linecap="round"/>
    <rect x="164" y="556" width="34" height="46" rx="5" fill="#F7F9FA" stroke="#C9D3DC" stroke-width="2"/><rect x="168" y="560" width="26" height="12" rx="2" fill="{a}"/>
    <rect x="170" y="578" width="22" height="3" rx="1.5" fill="#7A8A94"/><rect x="170" y="585" width="16" height="3" rx="1.5" fill="#7A8A94"/>
    <path d="M70 640 C74 590 86 560 104 540" stroke="{sh}" stroke-width="5" fill="none" stroke-linecap="round"/>
    <path d="M370 640 C366 590 354 560 336 540" stroke="{sh}" stroke-width="5" fill="none" stroke-linecap="round"/>"""
    if c["outfit_style"] == "chef_jacket":
        a = c["accent"]; o = c["outfit"]; sh = c["outfit_shade"]
        btn = ''.join(f'<circle cx="{x}" cy="{y}" r="5" fill="{c["cap"]}"/><circle cx="{x-1.5}" cy="{y-1.5}" r="1.5" fill="#FFFFFF" opacity="0.4"/>' for x0 in (196, 258) for y in (520, 560, 600) for x in [x0 + (y - 520) * 0.02])
        return f"""
    <rect x="190" y="372" width="60" height="90" rx="22" fill="{c["skin_shade"]}"/>
    <path d="M36 640 C36 524 88 464 172 446 L220 470 L268 446 C352 464 404 524 404 640 Z" fill="{o}"/>
    <path d="M180 456 Q220 488 262 456 L258 478 Q220 504 184 478 Z" fill="{a}"/>
    <path d="M206 486 L196 512 L220 500 L244 512 L234 486 Z" fill="{a}"/><circle cx="220" cy="492" r="7" fill="#A82A24"/>
    <path d="M166 446 Q220 474 274 446 L276 462 Q220 494 164 462 Z" fill="{o}" stroke="{sh}" stroke-width="3" stroke-linejoin="round"/>
    <path d="M164 462 Q200 500 268 520 L276 640" stroke="{sh}" stroke-width="3" fill="none"/>
    {btn}
    <path d="M276 640 L270 520" stroke="{c["cap"]}" stroke-width="2" opacity="0.4"/>
    <rect x="100" y="518" width="44" height="12" rx="3" fill="{sh}" opacity="0.7"/>
    <rect x="108" y="492" width="7" height="32" rx="2" fill="#2B2F36"/><rect x="107" y="490" width="9" height="6" rx="2" fill="{a}"/>
    <path d="M124 494 L124 526 M120 494 L120 504 M128 494 L128 504" stroke="#8A929B" stroke-width="2.5" stroke-linecap="round"/>
    <path d="M118 504 Q124 510 130 504" stroke="#8A929B" stroke-width="2.5" fill="none"/>
    <path d="M310 560 L330 640 L380 640 C380 600 372 570 356 550 Z" fill="#E9E4D8"/><path d="M314 576 L370 566 M320 600 L376 590" stroke="{a}" stroke-width="3" opacity="0.8"/>
    <path d="M70 640 C74 590 86 560 104 540" stroke="{sh}" stroke-width="5" fill="none" stroke-linecap="round"/>
    <path d="M370 640 C366 590 354 560 336 540" stroke="{sh}" stroke-width="5" fill="none" stroke-linecap="round"/>"""
    if c["outfit_style"] == "flannel":
        o = c["outfit"]; sh = c["outfit_shade"]
        plaid = ''.join(f'<path d="M{x} 440 L{x} 640" stroke="{sh}" stroke-width="7" opacity="0.7"/>' for x in range(52, 400, 34))
        plaid += ''.join(f'<path d="M30 {y} L410 {y}" stroke="{sh}" stroke-width="7" opacity="0.7"/>' for y in range(470, 640, 34))
        plaid += ''.join(f'<path d="M{x} 440 L{x} 640" stroke="#1E1A1A" stroke-width="1.6" opacity="0.35"/>' for x in range(69, 400, 34))
        plaid += ''.join(f'<path d="M30 {y} L410 {y}" stroke="#1E1A1A" stroke-width="1.6" opacity="0.35"/>' for y in range(487, 640, 34))
        hp = c.get("headphones", "#2B2F3A")
        return f"""
    <defs><clipPath id="fl"><path d="M36 640 C36 524 88 464 172 446 L194 520 L198 640 Z M404 640 C404 524 352 464 268 446 L246 520 L242 640 Z"/></clipPath></defs>
    <path d="M168 486 C164 430 276 430 272 486" stroke="{hp}" stroke-width="10" fill="none" stroke-linecap="round"/>
    <rect x="190" y="372" width="60" height="90" rx="22" fill="{c["skin_shade"]}"/>
    <path d="M36 640 C36 524 88 464 172 446 L220 470 L268 446 C352 464 404 524 404 640 Z" fill="{c["tee"]}"/>
    <path d="M180 448 Q220 488 260 448" stroke="{c["tee_shade"]}" stroke-width="8" fill="none"/>
    <path d="M36 640 C36 524 88 464 172 446 L194 520 L198 640 Z" fill="{o}"/><path d="M404 640 C404 524 352 464 268 446 L246 520 L242 640 Z" fill="{o}"/>
    <g clip-path="url(#fl)">{plaid}</g>
    <path d="M172 446 L152 450 L166 504 L194 520 Z" fill="{sh}"/><path d="M268 446 L288 450 L274 504 L246 520 Z" fill="{sh}"/>
    <circle cx="190" cy="556" r="3.5" fill="#F2E6CF"/><circle cx="192" cy="600" r="3.5" fill="#F2E6CF"/>
    <rect x="104" y="532" width="54" height="48" rx="4" fill="{sh}" opacity="0.6"/><path d="M102 530 L160 530 L156 546 L106 546 Z" fill="{sh}"/>
    <rect x="148" y="474" width="30" height="40" rx="12" fill="{hp}" transform="rotate(-18 163 494)"/><rect x="154" y="480" width="18" height="28" rx="8" fill="{c["accent"]}" transform="rotate(-18 163 494)"/>
    <rect x="262" y="474" width="30" height="40" rx="12" fill="{hp}" transform="rotate(18 277 494)"/><rect x="268" y="480" width="18" height="28" rx="8" fill="{c["accent"]}" transform="rotate(18 277 494)"/>
    <path d="M70 640 C74 590 86 560 104 540" stroke="{sh}" stroke-width="5" fill="none" stroke-linecap="round"/>
    <path d="M370 640 C366 590 354 560 336 540" stroke="{sh}" stroke-width="5" fill="none" stroke-linecap="round"/>"""
    if c["outfit_style"] == "bib_overalls":
        a = c["accent"]; o = c["outfit"]; sh = c["outfit_shade"]
        return f"""
    <rect x="190" y="372" width="60" height="90" rx="22" fill="{c["skin_shade"]}"/>
    <path d="M36 640 C36 524 88 464 172 446 L220 472 L268 446 C352 464 404 524 404 640 Z" fill="{c["tee"]}"/>
    <path d="M176 446 Q220 486 264 446" stroke="{c["tee_shade"]}" stroke-width="8" fill="none"/>
    <path d="M150 640 L150 532 Q150 520 162 520 L278 520 Q290 520 290 532 L290 640 Z" fill="{o}"/>
    <path d="M150 640 L150 532 Q150 520 162 520 L278 520 Q290 520 290 532 L290 640" fill="none" stroke="{a}" stroke-width="2.5" stroke-dasharray="6 5" transform="translate(0 0)"/>
    <path d="M150 536 L120 460 Q116 452 108 456 L96 462 L136 548 Z" fill="{o}"/><path d="M290 536 L320 460 Q324 452 332 456 L344 462 L304 548 Z" fill="{o}"/>
    <rect x="138" y="516" width="26" height="22" rx="4" fill="{a}"/><rect x="144" y="522" width="14" height="10" rx="2" fill="{sh}"/>
    <rect x="276" y="516" width="26" height="22" rx="4" fill="{a}"/><rect x="282" y="522" width="14" height="10" rx="2" fill="{sh}"/>
    <rect x="184" y="548" width="72" height="56" rx="5" fill="{sh}"/><path d="M184 560 L256 560" stroke="{a}" stroke-width="2.5" stroke-dasharray="5 4"/>
    <rect x="196" y="524" width="9" height="34" rx="3" fill="#F2C230"/><rect x="196" y="522" width="9" height="8" rx="3" fill="#2B2F3A"/><circle cx="200.5" cy="540" r="2" fill="#E0453A"/>
    <rect x="212" y="528" width="6" height="30" rx="2" fill="#E9C46A"/><path d="M212 528 L215 520 L218 528 Z" fill="#E8C9A0"/>
    <rect x="226" y="532" width="22" height="26" rx="4" fill="#E0453A"/><rect x="230" y="536" width="14" height="8" rx="2" fill="#2B2F3A"/><circle cx="237" cy="551" r="3.5" fill="#F4F1DE"/>
    <path d="M70 640 C74 590 86 560 104 540" stroke="{c["tee_shade"]}" stroke-width="5" fill="none" stroke-linecap="round"/>
    <path d="M370 640 C366 590 354 560 336 540" stroke="{c["tee_shade"]}" stroke-width="5" fill="none" stroke-linecap="round"/>"""
    if c["outfit_style"] == "pharmacy_tunic":
        a = c["accent"]
        return f"""
    <rect x="190" y="372" width="60" height="90" rx="22" fill="{c["skin_shade"]}"/>
    <path d="M36 640 C36 524 88 464 172 446 L220 470 L268 446 C352 464 404 524 404 640 Z" fill="{c["outfit"]}"/>
    <path d="M168 440 Q220 470 272 440 L274 458 Q220 492 166 458 Z" fill="{c["outfit"]}" stroke="{c["outfit_shade"]}" stroke-width="3" stroke-linejoin="round"/>
    <path d="M166 458 Q220 492 274 458" stroke="{a}" stroke-width="4" fill="none"/>
    <path d="M246 482 L252 640" stroke="{a}" stroke-width="4"/>
    <circle cx="258" cy="512" r="4" fill="{a}"/><circle cx="259" cy="552" r="4" fill="{a}"/><circle cx="260" cy="592" r="4" fill="{a}"/>
    <rect x="104" y="530" width="58" height="52" rx="4" fill="{c["outfit_shade"]}" opacity="0.45"/><path d="M104 530 L162 530" stroke="{a}" stroke-width="3"/>
    <rect x="118" y="506" width="7" height="32" rx="2" fill="#2B2F3A"/><rect x="117" y="504" width="9" height="6" rx="2" fill="{a}"/>
    <rect x="132" y="510" width="6" height="28" rx="2" fill="#E07A5F"/>
    <rect x="286" y="516" width="64" height="40" rx="5" fill="#FFFFFF" stroke="#BFC9CF" stroke-width="2"/><rect x="286" y="516" width="64" height="11" rx="5" fill="{a}"/><rect x="286" y="522" width="64" height="5" fill="{a}"/>
    <path d="M298 534 L304 534 L304 540 L310 540 L310 546 L304 546 L304 552 L298 552 L298 546 L292 546 L292 540 L298 540 Z" fill="#2BA84A"/>
    <rect x="316" y="536" width="28" height="4" rx="2" fill="#3D3552"/><rect x="316" y="545" width="20" height="4" rx="2" fill="#9AA6B2"/>
    <path d="M70 640 C74 590 86 560 104 540" stroke="{c["outfit_shade"]}" stroke-width="5" fill="none" stroke-linecap="round"/>
    <path d="M370 640 C366 590 354 560 336 540" stroke="{c["outfit_shade"]}" stroke-width="5" fill="none" stroke-linecap="round"/>"""
    if c["outfit_style"] == "overshirt":
        a = c["accent"]
        return f"""
    <rect x="190" y="372" width="60" height="90" rx="22" fill="{c["skin_shade"]}"/>
    <path d="M36 640 C36 524 88 464 172 446 L220 470 L268 446 C352 464 404 524 404 640 Z" fill="{c["tee"]}"/>
    <path d="M182 448 Q220 486 258 448" stroke="{c["tee_shade"]}" stroke-width="8" fill="none"/>
    <path d="M36 640 C36 524 88 464 172 446 L196 520 L200 640 Z" fill="{c["outfit"]}"/>
    <path d="M404 640 C404 524 352 464 268 446 L244 520 L240 640 Z" fill="{c["outfit"]}"/>
    <path d="M172 446 L150 448 L162 500 L196 520 Z" fill="{c["outfit_shade"]}"/><path d="M268 446 L290 448 L278 500 L244 520 Z" fill="{c["outfit_shade"]}"/>
    <path d="M200 540 L200 640 M240 540 L240 640" stroke="{c["outfit_shade"]}" stroke-width="3"/>
    <circle cx="190" cy="562" r="3.5" fill="#E9E2D6"/><circle cx="191" cy="602" r="3.5" fill="#E9E2D6"/>
    <rect x="104" y="530" width="56" height="56" rx="5" fill="{c["outfit_shade"]}" opacity="0.5"/><path d="M102 528 L162 528 L158 544 L106 544 Z" fill="{c["outfit_shade"]}"/>
    <rect x="280" y="530" width="56" height="56" rx="5" fill="{c["outfit_shade"]}" opacity="0.5"/><path d="M278 528 L338 528 L334 544 L282 544 Z" fill="{c["outfit_shade"]}"/>
    <rect x="292" y="500" width="7" height="36" rx="1.5" fill="{a}" transform="rotate(6 295 518)"/><path d="M292 500 L295.5 490 L299 500 Z" fill="#E8C9A0" transform="rotate(6 295 518)"/><rect x="292" y="532" width="7" height="5" fill="#E07A7A" transform="rotate(6 295 518)"/>
    <path d="M310 498 L322 498 L322 536 L310 536 Z" fill="#F4F4F2" stroke="#9AA0A8" stroke-width="1.5" transform="rotate(-4 316 517)"/>
    <path d="M312 506 L316 506 M312 512 L318 512 M312 518 L316 518 M312 524 L318 524" stroke="#5A606A" stroke-width="1.2" transform="rotate(-4 316 517)"/>
    <path d="M70 640 C74 590 86 560 104 540" stroke="{c["outfit_shade"]}" stroke-width="5" fill="none" stroke-linecap="round"/>
    <path d="M370 640 C366 590 354 560 336 540" stroke="{c["outfit_shade"]}" stroke-width="5" fill="none" stroke-linecap="round"/>"""
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
    if c["hair_style"] == "box_braids":
        h = c["hair"]
        hair = (f'<path d="M124 290 C108 186 168 138 222 140 C276 138 336 186 316 290 C312 250 300 226 284 212 C264 196 242 192 222 192 C202 192 176 196 156 212 C140 226 128 250 124 290 Z" fill="{h}"/>'
                + ''.join(f'<path d="M222 {150+i*2} C{222-k} {160+i*4} {222-k*1.6:.0f} {182+i*6} {222-k*2.2:.0f} {196+i*10}" stroke="#3A2A24" stroke-width="1.6" fill="none" opacity="0.35"/>' for i, k in enumerate((14, 30, 46)))
                + ''.join(f'<path d="M222 {150+i*2} C{222+k} {160+i*4} {222+k*1.6:.0f} {182+i*6} {222+k*2.2:.0f} {196+i*10}" stroke="#3A2A24" stroke-width="1.6" fill="none" opacity="0.35"/>' for i, k in enumerate((14, 30, 46)))
                + f'<path d="M222 142 L222 192" stroke="#4A3A32" stroke-width="2.5"/>'
                + f'<path d="M180 160 C196 150 212 148 216 152" stroke="#FFFFFF" stroke-width="4" fill="none" opacity="0.14" stroke-linecap="round"/>')
    elif c["hair_style"] == "curtain_lob":
        h = c["hair"]
        hair = (f'<path d="M120 300 C104 190 168 138 222 140 C276 138 340 190 320 300 C316 262 304 236 288 222 C268 206 242 198 222 198 C202 198 176 206 156 222 C140 236 126 262 120 300 Z" fill="{h}"/>'
                f'<path d="M222 194 C190 200 160 222 146 272 L132 274 C136 228 170 196 222 188 Z" fill="{h}"/>'
                f'<path d="M222 194 C254 200 282 222 294 272 L308 274 C304 228 272 196 222 188 Z" fill="{h}"/>'
                f'<path d="M222 146 L222 196" stroke="#000000" stroke-width="2" opacity="0.3"/>'
                f'<path d="M174 164 C194 152 212 150 216 156 M266 160 C288 166 304 184 310 204" stroke="#FFFFFF" stroke-width="4" fill="none" opacity="0.15" stroke-linecap="round"/>'
                f'<path d="M210 204 C184 214 164 234 154 262" stroke="#FFFFFF" stroke-width="2.5" fill="none" opacity="0.14" stroke-linecap="round"/>')
    elif c["hair_style"] == "curly_top":
        h = c["hair"]; hd = c["hair_dark"]
        hair = (f'<path d="M126 270 C120 240 124 214 138 198 C142 226 136 250 126 270 Z M314 270 C320 240 316 214 302 198 C298 226 304 250 314 270 Z" fill="{hd}" opacity="0.85"/>'
                f'<path d="M136 226 C128 178 166 150 220 148 C274 150 312 178 304 226 C292 212 266 206 220 206 C174 206 148 212 136 226 Z" fill="{h}"/>')
        import math
        for row, (cy, xs, r) in enumerate([(206, range(150, 300, 17), 13), (190, range(156, 292, 17), 15), (172, range(166, 282, 18), 16), (154, range(180, 266, 19), 16), (140, range(198, 250, 20), 14)]):
            for x in xs:
                yy = cy + abs(x - 220) * 0.18 * (1 if row else 0.4)
                hair += f'<circle cx="{x}" cy="{yy:.0f}" r="{r}" fill="{h}"/>'
                hair += f'<path d="M{x-6} {yy-3:.0f} Q{x} {yy-9:.0f} {x+6} {yy-3:.0f}" stroke="#FFFFFF" stroke-width="2" fill="none" opacity="0.13" stroke-linecap="round"/>'
    elif c["hair_style"] == "textured_crop":
        h = c["hair"]; hd = c["hair_dark"]
        hair = (f'<path d="M128 266 C122 238 126 214 140 200 C142 224 136 246 128 266 Z M312 266 C318 238 314 214 300 200 C298 224 304 246 312 266 Z" fill="{hd}"/>'
                f'<path d="M134 232 C122 168 166 132 222 130 C278 132 320 168 306 232 C298 216 284 208 268 204 C240 200 200 200 172 204 C156 208 142 216 134 232 Z" fill="{h}"/>'
                f'<path d="M150 214 C156 190 176 174 196 172 C188 186 186 198 192 210 C200 194 210 182 226 176 C222 190 224 202 232 212 C238 196 250 186 266 182 C262 194 266 206 276 214 C282 202 290 196 300 196 C302 206 302 214 298 220 C270 206 180 206 150 214 Z" fill="{h}"/>'
                + ''.join(f'<path d="M{x} {y} C{x+6} {y-14} {x+16} {y-26} {x+30} {y-34}" stroke="#FFFFFF" stroke-width="2.5" fill="none" opacity="0.14" stroke-linecap="round"/>' for x, y in [(168, 196), (196, 184), (226, 180), (254, 186)])
                + f'<path d="M170 214 C176 206 184 202 192 204 M214 212 C222 204 230 202 238 206 M258 214 C266 206 274 204 282 208" stroke="{hd}" stroke-width="2.5" fill="none" opacity="0.6" stroke-linecap="round"/>')
    elif c["hair_style"] == "twists":
        h = c["hair"]
        hair = (f'<path d="M126 276 C120 236 128 206 146 192 C150 222 140 250 126 276 Z M314 276 C320 236 312 206 294 192 C290 222 300 250 314 276 Z" fill="{h}"/>'
                f'<path d="M140 226 C132 178 168 150 220 148 C272 150 308 178 300 226 C290 210 262 202 220 202 C178 202 150 210 140 226 Z" fill="{h}"/>')
        for row, (y0, xs) in enumerate([(150, range(160, 286, 14)), (136, range(167, 280, 14)), (124, range(176, 270, 14))]):
            for x in xs:
                hgt = 34 - row * 4
                hair += (f'<rect x="{x-6}" y="{y0 + abs(x-220)//6}" width="12" height="{hgt}" rx="6" fill="{h}"/>'
                         f'<path d="M{x-3} {y0 + abs(x-220)//6 + 6} L{x+3} {y0 + abs(x-220)//6 + 12} M{x-3} {y0 + abs(x-220)//6 + 16} L{x+3} {y0 + abs(x-220)//6 + 22}" stroke="#FFFFFF" stroke-width="1.5" opacity="0.18" stroke-linecap="round"/>')
        hair += f'<path d="M150 214 C164 204 184 198 196 198" stroke="{c["skin"]}" stroke-width="2.5" fill="none" opacity="0.7" stroke-linecap="round"/>'
    elif c["hair_style"] == "trucker_cap":
        cp, cs, ms = c["cap"], c["cap_shade"], c["mesh"]
        hair = (f'<path d="M128 290 C122 262 124 240 132 224 L146 224 C140 246 136 268 128 290 Z M312 290 C318 262 316 240 308 224 L294 224 C300 246 304 268 312 290 Z" fill="{c["hair"]}"/>'
                f'<path d="M130 268 C128 256 128 246 132 236 M310 268 C312 256 312 246 308 236" stroke="{c["grey"]}" stroke-width="4" fill="none" stroke-linecap="round" opacity="0.9"/>'
                f'<path d="M126 232 C118 150 170 108 222 108 C274 108 326 150 314 232 Z" fill="{ms}"/>'
                + ''.join(f'<path d="M{x} 120 L{x} 230" stroke="#C9BFA8" stroke-width="1.2" opacity="0.7"/>' for x in range(134, 312, 7))
                + f'<path d="M150 228 C146 168 176 116 222 112 C268 116 298 168 292 228 Z" fill="{cp}"/>'
                + f'<path d="M222 112 L222 226" stroke="{cs}" stroke-width="2" opacity="0.6"/>'
                + f'<circle cx="222" cy="111" r="5" fill="{cs}"/>'
                + f'<path d="M190 162 L254 162 L254 200 L190 200 Z" fill="{ms}" rx="4"/>'
                + f'<path d="M222 194 L222 170 M222 178 Q212 170 206 174 Q214 182 222 178 M222 172 Q232 164 238 168 Q230 176 222 172 M222 186 Q212 178 206 182 Q214 190 222 186 M222 184 Q232 176 238 180 Q230 188 222 184" stroke="{cp}" stroke-width="2" fill="{cp}" stroke-linejoin="round"/>'
                + f'<path d="M118 238 C150 220 190 214 222 214 C254 214 292 220 322 238 C300 252 262 250 222 248 C182 250 140 252 118 238 Z" fill="{cs}"/>'
                + f'<path d="M124 236 C156 222 192 218 222 218 C252 218 288 222 316 236" stroke="{cp}" stroke-width="3" fill="none" opacity="0.8"/>'
                + f'<path d="M166 132 C194 118 246 118 274 130" stroke="#FFFFFF" stroke-width="4" fill="none" opacity="0.15" stroke-linecap="round"/>')
    elif c["hair_style"] == "faux_hawk":
        hd = c["hair_dark"]
        hair = (f'<path d="M128 262 C122 236 126 212 140 198 C142 222 136 244 128 262 Z M312 262 C318 236 314 212 300 198 C298 222 304 244 312 262 Z" fill="{hd}"/>'
                f'<path d="M136 230 C126 172 168 140 220 138 C272 140 314 172 304 230 C292 210 264 196 220 196 C176 196 148 210 136 230 Z" fill="{hd}"/>'
                + ''.join(f'<circle cx="{x}" cy="{y}" r="1.6" fill="#E9B994" opacity="0.35"/>' for x in range(146, 300, 11) for y in (188, 200, 212) if abs(x-220) > 40)
                + f'<path d="M178 206 C172 170 186 136 200 118 L208 130 L214 104 L224 122 L232 100 L238 124 L250 112 L252 140 C262 160 266 186 262 206 C246 198 196 198 178 206 Z" fill="{c["hair"]}"/>'
                + ''.join(f'<path d="M{x} 200 C{x+2} 176 {x+6} 152 {x+10} 132" stroke="{hd}" stroke-width="2.5" fill="none" opacity="0.5" stroke-linecap="round"/>' for x in (194, 212, 230, 246))
                + f'<path d="M204 128 C214 120 230 118 240 126" stroke="#FFFFFF" stroke-width="3" fill="none" opacity="0.25" stroke-linecap="round"/>')
    elif c["hair_style"] == "curly_pony":
        h = c["hair"]
        hair = (f'<path d="M124 286 C110 192 166 148 222 148 C280 148 332 192 316 286 C312 250 302 226 286 212 C252 200 190 200 156 212 C140 226 130 252 124 286 Z" fill="{h}"/>'
                f'<path d="M146 214 C140 176 178 150 222 148 C268 150 302 176 296 214 C272 196 172 196 146 214 Z" fill="{h}"/>'
                + ''.join(f'<path d="M{x} 206 C{x+4} 186 {x+14} 168 {x+30} 158" stroke="#FFFFFF" stroke-width="2.5" fill="none" opacity="0.14" stroke-linecap="round"/>' for x in (170, 196, 222, 248))
                + f'<path d="M134 232 C122 246 128 262 120 276 C132 270 136 254 140 240 Z M306 232 C318 246 312 262 320 276 C308 270 304 254 300 240 Z" fill="{h}"/>'
                + f'<path d="M150 208 C144 222 152 230 146 240" stroke="{h}" stroke-width="7" fill="none" stroke-linecap="round"/>')
    elif c["hair_style"] == "silver_swept":
        hd = c["hair_dark"]
        hair = (f'<path d="M124 280 C112 192 160 138 222 136 C286 136 334 188 316 280 C312 246 304 222 290 208 C256 198 188 198 154 208 C138 224 128 250 124 280 Z" fill="{c["hair"]}"/>'
                f'<path d="M138 214 C130 160 172 122 226 120 C282 120 320 156 310 210 C292 190 262 180 226 182 C190 184 160 196 138 214 Z" fill="{c["hair"]}"/>'
                + ''.join(f'<path d="M{x} 204 C{x+6} 176 {x+18} 150 {x+34} 134" stroke="{hd}" stroke-width="2.5" fill="none" opacity="0.45" stroke-linecap="round"/>' for x in (158, 182, 206, 230, 254))
                + f'<path d="M150 186 C176 150 236 132 296 158" stroke="#FFFFFF" stroke-width="4" fill="none" opacity="0.22" stroke-linecap="round"/>'
                + f'<path d="M130 262 C128 244 132 228 140 218 M310 262 C312 244 308 228 300 218" stroke="{hd}" stroke-width="4" fill="none" opacity="0.5" stroke-linecap="round"/>')
    elif c["hair_style"] == "beanie_waves":
        b, bs = c["beanie"], c["beanie_shade"]
        hair = (f'<path d="M128 300 C118 252 128 222 150 206 C152 244 142 272 128 300 Z M312 300 C322 252 312 222 290 206 C288 244 298 272 312 300 Z" fill="{c["hair"]}"/>'
                f'<path d="M150 214 C162 232 196 238 226 228 C200 246 168 248 146 236 Z" fill="{c["hair"]}"/>'
                f'<path d="M126 226 C116 150 170 108 222 108 C276 108 330 150 316 226 C290 212 256 206 220 206 C184 206 150 212 126 226 Z" fill="{b}"/>'
                + ''.join(f'<path d="M{x} {150 if abs(x-220) < 70 else 176} L{x} 214" stroke="{bs}" stroke-width="2.5" opacity="0.6"/>' for x in range(150, 296, 14))
                + f'<path d="M122 230 C150 208 190 202 220 202 C250 202 290 208 318 230 L316 206 C290 188 254 182 220 182 C186 182 150 188 124 206 Z" fill="{bs}"/>'
                + ''.join(f'<path d="M{x} {190 + abs(x-220)//14} L{x} {214 + abs(x-220)//10}" stroke="{b}" stroke-width="3" opacity="0.7"/>' for x in range(134, 310, 10))
                + f'<path d="M166 128 C196 112 246 112 276 126" stroke="#FFFFFF" stroke-width="4" fill="none" opacity="0.16" stroke-linecap="round"/>')
    elif c["hair_style"] == "crew_grey":
        hair = (f'<path d="M128 262 C122 236 126 212 140 198 C142 222 136 244 128 262 Z M312 262 C318 236 314 212 300 198 C298 222 304 244 312 262 Z" fill="{c["grey"]}"/>'
                f'<path d="M136 230 C126 172 168 140 220 138 C272 140 314 172 304 230 C292 210 264 196 220 196 C176 196 148 210 136 230 Z" fill="{c["hair"]}"/>'
                f'<path d="M142 222 C144 212 148 204 154 198 M298 222 C296 212 292 204 286 198" stroke="{c["grey"]}" stroke-width="5" fill="none" stroke-linecap="round" opacity="0.85"/>'
                f'<path d="M168 160 C198 146 244 146 274 160" stroke="#FFFFFF" stroke-width="3" fill="none" opacity="0.16" stroke-linecap="round"/>'
                + ''.join(f'<path d="M{x} 198 L{x+3} 186" stroke="{c["hair"]}" stroke-width="3" stroke-linecap="round"/>' for x in range(172, 272, 9)))
    elif c["hair_style"] == "locs_bun":
        hair = (f'<path d="M124 286 C112 196 166 150 222 150 C278 150 330 196 316 286 C310 250 300 226 282 214 C250 204 192 204 158 214 C140 228 130 252 124 286 Z" fill="{c["hair"]}"/>'
                + ''.join(f'<path d="M{x} {y0} Q{x+dx} {y0+30} {x+dx*0.4:.0f} {y0+52}" stroke="#3A2A22" stroke-width="2.5" fill="none" opacity="0.7" stroke-linecap="round"/>' for x, y0, dx in [(150, 196, -8), (172, 176, -6), (196, 164, -4), (244, 164, 4), (268, 176, 6), (290, 196, 8)])
                + f'<path d="M222 152 L222 206" stroke="#3A2A22" stroke-width="2.5" opacity="0.6"/>'
                + f'<path d="M136 230 C128 270 130 300 138 330" stroke="{c["hair"]}" stroke-width="14" fill="none" stroke-linecap="round"/><path d="M304 230 C312 270 310 300 302 330" stroke="{c["hair"]}" stroke-width="14" fill="none" stroke-linecap="round"/>')
    elif c["hair_style"] == "hijab":
        outline = "M220 140 C296 140 340 196 338 292 C336 356 342 400 362 458 C320 480 272 488 220 488 C168 488 120 480 78 458 C98 400 104 356 102 292 C100 196 144 140 220 140 Z"
        hair = (f'<path d="{outline} M220 206 C170 206 140 246 140 300 C140 360 176 400 220 400 C264 400 300 360 300 300 C300 246 270 206 220 206 Z" fill="{c["hijab"]}" fill-rule="evenodd"/>'
                f'<path d="M220 206 C170 206 140 246 140 300 C140 360 176 400 220 400 C264 400 300 360 300 300 C300 246 270 206 220 206 Z" fill="none" stroke="{c["hijab_shade"]}" stroke-width="7"/>'
                f'<path d="M160 168 C190 150 250 150 280 168" stroke="#FFFFFF" stroke-width="4" fill="none" opacity="0.14" stroke-linecap="round"/>'
                f'<path d="M130 380 C150 424 190 442 240 446 M118 414 C150 456 220 468 296 452 M318 360 C320 396 328 424 344 450" stroke="{c["hijab_shade"]}" stroke-width="4" fill="none" opacity="0.8" stroke-linecap="round"/>'
                f'<circle cx="296" cy="388" r="5" fill="{c["accent"]}"/><circle cx="294.5" cy="386.5" r="1.6" fill="#FFFFFF" opacity="0.7"/>')
    elif c["hair_style"] == "swoop":
        hair = (f'<path d="M124 282 C110 188 170 146 222 146 C284 144 334 190 316 282 C312 246 302 222 286 210 C252 202 192 202 156 210 C140 226 128 252 124 282 Z" fill="{c["hair"]}"/>'
                f'<path d="M140 226 C124 168 168 128 226 126 C286 126 324 160 318 212 C306 196 290 188 270 188 C250 190 234 198 214 210 C192 222 164 228 140 226 Z" fill="{c["hair"]}"/>'
                f'<path d="M150 212 C176 180 230 158 300 172" stroke="#FFFFFF" stroke-width="3" fill="none" opacity="0.18" stroke-linecap="round"/>'
                f'<path d="M168 196 C196 170 244 156 290 160" stroke="#FFFFFF" stroke-width="2.5" fill="none" opacity="0.12" stroke-linecap="round"/>')
    elif c["hair_style"] == "skull_cap":
        hair = (f'<path d="M128 252 C120 176 172 136 222 136 C274 136 324 176 314 252 C300 232 270 220 222 220 C174 220 142 232 128 252 Z" fill="{c["cap"]}"/>'
                f'<path d="M128 252 C142 232 174 220 222 220 C270 220 300 232 314 252 L312 238 C298 216 268 206 222 206 C176 206 144 216 130 238 Z" fill="{c["cap_shade"]}"/>'
                f'<path d="M168 162 C196 146 244 144 276 158" stroke="#FFFFFF" stroke-width="4" fill="none" opacity="0.14" stroke-linecap="round"/>'
                f'<path d="M134 256 C132 272 132 286 136 296 M306 256 C308 272 308 286 304 296" stroke="{c["hair"]}" stroke-width="7" fill="none" stroke-linecap="round"/>')
    elif c["hair_style"] == "side_braid":
        import math
        hair = (f'<path d="M124 284 C106 184 172 144 222 144 C288 142 338 190 318 286 C314 248 302 224 286 210 C254 196 190 196 156 210 C140 226 128 254 124 284 Z" fill="{c["hair"]}"/>'
                f'<path d="M220 148 C206 168 196 188 192 204" stroke="#000000" stroke-width="2" opacity="0.3" fill="none"/>'
                f'<path d="M170 172 C186 160 204 154 214 154 M232 156 C262 156 290 172 302 196" stroke="#FFFFFF" stroke-width="4" fill="none" opacity="0.16" stroke-linecap="round"/>')
        if c.get("safety_glasses"):
            hair += ('<path d="M150 196 Q220 160 290 196 L284 214 Q252 198 220 198 Q188 198 156 214 Z" fill="#CFE8F5" opacity="0.75" stroke="#2B2F3A" stroke-width="3" stroke-linejoin="round"/>'
                     '<path d="M150 198 Q140 206 132 222 M290 198 Q300 206 308 222" stroke="#2B2F3A" stroke-width="4" fill="none" stroke-linecap="round"/>'
                     '<path d="M174 196 Q196 186 214 186" stroke="#FFFFFF" stroke-width="3" fill="none" opacity="0.8" stroke-linecap="round"/>')
    elif c["hair_style"] == "flat_fade":
        hair = (f'<path d="M126 276 C120 236 128 206 146 192 C150 222 140 250 126 276 Z M314 276 C320 236 312 206 294 192 C290 222 300 250 314 276 Z" fill="{c["hair"]}" opacity="0.5"/>'
                f'<path d="M140 228 C132 176 170 150 220 148 C270 150 308 176 300 228 C290 210 262 200 220 200 C178 200 150 210 140 228 Z" fill="{c["hair"]}"/>'
                f'<path d="M178 202 C190 196 204 194 214 194" stroke="{c["skin"]}" stroke-width="2.5" fill="none" opacity="0.8" stroke-linecap="round"/>'
                f'<path d="M172 166 C200 156 240 156 268 166" stroke="#FFFFFF" stroke-width="3" fill="none" opacity="0.14" stroke-linecap="round"/>')
    elif c["hair_style"] == "asym_bob":
        hair = (f'<path d="M116 340 C94 196 168 142 222 144 C292 140 354 194 334 380 L306 386 C316 304 308 246 292 222 L152 214 C138 242 132 292 140 340 Z" fill="{c["hair"]}"/>'
                f'<path d="M146 228 C148 172 196 140 250 146 C298 152 324 190 316 252 C304 222 282 206 250 204 C214 206 182 216 146 228 Z" fill="{c["hair"]}"/>'
                f'<path d="M168 168 C194 150 236 144 270 154 M262 166 C290 176 306 200 312 230" stroke="#FFFFFF" stroke-width="4" fill="none" opacity="0.16" stroke-linecap="round"/>'
                f'<path d="M322 280 C326 310 324 340 318 370" stroke="#FFFFFF" stroke-width="3" fill="none" opacity="0.12" stroke-linecap="round"/>')
    elif c["hair_style"] == "tousled":
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
    elif c["hair_style"] == "man_bun":
        hair = (f'<path d="M124 282 C110 186 170 144 222 144 C284 142 334 188 316 282 C312 246 302 222 286 208 C252 198 192 198 156 208 C140 224 128 252 124 282 Z" fill="{c["hair"]}"/>'
                f'<path d="M154 210 C148 170 184 142 226 140 C272 140 300 166 296 204 C266 190 212 190 154 210 Z" fill="{c["hair"]}"/>'
                f'<path d="M170 196 C192 168 236 158 278 168 M184 182 C206 160 246 156 284 176 M196 206 C214 186 250 180 288 192" stroke="#FFFFFF" stroke-width="2.5" fill="none" opacity="0.16" stroke-linecap="round"/>')
    elif c["hair_style"] == "slick_back":
        hair = (f'<path d="M122 280 C108 184 168 140 222 140 C286 138 336 186 318 282 C314 246 304 222 288 208 C252 196 192 196 156 208 C140 224 128 250 122 280 Z" fill="{c["hair"]}"/>'
                f'<path d="M156 208 C150 172 182 138 226 136 C276 134 304 160 300 200 C270 186 214 186 156 208 Z" fill="{c["hair"]}"/>'
                f'<path d="M172 190 C196 160 248 152 286 166 M180 204 C206 178 250 172 292 184" stroke="#FFFFFF" stroke-width="3" fill="none" opacity="0.16" stroke-linecap="round"/>')
    elif c["hair_style"] == "short":
        hair = f'<path d="M122 282 C106 172 182 146 222 150 C298 144 338 204 318 284 C312 244 300 216 272 204 C232 216 180 216 150 208 C134 228 126 254 122 282 Z" fill="{c["hair"]}"/>'
    else:
        hair = f'<circle cx="220" cy="146" r="38" fill="{c["hair"]}"/><path d="M119 286 C104 176 188 150 228 160 C300 148 344 210 321 292 C312 250 292 226 262 216 C230 242 172 246 140 236 C128 250 122 268 119 286 Z" fill="{c["hair"]}"/>'
    glasses = '<rect x="149" y="272" width="58" height="42" rx="10" fill="none" stroke="#1B2A4A" stroke-width="5"/><rect x="233" y="272" width="58" height="42" rx="10" fill="none" stroke="#1B2A4A" stroke-width="5"/><path d="M207 289 Q220 282 233 289" stroke="#1B2A4A" stroke-width="4.5" fill="none"/><path d="M149 284 L128 280 M291 284 L312 280" stroke="#1B2A4A" stroke-width="4.5" stroke-linecap="round"/>' if c["glasses"] == "square" else '<rect x="152" y="278" width="52" height="34" rx="12" fill="none" stroke="#7A5E10" stroke-width="3"/><rect x="236" y="278" width="52" height="34" rx="12" fill="none" stroke="#7A5E10" stroke-width="3"/><path d="M204 292 Q220 286 236 292" stroke="#7A5E10" stroke-width="3" fill="none"/><path d="M152 290 L128 284 M288 290 L312 284" stroke="#7A5E10" stroke-width="3" stroke-linecap="round"/>' if c["glasses"] == "thin" else '<circle cx="178" cy="293" r="27" fill="none" stroke="#1B2A4A" stroke-width="4.5"/><circle cx="262" cy="293" r="27" fill="none" stroke="#1B2A4A" stroke-width="4.5"/><path d="M205 290 Q220 283 235 290" stroke="#1B2A4A" stroke-width="4.5" fill="none"/>' if c["glasses"] else ''
    if c["glasses"] == "wire_round":
        glasses = ('<circle cx="178" cy="293" r="25" fill="#FFFFFF" fill-opacity="0.06" stroke="#B8923A" stroke-width="2.5"/><circle cx="262" cy="293" r="25" fill="#FFFFFF" fill-opacity="0.06" stroke="#B8923A" stroke-width="2.5"/>'
                   '<path d="M203 289 Q220 281 237 289" stroke="#B8923A" stroke-width="2.5" fill="none"/><path d="M153 288 L128 282 M287 288 L312 282" stroke="#B8923A" stroke-width="2.5" stroke-linecap="round"/>')
    if c["glasses"] == "tortoise":
        glasses = ('<rect x="148" y="274" width="60" height="38" rx="7" fill="#FFFFFF" fill-opacity="0.08" stroke="#6B3E22" stroke-width="5.5"/><rect x="232" y="274" width="60" height="38" rx="7" fill="#FFFFFF" fill-opacity="0.08" stroke="#6B3E22" stroke-width="5.5"/>'
                   '<path d="M152 280 L162 276 M238 280 L250 276" stroke="#C08A4A" stroke-width="2.5" stroke-linecap="round"/>'
                   '<path d="M208 288 Q220 281 232 288" stroke="#6B3E22" stroke-width="4.5" fill="none"/><path d="M148 284 L128 280 M292 284 L312 280" stroke="#6B3E22" stroke-width="4.5" stroke-linecap="round"/>')
    if c["glasses"] == "rect_gold":
        glasses = ('<rect x="150" y="274" width="56" height="38" rx="8" fill="none" stroke="#C9963A" stroke-width="3"/><rect x="234" y="274" width="56" height="38" rx="8" fill="none" stroke="#C9963A" stroke-width="3"/>'
                   '<path d="M206 286 Q220 279 234 286" stroke="#C9963A" stroke-width="3" fill="none"/><path d="M150 284 L128 279 M290 284 L312 279" stroke="#C9963A" stroke-width="3" stroke-linecap="round"/>')
    if c["glasses"] == "round_thick":
        glasses = '<circle cx="178" cy="292" r="27" fill="none" stroke="#141418" stroke-width="6"/><circle cx="262" cy="292" r="27" fill="none" stroke="#141418" stroke-width="6"/><path d="M205 288 Q220 280 235 288" stroke="#141418" stroke-width="5" fill="none"/><path d="M151 286 L128 280 M289 286 L312 280" stroke="#141418" stroke-width="5" stroke-linecap="round"/>'
    if c["glasses"] == "browline":
        glasses = ('<rect x="150" y="276" width="56" height="36" rx="12" fill="none" stroke="#B8A27A" stroke-width="2.5"/><rect x="234" y="276" width="56" height="36" rx="12" fill="none" stroke="#B8A27A" stroke-width="2.5"/>'
                   '<path d="M150 284 Q152 274 176 274 L206 276 L206 286 M290 284 Q288 274 264 274 L234 276 L234 286" stroke="#1E1A1A" stroke-width="7" fill="none" stroke-linejoin="round"/>'
                   '<path d="M206 282 Q220 276 234 282" stroke="#B8A27A" stroke-width="3" fill="none"/><path d="M150 282 L128 278 M290 282 L312 278" stroke="#1E1A1A" stroke-width="4.5" stroke-linecap="round"/>')
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
    if c.get("goatee"):
        beard += f'<path d="M204 386 Q220 394 236 386 L234 394 Q228 400 220 400 Q212 400 206 394 Z" fill="{c["hair"]}"/>'
    blush = '0.5' if c["glasses"] else '0.25'
    if c.get("freckles"):
        beard += ''.join(f'<circle cx="{x}" cy="{y}" r="2.2" fill="#B9774E" opacity="0.6"/>' for x, y in [(146, 318), (156, 326), (168, 320), (160, 312), (274, 320), (284, 312), (292, 326), (280, 328), (208, 312), (232, 312)])
    back = ''
    if c["hair_style"] == "box_braids":
        h = c["hair"]
        back = ''.join(f'<path d="M{x} 210 C{x+d} 290 {x+d} 380 {x+d*1.3:.0f} {y}" stroke="{h}" stroke-width="12" fill="none" stroke-linecap="round"/>'
                       f'<path d="M{x} 216 C{x+d} 290 {x+d} 380 {x+d*1.3:.0f} {y-6}" stroke="#FFFFFF" stroke-width="2" fill="none" opacity="0.13" stroke-dasharray="6 6"/>'
                       for x, d, y in [(150, -40, 470), (162, -34, 488), (176, -28, 476), (290, 40, 470), (278, 34, 488), (264, 28, 476), (138, -44, 452), (302, 44, 452)])
        back += ''.join(f'<rect x="{x}" y="{y}" width="13" height="7" rx="2" fill="{c["accent"]}"/>' for x, y in [(102, 452), (346, 452), (118, 470), (330, 470)])
    if c["hair_style"] == "curtain_lob":
        h = c["hair"]
        back = (f'<path d="M124 226 C96 292 98 370 106 414 Q136 430 168 412 C174 376 170 330 160 290 Z" fill="{h}"/>'
                f'<path d="M316 226 C344 292 342 370 334 414 Q304 430 272 412 C266 376 270 330 280 290 Z" fill="{h}"/>'
                f'<path d="M112 300 Q104 350 114 398 M328 300 Q336 350 326 398" stroke="#FFFFFF" stroke-width="3" fill="none" opacity="0.13" stroke-linecap="round"/>')
    if c["hair_style"] == "curly_pony":
        import math
        h = c["hair"]
        pts = [(236 + 40 * math.cos(math.radians(t)), 98 - 34 * math.sin(math.radians(t))) for t in range(0, 360, 40)]
        back = (f'<ellipse cx="236" cy="96" rx="48" ry="40" fill="{h}"/>' + ''.join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="17" fill="{h}"/>' for x, y in pts)
                + ''.join(f'<path d="M{x-8:.0f} {y-4:.0f} Q{x:.0f} {y+6:.0f} {x+8:.0f} {y-4:.0f}" stroke="#FFFFFF" stroke-width="2.5" fill="none" opacity="0.16" stroke-linecap="round"/>' for x, y in pts[:6])
                + f'<ellipse cx="230" cy="140" rx="30" ry="10" fill="{c["accent"]}"/><path d="M206 138 Q218 146 230 138 Q242 146 254 138" stroke="#FFFFFF" stroke-width="2" fill="none" opacity="0.4"/>')
    if c["hair_style"] == "beanie_waves":
        h = c["hair"]
        back = (f'<path d="M124 220 C96 260 104 300 92 340 C80 380 100 410 92 440 C120 452 150 440 162 420 C150 380 140 330 146 280 Z" fill="{h}"/>'
                f'<path d="M316 220 C344 260 336 300 348 340 C360 380 340 410 348 440 C320 452 290 440 278 420 C290 380 300 330 294 280 Z" fill="{h}"/>'
                f'<path d="M110 300 Q100 340 110 380 Q118 410 104 432 M330 300 Q340 340 330 380 Q322 410 336 432" stroke="#FFFFFF" stroke-width="3" fill="none" opacity="0.14" stroke-linecap="round"/>'
                f'<path d="M124 330 Q112 370 126 410 M316 330 Q328 370 314 410" stroke="#000000" stroke-width="3" fill="none" opacity="0.15" stroke-linecap="round"/>')
    if c["hair_style"] == "locs_bun":
        back = (f'<ellipse cx="222" cy="128" rx="46" ry="36" fill="{c["hair"]}"/>'
                + ''.join(f'<path d="M{x} 100 Q{x+4} 128 {x} 156" stroke="#3A2A22" stroke-width="2.5" fill="none" opacity="0.7"/>' for x in (194, 210, 226, 242))
                + f'<rect x="196" y="150" width="52" height="10" rx="5" fill="{c["accent"]}"/>'
                + ''.join(f'<path d="M{x} 230 C{x+d} 300 {x+d} 360 {x+d*0.6:.0f} {y}" stroke="{c["hair"]}" stroke-width="19" fill="none" stroke-linecap="round"/><path d="M{x} 236 C{x+d} 300 {x+d} 360 {x+d*0.6:.0f} {y-6}" stroke="#FFFFFF" stroke-width="2" fill="none" opacity="0.12" stroke-dasharray="7 6"/>' for x, d, y in [(126, -6, 400), (136, -16, 424), (146, -24, 440), (314, 6, 400), (304, 16, 424), (294, 24, 440)]))
    if c["hair_style"] == "side_braid":
        bx = [326, 334, 338, 338, 334, 328, 322]
        back = f'<path d="M290 220 C326 250 336 290 330 320" stroke="{c["hair"]}" stroke-width="26" fill="none" stroke-linecap="round"/>'
        back += ''.join(f'<ellipse cx="{bx[i]}" cy="{310 + i*24}" rx="{17 - i*0.9:.1f}" ry="15" fill="{c["hair"]}" transform="rotate({-18 if i % 2 else 18} {bx[i]} {310 + i*24})"/>' for i in range(7))
        back += ''.join(f'<path d="M{bx[i]-12} {304 + i*24} Q{bx[i]} {314 + i*24} {bx[i]+12} {302 + i*24}" stroke="#FFFFFF" stroke-width="2.5" fill="none" opacity="0.15"/>' for i in range(7))
        back += f'<rect x="312" y="460" width="20" height="9" rx="4" fill="{c["accent"]}"/><path d="M314 468 Q322 492 330 468 Z" fill="{c["hair"]}"/>'
    if c["hair_style"] == "man_bun":
        back = (f'<ellipse cx="226" cy="124" rx="40" ry="32" fill="{c["hair"]}"/><path d="M200 112 Q226 96 252 112" stroke="#FFFFFF" stroke-width="3" fill="none" opacity="0.15" stroke-linecap="round"/>'
                f'<rect x="208" y="146" width="36" height="9" rx="4" fill="{c["accent"]}"/>')
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
    if c.get("earpiece"):
        ep = c["earpiece"]
        ear += (f'<path d="M322 312 C334 330 326 344 330 360 C334 376 324 388 330 404 C334 418 326 430 332 446" stroke="#D9DEE6" stroke-width="2.5" fill="none" opacity="0.9"/>'
                f'<path d="M325 320 C330 330 326 338 329 346" stroke="#D9DEE6" stroke-width="5" fill="none" stroke-dasharray="1.5 2.5" opacity="0.9"/>'
                f'<ellipse cx="318" cy="306" rx="7" ry="9" fill="{ep}"/><circle cx="317" cy="304" r="2.5" fill="#5A6070"/>')
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
