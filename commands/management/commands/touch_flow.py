import os
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Generate flowchart.txt (icons) and flowchart-raw.txt (full tree, no object noise)."

    # Internal object databases / cache bullshit -> never walked at all.
    # Everything else (venv, __pycache__, hidden files & folders) STAYS in raw.
    NOISE_SUBTREES = {
        os.path.join('.git', 'objects'),   
        os.path.join('.git', 'lfs'),      
        # '.docker',                       
    }

    ICON_EXCLUDE = {'venv', '__pycache__', '.git'}

    def handle(self, *args, **options):
        base_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        )
        self.stdout.write("Generating project tree...")

        structure_dir = os.path.join(base_dir, "structure")
        os.makedirs(structure_dir, exist_ok=True)

        noise = {os.path.normpath(p) for p in self.NOISE_SUBTREES}

        def get_items(root_dir):
            items = []
            for root, dirs, files in os.walk(root_dir):
                rel = os.path.relpath(root, root_dir)
                if rel == '.':
                    rel = ''
                # prune noise subtrees BEFORE descending into them
                dirs[:] = [d for d in dirs
                           if os.path.normpath(os.path.join(rel, d)) not in noise]
                for d in dirs:
                    items.append((os.path.join(rel, d), True))
                for f in files:
                    items.append((os.path.join(rel, f), False))
            return items

        def build_tree(items):
            tree = {}
            for path, is_dir in items:
                parts = path.split(os.sep)
                current = tree
                for i, part in enumerate(parts):
                    current = current.setdefault(part, {})
                    if i == len(parts) - 1:
                        current['__is_dir__'] = is_dir
            return tree

        def get_icon(name, is_dir):
            if is_dir:
                return "📁"
            ext = os.path.splitext(name)[1].lower()
            if ext == '.py': return "🐍"
            if ext in ('.html', '.htm'): return "🌐"
            if ext == '.css': return "🎨"
            if ext == '.js': return "✨"
            if ext in ('.txt', '.md', '.rst'): return "📄"
            if ext in ('.webp', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico'): return "🖼️"
            if ext in ('.woff', '.woff2', '.ttf', '.otf'): return "🔤"
            if ext in ('.mp4', '.mov', '.avi'): return "🎬"
            if ext in ('.yml', '.yaml', '.json', '.xml', '.toml'): return "📝"
            if ext in ('.ps1', '.sh', '.bat', '.cmd'): return "⚙️"
            return "📄"

        def generate_lines(node, prefix='', raw=False, exclude=None):
            lines = []
            keys = [k for k in node if not k.startswith('__')]
            if exclude:
                keys = [k for k in keys if k not in exclude]
            keys.sort(key=lambda x: (not node[x].get('__is_dir__', False), x.lower()))
            for idx, key in enumerate(keys):
                is_last = idx == len(keys) - 1
                is_dir = node[key].get('__is_dir__', False)
                connector = '└── ' if is_last else '├── '
                display = key if raw else f"{get_icon(key, is_dir)} {key}"
                lines.append(prefix + connector + display)
                if is_dir:
                    lines.extend(generate_lines(
                        node[key],
                        prefix + ('    ' if is_last else '│   '),
                        raw, exclude,
                    ))
            return lines

        full_tree = build_tree(get_items(base_dir))

        
        raw_lines = generate_lines(full_tree, raw=True)
        with open(os.path.join(structure_dir, "flowchart-raw.txt"), 'w', encoding='utf-8') as f:
            f.write('\n'.join(raw_lines))

        
        icon_lines = generate_lines(full_tree, raw=False, exclude=self.ICON_EXCLUDE)
        icon_lines.insert(0, "📁")
        with open(os.path.join(structure_dir, "flowchart.txt"), 'w', encoding='utf-8') as f:
            f.write('\n'.join(icon_lines))

        self.stdout.write(self.style.SUCCESS(f"✅ flowcharts updated in {structure_dir}"))