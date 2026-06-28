# Writing & publishing the 2026 Asia trip (Malaysia / Indonesia / Sri Lanka)

Everything for this trip is already scaffolded. When you finish a leg, you only
write content + drop in photos, then "flip" the post live. No layout/admin work.

## What already exists

**5 destination pages (LIVE now):**

| Page | URL |
|---|---|
| Malaysia — Kuala Lumpur | `/malaysia-kuala-lumpur/` |
| Indonesia — Komodo & Flores | `/indonesia-komodo-flores/` |
| Indonesia — Lombok & Rinjani | `/indonesia-lombok-rinjani/` |
| Indonesia — Sumatra | `/indonesia-sumatra/` |
| Sri Lanka | `/sri-lanka/` |

They appear on the Destinations page (grid + map pin + legend) and in the
sitemap. While a leg has no published posts, its page shows a friendly
"stories and photos coming soon" line.

**14 blog post stubs (HIDDEN / draft):** each is a complete page (nav, hero with
the right date, breadcrumb, footer, comments, schema) plus a draft outline taken
from your itinerary. They are `noindex` and **not linked** from anywhere, so they
are effectively invisible until you publish them.

| Slug (`/slug/`) | Destination | Planned date |
|---|---|---|
| `kuala-lumpur-stopover` | Malaysia | Jun 28 |
| `flores-arrival-labuan-bajo` | Komodo & Flores | Jun 30 |
| `komodo-national-park-boat-trip` | Komodo & Flores | Jul 5–9 |
| `lombok-arrival` | Lombok & Rinjani | Jul 9 |
| `mount-rinjani-3-day-trek` | Lombok & Rinjani | Jul ~12 |
| `bukit-lawang-jungle-trek-orangutans` | Sumatra | Jul 15–18 |
| `berastagi-mount-sibayak` | Sumatra | Jul 19–20 |
| `lake-toba-samosir-island` | Sumatra | Jul 20–22 |
| `kuala-lumpur-stopover-return` | Malaysia | Jul ~24 |
| `sigiriya-dambulla` | Sri Lanka | Jul 25–29 |
| `kandy` | Sri Lanka | Jul 29 |
| `ella-tea-country` | Sri Lanka | Jul 30–31 |
| `arugam-bay-surf-safari` | Sri Lanka | Aug 1–3 |
| `colombo` | Sri Lanka | Aug 4–6 |

## How to write + publish a finished post

There are two ways. Use whichever you prefer.

### Option A — let the generator do the wiring (recommended)

The generator `tools/gen_asia2026.py` is the source of truth for the stubs and
the destination cards. To publish a post:

1. **Write the content** in the post's stub file, e.g.
   `option-b-static/site/bukit-lawang-jungle-trek-orangutans/index.html`.
   Replace the draft banner + outline with real paragraphs and photos. For images,
   copy them into `option-b-static/site/wp-content/uploads/2026/07/` and use the
   same markup as older posts:
   ```html
   <p class='content-image'><a href='/wp-content/uploads/2026/07/IMG.jpg'><img src='/wp-content/uploads/2026/07/IMG.jpg' alt='...'></a></p>
   ```
   (Remember `wp-content/uploads/` is gitignored — `git add -f` the new images.)
2. In `tools/gen_asia2026.py`, find that post in the `POSTS` list and add
   `live=True` (and optionally `card_img="/wp-content/uploads/2026/07/IMG.jpg"`
   for the card thumbnail on the destination page).
3. Re-run: `python tools/gen_asia2026.py`.
   - ⚠️ Re-running **overwrites** stub files from the script. So: only set
     `live=True` AFTER you've moved your written content into the script's
     `outline`/lead, **or** (simpler) skip the generator for the body and use
     Option B below. The generator is best for posts you haven't hand-edited yet.

Because of that overwrite caveat, in practice **Option B is easier once you've
hand-written a post.**

### Option B — publish a hand-written post manually (3 small edits)

After you've written the post body in its stub file:

1. **Remove the draft markers** in the post file:
   - delete the line `<meta name="robots" content="noindex">`
   - delete the yellow "DRAFT — not yet linked publicly" banner `<div>`
2. **Add its card** to the destination page (e.g. `indonesia-sumatra/index.html`).
   If the page still shows the "coming soon" line, replace that line with:
   ```html
   <h2>Posts from this destination</h2><div class="post-cards">
   <div class="post-card">
     <a href="/SLUG/" class="post-card-img"><img src="/wp-content/uploads/2026/07/IMG.jpg" alt="TITLE"></a>
     <div class="post-card-body">
       <p class="meta">DATE</p>
       <h3><a href="/SLUG/">TITLE</a></h3>
       <p>One-line teaser…</p>
       <a href="/SLUG/" class="read-more">Read more &rarr;</a>
     </div>
   </div>
   </div>
   ```
   For each additional post on the same page, add another `<div class="post-card">…</div>`
   block inside the existing `<div class="post-cards">` (newest first).
3. **(Optional) add to the blog index** `blog/index.html` — paste the same
   `post-card` block at the top of its `<div class="post-cards">`, and add a
   `<url>` line to `sitemap.xml`.

That's it. Commit and push to `main`; the GitHub Action deploys to Hostinger
automatically (changes under `option-b-static/site/**` trigger it).

## Multiple posts per place

Fully supported. Just create another file with a new descriptive slug (e.g.
`komodo-pink-beach-and-mantas/`) — copy an existing stub as a starting point, or
add another entry to `POSTS` in the generator — and add its card to the same
destination page. Nothing assumes one post per place.

## Homepage "Featured Destinations" (optional, do later)

The homepage `index.html` has a curated **Featured Destinations** photo grid.
It uses real photos, so it was left unchanged (no broken images). Once you have a
hero photo from this trip, add one card at the top of that grid:
```html
<a href="/sri-lanka/" class="dest-card">
  <img src="/wp-content/uploads/2026/08/HERO.jpg" alt="Sri Lanka" loading="lazy">
  <div class="dest-card-overlay"><div><h3>Sri Lanka</h3><span>July/August 2026</span></div></div>
</a>
```

## Adding hero images to the destination pages

The 5 destination cards on the Destinations page currently use styled text
placeholders (dark box with the name) because there are no photos yet. To swap in
a real photo, replace the placeholder `<a class="dest-card-img" style="…"><span>…</span></a>`
with `<a class="dest-card-img"><img src="…" alt="…"></a>` (copy the format from
any older card like Peru).
