# One-click installer for TimeTrace on Windows
# Usage: Right-click -> Run with PowerShell

$ErrorActionPreference = 'Stop'

Write-Host "TimeTrace Installer starting..." -ForegroundColor Cyan

# Create target folder
$target = Join-Path $env:USERPROFILE "TimeTrace"
if (!(Test-Path $target)) { New-Item -ItemType Directory -Path $target | Out-Null }

# Download latest ZIP from GitHub
$zipUrl = "https://github.com/Cezeri73/timetrace/archive/refs/heads/main.zip"
$zipPath = Join-Path $target "timetrace.zip"
Invoke-WebRequest -Uri $zipUrl -OutFile $zipPath

# Extract ZIP
Add-Type -AssemblyName System.IO.Compression.FileSystem
$extractPath = Join-Path $target "timetrace"
if (Test-Path $extractPath) { Remove-Item $extractPath -Recurse -Force }
[System.IO.Compression.ZipFile]::ExtractToDirectory($zipPath, $target)

# Find extracted folder (it includes repo name-suffix)
$repoDir = Get-ChildItem -Path $target -Directory | Where-Object { $_.Name -like "timetrace-*" } | Select-Object -First 1
if ($null -eq $repoDir) { throw "Extraction failed" }

# Create venv and install requirements
$python = "python"
Push-Location $repoDir.FullName
python -m venv .venv
$venvPython = Join-Path $repoDir.FullName ".venv\Scripts\python.exe"
& $venvPython -m pip install --upgrade pip
& $venvPython -m pip install -r requirements.txt

Write-Host "Install complete. To run:" -ForegroundColor Green
Write-Host "`n$venvPython main.py" -ForegroundColor Yellow

Pop-Location
