param(
    [string]$XmlPath = "C:\Users\agile\VSCode projects\4globetrotters-migration\backup\4globetrotters.WordPress.2026-03-28.xml",
    [string]$ThemePath = "C:\Users\agile\VSCode projects\4globetrotters-migration\backup\wordpress\wp-content\themes\wp-simple",
    [string]$UploadsPath = "C:\Users\agile\VSCode projects\4globetrotters-migration\backup\wordpress-lean-candidate-v2\wp-content\uploads",
    [string]$OutDir = "C:\Users\agile\VSCode projects\4globetrotters-migration\option-b-static\site",
    [switch]$CopyUploads = $true
)

$ErrorActionPreference = "Stop"

function Ensure-Dir([string]$Path) {
    if (-not (Test-Path $Path)) {
        New-Item -ItemType Directory -Path $Path -Force | Out-Null
    }
}

function HtmlEncode([string]$Value) {
    if ([string]::IsNullOrEmpty($Value)) { return "" }
    return [System.Net.WebUtility]::HtmlEncode($Value)
}

function Get-YouTubeEmbedUrl([string]$Url) {
  if ([string]::IsNullOrWhiteSpace($Url)) { return $null }

  $decoded = [System.Net.WebUtility]::HtmlDecode($Url).Trim()
  try {
    $uri = [System.Uri]$decoded
  }
  catch {
    return $null
  }

  $ytHost = $uri.Host.ToLowerInvariant()
  $videoId = $null

  if ($ytHost -like '*youtu.be') {
    $videoId = $uri.AbsolutePath.Trim('/')
  }
  elseif ($ytHost -like '*youtube.com') {
    if ($uri.AbsolutePath -match '^/watch$') {
      $m = [regex]::Match($uri.Query, '(?:\?|&)v=([^&]+)', 'IgnoreCase')
      if ($m.Success) { $videoId = $m.Groups[1].Value }
    }
    elseif ($uri.AbsolutePath -match '^/embed/([^/?#]+)') {
      $videoId = $matches[1]
    }
    elseif ($uri.AbsolutePath -match '^/shorts/([^/?#]+)') {
      $videoId = $matches[1]
    }
  }

  if ([string]::IsNullOrWhiteSpace($videoId)) { return $null }
  $videoId = ($videoId -replace '[^A-Za-z0-9_-]', '')
  if ([string]::IsNullOrWhiteSpace($videoId)) { return $null }
  return "https://www.youtube.com/embed/$videoId"
}

  function Clean-Text([string]$Value) {
    if ([string]::IsNullOrEmpty($Value)) { return "" }
    $clean = $Value
    $clean = $clean.Replace([string][char]0x00A0, ' ')
    $clean = $clean.Replace([string][char]0x00C2, '')
    return $clean.Trim()
  }

