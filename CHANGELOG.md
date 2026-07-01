# Changelog

All notable changes to LlamaPhone will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-06-30

### Added

- **🎉 Pre-built Windows Installer**: Download and install with one click
- **🤖 GitHub Actions CI/CD**: Automatic builds on every release
- **📦 Single-file Executable**: Clean, portable .exe file

### Features

- **Retro CRT TV Interface**: Full PyQt6-based UI with phosphor green/amber colors, scanlines, and vignette effects
- **AI Terminal**: Chat interface powered by local Ollama LLM with natural language processing
- **Splash Screen**: Animated boot sequence with credits and VU meter
- **10 Module Tabs**: Terminal, Bypass, Connect, ADB, Sideload, Fastboot, Bootloader, Download, Root, Exploits
- **ADB Tools**: Complete ADB command wrapper for device connection and management
- **Fastboot Tools**: Fastboot command wrapper for bootloader operations
- **Device Discovery**: Network scanning for hidden devices and port scanning
- **Bypass Module**: FRP bypass, screen lock, and network unlock guides
- **Exploit Database**: Knowledge base of known exploits organized by category and device
- **Driver Database**: SQLite database of 5000+ device drivers
- **OAuth2 Simulation**: Session management and command validation
- **Audit Logging**: Complete logging of all operations for security

### Dependencies

- Python 3.10+
- PyQt6 6.4.0+
- httpx 0.24.0+
- Ollama (for AI features)
- Android SDK Platform Tools (for ADB/Fastboot)

---

## Version History

| Version | Date | Status |
|---------|------|--------|
| 1.0.0 | 2024-06-30 | Current - Pre-built installer available |
| 0.1.0 | 2024-00-00 | Initial |
