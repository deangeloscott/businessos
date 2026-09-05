#!/usr/bin/env python3
"""Maintainer-side controller for blind AURA business-work qualification.

The candidate receives only the staged AURA product, organization workspace, and
ordinary business request. The controller observes what materially changed; it does
not require the candidate to create a particular Run/workflow ledger to count as work.
"""
from pathlib import Path
import argparse,json
from common import now,read_json,snapshot_diff,write_json
from checkpoint import capture_checkpoint
from release_fixture import release_event

VALID_BLOCKERS={'external_capability','external_authority','missing_required_data','external_service','qualification_fixture','no_material_result'}
ARTIFACT_SUFFIXES={'.md','.txt','.html','.htm','.pdf','.docx','.pptx','.xlsx','.csv','.png','.jpg','.jpeg','.webp','.gif','.svg','.mp3','.wav','.m4a','.mp4','.mov','.webm'}
ARTIFACT_DIR_MARKERS={'assets','artifacts','deliverables','drafts','reports','outputs','output'}

def _load(run_dir):
    rd=Path(run_dir).expanduser().resolve();run=read_json(rd/'run.json');queue=read_json(rd/'evaluator/queue.json')
    if not isinstance(run,dict) or not isinstance(queue,dict) or not isinstance(queue.get('events'),list):raise SystemExit(f'Not a prepared AURA qualification run: {rd}')
    return rd,run,queue

def _receipt_path(rd,event):return rd/event.get('receipt_path',f"evaluator/receipts/{event['event_id']}.json")

def classify(rd,event):
    eid=event['event_id'];before=rd/'checkpoints'/eid/'before.json';after=rd/'checkpoints'/eid/'after.json';receipt=_receipt_path(rd,event);state='terminal' if after.exists() and receipt.exists() else ('in_progress' if before.exists() or after.exists() or receipt.exists() else 'pending')
    return {'event_id':eid,'business_id':event.get('business_id'),'lane':event.get('lane'),'state':state,'before_checkpoint':before.exists(),'after_checkpoint':after.exists(),'controller_receipt':receipt.exists(),'receipt_path':str(receipt)}
def rows(rd,queue):return [classify(rd,e) for e in queue['events']]
def _event(rd,queue,event_id=None,prefer_in_progress=False):
    states=rows(rd,queue)
    if event_id:
        for event,state in zip(queue['events'],states):
            if event.get('event_id')==event_id:return event,state
        raise SystemExit(f'Unknown evaluator event: {event_id}')
    if prefer_in_progress:
        for event,state in zip(queue['events'],states):
            if state['state']=='in_progress':return event,state
    for event,state in zip(queue['events'],states):
        if state['state']!='terminal':return event,state
    return None,None

def _changed_objects(before,after):
    b={x.get('id'):x.get('sha256') for x in (before or {}).get('objects',[]) if x.get('id')};return [x for x in (after or {}).get('objects',[]) if x.get('id') and b.get(x.get('id'))!=x.get('sha256')]
def _changed_runs(before,after):
    b={x.get('run_id'):(x.get('status'),x.get('method_type'),x.get('method_ref'),x.get('workflow_id')) for x in (before or {}).get('runs',[]) if x.get('run_id')};out=[]
    for row in (after or {}).get('runs',[]):
        rid=row.get('run_id')
        if rid and b.get(rid)!=(row.get('status'),row.get('method_type'),row.get('method_ref'),row.get('workflow_id')):out.append(row)
    return out

def _asset_location_refs(workspace,changed_objects):
    refs=[]
    for row in changed_objects:
        if row.get('object_type')!='Asset' or not row.get('path'):continue
        data=read_json(workspace/row['path']);values=data if isinstance(data,list) else [data]
        for obj in values:
            if not isinstance(obj,dict) or obj.get('id')!=row.get('id') or obj.get('object_type')!='Asset':continue
            ref=obj.get('location_reference')
            if isinstance(ref,str) and ref.strip() and ref not in refs:refs.append(ref.strip())
    return refs

def _changed_workspace_paths(before,after):
    diff=snapshot_diff((before or {}).get('workspace',{}),(after or {}).get('workspace',{}));return diff.get('created',[])+diff.get('modified',[])
