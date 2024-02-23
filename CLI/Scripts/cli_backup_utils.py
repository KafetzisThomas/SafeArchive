#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import pyzipper
import threading
from datetime import date
from Scripts.cli_functions import get_drive_usage_percentage, backup_expiry_date
from Scripts.cli_cloud_utils import GoogleDriveCloud, FTP, MegaCloud, Dropbox
from Scripts.cli_configs import config
from getpass import getpass

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
        if get_drive_usage_percentage() <= 90:
            if config['backup_expiry_date'] != None:
                backup_expiry_date(DESTINATION_PATH)

            encryption = pyzipper.WZ_AES if config['encryption'] else None
            password = self.get_backup_password() if config['encryption'] else None
            with pyzipper.AESZipFile(f'{DESTINATION_PATH}{date.today()}.zip', mode='w', compression=pyzipper.ZIP_DEFLATED, encryption=encryption, allowZip64=True, compresslevel=9) as zipObj:
                try:
                    zipObj.setpassword(password)
                except UnboundLocalError:
                    pass

                # Iterate over each path in the source list
                for item in config['source_path']:
                    # Iterate over the files and folders in the path
                    for root, dirs, files in os.walk(item):
                        for dirname in dirs:
                            dirpath = os.path.join(root, dirname)
                            zipObj.write(dirpath)

                        for filename in files:
                            filepath = os.path.join(root, filename)
                            zipObj.write(filepath)

            self.upload_to_cloud(DESTINATION_PATH)
            ##notify_backup_completion(DESTINATION_PATH, config['notifications'])##
        else:
            ##notify_drive_space_limitation(config['notifications'])##
            pass


    def upload_to_cloud(self, DESTINATION_PATH):
        """Initialize & Upload local backups to cloud if JSON value is True"""
        if config['backup_to_cloud']:
            if config['storage_provider'] == "Google Drive":
                google_drive.initialize()
                if google_drive.get_cloud_usage_percentage() >= 90:
                    ##notify_cloud_space_limitation(config['notifications'])##
                    pass
                else:
                    google_drive.backup_to_google_drive(DESTINATION_PATH[:-1], DESTINATION_PATH, parent_folder_id=google_drive.gdrive_folder['id'])
            elif config['storage_provider'] == "FTP":
                try:
                    ftp.backup_to_ftp_server(DESTINATION_PATH)
                except AttributeError:
                    ##notify_missing_ftp_credentials(config['notifications'])##
                    pass
            elif config['storage_provider'] == "Mega":
                mega_cloud.initialize()
                if mega_cloud.get_used_space_percentage() >= 90:
                    pass  # TODO: Display notification if True
                else:
                    mega_cloud.backup_to_mega(DESTINATION_PATH)
            elif config['storage_provider'] == "Dropbox":
                dropbox.initialize()
                if dropbox.get_used_space_percentage() >= 90:
                    pass  # TODO: Display notification if True
                else:    
                    dropbox.upload_to_dropbox(DESTINATION_PATH)


    def get_backup_password(self):
        password = getpass("Backup Password: ")
        return bytes(password, 'utf-8')


    def perform_backup(self, DESTINATION_PATH):
        """Start thread when backup is about to take action"""
        threading.Thread(target=self.zip_files(DESTINATION_PATH), daemon=True).start()
