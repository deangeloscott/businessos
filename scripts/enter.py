#!/usr/bin/env python3
"""Establish a governed AURA execution envelope for ordinary organization/business work.

This is deliberately not an agent, harness, scheduler, model router, or workflow engine.
A capable agent/harness decides whether the user's request is organizational work. Once
that boundary is crossed, this helper makes the reliability mechanics deterministic:
workspace/business resolution, routing, Run creation/recovery, process/context planning,
capability preflight, and lightweight monitoring-continuity visibility. The agent then
performs the actual business work using the returned envelope and whatever authorized host
capabilities are available.
"""
from pathlib import Path
import argparse, json, os, shlex, subprocess, sys

from _common import PRODUCT_ROOT, workspace_root, runtime_root, storage_ref, resolve_business, write_json_atomic
from route_and_resolve import route_and_resolve
from process_plan import build_process_plan
from context_plan import build_plan
from preflight_capabilities import preflight
from list_due_monitoring import summarize as summarize_monitoring


PERSISTENCE_MECHANICAL_FIELDS={'id','object_type','schema_version','business_id','created_at','updated_at','lineage','owner_system','producer_system','requesting_system','observed_at'}
SPECIALIZED_PERSISTENCE={
    'AttentionItem':'scripts/upsert_attention.py','PlatformChange':'scripts/record_platform_change.py',
    'SourceRecord':'scripts/persist_research_bundle.py','PreferenceProfile':'scripts/upsert_preference_profile.py',
    'Business':'scripts/bootstrap_explicit_context.py','Brand':'scripts/bootstrap_explicit_context.py','BusinessClaim':'scripts/bootstrap_explicit_context.py',
}


def _semantic_requirements(object_types):
    registry=json.loads((PRODUCT_ROOT/'generated/schema-registry.json').read_text());by_title={row.get('title'):row for row in registry}
    out={}
    for typ in object_types:
        row=by_title.get(typ)
        if not row:continue
        schema=json.loads((PRODUCT_ROOT/row['path']).read_text())
        out[typ]=[field for field in schema.get('required',[]) if field not in PERSISTENCE_MECHANICAL_FIELDS]
    return out


def _matching_active_runs(business_id,contract_id,task):
    root=runtime_root()/'runs'/business_id
    if not root.exists():return []
    rows=[]
    for rp in root.glob('*/run.json'):
        try:d=json.loads(rp.read_text())
        except Exception:continue
        if d.get('status')!='active':continue
        if d.get('business_id')!=business_id or d.get('contract_id')!=contract_id or d.get('task')!=task:continue
        rows.append((d.get('updated_at') or d.get('created_at') or '',d.get('run_id'),rp))
    return sorted(rows,reverse=True)


def _create_run(business_id,contract_id,task,operator_ref=None,team_ref=None,role_ref=None,output_type=None,channel=None,task_preferences=None):
    cmd=[sys.executable,str(PRODUCT_ROOT/'scripts/create_run.py'),business_id,contract_id,task]
    for flag,value in [('--operator-ref',operator_ref),('--team-ref',team_ref),('--role-ref',role_ref),('--output-type',output_type),('--channel',channel),('--task-preferences',task_preferences)]:
        if value is not None:cmd.extend([flag,str(value)])
    p=subprocess.run(cmd,cwd=PRODUCT_ROOT,capture_output=True,text=True)
    if p.returncode!=0:raise ValueError((p.stderr or p.stdout or 'Run creation failed').strip())
    rid=p.stdout.strip().splitlines()[-1].strip()
    if not rid.startswith('run_'):raise ValueError(f'Unexpected Run creation output: {p.stdout!r}')
    return rid


def _monitoring_continuity(business_id):
    try:
        data=summarize_monitoring(business_id)
        return {
            'status':'available',
            'tracked_subject_count':data.get('tracked_subject_count',0),
            'due_unbound_count':data.get('due_unbound_count',0),
            'due_unbound_subjects':data.get('due_unbound_subjects',[]),
            'environment':data.get('environment'),
            'rule':'Do not derail an unrelated request to clear a monitoring backlog. Refresh overdue work when relevant/authorized or surface one concise notice when it materially matters. A saved cadence/next check is not an active schedule without a verified scheduler binding.'
        }
    except (ValueError,json.JSONDecodeError) as e:
        return {
            'status':'degraded',
            'reason':str(e),
            'rule':'Monitoring-continuity inspection must not fabricate schedule state or silently block otherwise valid organizational work.'
        }