function Rewrite-Content([string]$Html) {
    if ([string]::IsNullOrEmpty($Html)) { return "" }

    $rewritten = $Html
    $rewritten = [regex]::Replace($rewritten, 'https?://(www\.)?4globetrotters\.world', '', 'IgnoreCase')
    $rewritten = [regex]::Replace($rewritten, 'src="//', 'src="https://', 'IgnoreCase')
    $rewritten = [regex]::Replace($rewritten, 'href="//', 'href="https://', 'IgnoreCase')
  $rewritten = $rewritten.Replace([string][char]0x00C2, '')

  # Replace linked WordPress thumbnails with full-size inline images.
  $rewritten = [regex]::Replace(
    $rewritten,
    '<a\s+href="(?<href>[^"]+\.(?:jpg|jpeg|png|gif|webp))"[^>]*>\s*<img[^>]*src="(?<src>[^"]+)"(?<attrs>[^>]*)\/?>\s*<\/a>',
    {
      param($match)
      $full = $match.Groups['href'].Value
      $attrs = $match.Groups['attrs'].Value
      $alt = ''
      if ($attrs -match 'alt="([^"]*)"') {
        $alt = $matches[1]
      }
      return "<p class='content-image'><a href='$full'><img src='$full' alt='$alt'></a></p>"
    },
    'IgnoreCase'
  )

  # Normalize standalone image tags that still reference WP-generated thumbnail sizes.
  $rewritten = [regex]::Replace(
    $rewritten,
    '<img(?<before>[^>]*?)src="(?<src>[^"]+)"(?<after>[^>]*)\/?>',
    {
      param($match)
      $src = $match.Groups['src'].Value
      $fullSrc = [regex]::Replace($src, '-\d+x\d+(?=\.(jpg|jpeg|png|gif|webp)$)', '', 'IgnoreCase')
      $attrs = ($match.Groups['before'].Value + ' ' + $match.Groups['after'].Value)
      $alt = ''
      if ($attrs -match 'alt="([^"]*)"') {
        $alt = $matches[1]
      }
      return "<img src='$fullSrc' alt='$alt'>"
    },
    'IgnoreCase'
  )

  $rewritten = [regex]::Replace($rewritten, '<p>(\s*<p class=''content-image''>.+?<\/p>\s*)+<\/p>', '$1', 'Singleline,IgnoreCase')

  # Convert YouTube links into responsive embedded players.
  $rewritten = [regex]::Replace(
    $rewritten,
    '<p>\s*(?<url>https?://(?:www\.)?(?:youtube\.com|youtu\.be)[^\s<]+)\s*<\/p>',
    {
      param($match)
      $embed = Get-YouTubeEmbedUrl $match.Groups['url'].Value
      if (-not $embed) { return $match.Value }
      return "<div class='video-embed'><iframe src='$embed' loading='lazy' allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share' allowfullscreen></iframe></div>"
    },
    'IgnoreCase'
  )

  $rewritten = [regex]::Replace(
    $rewritten,
    '(?im)^\s*(?<url>https?://(?:www\.)?(?:youtube\.com|youtu\.be)[^\s<]+)\s*$',
    {
      param($match)
      $embed = Get-YouTubeEmbedUrl $match.Groups['url'].Value
      if (-not $embed) { return $match.Value }
      return "<div class='video-embed'><iframe src='$embed' loading='lazy' allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share' allowfullscreen></iframe></div>"
    },
    'IgnoreCase,Multiline'
  )

  $rewritten = [regex]::Replace(
    $rewritten,
    '<a[^>]+href="(?<url>https?://(?:www\.)?(?:youtube\.com|youtu\.be)[^"]+)"[^>]*>[^<]*<\/a>',
    {
      param($match)
      $embed = Get-YouTubeEmbedUrl $match.Groups['url'].Value
      if (-not $embed) { return $match.Value }
      return "<div class='video-embed'><iframe src='$embed' loading='lazy' allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share' allowfullscreen></iframe></div>"
    },
    'IgnoreCase'
  )

    return $rewritten
}

  function Strip-Html([string]$Html) {
    if ([string]::IsNullOrWhiteSpace($Html)) { return '' }
    $text = [regex]::Replace($Html, '<script[\s\S]*?</script>', ' ', 'IgnoreCase')
    $text = [regex]::Replace($text, '<style[\s\S]*?</style>', ' ', 'IgnoreCase')
    $text = [regex]::Replace($text, '<[^>]+>', ' ')
    $text = [System.Net.WebUtility]::HtmlDecode($text)
    $text = [regex]::Replace($text, '\s+', ' ')
    return (Clean-Text $text)
  }

  function Build-Excerpt([string]$Html, [int]$MaxWords = 38) {
    $plain = Strip-Html $Html
    if ([string]::IsNullOrWhiteSpace($plain)) { return '' }
    $words = $plain -split '\s+'
    if ($words.Count -le $MaxWords) { return $plain }
    return (($words | Select-Object -First $MaxWords) -join ' ') + ' ...'
  }

function Normalize-Label([string]$Value) {
  if ([string]::IsNullOrWhiteSpace($Value)) { return '' }
  $v = $Value.ToLowerInvariant()
  $v = [regex]::Replace($v, '\s*\([^\)]*\)', '')
  $v = [regex]::Replace($v, '[^a-z0-9]+', ' ')
  return $v.Trim()
}

function Get-Tokens([string]$Value) {
  $n = Normalize-Label $Value
  if ([string]::IsNullOrWhiteSpace($n)) { return @() }
  return ($n -split '\s+' | Where-Object { $_.Length -ge 3 })
}

