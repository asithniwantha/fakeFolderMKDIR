@echo off
setlocal
cd /d "%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0run_game_data.ps1"
if errorlevel 1 (
	echo.
	echo The launcher ended with an error.
	pause
)
endlocal
