import os
import webbrowser
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtWidgets import QDialog, QFrame, QLabel, QPushButton, QVBoxLayout, QHBoxLayout


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
        # main frame layout
        main_frame = QFrame(self)
        main_frame.setGeometry(8, 8, 395, 234)  # x, y, width, height
        main_layout = QVBoxLayout(main_frame)
        main_layout.setContentsMargins(10, 0, 10, 10)
        main_layout.setSpacing(10)

        # top frame
        top_frame = QFrame()
        top_layout = QVBoxLayout(top_frame)
        top_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(5)

        # logo icon
        icon_pixmap = QPixmap(os.path.join("assets", "logo.png")).scaled(
            80, 80, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio, 
            transformMode=Qt.TransformationMode.SmoothTransformation
        )
        icon_label = QLabel()
        icon_label.setPixmap(icon_pixmap)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_layout.addWidget(icon_label)

        # project name + version labels
        name_label = QLabel("SafeArchive")
        name_label.setFont(QFont('Helvetica', 14))
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_layout.addWidget(name_label)

        version_label = QLabel(f"v{self.version}")
        version_label.setFont(QFont('Helvetica', 12))
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_layout.addWidget(version_label)

        main_layout.addWidget(top_frame)

        # bottom frame
        bottom_frame = QFrame()
        bottom_layout = QVBoxLayout(bottom_frame)
        bottom_layout.setContentsMargins(20, 0, 20, 0)
        bottom_layout.setSpacing(0)

        # github link
        website_layout = QHBoxLayout()
        website_layout.setContentsMargins(0, 0, 0, 0)
        website_layout.setSpacing(5)

        website_label = QLabel("Website:")
        website_label.setFont(QFont('Helvetica', 10))

        website_link_button = QPushButton("https://github.com/KafetzisThomas/SafeArchive")
        website_link_button.setFlat(True)
        website_link_button.setCursor(Qt.CursorShape.PointingHandCursor)
        website_link_button.clicked.connect(lambda: webbrowser.open("https://github.com/KafetzisThomas/SafeArchive"))

        website_layout.addWidget(website_label)
        website_layout.addWidget(website_link_button)
        website_layout.addStretch()  # push everything to the left
        bottom_layout.addLayout(website_layout)

        # author label
        author_layout = QHBoxLayout()
        author_layout.setContentsMargins(0, 0, 0, 0)
        author_layout.setSpacing(5)

        author_label = QLabel("Code By: KafetzisThomas")
        author_label .setFont(QFont('Helvetica', 10))

        author_layout.addWidget(author_label)
        author_layout.addStretch()
        bottom_layout.addLayout(author_layout)

        # license label
        license_layout = QHBoxLayout()
        license_layout.setContentsMargins(0, 0, 0, 0)
        license_layout.setSpacing(5)

        license_label = QLabel("Legal: Licensed under")
        license_label.setFont(QFont('Helvetica', 10))

        license_link_button = QPushButton("GPLv3")
        license_link_button.setFlat(True)
        license_link_button.setCursor(Qt.CursorShape.PointingHandCursor)
        license_link_button.clicked.connect(lambda: webbrowser.open("https://www.gnu.org/licenses/gpl-3.0.html"))

        license_layout.addWidget(license_label)
        license_layout.addWidget(license_link_button)
        license_layout.addStretch()
        bottom_layout.addLayout(license_layout)

        main_layout.addWidget(bottom_frame)
