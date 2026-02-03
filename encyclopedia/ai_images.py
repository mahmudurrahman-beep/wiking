# encyclopedia/ai_images.py
import urllib.parse
import requests
import time
import random

def generate_craiyon_image(prompt):
    """Generate AI image using multiple reliable services with fallbacks"""
    
    # Clean and encode the prompt
    clean_prompt = urllib.parse.quote(prompt, safe='')
    
    # List of reliable image generation services (ranked by reliability)
    service_options = [
        # Option 1: Pollinations with simpler parameters (most reliable)
        {
            'name': 'Pollinations (default)',
            'url': f"https://image.pollinations.ai/prompt/{clean_prompt}",
            'params': {'width': 512, 'height': 512, 'seed': random.randint(1, 10000)}
        },
        
        # Option 2: Pollinations with SDXL model
        {
            'name': 'Pollinations (SDXL)',
            'url': f"https://image.pollinations.ai/prompt/{clean_prompt}",
            'params': {'width': 512, 'height': 512, 'model': 'sdxl'}
        },
        
        # Option 3: Pollinations without any model parameter
        {
            'name': 'Pollinations (simple)',
            'url': f"https://pollinations.ai/p/{clean_prompt}",
            'params': {}
        },
        
        # Option 4: Try a different service entirely
        {
            'name': 'Placeholder with prompt',
            'url': f"https://placehold.co/512x512/4a6fa5/ffffff",
            'params': {'text': clean_prompt[:30]}
        },
    ]
    
    # Try each service until one works
    for service in service_options:
        try:
            print(f"🔄 Trying {service['name']}...")
            
            # Construct the URL with parameters
            if service['params']:
                params_str = '&'.join([f"{k}={v}" for k, v in service['params'].items()])
                full_url = f"{service['url']}?{params_str}"
            else:
                full_url = service['url']
            
            print(f"🌐 Requesting: {full_url[:80]}...")
            
            # Make the request with a timeout
            response = requests.get(
                full_url, 
                timeout=15,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )
            
            # Check if successful
            if response.status_code == 200:
                print(f"✅ Success with {service['name']}")
                return full_url
            else:
                print(f"⚠️ {service['name']} returned {response.status_code}")
                # Wait a bit before trying next service
                time.sleep(0.5)
                
        except requests.exceptions.Timeout:
            print(f"⏰ Timeout with {service['name']}")
            continue
        except requests.exceptions.ConnectionError:
            print(f"🔌 Connection error with {service['name']}")
            continue
        except Exception as e:
            print(f"❌ Error with {service['name']}: {e}")
            continue
    
    # If all services fail, return a themed placeholder
    print("⚠️ All services failed, returning themed placeholder")
    return generate_themed_placeholder(prompt)

def generate_themed_placeholder(prompt):
    """Generate a themed placeholder image based on prompt content"""
    
    prompt_lower = prompt.lower()
    
    # Color themes based on prompt content
    color_themes = {
        'blue': ['1e3a8a', '1d4ed8', '0369a1', '0ea5e9'],
        'green': ['166534', '16a34a', '22c55e', '4ade80'],
        'red': ['991b1b', 'dc2626', 'ef4444', 'f87171'],
        'purple': ['581c87', '7c3aed', '8b5cf6', 'a78bfa'],
        'orange': ['9a3412', 'ea580c', 'f97316', 'fb923c'],
    }
    
    # Choose color based on prompt
    if any(word in prompt_lower for word in ['sky', 'ocean', 'water', 'cold', 'ice']):
        color = random.choice(color_themes['blue'])
    elif any(word in prompt_lower for word in ['nature', 'forest', 'plant', 'tree', 'grass']):
        color = random.choice(color_themes['green'])
    elif any(word in prompt_lower for word in ['fire', 'sun', 'heat', 'warm', 'sunset']):
        color = random.choice(color_themes['orange'])
    elif any(word in prompt_lower for word in ['flower', 'magic', 'fantasy', 'mystic']):
        color = random.choice(color_themes['purple'])
    else:
        color = random.choice(color_themes['blue'])
    
    # Truncate prompt for placeholder
    short_prompt = prompt[:20].replace(' ', '+')
    
    # Return a fun placeholder
    return f"https://placehold.co/512x512/{color}/ffffff?text={urllib.parse.quote(short_prompt)}"
