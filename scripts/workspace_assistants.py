"""Small workspace-owned assistant profiles. Native apps still execute the work."""
import argparse
import json
import secrets
import time

from _common import workspace_root


def profiles(preferences, business):
    return preferences.get('assistants', {}).get(business, [])


def find(preferences, business, ident):
    profile = next((p for p in profiles(preferences, business) if p['id'] == ident), None)
    if not profile:
        raise ValueError('This agent is no longer available in this workspace.')
    return profile


def validate(data):
    if not isinstance(data, dict):
        raise ValueError('Saved agents need attention.')
    for business, items in data.items():
        if not isinstance(business, str) or not isinstance(items, list) or len(items) > 200:
            raise ValueError('Saved agents need attention.')
        seen = set()
        forbidden={'permission_mode','harness_permissions','approval_grants','pending_requests','credentials','requests'}
        for item in items:
            if isinstance(item,dict) and forbidden.intersection(item):raise ValueError('Agent packages cannot carry permission grants, sign-ins, or live requests.')
            if not isinstance(item, dict):
                raise ValueError('Saved agents need attention.')
            for field, limit in [('id', 100), ('name', 80), ('instructions', 20000),
                                 ('description',1000),('app', 40), ('model', 300), ('effort', 300), ('child_model', 300)]:
                value = item.get(field, '')
                if not isinstance(value, str) or len(value) > limit:
                    raise ValueError('An agent has an invalid name or preference.')
            if not item.get('id') or not item.get('name', '').strip() or item['id'] in seen:
                raise ValueError('Each agent needs a name and a unique identity.')
            seen.add(item['id'])
            binding=item.get('native_agent')
            if binding is not None:
                if not isinstance(binding,dict) or set(binding)-{'app','scope','file'} or not all(isinstance(binding.get(k),str) and binding[k] and len(binding[k])<300 for k in ('app','scope','file')):
                    raise ValueError('Choose a valid native agent reference.')
                from pathlib import PurePosixPath
                if binding['scope'] not in ({'profile'} if binding['app']=='hermes' else {'project','user'}) or PurePosixPath(binding['file']).is_absolute() or '..' in PurePosixPath(binding['file']).parts or '\\' in binding['file'] or ':' in binding['file']:
                    raise ValueError('Native agent references must stay relative to their native agent folder.')
            from workspace_context import references
            references(item.get('context_refs',[]))
            tasks = item.get('task_ids', [])
            if not isinstance(tasks, list) or len(tasks) > 1000 or any(not isinstance(t, str) or len(t) > 100 for t in tasks):
                raise ValueError('An agent has invalid task links.')
    return data


def save(preferences, business, data):
    old = find(preferences, business, data['id']) if data.get('id') else {}
    profile = {**old, 'id':old.get('id') or secrets.token_urlsafe(12), 'updated':time.time()}
    for field in ('name', 'description', 'instructions', 'app', 'model', 'effort', 'child_model'):
        if field in data:
            if not isinstance(data[field], str):
                raise ValueError('Enter a valid agent preference.')
            profile[field] = data[field].strip()
    if 'native_agent' in data:
        if data['native_agent'] is None:profile.pop('native_agent',None)
        else:profile['native_agent']=data['native_agent']
    if 'task_ids' in data:
        if not isinstance(data['task_ids'], list) or any(not isinstance(t, str) for t in data['task_ids']):
            raise ValueError('Choose valid scheduled tasks.')
        profile['task_ids'] = list(dict.fromkeys(data['task_ids']))
    if 'context_refs' in data:
        from workspace_context import references
        profile['context_refs']=references(data['context_refs'])
    profile.setdefault('task_ids', [])
    updated = [p for p in profiles(preferences, business) if p['id'] != profile['id']] + [profile]
    validate({business:updated})
    preferences.setdefault('assistants', {})[business] = updated
    return profile


def remove(preferences, business, ident):
    find(preferences, business, ident)
    preferences['assistants'][business] = [p for p in profiles(preferences, business) if p['id'] != ident]
    # Chats, schedules, files and their native histories are intentionally retained.


def guidance(profile,child_native=False,native_primary=False):
    return ('\nUser-selected agent profile (task preferences; preserve native permissions):\n' +
            json.dumps({k:profile.get(k, '') for k in ('name', 'description','instructions', 'child_model', 'task_ids') if (k!='child_model' or not child_native) and (k!='instructions' or not native_primary)}, ensure_ascii=False) +
            '\nUse the child model preference only when native delegation supports it. '
            'Give children the selected business/workspace, goal, relevant constraints and source references. '
            'Children should return questions and partial work to their parent; the parent asks the user when needed. '
            'Do not bypass approvals or claim a model override that the harness cannot apply. '
            'For assigned recurring work, use scripts/workspace_schedules.py history --id <task_id> '
            'and result --id <task_id> from the AURA product folder with the selected workspace. '
            'Read only results relevant to the request.\n')


def resolved(profile,kind,cwd,env,command=(),options=None,native_only=False):
    """A link reuses current native instructions; never maintain a competing copy."""
    binding=profile.get('native_agent')
    if not binding:return dict(profile)
    if binding['app']!=kind:raise ValueError('This agent is linked to a different AI app. Choose its AI app or unlink the native definition.')
    from workspace_specialists import read,local
    if not local(command):raise ValueError('This agent definition belongs to another environment. Reconnect it there.')
    if kind=='hermes' and native_only:
        # Hermes reads its own profile. Do not launch a second gateway on each message.
        return {**profile,'instructions':'','native_name':binding['file'],'native_primary':True,'native_revision':binding['file']}
    native=read(kind,cwd,env,binding['scope'],binding['file'],command,options)
    primary=kind in {'claude','hermes'} or kind=='antigravity' and native['settings'].get('mainAgent',True) is not False
    return {**profile,'description':native['description'],'instructions':native['instructions'],'native_name':native['name'],
            'native_primary':primary,'native_revision':native['revision']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['list', 'save', 'remove'])
    parser.add_argument('--business', required=True)
    parser.add_argument('--input', help='JSON profile; use - to read standard input')
    parser.add_argument('--id')
    args = parser.parse_args()
    from workspace_storage import view_preferences, save_view
    from workspace_catalog import preview
    if args.business not in {b['id'] for b in preview(workspace_root())['businesses']}:
        raise ValueError('Choose a business in this workspace.')
    prefs = view_preferences(workspace_root())
    if args.action == 'list':
        result = profiles(prefs, args.business)
    elif args.action == 'save':
        import sys
        result = save(prefs, args.business, json.loads(sys.stdin.read() if args.input == '-' else args.input or '{}'))
        save_view(workspace_root(), prefs)
    else:
        remove(prefs, args.business, args.id)
        save_view(workspace_root(), prefs)
        result = {'ok':True}
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
