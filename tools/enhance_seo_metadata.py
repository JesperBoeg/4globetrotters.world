#!/usr/bin/env python3
"""
Enhance blog post SEO metadata:
1. Add meta descriptions (160 chars from first paragraph)
2. Add Open Graph tags for social sharing
3. Add JSON-LD schema markup for blog posts
4. Generate and inject related posts section
5. Add breadcrumb structured data
"""

import re
import html
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Tuple

SITE_ROOT = Path(r"C:\Users\agile\VSCode projects\4globetrotters\option-b-static\site")
DOMAIN = "https://4globetrotters.world"

# Destination/country mapping for related posts
DEST_MAPPING = {
    "peru": ["70-km-salkantay-5d-4n-trek", "amazing-rainbow-mountain-and-red-valley-tour", 
             "a-very-rushed-sacred-valley-tour", "4-amazing-days-in-arequipa",
             "easy-days-in-lima-paracas-huacachina-and-nazca", "homestay-on-the-titicaca-lake"],
    "ecuador": ["beautiful-views-altitude-sickness-and-hiking-at-the-cotopaxi-national-park",
                "kayaking-rafting-canyoning-ziplines-hiking-and-horseback-riding-in-banos-agua-santa"],
    "galapagos": ["flying-to-isabela-hiking-to-the-wall-of-tears-and-visiting-los-tuneles",
                  "snorkeling-with-sea-lions-and-hiking-to-playa-baquerizo",
                  "immersed-in-nature-at-san-cristobal",
                  "santa-cruz-hammerheads-las-grietas-and-the-bellavista-beach"],
    "australia": ["perth-to-quobba-western-australia-part-1-kangaroos-campgrounds-pinnacles-gorges-dolphins-and-lots-of-humpback-whales",
                  "coral-bay-and-exmouth-western-australia-part-2-whale-shark-tour-ningaloo-body-boarding-and-hiking",
                  "karijini-and-tom-price-western-australia-part-3-beautiful-hikes-in-karijini-skate-park-mania-and-a-disappointing-mine-tour",
                  "meekatharra-jurian-bay-dwellingup-and-perth-western-australia-part-4-snorkeling-with-sea-lions-skate-park-crash-mountain-biking-and-the-big-city"],
    "fiji": ["fiji-viti-levu-roadtrip-out-of-our-comfort-zone-at-a-homestay-mud-pool-hiking-water-park-coral-reef-and-visit-to-tivua-island"],
    "french-polynesia": ["tahiti", "snorkeling-views-tennis-and-beaches-at-moorea", "maupiti-coral-gardens-view-points-missing-mantas-and-great-atmosphere",
                        "raiatea-amazing-reef-kayaking-giant-morey-eels-and-another-case-of-missing-mantas",
                        "huahine-our-favorite-island-in-french-polynesia-so-far",
                        "bora-bora-vanilla-is-grown-in-tahaa-tourists-are-grown-in-bora-bora",
                        "rangiroa-diving-dolphins-and-open-water-certificate-for-noah",
                        "tahiti-again-hikes-canoe-race-viewpoints-and-the-most-beautiful-coral-reef-in-french-polynesia"],
    "hawaii": ["lines-first-swim-with-sea-turtles-and-cliff-jumping-at-kaanapali-beach",
               "lots-and-lots-of-humpback-whales-in-maui",
               "the-road-to-hana-a-famous-maui-drive-with-600-hair-pin-turns-and-59-one-lane-bridges-and-a-good-chance-of-motion-sickness",
               "caught-way-down-in-the-haleakala-volcanos-crater",
               "oahu-hawaii-a-bit-of-a-hit-and-miss-affair-but-good-times-never-the-less"],
    "mexico": ["going-to-cuba-after-50-skype-calls-15-hour-flight-delay-and-3-hours-waiting-for-our-luggage-we-finally-arrived",
               "our-5-beautiful-day-trips-in-and-from-merida",
               "amazing-food-beautiful-reefs-and-two-freezing-kids-at-puerto-morelos-mexico",
               "lots-and-lots-of-sea-turtles-and-rays-snorkeling-at-akumal-beach-mexico"],
    "cuba": ["cuba-is-beautiful-ugly-friendly-difficult-dirty-sparse-and-just-really-really-different",
             "la-habana-havana",
             "relaxing-and-exploring-vinales-cuba-caves-bicycling-long-walks-in-the-valley-and-a-very-painful-horse-riding"],
    "thailand": ["first-stop-in-thailand-kanchanaburi-province", "full-day-trip-in-the-kanchanaburi-province",
                 "first-stop-copenhagen"],
    "indonesia": ["ubud-adventures-rafting-waterfalls-woodcarving-and-monkey-forrest-and-a-round-of-food-poisoning",
                  "gili-islands-relaxing-and-snorkeling-all-day-long",
                  "nusa-lembongan-roads-from-hell-on-nusa-penida-and-amazing-snorkeling-with-manta-rays"],
    "usa": ["arriving-in-denver-and-going-to-rocky-mountains",
            "hiking-to-the-fern-falls-and-lake-haiyaha-in-rocky-mountains",
            "first-days-in-amazing-yellowstone",
            "northern-yellowstone-hiking-safari-and-a-fantastic-grizzly-experience",
            "yellowstone-canyon-and-fairy-falls-hikes",
            "days-in-grand-teton-national-park",
            "splendid-views-in-bryce-and-zion-national-park-after-a-forgettable-stopover-in-salt-lake-city"],
}

