#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from ..configs import config


class SetupUI:
    """
    Manage UI configuration based on user preferences.
    """
    def __init__(self, DESTINATION_PATH):
        self.DESTINATION_PATH = DESTINATION_PATH

    def get_background_color(self):
        return "#343638" if config['appearance_mode'] == "dark" else "#ebebeb"

    def get_foreground_color(self):
        return "white" if config['appearance_mode'] == "dark" else "black"

    def get_image1(self):
        return "assets/PNG/info.png" if config['appearance_mode'] == "dark" else "assets/PNG/info2.png"

    def get_image2(self):
        return "assets/PNG/gear.png" if config['appearance_mode'] == "dark" else "assets/PNG/gear2.png"

    def get_image3(self):
        return "assets/PNG/restore.png" if config['appearance_mode'] == "dark" else "assets/PNG/restore2.png"

    def get_icon_fg_color(self):
        return "#242424" if config['appearance_mode'] == "dark" else "#ebebeb"

    def get_listbox_selection_background(self):
        if config['appearance_mode'] == "dark":
            hex_color = "#1f6aa5" if config['color_theme'] == "blue" else "#2fa572"
        else:
            hex_color = "#3b8ed0" if config['color_theme'] == "blue" else "#2cc985"
        return hex_color
