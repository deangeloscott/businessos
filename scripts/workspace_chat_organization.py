"""Chat pins and projects in the existing workspace preferences."""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from _common import workspace_root, workspace_scope


def items(app,bid):
    root=Path(workspace_root()).resolve()
    return [c for c in app.preferences['chats'] if c['business_id']==bid and Path(c.get('workspace') or root).resolve()==root]


def sort_key(chat):
    return (bool(chat.get('pinned')) and not chat.get('archived'),chat.get('updated') or 0)


def project_name(value,empty=False):
    if not isinstance(value,str) or len(value)>100 or any(ord(c)<32 for c in value):raise ValueError('Use a project name within 100 characters.')
    value=value.strip()
    if not value and not empty:raise ValueError('Enter a project name.')
    return value


def projects(app,bid):
    root=Path(workspace_root()).resolve()
    saved=[dict(p) for p in app.preferences.get('chat_projects',[]) if p['business_id']==bid and Path(p['workspace']).resolve()==root]
    known={p['name'] for p in saved}
    # Older chat labels remain usable without an eager migration or extra files.
    for chat in items(app,bid):
        name=chat.get('project')
        if name and name not in known:
            saved.append({'name':name,'folder':'','workspace':str(root),'business_id':bid});known.add(name)
    return sorted(saved,key=lambda p:p['name'].casefold())


def change_project(app,bid,data):
    action=data.get('action','create');name=project_name(data.get('name'))
    current=projects(app,bid);old=next((p for p in current if p['name']==name),None)
    if action=='open':
        if not old or not old.get('folder'):raise ValueError('Add a folder to this project first.')
        path=Path(old['folder'])
        if not path.is_dir():raise ValueError('This project folder is unavailable. Check its location in Edit project.')
        try:
            if os.name=='nt':os.startfile(str(path))
            else:subprocess.Popen(['open' if sys.platform=='darwin' else 'xdg-open',str(path)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        except OSError as exc:raise ValueError('Could not open the folder. Open its location in your file manager.') from exc
        return {'opened':True}
    if action not in {'create','edit','remove'}:raise ValueError('Choose a project action.')
    if action!='create' and not old:raise ValueError('This project is no longer available.')
    if action=='create' and old:raise ValueError('A project with this name already exists.')
    target=project_name(data.get('new_name',name))
    if any(p['name'].casefold()==target.casefold() and p is not old for p in current):raise ValueError('A project with this name already exists.')
    folder=data.get('folder',old.get('folder','') if old else '')
    if not isinstance(folder,str):raise ValueError('Enter a folder location.')
    folder=folder.strip()
    if folder and action!='remove':
        path=Path(folder).expanduser()
        if not path.is_absolute():path=Path(workspace_root())/path
        if not path.is_dir():raise ValueError('Choose an existing folder on this computer.')
        folder=str(path.resolve())
    current=[p for p in current if p['name']!=name]
    if action!='remove':current.append({'name':target,'folder':folder,'workspace':str(Path(workspace_root()).resolve()),'business_id':bid})
    # Removing a project only ungroups its chats; it never deletes chats or folders.
    for chat in items(app,bid):
        if chat.get('project')==name:chat['project']='' if action=='remove' else target
    root=Path(workspace_root()).resolve()
    outside=[p for p in app.preferences.get('chat_projects',[]) if p['business_id']!=bid or Path(p['workspace']).resolve()!=root]
    app.preferences['chat_projects']=outside+current
    app.save_preferences()
    return {'projects':projects(app,bid)}


def mutate(app,bid,data):
    chats=items(app,bid)
    chat=next((c for c in chats if c['id']==data.get('id')),None)
    if not chat:raise ValueError('Choose a chat in this workspace and business.')
    if 'pinned' in data:
        if not isinstance(data['pinned'],bool):raise ValueError('Choose Pin or Unpin.')
    if 'project' in data:
        value=project_name(data['project'],empty=True)
        current=projects(app,bid)
        existing=next((p for p in current if p['name'].casefold()==value.casefold()),None)
        if existing:value=existing['name']
        elif value:current.append({'name':value,'folder':'','workspace':str(Path(workspace_root()).resolve()),'business_id':bid})
    if not {'pinned','project'}.intersection(data):raise ValueError('Choose a pin or project change.')
    if 'pinned' in data:chat['pinned']=data['pinned']
    if 'project' in data:
        root=Path(workspace_root()).resolve()
        outside=[p for p in app.preferences.get('chat_projects',[]) if p['business_id']!=bid or Path(p['workspace']).resolve()!=root]
        app.preferences['chat_projects']=outside+current
        chat['project']=value
    app.save_preferences()
    return {'chat':chat}


def main():
    from workspace_goals import live_change
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['list','pin','unpin','move','projects','create-project','edit-project','remove-project','open-project'])
    parser.add_argument('--business-id',required=True);parser.add_argument('--chat');parser.add_argument('--project',default='')
    parser.add_argument('--name');parser.add_argument('--folder')
    parser.add_argument('--workspace',type=Path,default=workspace_root());parser.add_argument('--url',default='http://127.0.0.1:4187')
    args=parser.parse_args()
    with workspace_scope(args.workspace):
        if args.action=='list':
            from urllib.parse import urlencode
            result=live_change(args.url,args.business_id,None,'/api/chats?'+urlencode({'business':args.business_id}))
        elif args.action=='projects':result=live_change(args.url,args.business_id,None,'/api/projects?business='+args.business_id)
        elif args.action.endswith('-project'):
            result=live_change(args.url,args.business_id,{'action':args.action.removesuffix('-project'),'name':args.project,**({'new_name':args.name} if args.name is not None else {}),**({'folder':args.folder} if args.folder is not None else {})},'/api/projects')
        else:
            result=live_change(args.url,args.business_id,{'id':args.chat,**({'project':args.project} if args.action=='move' else {'pinned':args.action=='pin'})},'/api/chats/organize')
    print(json.dumps(result,ensure_ascii=False))


if __name__=='__main__':main()
