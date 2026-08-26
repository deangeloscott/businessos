#!/usr/bin/env python3
from pathlib import Path
import argparse, json, os, subprocess, sys
from common import ROOT, read_json, snapshot_diff, write_json, now
from integrity import (
    artifact_similarity_flags, exact_duplicate_artifact_flags, existing_ref_paths,
    event_specific_ref_paths, run_control_flags, selector_types,
    structured_prepublish_refs,
)

RUBRICS=json.loads((ROOT/'qualification/rubrics/rubrics.json').read_text())

def idx(items,key): return {x.get(key):x for x in items if isinstance(x,dict) and x.get(key)}
def object_types(snap): return {x.get('object_type') for x in snap.get('objects',[]) if x.get('object_type')}
def changed_object_types(before,after):
    b={x.get('id'):(x.get('object_type'),x.get('sha256')) for x in (before or {}).get('objects',[]) if x.get('id')}
    out=set()
    for x in (after or {}).get('objects',[]):
        oid=x.get('id')
        if oid and (oid not in b or b[oid][1]!=x.get('sha256')): out.add(x.get('object_type'))
    return out

def validate_workspace(product_root,workspace,business_id):
    env=dict(os.environ); env['BUSINESSOS_WORKSPACE']=str(workspace); env['PYTHONDONTWRITEBYTECODE']='1'
    out={}
    for name,cmd in {
        'workspace':[sys.executable,str(product_root/'scripts/validate_workspace.py')],
        'business':[sys.executable,str(product_root/'scripts/validate_business.py'),business_id,'--require-context']
    }.items():
        p=subprocess.run(cmd,cwd=product_root,env=env,capture_output=True,text=True)
        out[name]={'ok':p.returncode==0,'returncode':p.returncode,'stdout':p.stdout[-8000:],'stderr':p.stderr[-8000:]}
    return out

def run_details(workspace,business_id,run_id):
    d=workspace/'runtime'/'runs'/business_id/run_id
    return read_json(d/'run.json',{}),read_json(d/'contract-execution.json',{})

