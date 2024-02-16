#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import pyzipper
import threading
from datetime import date
from Scripts.cloud_utils import GoogleDriveCloud, FTP
from Scripts.notification_handlers import notify_backup_completion
from Scripts.notification_handlers import notify_cloud_space_limitation
from Scripts.notification_handlers import notify_drive_space_limitation
from Scripts.notification_handlers import notify_missing_ftp_credentials
from Scripts.file_utils import get_drive_usage_percentage
from Scripts.file_utils import backup_expiry_date
from Scripts.configs import config
import customtkinter as ctk

google_drive = GoogleDriveCloud()
ftp = FTP()


class Backup:

    def zip_files(self, App, DESTINATION_PATH):
        """
        Zip (backup) source path files to destination path:
            * Compression method: ZIP_DEFLATED
            * allowZip64 is set to True (this parameter use the ZIP64 extensions when the zip file is larger than 4gb)
            * Compresslevel is set to 9 (its sometimes really slow when source path files are too large, saves storage space)
        """
        if get_drive_usage_percentage() <= 90:
            if config['backup_expiry_date'] != "Forever (default)":
                backup_expiry_date(DESTINATION_PATH)

            try:
                encryption = pyzipper.WZ_AES if config['encryption'] else None
                password = self.get_backup_password() if config['encryption'] else None
                with pyzipper.AESZipFile(f'{DESTINATION_PATH}{date.today()}.zip', mode='w', compression=pyzipper.ZIP_DEFLATED, encryption=encryption, allowZip64=True, compresslevel=9) as zipObj:
                    try:
                        zipObj.setpassword(password)
                    except UnboundLocalError:
                        pass

                    # Iterate over each path in the source list
                    for item in config['source_path']:
                        source_item_label = ctk.CTkLabel(master=App, text=item, height=20, font=('Helvetica', 12))
                        source_item_label.place(x=15, y=430)

                        # Iterate over the files and folders in the path
                        for root, dirs, files in os.walk(item):
                            for dirname in dirs:
                                dirpath = os.path.join(root, dirname)
                                zipObj.write(dirpath)

                            for filename in files:
                                filepath = os.path.join(root, filename)
                                zipObj.write(filepath)
                        source_item_label.place_forget()

                self.upload_to_cloud(DESTINATION_PATH)
                notify_backup_completion(DESTINATION_PATH, config['notifications'])
            except RuntimeError:
                source_item_label.place_forget()
                App.backup_button.configure(state="normal")
                App.backup_progressbar.stop()
            except TypeError:
                App.backup_button.configure(state="normal")
                App.backup_progressbar.stop()
        else:
            notify_drive_space_limitation(config['notifications'])


    def upload_to_cloud(self, DESTINATION_PATH):
        """Initialize & Upload local backups to cloud if JSON value is True"""
        if config['backup_to_cloud']:
            if config['storage_provider'] == "Google Drive":
                google_drive.initialize()
                if google_drive.get_cloud_usage_percentage() >= 90:
                    notify_cloud_space_limitation(config['notifications'])
                else:
                    google_drive.backup_to_google_drive(DESTINATION_PATH[:-1], DESTINATION_PATH, parent_folder_id=google_drive.gdrive_folder['id'])
            else:
                try:
                    ftp.backup_to_ftp_server(DESTINATION_PATH)
                except AttributeError:
                    notify_missing_ftp_credentials(config['notifications'])


    def get_backup_password(self):
        password = ctk.CTkInputDialog(text="Backup Password:", title="Backup Encryption")
        return bytes(password.get_input(), 'utf-8')


    def start_progress_bar(self, App, DESTINATION_PATH):
        """Start/Stop progress bar & Call zip_files() function"""
        App.backup_progressbar.start()
        App.backup_button.configure(state="disabled")
        self.zip_files(App, DESTINATION_PATH)
        App.backup_button.configure(state="normal")
        App.backup_progressbar.stop()


    def perform_backup(self, App, DESTINATION_PATH):
        """Start thread when backup is about to take action"""
        threading.Thread(target=self.start_progress_bar, args=(
            App, DESTINATION_PATH), daemon=True).start()
