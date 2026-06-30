"""
LlamaPhone - ADB Tools
ADB command wrappers for the AI to use
"""

import subprocess
from dataclasses import dataclass
from typing import Any

from ..ollama_client import ToolDefinition


@dataclass
class ADBResult:
    """Result from an ADB command."""
    success: bool
    output: str
    error: str
    return_code: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "output": self.output,
            "error": self.error,
            "return_code": self.return_code
        }


class ADBTools:
    """ADB command execution tools."""

    def __init__(self, adb_path: str = "adb"):
        self.adb_path = adb_path

    def _run_command(self, args: list[str], timeout: int = 30) -> ADBResult:
        """Run an ADB command and return the result."""
        cmd = [self.adb_path] + args

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout
            )

            return ADBResult(
                success=result.returncode == 0,
                output=result.stdout,
                error=result.stderr,
                return_code=result.returncode
            )
        except subprocess.TimeoutExpired:
            return ADBResult(
                success=False,
                output="",
                error="Command timed out",
                return_code=-1
            )
        except FileNotFoundError:
            return ADBResult(
                success=False,
                output="",
                error=f"ADB not found at: {self.adb_path}",
                return_code=-1
            )
        except Exception as e:
            return ADBResult(
                success=False,
                output="",
                error=str(e),
                return_code=-1
            )

    def devices(self) -> ADBResult:
        """List all connected ADB devices."""
        return self._run_command(["devices", "-l"])

    def connect(self, ip: str, port: int = 5555) -> ADBResult:
        """Connect to a device over WiFi."""
        return self._run_command(["connect", f"{ip}:{port}"])

    def disconnect(self, ip: str | None = None) -> ADBResult:
        """Disconnect from a device."""
        if ip:
            return self._run_command(["disconnect", ip])
        return self._run_command(["disconnect"])

    def shell(self, device_id: str | None, command: str, timeout: int = 30) -> ADBResult:
        """Execute a shell command on the device."""
        args = []
        if device_id:
            args.extend(["-s", device_id])
        args.extend(["shell", command])
        return self._run_command(args, timeout=timeout)

    def install(self, device_id: str | None, apk_path: str, grant_perms: bool = True) -> ADBResult:
        """Install an APK on the device."""
        args = []
        if device_id:
            args.extend(["-s", device_id])
        args.append("install")
        if grant_perms:
            args.append("-g")
        args.append(apk_path)
        return self._run_command(args, timeout=120)

    def uninstall(self, device_id: str | None, package: str, keep_data: bool = False) -> ADBResult:
        """Uninstall an app from the device."""
        args = []
        if device_id:
            args.extend(["-s", device_id])
        args.append("uninstall")
        if keep_data:
            args.append("-k")
        args.append(package)
        return self._run_command(args)

    def push(self, device_id: str | None, local: str, remote: str) -> ADBResult:
        """Push a file to the device."""
        args = []
        if device_id:
            args.extend(["-s", device_id])
        args.extend(["push", local, remote])
        return self._run_command(args, timeout=120)

    def pull(self, device_id: str | None, remote: str, local: str) -> ADBResult:
        """Pull a file from the device."""
        args = []
        if device_id:
            args.extend(["-s", device_id])
        args.extend(["pull", remote, local])
        return self._run_command(args, timeout=120)

    def reboot(self, device_id: str | None, mode: str = "") -> ADBResult:
        """Reboot the device."""
        args = []
        if device_id:
            args.extend(["-s", device_id])
        args.append("reboot")
        if mode:
            args.append(mode)
        return self._run_command(args)

    def get_prop(self, device_id: str | None, property: str) -> ADBResult:
        """Get a system property."""
        return self.shell(device_id, f"getprop {property}")

    def set_prop(self, device_id: str | None, property: str, value: str) -> ADBResult:
        """Set a system property (requires root)."""
        return self.shell(device_id, f"setprop {property} {value}")

    def logcat(self, device_id: str | None, options: str = "-d", timeout: int = 30) -> ADBResult:
        """Get device logcat."""
        args = []
        if device_id:
            args.extend(["-s", device_id])
        args.extend(["logcat", "-d"])
        return self._run_command(args, timeout=timeout)

    def get_serialno(self, device_id: str | None) -> str | None:
        """Get device serial number."""
        result = self.shell(device_id, "getprop ro.serialno")
        if result.success:
            return result.output.strip()

        result = self.shell(device_id, "settings get secure android_id")
        if result.success:
            return result.output.strip()

        return None

    def get_model(self, device_id: str | None) -> str | None:
        """Get device model."""
        result = self.shell(device_id, "getprop ro.product.model")
        if result.success:
            return result.output.strip()
        return None

    def get_manufacturer(self, device_id: str | None) -> str | None:
        """Get device manufacturer."""
        result = self.shell(device_id, "getprop ro.product.manufacturer")
        if result.success:
            return result.output.strip()
        return None

    def get_android_version(self, device_id: str | None) -> str | None:
        """Get Android version."""
        result = self.shell(device_id, "getprop ro.build.version.release")
        if result.success:
            return result.output.strip()
        return None

    def get_device_info(self, device_id: str | None = None) -> dict[str, Any]:
        """Get comprehensive device information."""
        info = {}

        info["serial"] = self.get_serialno(device_id)
        info["model"] = self.get_model(device_id)
        info["manufacturer"] = self.get_manufacturer(device_id)
        info["android_version"] = self.get_android_version(device_id)

        # Build info
        result = self.shell(device_id, "getprop ro.build.display.id")
        info["build"] = result.output.strip() if result.success else "Unknown"

        # Security patch
        result = self.shell(device_id, "getprop ro.build.version.security_patch")
        info["security_patch"] = result.output.strip() if result.success else "Unknown"

        # Battery status
        result = self.shell(device_id, "dumpsys battery")
        if result.success:
            for line in result.output.split("\n"):
                if "level:" in line:
                    info["battery_level"] = line.split(":")[1].strip()
                if "status:" in line:
                    info["battery_status"] = line.split(":")[1].strip()

        return info


