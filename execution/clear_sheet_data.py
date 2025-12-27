
import os
import sys
import argparse
import gspread
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from dotenv import load_dotenv
import json

# Configure logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("clear_sheet")

# Load env vars
load_dotenv()

def get_credentials():
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    creds = None
    if os.path.exists('token.json'):
        with open('token.json', 'r') as token:
            token_data = json.load(token)
            creds = Credentials.from_authorized_user_info(token_data, scopes)
            
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds_file = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "credentials.json")
            flow = InstalledAppFlow.from_client_secrets_file(creds_file, scopes)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def main():
    parser = argparse.ArgumentParser(description="Clear all data from leads sheet (keep headers)")
    parser.add_argument("--sheet-url", default=os.getenv("LEADS_SHEET_URL"), help="Google Sheet URL")
    
    args = parser.parse_args()
    
    if not args.sheet_url:
        logger.error("No Sheet URL provided.")
        sys.exit(1)
        
    logger.info(f"Connecting to sheet: {args.sheet_url}")
    
    creds = get_credentials()
    client = gspread.authorize(creds)
    
    # Open sheet
    if '/d/' in args.sheet_url:
        sheet_key = args.sheet_url.split('/d/')[1].split('/')[0]
        spreadsheet = client.open_by_key(sheet_key)
    else:
        spreadsheet = client.open_by_url(args.sheet_url)
        
    worksheet = spreadsheet.sheet1
    
    # Get total rows
    total_rows = worksheet.row_count
    
    if total_rows > 1:
        logger.info(f"Clearing rows 2 to {total_rows}...")
        # Batch clear is efficient
        worksheet.batch_clear([f"A2:ZZ{total_rows}"])
        logger.info("✅ Sheet cleared. Headers preserved.")
    else:
        logger.info("Sheet is already empty (only headers or blank).")

if __name__ == "__main__":
    main()
