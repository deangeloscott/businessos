"""Explicit, local workspace consolidation and recoverable retirement.

The host supplies semantic decisions. This module compares and preserves files,
imports non-conflicting records, verifies a new workspace, and records recovery.
No model client, scheduler, or independent business truth store lives here.
"""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
import uuid
from datetime import datetime,timezone

from _common import PRODUCT_ROOT, write_json_atomic
from canonical_store import validate_canonical
import workspace_catalog as catalog
import workspace_storage as storage
from workspace_startup import state_dir
from migrate_workspace import _sha256

INSTRUCTIONS = {'AGENTS.md','AGENTS.override.md','CLAUDE.md','HERMES.md','.hermes.md'}


def folder(value):
    path = Path(value).expanduser().resolve()
    system=[Path(p).resolve() for p in (os.environ.get('WINDIR'),os.environ.get('PROGRAMFILES'),os.environ.get('PROGRAMFILES(X86)')) if p]
    if os.name!='nt':system += [Path(p) for p in ('/usr','/bin','/etc','/System','/Library','/Applications')]
    if path in {Path(path.anchor),Path.home().resolve()} or Path.home().resolve().is_relative_to(path) or path == PRODUCT_ROOT.resolve() or any(path.is_relative_to(p) for p in system):
        raise ValueError('Choose a saved workspace or project folder, not the application, your home, or an entire drive.')
    return path


def safe_relative(value):
    rel = PurePosixPath(value)
    if not rel.parts or rel.is_absolute() or '..' in rel.parts or '\\' in value or ':' in value:
        raise ValueError('An organization file location is invalid. Keep the originals and create a new review.')
    return Path(*rel.parts)


def snapshot(root, progress=lambda _:None):
    """Account for all original files, including excluded files; never read secrets into a plan."""
    root = Path(root)
    found, omitted = {}, []
    if not root.is_dir():
        raise ValueError('A selected folder is unavailable. Reconnect its drive or choose its current location.')
    def failed(error):
        raise ValueError('A selected folder could not be read. Check its permissions or availability: '+str(error.filename))
    for directory, dirs, files in os.walk(root,followlinks=False,onerror=failed):
        base = Path(directory)
        for name in list(dirs):
            path = base/name
            if path.is_symlink() or getattr(path,'is_junction',lambda:False)():
                omitted.append(path.relative_to(root).as_posix());dirs.remove(name)
        for name in sorted(files):
            path = base/name;rel = path.relative_to(root).as_posix()
            if path.is_symlink():omitted.append(rel);continue
            if len(found)>=100000:
                raise ValueError('This selection is too large for one organization pass. Choose smaller project folders.')
            progress('Checking '+path.name)
            found[rel]={'sha256':_sha256(path,lambda:progress('Checking '+path.name)),'bytes':path.stat().st_size}
    return found,sorted(omitted)


def _root(store=None):
    return Path(store or state_dir())/'organization'


def _path(ident,store=None):
    if not re.fullmatch(r'[a-f0-9]{32}',str(ident)):
        raise ValueError('Choose an existing organization review.')
    return _root(store)/ident/'plan.json'


def load(ident,store=None):
    path=_path(ident,store)
    if path.stat().st_size>128*1024*1024:raise ValueError('This organization review is too large. Choose smaller folders.')
    return json.loads(path.read_text(encoding='utf-8'))


def save(plan,store=None):
    write_json_atomic(_path(plan['id'],store),plan)
    write_json_atomic(_path(plan['id'],store).parent/'review.json',summary(plan))


def summary(plan):
    return {k:plan[k] for k in ('id','status','destination','created','businesses','counts','error') if k in plan} | {
        'sources':[{**s,'excluded_count':len(s['excluded']),'excluded':s['excluded'][:100]} for s in plan['sources']],
        'issues':plan['issues'][:200],
        'review_file':str(_path(plan['id'],plan.get('_store')).parent/'review.json')}


def history(store=None):
    paths=sorted(_root(store).glob('*/review.json'),key=lambda p:p.stat().st_mtime,reverse=True)[:20]
    result=[]
    for path in paths:
        try:result.append(catalog.read_json(path,{}))
        except (OSError,ValueError):continue
    return result


def _rewrite(value,ids,paths,bid,key=''):
    if isinstance(value,dict):return {k:_rewrite(v,ids,paths,bid,k) for k,v in value.items()}
    if isinstance(value,list):return [_rewrite(v,ids,paths,bid,key) for v in value]
    if not isinstance(value,str):return value
    if key=='business_id':return bid
    if value in paths and (key in {'location_reference','source_reference','content_hash_reference','path','from','to','lineage'} or key.endswith(('_ref','_refs'))):return paths[value]
    # IDs are exact reference tokens, never a substring replacement in prose.
    if value in ids and (key in {'id','lineage'} or key.endswith(('_ref','_refs'))):return ids[value]
    return value


