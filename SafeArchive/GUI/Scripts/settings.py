#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import tkinter as tk
import customtkinter as ctk
from Scripts.widgets import Combobox, Switch
from Scripts.configs import config


class Settings:
    """Create a toplevel widget containing a frame with settings"""

    def __init__(self, App):
        self.App = App
        self.create_settings_window()
        self.create_frame()
        self.display_settings_label()
        self.display_line_label()
        self.display_appearance_mode_label()
        self.create_appearance_mode_combobox()
        self.display_color_theme_label()
        self.create_color_theme_combobox()
        self.display_storage_provider_label()
        self.create_storage_provider_combobox()
        self.display_compression_method_label()
        self.create_compression_method_combobox()
        self.create_system_tray_switch()
        self.create_encryption_switch()
        self.create_notifications_switch()
        self.create_allowZip64_switch()
        self.display_apply_btn()


    def create_settings_window(self):
        self.settings_window = tk.Toplevel(self.App)
        self.settings_window.title("Settings")
        self.settings_window.geometry("600x310")
        self.settings_window.iconbitmap("assets/ICO/gear.ico") if config['platform'] == "Windows" else None
        self.settings_window.resizable(False, False)  # Disable minimize/maximize buttons
        self.settings_window.configure(background=self.get_window_background())


    def create_frame(self):
        self.frame = ctk.CTkFrame(master=self.settings_window, corner_radius=10, height=240, width=585)
        self.frame.place(x=8, y=8)


    def get_window_background(self):
        return "#242424" if config['appearance_mode'] == "dark" else "#ebebeb"


    def display_settings_label(self):
        settings_label = ctk.CTkLabel(master=self.frame, text="Settings", font=('Helvetica', 22))
        settings_label.place(x=170, y=10)


    def display_line_label(self):
        line_label = ctk.CTkLabel(master=self.frame, text="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", font=('Helvetica', 20))
        line_label.place(x=0, y=35)


    def display_appearance_mode_label(self):
        appearance_mode_label = ctk.CTkLabel(master=self.frame, text="Appearance Mode:", font=('Helvetica', 15))
        appearance_mode_label.place(x=20, y=60)


    def create_appearance_mode_combobox(self):
        appearance_mode_combobox_var = ctk.StringVar(value=config['appearance_mode'])
        appearance_mode_options = ["dark", "light"]
        appearance_mode_combobox = ctk.CTkComboBox(
            master=self.frame,
            width=112,
            values=appearance_mode_options,
            command=lambda choice: Combobox(key='appearance_mode', choice=choice),
            variable=appearance_mode_combobox_var
        )

        appearance_mode_combobox.place(x=160, y=60)


    def display_color_theme_label(self):
        color_theme_label = ctk.CTkLabel(master=self.frame, text="Color Theme:", font=('Helvetica', 15))
        color_theme_label.place(x=20, y=90)


    def create_color_theme_combobox(self):
        color_theme_combobox_var = ctk.StringVar(value=config['color_theme'])
        color_theme_options = ["blue", "green"]
        color_theme_combobox = ctk.CTkComboBox(
            master=self.frame,
            width=112,
            values=color_theme_options,
            command=lambda choice: Combobox(key='color_theme', choice=choice),
            variable=color_theme_combobox_var
        )

        color_theme_combobox.place(x=160, y=90)


    def display_storage_provider_label(self):
        storage_provider_label = ctk.CTkLabel(master=self.frame, text="Storage Provider:", font=('Helvetica', 15))
        storage_provider_label.place(x=20, y=120)


    def create_storage_provider_combobox(self):
        storage_provider_combobox_var = ctk.StringVar(value=config['storage_provider'])
        storage_provider_options = ["None", "Google Drive", "Mega", "Dropbox", "FTP"]
        storage_provider_combobox = ctk.CTkComboBox(
            master=self.frame,
            width=112,
            values=storage_provider_options,
            command=lambda choice: Combobox(key='storage_provider', choice=choice),
            variable=storage_provider_combobox_var
        )

        storage_provider_combobox.place(x=160, y=120)


    def display_compression_method_label(self):
        compression_method_label = ctk.CTkLabel(master=self.frame, text="Compression Method:", font=('Helvetica', 15))
        compression_method_label.place(x=290, y=60)


    def create_compression_method_combobox(self):
        compression_method_combobox_var = ctk.StringVar(value=config['compression_method'])
        compression_method_options = ["ZIP_DEFLATED", "ZIP_STORED", "ZIP_LZMA", "ZIP_BZIP2"]
        compression_method_combobox = ctk.CTkComboBox(
            master=self.frame,
            width=130,
            values=compression_method_options,
            command=lambda choice: Combobox(key='compression_method', choice=choice),
            variable=compression_method_combobox_var
        )

        compression_method_combobox.place(x=450, y=56)


    def create_system_tray_switch(self):
        system_tray_switch_var = ctk.StringVar(value="on" if config['system_tray'] else "off")
        system_tray_switch = ctk.CTkSwitch(
            master=self.frame,
            text="Display system tray [Windows]",
            font=('Helvetica', 15),
            command=lambda: Switch(key='system_tray', switch_var=system_tray_switch_var),
            variable=system_tray_switch_var,
            onvalue="on",
            offvalue="off"
        )

        system_tray_switch.place(x=20, y=155)


    def create_encryption_switch(self):
        encryption_switch_var = ctk.StringVar(value="on" if config['encryption'] else "off")
        encryption_switch = ctk.CTkSwitch(
            master=self.frame,
            text="Encrypt Backups",
            font=('Helvetica', 15),
            command=lambda: Switch(key='encryption', switch_var=encryption_switch_var),
            variable=encryption_switch_var,
            onvalue="on",
            offvalue="off"
        )

        encryption_switch.place(x=20, y=182)


    def create_notifications_switch(self):
        notifications_switch_var = ctk.StringVar(value="on" if config['notifications'] else "off")
        notifications_switch = ctk.CTkSwitch(
            master=self.frame,
            text="Allow all system notifications",
            font=('Helvetica', 15),
            command=lambda: Switch(key='notifications', switch_var=notifications_switch),
            variable=notifications_switch_var,
            onvalue="on",
            offvalue="off"
        )

        notifications_switch.place(x=20, y=209)


    def create_allowZip64_switch(self):
        allowZip64_switch_var = ctk.StringVar(value="on" if config['allowZip64'] else "off")
        allowZip64_switch = ctk.CTkSwitch(
            master=self.frame,
            text="allowZip64",
            font=('Helvetica', 15),
            command=lambda: Switch(key='allowZip64', switch_var=allowZip64_switch_var),
            variable=allowZip64_switch_var,
            onvalue="on",
            offvalue="off"
        )

        allowZip64_switch.place(x=290, y=155)


    def apply_btn(self):
        """Close window (settings_window)"""
        self.settings_window.destroy()


    def display_apply_btn(self):
        apply_button = ctk.CTkButton(master=self.settings_window, text="Apply", command=self.apply_btn)
        apply_button.place(x=145, y=255)
