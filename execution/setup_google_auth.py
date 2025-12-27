import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Scopes required for the project (Sheets, Gmail, Drive, etc.)
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.readonly'
]

def main():
    """Shows basic usage of the People API.
    Prints the name of the first 10 connections.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                print("❌ ERROR: 'credentials.json' not found.")
                print("Please download your OAuth 2.0 Client IDs from Google Cloud Console")
                print("and save it as 'credentials.json' in this directory.")
                return

            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Output the JSON for the .env file
    print("\n✅ Authentication successful!")
    print("\nHere is your GOOGLE_TOKEN_JSON string for the .env file:")
    print("-" * 50)
    # We load it back to ensure it's minified string format
    print(creds.to_json())
    print("-" * 50)
    print("\nCopy everything between the dashed lines and paste it into your .env file as:")
    print("GOOGLE_TOKEN_JSON='<paste_here>'")

if __name__ == '__main__':
    main()
