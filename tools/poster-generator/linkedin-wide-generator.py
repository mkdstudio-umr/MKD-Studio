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

W, H = 3200, 1800
M = 140
CW, CH = W-2*M, H-2*M
BG, INK, SOFT = "#F1EDE4", "#171512", "#8b857a"
NUM, YEL = "#1d1b18", "#E7C93B"
SERIF = "'Didot','Bodoni 72','Hoefler Text',Georgia,serif"
MONO = "'SF Mono','Menlo','Courier New',monospace"

# native-ratio, zero-crop placement (x,y frac of CW/CH; w frac of CW)
def ph(id, x, y, w):
    wpx = w*CW; hpx = wpx/ratio[id]
    return (f'<img class="ph" src="{img(id)}" style="left:{M+x*CW:.1f}px;top:{M+y*CH:.1f}px;'
            f'width:{wpx:.1f}px;height:{hpx:.1f}px">')

IMGS = [
    ("39", 0.37, 0.10, 0.40),   # panoramic fairway hero
    ("37", 0.79, 0.06, 0.175),  # B&W swing, tall
    ("66", 0.37, 0.66, 0.26),   # gold wedges
    ("69", 0.66, 0.63, 0.11),   # Masters flag (yellow echo)
    ("22", 0.79, 0.63, 0.20),   # putt shadow
]
body = "".join(ph(*t) for t in IMGS)

def T(x, y, html, size, fam, track, color, lh=None, align="left", weight=400):
    lh = lh or size
    a = f"right:{W-x:.0f}px;text-align:right" if align == "right" else f"left:{x:.0f}px"
    tt = "text-transform:uppercase;" if fam == MONO else ""
    return (f'<div style="position:absolute;{a};top:{y:.0f}px;font-family:{fam};{tt}'
            f'font-size:{size}px;line-height:{lh}px;letter-spacing:{track}px;font-weight:{weight};'
            f'color:{color}">{html}</div>')

el = []
# --- header chrome, matching the plates ---
el.append(f'<div style="position:absolute;left:{M}px;top:{M-6}px;width:26px;height:26px;background:{YEL}"></div>')
el.append(T(M+44, M-12, "Magnolia&nbsp;Golf&nbsp;Classic", 23, MONO, 5, SOFT, lh=30))
el.append(T(M+44, M+12, "SGH&nbsp;Events&nbsp;&middot;&nbsp;2026", 23, MONO, 5, SOFT, lh=30))
el.append(T(W-M, M-12, "The&nbsp;Magnolia&nbsp;Portfolio", 23, MONO, 5, SOFT, lh=30, align="right"))
el.append(T(W-M, M+12, "Six&nbsp;Plates&nbsp;&middot;&nbsp;I&ndash;VI", 23, MONO, 5, SOFT, lh=30, align="right"))
el.append(f'<div style="position:absolute;left:{M}px;top:{M+52}px;width:{CW}px;height:1px;background:{INK};opacity:.28"></div>')

# --- left title block, whisper Didot + CTA ---
tx = M
el.append(T(tx, 640, "Magnolia<br>Golf&nbsp;Classic", 92, SERIF, 0.5, INK, lh=90))
el.append(f'<div style="position:absolute;left:{tx}px;top:855px;width:230px;height:2px;background:{INK};opacity:.85"></div>')
el.append(T(tx, 884, "2026&nbsp;&nbsp;&middot;&nbsp;&nbsp;SGH&nbsp;Events", 23, MONO, 5, SOFT, lh=30))
el.append(T(tx, 940, "Read&nbsp;the&nbsp;edition&nbsp;&nbsp;&middot;&nbsp;&nbsp;mkdstudio.net", 25, MONO, 4.5, INK, lh=30))

CSS = f"""*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{background:#2f2f2f}}
.page{{position:relative;width:{W}px;height:{H}px;background:{BG};overflow:hidden;color:{INK}}}
.ph{{position:absolute;object-fit:cover;display:block;background:#e6e2d8}}"""

html = (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head>'
        f'<body><div class="page">{body}{"".join(el)}</div></body></html>')
with open(os.path.join(OUT_DIR, "linkedin-wide.html"), "w") as f:
    f.write(html)
print("linkedin-wide.html rewritten", W, "x", H)
