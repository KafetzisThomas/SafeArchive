#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Project Title: SafeArchive (https://github.com/KafetzisThomas/SafeArchive)
# Author / Project Owner: KafetzisThomas (https://github.com/KafetzisThomas)
# License: GPLv3
# NOTE: By contributing to this project, you agree to the terms of the GPLv3 license, and agree to grant the project owner the right to also provide or sell this software, including your contribution, to anyone under any other license, with no compensation to you.

import os
import sys
import runpy
import humanize
from Scripts.file_utils import get_backup_size, storage_media_free_space, last_backup, create_destination_directory_path
from Scripts.GUI.file_utils import get_available_drives, update_listbox, remove_item, add_item
from Scripts.GUI.widgets import Combobox
from Scripts.GUI.backup_utils import BackupWorker, get_backup_password
from Scripts.GUI.about import AboutWindow
from Scripts.GUI.restore import RestoreWindow
from Scripts.GUI.settings import SettingsWindow
from Scripts.system_notifications import notify_user
from Scripts.configs import config
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QFont, QPixmap
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QComboBox, QFrame,
    QListWidget, QVBoxLayout, QProgressBar, QPushButton, QMessageBox
)

version = "1.5.0"

DESTINATION_PATH = config["destination_path"] + "SafeArchive/"  # get value from the json file
create_destination_directory_path(DESTINATION_PATH)
config.load()  # load the json file into memory

try:
    if sys.argv[1] == "--nogui":
        runpy.run_path("cli.py")
        sys.exit()
