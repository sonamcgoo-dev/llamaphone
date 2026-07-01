"""
LlamaPhone - Main Window
Retro CRT TV-styled main application window
"""

import shlex
import socket
import subprocess

from PyQt6.QtCore import QTimer, pyqtSignal
from PyQt6.QtGui import QAction, QColor, QPainter, QPen
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QStatusBar,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from .control_panel import ControlPanel
from .styles import get_crt_stylesheet
from .terminal_screen import TerminalScreen


class MainWindow(QMainWindow):
    """Main window styled as a retro CRT TV."""

    # Signals
    device_connected = pyqtSignal(str)
    command_executed = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_device = None
        self.ai_ready = False
        self.adb_connected = False

        self.init_ui()
        self.setup_menus()
        self.start_status_updates()

    def init_ui(self):
        """Initialize the main UI."""
        self.setWindowTitle("LlamaPhone - AI Mobile Repair Console")
        self.setWindowIcon(QApplication.windowIcon())
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)

        # Apply stylesheet
        self.setStyleSheet(get_crt_stylesheet())

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)

        # Left side - TV Control Panel
        self.control_panel = ControlPanel(self)
        self.control_panel.setFixedWidth(180)
        main_layout.addWidget(self.control_panel)

        # Right side - TV Screen Area
        screen_container = self.create_screen_area()
        main_layout.addWidget(screen_container, 1)

        # Bottom - Status Bar Area
        self.create_status_bar()

        # Connect signals
        self.control_panel.module_selected.connect(self.on_module_selected)

    def create_screen_area(self):
        """Create the main screen area."""
        # Container frame
        container = QFrame()
        container.setObjectName("tvFrame")

        # Layout
        layout = QVBoxLayout(container)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # CRT Screen with tabs
        self.screen_tabs = QTabWidget()
        self.screen_tabs.setObjectName("crtScreen")
        self.screen_tabs.setStyleSheet("""
            QTabWidget#crtScreen {
                background-color: #0D0D0D;
                border-radius: 10px;
            }
        """)

        # Terminal/AI Screen
        self.terminal_screen = TerminalScreen(self)
        self.screen_tabs.addTab(self.terminal_screen, "🤖 AI TERMINAL")

        # Bypass Module
        self.bypass_screen = self.create_bypass_screen()
        self.screen_tabs.addTab(self.bypass_screen, "🔓 BYPASS/UNLOCK")

        # Connection Screen
        self.connection_screen = self.create_connection_screen()
        self.screen_tabs.addTab(self.connection_screen, "📡 CONNECT")

        # ADB Screen
        self.adb_screen = self.create_adb_screen()
        self.screen_tabs.addTab(self.adb_screen, "💻 ADB COMMANDS")

        # Fastboot Screen
        self.fastboot_screen = self.create_fastboot_screen()
        self.screen_tabs.addTab(self.fastboot_screen, "⚡ FASTBOOT")

        # Bootloader Screen
        self.bootloader_screen = self.create_bootloader_screen()
        self.screen_tabs.addTab(self.bootloader_screen, "🔧 BOOTLOADER")

        # Download Mode Screen
        self.download_screen = self.create_download_screen()
        self.screen_tabs.addTab(self.download_screen, "📥 DOWNLOAD MODE")

        # Root Screen
        self.root_screen = self.create_root_screen()
        self.screen_tabs.addTab(self.root_screen, "👑 ROOT ACCESS")

        # Exploits Screen
        self.exploits_screen = self.create_exploits_screen()
        self.screen_tabs.addTab(self.exploits_screen, "💣 EXPLOITS")

        # Settings Screen
        self.settings_screen = self.create_settings_screen()
        self.screen_tabs.addTab(self.settings_screen, "⚙️ SETTINGS")

        layout.addWidget(self.screen_tabs, 1)

        # VU Meter decoration
        vu_layout = QHBoxLayout()
        vu_layout.addStretch()

        vu_label = QLabel("🔊 SIGNAL")
        vu_label.setStyleSheet("color: #666666; font-size: 10px;")
        vu_layout.addWidget(vu_label)

        self.vu_bar = QProgressBar()
        self.vu_bar.setFixedSize(100, 10)
        self.vu_bar.setTextVisible(False)
        self.vu_bar.setStyleSheet("""
            QProgressBar {
                background-color: #1A1A1A;
                border: 1px solid #333;
                border-radius: 3px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #33FF33, stop:0.5 #00FF00, stop:1 #33FF33);
            }
        """)
        vu_layout.addWidget(self.vu_bar)

        layout.addLayout(vu_layout)

        return container

    def create_bypass_screen(self):
        """Create the bypass/unlock module screen."""
        screen = QWidget()
        layout = QVBoxLayout(screen)

        # Header
        header = QLabel("BYPASS & UNLOCK MODULE")
        header.setStyleSheet("""
            color: #FFB000;
            font-size: 16px;
            font-weight: bold;
            padding: 10px;
        """)
        layout.addWidget(header)

        # Description
        desc = QLabel(
            "Bypass FRP, remove screen locks, unlock network locks, "
            "and bypass activation screens safely."
        )
        desc.setStyleSheet("color: #33FF33; padding: 5px;")
        desc.setWordWrap(True)
        layout.addWidget(desc)

        # Button grid
        button_layout = QVBoxLayout()

        buttons = [
            ("🔓 FRP Bypass", "Google Account Bypass (Factory Reset Protection)"),
            ("🎯 Pattern/PIN Remove", "Remove screen lock without data loss"),
            ("📶 Network Unlock", "Remove SIM/network lock"),
            ("📱 Activation Bypass", "Bypass carrier activation"),
            ("🔐 OEM Unlock", "Enable OEM unlocking in developer options"),
            ("🆘 Emergency Call", "Access emergency dialer bypass"),
        ]

        for emoji_title, tooltip in buttons:
            btn = QPushButton(emoji_title)
            btn.setToolTip(tooltip)
            btn.setMinimumHeight(45)
            btn.clicked.connect(lambda checked, b=emoji_title: self.on_bypass_click(b))
            button_layout.addWidget(btn)

        layout.addLayout(button_layout)
        layout.addStretch()

        return screen

    def create_connection_screen(self):
        """Create the device connection screen."""
        screen = QWidget()
        layout = QVBoxLayout(screen)

        # Header
        header = QLabel("DEVICE CONNECTION HUB")
        header.setStyleSheet("""
            color: #FFB000;
            font-size: 16px;
            font-weight: bold;
            padding: 10px;
        """)
        layout.addWidget(header)

        # Connection type selector
        conn_type_layout = QHBoxLayout()
        conn_type_label = QLabel("Connection Type:")
        conn_type_label.setStyleSheet("color: #33FF33;")

        from PyQt6.QtWidgets import QComboBox
        self.conn_type_combo = QComboBox()
        self.conn_type_combo.addItems(["USB", "WiFi", "Bluetooth", "TCP/IP"])
        conn_type_layout.addWidget(conn_type_label)
        conn_type_layout.addWidget(self.conn_type_combo)
        conn_type_layout.addStretch()

        layout.addLayout(conn_type_layout)

        # Device list
        device_group = QGroupBox("Detected Devices")
        device_layout = QVBoxLayout()

        self.device_list = QTextEdit()
        self.device_list.setMaximumHeight(150)
        self.device_list.setPlaceholderText("No devices detected...")
        device_layout.addWidget(self.device_list)

        device_group.setLayout(device_layout)
        layout.addWidget(device_group)

        # Connection buttons
        btn_layout = QHBoxLayout()

        scan_btn = QPushButton("🔍 Scan for Devices")
        scan_btn.clicked.connect(self.scan_devices)
        btn_layout.addWidget(scan_btn)

        connect_btn = QPushButton("📡 Connect")
        connect_btn.clicked.connect(self.connect_device)
        btn_layout.addWidget(connect_btn)

        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.refresh_devices)
        btn_layout.addWidget(refresh_btn)

        layout.addLayout(btn_layout)

        # Port scanner section
        port_group = QGroupBox("Port Scanner")
        port_layout = QVBoxLayout()

        port_input_layout = QHBoxLayout()
        port_input_label = QLabel("IP Address:")
        self.port_ip_input = QLineEdit()
        self.port_ip_input.setPlaceholderText("192.168.1.100")
        port_scan_btn = QPushButton("Scan")
        port_scan_btn.clicked.connect(self.scan_ports)

        port_input_layout.addWidget(port_input_label)
        port_input_layout.addWidget(self.port_ip_input)
        port_input_layout.addWidget(port_scan_btn)
        port_layout.addLayout(port_input_layout)

        self.port_results = QTextEdit()
        self.port_results.setMaximumHeight(100)
        port_layout.addWidget(self.port_results)

        port_group.setLayout(port_layout)
        layout.addWidget(port_group)

        layout.addStretch()

        return screen

    def create_adb_screen(self):
        """Create the ADB commands screen."""
        screen = QWidget()
        layout = QVBoxLayout(screen)

        # Header
        header = QLabel("ADB COMMAND CENTER")
        header.setStyleSheet("""
            color: #FFB000;
            font-size: 16px;
            font-weight: bold;
            padding: 10px;
        """)
        layout.addWidget(header)

        # Quick commands
        quick_group = QGroupBox("Quick Commands")
        quick_layout = QVBoxLayout()

        commands = [
            ("devices", "List connected devices"),
            ("shell", "Open shell session"),
            ("logcat", "View device logs"),
            ("install", "Install APK"),
            ("uninstall", "Uninstall app"),
            ("push", "Push file to device"),
            ("pull", "Pull file from device"),
            ("reboot", "Reboot device"),
        ]

        for cmd, desc in commands:
            btn = QPushButton(f"$ adb {cmd}")
            btn.setToolTip(desc)
            btn.setMinimumHeight(35)
            btn.clicked.connect(lambda checked, c=cmd: self.execute_adb_command(c))
            quick_layout.addWidget(btn)

        quick_group.setLayout(quick_layout)
        layout.addWidget(quick_group)

        # Custom command input
        custom_group = QGroupBox("Custom Command")
        custom_layout = QHBoxLayout()

        self.adb_command_input = QLineEdit()
        self.adb_command_input.setPlaceholderText("Enter custom ADB command...")
        execute_btn = QPushButton("▶ EXECUTE")
        execute_btn.clicked.connect(self.execute_custom_adb)

        custom_layout.addWidget(self.adb_command_input)
        custom_layout.addWidget(execute_btn)

        custom_group.setLayout(custom_layout)
        layout.addWidget(custom_group)

        # Output area
        self.adb_output = QTextEdit()
        self.adb_output.setPlaceholderText("Command output will appear here...")
        layout.addWidget(self.adb_output, 1)

        return screen

    def create_fastboot_screen(self):
        """Create the Fastboot screen."""
        screen = QWidget()
        layout = QVBoxLayout(screen)

        header = QLabel("⚡ FASTBOOT MODE")
        header.setStyleSheet("""
            color: #FFB000;
            font-size: 16px;
            font-weight: bold;
            padding: 10px;
        """)
        layout.addWidget(header)

        desc = QLabel("Flash partitions, unlock/lock bootloader, and manage device firmware.")
        desc.setStyleSheet("color: #33FF33;")
        desc.setWordWrap(True)
        layout.addWidget(desc)

        # Fastboot commands
        fb_commands = [
            ("devices", "List devices in fastboot mode"),
            ("unlock", "Unlock bootloader (WIPES DATA)"),
            ("lock", "Lock bootloader"),
            ("flashing unlock", "Enable flashing (Samsung)"),
            ("oem unlock", "OEM unlock command"),
            ("reboot", "Reboot from fastboot"),
            ("recovery", "Boot to recovery"),
            ("bootloader", "Boot to bootloader"),
        ]

        for cmd, desc in fb_commands:
            btn = QPushButton(f"fastboot {cmd}")
            btn.setToolTip(desc)
            btn.setMinimumHeight(40)
            btn.clicked.connect(lambda checked, c=cmd: self.execute_fastboot(c))
            layout.addWidget(btn)

        # Flash partition section
        flash_group = QGroupBox("Flash Partition Image")
        flash_layout = QVBoxLayout()

        flash_layout.addWidget(QLabel("Select image file:"))

        flash_input_layout = QHBoxLayout()
        self.flash_file_input = QLineEdit()
        self.flash_file_input.setPlaceholderText("/path/to/image.img")
        browse_btn = QPushButton("📁 Browse")
        browse_btn.clicked.connect(lambda: self.browse_flash_file())
        flash_input_layout.addWidget(self.flash_file_input)
        flash_input_layout.addWidget(browse_btn)
        flash_layout.addLayout(flash_input_layout)

        partition_layout = QHBoxLayout()
        partition_layout.addWidget(QLabel("Partition:"))
        self.partition_combo = QComboBox()
        self.partition_combo.addItems([
            "boot", "recovery", "system", "vendor",
            "userdata", "radio", "abl", "aop", "custom"
        ])
        partition_layout.addWidget(self.partition_combo)
        flash_layout.addLayout(partition_layout)

        flash_btn = QPushButton("🔥 FLASH")
        flash_btn.setMinimumHeight(45)
        flash_btn.clicked.connect(self.flash_partition)
        flash_layout.addWidget(flash_btn)

        flash_group.setLayout(flash_layout)
        layout.addWidget(flash_group)

        layout.addStretch()

        return screen

    def create_bootloader_screen(self):
        """Create the Bootloader screen."""
        screen = QWidget()
        layout = QVBoxLayout(screen)

        header = QLabel("🔧 BOOTLOADER MANAGEMENT")
        header.setStyleSheet("""
            color: #FFB000;
            font-size: 16px;
            font-weight: bold;
            padding: 10px;
        """)
        layout.addWidget(header)

        # Status
        status_group = QGroupBox("Bootloader Status")
        status_layout = QVBoxLayout()
        self.bootloader_status = QLabel("Unknown - Connect a device")
        self.bootloader_status.setStyleSheet("color: #33FF33; font-size: 14px;")
        status_layout.addWidget(self.bootloader_status)
        status_group.setLayout(status_layout)
        layout.addWidget(status_group)

        # Operations
        operations = [
            ("Check Status", "Check current bootloader state"),
            ("Unlock Bootloader", "Unlock device bootloader (ERASES ALL DATA)"),
            ("Lock Bootloader", "Lock bootloader to stock"),
            ("Flash Custom Recovery", "Install TWRP or other custom recovery"),
            ("Patch Boot Image", "Patch AVB for custom ROM support"),
            ("Check OEM Info", "Display OEM and device info"),
        ]

        for title, tooltip in operations:
            btn = QPushButton(title)
            btn.setToolTip(tooltip)
            btn.setMinimumHeight(40)
            layout.addWidget(btn)

        layout.addStretch()

        return screen

    def create_download_screen(self):
        """Create the Download Mode screen."""
        screen = QWidget()
        layout = QVBoxLayout(screen)

        header = QLabel("📥 DOWNLOAD MODE")
        header.setStyleSheet("""
            color: #FFB000;
            font-size: 16px;
            font-weight: bold;
            padding: 10px;
        """)
        layout.addWidget(header)

        # Download mode types
        modes_group = QGroupBox("Download Mode Types")
        modes_layout = QVBoxLayout()

        modes = [
            ("Samsung ODIN", "Samsung devices - use Odin/flashtool"),
            ("Qualcomm EDL", "Emergency Download Mode - 9008 port"),
            ("MediaTek SP Flash", "MTK devices - use SP Flash Tool"),
            ("Qualcomm 9008", "Deep EDL - raw programmer mode"),
            ("Huawei eRecovery", "Huawei emergency recovery"),
            ("Xiaomi Fastboot", "Xiaomi EDL/dump mode"),
        ]

        for mode, desc in modes:
            btn = QPushButton(f"📱 {mode}")
            btn.setToolTip(desc)
            btn.setMinimumHeight(40)
            modes_layout.addWidget(btn)

        modes_group.setLayout(modes_layout)
        layout.addWidget(modes_group)

        # Firmware flashing
        fw_group = QGroupBox("Firmware Operations")
        fw_layout = QVBoxLayout()

        fw_layout.addWidget(QLabel("Firmware File:"))
        fw_input = QLineEdit()
        fw_input.setPlaceholderText("Select firmware package...")
        fw_layout.addWidget(fw_input)

        fw_btn = QPushButton("📥 Flash Firmware")
        fw_btn.setMinimumHeight(45)
        fw_layout.addWidget(fw_btn)

        fw_group.setLayout(fw_layout)
        layout.addWidget(fw_group)

        layout.addStretch()

        return screen

    def create_root_screen(self):
        """Create the Root Access screen."""
        screen = QWidget()
        layout = QVBoxLayout(screen)

        header = QLabel("👑 ROOT ACCESS")
        header.setStyleSheet("""
            color: #FFB000;
            font-size: 16px;
            font-weight: bold;
            padding: 10px;
        """)
        layout.addWidget(header)

        # Root methods
        root_group = QGroupBox("Root Methods")
        root_layout = QVBoxLayout()

        methods = [
            ("Magisk (Recommended)", "Systemless root via custom boot image"),
            ("SuperSU", "Traditional root with su binary"),
            ("Shizuku", "Root via ADB for app-level root access"),
            ("KernelSU", "Root integrated into kernel"),
            ("APatch", "Kernel patcher with APM (Android Patch Module)"),
        ]

        for method, desc in methods:
            btn = QPushButton(f"✓ {method}")
            btn.setToolTip(desc)
            btn.setMinimumHeight(40)
            root_layout.addWidget(btn)

        root_group.setLayout(root_layout)
        layout.addWidget(root_group)

        # Shizuku setup guide
        shizuku_group = QGroupBox("Shizuku Setup Guide")
        shizuku_layout = QVBoxLayout()

        steps = [
            "1. Download Shizuku APK from GitHub",
            "2. Enable Developer Options & USB Debugging",
            "3. Connect device via USB",
            "4. Click 'Start' to grant ADB permissions",
            "5. Copy the displayed commands to terminal",
        ]

        for step in steps:
            label = QLabel(step)
            label.setStyleSheet("color: #33FF33; padding: 3px;")
            shizuku_layout.addWidget(label)

        shizuku_group.setLayout(shizuku_layout)
        layout.addWidget(shizuku_group)

        layout.addStretch()

        return screen

    def create_exploits_screen(self):
        """Create the Exploits database screen."""
        screen = QWidget()
        layout = QVBoxLayout(screen)

        header = QLabel("💣 EXPLOIT DATABASE")
        header.setStyleSheet("""
            color: #FFB000;
            font-size: 16px;
            font-weight: bold;
            padding: 10px;
        """)
        layout.addWidget(header)

        # Search
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("🔍 Search:"))
        self.exploit_search = QLineEdit()
        self.exploit_search.setPlaceholderText("Search exploits by device or CVE...")
        search_btn = QPushButton("Search")
        search_layout.addWidget(self.exploit_search)
        search_layout.addWidget(search_btn)
        layout.addLayout(search_layout)

        # Exploit categories
        categories_group = QGroupBox("Categories")
        categories_layout = QVBoxLayout()

        categories = [
            "🔓 Bootloader Exploits",
            "📱 FRP Bypasses",
            "🔐 Lock Screen Bypasses",
            "🌐 Network Exploits",
            "⚙️ Modem Exploits",
            "💉 Privilege Escalation",
        ]

        for cat in categories:
            btn = QPushButton(cat)
            btn.setMinimumHeight(35)
            categories_layout.addWidget(btn)

        categories_group.setLayout(categories_layout)
        layout.addWidget(categories_group)

        # Exploit details
        details_group = QGroupBox("Exploit Details")
        details_layout = QVBoxLayout()
        self.exploit_details = QTextEdit()
        self.exploit_details.setMaximumHeight(150)
        self.exploit_details.setPlaceholderText(
            "Select an exploit to view details, steps, and security notes..."
        )
        details_layout.addWidget(self.exploit_details)
        details_group.setLayout(details_layout)
        layout.addWidget(details_group)

        layout.addStretch()

        return screen

    def create_settings_screen(self):
        """Create the Settings screen."""
        screen = QWidget()
        layout = QVBoxLayout(screen)

        header = QLabel("⚙️ SETTINGS")
        header.setStyleSheet("""
            color: #FFB000;
            font-size: 16px;
            font-weight: bold;
            padding: 10px;
        """)
        layout.addWidget(header)

        # AI Settings
        ai_group = QGroupBox("AI Configuration")
        ai_layout = QVBoxLayout()

        ai_layout.addWidget(QLabel("Ollama Model:"))
        self.model_combo = QComboBox()
        self.model_combo.addItems([
            "qwen2.5-coder-7b-instruct",
            "codellama:7b",
            "mistral:7b",
            "llama3:8b",
            "phi3:14b",
        ])
        ai_layout.addWidget(self.model_combo)

        self.ai_enabled_check = QPushButton("✓ AI Enabled")
        self.ai_enabled_check.setCheckable(True)
        self.ai_enabled_check.setChecked(True)
        ai_layout.addWidget(self.ai_enabled_check)

        ai_group.setLayout(ai_layout)
        layout.addWidget(ai_group)

        # ADB Settings
        adb_group = QGroupBox("ADB Configuration")
        adb_layout = QVBoxLayout()

        adb_layout.addWidget(QLabel("ADB Path:"))
        adb_path_layout = QHBoxLayout()
        self.adb_path_input = QLineEdit()
        self.adb_path_input.setText("/usr/bin/adb")
        browse_adb = QPushButton("Browse")
        adb_path_layout.addWidget(self.adb_path_input)
        adb_path_layout.addWidget(browse_adb)
        adb_layout.addLayout(adb_path_layout)

        self.wifi_mode_check = QPushButton("✓ Auto WiFi Mode")
        self.wifi_mode_check.setCheckable(True)
        self.wifi_mode_check.setChecked(True)
        adb_layout.addWidget(self.wifi_mode_check)

        adb_group.setLayout(adb_layout)
        layout.addWidget(adb_group)

        # Driver Settings
        driver_group = QGroupBox("Driver Database")
        driver_layout = QVBoxLayout()

        driver_layout.addWidget(QLabel("Driver Cache: 2,450 entries loaded"))
        update_btn = QPushButton("🔄 Update Driver Database")
        driver_layout.addWidget(update_btn)

        driver_group.setLayout(driver_layout)
        layout.addWidget(driver_group)

        # About
        about_group = QGroupBox("About")
        about_layout = QVBoxLayout()
        about_layout.addWidget(QLabel("LlamaPhone v1.0.0"))
        about_layout.addWidget(QLabel("AI-Powered Mobile Repair Console"))
        about_layout.addWidget(QLabel("Model: LP-3000 TUBE"))
        about_group.setLayout(about_layout)
        layout.addWidget(about_group)

        layout.addStretch()

        return screen

    def setup_menus(self):
        """Setup menu bar."""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("📁 File")

        new_action = QAction("New Session", self)
        new_action.setShortcut("Ctrl+N")
        file_menu.addAction(new_action)

        open_action = QAction("Open Script...", self)
        open_action.setShortcut("Ctrl+O")
        file_menu.addAction(open_action)

        save_action = QAction("Save Script...", self)
        save_action.setShortcut("Ctrl+S")
        file_menu.addAction(save_action)

        file_menu.addSeparator()

        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Device menu
        device_menu = menubar.addMenu("📱 Device")

        connect_action = QAction("Connect Device", self)
        connect_action.setShortcut("Ctrl+D")
        device_menu.addAction(connect_action)

        disconnect_action = QAction("Disconnect", self)
        device_menu.addAction(disconnect_action)

        device_menu.addSeparator()

        reboot_action = QAction("Reboot Device", self)
        device_menu.addAction(reboot_action)

        recovery_action = QAction("Reboot to Recovery", self)
        device_menu.addAction(recovery_action)

        fastboot_action = QAction("Reboot to Fastboot", self)
        device_menu.addAction(fastboot_action)

        # AI menu
        ai_menu = menubar.addMenu("🤖 AI")

        chat_action = QAction("Open AI Chat", self)
        chat_action.setShortcut("Ctrl+Shift+A")
        ai_menu.addAction(chat_action)

        generate_action = QAction("Generate Script", self)
        generate_action.setShortcut("Ctrl+G")
        ai_menu.addAction(generate_action)

        ai_menu.addSeparator()

        model_action = QAction("Change Model...", self)
        ai_menu.addAction(model_action)

        # Help menu
        help_menu = menubar.addMenu("❓ Help")

        docs_action = QAction("Documentation", self)
        help_menu.addAction(docs_action)

        about_action = QAction("About LlamaPhone", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def create_status_bar(self):
        """Create the status bar."""
        statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        # AI Status
        self.ai_status = QLabel("🤖 AI: READY")
        self.ai_status.setStyleSheet("color: #33FF33; padding: 0 10px;")
        statusbar.addWidget(self.ai_status)

        statusbar.addSeparator()

        # ADB Status
        self.adb_status = QLabel("💻 ADB: DISCONNECTED")
        self.adb_status.setStyleSheet("color: #FFB000; padding: 0 10px;")
        statusbar.addWidget(self.adb_status)

        statusbar.addSeparator()

        # Device Status
        self.device_status = QLabel("📱 Device: NONE")
        self.device_status.setStyleSheet("color: #FFB000; padding: 0 10px;")
        statusbar.addWidget(self.device_status)

        statusbar.addPermanentSeparator()

        # Model info
        model_label = QLabel("Model: qwen2.5-coder-7b")
        model_label.setStyleSheet("color: #666666; padding: 0 10px;")
        statusbar.addPermanentWidget(model_label)

        # Version
        version_label = QLabel("v1.0.0")
        version_label.setStyleSheet("color: #666666; padding: 0 10px;")
        statusbar.addPermanentWidget(version_label)

    def start_status_updates(self):
        """Start periodic status updates."""
        self.status_timer = QTimer(self)
        self.status_timer.timeout.connect(self.update_vu_meter)
        self.status_timer.start(100)

    def update_vu_meter(self):
        """Update VU meter animation."""
        import random
        level = random.randint(60, 95) if self.adb_connected else random.randint(10, 30)
        self.vu_bar.setValue(level)

    def on_module_selected(self, module_name):
        """Handle module selection from control panel."""
        # Map module names to tab indices
        module_map = {
            "bypass": 1,
            "connect": 2,
            "adb": 3,
            "sideload": 3,
            "fastboot": 4,
            "bootloader": 5,
            "download": 6,
            "root": 7,
            "exploits": 8,
            "settings": 9,
            "terminal": 0,
        }

        if module_name.lower() in module_map:
            self.screen_tabs.setCurrentIndex(module_map[module_name.lower()])

    def on_bypass_click(self, button_name):
        """Handle bypass button clicks."""
        self.terminal_screen.append_message(
            "AI Assistant",
            f"Starting {button_name} procedure. Please ensure device is connected and follow the on-screen instructions."
        )
        self.screen_tabs.setCurrentIndex(0)  # Switch to terminal

    def _run_cli(self, command: list[str], timeout: int = 30) -> tuple[int, str, str]:
        """Run a CLI command and return (returncode, stdout, stderr)."""
        result = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
        return result.returncode, result.stdout.strip(), result.stderr.strip()

    def scan_devices(self):
        """Scan for connected devices."""
        self.device_list.clear()
        self.device_list.append("Scanning for devices...")
        try:
            return_code, output, error = self._run_cli(["adb", "devices", "-l"], timeout=15)
            if return_code != 0:
                self.device_list.append(f"ADB error: {error or output}")
                self.adb_connected = False
                return

            lines = [line.strip() for line in output.splitlines()[1:] if line.strip()]
            ready = [line for line in lines if "\tdevice" in line]
            if ready:
                for entry in ready:
                    self.device_list.append(entry)
                self.current_device = ready[0].split()[0]
                self.adb_connected = True
                self.adb_status.setText("💻 ADB: CONNECTED")
                self.adb_status.setStyleSheet("color: #33FF33; padding: 0 10px;")
                self.device_status.setText(f"📱 Device: {self.current_device}")
            else:
                self.device_list.append("No ADB devices found.")
                self.current_device = None
                self.adb_connected = False
                self.adb_status.setText("💻 ADB: DISCONNECTED")
                self.adb_status.setStyleSheet("color: #FFB000; padding: 0 10px;")
                self.device_status.setText("📱 Device: NONE")
        except (subprocess.SubprocessError, FileNotFoundError) as error:
            self.device_list.append(f"Scan failed: {error}")
            self.adb_connected = False

    def connect_device(self):
        """Connect to selected device."""
        connection_type = self.conn_type_combo.currentText()
        if connection_type in {"WiFi", "TCP/IP"}:
            ip = self.port_ip_input.text().strip()
            if not ip:
                self.device_list.append("Enter an IP in the Port Scanner field first.")
                return
            target = ip if ":" in ip else f"{ip}:5555"
            return_code, output, error = self._run_cli(["adb", "connect", target], timeout=20)
            self.device_list.append(output or error or f"Connection attempt finished for {target}")
        else:
            self.device_list.append("Checking USB-connected devices...")
        self.scan_devices()

    def refresh_devices(self):
        """Refresh device list."""
        self.scan_devices()

    def scan_ports(self):
        """Scan ports on IP address."""
        ip = self.port_ip_input.text().strip()
        self.port_results.clear()
        if not ip:
            self.port_results.append("Enter an IP address.")
            return

        self.port_results.append(f"Scanning {ip}...")
        adb_ports = [5555, 5554, 5037]
        open_ports: list[int] = []
        for port in adb_ports:
            try:
                with socket.create_connection((ip, port), timeout=1.0):
                    open_ports.append(port)
            except OSError:
                continue

        if open_ports:
            self.port_results.append(f"Open ports: {', '.join(str(p) for p in open_ports)}")
        else:
            self.port_results.append("Scan complete. No open ADB ports found.")

    def execute_adb_command(self, command):
        """Execute an ADB command."""
        args = shlex.split(command, posix=False)
        if args and args[0].lower() == "adb":
            args = args[1:]
        cmd = ["adb"] + args
        self.adb_output.append(f"$ {' '.join(cmd)}")
        try:
            return_code, output, error = self._run_cli(cmd, timeout=120)
            if output:
                self.adb_output.append(output)
            if error:
                self.adb_output.append(error)
            if return_code != 0 and not output and not error:
                self.adb_output.append(f"Command failed with exit code {return_code}")
            self.terminal_screen.append_message("System", f"ADB: {' '.join(args) or 'help'}", is_ai=True)
        except (subprocess.SubprocessError, FileNotFoundError) as ex:
            self.adb_output.append(f"Execution failed: {ex}")

    def execute_custom_adb(self):
        """Execute custom ADB command."""
        cmd = self.adb_command_input.text()
        if cmd:
            self.execute_adb_command(cmd)
            self.adb_command_input.clear()

    def execute_fastboot(self, command):
        """Execute a fastboot command."""
        mapping = {
            "recovery": ["reboot", "recovery"],
            "bootloader": ["reboot-bootloader"],
            "unlock": ["oem", "unlock"],
            "lock": ["oem", "lock"],
        }
        args = mapping.get(command, shlex.split(command, posix=False))
        cmd = ["fastboot"] + args
        self.terminal_screen.append_message("System", f"$ {' '.join(cmd)}", is_ai=True)
        try:
            return_code, output, error = self._run_cli(cmd, timeout=180)
            if output:
                self.terminal_screen.append_message("Fastboot", output, is_ai=True)
            if error:
                self.terminal_screen.append_message("Fastboot", error, is_ai=True)
            if return_code != 0 and not output and not error:
                self.terminal_screen.append_message("Fastboot", f"Command failed: {return_code}", is_ai=True)
        except (subprocess.SubprocessError, FileNotFoundError) as ex:
            self.terminal_screen.append_message("Fastboot", f"Execution failed: {ex}", is_ai=True)

    def browse_flash_file(self):
        """Browse for flash file."""
        from PyQt6.QtWidgets import QFileDialog
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Image File", "", "Image Files (*.img *.bin);;All Files (*)"
        )
        if file_path:
            self.flash_file_input.setText(file_path)

    def flash_partition(self):
        """Flash a partition image."""
        image_path = self.flash_file_input.text().strip()
        partition = self.partition_combo.currentText().strip()
        if not image_path:
            self.terminal_screen.append_message("System", "Select an image file first.", is_ai=True)
            return
        cmd = ["fastboot", "flash", partition, image_path]
        self.terminal_screen.append_message("System", f"$ {' '.join(cmd)}", is_ai=True)
        try:
            return_code, output, error = self._run_cli(cmd, timeout=300)
            if output:
                self.terminal_screen.append_message("Fastboot", output, is_ai=True)
            if error:
                self.terminal_screen.append_message("Fastboot", error, is_ai=True)
            if return_code == 0:
                self.terminal_screen.append_message("System", "Flash completed.", is_ai=True)
            else:
                self.terminal_screen.append_message("System", f"Flash failed: {return_code}", is_ai=True)
        except (subprocess.SubprocessError, FileNotFoundError) as ex:
            self.terminal_screen.append_message("System", f"Flash failed: {ex}", is_ai=True)

    def show_about(self):
        """Show about dialog."""
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.about(
            self,
            "About LlamaPhone",
            "<h2>LlamaPhone v1.0.0</h2>"
            "<p>AI-Powered Mobile Repair Console</p>"
            "<p>Model: LP-3000 TUBE</p>"
            "<p>Built with PyQt6 • Ollama • ADB</p>"
            "<p>© 2024 LlamaPhone Industries</p>"
        )

    def paintEvent(self, event):
        """Custom paint for TV cabinet effects."""
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw subtle TV cabinet highlight
        painter.setPen(QPen(QColor(80, 80, 80), 1))

    def closeEvent(self, event):
        """Handle window close."""
        from PyQt6.QtWidgets import QMessageBox
        reply = QMessageBox.question(
            self,
            "Confirm Exit",
            "Are you sure you want to exit LlamaPhone?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()
