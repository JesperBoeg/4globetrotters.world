# Fix encoding mojibake in all subpages
# All special chars referenced by Unicode code point to avoid file encoding issues
param()

$siteRoot = "C:\Users\agile\VSCode projects\4globetrotters\option-b-static\site"

# Build the exact search strings using char codes
$euro    = [char]0x20AC  # EUR sign  (Windows-1252 byte 0x80)
$oe      = [char]0x0153  # oe ligature (Windows-1252 byte 0x9C) - left double quote suffix
$u009D   = [char]0x009D  # C1 control (Windows-1252 byte 0x9D) - right double quote suffix
$tm      = [char]0x2122  # TM sign   (Windows-1252 byte 0x99) - apostrophe suffix
$tilde   = [char]0x02DC  # small tilde (Windows-1252 byte 0x98) - left single quote suffix
$lCurly  = [char]0x201C  # left curly " (Windows-1252 byte 0x93) - en dash suffix
$brokBar = [char]0x00A6  # broken bar (Windows-1252 byte 0xA6) - ellipsis suffix
$aGrave  = [char]0x00E2  # a with circumflex (a)

# === Entity-form patterns (use &#226; for the a with circumflex) ===
$entBase = "&#226;" + $euro  # shared prefix for entity-form

$entLDQ  = $entBase + $oe      # &#226;EURoe  = left double quote
$entRDQ  = $entBase + $u009D   # &#226;EUR+009D = right double quote
$entRSQ  = $entBase + $tm      # &#226;EUR(TM) = apostrophe
$entLSQ  = $entBase + $tilde   # &#226;EUR~ = left single quote
$entND   = $entBase + $lCurly  # &#226;EUR" = en dash
$entHel  = $entBase + $brokBar # &#226;EUR| = ellipsis
$entFB   = $entBase            # &#226;EUR (fallback - char was dropped)

# === Literal-form patterns (a with circumflex is U+00E2) ===
$litBase = $aGrave + $euro  # a-circumflex + EUR

$litLDQ  = $litBase + $oe      # aEURoe  = left double quote
$litRDQ  = $litBase + $u009D   # aEUR+009D = right double quote
$litRSQ  = $litBase + $tm      # aEUR(TM) = apostrophe
$litLSQ  = $litBase + $tilde   # aEUR~ = left single quote
$litND   = $litBase + $lCurly  # aEUR" = en dash
$litHel  = $litBase + $brokBar # aEUR| = ellipsis

$fixed = 0; $unchanged = 0

$files = Get-ChildItem $siteRoot -Recurse -Filter "index.html" | Where-Object {
    $_.FullName -notmatch '\\assets\\' -and $_.FullName -notmatch '\\wp-content\\'
}

foreach ($file in $files) {
    $c = [System.IO.File]::ReadAllText($file.FullName, [System.Text.Encoding]::UTF8)
    $u = $c

    # Entity form (order matters: specific before fallback)
    $u = $u.Replace($entLDQ, "&ldquo;")
    $u = $u.Replace($entRDQ, "&rdquo;")
    $u = $u.Replace($entRSQ, "&rsquo;")
    $u = $u.Replace($entLSQ, "&lsquo;")
    $u = $u.Replace($entND,  "&ndash;")
    $u = $u.Replace($entHel, "&hellip;")
    $u = $u.Replace($entFB,  "&rdquo;")  # fallback: bare &#226;EUR = closing quote

    # Literal form
    $u = $u.Replace($litLDQ, "&ldquo;")
    $u = $u.Replace($litRDQ, "&rdquo;")
    $u = $u.Replace($litRSQ, "&rsquo;")
    $u = $u.Replace($litLSQ, "&lsquo;")
    $u = $u.Replace($litND,  "&ndash;")
    $u = $u.Replace($litHel, "&hellip;")

    if ($u -ne $c) {
        [System.IO.File]::WriteAllText($file.FullName, $u, (New-Object System.Text.UTF8Encoding $false))
        $fixed++
        Write-Host "  FIXED: $($file.Directory.Name)" -ForegroundColor Green
    } else {
        $unchanged++
    }
}

Write-Host ""
Write-Host "Encoding fix complete: $fixed files updated, $unchanged unchanged" -ForegroundColor Cyan
