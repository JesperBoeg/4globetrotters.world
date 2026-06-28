# -*- coding: utf-8 -*-
"""
Generator for the 2026 Asia trip (Malaysia / Indonesia / Sri Lanka).

Creates:
  - 5 destination overview pages (LIVE)
  - 14 individual blog post stubs (HIDDEN: full scaffold + itinerary outline,
    NOT linked from destination cards / blog index / sitemap until flipped live)

Design notes:
  - Destination pages list posts from each post's `live` flag. While a post is
    a draft (live=False) it is NOT shown on the destination page, blog index,
    or sitemap. Flip `live=True` here (or follow WRITING-GUIDE) and re-run to
    publish a finished post.
  - Multiple posts per place are supported: just add more entries to POSTS with
    the same `dest` and distinct `slug`.
"""
from pathlib import Path
import html

SITE = Path(__file__).resolve().parent.parent / "option-b-static" / "site"
BASE = "https://4globetrotters.world"

NAV = """<nav class="site-nav" id="siteNav">
  <div class="nav-inner">
    <a href="/" class="nav-logo">4Globetrotters</a>
    <button class="nav-toggle" id="navToggle" aria-label="Menu">&#9776;</button>
    <ul class="nav-links" id="navLinks">
      <li><a href="/">Home</a></li>
      <li><a href="/about-us-2/">About Us</a></li>
      <li><a href="/blog/">Blog</a></li>
      <li><a href="/countries-we-are-visiting/">Destinations</a></li>
    </ul>
  </div>
</nav>"""

FOOTER = """<footer class="site-footer">
  <div class="footer-inner">
    <div class="footer-col">
      <h4>4Globetrotters</h4>
      <p>A Danish family of four &mdash; Jesper, Line, Noah and Vitus &mdash; sharing our adventures traveling the world with children since 2015.</p>
      <div class="social-links" style="margin-top:16px;">
        <a href="https://www.facebook.com/linemarie.nathan" target="_blank" rel="noopener" aria-label="Facebook"><i class="fa fa-facebook"></i></a>
        <a href="https://www.linkedin.com/pub/jesper-boeg/1/401/332" target="_blank" rel="noopener" aria-label="LinkedIn"><i class="fa fa-linkedin"></i></a>
        <a href="https://twitter.com/j_boeg" target="_blank" rel="noopener" aria-label="Twitter"><i class="fa fa-twitter"></i></a>
      </div>
    </div>
    <div class="footer-col">
      <h4>Quick Links</h4>
      <ul>
        <li><a href="/about-us-2/">About Us</a></li>
        <li><a href="/blog/">Blog</a></li>
        <li><a href="/countries-we-are-visiting/">All Countries</a></li>
        <li><a href="/privacy-policy/">Privacy Policy</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Contact</h4>
      <p>4Globetrotters<br>Michael Anchers Vej 25<br>8270 Hojbjerg, Denmark</p>
      <p style="margin-top:8px;">Phone: +45 51 54 28 20</p>
    </div>
  </div>
  <div class="footer-bottom">
    &copy; 2015-2026 4Globetrotters. All rights reserved.
  </div>
</footer>"""

NAV_SCRIPT = """<script>
(function(){
  var t = document.getElementById('navToggle');
  var l = document.getElementById('navLinks');
  t.addEventListener('click', function(){ l.classList.toggle('open'); });
  var n = document.getElementById('siteNav');
  window.addEventListener('scroll', function(){
    n.classList.toggle('scrolled', window.scrollY > 20);
  });
})();
</script>
<script src="/assets/share-buttons.js"></script>"""

