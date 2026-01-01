"""
Social Media Orchestrator.
Runs the full pipeline: Plan -> Generate -> Update.
Authentication: OAuth (via utils_auth).
"""
import os
import argparse
import subprocess
import sys
import gspread
from dotenv import load_dotenv

# Import shared auth
from utils_auth import get_credentials

load_dotenv()

def run_script(script_name, args=None):
    """Runs a python script from the execution directory."""
    cmd = [sys.executable, f"execution/{script_name}"]
    if args:
        cmd.extend(args)
    
    print(f"--- Running {script_name} ---")
    try:
        subprocess.check_call(cmd)
        print(f"--- {script_name} Completed ---\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}: {e}")
        return False

def main():
    while True:
        print("\n=== JARVIS SOCIAL ORCHESTRATOR ===")
        print("1. Plan New Content (Add to Schedule)")
        print("2. Generate Assets (Process 'Pending' items)")
        print("3. Exit")
        
        choice = input("\nSelect an option (1-3): ").strip()
        
        if choice == "1":
            print("\n>>> STARTING PLANNING PHASE")
            run_script("plan_content.py")
            print("\n--- Auto-Formatting Sheet ---")
            run_script("format_social_sheet.py")
            input("\nPress Enter to return to menu...")
            
        elif choice == "2":
            print("\n>>> STARTING GENERATION PHASE")
            print("IMPORTANT: Ensure you have reviewed and approved the 'Proposed' rows in the Google Sheet.")
            confirm_gen = input("Type 'generate' to proceed with asset generation for strictly 'Pending' items: ").strip().lower()
            if confirm_gen != 'generate':
                print("Generation cancelled.")
                continue
            
            # --- GENERATION LOGIC ---
            from utils_drive import get_or_create_folder, upload_file
            import generate_captions
            import generate_visuals
            
            asset_folder_id = get_or_create_folder("Jarvis Social Assets")
            if not asset_folder_id:
                print("Failed to access Drive folder. proceeding with local storage only.")
            
            creds = get_credentials()
            if not creds:
                print("Auth failed.")
                return

            client = gspread.authorize(creds)
            sheet_id = os.getenv("GOOGLE_SHEET_ID_SOCIAL")
            sh = client.open_by_key(sheet_id)
            ws = sh.sheet1
            
            all_rows = ws.get_all_values()
            if not all_rows:
                print("Sheet is empty.")
                continue

            # Headers
            headers = all_rows[0][:8]
            records = []
            for r in all_rows[1:]:
                r_padded = r + [""] * (8 - len(r))
                records.append(dict(zip(headers, r_padded[:8])))

            pending_count = 0
            for i, row in enumerate(records):
                if row.get("Status") == "Pending":
                    pending_count += 1
                    row_num = i + 2
                    topic = row.get("Topic")
                    fmt = row.get("Format")
                    context = row.get("Context/Notes")
                    visual_prompt = row.get("Visual Prompt")
                    
                    print(f"\nProcessing Row {row_num}: {topic} ({fmt})")
                    
                    # 1. Caption
                    caption = generate_captions.generate_caption(topic, context, "Instagram")
                    
                    # 2. Visual
                    safe_topic = "".join(x for x in topic if x.isalnum() or x in " -_").strip()
                    output_filename = f".tmp/assets/{row['Date']}_{safe_topic}.png"
                    
                    # Use dedicated visual prompt if available, fallback to topic+context
                    prompt = visual_prompt if visual_prompt and len(visual_prompt) > 5 else f"{topic}. {context}"
                    print(f"Using Visual Prompt: '{prompt[:50]}...'")
                    
                    try:
                        if "Video" in fmt:
                            output_filename = output_filename.replace(".png", ".mp4")
                            generate_visuals.generate_video(prompt, output_filename)
                        else:
                            generate_visuals.generate_image(prompt, output_filename)
                            
                        # 3. Upload
                        drive_link = output_filename
                        if os.path.exists(output_filename):
                            print(f"Uploading {output_filename} to Drive (Folder ID: {asset_folder_id})...")
                            uploaded_link = upload_file(output_filename, asset_folder_id)
                            print(f"DEBUG: uploaded_link result: {uploaded_link}")
                            if uploaded_link:
                                drive_link = uploaded_link
                            else:
                                print("WARNING: Upload failed or returned None.")
                        else:
                             print(f"WARNING: File {output_filename} does not exist. Skipping upload.")
                    except Exception as e:
                        print(f"Generation Error: {e}")
                        continue

                    # 4. Update Sheet
                    if "Error" not in caption:
                        # Headers: Topic(1), Format(2), Status(3), Date(4), Context(5), Visual Prompt(6), Caption(7), Visual Path(8)
                        ws.update_cell(row_num, 7, caption) 
                        ws.update_cell(row_num, 8, drive_link)
                        ws.update_cell(row_num, 3, "Generated")
                        print(f"✅ Row {row_num} Complete!")
                    else:
                         ws.update_cell(row_num, 7, f"Error: {caption}")
            
            if pending_count == 0:
                print("No 'Pending' items found in the sheet.")
            
            input("\nGeneration Complete. Press Enter to return to menu...")

        elif choice == "3":
            print("Exiting...")
            sys.exit(0)
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
