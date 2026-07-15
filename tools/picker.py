# -*- coding: utf-8 -*-
"""
Local photo/video picker for choosing exactly which media go into a blog post.

Runs entirely on your desktop (nothing is uploaded, no internet needed). It reads
a folder of trip photos/videos, shows them oldest-first in a 2x3 grid, and lets
you tick the ones to use. Photos and videos are separate tabs. When you hit Save,
it writes tools/blog_selection.json with your exact picks, and the assistant then
builds the blog from those files.

USAGE:
    python tools/picker.py
    # then a browser opens at http://localhost:8765
    # 1. pick a folder from the dropdown
    # 2. tick photos (2 rows of 3 at a time, oldest first) -> Save
    # 3. switch to the Videos tab, tick videos -> Save
    # 4. tell the assistant "selection done"

Options:
    --root "G:\\My Drive\\Pictures"   base folder the dropdown lists (default this)
    --port 8765
"""
import argparse
import base64
import hashlib
import io
import json
import subprocess
import sys
import threading
import time
import urllib.parse
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from PIL import Image, ImageOps
try:
    import pillow_heif
    pillow_heif.register_heif_opener()
    HEIC_OK = True
except Exception:
    HEIC_OK = False

TOOLS = Path(__file__).resolve().parent
SELECTION_FILE = TOOLS / "blog_selection.json"
STATE_FILE = TOOLS / "picker_state.json"          # per-folder saved ticks
CACHE = TOOLS / ".picker_cache"                    # thumbnail cache
CACHE.mkdir(exist_ok=True)

FFMPEG = r"C:\ffmpeg\bin\ffmpeg.exe"
FFPROBE = r"C:\ffmpeg\bin\ffprobe.exe"

IMG_EXTS = {".jpg", ".jpeg", ".heic", ".png", ".insp"}
VID_EXTS = {".mov", ".mp4", ".m4v", ".avi", ".mkv", ".webm"}
THUMB = 520          # thumbnail longest side
PREVIEW = 1600       # full-screen preview longest side

ROOT = None          # base dir for the folder dropdown (set in main)


# ---------- media helpers ----------

def exif_key(p: Path):
    """Sort key: EXIF capture time first, else mtime, else name (oldest first)."""
    try:
        ex = Image.open(p).getexif()
        for tag in (36867, 306):          # DateTimeOriginal, DateTime
            v = ex.get(tag)
            if v:
                return (0, str(v), p.name)
    except Exception:
        pass
    try:
        return (1, p.stat().st_mtime, p.name)
    except Exception:
        return (2, 0, p.name)


def capture_label(p: Path):
    try:
        ex = Image.open(p).getexif()
        for tag in (36867, 306):
            v = ex.get(tag)
            if v:
                return str(v)
    except Exception:
        pass
    try:
        return time.strftime("%Y-%m-%d %H:%M", time.localtime(p.stat().st_mtime))
    except Exception:
        return ""


def _has_gpano(p: Path) -> bool:
    """True if the file carries GPano XMP marking it as an equirectangular 360.
    Scans the first ~200KB for the GPano projection markers (cheap, no deps)."""
    try:
        with open(p, "rb") as f:
            head = f.read(200000)
        return (b"GPano:ProjectionType" in head and b"equirectangular" in head) \
            or b"<GPano:ProjectionType>equirectangular" in head \
            or b'GPano:ProjectionType="equirectangular"' in head
    except Exception:
        return False


def classify_360(p: Path):
    """Return one of:
      'flat'    - a normal photo
      '360'     - an equirectangular 360 ready to use (GPano, or 2:1 pano JPG, or
                  an already-stitched .insp)
      '360raw'  - a raw dual-fisheye .insp that needs Insta360 Studio export
    Detection is cheap: metadata + image dimensions only.
    """
    ext = p.suffix.lower()
    try:
        with Image.open(p) as im:
            w, h = im.size
    except Exception:
        w = h = 0
    ratio = (w / h) if h else 0

    if ext == ".insp":
        # .insp is a JPEG-with-metadata. Already-stitched exports are ~2:1
        # equirectangular; raw camera files are dual-fisheye (~1:1 or two circles).
        if _has_gpano(p) or (1.9 <= ratio <= 2.1):
            return "360"
        return "360raw"

    # Regular JPG/JPEG that is actually a 360: GPano metadata, or a clean 2:1
    # panorama at real resolution.
    if ext in (".jpg", ".jpeg"):
        if _has_gpano(p):
            return "360"
        if 1.98 <= ratio <= 2.02 and w >= 4000:
            return "360"
    return "flat"