def _refs(value,key=''):
    if isinstance(value,dict):return set().union(*(_refs(v,k) for k,v in value.items())) if value else set()
    if isinstance(value,list):return set().union(*(_refs(v,key) for v in value)) if value else set()
    return {value} if isinstance(value,str) and (key=='lineage' or key.endswith(('_ref','_refs'))) else set()


def plan(primary,sources,destination,business_map=None,store=None,progress=lambda _:None):
    primary=Path(catalog.preview(primary)['path']).resolve()
    if primary in {Path(primary.anchor),Path.home().resolve()} or Path.home().resolve().is_relative_to(primary):
        raise ValueError('Choose the folder holding a workspace, not your home or an entire drive.')
    if catalog.preview(primary)['kind']!='workspace':raise ValueError('Choose a readable saved workspace as your starting point.')
    target=folder(destination)
    if target.is_relative_to(PRODUCT_ROOT.resolve()):raise ValueError('Save the organized workspace outside the AURA application so updates keep it separate.')
    if target.exists():raise ValueError('Choose a new destination folder. Existing workspaces are never overwritten.')
    selected=[primary]
    for value in sources:
        row=catalog.preview(value);path=Path(row['path']).resolve()
        if path!=PRODUCT_ROOT.resolve() or row['kind']!='workspace':path=folder(path)
        if path not in selected:selected.append(path)
    if len(selected)>24:raise ValueError('Choose up to 24 folders for one review.')
    for i,path in enumerate(selected):
        if target.is_relative_to(path) or path.is_relative_to(target):raise ValueError('Choose a destination outside the selected original folders.')
        if any(path.is_relative_to(other) or other.is_relative_to(path) for other in selected[:i]):
            raise ValueError('Selected folders overlap. Select the containing folder once.')
    ident=uuid.uuid4().hex;mapping=business_map or {};out={};canonical={};candidates=[];all_sources=[];issues=[];businesses={};duplicates=0
    views={};source_files=[];signatures={};primary_paths={}
    for index,source in enumerate(selected):
        files,omitted=snapshot(source,progress);row=catalog.preview(source)
        skey=hashlib.sha256(str(source).encode()).hexdigest()[:10]
        source_bids=[b['id'] for b in row['businesses']]
        groups={bid:mapping.get(str(source)+'|'+bid,bid) for bid in source_bids}
        if index==0 and any(bid!=group for bid,group in groups.items()):
            raise ValueError('Keep the starting workspace business identities unchanged; group additional copies into them.')
        if any(not re.fullmatch(r'[a-z0-9][a-z0-9_-]{0,63}',bid) for bid in groups.values()):
            raise ValueError('Choose a valid business grouping in the review.')
        for business in row['businesses']:
            businesses.setdefault(groups[business['id']],business['name'])
        first_bid=next(iter(groups.values()),mapping.get(str(source)+'|',next(iter(businesses),'workspace')))
        if first_bid not in businesses:raise ValueError('Choose an existing business for these project files.')
        if row['kind'] not in {'workspace','unrecognized'}:
            raise ValueError('This folder needs attention before consolidation: '+str(source))
        rows,excluded=storage.workspace_files(source,hashes=True)
        # Explicit local Asset references in legacy application folders matter too.
        if row['kind']=='workspace':rows=storage.backup_plan(source,hashes=True)['rows']
        rows=[r for r in rows if r[0].as_posix() in files]
        profile=source/'.businessos/workspace.json'
        if profile.is_file():
            meta=Path('organization')/ident/'sources'/skey/'workspace-profile.json'
            out[meta.as_posix()]={'source':str(profile),'sha256':_sha256(profile),'bytes':profile.stat().st_size}
        selected_names={r[0].as_posix() for r in rows}
        excluded=sorted((set(excluded)| (set(files)-selected_names))- {'.businessos/workspace.json'})
        import_root=Path('attachments')/first_bid/'imports'/skey
        def imported(rel):
            parts=rel.parts;owner=parts[1] if len(parts)>1 and parts[0] in {'instances','knowledge','attachments'} else parts[2] if len(parts)>2 and parts[:2]==('runtime','runs') else None
            if owner is None and len(set(groups.values()))>1:return Path('projects')/'imports'/skey/rel
            return Path('attachments')/groups.get(owner,first_bid)/'imports'/skey/rel
        same_tree=index>0 and files==source_files[0]
        paths={}
        for rel,path,digest,size in rows:
            name=rel.as_posix()
            if index==0 or same_tree:
                dest=rel
            else:
                dest=imported(rel)
                if path.name in INSTRUCTIONS:dest=dest.with_name(dest.name+'.source.txt')
            paths[name]=dest.as_posix();paths[str(path)]=dest.as_posix()
        ambiguous=set()
        for rel,_,_,_ in rows:
            dest=Path(paths[rel.as_posix()])
            for ancestor in list(rel.parents)[:-1]:
                offset=len(rel.parts)-len(ancestor.parts)
                mapped=dest.parents[offset-1].as_posix()
                for key in (ancestor.as_posix(),str(source/ancestor)):
                    if key in ambiguous:continue
                    if key in paths and paths[key]!=mapped:paths.pop(key);ambiguous.add(key)
                    else:paths[key]=mapped
        equivalence={}
        directory_hashes={}
        for rel,path,digest,size in rows:
            equivalence[rel.as_posix()]='file-bytes:'+digest;equivalence[str(path)]='file-bytes:'+digest
            for ancestor in list(rel.parents)[:-1]:directory_hashes.setdefault(ancestor,[]).append((rel.relative_to(ancestor).as_posix(),digest))
        for ancestor,entries in directory_hashes.items():
            token='directory-bytes:'+hashlib.sha256(json.dumps(sorted(entries)).encode()).hexdigest()
            equivalence[ancestor.as_posix()]=token;equivalence[str(source/ancestor)]=token
        ids={}
        record_rows=[]
        for rel,path,digest,size in rows:
            parts=rel.parts
            if len(parts)>=3 and parts[0]=='instances' and parts[1] in groups and path.suffix=='.json' and 'history' not in parts:
                try:obj=json.loads(path.read_text(encoding='utf-8'))
                except (ValueError,UnicodeError):obj={}
                if isinstance(obj,dict) and obj.get('object_type') and obj.get('id'):
                    bid=groups[parts[1]];old=obj['id']
                    ids[old]=old if bid==parts[1] else old.split('_',1)[0]+'_'+hashlib.sha256((skey+bid+old).encode()).hexdigest()[:20]
                    record_rows.append((rel,obj,bid))
        conflicts=set()
        for rel,obj,bid in record_rows:
            rewritten=_rewrite(obj,ids,paths,bid)
            key=(bid,rewritten['id'])
            signature=json.dumps(_rewrite(obj,ids,equivalence,bid),sort_keys=True,ensure_ascii=False)
            if key in signatures and signatures[key]!=signature:conflicts.add(obj['id'])
            if obj['object_type']=='Business' and any(k[0]==bid and v['object_type']=='Business' for k,v in canonical.items()) and key not in canonical:
                conflicts.add(obj['id'])
        variants=set()
        for rel,path,digest,size in rows:
            name=rel.as_posix();dest=safe_relative(paths[name])
            if index and rel.parts[0] not in {'instances','runtime','.businessos','knowledge'} and name in source_files[0] and source_files[0][name]['sha256']!=digest:
                variants.add('/'.join(rel.parts[:2]) if rel.parts[0]=='projects' and len(rel.parts)>2 else rel.parts[0])
            if index==0:
                parts=dest.parts
                if len(parts)>1 and parts[0] in {'instances','knowledge','attachments'} and parts[1] in groups:
                    dest=Path(parts[0])/groups[parts[1]]/Path(*parts[2:])
            existing=out.get(dest.as_posix())
            if existing and existing['sha256']==digest:duplicates+=1;continue
            if existing:
                dest=imported(rel)
            out[dest.as_posix()]={'source':str(path),'sha256':digest,'bytes':size}
        for variant in sorted(variants):issues.append({'kind':'file_alternative','source':str(source),'file':variant,
            'message':'Different files were kept as an alternative copy. Your starting project stays intact.'})
        for rel,obj,bid in record_rows:
            rewritten=_rewrite(obj,ids,paths,bid);key=(bid,rewritten['id'])
            if index==0:
                canonical[key]=rewritten
                signatures[key]=json.dumps(_rewrite(obj,ids,equivalence,bid),sort_keys=True,ensure_ascii=False)
                primary_paths[key]=rel.as_posix()
                archived=(Path('organization')/ident/'sources'/skey/rel).as_posix()
                original=source/rel
                out[archived]={'source':str(original),'sha256':_sha256(original),'bytes':original.stat().st_size}
                continue
            if key in canonical:
                if obj['id'] in conflicts:
                    issues.append({'kind':'business_context','business':bid,'source':str(source),'file':rel.as_posix(),
                        'message':'A different copy was preserved for review. The starting workspace remains current.'})
                else:duplicates+=1
                continue
            if obj['id'] in conflicts:
                issues.append({'kind':'business_context','business':bid,'source':str(source),'file':rel.as_posix(),
                    'message':'The starting business context stays current. This alternative was preserved for review.'});continue
            candidates.append((key,rewritten,obj,rel,source,conflicts,ids,paths))
        if index>0:
            for bid,group in groups.items():
                config=source/'instances'/bid/'instance.json'
                name=(Path('instances')/group/'instance.json').as_posix()
                if name not in out and config.is_file():
                    data=json.loads(config.read_text(encoding='utf-8'));data['business_id']=group;out[name]={'json':data}
        # Preserve different historical/configuration files outside active records.
        if index==0:
            try:views=storage.load_view(source)
            except (OSError,ValueError):issues.append({'kind':'settings','message':'Saved view settings need attention; originals remain available.'})
        else:
            incoming=storage.view_preferences(source) if row['kind']=='workspace' else {}
            for bid,prefs in incoming.get('library',{}).items():
                kept=views.setdefault('library',{}).setdefault(groups.get(bid,bid),{})
                for field,limit in [('favorites',500),('recent',24)]:
                    kept[field]=list(dict.fromkeys([*kept.get(field,[]),*prefs.get(field,[])]))[:limit]
            for bid,items in incoming.get('file_locations',{}).items():
                target_bid=groups.get(bid,bid);kept=views.setdefault('file_locations',{}).setdefault(target_bid,[])
                for item in items:
                    original=Path(item['path']);inside=original.is_relative_to(source)
                    item={**item,'id':skey+'-'+item['id'],'path':paths.get(original.relative_to(source).as_posix(),str(original)) if inside else str(original),'relative':inside}
                    if not any(r.get('path')==item['path'] and r.get('relative',False)==inside for r in kept):kept.append(item)
            if len(set(groups.values()))>1 and any(name.startswith('projects/imports/'+skey+'/') for name in out):
                for group in set(groups.values()):
                    views.setdefault('file_locations',{}).setdefault(group,[]).append({'id':skey+'-shared',
                        'name':'Shared project files from '+source.name,'kind':'folder','path':(Path('projects')/'imports'/skey).as_posix(),'relative':True})
        if omitted:issues.append({'kind':'linked_paths','source':str(source),'message':'Directory links were kept in the original folder and need an explicit connection.','files':omitted})
        all_sources.append({'path':str(source),'name':row['name'],'key':skey,'kind':row['kind'],'groups':groups,'owner':first_bid,
            'files':len(files),'bytes':sum(f['bytes'] for f in files.values()),'excluded':excluded,'linked_paths':omitted})
        source_files.append(files)
    # A new record depending on a divergent record is also held for review.
    blocked={}
    for _,_,_,_,source,conflicts,_,_ in candidates:blocked.setdefault(str(source),set()).update(conflicts)
    changed=True
    while changed:
        changed=False
        for _,obj,original,_,source,_,_,_ in candidates:
            bad=blocked[str(source)]
            if original['id'] not in bad and _refs(original)&bad:bad.add(original['id']);changed=True
    for key,obj,original,rel,source,_,_,_ in candidates:
        if original['id'] in blocked[str(source)]:
            issues.append({'kind':'business_context','business':key[0],'source':str(source),'file':rel.as_posix(),
                           'message':'This record depends on a conflicting copy. Its original is preserved for review.'});continue
        try:validate_canonical(obj['object_type'],obj)
        except ValueError:
            issues.append({'kind':'business_context','business':key[0],'source':str(source),'file':rel.as_posix(),
                           'message':'This record needs a supported update before it can become active. Its source copy is preserved.'});continue
        if key in canonical:
            if canonical[key]!=obj:issues.append({'kind':'business_context','business':key[0],'source':str(source),'file':rel.as_posix(),
                'message':'Additional copies differ. The earlier selected copy stays current and the alternative remains available.'})
            continue
        canonical[key]=obj
        parts=list(rel.parts);parts[1]=key[0]
        if Path(parts[-1]).stem==original['id']:parts[-1]=obj['id']+'.json'
        destination=Path(*parts).as_posix()
        out[destination]={'json':obj}
    for key,name in primary_paths.items():
        out[name]={'json':canonical[key]}
    for index,source in enumerate(all_sources):
        for bid in set(source['groups'].values()) or {source['owner']}:
            oid='src_organization_'+ident+'_'+source['key']+'_'+hashlib.sha256(bid.encode()).hexdigest()[:6]
            stamp=datetime.fromtimestamp(time.time(),timezone.utc).isoformat()
            obj={'id':oid,'object_type':'SourceRecord','schema_version':'1.0.0','business_id':bid,
                'source_type':'workspace_organization_input','source_reference':
                    (Path('organization')/ident/'sources'/source['key']).as_posix(),
                'origin':source['path'],'retrieved_at':stamp,'access_scope':'User-selected local organization material; preserved alternatives are not established business truth.',
                'extensions':{'businessos':{'authority':'unknown','display_name':'Work brought from '+source['name']}}}
            validate_canonical('SourceRecord',obj)
            out[(Path('instances')/bid/'intelligence/sources'/(oid+'.json')).as_posix()]={'json':obj}
        out[(Path('organization')/ident/'sources'/source['key']/'files.json').as_posix()]={'json':{
            'origin':source['path'],'files':source_files[index],'excluded':source['excluded']}}
    if len({name.casefold() for name in out})!=len(out):
        raise ValueError('Some file names differ only by letter case and would overlap on another computer. Keep the originals and ask your AI to rename the conflicting files and update their links before retrying.')
    for name in out:
        for part in safe_relative(name).parts:
            if re.search(r'[<>:"|?*]',part) or part.endswith((' ','.')) or re.fullmatch(r'(?i:con|prn|aux|nul|com[1-9]|lpt[1-9])',part.split('.')[0]):
                raise ValueError('A file name is incompatible with another platform: '+part+'. Keep the original and choose a portable name before retrying.')
    required=sum(row.get('bytes',len(json.dumps(row.get('json',{})).encode())) for row in out.values())
    ancestor=target.parent
    while not ancestor.exists():ancestor=ancestor.parent
    if shutil.disk_usage(ancestor).free<required+16*1024*1024:raise ValueError('There is not enough free space for the consolidated copy. Choose another drive or free space first.')
    result={'id':ident,'status':'review','created':time.time(),'destination':str(target),'primary':str(primary),
        'sources':all_sources,'snapshots':source_files,'files':out,'view':views,'businesses':[{'id':bid,'name':name} for bid,name in businesses.items()],
        'counts':{'original_files':sum(s['files'] for s in all_sources),'output_files':len(out),'duplicates':duplicates,
                  'needs_review':len(issues),'bytes':required},'issues':issues,'_store':str(Path(store)) if store else None}
    save(result,store);write_json_atomic(_path(ident,store).parent/'review.json',summary(result))
    return summary(result)


