import os
import shutil

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "This command lets you clean __pycache__ directories directly & faster."

    def handle(self, *args, **options):
        self.stdout.write("Starting pycache cleanup...")

        base_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        )

        deleted_count = 0
        # Walk, walks through given path recursverly and return a tuple with items:
        # root, dir, file
        # Reason ? WE DO run manage.py cahe_cleanup in "I:\mini-digi" , so it walks through all
        # foldesr and subfoldesr of Our pwd. 
        for root, dirs, files in os.walk(base_dir):
            if "venv" in root.split(os.sep):
                continue
            for dir_name in dirs:
                if dir_name == "__pycache__":
                    cache_path = os.path.join(root, dir_name)
                    try:
                        shutil.rmtree(cache_path)
                        self.stdout.write(self.style.SUCCESS(f"Removed: {cache_path}"))
                        deleted_count += 1
                    except Exception as e:
                        self.stderr.write(
                            self.style.ERROR(f"Failed to remove {cache_path}: {e}")
                        )

        self.stdout.write(
            self.style.NOTICE(
                f"\nCleanup complete! Removed {deleted_count} __pycache__ directories."
            )
        )
# First iteration: root = "I:\mini-digi"

# root = "I:\\mini-digi"
# dirs = ["app", "utils", "venv"]       # folders inside mini-digi
# files = ["manage.py", "README.md"]    # files inside mini-digi


# Second iteration: root = "I:\mini-digi\app"
# root = "I:\\mini-digi\\app"
# dirs = ["__pycache__"]        # folder inside app
# files = ["__init__.py", "views.py"]  # files inside app


# Third iteration: root = "I:\mini-digi\app\__pycache__"


# root = "I:\\mini-digi\\app\\__pycache__"
# dirs = []                     # no subfolders
# files = ["views.cpython-311.pyc"]  # the cached files