# 4Globetrotters Subpage Migration Script
# Transforms all subpages from old Bootstrap 3 template to new design

$siteRoot = "C:\Users\agile\VSCode projects\4globetrotters\option-b-static\site"
$skipDirs = @('assets', 'wp-content')
$migrated = 0; $skipped = 0; $errors = 0

$navHtml = @"
<nav class="site-nav" id="siteNav">
  <div class="nav-inner">
    <a href="/" class="nav-logo">4Globetrotters</a>
    <button class="nav-toggle" id="navToggle" aria-label="Menu">&#9776;</button>
    <ul class="nav-links" id="navLinks">
      <li><a href="/">Home</a></li>
      <li><a href="/about-us-2/">About Us</a></li>
      <li><a href="/blog/">Blog</a></li>
      <li><a href="/itinerary/">Travel Route</a></li>
      <li><a href="/countries-we-are-visiting/">Destinations</a></li>
    </ul>
  </div>
</nav>
"@

$footerHtml = @"
<footer class="site-footer">
  <div class="footer-inner">
    <div class="footer-col">
      <h4>4Globetrotters</h4>
      <p>A Danish family of four &mdash; Jesper, Line, Noah and Vitus &mdash; sharing our adventures traveling the world with children since 2015.</p>
      <div class="social-links" style="margin-top:16px;">
        <a href="https://www.facebook.com/linemarie.nathan" target="_blank" rel="noopener" aria-label="Facebook"><i class="fa fa-facebook"></i></a>
        <a href="https://www.linkedin.com/pub/jesper-boeg/1/401/332" target="_blank" rel="noopener" aria-label="LinkedIn"><i class="fa fa-linkedin"></i></a>
        <a href="https://twitter.com/j_boeg" target="_blank" rel="noopener" aria-label="Twitter"><i class="fa fa-twitter"></i></a>
      </div>
    </div>
    <div class="footer-col">
      <h4>Quick Links</h4>
      <ul>
        <li><a href="/about-us-2/">About Us</a></li>
        <li><a href="/blog/">Blog</a></li>
        <li><a href="/itinerary/">Travel Route</a></li>
        <li><a href="/countries-we-are-visiting/">All Countries</a></li>
        <li><a href="/privacy-policy/">Privacy Policy</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Contact</h4>
      <p>4Globetrotters<br>Michael Anchers Vej 25<br>8270 Hojbjerg, Denmark</p>
      <p style="margin-top:8px;">Phone: +45 51 54 28 20</p>
    </div>
  </div>
  <div class="footer-bottom">
    &copy; 2015-2026 4Globetrotters. All rights reserved.
  </div>
</footer>
"@

$navJs = @"
<script>
(function(){
  var t = document.getElementById('navToggle');
  var l = document.getElementById('navLinks');
  t.addEventListener('click', function(){ l.classList.toggle('open'); });
  var n = document.getElementById('siteNav');
  window.addEventListener('scroll', function(){
    n.classList.toggle('scrolled', window.scrollY > 20);
  });
})();
</script>
"@

function CleanContent($html) {
    $html = [regex]::Replace($html, '<!--\s*/?wp:\S[^>]*-->\s*', '', 'Singleline')
    $html = [regex]::Replace($html, '\[pt_view\s+id="[^"]*"\]\s*', '')
    $html = [regex]::Replace($html, '<p>\s*</p>\s*', '')
    $html = [regex]::Replace($html, '(\r?\n){3,}', [System.Environment]::NewLine + [System.Environment]::NewLine)
    return $html.Trim()
}

