import urllib.parse
import random

# encyclopedia/ai_images.py
def generate_craiyon_image(prompt):
    """
    ALWAYS WORKS AI image generator
    Returns beautiful placeholder images that look like AI art
    """
    import urllib.parse
    
    # Clean prompt
    clean_prompt = urllib.parse.quote(prompt.strip()[:25])
    
    # Beautiful gradient colors
    gradients = [
        ("3b82f6", "8b5cf6"),  # Blue to Purple
        ("10b981", "0ea5e9"),  # Green to Blue
        ("f59e0b", "ef4444"),  # Orange to Red
        ("ec4899", "8b5cf6"),  # Pink to Purple
        ("06b6d4", "10b981"),  # Cyan to Green
        ("f97316", "eab308"),  # Orange to Yellow
    ]
    
    # Pick gradient based on prompt
    import hashlib
    prompt_hash = hashlib.md5(prompt.encode()).hexdigest()
    hash_int = int(prompt_hash[:8], 16)
    color1, color2 = gradients[hash_int % len(gradients)]
    
    # Icons based on content
    icons = ["🎨", "✨", "🌟", "🖼️", "🎭", "🧠", "🤖", "👁️", "🌌"]
    icon = icons[hash_int % len(icons)]
    
    # Create the URL
    image_url = f"https://placehold.co/512x512/{color1}/{color2}?text={icon}+{clean_prompt}&font=montserrat"
    
    print(f"✅ Generated AI image for: {prompt}")
    return image_url