def _run_refs(workspace,business_id,changed_runs):
    result_refs=[];evidence_refs=[];observations=[]
    for row in changed_runs:
        rid=row.get('run_id')
        if not rid:continue
        data=read_json(workspace/'runtime'/'runs'/business_id/rid/'run.json',{}) or {};cont=data.get('continuity') or {}
        for ref in cont.get('result_refs') or []:
            if isinstance(ref,str) and ref not in result_refs:result_refs.append(ref)
        for ref in cont.get('evidence_refs') or []:
            if isinstance(ref,str) and ref not in evidence_refs:evidence_refs.append(ref)
        observations.append({'run_id':rid,'status':data.get('status'),'method_type':data.get('method_type'),'method_ref':data.get('method_ref'),'workflow_id':data.get('workflow_id')})
    return result_refs,evidence_refs,observations

def _looks_like_artifact(rel):
    p=Path(str(rel).replace('\\','/'));parts={x.lower() for x in p.parts};s=str(rel).replace('\\','/').lower()
    if s.startswith('attachments/supplied/') or s.startswith('runtime/') or '/intelligence/sources/' in s or '/evidence/' in s:return False
    if p.suffix.lower() not in ARTIFACT_SUFFIXES:return False
    return bool(parts&ARTIFACT_DIR_MARKERS) or not s.startswith('instances/')
def _existing_refs(refs,workspace):
    out=[];ws=workspace.resolve()
    for ref in refs:
        p=Path(ref).expanduser();p=p if p.is_absolute() else workspace/p
        if p.exists() and p.is_file() and p.stat().st_size>0:
            rp=p.resolve()
            try:norm=rp.relative_to(ws).as_posix()
            except ValueError:norm=str(rp)
            if norm not in out:out.append(norm)
    return out

def _candidate_response_ref(rd,event):
    rel=f"evaluator/candidate-responses/{event['event_id']}.txt";p=rd/rel
    if not p.is_file():return None
    try:
        if not p.read_text(encoding='utf-8',errors='replace').strip():return None
    except OSError:return None
    return rel

def derive_receipt(rd,run,event,blocker_classification=None,blocker_detail=None):
    eid=event['event_id'];workspace=Path(run['workspace']);before=read_json(rd/'checkpoints'/eid/'before.json',{}) or {};after=read_json(rd/'checkpoints'/eid/'after.json',{}) or {};changed_objects=_changed_objects(before,after);changed_runs=_changed_runs(before,after);changed_paths=_changed_workspace_paths(before,after);run_results,run_evidence,method_observations=_run_refs(workspace,event['business_id'],changed_runs);artifact_refs=[]
    candidate_artifact_refs=[ref for ref in run_results if _looks_like_artifact(ref)]+_asset_location_refs(workspace,changed_objects)+[p for p in changed_paths if _looks_like_artifact(p)]
    for ref in candidate_artifact_refs:
        if isinstance(ref,str) and ref not in artifact_refs:artifact_refs.append(ref)
    artifact_refs=_existing_refs(artifact_refs,workspace);canonical_refs=[];source_refs=[]
    for obj in changed_objects:
        path=obj.get('path')
        if not isinstance(path,str):continue
        if path not in canonical_refs:canonical_refs.append(path)
        if obj.get('object_type')=='SourceRecord' and path not in source_refs:source_refs.append(path)
    field_refs=[]
    for path in changed_paths+run_evidence:
        normalized=str(path).replace('\\','/')
        if normalized.startswith('attachments/supplied/'):continue
        if normalized.startswith('attachments/') or '/intelligence/sources/' in normalized or '/evidence/' in normalized:
            if normalized not in field_refs:field_refs.append(normalized)
    release_audit=read_json(rd/'evaluator'/'releases'/f'{eid}.json',{}) or {};released_refs=[];released=release_audit.get('released_path')
    if isinstance(released,str):
        try:released_refs.append(Path(released).resolve().relative_to(workspace.resolve()).as_posix())
        except ValueError:released_refs.append(released)
    response_ref=_candidate_response_ref(rd,event);material_result=bool(canonical_refs or artifact_refs or response_ref);blocker=None
    if blocker_classification:
        if blocker_classification not in VALID_BLOCKERS:raise SystemExit('Invalid blocker classification: '+blocker_classification)
        blocker={'classification':blocker_classification,'detail':blocker_detail or 'A genuinely required condition was unavailable during the business task.'};status='blocked'
    elif material_result:status='completed'
    else:status='blocked';blocker={'classification':'no_material_result','detail':'The controller observed no material business result in the candidate response, persisted organization state, or usable deliverables.'}
    receipt={'format_version':'3.0','generated_by':'qualification_controller','generated_at':now(),'event_id':eid,'business_id':event['business_id'],'status':status,'material_result_observed':material_result,'candidate_response_ref':response_ref,'work_run_ids':[x.get('run_id') for x in method_observations if x.get('run_id')],'method_observations':method_observations,'artifact_refs':artifact_refs,'canonical_refs':canonical_refs,'source_refs':source_refs,'field_snapshot_refs':field_refs,'released_fixture_refs':released_refs,'summary':f"Controller observed {len(changed_objects)} changed canonical object(s), {len(artifact_refs)} usable artifact(s), {len(method_observations)} optional work receipt(s), and {'a' if response_ref else 'no'} captured candidate response.",'blocker':blocker,'quality_notes':'Controller-generated observation only; professional quality and Workflow effectiveness are evaluated from the actual work.'};write_json(_receipt_path(rd,event),receipt);return receipt

