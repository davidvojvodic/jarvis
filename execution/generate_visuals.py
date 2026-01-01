"""
Generate Images and Videos using Google Gen AI SDK (Modern).
Authentication: OAuth (via utils_genai).
"""
import os
import argparse
from utils_genai import get_client
from google.genai import types
try:
    from analyze_brand_voice import analyze_brand_voice
except ImportError:
    analyze_brand_voice = lambda: None

def get_brand_context():
    # Attempt to refresh implementation plan from DB first
    analyze_brand_voice()
    try:
        with open('brand_context.txt', 'r', encoding='utf-8') as f:
            return f.read().strip()
    except Exception:
        return "Style: Professional, Modern, Business-focused."

def generate_image(prompt: str, output_path: str):
    """Generate image using Nano Banana Pro (Gemini 3 Pro Image) via Google Gen AI SDK."""
    brand_style = get_brand_context()
    
    # Nano Banana Pro excels at text, reasoning, and complex visuals
    if len(prompt) < 200:
        full_prompt = f"{prompt}, photorealistic, 4k, highly detailed, professional quality, clean composition."
    else:
        full_prompt = f"{prompt}\n\nStyle: {brand_style}\nRequirement: Photorealistic, professional quality."
    
    print(f"Generating Image (Nano Banana Pro) for: '{prompt[:50]}...'")
    try:
        # Use Gemini API Key for Nano Banana Pro access
        import os
        from google import genai
        from google.genai import types
        
        api_key = os.getenv("GEMINI_API_KEY")
        client = genai.Client(api_key=api_key, http_options={'api_version': 'v1alpha'})
        
        response = client.models.generate_content(
            model='gemini-3-pro-image-preview',
            contents=f"Generate an image: {full_prompt}",
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE", "TEXT"],
            )
        )
        
        # Nano Banana Pro returns images via generate_content
        # Extract image from response parts
        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    image_data = part.inline_data.data
                    with open(output_path, "wb") as f:
                        f.write(image_data)
                    print(f"Image saved to {output_path}")
                    return output_path
        
        print("No image found in response")
        return None
    
    except Exception as e:
        print(f"Error generating image: {e}")
        return None

def generate_video(prompt: str, output_path: str):
    """Generate video using Veo 3.1 via Google Gen AI SDK."""
    brand_style = get_brand_context()
    full_prompt = f"{prompt}\n\nStyle:\n{brand_style}"
    
    print(f"Generating Video (Veo 3.1) for: '{prompt[:50]}...'")
    try:
        from google import genai
        from utils_auth import get_credentials, PROJECT_ID
        
        # Consistent EU handling
        creds = get_credentials()
        client = genai.Client(
            vertexai=True, 
            project=PROJECT_ID, 
            location="europe-west1", 
            credentials=creds
        )
        
        response = client.models.generate_videos(
            model="veo-3.1-generate-001",
            prompt=full_prompt,
            config=types.GenerateVideosConfig(
                aspect_ratio="16:9" 
            )
        )
        
        print(f"DEBUG: Response type: {type(response)}")
        print(f"DEBUG: Response dir: {dir(response)}")
        
        import time
        retries = 0
        max_retries = 15
        
        # Brute force poll of .result property
        if hasattr(response, 'result'):
            print("Polling response.result...")
            
            # Initial Check
            current_result = response.result
            if callable(current_result): # Should not happen based on debug
                 try:
                    response = response.result() # Wait if it's a method
                 except Exception:
                    pass
            
            while retries < max_retries:
                # Check property
                if hasattr(response, 'result') and response.result:
                     response = response.result
                     print("Video generation complete!")
                     break
                
                print(f"Waiting for video... ({retries+1}/{max_retries})")
                time.sleep(10) # Wait 10s
                retries += 1
                
        print(f"DEBUG: Final Response type: {type(response)}")

        if hasattr(response, 'generated_videos') and response.generated_videos:
            video = response.generated_videos[0]
            if hasattr(video, "video_bytes"):
                with open(output_path, "wb") as f:
                    f.write(video.video_bytes)
            elif hasattr(video, "save"):
                video.save(output_path)
            else:
                print(f"Unknown video object: {dir(video)}")
                return None
                
            print(f"Video saved to {output_path}")
            return output_path

    except Exception as e:
        print(f"Video Generation Error: {e}")
        return None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--type", choices=["image", "video"], default="image")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    
    output_dir = os.path.dirname(args.output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    if args.type == "image":
        generate_image(args.prompt, args.output)
    else:
        generate_video(args.prompt, args.output)

if __name__ == "__main__":
    main()
