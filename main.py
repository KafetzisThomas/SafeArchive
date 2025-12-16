#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Project Title: SafeArchive (https://github.com/KafetzisThomas/SafeArchive)
# Author / Project Owner: KafetzisThomas (https://github.com/KafetzisThomas)
# License: GPLv3
# NOTE: By contributing to this project, you agree to the terms of the GPLv3 license, and agree to grant the project owner the right to also provide or sell this software, including your contribution, to anyone under any other license, with no compensation to you.

import sys
import runpy
import humanize
import qtawesome as qta
from Scripts.file_utils import get_backup_size, storage_media_free_space, last_backup, create_destination_directory_path
from Scripts.GUI.file_utils import get_available_drives, update_listbox, remove_item, add_item
from Scripts.GUI.widgets import Combobox
from Scripts.GUI.backup_utils import BackupWorker, get_backup_password
from Scripts.GUI.about import AboutWindow
from Scripts.GUI.restore import RestoreWindow
from Scripts.GUI.settings import SettingsWindow
from Scripts.configs import config
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QComboBox, QFrame, QListWidget,
    QVBoxLayout, QProgressBar, QPushButton, QMessageBox, QWidget, QHBoxLayout,
)

version = "1.5.0"

config.load()  # load the json file into memory
DESTINATION_PATH = config["destination_path"] + "SafeArchive/"

