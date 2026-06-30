# -*- mode: python ; coding: utf-8 -*-
"""
LlamaPhone - PyInstaller Build Specification
============================================
SINGLE-FILE executable for Windows.

Usage:
    pyinstaller --onefile llamaphone.spec
    Or just double-click build.bat
"""

import sys
import os
from pathlib import Path

block_cipher = None

# Project root
ROOT_DIR = Path(__file__).parent

# Main script
main_script = str(ROOT_DIR / "llamaphone.py")

# Hidden imports for PyQt6 and other dependencies
hiddenimports = [
    # PyQt6 core
    "PyQt6.QtCore",
    "PyQt6.QtGui",
    "PyQt6.QtWidgets",
    "PyQt6.sip",
    
    # Application modules
    "ui",
    "ui.splash_screen",
    "ui.main_window",
    "ui.terminal_screen",
    "ui.control_panel",
    "ui.styles",
    "ai",
    "ai.ollama_client",
    "ai.tools",
    "ai.tools.adb_tools",
    "ai.tools.fastboot_tools",
    "ai.tools.device_tools",
    "modules",
    "modules.bypass",
    "modules.exploits",
    "modules.drivers",
    "core",
    "core.auth",
    "core.config",
    "core.logger",
    
    # HTTP client
    "httpx",
    "httpcore",
    "anyio",
    "certifi",
    "h11",
    "idna",
    "sniffio",
    
    # JSON handling
    "json",
    "pickle",
    
    # Socket for network tools
    "socket",
    "concurrent.futures",
    "threading",
    "contextlib",
]

# Exclude patterns
excludes = [
    "matplotlib",
    "numpy",
    "pandas",
    "scipy",
    "PIL",
    "tkinter",
    "test",
    "unittest",
]

# Data files to include
datas = [
    (str(ROOT_DIR / "data"), "data"),
]

# Icons (if present)
icon_path = None
icon_locations = [
    ROOT_DIR / "assets" / "icon.ico",
    ROOT_DIR / "assets" / "icon.png",
]

for loc in icon_locations:
    if loc.exists():
        icon_path = str(loc)
        break

# Analysis configuration
a = Analysis(
    [main_script],
    pathex=[str(ROOT_DIR)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Create the PYZ archive
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Create SINGLE-FILE executable
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=False,
    name="LlamaPhone",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    console=False,  # Windowed mode - no console
    disable_windowed_traceback=True,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_path,
)
