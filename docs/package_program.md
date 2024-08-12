If you need to package the program yourself, follow these steps:

1. Clone the repo and install the requirements using:

    `$ pip install -r requirements.txt`

3. Package the program:

    ## Windows:

    ```
    pyinstaller --icon=assets\ICO\icon.ico --noconfirm --onedir --windowed --hidden-import plyer.platforms.win.notification --add-data "
    <fullpath>/site-packages/customtkinter;customtkinter/" "main.py"
    ```

    ## Linux/macOS:

    ```
    pyinstaller --noconfirm --onedir --hidden-import plyer.platforms.linux --hidden-import plyer.platforms.linux.notification --hidden- 
    import='PIL._tkinter_finder' --add-data "<fullpath>/site-packages/customtkinter:customtkinter/" "main.py"
    ```

**Note**: Remember to replace <**fullpath**> with the appropriate path where Python is installed on your system.
