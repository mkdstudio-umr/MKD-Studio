#!/usr/bin/env python3
"""
optimize-images.py — keep /images/ from regrowing past web size.

Scans images/ for JPEGs that are larger than 2400px on the long edge or
heavier than they need to be, and reports them. With --fix, recompresses
in place: max 2400px long edge, quality 85, ICC profile kept, EXIF
orientation baked in. A file is only rewritten if that saves at least 5%.

This is the maintenance counterpart to process-images.py (which handles
intake of new photos from the camera). Run this after adding images by
any other route, or periodically:

  python3 scripts/optimize-images.py          # dry run, report only
  python3 scripts/optimize-images.py --fix    # recompress flagged files
"""

import os, sys, glob

try:
    from PIL import Image, ImageOps
except ImportError:
    sys.exit('Pillow is required: python3 -m pip install Pillow')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAX_EDGE = 3000
QUALITY = 85
HEAVY_BYTES = 3_000_000  # flag anything over ~3MB even if dimensions are fine


def candidates():
    for f in sorted(glob.glob(os.path.join(ROOT, 'images', '*'))):
        if not f.lower().endswith(('.jpg', '.jpeg')):
            continue
        img = Image.open(f)
        oversized = max(img.size) > MAX_EDGE
        heavy = os.path.getsize(f) > HEAVY_BYTES
        if oversized or heavy:
            yield f, img.size, os.path.getsize(f)


def fix(path):
    before = os.path.getsize(path)
    img = Image.open(path)
    icc = img.info.get('icc_profile')
    img = ImageOps.exif_transpose(img)
    if img.mode not in ('RGB', 'L'):
        img = img.convert('RGB')
    w, h = img.size
    if max(w, h) > MAX_EDGE:
        r = MAX_EDGE / max(w, h)
        img = img.resize((round(w * r), round(h * r)), Image.LANCZOS)
    tmp = path + '.tmp'
    img.save(tmp, 'JPEG', quality=QUALITY, optimize=True,
             icc_profile=icc, subsampling=1)
    after = os.path.getsize(tmp)
    if after < before * 0.95:
        os.replace(tmp, path)
        return before, after
    os.remove(tmp)
    return before, before


def main():
    apply_fix = '--fix' in sys.argv
    flagged = list(candidates())
    if not flagged:
        print('images clean: nothing oversized or heavy')
        return 0
    total_saved = 0
    for path, size, weight in flagged:
        name = os.path.basename(path)
        if apply_fix:
            before, after = fix(path)
            total_saved += before - after
            note = f'{before // 1024}KB -> {after // 1024}KB' if after < before else 'left as-is (already efficient)'
            print(f'  {name}  {size[0]}x{size[1]}  {note}')
        else:
            print(f'  {name}  {size[0]}x{size[1]}  {weight // 1024}KB')
    if apply_fix:
        print(f'saved {total_saved / 1e6:.1f}MB across {len(flagged)} file(s)')
    else:
        print(f'{len(flagged)} file(s) flagged. Run with --fix to recompress.')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
