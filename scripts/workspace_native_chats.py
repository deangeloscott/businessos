"""Read-only native session discovery and cheap local freshness markers."""
import json
import os
import re
import subprocess
from pathlib import Path
import workspace_chats
import workspace_agents
import workspace_codex

KINDS={'pi','omp','codex','claude','hermes'}

def storage(kind,env):
    home=Path.home()
    if kind=='codex':return Path(env.get('CODEX_HOME') or home/'.codex')/'sessions'
    if kind=='claude':return Path(env.get('CLAUDE_CONFIG_DIR') or home/'.claude')/'projects'
    if kind=='hermes':return Path(env.get('HERMES_HOME') or home/'.hermes')/'state.db'
    return Path(env.get('PI_CODING_AGENT_DIR') or home/('.pi' if kind=='pi' else '.omp')/'agent')/'sessions'

def marker(path):
    if not path:return None
    value=[]
    for item in (Path(path),Path(str(path)+'-wal')) if str(path).endswith('.db') else (Path(path),):
        try:
            stat=item.stat();value.append([str(item),stat.st_mtime_ns,stat.st_size])
        except OSError:value.append([str(item),None,None])
    return value if value[0][1] is not None else None

def files(kind,env):
    root=storage(kind,env)
    if kind=='hermes':return []
    return sorted((p for p in root.glob('**/*.jsonl') if p.is_file() and not p.is_symlink()),key=lambda p:p.stat().st_mtime,reverse=True) if root.is_dir() else []

def source_hint(kind,env,ident):
    root=storage(kind,env)
    if kind=='hermes':return str(root) if root.is_file() else ''
    if not root.is_dir() or not re.fullmatch(r'[A-Za-z0-9_-]{1,160}',str(ident)):return ''
    found=list(root.glob('**/*'+ident+'*.jsonl'))
    return str(found[0]) if len(found)==1 and not found[0].is_symlink() else ''

def inspect_file(path,kind):
    # Prefix/tail only for discovery; the owning adapter reads full active history on import.
    with path.open('rb') as f:
        prefix=f.read(16384);f.seek(max(0,path.stat().st_size-32768));tail=f.read()
    rows=[]
    for line in (prefix+b'\n'+tail).decode('utf-8',errors='replace').splitlines():
        try:rows.append(json.loads(line))
        except ValueError:pass
    head=next((r.get('payload',{}) if r.get('type')=='session_meta' else r for r in rows if r.get('type') in {'session','session_meta'}),{})
    ident=head.get('id') or head.get('sessionId') or (path.stem if kind=='claude' else '')
    if not ident:return None
    title=next((r.get('name') or r.get('title') for r in reversed(rows) if r.get('type') in {'session_info','sessionInfo','custom-title'}),'')
    title=title or next((r.get('customTitle') for r in reversed(rows) if r.get('type')=='custom-title'),'')
    preview=''
    for r in rows:
        m=r.get('message') or r.get('payload') or {}
        if m.get('role')=='user':
            preview=workspace_agents.display_text(workspace_agents.message_text(m.get('content','')))
            if preview:break
    cwd=head.get('cwd') or head.get('workingDirectory') or ''
    return {'native_id':str(ident),'title':workspace_chats.short(title or preview or 'Native conversation',80),'description':workspace_chats.short(preview,240),'native_workspace':cwd,'updated':path.stat().st_mtime,'source_file':str(path)}

