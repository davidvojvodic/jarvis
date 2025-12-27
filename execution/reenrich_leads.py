
import os
import sys
import argparse
import time
import logging
import gspread
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from dotenv import load_dotenv
import json

# Import our new AI extractor
from extract_website_contacts import scrape_website_contacts

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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

def update_sheet_row(worksheet, row_index, ai_data):
    """
    Update specific columns in a row with AI data.
    """
    try:
        # Map our JSON keys to Sheet Headers (approximate)
        # We need to find column numbers for headers first
        headers = worksheet.row_values(1)
        
        updates = []
        
        # Helper to find col index (1-based)
        def get_col_idx(name):
            try:
                return headers.index(name) + 1
            except ValueError:
                return None

        # Data mapping: (Sheet Header, AI Data Value)
        fields_to_update = []
        
        if ai_data.get("owner_info"):
            owner = ai_data["owner_info"]
            fields_to_update.append(("owner_name", owner.get("name", "")))
            fields_to_update.append(("owner_title", owner.get("title", "")))
            fields_to_update.append(("owner_email", owner.get("email", "")))
            fields_to_update.append(("owner_phone", owner.get("phone", "")))
            fields_to_update.append(("owner_linkedin", owner.get("linkedin", "")))
            
        if ai_data.get("team_members"):
            fields_to_update.append(("team_contacts", json.dumps(ai_data["team_members"])))
            
        # Update emails if found
        if ai_data.get("emails"):
            # We should probably merge with existing, but for now let's just write what AI found + what was there?
            # actually, let's just update the 'emails' column with the FULL list from AI (which includes regex backup)
            fields_to_update.append(("emails", ", ".join(ai_data["emails"])))
            
        # Update status
        fields_to_update.append(("enrichment_status", "ai_enriched"))
            
        # Socials merge
        if ai_data.get("social_media"):
             # We might need to handle per-column socials if they exist in sheet
            pass 

        # Execute updates
        for header, value in fields_to_update:
            col_idx = get_col_idx(header)
            if col_idx and value:
                worksheet.update_cell(row_index, col_idx, str(value))
                time.sleep(0.5) # Rate limit safety
                
        return True
    except Exception as e:
        logger.error(f"Error updating row {row_index}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Re-enrich existing leads with AI")
    parser.add_argument("--sheet-url", default=os.getenv("LEADS_SHEET_URL"), help="Google Sheet URL")
    
    args = parser.parse_args()
    
    if not args.sheet_url:
        logger.error("No Sheet URL provided. Set LEADS_SHEET_URL or pass --sheet-url")
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
    all_records = worksheet.get_all_records()
    
    logger.info(f"Found {len(all_records)} leads. Checking for candidates to re-enrich...")
    
    updated_count = 0
    
    # Iterate (1-based index, so start at 2)
    for i, record in enumerate(all_records):
        row_num = i + 2 
        website = record.get("website", "")
        owner_name = record.get("owner_name", "")
        business_name = record.get("business_name", "")
        
        # Criteria: Has website BUT No Owner Name
        if website and not owner_name:
            logger.info(f"Processing row {row_num}: {business_name} ({website})")
            
            # Run AI Scraper
            try:
                data = scrape_website_contacts(website, business_name)
                
                # If AI found something useful (Owner or Team), write it back
                if data.get("owner_info") or data.get("team_members"):
                    update_sheet_row(worksheet, row_num, data)
                    logger.info(f"✅ Updated {business_name} with AI data")
                    updated_count += 1
                else:
                    logger.info(f"⚠️ AI found no new owner info for {business_name}")
                    
            except Exception as e:
                logger.error(f"Failed to process {business_name}: {e}")
            
            # Rate limiting for stability
            time.sleep(2)
            
    logger.info(f"Complete! Updated {updated_count} leads.")

if __name__ == "__main__":
    main()
