# One-time YouTube upload setup

This lets `tools/youtube_upload.py` upload trip clips to **your** YouTube channel.
You only do this **once**. It needs your Google account, so only you can do it —
I (the assistant) can't, because I never hold your Google credentials.

Budget ~10–15 minutes. Nothing here is committed to git (the secret files are
gitignored).

## Step 1 — Create a Google Cloud project
1. Go to https://console.cloud.google.com/ and sign in with the Google account
   that owns the YouTube channel.
2. Top bar → project dropdown → **New Project** → name it e.g. `4globetrotters` →
   Create, then select it.

## Step 2 — Enable the YouTube Data API
1. Left menu → **APIs & Services → Library**.
2. Search **"YouTube Data API v3"** → click it → **Enable**.

## Step 3 — Configure the consent screen
1. **APIs & Services → OAuth consent screen**.
2. User type: **External** → Create.
3. Fill the required fields (app name e.g. `4globetrotters uploader`, your email
   for support + developer contact). Save and continue.
4. **Scopes**: you can skip adding scopes here (the script requests the upload
   scope itself). Save and continue.
5. **Test users**: click **Add users** and add your own Google email. Save.
   - (Leaving the app in "Testing" is fine — as a test user you can upload
     indefinitely. You do NOT need to publish/verify the app.)

## Step 4 — Create the OAuth client
1. **APIs & Services → Credentials → Create credentials → OAuth client ID**.
2. Application type: **Desktop app** → name it anything → Create.
3. Click **Download JSON** on the client you just made.
4. Save that file as exactly:  `tools/client_secret.json`  in this repo.

## Step 5 — First run (browser consent, once)
From the repo root:
```
python tools/youtube_upload.py --folder "G:\My Drive\Pictures\2026 Labuan Bajo 2+3" --prefix "Labuan Bajo" --dry-run
```
That just lists videos (no auth needed). Then do a real run:
```
python tools/youtube_upload.py --folder "G:\My Drive\Pictures\2026 Labuan Bajo 2+3" --prefix "Labuan Bajo"
```
- A browser window opens → sign in → "Google hasn't verified this app" →
  **Continue** (it's your own app) → allow **upload YouTube videos**.
- A `tools/token.json` is written and cached. Future runs are silent — no browser.

## After that
- Each clip is uploaded **unlisted** (embeddable, but not shown publicly on your
  channel or in search). Change with `--privacy public` if you ever want.
- The script prints a ready-to-paste `<div class='video-embed'>…</div>` line for
  each video. Hand those to me (or paste them into the post) and I'll place them
  in the right spot.
- Re-running is safe: already-uploaded clips (matched by content) are skipped, so
  you never double-upload or waste quota.

## Good to know / limits
- **Quota:** the default YouTube Data API quota allows roughly **6 uploads/day**.
  Fine for a few clips per post; for a big batch, spread it over days (the script
  stops cleanly and tells you when quota is hit — just run again tomorrow).
- **Secrets:** `client_secret.json`, `token.json`, and `youtube_uploads.json` are
  gitignored and must never be committed.
- To revoke access later: https://myaccount.google.com/permissions
