#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
This file serves as the command-line interface (CLI) version of the program.
Supportive Platforms: Windows, Linux
"""

# Import built-in modules
import os
import sys
import time
import platform

# Append the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Import module files
from SafeArchive.Scripts.CLI.backup_utils import Backup
from SafeArchive.Scripts.CLI.restore import RestoreBackup
from SafeArchive.Scripts.file_utils import get_backup_size, storage_media_free_space, last_backup, create_destination_directory_path, edit_configs
from SafeArchive.Scripts.system_notifications import notify_user
from SafeArchive.Scripts.configs import config
config.load()

# Import other (third-party) modules
import humanize
import colorama
from art import text2art
from colorama import Fore as F, Back as B
colorama.init(autoreset=True)

backup = Backup()
restore_backup = RestoreBackup()

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

if config["source_paths"] is None or config["destination_path"] is None:
    print(f"{B.RED}{F.WHITE} NOTE {B.RESET}{F.RESET} Please specify your preferences in {F.LIGHTYELLOW_EX}settings.json{F.RESET} file...")
    print("\nREQUIRED:")
    print("'source_paths': [path/to/, path/to/, ...] --> string inside list")
    print("'destination_path': 'path' --> string")
    print("\nOPTIONAL:")
    print("'backup_to_cloud' --> boolean")
    print("'encryption' --> boolean")
    print("'backup_expiry_date' --> integer")
    print("'ftp_hostname' --> string")
    print("'ftp_username' --> string")
    print("'ftp_password' --> string")
    print("'mega_email' --> string")
    print("'mega_password' --> string")
    print("'dropbox_access_token' --> string\n")
    sys.exit()


create_destination_directory_path(DESTINATION_PATH)
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
    notify_user(message="Undefined choice.", terminal_color=F.LIGHTRED_EX)
    sys.exit()
except KeyboardInterrupt:
    notify_user(message="Exiting...", terminal_color=F.LIGHTCYAN_EX)
    sys.exit()

if choice == 1:
    try:
        start = time.time()
        backup.perform_backup(SOURCE_PATHS=config['source_paths'], DESTINATION_PATH=DESTINATION_PATH)
        end = time.time()
        time_elapsed = end - start
        print(f"[Finished in {time_elapsed:.1f}s]")
    except KeyboardInterrupt:
        notify_user(message="Backup process cancelled.", terminal_color=F.LIGHTRED_EX)
        sys.exit()
elif choice == 2:
    restore_backup.run_restore_thread(DESTINATION_PATH=DESTINATION_PATH)
else:
    notify_user(message="Undefined choice.", terminal_color=F.LIGHTRED_EX)
