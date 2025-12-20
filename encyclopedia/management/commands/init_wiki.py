# encyclopedia/management/commands/init_wiki.py - NEW FILE
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os
from pathlib import Path

class Command(BaseCommand):
    help = 'Initialize wiki with default data'

    def handle(self, *args, **options):
        # Create superuser if none exists
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@wiki.com',
                password='admin123'  # Change this!
            )
            self.stdout.write(self.style.SUCCESS('Created admin user'))
        
        # Ensure entries directory exists
        entries_dir = Path(__file__).parent.parent.parent.parent / 'entries'
        entries_dir.mkdir(exist_ok=True)
        
        # Create initial entries from existing MD files
        initial_entries = [
            'CSS.md',
            'Django.md', 
            'Git.md',
            'HTML.md',
            'Python.md',
            'README.md'
        ]
        
        for entry in initial_entries:
            if (entries_dir / entry).exists():
                self.stdout.write(f'✓ {entry} exists')
            else:
                self.stdout.write(f'✗ {entry} missing')
        
        self.stdout.write(self.style.SUCCESS('Wiki initialization complete!'))
