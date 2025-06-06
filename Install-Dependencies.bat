@echo off
chcp 936 >nul 2>&1
title NovelCraft Dependencies Installer

echo ========================================
echo    NovelCraft Dependencies Installer
echo ========================================
echo.

:: Check Python environment
echo [1/4] Checking Python environment...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found
    echo Please install Python 3.9 or higher
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)
python --version
echo Python environment OK

:: Check Node.js environment
echo [2/4] Checking Node.js environment...
node --version >nul 2>&1
if errorlevel 1 (
    echo Error: Node.js not found
    echo Please install Node.js 16 or higher
    echo Download: https://nodejs.org/
    pause
    exit /b 1
)
node --version
npm --version
echo Node.js environment OK

:: Install backend dependencies
echo [3/4] Installing backend dependencies...
if not exist "backend\requirements.txt" (
    echo Error: Backend requirements file not found
    pause
    exit /b 1
)

echo Installing Python packages...
cd backend
pip install -r requirements.txt
if errorlevel 1 (
    echo Backend dependencies installation failed
    echo Please check network connection or Python environment
    pause
    exit /b 1
)
cd ..
echo Backend dependencies installation completed

:: Install frontend dependencies
echo [4/4] Installing frontend dependencies...
if not exist "frontend\package.json" (
    echo Error: Frontend package file not found
    pause
    exit /b 1
)

echo Installing Node.js packages...
cd frontend
npm install
if errorlevel 1 (
    echo Frontend dependencies installation failed
    echo Please check network connection or Node.js environment
    pause
    exit /b 1
)
cd ..
echo Frontend dependencies installation completed

echo.
echo All dependencies installation completed!
echo.
echo Next steps:
echo    1. Run "Start-System.bat" to start NovelCraft system
echo    2. Or run "Stop-System.bat" to stop system
echo.
echo Tips:
echo    - Dependencies are usually installed once
echo    - You can re-run this script if problems occur
echo.

pause
