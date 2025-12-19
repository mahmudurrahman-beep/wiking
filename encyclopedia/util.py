import os
import re
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings

def list_entries():
    """Returns a list of all names of encyclopedia entries."""
    try:
        # Try to get entries from storage
        _, filenames = default_storage.listdir("entries")
        return list(sorted(re.sub(r"\.md$", "", filename) 
                    for filename in filenames if filename.endswith(".md")))
    except (FileNotFoundError, OSError):
        # If no entries folder, return empty list or sample entries
        print("⚠️  No entries folder found")
        return []

def save_entry(title, content):
    """Saves an encyclopedia entry."""
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))

def get_entry(title):
    """Retrieves an encyclopedia entry."""
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        print(f"⚠️  Entry not found: {title}")
        return None