def list_media(folder: Path):
    imgs, vids = [], []
    for p in folder.iterdir():
        if not p.is_file():
            continue
        e = p.suffix.lower()
        if e in IMG_EXTS:
            imgs.append(p)
        elif e in VID_EXTS:
            vids.append(p)
    imgs.sort(key=exif_key)
    vids.sort(key=lambda x: (x.stat().st_mtime, x.name))
    return imgs, vids


def _cache_path(folder: Path, name: str, kind: str, size: int):
    h = hashlib.md5(f"{folder}|{name}|{kind}|{size}".encode("utf-8")).hexdigest()
    return CACHE / f"{h}.jpg"


def _open_image(src: Path):
    """Open any supported still, including .insp (a JPEG with a non-JPEG ext)."""
    try:
        return Image.open(src)
    except Exception:
        # .insp / odd files: force-load the bytes as JPEG
        with open(src, "rb") as f:
            return Image.open(io.BytesIO(f.read()))


def img_thumb(folder: Path, name: str, size: int) -> bytes:
    cp = _cache_path(folder, name, "img", size)
    if cp.exists():
        return cp.read_bytes()
    src = folder / name
    im = _open_image(src)
    im = ImageOps.exif_transpose(im).convert("RGB")
    im.thumbnail((size, size))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=82)
    data = buf.getvalue()
    cp.write_bytes(data)
    return data


