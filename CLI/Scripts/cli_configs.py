#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
This file manages configurations and provides functionality to save and load them as well.
"""

import os
import json
from pathlib import Path


class ConfigDict(dict):
    """Set configs"""
    __slots__=["path"]

    def __init__(self, config: dict, path: str):
        self.update(config)
        self.path = Path(path)

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
        "source_path": "List of source paths (local folders) for backups (type: list with strings)",
        "destination_path": "Destination path (storage media) for backups (type: string)",
        "backup_to_cloud": "Flag indicating whether to backup to the cloud (specify: storage_provider) (type: boolean)",
        "backup_expiry_date": "Expiry date for the backups in the storage media (type: string)"
  },
    "source_path": None,
    "destination_path": None,
    "backup_to_cloud": None,
    "backup_expiry_date": None
}, SETTINGS_PATH)

if not os.path.exists(config.path):
    config.save()
