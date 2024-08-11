#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import pyzipper
import threading
from datetime import date
from pyzipper import BadZipFile
from ..cloud_utils import GoogleDriveCloud, FTP, Dropbox
from ..system_notifications import notify_user
from ..file_utils import get_drive_usage_percentage, backup_expiry_date, last_backup
from ..configs import config
import customtkinter as ctk

google_drive = GoogleDriveCloud()
ftp = FTP()
dropbox = Dropbox()

class Backup:
    """
    Handle the creation, compression, encryption, and storage of backups.
    """

    def zip_files(self, App, SOURCE_PATHS, DESTINATION_PATH):
        """
        Zip (backup) source path files to destination path:
            * Supported compression methods: ZIP_DEFLATED, ZIP_STORED, ZIP_LZMA, ZIP_BZIP2.
            * Enabled Zip64 (this parameter use the ZIP64 extensions when the zip file is larger than 4GiB).
            * Set compression level (1: fast ... 9: saves storage space).
        """
        if get_drive_usage_percentage() <= 90:
            if config['backup_expiry_date'] != "Forever":
                backup_expiry_date(DESTINATION_PATH)

            try:
                file_name = f"{DESTINATION_PATH}{date.today()}.zip"
                compression_method = self.get_compression_method()
                compression_level = config['compression_level']
                if config['encryption'] and (config['compression_method'] == "ZIP_DEFLATED" or config['compression_method'] == "ZIP_STORED"):
                    encryption = pyzipper.WZ_AES
                    self.password = self.get_backup_password()
                else:
                    encryption = None
                    self.password = None

                with pyzipper.AESZipFile(file=file_name, mode='w', compression=compression_method, encryption=encryption, allowZip64=True, compresslevel=int(compression_level)) as zipObj:
                    try:
                        zipObj.setpassword(self.password)
                    except UnboundLocalError:
                        pass

                    # Iterate over each path in the source list
                    for item in SOURCE_PATHS:
                        source_item_label = ctk.CTkLabel(master=App, text=item, height=20, font=('Helvetica', 12))
                        source_item_label.place(x=15, y=290)

                        # Iterate over the files and folders in the path
                        for root, dirs, files in os.walk(item):
                            for dirname in dirs:
                                dirpath = os.path.join(root, dirname)
                                zipObj.write(dirpath)

                            for filename in files:
                                filepath = os.path.join(root, filename)
                                zipObj.write(filepath)
                        source_item_label.place_forget()

                self.check_zip_file(DESTINATION_PATH)
                self.upload_to_cloud(DESTINATION_PATH)

                notify_user(
                    title="SafeArchive: Backup Completed",
                    message=f"SafeArchive has finished the backup to '{DESTINATION_PATH.replace('SafeArchive/', '')}'.",
                    icon='backup_completed.ico'
                )

            except RuntimeError:
                source_item_label.place_forget()
                App.backup_button.configure(state="normal")
                App.backup_progressbar.stop()
            except TypeError:
                App.backup_button.configure(state="normal")
                App.backup_progressbar.stop()
        else:
            notify_user(
                title='SafeArchive: [Warning] Your Drive storage is running out.',
                message='Your Drive storage is almost full. To make sure your files can sync, clean up space.',
                icon='drive.ico'
            )


    def get_compression_method(self):
        """
        Retrieve the compression method specified in the configuration.
        Return the corresponding pyzipper attribute.
        """
        compression_mapping = {
            "ZIP_STORED": pyzipper.ZIP_STORED,
            "ZIP_DEFLATED": pyzipper.ZIP_DEFLATED,
            "ZIP_BZIP2": pyzipper.ZIP_BZIP2,
            "ZIP_LZMA": pyzipper.ZIP_LZMA
        }

        compression_method_key = config['compression_method']
        compression_method = compression_mapping.get(compression_method_key)
        return compression_method


    def check_zip_file(self, DESTINATION_PATH):
        """
        Check if the zip file is valid and not corrupted.
        """
        filepath = os.path.join(DESTINATION_PATH, last_backup(DESTINATION_PATH))
        try:
            with pyzipper.AESZipFile(f"{filepath}.zip") as zf:
                zf.setpassword(self.password)
                zf.testzip()
        except BadZipFile:
            notify_user(
                title='SafeArchive: [Error] Backup corrupted.',
                message='The backup file is corrupted.',
                icon='error.ico'
            )


    def upload_to_cloud(self, DESTINATION_PATH):
        """
        Initialize & upload local backups to the cloud.
        """
        if config['storage_provider'] == "Google Drive":
            google_drive.backup_to_google_drive(DESTINATION_PATH)    
        elif config['storage_provider'] == "FTP":
            ftp.backup_to_ftp_server(DESTINATION_PATH)
        elif config['storage_provider'] == "Dropbox":
            dropbox.upload_to_dropbox(DESTINATION_PATH)


    def get_backup_password(self):
        """
        Prompt the user to enter a password, returning it as bytes (UTF-8).
        """
        password = ctk.CTkInputDialog(text="Backup Password:", title="Backup Encryption")
        return bytes(password.get_input(), 'utf-8')


    def start_progress_bar(self, App, SOURCE_PATHS, DESTINATION_PATH):
        """
        Start/Stop the progress bar while performing the backup operation.
        """
        App.backup_progressbar.start()
        App.backup_button.configure(state="disabled")
        self.zip_files(App, SOURCE_PATHS, DESTINATION_PATH)
        App.backup_button.configure(state="normal")
        App.backup_progressbar.stop()


    def perform_backup(self, App, SOURCE_PATHS, DESTINATION_PATH):
        """
        Create and start a thread for the backup process.
        """
        threading.Thread(target=self.start_progress_bar, args=(
            App, SOURCE_PATHS, DESTINATION_PATH), daemon=True).start()