COMMENTS = """<div class="comments-section" style="margin-top:48px; padding-top:32px; border-top:1px solid #eee;">
  <h3 style="font-family:'Playfair Display',serif; font-size:1.4rem; margin-bottom:24px;">Comments</h3>
  <div id="remark42"></div>
</div>

<script>
  var remark_config = {
    host: "https://4globetrotters-comments.fly.dev",
    site_id: "4globetrotters",
    url: window.location.href.replace(/^https?:\\/\\/www\\./, "https://").split(/[?#]/)[0],
    components: ["embed"],
    max_shown_comments: 10,
    theme: "light",
    locale: "en"
  };
</script>
<script>
  !function(e,n){for(var o=0;o<e.length;o++){var r=n.createElement("script"),c=".js",d=n.head||n.body;
  "noModule"in r?(r.type="module",c=".mjs"):r.async=!0,r.defer=!0,
  r.src=remark_config.host+"/web/"+e[o]+c,d.appendChild(r)}}(remark_config.components||["embed"],document);
</script>"""

HEAD_COMMON = """  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;500;600&display=swap">
  <link rel="stylesheet" href="/assets/wp-simple/css/font-awesome.min.css">
  <link rel="stylesheet" href="/assets/subpage.css">
  <link rel="stylesheet" href="/assets/analytics-consent.css">
  <script src="/assets/analytics-consent.js" defer></script>"""


def esc(s):
    return html.escape(s, quote=True)


# ---------------------------------------------------------------------------
# DESTINATIONS (live overview pages). order = chronological for this trip.
# ---------------------------------------------------------------------------
DESTS = {
    "malaysia-kuala-lumpur": {
        "title": "Malaysia &mdash; Kuala Lumpur (June 2026)",
        "short": "Malaysia — Kuala Lumpur",
        "region": "Asia",
        "when": "June &amp; July 2026",
        "intro": "Kuala Lumpur became our hub for this Southeast Asia leg &mdash; a quick first stop on the way to Indonesia, and again on the way back before flying on to Sri Lanka. Skyscrapers, street food, and a welcome dose of air-conditioning between jungles and volcanoes.",
    },
    "indonesia-komodo-flores": {
        "title": "Indonesia &mdash; Komodo &amp; Flores (June/July 2026)",
        "short": "Indonesia — Komodo &amp; Flores",
        "region": "Asia",
        "when": "June &ndash; July 2026",
        "intro": "From Flores we boarded a boat for several days through Komodo National Park &mdash; Komodo dragons, pink beaches, manta rays and some of the best snorkelling in Indonesia, all from the deck of our own liveaboard.",
    },
    "indonesia-lombok-rinjani": {
        "title": "Indonesia &mdash; Lombok &amp; Mount Rinjani (July 2026)",
        "short": "Indonesia — Lombok &amp; Rinjani",
        "region": "Asia",
        "when": "July 2026",
        "intro": "We left the boat in Lombok and set our sights upward: a three-day trek up Mount Rinjani, Indonesia&rsquo;s second-highest volcano, with a crater lake, a brutal summit push, and views that made every step worth it.",
    },
    "indonesia-sumatra": {
        "title": "Indonesia &mdash; Sumatra (July 2026)",
        "short": "Indonesia — Sumatra",
        "region": "Asia",
        "when": "July 2026",
        "intro": "Nine days across northern Sumatra: jungle trekking in Gunung Leuser National Park to find wild orangutans, sunrise on Mount Sibayak, and the vast caldera of Lake Toba with its Batak culture on Samosir Island.",
    },
    "sri-lanka": {
        "title": "Sri Lanka (July/August 2026)",
        "short": "Sri Lanka",
        "region": "Asia",
        "when": "July &ndash; August 2026",
        "intro": "Thirteen days across Sri Lanka: the ancient rock fortress of Sigiriya, elephant safaris, tea country by train to Ella, surf lessons and safaris at Arugam Bay, and the buzz of Colombo to finish.",
    },
}

