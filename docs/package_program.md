If you need to package the program yourself, follow these steps:

1. Clone the repo, navigate to the local folder **GUI** and install the requirements using:

   `$ pip install -r requirements.txt`

   **NOTE:** Ensure you have Python 3.10 installed or set up a virtual environment specifically for that version:

   `$ python3.10 -m venv "env_name"`

3. Package the program:

   ## Windows:

   ```
    pyinstaller --icon=assets\icon.ico --noconfirm --onedir --windowed --hidden-import plyer.platforms.win.notification --add-data " 
    <fullpath>/site-packages/customtkinter;customtkinter/" "main.py"
    ```

   ## Linux:

   Debian: 

   ```
   pyinstaller --noconfirm --onedir --hidden-import plyer.platforms.linux --hidden-import plyer.platforms.linux.notification --hidden- 
   import='PIL._tkinter_finder' --add-data "<fullpath>/site-packages/customtkinter:customtkinter/" "main.py"
   ```

    RPM:

    ```
    pyinstaller --noconfirm --onedir --hidden-import plyer.platforms.linux --hidden-import plyer.platforms.linux.notification --hidden- 
    import='PIL._tkinter_finder' --add-data "<fullpath>/site-packages/customtkinter:customtkinter/" "main.py"
    ```

**Note**: Remember to replace <**fullpath**> with the appropriate path where Python is installed on your computer.
