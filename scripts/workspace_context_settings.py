"""Read and edit native context settings. No Aura scheduler or provider requests."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import subprocess
import tempfile
import re


# Native keys only. Unset values keep the installed app's defaults.
FIELDS = {
    'omp': [
        ('providers.cacheWarming','Cache warming','cache',['off','streaming','idle']),
        ('providers.cacheRetention','Cache lifetime','cache',['auto','short','long','none']),
        ('compaction.enabled','Automatic compaction','context','bool'),
        ('compaction.thresholdPercent','Compact at · %','context',(1,100)),
        ('compaction.thresholdTokens','Compact at · tokens','context',(1,100000000)),
        ('compaction.keepRecentTokens','Keep recent tokens','context',(0,100000000)),
        ('compaction.methodOrder','Preferred compaction method','context','methods'),
        ('compaction.handoffSaveToDisk','Save automatic handoff documents','context','bool')],
    'pi': [
        ('cacheWarming','Cache warming','cache',['off','streaming','idle']),
        ('compaction.enabled','Automatic compaction','context','bool'),
        ('compaction.reserveTokens','Reserve tokens before compaction','context',(0,100000000)),
        ('compaction.keepRecentTokens','Keep recent tokens','context',(0,100000000))],
    'claude': [
        ('promptCacheTtl','Conversation cache lifetime','cache',['5m','1h']),
        ('subagentPromptCacheTtl','Other requests · cache lifetime','cache',['5m','1h']),
        ('env.CLAUDE_AUTOCOMPACT_PCT_OVERRIDE','Compact earlier · %','context',(1,100)),
        ('autoCompactEnabled','Automatic compaction','context','bool'),
        ('idleCompaction','Compact while idle','context','bool')],
    'hermes': [
        ('prompt_caching.cache_ttl','Claude cache lifetime','cache',['auto','5m','1h']),
        ('compression.enabled','Automatic compaction','context','bool'),
        ('compression.threshold','Compact at · %','context',(.01,1)),
        ('compression.target_ratio','Recent context to retain · %','context',(.01,1)),
        ('compression.codex_app_server_auto','Codex thread compaction','context',['native','hermes','off'])],
    'codex': [
        ('model_auto_compact_token_limit','Compact at · tokens','context',(1,100000000)),
        ('model_auto_compact_token_limit_scope','Count context','context',['total','body_after_prefix']),
        ('model_post_turn_compact_threshold_percent','Compact after a response · %','context',(0,100))],
}


class NativeSettingsError(ValueError):
    def __init__(self,message,diagnostic):
        super().__init__(message)
        self.diagnostic=diagnostic


def nested(data,key):
    for part in key.split('.'):
        if not isinstance(data,dict):return None
        data=data.get(part)
    return data


def assign(data,key,value):
    parts=key.split('.')
    for part in parts[:-1]:
        if not isinstance(data.get(part),dict):data[part]={}
        data=data[part]
    if value is None:data.pop(parts[-1],None)
    else:data[parts[-1]]=value


def run(command,args,cwd,env):
    from workspace_execution import Execution
    execution=Execution()
    try:
        process=execution.popen([*command,*args],cwd=cwd,env=env,stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='utf-8',errors='replace')
        stdout,stderr=process.communicate(timeout=30)
    except subprocess.TimeoutExpired:raise ValueError('The AI app took too long to respond. Check that it opens normally, then try again.') from None
    finally:
        if execution.process and execution.process.poll() is None:execution._force_stop()
    if process.returncode:raise NativeSettingsError('The AI app could not read or save these settings. Check its configuration and try again.',stderr[-2000:])
    return stdout.strip()


def native_command(command,kind):
    from workspace_agents import base_command
    from workspace_codex import base_command as codex_base
    return (codex_base if kind=='codex' else base_command)(command)


def settings_path(kind,env,cwd=None):
    home=Path(env.get('USERPROFILE') or env.get('HOME') or Path.home())
    path=(Path(env.get('PI_CODING_AGENT_DIR') or home/'.pi/agent')/'settings.json' if kind=='pi'
            else Path(env.get('CLAUDE_CONFIG_DIR') or home/'.claude')/'settings.json')
    return path if path.is_absolute() else Path(cwd or Path.cwd())/path


def read_json(path):
    if not path.exists():return {}
    try:data=json.loads(path.read_text(encoding='utf-8-sig'))
    except (ValueError,UnicodeError):raise ValueError('The AI app’s settings file could not be read. Fix its JSON formatting before saving.') from None
    if not isinstance(data,dict):raise ValueError('The AI app’s settings file must contain a JSON object.')
    return data


def describe(command,kind,cwd,env=None,definitions=None,profile=None):
    env=dict(os.environ if env is None else env);command=native_command(command,kind)
    definitions=FIELDS.get(kind,[]) if definitions is None else definitions;values={};note='';shadowed=[];local={};scope='Native app settings on this computer. Other chats using this profile share these settings.'
    if not definitions:return {'app':kind,'fields':[],'note':'This connection does not report editable cache or compaction settings. Its native behavior stays in effect.'}
    if kind=='omp':
        raw=json.loads(run(command,['config','list','--json'],cwd,env))
        values={key:raw[key].get('value') for key,*_ in definitions if key in raw}
        limits=raw.get('compaction.modelThresholds',{}).get('value')
        if limits and raw.get('compaction.modelThresholdsEnabled',{}).get('value') is not False:
            note='Native per-model compaction limits may take priority over the general trigger.'
        project=Path(cwd)/'.omp/config.yml'
        if project.is_file():
            import yaml
            try:local=yaml.safe_load(project.read_text(encoding='utf-8')) or {}
            except yaml.YAMLError:raise ValueError('The project’s OMP settings could not be read. Fix its YAML formatting before saving.') from None
            shadowed=[key for key,*_ in definitions if nested(local,key) is not None]
            if shadowed:note+=' Some settings are controlled by this project.'
    elif kind=='hermes':
        prefix=['--profile',profile] if profile else []
        raw={section:json.loads(run(command,[*prefix,'config','get',section,'--json'],cwd,env)) for section in dict.fromkeys(key.split('.')[0] for key,*_ in definitions)}
        values={key:nested(raw,key) for key,*_ in definitions}
    elif kind=='codex':
        from workspace_codex import rpc
        native=rpc(command,[('config/read',{'includeLayers':False,'cwd':str(cwd)})],cwd,env)[0]
        raw=native['config']
        values={key:raw[key] if key in raw else nested(raw,key) for key,*_ in definitions if key in raw or nested(raw,key) is not None or key.startswith('agents.')}
    else:
        # These apps document JSON settings files. Preserve unrelated keys and layers.
        if any(Path(arg).name.lower() in {'wsl','wsl.exe','ssh','ssh.exe','docker','podman'} for arg in command):
            return {'app':kind,'fields':[],'note':'This launcher runs outside Aura’s local environment. Use its native settings there.'}
        if kind=='claude':
            version=re.search(r'\b(\d+)\.(\d+)\.(\d+)\b',run(command,['--version'],cwd,env))
            version=tuple(map(int,version.groups())) if version else (0,0,0)
            definitions=[r for r in definitions if not (r[0] in {'promptCacheTtl','subagentPromptCacheTtl'} and version<(2,1,242)) and not (r[0]=='idleCompaction' and version<(2,1,290))]
        path=settings_path(kind,env,cwd);raw=read_json(path)
        values={key:nested(raw,key) for key,*_ in definitions}
        project_root=Path(cwd)
        if kind=='claude':project_root=next((p for p in [Path(cwd),*Path(cwd).parents] if (p/'.git').exists()),Path(cwd))
        project=project_root/('.pi/settings.json' if kind=='pi' else '.claude/settings.json')
        local=read_json(project)
        if kind=='claude':
            for key,value in read_json(project_root/'.claude/settings.local.json').items():
                if isinstance(value,dict) and isinstance(local.get(key),dict):local[key]={**local[key],**value}
                else:local[key]=value
        shadowed=[key for key,*_ in definitions if nested(local,key) is not None and not (kind=='pi' and key=='cacheWarming')]
        if shadowed:note='Some settings are overridden in this project. Project values are shown separately.'
        if kind=='pi' and (nested(raw,'compaction.modelOverrides') or nested(local,'compaction.modelOverrides')):
            note+=' Native per-model token settings may take priority over the general reserve.'
    rows=[]
    for key,label,group,kind_spec in definitions:
        if key not in values:continue
        row={'id':key,'name':label,'group':group,'value':None if kind=='omp' and key in {'compaction.thresholdPercent','compaction.thresholdTokens'} and values[key]==-1 else values[key]}
        if key.startswith('env.') and isinstance(row['value'],str) and row['value'].isdigit():row['value']=int(row['value'])
        if isinstance(kind_spec,list):
            row.update(type='select',options=[{'value':v,'name':{'streaming':'During work','idle':'During work and short breaks','off':'Off','auto':'Automatic','short':'Short','long':'Long','none':'Disabled','5m':'5 minutes','1h':'1 hour'}.get(v,v)} for v in kind_spec])
            if row['value'] is not None and row['value'] not in kind_spec:row['options'].append({'value':row['value'],'name':'Current: '+str(row['value'])})
        elif isinstance(kind_spec,tuple):row.update(type='number',min=0 if kind=='hermes' else kind_spec[0],max=9007199254740991 if kind_spec[1]==100000000 else kind_spec[1],step='any' if kind=='hermes' else 1)
        elif kind_spec in {'text','model-map'}:row.update(type=kind_spec)
        elif kind_spec=='methods':
            order=row['value'] if isinstance(row['value'],list) else []
            names={'remote':'Provider compaction','snapcompact':'Snapcompact','handoff':'Handoff document','shake':'Shake','soft':'Summary'}
            row.update(type='methods',options=[{'value':[method,*[v for v in order if v!=method]],'name':names.get(method,method)} for method in order],
                description='The preferred method runs first. Existing fallback methods are kept.')
        else:row.update(type='select',options=[{'value':True,'name':'On'},{'value':False,'name':'Off'}])
        if key in shadowed:row.update(project_value=nested(local,key),readonly=True)
        if kind=='codex':
            origin=(native.get('origins',{}).get(key) or {}).get('name') or {}
            if origin.get('type') not in {None,'user'} or origin.get('profile'):
                row.update(readonly=True,project_value=row['value'])
        if key=='compaction.thresholdTokens':row['description']='A fixed token trigger takes priority over the percentage trigger.'
        if key=='env.CLAUDE_AUTOCOMPACT_PCT_OVERRIDE':row['description']='Can lower the native trigger; values above the native default do not raise it.'
        if kind=='hermes' and isinstance(kind_spec,tuple):row['display_scale']=100
        if kind=='claude':
            source=key[4:] if key.startswith('env.') else {'promptCacheTtl':'CLAUDE_CODE_PROMPT_CACHE_TTL','subagentPromptCacheTtl':'CLAUDE_CODE_SUBAGENT_PROMPT_CACHE_TTL',
                    'autoCompactEnabled':'DISABLE_AUTO_COMPACT'}.get(key)
            if source and env.get(source):row.update(readonly=True,project_value=env[source],source_name='Environment')
        rows.append(row)
    revision=hashlib.sha256(json.dumps({'fields':rows,'app':kind,'cwd':str(Path(cwd).resolve()),'profile':profile,
        'homes':{k:env.get(k) for k in ('HOME','USERPROFILE','CODEX_HOME','PI_CODING_AGENT_DIR','CLAUDE_CONFIG_DIR','HERMES_HOME')}},sort_keys=True).encode()).hexdigest()
    return {'app':kind,'scope':scope,'fields':rows,'revision':revision,'note':note}


def reported(rows,overrides=None):
    """New ACP connections can expose native context controls without an Aura catalog."""
    from workspace_native_settings import options
    fields=[]
    for row in rows:
        if row.get('type','select')!='select' or row.get('category') in {'model','mode','thought_level'}:continue
        text=' '.join(str(row.get(k,'')) for k in ('id','name','category'))
        if not re.search(r'cache|compact|compression|context',text,re.I):continue
        fields.append({'id':row['id'],'name':row.get('name') or row['id'],'group':'cache' if re.search('cache',text,re.I) else 'context',
            'type':'select','options':list(options(row.get('options',[]))),
            'value':(overrides or {}).get(row['id'],row.get('currentValue'))})
    return {'fields':fields,'revision':hashlib.sha256(json.dumps(fields,sort_keys=True).encode()).hexdigest(),
        'scope':'This chat in its native AI app. Changes apply when you next send a request.',
        'note':'' if fields else 'This connection does not report editable cache or compaction settings. Its native behavior stays in effect.'}


def validate(rows,changes):
    if not isinstance(changes,dict) or not changes:raise ValueError('Choose a setting to change.')
    available={r['id']:r for r in rows};result={}
    for key,value in changes.items():
        row=available.get(key)
        if not row or row.get('readonly'):raise ValueError('This setting is unavailable or controlled by this project. Refresh the settings.')
        if value is None:result[key]=None;continue
        if row['type']=='select':
            if not any(type(value)==type(o['value']) and value==o['value'] for o in row['options']):raise ValueError('Choose an available value for '+row['name']+'.')
        elif row['type']=='number':
            import math
            if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value) or not row['min']<=value<=row['max'] or row['step']==1 and value!=int(value):raise ValueError('Enter a valid value for '+row['name']+'.')
        elif row['type']=='methods':
            value=value if isinstance(value,list) else [v.strip() for v in str(value).split(',') if v.strip()]
            allowed={'remote','snapcompact','handoff','shake','soft',*(row.get('value') or [])}
            if not value or not all(isinstance(v,str) for v in value) or len(value)!=len(set(value)) or set(value)-allowed:raise ValueError('Choose valid native compaction methods without duplicates.')
        elif row['type']=='text':
            if not isinstance(value,str) or len(value)>300 or '\0' in value:raise ValueError('Enter a valid model or provider for '+row['name']+'.')
        elif row['type']=='model-map':
            if not isinstance(value,dict) or len(value)>200 or any(not isinstance(k,str) or not k or len(k)>100 or not isinstance(v,str) or not v or len(v)>300 for k,v in value.items()):raise ValueError('Give each native role or agent a name and a model.')
        result[key]=value
    return result


def save(command,kind,cwd,env,changes,revision,definitions=None,profile=None):
    current=describe(command,kind,cwd,env,definitions,profile)
    if revision!=current.get('revision'):raise ValueError('The native settings changed. Refresh them before saving.')
    changes=validate(current['fields'],changes);base=native_command(command,kind)
    if kind in {'pi','claude'}:
        path=settings_path(kind,env,cwd);original=path.read_bytes() if path.exists() else None;data=read_json(path)
        for key,value in changes.items():assign(data,key,str(value) if key.startswith('env.') and value is not None else value)
        path.parent.mkdir(parents=True,exist_ok=True)
        handle,tmp=tempfile.mkstemp(prefix=path.name+'.',dir=path.parent)
        try:
            with os.fdopen(handle,'w',encoding='utf-8') as stream:json.dump(data,stream,indent=2,ensure_ascii=False);stream.write('\n')
            if (path.read_bytes() if path.exists() else None)!=original:raise ValueError('The native settings changed while saving. Refresh them before trying again.')
            os.replace(tmp,path)
        finally:
            if os.path.exists(tmp):os.unlink(tmp)
    elif kind=='codex':
        from workspace_codex import rpc
        rpc(base,[('config/batchWrite',{'edits':[{'keyPath':k,'value':v,'mergeStrategy':'replace'} for k,v in changes.items()]})],cwd,env)
    else:
        for key,value in changes.items():
            args=(['config','reset',key,'--json'] if kind=='omp' else ['config','unset',key]) if value is None else ['config','set',key,value if kind=='hermes' and isinstance(value,str) else json.dumps(value)]
            run(base,['--profile',profile,*args] if kind=='hermes' and profile else args,cwd,env)
    result=describe(command,kind,cwd,env,definitions,profile)
    observed={r['id']:r['value'] for r in result['fields']}
    if any(value is not None and observed.get(key)!=value for key,value in changes.items()):raise ValueError('The AI app did not apply every requested value. Refresh to see its current settings.')
    return result


def main(section='context'):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--app',required=True);parser.add_argument('--business-id',required=True)
    parser.add_argument('--chat');parser.add_argument('--url',default='http://127.0.0.1:4187')
    parser.add_argument('--profile',help='Native Hermes profile instead of an active chat')
    parser.add_argument('--set',help='JSON object of native setting keys and values; null removes a setting')
    parser.add_argument('--revision',help='Revision returned when reading settings')
    args=parser.parse_args()
    from workspace_goals import live_change
    from urllib.parse import urlencode
    data={'kind':args.app,**({'chat_id':args.chat} if args.chat else {}),**({'profile':args.profile} if args.profile else {})}
    endpoint='/api/delegation-settings' if section=='delegation' else '/api/context-settings'
    result=live_change(args.url,args.business_id,{**data,'changes':json.loads(args.set),'revision':args.revision},endpoint) if args.set else live_change(args.url,args.business_id,None,endpoint+'?'+urlencode({'business':args.business_id,**data}))
    print(json.dumps(result,ensure_ascii=False))


def cli_error(error):
    from urllib.error import HTTPError,URLError
    from workspace_support import human_error
    if isinstance(error,HTTPError):
        try:return human_error(ValueError(json.load(error).get('error','Aura could not save this change.')))
        except ValueError:return 'Aura could not save this change. Check --url and try again.'
    if isinstance(error,URLError):return 'Aura is not reachable. Start the local Aura service and check --url.'
    return human_error(error)


if __name__=='__main__':
    try:main()
    except (OSError,ValueError) as error:raise SystemExit('Error: '+cli_error(error))
