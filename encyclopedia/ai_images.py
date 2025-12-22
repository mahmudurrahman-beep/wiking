import requests
import base64
import os
import time
import json

def generate_craiyon_image(prompt):
    """
    Generate AI image using Craiyon API
    Returns the image URL or None if failed
    """
    try:
        print(f"🔧 Generating AI image for prompt: '{prompt}'")
        
        # Step 1: Call Craiyon API
        craiyon_url = "https://api.craiyon.com/v3"
        
        print(f"🌐 Calling Craiyon API at {craiyon_url}")
        response = requests.post(
            craiyon_url,
            json={"prompt": prompt},
            timeout=45  # Increased timeout
        )
        
        print(f"📊 Craiyon response status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ Craiyon API error: {response.status_code}")
            print(f"Response text: {response.text[:200]}")
            return None
        
        data = response.json()
        print(f"✅ Craiyon API success, got {len(data.get('images', []))} images")
        
        # Get the first image (base64)
        if 'images' in data and len(data['images']) > 0:
            image_base64 = data['images'][0]
            print("📸 Got base64 image from Craiyon")
            
            # Step 2: Upload to ImgBB if API key exists
            imgbb_api_key = os.environ.get('IMGBB_API_KEY', '')
            
            if imgbb_api_key:
                print("🌐 Uploading to ImgBB...")
                try:
                    imgbb_response = requests.post(
                        "https://api.imgbb.com/1/upload",
                        params={"key": imgbb_api_key},
                        data={"image": image_base64},
                        timeout=30
                    )
                    
                    print(f"📊 ImgBB response status: {imgbb_response.status_code}")
                    
                    if imgbb_response.status_code == 200:
                        imgbb_data = imgbb_response.json()
                        if imgbb_data.get("success"):
                            img_url = imgbb_data["data"]["url"]
                            print(f"✅ ImgBB upload successful: {img_url[:50]}...")
                            return img_url
                        else:
                            print(f"❌ ImgBB upload failed: {imgbb_data}")
                    else:
                        print(f"❌ ImgBB API error: {imgbb_response.status_code}")
                        print(f"ImgBB response: {imgbb_response.text[:200]}")
                        
                except requests.exceptions.Timeout:
                    print("⏰ ImgBB upload timeout")
                except Exception as imgbb_error:
                    print(f"❌ ImgBB error: {imgbb_error}")
            
            # Fallback: Use base64 data URL
            print("🔄 Using base64 data URL fallback")
            return f"data:image/png;base64,{image_base64}"
        else:
            print("❌ No images in Craiyon response")
            return None
            
    except requests.exceptions.Timeout:
        print("⏰ Craiyon API timeout")
    except requests.exceptions.ConnectionError:
        print("🔌 Craiyon API connection error")
    except requests.exceptions.RequestException as req_error:
        print(f"🌐 Request error: {req_error}")
    except Exception as e:
        print(f"💥 Unexpected error in AI generation: {e}")
    
    return None
