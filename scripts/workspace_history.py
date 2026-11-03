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

from _common import workspace_root, workspace_scope
from workspace_startup import state_dir

MAX_FILE=32*1024*1024
MAX_BYTES=256*1024*1024
MAX_VERSIONS=20
MAX_ENTRIES=500
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


def capture(path,bid,reason='Saved',content=None):
    path,relative=managed(path,bid)
    observed=None
    if content is None:
        before=path.stat()
        if before.st_size>MAX_FILE:return {'skipped':'File exceeds 32 MB'}
        with path.open('rb') as f:content=f.read(MAX_FILE+1)
        after=path.stat()
        if (before.st_mtime_ns,before.st_size)!=(after.st_mtime_ns,after.st_size):return {'skipped':'File is changing'}
        observed=after.st_mtime_ns
    if len(content)>MAX_FILE:return {'skipped':'File exceeds 32 MB'}
    digest=hashlib.sha256(content).hexdigest()
    with locked(bid) as base:
        rows=_read(base)
        previous=next((r for r in reversed(rows) if r['path']==relative),None)
        if previous and previous['hash']==digest:
            if observed is not None and previous.get('mtime_ns')!=observed:
                previous['mtime_ns']=observed;_write(base/'index.json',json.dumps(rows).encode())
            return previous
        row={'id':__import__('secrets').token_urlsafe(18),'path':relative,'hash':digest,'bytes':len(content),'at':time.time(),'reason':reason[:160]}
        if observed is not None:row['mtime_ns']=observed
        blob=base/(digest+'.bin')
        if not blob.exists():_write(blob,content)
        rows.append(row);kept=[];counts={};total=0;hashes=set()
        for item in reversed(rows):
            size=0 if item['hash'] in hashes else item['bytes']
            if counts.get(item['path'],0)>=MAX_VERSIONS or len(kept)>=MAX_ENTRIES or total+size>MAX_BYTES:continue
            kept.append(item);counts[item['path']]=counts.get(item['path'],0)+1;total+=size;hashes.add(item['hash'])
        _write(base/'index.json',json.dumps(list(reversed(kept))).encode())
        for old in base.glob('*.bin'):
            if old.stem not in hashes:old.unlink(missing_ok=True)
        return row


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
    latest={}
    for row in inventory(bid)['items']:latest.setdefault(row['path'],row)
    for namespace in ('instances','knowledge','attachments'):
        folder=root/namespace/bid
        for directory,dirs,names in os.walk(folder,followlinks=False):
            parent=Path(directory)
            dirs[:]=[d for d in dirs if not d.startswith('.') and d.lower() not in EXCLUDED and not (parent/d).is_symlink() and not (hasattr(parent/d,'is_junction') and (parent/d).is_junction())]
            for name in names:
                path=parent/name
                if count>=2000 or total>=64*1024*1024:return {'checked':count,'notes':notes+['Observation limit reached; inline saves are still versioned.']}
                try:
                    _,relative=managed(path,bid);info=path.stat();size=info.st_size
                    if size>MAX_FILE:continue
                    count+=1
                    previous=latest.get(relative)
                    if previous and previous.get('mtime_ns')==info.st_mtime_ns and previous['bytes']==size:continue
                    total+=size;capture(path,bid,reason)
                except ValueError:continue
                except OSError as exc:notes.append(f'{name}: {exc.strerror or "Could not read history"}')
    return {'checked':count,'notes':notes[:8]}


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
            if not current or saved.get('id')!=current.get('id') or saved.get('business_id')!=bid:
                raise ValueError('Restore this business record through its business editor so its references can be reviewed.')
            content_fields={k:v for k,v in saved.items() if k not in MECHANICAL_FIELDS}
            result=remember(bid,{'objects':[{'object_ref':saved['id'],'content':content_fields,
                'remove_fields':[k for k in current if k not in MECHANICAL_FIELDS and k not in saved]}]})
            return {'path':row['path'],'revision':revision(path),'restored':True,'validation':result['validation']}
        if path.is_file():capture(path,bid,'Before restore')
        mode=stat.S_IMODE(path.stat().st_mode) if path.exists() else 0o644
        if not mode & stat.S_IWUSR:raise ValueError('This file is read only. Restore it through its owning application.')
        fd,tmp=tempfile.mkstemp(prefix='.aura-restore-',dir=path.parent)
        try:
            with os.fdopen(fd,'wb') as f:f.write(content);f.flush();os.fsync(f.fileno())
            os.chmod(tmp,mode);os.replace(tmp,path)
        finally:Path(tmp).unlink(missing_ok=True)
        capture(path,bid,'Restored version')
    return {'path':row['path'],'revision':revision(path),'restored':True}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['list','observe','show','restore']);parser.add_argument('--workspace',type=Path,default=workspace_root())
    parser.add_argument('--business-id',required=True);parser.add_argument('--path');parser.add_argument('--id');parser.add_argument('--expected-revision');parser.add_argument('--json',action='store_true')
    args=parser.parse_args()
    with workspace_scope(args.workspace):
        result=inventory(args.business_id,workspace_root()/args.path if args.path else None) if args.action=='list' else observe(args.business_id) if args.action=='observe' else version(args.business_id,args.id) if args.action=='show' else restore(args.business_id,args.id,args.expected_revision)
    print(json.dumps(result,ensure_ascii=False))


if __name__=='__main__':main()
