# Journal volume frontispiece cards

Generates one restrained editorial **frontispiece** share card per Journal
volume (for LinkedIn / link previews). Locked design — treat changes as a
deliberate redesign, not a tweak.

## Run
```
cd tools/journal-cards
python3 generate.py 001 002      # specific volumes
python3 generate.py all          # every volume
```
Output: `images/cards/volume-0NN.jpg` (2960px wide, portrait, ~2x).
Volume data is parsed live from `journal/index.html`, so cards always match the
current volumes/essays/photos. Date string via `MKD_CARD_DATE` env (default
`JULY 2026`).

## Locked design
- **Palette only:** warm ivory `#F1EDE4`, near-black `(35,32,27)`, muted grey
  `(122,116,105)`, faint grey `(176,169,156)`. No yellow, no shadows, no
  decorative accents, no dot separators. Photos sit flat.
- **Type:** Cormorant (title, description, contents titles) + Jost (wordmark,
  labels, numbers, footer). Bundled `cormorant.ttf` / `jost.ttf` are read
  **directly by PIL** — headless Chrome ignores both `@font-face` and installed
  system fonts, so PIL rendering is the reliable path.
- **Brand mark:** `mkd STUDIO` in Jost 300 with .52em tracking (matches the site
  `.mark`).
- **Structure (top to bottom):** header `mkd STUDIO / JOURNAL 0NN / MONTH YEAR`
  -> Cormorant volume name (book-title scale) -> description paragraph (the
  volume's written thread, `vol-desc`) -> full-width **balanced 3+3 photo grid**
  of the six essay photos (natural ratio, no crop, justified rows auto-balanced
  to near-equal height, 30px gaps) -> two-column contents (small light Jost
  number + Cormorant title, no "THE SIX ESSAYS" heading) -> footer
  `mkdstudio.net/journal`.
- Generous margins, intentional negative space. Canvas height is dynamic.

## Photos
All six essay photographs are used exactly as supplied — never cropped, altered,
regenerated or filtered. The 3+3 split is chosen to minimise row-height
difference (the squarest image pairs with the two narrowest portraits).

## Wiring to the site
Each `/journal/volume-0NN/` page's `og:image` should point at
`https://mkdstudio.net/images/cards/volume-0NN.jpg` so the link unfurls with its
frontispiece. (Pages currently fall back to the volume's lead photo until the
cards are wired.)

Distinct from `tools/poster-generator/` (publication plates + Magnolia LinkedIn
montage), which uses Didot/mono and the yellow/rule motif.