def _unchanged(plan,progress=lambda _:None):
    for source,expected in zip(plan['sources'],plan['snapshots']):
        actual,links=snapshot(source['path'],progress)
        if actual!=expected or links!=source['linked_paths']:
            raise ValueError('A selected original changed after the review. Your originals are safe. Create an updated review before combining them.')


def apply(ident,store=None,progress=lambda _:None,cancel=lambda:False):
    p=load(ident,store);target=folder(p['destination'])
    if p['status']=='complete':
        if target.is_dir():return summary(p)
        raise ValueError('The completed workspace has moved. Find its folder before retrying.')
    if target.exists():raise ValueError('The destination now exists. Choose a new folder; nothing was overwritten.')
    target.parent.mkdir(parents=True,exist_ok=True)
    stage=target.parent/('.aura-organizing-'+ident)
    if stage.exists() and catalog.read_json(stage/'.aura-operation.json',{}).get('id')!=ident:
        raise ValueError('The preparation folder belongs to another operation. Choose another destination.')
    stage.mkdir(exist_ok=True);write_json_atomic(stage/'.aura-operation.json',{'id':ident})
    p['status']='preparing';save(p,store)
    try:
        _unchanged(p,progress)
        for number,(name,row) in enumerate(p['files'].items()):
            if cancel():raise ValueError('Organization stopped. Your originals are unchanged. You can retry this review.')
            progress(f'Copying {number+1} of {len(p["files"])} files')
            dest=stage/safe_relative(name);dest.parent.mkdir(parents=True,exist_ok=True)
            if dest.resolve()!=dest or not dest.resolve().is_relative_to(stage.resolve()):raise ValueError('A preparation folder was linked elsewhere. The originals were kept.')
            if 'json' in row:write_json_atomic(dest,row['json']);continue
            if dest.is_file() and _sha256(dest)==row['sha256']:continue
            from migrate_workspace import _copy_verified
            _copy_verified(stage,[(safe_relative(name),Path(row['source']),row['sha256'],row['bytes'])],lambda:progress(f'Copying {number+1} of {len(p["files"])} files'))
        write_json_atomic(stage/storage.VIEW_FILE,p['view'])
        storage.normalize_file_links(stage,p['primary'])
        profile=catalog.read_json(Path(p['primary'])/'.businessos/workspace.json',{})
        env=dict(os.environ,BUSINESSOS_WORKSPACE=str(stage),BUSINESSOS_WORKSPACE_CONFIG=str(stage/'.businessos/workspace.json'))
        flags={'creationflags':subprocess.CREATE_NO_WINDOW} if os.name=='nt' else {}
        configured=subprocess.run([sys.executable,str(PRODUCT_ROOT/'scripts/configure_workspace.py'),str(stage),'--profile',profile.get('profile','power_user'),'--no-link','--json',
            *(['--no-knowledge'] if profile.get('knowledge_enabled') is False else [])],env=env,capture_output=True,timeout=45,**flags)
        if configured.returncode:raise ValueError('The files were copied, but workspace preparation needs attention. Originals are unchanged; ask your AI to inspect the saved review.')
        for business in p['businesses']:
            progress('Checking '+business['name'])
            checked=subprocess.run([sys.executable,str(PRODUCT_ROOT/'scripts/validate_business.py'),business['id']],env=env,capture_output=True,timeout=90,**flags)
            if checked.returncode:
                detail=checked.stdout.decode('utf-8',errors='replace')[-5000:]
                (stage/'organization-validation.txt').write_text(detail,encoding='utf-8')
                raise ValueError('The copied business context needs attention before it can be opened. Your originals remain unchanged. Ask your AI to review the preparation report.')
        _unchanged(p,progress)
        for name,row in p['files'].items():
            dest=stage/safe_relative(name)
            if 'json' in row:
                if json.loads(dest.read_text(encoding='utf-8'))!=row['json']:
                    raise ValueError('A business record changed while preparing the copy. Originals were kept.')
            elif name!=storage.VIEW_FILE and _sha256(dest)!=row['sha256']:
                raise ValueError('A copied file did not verify. The workspace was not activated; originals are safe.')
        if cancel():raise ValueError('Organization stopped before opening the new workspace. Originals are unchanged.')
        expected=set(p['files'])|{'.aura-operation.json',storage.VIEW_FILE,'.businessos/workspace.json','.gitignore','WORKSPACE.md','knowledge/README.md'}
        unexpected=[file.relative_to(stage).as_posix() for file in stage.rglob('*') if file.is_file() and file.relative_to(stage).as_posix() not in expected]
        if unexpected:
            raise ValueError('Unexpected files appeared in the prepared copy. The originals were kept. Ask your AI to inspect the preparation before retrying.')
        # Portable receipt is informational. Retirement permission stays machine-local.
        write_json_atomic(stage/'organization'/ident/'review.json',summary(p))
        (stage/'.aura-operation.json').unlink()
        os.rename(stage,target)
        p['status']='complete';p['completed']=time.time();p.pop('error',None);save(p,store)
        write_json_atomic(target/'organization'/ident/'review.json',summary(p))
        return summary(p)
    except Exception as exc:
        p['status']='incomplete';p['error']=str(exc);save(p,store)
        raise


