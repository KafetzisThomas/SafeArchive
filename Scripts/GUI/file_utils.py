import psutil
import platform
from PyQt6.QtWidgets import QFileDialog
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
    Insert source paths from the json inside listbox.
    """
    listbox.clear()
    for item in SOURCE_PATHS:
        listbox.addItem(item)

    # set initial selection to the first item
    if listbox.count() > 0:
        listbox.setCurrentRow(0)

def remove_item(listbox, SOURCE_PATHS):
    """
    Remove a source path from the listbox and json file by selecting a specific one.
    """
    row = listbox.currentRow()  # get current selected row index
    try:
        item_text = listbox.item(row).text()
        SOURCE_PATHS.remove(item_text)
        listbox.takeItem(row)
    except AttributeError:
        pass
    finally:
        config.save()

def add_item(listbox, SOURCE_PATHS):
    """
    Add a source path to the listbox and json file.
    """
    source_path_file_explorer = QFileDialog.getExistingDirectory(None, "Backup these folders")
    if source_path_file_explorer:
        # normalize path which ends with a slash
        source_path_file_explorer = source_path_file_explorer.replace('\\', '/') + '/'
        if source_path_file_explorer not in SOURCE_PATHS:
            SOURCE_PATHS.append(source_path_file_explorer)
            config.save()
            listbox.addItem(source_path_file_explorer)
