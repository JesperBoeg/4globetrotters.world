$root = "C:\Users\agile\VSCode projects\4globetrotters\option-b-static\site"
$files = Get-ChildItem $root -Recurse -Include *.html -File
$changed = 0

# Build mojibake fragments from code points (ASCII-safe script file)
$aCirc = [char]0x00E2
$euro = [char]0x20AC
$tm = [char]0x2122
$oe = [char]0x0153
$rCtrl = [char]0x009D
$emDash = [char]0x2014
$enDash = [char]0x2013
$zwsp = [char]0x200B

$entBase = "&#226;" + $euro
$entRsq = $entBase + $tm
$entLdq = $entBase + $oe
$entRdq = $entBase + $rCtrl
$entMd = $entBase + $emDash
$entNd = $entBase + $enDash

$litBase = "$aCirc$euro"
$litRsq = $litBase + $tm
$litLdq = $litBase + $oe
$litRdq = $litBase + $rCtrl
$litMd = $litBase + $emDash

$pairs = [ordered]@{
  "Phillippines" = "Philippines"
  "Phillipines" = "Philippines"
  "Planing" = "Planning"
  "our boys a very much into cars" = "our boys are very much into cars"
  "could fit out travel route" = "could fit our travel route"
  "we has not planned" = "we had not planned"
  "2 month from October to December" = "2 months from October to December"
  "a real wild west ton, go to the rodeo" = "a real wild west town, go to the rodeo"
  "Excluciva" = "Exclusiva"
  "bids arrived" = "birds arrived"
  "medicin" = "medicine"
  "adrenalin" = "adrenaline"
  "Anthelope Canyon" = "Antelope Canyon"
  "Banos de Aqua Santa" = "Banos de Agua Santa"
  "Banos de agua santa" = "Banos de Agua Santa"
  "Praire" = "Prairie"
  "wont" = "won't"
  "Medicin (Ciprofloxasin" = "Medicine (Ciprofloxacin"
  "did disappoint a bit" = "was a bit disappointing"
}

foreach ($file in $files) {
  $c = Get-Content $file.FullName -Raw -Encoding UTF8
  if ($null -eq $c) { continue }

  $u = $c
  foreach ($kv in $pairs.GetEnumerator()) {
    $u = $u.Replace($kv.Key, $kv.Value)
  }

  $u = $u.Replace($entRsq, "&rsquo;")
  $u = $u.Replace($entLdq, "&ldquo;")
  $u = $u.Replace($entRdq, "&rdquo;")
  $u = $u.Replace($entMd, "&mdash;")
  $u = $u.Replace($entNd, "&ndash;")

  $u = $u.Replace($litRsq, "&rsquo;")
  $u = $u.Replace($litLdq, "&ldquo;")
  $u = $u.Replace($litRdq, "&rdquo;")
  $u = $u.Replace($litMd, "&mdash;")
  $u = $u.Replace([string]$zwsp, "")

  # Fix Danish word with broken charset by pattern
  $u = [regex]::Replace($u, 'blindtarmsbet.{1,3}ndelse', 'blindtarmsbet&aelig;ndelse')

  # Normalize frequent stretched misspellings seen in body text and excerpts
  $u = [regex]::Replace($u, '\badrenalinee+\b', 'adrenaline')
  $u = [regex]::Replace($u, '\bmedicinee+\b', 'medicine')

  # Visible text correction for Sapphire without changing URL slugs
  $u = [regex]::Replace($u, '(<title>)Saphire coast', '$1Sapphire Coast')
  $u = [regex]::Replace($u, '(>\s*)Saphire coast', '$1Sapphire Coast')
  $u = [regex]::Replace($u, '(alt=")Saphire coast', '$1Sapphire Coast')
  $u = [regex]::Replace($u, "(alt=')Saphire coast", '$1Sapphire Coast')

  if ($u -ne $c) {
    [System.IO.File]::WriteAllText($file.FullName, $u, (New-Object System.Text.UTF8Encoding($false)))
    $changed++
  }
}

Write-Output "Updated files: $changed"