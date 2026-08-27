#!/usr/bin/env python3
from pathlib import Path
import argparse, json, os, shutil, subprocess, sys, tempfile, uuid
from build_suite import build
from common import ROOT, now, product_snapshot, write_json

FIXTURES=ROOT/'qualification/fixtures'
RUBRICS=json.loads((ROOT/'qualification/rubrics/rubrics.json').read_text())

def event_from_contract(t):
    return {'event_id':t['test_id'],'kind':'contract_acceptance','business_id':'qa-'+t['fixture'].replace('_','-'),'fixture':t['fixture'],'contract_id':t['contract_id'],
            'task':t['candidate_task'],'competitive_profile':t['competitive_profile'],'required_output':t['output_policy'],'receipt_path':f"candidate-results/{t['test_id']}.json"}

def mission_dimensions(m,kind):
    base=[x['id'] for x in RUBRICS['base']]
    if kind=='cross_domain_mission': profile='cross_domain_system'
    elif kind=='marathon_mission': profile='marathon_system'
    else:
        owner=m.get('owner_system'); profile={'core':'governance_and_state','customer-intelligence':'customer_truth','competitor-intelligence':'competitive_intelligence','industry-intelligence':'ecosystem_truth','seo-aeo':'search_live_field','content-synthesis':'artifact_excellence','marketing-synthesis':'paid_and_persuasion_field','customer-optimization':'first_party_outcomes'}.get(owner,'cross_domain_system')
    return base + list(RUBRICS['profiles'].get(profile,[]))

def event_from_mission(m,kind):
    event={'event_id':m['id'],'kind':kind,'business_id':'qa-'+m['fixture'].replace('_','-'),'fixture':m['fixture'],'contract_id':None,'task':m['task'],
           'competitive_profile':'mission','rubric_dimensions':mission_dimensions(m,kind),'required_output':{'actual_output_not_description':True},'receipt_path':f"candidate-results/{m['id']}.json"}
    if m.get('release_fixture'): event['release_fixture']=m['release_fixture']
    return event

def select_events(suite,profile,domain=None,contract_ids=None):
    requested=set(contract_ids or [])
    if requested and profile!='atomic':
        raise SystemExit('--contract is supported only with --profile atomic so a representative contract run cannot silently include missions')
    known={t['contract_id'] for t in suite['contract_tests']}
    unknown=sorted(requested-known)
    if unknown: raise SystemExit('Unknown qualification contract filter(s): '+', '.join(unknown))
    events=[]
    if profile in ('atomic','full'):
        for t in suite['contract_tests']:
            if domain and t['owner_system']!=domain: continue
            if requested and t['contract_id'] not in requested: continue
            events.append(event_from_contract(t))
    if profile in ('domains','full'): events += [event_from_mission(m,'domain_mission') for m in suite['domain_missions'] if not domain or m['owner_system']==domain]
    if profile in ('cross-domain','full'): events += [event_from_mission(m,'cross_domain_mission') for m in suite['cross_domain_missions']]
    if profile in ('marathon','full'): events += [event_from_mission(m,'marathon_mission') for m in suite['marathon_missions']]
    if not events: raise SystemExit('Qualification filters selected no events')
    return events

def publicize_events(events):
    """Give the evaluator full metadata while the candidate sees ordinary opaque business tasks."""
    evaluator=[]; candidate=[]
    for i,event in enumerate(events,1):
        public_id=f'TASK-{i:04d}'
        full=dict(event);full['evaluation_id']=event['event_id'];full['event_id']=public_id;full['receipt_path']=f'candidate-results/{public_id}.json'
        evaluator.append(full)
        visible={'event_id':public_id,'kind':'business_task','business_id':full['business_id'],'fixture':full['fixture'],'task':full['task'],'receipt_path':full['receipt_path']}
        if full.get('release_fixture'):visible['release_fixture']=full['release_fixture']
        candidate.append(visible)
    return evaluator,candidate

def copy_product(src,dst):
    """Stage the runtime product a user would operate, not the maintainer test laboratory."""
    src=Path(src); dst=Path(dst)
    candidate_qualification_helpers={'common.py','checkpoint.py','release_fixture.py','resume_status.py','RECOVERY.md'}
    for p in src.rglob('*'):
        if not p.is_file(): continue
        rel=p.relative_to(src); parts=rel.parts
        if any(x in {'.git','__pycache__','.pytest_cache','.venv','venv'} for x in parts): continue
        if parts and parts[0] in {'generated','knowledge','attachments','aura-qualification-runs','tests'}: continue
        if parts and parts[0]=='qualification':
            if len(parts)!=2 or parts[1] not in candidate_qualification_helpers: continue
        if parts and parts[0]=='instances' and (len(parts)<2 or parts[1] != '_template'): continue
        if parts and parts[0]=='runtime' and not (len(parts)==2 and parts[1]=='README.md'): continue
        if rel.as_posix()=='.businessos/workspace.json': continue
        if rel.suffix in {'.pyc','.zip'}: continue
        q=dst/rel; q.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(p,q)
    return dst

