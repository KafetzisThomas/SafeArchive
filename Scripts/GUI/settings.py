from .widgets import Combobox, Switch
from ..configs import config

from PyQt6.QtWidgets import QDialog, QFrame, QLabel, QComboBox, QCheckBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class SettingsWindow(QDialog):
    def __init__(self,App):
        super().__init__(App)
        self.App = App
        self.create_settings_window()
        self.create_widgets()
        self.exec()

    def create_settings_window(self):
        self.setWindowTitle("Settings")
        self.setFixedSize(630, 190)

        # hide ? mark
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)

    def create_widgets(self):
        # frame
        self.frame = QFrame(self)
        self.frame.move(8, 8)
        self.frame.setFixedSize(615, 174)
        
        # rounded corners and background
        self.frame.setStyleSheet("""
            QFrame { 
                background-color: #2b2b2b; 
                border-radius: 10px; 
            }
        """)

        # display storage provider label
        lbl = QLabel("Storage Provider:", self.frame)
        lbl.setFont(QFont('Helvetica', 15))
        lbl.setStyleSheet("color: white; background: transparent;")
        lbl.move(10, 90)

        # storage provider combobox
        combo = QComboBox(self.frame)
        combo.addItems(["None", "Google Drive", "Dropbox", "FTP"])
        combo.setCurrentText(config['storage_provider'])
        combo.setFixedWidth(130)
        combo.move(160, 90)
        
        # signal connection
        combo.currentTextChanged.connect(
            lambda choice: Combobox(key='storage_provider', choice=choice)
        )

        # compression combobox
        lbl = QLabel("Compression Method:", self.frame)
        lbl.setFont(QFont('Helvetica', 15))
        lbl.setStyleSheet("color: white; background: transparent;")
        lbl.move(295, 20)

        combo = QComboBox(self.frame)
        combo.addItems(["ZIP_DEFLATED", "ZIP_STORED", "ZIP_LZMA", "ZIP_BZIP2"])
        combo.setCurrentText(config['compression_method'])
        combo.setFixedWidth(130)
        combo.move(465, 20)
        
        combo.currentTextChanged.connect(
            lambda choice: Combobox(key='compression_method', choice=choice)
        )

        # compression level combobox
        lbl = QLabel("Compression Level:", self.frame)
        lbl.setFont(QFont('Helvetica', 15))
        lbl.setStyleSheet("color: white; background: transparent;")
        lbl.move(295, 55)

        combo = QComboBox(self.frame)
        combo.addItems([str(i) for i in range(1, 10)])  # create a list of strings [1, 9]
        combo.setCurrentText(str(config['compression_level']))
        combo.setFixedWidth(130)
        combo.move(465, 55)
        
        combo.currentTextChanged.connect(
            lambda choice: Combobox(key='compression_level', choice=choice)
        )

        # keep my backups combobox
        lbl = QLabel("Keep my backups:", self.frame)
        lbl.setFont(QFont('Helvetica', 15))
        lbl.setStyleSheet("color: white; background: transparent;")
        lbl.move(295, 90)

        combo = QComboBox(self.frame)
        combo.addItems(["1 month", "3 months", "6 months", "9 months", "1 year", "Forever"])
        combo.setCurrentText(config['backup_expiry_date'])
        combo.setFixedWidth(130)
        combo.move(465, 90)
        
        combo.currentTextChanged.connect(
            lambda choice: Combobox(key='backup_expiry_date', choice=choice)
        )

        # encryption switch
        self.chk_encryption = QCheckBox("Encrypt Backups", self.frame)
        self.chk_encryption.setFont(QFont('Helvetica', 15))
        self.chk_encryption.setChecked(config['encryption'])
        self.chk_encryption.move(295, 130)
        
        # dark mode style
        self.chk_encryption.setStyleSheet("""
            QCheckBox {
                color: white;
                background: transparent;
                spacing: 10px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 1px solid #555;
                border-radius: 4px;
                background: #343638;
            }
            QCheckBox::indicator:checked {
                background-color: #1f6aa5;
                border: 1px solid #1f6aa5;
            }
        """)

        # signal connection
        self.chk_encryption.toggled.connect(
            lambda checked: Switch(key='encryption', value=checked)
        )

        combo.setStyleSheet("""
            QComboBox {
                background-color: #343638;
                color: white;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 5px;
            }
            QComboBox::drop-down {
                border: 0px;
            }
            QComboBox QAbstractItemView {
                background-color: #343638;
                color: white;
                selection-background-color: #1f6aa5;
            }
        """)




