$ErrorActionPreference = "Stop"
Set-Location -Path $PSScriptRoot

function Test-Python {
	try {
		$null = python --version 2>&1
		return $true
	}
	catch {
		Write-Host "Python was not found. Install Python and try again." -ForegroundColor Red
		return $false
	}
}

function Ensure-Dependencies {
	$requirementsFile = Join-Path $PSScriptRoot "requirements.txt"

	if (-not (Test-Path $requirementsFile)) {
		Write-Host "requirements.txt was not found. Skipping dependency installation." -ForegroundColor Yellow
		return $true
	}

	Write-Host "Checking Python dependencies..." -ForegroundColor Cyan
	python -c "import requests; import bs4" 2>$null
	if ($LASTEXITCODE -eq 0) {
		Write-Host "Dependencies are already installed." -ForegroundColor Green
		return $true
	}

	Write-Host "Installing dependencies from requirements.txt..." -ForegroundColor Yellow
	python -m pip install -r $requirementsFile
	if ($LASTEXITCODE -ne 0) {
		Write-Host "Dependency installation failed." -ForegroundColor Red
		return $false
	}

	Write-Host "Dependencies installed successfully." -ForegroundColor Green
	return $true
}

function Invoke-PythonScript([string]$ScriptName) {
	if (-not (Test-Path $ScriptName)) {
		Write-Host "Script not found: $ScriptName" -ForegroundColor Red
		return
	}

	Write-Host "`nRunning $ScriptName ..." -ForegroundColor Cyan
	python $ScriptName
	if ($LASTEXITCODE -ne 0) {
		Write-Host "$ScriptName ended with exit code $LASTEXITCODE." -ForegroundColor Red
	}
}

if (-not (Test-Python)) {
	Read-Host "Press Enter to exit"
	exit 1
}

if (-not (Ensure-Dependencies)) {
	Read-Host "Press Enter to exit"
	exit 1
}

if (-not (Test-Path ".\pc_games")) {
	Write-Host "The pc_games folder was not found in $PSScriptRoot." -ForegroundColor Red
	Read-Host "Press Enter to exit"
	exit 1
}

while ($true) {
	Clear-Host
	Write-Host "===============================================" -ForegroundColor DarkCyan
	Write-Host "       PC GAME DATA DOWNLOADER" -ForegroundColor Cyan
	Write-Host "===============================================" -ForegroundColor DarkCyan
	Write-Host "Folder: $((Resolve-Path '.\pc_games').Path)"
	Write-Host ""
	Write-Host "1. Download missing cover images"
	Write-Host "2. Fetch requirements for all folders"
	Write-Host "3. Resume interrupted requirements update"
	Write-Host "4. Run covers and requirements"
	Write-Host "5. Count downloaded files"
	Write-Host "0. Exit"
	Write-Host ""

	$choice = Read-Host "Choose an option"

	switch ($choice) {
		"1" {
			Invoke-PythonScript "download_cover_images.py"
			Read-Host "`nPress Enter to return to the menu"
		}
		"2" {
			Invoke-PythonScript "fetch_real_requirements.py"
			Read-Host "`nPress Enter to return to the menu"
		}
		"3" {
			Invoke-PythonScript "resume_fetch_requirements.py"
			Read-Host "`nPress Enter to return to the menu"
		}
		"4" {
			Invoke-PythonScript "download_cover_images.py"
			Invoke-PythonScript "resume_fetch_requirements.py"
			Read-Host "`nPress Enter to return to the menu"
		}
		"5" {
			$folders = @(Get-ChildItem ".\pc_games" -Directory).Count
			$covers = @(Get-ChildItem ".\pc_games" -Recurse -Filter "cover.jpg").Count
			$requirements = @(Get-ChildItem ".\pc_games" -Recurse -Filter "system_requirements.txt").Count
			Write-Host "`nGame folders: $folders" -ForegroundColor Green
			Write-Host "Cover images: $covers" -ForegroundColor Green
			Write-Host "Requirements files: $requirements" -ForegroundColor Green
			Read-Host "`nPress Enter to return to the menu"
		}
		"0" {
			exit 0
		}
		default {
			Write-Host "Invalid option." -ForegroundColor Yellow
			Start-Sleep -Seconds 1
		}
	}
}
