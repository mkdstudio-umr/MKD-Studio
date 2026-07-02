#!/usr/bin/env python3
"""
check-sitemap.py — flag drift between the site's pages and sitemap.xml.

Walks every index.html in the repo and compares against sitemap.xml, both ways:
  - pages that exist but are missing from the sitemap
  - sitemap entries that point at pages which no longer exist

Pages whose <head> carries a noindex robots meta are excluded (readers etc).

Usage (from the repo root):
  python3 scripts/check-sitemap.py

Exit code 0 = clean, 1 = drift found (usable in CI or a pre-push hook).
"""

import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://mkdstudio.net'


def site_pages():
    pages = set()
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d != 'scripts']
        if 'index.html' not in filenames:
            continue
        path = os.path.join(dirpath, 'index.html')
        with open(path, encoding='utf-8', errors='replace') as f:
            head = f.read(4096)
        if 'noindex' in head:
            continue
        rel = os.path.relpath(dirpath, ROOT)
        url = f'{BASE}/' if rel == '.' else f'{BASE}/{rel}/'
        pages.add(url)
    return pages


def sitemap_urls():
    with open(os.path.join(ROOT, 'sitemap.xml'), encoding='utf-8') as f:
        return set(re.findall(r'<loc>([^<]+)</loc>', f.read()))


def main():
    pages, listed = site_pages(), sitemap_urls()
    missing = sorted(pages - listed)
    stale = sorted(listed - pages)
    if missing:
        print(f'-- {len(missing)} page(s) missing from sitemap.xml --')
        for u in missing:
            print(f'  {u}')
    if stale:
        print(f'-- {len(stale)} sitemap entr(ies) with no matching page --')
        for u in stale:
            print(f'  {u}')
    if not missing and not stale:
        print(f'sitemap clean: {len(pages)} pages, all listed, nothing stale')
        return 0
    return 1


if __name__ == '__main__':
    sys.exit(main())
