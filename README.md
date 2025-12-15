<div align="center">
  <img src="/assets/logo.png" width="100" alt="Logo Icon"/>
  <h1>SafeArchive</h1>
  <p>Securely backup and manage your files locally and in the cloud.</p>
  <h3>
    <a href="https://github.com/KafetzisThomas/SafeArchive">Homepage</a> | 
    <a href="https://github.com/KafetzisThomas/SafeArchive/tree/main/docs">Docs</a> | 
    <a href="https://github.com/KafetzisThomas/SafeArchive/graphs/contributors">Contributors</a>
  </h3>
  <a href="https://github.com/KafetzisThomas/SafeArchive/releases">
    <img src="https://img.shields.io/github/v/release/KafetzisThomas/SafeArchive?include_prereleases&label=Latest%20Release"/>
  </a>
</div>

## Features

- [X] Backup files to your drive
- [X] Supported compression methods: `ZIP_DEFLATED`, `ZIP_STORED`, `ZIP_LZMA`, `ZIP_BZIP2`
- [X] Supported compression level range: **1-9**
- [X] ZIP64 support for backup larger than **4 GiB**
- [X] Automated backup expiry management
- [ ] Automatic backups in the background (beta)
- [X] Remote Backup: `FTP` (**NAS Support**)
- [X] Multi-threaded backup process
- [X] Command-line interface (CLI) support
- [X] Real-time system notifications
- [X] Backup **encryption** and **restoration**

**Supported platforms:** `Windows`, `Linux`, `macOS`

## Usage

```bash
git clone https://github.com/KafetzisThomas/SafeArchive.git
cd path/to/root/directory && pip install uv

# Run GUI
uv run main.py

# Run CLI
uv run main.py --nogui
```

**Note:** For the first run it's recommended to exit the program after setting your preferences so changes to be applied.

> **Tip**: Learn how to [package](https://github.com/KafetzisThomas/SafeArchive/blob/main/docs/package_program.md) it yourself!

## Setup for FTP Server

1. Enable the `FTP` switch within the application settings or set the `"ftp"` value to `true` in `settings.json`.

2. Configure your credentials (**hostname**, **username**, **password**) directly in `settings.json`.

## Demo Images

![Main Window](https://github.com/user-attachments/assets/6bd47490-dd3b-4b69-8854-1470f53e1904)

![Restore Backup Window](https://github.com/user-attachments/assets/6cd80527-d166-4a24-b383-79ba18c552c0)

![Settings Window](https://github.com/user-attachments/assets/6cefd88b-254d-480a-b0ef-6d86bbee225b)

## Contributing Guidelines

### Pull Requests

- **Simplicity**: Keep changes focused and easy to review.
- **Libraries**: Avoid adding non-standard libraries unless discussed via an issue.
- **Testing**: Ensure code runs error-free, passes all tests, and meets coding standards.

### Bug Reports

- Report bugs via GitHub Issues.
- Submit pull requests via GitHub Pull Requests.

Thank you for supporting SafeArchive!
