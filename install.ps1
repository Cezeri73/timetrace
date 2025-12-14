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
# Clean previous extracted repo folders like timetrace-*
Get-ChildItem -Path $target -Directory | Where-Object { $_.Name -like "timetrace-*" } | ForEach-Object { 
	try { Remove-Item $_.FullName -Recurse -Force } catch {}
}
[System.IO.Compression.ZipFile]::ExtractToDirectory($zipPath, $target)

# Find extracted folder (it includes repo name-suffix)
$repoDir = Get-ChildItem -Path $target -Directory | Where-Object { $_.Name -like "timetrace-*" } | Select-Object -First 1
if ($null -eq $repoDir) { throw "Extraction failed" }

# Create venv and install requirements
# Detect Python: prefer `python`, fallback to `py -3`
function Get-PythonCmd {
	try {
		$ver = & python --version 2>$null
		if ($LASTEXITCODE -eq 0) { return 'python' }
	} catch {}
	try {
		$ver = & py -3 --version 2>$null
		if ($LASTEXITCODE -eq 0) { return 'py -3' }
	} catch {}
	throw 'Python not found. Please install Python 3 and try again.'
}

$python = Get-PythonCmd
Push-Location $repoDir.FullName
& $python -m venv .venv
$venvPython = Join-Path $repoDir.FullName ".venv\Scripts\python.exe"
& $venvPython -m pip install --upgrade pip
& $venvPython -m pip install -r requirements.txt

Write-Host "Install complete." -ForegroundColor Green

# Create Desktop shortcut for one-click launch
try {
	$desktop = [Environment]::GetFolderPath('Desktop')
	$shortcutPath = Join-Path $desktop 'TimeTrace.lnk'
	$WshShell = New-Object -ComObject WScript.Shell
	$Shortcut = $WshShell.CreateShortcut($shortcutPath)
	$Shortcut.TargetPath = $venvPython
	$Shortcut.Arguments = '"' + (Join-Path $repoDir.FullName 'main.py') + '"'
	$Shortcut.WorkingDirectory = $repoDir.FullName
	$Shortcut.IconLocation = (Join-Path $repoDir.FullName 'icon.ico')
	$Shortcut.Description = 'Launch TimeTrace'
	$Shortcut.Save()
	Write-Host "Desktop shortcut created: TimeTrace" -ForegroundColor Green

	# Start Menu shortcut
	$startMenu = Join-Path $env:AppData 'Microsoft\\Windows\\Start Menu\\Programs'
	$startShortcutPath = Join-Path $startMenu 'TimeTrace.lnk'
	$StartShortcut = $WshShell.CreateShortcut($startShortcutPath)
	$StartShortcut.TargetPath = $venvPython
	$StartShortcut.Arguments = '"' + (Join-Path $repoDir.FullName 'main.py') + '"'
	$StartShortcut.WorkingDirectory = $repoDir.FullName
	$StartShortcut.IconLocation = (Join-Path $repoDir.FullName 'icon.ico')
	$StartShortcut.Description = 'Launch TimeTrace'
	$StartShortcut.Save()
	Write-Host "Start Menu shortcut created: TimeTrace" -ForegroundColor Green
} catch {
	Write-Host "Shortcut creation skipped: $_" -ForegroundColor Yellow
}

Write-Host "You can launch from the Desktop shortcut or run:" -ForegroundColor Green
Write-Host "`n$venvPython ""$(Join-Path $repoDir.FullName 'main.py')""" -ForegroundColor Yellow

Pop-Location
