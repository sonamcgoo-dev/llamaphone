@echo off
setlocal
title LlamaPhone Installer
color 0A

echo ============================================
echo     LlamaPhone - Quick Install
echo ============================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python 3.10+ not found.
    echo Download from: https://python.org/downloads/
    pause
    exit /b 1
)

REM Run full onboarding (deps + adb + ollama + model pull + launcher)
python setup.py
if errorlevel 1 (
    echo ERROR: Onboarding failed.
    pause
    exit /b 1
)

echo.
echo ============================================
echo   Done!  Run:  python llamaphone.py
echo ============================================
echo.
pause