def extract_first_paragraph(html_content: str) -> str:
    """Extract first paragraph for meta description."""
    # Find all <p> tags and skip those containing only images
    for match in re.finditer(r'<p>(.+?)</p>', html_content, re.DOTALL):
        text = match.group(1)
        
        # Skip paragraphs that only contain images
        if '<img' in text or text.strip() == '':
            continue
        
        # Remove HTML tags and entities
        text = re.sub(r'<[^>]+>', '', text)
        text = html.unescape(text)
        text = text.strip()
        
        # Skip if empty after cleaning
        if not text:
            continue
        
        # Truncate to 160 chars
        if len(text) > 160:
            text = text[:157] + "..."
        return text
    
    return ""

def get_post_title(html_content: str) -> str:
    """Extract post title from <h1> in page-hero."""
    match = re.search(r'<div class="page-hero"[^>]*>.*?<h1>(.+?)</h1>', html_content, re.DOTALL)
    if match:
        return html.unescape(match.group(1))
    # Fallback to title tag
    match = re.search(r'<title>(.+?)\s*\|\s*4Globetrotters</title>', html_content)
    if match:
        return html.unescape(match.group(1))
    return "4Globetrotters"

def get_post_date(html_content: str) -> str:
    """Extract post date from page-meta."""
    match = re.search(r'<p class="page-meta">(.+?)</p>', html_content)
    if match:
        return match.group(1).strip()
    return datetime.now().strftime("%B %d, %Y")

def get_post_image(html_content: str) -> str:
    """Extract first image URL from post content."""
    match = re.search(r"src='(/wp-content/uploads/[^']+)'", html_content)
    if match:
        return DOMAIN + match.group(1)
    return f"{DOMAIN}/assets/og-image.png"

def find_related_posts(slug: str) -> List[Tuple[str, str]]:
    """Find related posts based on destination mapping."""
    related = []
    for dest, posts in DEST_MAPPING.items():
        if slug in posts:
            # Return other posts from same destination (max 3)
            for related_slug in posts:
                if related_slug != slug:
                    related.append(related_slug)
            return related[:3]
    return []

def get_post_title_by_slug(slug: str) -> str:
    """Get title for a post slug."""
    post_dir = SITE_ROOT / slug
    index_file = post_dir / "index.html"
    if index_file.exists():
        content = index_file.read_text(encoding='utf-8', errors='ignore')
        return get_post_title(content)
    # Fallback: convert slug to title
    return slug.replace("-", " ").title()

def create_schema_markup(slug: str, title: str, description: str, date: str, image_url: str) -> str:
    """Create JSON-LD schema for BlogPosting."""
    date_iso = datetime.strptime(date, "%B %d, %Y").isoformat() if date else datetime.now().isoformat()
    
    schema = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": title,
        "description": description,
        "image": image_url,
        "datePublished": date_iso,
        "author": {
            "@type": "Organization",
            "name": "4Globetrotters"
        },
        "publisher": {
            "@type": "Organization",
            "name": "4Globetrotters",
            "logo": {
                "@type": "ImageObject",
                "url": f"{DOMAIN}/assets/logo.png"
            }
        }
    }
    
    return f'<script type="application/ld+json">{str(schema).replace("'", '"')}</script>\n    '