def _conditional_processes(node,parent=None):
    out=[]
    for row in node.get('conditional',[]) or []:
        child=row.get('process') or {}
        out.append({'parent_contract_id':node.get('contract_id') or parent,'when':row.get('when'),'contract_id':child.get('contract_id'),'owner_system':child.get('owner_system')})
        out.extend(_conditional_processes(child,node.get('contract_id')))
    for child in node.get('required',[]) or []:out.extend(_conditional_processes(child,node.get('contract_id')))
    return out


def _capability_summary(preflight):
    def small(row):
        return {k:row.get(k) for k in ('capability','execution_state','decision_required','next_action','fallback_if_not_authorized') if row.get(k) is not None}
    required=[small(x) for x in preflight.get('required',[]) or []]
    optional=[small(x) for x in preflight.get('optional',[]) or []]
    material_states={'provider_discovery','local_capability_discovery','provider_decision','manual_or_assisted_fallback'}
    host=preflight.get('host_discovery') or {}
    return {
        'status':preflight.get('status'),'environment':preflight.get('environment'),'automated_ready':preflight.get('automated_ready'),
        'required':required,
        'required_gaps':[x for x in required if x.get('execution_state')!='available'],
        'optional_available':[x.get('capability') for x in optional if x.get('execution_state')=='available'],
        'optional_gaps':[x for x in optional if x.get('execution_state') in material_states],
        'host_discovery':{k:host.get(k) for k in ('completed','policy') if host.get(k) is not None},
    }


def compact_handoff(envelope):
    """Project the durable full envelope into the ordinary agent-facing handoff."""
    if envelope.get('status')!='ready':return envelope
    process=envelope.get('process_plan') or {};context=envelope.get('context_plan') or {};run=envelope.get('run') or {}
    manifest_path=runtime_root()/'runs'/envelope['business_id']/run['run_id']/'contract-execution.json'
    try:manifest=json.loads(manifest_path.read_text())
    except Exception:manifest={}
    required=[]
    for cid in manifest.get('required_subcontracts',[]) or []:
        step=(manifest.get('contracts') or {}).get(cid) or {};spec=step.get('completion_evidence_spec') or {}
        required.append({'contract_id':cid,'status':step.get('status'),'evidence_profile':spec.get('profile'),'declared_write_types':spec.get('declared_write_types',[]),'strict_qa_target':spec.get('strict_qa_target',False)})
    root_spec=manifest.get('root_completion_evidence_spec') or {}
    allowed_write_types=sorted(set(root_spec.get('declared_write_types',[])).union(*(set(x.get('declared_write_types',[])) for x in required)))
    supported_write_types=[typ for typ in allowed_write_types if typ not in SPECIALIZED_PERSISTENCE]
    workspace_arg=shlex.quote(str(envelope.get('workspace')))
    route=envelope.get('route') or {}
    object_files=context.get('object_files',[]) or [];schema_files=context.get('schema_files',[]) or []
    classified=set(object_files)|set(schema_files)
    return {
        'format_version':'1.2','handoff_format':'compact','status':'ready',
        'workspace':envelope.get('workspace'),'business_id':envelope.get('business_id'),'business_resolution':envelope.get('business_resolution'),
        'original_request':envelope.get('original_request'),
        'authority':{
            'status':'resolved_authoritative_handoff',
            'resolved_surfaces':['route','process','context','capabilities','run'],
            'rule':'Use these resolved results as authoritative for this Run. Do not rerun context_plan.py, process_plan.py, preflight_capabilities.py, inspect their source, or use their --help during ordinary execution. Re-enter only if relevant workspace/Run/capability state materially changed or a high-level interface below reports a real unresolved need.'
        },
        'root_contract':{'contract_id':route.get('contract_id'),'owner_system':route.get('owner_system'),'path':route.get('path'),'reason':route.get('reason'),'declared_write_types':root_spec.get('declared_write_types',[])},
        'run':run,
        'process':{
            'entry_contract':process.get('entry_contract'),
            'required_execution_order':process.get('required_execution_order',[]),
            'conditional_processes':_conditional_processes(process.get('tree') or {}),
            'required_subcontracts':required,
        },
        'context':{
            'contract_and_policy_refs':[x for x in context.get('files',[]) if x not in classified],
            'object_refs':context.get('object_refs',[]),'object_files':object_files,'schema_files':schema_files,
            'unresolved_selectors':context.get('unresolved_selectors',[]),
            'optional_unavailable_selectors':context.get('optional_unavailable_selectors',[]),
        },
        'inputs':context.get('material_inputs') or {'declared_evidence_inputs':context.get('evidence_inputs',[]),'canonical_inputs':[],'supplied_evidence_refs':[]},
        'capabilities':_capability_summary(envelope.get('capability_preflight') or {}),
        'monitoring_continuity':envelope.get('monitoring_continuity'),
        'execution_env':envelope.get('execution_env'),
        'instructions':envelope.get('agent_handoff'),
        'persistence':{
            'interface':'scripts/persist_run_results.py',
            'command':f"python3 scripts/persist_run_results.py {envelope['business_id']} {run['run_id']} --workspace {workspace_arg} --input <results-json-in-work-dir>",
            'allowed_object_types':allowed_write_types,
            'supported_object_types':supported_write_types,
            'required_semantic_fields':_semantic_requirements(supported_write_types),
            'specialized_interfaces':{typ:interface for typ,interface in SPECIALIZED_PERSISTENCE.items() if typ in allowed_write_types},
            'input_shape':{'objects':[{'key':'local-label','object_type':'one supported_object_type','content':'AI-authored semantic fields only','lineage_refs':['existing_object_ref or @local-label']}]},
            'rule':'The model decides all business meaning. This interface only validates and wraps supplied semantic content with schema identity, IDs, timestamps, storage location, local-reference resolution, and Run/contract provenance; it returns focused pre-finalization validation and never invents an Opportunity, Action, WorkRequest, Insight, or other result.'
        },
        'completion':{
            'interface':'scripts/finalize_run.py',
            'command':f"python3 scripts/finalize_run.py {envelope['business_id']} {run['run_id']} --workspace {workspace_arg}",
            'rule':'Persist the real material results first, then call this interface directly. Do not run whole-business validation while the Run is active and do not invoke lower-level completion validators/helpers separately. Finalization reports genuine pre-finalization object/evidence issues while deferring only completion conditions caused by the active Run; semantic or ambiguous evidence returns needs_judgment and leaves the Run incomplete.'
        },
        'execution_envelope_ref':envelope.get('execution_envelope_ref'),
    }
