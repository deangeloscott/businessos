"""One archive and recovery view, using each item's existing owner and storage."""
import argparse
import json
import time
from pathlib import Path
from urllib.parse import urlencode

from _common import workspace_root, workspace_scope
import workspace_goals
import workspace_organization
from workspace_lifecycle import archived


def inventory(app, bid):
    import workspace_assistants
    from _common import object_index
    app.load_portable()
    notes=[]
    if not app.portable_view_ok:notes.append('Some saved workspace settings could not be read. Their files were kept.')
    items = [dict(kind='chat', id=c['id'], title=c.get('title') or 'Chat',
                  at=c.get('archived_at'), state='archived', action='Unarchive')
             for c in app.preferences['chats'] if c['business_id'] == bid and c.get('archived') and
             Path(c.get('workspace') or app.workspace_path).resolve() == workspace_root().resolve()]
    items += [dict(kind='goal', id=g['id'], title=g.get('name') or 'Goal',
                   at=workspace_goals.metadata(g).get('deleted_at'), state='deleted',
                   previous_status=workspace_goals.metadata(g).get('deleted_status','active'),
                   action='Restore as completed' if workspace_goals.metadata(g).get('deleted_status')=='completed' else 'Restore')
              for g in workspace_goals.goals(bid, include_deleted=True) if workspace_goals.deleted(g)]
    import workspace_projects
    items += [dict(kind='project',id=p['id'],title=p['name'],at=p.get('updated'),state='archived',action='Restore') for p in workspace_projects.list_projects(bid,archived=True) if p.get('status')=='archived']
    items += [dict(kind='agent',id=p['id'],title=p['name'],at=p['archived_at'],state='archived',action='Restore')
              for p in workspace_assistants.profiles(app.preferences,bid,True) if p.get('archived_at')]
    from _common import describe_object
    diagnostics=[]
    for obj,path in object_index(bid,diagnostics=diagnostics).values():
        if not archived(obj):continue
        collection=((obj.get('extensions') or {}).get('businessos',{}).get('collection') or {})
        items.append(dict(kind='collection' if collection else 'file' if obj['object_type']=='Asset' else 'record',
                          id=obj['id'],title=describe_object(obj,path).get('title') or obj['id'],
                          at=obj['extensions']['businessos']['archive']['at'],state='archived',action='Restore'))
    if diagnostics:notes.append('Some saved records could not be read. The other archived items are still available.')
    try:
        items += [dict(kind='recovery', id=e['id'], title=Path(e['original']).name,
                       at=e.get('retired'), state='recovery', action='Restore', expires=e.get('expires'), days=e.get('days', 0))
                  for e in workspace_organization.recovery(app.settings_file.parent)
                  if e.get('status') in {'available', 'changed'} and
                  Path(e.get('destination', '')).resolve() == workspace_root().resolve()]
    except (OSError, ValueError):
        notes.append('Recovery copies could not be read. Your chats and goals are still available.')
    import workspace_history
    deleted_paths=set()
    try:history=workspace_history.inventory(bid)['items']
    except (OSError,ValueError):
        history=[];notes.append('Saved file history could not be read. The other archived items are still available.')
    for row in history:
        if not (workspace_root()/row['path']).exists():
            if row['path'] in deleted_paths:continue
            deleted_paths.add(row['path'])
            deleted=row.get('reason')=='Deleted'
            items.append(dict(kind='deleted-file' if deleted else 'file-version',id=row['id'],title=Path(row['path']).name,
                              at=row['at'],state='deleted' if deleted else 'recovery',action='Restore',path=row['path']))
    return {'items': sorted(items, key=lambda item: item.get('at') or 0, reverse=True), 'notes': notes}


