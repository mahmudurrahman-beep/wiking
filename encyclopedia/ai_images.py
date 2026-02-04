# encyclopedia/ai_images.py
import os, time, random, urllib.parse
import requests

def _pollinations_url(prompt: str, width=768, height=768, model="flux", seed=None):
    seed = seed or random.randint(1, 10_000_000)
    encoded = urllib.parse.quote(prompt, safe="")
    return (
        f"https://image.pollinations.ai/prompt/{encoded}"
        f"?model={urllib.parse.quote(model)}&width={width}&height={height}&seed={seed}&nologo=true"
    )

def _hf_generate_bytes(prompt: str, model="stabilityai/sdxl-turbo", timeout=60):
    """
    Hugging Face Serverless Inference API (free tier, rate limited).
    Needs HF_TOKEN env var.
    """
    token = os.environ.get("HF_TOKEN")
    if not token:
        return None

    url = f"https://api-inference.huggingface.co/models/{model}"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"inputs": prompt}

    r = requests.post(url, headers=headers, json=payload, timeout=timeout)
    if r.status_code == 200 and r.headers.get("content-type","").startswith("image/"):
        return r.content
    return None

def fetch_image_bytes_from_url(url: str, timeout=30):
    r = requests.get(url, timeout=timeout)
    if r.status_code == 200 and r.headers.get("content-type","").startswith("image/"):
        return r.content
    return None

def generate_image_bytes(prompt: str) -> bytes | None:
    prompt = (prompt or "").strip()
    if not prompt:
        return None

    # Make short prompts more “accurate”
    if len(prompt.split()) <= 2:
        prompt = f"photorealistic, high detail: {prompt}"

    # 1) Try Pollinations (download bytes)
    try:
        url = _pollinations_url(prompt)
        img = fetch_image_bytes_from_url(url, timeout=25)
        if img:
            return img
    except:
        pass

    # 2) Try Hugging Face
    try:
        img = _hf_generate_bytes(prompt)
        if img:
            return img
    except:
        pass

    return None
