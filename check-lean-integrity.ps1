Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$siteRoot = Join-Path $repoRoot 'option-b-static\site'
$uploadsRoot = Join-Path $siteRoot 'wp-content\uploads'

if (-not (Test-Path $siteRoot)) {
    throw "Site root not found: $siteRoot"
}

if (-not (Test-Path $uploadsRoot)) {
    throw "Uploads root not found: $uploadsRoot"
}

$pattern = '/wp-content/uploads/[^"''<>\s\?]+\.(?:jpg|jpeg|png|webp|gif|avif)'
$scanFiles = Get-ChildItem -Path $siteRoot -Recurse -File -Include *.html,*.xml,*.css,*.js

$paths = foreach ($file in $scanFiles) {
    try {
        $text = Get-Content $file.FullName -Raw
    }
    catch {
        continue
    }

    if ([string]::IsNullOrEmpty($text)) {
        continue
    }

    [regex]::Matches($text, $pattern, [System.Text.RegularExpressions.RegexOptions]::IgnoreCase) |
        ForEach-Object { $_.Value.ToLower() }
}

$paths = $paths |
    Where-Object { $_ -notmatch '[\[\]<>]' } |
    Sort-Object -Unique

$check = foreach ($p in $paths) {
    $rel = $p -replace '^/wp-content/uploads/', ''
    $lean = Join-Path $uploadsRoot $rel
    $isThumb = [System.IO.Path]::GetFileNameWithoutExtension($rel) -match '-\d+x\d+$'

    [pscustomobject]@{
        Path = $rel
        InLean = Test-Path $lean
        InOrig = $true
        IsThumb = $isThumb
    }
}

$total = $check.Count
$missingLean = @($check | Where-Object { -not $_.InLean })
$missingOrig = @($check | Where-Object { -not $_.InOrig })
$missingLeanThumb = @($missingLean | Where-Object { $_.IsThumb })
$missingLeanOrig = @($missingLean | Where-Object { -not $_.IsThumb })

Write-Output "SOURCE_MODE=site-files"
Write-Output ("XML_MEDIA_REFERENCES=" + $total)
Write-Output ("MISSING_IN_ORIGINAL=" + $missingOrig.Count)
Write-Output ("MISSING_IN_LEAN=" + $missingLean.Count)
Write-Output ("MISSING_IN_LEAN_THUMBS=" + $missingLeanThumb.Count)
Write-Output ("MISSING_IN_LEAN_ORIGINALS=" + $missingLeanOrig.Count)
Write-Output ("LEAN_COVERAGE_PCT=" + [math]::Round((($total - $missingLean.Count) * 100.0) / [math]::Max(1, $total), 2))
Write-Output "SAMPLE_MISSING_IN_LEAN:"
$missingLean | Select-Object -First 25 Path, IsThumb | Format-Table -AutoSize | Out-String -Width 240
