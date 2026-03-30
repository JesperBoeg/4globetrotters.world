# import-comments.ps1 — Import WordPress comments into Remark42
# Run AFTER deploy.ps1 has finished successfully.
#
# What this does:
#   1. Copies the WordPress XML export to the running Fly.io container
#   2. Runs the Remark42 built-in WordPress importer inside it
#   The importer maps WordPress post URLs -> Remark42 comment threads automatically.

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$xmlPath = "C:\Users\agile\Downloads\4globetrotters.WordPress.2026-03-28.xml"
$appName = "4globetrotters-comments"
$siteId  = "4globetrotters"

if (-not (Test-Path $xmlPath)) {
    Write-Error "WordPress XML not found at: $xmlPath"
    exit 1
}

Write-Host "=== Uploading WordPress XML to Fly.io container ===" -ForegroundColor Cyan
# Copy the XML into the container's /tmp folder
fly sftp shell -a $appName -C "put `"$xmlPath`" /tmp/wp-export.xml"

Write-Host ""
Write-Host "=== Running Remark42 WordPress importer ===" -ForegroundColor Cyan
# This runs inside the container - maps WP post permalinks to Remark42 page URLs
fly ssh console -a $appName -C "remark42 import --provider=wordpress --site=$siteId --file=/tmp/wp-export.xml"

Write-Host ""
Write-Host "Done! Your old WordPress comments are now in Remark42." -ForegroundColor Green
Write-Host "Visit https://4globetrotters-comments.fly.dev/web to see the admin panel."
