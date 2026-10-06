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

showcase = json.loads((root / 'library/showcase.json').read_text(encoding='utf8'))
cases = showcase['cases']
case_ids = [case['id'] for case in cases]
if len(set(case_ids)) != len(case_ids):
    problems.append('Duplicate showcase IDs')
families = {case['family'] for case in cases}
for case in cases:
    for field in ('video', 'poster', 'prompt', 'credits', 'media'):
        destination = (root / case[field]).resolve()
        if not destination.is_relative_to(root) or not destination.is_file():
            problems.append(f'Invalid showcase asset: {case["id"]} / {field}')
    if not case.get('exposure') or not case.get('limit'):
        problems.append(f'Missing input boundary or limitation: {case["id"]}')
    movie = root / case['video']
    if movie.is_file() and (root / case['media']).is_file():
        metadata = json.loads((root / case['media']).read_text(encoding='utf8'))
        if hashlib.sha256(movie.read_bytes()).hexdigest() != metadata['delivery_sha256']:
            problems.append(f'Gallery delivery hash mismatch: {case["id"]}')
        if not metadata['reencoded'] and metadata['source_sha256'] != metadata['delivery_sha256']:
            problems.append(f'Unmodified movie source mismatch: {case["id"]}')
        video_streams = [s for s in metadata['measurements']['streams'] if s.get('width', 0) > 0 and s.get('height', 0) > 0]
        if not video_streams or float(metadata['measurements']['format']['duration']) <= 0:
            problems.append(f'Invalid gallery media measurements: {case["id"]}')

profile_ids = {item['id'] for item in profile['profiles']}
for item in profile['profiles']:
    if item.get('origin_type') not in {'external_work', 'third_party_tutorial', 'participating_author_project', 'own_adaptation'}:
        problems.append(f'Unknown research origin: {item["id"]}')
    if not item.get('implementation_status'):
        problems.append(f'Missing implementation boundary: {item["id"]}')
    if item.get('application_sample') and not (root / item['application_sample']).is_file():
        problems.append(f'Missing profile application sample: {item["id"]}')
recipes = json.loads((root / 'library/material-prompts.json').read_text(encoding='utf8'))['entries']
experimental_recipes = json.loads((root / 'library/experiment-material-prompts.json').read_text(encoding='utf8'))['entries']
for recipe in recipes:
    if recipe.get('source_profile') not in profile_ids:
        problems.append(f'Unknown research recipe profile: {recipe["id"]}')
    if not recipe.get('acceptance') or not recipe.get('basis'):
        problems.append(f'Missing recipe basis/acceptance: {recipe["id"]}')
for recipe in experimental_recipes:
    if recipe['based_on_case'] not in case_ids or recipe['style'] not in families:
        problems.append(f'Unknown experimental recipe case/style: {recipe["id"]}')
recipes = recipes + experimental_recipes
if len({recipe['id'] for recipe in recipes}) != len(recipes):
    problems.append('Duplicate material recipe IDs')
for recipe in recipes:
    if set(re.findall(r'\{([^{}]+)\}', recipe['prompt'])) != set(recipe['variables']):
        problems.append(f'Recipe placeholder mismatch: {recipe["id"]}')
    status = recipe['validation_status']
    if status not in {'authored_after_example_not_generation_tested', 'authored_from_reference_not_generation_tested', 'generation_tested_with_evidence', 'implementation_tested_with_evidence'}:
        problems.append(f'Unknown recipe validation status: {recipe["id"]}')
    if status in {'generation_tested_with_evidence', 'implementation_tested_with_evidence'}:
        evidence = recipe.get('evidence')
        if not evidence or not (root / evidence).is_file():
            problems.append(f'Tested recipe lacks evidence: {recipe["id"]}')
        elif recipe.get('source_profile'):
            report = json.loads((root / evidence).read_text(encoding='utf8'))
            matching = [x for x in report['recipe_execution'] if x['recipe_id'] == recipe['id']]
            if len(matching) != 1 or matching[0]['validation_status'] != status or matching[0]['observed_result'] != recipe.get('validation_result'):
                problems.append(f'Recipe evidence disagrees with actual execution: {recipe["id"]}')
    if recipe.get('test_attempt'):
        evidence = recipe['test_attempt'].get('evidence')
        if not evidence or not (root / evidence).is_file():
            problems.append(f'Blocked recipe lacks attempted-test evidence: {recipe["id"]}')

audit = root / 'examples/style-prompt-audit'
audit_manifest = json.loads((audit / 'manifest.json').read_text(encoding='utf8'))
audit_cases = json.loads((audit / 'cases.json').read_text(encoding='utf8'))['cases']
audit_ids = {x['id'] for x in audit_cases}
if audit_ids != {x['id'] for x in audit_manifest['cases']}:
    problems.append('Probe artifact IDs disagree with frozen input IDs')
audit_entries = {x['id']: x for x in recipes if x.get('source_profile')}
for frozen in audit_manifest['cases']:
    folder = audit / frozen['id']
    for filename, hash_key in [('input.json','input_sha256'),('existing-style-card.json','style_card_sha256')]:
        if hashlib.sha256((folder / filename).read_bytes()).hexdigest() != frozen[hash_key]:
            problems.append(f'Changed frozen probe input: {frozen["id"]}/{filename}')
    for prompt in json.loads((folder/'input.json').read_text(encoding='utf8'))['recipes']:
        current = audit_entries.get(prompt['id'], {})
        if any(current.get(field) != prompt.get(field) for field in ('prompt','variables','acceptance','source_profile')):
            problems.append(f'Tested prompt changed silently: {prompt["id"]}')
    artifact = next(x for x in audit_cases if x['id'] == frozen['id'])
    if hashlib.sha256((root / artifact['video']).read_bytes()).hexdigest() != artifact['delivery_sha256']:
        problems.append(f'Probe movie hash mismatch: {frozen["id"]}')
    if hashlib.sha256((folder/'index.html').read_bytes()).hexdigest() != artifact['source_portable_sha256']:
        problems.append(f'Probe portable source hash mismatch: {frozen["id"]}')
    if (folder/'generation.json').is_file():
        gen = json.loads((folder/'generation.json').read_text(encoding='utf8'))
        if hashlib.sha256((folder/gen['asset']).read_bytes()).hexdigest() != gen['sha256']:
            problems.append(f'Raw generated image changed: {frozen["id"]}')
    media = json.loads((folder/'measurements.json').read_text(encoding='utf8'))
    video = [s for s in media['streams'] if s.get('codec_type')=='video']
    if len(media['streams']) != 1 or len(video) != 1 or (video[0]['width'],video[0]['height'],video[0]['r_frame_rate'],video[0]['nb_frames']) != (1280,720,'30/1','180') or float(media['format']['duration']) != 6:
        problems.append(f'Probe media contract mismatch: {frozen["id"]}')
if any((audit/x).exists() for x in ('review/references', 'references')) or list(audit.rglob('*.ttc')):
    problems.append('Probe export unexpectedly includes local reference pixels or private font files')
if problems:
    print('\n'.join(problems))
    raise SystemExit(1)
print(f'Public package checks passed: {len(files)} files, {len(cases)} gallery cases, {len(recipes)} recipes, links, local-path/credential patterns and artifact hashes.')
