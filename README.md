<h1 align="center">SafeArchive</h1>

Allows you to backup your essential local files (+cloud support) quickly and schedule past backup deletions to optimize storage space.

## Setup & Configuration
1. Download or clone the repo and install the requirements using:

    ```py
    $ pip install -r requirements.txt
    ```

2. How to Run:

    ```py
    $ python3 main.py
    ```

* I wrote this using Python 3.10 but it will probably work with earlier versions too.

## Authentication
1. Go to [Google APIs Console](https://console.cloud.google.com/) and make your own project.

2. Search for '**Google Drive API**', select the entry, and click '**Enable**'.

3. Select '**Credentials**' from the left menu, click '**Create Credentials**', select '**OAuth client ID**'.

4. Now, the product name and consent screen need to be set, so click '**Configure consent screen**' and follow the instructions. Once finished:

    * Select '**Application type**' to be Web application. Enter an appropriate name.

    * Input `http://localhost:8080/` for '**Authorized redirect URIs**' and click '**Create**'.

5. Click '**Download JSON**' on the right side of Client ID to download the file.

6. Rename the file to `client_secrets.json` and place it in the path that the script exists.
