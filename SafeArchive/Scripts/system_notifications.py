#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from pathlib import Path
from plyer import notification
from Scripts.configs import config


def notify_user(title, message, icon, terminal_color):
    """Display notification message with specified title, message, and icon"""
    if config['platform'] == "Windows":
        if config['notifications']:
            notification.notify(
                title=title,
                app_name="SafeArchive",
                message=message,
                app_icon=str(Path("assets/ICO").joinpath(icon).resolve()),
                timeout=10
            )
    else:
        print(f"{terminal_color}* {message}")
