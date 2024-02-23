#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
This file serves as the command-line interface (CLI) version of the program.
Supportive Platforms: Windows, Mac, Linux
"""

# Import built-in modules
import os
import sys
import time
import platform

# Import module files
from Scripts.cli_functions import get_backup_size, storage_media_free_space, last_backup, restore_backup, edit_configs
from Scripts.cli_backup_utils import Backup
from Scripts.cli_configs import config
config.load()  # Load the JSON file into memory

# Import other (third-party) modules
import humanize
import colorama
from art import text2art
from colorama import Fore as F, Back as B
colorama.init(autoreset=True)

backup = Backup()

# Check system platform to set correct console clear command
clear_command = "cls" if platform.system() == "Windows" else "clear"
os.system(clear_command)

try:
    DESTINATION_PATH = config["destination_path"] + "SafeArchive/"  # Get value from the JSON file
except TypeError:
    pass

# Run check on python version, must be 3.6 or higher because of f strings
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    print("Error Code U-2: This program requires running python 3.6 or higher! You are running" +
          str(sys.version_info[0]) + "." + str(sys.version_info[1]))
    sys.exit()

try:
    if sys.argv[1] == "conf" or sys.argv[1] == "--conf" or sys.argv[1] == "-c":
        edit_configs()
        sys.exit()
except IndexError:
    pass

if (config["source_path"] is None) or (config["destination_path"] is None):
    print(f"{B.RED}{F.WHITE} NOTE {B.RESET}{F.RESET} Please specify your preferences in {F.LIGHTYELLOW_EX}settings.json{F.RESET} file...")
    print("\nREQUIRED:")
    print("'source_path': [path/to/, path/to/, ...] --> string inside list")
    print("'destination_path': 'path' --> string")
    print("\nOPTIONAL:")
    print("'backup_to_cloud' --> boolean")
    print("'backup_expiry_date' --> integer\n")
    sys.exit()

try:
    # Create the destination directory path if it doesn't exist
    if not os.path.exists(DESTINATION_PATH):
        os.makedirs(DESTINATION_PATH)
except FileNotFoundError:
    print("Your SafeArchive Drive is currently disconnected. Reconnect it to keep saving copies of your files.")
except PermissionError:
    print(f"No permissions given to make directory: '{DESTINATION_PATH}'.",
          "Change it in settings.json or run with elevated priveleges")
    sys.exit(77)

print(text2art("SafeArchive-CLI"))
print(f"> Author: {F.LIGHTYELLOW_EX}KafetzisThomas")
print("-------------------------")
print(f"\n~ Last Backup: {B.LIGHTBLUE_EX}{F.WHITE} {last_backup(DESTINATION_PATH)} {B.RESET}{F.RESET}")
print(f"~ Free space on ({DESTINATION_PATH.replace('SafeArchive/', '')}): {storage_media_free_space()} GB")
print(f"~ Size of backup: {humanize.naturalsize(get_backup_size(DESTINATION_PATH))}")
print(f"\n1. {F.LIGHTMAGENTA_EX}Backup{F.RESET} Now"
      f" - Zip source path files to {F.LIGHTCYAN_EX}destination{F.RESET} path")
print(f"2. Restore {F.LIGHTGREEN_EX}previous{F.RESET} backup"
      f" - {F.LIGHTBLACK_EX}Extract{F.RESET} selected zip file")

try:
    choice = int(input("\nChoice (1-2): "))
except ValueError:
    print(f"{F.LIGHTRED_EX}* Undefined choice.")
    sys.exit()
except KeyboardInterrupt:
    print(f"\n{F.LIGHTCYAN_EX}* Exiting...")
    sys.exit()

if choice == 1:
    print("/ Backing up your data...")
    try:
        start = time.time()
        backup.perform_backup(DESTINATION_PATH=DESTINATION_PATH)
        end = time.time()
        time_elapsed = end - start

        print(f"{F.LIGHTYELLOW_EX}* Backup completed successfully.")
        print(f"\n[Finished in {time_elapsed:.1f}s]")
    except KeyboardInterrupt:
        print(f"{F.LIGHTRED_EX}* Backup process cancelled.")
        sys.exit()
elif choice == 2:
    restore_backup(DESTINATION_PATH)
    print(f"{F.LIGHTYELLOW_EX}* Files restored successfully.")
else:
    print(f"{F.LIGHTRED_EX}* Undefined choice.")
