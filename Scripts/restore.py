#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import zipfile
import threading
import tkinter as tk
from Scripts.notification_handlers import notify_restore_completion
from Scripts.configs import config
import customtkinter as ctk


class RestoreBackup:
    """
    Create a toplevel widget containing a listbox inside a frame
    Show last backups inside the listbox
    Restore last backup files by selecting a specific one
    """

    def __init__(self, App, DESTINATION_PATH):
        self.App = App
        self.DESTINATION_PATH = DESTINATION_PATH

    def restore_backup(self):
        self.create_restore_window()
        self.create_listbox()
        self.populate_listbox()
        self.create_restore_button()

    def create_restore_window(self):
        self.restore_window = tk.Toplevel(self.App)  # Open new window (restore_window)
        self.restore_window.title("Select backup to restore")  # Set window title
        self.restore_window.geometry("410x245")  # Set window size
        self.restore_window.iconbitmap("assets/icon.ico")  # Set window title icon
        self.restore_window.resizable(False, False)  # Disable minimize/maximize buttons
        self.restore_window.configure(background=self.get_listbox_background())  # Set background color

    def create_listbox(self):
        frame = ctk.CTkFrame(master=self.restore_window)
        frame.place(x=8, y=8)
        self.listbox = tk.Listbox(
            master=frame,
            height=9,
            width=43,
            background=self.get_listbox_background(),
            foreground=self.get_listbox_foreground(),
            activestyle='dotbox',
            font='Helvetica, 13',
            justify="center",
            selectbackground=config['color_theme']
        )
        self.listbox.pack()

    def get_listbox_background(self):
        return "#343638" if config['appearance_mode'] == "dark" else "#ebebeb"

    def get_listbox_foreground(self):
        return "white" if config['appearance_mode'] == "dark" else "black"

    def populate_listbox(self):
        """Populate listbox with the zip file names from the DESTINATION_PATH directory"""
        for index, zip_file in enumerate(os.listdir(self.DESTINATION_PATH)):
            filename, _, filetype = zip_file.partition('.')
            if filetype == 'zip':
                self.listbox.insert(index, filename)
        self.listbox.selection_set(0)  # Set the initial selection to the first item

    def create_restore_button(self):
        self.App.restore_button = ctk.CTkButton(
            master=self.restore_window, text="Restore backup", command=self.run_restore_thread)
        self.App.restore_button.place(x=140, y=205)

    def run_restore_thread(self):
        """Create restore process thread"""
        threading.Thread(target=self.extract_item, daemon=True).start()

    def extract_item(self):
        """
        Extract (restore) selected zip file (backup)
        Move zip file content to it's original location
        """

        self.disable_restore_button()
        for item in self.listbox.curselection():
            # Open the zipfile in read mode, extract its content
            with zipfile.ZipFile(f'{self.DESTINATION_PATH}{self.listbox.get(item)}.zip') as zipObj:
                zipObj.extractall(config['destination_path'])
        notify_restore_completion(config['notifications'])
        self.enable_restore_button()

    def disable_restore_button(self):
        """Change restore button state to disabled"""
        self.App.restore_button.configure(state="disabled")

    def enable_restore_button(self):
        """Change restore button state back to normal"""
        self.App.restore_button.configure(state="normal")
