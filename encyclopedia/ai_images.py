# encyclopedia/ai_images.py
import random
import urllib.parse


def generate_ai_image_url(prompt: str, width: int = 768, height: int = 768, model: str = "flux", seed: int | None = None) -> str | None:
    """
    Returns a direct image URL from Pollinations.
    Browser will load the image (no server-side requests).
    This avoids Koyeb/server IP rate-limit & timeout problems.
    """
    prompt = (prompt or "").strip()
    if not prompt:
        return None

    # Improve short prompts
    if len(prompt.split()) <= 2:
        prompt = f"photorealistic, high detail, sharp focus: {prompt}"

    seed = seed or random.randint(1, 10_000_000)
    encoded = urllib.parse.quote(prompt, safe="")

    return (
        f"https://image.pollinations.ai/prompt/{encoded}"
        f"?model={urllib.parse.quote(model)}&width={width}&height={height}&seed={seed}&nologo=true"
    )
