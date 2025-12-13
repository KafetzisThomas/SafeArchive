import os
import pyzipper
import threading
from ..system_notifications import notify_user
from ..configs import config

from PyQt6.QtWidgets import QDialog, QFrame, QListWidget, QPushButton, QVBoxLayout, QInputDialog, QLineEdit
from PyQt6.QtCore import Qt

class RestoreWindow(QDialog):
    def __init__(self, App, DESTINATION_PATH):
        super().__init__(App)
        self.App = App
        self.DESTINATION_PATH = DESTINATION_PATH
        self.create_restore_window()
        self.create_listbox()
        self.populate_listbox()
        self.create_restore_button()
        self.exec()

    def create_restore_window(self):
        self.setWindowTitle("Select backup to restore")
        self.setFixedSize(410, 245)

        # hide ? mark
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)

    def create_listbox(self):
        # frame
        self.frame = QFrame(self)
        self.frame.move(8, 8)
        self.frame.setFixedSize(394, 150) 

        # list widget
        self.listbox = QListWidget(self.frame)

        # apply styles
        self.listbox.setStyleSheet("""
            QListWidget {
                background-color: #343638;
                color: white;
                font-family: Helvetica;
                font-size: 13pt;
                border: 1px solid #1f6aa5;
            }
            QListWidget::item {
                padding: 5px;
            }
            QListWidget::item:selected {
                background-color: #1f6aa5;
                color: white;
            }
        """)
        
        # layout inside frame
        layout = QVBoxLayout(self.frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.listbox)

    def populate_listbox(self):
        """
        Populate listbox with the zip file names from the DESTINATION_PATH directory.
        """
        self.listbox.clear()
        if os.path.exists(self.DESTINATION_PATH):
            for zip_file in os.listdir(self.DESTINATION_PATH):
                filename, _, filetype = zip_file.partition('.')
                if filetype == 'zip':
                    self.listbox.addItem(filename)

        # set initial selection to the first item if available
        if self.listbox.count() > 0: self.listbox.setCurrentRow(0)

    def create_restore_button(self):
        self.restore_button = QPushButton("Restore backup", self)
        self.restore_button.clicked.connect(self.run_restore_thread)
        self.restore_button.setFixedWidth(220)
        self.restore_button.move(95, 163)

        # style the button
        self.restore_button.setStyleSheet("""
            QPushButton {
                background-color: #1f6aa5;
                color: white;
                font-weight: bold;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #144870;
            }
            QPushButton:disabled {
                background-color: #555555;
                color: #aaaaaa;
            }
        """)

    def run_restore_thread(self):
        """
        Create and start a thread for the restore process.
        """
        threading.Thread(target=self.extract_item, daemon=True).start()

    def extract_item(self):
        """
        Extract selected zip file and move zip file content to its original location.
        """
        self.disable_restore_button()
        for item in self.listbox.selectedItems():
            file_name = f"{self.DESTINATION_PATH}{item.text()}.zip"
            try:
                with pyzipper.AESZipFile(file=file_name) as zipObj:
                    if config['encryption'] and (config['compression_method'] == "ZIP_DEFLATED" or config['compression_method'] == "ZIP_STORED"):
                         # TODO: ask for password before starting thread
                        zipObj.setpassword(self.get_backup_password())
                    
                    zipObj.extractall(config['destination_path'])

                    notify_user(
                        title='SafeArchive: Files Restored Successfully',
                        message='SafeArchive has finished the restore.',
                        icon='restore.ico'
                    )

            except (RuntimeError, TypeError):
                pass

        self.enable_restore_button()

    def get_backup_password(self):
        """
        Prompt the user to enter password and return it as bytes.
        """
        # TODO: call this inside main thread instead
        text, ok = QInputDialog.getText(self, "Backup Encryption", "Backup Password:", QLineEdit.EchoMode.Password)
        return bytes(text, 'utf-8') if ok else b''

    def disable_restore_button(self):
        from PyQt6.QtCore import QMetaObject, Q_ARG
        QMetaObject.invokeMethod(self.restore_button, "setEnabled", Qt.ConnectionType.QueuedConnection, Q_ARG(bool, False))

    def enable_restore_button(self):
        from PyQt6.QtCore import QMetaObject, Q_ARG
        QMetaObject.invokeMethod(self.restore_button, "setEnabled", Qt.ConnectionType.QueuedConnection, Q_ARG(bool, True))



