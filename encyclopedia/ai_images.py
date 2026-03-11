import random
import urllib.parse
import urllib.request
import base64
from django.conf import settings

def generate_ai_image_data_url(prompt: str, width: int = 768, height: int = 768, model: str = "flux", seed: int | None = None) -> str | None:
    """
    NEW VERSION (2026):
    - Uses the current Pollinations endpoint
    - Fetches on the SERVER with your private API key (no exposure to users)
    - Returns a data: URL (embedded image) so it NEVER fails to load
    - Keeps your original short-prompt enhancement
    """
    prompt = (prompt or "").strip()
    if not prompt:
        return None

    # Improve short prompts (your original logic)
    if len(prompt.split()) <= 2:
        prompt = f"photorealistic, high detail, sharp focus: {prompt}"

    seed = seed or random.randint(1, 10_000_000)
    encoded = urllib.parse.quote(prompt, safe="")

    key = getattr(settings, 'POLLINATIONS_API_KEY', None)
    if not key:
        raise ValueError("❌ POLLINATIONS_API_KEY is not set in settings.py")

    # NEW 2026 ENDPOINT + key
    url = (
        f"https://gen.pollinations.ai/image/{encoded}"
        f"?model={urllib.parse.quote(model)}"
        f"&width={width}&height={height}&seed={seed}&nologo=true"
        f"&key={urllib.parse.quote(key)}"
    )

    try:
        with urllib.request.urlopen(url, timeout=15) as response:
            if response.status != 200:
                print(f"Pollinations returned status {response.status}")
                return None
            image_bytes = response.read()

        # Convert to data: URL (works perfectly with your existing template + download button)
        return f"data:image/png;base64,{base64.b64encode(image_bytes).decode('utf-8')}"

    except Exception as e:
        print(f"Pollinations fetch error: {e}")
        return None
