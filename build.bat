@echo off
REM LlamaPhone Build Script for Windows
REM ===================================
REM Usage:
REM   build.bat           - Build directory executable
REM   build.bat --onefile - Build single-file executable
REM   build.bat --clean   - Clean and rebuild

color 0A
echo ========================================
echo    LlamaPhone Build Script
echo ========================================
echo.

set ONEFILE=
set CLEAN=
set DEBUG=

REM Parse arguments
if "%1"=="--onefile" set ONEFILE=--onefile
if "%1"=="--clean" set CLEAN=yes
if "%1"=="--debug" set DEBUG=yes

REM Clean if requested
if "%CLEAN%"=="yes" (
    echo Cleaning build artifacts...
    if exist build rmdir /s /q build
    if exist dist rmdir /s /q dist
    if exist __pycache__ rmdir /s /q __pycache__
    if exist *.spec del /q *.spec
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

REM Build the application
echo Building LlamaPhone executable...
echo.

if defined ONEFILE (
    echo Building single-file executable...
    pyinstaller --onefile --name LlamaPhone llamaphone.spec --console
) else (
    echo Building directory executable...
    if exist llamaphone.spec (
        pyinstaller llamaphone.spec --console
    ) else (
        pyinstaller --name LlamaPhone llamaphone.py --console
    )
)

echo.
echo ========================================
echo    Build Complete!
echo ========================================
echo.
echo Executable location:
if defined ONEFILE (
    echo   dist\LlamaPhone.exe
) else (
    echo   dist\LlamaPhone\LlamaPhone.exe
)
echo.
echo NOTE: Run with --debug flag to see console output
echo.
pause
