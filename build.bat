@echo off
setlocal
title LlamaPhone Builder
color 0A

echo ========================================
echo    LlamaPhone Build Script
echo    Packages app into a reliable onedir build
echo ========================================
echo.

REM Parse arguments
set CLEAN=
set INSTALLER=
if "%1"=="--clean"     set CLEAN=yes
if "%1"=="--installer" set INSTALLER=yes
if "%1"=="--all"       set CLEAN=yes & set INSTALLER=yes

REM Clean if requested
if "%CLEAN%"=="yes" (
    echo Cleaning build artifacts...
    if exist build     rmdir /s /q build
    if exist dist      rmdir /s /q dist
    if exist __pycache__ rmdir /s /q __pycache__
    if exist installer rmdir /s /q installer
    echo Done.
    echo.
)

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found.
    pause & exit /b 1
)

REM Install build dependencies
echo Installing build dependencies...
python -m pip install pyinstaller PyQt6 httpx --quiet
if errorlevel 1 (
    echo ERROR: pip install failed.
    pause & exit /b 1
)
echo.

REM Build using the spec file (includes hidden imports, data files, and icon)
echo Building LlamaPhone package...
echo.
python -m PyInstaller llamaphone.spec --noconfirm --clean

if errorlevel 1 (
    echo.
    echo BUILD FAILED. Check errors above.
    pause & exit /b 1
)

echo.
echo ========================================
echo    Build Complete!
echo    Output: dist\LlamaPhone\LlamaPhone.exe
echo ========================================
echo.

REM Create installer if requested
if "%INSTALLER%"=="yes" (
    if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
        echo Creating installer...
        "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
        echo Installer: installer\LlamaPhone_Setup_1.0.0.exe
    ) else if exist "C:\Program Files (x86)\Inno Setup 5\ISCC.exe" (
        "C:\Program Files (x86)\Inno Setup 5\ISCC.exe" installer.iss
    ) else (
        echo NOTE: Inno Setup not found - skipping installer.
        echo Download from: https://jrsoftware.org/isinfo.php
    )
    echo.
)

pause
