$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$outDir = Join-Path $PSScriptRoot "itch_releases"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

if (Test-Path "dist\CarRush.exe") {
    $zip = Join-Path $outDir "CarRush-Windows.zip"
    if (Test-Path $zip) { Remove-Item $zip }
    Compress-Archive -Path "dist\CarRush.exe" -DestinationPath $zip -Force
    Write-Host "Created: $zip"
} else {
    Write-Host "Missing dist\CarRush.exe - run .\build_windows.ps1 first"
}

$apk = Get-ChildItem -Path "bin" -Filter "*.apk" -ErrorAction SilentlyContinue | Select-Object -First 1
if ($apk) {
    Copy-Item $apk.FullName (Join-Path $outDir $apk.Name) -Force
    Write-Host "Copied: $($apk.FullName)"
} else {
    Write-Host "Missing Android APK - run build_android.sh in WSL/Linux or GitHub Actions"
}

Write-Host ""
Write-Host "itch.io upload guide:"
Write-Host "  Windows -> Upload CarRush-Windows.zip, set target to Windows"
Write-Host "  Android -> Upload the .apk file, set target to Android"
Write-Host "  iOS     -> itch.io cannot install iOS apps; use TestFlight/App Store or offer a web build"
