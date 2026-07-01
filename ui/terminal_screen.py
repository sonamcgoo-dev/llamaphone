"""
LlamaPhone - Terminal Screen
AI Chat interface with retro terminal styling
"""

from PyQt6.QtCore import QObject, Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from ai.ollama_client import LlamaPhoneAI, OllamaClient


class AIWorker(QObject):
    """Background worker for Ollama requests."""

    finished = pyqtSignal(str)
    failed = pyqtSignal(str)

    def __init__(self, user_input: str, model_name: str | None = None):
        super().__init__()
        self.user_input = user_input
        self.model_name = model_name

    def run(self):
        try:
            client = OllamaClient(model=self.model_name) if self.model_name else OllamaClient()
            if not client.is_available():
                self.failed.emit("Ollama is not running. Start it, then try again.")
                return
            ai = LlamaPhoneAI(client)
            result = ai.chat(self.user_input)
            content = result.get("content", "").strip()
            if not content:
                content = "I ran, but returned an empty response. Try rephrasing your prompt."
            self.finished.emit(content)
            client.close()
        except Exception as error:
            self.failed.emit(f"AI request failed: {error}")


class TerminalScreen(QWidget):
    """AI Terminal chat screen with retro CRT styling."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.messages = []
        self.ai_thread = None
        self.typing_indicator = None

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

        if self.ai_thread is not None and self.ai_thread.isRunning():
            self.append_message("System", "Previous request is still running. Please wait.", is_ai=True)
            return

        self.typing_indicator = QLabel("AI is thinking...")
        self.typing_indicator.setStyleSheet("""
            color: #666666;
            font-style: italic;
            padding: 10px;
        """)
        self.chat_layout.addWidget(self.typing_indicator)

        self.ai_thread = QThread(self)
        self.ai_worker = AIWorker(text, self.selected_model_name())
        self.ai_worker.moveToThread(self.ai_thread)
        self.ai_thread.started.connect(self.ai_worker.run)
        self.ai_worker.finished.connect(self.on_ai_response)
        self.ai_worker.failed.connect(self.on_ai_error)
        self.ai_worker.finished.connect(self.ai_thread.quit)
        self.ai_worker.failed.connect(self.ai_thread.quit)
        self.ai_thread.finished.connect(self.ai_thread.deleteLater)
        self.ai_thread.start()

    def selected_model_name(self) -> str | None:
        """Read active model from main window settings when available."""
        parent = self.parent()
        if parent is not None and hasattr(parent, "model_combo"):
            model_combo = parent.model_combo
            if model_combo is not None and hasattr(model_combo, "currentText"):
                model_name = model_combo.currentText().strip()
                if model_name:
                    return model_name
        return None

    def remove_typing_indicator(self):
        if self.typing_indicator is not None:
            self.typing_indicator.deleteLater()
            self.typing_indicator = None

    def on_ai_response(self, response: str):
        self.remove_typing_indicator()
        self.append_message("LlamaPhone AI", response, is_ai=True)

    def on_ai_error(self, error_message: str):
        self.remove_typing_indicator()
        self.append_message("System", error_message, is_ai=True)


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
