"""Portable project relationships. Files and native tools retain their ownership."""
import argparse
import hashlib
import json
import os
import secrets
import time
from pathlib import Path
from _common import workspace_root,workspace_scope,resolve_business,write_json_atomic,object_index
from workspace_sharing import destination_lock

FILE='.businessos/projects.json'


def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,allow_nan=False).encode()).hexdigest()


def identity(bid,name):return 'prj_'+digest([bid,name])[:20]


def target():
    from workspace_storage import checked_metadata
    p=checked_metadata(workspace_root()).with_name('projects.json')
    from _common import path_link
    if path_link(p):raise ValueError('Project settings are linked outside this workspace. Reconnect the original settings before editing.')
    return p


def load(legacy=()):
    path=target()
    if path.is_file():
        try:data=json.loads(path.read_text(encoding='utf-8'))
        except (ValueError,UnicodeError):raise ValueError('Project settings could not be read. The original file was kept; restore a backup or correct its JSON.') from None
        if not isinstance(data,dict) or data.get('format')!=1 or not isinstance(data.get('projects'),list):raise ValueError('Saved project relationships need attention. The original file was kept.')
        if any(not isinstance(p,dict) or not all(isinstance(p.get(k),str) for k in ('id','name','business_id','folder')) for p in data['projects']):raise ValueError('Saved project relationships need attention. The original file was kept.')
        if not isinstance(data.get('bindings',{}),dict):raise ValueError('Saved project relationships need attention. The original file was kept.')
        known={(p['business_id'],p['id']) for p in data['projects']}
        names={(p['business_id'],p['name'].casefold()) for p in data['projects']}
        for p in legacy:
            ident=p.get('id') or identity(p['business_id'],p['name'])
            if p.get('workspace') and Path(p['workspace']).resolve()!=workspace_root().resolve():continue
            if (p['business_id'],ident) not in known and (p['business_id'],p['name'].casefold()) not in names:
                data['projects'].append({**{k:v for k,v in p.items() if k not in {'workspace','revision'}},'id':ident,'status':'active'})
                known.add((p['business_id'],ident));names.add((p['business_id'],p['name'].casefold()))
        for p in data['projects']:
            if not isinstance(p,dict) or not all(isinstance(p.get(k),str) for k in ('id','name','business_id','folder')):raise ValueError('Saved project relationships need attention.')
            if p.get('relative') and (Path(p['folder']).is_absolute() or '..' in Path(p['folder']).parts):raise ValueError('A project folder points outside its workspace. Reconnect its original folder.')
        return data
    from workspace_storage import load_view
    old=load_view(workspace_root()).get('projects',[])
    rows=[];seen=set()
    for p in [*old,*legacy]:
        key=(p['business_id'],p['name'])
        if key in seen:continue
        seen.add(key);folder=p.get('folder','')
        if p.get('workspace') and Path(p['workspace']).resolve()!=workspace_root().resolve():continue
        rows.append({**{k:p[k] for k in ('name','business_id','context_refs') if k in p},'id':p.get('id') or identity(*key),
                     'folder':folder,'relative':p.get('relative',False),'members':p.get('members',[]),'status':'active'})
    return {'format':1,'projects':rows,'bindings':{}}


def public(p):
    return {**p,'revision':digest(p),'workspace':str(workspace_root().resolve()),
            'folder':str(workspace_root()/p['folder']) if p.get('relative') else p.get('folder','')}


def list_projects(bid,legacy=(),archived=False):
    return sorted((public(p) for p in load(legacy)['projects'] if p['business_id']==bid and (archived or p.get('status','active')=='active')),key=lambda p:p['name'].casefold())


def find(bid,ident,archived=False):
    p=next((p for p in list_projects(bid,archived=archived) if ident in {p['id'],p['name']}),None)
    if not p:raise ValueError('This project is unavailable. Choose a project in this workspace.')
    return p


def check_business(bid):
    if resolve_business(bid).get('status')!='resolved':raise ValueError('Choose a business in this workspace.')


def reference(bid,value,verify=True):
    if not isinstance(value,dict) or value.get('kind') not in {'file','record','goal','asset','task','collection','result','library'}:raise ValueError('Choose an existing file, record, goal, collection, task, or source.')
    if not isinstance(value.get('id'),str) or not value['id'] or len(value['id'])>2000:raise ValueError('Choose a valid resource reference.')
    if verify and value['kind'] in {'record','goal','asset'}:
        item=object_index(bid).get(value['id'])
        if not item or value['kind']=='asset' and item[0]['object_type']!='Asset' or value['kind']=='goal' and item[0]['object_type']!='Objective':raise ValueError('This resource does not belong to the selected business.')
    if verify and value['kind']=='file':
        from workspace_ui import local_file
        from workspace_storage import view_preferences
        local_file(bid,value['id'],view_preferences(workspace_root()).get('file_locations',{}).get(bid,[]))
    if verify and value['kind']=='collection':
        from workspace_collections import read
        read(bid,value['id'])
    out={k:value[k] for k in ('kind','id','variant','request_id','role') if k in value}
    if any(not isinstance(v,str) or len(v)>2000 for v in out.values()):raise ValueError('Choose a valid resource reference.')
    return out


