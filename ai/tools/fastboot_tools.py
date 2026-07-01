"""
LlamaPhone - Fastboot Tools
Fastboot command wrappers for the AI to use
"""

import re
import subprocess
from typing import Any

from ..ollama_client import ToolDefinition


class FastbootTools:
    """Fastboot command execution tools."""

    def __init__(self, fastboot_path: str = "fastboot"):
        self.fastboot_path = fastboot_path

    def _run_command(self, args: list[str], timeout: int = 60) -> dict[str, Any]:
        """Run a fastboot command and return the result."""
        cmd = [self.fastboot_path] + args

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout
            )

            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr,
                "return_code": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "output": "",
                "error": "Command timed out",
                "return_code": -1
            }
        except FileNotFoundError:
            return {
                "success": False,
                "output": "",
                "error": f"Fastboot not found at: {self.fastboot_path}",
                "return_code": -1
            }
        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": str(e),
                "return_code": -1
            }

    def devices(self) -> dict[str, Any]:
        """List all devices in fastboot mode."""
        return self._run_command(["devices"])

    def reboot(self) -> dict[str, Any]:
        """Reboot device from fastboot."""
        return self._run_command(["reboot"])

    def reboot_bootloader(self) -> dict[str, Any]:
        """Reboot to bootloader."""
        return self._run_command(["reboot-bootloader"])

    def reboot_recovery(self) -> dict[str, Any]:
        """Boot to recovery."""
        return self._run_command(["reboot", "recovery"])

    def unlock(self) -> dict[str, Any]:
        """Unlock the bootloader (generic)."""
        return self._run_command(["oem", "unlock"])

    def lock(self) -> dict[str, Any]:
        """Lock the bootloader."""
        return self._run_command(["oem", "lock"])

    def flashing_unlock(self) -> dict[str, Any]:
        """Unlock flashing (Pixel/Samsung devices)."""
        return self._run_command(["flashing", "unlock"])

    def flashing_lock(self) -> dict[str, Any]:
        """Lock flashing."""
        return self._run_command(["flashing", "lock"])

    def flash(self, partition: str, image: str) -> dict[str, Any]:
        """Flash a partition with an image."""
        return self._run_command(["flash", partition, image])

    def flash_all(self, zip_path: str) -> dict[str, Any]:
        """Flash all partitions from a zip (Samsung)."""
        return self._run_command(["update", zip_path])

    def erase(self, partition: str) -> dict[str, Any]:
        """Erase a partition."""
        return self._run_command(["erase", partition])

    def getvar(self, variable: str) -> dict[str, Any]:
        """Get a bootloader variable."""
        result = self._run_command(["getvar", variable])
        # Fastboot writes getvar output to stderr, not stdout
        output_to_parse = result["error"] if result["error"] else result["output"]
        match = re.search(rf"{variable}:\s*(.+)", output_to_parse)
        if match:
            result["value"] = match.group(1).strip()
        return result

    def oem(self, command: str) -> dict[str, Any]:
        """Execute an OEM command."""
        return self._run_command(["oem", command])

    def boot(self, kernel: str) -> dict[str, Any]:
        """Boot a kernel image without flashing."""
        return self._run_command(["boot", kernel])

    def flash_lockscreen(self, image: str) -> dict[str, Any]:
        """Flash lockscreen credential."""
        return self._run_command(["flashing", "unlock_critical"])

    def device_info(self) -> dict[str, Any]:
        """Get comprehensive device info via fastboot."""
        info = {}

        variables = [
            "version", "version-bootloader", "version-baseband",
            "product", "board", "bootloader", "carrier", "serialno",
            "secure", "slot-count", "current-slot"
        ]

        for var in variables:
            result = self.getvar(var)
            if result["success"] and "value" in result:
                info[var] = result["value"]

        return info

    def wipe_data(self) -> dict[str, Any]:
        """Wipe userdata (factory reset from fastboot)."""
        return self._run_command(["-w"])

    def set_active(self, slot: str) -> dict[str, Any]:
        """Set active slot (a or b)."""
        return self._run_command(["set_active", slot])


def get_fastboot_tools() -> list[ToolDefinition]:
    """Get Fastboot tool definitions for AI function calling."""
    return [
        ToolDefinition(
            name="fastboot_devices",
            description="List all devices in fastboot mode",
            parameters={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        ToolDefinition(
            name="fastboot_reboot",
            description="Reboot device from fastboot mode",
            parameters={
                "type": "object",
                "properties": {
                    "mode": {"type": "string", "description": "Reboot mode: 'bootloader', 'recovery', or empty for normal"}
                },
                "required": []
            }
        ),
        ToolDefinition(
            name="fastboot_unlock",
            description="Unlock the device bootloader",
            parameters={
                "type": "object",
                "properties": {
                    "method": {"type": "string", "description": "Unlock method: 'oem', 'flashing', or 'generic'"}
                },
                "required": []
            }
        ),
        ToolDefinition(
            name="fastboot_lock",
            description="Lock the device bootloader",
            parameters={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        ToolDefinition(
            name="fastboot_flash",
            description="Flash a partition with an image file",
            parameters={
                "type": "object",
                "properties": {
                    "partition": {"type": "string", "description": "Partition name: boot, recovery, system, vendor, etc."},
                    "image": {"type": "string", "description": "Path to the image file to flash"}
                },
                "required": ["partition", "image"]
            }
        ),
        ToolDefinition(
            name="fastboot_erase",
            description="Erase a partition",
            parameters={
                "type": "object",
                "properties": {
                    "partition": {"type": "string", "description": "Partition to erase"}
                },
                "required": ["partition"]
            }
        ),
        ToolDefinition(
            name="fastboot_getvar",
            description="Get a bootloader variable value",
            parameters={
                "type": "object",
                "properties": {
                    "variable": {"type": "string", "description": "Variable name: version, bootloader, product, secure, etc."}
                },
                "required": ["variable"]
            }
        ),
        ToolDefinition(
            name="fastboot_wipe",
            description="Wipe userdata (factory reset from fastboot)",
            parameters={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        ToolDefinition(
            name="fastboot_device_info",
            description="Get comprehensive device information from fastboot",
            parameters={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
    ]


# Global instance
_fastboot_tools: FastbootTools | None = None


def get_fastboot_instance(fastboot_path: str = "fastboot") -> FastbootTools:
    """Get or create the global Fastboot tools instance."""
    global _fastboot_tools
    if _fastboot_tools is None:
        _fastboot_tools = FastbootTools(fastboot_path)
    return _fastboot_tools