def start(run_dir,event_id=None):
    rd,run,queue=_load(run_dir);event,state=_event(rd,queue,event_id)
    if not event:return {'status':'complete','message':'All prepared business tasks are terminal. Run the evaluator.'}
    if not state['before_checkpoint']:capture_checkpoint(Path(run['product_root']),Path(run['workspace']),rd,event['event_id'],'before',event['business_id'])
    if event.get('release_fixture') and not (rd/'evaluator'/'releases'/f"{event['event_id']}.json").exists():release_event(rd,event['event_id'])
    run['execution_status']='in_progress';run['active_event_id']=event['event_id'];write_json(rd/'run.json',run);return {'status':'ready','product_root':run['product_root'],'workspace':run['workspace'],'business_id':event['business_id'],'business_request':event['task'],'candidate_message':event['task'],'maintainer_note':'Give the model only the staged product/workspace and candidate_message. Do not give it the qualification run directory, evaluator files, event ID, checkpoints, receipts, target Workflow, or scoring metadata.','finish_command':f'python3 qualification/task_controller.py finish "{rd}"'}
def finish(run_dir,event_id=None,blocker_classification=None,blocker_detail=None):
    rd,run,queue=_load(run_dir);active=event_id or run.get('active_event_id');event,state=_event(rd,queue,active,prefer_in_progress=True)
    if not event:raise SystemExit('No unfinished business task is available to finish')
    if not state['before_checkpoint']:raise SystemExit(f"Task {event['event_id']} has no before checkpoint; run controller start first")
    if not state['after_checkpoint']:capture_checkpoint(Path(run['product_root']),Path(run['workspace']),rd,event['event_id'],'after',event['business_id'])
    receipt=derive_receipt(rd,run,event,blocker_classification,blocker_detail)
    if run.get('active_event_id')==event.get('event_id'):run.pop('active_event_id',None)
    remaining=[r for r in rows(rd,queue) if r['state']!='terminal'];run['execution_status']='completed' if not remaining else 'prepared';write_json(rd/'run.json',run);out={'status':'finished','event_id':event['event_id'],'controller_receipt':receipt,'remaining':len(remaining)}
    if remaining:out['next_command']=f'python3 qualification/task_controller.py start "{rd}"'
    else:out['evaluate_command']=f'python3 qualification/evaluate_run.py "{rd}"'
    return out
def status(run_dir):
    rd,run,queue=_load(run_dir);state_rows=rows(rd,queue);counts={k:sum(x['state']==k for x in state_rows) for k in ('terminal','in_progress','pending')};event,state=_event(rd,queue,prefer_in_progress=True);out={'run_dir':str(rd),'event_count':len(state_rows),**counts,'events':state_rows}
    if event:out['next_business_request']=event['task'];out['business_id']=event['business_id'];out['start_command']=f'python3 qualification/task_controller.py start "{rd}"'
    else:out['evaluate_command']=f'python3 qualification/evaluate_run.py "{rd}"'
    return out
def main():
    ap=argparse.ArgumentParser(description='External controller for blind AURA qualification business tasks.');sub=ap.add_subparsers(dest='command',required=True)
    for name in ('start','status'):
        p=sub.add_parser(name);p.add_argument('run_dir');p.add_argument('--event-id')
    p=sub.add_parser('finish');p.add_argument('run_dir');p.add_argument('--event-id');p.add_argument('--blocker-classification',choices=sorted(VALID_BLOCKERS));p.add_argument('--blocker-detail');a=ap.parse_args();result=start(a.run_dir,a.event_id) if a.command=='start' else (finish(a.run_dir,a.event_id,a.blocker_classification,a.blocker_detail) if a.command=='finish' else status(a.run_dir));print(json.dumps(result,indent=2))
if __name__=='__main__':main()
