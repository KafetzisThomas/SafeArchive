import os
import json
import platform
from pathlib import Path

SETTINGS_PATH = Path("settings.json")

DEFAULT_CONFIG = {
    "source_paths": [  # type: list of strings
        str(Path('~/Desktop').expanduser()) + "/",
        str(Path('~/Documents').expanduser()) + "/",
        str(Path('~/Downloads').expanduser()) + "/",
    ],
    "destination_path": (  # type: string
        os.path.abspath(os.sep).replace("\\", "/") if platform.system() == "Windows" else str(Path("~").expanduser())
    ),
    "compression_method": "ZIP_DEFLATED",  # type: string
    "compression_level": "5",  # 1: fast process, 9: small file size, type: integer
    "backup_expiry_date": "Forever",  # type: string
    "backup_interval": False,  # automatic backup frequency (specify: hours), type: boolean
    "encryption": False,  # type: boolean
    "ftp": False,  # type: boolean
    "ftp_hostname": "",  # type: string
    "ftp_username": "",  # type: string
    "ftp_password": "",  # type: string
}

class Config:
    """
    JSON backed configuration manager.
    Automatically create the config file on first run.
    """
    def __init__(self, path: Path, defaults: dict):
        self.path = path
        self.data = defaults.copy()
        self.load_or_create()

    def load_or_create(self):
        """
        Load or create the config file.
        """
        if self.path.exists():
            with open(self.path, "r", encoding="utf-8") as f:
                self.data.update(json.load(f))
        else:
            self.save()

    def save(self):
        """
        Persist the current configuration to disk.
        """
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2)

    def get(self, key, default=None):
        """
        Retrieve a configuration value.
        """
        return self.data.get(key, default)

    def set(self, key, value):
        """
        Triggers whenever a value is set.
        """
        self.data[key] = value
        self.save()

    def delete(self, key):
        """
        Triggers whenever a value is deleted.
        """
        self.data.pop(key, None)
        self.save()

config = Config(SETTINGS_PATH, DEFAULT_CONFIG)
