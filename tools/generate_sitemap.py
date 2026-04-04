#!/usr/bin/env python3
"""
Generate XML sitemap for 4Globetrotters.world
Helps search engines discover and index all pages
"""

import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime
from urllib.parse import urljoin

SITE_ROOT = Path(r"C:\Users\agile\VSCode projects\4globetrotters\option-b-static\site")
DOMAIN = "https://4globetrotters.world"
OUTPUT_FILE = SITE_ROOT / "sitemap.xml"

def get_post_date(html_file: Path) -> str:
    """Extract date from HTML and return ISO format."""
    try:
        content = html_file.read_text(encoding='utf-8', errors='ignore')
        # Try to find date in page-meta
        import re
        match = re.search(r'<p class="page-meta">(.+?)</p>', content)
        if match:
            date_str = match.group(1).strip()
            # Try to parse the date
            try:
                dt = datetime.strptime(date_str, "%B %d, %Y")
                return dt.strftime("%Y-%m-%d")
            except:
                pass
    except:
        pass
    return datetime.now().strftime("%Y-%m-%d")

def generate_sitemap():
    """Generate XML sitemap."""
    urlset = ET.Element("urlset")
    urlset.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")
    
    # Add homepage
    url_elem = ET.SubElement(urlset, "url")
    ET.SubElement(url_elem, "loc").text = DOMAIN + "/"
    ET.SubElement(url_elem, "priority").text = "1.0"
    ET.SubElement(url_elem, "changefreq").text = "weekly"
    
    # Add main pages
    main_pages = [
        ("/blog/", "0.9", "weekly"),
        ("/about-us-2/", "0.8", "monthly"),
        ("/countries-we-are-visiting/", "0.8", "monthly"),
    ]
    
    for path, priority, freq in main_pages:
        url_elem = ET.SubElement(urlset, "url")
        ET.SubElement(url_elem, "loc").text = DOMAIN + path
        ET.SubElement(url_elem, "priority").text = priority
        ET.SubElement(url_elem, "changefreq").text = freq
    
    # Add blog posts
    post_count = 0
    for post_dir in sorted(SITE_ROOT.iterdir()):
        if not post_dir.is_dir():
            continue
        
        # Skip special directories
        if post_dir.name in ["assets", "wp-content", "blog", "category", "countries-we-are-visiting", 
                              "about-us", "about-us-2", "itinerary", "todo-list", "privacy-policy", "deploy-marker.txt"]:
            continue
        
        index_file = post_dir / "index.html"
        if not index_file.exists():
            continue
        
        post_count += 1
        url_elem = ET.SubElement(urlset, "url")
        ET.SubElement(url_elem, "loc").text = DOMAIN + "/" + post_dir.name + "/"
        
        # Get date
        date = get_post_date(index_file)
        ET.SubElement(url_elem, "lastmod").text = date
        
        # Blog posts get lower priority than main pages
        ET.SubElement(url_elem, "priority").text = "0.7"
        ET.SubElement(url_elem, "changefreq").text = "never"
    
    # Create pretty XML
    ET.indent(urlset, space="  ")
    tree = ET.ElementTree(urlset)
    tree.write(OUTPUT_FILE, encoding='utf-8', xml_declaration=True)
    
    print(f"[OK] Generated sitemap.xml")
    print(f"    Total URLs: {post_count + len(main_pages) + 1}")
    print(f"    Location: {OUTPUT_FILE}")
    print(f"\nSubmit to search engines:")
    print(f"    - Google Search Console: https://www.google.com/webmasters/tools/")
    print(f"    - Bing Webmaster Tools: https://www.bing.com/toolbox/webmaster/")
    print(f"    - Direct URL: {DOMAIN}/sitemap.xml")

if __name__ == "__main__":
    generate_sitemap()
