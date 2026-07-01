#!/usr/bin/env python3
"""
LlamaPhone - Setup Script
Checks prerequisites and installs dependencies.
"""

import os
import platform
import subprocess
import sys


def print_header():
    print("""
    ╔═══════════════════════════════════════════╗
    ║   LLAMAPHONE  -  AI Mobile Repair Console ║
    ╚═══════════════════════════════════════════╝
    """)


def check_python():
    """Check Python version."""
    if sys.version_info < (3, 10):
        print(f"❌ Python 3.10+ required (found {sys.version_info.major}.{sys.version_info.minor})")
        sys.exit(1)
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor}")


def check_ollama():
    """Check if Ollama is installed."""
    try:
        result = subprocess.run(
            ["ollama", "--version"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            print(f"✓ Ollama: {result.stdout.strip()}")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    print("⚠  Ollama not found — install from https://ollama.ai/ then run: ollama pull qwen2.5-coder:7b")
    return False


def check_adb():
    """Check if ADB is installed."""
    try:
        result = subprocess.run(
            ["adb", "version"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            print(f"✓ ADB: {result.stdout.splitlines()[0]}")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    print("⚠  ADB not found — install Android SDK Platform Tools and add to PATH")
    return False


def install_dependencies():
    """Install Python dependencies."""
    print("\n📦 Installing dependencies...")
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--quiet"],
        check=True
    )
    print("✓ Dependencies installed")


def create_launcher():
    """Create a platform-specific launch script."""
    home = os.path.expanduser("~")
    project_path = os.path.dirname(os.path.abspath(__file__))

    if platform.system() == "Windows":
        script_path = os.path.join(home, "llamaphone.bat")
        content = f'@echo off\ncd /d "{project_path}"\npython llamaphone.py %*\n'
    else:
        script_path = os.path.join(home, "llamaphone.sh")
        content = f'#!/bin/bash\ncd "{project_path}"\npython3 llamaphone.py "$@"\n'

    try:
        with open(script_path, "w") as f:
            f.write(content)
        if platform.system() != "Windows":
            os.chmod(script_path, 0o755)
        print(f"✓ Launcher created: {script_path}")
    except Exception as e:
        print(f"⚠  Could not create launcher: {e}")


def main():
    print_header()
    print("Checking requirements...\n")

    check_python()
    check_ollama()
    check_adb()

    try:
        install_dependencies()
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies — check your pip/internet connection")
        sys.exit(1)

    create_launcher()

    print("\n" + "=" * 44)
    print("  Setup complete!  Run: python llamaphone.py")
    print("=" * 44 + "\n")


if __name__ == "__main__":
    main()