function TransformPostCards($html) {
    $pat = "<div class=['""]post-card['""]><(h[23])><a href=['""]([^'""]+)['""]>([^<]+)</a></\1><p class=['""]meta['""]>([^<]+)</p><p><a href=['""][^'""]+['""]><img src=['""]([^'""]+)['""] alt=['""]([^'""]*)['""]></a></p><p>([\s\S]*?)</p><p><a href=['""][^'""]+['""]>Read more</a></p></div>"
    $cards = [regex]::Matches($html, $pat, 'Singleline')
    if ($cards.Count -eq 0) { return $html }

    foreach ($c in $cards) {
        $ht  = $c.Groups[1].Value
        $url = $c.Groups[2].Value
        $ttl = $c.Groups[3].Value
        $met = $c.Groups[4].Value
        $img = $c.Groups[5].Value
        $alt = $c.Groups[6].Value
        $exc = $c.Groups[7].Value

        $nc = '<div class="post-card">' + "`n" +
              '  <a href="' + $url + '" class="post-card-img"><img src="' + $img + '" alt="' + $alt + '"></a>' + "`n" +
              '  <div class="post-card-body">' + "`n" +
              '    <p class="meta">' + $met + '</p>' + "`n" +
              '    <' + $ht + '><a href="' + $url + '">' + $ttl + '</a></' + $ht + '>' + "`n" +
              '    <p>' + $exc + '</p>' + "`n" +
              '    <a href="' + $url + '" class="read-more">Read more &rarr;</a>' + "`n" +
              '  </div>' + "`n" + '</div>'
        $html = $html.Replace($c.Value, $nc)
    }

    # Wrap consecutive cards in a grid
    $html = [regex]::Replace($html, '((?:<div class="post-card">[\s\S]*?</div>\s*</div>\s*){2,})', '<div class="post-cards">' + "`n" + '$1</div>')
    return $html
}

function GetPageType($content, $dirName) {
    if ($content -match "<p class=['""]meta['""]>By ") { return 'blog-post' }
    if ($content -match 'Posts from this destination') { return 'destination' }
    if ($dirName -eq 'blog') { return 'blog-listing' }
    if ($dirName -eq 'countries-we-are-visiting') { return 'countries' }
    if ($dirName -eq 'itinerary') { return 'itinerary' }
    if ($dirName -match '^about') { return 'about' }
    if ($dirName -eq 'privacy-policy') { return 'about' }
    if ($dirName -eq 'category') { return 'category' }
    if ($content -match "class=['""]post-card['""]") { return 'destination' }
    return 'blog-post'
}

$dirs = Get-ChildItem $siteRoot -Directory | Where-Object { $skipDirs -notcontains $_.Name }

