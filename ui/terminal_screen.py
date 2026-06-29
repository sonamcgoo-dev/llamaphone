"""
LlamaPhone - Terminal Screen
AI Chat interface with retro terminal styling
"""

from PyQt6.QtCore import Qt, QThread
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)


class TerminalScreen(QWidget):
    """AI Terminal chat screen with retro CRT styling."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.messages = []
        self.ai_thread = None

        self.init_ui()

    def init_ui(self):
        """Initialize the terminal UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Terminal header
        header = QLabel("🤖 AI ASSISTANT - TERMINAL")
        header.setStyleSheet("""
            color: #FFB000;
            font-size: 14px;
            font-weight: bold;
            padding: 5px 10px;
            border-bottom: 2px solid #33FF33;
        """)
        layout.addWidget(header)

        # Chat area (scrollable)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
        """)

        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.chat_layout.setSpacing(15)

        scroll_area.setWidget(self.chat_container)
        layout.addWidget(scroll_area, 1)

        # Welcome message
        self.append_message(
            "LlamaPhone AI",
            "Welcome to LlamaPhone! 🐐📱\n\n"
            "I can help you with:\n"
            "• ADB and Fastboot commands\n"
            "• Device diagnostics and repair\n"
            "• FRP bypass procedures\n"
            "• Bootloader unlock guides\n"
            "• Root access setup (Magisk/Shizuku)\n"
            "• Script generation for automation\n\n"
            "Connect a device and describe what you need help with!",
            is_ai=True
        )

        # Input area
        input_frame = QWidget()
        input_frame.setStyleSheet("""
            background-color: #1A1A1A;
            border: 2px solid #33FF33;
            border-radius: 8px;
            padding: 5px;
        """)
        input_layout = QHBoxLayout(input_frame)
        input_layout.setContentsMargins(5, 5, 5, 5)
        input_layout.setSpacing(10)

        # Prompt symbol
        prompt_label = QLabel("❯")
        prompt_label.setStyleSheet("""
            color: #33FF33;
            font-size: 18px;
            font-weight: bold;
        """)
        input_layout.addWidget(prompt_label)

        # Input field
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Ask me anything about mobile repair...")
        self.input_field.setStyleSheet("""
            background-color: transparent;
            color: #33FF33;
            border: none;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            padding: 5px;
        """)
        self.input_field.setMinimumHeight(35)
        self.input_field.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.input_field, 1)

        # Send button
        send_btn = QPushButton("▶")
        send_btn.setFixedSize(40, 35)
        send_btn.setStyleSheet("""
            QPushButton {
                background-color: #33FF33;
                color: #0D0D0D;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #44FF44;
            }
            QPushButton:pressed {
                background-color: #22DD22;
            }
        """)
        send_btn.clicked.connect(self.send_message)
        input_layout.addWidget(send_btn)

        layout.addWidget(input_frame)

    def append_message(self, sender, message, is_ai=False):
        """Append a message to the chat."""
        msg_widget = MessageBubble(sender, message, is_ai=is_ai)
        self.chat_layout.addWidget(msg_widget)
        self.messages.append((sender, message, is_ai))

        # Scroll to bottom
        self.chat_container.updateGeometry()
        scroll_area = self.findChild(QScrollArea)
        if scroll_area:
            scroll_area.verticalScrollBar().setValue(
                scroll_area.verticalScrollBar().maximum()
            )

    def send_message(self):
        """Send user message to AI."""
        text = self.input_field.text().strip()
        if not text:
            return

        # Add user message
        self.append_message("You", text, is_ai=False)
        self.input_field.clear()

        # Simulate AI response
        self.simulate_ai_response(text)

    def simulate_ai_response(self, user_input):
        """Simulate AI response for demo."""
        # Typing indicator
        typing = QLabel("AI is thinking...")
        typing.setStyleSheet("""
            color: #666666;
            font-style: italic;
            padding: 10px;
        """)
        self.chat_layout.addWidget(typing)

        # Simulate delay
        QThread.msleep(500)

        # Remove typing indicator
        typing.deleteLater()

        # Generate response based on input
        response = self.generate_response(user_input)
        self.append_message("LlamaPhone AI", response, is_ai=True)

    def generate_response(self, user_input):
        """Generate a contextual response."""
        user_input_lower = user_input.lower()

        if any(word in user_input_lower for word in ['hello', 'hi', 'hey']):
            return "Hello! 👋 I'm your AI repair assistant. How can I help you today?"

        elif any(word in user_input_lower for word in ['adb', 'connect', 'device']):
            return (
                "To connect a device via ADB:\n\n"
                "1. Enable USB Debugging on the device:\n"
                "   Settings → Developer Options → USB Debugging\n\n"
                "2. Connect via USB cable\n\n"
                "3. Authorize the computer on the device\n\n"
                "4. Run `adb devices` to verify connection\n\n"
                "Would you like me to walk you through any specific step?"
            )

        elif any(word in user_input_lower for word in ['frp', 'bypass', 'google']):
            return (
                "FRP (Factory Reset Protection) Bypass:\n\n"
                "⚠️ **WARNING**: Only bypass FRP on devices you own!\n\n"
                "Common methods:\n"
                "1. **PIN/Pattern Backup** - Try last known credentials\n"
                "2. **Samsung**: Emergency dial → `*#0*#`\n"
                "3. **Google FRP**: Account recovery after 72 hours\n"
                "4. **OEM Methods**: Various exploits by manufacturer\n\n"
                "Which device brand are you working with?"
            )

        elif any(word in user_input_lower for word in ['bootloader', 'unlock']):
            return (
                "Bootloader Unlock Process:\n\n"
                "⚠️ **WARNING**: Unlocking erases ALL data!\n\n"
                "**Samsung**: Settings → Developer → OEM Unlock (enable)\n"
                "Then: `fastboot oem unlock`\n\n"
                "**Google/Pixel**: `fastboot flashing unlock`\n\n"
                "**OnePlus**: Developer → OEM Unlock → `fastboot oem unlock`\n\n"
                "**Xiaomi**: Mi Unlock Status → Add account → `fastboot oem unlock`\n\n"
                "What's your device model?"
            )

        elif any(word in user_input_lower for word in ['root', 'magisk']):
            return (
                "Root Access Methods:\n\n"
                "**Magisk (Recommended)**:\n"
                "1. Unlock bootloader\n"
                "2. Boot to recovery\n"
                "3. Flash Magisk ZIP\n"
                "4. Install Magisk Manager app\n\n"
                "**Shizuku (No Root)**:\n"
                "1. Install Shizuku APK\n"
                "2. Enable USB Debugging\n"
                "3. Grant ADB permissions\n"
                "4. Use apps with root-like access via ADB\n\n"
                "Would you like detailed steps for a specific device?"
            )

        elif any(word in user_input_lower for word in ['fastboot', 'flash']):
            return (
                "Fastboot Commands:\n\n"
                "```\n"
                "fastboot devices           # List devices\n"
                "fastboot reboot            # Normal reboot\n"
                "fastboot reboot recovery   # Boot to recovery\n"
                "fastboot flash boot boot.img  # Flash boot image\n"
                "fastboot oem unlock        # Unlock bootloader\n"
                "fastboot flashing unlock   # Unlock (Pixel/Samsung)\n"
                "fastboot erase userdata    # Wipe data\n"
                "```\n\n"
                "Which command would you like help with?"
            )

        elif any(word in user_input_lower for word in ['script', 'python', 'automation']):
            return (
                "I can generate Python scripts for repair automation!\n\n"
                "Here's an example ADB script:\n\n"
                "```python\n"
                "import subprocess\n\n"
                "def connect_wifi_device(ip, port=5555):\n"
                "    subprocess.run(['adb', 'tcpip', port])\n"
                "    time.sleep(2)\n"
                "    subprocess.run([\n"
                "        'adb', 'connect', f'{ip}:{port}'\n"
                "    ])\n\n"
                "def install_apk(apk_path):\n"
                "    subprocess.run([\n"
                "        'adb', 'install', '-r', apk_path\n"
                "    ])\n"
                "```\n\n"
                "What specific task would you like to automate?"
            )

        elif any(word in user_input_lower for word in ['exploit', 'cve', 'vulnerability']):
            return (
                "⚠️ **Security Notice**: Only use exploits on authorized devices!\n\n"
                "I have a database of known exploits organized by:\n"
                "• Device manufacturer\n"
                "• Android version\n"
                "• Attack type\n\n"
                "This database is for educational and authorized repair purposes.\n"
                "What's the device model you're researching?"
            )

        elif any(word in user_input_lower for word in ['help', 'commands', 'what can you']):
            return (
                "**I can help you with:**\n\n"
                "📱 **Device Connection**\n"
                "   ADB over USB/WiFi, device pairing\n\n"
                "🔓 **Bypass & Unlock**\n"
                "   FRP, screen locks, network locks\n\n"
                "⚡ **Flash Operations**\n"
                "   Fastboot, recovery, firmware\n\n"
                "🔧 **Bootloader**\n"
                "   Unlock, lock, check status\n\n"
                "👑 **Root Access**\n"
                "   Magisk, Shizuku, KernelSU\n\n"
                "💻 **Scripting**\n"
                "   Python automation scripts\n\n"
                "💣 **Exploit Database**\n"
                "   Known vulnerabilities by device\n\n"
                "Just describe what you need!"
            )

        else:
            return (
                f"I understand you need help with: **{user_input}**\n\n"
                "I specialize in mobile repair and device management.\n\n"
                "Try asking about:\n"
                "• Device connection (ADB/WiFi)\n"
                "• FRP bypass procedures\n"
                "• Bootloader unlock steps\n"
                "• Root access methods\n"
                "• Script generation\n\n"
                "What would you like to do?"
            )


class MessageBubble(QWidget):
    """Chat message bubble widget."""

    def __init__(self, sender, message, is_ai=False):
        super().__init__()
        self.sender = sender
        self.message = message
        self.is_ai = is_ai

        self.init_ui()

    def init_ui(self):
        """Initialize the message bubble UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(3)

        # Sender label
        sender_label = QLabel(self.sender)
        sender_color = "#00AAFF" if self.is_ai else "#FFB000"
        sender_label.setStyleSheet(f"""
            color: {sender_color};
            font-weight: bold;
            font-size: 12px;
        """)
        layout.addWidget(sender_label)

        # Message content
        content = self.format_message(self.message)

        if self.is_ai:
            # AI messages in terminal style
            msg_label = QLabel(content)
            msg_label.setStyleSheet("""
                color: #33FF33;
                background-color: #0D0D0D;
                border: 1px solid #33FF33;
                border-radius: 5px;
                padding: 10px;
                font-family: 'Courier New', monospace;
                font-size: 13px;
                line-height: 1.5;
            """)
            msg_label.setWordWrap(True)
            msg_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        else:
            # User messages
            msg_label = QLabel(content)
            msg_label.setStyleSheet("""
                color: #FFB000;
                background-color: #1A1A1A;
                border: 1px solid #FFB000;
                border-radius: 5px;
                padding: 10px;
                font-family: 'Courier New', monospace;
                font-size: 13px;
                line-height: 1.5;
            """)
            msg_label.setWordWrap(True)
            msg_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        layout.addWidget(msg_label)

    def format_message(self, message):
        """Format message with basic markdown-like syntax."""
        # Simple formatting
        formatted = message
        formatted = formatted.replace("```", "")
        formatted = formatted.replace("**", "")

        return formatted