function Build-ItineraryHtml() {
    return @"
<article>
  <h1>Travel route (2015/16)</h1>
  <p><em>Our travel route for our round-the-world trip looked like this. Click on the links below to get to the page of the countries we visited</em></p>
  <p><strong>Our travel route</strong></p>
  <p>Denmark</p>
  <p><a href="/cyprus/">Cyprus - two weeks, roadtrip &amp; airbnb (October 15. - October 29. 2015)</a></p>
  <p><a href="/thailand/">Thailand - 4 weeks, Kanchanaburi, Chiang Mai and Koh Lanta (October 29. - November 26. 2015)</a></p>
  <p><a href="/vietnam/">Vietnam - two weeks, Ho Chi Minh city and south Vietnam (November 26. - December 10. 2015)</a></p>
  <p><a href="/philippines/">Philippines - 3,5 weeks - including Christmas and new year's eve: Palawan, Mindoro (December 11. - January 4. 2016)</a></p>
  <p><a href="/australia/">Australia - 5 weeks, campervan from Adelaide to Sydney (January 5. - February 7. 2016)</a></p>
  <p><a href="/hawaii/">Hawaii - Oahu 3 days, Maui 7 days (February 8. - February 18. 2016)</a></p>
  <p><a href="/california-usa/">Los Angeles - one week (L.A., Universal Pictures, Hollywood etc.) (February 19. - February 25. 2016)</a></p>
  <p><a href="/mexico-yucatan/">Mexico - 4 weeks, Yucatan Peninsula (February 25. - March 24. 2016)</a></p>
  <p><a href="/cuba/">Cuba - two weeks (March 24. - April 7. 2016)</a></p>
  <p><a href="/deep-south/">U.S.A (Deep South + Texas) - 3,5 weeks (April 7. - May 1. 2016)</a></p>
</article>
"@
}

  function Build-MenuHtml([array]$MenuItems) {
    $parts = @()
    foreach ($item in $MenuItems) {
      $title = HtmlEncode $item.Title
      $url = if ([string]::IsNullOrWhiteSpace($item.Url)) { '/' } else { $item.Url }

      if ($item.Children -and $item.Children.Count -gt 0) {
        $childHtml = ($item.Children | ForEach-Object {
          $ctitle = HtmlEncode $_.Title
          $curl = if ([string]::IsNullOrWhiteSpace($_.Url)) { '/' } else { $_.Url }
          "<li><a href='$curl'>$ctitle</a></li>"
        }) -join "`n"

        $parts += @"
<li class="dropdown">
  <a href="$url" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="false">$title <span class="caret"></span></a>
  <ul class="dropdown-menu" role="menu">
    $childHtml
  </ul>
</li>
"@
      }
      else {
        $parts += "<li><a href='$url'>$title</a></li>"
      }
    }

    return ($parts -join "`n")
  }

