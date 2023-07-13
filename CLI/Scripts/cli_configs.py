#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
This file manages configurations and provides functionality to save and load them as well.
"""

import os, json
from pathlib import Path

class ConfigDict(dict):
  """Set configs"""
  __slots__=["path"]
  def __init__(self, config, path):
    self.update(config)
    self.path = Path(path)

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
  'source_path': None,
  'destination_path': None,
  'backup_to_cloud': None,
  'backup_expiry_date': None
}, SETTINGS_PATH)

if not os.path.exists(config.path):
  config.save()
