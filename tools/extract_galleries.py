"""
Reads the WordPress XML export and prints a complete GALLERIES dict
suitable for pasting into restore_static_posts.py.

Handles:
  - Envira galleries  ([envira-gallery id="NNN"])
  - Classic WP galleries ([gallery ids="..."] / [gallery columns="..." ids="..."])
"""

from __future__ import annotations
import re
import sys
from pathlib import Path

XML_PATH = Path(r'C:\Users\agile\Downloads\4globetrotters.WordPress.2026-03-28.xml')


def extract_srcs_from_serialized(data: str) -> list[str]:
    """Pull out src values from a PHP serialized _eg_gallery_data string."""
    # Matches:  s:3:"src";s:NNN:"<URL>";
    return re.findall(r's:3:"src";s:\d+:"([^"]+)"', data)


def normalise_url(url: str) -> str:
    """Convert absolute upload URL to site-relative /wp-content/... path."""
    return re.sub(r'^https?://[^/]+', '', url)


def main() -> None:
    text = XML_PATH.read_text(encoding='utf-8', errors='replace')

    # ── 1. Envira galleries ──────────────────────────────────────────────────
    # Each <item> with post_type=envira contains a _eg_gallery_data postmeta
    envira: dict[int, list[str]] = {}

    # Split into <item> blocks
    items = re.split(r'<item>', text)
    for item in items:
        if '<wp:post_type><![CDATA[envira]]></wp:post_type>' not in item:
            continue
        id_match = re.search(r'<wp:post_id>(\d+)</wp:post_id>', item)
        if not id_match:
            continue
        gid = int(id_match.group(1))

        gallery_data_match = re.search(
            r'<wp:meta_key><!\[CDATA\[_eg_gallery_data\]\]></wp:meta_key>\s*'
            r'<wp:meta_value><!\[CDATA\[(.*?)\]\]></wp:meta_value>',
            item, re.S
        )
        if not gallery_data_match:
            continue

        srcs = extract_srcs_from_serialized(gallery_data_match.group(1))
        if srcs:
            envira[gid] = [normalise_url(s) for s in srcs]

    # ── 2. Attachment posts  → id → /wp-content/... path ────────────────────
    attachments: dict[int, str] = {}
    for item in items:
        if '<wp:post_type><![CDATA[attachment]]></wp:post_type>' not in item:
            continue
        id_match = re.search(r'<wp:post_id>(\d+)</wp:post_id>', item)
        url_match = re.search(r'<wp:attachment_url><!\[CDATA\[(.*?)\]\]></wp:attachment_url>', item)
        if id_match and url_match:
            attachments[int(id_match.group(1))] = normalise_url(url_match.group(1))

    # ── 3. Collect every unique classic [gallery …] shortcode ───────────────
    gallery_shortcodes: set[str] = set(
        re.findall(r'\[gallery[^\]]*\]', text)
    )

    # ── 4. Print the full GALLERIES dict ────────────────────────────────────
    print('GALLERIES: dict[str, list[str]] = {')

    # Envira entries
    for gid in sorted(envira):
        key = f'[envira-gallery id="{gid}"]'
        imgs = envira[gid]
        print(f'    {key!r}: [')
        for img in imgs:
            print(f'        {img!r},')
        print('    ],')

    # Classic [gallery …] entries
    for sc in sorted(gallery_shortcodes):
        ids_match = re.search(r'\bids="([^"]+)"', sc)
        if not ids_match:
            continue
        ids = [int(x.strip()) for x in ids_match.group(1).split(',') if x.strip().isdigit()]
        imgs = [attachments[i] for i in ids if i in attachments]
        if not imgs:
            print(f'    # UNRESOLVED: {sc!r}')
            continue
        print(f'    {sc!r}: [')
        for img in imgs:
            print(f'        {img!r},')
        print('    ],')

    print('}')

    # ── 5. Summary ───────────────────────────────────────────────────────────
    print(f'\n# Envira galleries found: {len(envira)}', file=sys.stderr)
    print(f'# Classic gallery shortcodes found: {len(gallery_shortcodes)}', file=sys.stderr)
    unresolved_classic = [
        sc for sc in gallery_shortcodes
        if re.search(r'\bids="([^"]+)"', sc) and not any(
            i in attachments
            for i in [int(x) for x in re.search(r'\bids="([^"]+)"', sc).group(1).split(',') if x.strip().isdigit()]
        )
    ]
    if unresolved_classic:
        print(f'# Unresolved classic shortcodes: {unresolved_classic}', file=sys.stderr)


if __name__ == '__main__':
    main()
