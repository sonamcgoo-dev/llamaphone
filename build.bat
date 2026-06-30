@echo off
REM LlamaPhone Build Script for Windows
REM ===================================
REM Usage:
REM   build.bat              - Build single-file executable
REM   build.bat --clean      - Clean build folders
REM   build.bat --installer  - Build + create installer (requires Inno Setup)
REM   build.bat --all        - Full build + installer

color 0A
echo ========================================
echo    LlamaPhone Build Script
echo    Creating .exe with Installer
echo ========================================
echo.

set CLEAN=
set INSTALLER=
set FULL=

REM Parse arguments
if "%1"=="--clean" set CLEAN=yes
if "%1"=="--installer" set INSTALLER=yes
if "%1"=="--all" set FULL=yes

REM Clean if requested
if "%CLEAN%"=="yes" (
    echo Cleaning build artifacts...
    if exist build rmdir /s /q build
    if exist dist rmdir /s /q dist
    if exist __pycache__ rmdir /s /q __pycache__
    if exist installer rmdir /s /q installer
    echo Clean complete!
    echo.
)

REM Check Python version
echo Checking Python version...
python --version
echo.

REM Install dependencies
echo Installing build dependencies...
pip install pyinstaller PyQt6 httpx ruff --quiet
echo.

REM Build the single-file executable
echo Building LlamaPhone executable...
echo.

pyinstaller --onefile --name LlamaPhone llamaphone.py --noconfirm

if errorlevel 1 (
    echo.
    echo BUILD FAILED! Check errors above.
    pause
    exit /b 1
)

echo.
echo ========================================
echo    Build Complete!
echo ========================================
echo.
echo Executable location:
echo   dist\LlamaPhone.exe
echo.

REM Create installer if requested
if "%INSTALLER%"=="yes" (
    echo Creating installer...
    if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
        "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
    ) else if exist "C:\Program Files (x86)\Inno Setup 5\ISCC.exe" (
        "C:\Program Files (x86)\Inno Setup 5\ISCC.exe" installer.iss
    ) else (
        echo.
        echo WARNING: Inno Setup not found!
        echo Download from: https://jrsoftware.org/isinfo.php
        echo Then run: build.bat --installer
    )
)

if "%FULL%"=="yes" (
    echo Creating installer...
    if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
        "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
        echo.
        echo Installer location:
        echo   installer\LlamaPhone_Setup_1.0.0.exe
    ) else (
        echo.
        echo NOTE: Install Inno Setup to create installer
        echo Download from: https://jrsoftware.org/isinfo.php
    )
)

echo.
echo Done! Run: dist\LlamaPhone.exe
echo.
pause
