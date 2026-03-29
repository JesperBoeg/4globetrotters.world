param(
    [string]$SiteDir = "C:\Users\agile\VSCode projects\4globetrotters-migration\option-b-static\site",
    [string]$RemoteDir = "/public_html/",
    [string]$WinScpPath = "$env:LOCALAPPDATA\Programs\WinSCP\WinSCP.com",
    [switch]$IncludeUploads
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $SiteDir)) {
    throw "Site directory not found: $SiteDir"
}

if (-not (Test-Path $WinScpPath)) {
    throw "WinSCP.com not found at: $WinScpPath"
}

if ([string]::IsNullOrWhiteSpace($env:HOSTINGER_FTP_HOST) -or
    [string]::IsNullOrWhiteSpace($env:HOSTINGER_FTP_USER) -or
    [string]::IsNullOrWhiteSpace($env:HOSTINGER_FTP_PASS)) {
    throw "Set HOSTINGER_FTP_HOST, HOSTINGER_FTP_USER, and HOSTINGER_FTP_PASS environment variables first."
}

$escapedSite = $SiteDir.Replace("'", "''")
$escapedRemote = $RemoteDir.Replace("'", "''")

$syncCommand = if ($IncludeUploads) {
    "synchronize remote -criteria=time -mirror '$escapedSite' '$escapedRemote'"
}
else {
    "synchronize remote -criteria=time -mirror -filemask=\"| */wp-content/uploads/*\" '$escapedSite' '$escapedRemote'"
}

$tempScript = Join-Path $env:TEMP "winscp-hostinger-deploy.txt"
$logPath = Join-Path $env:TEMP "winscp-hostinger-deploy.log"

$scriptContent = @"
open ftpes://$($env:HOSTINGER_FTP_USER):$($env:HOSTINGER_FTP_PASS)@$($env:HOSTINGER_FTP_HOST)/
option batch abort
option confirm off
$syncCommand
exit
"@

Set-Content -Path $tempScript -Value $scriptContent -Encoding ASCII

& "$WinScpPath" /ini=nul /script="$tempScript" /log="$logPath"

Write-Output "DEPLOY_DONE=True"
Write-Output "REMOTE_DIR=$RemoteDir"
Write-Output "INCLUDE_UPLOADS=$IncludeUploads"
Write-Output "LOG=$logPath"
