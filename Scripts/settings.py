#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import tkinter as tk
import customtkinter as ctk
from Scripts.widgets import NotificationSwitch, AppearanceModeCombobox, ColorThemeCombobox, StorageProviderCombobox
from Scripts.configs import config

class Settings:
    """Create a toplevel widget containing a frame with settings"""

    def __init__(self, App):
        self.App = App


    def settings(self):
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
        self.create_notifications_switch()
        self.display_apply_btn()


    def create_settings_window(self):
        self.settings_window = tk.Toplevel(self.App)  # Open new window (settings_window)
        self.settings_window.title("Settings")  # Set window title
        self.settings_window.geometry("410x245")  # Set window size
        self.settings_window.iconbitmap("assets/ICO/gear.ico") if config['platform'] == "Windows" else None  # Set window title icon
        self.settings_window.resizable(False, False)  # Disable minimize/maximize buttons
        self.settings_window.configure(background=self.get_window_background())  # Set background color


    def create_frame(self):
        self.frame = ctk.CTkFrame(master=self.settings_window, corner_radius=10, height=190, width=395)
        self.frame.place(x=8, y=8)


    def get_window_background(self):
        return "#242424" if config['appearance_mode'] == "dark" else "#ebebeb"


    def display_settings_label(self):
        settings_label = ctk.CTkLabel(master=self.frame, text="Settings", font=('Helvetica', 22))
        settings_label.place(x=160, y=10)


    def display_line_label(self):
        line_label = ctk.CTkLabel(master=self.frame, text="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", font=('Helvetica', 20))
        line_label.place(x=0, y=35)


    def display_appearance_mode_label(self):
        appearance_mode_label = ctk.CTkLabel(master=self.frame, text="Appearance Mode:", font=('Helvetica', 15))
        appearance_mode_label.place(x=80, y=60)


    def create_appearance_mode_combobox(self):
        appearance_mode_combobox_var = ctk.StringVar(value=config['appearance_mode'])  # Set initial value
        appearance_mode_options = ["system", "dark", "light"]
        appearance_mode_combobox = ctk.CTkComboBox(
            master=self.frame,
            width=90,
            values=appearance_mode_options,
            command=AppearanceModeCombobox,
            variable=appearance_mode_combobox_var
        )

        appearance_mode_combobox.place(x=220, y=60)


    def display_color_theme_label(self):
        color_theme_label = ctk.CTkLabel(master=self.frame, text="Color Theme:", font=('Helvetica', 15))
        color_theme_label.place(x=80, y=90)


    def create_color_theme_combobox(self):
        color_theme_combobox_var = ctk.StringVar(value=config['color_theme'])  # Set initial value
        color_theme_options = ["blue", "green"]
        color_theme_combobox = ctk.CTkComboBox(
            master=self.frame,
            width=90,
            values=color_theme_options,
            command=ColorThemeCombobox,
            variable=color_theme_combobox_var
        )

        color_theme_combobox.place(x=220, y=90)


    def display_storage_provider_label(self):
        storage_provider_label = ctk.CTkLabel(master=self.frame, text="Storage Provider:", font=('Helvetica', 15))
        storage_provider_label.place(x=80, y=120)


    def create_storage_provider_combobox(self):
        storage_provider_combobox_var = ctk.StringVar(value=config['storage_provider'])  # Set initial value
        storage_provider_options = ["Google Drive", "FTP"]
        storage_provider_combobox = ctk.CTkComboBox(
            master=self.frame,
            width=90,
            values=storage_provider_options,
            command=StorageProviderCombobox,
            variable=storage_provider_combobox_var
        )

        storage_provider_combobox.place(x=220, y=120)


    def create_notifications_switch(self):
        notifications_switch_var = ctk.StringVar(value="on" if config['notifications'] else "off")  # Set initial value
        notifications_switch = ctk.CTkSwitch(
            master=self.frame,
            text="Allow all system notifications",
            font=('Helvetica', 15),
            command=lambda: NotificationSwitch(notifications_switch_var),
            variable=notifications_switch_var,
            onvalue="on",
            offvalue="off"
        )

        notifications_switch.place(x=80, y=155)


    def apply_btn(self):
        """Close window (settings_window)"""
        self.settings_window.destroy()


    def display_apply_btn(self):
        apply_button = ctk.CTkButton(master=self.settings_window, text="Apply", command=self.apply_btn)
        apply_button.place(x=140, y=207)
