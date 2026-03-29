<# 
    4Globetrotters Migration Verification Script
    Run this after migration to verify everything works
#>

param(
    [string]$SiteUrl = "https://4globetrotters.world"
)

Write-Host "`n=== 4Globetrotters Migration Verification ===" -ForegroundColor Cyan
Write-Host "Testing: $SiteUrl`n"

$pages = @(
    "",
    "about-us-2",
    "peru",
    "ecuador-july-2024",
    "galapagos-june-2024",
    "western-australia-julyaugust-2022",
    "blog"
)

$passed = 0
$failed = 0

foreach ($page in $pages) {
    $url = "$SiteUrl/$page"
    try {
        $response = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 30
        if ($response.StatusCode -eq 200) {
            Write-Host "[PASS] " -ForegroundColor Green -NoNewline
            Write-Host $url
            $passed++
        } else {
            Write-Host "[FAIL] " -ForegroundColor Red -NoNewline
            Write-Host "$url - Status: $($response.StatusCode)"
            $failed++
        }
    } catch {
        Write-Host "[FAIL] " -ForegroundColor Red -NoNewline
        Write-Host "$url - Error: $($_.Exception.Message)"
        $failed++
    }
}

# Check SSL
Write-Host "`nChecking SSL Certificate..." -ForegroundColor Yellow
try {
    $request = [System.Net.HttpWebRequest]::Create($SiteUrl)
    $request.AllowAutoRedirect = $false
    $request.Timeout = 10000
    $response = $request.GetResponse()
    $cert = $request.ServicePoint.Certificate
    if ($cert) {
        $expiry = [datetime]::Parse($cert.GetExpirationDateString())
        $daysLeft = ($expiry - (Get-Date)).Days
        Write-Host "[PASS] " -ForegroundColor Green -NoNewline
        Write-Host "SSL valid, expires in $daysLeft days"
    }
    $response.Close()
} catch {
    Write-Host "[WARN] " -ForegroundColor Yellow -NoNewline
    Write-Host "Could not verify SSL: $($_.Exception.Message)"
}

# Check response time
Write-Host "`nChecking Response Time..." -ForegroundColor Yellow
$times = @()
for ($i = 1; $i -le 3; $i++) {
    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    try {
        Invoke-WebRequest -Uri $SiteUrl -UseBasicParsing -TimeoutSec 30 | Out-Null
        $sw.Stop()
        $times += $sw.ElapsedMilliseconds
    } catch {}
}
if ($times.Count -gt 0) {
    $avg = [math]::Round(($times | Measure-Object -Average).Average)
    $color = if ($avg -lt 2000) { "Green" } elseif ($avg -lt 4000) { "Yellow" } else { "Red" }
    Write-Host "Average response time: ${avg}ms" -ForegroundColor $color
}

# Summary
Write-Host "`n=== Summary ===" -ForegroundColor Cyan
Write-Host "Pages Passed: $passed" -ForegroundColor Green
Write-Host "Pages Failed: $failed" -ForegroundColor $(if ($failed -eq 0) { "Green" } else { "Red" })

if ($failed -eq 0) {
    Write-Host "`n[SUCCESS] Migration verified! Site is working correctly." -ForegroundColor Green
} else {
    Write-Host "`n[WARNING] Some pages failed. Review errors above." -ForegroundColor Yellow
}
