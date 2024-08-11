#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import tkinter as tk
import customtkinter as ctk
from PIL import Image
import webbrowser
from ..configs import config


class About:
    """
    Create a toplevel widget containing a frame with information about the program.
    """
    def __init__(self, App, version):
        self.App = App
        self.version = version
        self.create_about_window()
        self.create_frame()
        self.display_icon()
        self.display_name_label()
        self.display_version_label()
        self.display_line_label()
        self.display_website_label()
        self.display_website_link_button()
        self.display_author_label()
        self.display_author_name_label()
        self.display_license_label()
        self.display_license_link_text()


    def create_about_window(self):
        self.about_window = tk.Toplevel(self.App)
        self.about_window.title("About SafeArchive")
        self.about_window.geometry("513x305")
        self.about_window.iconbitmap("assets/ICO/info.ico") if config['platform'] == "Windows" else None
        self.about_window.resizable(False, False)  # Disable minimize/maximize buttons
        self.about_window.configure(background=self.get_window_background())


    def create_frame(self):
        self.frame = ctk.CTkFrame(master=self.about_window, corner_radius=10, height=230, width=395)
        self.frame.place(x=8, y=8)


    def get_window_background(self):
        """
        Determine the background color of the window based on the application's appearance mode.
        """
        return "#242424" if config['appearance_mode'] == "dark" else "#ebebeb"


    def get_bg_color(self):
        """
        Determine the background color of the frame based on the application's appearance mode.
        """
        return "#343638" if config['appearance_mode'] == "dark" else "#ebebeb"


    def get_fg_color(self):
        """
        Determine the foreground color (text color) based on the application's appearance mode.
        """
        return "#2b2b2b" if config['appearance_mode'] == "dark" else "#dbdbdb"


    def display_icon(self):
        icon_image = ctk.CTkImage(Image.open("assets/ICO/icon.ico"), size=(80, 80))
        icon_button = ctk.CTkButton(master=self.frame, text="", fg_color=self.get_fg_color(), image=icon_image, width=5, height=5)
        icon_button.place(x=150, y=0)
        icon_button.configure(state="disabled")


    def display_name_label(self):
        name_label = ctk.CTkLabel(
            master=self.frame, text="SafeArchive", font=('Helvetica', 20))
        name_label.place(x=140, y=85)


    def display_version_label(self):
        version_label = ctk.CTkLabel(
            master=self.frame, text=f"v{self.version}", font=('Helvetica', 15))
        version_label.place(x=173, y=110)


    def display_line_label(self):
        line_label = ctk.CTkLabel(
            master=self.frame, text="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", font=('Helvetica', 20))
        line_label.place(x=0, y=130)


    def display_website_label(self):
        website_label = ctk.CTkLabel(
            master=self.frame, text="Website:", font=('Helvetica', 13))
        website_label.place(x=10, y=150)


    def display_website_link_button(self):
        website_link_text = "https://github.com/KafetzisThomas/SafeArchive"
        website_link_button = ctk.CTkButton(
            master=self.frame, text=website_link_text, bg_color=self.get_bg_color(), width=5, height=5, font=('Helvetica', 13, "underline"), command=lambda: webbrowser.open(website_link_text))
        website_link_button.place(x=65, y=153)    


    def display_author_label(self):
        author_message_label = ctk.CTkLabel(
            master=self.frame, text="Code By:", font=('Helvetica', 13))
        author_message_label.place(x=10, y=175)


    def display_author_name_label(self):
        author_name_label = ctk.CTkLabel(
            master=self.frame, text="KafetzisThomas", font=('Helvetica', 13, "underline"))
        author_name_label.place(x=70, y=175)


    def display_license_label(self):
        license_label = ctk.CTkLabel(
            master=self.frame, text="Legal: Licensed under", font=('Helvetica', 13))
        license_label.place(x=10, y=200)


    def display_license_link_text(self):
        license_link_text = "https://www.gnu.org/licenses/gpl-3.0.html"
        license_link_button = ctk.CTkButton(
            master=self.frame, text="GPLv3", bg_color=self.get_bg_color(), width=5, height=5, font=('Helvetica', 13, "underline"), command=lambda: webbrowser.open(license_link_text))
        license_link_button.place(x=140, y=203)
