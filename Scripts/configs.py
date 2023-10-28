#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
This file manages configurations and provides functionality to save and load them as well.
It also automatically triggers the saving of the configuration file whenever a setting is changed or deleted.
"""

import os
import json
from pathlib import Path

class ConfigDict(dict):
  """Set configs & save every time a setting changes"""
  __slots__=["path"]
  def __init__(self, config: dict, path: str):
    self.update(config)
    self.path = Path(path)

  def __setitem__(self, key, value):
    """Triggers whenever value is set"""
    super().__setitem__(key, value)
    self.save()

  def __delitem__(self, key):
    """Triggers whenever value is deleted"""
    super().__delitem__(key)
    self.save()

  def save(self):  
    """Saves config file to given path"""
    with open(self.path, 'w') as file:
      json.dump(self, file, indent=2)

  def load(self):
    """Loads config file from given path"""
    with open(self.path, 'r') as file:
      self.update(json.load(file))

SETTINGS_PATH = 'settings.json'
config = ConfigDict({
  'source_path': [
    str(Path('~/Desktop').expanduser()),
    str(Path('~/Documents').expanduser()),
    str(Path('~/Downloads').expanduser()),
  ],
  'destination_path': os.path.abspath(os.sep).replace("\\", "/"),
  'backup_to_cloud': False,
  'backup_expiry_date': "Forever (default)"
}, SETTINGS_PATH)

if not os.path.exists(config.path):
  config.save()