def enter(task,business_id=None,workspace=None,operator_ref=None,team_ref=None,role_ref=None,output_type=None,channel=None,task_preferences=None,new_run=False,include_optional_capabilities=True):
    task=(task or '').strip()
    if not task:return {'format_version':'1.0','status':'needs_input','missing':['request'],'reason':'Preserve and provide the user\'s original organizational request.'}
    if workspace:
        os.environ['BUSINESSOS_WORKSPACE']=str(Path(workspace).expanduser().resolve())
    resolved=resolve_business(business_id)
    if resolved['status']!='resolved':
        return {'format_version':'1.0','status':'needs_input','workspace':str(workspace_root()),**{k:v for k,v in resolved.items() if k!='status'}}
    bid=resolved['business_id']
    continuity=_monitoring_continuity(bid)
    try:route=route_and_resolve(task,bid,team_ref,role_ref,operator_ref)
    except ValueError as e:return {'format_version':'1.0','status':'blocked','business_id':bid,'workspace':str(workspace_root()),'monitoring_continuity':continuity,'reason':str(e)}
    cid=route.get('contract_id')
    if not cid or route.get('status')!='available':
        return {'format_version':'1.0','status':'blocked','business_id':bid,'workspace':str(workspace_root()),'original_request':task,'route':route,'monitoring_continuity':continuity,'reason':'AURA did not resolve an available business-work entry contract.'}

    matches=[] if new_run else _matching_active_runs(bid,cid,task)
    if matches:
        rid=matches[0][1];resumed=True
    else:
        try:rid=_create_run(bid,cid,task,operator_ref,team_ref,role_ref,output_type,channel,task_preferences);resumed=False
        except ValueError as e:return {'format_version':'1.0','status':'blocked','business_id':bid,'workspace':str(workspace_root()),'original_request':task,'route':route,'monitoring_continuity':continuity,'reason':str(e)}

    run_dir=runtime_root()/'runs'/bid/rid
    work_dir=run_dir/'work';work_dir.mkdir(parents=True,exist_ok=True)
    try:
        process=build_process_plan(contract_id=cid)
        context=build_plan(bid,cid,operator_ref=operator_ref,team_ref=team_ref,role_ref=role_ref,run_id=rid)
        capabilities=preflight(bid,cid,include_optional=include_optional_capabilities)
    except (ValueError,json.JSONDecodeError) as e:
        return {'format_version':'1.0','status':'blocked','business_id':bid,'workspace':str(workspace_root()),'original_request':task,'route':route,'monitoring_continuity':continuity,'run_id':rid,'run_ref':storage_ref(run_dir),'reason':str(e)}

    env={
        'BUSINESSOS_WORKSPACE':str(workspace_root()),
        'BUSINESSOS_BUSINESS_ID':bid,
        'BUSINESSOS_RUN_ID':rid,
        'BUSINESSOS_CONTRACT_ID':cid,
        'BUSINESSOS_WORK_DIR':str(work_dir),
    }
    envelope={
        'format_version':'1.1',
        'status':'ready',
        'workspace':str(workspace_root()),
        'business_id':bid,
        'business_resolution':resolved.get('resolution'),
        'original_request':task,
        'route':route,
        'monitoring_continuity':continuity,
        'run':{
            'run_id':rid,
            'resumed':resumed,
            'run_ref':storage_ref(run_dir),
            'work_dir':str(work_dir),
            'work_ref':storage_ref(work_dir),
        },
        'process_plan':process,
        'context_plan':context,
        'capability_preflight':capabilities,
        'execution_env':env,
        'agent_handoff':{
            'instruction':'Continue the user\'s complete original request inside this AURA Run. Use the resolved context/process and authorized host Skills/tools as executors; do not replace AURA routing, business truth, authorization, evidence, canonical state, required subcontracts, QA, completion, or Learning.',
            'resolution_rule':'The returned route, process, context, capability preflight, and Run are authoritative for this execution. Do not recompute or inspect the helpers that produced them unless relevant state materially changed or a returned high-level interface identifies a real unresolved need.',
            'scratch_rule':'Use the Run work_dir for build/cache/render/temp state. The AURA product root remains read-only during ordinary business operation.',
            'persistence_rule':'Persist only material organizational evidence, findings, decisions, governed Assets/state, completion evidence, and evidence-supported Learning; ordinary scratch/tool internals remain working state. Prefer the compact handoff persistence interface for Run results instead of reading schemas/writer/provenance source or hand-authoring canonical scaffolding.',
            'continuity_rule':'Use monitoring_continuity as a lightweight memory cue, not a competing task queue. If overdue unbound monitoring is relevant to this request, refresh it through the appropriate AURA process. If it materially matters but is unrelated, surface at most one concise notice. Otherwise continue the user\'s request. Never describe planned cadence as an active schedule without a verified scheduler binding.',
            'human_ux_rule':'In the final response, describe saved work using the organization/human knowledge concept first. Raw canonical/runtime filesystem paths are optional advanced inspection details, not the primary UX.'
        },
    }
    envelope_path=run_dir/'artifacts'/'execution-envelope.json'
    envelope['execution_envelope_ref']=storage_ref(envelope_path)
    write_json_atomic(envelope_path,envelope)
    return envelope


