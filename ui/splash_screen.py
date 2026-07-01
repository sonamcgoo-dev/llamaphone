"""
LlamaPhone - Splash Screen
Retro CRT TV boot animation with credits
"""

import math
import os

from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QBrush, QColor, QFont, QLinearGradient, QPixmap
from PyQt6.QtWidgets import QFrame, QLabel, QProgressBar, QVBoxLayout, QWidget


class SplashScreen(QWidget):
    """Retro CRT TV splash screen with boot animation."""

    finished = pyqtSignal()

    # Boot messages
    BOOT_MESSAGES = [
        "LLAMAPHONE SYSTEMS v1.0.0",
        "INITIALIZING CRT DISPLAY...",
        "LOADING PHOSPHOR ARRAYS...",
        "CALIBRATING SCANLINES...",
        "DETECTING ADB SERVICES...",
        "CONNECTING TO OLLAMA AI...",
        "LOADING EXPLOIT DATABASE...",
        "INITIALIZING SECURITY LAYER...",
        "WARMING UP VACUUM TUBES...",
        "ALL SYSTEMS NOMINAL",
        "",
        ">>> READY <<<",
    ]

    IMAGE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "branding")
    WORDMARK_PATH = os.path.join(IMAGE_DIR, "llamaphone-wordmark.png")

    def __init__(self, parent=None):
        super().__init__(parent)
        self.boot_index = 0
        self.progress_value = 0
        self.cursor_visible = True
        self.dial_angle = 0
        self.loader_tick = 0
        self.horizontal_images: list[QPixmap] = []
        self.vertical_images: list[QPixmap] = []
        self._load_branding_images()

        self.init_ui()
        self.start_animation()

    def _load_branding_images(self):
        """Load splash and loader art from assets/branding."""
        if not os.path.isdir(self.IMAGE_DIR):
            return

        image_files = [f for f in os.listdir(self.IMAGE_DIR) if f.lower().endswith(".png")]
        for filename in sorted(image_files):
            path = os.path.join(self.IMAGE_DIR, filename)
            pixmap = QPixmap(path)
            if pixmap.isNull():
                continue

            if pixmap.width() >= pixmap.height():
                self.horizontal_images.append(pixmap)
            else:
                self.vertical_images.append(pixmap)

    def init_ui(self):
        """Initialize the splash screen UI."""
        self.setFixedSize(800, 600)
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.SplashScreen
        )

        # Center on screen
        self.move_to_center()

        # Main container - TV Frame
        self.frame = QFrame(self)
        self.frame.setObjectName("splashFrame")
        self.frame.setGeometry(10, 10, 780, 580)

        # CRT Screen
        self.screen = QFrame(self.frame)
        self.screen.setObjectName("splashScreen")
        self.screen.setGeometry(50, 50, 700, 400)

        self.background_label = QLabel(self.screen)
        self.background_label.setGeometry(0, 0, 700, 400)
        self.background_label.setScaledContents(True)
        self.background_label.lower()
        self.set_background_frame(0)

        # Layout for screen content
        screen_layout = QVBoxLayout(self.screen)
        screen_layout.setContentsMargins(20, 20, 20, 20)

        # Title / wordmark
        self.title_label = QLabel("LLAMAPHONE")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont("Courier New", 32, QFont.Weight.Bold)
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet("""
            color: #33FF33;
            text-shadow: 0 0 10px #33FF33, 0 0 20px #33FF33;
            padding: 20px;
        """)
        self._set_title_wordmark()
        screen_layout.addWidget(self.title_label)

        # Subtitle
        self.subtitle_label = QLabel("AI-POWERED MOBILE REPAIR CONSOLE")
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_font = QFont("Courier New", 14)
        self.subtitle_label.setFont(subtitle_font)
        self.subtitle_label.setStyleSheet("color: #FFB000; padding: 5px;")
        screen_layout.addWidget(self.subtitle_label)

        # Boot log area
        self.boot_log = QLabel()
        self.boot_log.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        boot_font = QFont("Courier New", 11)
        self.boot_log.setFont(boot_font)
        self.boot_log.setStyleSheet("""
            color: #33FF33;
            background-color: transparent;
            padding: 15px;
            line-height: 1.6;
        """)
        self.boot_log.setText("\n".join(self.BOOT_MESSAGES[:1]))
        screen_layout.addWidget(self.boot_log)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(15)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #1A1A1A;
                border: 2px solid #33FF33;
                border-radius: 5px;
                height: 15px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #33FF33, stop:0.5 #00FF00, stop:1 #33FF33);
                border-radius: 3px;
            }
        """)
        screen_layout.addWidget(self.progress_bar)

        # Animated llama loader
        self.loading_llama = QLabel()
        self.loading_llama.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loading_llama.setFixedSize(130, 220)
        self.loading_llama.setStyleSheet("background: transparent;")
        screen_layout.addWidget(self.loading_llama, alignment=Qt.AlignmentFlag.AlignCenter)

        # Transition card (uses vertical art)
        self.transition_label = QLabel(self.screen)
        self.transition_label.setGeometry(250, 40, 200, 320)
        self.transition_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.transition_label.setStyleSheet(
            "background-color: rgba(13, 13, 13, 180); border: 2px solid #33FF33; border-radius: 8px;"
        )
        self.transition_label.hide()

        # Credits section
        credits_y = 480
        self.credits_label = QLabel(self.frame)
        self.credits_label.setGeometry(50, credits_y, 700, 80)
        self.credits_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        credits_font = QFont("Arial", 10)
        self.credits_label.setFont(credits_font)
        self.credits_label.setStyleSheet("color: #888888;")
        self.credits_label.setText(self.get_credits_text())

        # TV Brand label
        brand_y = 535
        self.brand_label = QLabel("LLAMAPHONE INDUSTRIES", self.frame)
        self.brand_label.setGeometry(50, brand_y, 350, 30)
        brand_font = QFont("Arial", 10, QFont.Weight.Bold)
        self.brand_label.setFont(brand_font)
        self.brand_label.setStyleSheet("color: #666666;")

        # Model label
        self.model_label = QLabel("MODEL: LP-3000 TUBE", self.frame)
        self.model_label.setGeometry(450, brand_y, 300, 30)
        self.model_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        model_font = QFont("Arial", 9)
        self.model_label.setFont(model_font)
        self.model_label.setStyleSheet("color: #555555;")

        # Scanline overlay
        self.scanline_overlay = QWidget(self.screen)
        self.scanline_overlay.setGeometry(0, 0, 700, 400)
        self.scanline_overlay.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        # VU Meter decoration
        self.vu_widget = VUMeterWidget(self.frame)
        self.vu_widget.setGeometry(620, 460, 100, 60)

    def move_to_center(self):
        """Center the splash screen on the primary display."""
        from PyQt6.QtWidgets import QApplication
        screen = QApplication.primaryScreen()
        if screen:
            geometry = screen.availableGeometry()
            x = (geometry.width() - self.width()) // 2
            y = (geometry.height() - self.height()) // 2
            self.move(x, y)

    def get_credits_text(self):
        """Get the credits text."""
        return """
        <b>CREDITS</b><br>
        Lead Developer: LlamaPhone Team<br>
        AI Integration: Ollama • Qwen2.5-Coder<br>
        ADB Bridge: adbutils • uiautomator2<br>
        Design: Retro CRT Tube Aesthetics
        """

    def start_animation(self):
        """Start the boot animation sequence."""
        # Timer for boot messages
        self.boot_timer = QTimer(self)
        self.boot_timer.timeout.connect(self.update_boot)
        self.boot_timer.start(400)  # Update every 400ms

        # Cursor blink timer
        self.cursor_timer = QTimer(self)
        self.cursor_timer.timeout.connect(self.toggle_cursor)
        self.cursor_timer.start(500)

        # VU meter animation
        self.vu_timer = QTimer(self)
        self.vu_timer.timeout.connect(self.update_vu_meter)
        self.vu_timer.start(50)

        self.loader_timer = QTimer(self)
        self.loader_timer.timeout.connect(self.update_loader_animation)
        self.loader_timer.start(150)

    def _set_title_wordmark(self):
        """Use the extracted LlamaPhone logo image as the splash title."""
        if not os.path.exists(self.WORDMARK_PATH):
            return
        pixmap = QPixmap(self.WORDMARK_PATH)
        if pixmap.isNull():
            return
        self.title_label.setText("")
        self.title_label.setPixmap(
            pixmap.scaledToWidth(420, Qt.TransformationMode.SmoothTransformation)
        )

    def update_boot(self):
        """Update boot messages."""
        if self.boot_index < len(self.BOOT_MESSAGES):
            # Build the text with all previous messages
            messages = []
            for i in range(self.boot_index + 1):
                msg = self.BOOT_MESSAGES[i]
                if i == self.boot_index:
                    # Add blinking cursor to current message
                    cursor = "_" if self.cursor_visible else " "
                    msg += cursor
                messages.append(msg)

            self.boot_log.setText("\n".join(messages))

            # Update progress
            self.progress_value = int(((self.boot_index + 1) / len(self.BOOT_MESSAGES)) * 100)
            self.progress_bar.setValue(self.progress_value)
            if self.horizontal_images:
                self.set_background_frame(self.boot_index // 3)

            self.boot_index += 1
        else:
            self.boot_timer.stop()
            self.cursor_timer.stop()
            self.loader_timer.stop()
            self.show_transition_frame()
            # Complete animation
            QTimer.singleShot(500, self.finished.emit)

    def toggle_cursor(self):
        """Toggle cursor visibility."""
        self.cursor_visible = not self.cursor_visible

    def update_vu_meter(self):
        """Update VU meter animation."""
        self.dial_angle += 5
        if self.dial_angle >= 360:
            self.dial_angle = 0
        self.vu_widget.update_angle(self.dial_angle)
        self.vu_widget.update_level(self.boot_index / len(self.BOOT_MESSAGES))

    def set_background_frame(self, index: int):
        """Set one of the horizontal splash images as CRT background."""
        if not self.horizontal_images:
            return
        frame = self.horizontal_images[index % len(self.horizontal_images)]
        self.background_label.setPixmap(
            frame.scaled(
                self.background_label.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation,
            )
        )

    def update_loader_animation(self):
        """Animate the vertical 'screaming llama' loading art."""
        if not self.vertical_images:
            return

        # Prefer the second vertical image (screaming llama) when available.
        scream_index = 1 if len(self.vertical_images) > 1 else 0
        frame = self.vertical_images[scream_index]

        # Small pulse keeps it animated even with a single image.
        pulse = 1.0 + (0.04 * math.sin(self.loader_tick * 0.6))
        width = int(120 * pulse)
        height = int(210 * pulse)
        pix = frame.scaled(
            width,
            height,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.loading_llama.setPixmap(pix)
        self.loader_tick += 1

    def show_transition_frame(self):
        """Show the transition card right before the main window appears."""
        if not self.vertical_images:
            return
        frame = self.vertical_images[0]
        self.transition_label.setPixmap(
            frame.scaled(
                self.transition_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )
        self.transition_label.show()

    def paintEvent(self, event):
        """Custom paint event for CRT effects."""
        super().paintEvent(event)

    def draw_scanlines(self, painter):
        """Draw CRT scanline effect."""
        painter.setPen(QColor(0, 0, 0, 30))
        screen_rect = self.screen.geometry()
        for y in range(0, screen_rect.height(), 3):
            painter.drawLine(
                screen_rect.left(),
                screen_rect.top() + y,
                screen_rect.right(),
                screen_rect.top() + y
            )

    def draw_vignette(self, painter):
        """Draw CRT vignette effect."""
        # Create radial gradient for vignette
        gradient = QLinearGradient(
            self.rect().topLeft(),
            self.rect().bottomRight()
        )
        gradient.setColorAt(0, QColor(0, 0, 0, 0))
        gradient.setColorAt(0.5, QColor(0, 0, 0, 0))
        gradient.setColorAt(1, QColor(0, 0, 0, 150))

        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(self.rect())


class VUMeterWidget(QWidget):
    """Stable VU meter decoration widget."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.angle = 0
        self.level = 0
        self.setFixedSize(100, 60)
        self.setStyleSheet("background-color: #1E1E1E; border: 1px solid #555; border-radius: 4px;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(4)

        self.title = QLabel("VU")
        self.title.setStyleSheet("color: #AAAAAA; font-size: 8px;")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title)

        self.bar = QProgressBar()
        self.bar.setRange(0, 100)
        self.bar.setTextVisible(False)
        self.bar.setFixedHeight(12)
        self.bar.setStyleSheet(
            """
            QProgressBar {
                background-color: #111111;
                border: 1px solid #333333;
                border-radius: 3px;
            }
            QProgressBar::chunk {
                background-color: #33FF33;
            }
            """
        )
        layout.addWidget(self.bar)

    def update_angle(self, angle):
        """Update the needle angle."""
        self.angle = angle

    def update_level(self, level):
        """Update the signal level."""
        self.level = level
        self.bar.setValue(max(0, min(100, int(level * 100))))
