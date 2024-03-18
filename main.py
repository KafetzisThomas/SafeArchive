#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Project Title: SafeArchive (https://github.com/KafetzisThomas/SafeArchive)
# Author / Project Owner: KafetzisThomas (https://github.com/KafetzisThomas)
# License: GPLv3
# NOTE: By contributing to this project, you agree to the terms of the GPLv3 license, and agree to grant the project owner the right to also provide or sell this software, including your contribution, to anyone under any other license, with no compensation to you.

version = "1.4.0"

# Import built-in modules
import tkinter as tk

# Import module files
from Scripts.file_utils import get_available_drives, get_backup_size, storage_media_free_space, last_backup, update_listbox, remove_item, add_item, create_destination_directory_path
from Scripts.widgets import Combobox, Switch
from Scripts.backup_utils import Backup
from Scripts.restore import RestoreBackup
from Scripts.settings import Settings
from Scripts.about import About
from Scripts.ui import SetupUI
from Scripts.configs import config
config.load() # Load the JSON file into memory

# Import other (third-party) modules
import humanize
from PIL import Image
import customtkinter as ctk

DESTINATION_PATH = config['destination_path'] + 'SafeArchive/'  # Get value from the JSON file
create_destination_directory_path(DESTINATION_PATH)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        ui = SetupUI(DESTINATION_PATH)
        backup = Backup()

        ctk.set_appearance_mode(config['appearance_mode'])
        ctk.set_default_color_theme(config['color_theme'])
        self.title(f"SafeArchive {version}")
        self.resizable(False, False)  # Disable minimize/maximize buttons
        self.geometry("500x500")
        self.iconbitmap("assets/ICO/icon.ico") if config['platform'] == "Windows" else None


        drive_properties_text = "Drive Properties ━━━━━━━━━━━━━━━━" if config['platform'] == "Windows" else "Drive Properties ━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        drive_properties_label = ctk.CTkLabel(
            master=self, text=drive_properties_text, font=('Helvetica', 20))
        drive_properties_label.place(x=15, y=15)

        drive_label = ctk.CTkLabel(master=self, text="Drive", font=('Helvetica', 12))
        drive_label.place(x=15, y=45)

        drive_combobox_var = ctk.StringVar(value=DESTINATION_PATH.replace('SafeArchive/', ''))
        drives_combobox = ctk.CTkComboBox(
            master=self,
            width=470,
            values=get_available_drives(),
            command=lambda choice: Combobox(key='destination_path', choice=choice),
            variable=drive_combobox_var
        )

        drives_combobox.place(x=15, y=70)

        size_of_backup_label = ctk.CTkLabel(
            master=self, text=f"Size of backup: {humanize.naturalsize(get_backup_size(DESTINATION_PATH))}", font=('Helvetica', 12))
        size_of_backup_label.place(x=15, y=100)

        total_drive_space_label = ctk.CTkLabel(
            master=self, text=f"Free space on ({DESTINATION_PATH.replace('SafeArchive/', '')}): {storage_media_free_space()} GB", font=('Helvetica', 12))
        total_drive_space_label.place(x=15, y=120)

        last_backup_label = ctk.CTkLabel(
            master=self, text=f"Last backup: {last_backup(DESTINATION_PATH)}", font=('Helvetica', 12))
        last_backup_label.place(x=15, y=140)

        backup_options_text = "Backup Options ━━━━━━━━━━━━━━━━" if config['platform'] == "Windows" else "Backup Options ━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        backup_options_label = ctk.CTkLabel(
            master=self, text=backup_options_text, font=('Helvetica', 20))
        backup_options_label.place(x=15, y=170)

        keep_my_backups_label = ctk.CTkLabel(
            master=self, text="Keep my backups", font=('Helvetica', 12))
        keep_my_backups_label.place(x=15, y=200)

        backup_expiry_date_combobox_var = ctk.StringVar(
            value=config['backup_expiry_date'])
        backup_expiry_date_options = [
            "1 month", "3 months", "6 months", "9 months", "1 year", "Forever (default)"]

        backup_expiry_date_combobox = ctk.CTkComboBox(
            master=self,
            width=150,
            values=backup_expiry_date_options,
            command=lambda choice: Combobox(key='backup_expiry_date', choice=choice),
            variable=backup_expiry_date_combobox_var
        )

        backup_expiry_date_combobox.place(x=15, y=225)

        cloud_switch_var = ctk.StringVar(
            value="on" if config['backup_to_cloud'] else "off")

        cloud_switch = ctk.CTkSwitch(
            master=self,
            text="Back up to Cloud",
            command=lambda: Switch(key='backup_to_cloud', switch_var=cloud_switch_var),
            variable=cloud_switch_var,
            onvalue="on",
            offvalue="off"
        )

        cloud_switch.place(x=340, y=225)

        backup_these_folders_label = ctk.CTkLabel(
            master=self, text="Backup these folders", font=('Helvetica', 12))
        backup_these_folders_label.place(x=15, y=255)

        frame = ctk.CTkFrame(master=self, corner_radius=10)
        frame.place(x=10, y=280)

        listbox = tk.Listbox(
            master=frame,
            height=4,
            width=52,
            background=ui.get_background_color(),
            foreground=ui.get_foreground_color(),
            activestyle='dotbox',
            font='Helvetica',
            selectbackground=ui.get_listbox_selection_background()
        )

        listbox.pack(padx=7, pady=7)
        update_listbox(listbox=listbox, SOURCE_PATHS=config['source_paths'])

        plus_button = ctk.CTkButton(
            master=self, text="+", width=20, height=10, command=lambda: add_item(listbox=listbox, SOURCE_PATHS=config['source_paths']))
        plus_button.place(x=220, y=250)

        minus_button = ctk.CTkButton(
            master=self, text="-", width=20, height=10, command=lambda: remove_item(listbox=listbox, SOURCE_PATHS=config['source_paths']))
        minus_button.place(x=250, y=250)

        status_text = "Status ━━━━━━━━━━━━━━━━━━━━" if config['platform'] == "Windows" else "Status ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        status_label = ctk.CTkLabel(
            master=self, text=status_text, font=('Helvetica', 20))
        status_label.place(x=15, y=375)

        self.backup_progressbar = ctk.CTkProgressBar(
            master=self, width=475, height=15, corner_radius=0, orientation='horizontal', mode='indeterminate')
        self.backup_progressbar.place(x=15, y=415)

        about_image = ctk.CTkImage(Image.open(ui.get_image1()), size=(25, 25))
        self.about_button = ctk.CTkButton(master=self, text="", fg_color=ui.get_icon_fg_color(), image=about_image,
                                             width=5, height=5, command=lambda: About(self, version))
        self.about_button.place(x=15, y=450)

        settings_image = ctk.CTkImage(Image.open(ui.get_image2()), size=(25, 25))
        self.settings_button = ctk.CTkButton(master=self, text="", fg_color=ui.get_icon_fg_color(), image=settings_image,
                                             width=5, height=5, command=lambda: Settings(self))
        self.settings_button.place(x=50, y=450)
        
        restore_image = ctk.CTkImage(Image.open(ui.get_image3()), size=(25, 25))
        self.restore_button = ctk.CTkButton(master=self, text="", fg_color=ui.get_icon_fg_color(), image=restore_image,
                                            width=5, height=5, command=lambda: RestoreBackup(self, DESTINATION_PATH))
        self.restore_button.place(x=85, y=450)

        self.backup_button = ctk.CTkButton(master=self, text="BACKUP", command=lambda: backup.perform_backup(
            SOURCE_PATHS=config['source_paths'], DESTINATION_PATH=DESTINATION_PATH, App=self))
        self.backup_button.place(x=200, y=450)

        close_button = ctk.CTkButton(
            master=self, text="CLOSE", command=self.destroy)
        close_button.place(x=350, y=450)

        if config['system_tray'] and config['platform'] == "Windows":
            from Scripts.system_tray import hide_window
            self.protocol('WM_DELETE_WINDOW', lambda: hide_window(
                DESTINATION_PATH=DESTINATION_PATH, App=self))


if __name__ == "__main__":
    app = App()
    app.mainloop()
