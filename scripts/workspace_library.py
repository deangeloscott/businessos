"""Read-only local skills/tools inventory. Native apps retain execution authority."""
from pathlib import Path
import hashlib
import json
import os
import re
import shutil
import subprocess
import copy
import yaml

APPS={'codex':'Codex','claude':'Claude Code','pi':'Pi','omp':'OMP','hermes':'Hermes','antigravity':'Google Antigravity'}
SKIP={'.git','node_modules','__pycache__','.venv','venv','credentials','secrets'}


def short(value, limit=240):
    if not isinstance(value,str):return ''
    value=re.sub(r'\x1b\[[0-9;]*m','',value)
    value=' '.join(value.split())
    if len(value)<=limit:return value
    cut=value[:limit-1]
    return (cut.rsplit(' ',1)[0] if ' ' in cut else cut)+'…'


def category(name, description):
    text=(name+' '+description).lower()
    for title, words in [('Content creation',('image','video','audio','design','writing','content','presentation')),
                         ('Research',('search','research','browse','competitor')),
                         ('Files & documents',('file','pdf','document','spreadsheet')),
                         ('Development',('code','terminal','shell','git','python','debug')),
                         ('Automation',('schedule','cron','automation'))]:
        if any(word in text for word in words):return title
    return 'Apps & capabilities'


def entry(kind, title, description, app, identity, status='Found locally', **extra):
    return dict(key=kind.lower()+':'+hashlib.sha256(identity.encode()).hexdigest()[:24],kind=kind,
                title=short(title,160),description=short(description),category=category(title,description),
                group=APPS.get(app,app) or 'This computer',area=kind.lower(),
                apps=[app] if app else [],sources=[dict(app=app,status=status,**extra)])


def skill(path, app, identity, status='Found locally'):
    path=Path(path).expanduser()
    if path.is_dir():path=path/'SKILL.md'
    if path.name!='SKILL.md' or not path.is_file() or path.is_symlink() or path.stat().st_size>128*1024:return None
    text=path.read_text(encoding='utf-8-sig',errors='replace')
    header=re.match(r'^---\s*\n(.*?)\n---(?:\s*\n|$)',text,re.S)
    try:meta=yaml.safe_load(header[1]) if header else {}
    except yaml.YAMLError:meta={}
    if not isinstance(meta,dict):meta={}
    title=meta.get('name') if isinstance(meta.get('name'),str) else path.parent.name
    description=meta.get('description') if isinstance(meta.get('description'),str) else ''
    result=entry('Skill',title,description,app,identity,status,path=str(path.resolve()),scope='Workspace' if identity.startswith('workspace:') else 'App')
    result['requirements']=short(meta.get('compatibility',''),500)
    result['_path']=path.resolve()
    result['_text_hash']=hashlib.sha256(text.encode()).hexdigest()
    return result


def pack_hash(folder):
    """Deduplicate copies only when the complete small package can be compared."""
    digest=hashlib.sha256();total=0;count=0
    def unreadable(error):raise error
    for directory, dirs, files in os.walk(folder,followlinks=False,onerror=unreadable):
        dirs.sort();files.sort()
        if any(d in SKIP for d in dirs):return None
        for name in [*dirs,*files]:
            if (Path(directory)/name).is_symlink():return None
        for name in files:
            path=Path(directory)/name;count+=1;total+=path.stat().st_size
            if count>128 or total>4*1024*1024:return None
            if name.lower().startswith('.env') or name.lower() in {'auth.json','credentials.json','secrets.json','api_keys.json'} or path.suffix.lower() in {'.key','.pem','.pfx'}:return None
            digest.update(path.relative_to(folder).as_posix().encode());digest.update(b'\0');digest.update(path.read_bytes())
    return digest.hexdigest()


