# encyclopedia/util.py - UPDATED FOR RENDER
import os
import re
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

def ensure_entries_directory():
    """Ensure entries directory exists (for Render compatibility)"""
    entries_dir = os.path.join(settings.BASE_DIR, 'entries')
    if not os.path.exists(entries_dir):
        os.makedirs(entries_dir, exist_ok=True)
        print(f"Created entries directory: {entries_dir}")
    return entries_dir

def list_entries():
    """Returns a list of all names of encyclopedia entries."""
    try:
        # Try the normal Django storage way
        _, filenames = default_storage.listdir("entries")
        entries = list(sorted(re.sub(r"\.md$", "", filename) 
                    for filename in filenames if filename.endswith(".md")))
        
        # If no entries found, check filesystem directly (for Render)
        if not entries:
            entries_dir = ensure_entries_directory()
            if os.path.exists(entries_dir):
                filenames = os.listdir(entries_dir)
                entries = list(sorted(re.sub(r"\.md$", "", filename) 
                            for filename in filenames if filename.endswith(".md")))
        
        return entries
    except (FileNotFoundError, OSError):
        # Fallback to filesystem for Render
        entries_dir = ensure_entries_directory()
        if os.path.exists(entries_dir):
            filenames = os.listdir(entries_dir)
            return list(sorted(re.sub(r"\.md$", "", filename) 
                        for filename in filenames if filename.endswith(".md")))
        return []

def save_entry(title, content):
    """Saves an encyclopedia entry, given its title and Markdown content."""
    filename = f"entries/{title}.md"
    
    # Save to Django storage
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))
    
    # ALSO save to filesystem for Render persistence
    entries_dir = ensure_entries_directory()
    fs_filename = os.path.join(entries_dir, f"{title}.md")
    with open(fs_filename, 'w', encoding='utf-8') as f:
        f.write(content)

def get_entry(title):
    """Retrieves an encyclopedia entry by its title."""
    try:
        # Try Django storage first
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        # Fallback to filesystem for Render
        entries_dir = ensure_entries_directory()
        fs_filename = os.path.join(entries_dir, f"{title}.md")
        if os.path.exists(fs_filename):
            with open(fs_filename, 'r', encoding='utf-8') as f:
                return f.read()
        return None
