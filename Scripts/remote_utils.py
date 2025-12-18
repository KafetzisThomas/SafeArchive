"""
This module handles remote file transfers via SFTP.

Setup Instructions:
1. Enable the SFTP switch within the application settings or set the "sftp" value to true in settings.json.
2. Configure your credentials (hostname, username, password) directly in settings.json.
"""

import os
import paramiko
from .configs import config


class SFTP:
    """
    Handle file transfers to an SFTP server.
    """
    def __init__(self):
        self.hostname = config.get('sftp_hostname')
        self.username = config.get('sftp_username')
        self.password = config.get('sftp_password')
        self.port = config.get('sftp_port')
        self.sftp_server = None

    def backup_to_sftp_server(self, folderpath):
        """
        Upload files to the sftp server.
        """
        try:
            self.initialize_connection()
            self.create_directory()
            for file in os.listdir(folderpath):
                filepath = os.path.join(folderpath, file)
                if os.path.isfile(filepath):
                    self.sftp_server.put(filepath, file)
            self.delete_files_not_in_local_folder(folderpath)
        finally:
            self.disconnect()

    def initialize_connection(self):
        """
        Connect to the sftp server.
        """
        self.transport = paramiko.Transport((self.hostname, self.port))  # create socket connection
        self.transport.connect(username=self.username, password=self.password)
        self.sftp_server = paramiko.SFTPClient.from_transport(self.transport)

    def create_directory(self):
        """
        Create directory on sftp server if it doesn't exist.
        """
        target_dir = '/SafeArchive'
        try:
            self.sftp_server.chdir(target_dir)
        except IOError:  # dir likely doesn't exist
            self.sftp_server.mkdir(target_dir)
            self.sftp_server.chdir(target_dir)

    def delete_files_not_in_local_folder(self, folderpath):
        """
        Delete remote files that are not present locally.
        """
        remote_files = self.sftp_server.listdir()
        local_files = os.listdir(folderpath)
        for file in remote_files:
            if file not in local_files:
                self.sftp_server.remove(file)

    def disconnect(self):
        """
        Disconnect from the sftp server.
        """
        if self.sftp_server:
            self.sftp_server.close()
        if self.transport:
            self.transport.close()