def change(app,bid,kind,ident,action='restore'):
    if action not in {'archive','restore'}:raise ValueError('Choose archive or restore.')
    if action=='restore' and kind in {'deleted-file','file-version','recovery'} and app.running_jobs(workspace_root()):
        raise ValueError('Wait for active work before restoring files.')
    if kind=='chat':return app.archive_chat(bid,ident,action=='archive')
    if kind=='goal':
        if action!='restore':raise ValueError('Delete a goal through its goal controls. Restore deleted goals here.')
        return workspace_goals.mutate(app,bid,{'id':ident,'action':'restore'})
    if kind=='project':
        import workspace_projects
        result=workspace_projects.change(bid,{'id':ident,'action':'remove' if action=='archive' else 'restore'})
    elif kind=='agent':return app.assistants(bid,{'id':ident,'action':action})
    elif kind in {'deleted-file','file-version'} and action=='restore':
        import workspace_history
        result=workspace_history.restore(bid,ident,'missing')
    elif kind=='recovery' and action=='restore':
        entry=next((e for e in workspace_organization.recovery(app.settings_file.parent) if e['id']==ident),None)
        if not entry or Path(entry.get('destination','')).resolve()!=workspace_root().resolve():raise ValueError('Choose a recovery copy in this workspace.')
        result=workspace_organization.recover(ident,'restore',app.settings_file.parent,references=app.organization_references())
    elif kind in {'record','file','collection'}:
        if kind=='collection':
            import workspace_collections
            obj=workspace_collections.asset(bid,ident)
            if obj:ident=obj['id']
        if kind=='file' and action=='archive':
            from _common import object_index
            if ident not in object_index(bid):
                from workspace_ui import local_file,asset_path
                from remember import remember
                path=local_file(bid,ident,app.preferences.get('file_locations',{}).get(bid,[]))
                candidates=object_index(bid)
                existing=next((o for o,p in candidates.values() if p.resolve()==path.resolve() or
                               o['object_type']=='Asset' and asset_path(bid,o.get('location_reference'))==path.resolve()),None)
                if existing:ident=existing['id']
                else:
                    location=path.relative_to(workspace_root()).as_posix() if path.is_relative_to(workspace_root()) else str(path)
                    saved=remember(bid,{'objects':[{'object_type':'Asset','content':{'asset_type':'file','business_role':path.name,'location_reference':location,'version':'1','status':'active',
                                     'extensions':{'businessos':{'archive':{'at':time.time()}}}}}]})
                    app.read_cache.clear()
                    return saved
        from workspace_lifecycle import change as change_record
        result=change_record(bid,ident,action)
    else:raise ValueError('Choose an archived item or recovery copy.')
    app.read_cache.clear()
    return result


def restore(url, bid, kind, ident):
    return workspace_goals.live_change(url,bid,{'id':ident,'kind':kind,'action':'restore'},'/api/archive')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['list', 'archive', 'restore'])
    parser.add_argument('--business-id', required=True)
    parser.add_argument('--workspace', type=Path, default=workspace_root())
    parser.add_argument('--url', default='http://127.0.0.1:4187', help='Running local AURA address')
    parser.add_argument('--kind', choices=['chat', 'goal', 'recovery','project','agent','record','file','collection','deleted-file','file-version'])
    parser.add_argument('--id')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    if args.action != 'list' and (not args.kind or not args.id):
        parser.error('archive and restore need --kind and --id')
    with workspace_scope(args.workspace):
        result = (workspace_goals.live_change(args.url,args.business_id,{'id':args.id,'kind':args.kind,'action':args.action},'/api/archive') if args.action != 'list' else
                  workspace_goals.live_change(args.url, args.business_id, None,
                                              '/api/archive?' + urlencode({'business': args.business_id})))
    print(json.dumps(result, ensure_ascii=False))


if __name__=='__main__':
    import sys
    from urllib.error import HTTPError,URLError
    try:main()
    except HTTPError as error:
        try:message=json.load(error).get('error','AURA could not complete this action.')
        except (ValueError,OSError):message='AURA could not complete this action.'
        print('Error: '+str(message),file=sys.stderr);sys.exit(1)
    except URLError:
        print('Error: AURA is not reachable. Start the local AURA service and check --url.',file=sys.stderr);sys.exit(1)
    except (OSError,ValueError) as error:
        print('Error: '+str(error),file=sys.stderr);sys.exit(1)
