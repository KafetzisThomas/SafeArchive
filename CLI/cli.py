#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
This file serves as the command-line interface (CLI) version of the program.
Supportive Platforms: Windows, Mac, Linux
"""

# Import built-in modules
import os, sys, time, platform

# Import module files
try: import Scripts.cli_functions as func
except TypeError: pass

import Scripts.cli_configs as conf
conf.config.load() # Load the JSON file into memory

# Import other (third-party) modules
import humanize, colorama
from art import text2art
from colorama import Fore as F, Back as B
colorama.init(autoreset=True)

# Check system platform to set correct console clear command
clear_command = "cls" if platform.system() == "Windows" else "clear"
os.system(clear_command)  # Clear console

# Run check on python version, must be 3.6 or higher because of f strings
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
  print("Error Code U-2: This program requires running python 3.6 or higher! You are running" + str(sys.version_info[0]) + "." + str(sys.version_info[1]))
  sys.exit()

if(conf.config["source_path"] is None) or (conf.config["destination_path"] is None):
  print(f"{B.RED}{F.WHITE} NOTE {B.RESET}{F.RESET} Please specify your preferences in {F.LIGHTYELLOW_EX}settings.json{F.RESET} file...")
  print("\nREQUIRED:")
  print("'source_path': [path/to/, path/to/, ...] --> string inside list")
  print("'destination_path': 'path' --> string")
  print("\nOPTIONAL:")
  print("'backup_to_cloud' --> boolean")
  print("'backup_expiry_date' --> integer\n")
  sys.exit()

# Set the destination directory path (type: string)
DESTINATION_PATH = conf.config["destination_path"] + "SafeArchive/"  # Get value from the JSON file

try:
  if not os.path.exists(DESTINATION_PATH):  # Create the destination directory path if it doesn't exist
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
print(f"\n~ Last Backup: {B.LIGHTBLUE_EX}{F.WHITE} {func.last_backup()} {B.RESET}{F.RESET}")
print(f"~ Free space on ({DESTINATION_PATH.replace('SafeArchive/', '')}): {func.storage_media_free_space()} GB")
print(f"~ Size of backup: {humanize.naturalsize(func.get_backup_size())}")
print(f"\n1. {F.LIGHTMAGENTA_EX}Backup{F.RESET} Now"
      f" - Zip source path files to {F.LIGHTCYAN_EX}destination{F.RESET} path")
print(f"2. Restore {F.LIGHTGREEN_EX}previous{F.RESET} backup"
      f" - {F.LIGHTBLACK_EX}Extract{F.RESET} selected zip file")

try: choice = int(input("\nChoice (1-2): "))
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
    func.backup()
    end = time.time()
    time_elapsed = end - start

    print(f"{F.LIGHTYELLOW_EX}* Backup completed successfully.")
    print(f"\n[Finished in {time_elapsed:.1f}s]")
  except KeyboardInterrupt:
    print(f"{F.LIGHTRED_EX}* Backup process cancelled.")
    sys.exit()
elif choice == 2:
  func.restore_backup()
  print(f"{F.LIGHTYELLOW_EX}* Files restored successfully.")
else:
  print(f"{F.LIGHTRED_EX}* Undefined choice.")
