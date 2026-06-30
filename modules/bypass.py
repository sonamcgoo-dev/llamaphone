"""
LlamaPhone - Bypass Module
FRP, screen lock, and network bypass procedures
"""

import subprocess
from dataclasses import dataclass
from enum import Enum
from typing import Any


class BypassType(Enum):
    """Types of bypass operations."""
    FRP = "frp"
    SCREEN_LOCK = "screen_lock"
    NETWORK_LOCK = "network_lock"
    ACTIVATION = "activation"
    OEM_UNLOCK = "oem_unlock"


@dataclass
class BypassResult:
    """Result from a bypass operation."""
    success: bool
    method: str
    message: str
    steps: list[str] = None
    warnings: list[str] = None

    def __post_init__(self):
        if self.steps is None:
            self.steps = []
        if self.warnings is None:
            self.warnings = []


class BypassModule:
    """Module for handling bypass operations."""

    def __init__(self, adb_path: str = "adb"):
        self.adb_path = adb_path

    def check_frp_status(self, device_id: str | None = None) -> dict[str, Any]:
        """Check FRP status on the device."""
        args = []
        if device_id:
            args.extend(["-s", device_id])
        args.extend(["shell", "settings", "get", "secure", "android_id"])

        result = subprocess.run(
            [self.adb_path] + args,
            capture_output=True,
            text=True
        )

        android_id = result.stdout.strip() if result.returncode == 0 else None

        return {
            "frp_enabled": android_id is not None and len(android_id) > 0,
            "android_id": android_id,
            "device_has_account": android_id is not None
        }

    def get_bypass_methods(self, device_manufacturer: str, android_version: str) -> list[dict[str, Any]]:
        """Get available bypass methods for a device."""
        methods = []

        # Generic methods
        methods.extend([
            {
                "name": "Account Recovery (Google)",
                "description": "Use Google's account recovery after 72 hours",
                "safety": "safe",
                "requires_wait": True,
                "wait_time": "72 hours"
            },
            {
                "name": "OEM Specific Methods",
                "description": "Manufacturer-specific bypass techniques",
                "safety": "moderate",
                "requires_root": False
            }
        ])

        # Samsung methods
        if device_manufacturer.lower() == "samsung":
            methods.extend([
                {
                    "name": "Samsung Emergency Dialer",
                    "description": "Access emergency dialer and hidden menus",
                    "safety": "safe",
                    "steps": ["Dial *#0*#", "Navigate to test menus"]
                },
                {
                    "name": "Samsung Find My Mobile",
                    "description": "Use Samsung's remote unlock feature",
                    "safety": "safe",
                    "requires_account": True
                }
            ])

        # Xiaomi methods
        elif device_manufacturer.lower() == "xiaomi":
            methods.extend([
                {
                    "name": "Mi Account Recovery",
                    "description": "Official Xiaomi account recovery",
                    "safety": "safe",
                    "requires_wait": True,
                    "wait_time": "72-168 hours"
                },
                {
                    "name": "Xiaomi FRP Tool",
                    "description": "Use Mi FRP bypass tool",
                    "safety": "moderate",
                    "requires_pc": True
                }
            ])

        # Google/Pixel methods
        elif device_manufacturer.lower() == "google":
            methods.extend([
                {
                    "name": "Google Account Recovery",
                    "description": "Standard Google account recovery process",
                    "safety": "safe",
                    "requires_wait": True,
                    "wait_time": "72 hours"
                }
            ])

        return methods

    def bypass_frp_generic(self, device_id: str | None = None) -> BypassResult:
        """Generic FRP bypass attempt."""
        warnings = [
            "⚠️ WARNING: Only bypass FRP on devices you own!",
            "Bypassing FRP on stolen devices is illegal.",
            "This may not work on all devices and Android versions."
        ]

        return BypassResult(
            success=False,
            method="generic",
            message="Generic bypass requires specific device methods.",
            steps=[
                "1. Boot to recovery mode",
                "2. Wipe data/factory reset",
                "3. Setup device with new account",
                "Or use manufacturer-specific methods"
            ],
            warnings=warnings
        )

    def bypass_frp_samsung(self, device_id: str | None = None) -> BypassResult:
        """Samsung FRP bypass."""
        return BypassResult(
            success=True,
            method="samsung",
            message="Samsung FRP bypass methods available.",
            steps=[
                "Method 1: Emergency Dialer",
                "  1. From lock screen, tap Emergency Call",
                "  2. Dial #0# or *#0*#",
                "  3. Navigate to test menus",
                "",
                "Method 2: Smart Switch (if enabled)",
                "  1. Download Smart Switch on PC",
                "  2. Connect device",
                "  3. Use emergency recovery option",
                "",
                "Method 3: Odin Mode (last resort)",
                "  1. Boot to download mode",
                "  2. Flash stock firmware via Odin",
                "  3. This resets FRP"
            ],
            warnings=[
                "⚠️ Only use on devices you own legally!"
            ]
        )

    def bypass_screen_lock(self, device_id: str | None = None) -> BypassResult:
        """Screen lock bypass."""
        return BypassResult(
            success=True,
            method="screen_lock",
            message="Screen lock bypass procedures.",
            steps=[
                "⚠️ WARNING: These methods will likely erase data!",
                "",
                "Method 1: ADB (if USB debugging enabled)",
                "  1. Connect device via USB",
                "  2. Run: adb shell rm /data/system/*.key",
                "  3. Reboot device",
                "",
                "Method 2: Recovery Mode",
                "  1. Boot to recovery",
                "  2. Wipe data/factory reset",
                "  3. Reboot",
                "",
                "Method 3: Find My Device (Google)",
                "  1. Visit google.com/android/find",
                "  2. Select device",
                "  3. Select 'Erase Device'",
                "",
                "⚠️ All methods may result in data loss!"
            ],
            warnings=[
                "Data loss is likely",
                "Only proceed if you have no other options",
                "Ensure you own the device legally"
            ]
        )

    def unlock_network_sim(self, device_id: str | None = None) -> BypassResult:
        """Network/SIM unlock."""
        return BypassResult(
            success=True,
            method="network_unlock",
            message="Network unlock options.",
            steps=[
                "Method 1: Contact Carrier (Recommended)",
                "  - Request unlock from your carrier",
                "  - Usually free after contract completion",
                "",
                "Method 2: IMEI Check",
                "  - Dial *#06# to get IMEI",
                "  - Check if already unlocked",
                "",
                "Method 3: Unlock Code",
                "  - Use IMEI to get unlock code",
                "  - Dial: *#*# unlock #*#*",
                "",
                "Method 4: Third-party Services",
                "  - Use reputable unlock service",
                "  - Provide IMEI and carrier info",
                "  - Wait for unlock code"
            ],
            warnings=[
                "Use only reputable services",
                "Never provide unlock codes to strangers"
            ]
        )

    def enable_oem_unlock(self, device_id: str | None = None) -> BypassResult:
        """Guide to enable OEM unlock."""
        return BypassResult(
            success=True,
            method="oem_unlock_guide",
            message="How to enable OEM unlocking.",
            steps=[
                "1. Enable Developer Options:",
                "   Settings > About Phone > Tap Build Number 7 times",
                "",
                "2. Enable OEM Unlock:",
                "   Settings > Developer Options > OEM Unlocking",
                "",
                "3. Connect device in normal mode (not fastboot)",
                "",
                "4. Boot to fastboot:",
                "   Power off > Hold Power + Volume Down",
                "",
                "5. Unlock bootloader:",
                "   fastboot flashing unlock",
                "   (or fastboot oem unlock for some devices)",
                "",
                "⚠️ WARNING: This will WIPE ALL DATA!"
            ],
            warnings=[
                "Unlocking bootloader erases all data",
                "May void warranty",
                "Device security is reduced"
            ]
        )


# Global instance
_bypass_module: BypassModule | None = None


def get_bypass_module() -> BypassModule:
    """Get or create the global bypass module."""
    global _bypass_module
    if _bypass_module is None:
        _bypass_module = BypassModule()
    return _bypass_module
