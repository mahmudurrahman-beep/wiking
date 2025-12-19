# import_entries.py
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wiki.settings')
django.setup()

from encyclopedia.models import Entry
from django.contrib.auth.models import User
from encyclopedia.util import list_entries, get_entry

def import_markdown_entries():
    """Import all Markdown files into database"""
    
    # Get or create a default user (or use your superuser)
    try:
        user = User.objects.get(username='admin')
    except User.DoesNotExist:
        user = User.objects.create_user('admin', 'admin@example.com', 'admin123')
        print("Created admin user (password: admin123)")
    
    # Import each Markdown file
    entries = list_entries()
    imported = 0
    
    for entry_title in entries:
        # Check if entry already exists in database
        if not Entry.objects.filter(title=entry_title, user=user).exists():
            content = get_entry(entry_title)
            if content:
                Entry.objects.create(
                    user=user,
                    title=entry_title,
                    content=content
                )
                imported += 1
                print(f"✓ Imported: {entry_title}")
    
    print(f"\n✅ Import complete! {imported} entries imported.")
    print(f"Total entries in database: {Entry.objects.count()}")

if __name__ == '__main__':
    import_markdown_entries()
