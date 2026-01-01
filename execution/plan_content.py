"""
Strategic Content Planner.
Acts as a Social Media Marketing Specialist to populate the content calendar.
Authentication: OAuth (Vertex AI).
"""
import os
import json
import warnings
from datetime import datetime, timedelta
import gspread
from dotenv import load_dotenv
from vertexai.generative_models import GenerativeModel

# Import shared auth
from utils_auth import init_vertex, get_credentials

from utils_auth import init_vertex, get_credentials

load_dotenv()

def get_last_date(worksheet):
    try:
        dates = worksheet.col_values(4)
        if len(dates) <= 1: 
            return datetime.now().date()
        last_date_str = dates[-1]
        return datetime.strptime(last_date_str, "%Y-%m-%d").date()
    except Exception:
        return datetime.now().date()

from utils_genai import get_client
from google import genai
from google.genai import types

def generate_plan(start_date, days=7):
    """Uses Gemini 2.0 via Google Gen AI SDK."""
    print("Initializing Google Gen AI Client...")
    try:
        client = get_client()
    except Exception as e:
        print(f"Auth Error: {e}")
        return []
        
    # Load Config
    try:
        with open('social_config.json', 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("Warning: social_config.json not found. Using defaults.")
        config = {
            "niche": "AI Automation",
            "target_audience": "Business Owners",
            "content_pillars": ["Education", "Case Study"],
            "tone": "Professional"
        }


    print(f"DEBUG: start_date type: {type(start_date)}")
    print(f"DEBUG: config pillars type: {type(config.get('content_pillars'))}")
    
    prompt = f"""
    Act as a Senior Social Media Strategist for a {config['niche']} Agency.
    Target Audience: {config['target_audience']}.
    
    Create a {days}-day content plan starting from {start_date + timedelta(days=1)}.
    
    Themes/Pillars: {', '.join(config['content_pillars'])}.
    Primary Platforms: {', '.join(config['platforms'])}.
    Tone: {config['tone']}.
    
    IMPORTANT RESTRICTIONS:
    - ONLY generate content for these platforms: {', '.join(config['platforms'])}.
    - Do NOT generate LinkedIn Articles if 'LinkedIn' is not in the platform list.
    - Suggested Formats: Carousel, Reel/Short Video, Single Image Post.
    
    Goal: Demonstrate expertise, solve pain points, generate inbound leads.
    
    Output Format: JSON Array of objects.
    STRICT REQUIREMENT: 
    - 'context' field is MANDATORY (2-3 sentences for caption context).
    - 'visual_prompt' field is MANDATORY. 
      * Description: "Visual description ONLY. Concise, high-quality, photorealistic style keywords. No text overlays description. Max 20 words."
      * Example: "Modern office desk, macbook, coffee cup, blurred background, warm lighting, 4k."
    
    Example:
    [
      {{
        "topic": "3 Cold Email Mistakes",
        "format": "Carousel Post",
        "context": "Explain why generic subject lines fail. Discuss the importance of personalization beyond just the name. Highlight call-to-action errors.",
        "visual_prompt": "Frustrated office worker looking at laptop, cluttered desk, cinematic lighting, realistic."
      }}
    ]
    """
    
    print(f"\nDrafting content plan (Model: gemini-3-flash-preview)...")
    
    # Use API Key for Gemini 3 Access (Bypasses Vertex AI restriction)
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        from google import genai
        # Initialize client specifically for AI Studio
        client = genai.Client(api_key=api_key, http_options={'api_version': 'v1alpha'})
    else:
        print("WARNING: GEMINI_API_KEY not found. Fallback to Vertex AI Client.")

    try:
        context_input = input("Enter specific context or focus for this week (or Press Enter to skip): ").strip()
        if context_input:
            prompt += f"\n\nAdditional User Context/Focus: {context_input}"
        
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7,
                top_p=0.95,
                top_k=40,
                max_output_tokens=8192,
                response_mime_type="application/json",
            )
        )
        
        text = response.text
        # Cleanup if needed (though mime_type json usually returns pure json)
        if text.startswith("```json"):
            text = text.replace("```json", "").replace("```", "")
            
        plan = json.loads(text)
        return plan
    except Exception as e:
        print(f"Error generating plan: {e}")
        return []

def main():
    sheet_id = os.getenv("GOOGLE_SHEET_ID_SOCIAL")
    if not sheet_id:
        print("Error: GOOGLE_SHEET_ID_SOCIAL not in .env")
        return

    # Use the same credentials for Sheets
    creds = get_credentials()
    if not creds:
        print("Auth Failed.")
        return
        
    client = gspread.authorize(creds)
    sh = client.open_by_key(sheet_id)
    ws = sh.sheet1 

    last_date = get_last_date(ws)
    print(f"Last planned date: {last_date}")
    
    print("Generating new plan...")
    plan = generate_plan(last_date)
    
    rows_to_add = []
    current_date = last_date
    
    print("\n--- Proposed Content Plan ---")
    for i, item in enumerate(plan):
        print(f"{i+1}. [{item.get('format')}] {item.get('topic')}")
        print(f"   Context: {item.get('context')}\n")
    
    confirm = 'n'
    try:
        confirm = input("\nPlan generated. Please review the output above.\nIf satisfied, type 'y' to save to the Sheet. You can then edit the Sheet before generating assets.\nSave plan? (y/n): ").strip().lower()
    except EOFError:
        print("Input stream closed.")
        
    if confirm != 'y':
        print("Plan discarded. No changes made.")
        return

    for item in plan:
        current_date += timedelta(days=1)
        row = [
            item.get("topic"),
            item.get("format", "Image"),
            "Pending",
            current_date.strftime("%Y-%m-%d"),
            item.get("context", ""),
            "", "" # Caption, Visual Path placeholders
        ]
        rows_to_add.append(row)
        
    if rows_to_add:
        ws.append_rows(rows_to_add)
        print(f"✅ Added {len(rows_to_add)} new posts to the schedule.")
    else:
        print("No rows generated.")

if __name__ == "__main__":
    main()
