# LlamaPhone

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-00AAFF?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-FFB000?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-FF3333?style=for-the-badge)

**AI-Powered Mobile Repair Console**

*A retro CRT TV-styled desktop application for mobile device repair technicians*

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Documentation](#documentation) • [Contributing](#contributing)

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
git clone https://github.com/llamaphone/llamaphone.git
cd llamaphone

# Install dependencies
pip install -r requirements.txt

# Download AI model (recommended)
ollama pull qwen2.5-coder:7b

# Run the application
python llamaphone.py
```

### Windows Executable

Download the pre-built executable from the releases page:

```
dist/LlamaPhone/LlamaPhone.exe
```

Or build your own:

```bash
# On Windows
build.bat

# On Linux/macOS
chmod +x build.sh
./build.sh
```

---

## Usage

### First Launch

1. Run `llamaphone.py` or the Windows executable
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

### Script Generation

```
You: Write a script to install multiple APKs
AI:  Here's a Python script:
     ```python
     import subprocess
     import os
     
     def install_apks(folder_path):
         for apk in os.listdir(folder_path):
             if apk.endswith('.apk'):
                 subprocess.run(['adb', 'install', '-r', apk])
     ```
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
│   ├── exploits.py        # Exploit DB
│   └── drivers.py         # Driver DB
└── core/                  # Utilities
    ├── auth.py            # OAuth2
    ├── config.py          # Settings
    └── logger.py          # Audit log
```

---

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Fork and clone
git clone https://github.com/YOUR_NAME/llamaphone.git
cd llamaphone

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate   # Windows

# Install in development mode
pip install -e ".[dev]"

# Run linting
ruff check .

# Run the app
python llamaphone.py
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

## Credits

| Component | Technology |
|-----------|------------|
| **GUI Framework** | PyQt6 |
| **AI Engine** | Ollama |
| **AI Model** | Qwen2.5-Coder |
| **ADB Bridge** | adbutils |
| **Design** | Retro CRT Tube Aesthetics |

---

*Model: LP-3000 TUBE*
