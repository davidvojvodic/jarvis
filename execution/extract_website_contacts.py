
import re
import httpx
import logging
import os
import json
import anthropic
from urllib.parse import urljoin, urlparse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("website_extractor")

SOCIAL_PLATFORMS = {
    "facebook": r"facebook\.com",
    "twitter": r"(twitter\.com|x\.com)",
    "linkedin": r"linkedin\.com",
    "instagram": r"instagram\.com",
    "youtube": r"youtube\.com",
    "tiktok": r"tiktok\.com"
}

def extract_emails(text):
    """Extract email addresses from text (Regex Baseline)."""
    if not text:
        return []
    # Basic email regex
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    matches = re.findall(email_pattern, text)
    
    # Filter out common image/file extensions that regex might mistake for TLDs
    invalid_extensions = {
        '.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg', '.bmp', '.ico',
        '.css', '.js', '.woff', '.woff2', '.ttf', '.eot', '.mp4', '.mp3'
    }
    
    valid_emails = []
    for email in matches:
        # Check if email ends with an invalid extension
        lower_email = email.lower()
        if any(lower_email.endswith(ext) for ext in invalid_extensions):
            continue
            
        # Additional cleanup: remove trailing punctuation if captured
        if lower_email.endswith('.'):
            email = email[:-1]
            
        valid_emails.append(email)
        
    return list(set(valid_emails))

def extract_phones(text):
    """Extract phone numbers from text (Regex Baseline)."""
    if not text:
        return []
    # US/International phone regex - simplified
    phone_pattern = r'\+?1?\s*\(?[- .]?\d{3}\)?[- .]?\d{3}[- .]?\d{4}'
    return list(set(re.findall(phone_pattern, text)))

def extract_social_media(html, base_url):
    """Extract social media links from HTML."""
    if not html:
        return {}
    social_links = {}
    for platform, pattern in SOCIAL_PLATFORMS.items():
        # Find links containing the platform domain
        # Using a simple regex to find hrefs
        links = re.findall(r'href=["\'](.*?)["\']', html)
        for link in links:
            if re.search(pattern, link, re.IGNORECASE):
                # Normalize URL
                full_url = urljoin(base_url, link)
                social_links[platform] = full_url
                break # Take the first one found for each platform
    return social_links

