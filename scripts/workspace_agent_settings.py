"""Native delegation preferences; no Aura routing or scheduling loop."""
import re

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
    return result


def save(command,kind,cwd,env,changes,revision,profile=None):
    # describe() must use the identical shape/revision as native.save().
    return native.save(command,kind,cwd,env,changes,revision,FIELDS.get(kind,[]),profile)


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
