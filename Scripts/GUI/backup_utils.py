import os
import pyzipper
from datetime import date
from pyzipper import BadZipFile
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QApplication, QInputDialog, QLineEdit
from ..remote_utils import FTP
from ..file_utils import get_drive_usage_percentage, backup_expiry_date, last_backup
from ..configs import config


class BackupWorker(QThread):
    """
    Worker thread that handles backup in background.
    """
    # signals to update ui elements safely in main thread
    started_signal = pyqtSignal()
    finished_signal = pyqtSignal()
    success_signal = pyqtSignal(str, str)
    warning_signal = pyqtSignal(str, str)
    error_signal = pyqtSignal(str, str)

    def __init__(self, source_paths, destination_path, password=None):
        super().__init__()
        self.source_paths = source_paths
        self.destination_path = destination_path
        self.password = password
    
    def run(self):
        """
        Zip source path files to destination path:
            - Supported compression methods: ZIP_DEFLATED, ZIP_STORED, ZIP_LZMA, ZIP_BZIP2.
            - Enabled Zip64 (this parameter use the ZIP64 extensions when the zip file is larger than 4GiB).
            - Set compression level (1: fast ... 9: saves storage space).
        """
        self.started_signal.emit()
        if get_drive_usage_percentage() <= 90:
            if config['backup_expiry_date'] != "Forever":
                backup_expiry_date(self.destination_path)
            try:
                self.perform_zip()
                self.check_zip_file()
                self.upload_to_remote()
                self.success_signal.emit(
                    "Backup Completed",
                    f"SafeArchive has finished the backup to '{self.destination_path.replace('SafeArchive/', '')}'."
                )
            except Exception as e:
                self.error_signal.emit("Backup Failed", str(e))
        else:
            self.warning_signal.emit(
                "Backup Failed",
                "Your Drive storage is almost full. To make sure your files can sync, clean up space."
            )

        self.finished_signal.emit()

    def perform_zip(self):
        filename = f"{self.destination_path}{date.today()}.zip"

        # retrieve compression method specified in the configuration
        compression_mapping = {
            "ZIP_STORED": pyzipper.ZIP_STORED, "ZIP_DEFLATED": pyzipper.ZIP_DEFLATED,
            "ZIP_BZIP2": pyzipper.ZIP_BZIP2, "ZIP_LZMA": pyzipper.ZIP_LZMA
        }
        compression_method = compression_mapping.get(config['compression_method'], pyzipper.ZIP_DEFLATED)
        compression_level = int(config['compression_level'])

        encryption = None
        if config['encryption'] and config['compression_method'] in ["ZIP_DEFLATED", "ZIP_STORED"]:
            encryption = pyzipper.WZ_AES

        with pyzipper.AESZipFile(file=filename, mode='w', compression=compression_method,
                                 encryption=encryption, compresslevel=compression_level, allowZip64=True) as zipObj:
            if self.password:
                zipObj.setpassword(self.password)

            # iterate over each path in the source list
            for item in self.source_paths:
                # iterate over the files and folders in the path
                for root, dirs, files in os.walk(item):
                    for dirname in dirs:
                        dirpath = os.path.join(root, dirname)
                        zipObj.write(dirpath)
                    for filename in files:
                        filepath = os.path.join(root, filename)
                        zipObj.write(filepath)

    def check_zip_file(self):
        """
        Check if the zip file is valid and not corrupted.
        """
        filepath = os.path.join(self.destination_path, last_backup(self.destination_path))
        try:
            with pyzipper.AESZipFile(f"{filepath}.zip") as zf:
                if self.password:
                    zf.setpassword(self.password)
                zf.testzip()
        except BadZipFile:
            raise Exception("Backup file is corrupted.")

    def upload_to_remote(self):
        """
        Upload zip file to the ftp server.
        """
        if config['ftp']:
            if config['ftp_hostname'] and config['ftp_username'] and config['ftp_password']: 
                FTP().backup_to_ftp_server(self.destination_path)
            else:
                raise Exception("FTP is enabled but credentials are missing in settings.json.")

def get_backup_password():
    """
    Prompt user to enter a password and return it as bytes.
    """
    parent = QApplication.activeWindow()
    password, ok = QInputDialog.getText(
        parent, "Backup Encryption", "Backup Password:", QLineEdit.EchoMode.Password, ""
    )
    return bytes(password, 'utf-8') if ok and password else None
