#!/usr/bin/env python3
import os
IMG_DIR = "/Users/umarmakda/Desktop/GitHub/MKD-Studio/images"
OUT_DIR = "/Users/umarmakda/Desktop/GitHub/MKD-Studio/publications/magnolia-classic/posters"
SCRATCH = "/private/tmp/claude-501/-Users-umarmakda-Desktop-GitHub/b6771f75-e812-4a00-a92b-5598f1f8c319/scratchpad"

ratio = {}
with open(os.path.join(SCRATCH, "dims.txt")) as f:
    for ln in f:
        n, w, h = ln.split(); ratio[n] = float(w)/float(h)
def img(n): return f"{IMG_DIR}/magnolia-{n}.jpg"

PPMM = 200/25.4
PW, PH = round(420*PPMM), round(594*PPMM)
MX, MT, MB = round(26*PPMM), round(24*PPMM), round(26*PPMM)
CW, CH = PW-2*MX, PH-MT-MB

BG, INK, SOFT = "#F1EDE4", "#171512", "#8b857a"
NUM = "#1d1b18"
YEL = "#E7C93B"
SERIF = "'Didot','Bodoni 72','Hoefler Text',Georgia,serif"
MONO = "'SF Mono','Menlo','Courier New',monospace"

# ---------- placement primitives (return dict with px rect) ----------
def P(id, x, y, w):
    wpx = w*CW; hpx = wpx/ratio[id]
    return dict(id=id, x=MX+x*CW, y=MT+y*CH, w=wpx, h=hpx, kind="place")

def BLEED(id, ycenter):
    wpx = PW; hpx = PW/ratio[id]
    return dict(id=id, x=0, y=ycenter*PH-hpx/2, w=wpx, h=hpx, kind="bleed")

def CELL(id, cx, cy, cw, ch):
    # contain + center inside cell (frac of CW/CH)
    cwx, chx = cw*CW, ch*CH
    if cwx/chx > ratio[id]:
        hpx = chx; wpx = hpx*ratio[id]
    else:
        wpx = cwx; hpx = wpx/ratio[id]
    x = MX+cx*CW + (cwx-wpx)/2
    y = MT+cy*CH + (chx-hpx)/2
    return dict(id=id, x=x, y=y, w=wpx, h=hpx, kind="cell")

def grid(ids, cols, rows, x0, y0, x1, y1, gx, gy):
    cw = ((x1-x0) - (cols-1)*gx)/cols
    ch = ((y1-y0) - (rows-1)*gy)/rows
    out = []
    for i, id in enumerate(ids):
        r, c = divmod(i, cols)
        cx = x0 + c*(cw+gx); cy = y0 + r*(ch+gy)
        out.append(CELL(id, cx, cy, cw, ch))
    return out

def shelf(row_ids, xs, w, baseline):
    out = []
    for id, x in zip(row_ids, xs):
        wpx = w*CW; hpx = wpx/ratio[id]
        y = MT + baseline*CH - hpx
        out.append(dict(id=id, x=MX+x*CW, y=y, w=wpx, h=hpx, kind="place"))
    return out

# ---------- plates ----------
PLATES = []

# I COVER - one photograph
PLATES.append(dict(numeral="I", section="The Portfolio", cover=True, items=[
    P("61", 0.30, 0.16, 0.48),
]))

# II THE SWING - huge verticals + motion
PLATES.append(dict(numeral="II", section="The Swing", items=[
    P("37", 0.05, 0.11, 0.44),
    P("47", 0.53, 0.11, 0.40),
    P("43", 0.33, 0.61, 0.62),
    P("42", 0.05, 0.62, 0.24),
    P("38", 0.05, 0.75, 0.24),
]))

# III IN PLAY - one panoramic bleed across the centre
PLATES.append(dict(numeral="III", section="In Play", items=[
    BLEED("39", 0.50),
    P("46", 0.05, 0.10, 0.13),
    P("09", 0.74, 0.11, 0.21),
    P("22", 0.05, 0.775, 0.26),
    P("40", 0.75, 0.775, 0.19),
]))

