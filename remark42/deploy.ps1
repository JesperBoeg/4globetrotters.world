# deploy.ps1 — One-time setup script for Remark42 on Fly.io
# Run this from the remark42/ folder: cd remark42; .\deploy.ps1
#
# Prerequisites:
#   1. Install flyctl:  winget install Superfly.flyctl
#   2. Sign up at https://fly.io (free, no credit card required for hobby tier)
#   3. Run: fly auth login

param(
    [string]$Secret,
    [string]$AdminPasswd,
    [string]$GoogleClientId,
    [string]$GoogleClientSecret
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function New-RandomSecret([int]$Length = 48) {
    $chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    $rng = [System.Security.Cryptography.RandomNumberGenerator]::Create()
    $bytes = New-Object byte[] ($Length)
    $rng.GetBytes($bytes)
    -join ($bytes | ForEach-Object { $chars[$_ % $chars.Length] })
}

if ([string]::IsNullOrWhiteSpace($Secret)) {
    $Secret = New-RandomSecret
}
if ([string]::IsNullOrWhiteSpace($AdminPasswd)) {
    $AdminPasswd = New-RandomSecret 24
}

Write-Host ""
Write-Host "=== Step 1: Create the Fly.io app ===" -ForegroundColor Cyan
Write-Host "This reads fly.toml in the current folder."
fly launch --no-deploy --copy-config

Write-Host ""
Write-Host "=== Step 2: Create a persistent 1GB volume for comment data ===" -ForegroundColor Cyan
fly volumes create remark42_data --region ams --size 1

Write-Host ""
Write-Host "=== Step 3: Set secrets ===" -ForegroundColor Cyan
Write-Host "Using provided credentials and auto-generated secrets when missing."
Write-Host ""

$secretsCmd = "SECRET=$Secret ADMIN_PASSWD=$AdminPasswd"
if ($GoogleClientId) {
    $secretsCmd += " AUTH_GOOGLE_CID=$GoogleClientId AUTH_GOOGLE_CSECRET=$GoogleClientSecret"
}

Invoke-Expression "fly secrets set $secretsCmd"

Write-Host ""
Write-Host "=== Step 4: Deploy ===" -ForegroundColor Cyan
fly deploy

Write-Host ""
Write-Host "=== Step 5: Verify ===" -ForegroundColor Cyan
fly status
Write-Host ""
Write-Host "Test: https://4globetrotters-comments.fly.dev/ping  — should return 'pong'" -ForegroundColor Green
Write-Host "ADMIN_PASSWD generated/used: $AdminPasswd" -ForegroundColor Yellow
Write-Host ""
Write-Host "=== Next: Import WordPress comments ===" -ForegroundColor Yellow
Write-Host "Run: .\import-comments.ps1"
