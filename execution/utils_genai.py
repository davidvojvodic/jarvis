"""
Unified Google Gen AI SDK Client (Modern v1.0).
Replaces legacy vertexai.init().
"""
from google import genai
from utils_auth import get_credentials, PROJECT_ID, LOCATION

def get_client() -> genai.Client:
    """Returns an authenticated google.genai.Client for Vertex AI."""
    creds = get_credentials()
    if not creds:
        raise ValueError("Authentication missing. Run setup_auth.py.")
    
    # Initialize Client with Vertex AI backend
    client = genai.Client(
        vertexai=True, 
        project=PROJECT_ID, 
        location=LOCATION,
        credentials=creds
    )
    return client
