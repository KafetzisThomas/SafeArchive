#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import sys
import psutil
import datetime
from .system_notifications import notify_user
from .configs import config


def create_destination_directory_path(DESTINATION_PATH):
    """Create the destination directory path if it doesn't exist"""
    try:
        if not os.path.exists(DESTINATION_PATH):
            os.makedirs(DESTINATION_PATH)
    except FileNotFoundError:
        notify_user(
            title='SafeArchive: Reconnect your drive',
            message='Your SafeArchive Drive was disconnected for too long. Reconnect it to keep saving copies of your files.',
            icon='drive.ico'
        )
    except PermissionError:
        notify_user(
            title='SafeArchive: [Error] Permission Denied.',
            message=f'No permissions given to make directory: \'{DESTINATION_PATH}\'. Change it in settings.json or run with elevated priveleges.',
            icon='error.ico'
        )


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
    """
    Check if last backup is older than 30 days, if True then display a system notification message
    Return last backup date
    """
    try:
        files = [file for file in os.listdir(DESTINATION_PATH) if os.path.isfile(os.path.join(DESTINATION_PATH, file))]  # Get a list of all the files in the destination path
        
        # Sort the list of files based on their modification time
        files.sort(key=lambda file: get_modification_time(DESTINATION_PATH, file))

        # The most recently modified file
        most_recently_modified_file = files[-1]
        filename, _, filetype = most_recently_modified_file.partition('.')

        # Get the modification time of the most recently modified file
        modification_time = datetime.datetime.fromtimestamp(
            os.path.getmtime(f"{DESTINATION_PATH}{most_recently_modified_file}"))

        # Check if the file is older than three months
        if modification_time < (datetime.datetime.now()) - (datetime.timedelta(days=30)):
            notify_user(
                title='SafeArchive: Reconnect your drive',
                message='Your SafeArchive Drive was disconnected for too long. Reconnect it to keep saving copies of your files.',
                icon='drive.ico'
            )

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
    is_valid_expiry_date  = True
    for filename in os.listdir(DESTINATION_PATH):  # Iterate through all files in the destination directory
        filepath = os.path.join(DESTINATION_PATH, filename)

        modification_time = datetime.datetime.fromtimestamp(
            os.path.getmtime(filepath))  # Get the modification time of the file

        if config['backup_expiry_date'] == "1 month":
            days = 30
        elif config['backup_expiry_date'] == "3 months":
            days = 90
        elif config['backup_expiry_date'] == "6 months":
            days = 180
        elif config['backup_expiry_date'] == "9 months":
            days = 270
        elif config['backup_expiry_date'] == "1 year":
            days = 365
        else:
            is_valid_expiry_date = False

        # Check if the file is older than JSON value
        if is_valid_expiry_date and modification_time < (datetime.datetime.now()) - (datetime.timedelta(days=int(days))):
            os.remove(filepath)  # Delete the file
