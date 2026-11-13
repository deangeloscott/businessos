"""The example business: a made-up organization, filled in, that anyone can open to see what AURA looks like in use.

It is built from a plain seed (examples/<name>/example.json plus its files) through the same helpers
real work uses, so every record is validated like any other, and dates are set relative to the day it is
built. It lives in its own workspace, never inside someone's real one, and is labelled as an example
wherever it appears. Nothing in it is a result AURA achieved for anyone.
"""
import argparse
import json
import os
import re
import shutil
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

PRODUCT = Path(__file__).resolve().parents[1]
DEFAULT = 'harbor-pine-bakery'
MARKER = '.businessos/example.json'
TOKEN = re.compile(r'\{\{now(?:([+-])(\d+)([dh]))?(?:@(\d{2}):(\d{2}))?\}\}')


def seed_folder(name=DEFAULT):
    if not re.fullmatch(r'[a-z0-9-]{1,60}', str(name)):raise ValueError('Choose a valid example.')
    folder = PRODUCT / 'examples' / name
    if not (folder / 'example.json').is_file():raise ValueError('This example is not available in this copy of AURA.')
    return folder


def dated(value, at):
    """Replace {{now-3d}}, {{now+6d}} or {{now-1d@05:40}} anywhere in the seed with real dates."""
    def swap(match):
        sign, amount, unit, hour, minute = match.groups()
        when = at
        if amount:when += (1 if sign == '+' else -1) * (timedelta(days=int(amount)) if unit == 'd' else timedelta(hours=int(amount)))
        if hour:when = when.replace(hour=int(hour), minute=int(minute), second=0)
        return when.isoformat(timespec='seconds').replace('+00:00', 'Z')
    if isinstance(value, str):return TOKEN.sub(swap, value)
    if isinstance(value, list):return [dated(v, at) for v in value]
    if isinstance(value, dict):return {k: dated(v, at) for k, v in value.items()}
    return value


def _tokens(value, names):
    """Replace {{collection:key}} and {{business}} with the identities created while building."""
    if isinstance(value, str):
        for key, real in names.items():value = value.replace('{{' + key + '}}', real)
        return value
    if isinstance(value, list):return [_tokens(v, names) for v in value]
    if isinstance(value, dict):return {k: _tokens(v, names) for k, v in value.items()}
    return value


