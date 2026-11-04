"""One view of existing archived chats, deleted goals, and workspace recovery copies."""
import argparse
import json
from pathlib import Path
from urllib.parse import urlencode

from _common import workspace_root, workspace_scope
import workspace_goals
import workspace_organization


def inventory(app, bid):
    items = [dict(kind='chat', id=c['id'], title=c.get('title') or 'Chat',
                  at=c.get('archived_at') or c.get('updated'), action='Unarchive')
             for c in app.preferences['chats'] if c['business_id'] == bid and c.get('archived')]
    items += [dict(kind='goal', id=g['id'], title=g.get('name') or 'Goal',
                   at=workspace_goals.metadata(g).get('deleted_at'), action='Restore')
              for g in workspace_goals.goals(bid, include_deleted=True) if workspace_goals.deleted(g)]
    notes = []
    try:
        items += [dict(kind='recovery', id=e['id'], title=Path(e['original']).name,
                       at=e.get('retired'), action='Restore', expires=e.get('expires'), days=e.get('days', 0))
                  for e in workspace_organization.recovery(app.settings_file.parent)
                  if e.get('status') in {'available', 'changed'} and
                  Path(e.get('destination', '')).resolve() == workspace_root().resolve()]
    except (OSError, ValueError):
        notes.append('Recovery copies could not be read. Your chats and goals are still available.')
    return {'items': sorted(items, key=lambda item: item.get('at') or 0, reverse=True), 'notes': notes}


def restore(url, bid, kind, ident):
    if kind == 'chat':
        return workspace_goals.live_change(url, bid, {'id': ident, 'archived': False}, '/api/chats/archive')
    if kind == 'goal':
        return workspace_goals.live_change(url, bid, {'id': ident, 'action': 'restore'})
    if kind == 'recovery':
        return workspace_goals.live_change(url, bid, {'id': ident, 'action': 'restore'}, '/api/recovery/update')
    raise ValueError('Choose an archived chat, deleted goal, or recovery copy.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['list', 'restore'])
    parser.add_argument('--business-id', required=True)
    parser.add_argument('--workspace', type=Path, default=workspace_root())
    parser.add_argument('--url', default='http://127.0.0.1:4187', help='Running local Aura address')
    parser.add_argument('--kind', choices=['chat', 'goal', 'recovery'])
    parser.add_argument('--id')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    if args.action == 'restore' and (not args.kind or not args.id):
        parser.error('restore needs --kind and --id')
    with workspace_scope(args.workspace):
        result = (restore(args.url, args.business_id, args.kind, args.id) if args.action == 'restore' else
                  workspace_goals.live_change(args.url, args.business_id, None,
                                              '/api/archive?' + urlencode({'business': args.business_id})))
    print(json.dumps(result, ensure_ascii=False))


if __name__=='__main__':
    import sys
    from urllib.error import HTTPError,URLError
    try:main()
    except HTTPError as error:
        try:message=json.load(error).get('error','Aura could not complete this action.')
        except (ValueError,OSError):message='Aura could not complete this action.'
        print('Error: '+str(message),file=sys.stderr);sys.exit(1)
    except URLError:
        print('Error: Aura is not reachable. Start the local Aura service and check --url.',file=sys.stderr);sys.exit(1)
    except (OSError,ValueError) as error:
        print('Error: '+str(error),file=sys.stderr);sys.exit(1)
