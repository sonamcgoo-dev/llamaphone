#!/usr/bin/env python3
"""
LlamaPhone - Main Entry Point
AI-Powered Mobile Repair Console with Retro CRT TV Aesthetics
"""

import os
import sys
import traceback
from datetime import datetime
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def runtime_log_path() -> Path:
    return Path.home() / ".llamaphone" / "runtime.log"


def log_runtime(message: str):
    log_file = runtime_log_path()
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with log_file.open("a", encoding="utf-8") as handle:
        handle.write(f"[{datetime.now().isoformat()}] {message}\n")


def resource_path(*parts: str) -> str:
    """Resolve resource paths for source runs and PyInstaller bundles."""
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, *parts)


def main():
    """Main entry point for LlamaPhone."""
    try:
        os.environ.setdefault("QT_OPENGL", "software")
        log_runtime(f"startup begin frozen={getattr(sys, 'frozen', False)}")

        from PyQt6.QtGui import QFontDatabase, QIcon
        from PyQt6.QtWidgets import QApplication

        from ui.main_window import MainWindow
        from ui.splash_screen import SplashScreen

        # Create application
        app = QApplication(sys.argv)
        app.setApplicationName("LlamaPhone")
        app.setApplicationVersion("1.0.0")
        app.setOrganizationName("LlamaPhone")
        app.setWindowIcon(QIcon(resource_path("assets", "icon.png")))

        # Set application-wide style
        app.setStyle("Fusion")

        # Load custom fonts
        font_dir = resource_path("assets", "fonts")
        if os.path.exists(font_dir):
            for font_file in os.listdir(font_dir):
                if font_file.endswith((".ttf", ".otf")):
                    QFontDatabase.addApplicationFont(os.path.join(font_dir, font_file))

        # Create main window
        main_window = MainWindow()

        # Splash is disabled for packaged builds for maximum runtime stability.
        if getattr(sys, "frozen", False):
            main_window.show()
            main_window.showNormal()
            log_runtime("main window shown (frozen)")
        else:
            splash = SplashScreen()
            splash.show()
            app.processEvents()

            def on_splash_complete():
                splash.close()
                main_window.show()
                main_window.showNormal()
                log_runtime("main window shown (source)")

            splash.finished.connect(on_splash_complete)

        # Start event loop
        exit_code = app.exec()
        log_runtime(f"event loop exited code={exit_code}")
        sys.exit(exit_code)
    except Exception:
        log_runtime("fatal startup exception:\n" + traceback.format_exc())
        raise


if __name__ == "__main__":
    main()
