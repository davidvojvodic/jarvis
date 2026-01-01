import os
import gspread
from dotenv import load_dotenv
from utils_auth import get_credentials

load_dotenv()

def format_sheet():
    sheet_id = os.getenv("GOOGLE_SHEET_ID_SOCIAL")
    if not sheet_id:
        print("❌ GOOGLE_SHEET_ID_SOCIAL not set.")
        return

    print(f"Formatting Sheet ID: {sheet_id}")
    
    try:
        creds = get_credentials()
        client = gspread.authorize(creds)
        sh = client.open_by_key(sheet_id)
        ws = sh.sheet1
        
        # 1. Unfreeze panes (or just freeze header)
        # set_frozen(rows=1, cols=0) -> Freeze top row, no columns
        ws.freeze(rows=1, cols=0)
        print("Frozen panes updated (Row 1 frozen, Cols unfrozen).")

        # 2. Text Wrapping & Vertical Alignment
        # Apply to Data Range (A2:G1000)
        # A: Topic, B: Format, C: Status, D: Date, E: Context, F: Caption, G: Visual
        
        # We want everything wrapped and top-aligned
        ranges = ['A1:G100'] 
        
        format_body = {
            "wrapStrategy": "WRAP",
            "verticalAlignment": "TOP", 
            "textFormat": {
                "fontFamily": "Arial",
                "fontSize": 10
            }
        }
        ws.format('A2:G200', format_body)
        print("Text wrapping and alignment applied.")
        
        # 3. Column Sizing
        # set_column_width(col_index, width)
        # A (Topic): 200, B(Format): 100, C(Status): 80, D(Date): 100
        # E (Context): 300 (Needs more space), F(Caption): 300, G(Visual): 150
        
        # ws.set_column_width(0, 200) # Removed invalid call
        # Using batch_update for resizing instead
        # gspread set_column_width usually takes (col, width). It is 1-based index usually? No, let's verify.
        # recent gspread versions: worksheet.set_column_width(col, width)
        # Actually standard gspread: update_cells or format.
        # But there IS a 'set_column_width' in recent versions but sometimes it's 'set_col_width'.
        # Let's use the batch update for column resizing if possible, or individual calls.
        # Let's assume standard 1-based index for columns.
        
        requests = [
            {"updateDimensionProperties": {"range": {"sheetId": ws.id, "dimension": "COLUMNS", "startIndex": 0, "endIndex": 1}, "properties": {"pixelSize": 200}, "fields": "pixelSize"}}, # A Topic
            {"updateDimensionProperties": {"range": {"sheetId": ws.id, "dimension": "COLUMNS", "startIndex": 1, "endIndex": 2}, "properties": {"pixelSize": 120}, "fields": "pixelSize"}}, # B Format
            {"updateDimensionProperties": {"range": {"sheetId": ws.id, "dimension": "COLUMNS", "startIndex": 2, "endIndex": 3}, "properties": {"pixelSize": 100}, "fields": "pixelSize"}}, # C Status
            {"updateDimensionProperties": {"range": {"sheetId": ws.id, "dimension": "COLUMNS", "startIndex": 3, "endIndex": 4}, "properties": {"pixelSize": 100}, "fields": "pixelSize"}}, # D Date
            {"updateDimensionProperties": {"range": {"sheetId": ws.id, "dimension": "COLUMNS", "startIndex": 4, "endIndex": 5}, "properties": {"pixelSize": 400}, "fields": "pixelSize"}}, # E Context (Wide)
            {"updateDimensionProperties": {"range": {"sheetId": ws.id, "dimension": "COLUMNS", "startIndex": 5, "endIndex": 6}, "properties": {"pixelSize": 400}, "fields": "pixelSize"}}, # F Caption (Wide)
            {"updateDimensionProperties": {"range": {"sheetId": ws.id, "dimension": "COLUMNS", "startIndex": 6, "endIndex": 7}, "properties": {"pixelSize": 200}, "fields": "pixelSize"}}, # G Visual
        ]
        sh.batch_update({"requests": requests})
        print("Column widths resized.")
        
        print("✅ Sheet formatting complete.")

    except Exception as e:
        print(f"Error formatting sheet: {e}")

if __name__ == "__main__":
    format_sheet()