def merge(rows):
    rows=copy.deepcopy(rows)
    # Shared paths are one skill. Same-named but different packages stay separate.
    by_path={};others=[]
    for row in rows:
        if row.get('_path'):
            ident=os.path.normcase(str(row['_path']))
            if ident in by_path:
                original=by_path[ident];original['sources']+=row['sources'];original.setdefault('aliases',[]).append(row['key'])
            else:by_path[ident]=row
        else:others.append(row)
    clusters={}
    for row in by_path.values():clusters.setdefault((row['title'],row['_text_hash']),[]).append(row)
    for candidates in clusters.values():
        exact={}
        for row in candidates:
            try:fingerprint=pack_hash(row['_path'].parent) if len(candidates)>1 else None
            except OSError:fingerprint=None
            if fingerprint and fingerprint in exact:
                original=exact[fingerprint];original['sources']+=row['sources'];original.setdefault('aliases',[]).extend([row['key'],*row.get('aliases',[])])
            else:
                if fingerprint:exact[fingerprint]=row
                others.append(row)
    seen={}
    for row in others:
        row['apps']=sorted({s['app'] for s in row['sources'] if s.get('app')})
        row['sources']=[dict(t) for t in {json.dumps(t,sort_keys=True):t for t in row['sources']}.values()]
        row['aliases']=sorted(set(row.get('aliases',[])))
        row.pop('_path',None);row.pop('_text_hash',None)
        seen.setdefault(row['key'],row)
    return list(seen.values())


def normalized(value):
    return ''.join(c for c in value.casefold() if c.isalnum()) or hashlib.sha256(value.encode()).hexdigest()


def retain_catalog(previous, current, incomplete):
    """An incomplete refresh must not turn previously reported items into absence."""
    if not incomplete:return current
    keys={row['key'] for row in current}
    retained=copy.deepcopy([row for row in previous if row['key'] not in keys])
    for row in retained:
        for source in row.get('sources',[]):source['stale']=True
    return [*current,*retained]


def organize(rows, group_services=True, scope=''):
    """One display entry; retain native identities, variants and callable actions."""
    rows=copy.deepcopy(rows);families={};services={}
    for row in rows:
        service=next((s.get('service') or s.get('connection') for s in row.get('sources',[]) if s.get('service') or s.get('connection')),'')
        if row['kind']=='Tool' and not service and any(s.get('type')=='Connection' for s in row.get('sources',[])):
            service=row['title']
            for source in row['sources']:source['service']=service
        if group_services and row['kind']=='Tool' and service:
            key='service:'+normalized(service)
            services.setdefault(key,[]).append(row)
        else:
            identity=row['key'] if row['kind'] in {'Workflow','Recipe'} else scope+row['kind']+':'+(normalized(row.get('package_name',row['title'])) if row['kind']=='Plugin' else row['title'].casefold())
            families.setdefault(identity,[]).append(row)
    def combined(candidates,identity,title=None):
        first=copy.deepcopy(candidates[0]);old_keys=[r['key'] for r in candidates]
        if first['kind'] not in {'Workflow','Recipe'}:
            first['key']=first['kind'].lower()+':'+hashlib.sha256(identity.encode()).hexdigest()[:24]
        first['title']=title or first['title']
        first['sources']=list({json.dumps(s,sort_keys=True):s for r in candidates for s in r.get('sources',[])}.values())
        first['apps']=sorted({s['app'] for s in first['sources'] if s.get('app')})
        first['aliases']=sorted(set(old_keys+[a for r in candidates for a in r.get('aliases',[])]))
        if len(candidates)>1:first['variants']=candidates
        if first['kind']=='Plugin':first['app_ids']=sorted({ident for r in candidates for ident in r.get('app_ids',[])})
        if first['kind']=='Plugin':first['tool_keys']=sorted({ident for r in candidates for ident in r.get('tool_keys',[])})
        return first
    result=[combined(candidates,key) for key,candidates in families.items()]
    for key,candidates in services.items():
        name=next((s.get('service') or s.get('connection') for r in candidates for s in r.get('sources',[]) if s.get('service') or s.get('connection')))
        title=re.sub(r'[_-]+',' ',name).strip()
        title={'github':'GitHub','openai':'OpenAI','google drive':'Google Drive','gmail':'Gmail','cua repl':'Browser & computer','node repl':'JavaScript'}.get(title.casefold(),title.title())
        item=combined(candidates,key,title)
        actions=[r for r in candidates if any(s.get('type')=='Tool' for s in r.get('sources',[]))]
        connections=[r for r in candidates if r not in actions]
        display=next((r['title'] for r in connections if any(s.get('type')=='App' for s in r['sources'])),None)
        if display:item['title']=display
        item.pop('variants',None)
        item['members']=organize(actions,False,key) if actions else []
        # Action rows retain their original server but must not regroup forever.
        item['description']=next((r.get('description','') for r in connections if r.get('description')),'Tools reported by your AI apps.')
        if connections:item['variants']=connections
        item['category']=category(title,item['description'])
        if item['category']=='Apps & capabilities' and item['members']:
            topics=[m['category'] for m in item['members'] if m['category']!='Apps & capabilities']
            if topics:item['category']=max(dict.fromkeys(topics),key=topics.count)
        item['group']='Connected services'
        result.append(item)
    for item in result:
        if item['kind'] in {'Skill','Plugin'}:item['group']='Shared' if len(item.get('apps',[]))>1 else 'Your '+item['kind'].lower()+'s'
    skill_rows=[r for r in rows if r['kind']=='Skill' and any(s.get('plugin') for s in r.get('sources',[]))]
    for item in result:
        if item['kind']=='Plugin':
            linked={r['key'] for r in skill_rows if any(s.get('plugin') in [item['key'],*item.get('aliases',[])] for s in r['sources'])}
            item['related']=[s['key'] for s in result if s['kind']=='Skill' and linked.intersection([s['key'],*s.get('aliases',[])])]
            item['related'] += [t['key'] for t in result if t['kind']=='Tool' and any(s.get('app_id') in item.get('app_ids',[]) for s in t.get('sources',[]))]
            item['related'] += [t['key'] for t in result if t['kind']=='Tool' and set(item.get('tool_keys',[])).intersection([t['key'],*t.get('aliases',[])])]
            item['related']=list(dict.fromkeys(item['related']))
    return result


