import os
import sys
from pathlib import Path
from plyer import notification

def notify_user(message, title=None, terminal_color=None):
    """
    Display notification message with specified title and message.
    """
    # get name of the script being executed
    if os.path.basename(sys.argv[0]) == "main.py":
        notification.notify(
            title=title,
            app_name="SafeArchive",
            message=message,
            app_icon=str(Path("assets/logo.ico").resolve()),
            timeout=10
        )
    else:
        print(f"{terminal_color}[*] {message}")
