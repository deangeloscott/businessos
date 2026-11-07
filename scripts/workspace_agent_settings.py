"""Native delegation preferences; no Aura routing or scheduling loop."""
import re
import copy
import hashlib
import json

import workspace_context_settings as native


FIELDS={
    'codex':[
        ('agents.default_subagent_model','Default subagent model','delegation','text'),
        ('agents.default_subagent_reasoning_effort','Default subagent effort','delegation','text'),
        ('agents.max_concurrent_threads_per_session','Concurrent subagents','delegation',(1,100000000))],
    'claude':[
        ('env.CLAUDE_CODE_SUBAGENT_MODEL','Default subagent model','delegation','text')],
    'omp':[
        ('modelRoles','Model roles','delegation','model-map'),
        ('task.agentModelOverrides','Models for named agents','delegation','model-map')],
    'hermes':[
        ('delegation.model','Default subagent model','delegation','text'),
        ('delegation.provider','Default subagent provider','delegation','text')],
}


def describe(command,kind,cwd,env=None,profile=None):
    if kind not in FIELDS:
        return {'fields':[],'note':('Set models on native agent definitions. Pi uses its installed subagent extension.' if kind=='pi' else 'Use the settings reported by this connection or its native agent definitions.')}
    # Reuse the same native readers, writers, scope checks and readback as context settings.
    result=native.describe(command,kind,cwd,env,FIELDS[kind],profile)
    result['note']={'omp':'Roles apply when native work uses that role. Named agent overrides take precedence over agent model defaults.',
        'codex':'These are defaults. Explicit native agent and model selections can take precedence.',
        'claude':'This environment setting supplies the native subagent default. Explicit selections can take precedence.',
        'hermes':'Applies to this Hermes profile. Named routes are available through compatible native delegation plugins.'}[kind]
    if kind=='hermes':
        routing=hermes_routes(command,cwd,env,profile)
        result['routing']={k:v for k,v in routing.items() if not k.startswith('_')}
        if routing.get('available'):result['revision']=hashlib.sha256((result['revision']+routing['_revision']).encode()).hexdigest()
    return result


def save(command,kind,cwd,env,changes,revision,profile=None):
    if kind!='hermes':return native.save(command,kind,cwd,env,changes,revision,FIELDS.get(kind,[]),profile)
    current=describe(command,kind,cwd,env,profile)
    if revision!=current.get('revision'):raise ValueError('The native settings changed. Refresh them before saving.')
    if not isinstance(changes,dict) or not changes:raise ValueError('Choose a setting to change.')
    changes=dict(changes);routes=changes.pop('_routing',None)
    checked=native.validate(current['fields'],changes) if changes else {}
    if routes is not None:
        routing=hermes_routes(command,cwd,env,profile)
        if not routing.get('available') or routing.get('_revision')!=current['routing'].get('revision'):raise ValueError('Hermes routing changed. Reopen its settings before saving.')
        section=route_changes(routing['_section'],routes)
        prior_models={r['name']:r for r in (routing['_section'].get('backends',{}).get('model_map',{}).get('options') or [])}
        changed=[r for r in section.get('backends',{}).get('model_map',{}).get('options',[]) if any(r.get(k)!=prior_models.get(r['name'],{}).get(k) for k in ('model','provider'))]
        if changed:
            from workspace_hermes import metadata,model_route
            catalog=metadata(command,None,cwd,env,'model.options',profile=profile or 'default',explicit_only=True)
            for row in changed:row.update(model_route(catalog,(row.get('provider','')+':' if row.get('provider') else '')+row['model']))
        if 'profiles' in routes:
            from workspace_hermes import profiles as native_profiles
            available={p['name'] for p in native_profiles(command,None,cwd,env)}
            if any(p['name'] not in available or p['name']==(profile or 'default') for p in routes['profiles']):raise ValueError('Choose another existing Hermes profile for each profile route.')
    if checked:
        base=native.describe(command,kind,cwd,env,FIELDS[kind],profile)
        native.save(command,kind,cwd,env,checked,base['revision'],FIELDS[kind],profile)
    if routes is not None:
        # Preserve native defaults and unfamiliar route fields. Hermes owns the write.
        prefix=['--profile',profile] if profile else []
        actual=json.loads(native.run(native.native_command(command,kind),[*prefix,'config','get','delegation','--json'],cwd,env))
        for key in ('model','provider'):
            if 'delegation.'+key in checked:section[key]=actual.get(key)
        ignored={key.split('.')[-1] for key in checked}
        if {k:v for k,v in actual.items() if k not in ignored}!={k:v for k,v in routing['_section'].items() if k not in ignored}:raise ValueError('Hermes routing changed while saving. Reopen its settings.')
        native.run(native.native_command(command,kind),[*prefix,'config','set','delegation',json.dumps(section)],cwd,env)
        readback=json.loads(native.run(native.native_command(command,kind),[*prefix,'config','get','delegation','--json'],cwd,env))
        if readback!=section:raise ValueError('Hermes did not confirm every routing change. Reopen its settings.')
    return describe(command,kind,cwd,env,profile)


