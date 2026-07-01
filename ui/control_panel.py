"""
LlamaPhone - Control Panel
Stable right-side panel for module selection.
"""

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget


class ControlPanel(QWidget):
    """Stable control panel with direct module buttons."""

    module_selected = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.channels = [
            ("terminal", "🤖 TERMINAL"),
            ("bypass", "🔓 BYPASS"),
            ("connect", "📡 CONNECT"),
            ("adb", "💻 ADB"),
            ("sideload", "📦 SIDELOAD"),
            ("fastboot", "⚡ FASTBOOT"),
            ("bootloader", "🔧 BOOTLOADER"),
            ("download", "📥 DOWNLOAD"),
            ("root", "👑 ROOT"),
            ("exploits", "💣 EXPLOITS"),
            ("settings", "⚙️ SETTINGS"),
        ]
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 12, 10, 12)
        layout.setSpacing(8)

        header = QLabel("CONTROLS")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet(
            """
            color: #46D8FF;
            font-size: 12px;
            font-weight: bold;
            letter-spacing: 2px;
            padding: 4px;
            """
        )
        layout.addWidget(header)

        for module_key, text in self.channels:
            btn = QPushButton(text)
            btn.setMinimumHeight(34)
            btn.clicked.connect(lambda checked=False, m=module_key: self.select_module(m))
            layout.addWidget(btn)

        layout.addStretch()

        brand = QLabel("LLAMAPHONE")
        brand.setAlignment(Qt.AlignmentFlag.AlignCenter)
        brand.setStyleSheet("color: #FF70DF; font-size: 10px; font-weight: bold; letter-spacing: 2px;")
        layout.addWidget(brand)

    def select_module(self, module_name: str):
        self.module_selected.emit(module_name)
