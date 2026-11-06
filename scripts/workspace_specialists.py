"""Read and edit native agent files. The native harness owns discovery and delegation."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import re
import tempfile
import tomllib

import yaml


APPS = {'codex':'Codex','omp':'OMP','pi':'Pi','claude':'Claude Code','antigravity':'Antigravity'}


def roots(kind, cwd, env):
    home=Path(env.get('USERPROFILE') or env.get('HOME') or Path.home())
    cwd=Path(cwd).resolve()
    if kind not in APPS:return {}
    project={'codex':'.codex','omp':'.omp','pi':'.pi','claude':'.claude','antigravity':'.agents'}[kind]
    # Use the nearest native project root, then the repository, then the working folder.
    candidates=[]
    for candidate in (cwd,*cwd.parents):
        if candidate!=cwd and candidate in {home.resolve(),Path.home().resolve()}:break
        candidates.append(candidate)
        if (candidate/'.git').exists():break
    parent=next((p for p in candidates if (p/project).is_dir()),None)
    parent=parent or next((p for p in candidates if (p/'.git').exists()),cwd)
    user={'codex':env.get('CODEX_HOME') or home/'.codex',
          'omp':env.get('PI_CODING_AGENT_DIR') or home/'.omp/agent',
          'pi':env.get('PI_CODING_AGENT_DIR') or home/'.pi/agent',
          'claude':env.get('CLAUDE_CONFIG_DIR') or home/'.claude',
          'antigravity':home/'.gemini/config'}[kind]
    user=Path(user)
    if not user.is_absolute():user=cwd/user
    return {'project':parent/project/'agents','user':user/'agents'}


def local(command):
    return not any(Path(v).name.lower() in {'wsl','wsl.exe','ssh','ssh.exe','docker','podman'} for v in command)


def path_for(kind,cwd,env,scope,file):
    locations=roots(kind,cwd,env)
    if scope not in locations:raise ValueError('Choose a supported native agent location.')
    relative=Path(file or '')
    suffix='.toml' if kind=='codex' else '.md'
    if not file or relative.is_absolute() or '..' in relative.parts or relative.suffix!=suffix:
        raise ValueError('Choose a native agent file in its agent folder.')
    root=locations[scope].resolve();path=root/relative
    if not path.resolve().is_relative_to(root):raise ValueError('The native agent file points outside its agent folder.')
    return path


def parse(kind,source):
    try:
        if kind=='codex':
            data=tomllib.loads(source);instructions=data.get('developer_instructions','');effort=data.get('model_reasoning_effort','')
        else:
            match=re.match(r'\A---\s*\n(.*?)\n---[ \t]*(?:\n|$)',source,re.S)
            if not match:raise ValueError()
            data=yaml.safe_load(match[1]);instructions=source[match.end():].strip()
            effort=data.get('thinkingLevel' if kind=='omp' else 'effort','') if isinstance(data,dict) else ''
        if not isinstance(data,dict) or not all(isinstance(data.get(k),str) and data[k].strip() for k in ('name','description')):raise ValueError()
        if not isinstance(instructions,str):raise ValueError()
        if kind=='codex' and 'developer_instructions' not in data:raise ValueError()
        model=data.get('model','')
        return {'name':data['name'],'description':data['description'],'instructions':instructions,
                'model':model,'effort':effort,'settings':data}
    except (ValueError,yaml.YAMLError,TypeError):
        raise ValueError('This native agent needs a name, a description, and valid '+('TOML' if kind=='codex' else 'Markdown frontmatter')+'.') from None


def read(kind,cwd,env,scope,file):
    path=path_for(kind,cwd,env,scope,file)
    try:
        raw=path.read_bytes()
        if len(raw)>256000:raise ValueError('This native agent file is too large to edit here. Open it in its AI app.')
        source=raw.decode('utf-8-sig').replace('\r\n','\n')
    except FileNotFoundError:raise ValueError('This native agent is missing. Reconnect it or choose another agent.') from None
    row=parse(kind,source)
    return {**row,'app':kind,'scope':scope,'file':file,'path':str(path),'source':source,'revision':hashlib.sha256(raw).hexdigest()}


def inventory(kind,cwd,env,command=()):
    if not local(command):return {'items':[],'note':'This connection runs in another environment. Manage its native agents there.','editable':False}
    if kind not in APPS:
        return {'items':[],'editable':False,'note':('Hermes uses native profiles and delegation routes. Configure them in Native delegation settings.' if kind=='hermes' else 'This connection does not expose native agent files. Its native agent behavior remains available.')}
    rows=[];notes=[];seen=set()
    for scope,root in roots(kind,cwd,env).items():
        if not root.exists():continue
        pattern='*.toml' if kind=='codex' else '*.md'
        paths=sorted(root.rglob(pattern) if kind=='claude' else root.glob(pattern))
        if kind=='antigravity':paths+=sorted(root.glob('*/agent.md'))
        for path in paths:
            file=path.relative_to(root).as_posix()
            try:row=read(kind,cwd,env,scope,file)
            except (OSError,ValueError) as error:
                from workspace_support import human_error
                notes.append(path.name+': '+human_error(error));continue
            row['shadowed']=row['name'] in seen;seen.add(row['name'])
            rows.append({k:v for k,v in row.items() if k not in {'source','settings','instructions'}})
    return {'items':rows,'editable':True,'notes':notes,'note':('Pi requires a compatible subagent extension. Project agents also depend on its scope settings.' if kind=='pi' else ''),
            'locations':{k:str(v) for k,v in roots(kind,cwd,env).items()}}


def changed_source(kind,source,changes):
    """Change only the edited fields; retain unfamiliar native settings and instructions."""
    current=parse(kind,source)
    fields={'name':'name','description':'description','model':'model',
            'effort':'model_reasoning_effort' if kind=='codex' else 'thinkingLevel' if kind=='omp' else 'effort'}
    if kind in {'pi','antigravity'}:fields.pop('effort')
    if kind=='codex':
        fields['instructions']='developer_instructions'
        for field,key in fields.items():
            if field not in changes or changes[field]==current.get(field):continue
            value=changes[field]
            replacement='' if field in {'model','effort'} and not value else key+' = '+json.dumps(value,ensure_ascii=False)+'\n'
            found=False
            for match in re.finditer(r'(?m)^'+re.escape(key)+r'\s*=',source):
                try:tomllib.loads(source[:match.start()])
                except ValueError:continue  # An apparent key inside a multiline instruction.
                # Required agent fields are top-level, before TOML tables.
                tables=[m for m in re.finditer(r'(?m)^\[',source[:match.start()]) if _toml_complete(source[:m.start()])]
                if tables:continue
                for end in [m.end() for m in re.finditer('\n',source[match.start():])]:
                    stop=match.start()+end
                    try:part=tomllib.loads(source[match.start():stop])
                    except ValueError:continue
                    if key in part:
                        source=source[:match.start()]+replacement+source[stop:];found=True;break
                if not found and _toml_complete(source[match.start():]):source=source[:match.start()]+replacement;found=True
                if found:break
            if not found:source=replacement+source
    else:
        match=re.match(r'\A---\s*\n(.*?)\n---[ \t]*(?:\n|$)',source,re.S)
        header=match[1];body=source[match.end():]
        for field,key in fields.items():
            if field not in changes or changes[field]==current.get(field):continue
            node=yaml.compose(header)
            pair=next(((k,v) for k,v in node.value if k.value==key),None)
            replacement=json.dumps(changes[field],ensure_ascii=False)
            if pair:
                value=pair[1];tail=header[value.end_mark.index:]
                if field in {'model','effort'} and not changes[field]:
                    header=header[:pair[0].start_mark.index]+tail
                    continue
                if value.end_mark.column==0 and tail and not tail.startswith('\n'):replacement+='\n'
                header=header[:value.start_mark.index]+replacement+tail
            elif field not in {'model','effort'} or changes[field]:header+='\n'+key+': '+replacement
        if 'instructions' in changes:body=changes['instructions'].strip()+'\n'
        source='---\n'+header+'\n---\n'+body
    parse(kind,source)
    return source


def _toml_complete(source):
    try:tomllib.loads(source);return True
    except ValueError:return False


def save(kind,cwd,env,data):
    scope=data.get('scope','project');file=data.get('file','');revision=data.get('revision')
    changes={k:data[k] for k in ('name','description','instructions','model','effort') if k in data}
    if any(not isinstance(v,str) or len(v)>20000 for v in changes.values()):raise ValueError('Enter valid agent instructions and preferences.')
    if not file:
        if not changes.get('name','').strip() or not changes.get('description','').strip():raise ValueError('Give the agent a name and a short description of when to use it.')
        stem=re.sub(r'[^\w-]+','-',changes['name'].strip(),flags=re.UNICODE).strip('-')[:80]
        if not stem:raise ValueError('Give this agent a name with letters or numbers.')
        file=stem+('.toml' if kind=='codex' else '.md')
    path=path_for(kind,cwd,env,scope,file)
    original=path.read_bytes() if path.exists() else None
    if original is not None:
        if revision!=hashlib.sha256(original).hexdigest():raise ValueError('This native agent changed. Reopen it before saving; your edits have not replaced it.')
        source=original.decode('utf-8-sig').replace('\r\n','\n')
    else:
        if revision:raise ValueError('This native agent was moved or removed. Reopen its list before saving.')
        source=('name = "New agent"\ndescription = "New agent"\ndeveloper_instructions = ""\n' if kind=='codex'
                else '---\nname: New agent\ndescription: New agent\n---\n')
    if 'source' in data:
        source=data['source']
        if not isinstance(source,str) or len(source)>256000:raise ValueError('Enter a native agent definition of up to 256,000 characters.')
    else:source=changed_source(kind,source,changes)
    parsed=parse(kind,source)
    if kind=='antigravity' and parsed['model'] not in {'','inherit','flash','pro'}:raise ValueError('Antigravity agent models use Inherit, Flash, or Pro.')
    if kind=='omp' and parsed['name'].strip().lower() in {'main','sub'}:raise ValueError('OMP reserves this agent name. Choose another name.')
    path.parent.mkdir(parents=True,exist_ok=True)
    handle,tmp=tempfile.mkstemp(prefix=path.name+'.',dir=path.parent)
    try:
        with os.fdopen(handle,'w',encoding='utf-8') as out:out.write(source)
        if (path.read_bytes() if path.exists() else None)!=original:raise ValueError('This native agent changed while saving. Reopen it before trying again.')
        if original is None:
            # Exclusive creation prevents replacing a same-named native definition.
            with path.open('x',encoding='utf-8') as out:out.write(source)
        else:os.replace(tmp,path)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)
    return read(kind,cwd,env,scope,file)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['list','read','save']);parser.add_argument('--app',required=True)
    parser.add_argument('--business-id',required=True);parser.add_argument('--scope',default='project')
    parser.add_argument('--file');parser.add_argument('--input');parser.add_argument('--url',default='http://127.0.0.1:4187')
    args=parser.parse_args()
    from workspace_goals import live_change
    from urllib.parse import urlencode
    import sys
    data={'kind':args.app,'action':args.action,'scope':args.scope,**({'file':args.file} if args.file else {})}
    if args.action=='save':
        data.update(json.loads(sys.stdin.read() if args.input=='-' else args.input or '{}'))
        result=live_change(args.url,args.business_id,data,'/api/native-agents')
    else:result=live_change(args.url,args.business_id,None,'/api/native-agents?'+urlencode({'business':args.business_id,**data}))
    print(json.dumps(result,ensure_ascii=False))


if __name__=='__main__':
    try:main()
    except (OSError,ValueError) as error:
        from workspace_context_settings import cli_error
        raise SystemExit('Error: '+cli_error(error))
