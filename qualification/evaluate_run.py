#!/usr/bin/env python3
"""Evaluate real qualification work: universal integrity first, capable quality review second."""
from pathlib import Path
import argparse,json,os,subprocess,sys
from common import ROOT,now,product_snapshot,read_json,snapshot_diff,write_json
sys.path.insert(0,str(ROOT/'scripts'))
from integrity import artifact_similarity_flags,checkpoint_chain_contiguous,exact_duplicate_artifact_flags,existing_ref_paths,run_control_flags

RUBRICS=json.loads((ROOT/'qualification/rubrics/rubrics.json').read_text())


def idx(items,key):return {x.get(key):x for x in items if isinstance(x,dict) and x.get(key)}


def validate_workspace(product_root,workspace,business_id):
    env=dict(os.environ);env['BUSINESSOS_WORKSPACE']=str(workspace);env['PYTHONDONTWRITEBYTECODE']='1';out={}
    for name,cmd in {
        'workspace':[sys.executable,str(product_root/'scripts/validate_workspace.py')],
        'business':[sys.executable,str(product_root/'scripts/validate_business.py'),business_id,'--require-context'],
    }.items():
        p=subprocess.run(cmd,cwd=product_root,env=env,capture_output=True,text=True)
        out[name]={'ok':p.returncode==0,'returncode':p.returncode,'stdout':p.stdout[-8000:],'stderr':p.stderr[-8000:]}
    return out


def _evaluator_issues(rd,event,before,after,receipt,previous_after=None):
    issues=[]
    if before is None:issues.append('before_checkpoint_missing')
    if after is None:issues.append('after_checkpoint_missing')
    if receipt is None:issues.append('controller_receipt_missing')
    elif receipt.get('generated_by')!='qualification_controller':issues.append('controller_receipt_untrusted')
    if previous_after is not None and before is not None and not checkpoint_chain_contiguous(previous_after,before):
        issues.append('checkpoint_chain_discontinuous')
    if event.get('release_fixture') and not (rd/'evaluator'/'releases'/f"{event['event_id']}.json").exists():
        issues.append('required_fixture_release_missing')
    return issues


def hard_grade(event,before,after,receipt,workspace,product_root):
    """Apply only universal facts that deterministic code can establish safely."""
    validation=(after or {}).get('validation') or validate_workspace(product_root,workspace,event['business_id'])
    gates={
        'workspace_valid':validation['workspace']['ok'],
        'business_valid':validation['business']['ok'],
    }
    material=bool((receipt or {}).get('material_result_observed'))
    gates['material_result_observed']=material
    gates['completion_claim_truthful']=not((receipt or {}).get('status')=='completed' and not material)
    artifact_refs=(receipt or {}).get('artifact_refs') or []
    actual_artifacts=[str(p) for p in existing_ref_paths(artifact_refs,workspace)]
    return gates,validation,actual_artifacts


def staged_product_integrity_flags(rd,product_root,run):
    baseline=read_json(rd/'evaluator/product-snapshot.json')
    if not isinstance(baseline,dict) or not baseline.get('digest'):
        return [{'type':'product_integrity_baseline_missing','path':str(rd/'evaluator/product-snapshot.json')}]
    if run.get('product_snapshot_digest')!=baseline.get('digest'):
        return [{'type':'product_integrity_baseline_mismatch','path':str(rd/'run.json')}]
    current=product_snapshot(product_root);diff=snapshot_diff(baseline,current)
    if not any(diff.values()):return []
    return [{
        'type':'staged_product_mutation','path':str(product_root),
        'created_count':len(diff['created']),'modified_count':len(diff['modified']),'deleted_count':len(diff['deleted']),
        'created':diff['created'][:20],'modified':diff['modified'][:20],'deleted':diff['deleted'][:20],
        'baseline_digest':baseline.get('digest'),'current_digest':current.get('digest'),
    }]


