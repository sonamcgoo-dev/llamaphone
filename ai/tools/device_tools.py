"""
LlamaPhone - Device Tools
Device discovery, port scanning, and network utilities
"""

import concurrent.futures
import contextlib
import platform
import socket
import subprocess
from dataclasses import dataclass
from typing import Any

from ..ollama_client import ToolDefinition


@dataclass
class DiscoveredDevice:
    """A discovered network device."""
    ip: str
    port: int
    mac: str | None = None
    hostname: str | None = None
    manufacturer: str | None = None
    device_type: str = "unknown"


class DeviceDiscoveryTools:
    """Tools for device discovery and network scanning."""

    def __init__(self):
        self.common_adb_ports = [5555, 5554, 5037]
        self.common_device_ports = [22, 80, 443, 8080, 8443]

    def scan_port(self, ip: str, port: int, timeout: float = 1.0) -> bool:
        """Scan a single port on an IP."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((ip, port))
            sock.close()
            return result == 0
        except Exception:
            return False

    def scan_device_ports(self, ip: str, ports: list[int] = None) -> dict[str, Any]:
        """Scan common ADB ports on a device."""
        if ports is None:
            ports = self.common_adb_ports

        results = {"ip": ip, "open_ports": [], "closed_ports": []}

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_port = {
                executor.submit(self.scan_port, ip, port): port
                for port in ports
            }

            for future in concurrent.futures.as_completed(future_to_port):
                port = future_to_port[future]
                try:
                    if future.result():
                        results["open_ports"].append(port)
                except Exception:
                    results["closed_ports"].append(port)

        return results

    def scan_network_range(
        self,
        base_ip: str,
        start: int = 1,
        end: int = 255,
        adb_only: bool = True
    ) -> list[DiscoveredDevice]:
        """Scan a network range for devices."""
        devices = []

        # Parse base IP
        ip_parts = base_ip.rsplit(".", 1)
        if len(ip_parts) != 2:
            return devices

        base = ip_parts[0] + "."
        start_range = int(ip_parts[1]) if isinstance(ip_parts[1], str) else start
        end_range = start_range + (end - start)

        def scan_ip(ip_addr: str) -> DiscoveredDevice | None:
            ports = self.common_adb_ports if adb_only else self.common_device_ports
            result = self.scan_device_ports(ip_addr, ports)

            if result["open_ports"]:
                return DiscoveredDevice(
                    ip=ip_addr,
                    port=result["open_ports"][0],
                    device_type="adb_device" if adb_only else "network_device"
                )
            return None

        ip_list = [f"{base}{i}" for i in range(start_range, min(end_range + 1, 256))]

        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            future_to_ip = {
                executor.submit(scan_ip, ip): ip
                for ip in ip_list
            }

            for future in concurrent.futures.as_completed(future_to_ip):
                try:
                    device = future.result()
                    if device:
                        devices.append(device)
                except Exception:
                    pass

        return devices

    def get_device_hostname(self, ip: str) -> str | None:
        """Get hostname for an IP via reverse DNS."""
        try:
            hostname, _, _ = socket.gethostbyaddr(ip)
            return hostname
        except Exception:
            return None

    def get_local_ip(self) -> str | None:
        """Get the local machine's IP address."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return None

    def get_network_info(self) -> dict[str, Any]:
        """Get local network information."""
        info = {
            "local_ip": self.get_local_ip(),
            "hostname": socket.gethostname(),
            "interfaces": []
        }

        # Try to get network interfaces
        try:
            if platform.system() == "Windows":
                result = subprocess.run(
                    ["ipconfig"],
                    capture_output=True,
                    text=True
                )
            else:
                result = subprocess.run(
                    ["ip", "addr", "show"],
                    capture_output=True,
                    text=True
                )
            info["interfaces"].append(result.stdout)
        except Exception:
            pass

        return info

    def ping_device(self, ip: str, count: int = 2) -> bool:
        """Ping a device to check connectivity."""
        try:
            if platform.system() == "Windows":
                cmd = ["ping", "-n", str(count), "-w", "1000", ip]
            else:
                cmd = ["ping", "-c", str(count), "-W", "1", ip]
            result = subprocess.run(cmd, capture_output=True, timeout=5)
            return result.returncode == 0
        except Exception:
            return False

    def adb_discover(self) -> list[dict[str, Any]]:
        """Discover ADB devices on the local network using mDNS."""
        devices = []

        # Try using adb mdns
        with contextlib.suppress(Exception):
            subprocess.run(
                ["adb", "mdns", "check"],
                capture_output=True,
                text=True,
                timeout=5
            )
            # Parse output if any

        return devices


