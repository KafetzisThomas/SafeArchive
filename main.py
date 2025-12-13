#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Project Title: SafeArchive (https://github.com/KafetzisThomas/SafeArchive)
# Author / Project Owner: KafetzisThomas (https://github.com/KafetzisThomas)
# License: GPLv3
# NOTE: By contributing to this project, you agree to the terms of the GPLv3 license, and agree to grant the project owner the right to also provide or sell this software, including your contribution, to anyone under any other license, with no compensation to you.

import sys
import runpy
from Scripts.file_utils import get_backup_size, storage_media_free_space, last_backup, create_destination_directory_path
from Scripts.GUI.file_utils import get_available_drives, update_listbox, remove_item, add_item
from Scripts.GUI.widgets import Combobox
from Scripts.GUI.backup_utils import Backup
from Scripts.GUI.settings import Settings
from Scripts.configs import config
import humanize



import os
import sys

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QFrame, QListWidget, QVBoxLayout, QProgressBar, QPushButton
from PyQt6.QtGui import QIcon, QFont, QPixmap

from Scripts.GUI.about import AboutWindow
from Scripts.GUI.restore import RestoreWindow

version = "1.5.0"

DESTINATION_PATH = config['destination_path'] + 'SafeArchive/'  # get value from the json file
create_destination_directory_path(DESTINATION_PATH)
config.load()  # load the json file into memory

try:
    if sys.argv[1] == "--nogui":
        runpy.run_path('cli.py')
        sys.exit()
except IndexError:
    pass



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        backup = Backup()

        self.setWindowTitle(f"SafeArchive {version}")
        self.setFixedSize(QSize(500, 360))  # disable minimize/maximize buttons

        # drive combobox
        self.drive_label = QLabel("Drive", self)
        self.drive_label.setFont(QFont('Helvetica', 12))
        self.drive_label.move(15, 15)

        self.drives_combobox = QComboBox(self)
        self.drives_combobox.setFixedWidth(475)
        self.drives_combobox.addItems(get_available_drives())

        # set initial value
        initial_val = DESTINATION_PATH.replace('SafeArchive/', '')
        self.drives_combobox.setCurrentText(initial_val)

        self.drives_combobox.currentTextChanged.connect(
            lambda choice: Combobox(key='destination_path', choice=choice)
        )
        self.drives_combobox.move(15, 40)

        # size of backup label
        self.size_of_backup_label = QLabel(f"Size of backup: {humanize.naturalsize(get_backup_size(DESTINATION_PATH))}", self)
        self.size_of_backup_label.setFont(QFont('Helvetica', 12))
        self.size_of_backup_label.move(15, 70)

        # total drive space label
        self.total_drive_space_label = QLabel(f"Free space on ({DESTINATION_PATH.replace('SafeArchive/', '')}): {storage_media_free_space()} GB", self)
        self.total_drive_space_label.setFont(QFont('Helvetica', 12))
        self.total_drive_space_label.move(15, 90)

        # last backup label
        self.last_backup_label = QLabel(f"Last backup: {last_backup(DESTINATION_PATH)}", self)
        self.last_backup_label.setFont(QFont('Helvetica', 12))
        self.last_backup_label.move(15, 110)

        # backup these folders label
        self.backup_these_folders_label = QLabel("Backup these folders:", self)
        self.backup_these_folders_label.setFont(QFont('Helvetica', 12))
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

        # update_listbox(listbox=self.listbox, SOURCE_PATHS=config['source_paths'])

        # backup progress bar
        self.backup_progressbar = QProgressBar(self)
        self.backup_progressbar.setGeometry(15, 275, 475, 15)  # x, y, width, height
        self.backup_progressbar.setRange(0, 0)  # make it pulse continuously
        self.backup_progressbar.setTextVisible(False)  # hide %

        # about window
        about_pixmap = QPixmap(os.path.join("assets", "PNG", "info.png"))
        about_scaled_pixmap = about_pixmap.scaled(25, 25, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio, transformMode=Qt.TransformationMode.SmoothTransformation)
        about_icon = QIcon(about_scaled_pixmap)

        self.about_button = QPushButton(self)
        self.about_button.setIcon(about_icon)
        self.about_button.setIconSize(about_scaled_pixmap.size())
        self.about_button.setText("")  # remove default text
        self.about_button.setFixedSize(35, 35)
        self.about_button.move(15, 310)
        self.about_button.clicked.connect(lambda: AboutWindow(self, version))

        # settings window
        settings_pixmap = QPixmap(os.path.join("assets", "PNG", "gear.png"))
        settings_scaled_pixmap = settings_pixmap.scaled(25, 25, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio, transformMode=Qt.TransformationMode.SmoothTransformation)
        settings_icon = QIcon(settings_scaled_pixmap)

        self.settings_icon = QPushButton(self)
        self.settings_icon.setIcon(settings_icon)
        self.settings_icon.setIconSize(settings_scaled_pixmap.size())
        self.settings_icon.setText("")  # remove default text
        self.settings_icon.setFixedSize(35, 35)
        self.settings_icon.move(50, 310)
        self.settings_icon.clicked.connect(lambda: Settings(self))

        # restore window
        restore_pixmap = QPixmap(os.path.join("assets", "PNG", "restore.png"))
        restore_scaled_pixmap = restore_pixmap.scaled(25, 25, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio, transformMode=Qt.TransformationMode.SmoothTransformation)
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
        self.plus_button.clicked.connect(
            lambda: add_item(listbox=self.listbox, SOURCE_PATHS=config['source_paths'])
        )
        self.plus_button.move(235, 310)

        # minus button
        self.minus_button = QPushButton("-", self)
        self.minus_button.setFixedWidth(65)
        self.minus_button.clicked.connect(
            lambda: remove_item(listbox=self.listbox, SOURCE_PATHS=config['source_paths'])
        )
        self.minus_button.move(280, 310)

        # backup button
        self.backup_button = QPushButton("BACKUP", self)
        self.backup_button.setFixedWidth(100)
        self.backup_button.clicked.connect(
            lambda: backup.perform_backup(
                SOURCE_PATHS=config['source_paths'], 
                DESTINATION_PATH=DESTINATION_PATH, 
                App=self
            )
        )
        self.backup_button.move(350, 310)

    # def show_about_window(self, version):
    #     self.about_dialog = AboutWindow(parent=self, version=version)
    #     self.about_dialog.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # set icon at the app level to apply it to all windows
    app.setWindowIcon(QIcon("assets/PNG/logo.png"))

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


