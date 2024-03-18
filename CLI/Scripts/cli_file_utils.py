#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import sys
import psutil
import datetime
import platform
import colorama
from Scripts.cli_configs import ConfigDict, config
from colorama import Fore as F, Back as B
colorama.init(autoreset=True)
config.load()


def create_destination_directory_path(DESTINATION_PATH):
    """Create the destination directory path if it doesn't exist"""
    try:
        if not os.path.exists(DESTINATION_PATH):
            os.makedirs(DESTINATION_PATH)
    except FileNotFoundError:
        print(f"{F.LIGHTYELLOW_EX}* Your SafeArchive Drive was disconnected for too long. Reconnect it to keep saving copies of your files.")
    except PermissionError:
        print(f"{F.LIGHTYELLOW_EX}* No permissions given to make directory: '{DESTINATION_PATH}'. Change it in settings.json or run with elevated priveleges.")


def get_backup_size(DESTINATION_PATH):
    """Walk through all files in the destination path & return total size"""
    total_size = 0

    for dirpath, _, filenames in os.walk(DESTINATION_PATH):
        for file in filenames:
            filepath = os.path.join(dirpath, file)

            # Add size of each file to total size
            total_size += os.path.getsize(filepath)
    return total_size


def storage_media_free_space():
    """Return storage media free space"""
    disk_usage = psutil.disk_usage(config['destination_path']).free
    free_space = round(disk_usage / (1024**3), 2)  # Convert free space to GB
    return free_space


def get_drive_usage_percentage():
    """Return drive usage percentage"""
    drive_usage_percentage = psutil.disk_usage(config['destination_path']).percent
    return drive_usage_percentage


def get_modification_time(file, DESTINATION_PATH):
    """Return the modification time of zip file"""
    file_path = os.path.join(DESTINATION_PATH, file)
    return os.path.getmtime(file_path)


def last_backup(DESTINATION_PATH):
    """Return last backup date"""
    try:
        files = [file for file in os.listdir(DESTINATION_PATH) if os.path.isfile(os.path.join(
            DESTINATION_PATH, file))]  # Get a list of all the files in the destination path
        # Sort the list of files based on their modification time
        files.sort(key=lambda file: get_modification_time(DESTINATION_PATH, file))

        # The most recently modified file
        most_recently_modified_file = files[-1]
        filename, _, filetype = most_recently_modified_file.partition('.')

        if filetype != 'zip':
            filename = "No backup"
    except IndexError:
        filename = "No backup"
    return filename


def backup_expiry_date(DESTINATION_PATH):
    """
    Check if previous backups are older than expiry date
    Remove every past backup if True
    """
    for filename in os.listdir(DESTINATION_PATH):  # Iterate through all files in the destination directory
        filepath = os.path.join(DESTINATION_PATH, filename)

        modification_time = datetime.datetime.fromtimestamp(
            os.path.getmtime(filepath))  # Get the modification time of the file

        # Check if the file is older than JSON value
        if modification_time < (datetime.datetime.now()) - (datetime.timedelta(days=config["backup_expiry_date"])):
            os.remove(filepath)  # Delete the file


def edit_configs():
    """Configure preferences through script arguments"""
    try:
        print(f"{B.GREEN} -- CONFIGURATION -- {B.RESET}")
        folder_to_backup = input(f"{B.RED}! TO SET MORE THAN ONE SOURCE PATH, EDIT THE CONFIG FILE !\n! YOU NEED TO INPUT THE WHOLE PATH !{B.RESET}\nPlease enter the folder to backup: ")
        backup_destination = input("Please enter the destination folder: ")
        cloud_backup = input("do you want to backup to cloud?(y/N): ")
        backup_expire = input("if you want to set the expiry date of backups, enter here(leave None if you don't want): ")
        encryption = input("do you want to encrypt your backups?(y/N): ")
        storage_provider = input("if you want to use a storage provider along with your drive, enter here (Google Drive, FTP, MegaCloud, Dropbox)\n(leave None if you don't want): ")
        ftp_hostname = input("if you have set FTP as your storage provider, enter hostname here: ")
        ftp_username = input("if you have set FTP as your storage provider, enter username here: ")
        ftp_password = input("if you have set FTP as your storage provider, enter password here: ")
        mega_email = input("if you have set Mega as your storage provider, enter email here: ")
        mega_password = input("if you have set Mega as your storage provider, enter password here: ")
        dropbox_access_token = input("if you have set Dropbox as your storage provider, enter token here: ")

        # Rewrite values for *efficiency*
        cloud_backup = True if cloud_backup.lower() == "y" else False
        encryption = True if encryption.lower() == "y" else False
        backup_expire = backup_expire if backup_expire else None
        storage_provider = storage_provider if storage_provider else None
        ftp_hostname = ftp_hostname if ftp_hostname else None
        ftp_username = ftp_username if ftp_username else None
        ftp_password = ftp_password if ftp_password else None
        mega_email = mega_email if mega_email else None
        mega_password = mega_password if mega_password else None
        dropbox_access_token = dropbox_access_token if dropbox_access_token else None


        SETTINGS_PATH = 'settings.json'
        config = ConfigDict({
            "platform": platform.system(),
            "source_paths": [folder_to_backup],
            "destination_path": backup_destination,
            "backup_to_cloud": cloud_backup,
            "encryption": encryption,
            "backup_expiry_date": backup_expire,
            "storage_provider": storage_provider,
            "ftp_hostname": ftp_hostname,
            "ftp_username": ftp_username,
            "ftp_password": ftp_password,
            "mega_email": mega_email,
            "mega_password": mega_password,
            "dropbox_access_token": dropbox_access_token
        }, SETTINGS_PATH)

        check = input(f"\nThis is the configuration:\n source_paths: {folder_to_backup}\n destination_path: {backup_destination}\n backup_to_cloud: {cloud_backup}\n backup_expiry_date: {backup_expire}\n Is this right?(Y/n): ")
        if check.lower() == "n":
            print(f"\n{F.YELLOW}Aborting..{F.RESET}")
            sys.exit()
        else:
            config.save()
            print(f"\n{F.GREEN}Done!{F.RESET}")

    except KeyboardInterrupt:
        print(f"\n{F.RED}User abort!{F.RESET}")
