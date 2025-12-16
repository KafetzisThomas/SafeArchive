"""
This module handles remote file transfers via FTP.

Setup Instructions:
1. Enable the FTP switch within the application settings or set the "ftp" value to true in settings.json.
2. Configure your credentials (hostname, username, password) directly in settings.json.
"""

import os
import ftplib
from .configs import config


class FTP:
    """
    Handle file transfers to an FTP server.
    """
    def __init__(self):
        self.hostname = config['ftp_hostname']
        self.username = config['ftp_username']
        self.password = config['ftp_password']
        self.ftp_server = None

    def backup_to_ftp_server(self, folderpath):
        """
        Upload files to the ftp server.
        """
        self.initialize_connection()
        self.create_directory()
        for file in os.listdir(folderpath):
            file_path = os.path.join(folderpath, file)
            if os.path.isfile(file_path):
                with open(file_path, 'rb') as f:
                    self.ftp_server.storbinary(f'STOR {file}', f)

        self.delete_files_not_in_local_folder(folderpath)
        self.disconnect()

    def initialize_connection(self):
        """
        Connect to the ftp server.
        """
        self.ftp_server = ftplib.FTP(self.hostname, self.username, self.password)
        self.ftp_server.encoding = "utf-8"

    def create_directory(self):
        """
        Create directory on ftp server.
        """
        try:
            self.ftp_server.mkd('/SafeArchive')
        except ftplib.error_perm:
            pass
        finally:
            self.ftp_server.cwd('/SafeArchive')

    def delete_files_not_in_local_folder(self, folderpath):
        """
        Delete remote files that are not present locally.
        """
        remote_files = self.ftp_server.nlst()

        for file in remote_files:
            if file not in os.listdir(folderpath):
                self.ftp_server.delete(file)

    def disconnect(self):
        """
        Disconnect from the ftp server.
        """
        if self.ftp_server:
            self.ftp_server.quit()
