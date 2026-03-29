$ErrorActionPreference = 'Stop'

$root = 'C:\Users\agile\VSCode projects\4globetrotters-migration\option-b-static\site'
$baseLive = 'https://www.4globetrotters.world'
$baseLocal = 'http://localhost:4173'
$maxPages = 80

function Get-Metrics {
    param([string]$Html)

    if ([string]::IsNullOrWhiteSpace($Html)) {
        return [pscustomobject]@{ Title = ''; H1 = ''; Words = 0 }
    }

    $title = ''
    if ($Html -match '<title>(.*?)</title>') { $title = $matches[1] }

    $h1 = ''
    if ($Html -match '<h1[^>]*>(.*?)</h1>') { $h1 = $matches[1] }

    $text = [regex]::Replace($Html, '<script[\s\S]*?</script>', ' ', 'IgnoreCase')
    $text = [regex]::Replace($text, '<style[\s\S]*?</style>', ' ', 'IgnoreCase')
    $text = [regex]::Replace($text, '<[^>]+>', ' ')
    $text = [regex]::Replace($text, '\s+', ' ')
    $words = ($text.Trim() -split '\s+' | Where-Object { $_ -ne '' }).Count

    return [pscustomobject]@{ Title = $title; H1 = $h1; Words = $words }
}

$pages = Get-ChildItem -Path $root -Filter 'index.html' -Recurse |
    Where-Object {
        $_.FullName -notmatch '\\wp-content\\' -and
        $_.FullName -notmatch '\\wp-admin\\' -and
        $_.FullName -notmatch '\\wp-includes\\'
    } |
    ForEach-Object {
        $rel = $_.FullName.Substring($root.Length).TrimStart('\\') -replace '\\', '/'
        if ($rel -eq 'index.html') { '/' }
        else { '/' + ($rel -replace '/index.html$', '/') }
    } |
    Sort-Object -Unique |
    Select-Object -First $maxPages

$results = @()
foreach ($path in $pages) {
    $liveUrl = "$baseLive$path"
    $localUrl = "$baseLocal$path"

    $liveResp = $null
    $localResp = $null

    try { $liveResp = Invoke-WebRequest -Uri $liveUrl -UseBasicParsing -TimeoutSec 20 } catch {}
    try { $localResp = Invoke-WebRequest -Uri $localUrl -UseBasicParsing -TimeoutSec 20 } catch {}

    $liveMetrics = Get-Metrics -Html $(if ($liveResp) { $liveResp.Content } else { '' })
    $localMetrics = Get-Metrics -Html $(if ($localResp) { $localResp.Content } else { '' })

    $deltaWords = [math]::Abs([int]$liveMetrics.Words - [int]$localMetrics.Words)
    $score = $deltaWords
    if ($liveMetrics.H1 -ne $localMetrics.H1) { $score += 200 }
    if ($liveMetrics.Title -ne $localMetrics.Title) { $score += 100 }

    $results += [pscustomobject]@{
        Path = $path
        LiveCode = $(if ($liveResp) { $liveResp.StatusCode } else { 'ERR' })
        LocalCode = $(if ($localResp) { $localResp.StatusCode } else { 'ERR' })
        LiveTitle = $liveMetrics.Title
        LocalTitle = $localMetrics.Title
        LiveH1 = $liveMetrics.H1
        LocalH1 = $localMetrics.H1
        LiveWords = $liveMetrics.Words
        LocalWords = $localMetrics.Words
        DeltaWords = $deltaWords
        Score = $score
    }
}

$top = $results | Sort-Object Score -Descending | Select-Object -First 25
$report = 'C:\Users\agile\VSCode projects\4globetrotters-migration\option-b-static\comparison-top25.csv'
$top | Export-Csv -NoTypeInformation -Encoding UTF8 -Path $report

$top | Format-Table -AutoSize | Out-String -Width 300
"REPORT=$report"
"SCANNED=$($results.Count)"
