param(
    [string]$SourceRoot = "C:\Users\agile\VSCode projects\4globetrotters-migration\backup\wordpress",
    [string]$DestRoot = "C:\Users\agile\VSCode projects\4globetrotters-migration\backup\wordpress-lean-candidate"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $SourceRoot)) {
    throw "Source root not found: $SourceRoot"
}

if (Test-Path $DestRoot) {
    Remove-Item -Recurse -Force $DestRoot
}

New-Item -ItemType Directory -Path $DestRoot | Out-Null

# Copy everything except uploads first (fast path for code/config/theme/plugin files)
$excludeUploads = Join-Path $SourceRoot "wp-content\uploads"
& robocopy $SourceRoot $DestRoot /E /R:2 /W:2 /XD $excludeUploads /NFL /NDL /NJH /NJS /NP | Out-Null

$srcUploads = Join-Path $SourceRoot "wp-content\uploads"
$dstUploads = Join-Path $DestRoot "wp-content\uploads"
New-Item -ItemType Directory -Path $dstUploads -Force | Out-Null

$all = Get-ChildItem $srcUploads -Recurse -File -ErrorAction SilentlyContinue
$kept = 0
$skipped = 0
$keptBytes = 0
$skippedBytes = 0

foreach ($f in $all) {
    $ext = $f.Extension.ToLowerInvariant()
    $isImage = $ext -in @('.jpg', '.jpeg', '.png', '.webp')
    $isThumbVariant = $f.BaseName -match '-\d+x\d+$'

    # Keep originals and all non-image files (pdf, json, etc.)
    if (-not ($isImage -and $isThumbVariant)) {
        $rel = $f.FullName.Substring($srcUploads.Length).TrimStart('\\')
        $dest = Join-Path $dstUploads $rel
        $parent = Split-Path $dest -Parent
        if (-not (Test-Path $parent)) {
            New-Item -ItemType Directory -Path $parent -Force | Out-Null
        }
        Copy-Item $f.FullName $dest
        $kept++
        $keptBytes += $f.Length
    }
    else {
        $skipped++
        $skippedBytes += $f.Length
    }
}

$srcBytes = (Get-ChildItem $SourceRoot -Recurse -File | Measure-Object Length -Sum).Sum
$dstBytes = (Get-ChildItem $DestRoot -Recurse -File | Measure-Object Length -Sum).Sum

Write-Output "LEAN_CANDIDATE_READY=True"
Write-Output ("SOURCE_GB=" + [math]::Round($srcBytes / 1GB, 2))
Write-Output ("CANDIDATE_GB=" + [math]::Round($dstBytes / 1GB, 2))
Write-Output ("SAVED_GB=" + [math]::Round(($srcBytes - $dstBytes) / 1GB, 2))
Write-Output ("UPLOADS_KEPT_FILES=" + $kept)
Write-Output ("UPLOADS_SKIPPED_THUMBS=" + $skipped)
Write-Output ("SKIPPED_THUMBS_GB=" + [math]::Round($skippedBytes / 1GB, 2))
