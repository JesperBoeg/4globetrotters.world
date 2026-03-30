"""
inject_comments.py — Inject Remark42 comment embed into every blog post page.

Run AFTER Remark42 is deployed and you have confirmed it's running.

Usage:
    python tools/inject_comments.py

It will:
  - Find all post pages (slug/index.html files that are blog posts, not category/destination pages)
  - Insert the Remark42 embed block just before </main>
  - Skip pages that already have the embed

Re-running is safe — already-injected pages are skipped.
"""
from pathlib import Path
import re

# ---- CONFIGURE THIS ----
REMARK_URL = "https://4globetrotters-comments.fly.dev"
SITE_ID    = "4globetrotters"
# -------------------------

SITE = Path(r"C:\Users\agile\VSCode projects\4globetrotters\option-b-static\site")

# Pages that are NOT blog posts (category/destination/special pages — skip them)
NON_POST_DIRS = {
    "blog", "about-us-2", "countries-we-are-visiting", "privacy-policy",
    "peru", "ecuador-july-2024", "galapagos-june-2024",
    "western-australia-julyaugust-2022", "fiji-2022", "french-polynesia",
    "san-francisco-2022", "usa-denver-to-las-vegas-rockies-yellowstone-bryce-zion",
    "indonesia-bali-and-nearby-islands", "australia-cairns",
    "australia-northern-territory", "deep-south", "cuba", "mexico-yucatan",
    "california-usa", "hawaii", "australia", "philippines", "vietnam",
    "thailand", "cyprus", "denmark-preparing-for-the-trip",
    "assets", "wp-content", "wp-simple",
}

EMBED_MARKER = "remark42"

EMBED_HTML = f"""
<div class="comments-section" style="margin-top:48px; padding-top:32px; border-top:1px solid #eee;">
  <h3 style="font-family:'Playfair Display',serif; font-size:1.4rem; margin-bottom:24px;">Comments</h3>
  <div id="remark42"></div>
</div>

<script>
  var remark_config = {{
    host: "{REMARK_URL}",
    site_id: "{SITE_ID}",
    components: ["embed"],
    max_shown_comments: 10,
    theme: "light",
    locale: "en"
  }};
</script>
<script>
  !function(e,n){{for(var o=0;o<e.length;o++){{var r=n.createElement("script"),c=".js",d=n.head||n.body;
  "noModule"in r?(r.type="module",c=".mjs"):r.async=!0,r.defer=!0,
  r.src=remark_config.host+"/web/"+e[o]+c,d.appendChild(r)}}}}(remark_config.components||["embed"],document);
</script>
"""

injected = 0
skipped  = 0
already  = 0

for index_file in sorted(SITE.glob("*/index.html")):
    folder = index_file.parent.name
    if folder in NON_POST_DIRS:
        skipped += 1
        continue

    content = index_file.read_text(encoding="utf-8")

    if EMBED_MARKER in content:
        already += 1
        continue

    if "</main>" not in content:
        print(f"  WARN: no </main> in {folder}/index.html — skipping")
        skipped += 1
        continue

    new_content = content.replace("</main>", f"{EMBED_HTML}</main>", 1)
    index_file.write_text(new_content, encoding="utf-8")
    injected += 1

print(f"\nDone.")
print(f"  Injected : {injected} pages")
print(f"  Already  : {already} pages (skipped, already have embed)")
print(f"  Skipped  : {skipped} pages (non-post or no </main>)")
