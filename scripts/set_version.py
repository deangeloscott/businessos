#!/usr/bin/env python3
"""Prepare a release number in one step: VERSION, the two files that repeat it, and the changelog's Unreleased heading.

    python scripts/set_version.py 0.7.6

Then commit and push the matching tag (`v0.7.6`); the release workflow does the rest.
"""
from datetime import date
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def set_version(number, today=None):
    if not re.fullmatch(r'0\.\d+\.\d+', number):
        raise SystemExit('Give the new version as 0.X.Y.')
    changelog = ROOT / 'CHANGELOG.md'
    text = changelog.read_text(encoding='utf-8')
    if re.search(r'^## ' + re.escape(number) + r'\b', text, re.M):
        raise SystemExit(f'CHANGELOG.md already has {number}.')
    if not re.search(r'^## Unreleased\s*$', text, re.M):
        raise SystemExit('Add the changes under "## Unreleased" in CHANGELOG.md first.')
    changelog.write_text(re.sub(r'^## Unreleased\s*$', f'## {number} Alpha — {(today or date.today()).isoformat()}',
                                text, count=1, flags=re.M), encoding='utf-8')
    (ROOT / 'VERSION').write_text(number + '\n', encoding='utf-8')
    for name, key in (('INSTALLATION.json', 'source_version'), ('SYSTEM-MANIFEST.json', 'version')):
        path = ROOT / name
        data = json.loads(path.read_text(encoding='utf-8'))
        data[key] = number
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    return f'AURA is now {number}. Commit, then push the tag v{number} to release it.'


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    print(set_version(sys.argv[1]))
