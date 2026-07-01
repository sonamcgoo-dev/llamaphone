"""
LlamaPhone - Control Panel
TV knobs and buttons for module selection
"""

import math

from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QBrush, QColor, QConicalGradient, QPainter, QPen
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class ControlPanel(QWidget):
    """TV-style control panel with knobs and buttons."""

    module_selected = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_channel = 1
        self.channels = [
            ("TERMINAL", "🤖", "AI Chat & Commands"),
            ("BYPASS", "🔓", "Unlock & Bypass"),
            ("CONNECT", "📡", "Device Connection"),
            ("ADB", "💻", "ADB Commands"),
            ("SIDELOAD", "📦", "App Sideloading"),
            ("FASTBOOT", "⚡", "Fastboot Mode"),
            ("BOOTLOADER", "🔧", "Bootloader"),
            ("DOWNLOAD", "📥", "Download Mode"),
            ("ROOT", "👑", "Root Access"),
            ("EXPLOITS", "💣", "Exploit Database"),
            ("SETTINGS", "⚙️", "Configuration"),
        ]

        self.init_ui()
        self.start_channel_animation()

    def init_ui(self):
        """Initialize the control panel UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 15, 10, 15)
        layout.setSpacing(15)

        # Panel header
        header = QLabel("CONTROLS")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("""
            color: #888888;
            font-size: 12px;
            font-weight: bold;
            letter-spacing: 2px;
            padding: 5px;
        """)
        layout.addWidget(header)

        # Channel selector (rotary knob style)
        channel_frame = self.create_channel_selector()
        layout.addWidget(channel_frame)

        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background-color: #333;")
        layout.addWidget(separator)

        # Module buttons
        self.create_module_buttons(layout)

        # Separator
        layout.addWidget(separator)

        # Volume knob
        volume_frame = self.create_volume_knob()
        layout.addWidget(volume_frame)

        # TV Brand decoration
        brand = QLabel("LLAMAPHONE")
        brand.setAlignment(Qt.AlignmentFlag.AlignCenter)
        brand.setStyleSheet("""
            color: #555555;
            font-size: 10px;
            font-weight: bold;
            letter-spacing: 3px;
            padding-top: 15px;
        """)
        layout.addWidget(brand)

        model_label = QLabel("LP-3000")
        model_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        model_label.setStyleSheet("""
            color: #444444;
            font-size: 9px;
        """)
        layout.addWidget(model_label)

    def create_channel_selector(self):
        """Create the channel selector knob."""
        frame = QFrame()
        frame_layout = QVBoxLayout(frame)
        frame_layout.setSpacing(10)

        # Channel label
        channel_label = QLabel("CHANNEL")
        channel_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        channel_label.setStyleSheet("color: #666666; font-size: 10px;")
        frame_layout.addWidget(channel_label)

        # Rotary knob
        self.channel_knob = RotaryKnob()
        self.channel_knob.setMinimumSize(80, 80)
        self.channel_knob.valueChanged.connect(self.on_channel_changed)
        self.channel_knob.setRange(1, len(self.channels))
        self.channel_knob.setValue(1)
        frame_layout.addWidget(self.channel_knob, alignment=Qt.AlignmentFlag.AlignCenter)

        # Current module name
        self.channel_display = QLabel(f"{self.channels[0][0]}\n{self.channels[0][1]}")
        self.channel_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.channel_display.setStyleSheet("""
            color: #33FF33;
            font-size: 14px;
            font-weight: bold;
            padding: 5px;
        """)
        frame_layout.addWidget(self.channel_display)

        # Module description
        self.channel_desc = QLabel(self.channels[0][2])
        self.channel_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.channel_desc.setStyleSheet("color: #888888; font-size: 10px;")
        frame_layout.addWidget(self.channel_desc)

        return frame

    def create_module_buttons(self, layout):
        """Create the module selection buttons and add them to layout."""
        button_widget = QWidget()
        button_layout = QVBoxLayout(button_widget)
        button_layout.setSpacing(8)

        for name, emoji, desc in self.channels:
            btn = ModuleButton(name, emoji, desc)
            btn.clicked.connect(lambda checked, n=name: self.select_module(n))
            button_layout.addWidget(btn)

        layout.addWidget(button_widget)

    def create_volume_knob(self):
        """Create the volume control knob."""
        frame = QFrame()
        frame_layout = QVBoxLayout(frame)
        frame_layout.setSpacing(5)

        vol_label = QLabel("VOLUME")
        vol_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vol_label.setStyleSheet("color: #666666; font-size: 10px;")
        frame_layout.addWidget(vol_label)

        self.volume_knob = RotaryKnob()
        self.volume_knob.setMinimumSize(50, 50)
        self.volume_knob.setRange(0, 100)
        self.volume_knob.setValue(75)
        frame_layout.addWidget(self.volume_knob, alignment=Qt.AlignmentFlag.AlignCenter)

        # LED indicator
        led_layout = QHBoxLayout()
        led_layout.addStretch()

        self.power_led = LEDIndicator(color="#33FF33")
        led_layout.addWidget(self.power_led)

        led_layout.addStretch()
        frame_layout.addLayout(led_layout)

        return frame

    def on_channel_changed(self, value):
        """Handle channel knob change."""
        index = value - 1
        if 0 <= index < len(self.channels):
            name, emoji, desc = self.channels[index]
            self.channel_display.setText(f"{emoji} {name}")
            self.channel_desc.setText(desc)
            self.current_channel = value

    def select_module(self, module_name):
        """Select and emit module selection."""
        # Find index
        for i, (name, _, _) in enumerate(self.channels):
            if name.lower() == module_name.lower():
                self.channel_knob.setValue(i + 1)
                break

        self.module_selected.emit(module_name.lower())

    def start_channel_animation(self):
        """Start channel switching animation."""
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.update_power_led)
        self.animation_timer.start(1000)

    def update_power_led(self):
        """Update power LED state."""
        # Pulse effect
        self.power_led.toggle()


class RotaryKnob(QWidget):
    """Rotary knob control widget."""

    valueChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._value = 0
        self._minimum = 0
        self._maximum = 100
        self._angle = -135  # Start angle

        self.setMinimumSize(60, 60)
        self.setMaximumSize(100, 100)

    def setRange(self, minimum, maximum):
        """Set the knob range."""
        self._minimum = minimum
        self._maximum = maximum

    def setValue(self, value):
        """Set the knob value."""
        value = max(self._minimum, min(self._maximum, value))
        if value != self._value:
            self._value = value
            self.update()

    def value(self):
        """Get the knob value."""
        return self._value

    def mousePressEvent(self, event):
        """Handle mouse press."""
        self._last_y = event.position().y()

    def mouseMoveEvent(self, event):
        """Handle mouse drag."""
        delta = self._last_y - event.position().y()
        self._last_y = event.position().y()

        # Calculate new value
        range_size = self._maximum - self._minimum
        delta_value = int(delta * range_size / 100)

        new_value = self._value + delta_value
        self.setValue(new_value)
        self.valueChanged.emit(self._value)

        # Update angle
        range_ratio = (self._value - self._minimum) / max(1, self._maximum - self._minimum)
        self._angle = -135 + (range_ratio * 270)
        self.update()

    def paintEvent(self, event):
        """Paint the rotary knob."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        size = min(self.width(), self.height())
        center = self.rect().center()
        radius = size // 2 - 5

        # Background circle
        painter.setBrush(QBrush(QColor(40, 40, 40)))
        painter.setPen(QPen(QColor(60, 60, 60), 2))
        painter.drawEllipse(center, radius, radius)

        # Inner circle (metallic look)
        gradient = QConicalGradient(center, -90)
        gradient.setColorAt(0, QColor(80, 80, 80))
        gradient.setColorAt(0.5, QColor(60, 60, 60))
        gradient.setColorAt(1, QColor(80, 80, 80))

        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(center, radius - 10, radius - 10)

        # Tick marks
        painter.setPen(QPen(QColor(100, 100, 100), 2))
        for i in range(11):
            angle = math.radians(-135 + (i * 27))
            inner = radius - 15
            outer = radius - 5
            x1 = center.x() + inner * math.cos(angle)
            y1 = center.y() + inner * math.sin(angle)
            x2 = center.x() + outer * math.cos(angle)
            y2 = center.y() + outer * math.sin(angle)
            painter.drawLine(int(x1), int(y1), int(x2), int(y2))

        # Indicator line
        indicator_angle = math.radians(self._angle)
        inner = 5
        outer = radius - 18
        x1 = center.x() + inner * math.cos(indicator_angle)
        y1 = center.y() + inner * math.sin(indicator_angle)
        x2 = center.x() + outer * math.cos(indicator_angle)
        y2 = center.y() + outer * math.sin(indicator_angle)

        painter.setPen(QPen(QColor(255, 180, 0), 3))
        painter.drawLine(int(x1), int(y1), int(x2), int(y2))

        # Center cap
        painter.setBrush(QBrush(QColor(50, 50, 50)))
        painter.setPen(QPen(QColor(70, 70, 70), 1))
        painter.drawEllipse(center, 8, 8)