def _run(cmd,product_root,env):
    p=subprocess.run(cmd,cwd=product_root,env=env,capture_output=True,text=True)
    if p.returncode!=0:
        raise SystemExit(f"Qualification preparation command failed ({p.returncode}): {' '.join(map(str,cmd))}\nSTDOUT:\n{p.stdout}\nSTDERR:\n{p.stderr}")
    return p

def init_business(product_root,workspace,fixture):
    data=json.loads((FIXTURES/f'{fixture}.json').read_text()); bid=data['business_id']; name=data['name']
    bootstrap=data.get('bootstrap_facts')
    if not isinstance(bootstrap,dict) or not bootstrap:
        raise SystemExit(f'Qualification fixture {fixture} requires non-empty bootstrap_facts so Level-2 tests begin from grounded canonical context')
    env=dict(os.environ); env['BUSINESSOS_WORKSPACE']=str(workspace); env['PYTHONDONTWRITEBYTECODE']='1'; env['PYTHONUTF8']='1'
    _run([sys.executable,str(product_root/'scripts/init_business.py'),bid,'--name',name],product_root,env)
    inputs=workspace/'attachments'/'qualification-inputs'; inputs.mkdir(parents=True,exist_ok=True)
    initial={k:v for k,v in data.items() if k!='timeline'}
    source_path=inputs/f'{fixture}.json'; source_path.write_text(json.dumps(initial,indent=2)+'\n',encoding='utf-8')
    if data.get('timeline'):
        hidden=workspace.parent/'evaluator'/'hidden-fixtures'; hidden.mkdir(parents=True,exist_ok=True)
        write_json(hidden/f'{fixture}-releases.json',data['timeline'])
    seed_dir=workspace/'runtime'/'qualification-bootstrap'; seed_dir.mkdir(parents=True,exist_ok=True)
    facts_path=seed_dir/f'{fixture}-facts.json'; facts_path.write_text(json.dumps(bootstrap,indent=2)+'\n',encoding='utf-8')
    boot=_run([sys.executable,str(product_root/'scripts/bootstrap_explicit_context.py'),bid,'--facts-file',str(facts_path),'--source-file',str(source_path),'--source-reference',f'qualification fixture {fixture}','--initialization-only'],product_root,env)
    validation=_run([sys.executable,str(product_root/'scripts/validate_business.py'),bid,'--require-context'],product_root,env)
    audit={'fixture':fixture,'business_id':bid,'source_path':str(source_path),'facts_path':str(facts_path),'future_evidence_hidden':bool(data.get('timeline')),'bootstrapped_at':now(),'bootstrap_stdout':boot.stdout,'bootstrap_stderr':boot.stderr,'validation_stdout':validation.stdout,'validation_stderr':validation.stderr}
    write_json(seed_dir/f'{fixture}-bootstrap-audit.json',audit)
    return bid

