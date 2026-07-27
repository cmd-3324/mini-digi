import os
import shutil
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "This command lets you clean __pycache__ directories directly & faster."

    def handle(self, *args, **options):
        self.stdout.write("Starting pycache cleanup...")
        
        # Get the project root directory (parent of manage.py)
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        deleted_count = 0
        
        # Walk through all directories starting from project root
        for root, dirs, files in os.walk(base_dir):
            for dir_name in dirs:
                if dir_name == "__pycache__":
                    cache_path = os.path.join(root, dir_name)
                    try:
                        shutil.rmtree(cache_path)
                        self.stdout.write(
                            self.style.SUCCESS(f"Removed: {cache_path}")
                        )
                        deleted_count += 1
                    except Exception as e:
                        self.stderr.write(
                            self.style.ERROR(f"Failed to remove {cache_path}: {e}")
                        )
        
        self.stdout.write(
            self.style.NOTICE(f"\nCleanup complete! Removed {deleted_count} __pycache__ directories.")
        )