#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from pathlib import Path
from plyer import notification
from Scripts.configs import config


def notify_user(title, message, icon):
    """Display notification message with specified title, message, and icon"""
    if config['notifications']:
        notification.notify(
            title=title,
            app_name="SafeArchive",
            message=message,
            app_icon=str(Path("assets/ICO").joinpath(icon).resolve()),
            timeout=10
        )