def instructions(product_root,run_dir,workspace,events):
    return f'''# AURA Representative Business Work Run

Operate ViralTrac AURA the way a real user would use it. The business tasks in the queue are intentionally phrased as ordinary requests. Do not try to infer a hidden target contract, scoring rule, or evaluator expectation; route each request through AURA normally and focus on producing useful professional work.

Product root: `{product_root}`
External workspace: `{workspace}`
Run directory: `{run_dir}`
Task queue: `{run_dir/'candidate/queue.json'}`

Set/retain these environment variables for all work:

```bash
export BUSINESSOS_WORKSPACE='{workspace}'
export AURA_QUALIFICATION_RUN='{run_dir}'
```

The benchmark businesses have already been initialized and their explicit starting context has been grounded into canonical AURA state. Their current supplied first-party evidence is available at `attachments/qualification-inputs/<fixture>.json`. Treat it exactly as you would treat material a real user supplied. Do not redo onboarding or ask for facts already present in canonical state or the supplied material. Later-period evidence may be released during a task; do not inspect evaluator or hidden files.

Process every task in order and continue directly to the next task. A genuine blocker is a valid work outcome when required evidence, authorization, data, or capability is actually unavailable. Never invent a source, business fact, tool action, artifact, measurement, or completed execution in order to avoid blocking.

The checkpoint and receipt steps below are external run bookkeeping. They are not the definition of quality and should not influence the substance or format of the work you produce.

For EVERY task:
1. Read the ordinary business request, current supplied material, and accumulated AURA state. Route the request from natural language through AURA as you would for a real user; do not search for a hidden contract under test.
2. Run `python3 qualification/checkpoint.py <TASK_ID> before --business-id <BUSINESS_ID>` before doing task work.
3. If the task has a `release_fixture` field, run `python3 qualification/release_fixture.py <TASK_ID>` now and treat the released material as newly supplied evidence.
4. Do the real business work. Research when research is required, use available tools when they materially improve or are necessary for the task, create the actual requested deliverable, and use graceful degradation only when the environment truly cannot render/execute the requested medium.
5. Use current external/competitive evidence when the business decision genuinely depends on it. Preserve enough evidence that important claims can be checked later, but do not gather research merely to satisfy bookkeeping.
6. Perform the QA a competent practitioner would actually perform for this result. Do not claim checks, scans, rendered media, publication, or execution that did not happen.
7. Persist the useful business result and relevant AURA state. Keep unknowns and limitations honest, and do not report a draft as executed or an unmeasured outcome as proven.
8. Write a compact receipt to the exact `receipt_path` in the queue. It must be JSON with: `event_id`, `business_id`, `status` (`completed` or `blocked`), `root_run_ids`, `artifact_refs`, `canonical_refs`, `source_refs`, `field_snapshot_refs`, `released_fixture_refs`, `summary`, `blocker` (null if completed; otherwise an object with `classification` and `detail`), and `quality_notes`. Valid blocker classifications are `external_capability`, `authorization`, `missing_required_data`, `external_service`, `qualification_fixture`, or `aura_process`.
9. Run `python3 qualification/checkpoint.py <TASK_ID> after --business-id <BUSINESS_ID>` after the receipt and AURA work are persisted.
10. Immediately continue to the next task.

There are {len(events)} tasks in this run. Completing the queue only means the work run ended; quality is assessed afterward from the actual business outputs.
'''

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--profile',choices=['atomic','domains','cross-domain','marathon','full'],default='atomic'); ap.add_argument('--domain'); ap.add_argument('--contract',action='append',default=[],help='Exact contract ID to include in an atomic representative run; repeat for multiple contracts.'); ap.add_argument('--run-root'); ap.add_argument('--run-id'); a=ap.parse_args()
    if a.profile=='atomic' and not a.domain and not a.contract:
        raise SystemExit('Atomic qualification requires --contract <exact-contract-id> or --domain <installed-domain>; use --profile full explicitly only for an intentional broad endurance run')
    suite=build(); selected=select_events(suite,a.profile,a.domain,a.contract); evaluator_events,candidate_events=publicize_events(selected)
    run_id=a.run_id or ('aura-qualification-'+uuid.uuid4().hex[:10]); root=Path(a.run_root).expanduser().resolve() if a.run_root else Path(tempfile.gettempdir())/'aura-qualification-runs'; run_dir=root/run_id
    if run_dir.exists(): raise SystemExit(f'Run already exists: {run_dir}')
    try:
        run_dir.relative_to(ROOT.resolve()); raise SystemExit('Qualification run root must be outside the AURA product tree to prevent recursive staging or product contamination')
    except ValueError: pass
    product_root=copy_product(ROOT,run_dir/'product'); generation_env=dict(os.environ); generation_env['PYTHONDONTWRITEBYTECODE']='1'; generation_env['PYTHONUTF8']='1'; _run([sys.executable,str(product_root/'scripts/generate_registry.py')],product_root,generation_env); workspace=run_dir/'workspace'; workspace.mkdir(parents=True); (run_dir/'candidate').mkdir(); (run_dir/'evaluator').mkdir(); (run_dir/'candidate-results').mkdir(); (run_dir/'checkpoints').mkdir()
    fixtures={t['fixture'] for t in suite['contract_tests']}|{m['fixture'] for k in ('domain_missions','cross_domain_missions','marathon_missions') for m in suite[k]}
    for f in sorted(fixtures): init_business(product_root,workspace,f)
    baseline=product_snapshot(product_root); write_json(run_dir/'evaluator/product-snapshot.json',baseline)
    contract_filter=sorted(set(a.contract))
    candidate_queue={'format_version':'1.1','run_id':run_id,'event_count':len(candidate_events),'events':candidate_events}
    evaluator_queue={'format_version':'1.1','run_id':run_id,'profile':a.profile,'domain_filter':a.domain,'contract_filter':contract_filter,'event_count':len(evaluator_events),'events':evaluator_events}
    write_json(run_dir/'candidate/queue.json',candidate_queue); write_json(run_dir/'evaluator/queue.json',evaluator_queue); write_json(run_dir/'evaluator/suite.json',suite)
    write_json(run_dir/'evaluator/preparation.json',{'profile':a.profile,'domain_filter':a.domain,'contract_filter':contract_filter,'prepared_at':now()})
    write_json(run_dir/'run.json',{'run_id':run_id,'created_at':now(),'product_root':str(product_root),'workspace':str(workspace),'profile':a.profile,'domain_filter':a.domain,'event_count':len(candidate_events),'status':'prepared','execution_status':'prepared','qualification_status':'NOT_EVALUATED','product_snapshot_digest':baseline['digest'],'benchmark_context_seeded':True,'future_evidence_staged':True})
    (run_dir/'candidate/RUN-INSTRUCTIONS.md').write_text(instructions(product_root,run_dir,workspace,candidate_events),encoding='utf-8')
    print(json.dumps({'run_id':run_id,'run_dir':str(run_dir),'product_root':str(product_root),'workspace':str(workspace),'event_count':len(candidate_events),'instructions':str(run_dir/'candidate/RUN-INSTRUCTIONS.md'),'queue':str(run_dir/'candidate/queue.json')},indent=2))
if __name__=='__main__': main()
