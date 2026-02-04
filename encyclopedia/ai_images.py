# encyclopedia/ai_images.py
import urllib.parse
import random

def generate_pollinations_image(prompt: str, *, width=768, height=768, model="flux", seed=None) -> str:
    """
    Real AI image generation via Pollinations (no API key).
    Returns a URL you can put directly in <img src="...">.
    """
    prompt = (prompt or "").strip()
    if not prompt:
        return ""

    # Better "accuracy" for short prompts like "messi"
    # (You can tune this however you like)
    if len(prompt.split()) <= 2:
        prompt = f"photorealistic portrait of {prompt}, close-up, high detail, sharp focus"

    if seed is None:
        seed = random.randint(1, 10_000_000)

    encoded = urllib.parse.quote(prompt, safe="")
    # Use query params to control model/size and reduce caching issues
    return (
        f"https://image.pollinations.ai/prompt/{encoded}"
        f"?model={urllib.parse.quote(model)}&width={width}&height={height}&seed={seed}&nologo=true"
    )

# Keep your old function name so views.py doesn't change
def generate_craiyon_image(prompt: str) -> str:
    return generate_pollinations_image(prompt)
