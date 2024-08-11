#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import pyzipper
import threading
import tkinter as tk
from ..system_notifications import notify_user
from ..configs import config
import customtkinter as ctk


class RestoreBackup:
    """
    Provide functionality to restore backups from a zip file.
    """

    def __init__(self, App, DESTINATION_PATH):
        self.App = App
        self.DESTINATION_PATH = DESTINATION_PATH
        self.create_restore_window()
        self.create_listbox()
        self.populate_listbox()
        self.create_restore_button()


    def create_restore_window(self):
        self.restore_window = tk.Toplevel(self.App)
        self.restore_window.title("Select backup to restore")
        self.restore_window.geometry("410x245")
        self.restore_window.iconbitmap("assets/ICO/restore.ico") if config['platform'] == "Windows" else None
        self.restore_window.resizable(False, False)  # Disable minimize/maximize buttons
        self.restore_window.configure(background=self.get_listbox_background())


    def create_listbox(self):
        frame = ctk.CTkFrame(master=self.restore_window)
        frame.place(x=8, y=8)
        height, width = (9, 43) if config['platform'] == "Windows" else (8, 35)
        self.listbox = tk.Listbox(
            master=frame,
            height=height,
            width=width,
            background=self.get_listbox_background(),
            foreground=self.get_listbox_foreground(),
            activestyle='dotbox',
            font='Helvetica, 13',
            justify="center",
            selectbackground=self.get_listbox_selection_background()
        )
        self.listbox.pack()


    def get_listbox_background(self):
        return "#343638" if config['appearance_mode'] == "dark" else "#ebebeb"


    def get_listbox_foreground(self):
        return "white" if config['appearance_mode'] == "dark" else "black"


    def get_listbox_selection_background(self):
        if config['color_theme'] == "blue":
            return "#1f6aa5"
        else:
            return "#2fa572"


    def populate_listbox(self):
        """
        Populate listbox with the zip file names from the DESTINATION_PATH directory.
        """
        for index, zip_file in enumerate(os.listdir(self.DESTINATION_PATH)):
            filename, _, filetype = zip_file.partition('.')
            if filetype == 'zip':
                self.listbox.insert(index, filename)
        self.listbox.selection_set(0)  # Set the initial selection to the first item


    def create_restore_button(self):
        self.App.restore_button = ctk.CTkButton(
            master=self.restore_window, text="Restore backup", command=self.run_restore_thread)
        self.App.restore_button.place(x=95, y=163)


    def run_restore_thread(self):
        """
        Create and start a thread for the restore process.
        """
        threading.Thread(target=self.extract_item, daemon=True).start()


    def extract_item(self):
        """
        Extract selected zip file & move zip file content to it's original location.
        """
        self.disable_restore_button()
        for item in self.listbox.curselection():
            file_name = f"{self.DESTINATION_PATH}{self.listbox.get(item)}.zip"
            with pyzipper.AESZipFile(file=file_name) as zipObj:
                try:
                    if config['encryption'] and (config['compression_method'] == "ZIP_DEFLATED" or config['compression_method'] == "ZIP_STORED"):
                        zipObj.setpassword(self.get_backup_password())
                    zipObj.extractall(config['destination_path'])

                    notify_user(
                        title='SafeArchive: Files Restored Sucessfully',
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
        password = ctk.CTkInputDialog(text="Backup Password:", title="Backup Encryption")
        return bytes(password.get_input(), 'utf-8')


    def disable_restore_button(self):
        self.App.restore_button.configure(state="disabled")


    def enable_restore_button(self):
        self.App.restore_button.configure(state="normal")