class HiddenDeviceFinder:
    """Find hidden or hard-to-discover devices."""

    def __init__(self):
        self.manufacturer_oui = self._load_manufacturer_prefixes()

    def _load_manufacturer_prefixes(self) -> dict[str, str]:
        """Load common MAC manufacturer prefixes."""
        return {
            "00:1A:11": "Google",
            "00:1E:58": "HTC",
            "00:21:FE": "Huawei",
            "00:25:00": "Apple",
            "00:26:BB": "Samsung",
            "00:27:0E": "Xiaomi",
            "00:1E:DC": "Nokia",
            "00:1F:E1": "HTC",
            "00:21:4C": "Motorola",
            "00:23:76": "HTC",
            "00:24:90": "HTC",
            "00:26:37": "Huawei",
            "00:26:5C": "Huawei",
            "00:27:09": "Huawei",
            "F8:95:EA": "OnePlus",
            "88:C9:D0": "OnePlus",
            "A4:77:33": "Google",
            "94:EB:2C": "Google",
            "58:2A:F7": "Fairphone",
        }

    def get_manufacturer(self, mac: str) -> str | None:
        """Look up manufacturer from MAC address."""
        if not mac:
            return None

        prefix = mac.upper()[:8]
        return self.manufacturer_oui.get(prefix)

    def is_android_device(self, mac: str) -> bool:
        """Check if MAC appears to be an Android device."""
        if not mac:
            return False

        # Common Android vendor prefixes
        android_prefixes = [
            "00:1A:11",  # Google
            "00:1E:58",  # HTC
            "00:1E:DC",  # Nokia
            "00:1F:E1",  # HTC
            "00:21:FE",  # Huawei
            "00:23:76",  # HTC
            "00:24:90",  # HTC
            "00:25:00",  # Apple
            "00:26:BB",  # Samsung
            "00:26:37",  # Huawei
            "00:26:5C",  # Huawei
            "00:27:0E",  # Xiaomi
            "00:27:09",  # Huawei
            "F8:95:EA",  # OnePlus
            "88:C9:D0",  # OnePlus
            "A4:77:33",  # Google
            "94:EB:2C",  # Google
        ]

        prefix = mac.upper()[:8]
        return prefix in android_prefixes


def get_device_tools() -> list[ToolDefinition]:
    """Get device discovery tool definitions for AI function calling."""
    return [
        ToolDefinition(
            name="scan_device",
            description="Scan a specific IP for open ADB ports",
            parameters={
                "type": "object",
                "properties": {
                    "ip": {"type": "string", "description": "IP address to scan"},
                    "ports": {"type": "array", "items": {"type": "integer"}, "description": "Ports to scan (default: 5555, 5554, 5037)"}
                },
                "required": ["ip"]
            }
        ),
        ToolDefinition(
            name="scan_network",
            description="Scan a network range for devices with open ports",
            parameters={
                "type": "object",
                "properties": {
                    "base_ip": {"type": "string", "description": "Base IP address (e.g., 192.168.1.1)"},
                    "start": {"type": "integer", "description": "Start of range (default: 1)"},
                    "end": {"type": "integer", "description": "End of range (default: 255)"},
                    "adb_only": {"type": "boolean", "description": "Only scan ADB ports (default: true)"}
                },
                "required": ["base_ip"]
            }
        ),
        ToolDefinition(
            name="get_local_ip",
            description="Get the local machine's IP address",
            parameters={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        ToolDefinition(
            name="ping_device",
            description="Ping a device to check connectivity",
            parameters={
                "type": "object",
                "properties": {
                    "ip": {"type": "string", "description": "IP address to ping"},
                    "count": {"type": "integer", "description": "Number of ping attempts (default: 2)"}
                },
                "required": ["ip"]
            }
        ),
        ToolDefinition(
            name="get_device_manufacturer",
            description="Look up device manufacturer from MAC address",
            parameters={
                "type": "object",
                "properties": {
                    "mac": {"type": "string", "description": "MAC address (e.g., AA:BB:CC:DD:EE:FF)"}
                },
                "required": ["mac"]
            }
        ),
        ToolDefinition(
            name="get_network_info",
            description="Get local network information including interfaces",
            parameters={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
    ]


# Global instances
_device_tools: DeviceDiscoveryTools | None = None
_hidden_finder: HiddenDeviceFinder | None = None


def get_device_discovery() -> DeviceDiscoveryTools:
    """Get or create the global device discovery instance."""
    global _device_tools
    if _device_tools is None:
        _device_tools = DeviceDiscoveryTools()
    return _device_tools


def get_hidden_finder() -> HiddenDeviceFinder:
    """Get or create the global hidden device finder."""
    global _hidden_finder
    if _hidden_finder is None:
        _hidden_finder = HiddenDeviceFinder()
    return _hidden_finder