# ---------------------------------------------------------------------------
# POSTS (one per place; multiple per place allowed). live=False => hidden.
# `outline` is a list of (heading, [bullet lines]) for the draft scaffold.
# `date` is the (planned) publish date used for ordering + schema.
# ---------------------------------------------------------------------------
POSTS = [
    # ---- Malaysia ----
    dict(slug="kuala-lumpur-stopover", dest="malaysia-kuala-lumpur",
         title="Kuala Lumpur &mdash; a one-day stopover", date="2026-06-28",
         when="June 28, 2026",
         lead="Our first stop on this Southeast Asia leg: a single day in Kuala Lumpur to shake off the flight before heading to Indonesia.",
         outline=[("The plan", ["Arrive KL, one night before flying to Flores on the 30th",
                                "What we did with ~24 hours in the city"]),
                  ("Highlights", ["(write up the day)", "Food / Petronas Towers / getting around"])]),

    # ---- Komodo & Flores ----
    dict(slug="flores-arrival-labuan-bajo", dest="indonesia-komodo-flores",
         title="Arriving in Flores &mdash; Labuan Bajo before the boat", date="2026-06-30",
         when="June 30, 2026",
         lead="We flew into Flores on the 30th and based ourselves in Labuan Bajo before boarding the boat through Komodo National Park.",
         outline=[("Getting to Flores", ["Flight from KL", "First impressions of Labuan Bajo"]),
                  ("Before the boat", ["Days before departure (boat boards on the 5th)", "Food, harbour, prep"])]),
    dict(slug="komodo-national-park-boat-trip", dest="indonesia-komodo-flores",
         title="Komodo National Park by boat &mdash; dragons, pink beaches &amp; manta rays", date="2026-07-09",
         when="July 5 &ndash; 9, 2026",
         lead="Five days (5th&ndash;9th) on a boat through Komodo National Park, ending in Lombok.",
         outline=[("The boat", ["Liveaboard setup, the route Flores → Lombok"]),
                  ("Komodo dragons", ["The dragon walk", "How the kids handled it"]),
                  ("Snorkelling & beaches", ["Pink Beach", "Manta rays", "Best snorkel spots"]),
                  ("Disembark in Lombok", ["Arrival on the 9th"])]),

    # ---- Lombok & Rinjani ----
    dict(slug="lombok-arrival", dest="indonesia-lombok-rinjani",
         title="Arriving in Lombok", date="2026-07-09",
         when="July 9, 2026",
         lead="We stepped off the Komodo boat in Lombok on the 9th &mdash; the launch point for our Rinjani trek.",
         outline=[("From boat to island", ["Disembarking", "Where we stayed", "Prepping for the trek"]) ]),
    dict(slug="mount-rinjani-3-day-trek", dest="indonesia-lombok-rinjani",
         title="Climbing Mount Rinjani &mdash; a 3-day trek", date="2026-07-12",
         when="July 2026",
         lead="A three-day trek up Mount Rinjani, Indonesia&rsquo;s second-highest volcano, with its crater lake and a punishing summit morning.",
         outline=[("Day 1", ["The climb begins", "First camp"]),
                  ("Day 2", ["Crater rim / lake", "Hot springs?"]),
                  ("Day 3 — summit", ["Pre-dawn summit push", "The descent"]),
                  ("Trekking Rinjani with kids", ["Logistics, fitness, what we'd advise"])]),

    # ---- Sumatra ----
    dict(slug="bukit-lawang-jungle-trek-orangutans", dest="indonesia-sumatra",
         title="Bukit Lawang &mdash; jungle trekking for wild orangutans", date="2026-07-18",
         when="July 15 &ndash; 18, 2026",
         lead="Our Sumatra adventure began in Bukit Lawang with a multi-day jungle trek through Gunung Leuser National Park.",
         outline=[("Day 1 (Jul 15)", ["Medan airport → Bukit Lawang by private car", "Check in to the homestay"]),
                  ("Day 2 (Jul 16)", ["Jungle trek into Gunung Leuser NP", "Gibbons, wildlife, wild orangutans", "Overnight in the tree house"]),
                  ("Day 3 (Jul 17)", ["Deeper into the jungle", "Tiger footprints?", "Second night at the camp"]),
                  ("Day 4 (Jul 18)", ["Bahorok river swim", "Tube rafting back to Bukit Lawang"])]),
    dict(slug="berastagi-mount-sibayak", dest="indonesia-sumatra",
         title="Berastagi &mdash; Mount Sibayak sunrise &amp; hot springs", date="2026-07-20",
         when="July 19 &ndash; 20, 2026",
         lead="From Bukit Lawang we drove to the highland town of Berastagi for a volcano sunrise and a soak in the hot springs.",
         outline=[("Day 5 (Jul 19)", ["~4.5h drive Bukit Lawang → Berastagi", "Fruit market", "Street-food court dinner"]),
                  ("Day 6 (Jul 20)", ["~4:30am start to hike Mount Sibayak for sunrise",
                                      "Sidebuk-debuk hot springs", "Buddhist temple, traditional Batak house"])]),
    dict(slug="lake-toba-samosir-island", dest="indonesia-sumatra",
         title="Lake Toba &amp; Samosir Island", date="2026-07-22",
         when="July 20 &ndash; 22, 2026",
         lead="We finished Sumatra at the vast volcanic Lake Toba, staying on Samosir Island in Tuk Tuk.",
         outline=[("Day 6 cont. (Jul 20)", ["Drive to Lake Toba", "Sipiso-piso waterfall",
                                            "Ferry from Tiga Raja harbour to Samosir, overnight in Tuk Tuk"]),
                  ("Day 7 (Jul 21)", ["Rent a motorbike around Samosir", "Tomok village & King Sidabutar's tomb",
                                      "Sigale-gale Batak dance", "Traditional Batak houses, stone chairs"]),
                  ("Day 8 (Jul 22)", ["Private car to Medan / airport for the next destination"])]),
    dict(slug="kuala-lumpur-stopover-return", dest="malaysia-kuala-lumpur",
         title="Kuala Lumpur again &mdash; a stop on the way to Sri Lanka", date="2026-07-24",
         when="July 2026",
         lead="After Sumatra we returned to Kuala Lumpur for another day before flying on to Sri Lanka.",
         outline=[("Second time in KL", ["What we did differently", "Resting up before Sri Lanka"]) ]),

    # ---- Sri Lanka ----
    dict(slug="sigiriya-dambulla", dest="sri-lanka",
         title="Sigiriya &amp; Dambulla &mdash; Lion Rock, caves &amp; elephants", date="2026-07-28",
         when="July 25 &ndash; 29, 2026",
         lead="Four nights in the Cultural Triangle: Dambulla cave temples, the Sigiriya Lion Rock fortress, an elephant safari and Polonnaruwa by bike.",
         outline=[("Day 1 (Jul 25)", ["Colombo airport → Sigiriya", "Dambulla Cave Temple on the way", "Check in (4 nights)"]),
                  ("Day 2 (Jul 26)", ["Sigiriya Museum", "Jeep safari for The Gathering (Minneriya / Kaudulla)"]),
                  ("Day 3 (Jul 27)", ["Early climb up Sigiriya Lion Rock", "Afternoon by the pool"]),
                  ("Day 4 (Jul 28)", ["Polonnaruwa by bike", "Village rice & curry lunch", "Pidurangala sunset hike"]) ]),
    dict(slug="kandy", dest="sri-lanka",
         title="Kandy &mdash; a curry class &amp; the Temple of the Tooth", date="2026-07-29",
         when="July 29, 2026",
         lead="A cooking masterclass in Sigiriya, then south to Kandy and the Temple of the Sacred Tooth Relic.",
         outline=[("Day 5 (Jul 29)", ["Curry cooking class at Lucky Leanne (Sigiriya)",
                                      "~2.5h drive to Kandy", "Temple of the Sacred Tooth evening ritual"]) ]),
    dict(slug="ella-tea-country", dest="sri-lanka",
         title="Ella &amp; tea country &mdash; the train, Little Adam&rsquo;s Peak &amp; Nine Arch Bridge", date="2026-07-31",
         when="July 30 &ndash; 31, 2026",
         lead="Up into the hills by the famous hill-country train, then two days exploring Ella.",
         outline=[("Day 6 (Jul 30)", ["Drive into tea country", "Pedro Tea Estate near Nuwara Eliya",
                                      "3:00pm train Ambewela → Ella (#1015)"]),
                  ("Day 7 (Jul 31)", ["Little Adam's Peak hike", "Flying Ravana zipline", "Nine Arch Bridge"]) ]),
    dict(slug="arugam-bay-surf-safari", dest="sri-lanka",
         title="Arugam Bay &mdash; surf lessons &amp; a Kumana safari", date="2026-08-03",
         when="August 1 &ndash; 3, 2026",
         lead="Down to the east coast for three days of beginner surf lessons and a quieter safari in Kumana.",
         outline=[("Day 8 (Aug 1)", ["Ravana Waterfalls", "~3h scenic drive to Arugam Bay", "Pick a surf school"]),
                  ("Day 9 (Aug 2)", ["Surf lesson 1 at Baby Point", "Beach cafés"]),
                  ("Day 10 (Aug 3)", ["Surf lesson 2 (Elephant Rock / Peanut Farm)", "Kumana National Park 4x4 safari"]) ]),
    dict(slug="colombo", dest="sri-lanka",
         title="Colombo &mdash; markets, the Lotus Tower &amp; goodbye", date="2026-08-06",
         when="August 4 &ndash; 6, 2026",
         lead="The final stretch: the drive west to Colombo, two days in the city, and the flight home.",
         outline=[("Day 11 (Aug 4)", ["Arugam Bay → Colombo via Southern Expressway", "Dinner (Ministry of Crab / Galle Face)"]),
                  ("Day 12 (Aug 5)", ["Pettah Market", "Lotus Tower observation deck", "Aluthkade street food"]),
                  ("Day 13 (Aug 6)", ["Last day in Colombo", "National Museum / Fort District", "Flight home 22:50"]) ]),
]


