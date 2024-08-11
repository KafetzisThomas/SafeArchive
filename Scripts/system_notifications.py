#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import sys
from pathlib import Path
from plyer import notification
from .configs import config


def notify_user(message, title=None, icon=None, terminal_color=None):
    """
    Display notification message with specified title, message, and icon.
    """
    if os.path.basename(sys.argv[0]) == "main.py":  # Get name of the script being executed
        if config['notifications']:
            notification.notify(
                title=title,
                app_name="SafeArchive",
                message=message,
                app_icon=str(Path("assets/ICO").joinpath(icon).resolve()),
                timeout=10
            )
    else:
        print(f"{terminal_color}[*] {message}")
