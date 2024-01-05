#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
This file contains the core functionality of the program.
"""

import Scripts.cli_configs as conf
conf.config.load() # Load JSON file into memory

try: import Scripts.cli_cloud as cloud
except TypeError: pass

import os, sys, datetime, zipfile, psutil, colorama
from prettytable import PrettyTable
from datetime import date
from colorama import Fore as F
colorama.init(autoreset=True)

# Set the destination directory path (type: string)
DESTINATION_PATH = conf.config["destination_path"] + "SafeArchive/"  # Get value from the JSON file

def backup_expiry_date():
  """
  Check if previous backups are older than expiry date
  Remove every past backup if True
  """
  for filename in os.listdir(DESTINATION_PATH):  # Iterate through all files in the destination directory
    filepath = os.path.join(DESTINATION_PATH, filename)

    modification_time = datetime.datetime.fromtimestamp(os.path.getmtime(filepath))  # Get the modification time of the file

    if modification_time < (datetime.datetime.now()) - (datetime.timedelta(days=conf.config["backup_expiry_date"])):  # Check if the file is older than JSON value
      os.remove(filepath)  # Delete the file

def get_backup_size():
  """Walk through all files in the destination path & return backup size"""
  total_size = 0  # Initialize total size to 0

  for dirpath, _, filenames in os.walk(DESTINATION_PATH):
    for file in filenames:
      filepath = os.path.join(dirpath, file)

      total_size += os.path.getsize(filepath)  # Add the size of each file to the total size
  return total_size

def storage_media_free_space():
  """Return storage media free space"""
  disk_usage = psutil.disk_usage(conf.config['destination_path']).free  # Get drive free space
  free_space = round(disk_usage / (1024**3), 2)  # Convert free space to GB
  return free_space

def get_drive_usage_percentage():
  """Return drive usage percentage"""
  drive_usage_percentage = psutil.disk_usage(conf.config['destination_path']).percent  # Get drive usage percentage
  return drive_usage_percentage

def get_modification_time(file):
  """Return the modification time of zip file"""
  file_path = os.path.join(DESTINATION_PATH, file)
  return os.path.getmtime(file_path)

def last_backup():
  """Return last backup date"""
  try:
    files = [file for file in os.listdir(DESTINATION_PATH) if os.path.isfile(os.path.join(DESTINATION_PATH, file))]  # Get a list of all the files in the destination path
    files.sort(key=get_modification_time)  # Sort the list of files based on their modification time

    most_recently_modified_file = files[-1]  # The most recently modified file  
    filename, _, filetype = most_recently_modified_file.partition(".")

    if filetype != "zip":
      filename = "No backup"
  except IndexError:
    filename = "No backup"
  return filename

def backup():
  """
  Zip (backup) source path files to destination path:
    * Compression method: ZIP_DEFLATED
    * allowZip64 is set to True (this parameter use the ZIP64 extensions when the zip file is larger than 4gb)
    * Compresslevel is set to 9 (its sometimes really slow when source path files are too large, saves storage space)
  Initialize & Upload local backups to cloud if JSON value is True
  """
  # Check if storage media usage is below or equal to 90%
  print("[!] backup init")
  if get_drive_usage_percentage() <= 90:
    print("[+] driver usage is below 90%")
    # Set expiry date for old backups (type: integer)
    print("[!] setting expiry date..")
    if conf.config["backup_expiry_date"]: backup_expiry_date()
    # Open the zipfile in write mode, create zip file with current date in its name
    print("[!] Opening zipfile in write mode")
    with zipfile.ZipFile(f'{DESTINATION_PATH}{date.today()}.zip', mode='w', compression=zipfile.ZIP_DEFLATED, allowZip64=True, compresslevel=9) as zipObj:
      print("[!] iterating..")
      i = 0
      for item in conf.config['source_path']:  # Iterate over each path in the source list
        print(f"[{i}] iterating over {item}")
        l=0
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
    if conf.config["backup_to_cloud"]:
      cloud.initialize()
      if cloud.get_cloud_usage_percentage() >= 90: print(f"{F.LIGHTRED_EX}* Your Google Drive storage is almost full. To make sure your files can sync, clean up space.")  # Check if cloud storage usage is above or equal to 90%
      else: cloud.backup_to_cloud(DESTINATION_PATH[:-1], parent_folder_id=cloud.gdrive_folder['id'])  # Upload the local folder and its content
  else: print(f"{F.LIGHTRED_EX}* Your Drive storage is almost full. To make sure your files can sync, clean up space.")

def restore_backup(**backups_table):
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
      zipObj.extractall(conf.config['destination_path'])
  else:
    print(f"{F.LIGHTRED_EX}* Invalid backup ID selected.")
    sys.exit()
