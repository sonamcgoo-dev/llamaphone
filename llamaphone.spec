# -*- mode: python ; coding: utf-8 -*-
"""
LlamaPhone - PyInstaller Build Specification
============================================
This spec file packages LlamaPhone as a standalone Windows executable.

Usage:
    pyinstaller llamaphone.spec

For a single-file executable:
    pyinstaller --onefile llamaphone.spec
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
    "llamaphone",
    "llamaphone.ui",
    "llamaphone.ui.splash_screen",
    "llamaphone.ui.main_window",
    "llamaphone.ui.terminal_screen",
    "llamaphone.ui.control_panel",
    "llamaphone.ui.styles",
    "llamaphone.ai",
    "llamaphone.ai.ollama_client",
    "llamaphone.ai.tools",
    "llamaphone.ai.tools.adb_tools",
    "llamaphone.ai.tools.fastboot_tools",
    "llamaphone.ai.tools.device_tools",
    "llamaphone.modules",
    "llamaphone.modules.bypass",
    "llamaphone.modules.exploits",
    "llamaphone.modules.drivers",
    "llamaphone.core",
    "llamaphone.core.auth",
    "llamaphone.core.config",
    "llamaphone.core.logger",
    
    # HTTP client
    "httpx",
    "httpcore",
    "anyio",
    "certifi",
    "h11",
    "idna",
    
    # JSON handling
    "json",
    "pickle",
    "sqlite3",
    
    # Socket for network tools
    "socket",
    "concurrent.futures",
    "threading",
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
    # Assets directory
    (str(ROOT_DIR / "assets"), "assets"),
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

# Create the executable
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="LlamaPhone",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Set to True for debug console
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_path,
)

# Collect all other files
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="LlamaPhone",
)

# Alternative: Single file executable (uncomment for single file)
# mode = 'single-file' # Uncomment for single-file mode
# mode = 'onedir'  # Default: directory with exe and dependencies