# class RestoreBackup:
#     """
#     Provide functionality to restore backups from a zip file.
#     """
#     def __init__(self, App, DESTINATION_PATH):
#         self.App = App
#         self.DESTINATION_PATH = DESTINATION_PATH
#         self.create_restore_window()
#         self.create_listbox()
#         self.populate_listbox()
#         self.create_restore_button()

#     def create_restore_window(self):
#         self.restore_window = tk.Toplevel(self.App)
#         self.restore_window.title("Select backup to restore")
#         self.restore_window.geometry("410x245")
#         self.restore_window.iconbitmap("assets/ICO/restore.ico") if config['platform'] == "Windows" else None
#         self.restore_window.resizable(False, False)  # Disable minimize/maximize buttons
#         self.restore_window.configure(background="#343638")

#     def create_listbox(self):
#         frame = ctk.CTkFrame(master=self.restore_window)
#         frame.place(x=8, y=8)
#         height, width = (9, 43) if config['platform'] == "Windows" else (8, 35)
#         self.listbox = tk.Listbox(
#             master=frame,
#             height=height,
#             width=width,
#             background="#343638",
#             foreground="white",
#             activestyle='dotbox',
#             font='Helvetica, 13',
#             justify="center",
#             selectbackground="#1f6aa5",
#         )
#         self.listbox.pack()

#     def populate_listbox(self):
#         """
#         Populate listbox with the zip file names from the DESTINATION_PATH directory.
#         """
#         for index, zip_file in enumerate(os.listdir(self.DESTINATION_PATH)):
#             filename, _, filetype = zip_file.partition('.')
#             if filetype == 'zip':
#                 self.listbox.insert(index, filename)
#         self.listbox.selection_set(0)  # set the initial selection to the first item

#     def create_restore_button(self):
#         self.App.restore_button = ctk.CTkButton(
#             master=self.restore_window, text="Restore backup", command=self.run_restore_thread)
#         self.App.restore_button.place(x=95, y=163)

#     def run_restore_thread(self):
#         """
#         Create and start a thread for the restore process.
#         """
#         threading.Thread(target=self.extract_item, daemon=True).start()

#     def extract_item(self):
#         """
#         Extract selected zip file and move zip file content to it's original location.
#         """
#         self.disable_restore_button()
#         for item in self.listbox.curselection():
#             file_name = f"{self.DESTINATION_PATH}{self.listbox.get(item)}.zip"
#             with pyzipper.AESZipFile(file=file_name) as zipObj:
#                 try:
#                     if config['encryption'] and (config['compression_method'] == "ZIP_DEFLATED" or config['compression_method'] == "ZIP_STORED"):
#                         zipObj.setpassword(self.get_backup_password())
#                     zipObj.extractall(config['destination_path'])

#                     notify_user(
#                         title='SafeArchive: Files Restored Sucessfully',
#                         message='SafeArchive has finished the restore.',
#                         icon='restore.ico'
#                     )

#                 except (RuntimeError, TypeError):
#                     pass
#         self.enable_restore_button()

#     def get_backup_password(self):
#         """
#         Prompt the user to enter password and return it as bytes.
#         """
#         password = ctk.CTkInputDialog(text="Backup Password:", title="Backup Encryption")
#         return bytes(password.get_input(), 'utf-8')

#     def disable_restore_button(self):
#         self.App.restore_button.configure(state="disabled")

#     def enable_restore_button(self):
#         self.App.restore_button.configure(state="normal")
