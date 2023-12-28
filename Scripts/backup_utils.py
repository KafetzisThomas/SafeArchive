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
        notify_drive_space_limitation(config['notification'])


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


def restore_backup(App, DESTINATION_PATH):
    """
    Create a toplevel widget containing a listbox inside a frame
    Show last backups inside the listbox
    Restore last backup files by selecting a specific one
    """

    restore_window = tk.Toplevel(App)  # Open new window (restore_window)
    restore_window.title("Select backup to restore")  # Set window title
    restore_window.geometry("440x240")  # Set window size
    restore_window.iconbitmap("assets/icon.ico")  # Set window title icon
    restore_window.resizable(False, False)  # Disable minimize/maximize buttons
    restore_window.configure(background="#242424")  # Set background color

    frame = ctk.CTkFrame(master=restore_window,
                         corner_radius=10, height=180, width=425)
    frame.place(x=8, y=8)

    if config['appearance_mode'] == "dark":
        restore_window.configure(background="#343638")
        background = "#343638"
        foreground = "white"
    else:
        restore_window.configure(background="#ebebeb")
        background = "#ebebeb"
        foreground = "black"

    listbox = tk.Listbox(
        master=frame,
        height=9,
        width=47,
        background=background,
        foreground=foreground,
        activestyle='dotbox',
        font='Helvetica, 13',
        justify="center"
    )

    listbox.pack()

    for index, zip_file in enumerate(os.listdir(DESTINATION_PATH)):
        filename, _, filetype = zip_file.partition('.')

        if filetype == 'zip':
            listbox.insert(index, filename)

    def selected_item():
        """
        Extract (restore) selected zip file (backup)
        Move zip file content to it's original location
        """
        App.restore_button.configure(
            state="disabled")  # Change backup button state to disabled

        for item in listbox.curselection():
            # Open the zipfile in read mode, extract its content
            with zipfile.ZipFile(f'{DESTINATION_PATH}{listbox.get(item)}.zip') as zipObj:
                zipObj.extractall(config['destination_path'])

        notify_restore_completion(config['notification'])
        # Change backup button state back to normal
        App.restore_button.configure(state="normal")

    def run_restore():
        """Start thread when restoration is processing"""
        threading.Thread(target=selected_item, daemon=True).start(
        )  # Create restore process thread

    App.restore_button = ctk.CTkButton(
        master=restore_window, text="Restore backup", command=run_restore)
    App.restore_button.place(x=155, y=200)
