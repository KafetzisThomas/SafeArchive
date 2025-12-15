from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QDialog, QFrame, QLabel, QComboBox, QCheckBox, QVBoxLayout
from .widgets import Combobox, Switch
from ..configs import config


class SettingsWindow(QDialog):
    def __init__(self, App):
        super().__init__(App)
        self.App = App
        self.create_settings_window()
        self.create_widgets()
        self.exec()

    def create_settings_window(self):
        self.setWindowTitle("Settings")
        self.setFixedSize(280, 320)  # disable minimize/maximize buttons

        # hide ? mark
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)

    def create_widgets(self):
        # main frame layout
        self.frame = QFrame(self)
        self.frame.setGeometry(0, 0, 280, 320)  # x, y, width, height
        main_layout = QVBoxLayout(self.frame)
        main_layout.setContentsMargins(25, 20, 25, 20)
        main_layout.setSpacing(10)

        # compression label + combobox
        compression_label = QLabel("Compression Method:")
        compression_label.setFont(QFont('Helvetica', 10))
        main_layout.addWidget(compression_label)

        compression_combobox = QComboBox()
        compression_combobox.addItems(["ZIP_DEFLATED", "ZIP_STORED", "ZIP_LZMA", "ZIP_BZIP2"])
        compression_combobox.setCurrentText(config['compression_method'])
        compression_combobox.setFixedSize(230, 30)
        compression_combobox.currentTextChanged.connect(lambda choice: Combobox(key='compression_method', choice=choice))
        main_layout.addWidget(compression_combobox)

        # compression level label + combobox
        compression_level_label = QLabel("Compression Level:")
        compression_level_label.setFont(QFont('Helvetica', 10))
        main_layout.addWidget(compression_level_label)

        compression_level_combobox = QComboBox()
        compression_level_combobox.addItems([str(i) for i in range(1, 10)])  # create a list of strings [1, 9]
        compression_level_combobox.setCurrentText(str(config['compression_level']))
        compression_level_combobox.setFixedSize(230, 30)
        compression_level_combobox.currentTextChanged.connect(lambda choice: Combobox(key='compression_level', choice=choice))
        main_layout.addWidget(compression_level_combobox)

        # keep my backups label + combobox
        keep_my_backups_label = QLabel("Keep my backups:")
        keep_my_backups_label.setFont(QFont('Helvetica', 10))
        main_layout.addWidget(keep_my_backups_label)

        keep_my_backups_combobox = QComboBox()
        keep_my_backups_combobox.addItems(["1 month", "3 months", "6 months", "9 months", "1 year", "Forever"])
        keep_my_backups_combobox.setCurrentText(config['backup_expiry_date'])
        keep_my_backups_combobox.setFixedSize(230, 30)
        keep_my_backups_combobox.currentTextChanged.connect(lambda choice: Combobox(key='backup_expiry_date', choice=choice))
        main_layout.addWidget(keep_my_backups_combobox)

        main_layout.addSpacing(10)

        # encryption switch
        encryption_switch = QCheckBox("Encrypt Backups")
        encryption_switch.setFont(QFont('Helvetica', 10))
        encryption_switch.setChecked(config['encryption'])
        encryption_switch.toggled.connect(lambda checked: Switch(key='encryption', value=checked))
        main_layout.addWidget(encryption_switch)

        # ftp switch
        ftp_switch = QCheckBox("Enable FTP")
        ftp_switch.setFont(QFont('Helvetica', 10))
        ftp_switch.setChecked(config['ftp'])
        ftp_switch.toggled.connect(lambda checked: Switch(key='ftp', value=checked))
        main_layout.addWidget(ftp_switch)

        main_layout.addStretch()
