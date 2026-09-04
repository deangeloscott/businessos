#!/usr/bin/env python3
from _common import *
import argparse, copy, fnmatch, json, os
from preference_semantics import validate_preference_semantics

SCOPE_RANK={'business':0,'team':1,'role':2,'operator':3}


def _matches_pattern(value, patterns):
    if not patterns:
        return True
    if value is None:
        return False
    return any(fnmatch.fnmatchcase(value, p) for p in patterns)


def _profile_applies(profile, system=None, workflow=None, output_type=None, channel=None):
    a=profile.get('applies_to') or {}
    return (
        _matches_pattern(system, a.get('systems') or []) and
        _matches_pattern(workflow, a.get('workflows') or []) and
        _matches_pattern(output_type, a.get('output_types') or []) and
        _matches_pattern(channel, a.get('channels') or [])
    )


def _subject_matches(profile,business_id,team_ref=None,role_ref=None,operator_ref=None):
    scope=profile.get('scope'); subject=profile.get('subject_ref')
    if scope=='business': return subject in {business_id, f'biz_{business_id}'}
    if scope=='team': return bool(team_ref) and subject==team_ref
    if scope=='role': return bool(role_ref) and subject==role_ref
    if scope=='operator': return bool(operator_ref) and subject==operator_ref
    return False


def _leaf_items(obj,prefix=''):
    for k,v in obj.items():
        path=f'{prefix}.{k}' if prefix else k
        if isinstance(v,dict):
            yield from _leaf_items(v,path)
        else:
            yield path,v


def _assign_path(root,path,value):
    parts=path.split('.')
    cur=root
    for p in parts[:-1]:
        nxt=cur.get(p)
        if not isinstance(nxt,dict):
            nxt={};cur[p]=nxt
        cur=nxt
    cur[parts[-1]]=copy.deepcopy(value)


def _load_profiles(business_id):
    out=[]
    for obj,path in iter_instance_objects(business_id):
        if obj.get('object_type')=='PreferenceProfile' and obj.get('status')=='active':
            validate_preference_semantics(obj.get('preferences') or {}, f'{path.relative_to(ROOT)}.preferences')
            out.append((obj,path))
    return out


def resolve_effective_preferences(business_id,operator_ref=None,team_ref=None,role_ref=None,system=None,workflow=None,output_type=None,channel=None,task_preferences=None,fail_on_conflict=True):
    if not (ROOT/'instances'/business_id).exists():
        raise ValueError('Unknown business')
    candidates=[]
    for profile,path in _load_profiles(business_id):
        if not _subject_matches(profile,business_id,team_ref,role_ref,operator_ref): continue
        if not _profile_applies(profile,system,workflow,output_type,channel): continue
        candidates.append((profile,path))
    candidates.sort(key=lambda x:(SCOPE_RANK[x[0]['scope']],int(x[0].get('priority',0)),x[0]['id']))
    effective={}; sources={}; meta={}; conflicts=[]; applied=[]
    for profile,path in candidates:
        rank=SCOPE_RANK[profile['scope']];priority=int(profile.get('priority',0))
        applied.append({'id':profile['id'],'scope':profile['scope'],'subject_ref':profile['subject_ref'],'priority':priority,'path':str(path.relative_to(ROOT))})
        for leaf,value in _leaf_items(profile.get('preferences') or {}):
            prev=meta.get(leaf)
            if prev and prev['rank']==rank and prev['priority']==priority and prev['value']!=value:
                conflicts.append({
                    'path':leaf,
                    'precedence':{'scope':profile['scope'],'priority':priority},
                    'first_profile':prev['profile_id'],'first_value':prev['value'],
                    'second_profile':profile['id'],'second_value':value
                })
                continue
            if not prev or (rank,priority) >= (prev['rank'],prev['priority']):
                _assign_path(effective,leaf,value)
                sources[leaf]={'source_type':'PreferenceProfile','profile_id':profile['id'],'scope':profile['scope'],'priority':priority}
                meta[leaf]={'rank':rank,'priority':priority,'profile_id':profile['id'],'value':copy.deepcopy(value)}
    if task_preferences:
        for leaf,value in _leaf_items(task_preferences):
            _assign_path(effective,leaf,value)
            sources[leaf]={'source_type':'task_preference','scope':'task'}
            meta[leaf]={'rank':4,'priority':0,'profile_id':None,'value':copy.deepcopy(value)}
    result={
        'format_version':'1.0',
        'business_id':business_id,
        'context':{'operator_ref':operator_ref,'team_ref':team_ref,'role_ref':role_ref,'system':system,'workflow':workflow,'output_type':output_type,'channel':channel},
        'precedence':['business','team','role','operator','task'],
        'boundary':'Preferences customize otherwise-valid choices. They do not override explicit user instructions, established organization truth, legal/compliance requirements, or real external permissions, and they do not authorize actions.',
        'applied_profiles':applied,
        'effective_preferences':effective,
        'leaf_sources':sources,
        'conflicts':conflicts,
    }
    if conflicts and fail_on_conflict:
        details='; '.join(f"{c['path']} ({c['first_profile']} vs {c['second_profile']})" for c in conflicts)
        raise ValueError('Unresolved equal-precedence preference conflict(s): '+details)
    return result