def change(bid,data,legacy=()):
    check_business(bid)
    from workspace_chat_organization import project_name
    from workspace_context import references
    action=data.get('action','create')
    with destination_lock(target()):
        doc=load(legacy);ident=data.get('id') or data.get('name');old=next((p for p in doc['projects'] if p['business_id']==bid and ident in {p['id'],p['name']}),None)
        if action=='create' and old:raise ValueError('An archived project uses this name. Restore it in Archive & recovery, or choose another name.' if old.get('status')=='archived' else 'A project with this name already exists.')
        if action!='create' and not old:raise ValueError('This project is no longer available.')
        if old and data.get('revision') is not None and data['revision']!=digest(old):raise ValueError('This project changed. Reopen it before saving.')
        p=dict(old or {'id':'prj_'+secrets.token_hex(10),'business_id':bid,'members':[],'context_refs':[]})
        p.setdefault('context_refs',[]);p.setdefault('members',[])
        if action in {'create','edit'}:
            name=project_name(data.get('new_name',data.get('name',p.get('name'))))
            if any(x['business_id']==bid and x['name'].casefold()==name.casefold() and x['id']!=p['id'] and x.get('status')=='active' for x in doc['projects']):raise ValueError('A project with this name already exists.')
            folder=data.get('folder',public(p)['folder'])
            if not isinstance(folder,str):raise ValueError('Choose a folder location.')
            folder=folder.strip();relative=False
            if folder:
                path=Path(folder).expanduser();path=(workspace_root()/path if not path.is_absolute() else path).resolve()
                if not path.is_dir():raise ValueError('This project folder is unavailable. Choose an existing folder.')
                relative=path.is_relative_to(workspace_root().resolve());folder=path.relative_to(workspace_root().resolve()).as_posix() if relative else str(path)
            p.update(name=name,folder=folder,relative=relative,status='active',context_refs=references(data.get('context_refs',p['context_refs'])))
            if 'description' in data:
                if not isinstance(data['description'],str) or len(data['description'])>2000:raise ValueError('Keep the project description within 2,000 characters.')
                p['description']=data['description'].strip()
        elif action in {'remove','restore'}:
            if action=='restore' and any(x['id']!=p['id'] and x['business_id']==bid and x['name'].casefold()==p['name'].casefold() and x.get('status')=='active' for x in doc['projects']):raise ValueError('Another active project uses this name. Rename this project before restoring it.')
            p['status']='archived' if action=='remove' else 'active'
        elif action in {'link','unlink'}:
            ref=reference(bid,data.get('reference'),verify=action=='link');key=lambda r:(r['kind'],r['id'],r.get('variant',''),r.get('request_id',''))
            p['members']=[r for r in p.get('members',[]) if key(r)!=key(ref)]
            p['excluded_members']=[r for r in p.get('excluded_members',[]) if key(r)!=key(ref)]
            if action=='link':p['members'].append(ref)
            else:p['excluded_members'].append(ref)
        else:raise ValueError('Choose a project action.')
        p['updated']=time.time();doc['projects']=[x for x in doc['projects'] if x['id']!=p['id'] or x['business_id']!=bid]+[p]
        write_json_atomic(target(),doc)
        return {'project':public(p),'projects':list_projects(bid)}


def bind(bid,kind,ident,projects=(),collection=None,goal_id=None):
    check_business(bid)
    if kind not in {'chat','task','agent'} or not isinstance(ident,str) or not ident or len(ident)>1000:raise ValueError('Choose an existing chat, task, or agent.')
    if not isinstance(projects,(list,tuple)) or len(projects)>100:raise ValueError('Choose a bounded list of projects.')
    if collection:
        from workspace_collections import read
        read(bid,collection)
    if goal_id:reference(bid,{'kind':'goal','id':goal_id})
    project_ids=[find(bid,p)['id'] for p in projects]
    with destination_lock(target()):
        doc=load();key=bid+'\0'+kind+'\0'+ident;row=doc.setdefault('bindings',{}).get(key,{})
        row={**row,'kind':kind,'id':ident,'business_id':bid,'project_refs':list(dict.fromkeys(project_ids))}
        if collection is not None:row['collection_id']=collection
        if goal_id is not None:row['goal_ref']=goal_id
        if row==doc['bindings'].get(key) or not project_ids and not row.get('collection_id') and not row.get('goal_ref') and key not in doc['bindings']:return row
        doc['bindings'][key]=row;write_json_atomic(target(),doc);return row


def binding(bid,kind,ident):return load().get('bindings',{}).get(bid+'\0'+kind+'\0'+ident,{})


