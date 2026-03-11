import random
import urllib.parse
import urllib.request
import base64
from django.conf import settings

def generate_ai_image_data_url(prompt: str, width: int = 768, height: int = 768, model: str = "flux", seed: int | None = None) -> str | None:
    """
    FIXED 2026 VERSION - Uses Authorization header + secret key support
    Returns data: URL (never fails to load in browser)
    """
    prompt = (prompt or "").strip()
    if not prompt:
        return None

    # Your original short-prompt enhancement
    if len(prompt.split()) <= 2:
        prompt = f"photorealistic, high detail, sharp focus: {prompt}"

    seed = seed or random.randint(1, 10_000_000)
    encoded_prompt = urllib.parse.quote(prompt, safe="")

    key = getattr(settings, 'POLLINATIONS_API_KEY', None)
    if not key:
        raise ValueError("❌ POLLINATIONS_API_KEY is not set in settings.py")

    # NEW ENDPOINT + RECOMMENDED HEADER AUTH (no ?key= in URL)
    base_url = (
        f"https://gen.pollinations.ai/image/{encoded_prompt}"
        f"?model={urllib.parse.quote(model)}"
        f"&width={width}&height={height}&seed={seed}&nologo=true"
    )

    try:
        req = urllib.request.Request(
            base_url,
            headers={
                'Authorization': f'Bearer {key}',
                'User-Agent': 'Wiki-AI-Image-Generator/1.0'  # helps avoid WAF blocks
            }
        )
        
        with urllib.request.urlopen(req, timeout=20) as response:
            if response.status != 200:
                error_body = response.read().decode('utf-8', errors='ignore')[:500]
                print(f"Pollinations error {response.status}: {error_body}")
                return None
            image_bytes = response.read()

        # Convert to embedded data URL (works perfectly with your template)
        return f"data:image/png;base64,{base64.b64encode(image_bytes).decode('utf-8')}"

    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8', errors='ignore')[:500]
        print(f"Pollinations HTTP {e.code} error: {error_body}")
        raise  # Let the view catch it and show real message
    except Exception as e:
        print(f"Pollinations fetch error: {e}")
        return None
