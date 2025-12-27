# How to Get Google Cloud Credentials (`credentials.json`)

## 1. Create a Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Click the project dropdown (top left) > **New Project**.
3. Name it "Jarvis Automation" and click **Create**.

## 2. Enable APIs
1. Select your new project.
2. Go to **APIs & Services** > **Library**.
3. Search for and **Enable** the following APIs:
   - **Google Sheets API**
   - **Google Drive API**
   - **Gmail API**

## 3. Configure OAuth Consent Screen
1. Go to **APIs & Services** > **OAuth consent screen**.
2. Select **External** (if you don't have a Workspace org) or **Internal**. Click **Create**.
3. Fill in:
   - **App Name**: Jarvis
   - **User Support Email**: Your email
   - **Developer Contact Info**: Your email
4. Click **Save and Continue**.
5. **Scopes**: Click **Add or Remove Scopes**. Select scopes for Sheets, Drive, and Gmail. (Or just skip, we can force it later).
6. **Test Users**: Add your own email address (`david...`). **Crucial step for External apps**.

## 4. Create Credentials
1. Go to **APIs & Services** > **Credentials**.
2. Click **+ CREATE CREDENTIALS** > **OAuth client ID**.
3. **Application type**: Desktop app.
4. **Name**: "Jarvis Desktop".
5. Click **Create**.

## 5. Download JSON
1. You'll see "OAuth client created".
2. Click the **Download JSON** button (icon with down arrow).
3. **Rename** the downloaded file to `credentials.json`.
4. **Move** it to your project folder: `C:\Users\david\jarvis\credentials.json`.

## 6. Run Setup
Now you can run the setup script:
```powershell
python execution/setup_google_auth.py
```
