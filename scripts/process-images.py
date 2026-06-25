#!/usr/bin/env python3
"""
process-images.py — resize study images for mkd STUDIO.

Handles EXIF orientation correctly for Fujifilm (and all camera bodies):
  - Reads the EXIF orientation tag from the source file
  - Applies the physical rotation to the pixel data via sips
  - Strips the orientation tag so browsers see a clean file
  - Resizes to 1500px long edge

Usage:
  python3 scripts/process-images.py <source.jpg> <dest.jpg>
  python3 scripts/process-images.py <source_dir/> <dest_dir/>

Examples:
  # Single file
  python3 scripts/process-images.py ~/Desktop/mkd/A7400813.JPG images/mkd-home-07.jpg

  # Whole folder (processes all JPEGs, outputs to dest dir)
  python3 scripts/process-images.py ~/Desktop/mkd/study/ images/
"""

import struct, subprocess, sys, os, shutil, tempfile

MAX_LONG_EDGE = 1500

ROTATE_FOR_ORIENTATION = {
    # EXIF value: degrees CW to rotate pixel data so image is upright
    3: 180,
    6: 90,   # 90° CW stored → rotate 90° CW to fix
    8: 270,  # 90° CCW stored → rotate 270° CW (= 90° CCW) to fix
}


def read_exif_orientation(path):
    """Return the EXIF orientation tag value (1–8), or 1 if absent/unreadable."""
    try:
        with open(path, 'rb') as f:
            data = f.read(65536)
        i = 2  # skip SOI marker
        while i < len(data) - 3:
            if data[i] != 0xFF:
                break
            marker = data[i + 1]
            seg_len = struct.unpack_from('>H', data, i + 2)[0]
            if marker == 0xE1:  # APP1 = EXIF
                exif_start = i + 4
                if data[exif_start:exif_start + 6] == b'Exif\x00\x00':
                    tiff = exif_start + 6
                    bo = data[tiff:tiff + 2]
                    big = (bo == b'MM')
                    fmt = '>' if big else '<'
                    ifd_off = struct.unpack_from(fmt + 'I', data, tiff + 4)[0]
                    ifd = tiff + ifd_off
                    num = struct.unpack_from(fmt + 'H', data, ifd)[0]
                    for e in range(num):
                        entry = ifd + 2 + e * 12
                        if entry + 12 > len(data):
                            break
                        tag = struct.unpack_from(fmt + 'H', data, entry)[0]
                        if tag == 0x0112:
                            return struct.unpack_from(fmt + 'H', data, entry + 8)[0]
            i += 2 + seg_len
    except Exception:
        pass
    return 1


def process(src, dest):
    os.makedirs(os.path.dirname(dest) if os.path.dirname(dest) else '.', exist_ok=True)

    # Step 1: resize to 1500px long edge via sips
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
        tmp_path = tmp.name
    try:
        subprocess.run(
            ['sips', '-Z', str(MAX_LONG_EDGE), src, '--out', tmp_path],
            check=True, capture_output=True
        )

        # Step 2: read orientation from the resized file (sips preserves EXIF)
        ori = read_exif_orientation(tmp_path)
        degrees = ROTATE_FOR_ORIENTATION.get(ori)

        if degrees:
            # Step 3: rotate pixel data in place
            subprocess.run(
                ['sips', '--rotate', str(degrees), tmp_path],
                check=True, capture_output=True
            )
            # Step 4: strip orientation tag (set to 1 = upright)
            subprocess.run(
                ['sips', '-s', 'orientation', '1', tmp_path],
                check=True, capture_output=True
            )

        shutil.move(tmp_path, dest)
        dims = subprocess.run(
            ['sips', '-g', 'pixelWidth', '-g', 'pixelHeight', dest],
            capture_output=True, text=True
        ).stdout
        w = next((l.split()[-1] for l in dims.splitlines() if 'pixelWidth' in l), '?')
        h = next((l.split()[-1] for l in dims.splitlines() if 'pixelHeight' in l), '?')
        print(f'  {os.path.basename(src)} → {os.path.basename(dest)}  [{w}×{h}]  EXIF ori={ori}')
    except Exception as e:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise e


def is_image(name):
    return name.lower().endswith(('.jpg', '.jpeg'))


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)

    src, dest = sys.argv[1], sys.argv[2]

    if os.path.isdir(src):
        os.makedirs(dest, exist_ok=True)
        files = sorted(f for f in os.listdir(src) if is_image(f) and not f.startswith('._'))
        for f in files:
            process(os.path.join(src, f), os.path.join(dest, f.lower().replace(' ', '-')))
    elif os.path.isfile(src):
        process(src, dest)
    else:
        print(f'Error: {src} not found')
        sys.exit(1)


if __name__ == '__main__':
    main()
