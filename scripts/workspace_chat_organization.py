"""Chat pins and project labels, scoped to the existing workspace chat store."""
import argparse
import json
from pathlib import Path
from _common import workspace_root, workspace_scope


def items(app,bid):
    root=Path(workspace_root()).resolve()
    return [c for c in app.preferences['chats'] if c['business_id']==bid and Path(c.get('workspace') or root).resolve()==root]


def sort_key(chat):
    return (bool(chat.get('pinned')) and not chat.get('archived'),chat.get('updated') or 0)


def mutate(app,bid,data):
    chats=items(app,bid)
    chat=next((c for c in chats if c['id']==data.get('id')),None)
    if not chat:raise ValueError('Choose a chat in this workspace and business.')
    if 'pinned' in data:
        if not isinstance(data['pinned'],bool):raise ValueError('Choose Pin or Unpin.')
    if 'project' in data:
        value=data['project']
        if not isinstance(value,str) or len(value)>100 or any(ord(c)<32 for c in value):raise ValueError('Use a project name within 100 characters.')
    if not {'pinned','project'}.intersection(data):raise ValueError('Choose a pin or project change.')
    if 'pinned' in data:chat['pinned']=data['pinned']
    if 'project' in data:chat['project']=data['project'].strip()
    app.save_preferences()
    return {'chat':chat}


def main():
    from workspace_goals import live_change
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['list','pin','unpin','move'])
    parser.add_argument('--business-id',required=True);parser.add_argument('--chat');parser.add_argument('--project',default='')
    parser.add_argument('--workspace',type=Path,default=workspace_root());parser.add_argument('--url',default='http://127.0.0.1:4187')
    args=parser.parse_args()
    with workspace_scope(args.workspace):
        if args.action=='list':
            from urllib.parse import urlencode
            result=live_change(args.url,args.business_id,None,'/api/chats?'+urlencode({'business':args.business_id}))
        else:
            result=live_change(args.url,args.business_id,{'id':args.chat,**({'project':args.project} if args.action=='move' else {'pinned':args.action=='pin'})},'/api/chats/organize')
    print(json.dumps(result,ensure_ascii=False))


if __name__=='__main__':main()
