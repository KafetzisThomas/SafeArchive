#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import sys
import colorama
import platform
from ..configs import ConfigDict
from ..system_notifications import notify_user
from ..configs import config
from colorama import Fore as F, Back as B

colorama.init(autoreset=True)


def get_config_info():
    print("Config Info:")
    print(f"\n{F.LIGHTGREEN_EX}Platform:{F.RESET} {config['platform']}")
    print(f"{F.LIGHTGREEN_EX}Source paths:{F.RESET} {config['source_paths']}")
    print(f"{F.LIGHTGREEN_EX}Destination path:{F.RESET} {config['destination_path']}")
    print(f"{F.LIGHTGREEN_EX}Notifications:{F.RESET} {config['notifications']}")
    print(f"{F.LIGHTGREEN_EX}System tray:{F.RESET} {config['system_tray']}")
    print(f"{F.LIGHTGREEN_EX}Encryption:{F.RESET} {config['encryption']}")
    print(f"{F.LIGHTGREEN_EX}Appearance mode:{F.RESET} {config['appearance_mode']}")
    print(f"{F.LIGHTGREEN_EX}Color theme:{F.RESET} {config['color_theme']}")
    print(
        f"{F.LIGHTGREEN_EX}Backup expiry date:{F.RESET} {config['backup_expiry_date']}"
    )
    print(f"{F.LIGHTGREEN_EX}Storage provider:{F.RESET} {config['storage_provider']}")
    print(
        f"{F.LIGHTGREEN_EX}Compression method:{F.RESET} {config['compression_method']}"
    )
    print(f"{F.LIGHTGREEN_EX}Allow Zip64:{F.RESET} {config['allowZip64']}")
    print(f"{F.LIGHTGREEN_EX}Compression level:{F.RESET} {config['compression_level']}")
    print(f"{F.LIGHTGREEN_EX}Backup interval:{F.RESET} {config['backup_interval']}")
    print(f"{F.LIGHTGREEN_EX}FTP hostname:{F.RESET} {config['ftp_hostname']}")
    print(f"{F.LIGHTGREEN_EX}FTP username:{F.RESET} {config['ftp_username']}")
    print(f"{F.LIGHTGREEN_EX}FTP password:{F.RESET} {config['ftp_password']}")
    print(f"{F.LIGHTGREEN_EX}Mega email:{F.RESET} {config['mega_email']}")
    print(f"{F.LIGHTGREEN_EX}Mega password:{F.RESET} {config['mega_password']}")
    print(
        f"{F.LIGHTGREEN_EX}Dropbox access token:{F.RESET} {config['dropbox_access_token']}\n"
    )


def edit_configs():
    """Configure preferences through script arguments"""

    try:
        print(f"{B.GREEN} -- CONFIGURATION -- {B.RESET}")
        folder_to_backup = input(
            f"{B.RED}! TO SET MORE THAN ONE SOURCE PATH, EDIT THE CONFIG FILE !\n! YOU NEED TO INPUT THE WHOLE PATH !{B.RESET}\nPlease enter the folder to backup: "
        )
        backup_destination = input("Please enter the destination folder: ")
        backup_expire = input(
            "if you want to set the expiry date of backups, enter here(leave None if you don't want): "
        )
        encryption = input("do you want to encrypt your backups?(y/N): ")
        compression_method = input(
            "Please enter the compression method for your backups\n(ZIP_DEFLATED, ZIP_STORED, ZIP_LZMA, ZIP_BZIP2): "
        )
        allowZip64 = input(
            "Do you want to allow Zip64 (backups larger than 4gb)?(y/N): "
        )
        compression_level = input(
            "Enter compression level for your backups (1: fast, ... 9: saves storage space): "
        )
        storage_provider = input(
            "if you want to use a storage provider along with your drive, enter here (Google Drive, FTP, MegaCloud, Dropbox)\n(leave None if you don't want): "
        )
        ftp_hostname = input(
            "if you have set FTP as your storage provider, enter hostname here: "
        )
        ftp_username = input(
            "if you have set FTP as your storage provider, enter username here: "
        )
        ftp_password = input(
            "if you have set FTP as your storage provider, enter password here: "
        )
        mega_email = input(
            "if you have set Mega as your storage provider, enter email here: "
        )
        mega_password = input(
            "if you have set Mega as your storage provider, enter password here: "
        )
        dropbox_access_token = input(
            "if you have set Dropbox as your storage provider, enter token here: "
        )

        # Rewrite values for *efficiency*
        encryption = True if encryption.lower() == "y" else False
        backup_expire = backup_expire if backup_expire else None
        storage_provider = storage_provider if storage_provider else "None"
        compression_method = (
            compression_method if compression_method else "ZIP_DEFLATED"
        )
        allowZip64 = allowZip64 if allowZip64 else "True"
        compression_level = compression_level if compression_level else 5
        backup_interval = None
        ftp_hostname = ftp_hostname if ftp_hostname else ""
        ftp_username = ftp_username if ftp_username else ""
        ftp_password = ftp_password if ftp_password else ""
        mega_email = mega_email if mega_email else ""
        mega_password = mega_password if mega_password else ""
        dropbox_access_token = dropbox_access_token if dropbox_access_token else ""

        SETTINGS_PATH = "settings.json"
        config = ConfigDict(
            {
                "platform": platform.system(),
                "source_paths": [folder_to_backup],
                "destination_path": backup_destination,
                "encryption": encryption,
                "backup_expiry_date": backup_expire,
                "compression_method": compression_method,
                "allowZip64": allowZip64,
                "compression_level": compression_level,
                "backup_interval": backup_interval,
                "storage_provider": storage_provider,
                "ftp_hostname": ftp_hostname,
                "ftp_username": ftp_username,
                "ftp_password": ftp_password,
                "mega_email": mega_email,
                "mega_password": mega_password,
                "dropbox_access_token": dropbox_access_token,
            },
            SETTINGS_PATH,
        )

        config_details = f"""
This is the configuration:
    source_paths: {folder_to_backup}
    destination_path: {backup_destination}
    backup_expiry_date: {backup_expire}
    encryption: {encryption}
    compression_method: {compression_method}
    allowZip64: {allowZip64}
    compression_level: {compression_level}
    backup_interval: {backup_interval}
    storage_provider: {storage_provider}
    ftp_hostname: {ftp_hostname}
    ftp_username: {ftp_username}
    ftp_password: {ftp_password}
    mega_email: {mega_email}
    mega_password: {mega_password}
    dropbox_access_token: {dropbox_access_token}
"""

        check = input(f"{config_details}\nIs this right? (Y/n): ")

        if check.lower() == "n":
            notify_user(message="Aborting...", terminal_color=F.YELLOW)
            sys.exit()
        else:
            config.save()
            notify_user(message="Done!", terminal_color=F.GREEN)

    except KeyboardInterrupt:
        notify_user(message="User abort!", terminal_color=F.RED)
