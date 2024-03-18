#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
This file allows you to sync your files with storage providers.
It allows uploading, updating, and deleting files in a specified folder.
Note: This feature becomes optional in the program. If you want to use it, just set the JSON value to true.
For detailed setup instructions:
https://github.com/KafetzisThomas/SafeArchive/wiki
"""

import os
import sys
import ftplib
import dropbox
import colorama
from mega import Mega
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from pydrive2.settings import InvalidConfigError
from Scripts.cli_configs import config
from colorama import Fore as F
colorama.init(autoreset=True)

config.load()
mega = Mega()


class GoogleDriveCloud:

    def backup_to_google_drive(self, DESTINATION_PATH):
        """Upload local backup files to Google Drive"""

        self.initialize_connection()
        if self.get_cloud_usage_percentage() < 90:
            foldername = os.path.basename(DESTINATION_PATH[:-1])
            self.gdrive_folder = self.get_or_create_folder(foldername)

            for filename in os.listdir(DESTINATION_PATH[:-1]):
                filepath = os.path.join(DESTINATION_PATH[:-1], filename)
                gdrive_file = self.get_or_create_file(filename, filepath)

                # Update existing files or upload new ones
                gdrive_file.SetContentFile(filepath)
                gdrive_file.Upload()

            # Delete files in Google Drive that don't exist in the local folder anymore
            self.delete_files_not_in_local_folder(DESTINATION_PATH[:-1])
        else:
            print(f"{F.LIGHTYELLOW_EX}* Your Google Drive storage is almost full.\nTo make sure your files can sync, clean up space.")


    def initialize_connection(self):
        """Authenticate request and initialize Google Drive"""

        try:
            gauth = GoogleAuth()
            gauth.LocalWebserverAuth()
            self.drive = GoogleDrive(gauth)
        except InvalidConfigError:
            print(f"{F.LIGHTYELLOW_EX}* [Error] File 'client_secrets.json' is missing.\nFile not found in the program directory.\nPlease refer to the documentation for instructions on how to get it.")
            sys.exit()

        # Check if the folder already exists in Google Drive
        folder_query = ("title='SafeArchive' and mimeType='application/vnd.google-apps.folder' and trashed=false")
        file_list = self.drive.ListFile({'q': folder_query}).GetList()

        if file_list:
            # The folder already exists, so just update the existing files
            self.gdrive_folder = file_list[0]
        else:
            # The folder doesn't exist, so create a new one
            self.gdrive_folder = self.drive.CreateFile(
                {'title': 'SafeArchive', 'mimeType': 'application/vnd.google-apps.folder'})
            self.gdrive_folder.Upload()


    def get_cloud_usage_percentage(self):
        """Return cloud usage percentage"""
        account_details = self.drive.GetAbout()
        used_storage = int(account_details['quotaBytesUsed'])
        total_storage = int(account_details['quotaBytesTotal'])
        storage_usage_percentage = (used_storage / total_storage) * 100
        return storage_usage_percentage


    def get_or_create_folder(self, foldername):
        """Get or create folder in Google Drive"""
        folder_query = (f"title='{foldername}' and mimeType='application/vnd.google-apps.folder' and trashed=false")
        folder_list = self.drive.ListFile({'q': folder_query}).GetList()

        if folder_list:
            return folder_list[0]
        else:
            folder_metadata = {'title': foldername}
            if self.gdrive_folder['id']:
                folder_metadata['parents'] = [{'id': self.gdrive_folder['id']}]

            new_folder = self.drive.CreateFile(folder_metadata)
            new_folder.Upload()
            return new_folder


    def get_or_create_file(self, filename):
        """Get or create file in Google Drive"""

        file_query = (f"title='{filename}' and '{self.gdrive_folder['id']}' in parents and trashed=false")
        file_list = self.drive.ListFile({'q': file_query}).GetList()

        if file_list:
            return file_list[0]
        else:
            new_file = self.drive.CreateFile({'title': filename, 'parents': [{'id': self.gdrive_folder['id']}]})
            return new_file


    def delete_files_not_in_local_folder(self, local_folder_path):
        """Delete files in Google Drive that don't exist in the local folder"""
        drive_files = self.drive.ListFile({'q': f"'{self.gdrive_folder['id']}' in parents and trashed=false"}).GetList()

        for file in drive_files:
            local_file_path = os.path.join(local_folder_path, file['title'])
            if not os.path.exists(local_file_path):
                file.Trash()


