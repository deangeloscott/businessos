#!/usr/bin/env python3
from pathlib import Path
import argparse, json, os, shutil, subprocess, sys, tempfile, uuid
from build_suite import build
from common import ROOT, now, write_json

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

def copy_product(src,dst):
    src=Path(src); dst=Path(dst)
    for p in src.rglob('*'):
        if not p.is_file(): continue
        rel=p.relative_to(src); parts=rel.parts
        if any(x in {'.git','__pycache__','.pytest_cache','.venv','venv'} for x in parts): continue
        if parts and parts[0] in {'generated','knowledge','attachments'}: continue
        if len(parts)>=2 and parts[0]=='qualification' and parts[1]=='fixtures': continue
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
    env=dict(os.environ); env['BUSINESSOS_WORKSPACE']=str(workspace); env['PYTHONDONTWRITEBYTECODE']='1'
    _run([sys.executable,str(product_root/'scripts/init_business.py'),bid,'--name',name],product_root,env)
    inputs=workspace/'attachments'/'qualification-inputs'; inputs.mkdir(parents=True,exist_ok=True)
    initial={k:v for k,v in data.items() if k!='timeline'}
    source_path=inputs/f'{fixture}.json'; source_path.write_text(json.dumps(initial,indent=2)+'\n',encoding='utf-8')
    if data.get('timeline'):
        hidden=workspace.parent/'evaluator'/'hidden-fixtures'; hidden.mkdir(parents=True,exist_ok=True)
        write_json(hidden/f'{fixture}-releases.json',data['timeline'])
    seed_dir=workspace/'runtime'/'qualification-bootstrap'; seed_dir.mkdir(parents=True,exist_ok=True)
    facts_path=seed_dir/f'{fixture}-facts.json'; facts_path.write_text(json.dumps(bootstrap,indent=2)+'\n',encoding='utf-8')
    boot=_run([
        sys.executable,str(product_root/'scripts/bootstrap_explicit_context.py'),bid,
        '--facts-file',str(facts_path),'--source-file',str(source_path),
        '--source-reference',f'qualification fixture {fixture}','--initialization-only'
    ],product_root,env)
    validation=_run([sys.executable,str(product_root/'scripts/validate_business.py'),bid,'--require-context'],product_root,env)
    audit={'fixture':fixture,'business_id':bid,'source_path':str(source_path),'facts_path':str(facts_path),'future_evidence_hidden':bool(data.get('timeline')),'bootstrapped_at':now(),
           'bootstrap_stdout':boot.stdout,'bootstrap_stderr':boot.stderr,'validation_stdout':validation.stdout,'validation_stderr':validation.stderr}
    write_json(seed_dir/f'{fixture}-bootstrap-audit.json',audit)
    return bid

