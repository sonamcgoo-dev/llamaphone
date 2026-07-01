#!/usr/bin/env python3
"""
LlamaPhone - Setup Script
Downloads and configures the AI model
"""

import os
import subprocess
import sys


def print_header():
    print("=" * 63)
    print("LlamaPhone - AI MOBILE REPAIR CONSOLE")
    print("=" * 63)


def check_python():
    """Check Python version."""
    if sys.version_info < (3, 10):
        print("ERROR: Python 3.10+ required!")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True


def check_ollama():
    """Check if Ollama is installed."""
    try:
        result = subprocess.run(
            ["ollama", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"✓ Ollama detected: {result.stdout.strip()}")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    print("WARNING: Ollama not detected")
    print("   Install from: https://ollama.ai/")
    return False


def check_adb():
    """Check if ADB is installed."""
    try:
        result = subprocess.run(
            ["adb", "version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"✓ ADB detected: {version_line}")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    print("WARNING: ADB not detected")
    print("   Install Android SDK Platform Tools")
    return False


def install_dependencies():
    """Install Python dependencies."""
    print("\nInstalling Python dependencies...")

    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            check=True
        )
        print("✓ Dependencies installed")
        return True
    except subprocess.CalledProcessError:
        print("ERROR: Failed to install dependencies")
        return False


def download_model():
    """Download the AI model."""
    print("\nDownloading AI Model...")
    print("   Recommended: Qwen2.5-Coder-7B")
    print()

    models = {
        "1": ("qwen2.5-coder:7b", "Qwen2.5-Coder 7B (Recommended - best for code)"),
        "2": ("codellama:7b", "CodeLlama 7B (Good for code generation)"),
        "3": ("mistral:7b", "Mistral 7B (General purpose)"),
        "4": ("llama3:8b", "Llama 3 8B (General purpose)"),
    }

    print("Available models:")
    for key, (_model, desc) in models.items():
        print(f"  [{key}] {desc}")
    print()

    choice = input("Select model (1-4) or Enter for default [1]: ").strip() or "1"

    model_name = models.get(choice, models["1"])[0]

    print(f"\nPulling {model_name}...")
    print("   This may take several minutes depending on your internet speed...")

    try:
        subprocess.run(["ollama", "pull", model_name], check=True)
        print(f"✓ {model_name} downloaded successfully!")
        return True
    except subprocess.CalledProcessError:
        print(f"ERROR: Failed to download {model_name}")
        return False


def create_shortcuts():
    """Create desktop shortcuts (if possible)."""
    home = os.path.expanduser("~")

    # Create a simple launcher script
    script_path = os.path.join(home, "llamaphone.sh")
    project_path = os.path.dirname(os.path.abspath(__file__))

    launcher = f"""#!/bin/bash
cd "{project_path}"
python llamaphone.py
"""

    try:
        with open(script_path, 'w') as f:
            f.write(launcher)
        os.chmod(script_path, 0o755)
        print(f"\n✓ Launcher script created: {script_path}")
    except Exception:
        pass


def main():
    """Main setup function."""
    print_header()

    print("Setting up LlamaPhone...\n")

    # Check requirements
    if not check_python():
        sys.exit(1)

    check_ollama()
    check_adb()

    # Install dependencies
    install_dependencies()

    # Download model
    if check_ollama():
        download_model()

    # Create shortcuts
    create_shortcuts()

    print("\n" + "="*60)
    print("Setup complete!")
    print("="*60)
    print()
    print("To run LlamaPhone:")
    print("  cd llamaphone")
    print("  python llamaphone.py")
    print()
    print("Or use the launcher script:")
    print("  ~/llamaphone.sh")
    print()


if __name__ == "__main__":
    main()