except IndexError:
    pass


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"SafeArchive {version}")
        self.setFixedSize(QSize(500, 360))  # disable minimize/maximize buttons

        # drive combobox
        self.drive_label = QLabel("Drive", self)
        self.drive_label.setFont(QFont("Helvetica", 12))
        self.drive_label.move(15, 15)

        self.drives_combobox = QComboBox(self)
        self.drives_combobox.setFixedWidth(475)
        self.drives_combobox.addItems(get_available_drives())

        # set initial value
        initial_val = DESTINATION_PATH.replace("SafeArchive/", "")
        self.drives_combobox.setCurrentText(initial_val)

        self.drives_combobox.currentTextChanged.connect(
            lambda choice: Combobox(key="destination_path", choice=choice)
        )
        self.drives_combobox.move(15, 40)

        # size of backup label
        self.size_of_backup_label = QLabel(
            f"Size of backup: {humanize.naturalsize(get_backup_size(DESTINATION_PATH))}", self
        )
        self.size_of_backup_label.setFont(QFont("Helvetica", 12))
        self.size_of_backup_label.move(15, 70)

        # total drive space label
        self.total_drive_space_label = QLabel(
            f"Free space on ({DESTINATION_PATH.replace('SafeArchive/', '')}): {storage_media_free_space()} GB", self
        )
        self.total_drive_space_label.setFont(QFont("Helvetica", 12))
        self.total_drive_space_label.move(15, 90)

        # last backup label
        self.last_backup_label = QLabel(f"Last backup: {last_backup(DESTINATION_PATH)}", self)
        self.last_backup_label.setFont(QFont("Helvetica", 12))
        self.last_backup_label.move(15, 110)

        # backup these folders label
        self.backup_these_folders_label = QLabel("Backup these folders:", self)
        self.backup_these_folders_label.setFont(QFont("Helvetica", 12))
        self.backup_these_folders_label.move(15, 130)

        # frame containing listbox
        self.frame = QFrame(self)

        # default visual border
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.frame.setGeometry(10, 160, 500, 100)  # x, y, width, height

        self.listbox = QListWidget()
        vbox = QVBoxLayout(self.frame)
        vbox.setContentsMargins(7, 7, 7, 7)
        vbox.addWidget(self.listbox)

        update_listbox(listbox=self.listbox, SOURCE_PATHS=config['source_paths'])

        # backup progress bar
        self.backup_progressbar = QProgressBar(self)
        self.backup_progressbar.setGeometry(15, 275, 475, 15)  # x, y, width, height
        self.backup_progressbar.setRange(0, 0)  # make it pulse continuously
        self.backup_progressbar.setTextVisible(False)  # hide %

        # about window
        about_pixmap = QPixmap(os.path.join("assets", "info.png"))
        about_scaled_pixmap = about_pixmap.scaled(
            25, 25, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio,
            transformMode=Qt.TransformationMode.SmoothTransformation,
        )
        about_icon = QIcon(about_scaled_pixmap)

        self.about_button = QPushButton(self)
        self.about_button.setIcon(about_icon)
        self.about_button.setIconSize(about_scaled_pixmap.size())
        self.about_button.setText("")  # remove default text
        self.about_button.setFixedSize(35, 35)
        self.about_button.move(15, 310)
        self.about_button.clicked.connect(lambda: AboutWindow(self, version))

        # settings window
        settings_pixmap = QPixmap(os.path.join("assets", "gear.png"))
        settings_scaled_pixmap = settings_pixmap.scaled(
            25, 25, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio,
            transformMode=Qt.TransformationMode.SmoothTransformation,
        )
        settings_icon = QIcon(settings_scaled_pixmap)

        self.settings_icon = QPushButton(self)
        self.settings_icon.setIcon(settings_icon)
        self.settings_icon.setIconSize(settings_scaled_pixmap.size())
        self.settings_icon.setText("")  # remove default text
        self.settings_icon.setFixedSize(35, 35)
        self.settings_icon.move(50, 310)
        self.settings_icon.clicked.connect(lambda: SettingsWindow(self))

        # restore window
        restore_pixmap = QPixmap(os.path.join("assets", "restore.png"))
        restore_scaled_pixmap = restore_pixmap.scaled(
            25, 25, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio,
            transformMode=Qt.TransformationMode.SmoothTransformation,
        )
        restore_icon = QIcon(restore_scaled_pixmap)

        self.restore_icon = QPushButton(self)
        self.restore_icon.setIcon(restore_icon)
        self.restore_icon.setIconSize(restore_scaled_pixmap.size())
        self.restore_icon.setText("")  # remove default text
        self.restore_icon.setFixedSize(35, 35)
        self.restore_icon.move(85, 310)
        self.restore_icon.clicked.connect(lambda: RestoreWindow(self, DESTINATION_PATH))

        # plus button
        self.plus_button = QPushButton("+", self)
        self.plus_button.setFixedWidth(40)
        self.plus_button.clicked.connect(lambda: add_item(listbox=self.listbox, SOURCE_PATHS=config["source_paths"]))
        self.plus_button.move(235, 310)

        # minus button
        self.minus_button = QPushButton("-", self)
        self.minus_button.setFixedWidth(65)
        self.minus_button.clicked.connect(
            lambda: remove_item(listbox=self.listbox, SOURCE_PATHS=config["source_paths"])
        )
        self.minus_button.move(280, 310)

        # backup button
        self.backup_button = QPushButton("BACKUP", self)
        self.backup_button.setFixedWidth(100)
        self.backup_button.clicked.connect(self.start_backup_process)
        self.backup_button.move(350, 310)

    def start_backup_process(self):
        """
        1. Get password (if needed) on main thread
        2. Create thread
        3. Connect signals
        4. Start thread
        """
        password = None

        # check if we need a password
        if config['encryption'] and config['compression_method'] in ["ZIP_DEFLATED", "ZIP_STORED"]:
            password = get_backup_password()
            if not password: 
                return

        # initialize worker thread
        self.worker = BackupWorker(source_paths=config["source_paths"], destination_path=DESTINATION_PATH, password=password)

        # connect signals
        self.worker.started_signal.connect(self.on_backup_start)
        self.worker.finished_signal.connect(self.on_backup_finish)
        self.worker.success_signal.connect(lambda t, m: QMessageBox.information(self, t, m))
        self.worker.start()  # start thread

    def on_backup_start(self):
        self.backup_progressbar.show()
        self.backup_button.setEnabled(False)

    def on_backup_finish(self):
        self.backup_progressbar.hide()
        self.backup_button.setEnabled(True)
        self.worker.deleteLater()  # clean up thread resource

    def on_backup_notify(self, title, message):
        notify_user(title=title, message=message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("assets/logo.png"))  # apply icon to all windows
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
