# encyclopedia/storage.py - NEW FILE
"""
Handles reading/writing markdown files and syncing with GitHub
"""
import os
import requests
import base64
from django.conf import settings
import subprocess
from pathlib import Path

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
    token = settings.GITHUB_TOKEN
    if not token:
        return False
    
    owner = settings.GITHUB_REPO_OWNER
    repo = settings.GITHUB_REPO_NAME
    
    if not owner or not repo:
        return False
    
    # Prepare the file content
    file_content = f"# {title}\n\n{content}"
    encoded_content = base64.b64encode(file_content.encode('utf-8')).decode('utf-8')
    
    # GitHub API URL
    path = f"entries/{title}.md"
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    try:
        # Check if file exists
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            # Update existing file
            sha = response.json()['sha']
            data = {
                'message': f'Update {title}' + (f' by {username}' if username else ''),
                'content': encoded_content,
                'sha': sha
            }
            response = requests.put(url, json=data, headers=headers)
        else:
            # Create new file
            data = {
                'message': f'Create {title}' + (f' by {username}' if username else ''),
                'content': encoded_content
            }
            response = requests.put(url, json=data, headers=headers)
        
        return response.status_code in [200, 201]
    except Exception as e:
        print(f"GitHub sync error: {e}")
        return False

# In encyclopedia/storage.py
def git_pull_latest():
    """Pull latest changes ONLY when needed (not on every startup)"""
    try:
        # Skip git operations if we're in a build/deploy environment
        if os.environ.get('RENDER'):
            print("⚠️  Skipping git pull during Render build/runtime")
            return True
            
        # Only run git operations if .git exists
        if not os.path.exists('.git'):
            print("Not a git repository, skipping pull")
            return True
            
        import subprocess
        
        # Save current state
        status = subprocess.run(
            ['git', 'status', '--porcelain'],
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        
        # If there are no changes, we can pull safely
        if not status.stdout.strip():
            print("✓ Repository clean, pulling latest...")
            result = subprocess.run(
                ['git', 'pull', '--ff-only'],
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            if result.returncode == 0:
                print("✓ Pull successful")
                return True
            else:
                print(f"⚠️  Pull failed: {result.stderr}")
                return False
        else:
            print("⚠️  Repository has uncommitted changes, skipping pull")
            print(f"Changes detected:\n{status.stdout}")
            return False
            
    except Exception as e:
        print(f"⚠️  Git check failed (non-critical): {e}")
        return False  # Don't crash the app on git errors
