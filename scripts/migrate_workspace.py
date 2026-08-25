#!/usr/bin/env python3
"""Copy and verify organization-owned AURA/BusinessOS state into another workspace.

Migration is intentionally non-destructive: source state is never deleted. Conflicting
non-identical target files abort before copying. The active workspace pointer is changed
only after every migrated file verifies by SHA-256.
"""
from _common import *
from configure_workspace import configure, _profile_id
import argparse, hashlib, json, os, shutil, tempfile

NAMESPACES=('instances','runtime','knowledge','attachments')


def _sha256(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):
            h.update(chunk)
    return h.hexdigest()


def _source_files(source):
    source=Path(source).resolve(); rows=[]
    for ns in NAMESPACES:
        base=source/ns
        if not base.exists(): continue
        if base.is_symlink(): raise ValueError(f'Refusing workspace migration through symlinked namespace: {base}')
        for root,dirs,files in os.walk(base,followlinks=False):
            rootp=Path(root)
            bad_dirs=[d for d in dirs if (rootp/d).is_symlink()]
            if bad_dirs: raise ValueError(f'Refusing workspace migration with symlinked directory: {rootp/bad_dirs[0]}')
            for name in files:
                p=rootp/name
                if p.is_symlink(): raise ValueError(f'Refusing workspace migration with symlinked file: {p}')
                rel=p.relative_to(source)
                if len(rel.parts)>=2 and rel.parts[0]=='instances' and rel.parts[1]=='_template':
                    continue
                rows.append((rel,p,_sha256(p),p.stat().st_size))
    return sorted(rows,key=lambda x:x[0].as_posix())


def _preflight(source,target,rows):
    conflicts=[]; identical=[]; pending=[]
    for rel,src,digest,size in rows:
        dst=target/rel
        if dst.exists():
            if not dst.is_file(): conflicts.append(f'{rel}: target exists and is not a regular file');continue
            if _sha256(dst)!=digest: conflicts.append(f'{rel}: target contains different content');continue
            identical.append(rel.as_posix())
        else:
            pending.append((rel,src,digest,size))
    if conflicts:
        raise ValueError('Workspace migration conflict(s); no files were copied:\n- '+'\n- '.join(conflicts))
    return identical,pending


def _copy_verified(target,pending):
    copied=[]
    for rel,src,digest,size in pending:
        dst=target/rel;dst.parent.mkdir(parents=True,exist_ok=True)
        fd,tmpname=tempfile.mkstemp(prefix=dst.name+'.migrating-',dir=str(dst.parent));os.close(fd)
        tmp=Path(tmpname)
        try:
            shutil.copy2(src,tmp)
            if _sha256(tmp)!=digest: raise ValueError(f'Hash mismatch while staging {rel}')
            os.replace(tmp,dst)
        finally:
            if tmp.exists(): tmp.unlink()
        copied.append(rel.as_posix())
    return copied


def migrate(target_value,profile_value=None,knowledge_enabled=None,activate=True,write_link=True):
    source=workspace_root().resolve()
    target=Path(os.path.expanduser(os.path.expandvars(str(target_value))))
    target=target.resolve() if target.is_absolute() else (Path.cwd()/target).resolve()
    if source==target: raise ValueError('Source and target workspace are the same')

    current_profile=workspace_profile()
    profile=_profile_id(profile_value or current_profile.get('profile','simple'))
    if knowledge_enabled is None: knowledge_enabled=bool(current_profile.get('knowledge_enabled',True))

    rows=_source_files(source)
    target.mkdir(parents=True,exist_ok=True)
    # Create the target workspace shell/profile without changing the active pointer yet.
    configure(target,profile,knowledge_enabled,write_link=False,force=False,allow_state_switch=True)
    identical,pending=_preflight(source,target,rows)
    copied=_copy_verified(target,pending)

    failures=[]
    for rel,src,digest,_ in rows:
        dst=target/rel
        if not dst.exists() or not dst.is_file() or _sha256(dst)!=digest:
            failures.append(rel.as_posix())
    if failures: raise ValueError('Workspace verification failed; source remains unchanged. Failed: '+', '.join(failures))

    activated=False; activation_instruction=None
    if activate:
        env_root=os.environ.get('BUSINESSOS_WORKSPACE')
        if env_root:
            env_path=Path(os.path.expanduser(os.path.expandvars(env_root)))
            env_path=env_path.resolve() if env_path.is_absolute() else (PRODUCT_ROOT/env_path).resolve()
            if env_path!=target:
                activation_instruction=f'BUSINESSOS_WORKSPACE is set and overrides local pointers. Set BUSINESSOS_WORKSPACE={target} (or unset it) to activate the migrated workspace.'
            else:
                activated=True
        if not env_root or activated:
            configure(target,profile,knowledge_enabled,write_link=write_link,force=True,allow_state_switch=True)
            if not env_root:
                activated=workspace_root().resolve()==target
        if not activated and activation_instruction is None:
            activation_instruction=f'Set BUSINESSOS_WORKSPACE={target} or configure the local workspace pointer to activate this verified workspace.'

    return {
        'source_workspace':str(source),'target_workspace':str(target),'profile':profile,
        'knowledge_enabled':bool(knowledge_enabled),'file_count':len(rows),
        'copied_file_count':len(copied),'identical_existing_file_count':len(identical),
        'bytes_verified':sum(x[3] for x in rows),'verified':True,'source_retained':True,
        'activated':activated,'activation_instruction':activation_instruction,
        'copied_files':copied,'identical_existing_files':identical
    }


def main():
    p=argparse.ArgumentParser(description='Non-destructively copy, hash-verify, and optionally activate a new ViralTrac AURA workspace.')
    p.add_argument('target_workspace')
    p.add_argument('--profile',help='simple | power_user | organization; defaults to the current workspace profile')
    kg=p.add_mutually_exclusive_group();kg.add_argument('--knowledge',dest='knowledge',action='store_true');kg.add_argument('--no-knowledge',dest='knowledge',action='store_false');p.set_defaults(knowledge=None)
    p.add_argument('--no-activate',action='store_true',help='Copy and verify only; leave active workspace selection unchanged.')
    p.add_argument('--no-link',action='store_true',help='Do not write a local product workspace pointer during activation; useful when the host selects BUSINESSOS_WORKSPACE.')
    p.add_argument('--json',action='store_true')
    a=p.parse_args()
    try:r=migrate(a.target_workspace,a.profile,a.knowledge,not a.no_activate,not a.no_link)
    except ValueError as e: raise SystemExit(str(e))
    if a.json: print(json.dumps(r,indent=2));return
    print(f"source={r['source_workspace']}")
    print(f"target={r['target_workspace']}")
    print(f"verified=true files={r['file_count']} copied={r['copied_file_count']} identical={r['identical_existing_file_count']} bytes={r['bytes_verified']}")
    print('source_retained=true')
    print(f"activated={str(r['activated']).lower()}")
    if r.get('activation_instruction'): print('NEXT: '+r['activation_instruction'])
    else: print('NEXT: run `python3 scripts/workspace_status.py` and validate the migrated business state before retiring any old local copy.')

if __name__=='__main__': main()
