# encyclopedia/ai_images.py
import os
import random
import urllib.parse
import requests

def pollinations_url(prompt: str, width=768, height=768, model="flux", seed=None) -> str:
    seed = seed or random.randint(1, 10_000_000)
    encoded = urllib.parse.quote(prompt, safe="")
    return (
        f"https://image.pollinations.ai/prompt/{encoded}"
        f"?model={urllib.parse.quote(model)}&width={width}&height={height}&seed={seed}&nologo=true"
    )

def pollinations_is_up(timeout=6) -> bool:
    try:
        # small sanity check endpoint: fetch a tiny image
        test = pollinations_url("test", width=64, height=64, seed=1)
        r = requests.get(test, timeout=timeout)
        return r.status_code == 200 and r.headers.get("content-type", "").startswith("image/")
    except:
        return False

def hf_generate_image_bytes(prompt: str, model="stabilityai/sdxl-turbo", timeout=60):
    token = os.environ.get("HF_TOKEN")
    if not token:
        return None

    url = f"https://api-inference.huggingface.co/models/{model}"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"inputs": prompt}

    r = requests.post(url, headers=headers, json=payload, timeout=timeout)
    if r.status_code == 200 and r.headers.get("content-type", "").startswith("image/"):
        return r.content
    return None

def generate_ai_image_url(prompt: str) -> str | None:
    prompt = (prompt or "").strip()
    if not prompt:
        return None

    # Make short prompts more specific
    if len(prompt.split()) <= 2:
        prompt = f"photorealistic, high detail, sharp focus: {prompt}"

    # 1) Prefer Pollinations URL (no local media needed)
    # If you don’t want the “is_up” check (extra request), remove it.
    if pollinations_is_up():
        return pollinations_url(prompt)

    # 2) If Pollinations is down, try HF (needs HF_TOKEN)
    # If HF works, we still need a URL to show.
    # Without external hosting, we cannot return a URL here,
    # so we return None and show an error.
    img = hf_generate_image_bytes(prompt)
    if img:
        # You need external hosting to convert bytes -> URL in production.
        # If you refuse external hosting, return None.
        return None

    return None
