"""Relationship-aware reconciliation for optional AURA work receipts.

Run lifecycle exists to preserve truthful organizational continuity. It reasons from
explicit Run relationships and material work already attached to those receipts. It does
not inspect host capability/provider state, and AttentionItems never become Run gates.
"""
from pathlib import Path
import json

from _common import iter_instance_objects, now, runtime_root, storage_ref, write_json_atomic


IGNORED_MECHANICAL_ARTIFACTS={'effective-preferences.json'}


def _json(path):
    try:return json.loads(Path(path).read_text(encoding='utf-8'))
    except Exception:return None


def _method_type(run):
    return run.get('method_type') or ('aura_playbook' if run.get('contract_id') else 'ad_hoc')


def _run_rows(business_id):
    root=runtime_root()/'runs'/business_id;rows={}
    if not root.exists():return rows
    for rp in root.glob('*/run.json'):
        run=_json(rp)
        if not isinstance(run,dict) or run.get('business_id')!=business_id or not run.get('run_id'):continue
        rd=rp.parent;manifest=_json(rd/'contract-execution.json')
        rows[run['run_id']]={
            'run':run,'manifest':manifest if isinstance(manifest,dict) else {},
            'run_path':rp,'manifest_path':rd/'contract-execution.json','run_dir':rd,
        }
    return rows


def _run_linked_objects(business_id,run_id):
    rr=f'runtime/runs/{business_id}/{run_id}';out=[]
    for obj,path in iter_instance_objects(business_id):
        ext=obj.get('extensions') if isinstance(obj.get('extensions'),dict) else {}
        bos=ext.get('businessos') if isinstance(ext.get('businessos'),dict) else {}
        lineage=obj.get('lineage') if isinstance(obj.get('lineage'),list) else []
        if bos.get('run_id')==run_id or bos.get('run_ref')==rr or run_id in lineage or rr in lineage:out.append((obj,path))
    return out


def _material_state(business_id,row):
    manifest=row['manifest'];material=[]
    if manifest.get('root_evidence_refs'):material.append('root completion evidence')
    for cid,step in (manifest.get('contracts') or {}).items():
        if step.get('status')!='pending' or step.get('evidence_refs'):material.append(f'playbook state for {cid}')
    linked=_run_linked_objects(business_id,row['run']['run_id'])
    if linked:material.append(f'{len(linked)} Run-linked canonical object(s)')
    artifacts=row['run_dir']/'artifacts'
    if artifacts.exists():
        files=[p for p in artifacts.rglob('*') if p.is_file() and p.name not in IGNORED_MECHANICAL_ARTIFACTS]
        if files:material.append(f'{len(files)} material Run artifact(s)')
    continuity=row['run'].get('continuity') if isinstance(row['run'].get('continuity'),dict) else {}
    if any(continuity.get(k) for k in ('summary','evidence_refs','result_refs','decision_refs','unresolved')):
        material.append('material organizational work receipt state')
    return material


def _run_role(run):return run.get('run_role') or ('support' if run.get('parent_run_id') else 'root')


def _same_job(left,right):
    return (
        all(left.get(key)==right.get(key) for key in ('business_id','contract_id','task','parent_run_id','method_ref'))
        and _method_type(left)==_method_type(right)
        and _run_role(left)==_run_role(right)
        and (left.get('focus_refs') or [])==(right.get('focus_refs') or [])
    )


def _summary(run,row,reasons=None,relationship=None):
    return {
        'run_id':run.get('run_id'),'run_ref':storage_ref(row['run_dir']),
        'method_type':_method_type(run),'method_ref':run.get('method_ref'),
        'contract_id':run.get('contract_id'),'task':run.get('task'),
        'relationship':relationship,'reasons':list(reasons or []),
    }


def _completed_exactly(row):
    run=row['run'];method=_method_type(run)
    if run.get('status')!='completed':return False
    if method!='aura_playbook':return not row['manifest']
    manifest=row['manifest']
    return bool(
        manifest
        and manifest.get('business_id')==run.get('business_id')
        and manifest.get('run_id')==run.get('run_id')
        and manifest.get('root_contract_id')==run.get('contract_id')
        and manifest.get('root_status')=='completed'
    )


def _empty_exact_replacement(row):
    run=row['run'];manifest=row['manifest'];method=_method_type(run)
    if run.get('status')!='active':return False
    if method=='aura_playbook':
        exact_state=bool(
            manifest
            and manifest.get('business_id')==run.get('business_id')
            and manifest.get('run_id')==run.get('run_id')
            and manifest.get('root_contract_id')==run.get('contract_id')
            and manifest.get('root_status')=='active'
        )
    else:
        exact_state=not manifest
    return exact_state


