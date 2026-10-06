"""Focused release checks; not a security guarantee or an aesthetic judge."""
from pathlib import Path
import hashlib
import json
import re

root = Path(__file__).resolve().parents[1]
ignored = {'.git', 'node_modules', '__pycache__', '.hyperframes', '.thumbnails', 'snapshots'}
files = [p for p in root.rglob('*') if p.is_file() and not any(part in ignored for part in p.relative_to(root).parts)]
problems = []
text_extensions = {'.md', '.py', '.mjs', '.json', '.yaml', '.html', '.txt'}
for path in files:
    if path.suffix not in text_extensions:
        continue
    text = path.read_text(encoding='utf-8-sig')
    if re.search(r'(?i)\b[A-Z]:[\\/]', text):
        problems.append(f'Local absolute path: {path.relative_to(root)}')
    if re.search(r'gh[pousr]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{25,}', text):
        problems.append(f'Credential-like string: {path.relative_to(root)}')
    if path.suffix == '.md':
        links = re.findall(r'\]\(([^)]+)\)', text)
    elif path.suffix == '.html':
        links = re.findall(r'(?:src|href)="([^"]+)"', text)
    else:
        links = []
    for link in links:
        if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', link) or link.startswith('#'):
            continue
        destination = link.split('#')[0].split('?')[0]
        if destination and not (path.parent / destination).exists():
            problems.append(f'Broken local link: {path.relative_to(root)} -> {destination}')

demo = root / 'examples/collage-paper-study'
manifest = json.loads((demo / 'evidence/asset-hashes.json').read_text(encoding='utf8'))
for relative, expected in manifest.items():
    if hashlib.sha256((root / relative).read_bytes()).hexdigest() != expected:
        problems.append(f'Changed frozen asset: {relative}')
review = json.loads((demo / 'creative-review.json').read_text(encoding='utf8'))
artifact = demo / review['artifact']['file']
if hashlib.sha256(artifact.read_bytes()).hexdigest() != review['artifact']['sha256']:
    problems.append('Original reviewed artifact hash mismatch')
profile = json.loads((root / 'docs/style-profiles.json').read_text(encoding='utf8'))
if any('image' in item for item in profile['profiles']):
    problems.append('Style catalog unexpectedly includes historical reference image paths')
if problems:
    print('\n'.join(problems))
    raise SystemExit(1)
print(f'Public package checks passed: {len(files)} files, links, local-path/credential patterns, frozen assets and reviewed artifact.')