def find(items, key):
    for item in items:
        if key==item['key'] or key in item.get('aliases',[]):return item
        nested=find(item.get('members',[]),key)
        if nested:return nested
    return None


def metadata(path):
    path=Path(path)
    if not path.is_file() or path.is_symlink() or path.stat().st_size>2*1024*1024:return {}
    text=path.read_text(encoding='utf-8-sig')
    if path.suffix=='.toml':
        import tomllib
        data=tomllib.loads(text)
    else:data=yaml.safe_load(text) if path.suffix in {'.yml','.yaml'} else json.loads(text)
    return data if isinstance(data,dict) else {}


def plugins(workspace, home, bases, apps):
    rows=[];notes=[]
    # Cache presence is file discovery, never evidence of installation or auth.
    for app,base,marker in [('codex',bases['codex']/ 'plugins/cache','.codex-plugin'),('claude',bases['claude']/ 'plugins/cache','.claude-plugin')]:
        if app not in apps:continue
        try:
            configured=metadata(bases[app]/('config.toml' if app=='codex' else 'settings.json')).get('plugins' if app=='codex' else 'enabledPlugins',{})
            installed=metadata(bases[app]/'plugins/installed_plugins.json').get('plugins',{}) if app=='claude' else {}
            installed_paths={str(Path(r['installPath']).resolve()) for values in installed.values() if isinstance(values,list) for r in values if isinstance(r,dict) and isinstance(r.get('installPath'),str)} if isinstance(installed,dict) else set()
        except (OSError,ValueError,TypeError,yaml.YAMLError):configured={};installed_paths=set();notes.append(APPS[app]+': plugin status could not be checked.')
        for manifest in sorted(base.glob('*/*/*/'+marker+'/plugin.json'))[:500]:
            try:
                data=metadata(manifest);folder=manifest.parent.parent
                if not isinstance(data.get('name'),str) or not data['name']:continue
                interface=data.get('interface') if isinstance(data.get('interface'),dict) else {}
                reference=str(data['name'])+'@'+manifest.relative_to(base).parts[0]
                setting=configured.get(reference) if isinstance(configured,dict) else None
                enabled=setting.get('enabled') if isinstance(setting,dict) else setting
                status='Disabled' if enabled is False else 'Configured' if enabled is True else 'Installed' if str(folder.resolve()) in installed_paths else 'Found locally'
                row=entry('Plugin',short(interface.get('displayName') or data['name']),short(data.get('description','')),app,
                          app+':plugin:'+str(manifest),status,path=str(manifest),version=short(data.get('version','')),type='Plugin')
                row['package_name']=short(data['name'])
                reference=data.get('apps')
                if isinstance(reference,str):
                    app_file=(folder/reference).resolve()
                    if app_file.is_relative_to(folder.resolve()):
                        declared=metadata(app_file).get('apps',{})
                        if isinstance(declared,dict):row['app_ids']=[a['id'] for a in declared.values() if isinstance(a,dict) and isinstance(a.get('id'),str)]
                rows.append(row)
                skill_root=data.get('skills','./skills')
                if isinstance(skill_root,str):
                    target=(folder/skill_root).resolve()
                    if target.is_relative_to(folder.resolve()) and target.is_dir():
                        for path in sorted(target.glob('*/SKILL.md'))[:200]:
                            found=skill(path,app,app+':plugin-skill:'+str(path))
                            if found:
                                found['sources'][0].update(plugin=row['key'],version=short(data.get('version','')))
                                rows.append(found)
            except (OSError,ValueError,TypeError,yaml.YAMLError):notes.append(APPS[app]+': some plugin files could not be read.')
    for app in ('pi','omp'):
        if app not in apps:continue
        paths=[bases[app]/'settings.json',Path(workspace)/('.'+app)/'settings.json']
        if app=='omp':paths+=[bases[app]/'config.yml',Path(workspace)/'.omp/config.yml']
        for path in paths:
            try:
                data=metadata(path)
                for field in ('extensions','packages'):
                    values=data.get(field,[])
                    if isinstance(values,dict):values=values.get('paths',[])
                    if not isinstance(values,list):continue
                    for value in values[:200]:
                        source=value.get('source','') if isinstance(value,dict) else value
                        if not isinstance(source,str) or source.startswith(('\\\\','//','https://','http://')):continue
                        status='Configured';description='An extension or package configured in '+APPS[app]+'.';package_data={};package_root=None
                        if source.startswith('npm:'):
                            package=source[4:];match=re.fullmatch(r'(@[\w.-]+/[\w.-]+|[\w.-]+)(?:@([\w.^~+-]+))?',package)
                            if not match:continue
                            name,version=match.groups();location=''
                            for folder in (bases[app]/'npm/node_modules'/name,bases[app]/'node_modules'/name,Path(workspace)/'node_modules'/name):
                                if (folder/'package.json').is_file():
                                    package_data=metadata(folder/'package.json');package_root=folder
                                    version=short(package_data.get('version','')) or version
                                    description=short(package_data.get('description','')) or description
                                    location=str(folder/'package.json');status='Installed';break
                        else:
                            target=Path(source).expanduser()
                            if not target.is_absolute():target=path.parent/target
                            if not target.exists():notes.append(APPS[app]+': a configured extension file is unavailable.');continue
                            name=target.stem;version='';location=str(target.resolve())
                            if name=='index':name=target.parent.name
                        row=entry('Plugin',name,description,app,app+':'+field+':'+source,status,path=location,version=version or '',type='Extension' if field=='extensions' else 'Package')
                        rows.append(row)
                        resources=package_data.get('pi',{})
                        declared=resources.get('skills',[]) if isinstance(resources,dict) else []
                        if isinstance(declared,str):declared=[declared]
                        if package_root and isinstance(declared,list):
                            for relative in declared[:50]:
                                if not isinstance(relative,str):continue
                                target=(package_root/relative).resolve()
                                if not target.is_relative_to(package_root.resolve()):continue
                                paths=list(target.glob('*/SKILL.md'))[:200] if target.is_dir() else [target]
                                for path in paths:
                                    found=skill(path,app,app+':package-skill:'+str(path))
                                    if found:found['sources'][0]['plugin']=row['key'];rows.append(found)
            except (OSError,ValueError,TypeError,yaml.YAMLError):notes.append(APPS[app]+': extension settings could not be read.')
    return rows,notes


