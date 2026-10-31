"""Public contributions over the existing selected-share format and import engine.

Preparation is local. Files are intentional selections, not automatically anonymized.
Old workflow InnovationPackages are converted into readable source material at import.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import shutil
import uuid
import zipfile

from _common import write_json_atomic
import workspace_sharing as share

TERMS = 'aura-community-1'
HOME = 'https://viraltrac.com/aura/community/'
MAX_ARCHIVE = 10 * 1024 ** 2
MAX_EXPANDED = 32 * 1024 ** 2
MAX_ENTRIES = 500
KINDS = {'workflow', 'layout', 'starter'}


def archive_manifest(archive):
    infos = archive.infolist()
    if len(infos)>MAX_ENTRIES or sum(i.file_size for i in infos)>MAX_EXPANDED:
        raise ValueError('Community packages support up to 500 files and 32 MB of expanded content.')
    names = [i.filename for i in infos]
    if len({n.casefold() for n in names})!=len(names):
        raise ValueError('This package contains overlapping file names.')
    for item in infos:
        share.safe(item.filename)
        if item.is_dir() or ((item.external_attr>>16)&0o170000)==0o120000:
            raise ValueError('Folder links and directory entries are not supported in community packages.')
    return names


def method_text(process):
    parts = ['# '+str(process['title']), '', str(process['purpose'])]
    for field,heading in [('applies_when','When to use it'),('does_not_apply_when','When it may not fit'),
                          ('instructions','Method'),('verification','What to check')]:
        values = process.get(field) or []
        if values:
            parts.extend(['', '## '+heading, '', *('- '+str(value) for value in values)])
    return '\n'.join(parts)+'\n'


def _portable_path(location):
    parts = location.split('/')
    if parts[:1]==['attachments'] and len(parts)>2:
        parts=parts[2:]
        if parts[:1]==['work']:parts=parts[1:]
    elif parts[:1]==['knowledge'] and len(parts)>2:
        parts=parts[2:]
    elif parts[:1]==['external'] and len(parts)>2:
        parts=parts[2:]
    value='/'.join(parts)
    share.safe(value)
    if value.upper()=='COMMUNITY.JSON':
        raise ValueError('Rename COMMUNITY.json in your selection; that name is reserved for package details.')
    return value


def public_path(value):
    share.safe(value)
    if any(re.fullmatch(r'(\.env(?:\..*)?|\.git|\.sharing|\.businessos|credentials|secrets|node_modules|__pycache__|\.ssh|\.aws)', part, re.I) for part in Path(value).parts) or re.search(r'\.(exe|dll|com|bat|cmd|ps1|pem|key|p12|pfx)$', value, re.I):
        raise ValueError('Remove private settings, credentials, dependencies and executable installers from the public selection.')


def prepare(root, bid, keys, name, note='', kind='starter', description='', author='', based_on='', store=None, locations=None):
    root=share.unlinked(root)
    share.business(root,bid)
    if kind not in KINDS or not str(name).strip() or len(str(name))>160:
        raise ValueError('Choose a contribution type and a name of up to 160 characters.')
    if not isinstance(keys,list) or not keys:
        raise ValueError('Select reusable files, folders, or methods first.')
    inventory=share.inventory(root,bid,locations)
    available={r['key']:r for r in inventory['items']}
    objects=share.objects(root,bid)
    file_keys=[];methods=[]
    for key in dict.fromkeys(keys):
        row=available.get(key)
        if not row:raise ValueError('Some selected items are missing. Refresh your selection.')
        if row['kind']!='record':file_keys.append(key);continue
        obj,path=objects[key[7:]]
        if obj['object_type']=='ProcessExtension':methods.append((obj,path));continue
        if obj['object_type']=='Asset':
            ref=obj.get('location_reference','')
            target=(Path(ref) if Path(ref).is_absolute() else root/ref).resolve()
            linked=next((r for r in inventory['items'] if r.get('_path')==str(target)),None)
            if linked:file_keys.append(linked['key']);continue
        raise ValueError('For public sharing, select reusable files, folders or methods. Business records and results stay private. Export a private package for other information.')
    ident=uuid.uuid4().hex;job=share._job(ident,store);payload=job/'payload'
    payload.mkdir(parents=True)
    entries=[];inputs=[];folders=[];notes=[];seen=set()
    def add(relative,content,title=None):
        public_path(relative)
        path='files/'+relative
        if path.casefold() in seen:raise ValueError('Selected public file names overlap. Rename them before preparing a package.')
        seen.add(path.casefold())
        if len(entries)>=MAX_ENTRIES-2 or sum(e['bytes'] for e in entries)+len(content)>MAX_EXPANDED-65536:
            raise ValueError('Choose a smaller community package (up to 500 files and 32 MB).')
        dest=payload/share.safe(path);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(content)
        entries.append({'key':'file:'+relative,'kind':'file','title':title or Path(relative).name,'path':path,
                        'sha256':share.digest(content),'bytes':len(content),'supporting':False,'dependencies':[]})
    try:
        for key in dict.fromkeys(file_keys):
            row=available[key];path=Path(row['_path']);found=share.walk(path,notes)
            if row['kind']=='folder':folders.append({'path':str(path),'files':[str(p) for p in found]})
            for file in found:
                if any(i['path']==str(file) for i in inputs):continue
                rel=_portable_path(row['location'])+('/'+file.relative_to(path).as_posix() if path.is_dir() else '')
                if file.stat().st_size>MAX_EXPANDED-65536:
                    raise ValueError('Choose smaller files for this community package (up to 32 MB expanded).')
                with file.open('rb') as stream:content=stream.read(MAX_EXPANDED+1)
                digest=share.digest(content)
                if share._sha256(file)!=digest:raise ValueError('A selected file changed. Prepare it again.')
                add(rel,content);inputs.append({'path':str(file),'sha256':digest})
        for obj,path in methods:
            add('methods/'+re.sub(r'[^a-zA-Z0-9_-]+','-',obj['title']).strip('-')[:80]+'.md',method_text(obj).encode('utf-8'),obj['title'])
            inputs.append({'path':str(path),'sha256':share._sha256(path)})
        if not entries:raise ValueError('No readable reusable content was selected.')
        notices=[]
        for filename in ('COMMUNITY-TERMS.md','LICENSE.md','PUBLISHER.json'):
            relative='aura-notices/'+filename
            add(relative,(Path(__file__).resolve().parents[1]/filename).read_bytes())
            entries[-1]['supporting']=True
            notices.append('file:'+relative)
        for entry in entries:
            if entry['key'] not in notices:entry['dependencies']=notices[:]
        if based_on and not re.fullmatch(r'[a-zA-Z0-9_-]{1,80}',based_on):
            raise ValueError('Use the original community contribution ID for attribution.')
        details={'format':'aura-community-profile-1','kind':kind,'description':str(description).strip()[:1000],
                 'author':str(author).strip()[:80],'based_on':based_on,'terms':TERMS,
                 'notice':'Review every file before sharing. Selected prose, images and files may still identify people or businesses.'}
        add('COMMUNITY.json',(json.dumps(details,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
        # An opaque origin supports updates without publishing the source business identity.
        origin_file=share.metadata(root,bid)/'community-origin.json'
        with share.destination_lock(root):
            origin=share.read(origin_file)
            if not origin:
                origin=uuid.uuid4().hex;write_json_atomic(origin_file,origin)
        manifest={'format':share.FORMAT,'name':str(name).strip(),'origin':{'id':origin,'business_id':'community','name':details['author'] or 'Community contributor'},
                  'created':share.now(),'note':str(note)[:8000],'items':sorted(entries,key=lambda e:e['key']),'notes':[]}
        manifest['revision']=share.digest({k:manifest[k] for k in ('name','origin','note','items','notes')})
        write_json_atomic(payload/'AURA-SHARE.json',manifest)
        write_json_atomic(job/'source.json',{'root':str(root),'business':bid,'keys':keys,'inputs':inputs,'folders':folders,'community':True})
        return {**share.package_summary(ident,manifest),'community_profile':details}
    except Exception:
        shutil.rmtree(job)
        raise


def import_package(path,store=None):
    try:return _import_package(path,store)
    except (zipfile.BadZipFile, RuntimeError, json.JSONDecodeError, KeyError, TypeError):
        raise ValueError('This package could not be read. Choose a verified Aura sharing or InnovationPackage ZIP.') from None


def _import_package(path,store=None):
    path=share.unlinked(path)
    if path.stat().st_size>share.MAX_BYTES:raise ValueError('Choose a smaller sharing package.')
    with zipfile.ZipFile(path) as archive:
        names=archive.namelist()
        if 'AURA-SHARE.json' in names:
            result=share.import_package(path,store)
            manifest,payload=share.load_package(result['id'],store)
            profile=payload/'files/COMMUNITY.json'
            if profile.is_file():result['community_profile']=share.read(profile)
            return result
        archive_manifest(archive)
        if 'innovation-package.json' not in names or any(n not in ('innovation-package.json','README.txt','COMMUNITY-TERMS.md','LICENSE.md','PUBLISHER.json') for n in names):
            raise ValueError('Choose an Aura sharing or Innovation Exchange package.')
        from innovation_common import validate_package
        original=archive.read('innovation-package.json')
        package=json.loads(original)
        validate_package(package,require_export_approval=True)
        notices={n:archive.read(n) for n in ('COMMUNITY-TERMS.md','LICENSE.md','PUBLISHER.json') if n in names}
    ident=uuid.uuid4().hex;job=share._job(ident,store);payload=job/'payload'
    try:
        payload.mkdir(parents=True)
        relative='files/methods/'+package['package_id']+'.md'
        content=method_text(package['process']).encode('utf-8');dest=payload/share.safe(relative);dest.parent.mkdir(parents=True);dest.write_bytes(content)
        entry={'key':'file:methods/'+package['package_id']+'.md','kind':'file','title':package['process']['title'],'path':relative,
               'sha256':share.digest(content),'bytes':len(content),'supporting':False,'dependencies':[]}
        # Keep the exact original contribution too; reported evidence stays source material.
        (payload/'files'/'innovation-package.json').write_bytes(original)
        source={'key':'file:innovation-package.json','kind':'file','title':'Original contribution and reported evidence','path':'files/innovation-package.json',
                'sha256':share.digest(original),'bytes':len(original),'supporting':True,'dependencies':[]}
        notice_entries=[]
        for name,data in notices.items():
            dest=payload/'files'/'aura-notices'/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
            notice_entries.append({'key':'file:aura-notices/'+name,'kind':'file','title':name,'path':'files/aura-notices/'+name,'sha256':share.digest(data),'bytes':len(data),'supporting':True,'dependencies':[]})
        entry['dependencies']=source['dependencies']=[i['key'] for i in notice_entries]
        author=package['contributor'].get('display_name') or package['contributor'].get('pseudonym') or 'Community contributor'
        manifest={'format':share.FORMAT,'name':package['process']['title'],'origin':{'id':hashlib.sha256(package['innovation_fingerprint'].encode()).hexdigest()[:32],'business_id':'community','name':author},
                  'created':package['created_at'],'note':package['process']['purpose'],'items':[entry,source,*notice_entries],
                  'notes':['This contributed method and its reported outcomes are source material. They are not established facts about your business.']}
        manifest['revision']=share.digest({k:manifest[k] for k in ('name','origin','note','items','notes')})
        write_json_atomic(payload/'AURA-SHARE.json',manifest)
        return {**share.package_summary(ident,manifest),'original_format':'innovation-package'}
    except Exception:
        if job.exists():shutil.rmtree(job)
        raise


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--store')
    sub=parser.add_subparsers(dest='action',required=True)
    p=sub.add_parser('prepare');p.add_argument('workspace');p.add_argument('business');p.add_argument('--select',action='append',required=True)
    p.add_argument('--name',required=True);p.add_argument('--note',default='');p.add_argument('--description',default='');p.add_argument('--kind',choices=sorted(KINDS),default='starter');p.add_argument('--author',default='');p.add_argument('--based-on',default='')
    p=sub.add_parser('import');p.add_argument('path')
    args=parser.parse_args()
    result=import_package(args.path,args.store) if args.action=='import' else prepare(args.workspace,args.business,args.select,args.name,args.note,args.kind,args.description,args.author,args.based_on,args.store)
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