def extract_with_claude(text_content: str, business_name: str) -> dict:
    """
    Use Claude 3.5 Sonnet to extract structured data from website text.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Warning: ANTHROPIC_API_KEY not found. Skipping AI extraction.")
        return {}

    if len(text_content) > 15000:
        text_content = text_content[:15000] + "...(truncated)"

    client = anthropic.Anthropic(api_key=api_key)

    prompt = f"""
    You are an expert lead researcher. Your task is to extract structured contact information for the business "{business_name}" from the website text provided below.

    GOAL: Find EVERY email, phone number, and social profile.
    SPECIFIC FOCUS: Identify the Owner, Founder, CEO, or key decision-maker.

    Analyze the text and return a JSON object with this EXACT schema:
    {{
        "emails": ["email1", "email2"],
        "phone_numbers": ["phone1"],
        "social_media": {{ "linkedin": "url", "facebook": "url" }},
        "owner_info": {{
            "name": "Full Name",
            "title": "Job Title (e.g. CEO)",
            "email": "personal email if found",
            "phone": "personal phone if found",
            "linkedin": "personal linkedin url"
        }},
        "team_members": [
            {{ "name": "Name", "title": "Role", "email": "email", "linkedin": "url" }}
        ]
    }}

    Rules:
    - Extract ALL valid emails you see.
    - Infer the owner if you see text like "Metod, Founder of Piksl".
    - If you find multiple team members, list them.
    - Return ONLY valid JSON. No markdown formatting.

    Website Text:
    {text_content}
    """

    try:
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1024,
            temperature=0,
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Parse JSON
        content = response.content[0].text
        # Clean potential markdown
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
            
        return json.loads(content)

    except Exception as e:
        print(f"Claude Extraction Error: {e}")
        return {}


from duckduckgo_search import DDGS

def perform_duckduckgo_search(query: str) -> str:
    """
    Perform a simple DuckDuckGo Text search to find additional context.
    Returns: First relevant result URL or None.
    """
    try:
        # Use simple text search from the library
        results = DDGS().text(query, max_results=1)
        if results:
            first = results[0]
            link = first.get("href")
            print(f"  👉 DDG found: {link}")
            return link
    except Exception as e:
        print(f"  ⚠️ DDG Search Error: {e}")
    return None

def clean_html_to_text(html: str) -> str:
    """Simple HTML to text cleaner."""
    # Remove scripts and styles
    html = re.sub(r'<script.*?>.*?</script>', ' ', html, flags=re.DOTALL)
    html = re.sub(r'<style.*?>.*?</style>', ' ', html, flags=re.DOTALL)
    # Remove tags
    text = re.sub(r'<[^>]+>', ' ', html)
    # Cleanup whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def scrape_website_contacts(url: str, business_name: str = None) -> dict:
    """
    Scrape a website for contact information (Hybrid: Regex + AI).
    """
    if not url:
        return {"error": "No URL provided"}
        
    if not url.startswith('http'):
        url = 'https://' + url

    result = {
        "emails": [],
        "phone_numbers": [],
        "social_media": {},
        "owner_info": {},
        "team_members": [],
        "additional_contacts": [],
        "business_hours": "",
        "_pages_scraped": 0,
        "_search_enriched": False
    }

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        # We want to check Homepage + About/Contact
        pages_to_check = [url]
        parsed_url = urlparse(url)
        
        full_text_content = ""
        
        with httpx.Client(timeout=15.0, headers=headers, follow_redirects=True) as client:
            # 1. Scrape Homepage
            try:
                response = client.get(url)
                result["_pages_scraped"] += 1
                
                if response.status_code == 200:
                    html = response.text
                    
                    # Regex Baseline
                    result["emails"].extend(extract_emails(html))
                    result["phone_numbers"].extend(extract_phones(html))
                    result["social_media"].update(extract_social_media(html, url))
                    
                    full_text_content += f"\n--- HOMEPAGE ---\n{clean_html_to_text(html)}"
                    
                    # Find About/Contact pages
                    hrefs = re.findall(r'href=["\'](.*?)["\']', html)
                    relevant_links = []
                    for link in hrefs:
                        lower_link = link.lower()
                        if any(x in lower_link for x in ['about', 'team', 'contact', 'people', 'staff']):
                            full_url = urljoin(url, link)
                            # Only internal links
                            if urlparse(full_url).netloc == parsed_url.netloc:
                                relevant_links.append(full_url)
                    
                    # Take up to 2 relevant sub-pages
                    for sub_url in list(set(relevant_links))[:2]:
                        try:
                            resp = client.get(sub_url)
                            result["_pages_scraped"] += 1
                            if resp.status_code == 200:
                                sub_html = resp.text
                                # Regex Baseline
                                result["emails"].extend(extract_emails(sub_html))
                                result["phone_numbers"].extend(extract_phones(sub_html))
                                result["social_media"].update(extract_social_media(sub_html, sub_url))
                                
                                page_name = sub_url.split('/')[-1]
                                full_text_content += f"\n--- {page_name.upper()} PAGE ---\n{clean_html_to_text(sub_html)}"
                        except Exception:
                            pass
                            
            except Exception as e:
                result["error"] = f"Network error: {str(e)}"

        # 1.5. DuckDuckGo Enrichment (If business name provided)
        if business_name:
            try:
                print(f"  🔎 Searching DDG for: '{business_name} owner email'")
                ddg_url = perform_duckduckgo_search(f"{business_name} owner email contact")
                if ddg_url and parsed_url.netloc not in ddg_url: # Don't re-scrape own site
                    print(f"  👉 Found external profile: {ddg_url}")
                    with httpx.Client(timeout=10.0, headers=headers, follow_redirects=True) as client:
                        resp = client.get(ddg_url)
                        if resp.status_code == 200:
                            result["_search_enriched"] = True
                            ddg_html = resp.text
                            # Brief regex check
                            result["emails"].extend(extract_emails(ddg_html))
                            result["social_media"].update(extract_social_media(ddg_html, ddg_url))
                            
                            full_text_content += f"\n--- EXTERNAL SEARCH ({ddg_url}) ---\n{clean_html_to_text(ddg_html)}"
            except Exception as e:
                print(f"  ⚠️ Enrichment failed: {e}")

        # 2. AI Extraction (The "Ultrathink")
        if full_text_content and business_name:
            print(f"  🧠 AI Analyzing {len(full_text_content)} chars for {business_name}...")
            ai_data = extract_with_claude(full_text_content, business_name)
            
            if ai_data:
                # Merge AI data (Priority)
                if ai_data.get("owner_info"):
                    result["owner_info"] = ai_data["owner_info"]
                    print(f"    ✨ Found Owner: {result['owner_info'].get('name')}")
                
                if ai_data.get("team_members"):
                    result["team_members"] = ai_data["team_members"]
                    print(f"    ✨ Found {len(result['team_members'])} Team Members")
                
                # Merge emails/phones found by AI
                if ai_data.get("emails"):
                    result["emails"].extend(ai_data["emails"])
                if ai_data.get("phone_numbers"):
                    result["phone_numbers"].extend(ai_data["phone_numbers"])
                
                # Merge socials
                if ai_data.get("social_media"):
                    for k, v in ai_data["social_media"].items():
                        if k not in result["social_media"]:
                            result["social_media"][k] = v

    except Exception as e:
        result["error"] = str(e)
        
    # Final Deduplication & Cleanup
    result["emails"] = list(set(result["emails"]))
    result["phone_numbers"] = list(set(result["phone_numbers"]))
    
    return result
