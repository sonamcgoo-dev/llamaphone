#!/usr/bin/env python3
"""
LlamaPhone onboarding script.
Installs Python deps, ADB platform-tools, Ollama, and pulls the default model.
"""

import os
import platform
import shutil
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path

DEFAULT_MODEL = "qwen2.5-coder:7b"
LOCAL_STATE_DIR = Path.home() / ".llamaphone"
LOCAL_PLATFORM_TOOLS_DIR = LOCAL_STATE_DIR / "platform-tools"


def print_header():
    print("""
    ╔═══════════════════════════════════════════╗
    ║   LLAMAPHONE  -  AI Mobile Repair Console ║
    ╚═══════════════════════════════════════════╝
    """)


def run_command(cmd: list[str], timeout: int | None = None, check: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=check)


def check_python():
    if sys.version_info < (3, 10):
        print(f"❌ Python 3.10+ required (found {sys.version_info.major}.{sys.version_info.minor})")
        sys.exit(1)
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor}")


def install_python_dependencies():
    print("\n📦 Installing Python dependencies...")
    run_command([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
    run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    print("✓ Python dependencies installed")


def install_adb_windows():
    LOCAL_STATE_DIR.mkdir(parents=True, exist_ok=True)
    zip_path = LOCAL_STATE_DIR / "platform-tools-latest-windows.zip"
    url = "https://dl.google.com/android/repository/platform-tools-latest-windows.zip"
    print("⬇ Downloading Android Platform Tools...")
    urllib.request.urlretrieve(url, zip_path)
    with zipfile.ZipFile(zip_path, "r") as archive:
        archive.extractall(LOCAL_STATE_DIR)
    zip_path.unlink(missing_ok=True)


def check_adb() -> bool:
    adb_from_path = shutil.which("adb")
    adb_local = LOCAL_PLATFORM_TOOLS_DIR / ("adb.exe" if platform.system() == "Windows" else "adb")
    adb_binary = adb_from_path or (str(adb_local) if adb_local.exists() else None)
    if not adb_binary:
        return False

    result = run_command([adb_binary, "version"], timeout=5)
    if result.returncode == 0:
        first_line = result.stdout.splitlines()[0] if result.stdout else "ADB detected"
        print(f"✓ ADB: {first_line}")
        return True
    return False


def ensure_adb():
    if check_adb():
        return
    if platform.system() == "Windows":
        install_adb_windows()
        if check_adb():
            return
    raise RuntimeError("ADB installation failed")


def install_ollama_windows():
    if not shutil.which("winget"):
        raise RuntimeError("winget not available to auto-install Ollama")
    print("⬇ Installing Ollama with winget...")
    run_command(
        [
            "winget",
            "install",
            "--id",
            "Ollama.Ollama",
            "-e",
            "--accept-package-agreements",
            "--accept-source-agreements",
        ],
        check=True,
    )


def find_ollama_binary() -> str | None:
    ollama = shutil.which("ollama")
    if ollama:
        return ollama
    if platform.system() == "Windows":
        candidates = [
            Path.home() / "AppData" / "Local" / "Programs" / "Ollama" / "ollama.exe",
            Path("C:/Program Files/Ollama/ollama.exe"),
        ]
        for candidate in candidates:
            if candidate.exists():
                return str(candidate)
    return None


def check_ollama() -> str | None:
    ollama = find_ollama_binary()
    if not ollama:
        return None
    result = run_command([ollama, "--version"], timeout=10)
    if result.returncode == 0:
        print(f"✓ Ollama: {result.stdout.strip()}")
        return ollama
    return None


def ensure_ollama() -> str:
    ollama = check_ollama()
    if ollama:
        return ollama
    if platform.system() == "Windows":
        install_ollama_windows()
        ollama = check_ollama()
        if ollama:
            return ollama
    raise RuntimeError("Ollama installation failed")


def pull_model(ollama_binary: str, model_name: str = DEFAULT_MODEL):
    print(f"🤖 Pulling model: {model_name}")
    run_command([ollama_binary, "pull", model_name], check=True)
    print(f"✓ Model pulled: {model_name}")


def create_launcher():
    home = Path.home()
    project_path = Path(__file__).resolve().parent
    platform_tools = LOCAL_PLATFORM_TOOLS_DIR

    if platform.system() == "Windows":
        script_path = home / "llamaphone.bat"
        content = (
            "@echo off\n"
            f'set "LLAMAPHONE_HOME={project_path}"\n'
            f'set "LLAMAPHONE_PLATFORM_TOOLS={platform_tools}"\n'
            'if exist "%LLAMAPHONE_PLATFORM_TOOLS%\\adb.exe" set "PATH=%LLAMAPHONE_PLATFORM_TOOLS%;%PATH%"\n'
            'cd /d "%LLAMAPHONE_HOME%"\n'
            "python llamaphone.py %*\n"
        )
    else:
        script_path = home / "llamaphone.sh"
        content = (
            "#!/bin/bash\n"
            f'LLAMAPHONE_HOME="{project_path}"\n'
            f'LLAMAPHONE_PLATFORM_TOOLS="{platform_tools}"\n'
            'if [ -x "$LLAMAPHONE_PLATFORM_TOOLS/adb" ]; then\n'
            '  export PATH="$LLAMAPHONE_PLATFORM_TOOLS:$PATH"\n'
            "fi\n"
            'cd "$LLAMAPHONE_HOME"\n'
            'python3 llamaphone.py "$@"\n'
        )

    script_path.write_text(content, encoding="utf-8")
    if platform.system() != "Windows":
        os.chmod(script_path, 0o755)
    print(f"✓ Launcher created: {script_path}")


def main():
    print_header()
    check_python()

    try:
        install_python_dependencies()
        ensure_adb()
        ollama_binary = ensure_ollama()
        pull_model(ollama_binary, DEFAULT_MODEL)
        create_launcher()
    except (subprocess.CalledProcessError, RuntimeError) as error:
        print(f"\n❌ Onboarding failed: {error}")
        sys.exit(1)

    print("\n" + "=" * 52)
    print(" Setup complete. Start with: python llamaphone.py")
    print("=" * 52 + "\n")


if __name__ == "__main__":
    main()