def dependency_reasons(source,references=()):
    root=Path(source).resolve();reasons=[]
    for value in references:
        try:
            path=Path(str(value)).expanduser().resolve()
            if path.is_relative_to(root):reasons.append('An AI chat, linked file, custom view, startup entry, or scheduled task still uses this folder.');break
        except (ValueError,OSError):pass
    return reasons


def known_references(store=None):
    """Read local connection/scheduler metadata, never provider credential stores."""
    values=[os.environ['BUSINESSOS_WORKSPACE']] if os.environ.get('BUSINESSOS_WORKSPACE') else []
    def collect(value,key=''):
        if isinstance(value,dict):
            for k,v in value.items():collect(v,k)
        elif isinstance(value,list):
            for v in value:collect(v,key)
        elif isinstance(value,str) and key in {'workspace','workspace_root','cwd','cwds','path','instructions','product','argv'}:
            values.append(value)
    root=Path(store or state_dir())
    for path in root.glob('*.json'):
        if path.name in {'recent-workspaces.json','workspace-selection.json','previous-product-workspace-link.json'}:continue
        try:collect(catalog.read_json(path,{}))
        except (OSError,ValueError):pass
    import workspace_schedules,workspace_startup
    native=workspace_schedules.inventory();collect(native.get('items',[]));collect(workspace_startup.status())
    return values


