# Build Car Rush as a standalone Windows .exe for itch.io
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host "Installing dependencies..."
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

Write-Host "Building CarRush.exe..."
python -m PyInstaller --noconfirm --clean CarRush.spec

$dist = Join-Path $PSScriptRoot "dist\CarRush.exe"
if (Test-Path $dist) {
    Write-Host ""
    Write-Host "SUCCESS: $dist"
    Write-Host "Upload dist\CarRush.exe (or zip it) to itch.io as the Windows download."
} else {
    Write-Error "Build failed - CarRush.exe was not created."
    exit 1
}
