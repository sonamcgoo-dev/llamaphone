#!/usr/bin/env python3
"""
LlamaPhone - Main Entry Point
AI-Powered Mobile Repair Console with Retro CRT TV Aesthetics
"""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtGui import QFontDatabase
from PyQt6.QtWidgets import QApplication

from ui.main_window import MainWindow
from ui.splash_screen import SplashScreen


def main():
    """Main entry point for LlamaPhone."""

    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("LlamaPhone")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("LlamaPhone")

    # Set application-wide style
    app.setStyle("Fusion")

    # Load custom fonts
    font_dir = os.path.join(os.path.dirname(__file__), "assets", "fonts")
    if os.path.exists(font_dir):
        for font_file in os.listdir(font_dir):
            if font_file.endswith(('.ttf', '.otf')):
                QFontDatabase.addApplicationFont(os.path.join(font_dir, font_file))

    # Show splash screen first
    splash = SplashScreen()
    splash.show()
    app.processEvents()

    # Create main window (hidden initially)
    main_window = MainWindow()

    # Connect splash completion to main window
    def on_splash_complete():
        splash.close()
        main_window.show()
        main_window.activateWindow()
        main_window.raise_()

    splash.finished.connect(on_splash_complete)

    # Start event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