def get_adb_tools() -> list[ToolDefinition]:
    """Get ADB tool definitions for AI function calling."""
    return [
        ToolDefinition(
            name="adb_list_devices",
            description="List all connected ADB devices with details",
            parameters={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        ToolDefinition(
            name="adb_connect",
            description="Connect to a device over WiFi",
            parameters={
                "type": "object",
                "properties": {
                    "ip": {"type": "string", "description": "Device IP address"},
                    "port": {"type": "integer", "description": "Port number (default: 5555)"}
                },
                "required": ["ip"]
            }
        ),
        ToolDefinition(
            name="adb_shell",
            description="Execute a shell command on the device",
            parameters={
                "type": "object",
                "properties": {
                    "device_id": {"type": "string", "description": "Device serial (optional)"},
                    "command": {"type": "string", "description": "Shell command to execute"}
                },
                "required": ["command"]
            }
        ),
        ToolDefinition(
            name="adb_install",
            description="Install an APK on the device",
            parameters={
                "type": "object",
                "properties": {
                    "device_id": {"type": "string", "description": "Device serial (optional)"},
                    "apk_path": {"type": "string", "description": "Path to APK file"}
                },
                "required": ["apk_path"]
            }
        ),
        ToolDefinition(
            name="adb_uninstall",
            description="Uninstall an app from the device",
            parameters={
                "type": "object",
                "properties": {
                    "device_id": {"type": "string", "description": "Device serial (optional)"},
                    "package": {"type": "string", "description": "Package name to uninstall"}
                },
                "required": ["package"]
            }
        ),
        ToolDefinition(
            name="adb_push",
            description="Push a file to the device",
            parameters={
                "type": "object",
                "properties": {
                    "device_id": {"type": "string", "description": "Device serial (optional)"},
                    "local_path": {"type": "string", "description": "Local file path"},
                    "remote_path": {"type": "string", "description": "Remote destination path"}
                },
                "required": ["local_path", "remote_path"]
            }
        ),
        ToolDefinition(
            name="adb_pull",
            description="Pull a file from the device",
            parameters={
                "type": "object",
                "properties": {
                    "device_id": {"type": "string", "description": "Device serial (optional)"},
                    "remote_path": {"type": "string", "description": "Remote file path"},
                    "local_path": {"type": "string", "description": "Local destination path"}
                },
                "required": ["remote_path", "local_path"]
            }
        ),
        ToolDefinition(
            name="adb_reboot",
            description="Reboot the device",
            parameters={
                "type": "object",
                "properties": {
                    "device_id": {"type": "string", "description": "Device serial (optional)"},
                    "mode": {"type": "string", "description": "Reboot mode: 'recovery', 'bootloader', 'fastboot', 'edl', or empty for normal"}
                },
                "required": []
            }
        ),
        ToolDefinition(
            name="adb_get_device_info",
            description="Get comprehensive device information including model, Android version, etc.",
            parameters={
                "type": "object",
                "properties": {
                    "device_id": {"type": "string", "description": "Device serial (optional)"}
                },
                "required": []
            }
        ),
        ToolDefinition(
            name="adb_logcat",
            description="Get device logcat output",
            parameters={
                "type": "object",
                "properties": {
                    "device_id": {"type": "string", "description": "Device serial (optional)"}
                },
                "required": []
            }
        ),
    ]


# Global instance
_adb_tools: ADBTools | None = None


def get_adb_instance(adb_path: str = "adb") -> ADBTools:
    """Get or create the global ADB tools instance."""
    global _adb_tools
    if _adb_tools is None:
        _adb_tools = ADBTools(adb_path)
    return _adb_tools
