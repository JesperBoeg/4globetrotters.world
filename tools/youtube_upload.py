# -*- coding: utf-8 -*-
"""
Upload trip video clips to the 4globetrotters YouTube channel and print ready-to-
paste blog embed markup.

One-time setup (only the account owner can do this — see tools/YOUTUBE-SETUP.md):
  1. Create a Google Cloud project, enable "YouTube Data API v3".
  2. Create an OAuth client (type: Desktop app), download the JSON as
     tools/client_secret.json (gitignored).
  3. Run this script once; it opens a browser for consent and caches a refresh
     token in tools/token.json (gitignored). After that it runs unattended.

Usage:
  # upload every video in a folder (skips ones already uploaded):
  python tools/youtube_upload.py --folder "G:\\My Drive\\Pictures\\2026 Labuan Bajo 2+3" --prefix "Labuan Bajo"

  # upload specific files:
  python tools/youtube_upload.py "clip1.MOV" "clip2.mp4" --prefix "Komodo"

  # just print embed markup for videos already uploaded (no upload):
  python tools/youtube_upload.py --embeds-only

Options:
  --privacy {unlisted,private,public}   default: unlisted (embeddable, not listed)
  --prefix TEXT      title prefix, e.g. "Labuan Bajo" -> "Labuan Bajo — IMG_4681"
  --dry-run          list what WOULD upload, do nothing

Notes:
  - Uploaded clips are tracked by CONTENT HASH in tools/youtube_uploads.json, so
    re-running never re-uploads the same file (protects the daily API quota:
    ~6 uploads/day on the default quota).
  - Prints, for each video, the exact <div class='video-embed'>...</div> line the
    blog uses. Paste those into the post where the clip belongs.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
CLIENT_SECRET = TOOLS / "client_secret.json"
TOKEN = TOOLS / "token.json"
UPLOADS_DB = TOOLS / "youtube_uploads.json"

VIDEO_EXTS = {".mov", ".mp4", ".m4v", ".avi", ".mkv", ".webm"}
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

EMBED_TMPL = (
    "<div class='video-embed'><iframe src='https://www.youtube.com/embed/{vid}' "
    "loading='lazy' allow='accelerometer; autoplay; clipboard-write; "
    "encrypted-media; gyroscope; picture-in-picture; web-share' "
    "allowfullscreen></iframe></div>"
)


def load_db():
    if UPLOADS_DB.exists():
        return json.loads(UPLOADS_DB.read_text(encoding="utf-8"))
    return {}


def save_db(db):
    UPLOADS_DB.write_text(json.dumps(db, indent=2, ensure_ascii=False), encoding="utf-8")


def file_hash(p, chunk=1 << 20):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(chunk), b""):
            h.update(b)
    return h.hexdigest()


def get_service():
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    creds = None
    if TOKEN.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CLIENT_SECRET.exists():
                sys.exit(
                    f"Missing {CLIENT_SECRET.name}. Do the one-time setup first "
                    f"(see tools/YOUTUBE-SETUP.md)."
                )
            flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET), SCOPES)
            print("\n=== Google sign-in required ===", flush=True)
            print("A browser tab should open. If it doesn't, copy the URL that "
                  "appears below into your browser.\n", flush=True)
            try:
                creds = flow.run_local_server(
                    port=8766,
                    open_browser=True,
                    authorization_prompt_message="Open this URL to authorize:\n{url}",
                    success_message="Done — you can close this tab and return to the terminal.",
                )
            except Exception as e:
                print(f"\nOAuth flow failed: {type(e).__name__}: {e}", flush=True)
                raise
        TOKEN.write_text(creds.to_json(), encoding="utf-8")
        print("Auth OK — token cached.", flush=True)
    return build("youtube", "v3", credentials=creds)


def upload_one(service, path: Path, title: str, privacy: str):
    from googleapiclient.http import MediaFileUpload

    body = {
        "snippet": {"title": title[:100], "description": "Uploaded by 4globetrotters trip tooling.", "categoryId": "19"},  # 19 = Travel & Events
        "status": {"privacyStatus": privacy, "selfDeclaredMadeForKids": False},
    }
    media = MediaFileUpload(str(path), chunksize=-1, resumable=True)
    req = service.videos().insert(part="snippet,status", body=body, media_body=media)
    resp = None
    while resp is None:
        status, resp = req.next_chunk()
        if status:
            print(f"    ...{int(status.progress() * 100)}%")
    return resp["id"]


def gather_targets(args):
    files = []
    if args.folder:
        folder = Path(args.folder)
        if not folder.is_dir():
            sys.exit(f"Not a folder: {folder}")
        files += sorted(p for p in folder.iterdir()
                        if p.is_file() and p.suffix.lower() in VIDEO_EXTS)
    for f in args.files:
        p = Path(f)
        if p.is_file():
            files.append(p)
        else:
            print(f"  (skip, not found) {f}")
    return files


def main():
    ap = argparse.ArgumentParser(description="Upload trip videos to YouTube + print embeds.")
    ap.add_argument("files", nargs="*", help="specific video files")
    ap.add_argument("--folder", help="upload all videos in this folder")
    ap.add_argument("--prefix", default="", help="title prefix")
    ap.add_argument("--privacy", default="unlisted",
                    choices=["unlisted", "private", "public"])
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--embeds-only", action="store_true",
                    help="just print embeds for everything already uploaded")
    args = ap.parse_args()

    db = load_db()

    if args.embeds_only:
        if not db:
            print("Nothing uploaded yet.")
            return
        for h, rec in db.items():
            print(f"# {rec['title']}   ({rec['source']})")
            print(EMBED_TMPL.format(vid=rec["id"]))
        return

    targets = gather_targets(args)
    if not targets:
        sys.exit("No video files given. Use --folder or list files. (--help for usage)")

    # figure out which still need uploading
    plan = []
    for p in targets:
        h = file_hash(p)
        if h in db:
            print(f"[already up] {p.name} -> {db[h]['id']}")
        else:
            plan.append((p, h))

    print(f"\n{len(plan)} new video(s) to upload"
          + (" (DRY RUN)" if args.dry_run else "")
          + f"; privacy={args.privacy}\n")
    if args.dry_run:
        for p, _ in plan:
            print(f"  would upload: {p.name}")
        return
    if not plan:
        print("Nothing new to upload. Use --embeds-only to reprint markup.")
        return

    service = get_service()
    for p, h in plan:
        title = (f"{args.prefix} — {p.stem}" if args.prefix else p.stem).strip(" —")
        print(f"[uploading] {p.name}  as  \"{title}\"")
        try:
            vid = upload_one(service, p, title, args.privacy)
        except Exception as e:
            print(f"    ERROR: {e}")
            if "quota" in str(e).lower():
                print("    (Daily upload quota likely hit — try again tomorrow.)")
                break
            continue
        db[h] = {"id": vid, "title": title, "source": p.name, "privacy": args.privacy}
        save_db(db)
        print(f"    done -> https://youtu.be/{vid}")

    print("\n=== Embed markup (paste into the post where each clip belongs) ===\n")
    for p, h in plan:
        if h in db:
            print(f"# {db[h]['title']}")
            print(EMBED_TMPL.format(vid=db[h]["id"]))


if __name__ == "__main__":
    main()
