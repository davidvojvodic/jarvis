import os
import gspread
from dotenv import load_dotenv
from utils_auth import get_credentials

load_dotenv()

def reset_sheet():
    sheet_id = os.getenv("GOOGLE_SHEET_ID_SOCIAL")
    if not sheet_id:
        print("❌ GOOGLE_SHEET_ID_SOCIAL not set.")
        return

    print(f"Resetting Sheet ID: {sheet_id}")
    
    try:
        creds = get_credentials()
        client = gspread.authorize(creds)
        sh = client.open_by_key(sheet_id)
        ws = sh.sheet1
        
        print("Clearing worksheet...")
        ws.clear()
        ws.resize(cols=8)
        
        print("Setting Headers...")
        headers = ["Topic", "Format", "Status", "Date", "Context/Notes", "Visual Prompt", "Caption", "Visual Path"]
        ws.append_row(headers)
        
        # Format headers (bold)
        ws.format('A1:H1', {'textFormat': {'bold': True}})
        
        print("✅ Sheet reset successfully (Headers restored).")
        
    except Exception as e:
        print(f"Error resetting sheet: {e}")

if __name__ == "__main__":
    reset_sheet()
