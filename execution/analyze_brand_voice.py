
import os
import sys
import psycopg2
from dotenv import load_dotenv
from utils_genai import get_client
from google.genai import types

def analyze_brand_voice():
    """
    RAG Research Agent:
    1. Searches Flowko Knowledge Base for brand-relevant concepts.
    2. Synthesizes snippets into a cohesive Brand Guide using Gemini.
    3. Saves to 'brand_context.txt'.
    """
    load_dotenv()
    print("🧠 Starting Brand Voice Analysis...")
    
    # 1. Fetch relevant chunks from Supabase
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("⚠️  DATABASE_URL not found. Skipping analysis (using local cache).")
        return

    context_snippets = []
    try:
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        
        # Query content from EMBEDDINGS table (where the text chunks actually live)
        # Use SELECT * to avoid ambiguity, but target the correct table
        # Fetching 200 rows to get a broader sample
        query = """
        SELECT *
        FROM knowledge_embeddings 
        LIMIT 200;
        """
        
        cur.execute(query)
        results = cur.fetchall()
        
        # De-duplicate and clean
        seen = set()
        
        # Find 'content' column index dynamically
        if cur.description:
            colnames = [desc[0] for desc in cur.description]
            print(f"🔎 Found columns in knowledge_embeddings: {colnames}")
            
            try:
                # Use 'content' column
                content_idx = colnames.index('content')
            except ValueError:
                print(f"⚠️ 'content' column not found in {colnames}. skipping.")
                return

            for r in results:
                text = r[content_idx]
                if text:
                    text_str = str(text).strip() # Ensure string
                    # Feed ALL content to Gemini (Let the LLM decide relevance)
                    if text_str and text_str not in seen and len(text_str) > 20:
                        context_snippets.append(text_str)
                        seen.add(text_str)
        else:
             print("⚠️ No description returned from cursor.")
                
        cur.close()
        conn.close()
        print(f"📚 Retrieved {len(context_snippets)} relevant text snippets from Knowledge Base.")
        
    except Exception as e:
        print(f"⚠️  DB Retrieval Failed: {e}")
        return

    if not context_snippets:
        print("ℹ️  No specific brand info found in Knowledge Base. Using default/local.")
        return

    # 2. Synthesize with Gemini
    try:
        combined_context = "\n\n---\n\n".join(context_snippets)
        client = get_client()
        
        prompt = f"""
        You are a Brand Strategist. Your goal is to create a concise "Brand Bible" based ONLY on the provided raw knowledge base snippets.
        
        **CRITICAL INSTRUCTION:** Output strictly in **ENGLISH**. If the source text is in another language (e.g., Slovenian), **TRANSLATE** the core concepts into professional English business language.
        
        Analyze the snippets below and extract:
        1. **Brand Voice & Tone**: (e.g., Professional, Witty, Authoritative)
        2. **Visual Style**: (e.g., Colors, Aesthetic, Mood for images)
        3. **Core Values/Mission**: What drives the company?
        4. **Do's and Don'ts**: Specific instructions if found.
        
        Output format: Pure text (Markdown), checking for consistency. Ignore irrelevant snippets.
        
        RAW KNOWLEDGE SNIPPETS:
        {combined_context[:50000]}  # Increased safety limit
        """
        
        print("🤔 Synthesizing Brand Guide with Gemini...")
        response = client.models.generate_content(
            model='gemini-2.0-flash-exp', # Fast and smart
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2, # Low temp for factual consistency
            )
        )
        
        brand_guide = response.candidates[0].content.parts[0].text
        
        # 3. Save Result
        with open('brand_context.txt', 'w', encoding='utf-8') as f:
            f.write(brand_guide)
            
        print("✨ Brand Analysis Complete! Updated 'brand_context.txt'.")
        print("\n--- NEW BRAND CONTEXT PREVIEW ---")
        print(brand_guide[:300] + "...")
        print("---------------------------------")
        
    except Exception as e:
        print(f"❌ AI Synthesis Failed: {e}")

if __name__ == "__main__":
    analyze_brand_voice()
