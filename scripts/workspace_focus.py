"""An organization's focus: its own description plus the focus areas it chose.

Focus areas are plain Markdown files (see focus-areas/README.md). They change emphasis, never
capability: the model receives short guidance and pointers, and the interface orders and suggests.
The choice is saved on the Business record, so it travels with the workspace like other memory.
"""
import argparse
import json
import re
from pathlib import Path

import yaml

from _common import PRODUCT_ROOT, workspace_root, workspace_scope, object_index

BUILT_IN = PRODUCT_ROOT / 'focus-areas'
KINDS = {'once', 'watch'}
DIRECTIONS = {'higher_better', 'lower_better'}
VIEWS = {'map', 'chart', 'board'}
GUIDANCE_LIMIT = 2000


def own_folder():
    return workspace_root() / 'knowledge' / 'focus-areas'


def _parse(path, origin):
    text = path.read_text(encoding='utf-8')
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n?(.*)$', text, re.S)
    if not match:raise ValueError(f'{path.name} needs front matter between --- lines.')
    meta = yaml.safe_load(match[1]) or {}
    if not isinstance(meta, dict) or not isinstance(meta.get('name'), str) or not meta['name'].strip():
        raise ValueError(f'{path.name} needs a name.')
    guidance = match[2].strip()
    if len(guidance) > GUIDANCE_LIMIT:raise ValueError(f'{path.name}: keep the guidance under {GUIDANCE_LIMIT} characters.')
    starts = meta.get('quick_starts') or []
    if not isinstance(starts, list) or len(starts) > 3:raise ValueError(f'{path.name}: offer up to three quick starts.')
    for s in starts:
        if not isinstance(s, dict) or not s.get('title') or not s.get('prompt') or s.get('kind', 'once') not in KINDS:
            raise ValueError(f'{path.name}: each quick start needs a title, a prompt, and kind once or watch.')
    goals = meta.get('goals') or []
    if not isinstance(goals, list) or len(goals) > 5:raise ValueError(f'{path.name}: suggest up to five goals.')
    for g in goals:
        if not isinstance(g, dict) or not g.get('name') or not g.get('measure') or g.get('direction') not in DIRECTIONS or not isinstance(g.get('target'), (int, float)):
            raise ValueError(f'{path.name}: each goal needs a name, a measure, a direction and a numeric target.')
    return {'id': path.stem, 'name': meta['name'].strip(), 'summary': str(meta.get('summary', '')).strip(), 'origin': origin,
            'keywords': [str(k).lower() for k in meta.get('keywords') or []], 'views': [v for v in meta.get('views') or [] if v in VIEWS],
            'knowledge': [str(k) for k in meta.get('knowledge') or []], 'quick_starts': [{**s, 'kind': s.get('kind', 'once')} for s in starts],
            'goals': goals, 'guidance': guidance, 'path': str(path), **({'source': meta['source']} if isinstance(meta.get('source'), dict) else {})}


def areas():
    """Every available area; a workspace file with a built-in area's name replaces it there."""
    found, problems = {}, []
    for folder, origin in ((BUILT_IN, 'built-in'), (own_folder(), 'yours')):
        for path in sorted(folder.glob('*.md')) if folder.is_dir() else []:
            if path.name.lower() == 'readme.md':continue
            try:
                area = _parse(path, origin)
                if origin == 'yours' and area.get('source'):area['origin'] = 'imported'
                if origin == 'yours' and path.stem in found:area['customized'] = True
                found[path.stem] = area
            except (OSError, ValueError, yaml.YAMLError) as error:
                problems.append(str(error) if isinstance(error, ValueError) else f'{path.name} could not be read.')
    return list(found.values()), problems


def _business(bid):
    return next(((o, p) for o, p in object_index(bid).values() if o.get('object_type') == 'Business'), (None, None))


def get(bid):
    obj, _ = _business(bid)
    if not obj:raise ValueError('This business is unavailable in the selected workspace.')
    chosen = ((obj.get('extensions') or {}).get('businessos') or {}).get('focus_areas') or []
    available, problems = areas()
    index = {a['id']: a for a in available}
    return {'description': obj.get('description', ''), 'areas': [index[i] for i in chosen if i in index],
            'missing': [i for i in chosen if i not in index], 'available': available, 'problems': problems}