def main():
    p=argparse.ArgumentParser(description='Enter AURA for an ordinary organization/business request and return a governed execution envelope. This helper is not for unrelated personal tasks or AURA product-development work.')
    p.add_argument('request',help='The user\'s complete original natural-language organizational request')
    p.add_argument('--business-id')
    p.add_argument('--workspace',help='Optional organization workspace root; otherwise use configured BUSINESSOS_WORKSPACE/workspace link')
    p.add_argument('--operator-ref');p.add_argument('--team-ref');p.add_argument('--role-ref')
    p.add_argument('--output-type');p.add_argument('--channel');p.add_argument('--task-preferences')
    p.add_argument('--new-run',action='store_true',help='Force a new Run instead of resuming an exact active business+contract+request match')
    p.add_argument('--required-only-capabilities',action='store_true',help='Skip optional capability checks in the returned preflight')
    p.add_argument('--full',action='store_true',help='Print the complete durable execution envelope instead of the compact ordinary agent handoff')
    a=p.parse_args()
    out=enter(a.request,a.business_id,a.workspace,a.operator_ref,a.team_ref,a.role_ref,a.output_type,a.channel,a.task_preferences,a.new_run,not a.required_only_capabilities)
    shown=out if a.full else compact_handoff(out)
    print(json.dumps(shown,indent=2)+'\n',end='')
    raise SystemExit(0 if out.get('status')=='ready' else 2)


if __name__=='__main__':main()
