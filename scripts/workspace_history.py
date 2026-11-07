"""Bounded, local file recovery shared by saves, native work, UI, and CLI."""
from pathlib import Path
from contextlib import contextmanager
import argparse
import hashlib
import json
import os
import stat
import tempfile
import threading
import time

from _common import workspace_root, workspace_scope,organization_transaction
from workspace_startup import state_dir

MAX_FILE=32*1024*1024
MAX_BYTES=256*1024*1024
MAX_VERSIONS=20
MAX_ENTRIES=500
MAX_OBSERVATIONS=4000
BATCH_BYTES=4*1024*1024
_lock=threading.RLock()
EXCLUDED={'credentials','secrets','node_modules','__pycache__','history','runtime','private','venv','dist','build'}
SENSITIVE={'.key','.pem','.pfx','.p12','.db','.sqlite','.sqlite3'}


def store(bid):
    if not isinstance(bid,str) or not bid or '/' in bid or '\\' in bid or bid in {'.','..'}:raise ValueError('Choose a business.')
    key=hashlib.sha256(os.path.normcase(str(workspace_root().resolve())).encode()).hexdigest()[:24]
    return state_dir()/'recovery'/key/bid


def managed(path,bid):
    root=workspace_root().resolve();path=Path(path).absolute()
    try:rel=path.relative_to(root)
    except ValueError:raise ValueError('File history is available for workspace-owned files.') from None
    if len(rel.parts)<3 or rel.parts[0] not in {'attachments','knowledge','instances'} or rel.parts[1]!=bid:
        raise ValueError('This file is outside the selected business.')
    if any(p.startswith('.') or p.lower() in EXCLUDED for p in rel.parts) or path.suffix.lower() in SENSITIVE or any(
            token in path.name.lower() for token in ('credential','secret','token','password','auth.json')):
        raise ValueError('Private or generated files are excluded from history.')
    for parent in [path,*path.parents]:
        if parent==root:break
        if parent.is_symlink() or (hasattr(parent,'is_junction') and parent.is_junction()):raise ValueError('Linked files are excluded from history.')
    if path.resolve()!=path:raise ValueError('Linked files are excluded from history.')
    return path,rel.as_posix()


@contextmanager
def locked(bid):
    # Same OS lock used by existing file saves; no daemon or stale lease.
    from workspace_sharing import destination_lock
    with _lock:
        base=store(bid);base.mkdir(parents=True,exist_ok=True)
        with destination_lock(base/'index.json'):yield base


def _read(base):
    try:return json.loads((base/'index.json').read_text(encoding='utf-8'))
    except FileNotFoundError:return []


def _write(path,data):
    # Deliberately independent of canonical writes: recovery never snapshots itself.
    fd,tmp=tempfile.mkstemp(prefix='.aura-history-',dir=path.parent)
    try:
        with os.fdopen(fd,'wb') as f:f.write(data);f.flush();os.fsync(f.fileno())
        os.replace(tmp,path)
    finally:Path(tmp).unlink(missing_ok=True)


def _prepare(path,bid,reason,content=None):
    path,relative=managed(path,bid)
    observed=None
    if content is None:
        before=path.stat()
        if before.st_size>MAX_FILE:return {'skipped':'File exceeds 32 MB'}
        with path.open('rb') as f:content=f.read(MAX_FILE+1)
        after=path.stat()
        if (before.st_mtime_ns,before.st_ctime_ns,before.st_size)!=(after.st_mtime_ns,after.st_ctime_ns,after.st_size):return {'skipped':'File is changing'}
        observed=after.st_mtime_ns
    if len(content)>MAX_FILE:return {'skipped':'File exceeds 32 MB'}
    digest=hashlib.sha256(content).hexdigest()
    row={'id':__import__('secrets').token_urlsafe(18),'path':relative,'hash':digest,'bytes':len(content),'at':time.time(),'reason':reason[:160]}
    if observed is not None:row['mtime_ns']=observed
    return row,content


def _commit(bid,prepared):
    """Publish a bounded batch with one index update and retention pass."""
    with locked(bid) as base:
        rows=_read(base);changed=False;results=[];contents={}
        latest={r['path']:r for r in rows}
        for row,content in prepared:
            previous=latest.get(row['path'])
            if previous and previous['hash']==row['hash'] and row['reason']!='Deleted':
                if 'mtime_ns' in row and previous.get('mtime_ns')!=row['mtime_ns']:
                    previous['mtime_ns']=row['mtime_ns'];changed=True
                results.append(previous);continue
            rows.append(row);latest[row['path']]=row;results.append(row);contents[row['hash']]=content;changed=True
        if not changed:return results
        kept=[];counts={};total=0;hashes=set()
        for item in reversed(rows):
            size=0 if item['hash'] in hashes else item['bytes']
            if counts.get(item['path'],0)>=MAX_VERSIONS or len(kept)>=MAX_ENTRIES or total+size>MAX_BYTES:continue
            kept.append(item);counts[item['path']]=counts.get(item['path'],0)+1;total+=size;hashes.add(item['hash'])
        for digest,content in contents.items():
            if digest in hashes and not (base/(digest+'.bin')).exists():_write(base/(digest+'.bin'),content)
        _write(base/'index.json',json.dumps(list(reversed(kept))).encode())
        for old in base.glob('*.bin'):
            if old.stem not in hashes:old.unlink(missing_ok=True)
        return results