def qualification_status(counts):
    if counts.get('EVALUATOR-ERROR'):return 'INCOMPLETE'
    if counts.get('FAIL'):return 'FAILED'
    if counts.get('BLOCKED-EXTERNAL') or counts.get('BLOCKED-QUALIFICATION-FIXTURE'):return 'INCOMPLETE'
    if counts.get('HARD-PASS / REVIEW-PENDING') or counts.get('HARD-PASS / REVIEW-INCOMPLETE'):return 'REVIEW_REQUIRED'
    qualified=sum(counts.get(x,0) for x in ('ACCEPTABLE','COMPETITIVE','EXCEPTIONAL'))
    total=sum(counts.values())
    return 'QUALIFIED' if total and qualified==total else 'NOT_QUALIFIED'


RUBRIC_DIMENSIONS=[x['id'] for x in RUBRICS['base']]


def main():
    ap=argparse.ArgumentParser();ap.add_argument('run_dir');ap.add_argument('--judgments');a=ap.parse_args()
    rd=Path(a.run_dir).expanduser().resolve()
    run=read_json(rd/'run.json');queue=read_json(rd/'evaluator/queue.json')
    workspace=Path(run['workspace']);product_root=Path(run['product_root']);os.environ['BUSINESSOS_WORKSPACE']=str(workspace)
    judgments={};event_by_id=idx(queue.get('events',[]),'event_id')
    jp=Path(a.judgments).expanduser() if a.judgments else rd/'evaluator/judgments.json'
    if jp.exists():judgments=idx(read_json(jp,[]),'event_id')

    results=[];previous_after=None
    for event in queue['events']:
        eid=event['event_id']
        before=read_json(rd/'checkpoints'/eid/'before.json')
        after=read_json(rd/'checkpoints'/eid/'after.json')
        receipt=read_json(rd/event['receipt_path'])
        evaluator_issues=_evaluator_issues(rd,event,before,after,receipt,previous_after)
        gates,validation,artifacts=hard_grade(event,before,after,receipt,workspace,product_root)
        hard_pass=all(gates.values()) if gates else False
        judge=judgments.get(eid);scores=(judge or {}).get('scores') or {};required_dims=RUBRIC_DIMENSIONS
        missing_dims=[d for d in required_dims if d not in scores]
        invalid_scores=[v for v in scores.values() if not isinstance(v,(int,float)) or v<0 or v>5]
        review_complete=bool(scores) and not missing_dims and not invalid_scores
        overall=(sum(scores[d] for d in required_dims)/len(required_dims)) if review_complete else None
        floor=min(scores[d] for d in required_dims) if review_complete else None
        blocker=(receipt or {}).get('blocker');blocked_class=blocker.get('classification') if isinstance(blocker,dict) else None

        if evaluator_issues:verdict='EVALUATOR-ERROR';hard_pass=False
        elif (receipt or {}).get('status')=='blocked' and blocked_class=='qualification_fixture':verdict='BLOCKED-QUALIFICATION-FIXTURE'
        elif (receipt or {}).get('status')=='blocked' and blocked_class in {'external_capability','external_authority','missing_required_data','external_service'}:verdict='BLOCKED-EXTERNAL'
        elif not hard_pass:verdict='FAIL'
        elif scores and not review_complete:verdict='HARD-PASS / REVIEW-INCOMPLETE'
        elif overall is None:verdict='HARD-PASS / REVIEW-PENDING'
        elif floor<RUBRICS['minimums']['dimension_floor']:verdict='FUNCTIONAL-NOT-ACCEPTABLE'
        elif overall>=RUBRICS['minimums']['exceptional_overall']:verdict='EXCEPTIONAL'
        elif overall>=RUBRICS['minimums']['competitive_overall']:verdict='COMPETITIVE'
        elif overall>=RUBRICS['minimums']['acceptable_overall']:verdict='ACCEPTABLE'
        else:verdict='FUNCTIONAL-NOT-ACCEPTABLE'

        results.append({
            'event_id':eid,'evaluation_id':event.get('evaluation_id'),'kind':event['kind'],
            'workflow_id':event.get('workflow_id'),'business_id':event['business_id'],
            'hard_pass':hard_pass,'hard_gates':gates,'evaluator_integrity_issues':evaluator_issues,
            'validation':validation,
            'workspace_diff':snapshot_diff((before or {}).get('workspace',{}),(after or {}).get('workspace',{})),
            'receipt':receipt,'actual_artifacts':artifacts,'method_observations':(receipt or {}).get('method_observations',[]),
            'judge':judge,'review_complete':review_complete,'missing_review_dimensions':missing_dims,
            'invalid_review_scores':invalid_scores,'overall_quality_score':overall,
            'blocker_classification':blocked_class,'integrity_flags':[],'verdict':verdict,
        })
        previous_after=after

    similarity=artifact_similarity_flags(results)
    duplicates=exact_duplicate_artifact_flags(results)
    run_flags=run_control_flags(rd,workspace)+staged_product_integrity_flags(rd,product_root,run)
    critical_types={'candidate_evaluator_spec_access','staged_product_mutation','product_integrity_baseline_missing','product_integrity_baseline_mismatch'}
    critical_run_flags=[x for x in run_flags if x.get('type') in critical_types]

    for result in results:
        result['integrity_flags']=(similarity.get(result['event_id']) or [])+(duplicates.get(result['event_id']) or [])
        exact_duplicate=any(x.get('type')=='exact_artifact_reuse' for x in result['integrity_flags'])
        if result.get('actual_artifacts'):
            result['hard_gates']['artifact_not_exact_duplicate']=not exact_duplicate
            if exact_duplicate:result['hard_pass']=False
        if critical_run_flags:
            result['hard_gates']['qualification_integrity_clean']=False;result['hard_pass']=False
        if (exact_duplicate or critical_run_flags) and result.get('verdict') not in {'EVALUATOR-ERROR','BLOCKED-EXTERNAL','BLOCKED-QUALIFICATION-FIXTURE'}:
            result['verdict']='FAIL'

    review=[]
    for result,event in zip(results,queue['events']):
        receipt=result.get('receipt') or {};dims=RUBRIC_DIMENSIONS
        claim=event.get('claim_under_test') or {}
        review.append({
            'event_id':result['event_id'],'evaluation_id':event.get('evaluation_id'),'workflow_id':event.get('workflow_id'),
            'claim_under_test':claim or None,'task':event['task'],
            'workflow_process_steps':event.get('workflow_process_steps') or [],
            'completion_evidence':claim.get('completion_evidence'),
            'hard_pass':result['hard_pass'],'hard_gates':result['hard_gates'],
            'evaluator_integrity_issues':result['evaluator_integrity_issues'],
            'integrity_flags':result['integrity_flags'],'run_integrity_flags':run_flags,
            'artifact_refs':receipt.get('artifact_refs',[]),'actual_artifacts':result.get('actual_artifacts',[]),
            'canonical_refs':receipt.get('canonical_refs',[]),'source_refs':receipt.get('source_refs',[]),
            'field_snapshot_refs':receipt.get('field_snapshot_refs',[]),'released_fixture_refs':receipt.get('released_fixture_refs',[]),
            'method_observations':receipt.get('method_observations',[]),'rubric_dimensions':dims,
            'score_scale':RUBRICS['score_scale'],
            'instructions':'Judge the actual business result first. Infer substantive requirements from the ordinary request, relevant AURA operating knowledge, business context, and professional standards—not from hidden id taxonomies. If the job required a usable artifact, current external research, rendered QA, implementation, comparison, measurement, or another material step and that work is absent or weak, score it accordingly even though the universal hard gates passed. Equivalent or better methods are valid; creating a particular Run or matching an execution graph is not required. Verify that evidence is real, durable AURA state is truthful/useful, and the result is professionally usable.',
        })

    write_json(rd/'evaluator/hard-and-merged-results.json',results)
    write_json(rd/'evaluator/review-packets.json',review)
    counts={};gate_failures={};integrity_counts={};evaluator_issue_counts={}
    for result in results:
        counts[result['verdict']]=counts.get(result['verdict'],0)+1
        for gate,value in result['hard_gates'].items():
            if not value:gate_failures[gate]=gate_failures.get(gate,0)+1
        for flag in result.get('integrity_flags',[]):
            integrity_counts[flag.get('type','unknown')]=integrity_counts.get(flag.get('type','unknown'),0)+1
        for issue in result.get('evaluator_integrity_issues',[]):
            evaluator_issue_counts[issue]=evaluator_issue_counts.get(issue,0)+1

    qstatus=qualification_status(counts)
    use_case_events=sum(1 for r in results if r['kind']=='use_case')
    workflow_diagnostics=sum(1 for r in results if r['kind']=='workflow_diagnostic')
    report=[
        '# AURA Qualification Report','',
        f"Run: `{run['run_id']}`",
        f"Mode: `{run['mode']}`",
        f"Events: {len(results)}",
        f"Qualification status: **{qstatus}**",'',
        '## Verdict summary','',
    ]
    for key in sorted(counts):report.append(f'- **{key}**: {counts[key]}')
    report += [
        '',
        '## Run shape','',
        f'- Real-world use-case events: {use_case_events}',
        f'- Focused Workflow diagnostic events: {workflow_diagnostics}',
        '',
        '## Business-work gate failures','',
    ] + ([f"- `{g}`: {n}" for g,n in sorted(gate_failures.items(),key=lambda x:(-x[1],x[0]))] or ['- None'])
    report += ['','## Evaluator integrity issues',''] + ([f"- `{k}`: {n}" for k,n in sorted(evaluator_issue_counts.items())] if evaluator_issue_counts else ['- None'])
    report += ['','## Artifact/integrity warnings',''] + ([f"- `{k}`: {n}" for k,n in sorted(integrity_counts.items())] if integrity_counts else ['- None'])
    if run_flags:report += ['','## Qualification integrity flags','']+[f"- `{x['type']}`: {x['path']}" for x in run_flags]
    report += ['','## Event results','']
    for result in results:
        report.append(
            f"- `{result['event_id']}` — **{result['verdict']}**"
            +(f" — {result['overall_quality_score']:.2f}/5" if result['overall_quality_score'] is not None else '')
            +(f" — integrity warnings: {len(result['integrity_flags'])}" if result['integrity_flags'] else '')
        )

    (rd/'REPORT.md').write_text('\n'.join(report)+'\n',encoding='utf-8')
    summary={
        'qualification_status':qstatus,'verdict_counts':counts,'gate_failure_counts':gate_failures,
        'evaluator_integrity_issue_counts':evaluator_issue_counts,'integrity_flag_counts':integrity_counts,
        'run_integrity_flags':run_flags,'use_case_events':use_case_events,'workflow_diagnostic_events':workflow_diagnostics,
    }
    write_json(rd/'evaluator/summary.json',summary)
    write_json(rd/'run.json',{
        **run,'status':'evaluated','execution_status':'evaluated','qualification_status':qstatus,
        'evaluated_at':now(),'verdict_counts':counts,
    })
    print(json.dumps({
        'results':str(rd/'evaluator/hard-and-merged-results.json'),
        'review_packets':str(rd/'evaluator/review-packets.json'),
        'report':str(rd/'REPORT.md'),'qualification_status':qstatus,
        'verdict_counts':counts,'evaluator_integrity_issue_counts':evaluator_issue_counts,
        'integrity_flag_counts':integrity_counts,'run_integrity_flags':run_flags,
    },indent=2))


if __name__=='__main__':main()