ROUTE_FIELDS=('name','description','provider','model')


def hermes_routes(command,cwd,env,profile=None):
    """The optional official plugin owns routing. Do not install or imitate it."""
    base=native.native_command(command,'hermes');prefix=['--profile',profile] if profile else []
    try:
        plugins=json.loads(native.run(base,[*prefix,'plugins','list','--json'],cwd,env))
        if not any(p.get('name')=='advanced-delegation' and p.get('status')=='enabled' for p in plugins):
            return {'available':False,'note':'Named routes need the official Advanced Delegation plugin and Hermes 0.22.5 or later.'}
        section=json.loads(native.run(base,[*prefix,'config','get','delegation','--json'],cwd,env)) or {}
        revision=hashlib.sha256(json.dumps(section,sort_keys=True).encode()).hexdigest()
        backends=section.get('backends') or {};models=backends.get('model_map') or {};profiles=backends.get('profile_routes') or {}
        return {'available':True,'mode':section.get('backend') or 'default','revision':revision,
            'models':[{k:r[k] for k in ROUTE_FIELDS if k in r} for r in models.get('options',[])],
            'profiles':[{k:r[k] for k in ('name','description') if k in r} for r in profiles.get('profiles',[])],
            'model_default':models.get('default',''),'profile_default':profiles.get('default',''),
            '_section':section,'_revision':revision}
    except (OSError,ValueError) as error:
        from workspace_support import human_error
        return {'available':False,'note':'Native routing could not be checked. '+human_error(error)}


def route_changes(section,requested):
    if not isinstance(requested,dict) or set(requested)-{'mode','models','profiles','model_default','profile_default'}:raise ValueError('Choose valid native routing settings.')
    mode=requested.get('mode')
    if mode not in {'default','model_map','profile_routes'}:raise ValueError('Choose a native delegation mode.')
    updated=copy.deepcopy(section);backends=updated.setdefault('backends',{})
    for key,backend,entries,default in (('models','model_map','options','model_default'),('profiles','profile_routes','profiles','profile_default')):
        if key not in requested:continue
        rows=requested[key];fields=ROUTE_FIELDS if key=='models' else ('name','description')
        if not isinstance(rows,list) or len(rows)>200:raise ValueError('Choose up to 200 native routes.')
        block=backends.setdefault(backend,{});prior={r['name']:r for r in block.get(entries,[])};saved=[];names=set()
        for row in rows:
            if not isinstance(row,dict) or set(row)-set(fields) or any(not isinstance(v,str) or len(v)>1000 or '\0' in v for v in row.values()):raise ValueError('Enter a name, description and native model for each route.')
            name=row.get('name','')
            previous=prior.get(name,{})
            if key=='models' and row.get('provider','')!=previous.get('provider','') and any(previous.get(k) for k in ('api_key','base_url','api_mode','fallback_providers')):raise ValueError('This route has its own connection settings. Change its provider in Hermes so its credentials stay with the right service.')
            if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,63}',name) or name in names:raise ValueError('Give each route a unique name using letters, numbers, hyphens or underscores.')
            if key=='models' and not row.get('description','').strip():raise ValueError('Describe when to use each model route.')
            if key=='models' and not row.get('model'):raise ValueError('Choose a model for each model route.')
            names.add(name);saved.append({**prior.get(name,{}),**row})
        chosen=requested.get(default,'')
        if not isinstance(chosen,str) or chosen and chosen not in names:raise ValueError('Choose a default from the listed routes, or leave it empty to inherit the main model.')
        block[entries]=saved;block['default']=chosen
    target=backends.get(mode,{})
    if mode!='default' and not target.get('options' if mode=='model_map' else 'profiles'):raise ValueError('Add a route before selecting this delegation mode.')
    updated['backend']=mode
    return updated


def reported(rows,overrides=None):
    from workspace_native_settings import options
    import hashlib,json
    fields=[]
    for row in rows:
        text=' '.join(str(row.get(k,'')) for k in ('id','name','category'))
        if row.get('type','select')!='select' or row.get('category') in {'model','mode','thought_level'} or not re.search(r'delegat|subagent|specialist',text,re.I):continue
        fields.append({'id':row['id'],'name':row.get('name') or row['id'],'group':'delegation','type':'select',
                       'options':list(options(row.get('options',[]))),'value':(overrides or {}).get(row['id'],row.get('currentValue'))})
    return {'fields':fields,'revision':hashlib.sha256(json.dumps(fields,sort_keys=True).encode()).hexdigest(),
            'scope':'This chat in its native AI app.','note':'' if fields else 'This connection does not report editable delegation settings. Native agent definitions and app defaults still apply.'}


if __name__=='__main__':
    try:native.main('delegation')
    except (OSError,ValueError) as error:raise SystemExit('Error: '+native.cli_error(error))
