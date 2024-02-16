#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from pathlib import Path
from plyer import notification

# Get absolute paths of icon files
app_icon = str(Path("assets/ICO").joinpath("icon.ico").resolve())
backup_completion_icon = str(Path("assets/ICO").joinpath("backup_completed.ico").resolve())
restore_completion_icon = str(Path("assets/ICO").joinpath("restore.ico").resolve())
drive_icon = str(Path("assets/ICO").joinpath("drive.ico").resolve())
cloud_icon = str(Path("assets/ICO").joinpath("cloud.ico").resolve())
file_missing_icon = str(Path("assets/ICO").joinpath("file_missing.ico").resolve())
error_icon = str(Path("assets/ICO").joinpath("error.ico").resolve())


def notify_backup_completion(DESTINATION_PATH, notifications):
    """Display notification message when backup process successfully completes"""
    if notifications:
        notification.notify(
            title="SafeArchive: Backup Completed",
            app_name="SafeArchive",
            message=f"SafeArchive has finished the backup to '{DESTINATION_PATH.replace('SafeArchive/', '')}'.",
            app_icon=backup_completion_icon,
            timeout=10
        )


def notify_restore_completion(notifications):
    """Display notification message when restore process successfully completes"""
    if notifications:
        notification.notify(
            title="SafeArchive: Files Restored Sucessfully",
            app_name="SafeArchive",
            message=f"SafeArchive has finished the restore.",
            app_icon=restore_completion_icon,
            timeout=10
        )


def notify_drive_reconnection(notifications):
    """Display notification message when drive was disconnected / for too long"""
    if notifications:
        notification.notify(
            title="SafeArchive: Reconnect your drive",
            app_name="SafeArchive",
            message="Your SafeArchive Drive was disconnected for too long. Reconnect it to keep saving copies of your files.",
            app_icon=drive_icon,
            timeout=10
        )


def notify_drive_space_limitation(notifications):
    """Display notification message when drive storage is running out"""
    if notifications:
        notification.notify(
            title="SafeArchive: [Warning] Your Drive storage is running out.",
            app_name="SafeArchive",
            message="Your Drive storage is almost full. To make sure your files can sync, clean up space.",
            app_icon=drive_icon,
            timeout=10
        )


def notify_cloud_space_limitation(notifications):
    """Display notification message when cloud storage is running out"""
    if notifications:
        notification.notify(
            title="SafeArchive: [Warning] Your Google Drive storage is running out.",
            app_name="SafeArchive",
            message="Your Google Drive storage is almost full. To make sure your files can sync, clean up space.",
            app_icon=cloud_icon,
            timeout=10
        )

def notify_missing_client_secrets_file(notifications):
    if notifications:
        notification.notify(
            title="SafeArchive: [Error] File 'client_secrets.json' is missing.",
            app_name="SafeArchive",
            message="File not found in the program directory. Please refer to the documentation for instructions on how to get it.",
            app_icon=file_missing_icon,
            timeout=10
        )


def notify_missing_ftp_credentials(notifications):
    if notifications:
        notification.notify(
            title="SafeArchive: [Error] FTP credentials are missing.",
            app_name="SafeArchive",
            message="FTP not configured. Please edit the configuration file (settings.json) to add your ftp credentials.",
            app_icon=error_icon,
            timeout=10
        )
