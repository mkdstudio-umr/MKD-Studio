# mkd STUDIO — Editorial Poster Generator

Reusable pipeline for mkd multi-plate poster series. First built for the Magnolia
Golf Classic 2026 set (6 A2 narrative plates I–VI + an appendix, plus a 16:9 LinkedIn
hero). See `../../projects/.../memory/project_editorial_poster_system.md` for the
locked art-direction concept.

## The concept (in short)
A poster set is a **publication, not a collage**. Curate the strongest frames, give
each **plate its own layout identity** that reinforces its title, use dramatic scale
hierarchy, allow 40–50% negative space, and keep typography a whisper so the
photography dominates. Every photo is used at its **native aspect ratio, zero crop**.

Recurring motif on every plate: oversized quiet Didot numeral (an `&` for the
appendix), a tiny brand-yellow square (`#E7C93B`), one thin hairline rule, a whisper
mono wordmark + folio, and a vertical `mkdstudio.net`.

Palette: warm off-white paper `#F1EDE4`, ink `#171512`, muted grey `#8b857a`.

## Pipeline (macOS, no ImageMagick — uses sips + headless Chrome)

1. **Measure images** → `dims.txt` (`id w h` per line):
   ```sh
   cd <images-dir>
   for f in $(ls magnolia-[0-9][0-9].jpg | sort -V); do
     d=$(sips -g pixelWidth -g pixelHeight "$f" | awk '/pixelWidth/{w=$2}/pixelHeight/{h=$2}END{print w" "h}')
     echo "$(echo $f|sed 's/[^0-9]//g;s/^0*//') $d"
   done > dims.txt
   ```
   (See `dims.example.txt`. `ratio = w/h`; >1 = landscape, <1 = portrait.)

2. **Edit `plate-generator.py`**: set `IMG_DIR`, `OUT_DIR`, dims path. Define plates via
   `P(id,x,y,w)` (native-ratio place, x/w = frac of content width, y = frac of content
   height), `BLEED(id,ycenter)` (full-width panoramic), `CELL`/`grid` (contain+center
   museum grid), `shelf(ids,xs,w,baseline)` (bottom-aligned still-life row). A built-in
   **validator** flags any overlap (min gap enforced) or margin overflow — keep it "clean".

3. **Render** each plate HTML → PNG at A2 200dpi (3307×4677):
   ```sh
   "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu \
     --hide-scrollbars --force-device-scale-factor=1 --screenshot="plate-01.png" \
     --window-size=3307,4677 "file://<abs>/plate-01.html"
   ```
   (Chrome resets cwd between Bash calls — always use absolute `file://` paths.)

4. **Combine to print PDF** (true A2 `@page{size:420mm 594mm;margin:0}`, one PNG per page,
   `--print-to-pdf --no-pdf-header-footer`).

5. **LinkedIn hero**: `linkedin-wide-generator.py` → 3200×1800 (2× of 1600×900), same
   quiet system, curated cluster, CTA `READ THE EDITION · mkdstudio.net`.

## Plate archetypes (mix & match; vary rhythm/counts so no two pages repeat)
- **Cover** — one photograph only, ~50% empty, small masthead.
- **Action/Swing** — two huge verticals + a motion strip (dramatic B&W).
- **Panoramic** — one image bleeding full-width across the centre, tiny corner satellites.
- **Still Life** — objects on shared baselines ("shelves"), calm, product feel.
- **Details** — museum grid of small crops; give **landscape frames double-width** so
  they don't float small among portraits.
- **People** — a few large portraits, lots of air.
- **Appendix (Partners/sponsors)** — no numeral (oversized `&`), folio reads "Appendix";
  brand frames with legible logos, one hero + paired signboards.