foreach ($dir in $dirs) {
    $indexFile = Join-Path $dir.FullName "index.html"
    if (-not (Test-Path $indexFile)) {
        Write-Host "  SKIP: $($dir.Name)" -ForegroundColor DarkGray
        $skipped++
        continue
    }

    try {
        $rawHtml = [System.IO.File]::ReadAllText($indexFile, [System.Text.Encoding]::UTF8)

        # Extract title
        $tm = [regex]::Match($rawHtml, '<title>([^<]+)</title>')
        if ($tm.Success) {
            $pageTitle = ($tm.Groups[1].Value -replace '\s*\|\s*4Globetrotters\s*$', '').Trim()
        } else {
            $pageTitle = (Get-Culture).TextInfo.ToTitleCase(($dir.Name -replace '-', ' '))
        }

        # Extract content
        $cm = [regex]::Match($rawHtml, '<div class="container-card editable">\s*([\s\S]*?)\s*</div>\s*</div>\s*<div class="col-md-4', 'Singleline')
        if (-not $cm.Success) {
            Write-Host "  WARN: $($dir.Name)" -ForegroundColor Yellow
            $skipped++
            continue
        }

        $content = $cm.Groups[1].Value
        $pageType = GetPageType $content $dir.Name

        # Blog post meta
        $authorDate = ''
        if ($pageType -eq 'blog-post') {
            $mm = [regex]::Match($content, "<p class=['""]meta['""]>By\s+(.*?)\s+on\s+(.*?)</p>")
            if ($mm.Success) { $authorDate = $mm.Groups[2].Value }
        }

        $content = CleanContent $content
        $content = TransformPostCards $content
        $content = $content -replace "<ul class=['""]dest-list['""]>", '<ul class="dest-list-grid">'

        # Hero image for blog posts
        $heroImg = ''
        if ($pageType -eq 'blog-post') {
            $im = [regex]::Match($content, "<img src=['""]([^'""]+)['""]")
            if ($im.Success) { $heroImg = $im.Groups[1].Value }
        }

        # Breadcrumb
        $bc = '<a href="/">Home</a>'
        if ($pageType -eq 'blog-post') { $bc += ' &rsaquo; <a href="/blog/">Blog</a>' }
        elseif ($pageType -eq 'destination') { $bc += ' &rsaquo; <a href="/countries-we-are-visiting/">Destinations</a>' }
        $bc += ' &rsaquo; ' + $pageTitle

        # Hero section
        $hs = ''
        if ($heroImg -and $pageType -eq 'blog-post') {
            $hs = " style=""background:linear-gradient(rgba(0,0,0,.45),rgba(0,0,0,.65)),url('" + $heroImg + "') center/cover no-repeat"""
        }
        $ml = ''
        if ($authorDate) { $ml = "`n    <p class=""page-meta"">$authorDate</p>" }
        $heroHtml = '<div class="page-hero"' + $hs + ">`n    <h1>" + $pageTitle + '</h1>' + $ml + "`n</div>"

        # Strip h1/meta from content (now in hero)
        if ($pageType -eq 'blog-post') {
            $content = $content -replace '^\s*<article>\s*', ''
            $content = $content -replace '\s*</article>\s*$', ''
            $content = [regex]::Replace($content, '^\s*<h1>[^<]*</h1>\s*', '')
            $content = [regex]::Replace($content, '^\s*<p class=[''"]meta[''"]>[^<]*</p>\s*', '')
        } elseif ($pageType -ne 'blog-listing') {
            $content = $content -replace '^\s*<article>\s*', ''
            $content = $content -replace '\s*</article>\s*$', ''
            $content = [regex]::Replace($content, '^\s*<h1>[^<]*</h1>\s*', '')
        } else {
            $content = [regex]::Replace($content, '^\s*<h1>[^<]*</h1>\s*', '')
        }

        # Build page
        $sb = New-Object System.Text.StringBuilder 8000
        [void]$sb.AppendLine('<!doctype html>')
        [void]$sb.AppendLine('<html lang="en">')
        [void]$sb.AppendLine('<head>')
        [void]$sb.AppendLine('  <meta charset="utf-8">')
        [void]$sb.AppendLine('  <meta name="viewport" content="width=device-width, initial-scale=1.0">')
        [void]$sb.AppendLine("  <title>$pageTitle | 4Globetrotters</title>")
        [void]$sb.AppendLine('  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;500;600&display=swap">')
        [void]$sb.AppendLine('  <link rel="stylesheet" href="/assets/wp-simple/css/font-awesome.min.css">')
        [void]$sb.AppendLine('  <link rel="stylesheet" href="/assets/subpage.css">')
        [void]$sb.AppendLine('</head>')
        [void]$sb.AppendLine('<body>')
        [void]$sb.AppendLine('')
        [void]$sb.AppendLine($navHtml)
        [void]$sb.AppendLine('')
        [void]$sb.AppendLine($heroHtml)
        [void]$sb.AppendLine('')
        [void]$sb.AppendLine('<div class="breadcrumb-bar">')
        [void]$sb.AppendLine("  <div class=""breadcrumb-inner"">$bc</div>")
        [void]$sb.AppendLine('</div>')
        [void]$sb.AppendLine('')
        [void]$sb.AppendLine('<main class="page-content">')
        [void]$sb.AppendLine($content)
        [void]$sb.AppendLine('</main>')
        [void]$sb.AppendLine('')
        [void]$sb.AppendLine($footerHtml)
        [void]$sb.AppendLine('')
        [void]$sb.AppendLine($navJs)
        [void]$sb.AppendLine('</body>')
        [void]$sb.Append('</html>')

        $newHtml = $sb.ToString()
        [System.IO.File]::WriteAllText($indexFile, $newHtml, (New-Object System.Text.UTF8Encoding $false))
        $migrated++
        Write-Host "  OK [$pageType]: $($dir.Name)" -ForegroundColor Green
    } catch {
        Write-Host "  ERROR: $($dir.Name) - $_" -ForegroundColor Red
        $errors++
    }
}

Write-Host ""
Write-Host "-- Migration Complete --" -ForegroundColor Cyan
Write-Host "  Migrated: $migrated" -ForegroundColor Green
Write-Host "  Skipped:  $skipped" -ForegroundColor Yellow
Write-Host "  Errors:   $errors" -ForegroundColor Red
