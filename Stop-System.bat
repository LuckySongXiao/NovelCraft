@echo off
chcp 936 >nul 2>&1
title NovelCraft System Stopper

echo ========================================
echo    NovelCraft System Stopper
echo ========================================
echo.

echo Stopping NovelCraft system...
echo.

:: Stop Node.js processes (frontend)
echo [1/3] Stopping frontend service...
taskkill /f /im node.exe >nul 2>&1
if errorlevel 1 (
    echo Warning: No running frontend service found
) else (
    echo Frontend service stopped
)

:: Stop Python processes (backend)
echo [2/3] Stopping backend service...
taskkill /f /im python.exe >nul 2>&1
if errorlevel 1 (
    echo Warning: No running backend service found
) else (
    echo Backend service stopped
)

:: Stop related cmd windows
echo [3/3] Cleaning up windows...
taskkill /f /fi "WINDOWTITLE eq NovelCraft Backend" >nul 2>&1
taskkill /f /fi "WINDOWTITLE eq NovelCraft Frontend" >nul 2>&1
echo Windows cleaned up

echo.
echo NovelCraft system completely stopped!
echo.
echo Tips:
echo    - All related processes have been terminated
echo    - You can safely close this window
echo    - To restart, run "Start-System.bat"
echo.

pause