# class App(ctk.CTk):
#     def __init__(self):
#         super().__init__()
#         backup = Backup()
        
#         ctk.set_appearance_mode("dark")
#         ctk.set_default_color_theme("blue")
#         self.title(f"SafeArchive {version}")
#         self.resizable(False, False)  # Disable minimize/maximize buttons
#         self.geometry("500x360")
#         self.iconbitmap("assets/ICO/icon.ico") if config['platform'] == "Windows" else None

#         drive_label = ctk.CTkLabel(master=self, text="Drive", font=('Helvetica', 12))
#         drive_label.place(x=15, y=15)

#         drive_combobox_var = ctk.StringVar(value=DESTINATION_PATH.replace('SafeArchive/', ''))
#         drives_combobox = ctk.CTkComboBox(
#             master=self, width=475, values=get_available_drives(),
#             command=lambda choice: Combobox(key='destination_path', choice=choice), variable=drive_combobox_var
#         )
#         drives_combobox.place(x=15, y=40)

#         size_of_backup_label = ctk.CTkLabel(
#             master=self, text=f"Size of backup: {humanize.naturalsize(get_backup_size(DESTINATION_PATH))}", font=('Helvetica', 12))
#         size_of_backup_label.place(x=15, y=70)

#         total_drive_space_label = ctk.CTkLabel(
#             master=self, text=f"Free space on ({DESTINATION_PATH.replace('SafeArchive/', '')}): {storage_media_free_space()} GB", font=('Helvetica', 12))
#         total_drive_space_label.place(x=15, y=90)

#         last_backup_label = ctk.CTkLabel(
#             master=self, text=f"Last backup: {last_backup(DESTINATION_PATH)}", font=('Helvetica', 12))
#         last_backup_label.place(x=15, y=110)

#         backup_these_folders_label = ctk.CTkLabel(
#             master=self, text="Backup these folders:", font=('Helvetica', 12))
#         backup_these_folders_label.place(x=15, y=130)

#         frame = ctk.CTkFrame(master=self, corner_radius=10)
#         frame.place(x=10, y=160)

#         listbox = tk.Listbox(
#             master=frame, height=4, width=53,
#             background="#343638", foreground="white", activestyle='dotbox',
#             font='Helvetica', selectbackground="#1f6aa5",
#         )

#         listbox.pack(padx=7, pady=7)
#         update_listbox(listbox=listbox, SOURCE_PATHS=config['source_paths'])

#         self.backup_progressbar = ctk.CTkProgressBar(
#             master=self, width=475, height=15, corner_radius=0, orientation='horizontal', mode='indeterminate')
#         self.backup_progressbar.place(x=15, y=275)

#         about_image = ctk.CTkImage(Image.open("assets/PNG/info.png"), size=(25, 25))
#         self.about_button = ctk.CTkButton(master=self, text="", fg_color="#242424", image=about_image,
#                                              width=5, height=5, command=lambda: About(self, version))
#         self.about_button.place(x=15, y=310)

#         settings_image = ctk.CTkImage(Image.open("assets/PNG/gear.png"), size=(25, 25))
#         self.settings_button = ctk.CTkButton(master=self, text="", fg_color="#242424", image=settings_image,
#                                              width=5, height=5, command=lambda: Settings(self))
#         self.settings_button.place(x=50, y=310)
        
#         restore_image = ctk.CTkImage(Image.open("assets/PNG/restore.png"), size=(25, 25))
#         self.restore_button = ctk.CTkButton(master=self, text="", fg_color="#242424", image=restore_image,
#                                             width=5, height=5, command=lambda: RestoreBackup(self, DESTINATION_PATH))
#         self.restore_button.place(x=85, y=310)

#         plus_button = ctk.CTkButton(
#             master=self, text="ADD", width=20, command=lambda: add_item(listbox=listbox, SOURCE_PATHS=config['source_paths']))
#         plus_button.place(x=235, y=310)

#         minus_button = ctk.CTkButton(
#             master=self, text="REMOVE", width=20, command=lambda: remove_item(listbox=listbox, SOURCE_PATHS=config['source_paths']))
#         minus_button.place(x=280, y=310)

#         self.backup_button = ctk.CTkButton(master=self, text="BACKUP", command=lambda: backup.perform_backup(
#             SOURCE_PATHS=config['source_paths'], DESTINATION_PATH=DESTINATION_PATH, App=self))
#         self.backup_button.place(x=350, y=310)


# if __name__ == "__main__":
#     app = App()
#     app.mainloop()
