@echo off
chcp 936 >nul 2>&1
title NovelCraft System Launcher

echo ========================================
echo    NovelCraft System Launcher
echo ========================================
echo.

:: Check Python environment
echo [1/5] Checking Python environment...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found
    echo Please install Python 3.9 or higher
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo Python environment OK

:: Check Node.js environment
echo [2/5] Checking Node.js environment...
node --version >nul 2>&1
if errorlevel 1 (
    echo Error: Node.js not found
    echo Please install Node.js 16 or higher
    echo Download: https://nodejs.org/
    pause
    exit /b 1
)
echo Node.js environment OK

:: Check backend dependencies
echo [3/5] Checking backend dependencies...
if not exist "backend\requirements.txt" (
    echo Error: Backend requirements file not found
    pause
    exit /b 1
)

cd backend
pip install -r requirements.txt >nul 2>&1
if errorlevel 1 (
    echo Error: Backend dependencies installation failed
    echo Retrying installation...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Backend dependencies installation failed, please check network
        pause
        exit /b 1
    )
)
cd ..
echo Backend dependencies OK

:: Check frontend dependencies
echo [4/5] Checking frontend dependencies...
if not exist "frontend\package.json" (
    echo Error: Frontend package file not found
    pause
    exit /b 1
)

cd frontend
if not exist "node_modules" (
    echo Installing frontend dependencies, please wait...
    npm install
    if errorlevel 1 (
        echo Frontend dependencies installation failed, please check network
        pause
        exit /b 1
    )
)
cd ..
echo Frontend dependencies OK

:: Start services
echo [5/5] Starting services...
echo.
echo Starting NovelCraft system...
echo.
echo Service addresses:
echo    Frontend: http://localhost:3000
echo    Backend:  http://localhost:8000
echo    API Docs: http://localhost:8000/docs
echo.
echo Default AI Configuration:
echo    Provider: Ollama (Local AI)
echo    Model: mollysama/rwkv-7-g1:0.4B
echo    Service: http://localhost:11434
echo.
echo Tips:
echo    - Keep this window open
echo    - Press Ctrl+C to stop services
echo    - Browser will open automatically
echo    - Install Ollama for AI features: https://ollama.ai/
echo.

:: Start backend service
echo Starting backend service...
start "NovelCraft Backend" cmd /k "cd backend && python run.py"

:: Wait for backend startup
echo Waiting for backend service...
timeout /t 5 /nobreak >nul

:: Start frontend service
echo Starting frontend service...
start "NovelCraft Frontend" cmd /k "cd frontend && npm start"

:: Wait for frontend startup and open browser
echo Waiting for frontend service...
timeout /t 10 /nobreak >nul

:: Note: Browser will be opened automatically by the application
echo Browser will open automatically when frontend is ready...

echo.
echo System startup completed!
echo.
echo Management options:
echo    1. Press any key to close this window (services continue running)
echo    2. Run "Stop-System.bat" to stop all services
echo    3. Press Ctrl+C to stop services (if needed)
echo.

pause
