import os
import webbrowser
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtWidgets import QDialog, QFrame, QLabel, QPushButton


class AboutWindow(QDialog):
    def __init__(self, App, version=""):
        super().__init__(App)
        self.App = App
        self.version = version
        self.create_about_window()
        self.create_widgets()
        self.exec()

    def create_about_window(self):
        self.setWindowTitle("About SafeArchive")
        self.setFixedSize(QSize(410, 250))

        # hide ? mark
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
    
    def create_widgets(self):
        # frame
        self.frame = QFrame(self)
        self.frame.setFixedSize(395, 230)
        self.frame.move(8, 8) 

        # logo icon
        icon_pixmap = QPixmap(os.path.join("assets", "PNG", "logo.png")).scaled(
            80, 80, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio, 
            transformMode=Qt.TransformationMode.SmoothTransformation
        )
        icon_label = QLabel(self.frame)
        icon_label.setPixmap(icon_pixmap)
        icon_label.setGeometry(157, 0, 80, 80)  # x, y, width, height

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
