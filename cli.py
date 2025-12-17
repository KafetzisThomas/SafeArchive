#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
This file serves as the command-line interface (CLI) version of the program.
Supported platforms: Windows, Linux, macOS
"""

import os
import sys
import platform
from Scripts.CLI.backup_utils import Backup
from Scripts.CLI.restore import RestoreBackup
from Scripts.file_utils import get_backup_size, storage_media_free_space,last_backup, create_destination_directory_path
from Scripts.configs import config
import humanize
import colorama
from art import text2art
from colorama import Fore as F, Back as B
colorama.init(autoreset=True)

# check system platform to set correct console clear command
clear_command = "cls" if platform.system() == "Windows" else "clear"
os.system(clear_command)

DESTINATION_PATH = config.get("destination_path") + "SafeArchive/"

create_destination_directory_path(DESTINATION_PATH)
print(text2art("SafeArchive"))
print(f"> Author: {F.LIGHTYELLOW_EX}KafetzisThomas")
print("-------------------------")
print(f"\n~ Last Backup: {B.LIGHTBLUE_EX}{F.WHITE} {last_backup(DESTINATION_PATH)} {B.RESET}{F.RESET}")
print(f"~ Free space on ({DESTINATION_PATH.replace('SafeArchive/', '')}): {storage_media_free_space()} GB")
print(f"~ Size of backup: {humanize.naturalsize(get_backup_size(DESTINATION_PATH))}")
print("\nMenu Options:")
print(f"  |- 1) Config {F.LIGHTWHITE_EX}Info{F.RESET} - Display your {F.LIGHTBLUE_EX}preferences{F.RESET}")
print(f"  |- 2) {F.LIGHTMAGENTA_EX}Backup{F.RESET} Now - Zip source path files to {F.LIGHTCYAN_EX}destination{F.RESET} path")
print(f"  |- 3) Restore {F.LIGHTGREEN_EX}past{F.RESET} backup - {F.LIGHTBLACK_EX}Extract{F.RESET} selected zip file")

try:
    choice = int(input("\nChoice (1-3): "))
except ValueError:
    print(f"{F.LIGHTRED_EX}[*] Undefined choice.")
    sys.exit()
except KeyboardInterrupt:
    print(f"{F.LIGHTCYAN_EX}[*] Exiting...")
    sys.exit()

if choice == 1:
    config_fields = {
        "Source paths": config.get('source_paths'),
        "Destination path": config.get('destination_path'),
        "Compression method": config.get('compression_method'),
        "Compression level": config.get('compression_level'),
        "Backup expiry date": config.get('backup_expiry_date'),
        "Backup interval": config.get('backup_interval'),
        "Encryption": config.get('encryption'),
        "ftp": config.get('ftp'),
        "FTP hostname": config.get('ftp_hostname'),
        "FTP username": config.get('ftp_username'),
        "FTP password": config.get('ftp_password'),
    }
    print("Config Info:\n")
    for key, value in config_fields.items():
        print(f"{F.LIGHTGREEN_EX}{key}:{F.RESET} {value}")

elif choice == 2:
    try:
        Backup().perform_backup(config.get("source_paths"), DESTINATION_PATH)
    except KeyboardInterrupt:
        print(f"{F.LIGHTRED_EX}[*] Backup process cancelled.")
        sys.exit()

elif choice == 3:
    RestoreBackup().run_restore_thread(DESTINATION_PATH)

else:
    print(f"{F.LIGHTRED_EX}[*] Undefined choice.")