def _destination_intact(p):
    root=Path(p['destination'])
    if not root.is_dir():return False
    for name,row in p['files'].items():
        if name==storage.VIEW_FILE:continue
        path=root/safe_relative(name)
        try:
            if 'json' in row:
                # The exact source records were archived; current truth may
                # legitimately evolve without making that archive disposable.
                if not path.is_file():return False
            elif _sha256(path)!=row['sha256']:return False
        except OSError:return False
    return True


def retirement_review(ident,store=None,references=()):
    p=load(ident,store)
    if p['status']!='complete':raise ValueError('Finish and verify the consolidated workspace before retiring originals.')
    rows=[];references=[*references,*known_references(store)]
    retired={r['original'] for r in recovery(store) if r.get('operation')==ident and r['status'] in {'available','changed'}}
    for source,expected in zip(p['sources'],p['snapshots']):
        reasons=dependency_reasons(source['path'],references)
        if source['excluded']:reasons.append('Some excluded or private files remain here. Review them before retiring the whole folder.')
        if source['linked_paths']:reasons.append('Directory links need attention before this folder can be retired.')
        if source['kind']!='workspace':reasons.append('This is a linked project folder. Keep its original ownership and location unless you deliberately move it yourself.')
        if not _destination_intact(p):reasons.append('Some consolidated files changed or are unavailable. Review the saved result before retiring originals.')
        try:
            files,links=snapshot(source['path'])
            if files!=expected or links!=source['linked_paths']:reasons.append('The original changed after consolidation. Review its new work first.')
        except (OSError,ValueError):reasons.append('The original folder is unavailable or already retired.')
        recovery_root=catalog.default_home().parent/'AURA Recovery'
        if recovery_root.anchor.lower()!=Path(source['path']).anchor.lower():recovery_root=Path(source['path']).parent/'AURA Recovery'
        rows.append({'path':source['path'],'name':source['name'],'eligible':not reasons,'retired':source['path'] in retired,
                     'reasons':['This original is in AURA Recovery.'] if source['path'] in retired else reasons,'recovery':str(recovery_root)})
    return {'id':ident,'items':rows}


