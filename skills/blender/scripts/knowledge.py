"""Portable library knowledge cards; host Python or Blender, standard library only.

Each explicit library root owns knowledge/*.json and relative asset references.
Cards are the source of truth; search builds no persistent index or global registry.
"""
import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import re
import sys
import unicodedata
import uuid


LIBRARY = Path(__file__).resolve().parents[1] / 'assets' / 'library'
STOP = set('a an the and or with for of to in from is are can be by on as this that have has'.split())


def tokens(text):
    text = unicodedata.normalize('NFKC', text).casefold()
    words = re.findall(r'[a-z0-9]+|[\u3040-\u30ff\u3400-\u9fff]+', text)
    result = set()
    for word in words:
        if word in STOP:
            continue
        if re.match('[a-z0-9]', word):
            result.add(word[:-1] if len(word) > 3 and word.endswith('s') else word)
        else:
            result.update(word[i:i+2] for i in range(max(1, len(word)-1)))
    return result


def _strings(value):
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return ' '.join(_strings(v) for v in value.values())
    if isinstance(value, list):
        return ' '.join(_strings(v) for v in value)
    return ''


def cards(roots=None):
    """Read only selected libraries. Missing roots and malformed cards are errors."""
    result = []
    for root in dict.fromkeys(Path(p).resolve() for p in (roots if roots is not None else [LIBRARY])):
        if not root.is_dir():
            raise FileNotFoundError(root)
        seen = set()
        for path in sorted((root / 'knowledge').glob('*.json')):
            card = json.loads(path.read_text(encoding='utf-8-sig'))
            for key in ('id', 'kind', 'title', 'summary'):
                if not isinstance(card.get(key), str) or not card[key].strip():
                    raise ValueError(f'{path}: missing text {key}')
            if card['id'] in seen:
                raise ValueError(f'{root}: duplicate card ID {card["id"]}')
            seen.add(card['id'])
            result.append({'root': str(root), 'path': str(path), 'card': card})
    return result


def search(query='', roots=None, limit=10):
    """Lexical structural retrieval, not inferred compatibility or embedding search.

    Returns matched terms and coverage so a partial hit cannot imply all requested
    capabilities exist. Read the full card (including limits/rights) before use.
    """
    if limit < 1:
        raise ValueError('limit must be positive')
    entries = cards(roots)
    query_terms = tokens(query)
    fields = ('title', 'summary', 'terms', 'structure', 'interfaces', 'uses', 'principle')
    documents = [tokens(_strings({k: e['card'].get(k) for k in fields})) for e in entries]
    frequencies = Counter(t for doc in documents for t in doc)
    result = []
    for entry, doc in zip(entries, documents):
        matched = query_terms & doc
        if query_terms and not matched:
            continue
        score = sum(math.log(1 + len(entries) / frequencies[t]) for t in matched)
        result.append({**entry, 'score': round(score, 4), 'matched': sorted(matched),
                       'coverage': len(matched) / len(query_terms) if query_terms else 1.0})
    return sorted(result, key=lambda e: (-e['score'], e['card']['id'], e['root']))[:limit]


def save(card, root, expected_revision=None):
    """Create or deliberately revise one card in an explicit writable root.

    Single writer per library. Existing edits require the revision read by caller;
    unknown fields survive when caller updates the full loaded card. Atomic replace
    prevents a half-written JSON file; this is not a multi-writer database lock.
    """
    slug = card.get('id', '')
    if not re.fullmatch(r'[a-z0-9][a-z0-9._-]*', slug):
        raise ValueError('Use a portable lowercase ID')
    for key in ('kind', 'title', 'summary'):
        if not isinstance(card.get(key), str) or not card[key].strip():
            raise ValueError(f'missing text {key}')
    root = Path(root).resolve()
    if not root.is_dir():
        raise FileNotFoundError(root)
    folder = root / 'knowledge'
    folder.mkdir(exist_ok=True)
    path = folder / (slug + '.json')
    existing = next((e for e in cards([root]) if e['card']['id'] == slug), None)
    if existing:
        path = Path(existing['path'])
    revision = existing['card'].get('revision', 0) if existing else None
    if expected_revision != revision:
        raise ValueError(f'Card revision changed: expected {expected_revision}, found {revision}')
    card = {**card, 'revision': (revision or 0) + 1}
    temp = folder / ('.' + uuid.uuid4().hex + '.tmp')
    try:
        temp.write_text(json.dumps(card, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        temp.replace(path)
    finally:
        temp.unlink(missing_ok=True)
    return card


def fingerprint(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def resolve(entry):
    """Resolve an exact native asset; refuse changed bytes before Blender append.

    A matching digest proves identity of bytes, not license, quality or safety.
    Re-inspect a new library revision before updating the card's fingerprint.
    """
    source = entry['card']['source']
    root = Path(entry['root']).resolve()
    relative = Path(source['file'])
    path = (root / relative).resolve()
    if relative.is_absolute() or not path.is_relative_to(root):
        raise ValueError('Asset reference must stay relative to its library root')
    if fingerprint(path) != source['sha256']:
        raise ValueError(f'Stale knowledge for {path.name}; inspect source before updating card')
    return {'file': str(path), 'kind': source['kind'], 'name': source['name']}


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('query', nargs='?', default='')
    parser.add_argument('--root', action='append', type=Path, help='Repeat for project/private roots')
    parser.add_argument('--limit', type=int, default=10)
    parser.add_argument('--full', action='store_true', help='Include full cards and evidence')
    args = parser.parse_args()
    results = search(args.query, args.root, args.limit)
    if not args.full:
        results = [{'id': e['card']['id'], 'title': e['card']['title'], 'kind': e['card']['kind'],
                    'summary': e['card']['summary'], 'path': e['path'], 'root': e['root'],
                    'matched': e['matched'], 'coverage': e['coverage'], 'score': e['score']}
                   for e in results]
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