def producer_context(bid,producer=None):
    if producer is None:
        try:producer=json.loads(os.environ.get('AURA_PRODUCER','{}'))
        except ValueError:producer={}
    if not isinstance(producer,dict) or producer.get('business_id')!=bid or producer.get('workspace')!=str(workspace_root().resolve()):return {}
    current=binding(bid,producer.get('kind',''),producer.get('id',''))
    active={p['id'] for p in list_projects(bid)}
    return {**(current or {k:producer[k] for k in ('kind','id','business_id') if k in producer}),'project_refs':[p for p in current.get('project_refs',[]) if p in active]}


def asset_context(bid,obj):
    """Attach proven producer context only when an actual Asset is deliberately saved."""
    context=producer_context(bid)
    if not context:return obj
    obj=json.loads(json.dumps(obj));bos=obj.setdefault('extensions',{}).setdefault('businessos',{})
    # Existing explicit associations survive; moving a chat does not move earlier work.
    work=bos.setdefault('work',{})
    work.setdefault('producer',{'kind':context['kind'],'id':context['id']})
    work.setdefault('project_refs',context.get('project_refs',[]))
    if context.get('goal_ref'):bos.setdefault('goal_ref',context['goal_ref'])
    return obj


def resources(app,bid,ident):
    from workspace_ui import records,archived_paths,file_visible
    from workspace_lifecycle import archived
    all_rows=records(bid,include_archived=True)[0];hidden_refs={r['ref'] for r in all_rows if archived(r['data'])};hidden_paths=archived_paths(bid,all_rows)
    p=find(bid,ident,archived=True);rows=[r for r in all_rows if r['ref'] not in hidden_refs];index={r['ref']:r for r in rows};out=[]
    excluded={r['id'] for r in p.get('excluded_members',[])}
    for ref in p.get('members',[]):
        if ref['id'] in hidden_refs:continue
        record=index.get(ref['id']);label=record['title'] if record else ref['id'];available=bool(record) if ref['kind'] in {'asset','record','goal'} else None
        if ref['kind']=='file':
            try:
                from workspace_ui import local_file
                original=local_file(bid,ref['id'],app.preferences.get('file_locations',{}).get(bid,[]))
                if not file_visible(original,hidden_paths):continue
                label=original.name;available=True
            except (ValueError,OSError):label=Path(ref['id']).name;available=False
        elif ref['kind']=='library':
            import workspace_library
            item=workspace_library.find(app.library_items()['items'],ref['id']);label=(item or {}).get('title') or 'Library item';available=item is not None
        elif ref['kind']=='task':
            import workspace_schedules
            task=next((t for t in workspace_schedules.inventory()['items'] if t['id']==ref['id']),None);label=(task or {}).get('name') or 'Scheduled task';available=task is not None
        elif ref['kind']=='result':
            chat=next((c for c in app.preferences.get('chats',[]) if c['id']==ref['id'] and c['business_id']==bid),None);label=(chat or {}).get('name') or (chat or {}).get('title') or 'Chat result'
        out.append({**ref,'label':label,'available':available})
    for row in rows:
        bos=(row['data'].get('extensions') or {}).get('businessos',{});work=bos.get('work') or {}
        if p['id'] in work.get('project_refs',[]) and row['ref'] not in excluded and not bos.get('collection') and not any(r['id']==row['ref'] for r in out):
            out.append({'kind':'asset' if row['type']=='Asset' else 'record','id':row['ref'],'label':row['title'],'role':work.get('role',''),'available':True})
    bindings=[v for v in load().get('bindings',{}).values() if v['business_id']==bid and p['id'] in v.get('project_refs',[])]
    tasks=None
    for v in bindings:
        if v['kind']=='task' and not any(r['kind']=='task' and r['id']==v['id'] for r in out):
            if tasks is None:
                import workspace_schedules
                tasks={t['id']:t for t in workspace_schedules.inventory()['items']}
            task=tasks.get(v['id']);out.append({'kind':'task','id':v['id'],'label':(task or {}).get('name') or 'Scheduled task','available':task is not None})
    return {'project':p,'items':out,'bindings':bindings}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['list','show','create','edit','remove','restore','link','unlink','bind']);p.add_argument('--business-id',required=True);p.add_argument('--workspace',type=Path,default=workspace_root());p.add_argument('--id');p.add_argument('--input',default='{}')
    a=p.parse_args()
    with workspace_scope(a.workspace):
        data=json.loads(__import__('sys').stdin.read() if a.input=='-' else a.input);check_business(a.business_id)
        if a.action=='list':result={'projects':list_projects(a.business_id)}
        elif a.action=='show':
            from workspace_ui import Workspace
            result=resources(Workspace(),a.business_id,a.id)
        elif a.action=='bind':result=bind(a.business_id,**data)
        else:result=change(a.business_id,{**data,'action':a.action,**({'id':a.id} if a.id else {})})
    print(json.dumps(result,ensure_ascii=False))


if __name__=='__main__':
    try:main()
    except (ValueError,OSError) as e:raise SystemExit(str(e))
