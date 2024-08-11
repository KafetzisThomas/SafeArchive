#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import sys
import pyzipper
import threading
import colorama
from getpass import getpass
from prettytable import PrettyTable
from ..configs import config
from ..system_notifications import notify_user
from colorama import Fore as F

colorama.init(autoreset=True)
config.load()


class RestoreBackup:
    """
    Provide functionality to restore backups from a zip file.
    """

    def extract_item(self, DESTINATION_PATH, **backups_table):
        """
        Extract selected zip file & move zip file content to it's original location.
        """
        table = PrettyTable()
        table.field_names = ["ID", "Backups", "Type"]

        # Iterate over the files in the destination path
        for index, zip_file in enumerate(os.listdir(DESTINATION_PATH)):
            filename, _, filetype = zip_file.partition('.')

            # Check if it's a zip file
            if filetype == 'zip':
                backups_table[index] = filename
                # Add file information to the table
                table.add_row([index, filename, filetype])

        print(table)

        try:
            selected_id = input("\nSelect backup to restore (Enter the ID): ")
        except KeyboardInterrupt:
            print(f"\n{F.LIGHTCYAN_EX}* Exiting...")
            sys.exit()

        if selected_id.isdigit() and int(selected_id) in backups_table:
            selected_filename = backups_table[int(selected_id)]
            file_name = f"{DESTINATION_PATH}{selected_filename}.zip"

            # Open the zipfile in read mode, extract its content
            with pyzipper.AESZipFile(file=file_name, mode='r') as zipObj:
                try:
                    if config['encryption'] and (config['compression_method'] == "ZIP_DEFLATED" or config['compression_method'] == "ZIP_STORED"):
                        zipObj.setpassword(self.get_backup_password())
                    zipObj.extractall(config['destination_path'])
                    notify_user(message="Files Restored Sucessfully.", terminal_color=F.LIGHTYELLOW_EX)
                except (RuntimeError, TypeError):
                    pass
        else:
            notify_user(message="Invalid backup ID selected.", terminal_color=F.LIGHTRED_EX)
            sys.exit()


    def get_backup_password(self):
        """
        Prompt the user to enter password and return it as bytes.
        """
        password = getpass("Backup Password: ")
        return bytes(password, 'utf-8')


    def run_restore_thread(self, DESTINATION_PATH):
        """
        Create and start a thread for the restore process.
        """
        threading.Thread(target=self.extract_item(DESTINATION_PATH), daemon=True).start()
