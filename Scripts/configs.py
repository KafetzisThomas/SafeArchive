#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import os, json
from pathlib import Path

'''Set configs'''
# Save every time a setting changes
class ConfigDict(dict):
  __slots__=["path"]
  def __init__(self, config: dict, path: str):
    self.update(config)
    self.path = Path(path)

  '''Triggers whenever value is set'''
  def __setitem__(self, key, value):  
    super().__setitem__(key, value)
    self.save()

  '''Triggers whenever value is deleted'''
  def __delitem__(self, key):
    super().__delitem__(key)
    self.save()

  '''Saves config file to given path'''
  def save(self):  
    with open(self.path, 'w') as file:
      json.dump(self, file, indent=2)

  '''Loads config file from given path'''
  def load(self):
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
