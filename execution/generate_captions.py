"""
Generate Social Media Captions using Gemini (Vertex AI).
Authentication: OAuth (via utils_auth).
"""
import argparse
from utils_genai import get_client

def generate_caption(topic: str, context: str, platform: str = "Instagram"):
    """Generates a caption using Gemini 2.0 via Google Gen AI SDK."""
    try:
        client = get_client()
    except Exception as e:
        return f"Auth Error: {e}"

    # Load Config
    import json
    try:
        with open('social_config.json', 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        config = {"niche": "Agency", "tone": "Professional"}

    prompt = f"""
    Act as a Senior Social Media Manager for a {config.get('niche', 'Business')}.
    Write a {platform} caption about: "{topic}".
    
    Context/Details:
    {context}
    
    Requirements:
    - Tone: {config.get('tone', 'Engaging')}.
    - Structure:
        1. HOOK: Stop the scroll (Question or Bold Statement).
        2. VALUE: The core message/tip.
        3. CTA: "Comment 'SCALE' for details" or "Link in Bio".
    - Hashtags: Include 3-5 relevant hashtags for {config.get('niche')}.
    - Formatting: Use emojis 🚀, line breaks for readability.
    - NO generic fluff. Keep it punchy.
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        print(f"Error generating caption: {e}")
        return f"Error: {e}"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", required=True)
    parser.add_argument("--context", default="")
    parser.add_argument("--platform", default="Instagram")
    args = parser.parse_args()
    
    caption = generate_caption(args.topic, args.context, args.platform)
    print(caption)

if __name__ == "__main__":
    main()
