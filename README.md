<div align="center">
    <h1>
        <img 
            src="/assets/ICO/icon.ico" 
            height="100" 
            width="100" 
            alt="Icon" 
        />
        <div>SafeArchive</div>
    </h1>
    <p>Securely backup and manage your files locally and in the cloud (Windows, macOS, Linux - desktop, server)</p>
    <h3>
        <a href="https://github.com/KafetzisThomas/SafeArchive">Homepage</a> | 
        <a href="https://github.com/KafetzisThomas/SafeArchive/wiki">Wiki</a> | 
        <a href="https://github.com/KafetzisThomas/SafeArchive/graphs/contributors">Contributors</a>
    </h3>
    <a href="https://github.com/KafetzisThomas/SafeArchive/releases">
        <img src = 'https://img.shields.io/github/v/release/KafetzisThomas/SafeArchive?include_prereleases&label=Latest%20Release'/>
    </a>
</div>

---

**How to Download:** Click the "[Releases](https://github.com/KafetzisThomas/SafeArchive/releases)" link on the right, then on the latest release, under 'Assets' click to download the zip file. (You might have to click "Assets" to view the files for the release)

> * [Server Instructions](https://github.com/KafetzisThomas/SafeArchive/wiki/Server-Instructions)
> * Windows/Linux installation not necessary if using executable file.

**Note:** No matter the settings, the program runs completely locally on your own machine using the API key and Google Cloud project you created yourself, so even as the program's creator I will never have access to your account.

* For the first run, I recommend you to exit the program after setting your preferences, so changes to be applied.

## Features

* Backup Compression (ZIP_DEFLATED, ZIP64, compression level: 9)
* Automated Backup Expiry Management
* Cloud Integration (Google Drive, MEGA, Dropbox, FTP)
* Multi-threaded Backup Process
* Command-Line Interface (CLI) Support
* System Tray Integration
* System Notifications
* Backup Restoration
* Backup Encryption

## Manual Setup

1. Ensure you have Python 3.10 installed or set up a virtual environment specifically for that version:

    ```py
    $ python3.10 -m venv "env_name"
    ```

2. Download or clone the repo and install the requirements using:

    ```py
    $ pip install -r requirements.txt
    ```

3. How to Run:

    ```py
    $ python3 main.py
    ```

## Screenshots

<div align = 'center'>
    <h2>Software Startup<br>(Drive Properties, Backup Options)</h2>
    <br>
    <img
        alt = 'Software Startup (Drive Properties, Backup Options)' 
        src = 'https://github.com/KafetzisThomas/SafeArchive/assets/105563667/3361483c-876c-4e08-911f-413233739bec'>
    <br>
    <h2>Restore Selected Backup</h2>
    <br>
    <img
        alt = 'Restore Selected Backup' 
        src = 'https://github.com/KafetzisThomas/SafeArchive/assets/105563667/cee02400-6b7d-482d-a871-4c7e0ba3853a'>
    <br>
    <h2>Settings Window</h2>
    <br>
    <img
        alt = 'Settings Window'
        src = 'https://github.com/KafetzisThomas/SafeArchive/assets/105563667/2c1a016c-8b80-42e9-a10e-50c933627f87'>
    <br>
    <h2>System Tray Icon<br>(Taskbar Icon)</h2>
    <br>
    <img
        alt = 'System Tray Icon (Taskbar Icon)'
        src = 'https://user-images.githubusercontent.com/105563667/236020690-da79fd52-fce6-4266-8d66-e0ad3a8d2583.png'>
    <br>
</div>

<br>

## Getting Help

If you find a bug, please see [CONTRIBUTING.md](https://github.com/KafetzisThomas/SafeArchive/blob/main/CONTRIBUTING.md) for information on how to report it.

## License

SafeArchive is distributed under the GPL-3.0 license, please see [LICENSE](https://github.com/KafetzisThomas/SafeArchive/blob/main/LICENSE) for more information.
