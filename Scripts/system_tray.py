#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from pystray import MenuItem as item
from Scripts.backup_utils import backup
from PIL import Image
import pystray


def backup_from_taskbar(App, icon, DESTINATION_PATH):
    """Backup from taskbar"""
    icon.stop()
    backup(App, DESTINATION_PATH)
    hide_window(App, DESTINATION_PATH)


def show_window(App, icon):
    """Show window"""
    icon.stop()
    App.after(0, App.deiconify)


def quit_window(App, icon):
    """Quit window"""
    icon.stop()
    App.destroy()


def hide_window(App, DESTINATION_PATH):
    """Hide window & show system taskbar"""
    App.withdraw()
    image = Image.open("assets/icon.ico")
    menu = item('Backup Now', lambda icon: backup_from_taskbar(App, icon, DESTINATION_PATH)), item('Open', lambda icon: show_window(App, icon)), item('Exit', lambda icon: quit_window(App, icon))
    App.icon = pystray.Icon("name", image, "SafeArchive", menu)
    App.icon.run()
