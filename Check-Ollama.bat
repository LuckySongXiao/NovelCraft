@echo off
chcp 936 >nul 2>&1
title Ollama Status Checker

echo ========================================
echo    Ollama Status Checker
echo ========================================
echo.

:: Check if Ollama is installed
echo [1/5] Checking Ollama installation...
ollama --version >nul 2>&1
if errorlevel 1 (
    echo Error: Ollama not found
    echo Please install Ollama from: https://ollama.ai/
    echo.
    pause
    exit /b 1
) else (
    ollama --version
    echo Ollama installation OK
)
echo.

:: Check if Ollama service is running
echo [2/5] Checking Ollama service...
tasklist /FI "IMAGENAME eq ollama.exe" 2>nul | find /I "ollama.exe" >nul
if errorlevel 1 (
    echo Warning: Ollama service not running
    echo Starting Ollama service...
    start "Ollama Service" ollama serve
    echo Waiting for service to start...
    timeout /t 5 /nobreak >nul
) else (
    echo Ollama service is running
)
echo.

:: Check API connection
echo [3/5] Testing API connection...
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo Error: Cannot connect to Ollama API
    echo Please ensure Ollama service is running
) else (
    echo API connection OK
)
echo.

:: List available models
echo [4/5] Checking available models...
ollama list
echo.

:: Check default model
echo [5/5] Checking default model...
ollama list | find "mollysama/rwkv-7-g1:0.4B" >nul
if errorlevel 1 (
    echo Warning: Default model not found
    echo To install default model, run:
    echo   ollama pull mollysama/rwkv-7-g1:0.4B
) else (
    echo Default model found: mollysama/rwkv-7-g1:0.4B
)
echo.

echo ========================================
echo Status check completed
echo ========================================
echo.
echo Service URL: http://localhost:11434
echo NovelCraft should now be able to connect to Ollama
echo.

pause
