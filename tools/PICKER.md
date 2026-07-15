# Media picker — choose exactly which photos & videos go in a blog post

Instead of the assistant guessing which shots to use, **you** pick them in a small
local tool, then the assistant builds the post from your exact selection.

## Run it

From the repo root:

```
python tools/picker.py
```

A browser opens at <http://localhost:8765>. Everything runs locally on your PC —
nothing is uploaded, no internet needed.

1. **Pick a folder** from the dropdown (lists sub-folders of `G:\My Drive\Pictures`).
2. **Photos tab** — photos are shown **oldest first**, 2 rows of 3 at a time, with
   **JPG and HEIC mixed together by date** (not grouped by format).
   - Click the circle (top-left) to **tick** a photo, or click the caption.
   - Click the image (or "🔍 view") to open a **big preview** to judge detail.
     In the preview: **spacebar** toggles select, **←/→** move between photos,
     **Esc** closes.
   - Use **Prev/Next**, the **page jump** box, or **←/→** arrow keys to move through
     pages. **"Selected only"** shows just your ticks so you can review/prune.
3. **Videos tab** — same UI. Each shows a poster frame + duration; click to play
   inline in the preview.
4. **360° photos** appear inline in the Photos tab with a blue **360°** badge; the
   preview opens them as a **spinnable sphere** (drag to look around). See below.
5. Hit **Save selection**. Your ticks are also **remembered per folder**, so you can
   close the tool and come back to the same folder later.
6. Tell the assistant **"selection done"** — it reads `tools/blog_selection.json`,
   converts exactly those photos to web JPGs, uploads exactly those videos to
   YouTube, and writes the post from your description of the trip.

Options: `--root "G:\My Drive\Pictures"` (folder the dropdown lists), `--port 8765`.

## 360° photos (Insta360 etc.)

The picker auto-detects 360° panoramas and marks them with a **360°** badge:

- **Equirectangular JPGs** (already-stitched 360s, e.g. exported from Insta360
  Studio, or any 2:1 spherical JPG with GPano metadata) → shown as **360°**, ready
  to use. This is the recommended, best-quality path.
- **Already-stitched `.insp`** files (2:1) → also shown as **360°**, converted
  losslessly.
- **Raw dual-fisheye `.insp`** (straight off the camera, roughly square) → shown
  dimmed with a **"360 · needs Studio"** badge. These aren't auto-stitched (a clean
  stitch needs Insta360 Studio). Export them as equirectangular JPG from Insta360
  Studio into the folder and they'll turn into proper spinnable 360s.

On the **blog**, a chosen 360 becomes an interactive, draggable sphere via the
self-hosted **Pannellum** viewer (`/assets/pannellum/`, ~21KB, loaded only on posts
that have a 360). The embed markup is:

```html
<div class="pano-embed" data-pano="/wp-content/uploads/2026/07/xxx-360.jpg"
     data-caption="Optional caption"></div>
```
and the post's `<head>` (or before `</body>`) needs:
```html
<script src="/assets/pano-init.js" defer></script>
```
The `.pano-embed` CSS lives in `assets/subpage.css`; the viewer lazy-loads when
scrolled near, so pages stay fast.

## Files it writes (all gitignored, local only)

- `tools/blog_selection.json` — the handoff file: `{folder, photos:[…], videos:[…]}`.
- `tools/picker_state.json` — per-folder saved ticks (so reopening restores them).
- `tools/.picker_cache/` — thumbnail cache for fast paging.
