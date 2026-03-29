# 4Globetrotters.world Migration: simply.com → Hostinger

## Overview
- **Site**: www.4globetrotters.world (WordPress travel blog)
- **From**: simply.com
- **To**: Hostinger
- **Method**: All-in-One WP Migration plugin (easiest, most reliable)

---

## STEP 1: Sign Up at Hostinger (5 minutes)

1. Go to: https://www.hostinger.com/wordpress-hosting
2. Select **Premium WordPress** plan (~€2.99/month if paying yearly)
3. During checkout:
   - Choose **"I already have a domain"**
   - Enter: `4globetrotters.world`
   - Pick datacenter: **Europe (Netherlands or Lithuania)** for best speed
4. After purchase, go to **hPanel** (Hostinger's control panel)
5. Click **"Setup"** on your new hosting → Select **"Migrate my website"**

**IMPORTANT**: Don't change DNS yet! We'll do that after migration is verified.

---

## STEP 2: Install Migration Plugin on Current Site (2 minutes)

Log into your current WordPress at: https://4globetrotters.world/wp-admin

1. Go to **Plugins → Add New**
2. Search for: `All-in-One WP Migration`
3. Install and **Activate** the plugin by ServMask
4. Also install: `All-in-One WP Migration Unlimited Extension` (optional, for large sites)

---

## STEP 3: Export Your Site (5-10 minutes)

In your WordPress admin:

1. Go to **All-in-One WP Migration → Export**
2. Click **"Export To"** → Select **"File"**
3. Wait for export to complete (may take 5-10 min for a site with many photos)
4. **Download** the .wpress file to your computer
5. Save it to: `C:\Users\agile\VSCode projects\4globetrotters-migration\backup\`

**Expected file size**: 500MB - 2GB (depending on how many photos you have)

---

## STEP 4: Set Up WordPress on Hostinger (5 minutes)

In Hostinger hPanel:

1. Go to **Websites → Manage**
2. Click **Auto Installer → WordPress**
3. Install WordPress with these settings:
   - Admin username: (choose your own)
   - Admin password: (strong password)
   - Admin email: your email
   - Website title: 4Globetrotters
4. Wait for installation to complete

**Temporary URL**: Hostinger gives you a preview URL like `srv123.main-hosting.eu`
Use this to access your new WordPress installation before DNS change.

---

## STEP 5: Import to Hostinger (10-20 minutes)

1. Access your NEW WordPress on Hostinger via the temporary URL
2. Install **All-in-One WP Migration** plugin (same as Step 2)
3. Go to **All-in-One WP Migration → Import**
4. Upload your .wpress backup file
5. **Confirm** the import (it will overwrite the fresh installation)
6. After import: **log in again** using your OLD WordPress credentials

---

## STEP 6: Verify Before DNS Change

Before switching DNS, verify everything works:

- [ ] Homepage loads correctly on temp URL
- [ ] Blog posts display with images
- [ ] Navigation menus work
- [ ] About page loads
- [ ] Contact information correct
- [ ] Test a few trip pages (Peru, Galapagos, etc.)

---

## STEP 7: Change DNS (Final Step)

**Option A: Change Nameservers (recommended)**

Log into wherever you registered 4globetrotters.world and change nameservers to:
```
ns1.dns-parking.com
ns2.dns-parking.com
```
(Hostinger will show you the exact nameservers in hPanel → Domains)

**Option B: Change A Record**

If you want to keep current nameservers, just update the A record:
- Log into your DNS provider
- Change A record for `@` and `www` to point to your Hostinger IP
- (Get the IP from hPanel → Hosting → Manage → Website → Details)

**Propagation**: DNS changes take 1-48 hours (usually ~1 hour)

---

## STEP 8: Post-Migration Checklist

After DNS propagates:

- [ ] Site loads at https://4globetrotters.world
- [ ] SSL certificate works (https padlock)
- [ ] Images load correctly
- [ ] Forms work (if any)
- [ ] Speed improved?

---

## Troubleshooting

### Import fails due to file size
Hostinger free tier limits uploads to ~256MB. Solutions:
1. Use FTP upload method in the plugin
2. Or use Hostinger's free migration service (they do it for you)

### Images missing after migration
Run in WordPress admin: **Tools → Available Tools → Regenerate Thumbnails**

### SSL Certificate issues
In hPanel → Security → SSL, install free SSL certificate

---

## Hostinger Free Migration Service

If any step fails, Hostinger offers **FREE migration**:
1. In hPanel, go to **Websites → Migrate Website**
2. Provide your simply.com WordPress login
3. They handle everything (takes 24-48 hours)

---

## Support Contacts

- Hostinger support: 24/7 live chat in hPanel
- Your domain registrar: for DNS help

