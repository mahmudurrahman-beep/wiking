# encyclopedia/storage.py - COMPLETE FIXED VERSION
"""
Handles reading/writing markdown files and syncing with GitHub
"""
import os
import requests
import base64
from django.conf import settings  # THIS LINE IS CRITICAL
import subprocess
from pathlib import Path
from datetime import datetime

# ===== GITHUB SETTINGS =====
# Get from Django settings (which get from environment variables)
GITHUB_TOKEN = getattr(settings, 'GITHUB_TOKEN', '')
GITHUB_REPO_OWNER = getattr(settings, 'GITHUB_REPO_OWNER', '')
GITHUB_REPO_NAME = getattr(settings, 'GITHUB_REPO_NAME', '')

def get_entries_dir():
    """Get the path to entries directory"""
    return Path(settings.BASE_DIR) / 'entries'

def get_entry_content(title):
    """Read an entry from MD file"""
    filepath = get_entries_dir() / f"{title}.md"
    if filepath.exists():
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        # Remove title header if it's the first line
        if content.startswith(f'# {title}\n'):
            content = content[len(f'# {title}\n'):]
        elif content.startswith(f'# {title}\r\n'):
            content = content[len(f'# {title}\r\n'):]
        return content.strip()
    return None

def save_entry_locally(title, content):
    """Save entry to local MD file"""
    entries_dir = get_entries_dir()
    entries_dir.mkdir(exist_ok=True)
    
    filepath = entries_dir / f"{title}.md"
    
    # Write with title as header
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"# {title}\n\n")
        f.write(content)
    
    return str(filepath)

def get_all_titles():
    """Get all entry titles from local MD files"""
    entries_dir = get_entries_dir()
    titles = []
    if entries_dir.exists():
        for file in entries_dir.iterdir():
            if file.suffix == '.md':
                titles.append(file.stem)  # Remove .md extension
    return sorted(titles)

def sync_with_github(title, content, username=""):
    """
    Sync a file with GitHub using GitHub API
    Returns True if successful, False otherwise
    """
    # Check if GitHub sync is configured
    if not GITHUB_TOKEN or not GITHUB_REPO_OWNER or not GITHUB_REPO_NAME:
        print("⚠️ GitHub sync disabled - environment variables not set")
        print(f"   GITHUB_TOKEN: {'Set' if GITHUB_TOKEN else 'NOT SET'}")
        print(f"   GITHUB_REPO_OWNER: {GITHUB_REPO_OWNER or 'NOT SET'}")
        print(f"   GITHUB_REPO_NAME: {GITHUB_REPO_NAME or 'NOT SET'}")
        return False
    
    # Prepare the file content
    file_content = f"# {title}\n\n{content}"
    encoded_content = base64.b64encode(file_content.encode('utf-8')).decode('utf-8')
    
    # GitHub API URL
    path = f"entries/{title}.md"
    url = f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/contents/{path}"
    
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    try:
        # Check if file exists
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            # Update existing file
            sha = response.json()['sha']
            data = {
                'message': f'Update {title}' + (f' by {username}' if username else ''),
                'content': encoded_content,
                'sha': sha
            }
            response = requests.put(url, json=data, headers=headers, timeout=30)
        elif response.status_code == 404:
            # Create new file
            data = {
                'message': f'Create {title}' + (f' by {username}' if username else ''),
                'content': encoded_content
            }
            response = requests.put(url, json=data, headers=headers, timeout=30)
        else:
            print(f"❌ GitHub API error (check): {response.status_code}")
            if response.status_code == 401:
                print("   Authentication failed - check GITHUB_TOKEN")
            elif response.status_code == 403:
                print("   Permission denied - token needs 'repo' scope")
            return False
        
        if response.status_code in [200, 201]:
            print(f"✅ GitHub sync successful for '{title}'")
            return True
        else:
            print(f"❌ GitHub sync failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
            
    except requests.exceptions.Timeout:
        print("⏰ GitHub sync timeout")
        return False
    except Exception as e:
        print(f"💥 GitHub sync error: {type(e).__name__}: {e}")
        return False

def git_pull_latest():
    """
    Simplified git pull - always succeeds
    """
    print("ℹ️ GitHub sync via API - skipping git pull")
    return True
