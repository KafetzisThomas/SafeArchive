from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QDialog, QFrame, QLabel, QComboBox, QCheckBox
from .widgets import Combobox, Switch
from ..configs import config


class SettingsWindow(QDialog):
    def __init__(self,App):
        super().__init__(App)
        self.App = App
        self.create_settings_window()
        self.create_widgets()
        self.exec()

    def create_settings_window(self):
        self.setWindowTitle("Settings")
        self.setFixedSize(630, 190)  # disable minimize/maximize buttons

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
        combo.currentTextChanged.connect(lambda choice: Combobox(key='storage_provider', choice=choice))

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
        
        combo.currentTextChanged.connect(lambda choice: Combobox(key='compression_method', choice=choice))

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
        
        combo.currentTextChanged.connect(lambda choice: Combobox(key='compression_level', choice=choice))

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
        
        combo.currentTextChanged.connect(lambda choice: Combobox(key='backup_expiry_date', choice=choice))

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
