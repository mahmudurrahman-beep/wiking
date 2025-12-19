# import_entries.py - UPDATED
import os
import sys
import django
from pathlib import Path

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wiki.settings')
django.setup()

from encyclopedia.util import save_entry, ensure_entries_directory, list_entries
from encyclopedia.models import Entry
from django.contrib.auth.models import User

def copy_md_files_to_storage():
    """Copy markdown files from entries/ folder to Django storage"""
    entries_dir = ensure_entries_directory()
    
    if not os.path.exists(entries_dir):
        print(f"❌ ERROR: No entries directory found at {entries_dir}")
        return 0
    
    # Get all .md files
    md_files = [f for f in os.listdir(entries_dir) if f.endswith('.md')]
    
    if not md_files:
        print(f"⚠️  No .md files found in {entries_dir}")
        return 0
    
    copied = 0
    for filename in md_files:
        title = filename[:-3]  # Remove .md extension
        filepath = os.path.join(entries_dir, filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Save to Django storage
            save_entry(title, content)
            copied += 1
            print(f"✓ Copied: {title}")
        except Exception as e:
            print(f"✗ Failed to copy {title}: {e}")
    
    return copied

def create_database_entries():
    """Create database entries from markdown files"""
    try:
        user = User.objects.get(username='admin')
    except User.DoesNotExist:
        user = User.objects.create_user(
            'admin', 
            'admin@example.com', 
            'admin123',
            is_staff=True,
            is_superuser=True
        )
        print("Created admin user (password: admin123)")
    
    # Get entries from storage (should now have them)
    entries = list_entries()
    imported = 0
    
    for title in entries:
        if not Entry.objects.filter(title=title, user=user).exists():
            from encyclopedia.util import get_entry
            content = get_entry(title)
            if content:
                Entry.objects.create(
                    user=user,
                    title=title,
                    content=content
                )
                imported += 1
                print(f"✓ Created DB entry: {title}")
    
    return imported

def import_markdown_entries():
    """Main import function"""
    print("=== Starting Import Process ===")
    
    # Step 1: Copy .md files to Django storage
    print("\n1. Copying markdown files to storage...")
    copied = copy_md_files_to_storage()
    print(f"   Copied {copied} files")
    
    # Step 2: Create database entries
    print("\n2. Creating database entries...")
    imported = create_database_entries()
    print(f"   Created {imported} database entries")
    
    # Step 3: Verify
    print("\n3. Verification:")
    from encyclopedia.util import list_entries
    entries = list_entries()
    print(f"   Total entries available: {len(entries)}")
    print(f"   Database entries count: {Entry.objects.count()}")
    
    if entries:
        print(f"   Available entries: {', '.join(entries[:5])}")
        if len(entries) > 5:
            print(f"   ... and {len(entries)-5} more")
    
    print("\n✅ Import complete!")

if __name__ == '__main__':
    import_markdown_entries()
