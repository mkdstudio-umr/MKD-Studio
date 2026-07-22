#!/usr/bin/env python3
"""
mkd STUDIO Journal - volume frontispiece card generator (LOCKED DESIGN).

Renders one restrained editorial "frontispiece" share card per Journal volume:
  header (mkd STUDIO / JOURNAL 0NN / MONTH YEAR)  ->  Cormorant volume title
  -> description paragraph (the volume's written thread)
  -> full-width balanced 3+3 photo grid of the six essay photos (natural ratio,
     no crop, flat, narrow consistent gaps)  ->  two-column contents (small light
     Jost numbers + Cormorant titles, no heading)  ->  footer "mkdstudio.net/journal"

Palette: warm ivory / near-black / muted grey ONLY. No yellow, no shadows, no
decorative accents, no dot separators. Fonts: Cormorant + Jost (bundled TTFs,
read directly by PIL - do NOT rely on system fonts or @font-face; headless
Chrome ignores both).

Data source: parsed live from ../../journal/index.html so it always reflects the
current volumes/essays/photos. Output: ../../images/cards/volume-0NN.jpg (2960px
wide, portrait, ~2x).

Usage:
  python3 generate.py 001 002        # specific volumes
  python3 generate.py all            # every volume
"""
import os, re, sys, html as htmlmod
from itertools import combinations
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
IMGDIR = os.path.join(ROOT, "images")
CARDS = os.path.join(IMGDIR, "cards")
COR = os.path.join(HERE, "cormorant.ttf")
JOST = os.path.join(HERE, "jost.ttf")

# ---- locked visual tokens ----
IVORY = (241, 237, 228)      # #F1EDE4
INK   = (35, 32, 27)
GREY  = (122, 116, 105)
FAINT = (176, 169, 156)
W, M = 2960, 280
CW = W - 2 * M
MONTHYEAR = os.environ.get("MKD_CARD_DATE", "2026")   # year only; override if needed

# ---- parse volumes from the live journal index ----
def parse_volumes():
    html = open(os.path.join(ROOT, "journal/index.html")).read()
    names = {m.group(1): m.group(2).strip()
             for m in re.finditer(r'<a href="#vol-(\d+)"[^>]*>.*?<em>(.*?)</em></a>', html, re.S)}
    vols = []
    for b in re.split(r'<div class="j-vol reveal" id="vol-', html)[1:]:
        num = b[:3]
        tm = re.search(r'<p class="vol-desc">(.*?)</p>', b, re.S)
        thread = tm.group(1).strip() if tm else ""
        rr = re.compile(
            r'<a class="j-row reveal" href="/journal/(?P<slug>[^"]+?)/">.*?'
            r'src="/images/(?P<img>[^"]+?)"(?:\s+srcset="[^"]*?")?[^>]*?alt="[^"]*?">.*?'
            r'<span class="jno">(?P<jno>[^<]+?)</span><h3>(?P<title>[^<]+?)</h3>', re.S)
        essays = [{k: (v or "").strip() for k, v in m.groupdict().items()} for m in rr.finditer(b)]
        for e in essays:
            e["img"] = e["img"].split("?")[0]   # drop ?v=N cache-bust suffix
        vols.append({"num": num, "name": names.get(num, ""), "thread": thread, "essays": essays})
    return {v["num"]: v for v in vols}

# ---- helpers ----
def font(path, size, weight=None):
    f = ImageFont.truetype(path, size)
    if weight is not None:
        try: f.set_variation_by_axes([weight])
        except Exception: pass
    return f

def tracked(d, xy, text, fnt, fill, track=0):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=fnt, fill=fill, anchor="la")
        x += d.textlength(ch, font=fnt) + track

def wrap(d, text, fnt, maxw):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= maxw: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def imsize(fn):
    with Image.open(os.path.join(IMGDIR, fn)) as im: return im.size

def paste(base, fn, x, y, w, h):
    base.paste(Image.open(os.path.join(IMGDIR, fn)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y))

