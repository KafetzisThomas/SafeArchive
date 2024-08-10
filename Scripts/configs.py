#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
This file manages configurations and provides functionality to save and load them as well.
It also automatically triggers the saving of the configuration file whenever a setting is changed or deleted.
"""

import os
import json
import platform
import colorama
from pathlib import Path
from colorama import Fore as F

colorama.init(autoreset=True)


class ConfigDict(dict):
    """Set configs & save every time a setting changes"""
    __slots__ = ["path"]

    def __init__(self, config: dict, path: str):
        self.update(config)
        self.path = Path(path)

    def __setitem__(self, key, value):
        """Triggers whenever a value is set"""
        super().__setitem__(key, value)
        self.save()

    def __delitem__(self, key):
        """Triggers whenever a value is deleted"""
        super().__delitem__(key)
        self.save()

    def save(self):
        """Saves the config file to the given path"""
        with open(self.path, 'w') as file:
            json.dump(self, file, indent=2)

    def load(self):
        """Loads the config file from the given path"""
        with open(self.path, 'r') as file:
            self.update(json.load(file))


SETTINGS_PATH = 'settings.json'
config = ConfigDict({
    "_comments": {
        "platform": "Get name of operating system (Windows, Linux, macOS)",
        "source_paths": "List of source paths (local folders) for backups (type: list with strings)",
        "destination_path": "Destination path (storage media) for backups (type: string)",
        "notifications": "Enable/Disable notifications (type: boolean)",
        "encryption": "Enable/Disable encryption on backups (type: boolean)",
        "system_tray": "Enable or disable system tray [Windows] (type: boolean)",
        "appearance_mode": "Appearance mode for the application (type: string)",
        "color_theme": "Color theme for the application (type: string)",
        "backup_expiry_date": "Expiry date for the backups in the storage media (type: string)",
        "storage_provider": "Storage provider for backups (Google Drive / FTP) (type: string)",
        "compression_method": "Specify the compression method for your backups (type: string)",
        "allowZip64": "Enable/Disable zip files (backups) to extend larger than 4 GiB (type: boolean)",
        "compression_level": "Specify compression level for zip files (backups) - 1: fast, 9: small size (type: integer)",
        "backup_interval": "Set automatic backup frequency (specify: hours) (type: integer)",
        "ftp_hostname": "Hostname for FTP configuration (type: string)",
        "ftp_username": "Username for FTP configuration (type: string)",
        "ftp_password": "Password for FTP configuration (type: string)",
        "mega_email": "Email for Mega login (type: string)",
        "mega_password": "Password for Mega login (type: string)",
        "dropbox_access_token": "Access Dropbox account using token with individual scopes (type: string)"
  },
    "platform": platform.system(),
    "source_paths": [
        str(Path('~/Desktop').expanduser()).replace("\\", "/") + "/",
        str(Path('~/Documents').expanduser()).replace("\\", "/") + "/",
        str(Path('~/Downloads').expanduser()).replace("\\", "/") + "/",
    ],
    "destination_path": os.path.abspath(os.sep).replace("\\", "/") if platform.system() == "Windows" else os.path.join(os.path.expanduser("~"), ""),
    "notifications": True,
    "system_tray": True,
    "encryption": False,
    "appearance_mode": "dark",
    "color_theme": "blue",
    "backup_expiry_date": "Forever",
    "storage_provider": "None",
    "compression_method": "ZIP_DEFLATED",
    "allowZip64": True,
    "compression_level": "5",
    "backup_interval": None,
    "ftp_hostname": "",
    "ftp_username": "",
    "ftp_password": "",
    "mega_email": "",
    "mega_password": "",
    "dropbox_access_token": ""
}, SETTINGS_PATH)


def get_config_info():
    print("Config Info:")
    print(f"\n{F.LIGHTGREEN_EX}Platform:{F.RESET} {config['platform']}")
    print(f"{F.LIGHTGREEN_EX}Source paths:{F.RESET} {config['source_paths']}")
    print(f"{F.LIGHTGREEN_EX}Destination path:{F.RESET} {config['destination_path']}")
    print(f"{F.LIGHTGREEN_EX}Notifications:{F.RESET} {config['notifications']}")
    print(f"{F.LIGHTGREEN_EX}System tray:{F.RESET} {config['system_tray']}")
    print(f"{F.LIGHTGREEN_EX}Encryption:{F.RESET} {config['encryption']}")
    print(f"{F.LIGHTGREEN_EX}Appearance mode:{F.RESET} {config['appearance_mode']}")
    print(f"{F.LIGHTGREEN_EX}Color theme:{F.RESET} {config['color_theme']}")
    print(
        f"{F.LIGHTGREEN_EX}Backup expiry date:{F.RESET} {config['backup_expiry_date']}"
    )
    print(f"{F.LIGHTGREEN_EX}Storage provider:{F.RESET} {config['storage_provider']}")
    print(
        f"{F.LIGHTGREEN_EX}Compression method:{F.RESET} {config['compression_method']}"
    )
    print(f"{F.LIGHTGREEN_EX}Allow Zip64:{F.RESET} {config['allowZip64']}")
    print(f"{F.LIGHTGREEN_EX}Compression level:{F.RESET} {config['compression_level']}")
    print(f"{F.LIGHTGREEN_EX}Backup interval:{F.RESET} {config['backup_interval']}")
    print(f"{F.LIGHTGREEN_EX}FTP hostname:{F.RESET} {config['ftp_hostname']}")
    print(f"{F.LIGHTGREEN_EX}FTP username:{F.RESET} {config['ftp_username']}")
    print(f"{F.LIGHTGREEN_EX}FTP password:{F.RESET} {config['ftp_password']}")
    print(f"{F.LIGHTGREEN_EX}Mega email:{F.RESET} {config['mega_email']}")
    print(f"{F.LIGHTGREEN_EX}Mega password:{F.RESET} {config['mega_password']}")
    print(
        f"{F.LIGHTGREEN_EX}Dropbox access token:{F.RESET} {config['dropbox_access_token']}\n"
    )


if not os.path.exists(config.path):
    config.save()