def create_breadcrumb_schema(slug: str, title: str) -> str:
    """Create JSON-LD schema for BreadcrumbList."""
    schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Home",
                "item": DOMAIN
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": "Blog",
                "item": f"{DOMAIN}/blog/"
            },
            {
                "@type": "ListItem",
                "position": 3,
                "name": title,
                "item": f"{DOMAIN}/{slug}/"
            }
        ]
    }
    
    return f'<script type="application/ld+json">{str(schema).replace("'", '"')}</script>\n    '

def create_related_posts_html(related_slugs: List[str]) -> str:
    """Create HTML for related posts section."""
    if not related_slugs:
        return ""
    
    html_content = """
<hr style="margin: 40px 0; border: none; border-top: 1px solid #ddd;">
<div class="related-posts" style="margin-top: 40px;">
  <h3 style="font-size: 1.4rem; margin-bottom: 20px; color: #1a1a1a;">You Might Also Enjoy</h3>
  <ul style="list-style: none; padding: 0; margin: 0; display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px;">
"""
    
    for slug in related_slugs:
        title = get_post_title_by_slug(slug)
        html_content += f"""    <li style="padding: 15px; border: 1px solid #eee; border-radius: 8px; transition: all 0.3s;">
      <a href="/{slug}/" style="color: #c0392b; text-decoration: none; font-weight: 600;">→ {title}</a>
    </li>
"""
    
    html_content += """  </ul>
</div>
"""
    return html_content

def enhance_post(post_path: Path) -> bool:
    """Enhance a single blog post with SEO metadata."""
    index_file = post_path / "index.html"
    
    if not index_file.exists():
        return False
    
    content = index_file.read_text(encoding='utf-8', errors='ignore')
    slug = post_path.name
    
    # Extract metadata
    title = get_post_title(content)
    description = extract_first_paragraph(content)
    date = get_post_date(content)
    image_url = get_post_image(content)
    
    # Skip if description is empty or already has og:title (indicates already enhanced)
    if not description:
        print(f"  SKIPPED {slug} (no description found)")
        return False
    
    if 'property="og:title"' in content:
        print(f"  SKIPPED {slug} (already enhanced)")
        return False
    
    # Create new metadata tags
    og_tags = f"""    <meta name="description" content="{html.escape(description)}">
    <meta property="og:title" content="{html.escape(title)}">
    <meta property="og:description" content="{html.escape(description)}">
    <meta property="og:image" content="{image_url}">
    <meta property="og:url" content="{DOMAIN}/{slug}/">
    <meta property="og:type" content="article">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{html.escape(title)}">
    <meta name="twitter:description" content="{html.escape(description)}">
    <meta name="twitter:image" content="{image_url}">"""
    
    schema_markup = create_schema_markup(slug, title, description, date, image_url)
    breadcrumb_schema = create_breadcrumb_schema(slug, title)
    
    # Find location to inject tags (after viewport meta tag)
    head_pattern = r'(<meta name="viewport"[^>]*>)'
    head_insert = r'\1\n' + og_tags + '\n    '
    content = re.sub(head_pattern, head_insert, content)
    
    # Add schema markup before </head>
    schema_insert = schema_markup + breadcrumb_schema + '    '
    content = content.replace('</head>', schema_insert + '</head>')
    
    # Add related posts before </main>
    related_slugs = find_related_posts(slug)
    related_html = create_related_posts_html(related_slugs)
    if related_html:
        content = content.replace('</main>', related_html + '\n</main>')
    
    # Write back
    index_file.write_text(content, encoding='utf-8')
    print(f"  + {slug}")
    return True

def main():
    """Process all blog posts."""
    print("[*] Scanning blog posts for SEO enhancement...\n")
    
    enhanced_count = 0
    skipped_count = 0
    
    # Find all blog post directories
    for post_dir in sorted(SITE_ROOT.iterdir()):
        if post_dir.is_dir() and (post_dir / "index.html").exists():
            # Skip non-blog directories
            if post_dir.name in ["assets", "wp-content", "blog", "category", "countries-we-are-visiting", "about-us", "about-us-2", "itinerary", "todo-list", "privacy-policy"]:
                continue
            
            if enhance_post(post_dir):
                enhanced_count += 1
            else:
                skipped_count += 1
    
    print(f"\n[OK] Complete!")
    print(f"    Enhanced: {enhanced_count} posts")
    print(f"    Skipped: {skipped_count} posts")
    print(f"\nWhat was added:")
    print(f"    * Meta descriptions for search results")
    print(f"    * Open Graph tags for social media")
    print(f"    * JSON-LD schema for search engines")
    print(f"    * Breadcrumb navigation markup")
    print(f"    * Related posts section")

if __name__ == "__main__":
    main()