# class Settings:
#     """
#     Create a toplevel widget containing a frame with settings.
#     """
#     def __init__(self, App):
#         self.App = App
#         self.create_settings_window()
#         self.create_frame()
#         self.display_storage_provider_label()
#         self.create_storage_provider_combobox()
#         self.display_compression_method_label()
#         self.create_compression_method_combobox()
#         self.display_compression_level_label()
#         self.create_compression_level_combobox()
#         self.display_keep_my_backups_label()
#         self.create_keep_my_backups_combobox()
#         self.create_encryption_switch()

#     def create_settings_window(self):
#         self.settings_window = tk.Toplevel(self.App)
#         self.settings_window.title("Settings")
#         self.settings_window.geometry("775x235")
#         self.settings_window.iconbitmap("assets/ICO/gear.ico") if config['platform'] == "Windows" else None
#         self.settings_window.resizable(False, False)  # Disable minimize/maximize buttons
#         self.settings_window.configure(background="#242424")

#     def create_frame(self):
#         self.frame = ctk.CTkFrame(master=self.settings_window, corner_radius=10, height=170, width=605)
#         self.frame.place(x=8, y=8)

#     def display_storage_provider_label(self):
#         storage_provider_label = ctk.CTkLabel(master=self.frame, text="Storage Provider:", font=('Helvetica', 15))
#         storage_provider_label.place(x=10, y=90)

#     def create_storage_provider_combobox(self):
#         storage_provider_combobox_var = ctk.StringVar(value=config['storage_provider'])
#         storage_provider_options = ["None", "Google Drive", "Dropbox", "FTP"]
#         storage_provider_combobox = ctk.CTkComboBox(
#             master=self.frame,
#             width=112,
#             values=storage_provider_options,
#             command=lambda choice: Combobox(key='storage_provider', choice=choice),
#             variable=storage_provider_combobox_var
#         )
#         storage_provider_combobox.place(x=160, y=90)

#     def display_compression_method_label(self):
#         compression_method_label = ctk.CTkLabel(master=self.frame, text="Compression Method:", font=('Helvetica', 15))
#         compression_method_label.place(x=295, y=20)

#     def create_compression_method_combobox(self):
#         compression_method_combobox_var = ctk.StringVar(value=config['compression_method'])
#         compression_method_options = ["ZIP_DEFLATED", "ZIP_STORED", "ZIP_LZMA", "ZIP_BZIP2"]
#         compression_method_combobox = ctk.CTkComboBox(
#             master=self.frame,
#             width=130,
#             values=compression_method_options,
#             command=lambda choice: Combobox(key='compression_method', choice=choice),
#             variable=compression_method_combobox_var
#         )
#         compression_method_combobox.place(x=465, y=20)

#     def display_compression_level_label(self):
#         compression_level_label = ctk.CTkLabel(master=self.frame, text="Compression Level:", font=('Helvetica', 15))
#         compression_level_label.place(x=295, y=55)

#     def create_compression_level_combobox(self):
#         compression_level_combobox_var = ctk.StringVar(value=config['compression_level'])
#         integers = list(range(1, 10))  # Create a list of integers
#         compression_level_options = [str(i) for i in integers]
#         compression_level_combobox = ctk.CTkComboBox(
#             master=self.frame,
#             width=130,
#             values=compression_level_options,
#             command=lambda choice: Combobox(key='compression_level', choice=choice),
#             variable=compression_level_combobox_var
#         )
#         compression_level_combobox.place(x=465, y=55)

#     def display_keep_my_backups_label(self):
#         keep_my_backups_label = ctk.CTkLabel(master=self.frame, text="Keep my backups:", font=('Helvetica', 15))
#         keep_my_backups_label.place(x=295, y=90)

#     def create_keep_my_backups_combobox(self):
#         backup_expiry_date_combobox_var = ctk.StringVar(value=config['backup_expiry_date'])
#         backup_expiry_date_options = ["1 month", "3 months", "6 months", "9 months", "1 year", "Forever"]
#         backup_expiry_date_combobox = ctk.CTkComboBox(
#             master=self.frame,
#             width=130,
#             values=backup_expiry_date_options,
#             command=lambda choice: Combobox(key='backup_expiry_date', choice=choice),
#             variable=backup_expiry_date_combobox_var
#         )
#         backup_expiry_date_combobox.place(x=465, y=90)

#     def create_encryption_switch(self):
#         encryption_switch_var = ctk.StringVar(value="on" if config['encryption'] else "off")
#         encryption_switch = ctk.CTkSwitch(
#             master=self.frame,
#             text="Encrypt Backups",
#             font=('Helvetica', 15),
#             command=lambda: Switch(key='encryption', switch_var=encryption_switch_var),
#             variable=encryption_switch_var,
#             onvalue="on",
#             offvalue="off"
#         )
#         encryption_switch.place(x=295, y=130)