def build(destination, name=DEFAULT, at=None):
    """Create the example workspace in an empty folder. The caller's process must not have another workspace in use."""
    folder = seed_folder(name);destination = Path(destination).expanduser().resolve()
    if destination.is_relative_to(PRODUCT):raise ValueError('Choose a folder outside the AURA application.')
    if destination.exists() and any(destination.iterdir()):raise ValueError('That folder already has something in it. Choose an empty folder.')
    at = at or datetime.now(timezone.utc)
    seed = dated(json.loads((folder / 'example.json').read_text(encoding='utf-8')), at)
    os.environ.update(BUSINESSOS_WORKSPACE=str(destination), BUSINESSOS_WORKSPACE_CONFIG=str(destination / '.businessos/workspace.json'))
    sys.path.insert(0, str(PRODUCT / 'scripts'))
    from setup import setup
    from remember import remember
    from persist_research_bundle import persist
    from upsert_attention import upsert
    from validate_business import validate_business
    import workspace_collections as collections
    import workspace_focus as focus
    import workspace_goals as goals
    import workspace_storage
    try:
        bid = setup(organization=seed['name'], write_link=False)['business_id']
        names = {'business': bid, 'work': f'attachments/{bid}/work'}
        business = next(o for o, _ in __import__('_common').object_index(bid).values() if o['object_type'] == 'Business')
        remember(bid, {'provenance': {'method': 'ad_hoc'}, 'objects': [{'object_ref': business['id'], 'content': {
            'description': seed['description'], 'extensions': {'businessos': {'example': {'name': name, 'built_at': at.isoformat(timespec='seconds').replace('+00:00', 'Z')}}}}}]})
        if seed.get('focus'):focus.save(bid, seed['focus'])

        # The example's own files: invented source documents and finished sample work.
        work = destination / 'attachments' / bid / 'work'
        if (folder / 'files').is_dir():shutil.copytree(folder / 'files', work, dirs_exist_ok=True)

        # Collections first, so findings can link to the watch they belong to.
        made = {}
        for c in seed.get('collections', []):
            made[c['key']] = collections.create(bid, {k: c[k] for k in ('key', 'name', 'purpose', 'mode') if k in c})
            names['collection:' + c['key']] = made[c['key']]['id']
        seed = _tokens(seed, names)

        for payload in seed.get('memory', []):remember(bid, {'provenance': {'method': 'ad_hoc'}, **payload})
        for bundle in seed.get('research', []):persist(bid, bundle)
        # Records that point at the research above, such as proof for a claim.
        for payload in seed.get('memory_after', []):remember(bid, {'provenance': {'method': 'ad_hoc'}, **payload})
        for goal in seed.get('goals', []):
            saved = goals.save(bid, {'scope': 'workspace', **{k: goal[k] for k in ('name', 'measure') if k in goal}})
            for point in goal.get('measurements', []):
                remember(bid, {'objects': [{'object_type': 'MetricObservation', 'content': {'metric_ref': saved['metric_refs'][0], **point}}]})
        for item in seed.get('attention', []):
            upsert(bid, item['key'], item['type'], item['severity'], item['title'], item['reason'], item.get('recommended_action'))

        # Each run is saved as of its own moment, so a watch shows a few days of real history.
        clock = collections.now
        try:
            for c in seed.get('collections', []):
                for number, run in enumerate(c.get('runs', []), 1):
                    collections.now = lambda moment=run['at']: moment
                    shown = collections.show(bid, made[c['key']]['id'])
                    collections.apply(bid, shown['id'], {'revision': shown['revision'], 'run_id': f"example-{c['key']}-{number}", 'items': run['items'],
                                                         **{k: run[k] for k in ('coverage', 'status', 'upkeep') if k in run}})
        finally:collections.now = clock

        if seed.get('agents'):
            view = workspace_storage.view_preferences(destination)
            view['assistants'] = {bid: [{'id': 'agt_example_' + str(n), 'updated': at.timestamp(), **a} for n, a in enumerate(seed['agents'], 1)]}
            workspace_storage.save_view(destination, view)
            workspace_storage.view_preferences(destination)  # reads back through the same validation real agents get

        errors, _, counts = validate_business(bid, True)
        if errors:raise ValueError('The example did not pass validation: ' + '; '.join(errors[:5]))
        marker = destination / MARKER;marker.parent.mkdir(parents=True, exist_ok=True)
        marker.write_text(json.dumps({'example': name, 'business_id': bid, 'built_at': at.isoformat(timespec='seconds').replace('+00:00', 'Z')}, indent=2) + '\n', encoding='utf-8')
        return {'path': str(destination), 'business_id': bid, 'records': sum(counts.values())}
    except Exception:
        # A half-built example would look like a broken workspace; leave nothing behind.
        shutil.rmtree(destination, ignore_errors=True)
        raise


def existing(home, name=DEFAULT):
    """Example workspaces already built in a folder, newest first."""
    found = []
    for folder in sorted(Path(home).iterdir()) if Path(home).is_dir() else []:
        try:info = json.loads((folder / MARKER).read_text(encoding='utf-8'))
        except (OSError, ValueError):continue
        if isinstance(info, dict) and info.get('example') == name and isinstance(info.get('built_at'), str):found.append({'path': str(folder), **info})
    return sorted(found, key=lambda e: e['built_at'], reverse=True)


def free_folder(home, name=DEFAULT):
    base = 'Example - ' + name.replace('-', ' ').title();target = Path(home) / base;n = 2
    while target.exists():target = Path(home) / f'{base} ({n})';n += 1
    return target


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('action', choices=['build'])
    p.add_argument('--destination', required=True, help='An empty folder for the example workspace')
    p.add_argument('--example', default=DEFAULT)
    a = p.parse_args()
    print(json.dumps(build(a.destination, a.example), ensure_ascii=False))


if __name__ == '__main__':
    try:main()
    except (ValueError, OSError) as e:raise SystemExit(str(e))
