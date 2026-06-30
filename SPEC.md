# LlamaPhone - AI-Powered Mobile Repair Console

## Project Overview

**Project Name:** LlamaPhone  
**Type:** Desktop Application (Standalone PC Software)  
**Core Functionality:** A local AI-powered toolkit for mobile device repair technicians, featuring an ADB bridge, device diagnostics, exploit database, and script generation—all wrapped in a nostalgic retro CRT TV aesthetic.  
**Target Users:** Mobile repair technicians, custom ROM flashers, bootloader unlock enthusiasts, and Android diagnostics professionals.

---

## Technical Stack

| Component | Technology |
|-----------|------------|
| **Frontend** | PyQt6 with custom CSS for retro CRT effects |
| **Backend** | Python 3.10+ |
| **AI Engine** | Ollama (local LLM) with Qwen2.5-Coder-7B |
| **ADB Bridge** | adbutils + uiautomator2 |
| **Fastboot** | subprocess wrapper around fastboot binary |
| **Security** | OAuth2 simulation for session management |
| **Driver DB** | SQLite with vendor chipset database |
| **Exploits** | Encrypted local JSON knowledge base |

---

## AI Model Selection & Import

### Recommended Model: **Qwen2.5-Coder-7B-Instruct-GGUF**

| Criteria | Rating |
|----------|--------|
| Code Generation | ⭐⭐⭐⭐⭐ Excellent |
| Function Calling | ⭐⭐⭐⭐⭐ Native support |
| Tool Use | ⭐⭐⭐⭐⭐ Optimized |
| Quantization Quality | ⭐⭐⭐⭐⭐ Q4_K_M ideal |
| Context Window | 128K tokens |
| License | Apache 2.0 (commercial OK) |

### Why Qwen2.5-Coder?
- Trained specifically on code generation tasks
- Native function calling support via Qwen-Agent framework
- Excellent Python + shell command generation for ADB scripts
- Small enough for consumer GPUs (7B) while maintaining quality

### Import Process

```bash
# 1. Download GGUF model
wget https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct-GGUF/resolve/main/qwen2.5-coder-7b-instruct-q4_k_m.gguf

# 2. Create Ollama Modelfile
cat > Modelfile << 'EOF'
FROM ./qwen2.5-coder-7b-instruct-q4_k_m.gguf
TEMPLATE """{{ if .System }}{{ .System }}\n{{ end }}{{ .Prompt }}
"""
PARAMETER num_ctx 4096
PARAMETER temperature 0.7
EOF

# 3. Import to Ollama
ollama create llamaphone-ai -f Modelfile
ollama run llamaphone-ai "Hello"
```

---

## UI Design: Retro CRT TV Aesthetic

### Overall Visual Theme
- **Chassis:** Dark gray/beige plastic TV cabinet (1980s style)
- **Screen:** Curved CRT glass with phosphor glow effect
- **Controls:** Physical knob and button styling
- **Typography:** Monospace terminal font with scanlines

### Window Structure

```
┌─────────────────────────────────────────────────────────────────┐
│  ┌──────────────┐  ┌────────────────────────────────────────┐  │
│  │   [KNOB]     │  │                                        │  │
│  │   CHANNEL    │  │         MAIN SCREEN / TERMINAL          │  │
│  │   [KNOB]     │  │                                        │  │
│  │──────────────│  │   (AI Chat, Command Output,             │  │
│  │  [BUTTON]    │  │    Device Status, Logs)                 │  │
│  │   BYPASS     │  │                                        │  │
│  │  [BUTTON]    │  │                                        │  │
│  │   CONNECT    │  │                                        │  │
│  │  [BUTTON]    │  │                                        │  │
│  │    ADB       │  ├────────────────────────────────────────┤  │
│  │  [BUTTON]    │  │   > COMMAND INPUT BAR ___________[⏎]   │  │
│  │   SIDELOAD   │  └────────────────────────────────────────┘  │
│  │  [BUTTON]    │                                               │
│  │  FASTBOOT    │  ┌────────────────────────────────────────┐  │
│  │  [BUTTON]    │  │  STATUS BAR: Device │ Model │ Status  │  │
│  │ BOOTLOADER   │  └────────────────────────────────────────┘  │
│  │  [BUTTON]    │                                               │
│  │  DOWNLOAD    │         ╔══════════════════════════╗         │
│  │  [BUTTON]    │         ║   VU METER / SIGNAL      ║         │
│  │    ROOT      │         ╚══════════════════════════╝         │
│  │  [BUTTON]    │                                               │
│  │   EXPLOITS   │  ┌────────────────────────────────────────┐  │
│  │  [BUTTON]    │  │  🔊 SYSTEM: AI Ready | ADB Connected    │  │
│  │   SETTINGS   │  └────────────────────────────────────────┘  │
│  │              │                                               │
│  │   [KNOB]     │   ┌────────────────────────────────────────┐  │
│  │   VOLUME     │   │  📋 Recent Commands Log (scrolling)   │  │
│  │   [KNOB]     │   └────────────────────────────────────────┘  │
│  └──────────────┘                                               │
└─────────────────────────────────────────────────────────────────┘
```

### Color Palette

| Role | Color | Hex |
|------|-------|-----|
| CRT Phosphor Green | Terminal text | `#33FF33` |
| CRT Amber | Secondary text | `#FFB000` |
| CRT Blue | Links/highlights | `#00AAFF` |
| CRT Red | Errors/alerts | `#FF3333` |
| Cabinet Dark | Frame | `#2A2A2A` |
| Cabinet Light | Highlights | `#4A4A4A` |
| Screen Black | Background | `#0D0D0D` |
| Scanline Overlay | Effects | `rgba(0,0,0,0.3)` |