def hard_grade(event,test,before,after,receipt,workspace,product_root):
    gates={}
    gates['checkpoint_before_exists']=before is not None; gates['checkpoint_after_exists']=after is not None; gates['candidate_receipt_exists']=receipt is not None
    run_ids=(receipt or {}).get('root_run_ids') or []; gates['root_run_exists']=bool(run_ids)
    matching=False; matching_complete=False; any_complete=False; all_subcontracts_ok=True; matching_subcontracts_ok=True; run_audit=[]
    for rid in run_ids:
        r,m=run_details(workspace,event['business_id'],rid); run_audit.append({'run_id':rid,'run':r,'manifest':m})
        complete=bool(r.get('status')=='completed' and m.get('root_status')=='completed' and m.get('root_evidence_refs'))
        sub_ok=not any(v.get('status')!='completed' or not v.get('evidence_refs') for v in (m.get('contracts') or {}).values())
        any_complete=any_complete or complete; all_subcontracts_ok=all_subcontracts_ok and sub_ok
        if event.get('contract_id') and r.get('contract_id')==event['contract_id']:
            matching=True; matching_complete=matching_complete or complete; matching_subcontracts_ok=matching_subcontracts_ok and sub_ok
    gates['root_run_contract_matches']=matching if event.get('contract_id') else bool(run_ids)
    gates['root_run_completed']=matching_complete if event.get('contract_id') else any_complete
    gates['required_subcontracts_completed']=(matching_subcontracts_ok and matching) if event.get('contract_id') else (all_subcontracts_ok and bool(run_ids))
    validation=(after or {}).get('validation') or validate_workspace(product_root,workspace,event['business_id']); gates['workspace_valid']=validation['workspace']['ok']; gates['business_valid']=validation['business']['ok']
    gates['completion_claim_truthful']=not(receipt and receipt.get('status')=='completed' and not gates['root_run_completed'])
    artifact_refs=(receipt or {}).get('artifact_refs') or []; actual_artifacts=[str(p) for p in existing_ref_paths(artifact_refs,workspace)]
    if test and test.get('competitive_profile') in {'search_live_field','paid_and_persuasion_field','organic_attention_field'}:
        field_refs=(receipt or {}).get('field_snapshot_refs') or []
        gates['competitive_field_evidence_recorded']=bool(field_refs)
        gates['competitive_field_evidence_exists']=bool(existing_ref_paths(field_refs,workspace))
        gates['competitive_field_evidence_event_specific']=bool(event_specific_ref_paths(field_refs,before,after,workspace))
    if event.get('release_fixture'):
        released_refs=(receipt or {}).get('released_fixture_refs') or []
        gates['released_fixture_recorded']=bool(released_refs)
        gates['released_fixture_exists']=bool(existing_ref_paths(released_refs,workspace))
    if test and test['output_policy'].get('artifact_required'):
        gates['actual_artifact_exists']=bool(actual_artifacts); gates['artifact_referenced_by_receipt']=bool(artifact_refs)
        gates['artifact_nontrivial']=any(Path(p).stat().st_size>=200 for p in actual_artifacts)
    if test and test.get('writes'):
        changed=changed_object_types(before,after); declared=selector_types(test['writes']); gates['declared_write_type_observed_or_explicitly_justified']=bool(declared & changed)
    if test and test.get('artifact_role')=='customer_facing_production_root':
        gates['customer_facing_claim_governance_passed']=gates['root_run_completed']
        gates['prepublish_or_required_qa_recorded']=bool(structured_prepublish_refs(workspace,event['business_id'],before,after,run_audit))
    return gates,validation,run_audit,actual_artifacts

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('run_dir'); ap.add_argument('--judgments'); a=ap.parse_args(); rd=Path(a.run_dir).expanduser().resolve()
    run=read_json(rd/'run.json'); queue=read_json(rd/'candidate/queue.json'); suite=read_json(rd/'evaluator/suite.json'); workspace=Path(run['workspace']); product_root=Path(run['product_root'])
    tests=idx(suite['contract_tests'],'test_id'); judgments={}
    jp=Path(a.judgments).expanduser() if a.judgments else rd/'evaluator/judgments.json'
    if jp.exists(): judgments=idx(read_json(jp,[]),'event_id')
    results=[]
    for event in queue['events']:
        eid=event['event_id']; test=tests.get(eid); before=read_json(rd/'checkpoints'/eid/'before.json'); after=read_json(rd/'checkpoints'/eid/'after.json'); receipt=read_json(rd/event['receipt_path'])
        gates,validation,run_audit,artifacts=hard_grade(event,test,before,after,receipt,workspace,product_root)
        hard_pass=all(gates.values()) if gates else False
        judge=judgments.get(eid); scores=(judge or {}).get('scores') or {}; required_dims=(test or {}).get('rubric_dimensions') or event.get('rubric_dimensions') or [x['id'] for x in RUBRICS['base']]; missing_dims=[d for d in required_dims if d not in scores]; invalid_scores=[v for v in scores.values() if not isinstance(v,(int,float)) or v<0 or v>5]; review_complete=bool(scores) and not missing_dims and not invalid_scores; overall=(sum(scores[d] for d in required_dims)/len(required_dims)) if review_complete else None
        floor=min(scores[d] for d in required_dims) if review_complete else None
        blocker=(receipt or {}).get('blocker'); blocked_class=blocker.get('classification') if isinstance(blocker,dict) else None
        if (receipt or {}).get('status')=='blocked' and blocked_class=='qualification_fixture': verdict='BLOCKED-QUALIFICATION-FIXTURE'
        elif (receipt or {}).get('status')=='blocked' and blocked_class in {'external_capability','authorization','missing_required_data','external_service'}: verdict='BLOCKED-EXTERNAL'
        elif not hard_pass: verdict='FAIL'
        elif scores and not review_complete: verdict='HARD-PASS / REVIEW-INCOMPLETE'
        elif overall is None: verdict='HARD-PASS / REVIEW-PENDING'
        elif floor < RUBRICS['minimums']['dimension_floor']: verdict='FUNCTIONAL-NOT-ACCEPTABLE'
        elif overall >= RUBRICS['minimums']['exceptional_overall']: verdict='EXCEPTIONAL'
        elif overall >= RUBRICS['minimums']['competitive_overall']: verdict='COMPETITIVE'
        elif overall >= RUBRICS['minimums']['acceptable_overall']: verdict='ACCEPTABLE'
        else: verdict='FUNCTIONAL-NOT-ACCEPTABLE'
        results.append({'event_id':eid,'kind':event['kind'],'contract_id':event.get('contract_id'),'business_id':event['business_id'],'hard_pass':hard_pass,'hard_gates':gates,'validation':validation,'workspace_diff':snapshot_diff((before or {}).get('workspace',{}),(after or {}).get('workspace',{})),'receipt':receipt,'actual_artifacts':artifacts,'run_audit':run_audit,'judge':judge,'review_complete':review_complete,'missing_review_dimensions':missing_dims,'invalid_review_scores':invalid_scores,'overall_quality_score':overall,'blocker_classification':blocked_class,'integrity_flags':[],'verdict':verdict})

    similarity=artifact_similarity_flags(results); duplicates=exact_duplicate_artifact_flags(results); run_flags=run_control_flags(rd)
    for r in results:
        r['integrity_flags']=(similarity.get(r['event_id']) or [])+(duplicates.get(r['event_id']) or [])

    review=[]
    for r,event in zip(results,queue['events']):
        test=tests.get(r['event_id']) or {}; receipt=r.get('receipt') or {}; dims=(test or {}).get('rubric_dimensions') or event.get('rubric_dimensions') or [x['id'] for x in RUBRICS['base']]
        review.append({'event_id':r['event_id'],'contract_id':event.get('contract_id'),'claim_under_test':test.get('claim_under_test'),'task':event['task'],'process_steps':test.get('process_steps',[]),'completion_evidence':(test.get('claim_under_test') or {}).get('completion_evidence'),'competitive_profile':event.get('competitive_profile'),'hard_pass':r['hard_pass'],'hard_gates':r['hard_gates'],'integrity_flags':r['integrity_flags'],'run_integrity_flags':run_flags,'artifact_refs':receipt.get('artifact_refs',[]),'actual_artifacts':r.get('actual_artifacts',[]),'source_refs':receipt.get('source_refs',[]),'field_snapshot_refs':receipt.get('field_snapshot_refs',[]),'released_fixture_refs':receipt.get('released_fixture_refs',[]),'rubric_dimensions':dims,'score_scale':RUBRICS['score_scale'],'instructions':'Inspect the actual contract process/completion requirement and the actual artifacts/evidence. Generic contract-shaped placeholders, boilerplate substituted for distinct deliverables, self-attested QA without demonstrated checks, recycled unrelated competitive snapshots, or automation that manufactures qualification paperwork instead of performing the business work must be scored as materially incomplete. A hard-pass proves structural bookkeeping only, not professional quality.'})
    write_json(rd/'evaluator/hard-and-merged-results.json',results); write_json(rd/'evaluator/review-packets.json',review)
    counts={}; gate_failures={}; domain_summary={}; integrity_counts={}
    for r in results:
        counts[r['verdict']]=counts.get(r['verdict'],0)+1
        for g,v in r['hard_gates'].items():
            if not v: gate_failures[g]=gate_failures.get(g,0)+1
        for flag in r.get('integrity_flags',[]): integrity_counts[flag.get('type','unknown')]=integrity_counts.get(flag.get('type','unknown'),0)+1
        if r['kind']=='contract_acceptance':
            t=tests.get(r['event_id']) or {}; d=t.get('owner_system','unknown')
            row=domain_summary.setdefault(d,{'events':0,'hard_pass':0,'quality_scores':[],'verdicts':{}})
            row['events']+=1; row['hard_pass']+=1 if r['hard_pass'] else 0; row['verdicts'][r['verdict']]=row['verdicts'].get(r['verdict'],0)+1
            if r['overall_quality_score'] is not None: row['quality_scores'].append(r['overall_quality_score'])
    for d,row in domain_summary.items(): row['average_quality']=sum(row['quality_scores'])/len(row['quality_scores']) if row['quality_scores'] else None
    report=['# AURA Qualification Report','',f"Run: `{run['run_id']}`",f"Profile: `{run['profile']}`",f"Events: {len(results)}",'', '## Verdict summary','']
    for k in sorted(counts): report.append(f'- **{k}**: {counts[k]}')
    report += ['', '## Coverage','',f"- Contract acceptance events: {sum(1 for r in results if r['kind']=='contract_acceptance')} / {suite['contract_count']}",f"- Domain missions: {sum(1 for r in results if r['kind']=='domain_mission')} / {len(suite['domain_missions'])}",f"- Cross-domain missions: {sum(1 for r in results if r['kind']=='cross_domain_mission')} / {len(suite['cross_domain_missions'])}",f"- Marathon missions: {sum(1 for r in results if r['kind']=='marathon_mission')} / {len(suite['marathon_missions'])}",f"- Concurrency missions: {sum(1 for r in results if r['kind']=='concurrency_mission')} / {len(suite.get('concurrency_missions',[]))}",'','## Domain contract summary',''] + [f"- **{d}**: {row['hard_pass']}/{row['events']} hard-pass" + (f", avg quality {row['average_quality']:.2f}/5" if row['average_quality'] is not None else '') for d,row in sorted(domain_summary.items())] + ['','## Hard-gate failure counts',''] + [f"- `{g}`: {n}" for g,n in sorted(gate_failures.items(), key=lambda x:(-x[1],x[0]))]
    report += ['','## Integrity flags',''] + ([f"- `{k}`: {n}" for k,n in sorted(integrity_counts.items())] if integrity_counts else ['- None'])
    if run_flags: report += ['','## Run-level integrity flags',''] + [f"- `{x['type']}`: {x['path']}" for x in run_flags]
    report += ['','## Event results','']
    for r in results: report.append(f"- `{r['event_id']}` — **{r['verdict']}**"+(f" — {r['overall_quality_score']:.2f}/5" if r['overall_quality_score'] is not None else '')+(f" — integrity flags: {len(r['integrity_flags'])}" if r['integrity_flags'] else ''))
    (rd/'REPORT.md').write_text('\n'.join(report)+'\n',encoding='utf-8')
    write_json(rd/'evaluator/summary.json',{'verdict_counts':counts,'gate_failure_counts':gate_failures,'integrity_flag_counts':integrity_counts,'run_integrity_flags':run_flags,'domain_summary':domain_summary}); write_json(rd/'run.json',{**run,'status':'evaluated','evaluated_at':now(),'verdict_counts':counts})
    print(json.dumps({'results':str(rd/'evaluator/hard-and-merged-results.json'),'review_packets':str(rd/'evaluator/review-packets.json'),'report':str(rd/'REPORT.md'),'verdict_counts':counts,'integrity_flag_counts':integrity_counts,'run_integrity_flags':run_flags},indent=2))
if __name__=='__main__': main()