def post_url(p):
    return f"/{p['slug']}/"


def render_destination(dslug, d):
    posts = [p for p in POSTS if p["dest"] == dslug and p.get("live")]
    posts.sort(key=lambda p: p["date"])  # chronological
    cards = []
    if posts:
        for p in posts:
            img = p.get("card_img", "/assets/og-image.png")
            cards.append(f"""<div class="post-card">
  <a href="{post_url(p)}" class="post-card-img"><img src="{img}" alt="{esc(p['title'])}"></a>
  <div class="post-card-body">
    <p class="meta">{p['when']}</p>
    <h3><a href="{post_url(p)}">{p['title']}</a></h3>
    <p>{p.get('lead','')}</p>
    <a href="{post_url(p)}" class="read-more">Read more &rarr;</a>
  </div>
</div>""")
        posts_block = '<h2>Posts from this destination</h2><div class="post-cards">\n' + "\n".join(cards) + "\n</div>"
    else:
        posts_block = ('<h2>Posts from this destination</h2>\n'
                       '<p><em>We&rsquo;re travelling here right now &mdash; stories and photos coming soon.</em></p>')

    title_plain = d["title"].replace("&mdash;", "—").replace("&amp;", "&").replace("&ndash;", "–")
    desc = d["intro"][:160]
    url = f"{BASE}/{dslug}/"
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{esc(desc)}">
    <meta property="og:title" content="{esc(title_plain)}">
    <meta property="og:description" content="{esc(desc)}">
    <meta property="og:image" content="{BASE}/assets/og-image.png">
    <meta property="og:url" content="{url}">
    <meta property="og:type" content="article">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{esc(title_plain)}">
    <meta name="twitter:description" content="{esc(desc)}">
    <meta name="twitter:image" content="{BASE}/assets/og-image.png">
  <title>{title_plain} | 4Globetrotters</title>
{HEAD_COMMON}
    <script type="application/ld+json">{{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{{"@type": "ListItem", "position": 1, "name": "Home", "item": "{BASE}"}}, {{"@type": "ListItem", "position": 2, "name": "Destinations", "item": "{BASE}/countries-we-are-visiting/"}}, {{"@type": "ListItem", "position": 3, "name": "{esc(title_plain)}", "item": "{url}"}}]}}</script>
