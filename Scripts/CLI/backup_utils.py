import os
import time
import pyzipper
import threading
import colorama
from datetime import date
from pyzipper import BadZipFile
from ..file_utils import get_drive_usage_percentage, backup_expiry_date, last_backup
from ..remote_utils import SFTP
from ..configs import config
from getpass import getpass
from colorama import Fore as F
colorama.init(autoreset=True)


class Backup:
    """
    Handle the creation, compression, encryption, and storage of backups.
    """
    def zip_files(self, SOURCE_PATHS, DESTINATION_PATH):
        """
        Zip source path files to destination path:
        - Supported compression methods: ZIP_DEFLATED, ZIP_STORED, ZIP_LZMA, ZIP_BZIP2.
        - Enabled Zip64 (this parameter use the ZIP64 extensions when the zip file is larger than 4GiB).
        - Set compression level (1: fast process, 9: small file size).
        """
        print("[!] backup init")
        if get_drive_usage_percentage() <= 90:
            print("[+] driver usage is below 90%")
            print("[!] setting expiry date..")
            if config.get('backup_expiry_date') != "Forever":
                backup_expiry_date(DESTINATION_PATH)

            filename = f"{DESTINATION_PATH}{date.today()}.zip"
            compression_method = self.get_compression_method()
            compression_level = config.get('compression_level')

            encryption, self.password = None, None
            if config.get('encryption') and config.get('compression_method') in ["ZIP_DEFLATED", "ZIP_STORED"]:
                encryption = pyzipper.WZ_AES
                self.password = self.get_backup_password()

            print("[!] Opening zipfile in write mode")
            with pyzipper.AESZipFile(file=filename, mode='w', compression=compression_method, encryption=encryption,
                                     allowZip64=True, compresslevel=compression_level) as zipObj:
                try:
                    if self.password:
                        zipObj.setpassword(self.password)
                except UnboundLocalError:
                    pass

                start = time.time()
                print("[!] iterating..")
                i, j = 1, 1
                # iterate over each path in the source list
                for item in SOURCE_PATHS:
                    print(f"[{i}] iterating over {item}")
                    # iterate over the files and folders in the path
                    for root, dirs, files in os.walk(item):
                        print(f"[{j}] iterating over files and folders in {item}")
                        for dirname in dirs:
                            dirpath = os.path.join(root, dirname)
                            print(f"[+] Writing '{dirname}' to zip")
                            zipObj.write(dirpath)

                        for filename in files:
                            filepath = os.path.join(root, filename)
                            print(f"[+] Writing '{filename}' to zip")
                            zipObj.write(filepath)
                        j += 1
                    i += 1
                end = time.time()

            self.check_zip_file(DESTINATION_PATH)
            self.upload_to_remote(DESTINATION_PATH)
            print(f"[!] Finished in {end-start:.1f}s")
            print(f"{F.LIGHTYELLOW_EX}[*] Backup completed successfully.")
        else:
            print(f"{F.LIGHTYELLOW_EX}[*] Your Drive storage is almost full.\nTo make sure your files can sync, clean up space.")


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
        compression_method_key = config.get('compression_method')
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
            print(f"{F.LIGHTRED_EX}[*] The backup file is corrupted.")

    def upload_to_remote(self, DESTINATION_PATH):
        """
        Upload zip file to the sftp server.
        """
        if config.get('sftp'):
            if config.get('sftp_hostname') and config.get('sftp_username') and config.get('sftp_password'):
                SFTP().backup_to_sftp_server(DESTINATION_PATH)
            else:
                print(f"{F.LIGHTRED_EX}[*] SFTP is enabled but credentials are missing in settings.json.")

    def get_backup_password(self):
        """
        Prompt the user to enter password and return it as bytes.
        """
        password = getpass("Backup Password: ")
        return bytes(password, 'utf-8')

    def perform_backup(self, SOURCE_PATHS, DESTINATION_PATH):
        """
        Create and start a thread for the backup process.
        """
        threading.Thread(target=self.zip_files(SOURCE_PATHS, DESTINATION_PATH), daemon=True).start()
