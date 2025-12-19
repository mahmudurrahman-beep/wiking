"""
Utility functions for the encyclopedia app.
Optimized for Render.com deployment
"""

import os
import re
from pathlib import Path
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings

# ====== FILE SYSTEM HELPERS ======

def ensure_entries_directory():
    """
    Ensure entries directory exists in media folder.
    Returns: Path to entries directory
    """
    # Get media root from settings
    media_root = Path(settings.MEDIA_ROOT) if hasattr(settings, 'MEDIA_ROOT') else Path(settings.BASE_DIR) / 'media'
    
    # Create entries directory inside media
    entries_dir = media_root / 'entries'
    entries_dir.mkdir(parents=True, exist_ok=True)
    
    # Also ensure Django storage knows about it
    try:
        default_storage.save('entries/.keep', ContentFile(''))
    except:
        pass  # Ignore if already exists
    
    return str(entries_dir)

def get_entries_from_filesystem():
    """
    Get entries directly from filesystem (fallback for Render).
    Returns: List of entry titles
    """
    entries_dir = ensure_entries_directory()
    
    if not os.path.exists(entries_dir):
        return []
    
    # Get all .md files
    filenames = [f for f in os.listdir(entries_dir) if f.endswith('.md')]
    
    # Remove .md extension and sort
    return sorted([re.sub(r"\.md$", "", filename) for filename in filenames])

# ====== MAIN ENTRY FUNCTIONS ======

def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    Tries Django storage first, falls back to filesystem for Render.
    """
    try:
        # Try Django default storage (works in development)
        _, filenames = default_storage.listdir("entries")
        
        # Filter only .md files and remove extension
        entries = [
            re.sub(r"\.md$", "", filename) 
            for filename in filenames 
            if filename.endswith(".md")
        ]
        
        # If found entries, return sorted list
        if entries:
            return sorted(entries)
        
    except (FileNotFoundError, OSError, NotImplementedError):
        # Django storage failed, fall back to filesystem
        pass
    
    # Fallback: get from filesystem (Render-compatible)
    return get_entries_from_filesystem()

def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown content.
    Saves to both Django storage AND filesystem for Render compatibility.
    """
    # 1. Save to Django storage
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))
    
    # 2. ALSO save to filesystem (for Render persistence)
    entries_dir = ensure_entries_directory()
    fs_filename = os.path.join(entries_dir, f"{title}.md")
    
    with open(fs_filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title.
    Tries Django storage first, falls back to filesystem.
    """
    # 1. Try Django storage
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except (FileNotFoundError, OSError):
        # 2. Fall back to filesystem
        entries_dir = ensure_entries_directory()
        fs_filename = os.path.join(entries_dir, f"{title}.md")
        
        if os.path.exists(fs_filename):
            try:
                with open(fs_filename, 'r', encoding='utf-8') as f:
                    return f.read()
            except:
                return None
    
    return None

def delete_entry(title):
    """
    Deletes an encyclopedia entry by title.
    Removes from both Django storage AND filesystem.
    """
    # 1. Delete from Django storage
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    
    # 2. Delete from filesystem
    entries_dir = ensure_entries_directory()
    fs_filename = os.path.join(entries_dir, f"{title}.md")
    
    if os.path.exists(fs_filename):
        os.remove(fs_filename)
    
    return True

# ====== HELPER FUNCTIONS ======

def entry_exists(title):
    """Check if an entry exists"""
    # Check Django storage
    if default_storage.exists(f"entries/{title}.md"):
        return True
    
    # Check filesystem
    entries_dir = ensure_entries_directory()
    fs_filename = os.path.join(entries_dir, f"{title}.md")
    
    return os.path.exists(fs_filename)

def get_all_entries_with_content():
    """Get all entries with their content (for debugging)"""
    entries = list_entries()
    result = []
    
    for title in entries:
        content = get_entry(title)
        if content:
            result.append({
                'title': title,
                'content_preview': content[:100] + '...' if len(content) > 100 else content,
                'length': len(content)
            })
    
    return result
