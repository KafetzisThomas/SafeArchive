#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import tkinter as tk
import customtkinter as ctk
from PIL import Image
import webbrowser
from Scripts.configs import config


def about(App, version):
    """Create a toplevel widget containing a frame with information about the program"""
    about_window = tk.Toplevel(App)  # Open new window (about_window)
    about_window.title("About SafeArchive")  # Set window title
    about_window.geometry("410x245")  # Set window size
    about_window.iconbitmap("assets/icon.ico") if config['platform'] == "Windows" else None  # Set window title icon
    about_window.resizable(False, False)  # Disable minimize/maximize buttons
    about_window.configure(background="#242424")  # Set background color

    frame = ctk.CTkFrame(master=about_window,
                         corner_radius=10, height=230, width=395)
    frame.place(x=8, y=8)

    # Set background color
    if config['appearance_mode'] == "dark":
        about_window.configure(background="#242424")
        bg_color = "#343638"
        fg_color = "#2b2b2b"
    else:
        about_window.configure(background="#ebebeb")
        bg_color = "#ebebeb"
        fg_color = "#dbdbdb"

    icon_image = ctk.CTkImage(Image.open("assets/icon.ico"), size=(80, 80))
    icon_button = ctk.CTkButton(master=frame, text="", fg_color=fg_color, image=icon_image, width=5, height=5)
    icon_button.place(x=150, y=0)
    icon_button.configure(state="disabled")  # Change icon button state to disabled

    name_label = ctk.CTkLabel(
        master=frame, text="SafeArchive", font=('Helvetica', 20))
    name_label.place(x=140, y=85)

    version_label = ctk.CTkLabel(
        master=frame, text=f"v{version}", font=('Helvetica', 15))
    version_label.place(x=173, y=110)

    line_label = ctk.CTkLabel(
        master=frame, text="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", font=('Helvetica', 20))
    line_label.place(x=0, y=130)

    website_label = ctk.CTkLabel(
        master=frame, text="Website:", font=('Helvetica', 13))
    website_label.place(x=10, y=150)

    website_link_text = "https://github.com/KafetzisThomas/SafeArchive"
    website_link_button = ctk.CTkButton(
        master=frame, text=website_link_text, bg_color=bg_color, width=5, height=5, font=('Helvetica', 13, "underline"), command=lambda: webbrowser.open(website_link_text))
    website_link_button.place(x=65, y=153)

    author_message_label = ctk.CTkLabel(
        master=frame, text="Code By:", font=('Helvetica', 13))
    author_message_label.place(x=10, y=175)

    author_name_label = ctk.CTkLabel(
        master=frame, text="KafetzisThomas", font=('Helvetica', 13, "underline"))
    author_name_label.place(x=70, y=175)

    license_label = ctk.CTkLabel(
        master=frame, text="Legal: Licensed under", font=('Helvetica', 13))
    license_label.place(x=10, y=200)

    license_link_text = "https://www.gnu.org/licenses/gpl-3.0.html"
    license_link_button = ctk.CTkButton(
        master=frame, text="GPLv3", bg_color=bg_color, width=5, height=5, font=('Helvetica', 13, "underline"), command=lambda: webbrowser.open(license_link_text))
    license_link_button.place(x=140, y=203)
