
<!---------------------------------[ Header ]---------------------------------->

<h1 align = 'center'>
    <img 
        src = '/assets/icon.ico' 
        height = '100' 
        width = '100' 
        alt = 'Icon' 
    />
    <br>
    SafeArchive
    <br>
</h1>

<!---------------------------------[ Badge ]---------------------------------->

<div align = 'center'>
    <a href = 'https://github.com/KafetzisThomas/SafeArchive/releases'>
        <img src = 'https://img.shields.io/github/v/release/KafetzisThomas/SafeArchive?include_prereleases&label=Latest%20Release'/>
    </a>
</div>

<br>

Allows you to backup your essential local files (+cloud support) quickly and schedule past backup deletions to optimize storage space.

**How to Download:** Click the "[Releases](https://github.com/KafetzisThomas/SafeArchive/releases)" link on the right, then on the latest release, under 'Assets' click to download the zip file. (You might have to click "Assets" to view the files for the release)

> * Linux Setup Instructions - not available yet
> * MacOS Setup Instructions - not available yet
> * (Windows installation not necessary if using exe file. But see how to set up API key for uploading your backups to the cloud [on this page](https://github.com/KafetzisThomas/SafeArchive/wiki/Obtaining-API-Key))

**Note:** No matter the settings, the program runs completely locally on your own machine using the API key and Google Cloud project you created yourself, so even as the program's creator I will never have access to your account.

* For the first run, I recommend you to exit the program after setting your preferences, so changes to be applied.

* I wrote this using Python 3.9 but it will probably work with earlier versions too.

## Features

* Zip (backup) source path files to destination path
    * Compression method: ZIP_DEFLATED
    * allowZip64 is set to True (this parameter use the ZIP64 extensions when the zip file is larger than 4gb)
    * Compresslevel is set to 9 (its sometimes really slow when source path files are too large, saves storage space)
* Set expiry date for old backups
* Get backup size
* Added cloud support (Google Drive)
* Separate backup process from the main one (GUI) by creating a new thread to prevent script crash
* Add system tray icon to hide the main window instead of terminating it when clicking the X button upper-right. Specifically, a taskbar icon appears with options to backup your files from anywhere without opening the GUI window, open the GUI window and exit the script
* Restore past backups to their original location
* Pop up system notifications when backup process completes, selected backup restored successfully and drive hasn't reconnected for too long.

## Manual Setup
1. Download or clone the repo and install the requirements using:

    ```py
    $ pip install -r requirements.txt
    ```

2. How to Run:

    ```py
    $ python3 main.py
    ```

## Screenshots

<div align = 'center'>
    <h2>Software Startup<br>(Drive Properties, Backup Options)</h2>
    <br>
    <img
        alt = 'Software Startup (Drive Properties, Backup Options)' 
        src = 'https://user-images.githubusercontent.com/105563667/236015929-cf0020ad-4cab-425a-8a87-26e6668d2d65.png'>
    <br>
    <h2>Restore Selected Backup</h2>
    <br>
    <img
        alt = 'Restore Selected Backup' 
        src = 'https://user-images.githubusercontent.com/105563667/236017273-263abe17-26de-4c22-ba2d-f6be8d3dad18.png'>
    <br>
    <h2>System Tray Icon<br>(Taskbar Icon)</h2>
    <br>
    <img
        alt = 'System Tray Icon (Taskbar Icon)'
        src = 'https://user-images.githubusercontent.com/105563667/236020690-da79fd52-fce6-4266-8d66-e0ad3a8d2583.png'>
    <br>
</div>

<br>

## Obtaining API Key

To upload your backups to your cloud account (Google Drive), you will need an "Oauth2" credential to make the GUI switch to work.

* **Instructions can be found on this page: [Obtaining API Key](https://github.com/KafetzisThomas/SafeArchive/wiki/Obtaining-API-Key)**