class ModuleButton(QPushButton):
    """Custom TV-style module button."""

    def __init__(self, name, emoji, description):
        super().__init__(f"{emoji}")
        self.module_name = name
        self.description = description

        self.setToolTip(f"{name}\n{description}")
        self.setMinimumHeight(35)

        self.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3A3A3A,
                    stop:0.5 #2D2D2D,
                    stop:1 #2A2A2A);
                color: #FFB000;
                border: 2px solid #1A1A1A;
                border-radius: 8px;
                font-size: 16px;
                padding: 5px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4A4A4A,
                    stop:0.5 #3A3A3A,
                    stop:1 #333333);
                color: #33FF33;
                border: 2px solid #33FF33;
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2A2A2A,
                    stop:0.5 #1A1A1A,
                    stop:1 #2A2A2A);
                padding-top: 7px;
                padding-bottom: 3px;
            }
        """)


class LEDIndicator(QWidget):
    """LED indicator light."""

    def __init__(self, color="#33FF33", parent=None):
        super().__init__(parent)
        self.color = QColor(color)
        self._on = True
        self._brightness = 1.0

        self.setMinimumSize(12, 12)
        self.setMaximumSize(12, 12)

    def setOn(self, on):
        """Set LED on/off state."""
        self._on = on
        self.update()

    def toggle(self):
        """Toggle LED state."""
        self._on = not self._on
        self.update()

    def paintEvent(self, event):
        """Paint the LED."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self._on:
            # Glow effect
            glow = self.color.lighter(150)
            glow.setAlpha(100)
            painter.setBrush(QBrush(glow))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(self.rect().adjusted(-3, -3, 3, 3))

        # LED body
        led_color = self.color if self._on else QColor(50, 20, 20)
        painter.setBrush(QBrush(led_color))
        painter.setPen(QPen(self.color.darker(150), 1) if self._on else QPen(QColor(30, 30, 30), 1))
        painter.drawEllipse(self.rect())


class TVButton(QPushButton):
    """Large TV power button with LED."""

    def __init__(self):
        super().__init__("⏻")

        self.setMinimumSize(60, 60)
        self.setMaximumSize(80, 80)

        self.setStyleSheet("""
            QPushButton {
                background: qradialgradient(cx:0.5, cy:0.5, radius:0.8,
                    stop:0 #4A4A4A,
                    stop:0.7 #2A2A2A,
                    stop:1 #1A1A1A);
                color: #33FF33;
                border: 3px solid #0A0A0A;
                border-radius: 30px;
                font-size: 24px;
            }
            QPushButton:hover {
                background: qradialgradient(cx:0.5, cy:0.5, radius:0.8,
                    stop:0 #5A5A5A,
                    stop:0.7 #3A3A3A,
                    stop:1 #2A2A2A);
                color: #44FF44;
            }
            QPushButton:pressed {
                background: qradialgradient(cx:0.5, cy:0.5, radius:0.8,
                    stop:0 #2A2A2A,
                    stop:0.7 #1A1A1A,
                    stop:1 #0A0A0A);
            }
        """)
