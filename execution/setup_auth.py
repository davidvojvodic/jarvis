"""
Setup Authentication for Vertex AI (Imagen/Veo).
Run this once to generate 'token_vertex.json'.
Uses 'credentials_vertex.json' (Specific to this app).
"""
import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

# Scopes needed for Vertex AI + Storage
SCOPES = [
    'https://www.googleapis.com/auth/cloud-platform',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

def authenticate():
    creds = None
    token_file = 'token.json'
    creds_file = 'credentials.json'
    
    
    # FORCE RE-AUTH: Always delete old token to ensure we switch projects/accounts
    if os.path.exists(token_file):
        print("Removing old token to force re-authentication...")
        os.remove(token_file)

    # Proceed to create new creds
    # (Old loading logic removed)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired token...")
            try:
                creds.refresh(Request())
            except Exception:
                print("Refresh failed. Re-authenticating.")
                creds = None
        
        if not creds:
            if not os.path.exists(creds_file):
                print(f"Error: '{creds_file}' not found. Please make sure you copied the JSON file correctly.")
                return

            print(f"Launching Browser for Authentication using {creds_file}...")
            flow = InstalledAppFlow.from_client_secrets_file(creds_file, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the token
        with open(token_file, 'w') as token:
            token.write(creds.to_json())
            print(f"Success! Token saved to {token_file}")

if __name__ == "__main__":
    authenticate()