if len(sys.argv) > 1 and sys.argv[1] == "--nogui":
    runpy.run_path("cli.py")
    sys.exit()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"SafeArchive {version}")
        self.setFixedSize(QSize(500, 380))  # disable minimize/maximize buttons

        top_widget = QWidget(self)
        top_widget.setGeometry(10, 10, 480, 150)  # x, y, width, height

        top_layout = QVBoxLayout(top_widget)
        top_layout.setContentsMargins(5, 5, 5, 5)
        top_layout.setSpacing(6)

        # drive combobox
        self.drive_label = QLabel("Drive", self)
        self.drive_label.setFont(QFont("Helvetica", 12))
        top_layout.addWidget(self.drive_label)

        self.drives_combobox = QComboBox(self)
        self.drives_combobox.setFixedWidth(470)
        self.drives_combobox.setFixedHeight(24)
        self.drives_combobox.addItems(get_available_drives())

        # set initial value
        initial_val = DESTINATION_PATH.replace("SafeArchive/", "")
        self.drives_combobox.setCurrentText(initial_val)

        self.drives_combobox.currentTextChanged.connect(self.on_drive_changed)
        top_layout.addWidget(self.drives_combobox)

        # size of backup label
        self.size_of_backup_label = QLabel(self)
        self.size_of_backup_label.setFont(QFont("Helvetica", 10))
        self.size_of_backup_label.setWordWrap(True)
        top_layout.addWidget(self.size_of_backup_label)

        # total drive space label
        self.total_drive_space_label = QLabel(self)
        self.total_drive_space_label.setFont(QFont("Helvetica", 10))
        self.total_drive_space_label.setWordWrap(True)
        top_layout.addWidget(self.total_drive_space_label)

        # last backup label
        self.last_backup_label = QLabel(self)
        self.last_backup_label.setFont(QFont("Helvetica", 10))
        self.last_backup_label.setWordWrap(True)
        top_layout.addWidget(self.last_backup_label)

        self.update_drive_labels(initial_val)

        # backup these folders label
        self.backup_these_folders_label = QLabel("Backup these folders:", self)
        self.backup_these_folders_label.setFont(QFont("Helvetica", 10))
        top_layout.addWidget(self.backup_these_folders_label)

        # frame containing listbox
        self.frame = QFrame(self)
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.frame.setGeometry(10, 160, 480, 130)  # x, y, width, height

        self.listbox = QListWidget()
        vbox = QVBoxLayout(self.frame)
        vbox.setContentsMargins(7, 7, 7, 7)
        vbox.addWidget(self.listbox)

        update_listbox(listbox=self.listbox, SOURCE_PATHS=config['source_paths'])

        # backup progress bar
        self.backup_progressbar = QProgressBar(self)
        self.backup_progressbar.setGeometry(15, 305, 475, 15)  # x, y, width, height
        self.backup_progressbar.setRange(0, 100)  # make it static by default
        self.backup_progressbar.setValue(0)
        self.backup_progressbar.setTextVisible(False)  # hide %

        # bottom bar layout
        bottom_widget = QWidget(self)
        bottom_widget.setGeometry(10, 320, 480, 45)  # x, y, width, height

        bottom_layout = QHBoxLayout(bottom_widget)
        bottom_layout.setContentsMargins(1, 1, 1, 1)
        bottom_layout.setSpacing(1)

        no_border_style = "QPushButton { border: none; padding: 0px; }"

        # about window
        self.about_button = QPushButton()
        self.about_button.setIcon(qta.icon('mdi.information'))
        self.about_button.setIconSize(QSize(22, 22))
        self.about_button.setFixedSize(35, 35)
        self.about_button.setStyleSheet(no_border_style)
        self.about_button.clicked.connect(lambda: AboutWindow(self, version))
        bottom_layout.addWidget(self.about_button)

        # settings window
        self.settings_icon = QPushButton()
        self.settings_icon.setIcon(qta.icon('ph.gear-fill'))
        self.settings_icon.setIconSize(QSize(22, 22))
        self.settings_icon.setFixedSize(35, 35)
        self.settings_icon.setStyleSheet(no_border_style)
        self.settings_icon.clicked.connect(lambda: SettingsWindow(self))
        bottom_layout.addWidget(self.settings_icon)

        # restore window
        self.restore_icon = QPushButton()
        self.restore_icon.setIcon(qta.icon('fa6s.rotate'))
        self.restore_icon.setIconSize(QSize(20, 20))
        self.restore_icon.setFixedSize(35, 35)
        self.restore_icon.setStyleSheet(no_border_style)
        self.restore_icon.clicked.connect(lambda: RestoreWindow(self, self.current_destination_path))
        bottom_layout.addWidget(self.restore_icon)

        # spacer
        bottom_layout.addStretch()

        # plus button
        self.plus_button = QPushButton("+")
        self.plus_button.setFixedSize(35, 35)
        self.plus_button.clicked.connect(lambda: add_item(listbox=self.listbox, SOURCE_PATHS=config["source_paths"]))
        bottom_layout.addWidget(self.plus_button)

        # minus button
        self.minus_button = QPushButton("-")
        self.minus_button.setFixedSize(35, 35)
        self.minus_button.clicked.connect(lambda: remove_item(listbox=self.listbox, SOURCE_PATHS=config["source_paths"]))
        bottom_layout.addWidget(self.minus_button)

        # backup button
        self.backup_button = QPushButton("BACKUP")
        self.backup_button.setFixedSize(100, 35)
        self.backup_button.clicked.connect(self.start_backup_process)
        bottom_layout.addWidget(self.backup_button)

    def on_drive_changed(self, choice):
        """
        Triggered when the user selects a different drive from combobox:
        1. Save new path to config
        2. Update labels
        """
        Combobox(key="destination_path", choice=choice)  # save config
        self.update_drive_labels(choice)  # update ui

    def update_drive_labels(self, drive_path):
        """
        Recalculate stats for the given drive path and update labels.
        Ensure folder exists on the selected drive.
        """
        self.current_destination_path = drive_path + "SafeArchive/"
        create_destination_directory_path(self.current_destination_path)

        # update backup size label
        size = get_backup_size(self.current_destination_path)
        size_str = humanize.naturalsize(size)
        self.size_of_backup_label.setText(f"Size of backup: {size_str}")

        # update free space label
        free = storage_media_free_space(drive_path)
        self.total_drive_space_label.setText(f"Free space on ({drive_path}): {free} GB")

        # update last backup label
        lb_text = last_backup(self.current_destination_path)
        self.last_backup_label.setText(f"Last backup: {lb_text}")

    def start_backup_process(self):
        # check if we need a password
        password = None
        if config['encryption'] and config['compression_method'] in ["ZIP_DEFLATED", "ZIP_STORED"]:
            password = get_backup_password()
            if not password: 
                return

        # ensure we use the active drive selection
        self.worker = BackupWorker(
            source_paths=config["source_paths"], destination_path=self.current_destination_path, password=password
        )
        self.worker.started_signal.connect(self.on_backup_start)
        self.worker.finished_signal.connect(self.on_backup_finish)
        self.worker.success_signal.connect(lambda t, m: QMessageBox.information(self, t, m))
        self.worker.warning_signal.connect(lambda t, m: QMessageBox.warning(self, t, m))
        self.worker.error_signal.connect(lambda t, m: QMessageBox.critical(self, t, m))
        self.worker.start()  # start thread

    def on_backup_start(self):
        self.backup_progressbar.setRange(0, 0)  # make it pulse continuously
        self.backup_button.setEnabled(False)

    def on_backup_finish(self):
        self.backup_progressbar.setRange(0, 100)  # make it static again
        self.backup_progressbar.setValue(0)
        self.backup_button.setEnabled(True)
        self.worker.deleteLater()  # clean up thread resource

        # refresh info in labels after backup finishes
        current_drive = self.drives_combobox.currentText()
        self.update_drive_labels(current_drive)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("assets/logo.png"))  # apply icon to all windows
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
