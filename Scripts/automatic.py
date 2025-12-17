#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
This script is designed for automatic backups in the background.
While currently requiring user interaction in some cases,
I'm actively working to minimize this need.


Encryption Enabled:
-------------------

If backup encryption is enabled in the configuration file,
you will be prompted to set a password every time a backup is performed.
(Work in progress to automate password management)

To run backups continuously:
----------------------------

This script is designed to run 24/7 in the background.
Please refer to your operating system's documentation for instructions on configuring background execution of scripts.
Common methods include using task schedulers or systemd services.
For detailed setup instructions:
https://github.com/KafetzisThomas/SafeArchive/blob/main/docs/automatic_backups.md
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
