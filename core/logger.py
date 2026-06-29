"""
LlamaPhone - Logger Module
Audit logging for all operations
"""

import json
import os
import threading
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any


@dataclass
class LogEntry:
    """Log entry for an operation."""
    timestamp: str
    level: str  # INFO, WARNING, ERROR, COMMAND, SECURITY
    operation: str
    details: str
    user: str
    session_id: str | None
    device_id: str | None
    success: bool
    metadata: dict[str, Any] = None

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        if self.metadata:
            data.update(self.metadata)
        return data


class AuditLogger:
    """
    Audit logger for tracking all operations.

    Logs are stored in JSON format for easy analysis.
    """

    def __init__(self, log_dir: str | None = None):
        if log_dir is None:
            log_dir = os.path.join(
                os.path.expanduser("~"),
                ".llamaphone",
                "logs"
            )

        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)

        self.current_log_file = os.path.join(
            log_dir,
            f"llamaphone_{datetime.now().strftime('%Y%m%d')}.json"
        )

        self._lock = threading.Lock()

    def _write_entry(self, entry: LogEntry):
        """Write a log entry to file."""
        with self._lock, open(self.current_log_file, 'a') as f:
            f.write(json.dumps(entry.to_dict()) + '\n')

    def info(self, operation: str, details: str, **kwargs):
        """Log an info message."""
        self._write_entry(LogEntry(
            timestamp=datetime.now().isoformat(),
            level="INFO",
            operation=operation,
            details=details,
            **kwargs
        ))

    def warning(self, operation: str, details: str, **kwargs):
        """Log a warning message."""
        self._write_entry(LogEntry(
            timestamp=datetime.now().isoformat(),
            level="WARNING",
            operation=operation,
            details=details,
            **kwargs
        ))

    def error(self, operation: str, details: str, **kwargs):
        """Log an error message."""
        self._write_entry(LogEntry(
            timestamp=datetime.now().isoformat(),
            level="ERROR",
            operation=operation,
            details=details,
            success=False,
            **kwargs
        ))

    def command(self, command: str, details: str, **kwargs):
        """Log a command execution."""
        self._write_entry(LogEntry(
            timestamp=datetime.now().isoformat(),
            level="COMMAND",
            operation="command_execution",
            details=f"{command}: {details}",
            **kwargs
        ))

    def security(self, operation: str, details: str, **kwargs):
        """Log a security-related event."""
        self._write_entry(LogEntry(
            timestamp=datetime.now().isoformat(),
            level="SECURITY",
            operation=operation,
            details=details,
            **kwargs
        ))

    def get_recent_logs(self, limit: int = 100) -> list[LogEntry]:
        """Get recent log entries."""
        if not os.path.exists(self.current_log_file):
            return []

        entries = []
        with open(self.current_log_file) as f:
            for line in f:
                try:
                    data = json.loads(line.strip())
                    entries.append(LogEntry(**data))
                except Exception:
                    pass

        return entries[-limit:]

    def get_logs_by_level(self, level: str) -> list[LogEntry]:
        """Get logs by level."""
        if not os.path.exists(self.current_log_file):
            return []

        entries = []
        with open(self.current_log_file) as f:
            for line in f:
                try:
                    data = json.loads(line.strip())
                    if data.get("level") == level:
                        entries.append(LogEntry(**data))
                except Exception:
                    pass

        return entries

    def get_security_logs(self) -> list[LogEntry]:
        """Get all security-related logs."""
        return self.get_logs_by_level("SECURITY")


# Global instance
_audit_logger: AuditLogger | None = None


def get_logger() -> AuditLogger:
    """Get or create the global audit logger."""
    global _audit_logger
    if _audit_logger is None:
        _audit_logger = AuditLogger()
    return _audit_logger
