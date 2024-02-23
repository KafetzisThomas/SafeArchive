#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import sys
import pyzipper
import threading
import colorama
from getpass import getpass
from prettytable import PrettyTable
from Scripts.cli_configs import config
from colorama import Fore as F
colorama.init(autoreset=True)


class RestoreBackup:

    def extract_item(self, DESTINATION_PATH, **backups_table):
        """
        Extract (restore) selected zip file (backup)
        Move zip file content to it's original location
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
            # Open the zipfile in read mode, extract its content
            with pyzipper.AESZipFile(f'{DESTINATION_PATH}{selected_filename}.zip', mode='r') as zipObj:
                zipObj.extractall(config['destination_path'])
                try:
                    if config['encryption']:
                        zipObj.setpassword(self.get_backup_password())
                    zipObj.extractall(config['destination_path'])
                    ##notify_restore_completion(config['notifications'])##
                except (RuntimeError, TypeError):
                    pass
        else:
            print(f"{F.LIGHTRED_EX}* Invalid backup ID selected.")
            sys.exit()


    def get_backup_password(self):
        password = getpass("Backup Password: ")
        return bytes(password, 'utf-8')


    def run_restore_thread(self, DESTINATION_PATH):
        """Create restore process thread"""
        threading.Thread(target=self.extract_item(DESTINATION_PATH), daemon=True).start()
