import tkinter as tk
import customtkinter as ctk
from PIL import Image
import webbrowser
from ..configs import config

import os
import webbrowser
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QDialog, QFrame, QLabel, QPushButton
from PyQt6.QtGui import QFont, QIcon, QPixmap


class AboutWindow(QDialog):
    def __init__(self, parent=None, version=""):
        super().__init__(parent)
        self.App = parent  # reference to the main window
        self.version = version

        self.create_about_window()
        self.create_widgets()

    def create_about_window(self):
        self.setWindowTitle("About SafeArchive")
        self.setFixedSize(QSize(410, 250))

        # make window non resizable
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
    
    def create_widgets(self):
        # frame
        self.frame = QFrame(self)
        self.frame.setFixedSize(395, 230)
        self.frame.move(8, 8) 

        # logo icon
        icon_pixmap = QPixmap(os.path.join("assets", "PNG", "logo.png")).scaled(
            80, 80, 
            aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio, 
            transformMode=Qt.TransformationMode.SmoothTransformation
        )
        icon_label = QLabel(self.frame)
        icon_label.setPixmap(icon_pixmap)
        icon_label.setGeometry(157, 0, 80, 80)

        # project name label
        name_label = QLabel("SafeArchive", self.frame)
        name_label.setFont(QFont('Helvetica', 20))
        name_label.move(140, 85)

        # version label
        version_label = QLabel(f"v{self.version}", self.frame)
        version_label.setFont(QFont('Helvetica', 15))
        version_label.move(173, 110)

        # line seperator
        line_label = QLabel("—" * 25, self.frame)
        line_label.setFont(QFont('Helvetica', 20))
        line_label.move(0, 130)

        # github link
        website_label = QLabel("Website:", self.frame)
        website_label.setFont(QFont('Helvetica', 13))
        website_label.move(10, 150)

        website_link_text = "https://github.com/KafetzisThomas/SafeArchive"
        website_link_button = QPushButton(website_link_text, self.frame)
        website_link_button.setFlat(True)  # make it look like a link
        website_link_button.setCursor(Qt.CursorShape.PointingHandCursor)
        website_link_button.clicked.connect(lambda: webbrowser.open(website_link_text))
        website_link_button.move(65, 153)
        website_link_button.setFixedWidth(300)

        # author label
        author_label = QLabel("Code By: KafetzisThomas", self.frame)
        author_label.setFont(QFont('Helvetica', 13))
        author_label.move(10, 175)

        # license label
        license_link_text = "https://www.gnu.org/licenses/gpl-3.0.html"
        license_label = QLabel("Legal: Licensed under", self.frame)
        license_label.setFont(QFont('Helvetica', 13))
        license_label.move(10, 200)
        
        license_link_button = QPushButton("GPLv3", self.frame)
        license_link_button.setFlat(True)
        license_link_button.setCursor(Qt.CursorShape.PointingHandCursor)
        license_link_button.clicked.connect(lambda: webbrowser.open(license_link_text))
        license_link_button.move(140, 203)
        license_link_button.setFixedWidth(50)





# class About:
#     """
#     Create a toplevel widget containing a frame with information about the program.
#     """
#     def __init__(self, App, version):
#         self.App = App
#         self.version = version
#         self.create_about_window()
#         self.create_frame()
#         self.display_icon()
#         self.display_name_label()
#         self.display_version_label()
#         self.display_line_label()
#         self.display_website_label()
#         self.display_website_link_button()
#         self.display_author_label()
#         self.display_author_name_label()
#         self.display_license_label()
#         self.display_license_link_text()

#     def create_about_window(self):
#         self.about_window = tk.Toplevel(self.App)
#         self.about_window.title("About SafeArchive")
#         self.about_window.geometry("513x305")
#         self.about_window.iconbitmap("assets/ICO/info.ico") if config['platform'] == "Windows" else None
#         self.about_window.resizable(False, False)  # Disable minimize/maximize buttons
#         self.about_window.configure(background="#242424")

#     def create_frame(self):
#         self.frame = ctk.CTkFrame(master=self.about_window, corner_radius=10, height=230, width=395)
#         self.frame.place(x=8, y=8)

#     def display_icon(self):
#         icon_image = ctk.CTkImage(Image.open("assets/ICO/icon.ico"), size=(80, 80))
#         icon_button = ctk.CTkButton(master=self.frame, text="", fg_color="#2b2b2b", image=icon_image, width=5, height=5)
#         icon_button.place(x=150, y=0)
#         icon_button.configure(state="disabled")

#     def display_name_label(self):
#         name_label = ctk.CTkLabel(
#             master=self.frame, text="SafeArchive", font=('Helvetica', 20))
#         name_label.place(x=140, y=85)

#     def display_version_label(self):
#         version_label = ctk.CTkLabel(
#             master=self.frame, text=f"v{self.version}", font=('Helvetica', 15))
#         version_label.place(x=173, y=110)

#     def display_line_label(self):
#         line_label = ctk.CTkLabel(
#             master=self.frame, text="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", font=('Helvetica', 20))
#         line_label.place(x=0, y=130)

#     def display_website_label(self):
#         website_label = ctk.CTkLabel(
#             master=self.frame, text="Website:", font=('Helvetica', 13))
#         website_label.place(x=10, y=150)

#     def display_website_link_button(self):
#         website_link_text = "https://github.com/KafetzisThomas/SafeArchive"
#         website_link_button = ctk.CTkButton(
#             master=self.frame, text=website_link_text, bg_color="#343638", width=5, height=5, font=('Helvetica', 13, "underline"), command=lambda: webbrowser.open(website_link_text))
#         website_link_button.place(x=65, y=153)    

#     def display_author_label(self):
#         author_message_label = ctk.CTkLabel(
#             master=self.frame, text="Code By:", font=('Helvetica', 13))
#         author_message_label.place(x=10, y=175)

#     def display_author_name_label(self):
#         author_name_label = ctk.CTkLabel(
#             master=self.frame, text="KafetzisThomas", font=('Helvetica', 13, "underline"))
#         author_name_label.place(x=70, y=175)

#     def display_license_label(self):
#         license_label = ctk.CTkLabel(
#             master=self.frame, text="Legal: Licensed under", font=('Helvetica', 13))
#         license_label.place(x=10, y=200)

#     def display_license_link_text(self):
#         license_link_text = "https://www.gnu.org/licenses/gpl-3.0.html"
#         license_link_button = ctk.CTkButton(
#             master=self.frame, text="GPLv3", bg_color="#343638", width=5, height=5, font=('Helvetica', 13, "underline"), command=lambda: webbrowser.open(license_link_text))
#         license_link_button.place(x=140, y=203)
