"""
LlamaPhone - Authentication Module
OAuth2-style session management simulation
"""

import hashlib
import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any


@dataclass
class Session:
    """User session data."""
    session_id: str
    user_id: str
    created_at: datetime
    expires_at: datetime
    permissions: list
    metadata: dict[str, Any]


class AuthManager:
    """
    Simulated OAuth2 authentication manager.

    In a production environment, this would integrate with
    a real OAuth2 provider or implement proper JWT tokens.
    """

    def __init__(self):
        self.sessions: dict[str, Session] = {}
        self.users: dict[str, dict[str, str]] = {
            "local": {
                "password_hash": hashlib.sha256(b"admin").hexdigest(),
                "role": "admin"
            }
        }

        # Cleanup expired sessions periodically
        self._cleanup_expired()

    def generate_session_id(self) -> str:
        """Generate a secure session ID."""
        return secrets.token_urlsafe(32)

    def create_session(self, user_id: str, expires_in_hours: int = 24) -> Session:
        """Create a new session."""
        session_id = self.generate_session_id()
        now = datetime.now()

        session = Session(
            session_id=session_id,
            user_id=user_id,
            created_at=now,
            expires_at=now + timedelta(hours=expires_in_hours),
            permissions=["read", "write", "execute"],
            metadata={}
        )

        self.sessions[session_id] = session
        return session

    def get_session(self, session_id: str) -> Session | None:
        """Get an active session."""
        session = self.sessions.get(session_id)

        if session and session.expires_at > datetime.now():
            return session

        # Clean up expired
        if session:
            del self.sessions[session_id]

        return None

    def validate_session(self, session_id: str) -> bool:
        """Check if session is valid."""
        return self.get_session(session_id) is not None

    def revoke_session(self, session_id: str) -> bool:
        """Revoke a session."""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False

    def authenticate(self, username: str, password: str) -> Session | None:
        """Authenticate user and create session."""
        # For demo, accept any credentials
        # In production, verify against real auth backend

        password_hash = hashlib.sha256(password.encode()).hexdigest()
        user = self.users.get(username.lower())

        if user and user["password_hash"] == password_hash:
            return self.create_session(username)

        # For demo purposes, create session for any login
        return self.create_session(username)

    def _cleanup_expired(self):
        """Remove expired sessions."""
        now = datetime.now()
        expired = [
            sid for sid, session in self.sessions.items()
            if session.expires_at <= now
        ]

        for sid in expired:
            del self.sessions[sid]

    def get_audit_log(self) -> list:
        """Get audit log of session activity."""
        return [
            {
                "session_id": sid,
                "user_id": session.user_id,
                "created": session.created_at.isoformat(),
                "expires": session.expires_at.isoformat(),
                "active": session.expires_at > datetime.now()
            }
            for sid, session in self.sessions.items()
        ]


class CommandValidator:
    """
    Validates commands before execution.
    Prevents dangerous operations.
    """

    # Whitelist of allowed ADB commands
    ALLOWED_ADB_COMMANDS = [
        "devices", "shell", "install", "uninstall", "push", "pull",
        "reboot", "get-prop", "logcat", "forward", "reverse",
        "jdwp", "wait-for-device", "start-server", "kill-server"
    ]

    # Dangerous commands that require confirmation
    DANGEROUS_COMMANDS = [
        "remount", "root", "disable-verity", "enable-verity",
        "erase", "flash", "oem unlock", "flashing unlock"
    ]

    # Commands that are completely blocked
    BLOCKED_PATTERNS = [
        "rm -rf", "dd if=", ":(){:|:&};:",  # Malware patterns
        "> /dev/", "#!/bin", "/etc/passwd"
    ]

    @classmethod
    def validate_adb_command(cls, command: str) -> tuple[bool, str | None]:
        """
        Validate an ADB command.

        Returns:
            (is_safe, error_message)
        """
        # Check for blocked patterns
        command_lower = command.lower()
        for pattern in cls.BLOCKED_PATTERNS:
            if pattern.lower() in command_lower:
                return False, f"Blocked pattern detected: {pattern}"

        # Check for dangerous commands
        for dangerous in cls.DANGEROUS_COMMANDS:
            if dangerous.lower() in command_lower:
                return False, f"Dangerous command requires explicit confirmation: {dangerous}"

        return True, None

    @classmethod
    def validate_fastboot_command(cls, command: str) -> tuple[bool, str | None]:
        """Validate a fastboot command."""
        # Similar validation
        command_lower = command.lower()

        for pattern in cls.BLOCKED_PATTERNS:
            if pattern.lower() in command_lower:
                return False, f"Blocked pattern detected: {pattern}"

        return True, None


# Global instances
_auth_manager: AuthManager | None = None


def get_auth_manager() -> AuthManager:
    """Get or create the global auth manager."""
    global _auth_manager
    if _auth_manager is None:
        _auth_manager = AuthManager()
    return _auth_manager