class FTP:

    def __init__(self):
        """Initialize FTP server connection"""
        self.hostname = config['ftp_hostname']
        self.username = config['ftp_username']
        self.password = config['ftp_password']
        self.ftp_server = None


    def backup_to_ftp_server(self, folderpath):
        """Upload folder and files to the FTP server"""
        try:
            self.connect()
            self.create_directory()

            for file in os.listdir(folderpath):
                file_path = os.path.join(folderpath, file)
                if os.path.isfile(file_path):
                    with open(file_path, 'rb') as f:
                        self.ftp_server.storbinary(f'STOR {file}', f)

            self.delete_files_not_in_local_folder(folderpath)
            self.disconnect()
        except AttributeError:
            print(f"{F.LIGHTYELLOW_EX}* FTP not configured.\nPlease edit the configuration file (settings.json) to add your ftp credentials.")


    def initialize_connection(self):
        """Connect to FTP Server"""
        self.ftp_server = ftplib.FTP(self.hostname, self.username, self.password)
        self.ftp_server.encoding = "utf-8"  # force UTF-8 encoding


    def create_directory(self):
        """Create directory on FTP server"""
        try:
            self.ftp_server.mkd('/SafeArchive')
        except ftplib.error_perm:
            pass
        finally:
            self.ftp_server.cwd('/SafeArchive')


    def delete_files_not_in_local_folder(self, folderpath):
        """Delete remote files that are not present locally"""
        remote_files = self.ftp_server.nlst()

        for file in remote_files:
            if file not in os.listdir(folderpath):
                self.ftp_server.delete(file)


    def disconnect(self):
        """Disconnect from FTP Server"""
        if self.ftp_server:
            self.ftp_server.quit()


class MegaCloud:

    def backup_to_mega(self, DESTINATION_PATH):
        """Upload folder and files to Mega account"""
        self.initialize_connection()
        if self.get_used_space_percentage() < 90:
            folder = self.create_directory()
            for file_name in os.listdir(DESTINATION_PATH):
                file_path = os.path.join(DESTINATION_PATH, file_name)
                try:
                    self.m.upload(file_path, folder[0])
                    print(f"Uploaded {file_name} successfully.")
                except Exception as e:
                    print(f"Error uploading {file_name}: {str(e)}")
        else:
            print(f"{F.LIGHTYELLOW_EX}* Your Mega storage is almost full.\nTo make sure your files can sync, clean up space.")


    def initialize_connection(self):
        """Login to Mega"""
        self.m = mega.login(config['mega_email'], config['mega_password'])


    def get_used_space_percentage(self):
        """Return used space percentage"""
        space = self.m.get_storage_space(kilo=True)
        total_space = space.get('total')
        used_space = space.get('used')
        space_usage_percentage = (used_space / total_space) * 100
        return space_usage_percentage


    def create_directory(self):
        """Create directory on Mega account"""
        files = self.m.get_files()
        if "SafeArchive" not in files:
            self.m.create_folder('SafeArchive')
        folder = self.m.find('SafeArchive')
        return folder


class Dropbox:

    def upload_to_dropbox(self, DESTINATION_PATH):
        """Upload folder and files to Dropbox account"""
        self.initialize_connection()
        if self.get_used_space_percentage() < 90:
            self.create_directory()
            self.delete_directory(self.dropbox_folder_path)
            for root, dirs, files in os.walk(DESTINATION_PATH):
                for filename in files:
                    local_file_path = os.path.join(root, filename)
                    dropbox_file_path = os.path.join(self.dropbox_folder_path, os.path.relpath(local_file_path, DESTINATION_PATH))
                    with open(local_file_path, 'rb') as f:
                        self.dbx.files_upload(f.read(), dropbox_file_path, mode=dropbox.files.WriteMode.overwrite)
        else:
            print(f"{F.LIGHTYELLOW_EX}* Your Dropbox storage is almost full.\nTo make sure your files can sync, clean up space.")


    def initialize_connection(self):
        """Authenticate access token"""
        self.dbx = dropbox.Dropbox(config['dropbox_access_token'])
        self.dropbox_folder_path = '/SafeArchive'


    def get_used_space_percentage(self):
        space = self.dbx.users_get_space_usage()
        used_space = space.used
        total_space = space.allocation.get_individual().allocated
        space_usage_percentage = (used_space / total_space) * 100
        return space_usage_percentage


    def create_directory(self):
        """Create directory on Dropbox account"""
        try:
            self.dbx.files_get_metadata(self.dropbox_folder_path)
        except dropbox.exceptions.ApiError as e:
            if e.error.is_path() and e.error.get_path().is_not_found():
                self.dbx.files_create_folder(self.dropbox_folder_path)


    def delete_directory(self):
        """Delete existing directory so files to be overwritten"""
        self.dbx.files_delete_v2(self.dropbox_folder_path)