def local(workspace, apps, home=None):
    home=Path(home or Path.home());workspace=Path(workspace)
    bases={'codex':Path(os.environ.get('CODEX_HOME',home/'.codex')),
           'claude':Path(os.environ.get('CLAUDE_CONFIG_DIR',home/'.claude')),
           'pi':Path(os.environ.get('PI_CODING_AGENT_DIR',home/'.pi/agent')),
           'omp':home/'.omp/agent','hermes':Path(os.environ.get('HERMES_HOME',home/'.hermes')),
           'antigravity':home/'.gemini'}
    rows=[];notes=[]
    roots=[]
    for app in apps:
        roots += [(app,bases[app]/'skills','personal:'+app),
                  (app,workspace/('.'+('gemini' if app=='antigravity' else app))/'skills','workspace:'+app)]
    roots += [('',workspace/'.agents/skills','workspace:shared'),('',home/'.agents/skills','personal:shared')]
    if 'antigravity' in apps:
        roots += [('antigravity',bases['antigravity']/'antigravity/skills','personal:antigravity-desktop'),
                  ('antigravity',workspace/'.agent/skills','workspace:antigravity-desktop')]
    for app,folder,scope in roots:
        if not folder.is_dir():continue
        count=0
        for directory,dirs,files in os.walk(folder,followlinks=False):
            base=Path(directory)
            dirs[:]=sorted(d for d in dirs if d not in SKIP and not (base/d).is_symlink())
            if len(base.relative_to(folder).parts)>7:dirs[:]=[];continue
            if 'SKILL.md' not in files:continue
            count+=1
            if count>800:notes.append('Some skill folders contain more entries than this view can show.');break
            try:
                row=skill(base/'SKILL.md',app,scope+':'+base.relative_to(folder).as_posix())
                if row:rows.append(row)
            except OSError:notes.append('Some local skill files could not be read.')
    # Only server names/status are exposed. Commands, headers and credentials stay private.
    for app,path,field in [('codex',bases['codex']/'config.toml','mcp_servers'),
                           ('claude',workspace/'.mcp.json','mcpServers'),
                           ('claude',home/'.claude.json','mcpServers'),
                           ('pi',bases['pi']/'mcp.json','mcpServers'),
                           ('omp',bases['omp']/'mcp.json','mcpServers'),
                           ('antigravity',bases['antigravity']/'antigravity/mcp_config.json','mcpServers')]:
        if app not in apps or not path.is_file() or path.is_symlink() or path.stat().st_size>2*1024*1024:continue
        try:
            if path.suffix=='.toml':
                import tomllib
                data=tomllib.loads(path.read_text(encoding='utf-8'))
            else:data=json.loads(path.read_text(encoding='utf-8'))
            for name,config in (data.get(field) or {}).items():
                if not isinstance(config,dict):continue
                disabled=config.get('disabled') is True or config.get('enabled') is False
                rows.append(entry('Tool',str(name),'A configured connection. Access is checked by its AI app.',app,
                                  app+':connection:'+str(name),'Disabled' if disabled else 'Configured',type='Connection'))
        except (OSError,ValueError,AttributeError,ImportError):notes.append(APPS[app]+': connection details could not be read.')
    for command,title,description in [('ffmpeg','FFmpeg','Process video and audio.'),('ffprobe','FFprobe','Inspect video and audio files.'),
                                      ('git','Git','Work with versioned files and repositories.'),('python','Python','Run Python scripts.'),('node','Node.js','Run JavaScript tools.')]:
        if shutil.which(command):rows.append(entry('Tool',title,description,'','local:'+command,'Installed',type='Local tool'))
    extra,plugin_notes=plugins(workspace,home,bases,apps)
    rows+=extra;notes+=plugin_notes
    return rows,notes


