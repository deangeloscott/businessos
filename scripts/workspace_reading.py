#!/usr/bin/env python3
"""Read-only context from the person's other AURA workspaces that allow it.

Each workspace decides for itself, with one switch stored in its own folder, whether the
person's other workspaces on this computer may read it. Reading never copies, writes or links
anything across workspaces; results name where they came from. Organization isolation is
unchanged: another workspace's records are context, never this organization's truth.
"""
from pathlib import Path
import argparse
import json
import time

from _common import workspace_root, workspace_scope, object_index, business_directory, write_json_atomic

SETTING = Path('.businessos') / 'reading.json'


def allowed(root=None):
    """Whether this workspace lets the person's other workspaces read it. Off unless chosen."""
    try:data = json.loads((Path(root or workspace_root()) / SETTING).read_text(encoding='utf-8'))
    except (OSError, ValueError):return False
    return isinstance(data, dict) and data.get('readable_by_other_workspaces') is True


def set_allowed(value, root=None):
    if not isinstance(value, bool):raise ValueError('Choose on or off.')
    target = Path(root or workspace_root()) / SETTING
    write_json_atomic(target, {'readable_by_other_workspaces': value, 'changed_at': time.time()})
    return {'readable_by_other_workspaces': value}


def _recent():
    from workspace_startup import state_dir
    try:rows = json.loads((state_dir() / 'recent-workspaces.json').read_text(encoding='utf-8'))
    except (OSError, ValueError):return []
    return [r for r in rows if isinstance(r, dict) and isinstance(r.get('path'), str)] if isinstance(rows, list) else []


def readable_workspaces():
    """Other workspaces this computer has opened in AURA that allow reading."""
    here = Path(workspace_root()).resolve();out = []
    for row in _recent():
        try:root = Path(row['path']).resolve()
        except OSError:continue
        if root == here or not root.is_dir() or any(o['path'] == str(root) for o in out) or not allowed(root):continue
        out.append({'path': str(root), 'name': str(row.get('name') or root.name)[:160]})
    return out


def search(task, limit=5):
    """Matching saved work from readable workspaces, labelled with where it came from."""
    from enter import _saved_work_candidates
    found = []
    for workspace in readable_workspaces():
        try:
            with workspace_scope(workspace['path']):
                for business in business_directory():
                    bid = business['id'];index = object_index(bid)
                    for row in _saved_work_candidates(task, index, limit):
                        if row.get('status') in {'archived', 'superseded'}:continue
                        _, path = index[row['object_ref']]
                        found.append({**row, 'path': str(Path(path).resolve()), 'workspace': workspace['name'], 'workspace_path': workspace['path'],
                                      'business_id': bid, 'business': business.get('name') or bid})
        except (OSError, ValueError, KeyError):continue
    found.sort(key=lambda r: -r.get('lexical_score', 0))
    return found[:limit]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('action', choices=['status', 'set', 'list', 'search'])
    p.add_argument('--workspace', type=Path, default=None)
    p.add_argument('--on', action='store_true');p.add_argument('--off', action='store_true')
    p.add_argument('--query', default='');p.add_argument('--limit', type=int, default=5)
    a = p.parse_args()
    with workspace_scope(a.workspace or workspace_root()):
        if a.action == 'status':result = {'readable_by_other_workspaces': allowed()}
        elif a.action == 'set':
            if a.on == a.off:raise ValueError('Choose --on or --off.')
            result = set_allowed(a.on)
        elif a.action == 'list':result = {'workspaces': readable_workspaces()}
        else:result = {'items': search(a.query, max(1, min(20, a.limit)))}
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    try:main()
    except (ValueError, OSError) as e:raise SystemExit(str(e))
