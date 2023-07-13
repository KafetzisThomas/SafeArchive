#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
This file allows you to sync your files with Google Drive.
It allows uploading, updating, and deleting files in a specified folder on Google Drive.
Note: This feature becomes optional in the program. If you want to use it, just turn the cloud switch on.
Follow instructions to get your Oauth2 credential key:
https://github.com/KafetzisThomas/SafeArchive/wiki/Obtaining-API-Key
"""

import os
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import Scripts.configs as configs
configs.config.load() # Load the JSON file into memory

DESTINATION_PATH = configs.config['destination_path'] + 'SafeArchive/'  # Get value from the JSON file

def initialize():
  """Authenticate request & store authorization credentials"""
  global drive, gdrive_folder

  gauth = GoogleAuth()  # Create a GoogleAuth instance

  gauth.LoadCredentialsFile('credentials.txt')  # Load the stored OAuth2 credential

  # Check if stored credential is valid
  if not gauth.credentials:
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

def get_cloud_usage_percentage():
  """Return cloud usage percentage"""
  account_details = drive.GetAbout()  # Get account details

  # Calculate storage usage percentage
  used_storage = int(account_details['quotaBytesUsed'])
  total_storage = int(account_details['quotaBytesTotal'])
  storage_usage_percentage = (used_storage / total_storage) * 100
  return storage_usage_percentage

def backup_to_cloud(folderpath, parent_folder_id=None):
  """
  Upload local backup files to cloud (google drive)
    * Delete files that have been locally removed
    * Upload files that have been added locally
    * Update existing files with new content
  """
  foldername = os.path.basename(folderpath)
  folder_metadata = {'title': foldername, 'mimeType': 'application/vnd.google-apps.folder'}

  if parent_folder_id:
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
    if not os.path.exists(os.path.join(DESTINATION_PATH[:-1], file['title'])):
      file.Trash()
