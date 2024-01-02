#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from plyer import notification


def notify_backup_completion(DESTINATION_PATH, notifications):
    """Display notification message when backup process successfully completes"""
    if notifications:
        notification.notify(
            title="Backup Completed",
            app_name="SafeArchive",
            message=f"SafeArchive has finished the backup to '{DESTINATION_PATH.replace('SafeArchive/', '')}'.",
            app_icon="assets/icon.ico",
            timeout=10
        )


def notify_restore_completion(notifications):
    """Display notification message when restore process successfully completes"""
    if notifications:
        notification.notify(
            title="Files Restored Sucessfully",
            app_name="SafeArchive",
            message=f"SafeArchive has finished the restore.",
            app_icon="assets/icon.ico",
            timeout=10
        )


def notify_drive_reconnection(notifications):
    """Display notification message when drive was disconnected / for too long"""
    if notifications:
        notification.notify(
            title="Reconnect your drive",
            app_name="SafeArchive",
            message="Your SafeArchive Drive was disconnected for too long. Reconnect it to keep saving copies of your files.",
            app_icon="assets/icon.ico",
            timeout=10
        )


def notify_drive_space_limitation(notifications):
    """Display notification message when drive storage is running out"""
    if notifications:
        notification.notify(
            title="Warning: Your Drive storage is running out.",
            app_name="SafeArchive",
            message="Your Drive storage is almost full. To make sure your files can sync, clean up space.",
            app_icon="assets/icon.ico",
            timeout=10
        )


def notify_cloud_space_limitation(notifications):
    """Display notification message when cloud storage is running out"""
    if notifications:
        notification.notify(
            title="Warning: Your Google Drive storage is running out.",
            app_name="SafeArchive",
            message="Your Google Drive storage is almost full. To make sure your files can sync, clean up space.",
            app_icon="assets/icon.ico",
            timeout=10
        )

def notify_client_secrets_file_missing(notifications):
    if notifications:
        notification.notify(
            title="Error: File 'client_secrets.json' is missing.",
            app_name="SafeArchive",
            message="File not found in the program directory. Please refer to the documentation for instructions on how to get it.",
            app_icon="assets/icon.ico",
            timeout=10
        )