function Write-Page([string]$OutPath, [string]$Title, [string]$BodyHtml, [array]$RecentPosts, [array]$TopPages, [string]$MenuHtml, [switch]$SiteTitleOnly) {
    $recentHtml = ($RecentPosts | ForEach-Object {
        "<li><a href='/{0}/'>{1}</a></li>" -f $_.Slug, (HtmlEncode $_.Title)
    }) -join "`n"

    $pagesHtml = ($TopPages | ForEach-Object {
        "<li><a href='/{0}/'>{1}</a></li>" -f $_.Slug, (HtmlEncode $_.Title)
    }) -join "`n"

    $year = (Get-Date).Year

    $fullTitle = if ($SiteTitleOnly) { '4Globetrotters' } else { "$(HtmlEncode $Title) | 4Globetrotters" }

    $template = @"
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>$fullTitle</title>
  <link rel="stylesheet" href="/assets/wp-simple/css/bootstrap.min.css">
  <link rel="stylesheet" href="/assets/wp-simple/css/font-awesome.min.css">
  <link rel="stylesheet" href="/assets/wp-simple/style.css">
  <style>
    body { background:#f4f4f4; }
    .container-card { background:#fff; padding:30px; box-shadow:0 1px 8px rgba(0,0,0,.08); }
    .text_logo { margin:0; }
    .text_logo a { color:#222; text-decoration:none; }
    #menu_row .navbar-nav > li > a { font-weight:600; }
    .sidebar-box { margin-bottom:22px; padding:16px; background:#fff; border:1px solid #e9e9e9; }
    .sidebar-box h4 { margin-top:0; margin-bottom:10px; }
    .sidebar-box ul { margin:0; padding-left:18px; }
    .dest-list { columns: 2; column-gap: 24px; }
    .dest-list li { break-inside: avoid; margin: 0 0 8px 0; }
    .meta { font-size:13px; color:#666; margin-bottom:14px; }
    .post-card { margin-bottom:28px; border-bottom:1px solid #eee; padding-bottom:22px; }
    .post-card img { width:100%; height:auto; margin:0 0 10px 0; }
    .editable article img { display:block; max-width:100%; height:auto; margin:0 0 16px 0; }
    .editable article .content-image { margin:0 0 18px 0; }
    .editable article .content-image a { display:block; }
    .editable article .video-embed { position:relative; width:100%; height:0; padding-bottom:56.25%; margin:0 0 18px 0; }
    .editable article .video-embed iframe { position:absolute; top:0; left:0; width:100%; height:100%; border:0; }
    #footer_row { margin-top:45px; padding:20px 0; background:#f2f2f2; border-top:1px solid #ddd; }
  </style>
</head>
<body>
<header>
  <div class="container">
    <h1 class="text_logo"><a href="https://4globetrotters.world/">4Globetrotters</a></h1>
  </div>
  <nav id="menu_row" class="navbar navbar-default" role="navigation">
    <div class="container">
      <div class="navbar-header">
        <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-ex1-collapse">
          <span class="icon-bar"></span>
          <span class="icon-bar"></span>
          <span class="icon-bar"></span>
        </button>
      </div>
      <div class="collapse navbar-collapse navbar-ex1-collapse">
        <ul class="nav navbar-nav">
          $MenuHtml
        </ul>
      </div>
    </div>
  </nav>
</header>

<div id="blog_content_row">
  <div class="container">
    <div class="row">
      <div class="col-md-8">
        <div class="container-card editable">
          $BodyHtml
        </div>
      </div>
      <div class="col-md-4 sidebar sidebar_editable">
        <div class="sidebar-box">
          <h4>Connect With Us</h4>
          <p>
            <a href="https://www.facebook.com/linemarie.nathan" target="_blank">Facebook</a><br>
            <a href="https://www.linkedin.com/pub/jesper-boeg/1/401/332" target="_blank">LinkedIn</a><br>
            <a href="https://twitter.com/j_boeg" target="_blank">Twitter</a>
          </p>
        </div>
        <div class="sidebar-box">
          <h4>Recent Posts</h4>
          <ul>
            $recentHtml
          </ul>
        </div>
        <div class="sidebar-box">
          <h4>Contact information</h4>
          <p>4globetrotters, Michael Anchers Vej 25. 8270 Hojbjerg. Phone: +45 51 54 28 20</p>
        </div>
        <div class="sidebar-box">
          <h4>Pages</h4>
          <ul>
            $pagesHtml
          </ul>
        </div>
      </div>
    </div>
  </div>
</div>

<div id="footer_row">
  <div class="container">
    <div class="row">
      <div class="col-md-6"><p id="copyright">&copy; 2015-$year 4Globetrotters</p></div>
      <div class="col-md-6"><p id="credit">Static Option B starter build</p></div>
    </div>
  </div>
</div>

<script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
<script src="/assets/wp-simple/js/bootstrap.min.js"></script>
</body>
</html>
"@

    $dir = Split-Path -Parent $OutPath
    Ensure-Dir $dir
    Set-Content -Path $OutPath -Value $template -Encoding UTF8
}

if (-not (Test-Path $XmlPath)) { throw "XML not found: $XmlPath" }
if (-not (Test-Path $ThemePath)) { throw "Theme not found: $ThemePath" }
if (-not (Test-Path $UploadsPath)) { throw "Uploads not found: $UploadsPath" }

if (Test-Path $OutDir) {
    Remove-Item -Recurse -Force $OutDir
}
Ensure-Dir $OutDir
Ensure-Dir (Join-Path $OutDir "assets")

# Copy theme assets for similar visual style
$themeOut = Join-Path $OutDir "assets\wp-simple"
& robocopy $ThemePath $themeOut /E /R:2 /W:2 /XD nimbus lang /NFL /NDL /NJH /NJS /NP | Out-Null

# Copy lean uploads into static output
if ($CopyUploads) {
    $uploadsOut = Join-Path $OutDir "wp-content\uploads"
    Ensure-Dir $uploadsOut
    & robocopy $UploadsPath $uploadsOut /E /R:2 /W:2 /NFL /NDL /NJH /NJS /NP | Out-Null
}

[xml]$doc = Get-Content $XmlPath
$ns = New-Object System.Xml.XmlNamespaceManager($doc.NameTable)
$ns.AddNamespace("wp", "http://wordpress.org/export/1.2/")
$ns.AddNamespace("content", "http://purl.org/rss/1.0/modules/content/")
$ns.AddNamespace("excerpt", "http://wordpress.org/export/1.2/excerpt/")
$ns.AddNamespace("dc", "http://purl.org/dc/elements/1.1/")

$items = $doc.SelectNodes('/rss/channel/item', $ns)
$dateCulture = New-Object System.Globalization.CultureInfo('en-US')

# Map attachment id -> media URL using _wp_attached_file metadata
$attachmentById = @{}
foreach ($item in $items) {
    $ptypeNode = $item.SelectSingleNode('wp:post_type', $ns)
    if (-not $ptypeNode -or $ptypeNode.InnerText -ne 'attachment') { continue }

    $idNode = $item.SelectSingleNode('wp:post_id', $ns)
    if (-not $idNode) { continue }
    $id = $idNode.InnerText

    $fileMeta = $item.SelectNodes('wp:postmeta', $ns) | Where-Object {
        $_.SelectSingleNode('wp:meta_key', $ns).InnerText -eq '_wp_attached_file'
    } | Select-Object -First 1

    if ($fileMeta) {
        $rel = $fileMeta.SelectSingleNode('wp:meta_value', $ns).InnerText.TrimStart('/')
        if ($rel) {
            $attachmentById[$id] = '/wp-content/uploads/' + $rel
        }
    }
}

$posts = @()
$pages = @()

foreach ($item in $items) {
    $ptype = $item.SelectSingleNode('wp:post_type', $ns)
    $status = $item.SelectSingleNode('wp:status', $ns)
    if (-not $ptype -or -not $status) { continue }
    if ($status.InnerText -ne 'publish') { continue }
    if ($ptype.InnerText -notin @('post','page')) { continue }

    $slug = $item.SelectSingleNode('wp:post_name', $ns).InnerText
    if ([string]::IsNullOrWhiteSpace($slug)) {
        $slug = ('post-' + $item.SelectSingleNode('wp:post_id', $ns).InnerText)
    }

    $title = Clean-Text $item.SelectSingleNode('title', $ns).InnerText
    $authorNode = $item.SelectSingleNode('dc:creator', $ns)
    $author = if ($authorNode) { Clean-Text $authorNode.InnerText } else { '4Globetrotters' }
    $dateRaw = $item.SelectSingleNode('wp:post_date', $ns).InnerText
    $date = [datetime]::Parse($dateRaw)

    $contentNode = $item.SelectSingleNode('content:encoded', $ns)
    $content = if ($contentNode) { Rewrite-Content $contentNode.InnerText } else { '' }

    $excerptNode = $item.SelectSingleNode('excerpt:encoded', $ns)
    $excerpt = if ($excerptNode) { $excerptNode.InnerText } else { '' }

    $cats = @()
    foreach ($cat in $item.SelectNodes('category', $ns)) {
        $domainAttr = $cat.Attributes['domain']
        if ($domainAttr -and $domainAttr.Value -eq 'category') {
            $nicename = $cat.Attributes['nicename'].Value
            $cats += [pscustomobject]@{ Name=(Clean-Text $cat.InnerText); Slug=$nicename }
        }
    }

    $thumbIdNode = $item.SelectNodes('wp:postmeta', $ns) | Where-Object {
        $_.SelectSingleNode('wp:meta_key', $ns).InnerText -eq '_thumbnail_id'
    } | Select-Object -First 1

    $featured = $null
    if ($thumbIdNode) {
        $thumbId = $thumbIdNode.SelectSingleNode('wp:meta_value', $ns).InnerText
        if ($attachmentById.ContainsKey($thumbId)) {
            $featured = $attachmentById[$thumbId]
        }
    }

    $obj = [pscustomobject]@{
      PostId = $item.SelectSingleNode('wp:post_id', $ns).InnerText
        Slug = $slug
        Title = $title
        Author = $author
        Date = $date
        Content = $content
        Excerpt = $excerpt
        Categories = $cats
        FeaturedImage = $featured
        Type = $ptype.InnerText
    }

    if ($ptype.InnerText -eq 'post') {
        $posts += $obj
    } else {
        $pages += $obj
    }
}

$posts = $posts | Sort-Object Date -Descending
$pages = $pages | Sort-Object Title
$recentPosts = $posts | Select-Object -First 10
$topPages = $pages

# Build category map early so pages can include related trip posts like the live site.
$allCategories = @{}
foreach ($p in $posts) {
  foreach ($c in $p.Categories) {
    if (-not $allCategories.ContainsKey($c.Slug)) {
      $allCategories[$c.Slug] = [pscustomobject]@{ Name = $c.Name; Posts = @() }
    }
    $allCategories[$c.Slug].Posts += $p
  }
}

# Build menu from original WordPress nav_menu_item hierarchy
$pageById = @{}
foreach ($pg in $pages) {
  $pageById[[string]$pg.PostId] = $pg
}

$menuItems = @()
foreach ($item in $items) {
  $ptypeNode = $item.SelectSingleNode('wp:post_type', $ns)
  $statusNode = $item.SelectSingleNode('wp:status', $ns)
  if (-not $ptypeNode -or -not $statusNode) { continue }
  if ($ptypeNode.InnerText -ne 'nav_menu_item' -or $statusNode.InnerText -ne 'publish') { continue }

  $meta = @{}
  foreach ($pm in $item.SelectNodes('wp:postmeta', $ns)) {
    $kNode = $pm.SelectSingleNode('wp:meta_key', $ns)
    $vNode = $pm.SelectSingleNode('wp:meta_value', $ns)
    if ($kNode -and $vNode) {
      $meta[$kNode.InnerText] = $vNode.InnerText
    }
  }

  $menuItems += [pscustomobject]@{
    Id = $item.SelectSingleNode('wp:post_id', $ns).InnerText
    Title = Clean-Text $item.SelectSingleNode('title', $ns).InnerText
    Order = [int]$item.SelectSingleNode('wp:menu_order', $ns).InnerText
    Parent = $meta['_menu_item_menu_item_parent']
    ObjectId = $meta['_menu_item_object_id']
    Object = $meta['_menu_item_object']
    Type = $meta['_menu_item_type']
    Url = $meta['_menu_item_url']
  }
}

function Resolve-MenuNode($menuItem, $pageById) {
  if ($menuItem.Object -eq 'page' -and $pageById.ContainsKey([string]$menuItem.ObjectId)) {
    $pg = $pageById[[string]$menuItem.ObjectId]
    $menuTitle = $pg.Title
    if ($pg.Slug -eq 'countries-we-are-visiting') {
      $menuTitle = 'Countries'
    }
    return [pscustomobject]@{ Title = $menuTitle; Url = ('/' + $pg.Slug + '/'); Page = $pg }
  }

  $title = if ([string]::IsNullOrWhiteSpace($menuItem.Title)) { 'Menu' } else { $menuItem.Title }
  $url = '/'
  if (-not [string]::IsNullOrWhiteSpace($menuItem.Url)) {
    $url = [regex]::Replace($menuItem.Url, '^https?://(www\.)?4globetrotters\.world', '', 'IgnoreCase')
    if ([string]::IsNullOrWhiteSpace($url)) { $url = '/' }
  }
  elseif ($title -match '^home$') {
    $url = '/'
  }

  return [pscustomobject]@{ Title = $title; Url = $url; Page = $null }
}

$menuByParent = @{}
foreach ($m in ($menuItems | Sort-Object Order)) {
  $key = [string]$m.Parent
  if (-not $menuByParent.ContainsKey($key)) {
    $menuByParent[$key] = New-Object System.Collections.ArrayList
  }
  [void]$menuByParent[$key].Add($m)
}

$topMenu = @()
foreach ($m in ($menuItems | Where-Object { [string]$_.Parent -eq '0' } | Sort-Object Order)) {
  $resolved = Resolve-MenuNode -menuItem $m -pageById $pageById
  $children = @()
  if ($menuByParent.ContainsKey([string]$m.Id)) {
    foreach ($cm in ($menuByParent[[string]$m.Id] | Sort-Object Order)) {
      $cres = Resolve-MenuNode -menuItem $cm -pageById $pageById
      $children += [pscustomobject]@{ Title = $cres.Title; Url = $cres.Url; Page = $cres.Page }
    }
  }

  $topMenu += [pscustomobject]@{
    Id = $m.Id
    Title = $resolved.Title
    Url = $resolved.Url
    Page = $resolved.Page
    Children = $children
  }
}

$menuHtml = Build-MenuHtml -MenuItems $topMenu

$destinationsMenu = $topMenu | Where-Object { $_.Title -match 'Destinations|Countries' } | Select-Object -First 1
$destinationPagesOrdered = @()
if ($destinationsMenu -and $destinationsMenu.Children.Count -gt 0) {
  foreach ($child in $destinationsMenu.Children) {
    if ($child.Page) {
      $destinationPagesOrdered += $child.Page
    }
  }
}

# Build post pages
foreach ($post in $posts) {
    $catsHtml = ($post.Categories | ForEach-Object { "<a href='/category/{0}/'>{1}</a>" -f $_.Slug, (HtmlEncode $_.Name) }) -join ', '
    $imgHtml = if ($post.FeaturedImage) { "<p><img src='" + $post.FeaturedImage + "' alt='" + (HtmlEncode $post.Title) + "'></p>" } else { '' }

    $postExcerpt = Build-Excerpt -Html $(if ([string]::IsNullOrWhiteSpace($post.Excerpt)) { $post.Content } else { $post.Excerpt }) -MaxWords 60

    $body = @"
<article>
  <h1>$(HtmlEncode $post.Title)</h1>
  <p class="meta">By $(HtmlEncode $post.Author) on $($post.Date.ToString('MMMM d, yyyy', $dateCulture))</p>
  $imgHtml
  $($post.Content)
  <p>$(HtmlEncode $postExcerpt)</p>
  <p class="meta">Category: $catsHtml</p>
</article>
"@

    Write-Page -OutPath (Join-Path $OutDir ($post.Slug + '\index.html')) -Title $post.Title -BodyHtml $body -RecentPosts $recentPosts -TopPages $topPages -MenuHtml $menuHtml
}

# Build page pages
foreach ($page in $pages) {
  $pageContent = $page.Content

  if ($page.Slug -eq 'itinerary') {
    $body = Build-ItineraryHtml
    Write-Page -OutPath (Join-Path $OutDir ($page.Slug + '\index.html')) -Title $page.Title -BodyHtml $body -RecentPosts $recentPosts -TopPages $topPages -MenuHtml $menuHtml
    continue
  }

  # The original "Countries we are visiting" page has no body content and relied on WP setup.
  # For static mode, generate a destination index from published pages.
  if ($page.Slug -eq 'countries-we-are-visiting' -and [string]::IsNullOrWhiteSpace($pageContent)) {
    $exclude = @('about-us', 'about-us-2', 'blog', 'countries-we-are-visiting', 'privacy-policy', 'itinerary')
    $destPages = if ($destinationPagesOrdered.Count -gt 0) {
      $destinationPagesOrdered
    } else {
      $pages | Where-Object { $_.Slug -notin $exclude } | Sort-Object Title
    }

    $destLinks = ($destPages | ForEach-Object {
      "<li><a href='/{0}/'>{1}</a></li>" -f $_.Slug, (HtmlEncode $_.Title)
    }) -join "`n"

    $pageContent = @"
<p>Pick a destination to see trip pages and stories.</p>
<ul>
$destLinks
</ul>
"@
  }

  $relatedCards = ''
  $pageNorm = Normalize-Label $page.Title
  if (-not [string]::IsNullOrWhiteSpace($pageNorm)) {
    $matches = @()
    $pageTokens = Get-Tokens $page.Title
    foreach ($catEntry in $allCategories.GetEnumerator()) {
      $catNorm = Normalize-Label $catEntry.Value.Name
      if ([string]::IsNullOrWhiteSpace($catNorm)) { continue }
      if ($catNorm -eq $pageNorm -or $catNorm.StartsWith($pageNorm) -or $pageNorm.StartsWith($catNorm)) {
        $matches += $catEntry.Value
      }
    }

    # Fallback for naming differences like "Deep South" vs "Southern USA".
    if ($matches.Count -eq 0 -and $pageTokens.Count -gt 0) {
      $best = $null
      $bestScore = 0
      foreach ($catEntry in $allCategories.GetEnumerator()) {
        $catTokens = Get-Tokens $catEntry.Value.Name
        if ($catTokens.Count -eq 0) { continue }
        $overlap = ($pageTokens | Where-Object { $catTokens -contains $_ }).Count
        if ($overlap -gt $bestScore) {
          $bestScore = $overlap
          $best = $catEntry.Value
        }
      }
      if ($best -and $bestScore -ge 1) {
        $matches += $best
      }
    }

    if ($matches.Count -gt 0) {
      $relPosts = $matches | ForEach-Object { $_.Posts } | Sort-Object Date -Descending -Unique
      if ($relPosts.Count -gt 0) {
        $cards = ($relPosts | ForEach-Object {
          $img = if ($_.FeaturedImage) { "<p><a href='/{0}/'><img src='{1}' alt='{2}'></a></p>" -f $_.Slug, $_.FeaturedImage, (HtmlEncode $_.Title) } else { '' }
          $excerpt = Build-Excerpt -Html $(if ([string]::IsNullOrWhiteSpace($_.Excerpt)) { $_.Content } else { $_.Excerpt })
          "<div class='post-card'><h3><a href='/{0}/'>{1}</a></h3><p class='meta'>{2}</p>{3}<p>{4}</p><p><a href='/{0}/'>Read more</a></p></div>" -f $_.Slug, (HtmlEncode $_.Title), $_.Date.ToString('MMMM d, yyyy', $dateCulture), $img, (HtmlEncode $excerpt)
        }) -join "`n"
        $relatedCards = "<h2>Posts from this destination</h2>" + $cards
      }
    }
  }

    $body = @"
<article>
  <h1>$(HtmlEncode $page.Title)</h1>
  $pageContent
  $relatedCards
</article>
"@

    Write-Page -OutPath (Join-Path $OutDir ($page.Slug + '\index.html')) -Title $page.Title -BodyHtml $body -RecentPosts $recentPosts -TopPages $topPages -MenuHtml $menuHtml
}

foreach ($slug in $allCategories.Keys) {
    $cat = $allCategories[$slug]
    $cards = ($cat.Posts | Sort-Object Date -Descending | ForEach-Object {
        $img = if ($_.FeaturedImage) { "<p><a href='/{0}/'><img src='{1}' alt='{2}'></a></p>" -f $_.Slug, $_.FeaturedImage, (HtmlEncode $_.Title) } else { '' }
      $excerpt = Build-Excerpt -Html $(if ([string]::IsNullOrWhiteSpace($_.Excerpt)) { $_.Content } else { $_.Excerpt })
      "<div class='post-card'><h3><a href='/{0}/'>{1}</a></h3><p class='meta'>{2}</p>{3}<p>{4}</p><p><a href='/{0}/'>Read more</a></p></div>" -f $_.Slug, (HtmlEncode $_.Title), $_.Date.ToString('MMMM d, yyyy', $dateCulture), $img, (HtmlEncode $excerpt)
    }) -join "`n"

    $body = "<h1>Category: " + (HtmlEncode $cat.Name) + "</h1>" + $cards
    Write-Page -OutPath (Join-Path $OutDir ('category\' + $slug + '\index.html')) -Title ('Category: ' + $cat.Name) -BodyHtml $body -RecentPosts $recentPosts -TopPages $topPages -MenuHtml $menuHtml -SiteTitleOnly
}

# Build blog index page
$blogCards = ($posts | ForEach-Object {
    $img = if ($_.FeaturedImage) { "<p><a href='/{0}/'><img src='{1}' alt='{2}'></a></p>" -f $_.Slug, $_.FeaturedImage, (HtmlEncode $_.Title) } else { '' }
  $excerptText = Build-Excerpt -Html $(if ([string]::IsNullOrWhiteSpace($_.Excerpt)) { $_.Content } else { $_.Excerpt }) -MaxWords 45
  $excerpt = if ([string]::IsNullOrWhiteSpace($excerptText)) { '' } else { "<p>" + (HtmlEncode $excerptText) + "</p>" }
    "<div class='post-card'><h2><a href='/{0}/'>{1}</a></h2><p class='meta'>By {2} on {3}</p>{4}{5}<p><a href='/{0}/'>Read more</a></p></div>" -f $_.Slug, (HtmlEncode $_.Title), (HtmlEncode $_.Author), $_.Date.ToString('MMMM d, yyyy', $dateCulture), $img, $excerpt
}) -join "`n"
Write-Page -OutPath (Join-Path $OutDir 'blog\index.html') -Title 'Blog' -BodyHtml ("<h1>Blog</h1>" + $blogCards) -RecentPosts $recentPosts -TopPages $topPages -MenuHtml $menuHtml

# Build homepage
$hero = $posts | Select-Object -First 1
$heroImg = if ($hero.FeaturedImage) { "<p><a href='/{0}/'><img src='{1}' alt='{2}'></a></p>" -f $hero.Slug, $hero.FeaturedImage, (HtmlEncode $hero.Title) } else { '' }
$homeCards = ($posts | Select-Object -First 20 | ForEach-Object {
  $excerpt = Build-Excerpt -Html $(if ([string]::IsNullOrWhiteSpace($_.Excerpt)) { $_.Content } else { $_.Excerpt }) -MaxWords 70
  "<div class='post-card'><h3><a href='/{0}/'>{1}</a></h3><p class='meta'>{2}</p><p>{3}</p><p><a href='/{0}/'>Read more</a></p></div>" -f $_.Slug, (HtmlEncode $_.Title), $_.Date.ToString('MMMM d, yyyy', $dateCulture), (HtmlEncode $excerpt)
}) -join "`n"

$featuredDestinations = if ($destinationPagesOrdered.Count -gt 0) { $destinationPagesOrdered | Select-Object -First 12 } else { @() }
$destinationsHtml = ($featuredDestinations | ForEach-Object {
  "<li><a href='/{0}/'>{1}</a></li>" -f $_.Slug, (HtmlEncode $_.Title)
}) -join "`n"

$aboutPage = $pages | Where-Object { $_.Slug -eq 'about-us' } | Select-Object -First 1
$introHtml = if ($aboutPage -and -not [string]::IsNullOrWhiteSpace($aboutPage.Content)) {
  $aboutPage.Content
} else {
  "<p>This is the static Option B starter built from your existing WordPress export and media.</p>"
}

$homeBody = @"
<h1>Traveling the world with children</h1>
<div class='post-card'>
$introHtml
</div>
<h2>Destinations</h2>
<ul class='dest-list'>
$destinationsHtml
</ul>
<div class='post-card'>
  <h2><a href='/$($hero.Slug)/'>$(HtmlEncode $hero.Title)</a></h2>
  <p class='meta'>By $(HtmlEncode $hero.Author) on $($hero.Date.ToString('MMMM d, yyyy', $dateCulture))</p>
  $heroImg
  $($hero.Content)
</div>
<h2>Recent Posts</h2>
$homeCards
"@
Write-Page -OutPath (Join-Path $OutDir 'index.html') -Title 'Home' -BodyHtml $homeBody -RecentPosts $recentPosts -TopPages $topPages -MenuHtml $menuHtml -SiteTitleOnly

# Legacy URL behavior: /about-us/ on the live site resolves to the same front-page content.
Write-Page -OutPath (Join-Path $OutDir 'about-us\index.html') -Title 'About us' -BodyHtml $homeBody -RecentPosts $recentPosts -TopPages $topPages -MenuHtml $menuHtml -SiteTitleOnly

# Optional mirror for old root blog URL pattern
Copy-Item (Join-Path $OutDir 'blog\index.html') (Join-Path $OutDir 'blog.html') -Force

Write-Output ('BUILD_OK=True')
Write-Output ('OUT_DIR=' + $OutDir)
Write-Output ('POSTS=' + $posts.Count)
Write-Output ('PAGES=' + $pages.Count)
Write-Output ('CATEGORIES=' + $allCategories.Keys.Count)
