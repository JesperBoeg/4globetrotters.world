$xml = "C:\Users\agile\VSCode projects\4globetrotters-migration\backup\4globetrotters.WordPress.2026-03-28.xml"
$leanUploads = "C:\Users\agile\VSCode projects\4globetrotters-migration\backup\wordpress-lean-candidate-v2\wp-content\uploads"
$origUploads = "C:\Users\agile\VSCode projects\4globetrotters-migration\backup\wordpress\wp-content\uploads"

$text = Get-Content $xml -Raw
$pattern = '/wp-content/uploads/[^"''<>\s\?]+\.(?:jpg|jpeg|png|webp)'
$matches = [regex]::Matches($text, $pattern, [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
$paths = $matches |
    ForEach-Object { $_.Value.ToLower() } |
    Where-Object { $_ -notmatch '[\[\]<>]' } |
    Sort-Object -Unique

$check = foreach ($p in $paths) {
    $rel = $p -replace '^/wp-content/uploads/', ''
    $lean = Join-Path $leanUploads $rel
    $orig = Join-Path $origUploads $rel
    $isThumb = [System.IO.Path]::GetFileNameWithoutExtension($rel) -match '-\d+x\d+$'

    [pscustomobject]@{
        Path = $rel
        InLean = Test-Path $lean
        InOrig = Test-Path $orig
        IsThumb = $isThumb
    }
}

$total = $check.Count
$missingLean = @($check | Where-Object { -not $_.InLean })
$missingOrig = @($check | Where-Object { -not $_.InOrig })
$missingLeanThumb = @($missingLean | Where-Object { $_.IsThumb })
$missingLeanOrig = @($missingLean | Where-Object { -not $_.IsThumb })

Write-Output ("XML_MEDIA_REFERENCES=" + $total)
Write-Output ("MISSING_IN_ORIGINAL=" + $missingOrig.Count)
Write-Output ("MISSING_IN_LEAN=" + $missingLean.Count)
Write-Output ("MISSING_IN_LEAN_THUMBS=" + $missingLeanThumb.Count)
Write-Output ("MISSING_IN_LEAN_ORIGINALS=" + $missingLeanOrig.Count)
Write-Output ("LEAN_COVERAGE_PCT=" + [math]::Round((($total - $missingLean.Count) * 100.0) / [math]::Max(1, $total), 2))
Write-Output "SAMPLE_MISSING_IN_LEAN:"
$missingLean | Select-Object -First 25 Path, IsThumb | Format-Table -AutoSize | Out-String -Width 240
