import os
import platform
import datetime
import psutil
from PyQt6.QtWidgets import QFileDialog
from .configs import config

# storage utils

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

def storage_media_free_space(path=None):
    """
    Return storage media free space.
    Use provided path or fallback to the config if running cli.
    """
    target_path = path if path else config['destination_path']
    disk_usage = psutil.disk_usage(target_path).free
    free_space = round(disk_usage / (1024**3), 2)  # convert free space to gb
    return free_space

def get_drive_usage_percentage():
    """
    Return drive usage percentage.
    """
    drive_usage_percentage = psutil.disk_usage(config['destination_path']).percent
    return drive_usage_percentage

# backup utils

def create_destination_directory_path(DESTINATION_PATH):
    """
    Create the destination directory path if it doesn't exist.
    """
    if not os.path.exists(DESTINATION_PATH):
        os.makedirs(DESTINATION_PATH)

def get_backup_size(DESTINATION_PATH):
    """
    Walk through all files in the destination path and return the total size.
    """
    total_size = 0
    for dirpath, _, filenames in os.walk(DESTINATION_PATH):
        for file in filenames:
            filepath = os.path.join(dirpath, file)
            # add size of each file to total size
            total_size += os.path.getsize(filepath)

    return total_size

def get_modification_time(file, DESTINATION_PATH):
    """
    Return the modification time of zip file.
    """
    file_path = os.path.join(DESTINATION_PATH, file)
    return os.path.getmtime(file_path)

def last_backup(DESTINATION_PATH):
    """
    Return last backup date.
    """
    try:
        # get a list of all the files in the destination path
        files = [file for file in os.listdir(DESTINATION_PATH) if os.path.isfile(os.path.join(DESTINATION_PATH, file))]
        
        # sort the list of files based on their modification time
        files.sort(key=lambda file: get_modification_time(DESTINATION_PATH, file))

        # the most recently modified file
        most_recently_modified_file = files[-1]
        filename, _, filetype = most_recently_modified_file.partition('.')

        if filetype != 'zip':
            filename = "No backup"
    except IndexError:
        filename = "No backup"
    return filename

def backup_expiry_date(DESTINATION_PATH):
    """
    Check if previous backups are older than expiry date,
    remove every past backup if True.
    """
    is_valid_expiry_date  = True
    # iterate through all files in the destination directory
    for filename in os.listdir(DESTINATION_PATH):
        filepath = os.path.join(DESTINATION_PATH, filename)

        modification_time = datetime.datetime.fromtimestamp(
            # get the modification time of the file
            os.path.getmtime(filepath))

        if config['backup_expiry_date'] == "1 month":
            days = 30
        elif config['backup_expiry_date'] == "3 months":
            days = 90
        elif config['backup_expiry_date'] == "6 months":
            days = 180
        elif config['backup_expiry_date'] == "9 months":
            days = 270
        elif config['backup_expiry_date'] == "1 year":
            days = 365
        else:
            is_valid_expiry_date = False

        # check if the file is older than json value
        if is_valid_expiry_date and modification_time < (datetime.datetime.now()) - (datetime.timedelta(days=int(days))):
            os.remove(filepath)

# listbox ui utils

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
