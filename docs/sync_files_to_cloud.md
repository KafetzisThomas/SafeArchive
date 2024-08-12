# [Option 1] Set Up For Google Drive

To sync your backups to your Google Drive, you will need an "Oauth2" credential.

1. Go to [Google APIs Console](https://console.cloud.google.com/) and make your own project

2. Search for **Google Drive API**, select the entry, and click **Enable**

3. Select **Credentials** from the left menu, click **Create Credentials**, select **OAuth client ID**

4. Now, the product name and consent screen need to be set, so click **Configure consent screen** and follow the instructions. Once finished:
    * Select **Application type** to be Web application. Enter an appropriate name
    * Input `http://localhost:8080/` for **Authorized redirect URIs** and click **Create**

5. Click **Download JSON** on the right side of Client ID to download the file

6. Rename the file to `client_secrets.json` and place it in the path that the script exists

7. Select **Google Drive** as the storage provider or set the corresponding JSON value


# [Option 2] Set Up For Dropbox

To sync your backups to your Dropbox, you will need an access token.

1. Visit the [Dropbox Developer Console](https://dropbox.com/developers/apps) and make your own app

2. Choose **Scoped access** and **App folder** access

3. Give your app a descriptive name

4. Navigate to the **Permissions** tab and enable the following permissions:
    * files.metadata.write
    * files.metadata.read
    * files.content.write
    * files.content.read
5. Click **Generate** to create an access token

6. Grab token and paste it to the **'dropbox_access_token'** field (within settings.json)

7. Select **Dropbox** as the storage provider or set the corresponding JSON value

# [Option 3] Set Up For FTP Server

1. Select **FTP** as the storage provider or set the corresponding JSON value

2. Edit the configuration file (settings.json) and add your FTP server **hostname**, **username** and **password** to the corresponding JSON keys ~~**(for enhanced security, option to set credentials as environment variables will be implemented)**~~ --> The JSON file serves the exact same security measures as environment variables would for the purpose of this script.