def _load_task_preferences(path):
    if not path:return None
    p=Path(path); p=p if p.is_absolute() else ROOT/p
    if not p.exists(): raise ValueError(f'Task preferences file not found: {path}')
    data=json.loads(p.read_text())
    if not isinstance(data,dict): raise ValueError('Task preferences must be a JSON object')
    validate_preference_semantics(data, 'task_preferences')
    return data


def _run_context(business_id,run_id):
    if not run_id:return None,None
    rp=ROOT/'runtime/runs'/business_id/run_id/'run.json'
    if not rp.exists(): raise ValueError(f'Unknown Run: {run_id}')
    run=json.loads(rp.read_text())
    if run.get('business_id')!=business_id: raise ValueError('Run business_id mismatch')
    return run,rp


def resolve_for_run(business_id,run_id,task_preferences=None,output_type=None,channel=None):
    run,rp=_run_context(business_id,run_id)
    snapref=run.get('preference_snapshot_ref');out=(ROOT/snapref) if snapref else (rp.parent/'artifacts'/'effective-preferences.json')
    if out.exists():
        if task_preferences is not None: raise ValueError('existing Run preference snapshot is immutable; task preferences must be supplied when creating the Run')
        return json.loads(out.read_text()),out
    result=resolve_effective_preferences(
        business_id,
        operator_ref=run.get('operator_ref'),team_ref=run.get('team_ref'),role_ref=run.get('role_ref'),
        system=(load_registry_workflow(run.get('workflow_id')) or {}).get('owner_system'),
        workflow=run.get('workflow_id'),output_type=run.get('preference_output_type') if output_type is None else output_type,channel=run.get('preference_channel') if channel is None else channel,
        task_preferences=task_preferences,
    )
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2)+'\n')
    run['preference_snapshot_ref']=out.relative_to(ROOT).as_posix();run['updated_at']=now()
    rp.write_text(json.dumps(run,indent=2)+'\n')
    return result,out


def load_registry_workflow(workflow_id):
    if not workflow_id:return None
    return next((x for x in load_registry().get('workflows',[]) if x.get('id')==workflow_id),None)


def main():
    p=argparse.ArgumentParser(description='Resolve effective AURA preferences. Preferences guide otherwise-valid choices; they do not authorize actions or constrain model judgment.')
    p.add_argument('business_id');p.add_argument('--operator-ref');p.add_argument('--team-ref');p.add_argument('--role-ref')
    p.add_argument('--system');p.add_argument('--workflow');p.add_argument('--output-type');p.add_argument('--channel')
    p.add_argument('--task-preferences',help='JSON object file containing one-task optional preference overrides')
    p.add_argument('--run-id',help='Use operator/team/role/Workflow context from an existing optional Run receipt and write a run-local effective-preference snapshot')
    p.add_argument('--output')
    a=p.parse_args()
    try:
        task=_load_task_preferences(a.task_preferences)
        if a.run_id:
            run,rp=_run_context(a.business_id,a.run_id)
            for supplied,stored,label in [(a.operator_ref,run.get('operator_ref'),'operator_ref'),(a.team_ref,run.get('team_ref'),'team_ref'),(a.role_ref,run.get('role_ref'),'role_ref')]:
                if supplied is not None and supplied!=stored: raise ValueError(f'{label} cannot override an existing Run attribution')
            if a.workflow is not None and a.workflow!=run.get('workflow_id'): raise ValueError('workflow cannot override an existing Run Workflow context')
            for supplied,stored,label in [(a.output_type,run.get('preference_output_type'),'output_type'),(a.channel,run.get('preference_channel'),'channel')]:
                if supplied is not None and supplied!=stored: raise ValueError(f'{label} cannot override an existing Run preference context')
            snapref=run.get('preference_snapshot_ref');out=(ROOT/snapref) if snapref else (rp.parent/'artifacts'/'effective-preferences.json')
            if out.exists():
                if task is not None: raise ValueError('existing Run preference snapshot is immutable; task preferences must be supplied when creating the Run')
                result=json.loads(out.read_text())
            else:
                workflow=run.get('workflow_id');rw=load_registry_workflow(workflow);system=a.system or ((rw or {}).get('owner_system'))
                result=resolve_effective_preferences(a.business_id,run.get('operator_ref'),run.get('team_ref'),run.get('role_ref'),system,workflow,run.get('preference_output_type'),run.get('preference_channel'),task)
                out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,indent=2)+'\n')
                run['preference_snapshot_ref']=out.relative_to(ROOT).as_posix();run['updated_at']=now();rp.write_text(json.dumps(run,indent=2)+'\n')
        else:
            operator=a.operator_ref or os.environ.get('BUSINESSOS_OPERATOR_REF')
            team=a.team_ref or os.environ.get('BUSINESSOS_TEAM_REF');role=a.role_ref or os.environ.get('BUSINESSOS_ROLE_REF')
            result=resolve_effective_preferences(a.business_id,operator,team,role,a.system,a.workflow,a.output_type,a.channel,task)
            out=None
        text=json.dumps(result,indent=2)+'\n'
        if a.output:
            op=Path(a.output);op=op if op.is_absolute() else ROOT/op;op.parent.mkdir(parents=True,exist_ok=True);op.write_text(text);print(op)
        else: print(text,end='')
        if out: print(f'preference_snapshot_ref={out.relative_to(ROOT).as_posix()}')
    except (ValueError,json.JSONDecodeError) as e: raise SystemExit(str(e))

if __name__=='__main__':main()
