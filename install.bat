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

REM Upgrade pip silently
python -m pip install --upgrade pip --quiet

REM Install runtime dependencies
echo Installing dependencies...
pip install PyQt6 httpx --quiet
if errorlevel 1 (
    echo ERROR: pip install failed. Check your internet connection.
    pause
    exit /b 1
)

REM Create desktop launcher
echo Creating launcher...
python -c "import os,sys; home=os.path.expanduser('~'); path=os.path.dirname(os.path.abspath('llamaphone.py')); open(os.path.join(home,'llamaphone.bat'),'w').write(f'@echo off\ncd /d \"{path}\"\npython llamaphone.py %%*\n'); print('Launcher: ' + os.path.join(home,'llamaphone.bat'))"

echo.
echo ============================================
echo   Done!  Run:  python llamaphone.py
echo ============================================
echo.
pause
