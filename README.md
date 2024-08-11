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
    <p>Securely backup and manage your files locally and in the cloud.</p>
    <h3>
        <a href="https://github.com/KafetzisThomas/SafeArchive">Homepage</a> | 
        <a href="https://github.com/KafetzisThomas/SafeArchive/tree/main/docs">Docs</a> | 
        <a href="https://github.com/KafetzisThomas/SafeArchive/graphs/contributors">Contributors</a>
    </h3>
    <a href="https://github.com/KafetzisThomas/SafeArchive/releases">
        <img src = 'https://img.shields.io/github/v/release/KafetzisThomas/SafeArchive?include_prereleases&label=Latest%20Release'/>
    </a>
</div>

---

**Supported platforms**: `Windows`, `Linux`, `macOS`

## Features

- [X] Backup files to your drive
- [X] Supported compression methods: `ZIP_DEFLATED`, `ZIP_STORED`, `ZIP_LZMA`, `ZIP_BZIP2`
- [X] Supported compression level range: **1-9**
- [X] ZIP64 Support for backup larger than **4 GiB**
- [X] Automated Backup Expiry Management
- [ ] Automatic Backups in the background (beta)
- [X] Cloud Integration
    * Google Drive
    * Dropbox
    * FTP
- [X] Multi-threaded Backup Process
- [X] Command-Line Interface (CLI) Support
- [X] Real-time system notifications
- [X] Backup Encryption & Restoration

## Setup

1. **Download or clone the repository**

    First, download or clone the repository to your local machine:

    ```sh
    $ git clone https://github.com/KafetzisThomas/SafeArchive.git
    ```

2. **Install dependencies**

    Navigate to the project directory and install the required python packages:

    ```sh
    $ pip install -r requirements.txt
    ```

3. **Run the application**

    - **With GUI**: To run the application with the graphical user interface (GUI), use:

      ```sh
      $ python3 main.py
      ```

    - **Without GUI**: To run the application without the GUI (CLI mode), use the `--nogui` option:

      ```sh
      $ python3 main.py --nogui
      ```

      This will start the application in command-line interface mode, bypassing the GUI components.

**Note:** For the first run, I recommend you to exit the program after setting your preferences, so changes to be applied.

> **Tip**: Learn how to [package](https://github.com/KafetzisThomas/SafeArchive/blob/main/docs/package_program.md) it yourself!

## Screenshots

<div align = 'center'>
    <br>
    <img
        height = '353'
        alt = 'Main Window - blue'
        src = 'https://github.com/user-attachments/assets/6bd47490-dd3b-4b69-8854-1470f53e1904'>
    <hr>
    <img
        height = '353'
        alt = 'Main Window - green'
        src = 'https://github.com/user-attachments/assets/67ea5f0d-387e-4e5f-ae26-064783f269bb'>
    <hr>
    <img
        height = '353'
        alt = 'Restore Backup Window' 
        src = 'https://github.com/user-attachments/assets/6cd80527-d166-4a24-b383-79ba18c552c0'>
    <hr>
    <img
        height = '353'
        alt = 'Settings Window'
        src = 'https://github.com/user-attachments/assets/6cefd88b-254d-480a-b0ef-6d86bbee225b'>
    <br>
</div>

<br>

## Getting Help

If you find a bug, please see [CONTRIBUTING.md](https://github.com/KafetzisThomas/SafeArchive/blob/main/CONTRIBUTING.md) for information on how to report it.

## License

SafeArchive is distributed under the GPL-3.0 license, please see [LICENSE](https://github.com/KafetzisThomas/SafeArchive/blob/main/LICENSE) for more information.
