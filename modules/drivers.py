"""
LlamaPhone - Drivers Module
Driver database and management
"""

import os
import sqlite3
from dataclasses import dataclass


@dataclass
class Driver:
    """Driver information."""
    id: int
    name: str
    manufacturer: str
    device_models: list[str]
    chipset: str | None
    android_version: str | None
    download_url: str
    file_size: str | None
    version: str | None
    file_type: str  # inf, apk, zip
    checksum: str | None
    install_instructions: str | None


class DriverDatabase:
    """Database of device drivers."""

    def __init__(self, db_path: str | None = None):
        self.db_path = db_path or os.path.join(
            os.path.dirname(__file__), "..", "data", "drivers.db"
        )
        self.conn = None
        self._init_db()

    def _init_db(self):
        """Initialize the database."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS drivers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                manufacturer TEXT NOT NULL,
                device_models TEXT,
                chipset TEXT,
                android_version TEXT,
                download_url TEXT NOT NULL,
                file_size TEXT,
                version TEXT,
                file_type TEXT,
                checksum TEXT,
                install_instructions TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        self.conn.commit()

        # Add sample data if empty
        cursor.execute("SELECT COUNT(*) FROM drivers")
        if cursor.fetchone()[0] == 0:
            self._add_sample_drivers()

    def _add_sample_drivers(self):
        """Add sample driver data."""
        sample_drivers = [
            # Samsung
            ("Samsung USB Driver", "Samsung",
             "Galaxy S series, A series, Note series, Tab series",
             "Various", "Android 4.0+",
             "https://developer.samsung.com/android/others/Samsung_USB_Driver_1.5.65.0.zip",
             "15 MB", "1.5.65.0", "exe", None,
             "Run installer, follow prompts, restart PC"),

            ("Samsung KIES", "Samsung",
             "Galaxy S2, S3, Note 2 (older devices)",
             "Various", "Android 2.x-4.x",
             "https://www.samsung.com/us/support/owners/app/kies",
             "150 MB", "3.0", "exe", None,
             "Full software suite, install all components"),

            # Google/Pixel
            ("Google USB Driver", "Google",
             "Pixel series, Nexus devices, Android devices with stock ROM",
             "Qualcomm, MediaTek", "Android 5.0+",
             "https://developer.android.com/studio/run/win-usb",
             "10 MB", "11.0.0", "exe", None,
             "Enable USB debugging, install driver manually from Device Manager"),

            # Qualcomm
            ("Qualcomm USB Driver", "Qualcomm",
             "Devices with Qualcomm Snapdragon chipsets",
             "Snapdragon 200/400/600/700/800 series", "Android 5.0+",
             "https://www.qualcomm.com/media/documents/files/qualcomm-usb-driver-installer.zip",
             "8 MB", "1.0", "exe", None,
             "Run installer as administrator"),

            ("QPST Tool", "Qualcomm",
             "Qualcomm devices for EDL/9008 mode flashing",
             "Snapdragon all series", "All",
             "https://qpsttool.com/",
             "50 MB", "2.7.496", "exe", None,
             "Install QPST, connect device in EDL mode"),

            # MediaTek
            ("MediaTek USB Driver", "MediaTek",
             "Devices with MediaTek chipsets",
             "MT6735, MT6750, MT6795, MT6771, etc.", "Android 5.0+",
             "https://download.mediatek.com.tw/driver/MTK_USB_DRIVER.zip",
             "12 MB", "1.1.4", "exe", None,
             "Install VCOM drivers before flashing"),

            ("SP Flash Tool", "MediaTek",
             "MediaTek devices firmware flashing",
             "All MediaTek", "All",
             "https://spflashtool.com/",
             "40 MB", "5.x", "exe", None,
             "Load scatter file, select firmware, flash"),

            # Xiaomi
            ("Xiaomi USB Driver", "Xiaomi",
             "Xiaomi Mi, Redmi, POCO series",
             "Qualcomm, MediaTek", "Android 6.0+",
             "https://xiaomifirmware.com/downloads/",
             "20 MB", "1.0.4", "exe", None,
             "Install driver before connecting device"),

            # OnePlus
            ("OnePlus USB Driver", "OnePlus",
             "OnePlus One, 2, 3, 3T, 5, 5T, 6, 6T, 7, 8, 9, 10, 11 series",
             "Qualcomm Snapdragon", "Android 5.0+",
             "https://www.oneplus.com/support/software-program",
             "15 MB", "2.0", "exe", None,
             "Install and enable USB debugging"),

            # Huawei
            ("HiSuite (Huawei)", "Huawei",
             "Huawei Mate, P, Nova, Honor series",
             "Kirin 900/800/700 series", "Android 5.0+",
             "https://consumer.huawei.com/en/support/hisuite/",
             "80 MB", "13.0", "exe", None,
             "Install HiSuite, connect device with USB debugging"),

            # Sony
            ("Sony Flash Tool Drivers", "Sony",
             "Xperia XZ, XA, X, Z series",
             "Qualcomm Snapdragon", "Android 6.0+",
             "https://developer.sonymobile.com/downloads/tool/sony-mobile-development-tools/",
             "25 MB", "1.0", "exe", None,
             "Install Sony companion or XperiFirm"),

            # LG
            ("LG United Mobile Driver", "LG",
             "LG G series, V series, K series",
             "Qualcomm Snapdragon", "Android 4.0+",
             "https://www.lge.com/in/software-resource",
             "18 MB", "5.0.0", "exe", None,
             "Run installer, connect device in debugging mode"),

            # Motorola
            ("Motorola USB Driver", "Motorola",
             "Moto G, E, X, Z series",
             "Qualcomm Snapdragon", "Android 5.0+",
             "https://support.motorola.com/us/en/",
             "14 MB", "6.4.0", "exe", None,
             "Install driver from device manager or support site"),

            # Nokia
            ("Nokia USB Driver", "Nokia",
             "Nokia 6, 7, 8 series, Nokia X series",
             "Qualcomm Snapdragon", "Android 7.0+",
             "https://www.nokia.com/phones/usb-drivers/",
             "10 MB", "1.0.2", "exe", None,
             "Download and install from Nokia support site"),

            # ASUS
            ("ASUS USB Driver", "ASUS",
             "ZenFone series, ROG Phone",
             "Qualcomm Snapdragon, Intel", "Android 5.0+",
             "https://www.asus.com/supportonly/",
             "22 MB", "1.0.1", "exe", None,
             "Install from ASUS support site"),

            # OPPO/Realme
            ("OPPO/Realme USB Driver", "OPPO",
             "OPPO Find, Reno, F series; Realme C, X, Narzo series",
             "MediaTek, Qualcomm", "Android 5.0+",
             "https://www.oppo.com/en/software/",
             "16 MB", "1.0.3", "exe", None,
             "Install driver before using flashing tools"),

            # Vivo
            ("Vivo USB Driver", "Vivo",
             "Vivo X, V, Y series",
             "Qualcomm, MediaTek", "Android 5.0+",
             "https://www.vivo.com.in/support/software-detail",
             "18 MB", "1.0.2", "exe", None,
             "Install before using Vivo firmware tools"),
        ]

        cursor = self.conn.cursor()
        cursor.executemany("""
            INSERT INTO drivers
            (name, manufacturer, device_models, chipset, android_version,
             download_url, file_size, version, file_type, install_instructions)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, sample_drivers)

        self.conn.commit()

    def search(self, query: str, manufacturer: str | None = None) -> list[Driver]:
        """Search for drivers."""
        cursor = self.conn.cursor()

        sql = """
            SELECT * FROM drivers
            WHERE (name LIKE ? OR device_models LIKE ? OR manufacturer LIKE ?)
        """
        params = [f"%{query}%", f"%{query}%", f"%{query}%"]

        if manufacturer:
            sql += " AND manufacturer LIKE ?"
            params.append(f"%{manufacturer}%")

        cursor.execute(sql, params)

        drivers = []
        for row in cursor.fetchall():
            drivers.append(Driver(
                id=row[0],
                name=row[1],
                manufacturer=row[2],
                device_models=row[3].split(", ") if row[3] else [],
                chipset=row[4],
                android_version=row[5],
                download_url=row[6],
                file_size=row[7],
                version=row[8],
                file_type=row[9],
                checksum=row[10],
                install_instructions=row[11]
            ))

        return drivers

    def get_by_manufacturer(self, manufacturer: str) -> list[Driver]:
        """Get all drivers for a manufacturer."""
        return self.search("", manufacturer=manufacturer)

    def get_all_manufacturers(self) -> list[str]:
        """Get list of all manufacturers."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT manufacturer FROM drivers ORDER BY manufacturer")
        return [row[0] for row in cursor.fetchall()]

    def add_driver(self, driver: Driver) -> int:
        """Add a new driver."""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO drivers
            (name, manufacturer, device_models, chipset, android_version,
             download_url, file_size, version, file_type, checksum, install_instructions)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            driver.name, driver.manufacturer,
            ", ".join(driver.device_models) if driver.device_models else None,
            driver.chipset, driver.android_version,
            driver.download_url, driver.file_size, driver.version,
            driver.file_type, driver.checksum, driver.install_instructions
        ))
        self.conn.commit()
        return cursor.lastrowid

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()


# Global instance
_driver_db: DriverDatabase | None = None


def get_driver_database(db_path: str | None = None) -> DriverDatabase:
    """Get or create the global driver database."""
    global _driver_db
    if _driver_db is None:
        _driver_db = DriverDatabase(db_path)
    return _driver_db