def instructions(product_root,run_dir,workspace,events):
    return f'''# AURA Qualification Gauntlet — Candidate Instructions

You are operating ViralTrac AURA as a real business tool. This is an uninterrupted qualification run, not a discussion or architecture review.

Product root: `{product_root}`
External qualification workspace: `{workspace}`
Qualification run directory: `{run_dir}`
Queue: `{run_dir/'candidate/queue.json'}`

Set/retain these environment variables for all work:

```bash
export BUSINESSOS_WORKSPACE='{workspace}'
export AURA_QUALIFICATION_RUN='{run_dir}'
```

The benchmark businesses have already been initialized and their explicit starting context has been grounded into canonical AURA state. Their current controlled first-party evidence is available at `attachments/qualification-inputs/<fixture>.json`. Treat that file as supplied first-party evidence for the qualification business; ingest/persist relevant evidence through normal AURA processes as the event requires. Do not redo onboarding or ask for basic benchmark facts already present in canonical state or the supplied fixture. Later-period evidence is deliberately withheld until an event explicitly releases it; do not inspect evaluator/hidden files.

Process every queue event in order and continue directly to the next event. Do not stop between events to ask whether to continue. A genuine blocker should be recorded for that event, then continue with later events when safe.

For EVERY event:
1. Read the event, the controlled current fixture for that event, existing accumulated AURA state, and relevant AURA contract/process material. Do not modify canonical AURA product source.
2. Run `python3 qualification/checkpoint.py <EVENT_ID> before --business-id <BUSINESS_ID>` before doing event work.
3. If the event has a `release_fixture` field, run `python3 qualification/release_fixture.py <EVENT_ID>` now. This simulates new evidence arriving after the before-checkpoint. Use the released path as new supplied evidence and preserve its provenance.
4. Execute the business work fully using controlled evidence, accumulated AURA state, and legitimate current research/tool access. Do **not** invent a missing business condition or easy synthetic scenario merely to make the contract pass. If the required controlled input is absent and cannot legitimately be obtained from current research or accumulated state, record a blocker with classification `qualification_fixture`; that means the benchmark needs enrichment, not that AURA passed or failed. If AURA says an artifact is creatable, create the actual artifact; a description, outline, or proposed version is not a substitute unless that is the contract's promised output.
5. Where the competitive environment is material, inspect it. For SEO/AEO inspect current leaders/surfaces and compare multiple leaders; for ads use relevant transparency/creative centers and landing paths; for organic content use visible performance proxies and normalize them when possible. Treat proxies as proxies, not proof of profit or causality. Save enough timestamped source/evidence references in `field_snapshot_refs` that a reviewer can reconstruct the competitive field you evaluated.
6. Aim for outcome readiness: do the research, competitive analysis, strategy, execution, QA, integration, and measurement preparation a strong practitioner would reasonably expect to maximize the intended business result.
7. Follow AURA evidence, provenance, semantic ownership, authorization, required-subcontract, customer-facing claim, and completion rules. Never report a draft as executed or an unmeasured result as proven.
8. Persist the real business result and state through AURA. Reuse existing evidence/state instead of redoing work without reason.
9. Write the event receipt to the exact `receipt_path` relative to the qualification run directory. It must be JSON with: `event_id`, `business_id`, `status` (`completed` or `blocked`), `root_run_ids`, `artifact_refs`, `canonical_refs`, `source_refs`, `field_snapshot_refs`, `released_fixture_refs`, `summary`, `blocker` (null if completed; otherwise an object with `classification` and `detail`), and `quality_notes`. Valid blocker classifications are `external_capability`, `authorization`, `missing_required_data`, `external_service`, `qualification_fixture`, or `aura_process`.
10. Run `python3 qualification/checkpoint.py <EVENT_ID> after --business-id <BUSINESS_ID>` after the receipt and AURA work are persisted.
11. Immediately continue to the next queue item.

There are {len(events)} events in this run. Completion means the queue is exhausted, not merely that one event succeeded.
'''

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--profile',choices=['atomic','domains','cross-domain','marathon','full'],default='full'); ap.add_argument('--domain'); ap.add_argument('--run-root'); ap.add_argument('--run-id'); a=ap.parse_args()
    suite=build(); run_id=a.run_id or ('aura-qualification-'+uuid.uuid4().hex[:10]); root=Path(a.run_root).expanduser().resolve() if a.run_root else Path(tempfile.gettempdir())/'aura-qualification-runs'; run_dir=root/run_id
    if run_dir.exists(): raise SystemExit(f'Run already exists: {run_dir}')
    try:
        run_dir.relative_to(ROOT.resolve()); raise SystemExit('Qualification run root must be outside the AURA product tree to prevent recursive staging or product contamination')
    except ValueError:
        pass
    product_root=copy_product(ROOT,run_dir/'product'); _run([sys.executable,str(product_root/'scripts/generate_registry.py')],product_root,dict(os.environ)); workspace=run_dir/'workspace'; workspace.mkdir(parents=True); (run_dir/'candidate').mkdir(); (run_dir/'evaluator').mkdir(); (run_dir/'candidate-results').mkdir(); (run_dir/'checkpoints').mkdir()
    fixtures={t['fixture'] for t in suite['contract_tests']}|{m['fixture'] for k in ('domain_missions','cross_domain_missions','marathon_missions') for m in suite[k]}
    for f in sorted(fixtures): init_business(product_root,workspace,f)
    events=[]
    if a.profile in ('atomic','full'):
        for t in suite['contract_tests']:
            if not a.domain or t['owner_system']==a.domain: events.append(event_from_contract(t))
    if a.profile in ('domains','full'):
        events += [event_from_mission(m,'domain_mission') for m in suite['domain_missions'] if not a.domain or m['owner_system']==a.domain]
    if a.profile in ('cross-domain','full'): events += [event_from_mission(m,'cross_domain_mission') for m in suite['cross_domain_missions']]
    if a.profile in ('marathon','full'): events += [event_from_mission(m,'marathon_mission') for m in suite['marathon_missions']]
    queue={'format_version':'1.0','run_id':run_id,'created_at':now(),'profile':a.profile,'domain_filter':a.domain,'event_count':len(events),'events':events}
    write_json(run_dir/'candidate/queue.json',queue); write_json(run_dir/'evaluator/suite.json',suite); write_json(run_dir/'run.json',{'run_id':run_id,'created_at':now(),'product_root':str(product_root),'workspace':str(workspace),'profile':a.profile,'event_count':len(events),'status':'prepared','benchmark_context_seeded':True,'future_evidence_staged':True})
    (run_dir/'candidate/RUN-INSTRUCTIONS.md').write_text(instructions(product_root,run_dir,workspace,events),encoding='utf-8')
    print(json.dumps({'run_id':run_id,'run_dir':str(run_dir),'product_root':str(product_root),'workspace':str(workspace),'event_count':len(events),'instructions':str(run_dir/'candidate/RUN-INSTRUCTIONS.md'),'queue':str(run_dir/'candidate/queue.json')},indent=2))
if __name__=='__main__': main()
