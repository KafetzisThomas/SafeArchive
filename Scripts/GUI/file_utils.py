#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import psutil
import platform
from tkinter import filedialog
from ..configs import config


def get_available_drives():
    """
    Retrieve a list of available external drives on the system.
    """
    drives = psutil.disk_partitions()
    external_drives = []

    if platform.system() == "Windows":
        for drive in drives:
            external_drives.append(drive.device.replace('\\', '/'))
    else:
        for drive in drives:
            if drive.mountpoint.startswith('/media/') or drive.mountpoint.startswith('/run/media/'):
                external_drives.append(f"{drive.mountpoint}/")
    return external_drives


def update_listbox(listbox, SOURCE_PATHS):
    """
    Insert source paths from the JSON file inside a listbox.
    """
    for index, item in enumerate(SOURCE_PATHS):
        listbox.insert(index, item)
    listbox.selection_set(0)  # Set the initial selection to the first item


def remove_item(listbox, SOURCE_PATHS):
    """
    Remove a source path from the listbox & JSON file, by selecting a specific one.
    """
    selected_items = listbox.curselection()
    for i in reversed(selected_items):
        del SOURCE_PATHS[i]
    config.save()

    try:
        listbox.delete(i)
    except UnboundLocalError:
        pass


def add_item(listbox, SOURCE_PATHS):
    """
    Add a source path to the listbox & JSON file.
    """
    try:
        source_path_file_explorer = filedialog.askdirectory(title='Backup these folders') + '/'
        if (source_path_file_explorer != '/') and (source_path_file_explorer not in SOURCE_PATHS):
            SOURCE_PATHS.append(source_path_file_explorer)
            config.save()  # This needs to be done because the saver may not be triggered by the sublist appending

            listbox.insert(len(SOURCE_PATHS) - 1, source_path_file_explorer)
    except TypeError:
        pass
