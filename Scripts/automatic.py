#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
This script is designed for automatic backups in the background.
Since it still requires some user interaction this feature is not yet complete.
"""

import time
import schedule
from CLI.backup_utils import Backup
from .configs import config

DESTINATION_PATH = config.get("destination_path") + "SafeArchive/"
backup_interval = config.get('backup_interval')

if backup_interval:
    schedule.every(backup_interval).hours.do(Backup().perform_backup, DESTINATION_PATH)

while True:
    schedule.run_pending()
    time.sleep(1)