def capture(path,bid,reason='Saved',content=None):
    prepared=_prepare(path,bid,reason,content)
    return prepared if isinstance(prepared,dict) else _commit(bid,[prepared])[0]


def capture_many(bid,snapshots,reason='Saved'):
    """Reuse one retention/index pass for a canonical transaction's prior bytes."""
    prepared=[_prepare(path,bid,reason,content) for path,content in snapshots.items()]
    return _commit(bid,[p for p in prepared if not isinstance(p,dict)]) if prepared else []


def inventory(bid,path=None):
    relative=managed(path,bid)[1] if path else None
    with locked(bid) as base:rows=_read(base)
    return {'items':[r for r in reversed(rows) if relative is None or r['path']==relative],
            'limits':{'versions_per_file':MAX_VERSIONS,'total_bytes':MAX_BYTES,'max_file_bytes':MAX_FILE}}


def version(bid,ident):
    from workspace_documents import revision
    row=next((r for r in inventory(bid)['items'] if r['id']==ident),None)
    if not row:raise ValueError('This version is no longer in local history.')
    path,_=managed(workspace_root()/row['path'],bid)
    content=(store(bid)/(row['hash']+'.bin')).read_bytes()
    if hashlib.sha256(content).hexdigest()!=row['hash']:raise ValueError('This saved version failed its integrity check.')
    preview=''
    if len(content)<=128*1024:
        try:preview=content.decode('utf-8-sig')
        except UnicodeError:pass
        if '\0' in preview:preview=''
    return {**row,'text':preview,'current_revision':revision(path) if path.is_file() else 'missing','exists':path.is_file()}


def observe(bid,reason='Observed native work'):
    """Bounded at work boundaries, never a background full-disk scan."""
    root=workspace_root().resolve();count=total=0;notes=[]
    with locked(bid) as base:
        try:observed=json.loads((base/'observed.json').read_text(encoding='utf-8'))
        except FileNotFoundError:observed={}
    updates={};batch=[];batch_bytes=0;batch_updates={};limited=False
    def flush():
        nonlocal batch,batch_bytes,batch_updates
        if batch:_commit(bid,batch)
        updates.update(batch_updates);batch=[];batch_bytes=0;batch_updates={}
    for namespace in ('instances','knowledge','attachments'):
        folder=root/namespace/bid
        for directory,dirs,names in os.walk(folder,followlinks=False):
            parent=Path(directory)
            dirs[:]=[d for d in dirs if not d.startswith('.') and d.lower() not in EXCLUDED and not (parent/d).is_symlink() and not (hasattr(parent/d,'is_junction') and (parent/d).is_junction())]
            for name in names:
                path=parent/name
                if count>=2000 or total>=64*1024*1024:limited=True;break
                try:
                    _,relative=managed(path,bid);info=path.stat();size=info.st_size
                except ValueError:continue
                except OSError as exc:notes.append(f'{name}: {exc.strerror or "Could not read history"}')
                else:
                    if size>MAX_FILE:continue
                    count+=1;stamp=[info.st_mtime_ns,info.st_ctime_ns,size]
                    previous=observed.get(relative)
                    if previous and previous['stamp']==stamp:continue
                    if total+size>64*1024*1024:limited=True;break
                    total+=size
                    try:prepared=_prepare(path,bid,reason)
                    except (OSError,ValueError) as exc:
                        notes.append(f'{name}: {exc}');continue
                    if isinstance(prepared,dict):
                        notes.append(f'{name}: {prepared["skipped"]}');continue
                    row,content=prepared
                    # A stable preparation must still match the metadata we observed.
                    if row.get('mtime_ns')!=stamp[0] or row['bytes']!=size:
                        notes.append(f'{name}: File is changing');continue
                    marker={'stamp':stamp,'hash':row['hash'],'at':time.time()}
                    if previous and previous.get('hash')==row['hash']:
                        updates[relative]=marker;continue
                    if batch and batch_bytes+len(content)>BATCH_BYTES:flush()
                    batch.append(prepared);batch_bytes+=len(content);batch_updates[relative]=marker
            if limited:break
        if limited:break
    flush()
    if updates:
        with locked(bid) as base:
            try:current=json.loads((base/'observed.json').read_text(encoding='utf-8'))
            except FileNotFoundError:current={}
            for path,value in updates.items():
                if value['at']>=current.get(path,{}).get('at',0):current[path]=value
            current=dict(sorted(current.items(),key=lambda item:item[1]['at'],reverse=True)[:MAX_OBSERVATIONS])
            _write(base/'observed.json',json.dumps(current).encode())
    if limited:notes.append('Observation limit reached; inline saves are still versioned.')
    return {'checked':count,'notes':notes[:8]}