def save(bid, area_ids):
    from remember import remember
    if not isinstance(area_ids, list) or len(area_ids) > 12 or any(not isinstance(i, str) for i in area_ids):
        raise ValueError('Choose up to 12 focus areas.')
    known = {a['id'] for a in areas()[0]}
    unknown = [i for i in area_ids if i not in known]
    if unknown:raise ValueError('Some focus areas are no longer available. Refresh and choose again.')
    obj, _ = _business(bid)
    if not obj:raise ValueError('This business is unavailable in the selected workspace.')
    remember(bid, {'objects': [{'object_ref': obj['id'], 'content': {'extensions': {'businessos': {'focus_areas': list(dict.fromkeys(area_ids))}}}}]})
    return get(bid)


def suggest(text, limit=4):
    """Areas whose words appear in a description. A quick offline starting point; the AI can do better."""
    words = ' ' + re.sub(r'[^a-z0-9()]+', ' ', str(text or '').lower()) + ' '
    scored = []
    for area in areas()[0]:
        terms = set(area['keywords']) | {area['name'].lower()}
        score = sum(2 if len(t) > 6 else 1 for t in terms if f' {re.sub(r"[^a-z0-9()]+", " ", t).strip()} ' in words)
        if score:scored.append((score, area['id']))
    return [i for _, i in sorted(scored, key=lambda s: -s[0])[:limit]]


def quick_starts(focus, limit=3):
    """Up to three overall, taking each chosen area's first ideas in turn so no area crowds out the rest."""
    pools = [[{**s, 'area': a['name']} for s in a['quick_starts']] for a in focus['areas']]
    out = []
    while any(pools) and len(out) < limit:
        for pool in pools:
            if pool and len(out) < limit:out.append(pool.pop(0))
    return out


def suggested_goals(focus):
    return [{**g, 'area': a['name']} for a in focus['areas'] for g in a['goals']]


def context(bid, limit=1800):
    """Short focus text for a request. Specific facts saved about the organization take priority."""
    try:focus = get(bid)
    except ValueError:return ''
    if not focus['areas']:return ''
    lines = [f'Organization focus areas: {", ".join(a["name"] for a in focus["areas"])}. '
             'They are general emphasis, not rules; facts saved about this organization take priority.']
    for a in focus['areas']:
        first = a['guidance'].split('\n\n')[0]
        lines.append(f'- {a["name"]}: {first[:420]}' + (f' (more: {a["path"]})' if len(a['guidance']) > len(first) or a['knowledge'] else ''))
    text = '\n'.join(lines)
    return text[:limit]


def public(focus):
    """What the interface and API show: no file paths beyond each area's own file."""
    slim = lambda a: {k: a[k] for k in ('id', 'name', 'summary', 'origin', 'views', 'path') if k in a} | ({'customized': True} if a.get('customized') else {})
    return {'description': focus['description'], 'areas': [slim(a) for a in focus['areas']], 'available': [slim(a) for a in focus['available']],
            'missing': focus['missing'], 'problems': focus['problems'], 'quick_starts': quick_starts(focus), 'goals': suggested_goals(focus),
            'views': list(dict.fromkeys(v for a in focus['areas'] for v in a['views'])),
            'suggested': suggest(focus['description']) if not focus['areas'] else [],
            'knowledge': list(dict.fromkeys(prefix(k) for a in focus['areas'] for k in a['knowledge']))}


def prefix(path):
    """Where a knowledge link's library items live: a playbook page stands for its system's workflows."""
    match = re.fullmatch(r'docs/playbooks/([\w-]+)\.md', path)
    if match:return f'systems/{match[1]}/'
    return path.rsplit('/', 1)[0] + '/' if path.endswith(('.md', 'CONTEXT.md')) else path.rstrip('/') + '/'


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('action', choices=['areas', 'show', 'set', 'suggest'])
    p.add_argument('--business-id', required=True);p.add_argument('--workspace', type=Path, default=workspace_root())
    p.add_argument('--areas', default='', help='Comma-separated focus area ids for set')
    p.add_argument('--text', default='', help='Description to suggest areas from (defaults to the saved description)')
    a = p.parse_args()
    with workspace_scope(a.workspace):
        if a.action == 'areas':result = [{k: x[k] for k in ('id', 'name', 'summary', 'origin')} for x in areas()[0]]
        elif a.action == 'set':result = public(save(a.business_id, [x.strip() for x in a.areas.split(',') if x.strip()]))
        elif a.action == 'suggest':result = {'suggested': suggest(a.text or get(a.business_id)['description'])}
        else:result = public(get(a.business_id))
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    try:main()
    except (ValueError, OSError) as e:raise SystemExit(str(e))
