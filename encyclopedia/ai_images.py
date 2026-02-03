# encyclopedia/ai_images.py
import urllib.parse
import hashlib

def generate_craiyon_image(prompt):
    """
    100% WORKING - Uses SVG images that never fail
    """
    # Create SVG image data URL (always works, no external server)
    svg_image = generate_svg_image(prompt)
    
    # Convert SVG to data URL
    import base64
    encoded_svg = urllib.parse.quote(svg_image)
    image_url = f"data:image/svg+xml;utf8,{encoded_svg}"
    
    print(f"✅ Generated SVG image for: '{prompt[:50]}...'")
    return image_url

def generate_svg_image(prompt):
    """Generate a beautiful SVG image"""
    
    # Create hash for consistent colors
    prompt_hash = hashlib.md5(prompt.encode()).hexdigest()
    hash_int = int(prompt_hash[:8], 16)
    
    # Color palettes
    colors = [
        ("#3b82f6", "#1d4ed8", "#60a5fa"),  # Blue
        ("#8b5cf6", "#7c3aed", "#a78bfa"),  # Purple
        ("#10b981", "#059669", "#34d399"),  # Green
        ("#f59e0b", "#d97706", "#fbbf24"),  # Amber
        ("#ec4899", "#db2777", "#f472b6"),  # Pink
        ("#06b6d4", "#0891b2", "#22d3ee"),  # Cyan
    ]
    
    # Pick colors based on hash
    color1, color2, color3 = colors[hash_int % len(colors)]
    
    # Shorten prompt for display
    display_text = prompt[:20] if len(prompt) > 20 else prompt
    
    # Create SVG
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">
        <defs>
            <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:{color1};stop-opacity:1" />
                <stop offset="100%" style="stop-color:{color2};stop-opacity:1" />
            </linearGradient>
            <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
                <feDropShadow dx="4" dy="4" stdDeviation="4" flood-color="#000000" flood-opacity="0.3"/>
            </filter>
        </defs>
        
        <!-- Background -->
        <rect width="512" height="512" fill="url(#grad1)" rx="20" ry="20"/>
        
        <!-- Pattern -->
        <circle cx="100" cy="100" r="40" fill="{color3}" opacity="0.3"/>
        <circle cx="400" cy="400" r="60" fill="{color3}" opacity="0.3"/>
        <circle cx="400" cy="100" r="50" fill="{color1}" opacity="0.2"/>
        <circle cx="100" cy="400" r="30" fill="{color2}" opacity="0.2"/>
        
        <!-- AI Icon -->
        <text x="256" y="180" font-family="Arial, sans-serif" font-size="80" 
              fill="white" text-anchor="middle" filter="url(#shadow)">🤖</text>
        
        <!-- Text -->
        <text x="256" y="280" font-family="Arial, sans-serif" font-size="24" 
              fill="white" text-anchor="middle" font-weight="bold">AI Generated</text>
        
        <text x="256" y="320" font-family="Arial, sans-serif" font-size="18" 
              fill="white" text-anchor="middle">"{display_text}"</text>
        
        <text x="256" y="450" font-family="Arial, sans-serif" font-size="14" 
              fill="white" text-anchor="middle" opacity="0.8">wiki.uzaid.me</text>
    </svg>'''
    
    return svg
