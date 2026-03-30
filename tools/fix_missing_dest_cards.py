"""
Inject missing post cards into Fiji and Philippines destination pages,
using the WordPress XML export as source of truth.
"""
from pathlib import Path
import xml.etree.ElementTree as ET
import re
import html as html_mod
from datetime import datetime

xml_path = Path(r"C:\Users\agile\Downloads\4globetrotters.WordPress.2026-03-28.xml")
site = Path(r"C:\Users\agile\VSCode projects\4globetrotters\option-b-static\site")

tree = ET.parse(xml_path)
root = tree.getroot()
WP = "http://wordpress.org/export/1.2/"
CONTENT = "http://purl.org/rss/1.0/modules/content/"

# Which destination category → folder mappings to fix
FIX = {
    "fiji": "fiji-2022",
    "phillipines": "philippines",   # note WP typo
}

def strip_tags(text):
    return re.sub(r'<[^>]+>', '', text or '')

def first_img_from_html(slug):
    f = site / slug / "index.html"
    if not f.exists():
        return ""
    t = f.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"src='(/wp-content/uploads/[^']+)'", t)
    return m.group(1) if m else ""

def make_excerpt(raw, length=200):
    """Strip HTML/shortcodes, return first ~length chars."""
    text = re.sub(r'\[/?[^\]]+\]', '', raw or '')  # remove shortcodes
    text = strip_tags(text)
    text = re.sub(r'\s+', ' ', text).strip()
    if len(text) > length:
        text = text[:length].rsplit(' ', 1)[0] + ' ...'
    return html_mod.escape(text)

# Collect posts per target category from XML
channel = root.find("channel")
cat_posts = {k: [] for k in FIX}

for item in channel.findall("item"):
    if item.findtext(f"{{{WP}}}post_type") != "post":
        continue
    if item.findtext(f"{{{WP}}}status") != "publish":
        continue

    slug = item.findtext(f"{{{WP}}}post_name")
    title = item.findtext("title") or slug
    pub_date = item.findtext("pubDate") or ""
    raw_content = item.findtext(f"{{{CONTENT}}}encoded") or ""

    # parse date
    try:
        # pubDate format: "Wed, 23 Dec 2015 13:09:15 +0000"
        # Skip the day-name prefix to avoid locale issues on Windows
        parts = pub_date.split(', ', 1)
        date_part = parts[1][:20]  # "23 Dec 2015 13:09:15"
        dt = datetime.strptime(date_part, "%d %b %Y %H:%M:%S")
        date_str = f"{dt.strftime('%B')} {dt.day}, {dt.year}"
    except Exception:
        date_str = pub_date[:16]

    for cat_el in item.findall("category"):
        nicename = cat_el.get("nicename", "")
        if nicename in FIX:
            img = first_img_from_html(slug)
            excerpt = make_excerpt(raw_content)
            cat_posts[nicename].append({
                "slug": slug,
                "title": title,
                "date": date_str,
                "img": img,
                "excerpt": excerpt,
            })

# Sort posts by date descending (most recent first)
for cat in cat_posts:
    cat_posts[cat].sort(key=lambda p: p["date"], reverse=True)

def build_cards_html(posts):
    lines = ['<h2>Posts from this destination</h2><div class="post-cards">']
    for p in posts:
        img_html = (
            f'  <a href="/{p["slug"]}/" class="post-card-img">'
            f'<img src="{p["img"]}" alt="{html_mod.escape(p["title"])}"></a>'
            if p["img"] else
            f'  <a href="/{p["slug"]}/" class="post-card-img post-card-img--no-photo"></a>'
        )
        lines.append('<div class="post-card">')
        lines.append(img_html)
        lines.append('  <div class="post-card-body">')
        lines.append(f'    <p class="meta">{p["date"]}</p>')
        lines.append(f'    <h3><a href="/{p["slug"]}/">{html_mod.escape(p["title"])}</a></h3>')
        lines.append(f'    <p>{p["excerpt"]}</p>')
        lines.append(f'    <a href="/{p["slug"]}/" class="read-more">Read more &rarr;</a>')
        lines.append('  </div>')
        lines.append('</div>')
    lines.append('</div>')
    return '\n'.join(lines)

# Inject into each destination page
for cat_slug, folder_slug in FIX.items():
    posts = cat_posts[cat_slug]
    if not posts:
        print(f"WARNING: no posts found for {cat_slug}")
        continue

    dest_file = site / folder_slug / "index.html"
    content = dest_file.read_text(encoding="utf-8")

    cards_html = build_cards_html(posts)

    # Extract the existing intro text from <main> (before any card junk)
    main_match = re.search(r'<main[^>]*>(.*?)</main>', content, re.DOTALL)
    if main_match:
        raw_main = main_match.group(1)
        # Keep only the intro paragraph - strip everything from "See blog" or "Blog post" stub
        # and any previously-injected post-card content
        intro = re.split(
            r'(See blog post|Blog post|<h2>Posts from|<div class="post-card)',
            raw_main, maxsplit=1, flags=re.IGNORECASE
        )[0].strip()
        new_main_content = f'\n{intro}\n{cards_html}\n' if intro else f'\n{cards_html}\n'
    else:
        new_main_content = f'\n{cards_html}\n'

    new_content = re.sub(
        r'<main[^>]*>.*?</main>',
        f'<main class="page-content">{new_main_content}</main>',
        content,
        flags=re.DOTALL,
    )

    dest_file.write_text(new_content, encoding="utf-8")
    print(f"✓ {folder_slug}: injected {len(posts)} post card(s)")

print("Done.")