# IV STILL LIFE - calm aligned shelves
IV = []
IV += shelf(["66", "13", "12"], [0.05, 0.37, 0.69], 0.26, 0.46)
IV += shelf(["23", "56", "48"], [0.05, 0.37, 0.69], 0.26, 0.90)
PLATES.append(dict(numeral="IV", section="Still Life", items=IV))

# V DETAILS - museum grid; the two landscape frames (17, 20) given double-width
PLATES.append(dict(numeral="V", section="Details", items=[
    P("16", 0.03,   0.10,  0.2125),
    P("17", 0.2725, 0.10,  0.455),    # landscape, enlarged
    P("18", 0.7575, 0.10,  0.2125),
    P("19", 0.03,   0.375, 0.2125),
    P("01", 0.2725, 0.375, 0.2125),
    P("06", 0.515,  0.375, 0.2125),
    P("57", 0.7575, 0.375, 0.2125),
    P("15", 0.03,   0.61,  0.2125),
    P("69", 0.2725, 0.61,  0.2125),
    P("62", 0.515,  0.61,  0.2125),
    P("20", 0.2725, 0.84,  0.455),    # panoramic, enlarged
]))

# VI THE COMPANY - large portraits, breathing
PLATES.append(dict(numeral="VI", section="The Company", items=[
    P("34", 0.08, 0.12, 0.52),
    P("27", 0.64, 0.14, 0.30),
    P("30", 0.08, 0.48, 0.36),
    P("67", 0.52, 0.44, 0.30),
    P("65", 0.68, 0.78, 0.20),
]))

# APPENDIX THE PARTNERS - sponsors: BMW hero, paired signboards, support
PLATES.append(dict(numeral="&amp;", section="The Partners", appendix=True, items=[
    P("04", 0.05, 0.11, 0.40),   # BMW grille (hero)
    P("14", 0.56, 0.11, 0.29),   # Cairns Cup bag
    P("10", 0.60, 0.45, 0.34),   # SGH Events board
    P("32", 0.05, 0.60, 0.26),   # Yorkshire Flooring sign
    P("33", 0.34, 0.60, 0.26),   # Marriott Bonvoy sign
    P("07", 0.66, 0.66, 0.24),   # Club Car
]))

# ---------- validator ----------
def validate():
    ok = True
    gapmin = 0.010 * CH
    for idx, pl in enumerate(PLATES, 1):
        rs = [it for it in pl["items"] if it["kind"] != "bleed"]
        for it in rs:
            if it["x"]+it["w"] > PW-MX+2 or it["y"]+it["h"] > PH-MB+2 or it["x"] < MX-2 or it["y"] < MT-2:
                # allow small tolerance; grids/bleeds excepted already
                if it["kind"] != "cell":
                    print(f"  ! plate {idx} {it['id']} out of margin box"); ok = False
        for i in range(len(rs)):
            for j in range(i+1, len(rs)):
                a, b = rs[i], rs[j]
                ox = min(a["x"]+a["w"], b["x"]+b["w"]) - max(a["x"], b["x"])
                oy = min(a["y"]+a["h"], b["y"]+b["h"]) - max(a["y"], b["y"])
                if ox > gapmin and oy > gapmin:
                    print(f"  ! plate {idx} OVERLAP {a['id']} & {b['id']}"); ok = False
    print("VALIDATE:", "clean" if ok else "ISSUES")
validate()

# ---------- html ----------
def imtag(it):
    return (f'<img class="ph" src="{img(it["id"])}" style="left:{it["x"]:.1f}px;top:{it["y"]:.1f}px;'
            f'width:{it["w"]:.1f}px;height:{it["h"]:.1f}px">')

def txt(left, top, html, size, fam, track, color, lh=None, align="left", weight=400):
    lh = lh or size
    a = f"right:{PW-left:.0f}px;text-align:right" if align == "right" else f"left:{left:.0f}px"
    tt = "text-transform:uppercase;" if fam == MONO else ""
    return (f'<div style="position:absolute;{a};top:{top:.0f}px;font-family:{fam};{tt}'
            f'font-size:{size:.0f}px;line-height:{lh:.0f}px;letter-spacing:{track:.1f}px;'
            f'font-weight:{weight};color:{color}">{html}</div>')