def retire(ident,source,days=0,store=None,references=()):
    if days not in {0,7,30,90}:raise ValueError('Choose Keep until I remove it, 7, 30, or 90 days.')
    p=load(ident,store);source=folder(source)
    row=next((r for r in retirement_review(ident,store,references)['items'] if Path(r['path'])==source),None)
    if not row or not row['eligible']:raise ValueError('This original still needs attention and was kept in place. Review its cleanup details.')
    index=next(i for i,r in enumerate(p['sources']) if Path(r['path'])==source)
    eid=uuid.uuid4().hex;root=Path(row['recovery']).resolve();root.mkdir(parents=True,exist_ok=True)
    destination=root/(source.name+'-'+eid[:8])
    if root.is_relative_to(source) or destination.exists():raise ValueError('Choose a separate recovery location. The original was kept.')
    entry={'id':eid,'operation':ident,'original':str(source),'path':str(destination),'recovery_root':str(root),
        'destination':p['destination'],'snapshot':p['snapshots'][index],'retired':time.time(),'days':days,'status':'moving'}
    entry_file=_root(store)/'recovery'/ (eid+'.json');write_json_atomic(entry_file,entry)
    os.rename(source,destination)  # Same filesystem only: failure never turns into copy-and-delete.
    entry.update(status='available',expires=time.time()+days*86400 if days else None);write_json_atomic(entry_file,entry)
    return {k:v for k,v in entry.items() if k!='snapshot'}


