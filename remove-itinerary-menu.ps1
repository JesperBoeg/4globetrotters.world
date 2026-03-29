$root = "C:\Users\agile\VSCode projects\4globetrotters\option-b-static\site"
$files = Get-ChildItem $root -Recurse -Include *.html -File
$changed = 0

foreach ($f in $files) {
  $c = Get-Content $f.FullName -Raw -Encoding UTF8
  if ($null -eq $c) { continue }
  $u = $c

  # Remove any nav/footer list item linking to itinerary
  $u = [regex]::Replace($u, '<li><a href="/itinerary/">[^<]*</a></li>\s*', '')
  $u = [regex]::Replace($u, "<li><a href='/itinerary/'>[^<]*</a></li>\s*", "")

  if ($u -ne $c) {
    [System.IO.File]::WriteAllText($f.FullName, $u, (New-Object System.Text.UTF8Encoding($false)))
    $changed++
  }
}

Write-Output "Updated files: $changed"