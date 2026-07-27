

import re
import os
from datetime import datetime
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings


class Command(BaseCommand):
    help = 'Compile .po files with updated PO-Revision-Date header'

    def handle(self, *args, **options):
        # Get all locale paths from settings
        locale_paths = getattr(settings, 'LOCALE_PATHS', [])
        
        # Also check app-level locales
        for app in settings.INSTALLED_APPS:
            try:
                app_path = __import__(app).__path__[0]
                locale_path = os.path.join(app_path, 'locale')
                if os.path.exists(locale_path):
                    locale_paths.append(locale_path)
            except (ImportError, AttributeError):
                pass

        # Remove duplicates
        locale_paths = list(set(locale_paths))

        if not locale_paths:
            self.stderr.write(self.style.ERROR('No LOCALE_PATHS found.'))
            return

        now = datetime.now().strftime("%Y-%m-%d %H:%M%z")
        # Insert colon in timezone offset (e.g., +0330 -> +03:30)
        # Some tools expect this format, but we'll use simple format
        # For msgfmt, simple format works: 2026-07-04 10:00+0000

        for locale_path in locale_paths:
            po_file = os.path.join(locale_path, 'de', 'LC_MESSAGES', 'django.po')
            
            if not os.path.exists(po_file):
                self.stdout.write(self.style.WARNING(f'File not found: {po_file}'))
                continue

            with open(po_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Replace PO-Revision-Date placeholder or existing date
            pattern = r'"PO-Revision-Date: .*?\\n"'
            replacement = f'"PO-Revision-Date: {now}\\n"'

            if re.search(pattern, content):
                new_content = re.sub(pattern, replacement, content)
            else:
                # If not found, insert after Project-Id-Version or at top
                header_pattern = r'(# SOME DESCRIPTIVE TITLE\..*?"Project-Id-Version: .*?\\n")'
                if re.search(header_pattern, content, re.DOTALL):
                    new_content = re.sub(
                        header_pattern,
                        rf'\1\n"PO-Revision-Date: {now}\\n"',
                        content,
                        flags=re.DOTALL
                    )
                else:
                    # Fallback: insert after first empty msgid
                    new_content = content.replace(
                        'msgid ""\nmsgstr ""',
                        f'msgid ""\nmsgstr ""\n"PO-Revision-Date: {now}\\n"'
                    )

            with open(po_file, 'w', encoding='utf-8') as f:
                f.write(new_content)

            self.stdout.write(self.style.SUCCESS(f'Updated PO-Revision-Date in {po_file}'))

        # Now run compilemessages
        self.stdout.write(self.style.NOTICE('Compiling messages...'))
        call_command('compilemessages', verbosity=1)

        self.stdout.write(self.style.SUCCESS('✅ Done!'))