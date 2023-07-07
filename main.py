#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Project Title: SafeArchive (https://github.com/KafetzisThomas/SafeArchive)
# Author / Project Owner: KafetzisThomas (https://github.com/KafetzisThomas)
# License: GPLv3
# NOTE: By contributing to this project, you agree to the terms of the GPLv3 license, and agree to grant the project owner the right to also provide or sell this software, including your contribution, to anyone under any other license, with no compensation to you.

version = "1.1.0"

# Import built-in modules
import os, sys, zipfile, datetime, threading
from datetime import date
from tkinter import filedialog
import tkinter as tk

# Import module files
import Scripts.configs as configs
import Scripts.cloud as cloud

# Import other (third-party) modules
from plyer import notification
from pystray import MenuItem as item
from PIL import Image
import humanize, psutil, pystray
import customtkinter as ctk

configs.config.load() # Load the JSON file into memory

# Get value from the JSON file
# Set the destination directory path (type: string)
DESTINATION_PATH = configs.config['destination_path'] + 'SafeArchive/'

class App(ctk.CTk):
  def __init__(self):
    super().__init__()
    
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    self.title(f"SafeArchive {version}")  # Set window title
    self.resizable(False, False)  # Disable minimize/maximize buttons
    self.geometry("500x500")  # Set window size
    self.iconbitmap("assets/icon.ico")  # Set window title icon

    try:
      if not os.path.exists(DESTINATION_PATH):  # Create the destination directory path if it doesn't exist
        os.makedirs(DESTINATION_PATH)
    except FileNotFoundError:
      self.notify_drive_reconnection()
      sys.exit()
    except PermissionError:
      print(f"No permissions given to make directory: '{DESTINATION_PATH}'.",
            "Change it in settings.json or run with elevated priveleges")
      sys.exit(77)

    backup_options_label = ctk.CTkLabel(master=self, text="Drive Properties ━━━━━━━━━━━━━━━━", font=('Helvetica', 20))
    backup_options_label.place(x=15, y=15)

    device_label = ctk.CTkLabel(master=self, text="Device", font=('Helvetica', 12))
    device_label.place(x=15, y=45)

    drives = psutil.disk_partitions()
    drive_options = [drive.device.replace('\\', '/') for drive in drives]
    
    device_combobox_var = ctk.StringVar(value=DESTINATION_PATH.replace('SafeArchive/', ''))  # Set initial value

    combobox_1 = ctk.CTkComboBox(master=self, width=470, values=drive_options, command=self.drives_combobox, variable=device_combobox_var)
    combobox_1.place(x=15, y=70)

    size_of_backup_label = ctk.CTkLabel(master=self, text=f"Size of backup: {humanize.naturalsize(self.get_backup_size())}", font=('Helvetica', 12))
    size_of_backup_label.place(x=15, y=100)

    total_drive_space_label = ctk.CTkLabel(master=self, text=f"Free space on ({DESTINATION_PATH.replace('SafeArchive/', '')}): {self.storage_media_free_space()} GB", font=('Helvetica', 12))
    total_drive_space_label.place(x=15, y=120)

    last_backup_label = ctk.CTkLabel(master=self, text=f"Last backup: {self.last_backup()}", font=('Helvetica', 12))
    last_backup_label.place(x=15, y=140)

    additional_settings_label = ctk.CTkLabel(master=self, text="Backup Options ━━━━━━━━━━━━━━━━", font=('Helvetica', 20))
    additional_settings_label.place(x=15, y=170)

    keep_my_backups_label = ctk.CTkLabel(master=self, text="Keep my backups", font=('Helvetica', 12))
    keep_my_backups_label.place(x=15, y=200)
    
    backup_expiry_date_combobox_var = ctk.StringVar(value=configs.config['backup_expiry_date'])  # Set initial value
    
    backup_expiry_date_options = ["1 month", "3 months", "6 months", "9 months", "1 year", "Forever (default)"]

    backup_expiry_date_combobox = ctk.CTkComboBox(
      master=self,
      width=150,
      values=backup_expiry_date_options,
      command=self.backup_expiry_date_combobox,
      variable=backup_expiry_date_combobox_var
    )

    backup_expiry_date_combobox.place(x=15, y=225)
    
    self.cloud_switch_var = ctk.StringVar(value="on" if configs.config['backup_to_cloud'] else "off")  # Set initial value
    
    switch = ctk.CTkSwitch(
      master=self,
      text="Back up to Cloud",
      command=self.cloud_switch,
      variable=self.cloud_switch_var,
      onvalue="on",
      offvalue="off"
    )

    switch.place(x=340, y=225)

    backup_these_folders_label = ctk.CTkLabel(master=self, text="Backup these folders", font=('Helvetica', 12))
    backup_these_folders_label.place(x=15, y=255)

    listbox_frame = ctk.CTkFrame(master=self, corner_radius=10)
    listbox_frame.place(x=10, y=280)

    source_listbox = tk.Listbox(
      master=listbox_frame,
      height=4,
      width=52,
      background="#343638",
      foreground="white",
      activestyle='dotbox',
      font='Helvetica'
    )

    source_listbox.pack(padx=7, pady=7)

    def update_listbox():
      """Insert source paths from JSON file inside a listbox"""
      global index
      for index, item in enumerate(configs.config['source_path']):
        source_listbox.insert(index, item)

    def remove_item():
      """Remove a source path from listbox & JSON file, by selecting a specific one"""
      selected_items = source_listbox.curselection()
      for i in reversed(selected_items):
        del configs.config['source_path'][i]
      configs.config.save()

      try: source_listbox.delete(i)  
      except UnboundLocalError: pass

    def add_item():
      """Add a source path to the listbox & JSON file"""
      source_path_file_explorer = filedialog.askdirectory(title='Backup these folders') + '/'
      if (source_path_file_explorer != '/') and (source_path_file_explorer not in configs.config['source_path']):
        configs.config['source_path'].append(source_path_file_explorer)
        configs.config.save() # This needs to be done because the saver may not be triggered by the sublist appending

        source_listbox.insert(len(configs.config['source_path']) - 1, source_path_file_explorer)

    update_listbox()

    plus_button = ctk.CTkButton(master=self, text="+", width=20, height=10, command=add_item)
    plus_button.place(x=220, y=250)

    minus_button = ctk.CTkButton(master=self, text="-", width=20, height=10, command=remove_item)
    minus_button.place(x=250, y=250)

    status_label = ctk.CTkLabel(master=self, text="Status ━━━━━━━━━━━━━━━━━━━━", font=('Helvetica', 20))
    status_label.place(x=15, y=375)

    self.backup_progressbar = ctk.CTkProgressBar(master=self, width=475, height=15, corner_radius=0, orientation='horizontal', mode='indeterminate')
    self.backup_progressbar.place(x=15, y=415)

    restore_image = ctk.CTkImage(Image.open("assets/restore.png"), size=(25, 25))

    self.restore_button = ctk.CTkButton(master=self, text="", fg_color="#242424", image=restore_image, width=5, height=5, command=self.restore_backup)
    self.restore_button.place(x=15, y=450)

    self.backup_button = ctk.CTkButton(master=self, text="BACKUP", command=self.run_backup)
    self.backup_button.place(x=200, y=450)

    close_button = ctk.CTkButton(master=self, text="CLOSE", command=self.destroy)
    close_button.place(x=350, y=450)

    self.protocol('WM_DELETE_WINDOW', self.hide_window)


  def drives_combobox(self, choice):
    """Update the value of the key in the dictionary"""
    configs.config['destination_path'] = choice

  def cloud_switch(self):
    """
    Get switch position (True/False)
    Update the value of the key in the dictionary
    """
    switch_position = self.cloud_switch_var.get()
    configs.config['backup_to_cloud'] = True if switch_position == "on" else False

  def backup_expiry_date_combobox(self, choice):
    """Update the value of the key in the dictionary"""
    configs.config['backup_expiry_date'] = choice

  def get_backup_size(self):
    """Walk through all files in the destination path & return backup size"""
    total_size = 0  # Initialize total size to 0

    for dirpath, _, filenames in os.walk(DESTINATION_PATH):
      for file in filenames:
        filepath = os.path.join(dirpath, file)

        total_size += os.path.getsize(filepath)  # Add the size of each file to the total size
    return total_size

  def storage_media_free_space(self):
    """Return storage media free space"""
    disk_usage = psutil.disk_usage(configs.config['destination_path']).free  # Get disk usage statistics in bytes
    free_space = round(disk_usage / (1024**3), 2)  # Convert free space to GB
    return free_space

  def get_drive_usage_percentage(self):
    """Return drive usage percentage"""
    drive_usage_percentage = psutil.disk_usage(configs.config['destination_path']).percent  # Get drive usage percentage
    return drive_usage_percentage

  def last_backup(self):
    """
    Check if last backup is older than 30 days, if True then display a system notification message
    Return last backup date
    """
    try:
      files = [file for file in os.listdir(DESTINATION_PATH) if os.path.isfile(os.path.join(DESTINATION_PATH, file))]  # Get a list of all the files in the destination path
      files.sort(key=self.get_modification_time)  # Sort the list of files based on their modification time

      most_recently_modified_file = files[-1]  # The most recently modified file
      filename, _, filetype = most_recently_modified_file.partition('.')

      # Get the modification time of the most recently modified file
      modification_time = datetime.datetime.fromtimestamp(os.path.getmtime(f"{DESTINATION_PATH}{most_recently_modified_file}"))

      # Check if the file is older than three months
      if modification_time < (datetime.datetime.now()) - (datetime.timedelta(days=30)):
        self.notify_drive_reconnection()

      if filetype != 'zip': 
        filename = "No backup"
    except IndexError: 
      filename = "No backup"
    return filename

  def get_modification_time(self, file):
    """Return the modification time of zip file"""
    file_path = os.path.join(DESTINATION_PATH, file)
    return os.path.getmtime(file_path)

  def backup_expiry_date(self):
    """
    Check if previous backups are older than expiry date
    Remove every past backup if True
    """
    for filename in os.listdir(DESTINATION_PATH):  # Iterate through all files in the destination directory
      filepath = os.path.join(DESTINATION_PATH, filename)

      modification_time = datetime.datetime.fromtimestamp(os.path.getmtime(filepath))  # Get the modification time of the file

      if configs.config['backup_expiry_date'] == "1 month": days = 30
      elif configs.config['backup_expiry_date'] == "3 months": days = 90
      elif configs.config['backup_expiry_date'] == "6 months": days = 180
      elif configs.config['backup_expiry_date'] == "9 months": days = 270
      elif configs.config['backup_expiry_date'] == "1 year": days = 365
    
      if modification_time < (datetime.datetime.now()) - (datetime.timedelta(days=days)):  # Check if the file is older than JSON value
        os.remove(filepath)  # Delete the file

  def notify_backup_completion(self):
    """Display notification message when backup process successfully completes"""
    notification.notify(
      title="Backup Completed",
      app_name="SafeArchive",
      message=f"SafeArchive has finished the backup to '{DESTINATION_PATH.replace('SafeArchive/', '')}'.",
      app_icon="assets/icon.ico",
      timeout = 10
    )

  def notify_restore_completion(self):
    """Display notification message when restore process successfully completes"""
    notification.notify(
      title="Files Restored Sucessfully",
      app_name="SafeArchive",
      message=f"SafeArchive has finished the restore.",
      app_icon="assets/icon.ico",
      timeout = 10
    )

  def notify_drive_reconnection(self):
    """Display notification message when drive was disconnected / for too long"""
    notification.notify(
      title="Reconnect your drive",
      app_name="SafeArchive",
      message="Your SafeArchive Drive was disconnected for too long. Reconnect it to keep saving copies of your files.",
      app_icon="assets/icon.ico",
      timeout = 10
    )

  def notify_drive_space_limitation(self):
    """Display notification message when drive storage is running out"""
    notification.notify(
      title="Warning: Your Drive storage is running out.",
      app_name="SafeArchive",
      message="Your Drive storage is almost full. To make sure your files can sync, clean up space.",
      app_icon="assets/icon.ico",
      timeout = 10
    )

  def notify_cloud_space_limitation(self):
    """Display notification message when cloud storage is running out"""
    notification.notify(
      title="Warning: Your Google Drive storage is running out.",
      app_name="SafeArchive",
      message="Your Google Drive storage is almost full. To make sure your files can sync, clean up space.",
      app_icon="assets/icon.ico",
      timeout = 10
    )

  def backup(self):
    """
    Zip (backup) source path files to destination path:
      * Compression method: ZIP_DEFLATED
      * allowZip64 is set to True (this parameter use the ZIP64 extensions when the zip file is larger than 4gb)
      * Compresslevel is set to 9 (its sometimes really slow when source path files are too large, saves storage space)
    Initialize & Upload local backups to cloud if JSON value is True
    """
    self.backup_button.configure(state="disabled")  # Change backup button state to disabled
    # Check if drive usage is below or equal to 90%
    if self.get_drive_usage_percentage() <= 90:
      # Set expiry date for old backups (type: integer)
      if configs.config['backup_expiry_date'] != "Forever (default)": self.backup_expiry_date()
      # Open the zipfile in write mode, create zip file with current date in its name
      with zipfile.ZipFile(f'{DESTINATION_PATH}{date.today()}.zip', mode='w', compression=zipfile.ZIP_DEFLATED, allowZip64=True, compresslevel=9) as zipObj:
        for item in configs.config['source_path']:  # Iterate over each path in the source list
          source_item_label = ctk.CTkLabel(master=self, text=item, height=20, font=('Helvetica', 12))
          source_item_label.place(x=15, y=430)

          for root, dirs, files in os.walk(item):  # Iterate over the files and folders in the path
            for dirname in dirs:
              dirpath = os.path.join(root, dirname)
              zipObj.write(dirpath)  # Write the folder to the zip archive

            for filename in files:
              filepath = os.path.join(root, filename)
              zipObj.write(filepath)  # Write the file to the zip archive
    
          source_item_label.place_forget()

      # Choose if you want local backups to be uploaded to cloud (type: boolean)
      if configs.config['backup_to_cloud']:
        cloud.initialize()
        if cloud.get_storage_usage_percentage() >= 90: self.notify_cloud_space_limitation()  # Check if cloud storage usage is above or equal to 90%
        else: cloud.backup_to_cloud(DESTINATION_PATH[:-1], parent_folder_id=cloud.gdrive_folder['id'])  # Upload the local folder and its content

      self.notify_backup_completion()
    else: self.notify_drive_space_limitation()

    self.backup_button.configure(state="normal")  # Change backup button state back to normal

  def start_progress_bar(self):
    """Start/Stop progress bar & call backup() function"""
    self.backup_progressbar.start()
    self.backup()
    self.backup_progressbar.stop()

  def run_backup(self):
    """Start thread when backup is about to take action"""
    threading.Thread(target=self.start_progress_bar, daemon=True).start()

  def restore_backup(self):
    """
    Create a toplevel widget containing a listbox inside a frame
    Show last backups inside the listbox
    Restore last backup files by selecting a specific one
    """
    restore_window = tk.Toplevel(self)  # Open new window (restore_window)
    restore_window.title("Select backup to restore")  # Set window title
    restore_window.geometry("440x240")  # Set window size
    restore_window.iconbitmap("assets/icon.ico")  # Set window title icon
    restore_window.resizable(False, False)  # Disable minimize/maximize buttons
    restore_window.configure(background="#242424")  # Set background color

    frame = ctk.CTkFrame(master=restore_window, corner_radius=10, height=180, width=425)
    frame.place(x=8, y=8)

    listbox = tk.Listbox(
      master=frame,
      height=9,
      width=47,
      background="#343638",
      foreground="white",
      activestyle='dotbox',
      font='Helvetica'
    )

    listbox.pack()

    for index, zip_file in enumerate(os.listdir(DESTINATION_PATH)):
      filename, _,filetype = zip_file.partition('.')
      
      if filetype == 'zip':  
        listbox.insert(index, filename)

    def selected_item():
      """
      Extract (restore) selected zip file (backup)
      Move zip file content to it's original location
      """
      self.restore_button.configure(state="disabled")  # Change backup button state to disabled

      for item in listbox.curselection():
        # Open the zipfile in read mode, extract its content
        with zipfile.ZipFile(f'{DESTINATION_PATH}{listbox.get(item)}.zip') as zipObj:
          zipObj.extractall(configs.config['destination_path'])

      self.notify_restore_completion()
      self.restore_button.configure(state="normal")  # Change backup button state back to normal

    def run_restore():
      """Start thread when restoration is processing"""
      threading.Thread(target=selected_item, daemon=True).start()  # Create restore process thread

    self.restore_button = ctk.CTkButton(master=restore_window, text="Restore backup", command=run_restore)
    self.restore_button.place(x=150, y=197)

  def backup_from_taskbar(self, icon):
    """Backup from taskbar"""
    icon.stop()
    self.backup()
    self.hide_window()

  def show_window(self, icon):
    """Show window"""
    icon.stop()
    self.after(0, self.deiconify)

  def quit_window(self, icon):
    """Quit window"""
    icon.stop()
    self.destroy()

  def hide_window(self):
    """Hide window & show system taskbar"""
    self.withdraw()
    image = Image.open("assets/icon.ico")
    menu = item('Backup Now', self.backup_from_taskbar), item('Open', self.show_window), item('Exit', self.quit_window)
    self.icon = pystray.Icon("name", image, "SafeArchive", menu)
    self.icon.run()

if __name__ == "__main__":
  app = App()
  app.mainloop()
