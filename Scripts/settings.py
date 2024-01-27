#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import tkinter as tk
import customtkinter as ctk
from Scripts.widgets import NotificationSwitch, AppearanceModeCombobox, ColorThemeCombobox, StorageProviderCombobox
from Scripts.configs import config


def settings(App):
    """Create a toplevel widget containing a frame with settings"""
    settings_window = tk.Toplevel(App)  # Open new window (settings_window)
    settings_window.title("Settings")  # Set window title
    settings_window.geometry("410x245")  # Set window size
    settings_window.iconbitmap("assets/icon.ico") if config['platform'] == "Windows" else None  # Set window title icon
    settings_window.resizable(False, False)  # Disable minimize/maximize buttons
    settings_window.configure(background="#242424")  # Set background color

    frame = ctk.CTkFrame(master=settings_window,
                         corner_radius=10, height=190, width=395)
    frame.place(x=8, y=8)

    # Set background color
    if config['appearance_mode'] == "dark":
        settings_window.configure(background="#242424")
    else:
        settings_window.configure(background="#ebebeb")

    settings_label = ctk.CTkLabel(
        master=frame, text="Settings", font=('Helvetica', 22))
    settings_label.place(x=160, y=10)

    line_label = ctk.CTkLabel(
        master=frame, text="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", font=('Helvetica', 20))
    line_label.place(x=0, y=35)

    appearance_mode_label = ctk.CTkLabel(
        master=frame, text="Appearance Mode:", font=('Helvetica', 15))
    appearance_mode_label.place(x=80, y=60)

    appearance_mode_combobox_var = ctk.StringVar(
        value=config['appearance_mode'])  # Set initial value
    appearance_mode_options = ["system", "dark", "light"]

    appearance_mode_combobox = ctk.CTkComboBox(
        master=frame,
        width=90,
        values=appearance_mode_options,
        command=AppearanceModeCombobox,
        variable=appearance_mode_combobox_var
    )

    appearance_mode_combobox.place(x=220, y=60)

    color_theme_label = ctk.CTkLabel(
        master=frame, text="Color Theme:", font=('Helvetica', 15))
    color_theme_label.place(x=80, y=90)

    color_theme_combobox_var = ctk.StringVar(
        value=config['color_theme'])  # Set initial value
    color_theme_options = ["blue", "green"]

    color_theme_combobox = ctk.CTkComboBox(
        master=frame,
        width=90,
        values=color_theme_options,
        command=ColorThemeCombobox,
        variable=color_theme_combobox_var
    )

    color_theme_combobox.place(x=220, y=90)

    storage_provider_label = ctk.CTkLabel(
        master=frame, text="Storage Provider:", font=('Helvetica', 15))
    storage_provider_label.place(x=80, y=120)

    storage_provider_combobox_var = ctk.StringVar(
        value=config['storage_provider'])  # Set initial value
    storage_provider_options = ["Google Drive", "FTP"]

    storage_provider_combobox = ctk.CTkComboBox(
        master=frame,
        width=90,
        values=storage_provider_options,
        command=StorageProviderCombobox,
        variable=storage_provider_combobox_var
    )

    storage_provider_combobox.place(x=220, y=120)

    notifications_switch_var = ctk.StringVar(
        value="on" if config['notifications'] else "off")  # Set initial value

    switch = ctk.CTkSwitch(
        master=frame,
        text="Allow all system notifications",
        font=('Helvetica', 15),
        command=lambda: NotificationSwitch(notifications_switch_var),
        variable=notifications_switch_var,
        onvalue="on",
        offvalue="off"
    )

    switch.place(x=80, y=155)

    # Close the window (settings_window)
    def apply_button():
        settings_window.destroy()

    apply_button = ctk.CTkButton(
        master=settings_window, text="Apply", command=apply_button)
    apply_button.place(x=140, y=207)