### Visual Effects

- **CRT Curvature:** CSS border-radius with perspective transform
- **Scanlines:** Repeating linear gradient overlay
- **Phosphor Glow:** text-shadow with green blur
- **Screen Flicker:** Subtle opacity animation (0.98-1.0)
- **Vignette:** Radial gradient darkening at edges
- **RGB Shift:** Subtle chromatic aberration on edges

---

## Core Features

### 1. AI Terminal (Main Screen)
- Chat interface with local AI assistant
- Natural language commands → ADB/fastboot execution
- Script generation (Python, shell, batch)
- Context-aware suggestions

### 2. Bypass/Unlock Module
- FRP bypass automation
- Pattern/PIN lock removal (via exploits)
- Network lock bypass
- Bootloader unlock assistant

### 3. Device Connection Hub
- ADB over WiFi/USB
- Port scanning for devices
- Hidden device finder
- Device pairing assistant

### 4. ADB Command Center
- Quick command buttons
- Shell access
- File manager (push/pull)
- App installation (sideload)
- Logcat viewer

### 5. Fastboot/Bootloader
- Flash partitions
- Unlock/lock bootloader
- Boot image injection
- Device info readout

### 6. Download Mode
- Samsung ODIN mode detection
- Qualcomm EDL detection
- Mediatek SP Flash Tool mode
- Firmware flashing interface

### 7. Root Access
- Shizuku integration guide
- Magisk installation
- Root verification
- Systemless root options

### 8. Exploit Database
- Known exploits by device model
- Step-by-step procedures
- Security notes
- Success rate indicators

### 9. Driver Database
- 5000+ device/driver combinations
- Auto-fetch from vendor servers
- Manual download links
- Chipset database

---

## Security Architecture

### OAuth2 Simulation Flow
```
┌──────────┐     ┌──────────┐     ┌──────────┐
│  Client  │────>│  Auth    │────>│  Local   │
│  App     │<────│  Server  │<────│  Token   │
└──────────┘     └──────────┘     └──────────┘
     │                               │
     └─────────── JWT Token ──────────┘
```

### Security Features
- **Local OAuth:** Simulated OAuth2 server for session tokens
- **Command Whitelist:** Approved ADB commands only
- **Audit Log:** All operations logged with timestamps
- **Confirmation Dialogs:** Destructive operations require confirmation
- **Sandboxed Execution:** Commands run in controlled environment

---

## File Structure

```
llamaphone/
├── llamaphone.py              # Main entry point
├── ui/
│   ├── main_window.py         # Main window with TV frame
│   ├── terminal_screen.py     # AI chat / terminal
│   ├── control_panel.py       # Knobs and buttons
│   ├── styles.py              # Retro CSS styling
│   └── effects.py             # CRT visual effects
├── ai/
│   ├── ollama_client.py       # Ollama API wrapper
│   ├── tools/
│   │   ├── adb_tools.py       # ADB command wrappers
│   │   ├── fastboot_tools.py  # Fastboot wrappers
│   │   └── device_tools.py    # Device detection
│   └── prompts.py             # System prompts
├── modules/
│   ├── bypass.py               # Bypass/unlock logic
│   ├── exploits.py            # Exploit database
│   ├── drivers.py             # Driver management
│   └── connection.py           # Connection manager
├── data/
│   ├── exploits.json          # Encrypted exploit DB
│   ├── drivers.db             # SQLite driver DB
│   └── settings.json           # App configuration
├── core/
│   ├── auth.py                 # OAuth2 simulation
│   ├── logger.py               # Audit logging
│   └── config.py               # Configuration
└── assets/
    ├── sounds/                 # TV sound effects
    └── fonts/                  # Retro fonts
```

---

## Installation & Setup

### Prerequisites
```bash
# Python 3.10+
python --version

# Ollama installed
ollama --version

# Android SDK platform-tools (ADB)
# Download from: https://developer.android.com/studio/releases/platform-tools
```

### Installation Steps
```bash
# 1. Clone/install llamaphone
pip install llamaphone

# 2. Download AI model
llamaphone download-model

# 3. Detect/setup ADB
llamaphone setup-adb

# 4. Launch
llamaphone
```

---

## Splash Screen Features

### Boot Animation
The splash screen features a CRT TV boot sequence:
- Phosphor green text with glow effects
- Animated boot messages scrolling
- Progress bar with gradient fill
- VU meter animation

### Credits Display
The splash screen includes:
- Lead Developer: LlamaPhone Team
- AI Integration: Ollama • Qwen2.5-Coder
- ADB Bridge: adbutils • uiautomator2
- Design: Retro CRT Tube Aesthetics

### Boot Sequence Messages
```
LLAMAPHONE SYSTEMS v1.0.0
INITIALIZING CRT DISPLAY...
LOADING PHOSPHOR ARRAYS...
CALIBRATING SCANLINES...
DETECTING ADB SERVICES...
CONNECTING TO OLLAMA AI...
LOADING EXPLOIT DATABASE...
INITIALIZING SECURITY LAYER...
WARMING UP VACUUM TUBES...
ALL SYSTEMS NOMINAL
>>> READY <<<
```

---

## Success Metrics

- ✅ Local AI responds within 3 seconds
- ✅ ADB commands execute reliably
- ✅ All UI elements match retro TV aesthetic
- ✅ Secure command execution with audit trail
- ✅ Works offline after initial setup

---

## Future Enhancements (Phase 2)

1. **Multi-Device Support:** Manage multiple devices simultaneously
2. **Script Library:** Community-contributed repair scripts
3. **Remote Assist:** TeamViewer-style screen sharing
4. **Cloud Sync:** Encrypted backup of configurations
5. **AI Fine-tuning:** Custom model trained on repair data
