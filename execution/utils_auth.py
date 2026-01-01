"""
Shared Authentication Utility for Vertex AI.
Loads the 'token_vertex.json' (OAuth) and initializes Vertex AI.
"""
import os
import json
from dotenv import load_dotenv
import vertexai
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

load_dotenv()

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

TOKEN_FILE = 'token.json'
CREDS_FILE = 'credentials.json'
SCOPES = [
    'https://www.googleapis.com/auth/cloud-platform',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

def get_credentials():
    """Loads valid user credentials from token file."""
    creds = None
    
    if os.path.exists(TOKEN_FILE):
        try:
            with open(TOKEN_FILE, 'r') as token:
                token_data = json.load(token)
                creds = Credentials.from_authorized_user_info(token_data, SCOPES)
        except Exception as e:
            print(f"Error loading token: {e}")

    # Refresh if expired
    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            # Save refreshed token
            with open(TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())
        except Exception as e:
            print(f"Error refreshing token: {e}")
            creds = None
            
    return creds

def init_vertex():
    """Initializes Vertex AI SDK with User Credentials."""
    if not PROJECT_ID:
        raise ValueError("GOOGLE_CLOUD_PROJECT not set in .env")

    creds = get_credentials()
    if not creds:
        raise RuntimeError(
            "No valid credentials found. Please run 'python execution/setup_auth.py' first."
        )
    
    vertexai.init(project=PROJECT_ID, location=LOCATION, credentials=creds)
    return True