def pano_jpg(folder: Path, name: str) -> bytes:
    """Serve a full-resolution equirectangular JPG for the 360 sphere preview.
    For already-equirectangular sources this is a straight (re-)encode."""
    cp = _cache_path(folder, name, "pano", 0)
    if cp.exists():
        return cp.read_bytes()
    src = folder / name
    im = _open_image(src)
    im = ImageOps.exif_transpose(im).convert("RGB")
    # cap very large panos so the browser sphere stays smooth
    if im.width > 5400:
        im = im.resize((5400, im.height * 5400 // im.width))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=88)
    data = buf.getvalue()
    cp.write_bytes(data)
    return data


def vid_poster(folder: Path, name: str, size: int) -> bytes:
    cp = _cache_path(folder, name, "vidposter", size)
    if cp.exists():
        return cp.read_bytes()
    src = folder / name
    # grab a frame ~1s in
    out = subprocess.run(
        [FFMPEG, "-y", "-ss", "1", "-i", str(src), "-frames:v", "1",
         "-vf", f"scale={size}:-1", "-f", "mjpeg", "pipe:1"],
        capture_output=True)
    data = out.stdout
    if not data:  # fallback: first frame
        out = subprocess.run(
            [FFMPEG, "-y", "-i", str(src), "-frames:v", "1",
             "-vf", f"scale={size}:-1", "-f", "mjpeg", "pipe:1"],
            capture_output=True)
        data = out.stdout
    if data:
        cp.write_bytes(data)
    return data


def vid_duration(folder: Path, name: str) -> float:
    try:
        out = subprocess.run(
            [FFPROBE, "-v", "quiet", "-show_entries", "format=duration",
             "-of", "default=nk=1:nw=1", str(folder / name)],
            capture_output=True, text=True)
        return float(out.stdout.strip())
    except Exception:
        return 0.0


# ---------- persistence ----------

def load_state():
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")


# ---------- HTTP handler ----------

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send(self, code, body, ctype="application/json"):
        if isinstance(body, (dict, list)):
            body = json.dumps(body).encode("utf-8")
        elif isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        q = urllib.parse.parse_qs(u.query)
        path = u.path

        if path == "/":
            return self._send(200, PAGE, "text/html; charset=utf-8")

        if path == "/api/folders":
            folders = []
            if ROOT.exists():
                for p in sorted(ROOT.iterdir()):
                    if p.is_dir():
                        folders.append(p.name)
            return self._send(200, {"root": str(ROOT), "folders": folders})

        if path == "/api/media":
            folder = Path(q["folder"][0])
            imgs, vids = list_media(folder)
            state = load_state().get(str(folder), {"photos": [], "videos": []})
            photos = [{"name": p.name, "date": capture_label(p),
                       "k360": classify_360(p)} for p in imgs]
            videos = [{"name": p.name, "date": capture_label(p),
                       "dur": round(vid_duration(folder, p.name), 1)} for p in vids]
            return self._send(200, {
                "folder": str(folder),
                "photos": photos, "videos": videos,
                "selected_photos": state.get("photos", []),
                "selected_videos": state.get("videos", []),
            })

        if path == "/api/thumb":
            folder = Path(q["folder"][0]); name = q["name"][0]
            kind = q.get("kind", ["img"])[0]
            size = int(q.get("size", [str(THUMB)])[0])
            try:
                data = vid_poster(folder, name, size) if kind == "vid" else img_thumb(folder, name, size)
                return self._send(200, data, "image/jpeg")
            except Exception as e:
                return self._send(500, str(e), "text/plain")

        if path == "/api/pano":
            # full equirectangular JPG for the 360 sphere preview
            folder = Path(q["folder"][0]); name = q["name"][0]
            try:
                return self._send(200, pano_jpg(folder, name), "image/jpeg")
            except Exception as e:
                return self._send(500, str(e), "text/plain")

        if path == "/api/videofile":
            # stream the raw video for inline playback
            folder = Path(q["folder"][0]); name = q["name"][0]
            src = folder / name
            data = src.read_bytes()
            ctype = "video/mp4" if src.suffix.lower() in (".mp4", ".m4v") else "video/quicktime"
            self.send_response(200)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Accept-Ranges", "bytes")
            self.end_headers()
            self.wfile.write(data)
            return

        return self._send(404, {"error": "not found"})

    def do_POST(self):
        u = urllib.parse.urlparse(self.path)
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length) or b"{}")

        if u.path == "/api/save":
            folder = body["folder"]
            photos = body.get("photos", [])
            videos = body.get("videos", [])
            # per-folder state
            state = load_state()
            state[folder] = {"photos": photos, "videos": videos}
            save_state(state)
            # the actual handoff file
            SELECTION_FILE.write_text(json.dumps({
                "folder": folder, "photos": photos, "videos": videos,
                "saved_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            }, indent=2, ensure_ascii=False), encoding="utf-8")
            return self._send(200, {"ok": True,
                                    "photos": len(photos), "videos": len(videos),
                                    "file": str(SELECTION_FILE)})

        if u.path == "/api/state":
            # autosave ticks per folder as you go
            folder = body["folder"]
            state = load_state()
            state[folder] = {"photos": body.get("photos", []),
                             "videos": body.get("videos", [])}
            save_state(state)
            return self._send(200, {"ok": True})

        return self._send(404, {"error": "not found"})


# ---------- frontend (single page) ----------

PAGE = r"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><title>Blog media picker</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/pannellum@2.5.6/build/pannellum.css">
<script src="https://cdn.jsdelivr.net/npm/pannellum@2.5.6/build/pannellum.js"></script>
<style>
  :root { --accent:#c0392b; }
  * { box-sizing:border-box; }
  body { margin:0; font-family:-apple-system,Segoe UI,Roboto,sans-serif; background:#f4f5f7; color:#1a1a1a; }
  header { position:sticky; top:0; z-index:10; background:#fff; border-bottom:1px solid #e3e3e3;
           padding:10px 18px; display:flex; align-items:center; gap:14px; flex-wrap:wrap; box-shadow:0 1px 8px rgba(0,0,0,.05); }
  header h1 { font-size:1rem; margin:0; font-weight:700; }
  .tabs { display:flex; gap:6px; }
  .tab { padding:6px 16px; border-radius:20px; border:1px solid #ddd; background:#f5f5f5; cursor:pointer; font-size:.85rem; }
  .tab.active { background:var(--accent); color:#fff; border-color:var(--accent); }
  .spacer { flex:1; }
  .btn { padding:7px 16px; border-radius:8px; border:1px solid #ccc; background:#fff; cursor:pointer; font-size:.85rem; }
  .btn:hover { background:#f0f0f0; }
  .btn.primary { background:var(--accent); color:#fff; border-color:var(--accent); }
  .btn.primary:hover { opacity:.9; }
  .count { font-size:.85rem; color:#555; }
  .count b { color:var(--accent); }
  main { max-width:1200px; margin:0 auto; padding:20px 18px 80px; }
  .start { max-width:560px; margin:60px auto; background:#fff; padding:34px; border-radius:14px; box-shadow:0 4px 24px rgba(0,0,0,.08); }
  .start h2 { margin:0 0 6px; }
  .start p { color:#666; margin:0 0 20px; font-size:.92rem; }
  select { width:100%; padding:10px; font-size:1rem; border-radius:8px; border:1px solid #ccc; margin-bottom:18px; }
  .grid { display:grid; grid-template-columns:repeat(3,1fr); gap:16px; }
  .cell { background:#fff; border:3px solid transparent; border-radius:12px; overflow:hidden; cursor:pointer;
          box-shadow:0 2px 10px rgba(0,0,0,.06); transition:transform .12s, border-color .12s; position:relative; }
  .cell:hover { transform:translateY(-2px); }
  .cell.sel { border-color:var(--accent); }
  .cell .imgwrap { aspect-ratio:4/3; background:#e9e9e9; display:flex; align-items:center; justify-content:center; overflow:hidden; }
  .cell img { width:100%; height:100%; object-fit:cover; display:block; }
  .cell .cap { padding:7px 10px; font-size:.72rem; color:#666; display:flex; justify-content:space-between; gap:8px; }
  .cell .cap .nm { overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
  .check { position:absolute; top:8px; left:8px; width:26px; height:26px; border-radius:50%; background:rgba(255,255,255,.9);
           border:2px solid #bbb; display:flex; align-items:center; justify-content:center; font-size:16px; color:#fff; }
  .cell.sel .check { background:var(--accent); border-color:var(--accent); }
  .badge { position:absolute; top:8px; right:8px; background:rgba(0,0,0,.7); color:#fff; font-size:.7rem; padding:2px 7px; border-radius:10px; }
  .badge360 { position:absolute; top:8px; right:8px; background:#2e86de; color:#fff; font-size:.7rem; font-weight:700; padding:2px 8px; border-radius:10px; letter-spacing:.3px; }
  .badgeraw { position:absolute; top:8px; right:8px; background:#e67e22; color:#fff; font-size:.66rem; font-weight:700; padding:2px 7px; border-radius:10px; }
  .cell.raw { opacity:.7; }
  #pano { width:94vw; height:82vh; }
  .peek { position:absolute; bottom:8px; right:8px; background:rgba(0,0,0,.55); color:#fff; font-size:.68rem; padding:3px 8px; border-radius:10px; }
  .pager { display:flex; align-items:center; justify-content:center; gap:12px; margin:22px 0 4px; flex-wrap:wrap; }
  .pager input { width:56px; padding:5px; text-align:center; border:1px solid #ccc; border-radius:6px; }
  .progress { text-align:center; font-size:.8rem; color:#888; margin-top:4px; }
  /* fullscreen preview */
  .overlay { position:fixed; inset:0; background:rgba(0,0,0,.9); z-index:50; display:none; align-items:center; justify-content:center; flex-direction:column; }
  .overlay.on { display:flex; }
  .overlay img, .overlay video { max-width:94vw; max-height:82vh; border-radius:6px; }
  .overlay .obar { color:#fff; margin-top:14px; display:flex; gap:14px; align-items:center; }
  .overlay .obar .btn { background:#222; color:#fff; border-color:#444; }
  .empty { text-align:center; color:#888; padding:60px; }
</style></head>
<body>
<header id="hdr" style="display:none">
  <h1 id="folderName">—</h1>
  <div class="tabs">
    <div class="tab active" data-tab="photos" id="tabPhotos">Photos</div>
    <div class="tab" data-tab="videos" id="tabVideos">Videos</div>
  </div>
  <div class="count">Selected: <b id="selCount">0</b></div>
  <label class="count"><input type="checkbox" id="selOnly"> Selected only</label>
  <div class="spacer"></div>
  <button class="btn" id="changeFolder">Change folder</button>
  <button class="btn primary" id="saveBtn">Save selection</button>
</header>

<main>
  <div id="startScreen" class="start">
    <h2>Pick a folder</h2>
    <p>Choose the trip folder to select photos and videos from.</p>
    <select id="folderSelect"><option>Loading…</option></select>
    <button class="btn primary" id="openFolder">Open</button>
  </div>

  <div id="browser" style="display:none">
    <div class="grid" id="grid"></div>
    <div class="pager" id="pager"></div>
    <div class="progress" id="progress"></div>
  </div>
</main>

<div class="overlay" id="overlay">
  <div id="overlayContent"></div>
  <div class="obar">
    <button class="btn" id="ovToggle">Toggle select (space)</button>
    <button class="btn" id="ovClose">Close (esc)</button>
  </div>
</div>

<script>
const PER = 6;
let folder = null, tab = "photos";
let data = { photos: [], videos: [] };
let sel = { photos: new Set(), videos: new Set() };
let page = 0, selOnly = false, ovIndex = -1;

const $ = s => document.querySelector(s);

async function loadFolders() {
  const r = await fetch("/api/folders"); const j = await r.json();
  const sel = $("#folderSelect");
  sel.innerHTML = "";
  if (!j.folders.length) { sel.innerHTML = "<option>(no sub-folders found in " + j.root + ")</option>"; return; }
  j.folders.forEach(f => { const o = document.createElement("option"); o.value = f; o.textContent = f; sel.appendChild(o); });
  window._root = j.root;
}
loadFolders();

$("#openFolder").onclick = async () => {
  const name = $("#folderSelect").value;
  folder = window._root.replace(/\\+$/,"") + "\\" + name;
  const r = await fetch("/api/media?folder=" + encodeURIComponent(folder));
  data = await r.json();
  sel.photos = new Set(data.selected_photos || []);
  sel.videos = new Set(data.selected_videos || []);
  $("#folderName").textContent = name;
  $("#startScreen").style.display = "none";
  $("#browser").style.display = "block";
  $("#hdr").style.display = "flex";
  page = 0; render();
};

$("#changeFolder").onclick = () => {
  $("#startScreen").style.display = "block";
  $("#browser").style.display = "none";
  $("#hdr").style.display = "none";
};

function items() {
  let arr = data[tab];
  if (selOnly) arr = arr.filter(x => sel[tab].has(x.name));
  return arr;
}
function pageCount() { return Math.max(1, Math.ceil(items().length / PER)); }

function render() {
  const arr = items();
  if (page >= pageCount()) page = pageCount() - 1;
  if (page < 0) page = 0;
  const start = page * PER;
  const slice = arr.slice(start, start + PER);
  const g = $("#grid");
  g.innerHTML = "";
  if (!slice.length) { g.innerHTML = "<div class='empty'>No " + tab + " here" + (selOnly ? " selected yet." : ".") + "</div>"; }
  slice.forEach((it, i) => {
    const idx = start + i;
    const div = document.createElement("div");
    const isRaw = it.k360 === "360raw";
    div.className = "cell" + (sel[tab].has(it.name) ? " sel" : "") + (isRaw ? " raw" : "");
    const kind = tab === "videos" ? "vid" : "img";
    const thumb = "/api/thumb?folder=" + encodeURIComponent(folder) + "&name=" + encodeURIComponent(it.name) + "&kind=" + kind;
    let badge = "";
    if (tab === "videos") { const m = Math.floor(it.dur/60), s = Math.round(it.dur%60); badge = "<div class='badge'>" + m + ":" + String(s).padStart(2,"0") + "</div>"; }
    else if (it.k360 === "360") { badge = "<div class='badge360'>360°</div>"; }
    else if (it.k360 === "360raw") { badge = "<div class='badgeraw'>360 · needs Studio</div>"; }
    div.innerHTML =
      "<div class='imgwrap'><img loading='lazy' src='" + thumb + "'></div>" +
      "<div class='check'>" + (sel[tab].has(it.name) ? "✓" : "") + "</div>" + badge +
      "<div class='peek'>🔍 view</div>" +
      "<div class='cap'><span class='nm' title='" + it.name + "'>" + it.name + "</span><span>" + (it.date||"") + "</span></div>";
    div.querySelector(".imgwrap").onclick = () => openPreview(idx);
    div.querySelector(".peek").onclick = (e) => { e.stopPropagation(); openPreview(idx); };
    div.querySelector(".check").onclick = (e) => { e.stopPropagation(); toggle(it.name); };
    div.querySelector(".cap").onclick = () => toggle(it.name);
    g.appendChild(div);
  });
  // pager
  const pc = pageCount();
  $("#pager").innerHTML =
    "<button class='btn' " + (page<=0?"disabled":"") + " id='prev'>&larr; Prev</button>" +
    "<span>Page <input id='pageJump' type='number' min='1' max='" + pc + "' value='" + (page+1) + "'> / " + pc + "</span>" +
    "<button class='btn' " + (page>=pc-1?"disabled":"") + " id='next'>Next &rarr;</button>";
  $("#prev") && ($("#prev").onclick = () => { page--; render(); });
  $("#next") && ($("#next").onclick = () => { page++; render(); });
  $("#pageJump").onchange = (e) => { page = Math.min(pc, Math.max(1, +e.target.value)) - 1; render(); };
  $("#progress").textContent = items().length + " " + tab + " total · " + sel[tab].size + " selected";
  $("#selCount").textContent = sel[tab].size;
  autosave();
}

function toggle(name) {
  if (sel[tab].has(name)) sel[tab].delete(name); else sel[tab].add(name);
  render();
}

async function autosave() {
  if (!folder) return;
  fetch("/api/state", { method:"POST", headers:{"Content-Type":"application/json"},
    body: JSON.stringify({ folder, photos:[...sel.photos], videos:[...sel.videos] }) });
}

// tabs
document.querySelectorAll(".tab").forEach(t => t.onclick = () => {
  document.querySelectorAll(".tab").forEach(x => x.classList.remove("active"));
  t.classList.add("active"); tab = t.dataset.tab; page = 0; render();
});
$("#selOnly").onchange = (e) => { selOnly = e.target.checked; page = 0; render(); };

// save
$("#saveBtn").onclick = async () => {
  const r = await fetch("/api/save", { method:"POST", headers:{"Content-Type":"application/json"},
    body: JSON.stringify({ folder, photos:[...sel.photos], videos:[...sel.videos] }) });
  const j = await r.json();
  alert("Saved!\n\n" + j.photos + " photos and " + j.videos + " videos.\n\nNow tell the assistant: \"selection done\".");
};

// fullscreen preview
let panoViewer = null;
function destroyPano() { if (panoViewer) { try { panoViewer.destroy(); } catch(e){} panoViewer = null; } }
function openPreview(idx) {
  destroyPano();
  ovIndex = idx;
  const arr = items(); const it = arr[idx];
  const c = $("#overlayContent");
  if (tab === "videos") {
    c.innerHTML = "<video controls autoplay src='/api/videofile?folder=" + encodeURIComponent(folder) + "&name=" + encodeURIComponent(it.name) + "'></video>";
  } else if (it.k360 === "360") {
    // interactive 360 sphere
    c.innerHTML = "<div id='pano'></div>";
    const src = "/api/pano?folder=" + encodeURIComponent(folder) + "&name=" + encodeURIComponent(it.name);
    panoViewer = pannellum.viewer("pano", { type:"equirectangular", panorama:src, autoLoad:true, autoRotate:-2, showControls:true });
  } else if (it.k360 === "360raw") {
    c.innerHTML = "<div style='color:#fff;max-width:600px;text-align:center;padding:30px'>" +
      "<div style='font-size:2rem'>🌐</div><p><b>" + it.name + "</b> is a raw dual-fisheye Insta360 file.</p>" +
      "<p style='color:#ccc'>To use it, export it as an equirectangular JPG from Insta360 Studio into this folder, then it'll show as a spinnable 360°. (You can still tick it, but it won't render as a sphere until exported.)</p></div>";
  } else {
    const big = "/api/thumb?folder=" + encodeURIComponent(folder) + "&name=" + encodeURIComponent(it.name) + "&kind=img&size=1600";
    c.innerHTML = "<img src='" + big + "'>";
  }
  $("#overlay").classList.add("on");
  $("#ovToggle").textContent = (sel[tab].has(it.name) ? "✓ Selected — click to unselect" : "Select this");
}
function closePreview() { destroyPano(); $("#overlay").classList.remove("on"); $("#overlayContent").innerHTML = ""; ovIndex = -1; }
$("#ovClose").onclick = closePreview;
$("#ovToggle").onclick = () => { const it = items()[ovIndex]; if (it) { toggle(it.name); openPreview(ovIndex); } };
document.addEventListener("keydown", (e) => {
  if ($("#overlay").classList.contains("on")) {
    if (e.key === "Escape") closePreview();
    if (e.key === " ") { e.preventDefault(); $("#ovToggle").click(); }
    if (e.key === "ArrowRight" && ovIndex < items().length-1) openPreview(ovIndex+1);
    if (e.key === "ArrowLeft" && ovIndex > 0) openPreview(ovIndex-1);
  } else if ($("#browser").style.display !== "none") {
    if (e.key === "ArrowRight") { page = Math.min(pageCount()-1, page+1); render(); }
    if (e.key === "ArrowLeft") { page = Math.max(0, page-1); render(); }
  }
});
</script>
</body></html>
"""


def main():
    global ROOT
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=r"G:\My Drive\Pictures")
    ap.add_argument("--port", type=int, default=8765)
    args = ap.parse_args()
    ROOT = Path(args.root)

    srv = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    url = f"http://localhost:{args.port}"
    print(f"Media picker running at {url}")
    print("Pick a folder, tick photos + videos, hit Save. Ctrl+C to stop.")
    threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
