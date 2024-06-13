#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import pyzipper
import threading
import colorama
from datetime import date
from pyzipper import BadZipFile
from SafeArchive.Scripts.file_utils import get_drive_usage_percentage, backup_expiry_date, last_backup
from SafeArchive.Scripts.cloud_utils import GoogleDriveCloud, FTP, MegaCloud, Dropbox
from SafeArchive.Scripts.system_notifications import notify_user
from SafeArchive.Scripts.configs import config
from getpass import getpass
from colorama import Fore as F
colorama.init(autoreset=True)

config.load()
google_drive = GoogleDriveCloud()
ftp = FTP()
mega_cloud = MegaCloud()
dropbox = Dropbox()


class Backup:

    def zip_files(self, SOURCE_PATHS, DESTINATION_PATH):
        """
        Zip (backup) source path files to destination path:
            * Compression method: ZIP_DEFLATED
            * allowZip64 is set to True (this parameter use the ZIP64 extensions when the zip file is larger than 4gb)
            * Compresslevel is set to 9 (its sometimes really slow when source path files are too large, saves storage space)
        """
        print("[!] backup init")
        if get_drive_usage_percentage() <= 90:
            print("[+] driver usage is below 90%")
            print("[!] setting expiry date..")
            if config['backup_expiry_date'] != None:
                backup_expiry_date(DESTINATION_PATH)

            file_name = f"{DESTINATION_PATH}{date.today()}.zip"
            compression_method = self.get_compression_method()
            allowZip64 = config['allowZip64']
            compression_level = config['compression_level']
            if config['encryption'] and (config['compression_method'] == "ZIP_DEFLATED" or config['compression_method'] == "ZIP_STORED"):
                encryption = pyzipper.WZ_AES
                self.password = self.get_backup_password()
            else:
                encryption = None
                self.password = None

            print("[!] Opening zipfile in write mode")
            with pyzipper.AESZipFile(file=file_name, mode='w', compression=compression_method, encryption=encryption, allowZip64=allowZip64, compresslevel=int(compression_level)) as zipObj:
                try:
                    zipObj.setpassword(self.password)
                except UnboundLocalError:
                    pass

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

            self.check_zip_file(DESTINATION_PATH)
            self.upload_to_cloud(DESTINATION_PATH)
            notify_user(message="Backup completed successfully.", terminal_color=F.LIGHTYELLOW_EX)
        else:
            notify_user(message="Your Drive storage is almost full.\nTo make sure your files can sync, clean up space.", terminal_color=F.LIGHTYELLOW_EX)


    def get_compression_method(self):
        # Define a mapping from JSON values to pyzipper attributes
        compression_mapping = {
            "ZIP_STORED": pyzipper.ZIP_STORED,
            "ZIP_DEFLATED": pyzipper.ZIP_DEFLATED,
            "ZIP_BZIP2": pyzipper.ZIP_BZIP2,
            "ZIP_LZMA": pyzipper.ZIP_LZMA
        }

        # Retrieve the compression method from the configuration
        compression_method_key = config['compression_method']

        # Get the corresponding pyzipper attribute
        compression_method = compression_mapping.get(compression_method_key)

        return compression_method


    def check_zip_file(self, DESTINATION_PATH):
        """Check if zip file is valid and not corrupted"""
        filepath = os.path.join(DESTINATION_PATH, last_backup(DESTINATION_PATH))
        try:
            with pyzipper.AESZipFile(f"{filepath}.zip") as zf:
                zf.setpassword(self.password)
                zf.testzip()
        except BadZipFile:
            notify_user(message="The backup file is corrupted.", terminal_color=F.LIGHTRED_EX)


    def upload_to_cloud(self, DESTINATION_PATH):
        """Initialize & Upload local backups to cloud if JSON value is True"""
        if config['backup_to_cloud']:
            if config['storage_provider'] == "Google Drive":
                google_drive.backup_to_google_drive(DESTINATION_PATH)
            elif config['storage_provider'] == "FTP":
                ftp.backup_to_ftp_server(DESTINATION_PATH)
            elif config['storage_provider'] == "Mega":
                mega_cloud.backup_to_mega(DESTINATION_PATH)
            elif config['storage_provider'] == "Dropbox":
                dropbox.upload_to_dropbox(DESTINATION_PATH)


    def get_backup_password(self):
        """Return user-input backup password in bytes (UTF-8)"""
        password = getpass("Backup Password: ")
        return bytes(password, 'utf-8')


    def perform_backup(self, SOURCE_PATHS, DESTINATION_PATH):
        """Start thread when backup is about to take action"""
        threading.Thread(target=self.zip_files(SOURCE_PATHS, DESTINATION_PATH), daemon=True).start()
