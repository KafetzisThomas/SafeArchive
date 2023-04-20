#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Project Title: SafeArchive (https://github.com/KafetzisThomas/SafeArchive)
# Author / Project Owner: KafetzisThomas (https://github.com/KafetzisThomas)

# Import built-in modules
import os, zipfile, json, datetime, threading
from datetime import date
from tkinter import filedialog
import tkinter as tk

# Import other (third-party) modules
from plyer import notification
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from pystray import MenuItem as item
from PIL import Image
import humanize, psutil, pystray
import customtkinter as ctk

# ================================ SET CONFIGS ================================

config = {
  'source_path': [
  os.path.expanduser('~/Desktop').replace('\\', '/') + '/',
  os.path.expanduser('~/Documents').replace('\\', '/') + '/',
  os.path.expanduser('~/Downloads').replace('\\', '/') + '/'
  ],
  'destination_path': os.path.abspath(os.sep).replace("\\", "/"),
  'backup_to_cloud': "off",
  'backup_expiry_date': "Forever (default)"
}

if not os.path.exists('settings.json'):
  with open('settings.json', 'w') as file:
    json.dump(config, file, indent=2)

# Load the JSON file into memory
with open('settings.json', 'r') as file:
  config = json.load(file)

## Get value from the JSON file

# Set the destination directory path (type: string)
destination_path = config['destination_path'] + 'SafeArchive/'

# Create the destination directory path if it doesn't exist
if not os.path.exists(destination_path):
  os.makedirs(destination_path)

# =================================== MAIN ====================================

