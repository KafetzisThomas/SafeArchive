#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import pyzipper
import threading
import colorama
from datetime import date
from pyzipper import BadZipFile
from Scripts.cli_file_utils import get_drive_usage_percentage, backup_expiry_date, last_backup
from Scripts.cli_cloud_utils import GoogleDriveCloud, FTP, MegaCloud, Dropbox
from Scripts.cli_configs import config
from getpass import getpass
from colorama import Fore as F
colorama.init(autoreset=True)

config.load()
google_drive = GoogleDriveCloud()
ftp = FTP()
mega_cloud = MegaCloud()
dropbox = Dropbox()


class Backup:

    def zip_files(self, DESTINATION_PATH):
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

            encryption = pyzipper.WZ_AES if config['encryption'] else None
            self.password = self.get_backup_password() if config['encryption'] else None
            print("[!] Opening zipfile in write mode")
            with pyzipper.AESZipFile(f'{DESTINATION_PATH}{date.today()}.zip', mode='w', compression=pyzipper.ZIP_DEFLATED, encryption=encryption, allowZip64=True, compresslevel=9) as zipObj:
                try:
                    zipObj.setpassword(self.password)
                except UnboundLocalError:
                    pass

                print("[!] iterating..")
                i, l = 1, 1
                # Iterate over each path in the source list
                for item in config['source_path']:
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
            print(f"{F.LIGHTYELLOW_EX}* Backup completed successfully.")
        else:
            print(f"{F.LIGHTYELLOW_EX}* Your Drive storage is almost full.\nTo make sure your files can sync, clean up space.")


    def check_zip_file(self, DESTINATION_PATH):
        """Check if zip file is valid and not corrupted"""
        filepath = os.path.join(DESTINATION_PATH, last_backup(DESTINATION_PATH))
        try:
            with pyzipper.AESZipFile(f"{filepath}.zip") as zf:
                zf.setpassword(self.password)
                zf.testzip()
        except BadZipFile:
            print(f"{F.LIGHTRED_EX}* The backup file is corrupted.")


    def upload_to_cloud(self, DESTINATION_PATH):
        """Initialize & Upload local backups to cloud if JSON value is True"""
        if config['backup_to_cloud']:
            if config['storage_provider'] == "Google Drive":
                google_drive.initialize()
                if google_drive.get_cloud_usage_percentage() >= 90:
                    print(f"{F.LIGHTYELLOW_EX}* Your Google Drive storage is almost full.\nTo make sure your files can sync, clean up space.")
                else:
                    google_drive.backup_to_google_drive(DESTINATION_PATH[:-1], DESTINATION_PATH, parent_folder_id=google_drive.gdrive_folder['id'])
            elif config['storage_provider'] == "FTP":
                try:
                    ftp.backup_to_ftp_server(DESTINATION_PATH)
                except AttributeError:
                    print(f"{F.LIGHTYELLOW_EX}* FTP not configured.\nPlease edit the configuration file (settings.json) to add your ftp credentials.")
            elif config['storage_provider'] == "Mega":
                mega_cloud.initialize()
                if mega_cloud.get_used_space_percentage() >= 90:
                    print(f"{F.LIGHTYELLOW_EX}* Your Mega storage is almost full.\nTo make sure your files can sync, clean up space.")
                else:
                    mega_cloud.backup_to_mega(DESTINATION_PATH)
            elif config['storage_provider'] == "Dropbox":
                dropbox.initialize()
                if dropbox.get_used_space_percentage() >= 90:
                    print(f"{F.LIGHTYELLOW_EX}* Your Dropbox storage is almost full.\nTo make sure your files can sync, clean up space.")
                else:    
                    dropbox.upload_to_dropbox(DESTINATION_PATH)


    def get_backup_password(self):
        """Return user-input backup password in bytes (UTF-8)"""
        password = getpass("Backup Password: ")
        return bytes(password, 'utf-8')


    def perform_backup(self, DESTINATION_PATH):
        """Start thread when backup is about to take action"""
        threading.Thread(target=self.zip_files(DESTINATION_PATH), daemon=True).start()
