# -*- mode: python ; coding: utf-8 -*-
"""
LlamaPhone - PyInstaller Build Specification
============================================
SINGLE-FILE executable for Windows.

Usage:
    pyinstaller --onefile llamaphone.spec
    Or just double-click build.bat
"""

from pathlib import Path
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

# Project root
ROOT_DIR = Path(SPECPATH)

# Main script
main_script = str(ROOT_DIR / "llamaphone.py")

# Hidden imports for PyQt6 and application modules
hiddenimports = [
    "PyQt6.QtCore",
    "PyQt6.QtGui",
    "PyQt6.QtWidgets",
    "PyQt6.sip",
    "httpx",
    "httpcore",
    "anyio",
    "certifi",
    "h11",
    "idna",
    "sniffio",
]
hiddenimports += collect_submodules("ui")
hiddenimports += collect_submodules("ai")
hiddenimports += collect_submodules("modules")
hiddenimports += collect_submodules("core")

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

assets_dir = ROOT_DIR / "assets"
if assets_dir.exists():
    datas.append((str(assets_dir), "assets"))

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
