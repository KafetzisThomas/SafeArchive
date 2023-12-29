#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import zipfile
import threading
from datetime import date
import tkinter as tk
from Scripts.cloud_utils import GoogleDriveCloud, FTP
from Scripts.notification_handlers import notify_backup_completion
from Scripts.notification_handlers import notify_cloud_space_limitation
from Scripts.notification_handlers import notify_restore_completion
from Scripts.notification_handlers import notify_drive_space_limitation
from Scripts.file_utils import get_drive_usage_percentage
from Scripts.file_utils import backup_expiry_date
from Scripts.configs import config
import customtkinter as ctk

google_drive = GoogleDriveCloud()
ftp = FTP()

def backup(App, DESTINATION_PATH):
    """
    Zip (backup) source path files to destination path:
        * Compression method: ZIP_DEFLATED
        * allowZip64 is set to True (this parameter use the ZIP64 extensions when the zip file is larger than 4gb)
        * Compresslevel is set to 9 (its sometimes really slow when source path files are too large, saves storage space)
    Initialize & Upload local backups to cloud if JSON value is True
    """
    # Check if drive usage is below or equal to 90%
    if get_drive_usage_percentage() <= 90:
        # Set expiry date for old backups (type: integer)
        if config['backup_expiry_date'] != "Forever (default)":
            backup_expiry_date(DESTINATION_PATH)

        # Open the zipfile in write mode, create zip file with current date in its name
        with zipfile.ZipFile(f'{DESTINATION_PATH}{date.today()}.zip', mode='w', compression=zipfile.ZIP_DEFLATED, allowZip64=True, compresslevel=9) as zipObj:
            # Iterate over each path in the source list
            for item in config['source_path']:
                source_item_label = ctk.CTkLabel(
                    master=App, text=item, height=20, font=('Helvetica', 12))
                source_item_label.place(x=15, y=430)

                # Iterate over the files and folders in the path
                for root, dirs, files in os.walk(item):
                    for dirname in dirs:
                        dirpath = os.path.join(root, dirname)
                        # Write the folder to the zip archive
                        zipObj.write(dirpath)

                    for filename in files:
                        filepath = os.path.join(root, filename)
                        # Write the file to the zip archive
                        zipObj.write(filepath)

                source_item_label.place_forget()

        # Choose if you want local backups to be uploaded to cloud (type: boolean)
        if config['backup_to_cloud']:
            if config['cloud_provider'] == "Google Drive":
                google_drive.initialize()
                if google_drive.get_cloud_usage_percentage() >= 90:
                    # Check if cloud storage usage is above or equal to 90%
                    notify_cloud_space_limitation(config['notifications'])
                else:
                    # Upload the local folder and its content
                    google_drive.backup_to_google_drive(
                        DESTINATION_PATH[:-1], DESTINATION_PATH, parent_folder_id=google_drive.gdrive_folder['id'])
            else:
                # Upload the local folder and its content
                ftp.backup_to_ftp_server(DESTINATION_PATH)

        notify_backup_completion(DESTINATION_PATH, config['notifications'])
    else:
        notify_drive_space_limitation(config['notifications'])


def start_progress_bar(App, DESTINATION_PATH):
    """Start/Stop progress bar & call backup() function"""
    App.backup_progressbar.start()
    # Change backup button state to disabled
    App.backup_button.configure(state="disabled")
    backup(App, DESTINATION_PATH)
    # Change backup button state back to normal
    App.backup_button.configure(state="normal")
    App.backup_progressbar.stop()


def run_backup(App, DESTINATION_PATH):
    """Start thread when backup is about to take action"""
    threading.Thread(target=start_progress_bar, args=(
        App, DESTINATION_PATH), daemon=True).start()
