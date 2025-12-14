# Build a standalone EXE with PyInstaller
# Requires: pip install pyinstaller

$ErrorActionPreference = 'Stop'

Write-Host "Building TimeTrace EXE..." -ForegroundColor Cyan

# Activate venv if exists
$venvPy = "C:/Users/PC1/Desktop/TRACKER/.venv/Scripts/python.exe"
if (Test-Path $venvPy) {
  & $venvPy -m pip install --upgrade pip
  & $venvPy -m pip install pyinstaller
  & $venvPy -m PyInstaller --noconfirm --onefile --name TimeTrace --add-data "settings.json;." --add-data "README.md;." main.py
} else {
  python -m pip install --upgrade pip
  python -m pip install pyinstaller
  python -m PyInstaller --noconfirm --onefile --name TimeTrace --add-data "settings.json;." --add-data "README.md;." main.py
}

Write-Host "Build complete. EXE is under 'dist/TimeTrace.exe'" -ForegroundColor Green
