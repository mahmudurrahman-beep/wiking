# In encyclopedia/ai_images.py
import requests
import os

def generate_craiyon_image(prompt):
    """
    Generate AI image using Pollinations.ai API.
    Returns a direct image URL.
    """
    try:
        # 1. Clean and format the prompt
        clean_prompt = requests.utils.quote(prompt)  # URL-encode the prompt
        
        # 2. Construct the Pollinations API URL
        # You can customize the model (e.g., 'flux', 'realistic', 'anime')
        pollinations_url = f"https://image.pollinations.ai/prompt/{clean_prompt}?width=512&height=512&model=flux&seed=1"
        
        print(f"🔄 Calling Pollinations API for: '{prompt}'")
        print(f"🌐 URL: {pollinations_url[:80]}...")
        
        # 3. The URL *is* the image. We return it directly.
        # Pollinations serves the image directly from this endpoint.
        return pollinations_url
        
    except Exception as e:
        print(f"❌ Error generating image: {e}")
        # Fallback to a themed placeholder
        import urllib.parse
        safe_prompt = urllib.parse.quote(prompt[:30])
        return f"https://placehold.co/512x512/4a6fa5/ffffff?text=AI+Wiki:+\n{safe_prompt}&font=montserrat"