def recovery(store=None):
    result=[]
    for path in sorted((_root(store)/'recovery').glob('*.json')):
        try:
            entry=catalog.read_json(path,{})
            if entry.get('status')=='moving' and Path(entry['path']).is_dir() and not Path(entry['original']).exists():
                entry.update(status='available',expires=None,days=0);write_json_atomic(path,entry)
            result.append({k:v for k,v in entry.items() if k!='snapshot'})
        except (OSError,ValueError,KeyError):continue
    return result


def recover(ident,action,store=None,days=None,references=(),progress=lambda _:None):
    if not re.fullmatch(r'[a-f0-9]{32}',str(ident)):raise ValueError('Choose an item from AURA Recovery.')
    record=_root(store)/'recovery'/(ident+'.json');entry=catalog.read_json(record,{})
    if entry.get('status') not in {'available','changed'}:raise ValueError('This recovery item is unavailable or already restored.')
    path=Path(entry['path']);root=Path(entry['recovery_root']).resolve()
    if path.resolve()!=path or path.parent!=root or not path.name.endswith('-'+ident[:8]) or path.is_symlink():
        raise ValueError('The recovery location changed. Keep it and inspect its files manually.')
    if action=='restore':
        original=folder(entry['original'])
        if original.exists():raise ValueError('The original location now contains work. Choose another location manually; no files were replaced.')
        original.parent.mkdir(parents=True,exist_ok=True);os.rename(path,original);entry['status']='restored'
    elif action=='retention':
        if days not in {0,7,30,90}:raise ValueError('Choose a supported retention period.')
        entry.update(days=days,expires=time.time()+days*86400 if days else None)
    elif action=='remove':
        operation=load(entry['operation'],store)
        if entry.get('kind')=='preparation':
            if entry.get('unaccounted'):raise ValueError('Additional files were preserved in this unfinished copy. Ask your AI to preserve or review them before permanent cleanup.')
            _unchanged(operation,progress)
        elif not _destination_intact(operation):raise ValueError('The consolidated result changed or is unavailable. Keep the recovery copy and review the saved result.')
        if Path(entry['original']).exists():raise ValueError('Work appeared at the original location again. Keep this recovery copy and review both folders.')
        if dependency_reasons(path,[*references,*known_references(store)]):raise ValueError('Something still uses this recovery folder. It was kept.')
        actual,links=snapshot(path,progress)
        if actual!=entry['snapshot'] or links:
            entry.update(status='changed',expires=None,days=0);write_json_atomic(record,entry)
            raise ValueError('This recovery copy changed. Automatic removal is disabled; review its new work first.')
        # Absolute path and owned parent/name were checked above. Only this
        # explicitly retired, unchanged entry is eligible for recursive removal.
        progress('Removing an unchanged retired copy')
        shutil.rmtree(path);entry['status']='removed'
    else:raise ValueError('Choose Restore, change retention, or Remove permanently.')
    write_json_atomic(record,entry)
    return {k:v for k,v in entry.items() if k!='snapshot'}


