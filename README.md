# 📺 LlamaPhone

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-00AAFF?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-FFB000?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-FF3333?style=for-the-badge)
![GitHub](https://img.shields.io/github/stars/sonamcgoo-dev/llamaphone?style=for-the-badge)

### 🤖 AI-Powered Mobile Repair Console

*A retro CRT TV-styled desktop application for mobile device repair technicians*

**[Features](#features)** • **[Installation](#installation)** • **[Build](#building)** • **[Documentation](#documentation)**

</div>

---

## Overview

LlamaPhone is a standalone desktop application that combines local AI assistance with comprehensive mobile repair tools. The application features a unique **retro CRT TV aesthetic** with phosphor green terminals, TV knobs, and animated VU meters.

### Key Features

- 🤖 **Local AI Assistant** - Powered by Ollama, works completely offline
- 📱 **ADB/Fastboot Integration** - Full device management suite
- 🔓 **Bypass & Unlock Tools** - FRP, screen lock, network unlock guides
- 💣 **Exploit Database** - Known vulnerabilities organized by device
- 🔧 **Driver Database** - 5000+ device drivers with download links
- 🛡️ **Security First** - OAuth2 simulation, command validation, audit logging

---

## Features

### Interface Modules

| Module | Description |
|--------|-------------|
| 🤖 **AI Terminal** | Chat with local AI for repair guidance |
| 🔓 **Bypass** | FRP, screen lock, network unlock |
| 📡 **Connect** | USB/WiFi ADB, port scanning |
| 💻 **ADB** | Shell, push/pull, install, logcat |
| ⚡ **Fastboot** | Flash, unlock, lock, device info |
| 🔧 **Bootloader** | Unlock, lock, check status |
| 📥 **Download** | Samsung ODIN, Qualcomm EDL, MTK |
| 👑 **Root** | Magisk, Shizuku, KernelSU |
| 💣 **Exploits** | Known exploits by device/CVE |
| ⚙️ **Settings** | Model selection, config |

### UI Design

- **Retro CRT TV Frame** with curved screen effect
- **Phosphor Colors**: Green `#33FF33`, Amber `#FFB000`
- **Scanline Overlay** for authentic CRT look
- **Rotary Knobs** for channel and volume
- **LED Indicators** for power and status
- **VU Meter** animation

---

## Installation

### Prerequisites

| Requirement | Version | Notes |
|-------------|---------|-------|
| Python | 3.10+ | [python.org](https://python.org) |
| Ollama | Latest | [ollama.ai](https://ollama.ai) |
| ADB | Latest | Part of Android SDK |

### Quick Install

```bash
# Clone the repository
git clone https://github.com/sonamcgoo-dev/llamaphone.git
cd llamaphone

# Install dependencies
pip install -r requirements.txt

# Download AI model (recommended)
ollama pull qwen2.5-coder:7b

# Run the application
python llamaphone.py
```

---

## Building

### Windows Executable with Installer

1. **Download** the source code from GitHub

2. **Install Python** 3.10+ from [python.org](https://python.org)

3. **Install Inno Setup** (for installer):
   - Download from: https://jrsoftware.org/isinfo.php

4. **Run the build script:**
   ```bash
   build.bat
   ```

5. **Your executable is ready at:**
   ```
   dist\LlamaPhone.exe
   ```

### Create Installer

```bash
build.bat --all
```

This creates:
- `dist\LlamaPhone.exe` - The main executable
- `installer\LlamaPhone_Setup_1.0.0.exe` - Windows installer

### Build Options

| Command | Description |
|---------|-------------|
| `build.bat` | Build single-file exe |
| `build.bat --clean` | Clean build folders |
| `build.bat --installer` | Build + create installer |
| `build.bat --all` | Full build with installer |

---

## Usage

### First Launch

1. Run `LlamaPhone.exe` or install via the installer
2. Wait for the boot animation (splash screen)
3. The main window will appear with the TV-styled interface

### Connecting a Device

1. **Enable USB Debugging** on your Android device:
   - Settings → About Phone → Tap "Build Number" 7 times
   - Settings → Developer Options → Enable "USB Debugging"

2. **Connect via USB** or **WiFi**:
   ```
   USB: Just plug in the cable
   WiFi: adb connect 192.168.1.100:5555
   ```

3. **Verify Connection**:
   - Check the status bar in LlamaPhone
   - Use the "Connect" tab to scan for devices

### AI Assistant

The AI terminal understands natural language:

```
You: How do I unlock the bootloader on a Samsung?
AI:  Bootloader Unlock Guide for Samsung:
     1. Enable Developer Options
     2. Settings → Developer → OEM Unlocking
     3. Boot to download mode (Power + Vol Down + Bixby)
     4. Run: fastboot flashing unlock
     ⚠️ WARNING: This will ERASE ALL DATA!
```

---

## Documentation

| Document | Description |
|----------|-------------|
| [SPEC.md](SPEC.md) | Technical specification |
| [MODELS.md](MODELS.md) | AI model setup guide |
| [CHANGELOG.md](CHANGELOG.md) | Version history |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Developer guide |

### Project Structure

```
llamaphone/
├── llamaphone.py          # Main entry point
├── llamaphone.spec        # PyInstaller spec
├── build.bat              # Windows build script
├── build.sh              # Linux/macOS build script
├── installer.iss          # Inno Setup installer script
├── ui/                    # PyQt6 interface
│   ├── splash_screen.py   # Boot animation
│   ├── main_window.py     # Main TV window
│   ├── terminal_screen.py # AI chat
│   ├── control_panel.py   # Knobs & buttons
│   └── styles.py          # CRT styling
├── ai/                    # AI integration
│   ├── ollama_client.py   # Ollama API
│   └── tools/             # ADB/Fastboot tools
├── modules/               # Feature modules
│   ├── bypass.py          # FRP/unlock
│   ├── exploits.py         # Exploit DB
│   └── drivers.py         # Driver DB
└── core/                  # Utilities
    ├── auth.py            # OAuth2
    ├── config.py          # Settings
    └── logger.py          # Audit log
```

---

## Security

- **Local Processing**: All AI processing happens on your machine
- **Command Validation**: Dangerous commands require confirmation
- **Audit Logging**: All operations are logged
- **No Data Exfiltration**: No network requests except to local Ollama

### Disclaimer

LlamaPhone is intended for:
- Mobile repair technicians
- Device owners repairing their own devices
- Educational purposes

**Do NOT use for:**
- Unauthorized access to devices
- Bypassing security on stolen devices
- Any illegal activities

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Demo

```
╔══════════════════════════════════════════════════════════╗
║  LLAMAPHONE SYSTEMS v1.0.0                             ║
║  ┌──────────────────────────────────────────────────┐   ║
║  │ > Connect device via USB or WiFi                  │   ║
║  │ > Type commands or chat with AI assistant        │   ║
║  │ > Bypass FRP, unlock bootloaders, root devices  │   ║
║  │ > Access exploit database and driver library     │   ║
║  └──────────────────────────────────────────────────┘   ║
║  [VU] ████████████░░░░ [POWER] [CH] [VOL]           ║
╚══════════════════════════════════════════════════════════╝
```

---

<div align="center">

**Built with ❤️ for mobile repair technicians**

📺 *Model: LP-3000 TUBE* • 🔧 *Powered by Ollama AI*

[![Star on GitHub](https://img.shields.io/github/stars/sonamcgoo-dev/llamaphone?style=social)](https://github.com/sonamcgoo-dev/llamaphone)

</div>