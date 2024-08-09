#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
This script is designed for automatic backups in the background.
While currently requiring user interaction in some cases,
I'm actively working to minimize this need.


Encryption Enabled:
----

If backup encryption is enabled in the configuration file,
you will be prompted to set a password every time a backup is performed.
(Work in progress to automate password management)

Google Drive Storage:
----

If Google Drive is selected as the storage provider,
an authorization window will be displayed every time a backup is performed.
(Investigating alternative authentication methods)

To run backups continuously:
----

This script is designed to run 24/7 in the background.
Please refer to your operating system's documentation for instructions on configuring background execution of scripts.
Common methods include using task schedulers or systemd services.
For detailed setup instructions:
https://github.com/KafetzisThomas/SafeArchive/blob/main/docs/automatic_backups.md
"""

import schedule
import time
from CLI.backup_utils import Backup
from .configs import config
config.load()

backup = Backup()

DESTINATION_PATH = config['destination_path'] + "SafeArchive/"  # Get value from the JSON file

schedule.every(config['backup_interval']).hours.do(backup.perform_backup, DESTINATION_PATH)

while True:
    schedule.run_pending()
    time.sleep(1)
