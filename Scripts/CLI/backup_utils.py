#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import sys
import time
import pyzipper
import threading
import colorama
from datetime import date
from pyzipper import BadZipFile
from ..file_utils import get_drive_usage_percentage, backup_expiry_date, last_backup
from ..cloud_utils import GoogleDriveCloud, FTP, Dropbox
from ..system_notifications import notify_user
from ..configs import config
from getpass import getpass
from colorama import Fore as F
colorama.init(autoreset=True)

config.load()
google_drive = GoogleDriveCloud()
dropbox = Dropbox()
ftp = FTP()


class Backup:
    """
    Handle the creation, compression, encryption, and storage of backups.
    """

    def zip_files(self, SOURCE_PATHS, DESTINATION_PATH):
        """
        Zip (backup) source path files to destination path:
            * Supported compression methods: ZIP_DEFLATED, ZIP_STORED, ZIP_LZMA, ZIP_BZIP2.
            * Enabled Zip64 (this parameter use the ZIP64 extensions when the zip file is larger than 4GiB).
            * Set compression level (1: fast ... 9: saves storage space).
        """
        print("[!] backup init")
        if get_drive_usage_percentage() <= 90:
            print("[+] driver usage is below 90%")
            print("[!] setting expiry date..")
            if config['backup_expiry_date'] != "Forever":
                backup_expiry_date(DESTINATION_PATH)

            file_name = f"{DESTINATION_PATH}{date.today()}.zip"
            compression_method = self.get_compression_method()
            compression_level = config['compression_level']
            if config['encryption'] and (config['compression_method'] == "ZIP_DEFLATED" or config['compression_method'] == "ZIP_STORED"):
                encryption = pyzipper.WZ_AES
                self.password = self.get_backup_password()
                if not self.password:
                    notify_user(message="The two password fields didn't match.", terminal_color=F.LIGHTRED_EX)
                    sys.exit()
            else:
                encryption = None
                self.password = None

            print("[!] Opening zipfile in write mode")
            with pyzipper.AESZipFile(file=file_name, mode='w', compression=compression_method, encryption=encryption, allowZip64=True, compresslevel=int(compression_level)) as zipObj:
                try:
                    zipObj.setpassword(self.password)
                except UnboundLocalError:
                    pass

                start = time.time()
                print("[!] iterating..")
                i, l = 1, 1
                # Iterate over each path in the source list
                for item in SOURCE_PATHS:
                    print(f"[{i}] iterating over {item}")
                    # Iterate over the files and folders in the path
                    for root, dirs, files in os.walk(item):
                        print(f"[{l}] iterating over files and folders in {item}")
                        for dirname in dirs:
                            dirpath = os.path.join(root, dirname)
                            print(f"[+] Writing '{dirname}' to zip")
                            zipObj.write(dirpath)

                        for filename in files:
                            filepath = os.path.join(root, filename)
                            print(f"[+] Writing '{filename}' to zip")
                            zipObj.write(filepath)
                        l += 1
                    i += 1
                end = time.time()

            self.check_zip_file(DESTINATION_PATH)
            self.upload_to_cloud(DESTINATION_PATH)
            print(f"[!] Finished in {end-start:.1f}s")
            notify_user(message="Backup completed successfully.", terminal_color=F.LIGHTYELLOW_EX)
        else:
            notify_user(message="Your Drive storage is almost full.\nTo make sure your files can sync, clean up space.", terminal_color=F.LIGHTYELLOW_EX)


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
            notify_user(message="The backup file is corrupted.", terminal_color=F.LIGHTRED_EX)


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
        Prompt the user to enter and confirm a password, returning it as bytes (UTF-8).
        """
        password = getpass("Backup Password: ")
        confirm_password = getpass("Confirm Backup Password: ")
        return bytes(password, 'utf-8') if password == confirm_password else None


    def perform_backup(self, SOURCE_PATHS, DESTINATION_PATH):
        """
        Create and start a thread for the backup process.
        """
        threading.Thread(target=self.zip_files(SOURCE_PATHS, DESTINATION_PATH), daemon=True).start()