# ---- render one volume ----
def build(v):
    num, name = v["num"], htmlmod.unescape(v["name"])
    desc = htmlmod.unescape(v["thread"])
    es = v["essays"]
    assert len(es) == 6, f"volume {num} has {len(es)} essays, expected 6"

    d0 = ImageDraw.Draw(Image.new("RGB", (W, 10)))
    desc_f = font(COR, 41, 400); desc_lh = 60
    desc_lines = wrap(d0, desc, desc_f, 1640)

    r = [imsize(e["img"])[0] / imsize(e["img"])[1] for e in es]
    best = min(combinations(range(6), 3),
               key=lambda c: abs(sum(r[i] for i in c) - sum(r[i] for i in range(6) if i not in c)))
    rowA, rowB = sorted(best), sorted(i for i in range(6) if i not in best)
    GAP = 30
    CAP_H = 1120  # max row height; portrait-heavy volumes get a centered (inset) grid
    hf = lambda idx, gw: (gw - 2 * GAP) / sum(r[i] for i in idx)
    hA_full, hB_full = hf(rowA, CW), hf(rowB, CW)
    if max(hA_full, hB_full) > CAP_H:
        taller = rowA if hA_full >= hB_full else rowB
        GW = round(CAP_H * sum(r[i] for i in taller) + 2 * GAP)
    else:
        GW = CW
    GX = M + (CW - GW) // 2
    hA, hB = round(hf(rowA, GW)), round(hf(rowB, GW))

    y_title, y_desc = 604, 764
    desc_bottom = y_desc + len(desc_lines) * desc_lh
    rowA_top = desc_bottom + 96
    rowB_top = rowA_top + hA + GAP
    grid_bottom = rowB_top + hB
    contents_top = grid_bottom + 150
    step = 108
    H = contents_top + 3 * step + 300

    img = Image.new("RGB", (W, H), IVORY)
    d = ImageDraw.Draw(img)

    tracked(d, (M, 300), "mkd STUDIO", font(JOST, 46, 300), INK, 24)
    tracked(d, (M, 398), f"JOURNAL {num}", font(JOST, 25, 400), GREY, 8.5)
    tracked(d, (M, 444), MONTHYEAR, font(JOST, 25, 400), GREY, 8.5)

    d.text((M - 2, y_title), name, font=font(COR, 92, 500), fill=INK, anchor="la")
    yy = y_desc
    for ln in desc_lines:
        d.text((M, yy), ln, font=desc_f, fill=GREY, anchor="la"); yy += desc_lh

    for idxs, top, h in ((rowA, rowA_top, hA), (rowB, rowB_top, hB)):
        x = GX
        for i in idxs:
            w = round(h * r[i]); paste(img, es[i]["img"], x, top, w, h); x += w + GAP

    num_f = font(JOST, 26, 300)
    def fit(text, avail):
        for s in range(50, 39, -2):
            f = font(COR, s, 500)
            if d.textlength(text, font=f) <= avail:
                return f
        return font(COR, 40, 500)
    def col(entries, cx, avail):
        yy = contents_top
        for e in entries:
            n = e["jno"].replace("Journal ", "")
            t = htmlmod.unescape(e["title"])
            d.text((cx, yy + 10), n, font=num_f, fill=FAINT, anchor="la")
            d.text((cx + 78, yy), t, font=fit(t, avail), fill=INK, anchor="la")
            yy += step
    col(es[:3], M, 1180 - 78 - 14)            # col1: stop before col2
    col(es[3:], M + 1180, (W - M) - (M + 1180 + 78) - 6)

    tracked(d, (M, H - 190), "mkdstudio.net/journal", font(JOST, 28, 400), GREY, 5.6)

    os.makedirs(CARDS, exist_ok=True)
    out = os.path.join(CARDS, f"volume-{num}.jpg")
    img.save(out, quality=90)
    print(f"volume-{num}  {W}x{H}  rows={hA},{hB}  desc={len(desc_lines)}L  -> {out}")

if __name__ == "__main__":
    vols = parse_volumes()
    args = sys.argv[1:] or ["all"]
    nums = sorted(vols) if args == ["all"] else [f"{int(a):03d}" for a in args]
    for n in nums:
        build(vols[n])