class App(ctk.CTk):
  def __init__(self):
    super().__init__()
    
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    self.title(f"SafeArchive")  # Set window title
    self.resizable(False, False)  # Disable minimize/maximize buttons
    self.geometry("500x500")  # Set window size
    self.iconbitmap("assets/icon.ico")  # Set window title icon

    ## Get backup size

    # Initialize total size to 0
    total_size = 0

    # Walk through all files in the destination path
    for dirpath, dirnames, filenames in os.walk(destination_path):
      for file in filenames:
        filepath = os.path.join(dirpath, file)
          
        # Add the size of each file to the total size
        total_size += os.path.getsize(filepath)

    ## Get storage media free space

    # Get disk usage statistics in bytes
    disk_usage = psutil.disk_usage(config['destination_path']).free

    # Convert free space to GB
    free_space = round(disk_usage / (1024**3), 2)

    try:
      # Get a list of all the files in the destination path
      files = [file for file in os.listdir(destination_path) if os.path.isfile(os.path.join(destination_path, file))]

      # Sort the list of files based on their modification time
      files.sort(key=self.get_modification_time)

      # The most recently modified file
      most_recently_modified_file = files[-1]

      filename, _, filetype = most_recently_modified_file.partition('.')

      if filetype != 'zip':
        filename = "No backup"

    except IndexError:
      filename = "No backup"

    for filename in os.listdir(destination_path): 
      filepath = os.path.join(destination_path, filename)

      # Get the modification time of the file
      modification_time = datetime.datetime.fromtimestamp(os.path.getmtime(filepath))

      # Check if the file is older than three months
      if modification_time < (datetime.datetime.now()) - (datetime.timedelta(days=90)):
        self.reconnect_drive_notification()

    backup_options_label = ctk.CTkLabel(master=self, text="Drive Properties ━━━━━━━━━━━━━━━━", font=('Helvetica', 20))
    backup_options_label.place(x=15, y=15)

    device_label = ctk.CTkLabel(master=self, text="Device", font=('Helvetica', 12))
    device_label.place(x=15, y=45)

    drives = psutil.disk_partitions()
    drive_options = [drive.device.replace('\\', '/') for drive in drives]
    
    device_combobox_var = ctk.StringVar(value=destination_path.replace('SafeArchive/', ''))  # Set initial value

    combobox_1 = ctk.CTkComboBox(master=self, width=470, values=drive_options, command=self.drives_combobox, variable=device_combobox_var)
    combobox_1.place(x=15, y=70)

    size_of_backup_label = ctk.CTkLabel(master=self, text=f"Size of backup: {humanize.naturalsize(total_size)}", font=('Helvetica', 12))
    size_of_backup_label.place(x=15, y=100)

    total_drive_space_label = ctk.CTkLabel(master=self, text=f"Free space on ({destination_path.replace('SafeArchive/', '')}): {free_space} GB", font=('Helvetica', 12))
    total_drive_space_label.place(x=15, y=120)

    last_backup_label = ctk.CTkLabel(master=self, text=f"Last backup: {filename}", font=('Helvetica', 12))
    last_backup_label.place(x=15, y=140)

    additional_settings_label = ctk.CTkLabel(master=self, text="Backup Options ━━━━━━━━━━━━━━━━", font=('Helvetica', 20))
    additional_settings_label.place(x=15, y=170)

    keep_my_backups_label = ctk.CTkLabel(master=self, text="Keep my backups", font=('Helvetica', 12))
    keep_my_backups_label.place(x=15, y=200)
    
    backup_expiry_date_combobox_var = ctk.StringVar(value=config['backup_expiry_date'])  # Set initial value
    
    backup_expiry_date_options = ["1 month", "3 months", "6 months", "9 months", "1 year", "Forever (default)"]

    combobox_2 = ctk.CTkComboBox(
      master=self,
      width=150,
      values=backup_expiry_date_options,
      command=self.backup_expiry_date_combobox,
      variable=backup_expiry_date_combobox_var
    )

    combobox_2.place(x=15, y=225)
    
    self.cloud_switch_var = ctk.StringVar(value=config['backup_to_cloud'])  # Set initial value
    
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

    listbox_1 = tk.Listbox(
      master=listbox_frame,
      height=4,
      width=52,
      background="#343638",
      foreground="white",
      activestyle='dotbox',
      font='Helvetica'
    )

    listbox_1.pack(padx=7, pady=7)

    self.counter = 1
    def update_listbox():
      for item in config['source_path']:
        listbox_1.insert(self.counter, item)
        self.counter += 1

    def remove_item():
      selected_items = listbox_1.curselection()
      for i in reversed(selected_items):
        del config['source_path'][i]

      with open('settings.json', 'w') as f:
        json.dump(config, f, indent=2)
      
      try: listbox_1.delete(i)  
      except UnboundLocalError: pass

    def add_item():
      source_path_file_explorer = filedialog.askdirectory(title='Backup these folders') + '/'

      if (source_path_file_explorer != '/') and (source_path_file_explorer not in config['source_path']):
        # Add value to key
        config['source_path'].append(source_path_file_explorer)

        # Write the updated dictionary to the JSON file
        with open('settings.json', 'w') as f:
          json.dump(config, f, indent=2)

        listbox_1.insert(self.counter, source_path_file_explorer)

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

    self.backup_button = ctk.CTkButton(master=self, text="BACKUP", command=self.start_function)
    self.backup_button.place(x=200, y=450)

    close_button = ctk.CTkButton(master=self, text="CLOSE", command=self.destroy)
    close_button.place(x=350, y=450)

    self.protocol('WM_DELETE_WINDOW', self.hide_window)


  # Get the modification time of zip file
  def get_modification_time(self, file):
    file_path = os.path.join(destination_path, file)
    return os.path.getmtime(file_path)

  def drives_combobox(self, choice):
    # Update the value of the key in the dictionary
    config['destination_path'] = choice

    # Write the updated dictionary back to the JSON file
    with open('settings.json', 'w') as f:
      json.dump(config, f, indent=2)

  # Upload the local folder and its content
  def cloud_switch(self):
    # Update the value of the key in the dictionary
    config['backup_to_cloud'] = self.cloud_switch_var.get()

    # Write the updated dictionary back to the JSON file
    with open('settings.json', 'w') as f:
      json.dump(config, f, indent=2)

  def backup_expiry_date_combobox(self, choice):
    # Update the value of the key in the dictionary
    config['backup_expiry_date'] = choice

    # Write the updated dictionary back to the JSON file
    with open('settings.json', 'w') as f:
      json.dump(config, f, indent=2)

  def BackupExpiryDate(self):
    # Iterate through all files in the destination directory
    for filename in os.listdir(destination_path): 
      filepath = os.path.join(destination_path, filename)

      # Get the modification time of the file
      modification_time = datetime.datetime.fromtimestamp(os.path.getmtime(filepath))

      if config['backup_expiry_date'] == "1 month": days = 30
      elif config['backup_expiry_date'] == "3 months": days = 90
      elif config['backup_expiry_date'] == "6 months": days = 180
      elif config['backup_expiry_date'] == "9 months": days = 270
      elif config['backup_expiry_date'] == "1 year": days = 365
    
      # Check if the file is older than JSON value
      if modification_time < (datetime.datetime.now()) - (datetime.timedelta(days=days)):
        os.remove(filepath)  # Delete the file
  
  # Show notification message when backup process successfully completes
  def backup_completed_notification(self):
    # Show notification
    notification.notify(
      title="Backup Completed",
      app_name="SafeArchive",
      message=f"SafeArchive has finished the backup to '{destination_path.replace('SafeArchive/', '')}'.",
      app_icon="assets/icon.ico",
      timeout = 10
    )

  # Show notification message when backup process successfully completes
  def restore_completed_notification(self):
    # Show notification
    notification.notify(
      title="Files Restored Sucessfully",
      app_name="SafeArchive",
      message=f"SafeArchive has finished the restore.",
      app_icon="assets/icon.ico",
      timeout = 10
    )

  # Show notification message when drive was disconnected for too long
  def reconnect_drive_notification(self):
    # Show notification
    notification.notify(
      title="Reconnect your drive",
      app_name="SafeArchive",
      message="Your SafeArchive Drive was disconnected for too long. Reconnect it to keep saving copies of your files.",
      app_icon="assets/icon.ico",
      timeout = 10
    )

  def backup(self):
    self.backup_button.configure(state="disabled")  # Change backup button state to disabled

    if config['backup_expiry_date'] != "Forever (default)":
      self.BackupExpiryDate()
  
    # Open the zipfile in write mode, create zip file with the current date in its name
    with zipfile.ZipFile(f'{destination_path}{date.today()}.zip', mode='w', compression=zipfile.ZIP_DEFLATED, allowZip64=True, compresslevel=9) as zipObj:
      # Iterate over each path in the source list
      for item in config['source_path']:
        # Iterate over the files and folders in the path
        for root, dirs, files in os.walk(item):
          # Add each directory to the archive
          for dirname in dirs:
            dirpath = os.path.join(root, dirname)
            zipObj.write(dirpath)  # Write the folder to the zip archive

          # Add each file to the archive
          for filename in files:
            filepath = os.path.join(root, filename)
            zipObj.write(filepath)  # Write the file to the zip archive
  
    # ============================== AUTHENTICATION ===============================    

    if config['backup_to_cloud'] != "off":
      gauth = GoogleAuth()  # Create a GoogleAuth instance

      gauth.LoadCredentialsFile('credentials.txt')  # Load the stored OAuth2 credential

      # Check if stored credential is valid
      if gauth.credentials is None:
        gauth.LocalWebserverAuth()  # If not, authenticate with LocalWebserverAuth()
      elif gauth.access_token_expired:
        gauth.Refresh()  # If expired, refresh the token
      else:
        gauth.Authorize()  # If valid, use credential to authenticate with GoogleDrive

      gauth.SaveCredentialsFile('credentials.txt')  # Save credentials to file

      drive = GoogleDrive(gauth)  # Create a GoogleDrive instance to interact with Google Drive

      # Check if the folder already exists in Google Drive
      file_list = drive.ListFile({'q': f"title='SafeArchive' and mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()

      if file_list:
        gdrive_folder = file_list[0]  # The folder already exists, so just update the existing files

      else:
        # The folder doesn't exist, so create a new one
        gdrive_folder = drive.CreateFile({'title': 'SafeArchive', 'mimeType': 'application/vnd.google-apps.folder'})
        gdrive_folder.Upload()


    # Upload backup files
    def backup_to_cloud(folderpath, parent_folder_id=None):
      foldername = os.path.basename(folderpath)
      folder_metadata = {'title': foldername, 'mimeType': 'application/vnd.google-apps.folder'}

      if parent_folder_id is not None:
        folder_metadata['parents'] = [{'id': parent_folder_id}]

      file_list = drive.ListFile({'q': f"title='{foldername}' and mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()

      for filename in os.listdir(folderpath):
        filepath = os.path.join(folderpath, filename)

        file_list = drive.ListFile({'q': f"title='{filename}' and '{gdrive_folder['id']}' in parents and trashed=false"}).GetList()

        if file_list:
          # The file already exists, so just update it
          gdrive_file = file_list[0]
          gdrive_file.SetContentFile(filepath)
          gdrive_file.Upload()
        
        else:
          # The file doesn't exist, so create a new one
          gdrive_file = drive.CreateFile({'title': filename, 'parents': [{'id': gdrive_folder['id']}]})
          gdrive_file.SetContentFile(filepath)
          gdrive_file.Upload()

      # Delete files in Google Drive that don't exist in the local folder anymore
      for file in drive.ListFile({'q': f"'{gdrive_folder['id']}' in parents and trashed=false"}).GetList():
        if not os.path.exists(os.path.join(destination_path[:-1], file['title'])):
          file.Trash()

    # Choose if you want local backups to be uploaded to cloud (type: boolean)
    if config['backup_to_cloud'] != "off":
      # Upload the local folder and its content
      backup_to_cloud(destination_path[:-1], parent_folder_id=gdrive_folder['id'])
    
    self.backup_button.configure(state="normal")  # Change backup button state back to normal
    
    self.backup_completed_notification()

  def restore_backup(self):
    restore_window = tk.Toplevel(self)  # Open new window (restore_window)
    restore_window.title("Select backup to restore")  # Set window title
    restore_window.geometry("440x240")  # Set window size
    restore_window.iconbitmap("assets/icon.ico")  # Set window title icon
    restore_window.resizable(False, False)  # Disable minimize/maximize buttons
    restore_window.configure(background="#242424")  # Set background color

    frame = ctk.CTkFrame(master=restore_window, corner_radius=10, height=180, width=425)
    frame.place(x=8, y=8)

    # create listbox object
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

    counter = 1
    for zip_file in os.listdir(destination_path):
      filename, _,filetype = zip_file.partition('.')

      if filetype == 'zip':  
        listbox.insert(counter, zip_file.replace('.zip', ''))
        counter += 1

    def selected_item():
      self.restore_button.configure(state="disabled")  # Change backup button state to disabled

      for i in listbox.curselection():
        # Open the zipfile in read mode, extract its content
        with zipfile.ZipFile(f'{destination_path}{listbox.get(i)}.zip', mode='r') as zipObj:
          zipObj.extractall(config['destination_path'])

      self.restore_completed_notification()
      self.restore_button.configure(state="normal")  # Change backup button state back to normal

    def run_restore():
      threading.Thread(target=selected_item).start()  # Create new thread

    self.restore_button = ctk.CTkButton(master=restore_window, text="Restore backup", command=run_restore)
    self.restore_button.place(x=150, y=197)

  def start_function(self):
    self.is_running = True
    self.run_function()

  def run_function(self):
    if self.is_running:
      threading.Thread(target=self.start_progress_bar).start()  # Create new thread

  is_running = False

  # Set progress bar
  def start_progress_bar(self):
    self.backup_progressbar.start()
    self.backup()
    self.backup_progressbar.stop()

  # Backup from taskbar
  def backup_from_taskbar(self, icon):
    icon.stop()
    self.backup()
    self.hide_window()

  # Show window
  def show_window(self, icon):
    icon.stop()
    self.after(0, self.deiconify())

  # Quit window
  def quit_window(self, icon):
    icon.stop()
    self.destroy()

  # Hide window and show system taskbar
  def hide_window(self):
    self.withdraw()
    image = Image.open("assets/icon.ico")
    menu = item('Backup Now', self.backup_from_taskbar), item('Open', self.show_window), item('Exit', self.quit_window)
    self.icon = pystray.Icon("name", image, "SafeArchive", menu)
    self.icon.run()

if __name__ == "__main__":
  app = App()
  app.mainloop()