def recent(command,kind,cwd,env,excluded):
    if kind not in KINDS:return {'items':[],'note':'This app does not expose native chat discovery. Use its own conversation list.'}
    items=[]
    if kind=='codex':
        def read(call):
            found=[];cursor=None
            for _ in range(3):
                page=call('thread/list',{'limit':30,'sortKey':'updated_at',**({'cursor':cursor} if cursor else {})})
                found.extend(page.get('data',[]));cursor=page.get('nextCursor')
                if len([r for r in found if r.get('id') not in excluded])>=5 or not cursor:break
            return found
        for r in workspace_codex.rpc(command,read,cwd,env):
            if r.get('id') in excluded:continue
            items.append({'native_id':r['id'],'title':workspace_chats.short(r.get('name') or r.get('preview') or 'Codex conversation',80),'description':workspace_chats.short(r.get('preview'),240),'native_workspace':r.get('cwd',''),'updated':r.get('updatedAt',0),'source_file':r.get('path','')})
    elif kind=='hermes':
        # Listing is metadata only, including for a launcher into another environment.
        result=subprocess.run([*workspace_agents.base_command(command),'sessions','list','--limit','30'],cwd=cwd,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=12,creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
        if result.returncode:raise ValueError('Open Hermes to check its saved sessions, or enter a session ID.')
        clean=re.sub(r'\x1b\[[0-9;]*m','',result.stdout)
        for line in clean.splitlines():
            match=re.search(r'(?<![\w-])(?:[0-9]{8}_[0-9]{6}_[a-fA-F0-9]+|[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12})(?![\w-])',line)
            if match and match.group() not in excluded:
                items.append({'native_id':match.group(),'title':workspace_chats.short(line[match.end():].strip(' |│'),80) or 'Hermes conversation','description':'Open this native session to review its messages.','native_workspace':'','updated':0,'source_file':str(storage(kind,env)) if storage(kind,env).is_file() else ''})
    else:
        for path in files(kind,env):
            try:r=inspect_file(path,kind)
            except (OSError,ValueError):continue
            if r and r['native_id'] not in excluded:items.append(r)
            if len(items)>=5:break
    return {'items':items[:5],'note':'' if items else 'No additional sessions were found here. You can look up an exact session ID, including sessions kept by a remote launcher.'}

def lookup(command,kind,cwd,env,ident):
    if kind not in KINDS or not isinstance(ident,str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,160}',ident):raise ValueError('Choose an AI app and enter its exact session ID.')
    source=None
    if kind in {'pi','omp','claude','codex'}:
        for path in files(kind,env):
            if ident in path.stem:
                try:r=inspect_file(path,kind)
                except (OSError,ValueError):continue
                if r and r['native_id']==ident:source=r;break
    native_cwd=(source or {}).get('native_workspace') or str(cwd)
    if not Path(native_cwd).is_dir():native_cwd=str(cwd)
    result=workspace_codex.history(command,Path(native_cwd),ident,env) if kind=='codex' else workspace_agents.history(command,kind,Path(native_cwd),env,ident)
    if result.get('native_id',ident)!=ident:raise ValueError('The app returned a different session. Nothing was added.')
    messages=result.get('messages',[])
    result.update(native_workspace=(source or {}).get('native_workspace') or result.get('native_workspace') or str(cwd),source_file=(source or {}).get('source_file') or result.get('source_file') or (str(storage(kind,env)) if kind=='hermes' and storage(kind,env).is_file() else ''))
    result['title']=result.get('title') or (source or {}).get('title') or next((workspace_chats.short(m.get('text',''),80) for m in messages if m.get('role')=='user'),'Native conversation')
    result['description']=result.get('summary') or next((workspace_chats.short(m.get('text',''),240) for m in reversed(messages) if m.get('role')=='assistant'),'')
    return result


if __name__=='__main__':
    import argparse
    from _common import workspace_scope,workspace_root
    from workspace_ui import installed_agents
    parser=argparse.ArgumentParser(description='Discover or inspect native conversations without sending AI work.')
    parser.add_argument('action',choices=['list','show']);parser.add_argument('--kind',required=True,choices=sorted(KINDS));parser.add_argument('--id');parser.add_argument('--workspace',type=Path,default=workspace_root())
    args=parser.parse_args()
    with workspace_scope(args.workspace):
        app=next((a for a in installed_agents() if a['id']==args.kind and a['argv']),None)
        if not app:parser.error('This AI app is not installed.')
        if args.action=='show' and not args.id:parser.error('Show requires --id.')
        result=lookup(app['argv'],args.kind,args.workspace,dict(os.environ),args.id) if args.action=='show' else recent(app['argv'],args.kind,args.workspace,dict(os.environ),set())
        print(json.dumps(result,ensure_ascii=False))
