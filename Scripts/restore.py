import os
import pyzipper
from pyzipper import BadZipFile
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import QDialog, QListWidget, QPushButton, QVBoxLayout, QInputDialog, QLineEdit, QMessageBox
from .configs import config


class RestoreWorker(QThread):
    """
    Worker thread that handles zip extraction in background.
    """
    finished_signal = pyqtSignal()
    success_signal = pyqtSignal(str, str)
    error_signal = pyqtSignal(str, str)

    def __init__(self, zip_path, extract_to, password=None):
        super().__init__()
        self.zip_path = zip_path
        self.extract_to = extract_to
        self.password = password

    def run(self):
        """
        Extract selected zip file and move zip file content to it's original location.
        """
        try:
            with pyzipper.AESZipFile(self.zip_path) as zipObj:
                if self.password:
                    zipObj.setpassword(self.password)
                zipObj.extractall(self.extract_to)

            self.success_signal.emit("Files Restored Successfully", "SafeArchive has finished the restore.")

        except RuntimeError:
            self.error_signal.emit("Restore Failed", "Wrong password or unable to decrypt.")
        except BadZipFile:
            self.error_signal.emit("Restore Failed", "The archive is corrupted.")
        except Exception as e:
            self.error_signal.emit("Restore Failed", str(e))
        finally:
            self.finished_signal.emit()

class RestoreWindow(QDialog):
    def __init__(self, App, DESTINATION_PATH):
        super().__init__(App)
        self.App = App
        self.DESTINATION_PATH = DESTINATION_PATH
        self.create_restore_window()
        self.create_widgets()
        self.exec()

    def create_restore_window(self):
        self.setWindowTitle("Select backup to restore")
        self.setFixedSize(410, 245)  # disable minimize/maximize buttons

        # hide ? mark
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)

    def create_widgets(self):
        # main frame layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(8, 8, 8, 20)
        main_layout.setSpacing(12)

        # list widget
        self.listbox = QListWidget()
        main_layout.addWidget(self.listbox)

        # populate listbox
        self.listbox.clear()
        if os.path.exists(self.DESTINATION_PATH):
            for zip_file in os.listdir(self.DESTINATION_PATH):
                filename, _, filetype = zip_file.partition('.')
                if filetype == 'zip':
                    self.listbox.addItem(filename)

        # set initial selection to the first item if available
        if self.listbox.count() > 0:
            self.listbox.setCurrentRow(0)

        # restore button
        self.restore_button = QPushButton("Restore backup")
        self.restore_button.setFixedSize(394, 35)

        # connect to main thread
        self.restore_button.clicked.connect(self.prepare_restore)
        main_layout.addWidget(self.restore_button)

    def prepare_restore(self):
        """
        Main thread:
        1. Identify file
        2. Ask user for password (if needed) on main thread
        3. Start thread
        """
        selected_items = self.listbox.selectedItems()
        if not selected_items:
            return

        item = selected_items[0]
        filename = f"{self.DESTINATION_PATH}{item.text()}.zip"

        # ask for password if needed
        password = None
        if config["encryption"]:
            pwd_text, ok = QInputDialog.getText(
                self, "Backup Encryption", "Enter Backup Password:", QLineEdit.EchoMode.Password
            )
            if not ok:
                return
            password = bytes(pwd_text, 'utf-8')

        # setup worker
        self.worker = RestoreWorker(filename, config['destination_path'], password)
        self.worker.finished_signal.connect(self.on_restore_finish)
        self.worker.success_signal.connect(lambda t, m: QMessageBox.information(self, t, m))
        self.worker.error_signal.connect(lambda t, m: QMessageBox.critical(self, t, m ))
        self.worker.start()

    def on_restore_finish(self):
        self.restore_button.setEnabled(True)
        self.worker.deleteLater()  # clean up thread resource
