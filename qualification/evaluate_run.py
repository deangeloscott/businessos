#!/usr/bin/env python3
from pathlib import Path
import argparse, json, os, subprocess, sys
from common import ROOT, now, product_snapshot, read_json, snapshot_diff, write_json
sys.path.insert(0,str(ROOT/'scripts'))
from completion_evidence import completion_spec, contract_index, subcontract_manifest_errors, validate_evidence
from integrity import (
    artifact_similarity_flags, checkpoint_chain_contiguous, declared_write_absence_justified,
    exact_duplicate_artifact_flags, existing_ref_paths,
    event_specific_ref_paths, integrity_hard_failure, reconstructable_field_snapshot_paths,
    run_control_flags, selector_types,
)
from qa_resolution import required_qa_contract_ids, recorded_required_qa_refs

RUBRICS=json.loads((ROOT/'qualification/rubrics/rubrics.json').read_text())
CONTRACTS=contract_index()

def idx(items,key): return {x.get(key):x for x in items if isinstance(x,dict) and x.get(key)}
def test_for_event(event,tests): return tests.get(event.get('evaluation_id') or event.get('event_id')) or {}
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

def hard_grade(event,test,before,after,receipt,workspace,product_root,previous_after=None):
    gates={}
    gates['checkpoint_before_exists']=before is not None; gates['checkpoint_after_exists']=after is not None; gates['candidate_receipt_exists']=receipt is not None
    if previous_after is not None:gates['checkpoint_chain_contiguous']=checkpoint_chain_contiguous(previous_after,before)
    run_ids=(receipt or {}).get('root_run_ids') or []; gates['root_run_exists']=bool(run_ids)
    matching=False; matching_complete=False; any_complete=False; all_subcontracts_ok=True; matching_subcontracts_ok=True; run_audit=[]
    matching_root_evidence_valid=False;matching_subcontract_evidence_valid=False
    for rid in run_ids:
        r,m=run_details(workspace,event['business_id'],rid); run_audit.append({'run_id':rid,'run':r,'manifest':m})
        complete=bool(r.get('status')=='completed' and m.get('root_status')=='completed' and m.get('root_evidence_refs'))
        sub_ok=not any(v.get('status')!='completed' or not v.get('evidence_refs') for v in (m.get('contracts') or {}).values())
        any_complete=any_complete or complete; all_subcontracts_ok=all_subcontracts_ok and sub_ok
        if event.get('contract_id') and r.get('contract_id')==event['contract_id']:
            matching=True; matching_complete=matching_complete or complete; matching_subcontracts_ok=matching_subcontracts_ok and sub_ok
            root=CONTRACTS.get(event['contract_id']);root_errors=['contract missing from evaluator registry'] if not root else validate_evidence(root,m.get('root_evidence_refs') or [],event['business_id'],rid,phase='root',manifest=m)
            subcontract_errors=subcontract_manifest_errors(m,event['business_id'],rid,CONTRACTS)
            matching_root_evidence_valid=matching_root_evidence_valid or (complete and not root_errors)
            matching_subcontract_evidence_valid=matching_subcontract_evidence_valid or (sub_ok and not subcontract_errors)
    gates['root_run_contract_matches']=matching if event.get('contract_id') else bool(run_ids)
    gates['root_run_completed']=matching_complete if event.get('contract_id') else any_complete
    gates['required_subcontracts_completed']=(matching_subcontracts_ok and matching) if event.get('contract_id') else (all_subcontracts_ok and bool(run_ids))
    if event.get('contract_id'):
        gates['root_completion_evidence_valid']=matching_root_evidence_valid
        gates['required_subcontract_evidence_valid']=matching_subcontract_evidence_valid
    validation=(after or {}).get('validation') or validate_workspace(product_root,workspace,event['business_id']); gates['workspace_valid']=validation['workspace']['ok']; gates['business_valid']=validation['business']['ok']
    gates['completion_claim_truthful']=not(receipt and receipt.get('status')=='completed' and not gates['root_run_completed'])
    artifact_refs=(receipt or {}).get('artifact_refs') or []; actual_artifacts=[str(p) for p in existing_ref_paths(artifact_refs,workspace)]
    if test and test.get('competitive_profile') in {'search_live_field','paid_and_persuasion_field','organic_attention_field'}:
        field_refs=(receipt or {}).get('field_snapshot_refs') or []
        gates['competitive_field_evidence_recorded']=bool(field_refs)
        gates['competitive_field_evidence_exists']=bool(existing_ref_paths(field_refs,workspace))
        gates['competitive_field_evidence_event_specific']=bool(event_specific_ref_paths(field_refs,before,after,workspace))
        gates['competitive_field_evidence_reconstructable']=bool(reconstructable_field_snapshot_paths(field_refs,before,after,workspace))
    if event.get('release_fixture'):
        released_refs=(receipt or {}).get('released_fixture_refs') or []
        gates['released_fixture_recorded']=bool(released_refs)
        gates['released_fixture_exists']=bool(existing_ref_paths(released_refs,workspace))
    if test and test['output_policy'].get('artifact_required'):
        gates['actual_artifact_exists']=bool(actual_artifacts); gates['artifact_referenced_by_receipt']=bool(artifact_refs)
        gates['artifact_nontrivial']=any(Path(p).stat().st_size>=200 for p in actual_artifacts)
    if test and test.get('writes'):
        changed=changed_object_types(before,after); declared=selector_types(test['writes']); root=CONTRACTS.get(event.get('contract_id'),{})
        justified=declared_write_absence_justified(completion_spec(root).get('profile'),actual_artifacts)
        gates['declared_write_type_observed_or_explicitly_justified']=bool(declared & changed) or justified
    if test and test.get('artifact_role')=='customer_facing_production_root':
        # Active-business validation is the shared claim-governance gate. It understands
        # text-native artifacts and declared claim surfaces for opaque rendered media.
        gates['customer_facing_claim_governance_passed']=gates['business_valid']
        # Qualification verifies QA that the actual production Run declares. It does not
        # invent a domain-independent QA subcontract. Content Run creation supplies its
        # shared pre-publish invariant; Marketing and other owners keep their own graph.
        qa_ids=required_qa_contract_ids(run_audit,CONTRACTS,completion_spec,event.get('contract_id'))
        qa_refs=recorded_required_qa_refs(run_audit,qa_ids,event.get('contract_id'))
        if qa_ids:
            gates['customer_facing_required_qa_recorded']=all(qa_refs.get(cid) for cid in qa_ids)
    return gates,validation,run_audit,actual_artifacts

