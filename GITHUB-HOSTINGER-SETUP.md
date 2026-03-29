# GitHub + Hostinger Setup (Static Option B)

This setup uses a two-phase deployment model:

1. Initial full publish to Hostinger from local machine (includes all media uploads).
2. Ongoing GitHub deployments for HTML/CSS/JS updates (excludes large uploads folder).

## 1) Go Live on Hostinger Now (Initial Full Upload)

### A. Build latest static output

Run:

```powershell
& "C:\Users\agile\VSCode projects\4globetrotters-migration\build-option-b-static.ps1"
```

### B. Upload full site to Hostinger `public_html`

Use Hostinger FTP details in hPanel (`Files -> FTP Accounts`) and upload everything from:

`C:\Users\agile\VSCode projects\4globetrotters-migration\option-b-static\site`

Target folder on Hostinger:

`/public_html/`

## 2) Initialize Local Git Repository

Run from project root:

```powershell
Set-Location "C:\Users\agile\VSCode projects\4globetrotters-migration"
git init
git branch -M main
git add .
```

## 3) Create GitHub Repository and Connect Remote

Create an empty GitHub repo (for example: `4globetrotters-static`).

Then run:

```powershell
git remote add origin <YOUR_GITHUB_REPO_URL>
```

## 4) Add Hostinger Secrets in GitHub

In GitHub repo: `Settings -> Secrets and variables -> Actions`

Add these repository secrets:

- `HOSTINGER_FTP_HOST`
- `HOSTINGER_FTP_USER`
- `HOSTINGER_FTP_PASS`

## 5) Push to Trigger Auto Deploy

After you are ready:

```powershell
git commit -m "Initial static site pipeline"
git push -u origin main
```

The workflow in `.github/workflows/deploy-hostinger.yml` will deploy files from `option-b-static/site/` to `/public_html/`.

## Notes

- `.gitignore` excludes `backup/` and `option-b-static/site/wp-content/uploads/` to keep repository size manageable.
- Because uploads are excluded from GitHub deploys, upload new media files to Hostinger when adding content that references new images.
- Existing uploaded media remains on Hostinger and continues to be served.