def native(choice, workspace, env, notes=None):
    import workspace_agents as agents
    import workspace_codex as codex
    app=choice['id'];rows=[];notes=notes if notes is not None else []
    def add_skill(data):
        path=data.get('path') or (data.get('sourceInfo') or {}).get('path')
        if path:
            row=skill(path,app,app+':reported:'+str(path),'Disabled' if data.get('enabled') is False else 'Reported by app')
            if row:rows.append(row);return
        name=short(data.get('name',''))
        if name:rows.append(entry('Skill',name,short(data.get('description','')),app,app+':skill:'+name,'Disabled' if data.get('enabled') is False else 'Reported by app',command=name))
    if app=='codex':
        def read_catalog(fetch):
            def pages(method,params):
                cursor=None;seen=set()
                for _ in range(20):
                    result=fetch(method,dict(params,**({'cursor':cursor} if cursor else {})))
                    yield from result.get('data',[])
                    cursor=result.get('nextCursor')
                    if not cursor:return
                    if cursor in seen:break
                    seen.add(cursor)
                notes.append('Codex: this catalog has more pages than this view can load.')
            try:
                result=fetch('skills/list',{'cwds':[str(workspace)],'forceReload':True})
                for block in result.get('data',[]):
                    for data in block.get('skills',[]):add_skill(data)
            except (ValueError,OSError,subprocess.SubprocessError):notes.append('Codex: skills could not be refreshed. Local skill files are still shown.')
            try:
                for server in pages('mcpServerStatus/list',{'limit':100}):
                    for name,tool in (server.get('tools') or {}).items():
                        connection=short(server.get('name',''))
                        service=str(name).split('.',1)[0] if connection=='codex_apps' and '.' in str(name) else connection
                        row=entry('Tool',str(name),short(tool.get('description','')),app,app+':tool:'+connection+':'+str(name),'Reported by app',connection=connection,service=service,type='Tool')
                        row['aliases']=[entry('Tool',str(name),'',app,app+':tool:'+str(name))['key']]
                        rows.append(row)
            except (ValueError,OSError,subprocess.SubprocessError):notes.append('Codex: some connected tools could not be refreshed.')
            try:
                # Prefer the runtime snapshot: app/list also pages the public directory.
                try:
                    installed=fetch('app/installed',{'forceRefresh':False}).get('apps')
                    if not isinstance(installed,list):raise ValueError('No runtime snapshot')
                    ids=[a['id'] for a in installed if isinstance(a,dict) and isinstance(a.get('id'),str)]
                    details={}
                    for offset in range(0,len(ids),100):
                        for data in fetch('app/read',{'appIds':ids[offset:offset+100],'includeTools':False}).get('apps',[]):details[data['id']]=data
                    available=[dict(details.get(a['id'],{}),id=a['id'],runtimeName=a.get('runtimeName'),name=details.get(a['id'],{}).get('name') or a.get('runtimeName') or '',
                                    isAccessible=True,isEnabled=a.get('enabled',False)) for a in installed if isinstance(a,dict) and a.get('id')]
                except (ValueError,OSError,subprocess.SubprocessError):available=pages('app/list',{'limit':100})
                for data in available:
                    if data.get('isAccessible') is not True:continue
                    name=short(data.get('name',''))
                    if name:rows.append(entry('Tool',name,short(data.get('description','')),app,'codex:app:'+str(data['id']),
                        'Disabled' if data.get('isEnabled') is False else 'Reported by app',service=data.get('runtimeName') or name,app_id=data['id'],type='App'))
            except (ValueError,OSError,subprocess.SubprocessError):notes.append('Codex: connected apps could not be refreshed. Open Codex, then try Refresh.')
        codex.rpc(choice['argv'],read_catalog,workspace,env)
    elif app in {'pi','omp'}:
        host=agents.Metadata(choice['argv'],app,workspace,env)
        try:
            data=host.call('get_commands' if app=='pi' else 'get_available_commands')
            for row in data.get('commands',[]):
                if row.get('source')=='skill' or str(row.get('name','')).startswith('skill:'):add_skill(row)
                elif row.get('source')=='mcp':rows.append(entry('Tool',row['name'],short(row.get('description','')),app,app+':tool:'+row['name'],'Reported by app',type='Tool'))
            state=host.call('get_state')
            for tool in state.get('dumpTools',[]):
                if isinstance(tool,dict) and tool.get('name'):
                    rows.append(entry('Tool',tool['name'],short(tool.get('description','').split('\n')[0]),app,app+':tool:'+tool['name'],'Reported by app',type='Tool'))
        finally:host.close()
    elif app=='hermes':
        result=subprocess.run([*agents.base_command(choice['argv']),'tools','list'],cwd=workspace,env=env,
            stdin=subprocess.DEVNULL,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=20,
            **({'creationflags':subprocess.CREATE_NO_WINDOW} if os.name=='nt' else {}))
        if result.returncode:raise ValueError('Hermes could not report its tools.')
        plugin_section=False
        for line in result.stdout.splitlines():
            if 'Plugin toolsets' in line:plugin_section=True
            elif 'Built-in toolsets' in line or 'MCP servers' in line:plugin_section=False
            match=re.match(r'\s*[✓✗]?\s*(enabled|disabled)\s+([\w-]+)\s+(.*)',line)
            if match:
                state,name,description=match.groups()
                row=entry('Tool',name,short(description),app,app+':toolset:'+name,'Enabled in app' if state=='enabled' else 'Disabled',type='Toolset')
                rows.append(row)
                if plugin_section:
                    plugin=entry('Plugin',name,short(description),app,app+':plugin-toolset:'+name,row['sources'][0]['status'],type='Plugin toolset')
                    plugin['tool_keys']=[row['key']];rows.append(plugin)
            else:
                match=re.match(r'\s+([\w-]+)\s+all tools enabled\s*$',line)
                if match:rows.append(entry('Tool',match[1],'A connection enabled in Hermes.',app,app+':connection:'+match[1],'Enabled in app',type='Connection'))
    return rows


def document(item):
    paths=[Path(s['path']) for s in item.get('sources',[]) if s.get('path')]
    if not paths:return ''
    path=paths[0]
    if path.name!='SKILL.md' or path.is_symlink() or not path.is_file() or path.stat().st_size>128*1024:
        raise ValueError('This skill file has moved or cannot be opened. Refresh the library.')
    try:return path.read_text(encoding='utf-8-sig',errors='replace')
    except OSError:raise ValueError('This skill file could not be read. Check its permissions or refresh the library.') from None