def reconcile_run_lifecycle(business_id,completed_run_id,apply_safe_supersession=False):
    """Classify related work receipts and safely supersede only exact empty replacements."""
    rows=_run_rows(business_id);target_row=rows.get(completed_run_id)
    empty={
        'completed_runs':[],'mechanically_redundant_runs':[],'mechanically_superseded_runs':[],
        'legitimately_active_runs':[],'needs_judgment':[],'mutation':'none',
    }
    if not target_row:
        return {'status':'needs_judgment','reason':f'Completed Run not found: {completed_run_id}',**empty}
    target=target_row['run'];target_root=target.get('root_run_id') or target.get('run_id');target_corr=target.get('correlation_id')
    if not _completed_exactly(target_row):
        return {
            'status':'needs_judgment',
            'reason':f'Run {completed_run_id} is not exactly completed for its actual method; reconciliation cannot mutate related Runs',
            **empty,
        }

    completed=[];redundant=[];active=[];judgment=[]
    for rid,row in sorted(rows.items()):
        run=row['run'];status=run.get('status')
        explicit_related=(run.get('root_run_id')==target_root or run.get('parent_run_id')==completed_run_id)
        correlation_related=bool(target_corr and run.get('correlation_id')==target_corr)
        same_task=run.get('task')==target.get('task')
        if status=='completed' and (rid==completed_run_id or explicit_related or correlation_related):
            completed.append(_summary(run,row,relationship='completed'))
        if rid==completed_run_id or status!='active':continue

        replacement=(target.get('supersedes_run_id')==rid or run.get('superseded_by_run_id')==completed_run_id)
        material=_material_state(business_id,row)
        if replacement:
            reasons=[]
            if not _same_job(target,run):reasons.append('replacement link does not identify the same exact method/task/focus')
            if not _empty_exact_replacement(row):reasons.append('replacement Run does not have the expected clean active state for its method')
            if material:reasons.extend(material)
            if not reasons:
                redundant.append(_summary(run,row,['explicit exact replacement relation; no material organizational work'],relationship='superseded_by_completed_run'))
            else:
                judgment.append(_summary(run,row,reasons,relationship='replacement_requires_judgment'))
            continue

        exact_parent=(target.get('parent_run_id')==rid)
        exact_family_root=bool(target.get('parent_run_id') and target_root==rid)
        if exact_parent or exact_family_root:
            relationship='exact_parent' if exact_parent else 'exact_family_root'
            reasons=material or ['Parent/root receipt remains active to compose completed support work and any other material work.']
            active.append(_summary(run,row,reasons,relationship=relationship))
            continue

        if explicit_related or correlation_related or same_task:
            relationship='explicit_support_or_sibling' if explicit_related else ('shared_correlation' if correlation_related else 'same_task_without_explicit_relationship')
            if material:
                active.append(_summary(run,row,material,relationship=relationship))
            else:
                judgment.append(_summary(run,row,['Related active Run has no conclusive completion or supersession relationship.'],relationship=relationship))
        else:
            active.append(_summary(run,row,['Independent active work receipt outside the completed Run relationship/correlation.'],relationship='independent'))

    superseded=[]
    if apply_safe_supersession:
        snapshots={}
        try:
            for item in redundant:
                row=rows[item['run_id']]
                for path in (row['run_path'],row['manifest_path']):
                    if path.exists():snapshots[path]=path.read_bytes()
                ts=now();run=dict(row['run']);manifest=dict(row['manifest'])
                run.update({'status':'superseded','superseded_by_run_id':completed_run_id,'updated_at':ts,'lifecycle_reason':'mechanically_redundant_exact_replacement'})
                continuity=dict(run.get('continuity') or {})
                if continuity:
                    continuity.update({'state':'superseded','superseded_by_run_id':completed_run_id});run['continuity']=continuity
                write_json_atomic(row['run_path'],run)
                if manifest:
                    manifest.update({'root_status':'superseded','superseded_by_run_id':completed_run_id,'updated_at':ts,'lifecycle_reason':'mechanically_redundant_exact_replacement'})
                    write_json_atomic(row['manifest_path'],manifest)
                superseded.append(item)
        except Exception as exc:
            for path,data in snapshots.items():path.write_bytes(data)
            judgment.extend({**item,'reasons':[f'Safe supersession transaction failed and was rolled back: {exc}']} for item in redundant)
            superseded=[]

    related_active=[x for x in active if x.get('relationship')!='independent']
    if judgment:status='needs_judgment'
    elif related_active:status='remaining_work'
    elif superseded:status='reconciled'
    elif redundant:status='safe_supersession_available'
    else:status='clean'
    return {
        'status':status,
        'completed_runs':completed or [_summary(target,target_row,relationship='completed')],
        'mechanically_redundant_runs':redundant,
        'mechanically_superseded_runs':superseded,
        'legitimately_active_runs':active,
        'needs_judgment':judgment,
        'mutation':'safe_exact_supersession_only' if superseded else 'none',
        'rule':'Run reconciliation uses explicit receipt relationships and material work only. Runtime capability state and AttentionItems never become AURA execution gates.',
    }
