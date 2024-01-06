#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
This file contains the core functionality of the program.
"""

import os
import sys
import datetime
import zipfile
import psutil
import colorama
from Scripts.cli_cloud import GoogleDriveCloud
from Scripts.cli_configs import ConfigDict, config
from prettytable import PrettyTable
from datetime import date
from colorama import Fore as F, Back as B
colorama.init(autoreset=True)
config.load() # Load JSON file into memory

google_drive = GoogleDriveCloud()


def backup_expiry_date(DESTINATION_PATH):
  """
  Check if previous backups are older than expiry date
  Remove every past backup if True
  """
  for filename in os.listdir(DESTINATION_PATH):  # Iterate through all files in the destination directory
    filepath = os.path.join(DESTINATION_PATH, filename)

    modification_time = datetime.datetime.fromtimestamp(os.path.getmtime(filepath))  # Get the modification time of the file

    if modification_time < (datetime.datetime.now()) - (datetime.timedelta(days=config["backup_expiry_date"])):  # Check if the file is older than JSON value
      os.remove(filepath)  # Delete the file


def get_backup_size(DESTINATION_PATH):
  """Walk through all files in the destination path & return backup size"""
  total_size = 0  # Initialize total size to 0

  for dirpath, _, filenames in os.walk(DESTINATION_PATH):
    for file in filenames:
      filepath = os.path.join(dirpath, file)

      total_size += os.path.getsize(filepath)  # Add the size of each file to the total size
  return total_size


def storage_media_free_space():
  """Return storage media free space"""
  disk_usage = psutil.disk_usage(config['destination_path']).free  # Get drive free space
  free_space = round(disk_usage / (1024**3), 2)  # Convert free space to GB
  return free_space


def get_drive_usage_percentage():
  """Return drive usage percentage"""
  drive_usage_percentage = psutil.disk_usage(config['destination_path']).percent  # Get drive usage percentage
  return drive_usage_percentage


def get_modification_time(file, DESTINATION_PATH):
  """Return the modification time of zip file"""
  file_path = os.path.join(DESTINATION_PATH, file)
  return os.path.getmtime(file_path)


def last_backup(DESTINATION_PATH):
  """Return last backup date"""
  try:
    files = [file for file in os.listdir(DESTINATION_PATH) if os.path.isfile(os.path.join(DESTINATION_PATH, file))]  # Get a list of all the files in the destination path
    # Sort the list of files based on their modification time
    files.sort(key=lambda file: get_modification_time(DESTINATION_PATH, file))

    most_recently_modified_file = files[-1]  # The most recently modified file  
    filename, _, filetype = most_recently_modified_file.partition(".")

    if filetype != "zip":
      filename = "No backup"
  except IndexError:
    filename = "No backup"
  return filename


def backup(DESTINATION_PATH):
  """
  Zip (backup) source path files to destination path:
    * Compression method: ZIP_DEFLATED
    * allowZip64 is set to True (this parameter use the ZIP64 extensions when the zip file is larger than 4gb)
    * Compresslevel is set to 9 (its sometimes really slow when source path files are too large, saves storage space)
  Initialize & Upload local backups to cloud if JSON value is True
  """
  print("[!] backup init")
  # Check if storage media usage is below or equal to 90%
  if get_drive_usage_percentage() <= 90:
    print("[+] driver usage is below 90%")
    print("[!] setting expiry date..")
    # Set expiry date for old backups (type: integer)
    if config["backup_expiry_date"]:
      backup_expiry_date(DESTINATION_PATH)

    print("[!] Opening zipfile in write mode")
    # Open the zipfile in write mode, create zip file with current date in its name
    with zipfile.ZipFile(f'{DESTINATION_PATH}{date.today()}.zip', mode='w', compression=zipfile.ZIP_DEFLATED, allowZip64=True, compresslevel=9) as zipObj:
      print("[!] iterating..")
      i,l = 1,1
      for item in config['source_path']:  # Iterate over each path in the source list
        print(f"[{i}] iterating over {item}")
        for root, dirs, files in os.walk(item):  # Iterate over the files and folders in the path
          print(f"[{l}] iterating over files and folders in {item}")
          for dirname in dirs:
            dirpath = os.path.join(root, dirname)
            print(f"[+] Writing {dirname} to zip")
            zipObj.write(dirpath)  # Write the folder to the zip archive

          for filename in files:
            filepath = os.path.join(root, filename)
            print(f"[+] Writing {filename} to zip")
            zipObj.write(filepath)  # Write the file to the zip archive
          l+=1
        i+=1

    # Choose if you want local backups to sync in cloud (type: boolean)
    if config["backup_to_cloud"]:
      google_drive.initialize()
      # Check if cloud storage usage is above or equal to 90%
      if google_drive.get_cloud_usage_percentage() >= 90:
        print(f"{F.LIGHTRED_EX}* Your Google Drive storage is almost full. To make sure your files can sync, clean up space.")
      else:
        # Upload the local folder and its content
        google_drive.backup_to_google_drive(DESTINATION_PATH[:-1], DESTINATION_PATH, parent_folder_id=google_drive.gdrive_folder['id'])
  else:
    print(f"{F.LIGHTRED_EX}* Your Drive storage is almost full. To make sure your files can sync, clean up space.")


def restore_backup(DESTINATION_PATH, **backups_table):
  """
  Display last backups & extract (restore) selected zip file (backup)
  Move zip file content to it's original location
  """
  table = PrettyTable()  # Create table
  table.field_names = ["ID", "Backups", "Type"]

  # Iterate over the files in the destination path
  for index, zip_file in enumerate(os.listdir(DESTINATION_PATH)):
    filename, _,filetype = zip_file.partition('.')

    # Check if it's a zip file
    if filetype == 'zip':  
      backups_table[index] = filename
      table.add_row([index, filename, filetype])  # Add file information to the table

  print(table)

  try:
    # Prompt user to select a backup to restore
    selected_id = input("\nSelect backup to restore (Enter the ID): ")
  except KeyboardInterrupt: 
    print(f"\n{F.LIGHTCYAN_EX}* Exiting...")
    sys.exit()

  if selected_id.isdigit() and int(selected_id) in backups_table:
    selected_filename = backups_table[int(selected_id)]
    # Open the zipfile in read mode, extract its content
    with zipfile.ZipFile(f'{DESTINATION_PATH}{selected_filename}.zip', mode='r') as zipObj:
      zipObj.extractall(config['destination_path'])
  else:
    print(f"{F.LIGHTRED_EX}* Invalid backup ID selected.")
    sys.exit()


def edit_configs():
  """Configure preferences through script arguments"""
  try:
      print(f"{B.GREEN} -- CONFIGURATION -- {B.RESET}")
      folder_to_backup = input(f"{B.RED}! TO SET MORE THAN ONE SOURCE PATH, EDIT THE CONFIG FILE !\n! YOU NEED TO INPUT THE WHOLE PATH !{B.RESET}\nPlease enter the folder to backup: ")
      backup_destination = input("Please enter the destination folder: ")
      cloud_backup = input("do you want to backup to cloud?(y/N): ")
      backup_expire = input("if you want to set the expiry date of backups, enter here(leave None if you don't want): ")

      cloud_backup = True if cloud_backup.lower() == "y" else False  # Rewrite values for *efficiency*
      if not backup_expire: backup_expire = None

      SETTINGS_PATH = 'settings.json'
      config = ConfigDict({
        'source_path': [folder_to_backup],
        'destination_path': backup_destination,
        'backup_to_cloud': cloud_backup,
        'backup_expiry_date': backup_expire
      }, SETTINGS_PATH)

      check = input(f"\nThis is the configuration:\n source_path: {folder_to_backup}\n destination_path: {backup_destination}\n backup_to_cloud: {cloud_backup}\n backup_expiry_date: {backup_expire}\n Is this right?(Y/n): ")
      if check.lower() == "n":
        print(f"\n{F.YELLOW}Aborting..{F.RESET}")
        sys.exit()
      else:
        config.save()
        print(f"\n{F.GREEN}Done!{F.RESET}")

  except KeyboardInterrupt:
    print(f"\n{F.RED}User abort!{F.RESET}")