def chrome(pl, folio):
    e = []
    ytop = round(9*PPMM)
    # yellow motif square, far top-left
    ysq = round(5.5*PPMM)
    e.append(f'<div style="position:absolute;left:{MX}px;top:{ytop+round(4*PPMM)}px;'
             f'width:{ysq}px;height:{ysq}px;background:{YEL}"></div>')
    # oversized roman numeral
    numx = MX + round(11*PPMM)
    e.append(txt(numx, ytop-round(4*PPMM), pl["numeral"], round(20*PPMM), SERIF, 0, NUM, lh=round(20*PPMM)))
    # whisper title beside numeral
    tx = numx + round(30*PPMM)
    e.append(txt(tx, ytop, "Magnolia&nbsp;Golf&nbsp;Classic", round(2.9*PPMM), MONO, round(2.1*PPMM), SOFT, lh=round(4.6*PPMM)))
    e.append(txt(tx, ytop+round(5*PPMM), "SGH&nbsp;Events&nbsp;&middot;&nbsp;2026", round(2.9*PPMM), MONO, round(2.1*PPMM), SOFT, lh=round(4.6*PPMM)))
    # section + folio right
    e.append(txt(PW-MX, ytop, pl["section"], round(2.9*PPMM), MONO, round(2.1*PPMM), SOFT, lh=round(4.6*PPMM), align="right"))
    e.append(txt(PW-MX, ytop+round(5*PPMM), folio, round(2.9*PPMM), MONO, round(2.1*PPMM), SOFT, lh=round(4.6*PPMM), align="right"))
    # thin rule
    ruley = ytop + round(15*PPMM)
    e.append(f'<div style="position:absolute;left:{MX}px;top:{ruley}px;width:{CW}px;height:1px;background:{INK};opacity:.28"></div>')
    # vertical url footer
    e.append(f'<div style="position:absolute;right:{round(10*PPMM)}px;bottom:{MB}px;writing-mode:vertical-rl;'
             f'font-family:{MONO};font-size:{round(3.0*PPMM)}px;letter-spacing:{round(1.4*PPMM)}px;color:{SOFT}">mkdstudio.net</div>')
    return "".join(e)

def cover_caption():
    cy = round(MT + 0.685*CH)
    line = txt(0, cy, "The&nbsp;Magnolia&nbsp;Portfolio", round(3.0*PPMM), MONO, round(3.0*PPMM), SOFT, align="left")
    # centered manually
    return (f'<div style="position:absolute;left:0;right:0;top:{cy}px;text-align:center;font-family:{MONO};'
            f'text-transform:uppercase;font-size:{round(3.0*PPMM)}px;letter-spacing:{round(3.4*PPMM)}px;color:{SOFT}">'
            f'Magnolia&nbsp;Golf&nbsp;Classic&nbsp;&nbsp;/&nbsp;&nbsp;2026</div>')

CSS = f"""*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{background:#2f2f2f}}
.page{{position:relative;width:{PW}px;height:{PH}px;background:{BG};overflow:hidden;color:{INK}}}
.ph{{position:absolute;object-fit:cover;display:block;background:#e6e2d8}}"""

os.makedirs(OUT_DIR, exist_ok=True)
for idx, pl in enumerate(PLATES, 1):
    body = "".join(imtag(it) for it in pl["items"])
    folio = "Appendix" if pl.get("appendix") else f"Plate&nbsp;{pl['numeral']}&nbsp;/&nbsp;VI"
    ch = chrome(pl, folio)
    cap = cover_caption() if pl.get("cover") else ""
    html = (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head>'
            f'<body><div class="page">{body}{ch}{cap}</div></body></html>')
    with open(os.path.join(OUT_DIR, f"plate-{idx:02d}.html"), "w") as f:
        f.write(html)
    print(f"plate-{idx:02d}  {pl['section']:14s} items={len(pl['items'])}")
