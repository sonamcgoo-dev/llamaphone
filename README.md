# 📺 LlamaPhone

<div align="center">

[![GitHub release](https://img.shields.io/github/v/release/sonamcgoo-dev/llamaphone?style=for-the-badge&color=33FF33)](https://github.com/sonamcgoo-dev/llamaphone/releases)
[![Python](https://img.shields.io/badge/Python-3.10+-00AAFF?style=for-the-badge)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-FFB000?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-FF3333?style=for-the-badge)](https://github.com/sonamcgoo-dev/llamaphone/actions)

### 🤖 AI-Powered Mobile Repair Console

*A retro CRT TV-styled desktop application for mobile device repair technicians*

**[📦 Download Installer](https://github.com/sonamcgoo-dev/llamaphone/releases)** • **[Features](#features)** • **[Documentation](#documentation)**

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
| Ollama | Latest | Auto-installed on Windows during onboarding (winget) |
| ADB | Latest | Auto-installed on Windows during onboarding (Platform Tools) |

### Quick Install (Windows)

```bash
# Clone the repository
git clone https://github.com/sonamcgoo-dev/llamaphone.git
cd llamaphone

# Full onboarding (installs Python deps, ADB, Ollama, and pulls default model)
install.bat

# Run the application
python llamaphone.py
```

### Quick Install (Cross-platform)

```bash
python onboarding.py
python llamaphone.py
```

Onboarding now prints live install output and **model download progress lines** during `ollama pull`, so you can see that dependency setup and model download are actively running.

---

## Downloads

### Pre-built Installer (Recommended)

📦 **Download from Releases:**
👉 **[https://github.com/sonamcgoo-dev/llamaphone/releases](https://github.com/sonamcgoo-dev/llamaphone/releases)**

Simply download `LlamaPhone_Setup_1.0.0.exe` and run it!

### Build Options

| Method | Description |
|--------|-------------|
| **GitHub Actions** | Push tag → auto-builds .exe + installer |
| **Build Script** | Run `build.bat` locally (packs Python runtime dependencies and bundled assets into `dist\LlamaPhone.exe`) |

### Build from Source

```bash
# Clone repository
git clone https://github.com/sonamcgoo-dev/llamaphone.git
cd llamaphone

# Full onboarding first
python onboarding.py

# Run
python llamaphone.py

# Or build .exe
build.bat
```

### GitHub Actions Auto-Build

Every release automatically creates:
- `dist\LlamaPhone.exe` - Portable executable
- `installer\LlamaPhone_Setup_X.X.X.exe` - Windows installer

**To trigger a build:**
```bash
git tag v1.0.1
git push origin v1.0.1
```

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
├── onboarding.py          # Full onboarding (deps + tools + model pull)
├── setup.py               # Packaging metadata entry point
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