</head>
<body>

{NAV}

<div class="page-hero">
    <h1>{d['title']}</h1>
</div>

<div class="breadcrumb-bar">
  <div class="breadcrumb-inner"><a href="/">Home</a> &rsaquo; <a href="/countries-we-are-visiting/">Destinations</a> &rsaquo; {d['short']}</div>
</div>

<main class="page-content">
<p>{d['intro']}</p>
{posts_block}
</main>

{FOOTER}

{NAV_SCRIPT}
</body>
</html>
"""


def render_post(p):
    d = DESTS[p["dest"]]
    title_plain = (p["title"].replace("&mdash;", "—").replace("&amp;", "&")
                   .replace("&ndash;", "–").replace("&rsquo;", "’"))
    url = f"{BASE}{post_url(p)}"
    iso = p["date"] + "T00:00:00"
    # draft outline
    outline_html = []
    for heading, bullets in p["outline"]:
        outline_html.append(f"<h2>{heading}</h2>")
        outline_html.append("<ul>")
        for b in bullets:
            outline_html.append(f"  <li>{b}</li>")
        outline_html.append("</ul>")
    outline_block = "\n".join(outline_html)

    draft_banner = ('<div style="background:#fff8e1; border:1px solid #ffe082; border-radius:8px; '
                    'padding:14px 18px; margin-bottom:24px; font-size:.92rem; color:#7a5c00;">'
                    '<strong>DRAFT &mdash; not yet linked publicly.</strong> '
                    'Fill in the content below, add photos, then follow WRITING-GUIDE.md to publish.</div>')

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="noindex">
    <meta name="description" content="{esc(p['lead'][:160])}">
    <meta property="og:title" content="{esc(title_plain)}">
    <meta property="og:description" content="{esc(p['lead'][:160])}">
    <meta property="og:image" content="{BASE}/assets/og-image.png">
    <meta property="og:url" content="{url}">
    <meta property="og:type" content="article">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{esc(title_plain)}">
    <meta name="twitter:description" content="{esc(p['lead'][:160])}">
    <meta name="twitter:image" content="{BASE}/assets/og-image.png">
    <link rel="canonical" href="{url}">
  <title>{title_plain} | 4Globetrotters</title>
{HEAD_COMMON}
    <script type="application/ld+json">{{"@context": "https://schema.org", "@type": "BlogPosting", "headline": "{esc(title_plain)}", "description": "{esc(p['lead'][:160])}", "image": "{BASE}/assets/og-image.png", "datePublished": "{iso}", "author": {{"@type": "Organization", "name": "4Globetrotters"}}, "publisher": {{"@type": "Organization", "name": "4Globetrotters", "logo": {{"@type": "ImageObject", "url": "{BASE}/assets/logo.png"}}}}}}</script>
</head>
<body>

{NAV}

<div class="page-hero">
    <h1>{p['title']}</h1>
    <p class="page-meta">{p['when']}</p>
</div>

<div class="breadcrumb-bar">
  <div class="breadcrumb-inner"><a href="/">Home</a> &rsaquo; <a href="/blog/">Blog</a> &rsaquo; {title_plain}</div>
</div>

<main class="page-content">

{draft_banner}

<p>{p['lead']}</p>

{outline_block}

<p><em>(Write the story here. Use &lt;p class='content-image'&gt;&lt;a href='IMG'&gt;&lt;img src='IMG' alt='...'&gt;&lt;/a&gt;&lt;/p&gt; for photos, matching the other posts.)</em></p>

<p class="meta">Destination: <a href="/{p['dest']}/">{d['short']}</a></p>

{COMMENTS}
</main>

{FOOTER}

{NAV_SCRIPT}
</body>
</html>
"""


def main():
    written = []
    for dslug, d in DESTS.items():
        path = SITE / dslug / "index.html"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render_destination(dslug, d), encoding="utf-8")
        written.append(("DEST", dslug, path))
    for p in POSTS:
        path = SITE / p["slug"] / "index.html"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render_post(p), encoding="utf-8")
        written.append(("POST" + (" (live)" if p.get("live") else " (draft)"), p["slug"], path))
    for kind, slug, path in written:
        print(f"{kind:14} {slug}")
    print(f"\nTotal: {len(written)} files")


if __name__ == "__main__":
    main()
