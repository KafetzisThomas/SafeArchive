#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
This file serves as the command-line interface (CLI) version of the program.
Supportive Platforms: Windows, Linux, macOS
"""

# Import built-in modules
import os
import sys
import time
import platform

# Import module files
from Scripts.CLI.backup_utils import Backup
from Scripts.CLI.restore import RestoreBackup
from Scripts.file_utils import (
    get_backup_size,
    storage_media_free_space,
    last_backup,
    create_destination_directory_path,
)
from Scripts.system_notifications import notify_user
from Scripts.configs import config, get_config_info

# Import other (third-party) modules
import humanize
import colorama
from art import text2art
from colorama import Fore as F, Back as B

backup = Backup()
restore_backup = RestoreBackup()
colorama.init(autoreset=True)
config.load()

# Check system platform to set correct console clear command
clear_command = "cls" if platform.system() == "Windows" else "clear"
os.system(clear_command)

# Get value from the JSON file
DESTINATION_PATH = config["destination_path"] + "SafeArchive/"

# Run check on python version, must be 3.6 or higher because of f strings
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    print(
        "Error Code U-2: This program requires running python 3.6 or higher! You are running"
        + str(sys.version_info[0])
        + "."
        + str(sys.version_info[1])
    )
    sys.exit()

create_destination_directory_path(DESTINATION_PATH)
print(text2art("SafeArchive-CLI"))
print(f"> Author: {F.LIGHTYELLOW_EX}KafetzisThomas")
print("-------------------------")
print(
    f"\n~ Last Backup: {B.LIGHTBLUE_EX}{F.WHITE} {last_backup(DESTINATION_PATH)} {B.RESET}{F.RESET}"
)
print(
    f"~ Free space on ({DESTINATION_PATH.replace('SafeArchive/', '')}): {storage_media_free_space()} GB"
)
print(f"~ Size of backup: {humanize.naturalsize(get_backup_size(DESTINATION_PATH))}")
print(
    f"\n1. {F.LIGHTMAGENTA_EX}Config{F.RESET} Info"
    f" - Display {F.LIGHTCYAN_EX}your{F.RESET} preferences"
)
print(
    f"2. {F.LIGHTMAGENTA_EX}Backup{F.RESET} Now"
    f" - Zip source path files to {F.LIGHTCYAN_EX}destination{F.RESET} path"
)
print(
    f"3. Restore {F.LIGHTGREEN_EX}previous{F.RESET} backup"
    f" - {F.LIGHTBLACK_EX}Extract{F.RESET} selected zip file"
)

try:
    choice = int(input("\nChoice (1-3): "))
except ValueError:
    notify_user(message="Undefined choice.", terminal_color=F.LIGHTRED_EX)
    sys.exit()
except KeyboardInterrupt:
    notify_user(message="Exiting...", terminal_color=F.LIGHTCYAN_EX)
    sys.exit()

if choice == 1:
    get_config_info()
elif choice == 2:
    try:
        start = time.time()
        backup.perform_backup(
            SOURCE_PATHS=config["source_paths"], DESTINATION_PATH=DESTINATION_PATH
        )
        end = time.time()
        time_elapsed = end - start
        print(f"[Finished in {time_elapsed:.1f}s]")
    except KeyboardInterrupt:
        notify_user(message="Backup process cancelled.", terminal_color=F.LIGHTRED_EX)
        sys.exit()
elif choice == 3:
    restore_backup.run_restore_thread(DESTINATION_PATH=DESTINATION_PATH)
else:
    notify_user(message="Undefined choice.", terminal_color=F.LIGHTRED_EX)
