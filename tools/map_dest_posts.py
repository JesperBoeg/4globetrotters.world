"""
Parse the WordPress XML export and output:
  - For each destination category: list of post slugs assigned to it
  - For each post: its first image attachment URL (from media:content or img in body)
"""
from pathlib import Path
import xml.etree.ElementTree as ET
import re
from collections import defaultdict

xml_path = Path(r"C:\Users\agile\Downloads\4globetrotters.WordPress.2026-03-28.xml")
site = Path(r"C:\Users\agile\VSCode projects\4globetrotters\option-b-static\site")

tree = ET.parse(xml_path)
root = tree.getroot()
WP = "http://wordpress.org/export/1.2/"
CONTENT = "http://purl.org/rss/1.0/modules/content/"

# --- collect all categories (excl. uncategorized) ---
dest_cats = set()
for cat in root.iter(f"{{{WP}}}category"):
    slug = cat.findtext(f"{{{WP}}}category_nicename")
    if slug and slug != "uncategorized" and slug != "preparing-for-the-trip":
        dest_cats.add(slug)

# --- map post slug -> categories -> first image ---
cat_to_posts = defaultdict(list)

channel = root.find("channel")
for item in channel.findall("item"):
    post_type = item.findtext(f"{{{WP}}}post_type")
    status = item.findtext(f"{{{WP}}}status")
    if post_type != "post" or status != "publish":
        continue

    slug = item.findtext(f"{{{WP}}}post_name")
    title = item.findtext("title")

    # categories this post belongs to
    post_cats = []
    for cat_el in item.findall("category"):
        domain = cat_el.get("domain", "")
        nicename = cat_el.get("nicename", "")
        if domain == "category" and nicename in dest_cats:
            post_cats.append(nicename)

    if not post_cats:
        continue

    # find first image: from the static site HTML
    img = "NO IMG"
    html_file = site / slug / "index.html"
    if html_file.exists():
        text = html_file.read_text(encoding="utf-8", errors="ignore")
        imgs = re.findall(r"src='(/wp-content/uploads/[^']+)'", text)
        if imgs:
            img = imgs[0]

    for c in post_cats:
        cat_to_posts[c].append((slug, title, img))

# --- destination folder slug mapping ---
folder_map = {
    "peru": "peru",
    "ecuador": "ecuador-july-2024",
    "galapagos": "galapagos-june-2024",
    "western-australia": "western-australia-julyaugust-2022",
    "fiji": "fiji-2022",
    "french-polynesia": "french-polynesia",
    "san-francisco": "san-francisco-2022",
    "usa-denver-to-las-vegas-rockies-yellowstone": "usa-denver-to-las-vegas-rockies-yellowstone-bryce-zion",
    "indonesia-bali": "indonesia-bali-and-nearby-islands",
    "australia-cairns": "australia-cairns",
    "australia-northern-territory": "australia-northern-territory",
    "southernusa": "deep-south",
    "cuba": "cuba",
    "mexico": "mexico-yucatan",
    "california": "california-usa",
    "hawaii": "hawaii",
    "australia-adelaide-to-sydney": "australia",
    "phillipines": "philippines",
    "vietnam": "vietnam",
    "thailand": "thailand",
    "cyprus": "cyprus",
    "malaysia": None,
    "singapore": None,
}

print("=" * 70)
print("DESTINATION → POSTS (with first image from static site)")
print("=" * 70)
for cat_slug, folder_slug in sorted(folder_map.items()):
    posts = cat_to_posts.get(cat_slug, [])
    print(f"\n[{cat_slug}] → folder: {folder_slug}  ({len(posts)} posts)")
    for post_slug, title, img in sorted(posts, key=lambda x: x[0]):
        exists = "✓" if (site / post_slug / "index.html").exists() else "MISSING"
        print(f"  {exists}  {post_slug}")
        print(f"       img: {img}")