def staged_product_integrity_flags(rd,product_root,run):
    baseline=read_json(rd/'evaluator/product-snapshot.json')
    if not isinstance(baseline,dict) or not baseline.get('digest'):
        return [{'type':'product_integrity_baseline_missing','path':str(rd/'evaluator/product-snapshot.json')}]
    if run.get('product_snapshot_digest')!=baseline.get('digest'):
        return [{'type':'product_integrity_baseline_mismatch','path':str(rd/'run.json')}]
    current=product_snapshot(product_root); diff=snapshot_diff(baseline,current)
    if not any(diff.values()): return []
    return [{
        'type':'staged_product_mutation','path':str(product_root),
        'created_count':len(diff['created']),'modified_count':len(diff['modified']),'deleted_count':len(diff['deleted']),
        'created':diff['created'][:20],'modified':diff['modified'][:20],'deleted':diff['deleted'][:20],
        'baseline_digest':baseline.get('digest'),'current_digest':current.get('digest'),
    }]

def qualification_status(counts):
    if counts.get('FAIL'): return 'FAILED'
    if counts.get('BLOCKED-EXTERNAL') or counts.get('BLOCKED-QUALIFICATION-FIXTURE'): return 'INCOMPLETE'
    if counts.get('HARD-PASS / REVIEW-PENDING') or counts.get('HARD-PASS / REVIEW-INCOMPLETE'): return 'REVIEW_REQUIRED'
    qualified=sum(counts.get(x,0) for x in ('ACCEPTABLE','COMPETITIVE','EXCEPTIONAL'))
    total=sum(counts.values())
    return 'QUALIFIED' if total and qualified==total else 'NOT_QUALIFIED'

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('run_dir'); ap.add_argument('--judgments'); a=ap.parse_args(); rd=Path(a.run_dir).expanduser().resolve()
    run=read_json(rd/'run.json'); queue=read_json(rd/'evaluator/queue.json') or read_json(rd/'candidate/queue.json'); suite=read_json(rd/'evaluator/suite.json'); workspace=Path(run['workspace']); product_root=Path(run['product_root'])
    os.environ['BUSINESSOS_WORKSPACE']=str(workspace)
    tests=idx(suite['contract_tests'],'test_id'); judgments={}; event_by_id=idx(queue.get('events',[]),'event_id')
    jp=Path(a.judgments).expanduser() if a.judgments else rd/'evaluator/judgments.json'
    if jp.exists(): judgments=idx(read_json(jp,[]),'event_id')
    results=[]
    previous_after=None
    for event in queue['events']:
        eid=event['event_id']; test=test_for_event(event,tests); before=read_json(rd/'checkpoints'/eid/'before.json'); after=read_json(rd/'checkpoints'/eid/'after.json'); receipt=read_json(rd/event['receipt_path'])
        gates,validation,run_audit,artifacts=hard_grade(event,test,before,after,receipt,workspace,product_root,previous_after)
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
        results.append({'event_id':eid,'evaluation_id':event.get('evaluation_id'),'kind':event['kind'],'contract_id':event.get('contract_id'),'business_id':event['business_id'],'hard_pass':hard_pass,'hard_gates':gates,'validation':validation,'workspace_diff':snapshot_diff((before or {}).get('workspace',{}),(after or {}).get('workspace',{})),'receipt':receipt,'actual_artifacts':artifacts,'run_audit':run_audit,'judge':judge,'review_complete':review_complete,'missing_review_dimensions':missing_dims,'invalid_review_scores':invalid_scores,'overall_quality_score':overall,'blocker_classification':blocked_class,'integrity_flags':[],'verdict':verdict})
        previous_after=after

    similarity=artifact_similarity_flags(results); duplicates=exact_duplicate_artifact_flags(results); run_flags=run_control_flags(rd,workspace)+staged_product_integrity_flags(rd,product_root,run)
    critical_types={'mass_completion_runner','candidate_evaluator_spec_access','staged_product_mutation','product_integrity_baseline_missing','product_integrity_baseline_mismatch'}
    critical_run_flags=[x for x in run_flags if x.get('type') in critical_types]
    for r in results:
        r['integrity_flags']=(similarity.get(r['event_id']) or [])+(duplicates.get(r['event_id']) or [])
        if r.get('actual_artifacts'):
            r['hard_gates']['artifact_contract_specific']=not integrity_hard_failure(r['integrity_flags'])
            if not r['hard_gates']['artifact_contract_specific']:
                r['hard_pass']=False
                if r.get('verdict') not in {'BLOCKED-EXTERNAL','BLOCKED-QUALIFICATION-FIXTURE'}:r['verdict']='FAIL'
        if critical_run_flags:
            r['hard_gates']['qualification_integrity_clean']=False
            r['hard_pass']=False
            if r.get('verdict') not in {'BLOCKED-EXTERNAL','BLOCKED-QUALIFICATION-FIXTURE'}:r['verdict']='FAIL'

    review=[]
    for r,event in zip(results,queue['events']):
        test=test_for_event(event,tests); receipt=r.get('receipt') or {}; dims=(test or {}).get('rubric_dimensions') or event.get('rubric_dimensions') or [x['id'] for x in RUBRICS['base']]
        review.append({'event_id':r['event_id'],'evaluation_id':event.get('evaluation_id'),'contract_id':event.get('contract_id'),'claim_under_test':test.get('claim_under_test'),'task':event['task'],'process_steps':test.get('process_steps',[]),'completion_evidence':(test.get('claim_under_test') or {}).get('completion_evidence'),'competitive_profile':event.get('competitive_profile'),'hard_pass':r['hard_pass'],'hard_gates':r['hard_gates'],'integrity_flags':r['integrity_flags'],'run_integrity_flags':run_flags,'artifact_refs':receipt.get('artifact_refs',[]),'actual_artifacts':r.get('actual_artifacts',[]),'source_refs':receipt.get('source_refs',[]),'field_snapshot_refs':receipt.get('field_snapshot_refs',[]),'released_fixture_refs':receipt.get('released_fixture_refs',[]),'rubric_dimensions':dims,'score_scale':RUBRICS['score_scale'],'instructions':'Judge the actual business result first. Verify that the requested work was genuinely performed, important evidence is real, and the deliverable is useful and professional for its audience. Do not reward or penalize arbitrary word counts, slide counts, formatting conventions, or validator-shaped language. Structural hard gates establish integrity only; they are not a quality score.'})
    write_json(rd/'evaluator/hard-and-merged-results.json',results); write_json(rd/'evaluator/review-packets.json',review)
    counts={}; gate_failures={}; domain_summary={}; integrity_counts={}
    for r in results:
        counts[r['verdict']]=counts.get(r['verdict'],0)+1
        for g,v in r['hard_gates'].items():
            if not v: gate_failures[g]=gate_failures.get(g,0)+1
        for flag in r.get('integrity_flags',[]): integrity_counts[flag.get('type','unknown')]=integrity_counts.get(flag.get('type','unknown'),0)+1
        event=event_by_id.get(r['event_id']) or {}
        if r['kind']=='contract_acceptance':
            t=test_for_event(event,tests); d=t.get('owner_system','unknown')
            row=domain_summary.setdefault(d,{'events':0,'hard_pass':0,'quality_scores':[],'verdicts':{}})
            row['events']+=1; row['hard_pass']+=1 if r['hard_pass'] else 0; row['verdicts'][r['verdict']]=row['verdicts'].get(r['verdict'],0)+1
            if r['overall_quality_score'] is not None: row['quality_scores'].append(r['overall_quality_score'])
    for d,row in domain_summary.items(): row['average_quality']=sum(row['quality_scores'])/len(row['quality_scores']) if row['quality_scores'] else None
    qstatus=qualification_status(counts)
    report=['# AURA Qualification Report','',f"Run: `{run['run_id']}`",f"Profile: `{run['profile']}`",f"Events: {len(results)}",f"Qualification status: **{qstatus}**",'', '## Verdict summary','']
    for k in sorted(counts): report.append(f'- **{k}**: {counts[k]}')
    report += ['', '## Coverage','',f"- Contract acceptance events: {sum(1 for r in results if r['kind']=='contract_acceptance')} / {suite['contract_count']}",f"- Domain missions: {sum(1 for r in results if r['kind']=='domain_mission')} / {len(suite['domain_missions'])}",f"- Cross-domain missions: {sum(1 for r in results if r['kind']=='cross_domain_mission')} / {len(suite['cross_domain_missions'])}",f"- Marathon missions: {sum(1 for r in results if r['kind']=='marathon_mission')} / {len(suite['marathon_missions'])}",f"- Concurrency missions: {sum(1 for r in results if r['kind']=='concurrency_mission')} / {len(suite.get('concurrency_missions',[]))}",'','## Domain contract summary',''] + [f"- **{d}**: {row['hard_pass']}/{row['events']} hard-pass" + (f", avg quality {row['average_quality']:.2f}/5" if row['average_quality'] is not None else '') for d,row in sorted(domain_summary.items())] + ['','## Hard-gate failure counts',''] + [f"- `{g}`: {n}" for g,n in sorted(gate_failures.items(), key=lambda x:(-x[1],x[0]))]
    report += ['','## Integrity flags',''] + ([f"- `{k}`: {n}" for k,n in sorted(integrity_counts.items())] if integrity_counts else ['- None'])
    if run_flags: report += ['','## Run-level integrity flags',''] + [f"- `{x['type']}`: {x['path']}" for x in run_flags]
    report += ['','## Event results','']
    for r in results: report.append(f"- `{r['event_id']}` — **{r['verdict']}**"+(f" — {r['overall_quality_score']:.2f}/5" if r['overall_quality_score'] is not None else '')+(f" — integrity flags: {len(r['integrity_flags'])}" if r['integrity_flags'] else ''))
    (rd/'REPORT.md').write_text('\n'.join(report)+'\n',encoding='utf-8')
    write_json(rd/'evaluator/summary.json',{'qualification_status':qstatus,'verdict_counts':counts,'gate_failure_counts':gate_failures,'integrity_flag_counts':integrity_counts,'run_integrity_flags':run_flags,'domain_summary':domain_summary}); write_json(rd/'run.json',{**run,'status':'evaluated','execution_status':'evaluated','qualification_status':qstatus,'evaluated_at':now(),'verdict_counts':counts})
    print(json.dumps({'results':str(rd/'evaluator/hard-and-merged-results.json'),'review_packets':str(rd/'evaluator/review-packets.json'),'report':str(rd/'REPORT.md'),'qualification_status':qstatus,'verdict_counts':counts,'integrity_flag_counts':integrity_counts,'run_integrity_flags':run_flags},indent=2))
if __name__=='__main__': main()