def discard(ident,store=None):
    p=load(ident,store)
    if p['status']=='complete':raise ValueError('This workspace is complete. Use optional cleanup to review its originals.')
    stage=Path(p['destination']).parent/('.aura-organizing-'+ident)
    if not stage.exists():p['status']='discarded';save(p,store);return {'status':'discarded'}
    if stage.resolve()!=stage or catalog.read_json(stage/'.aura-operation.json',{}).get('id')!=ident:
        raise ValueError('This preparation folder changed ownership. Keep it and ask your AI to inspect it.')
    files,links=snapshot(stage)
    allowed=set(p['files'])|{'.aura-operation.json',storage.VIEW_FILE,'.businessos/workspace.json','.gitignore','WORKSPACE.md','knowledge/README.md','organization-validation.txt'}
    if links:raise ValueError('Directory links appeared in the preparation folder. Keep it and ask your AI to inspect them before cleanup.')
    eid=uuid.uuid4().hex;root=stage.parent/'AURA Recovery';root.mkdir(exist_ok=True)
    destination=root/(Path(p['destination']).name+'-preparation-'+eid[:8])
    entry={'id':eid,'kind':'preparation','operation':ident,'original':str(stage),'path':str(destination),'recovery_root':str(root),
        'destination':p['destination'],'snapshot':files,'unaccounted':sorted(set(files)-allowed),'retired':time.time(),'days':0,'expires':None,'status':'moving'}
    record=_root(store)/'recovery'/(eid+'.json');write_json_atomic(record,entry)
    os.rename(stage,destination);entry['status']='available';write_json_atomic(record,entry)
    p['status']='discarded';save(p,store)
    return {k:v for k,v in entry.items() if k!='snapshot'}


def expire(store=None,references=(),progress=lambda _:None):
    messages=[]
    for entry in recovery(store):
        if entry.get('status')=='available' and entry.get('expires') and entry['expires']<=time.time():
            progress('Checking a retired copy before removal')
            try:recover(entry['id'],'remove',store,references=references,progress=progress)
            except (OSError,ValueError) as exc:
                messages.append(str(exc))
                record=_root(store)/'recovery'/(entry['id']+'.json')
                saved=catalog.read_json(record,{})
                saved.update(expires=None,days=0,notice=str(exc));write_json_atomic(record,saved)
    return messages


if __name__=='__main__':
    parser=argparse.ArgumentParser(description='Review and consolidate saved AURA work; originals stay intact.')
    sub=parser.add_subparsers(dest='action',required=True)
    scan=sub.add_parser('plan');scan.add_argument('--primary',required=True);scan.add_argument('--source',action='append',default=[]);scan.add_argument('--destination',required=True);scan.add_argument('--business-map',help='Optional JSON file mapping source-path|business-id to destination business ID.')
    for action in ('apply','status','cleanup-preview','discard'):
        command=sub.add_parser(action);command.add_argument('id')
    command=sub.add_parser('retire');command.add_argument('id');command.add_argument('source');command.add_argument('--days',type=int,default=0)
    sub.add_parser('recovery')
    sub.add_parser('cleanup-expired')
    for action in ('restore','remove'):
        command=sub.add_parser(action);command.add_argument('id')
    args=parser.parse_args()
    try:
        if args.action=='plan':result=plan(args.primary,args.source,args.destination,catalog.read_json(args.business_map,{}) if args.business_map else None)
        elif args.action=='apply':result=apply(args.id)
        elif args.action=='status':result=summary(load(args.id))
        elif args.action=='cleanup-preview':result=retirement_review(args.id)
        elif args.action=='discard':result=discard(args.id)
        elif args.action=='retire':result=retire(args.id,args.source,args.days)
        elif args.action=='recovery':result=recovery()
        elif args.action=='cleanup-expired':result={'notices':expire()}
        else:result=recover(args.id,'restore' if args.action=='restore' else 'remove')
        print(json.dumps(result,ensure_ascii=False,indent=2))
    except (OSError,ValueError,subprocess.SubprocessError) as exc:parser.exit(1,str(exc)+'\n')