@organization_transaction
def restore(bid,ident,expected):
    from workspace_documents import revision,Conflict
    from workspace_sharing import destination_lock
    rows=inventory(bid)['items'];row=next((r for r in rows if r['id']==ident),None)
    if not row:raise ValueError('This version is no longer in local history.')
    path,_=managed(workspace_root()/row['path'],bid)
    path.parent.mkdir(parents=True,exist_ok=True)
    with destination_lock(path):
        if not isinstance(expected,str) or not expected:raise ValueError('Review the current file before restoring.')
        if (revision(path) if path.is_file() else 'missing')!=expected:raise Conflict('This file changed. Reopen its history before restoring.')
        content=(store(bid)/(row['hash']+'.bin')).read_bytes()
        if hashlib.sha256(content).hexdigest()!=row['hash']:raise ValueError('This saved version failed its integrity check.')
        if row['path'].startswith('instances/'):
            from remember import remember,MECHANICAL_FIELDS
            saved=json.loads(content);current=json.loads(path.read_text(encoding='utf-8')) if path.is_file() else None
            if not current and saved.get('business_id')==bid:
                from _common import object_index
                from canonical_store import write_canonical
                from validate_business import validate_business
                if saved.get('object_type')=='Business' or saved.get('id') in object_index(bid):raise ValueError('This record already exists or cannot be restored here.')
                try:
                    write_canonical(saved,path)
                    errors,warnings,counts=validate_business(bid)
                    if errors:raise ValueError('This record cannot be restored until its references are available. Restore its related records first.')
                except Exception:
                    path.unlink(missing_ok=True)
                    raise
                return {'path':row['path'],'revision':revision(path),'restored':True,'validation':{'status':'clean','warnings':warnings[:5]}}
            if not current or saved.get('id')!=current.get('id') or saved.get('business_id')!=bid:
                raise ValueError('Restore this business record through its business editor so its references can be reviewed.')
            content_fields={k:v for k,v in saved.items() if k not in MECHANICAL_FIELDS}
            result=remember(bid,{'objects':[{'object_ref':saved['id'],'content':content_fields,
                **({'replace_extensions':True} if 'extensions' in content_fields else {}),
                'remove_fields':[k for k in current if k not in MECHANICAL_FIELDS and k not in saved]}]})
            return {'path':row['path'],'revision':revision(path),'restored':True,'validation':result['validation']}
        if path.is_file():
            retained=capture(path,bid,'Before restore')
            if retained.get('skipped'):raise Conflict('This file changed while preserving its current contents. Reopen its history before restoring.')
        mode=stat.S_IMODE(path.stat().st_mode) if path.exists() else 0o644
        if not mode & stat.S_IWUSR:raise ValueError('This file is read only. Restore it through its owning application.')
        fd,tmp=tempfile.mkstemp(prefix='.aura-restore-',dir=path.parent)
        try:
            with os.fdopen(fd,'wb') as f:f.write(content);f.flush();os.fsync(f.fileno())
            if (revision(path) if path.is_file() else 'missing')!=expected:raise Conflict('This file changed. Reopen its history before restoring.')
            os.chmod(tmp,mode);os.replace(tmp,path)
        finally:Path(tmp).unlink(missing_ok=True)
        warning=''
        try:
            retained=capture(path,bid,'Restored version')
            if retained.get('skipped'):warning='Restored successfully, but the file changed before its restored version could be added to local history.'
        except (OSError,ValueError):warning='Restored successfully, but the restored version could not be added to local history.'
        restored_revision=revision(path)
    return {'path':row['path'],'revision':restored_revision,'restored':True,**({'warning':warning} if warning else {})}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['list','observe','show','restore']);parser.add_argument('--workspace',type=Path,default=workspace_root())
    parser.add_argument('--business-id',required=True);parser.add_argument('--path');parser.add_argument('--id');parser.add_argument('--expected-revision');parser.add_argument('--json',action='store_true')
    args=parser.parse_args()
    with workspace_scope(args.workspace):
        result=inventory(args.business_id,workspace_root()/args.path if args.path else None) if args.action=='list' else observe(args.business_id) if args.action=='observe' else version(args.business_id,args.id) if args.action=='show' else restore(args.business_id,args.id,args.expected_revision)
    print(json.dumps(result,ensure_ascii=False))


if __name__=='__main__':main()
