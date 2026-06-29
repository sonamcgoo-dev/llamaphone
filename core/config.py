"""
LlamaPhone - Configuration Module
Application configuration management
"""

import json
import os
from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class AppConfig:
    """Application configuration."""
    # AI Settings
    ollama_url: str = "http://localhost:11434"
    default_model: str = "qwen2.5-coder:7b"
    ai_temperature: float = 0.7
    ai_max_tokens: int = 2048

    # ADB Settings
    adb_path: str = "adb"
    fastboot_path: str = "fastboot"
    auto_connect_wifi: bool = True
    default_device_timeout: int = 30

    # UI Settings
    theme: str = "crt_retro"
    show_splash: bool = True
    terminal_font_size: int = 14
    chat_history_limit: int = 100

    # Security Settings
    enable_audit_log: bool = True
    confirm_dangerous_commands: bool = True
    session_timeout_hours: int = 24

    # Paths
    exploit_db_path: str = ""
    driver_db_path: str = ""
    log_path: str = ""
    scripts_path: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'AppConfig':
        """Create from dictionary."""
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


class ConfigManager:
    """Manages application configuration."""

    DEFAULT_CONFIG_NAME = "config.json"

    def __init__(self, config_dir: str | None = None):
        if config_dir is None:
            config_dir = os.path.join(
                os.path.expanduser("~"),
                ".llamaphone"
            )

        self.config_dir = config_dir
        self.config_path = os.path.join(config_dir, self.DEFAULT_CONFIG_NAME)

        os.makedirs(config_dir, exist_ok=True)

        self.config = self._load()

    def _load(self) -> AppConfig:
        """Load configuration from file."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path) as f:
                    data = json.load(f)
                return AppConfig.from_dict(data)
            except Exception:
                pass

        return AppConfig()

    def save(self):
        """Save configuration to file."""
        with open(self.config_path, 'w') as f:
            json.dump(self.config.to_dict(), f, indent=2)

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return getattr(self.config, key, default)

    def set(self, key: str, value: Any):
        """Set a configuration value."""
        if hasattr(self.config, key):
            setattr(self.config, key, value)
            self.save()

    def reset(self):
        """Reset to default configuration."""
        self.config = AppConfig()
        self.save()


# Global instance
_config_manager: ConfigManager | None = None


def get_config() -> ConfigManager:
    """Get or create the global config manager."""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager


def get_app_config() -> AppConfig:
    """Get the application configuration."""
    return get_config().config
