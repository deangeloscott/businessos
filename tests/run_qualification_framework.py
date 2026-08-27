#!/usr/bin/env python3
from pathlib import Path
import inspect, json, os, subprocess, sys, tempfile
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'qualification'))
from build_suite import build
from prepare_run import init_business, copy_product

def req(c,m):
    if not c: raise AssertionError(m)

def smoke_prepare():
    with tempfile.TemporaryDirectory(prefix='aura-qualification-smoke-') as td:
        selected=['content.intelligence.creator-monitoring','content.production.article']
        cmd=[sys.executable,str(ROOT/'qualification/prepare_run.py'),'--profile','atomic','--domain','content-synthesis','--run-root',td,'--run-id','smoke']
        for cid in selected: cmd += ['--contract',cid]
        prep_env=dict(os.environ); prep_env['PYTHONUTF8']='0'; prep_env['PYTHONDONTWRITEBYTECODE']='1'
        p=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,env=prep_env)
        req(p.returncode==0,f'qualification prepare smoke failed:\nSTDOUT:\n{p.stdout}\nSTDERR:\n{p.stderr}')
        rd=Path(td)/'smoke'; meta=json.loads((rd/'run.json').read_text()); queue_path=rd/'candidate/queue.json'; queue=json.loads(queue_path.read_text())
        evaluator_queue=json.loads((rd/'evaluator/queue.json').read_text()); prep=json.loads((rd/'evaluator/preparation.json').read_text())
        req(meta.get('benchmark_context_seeded') is True,'prepared run must record grounded benchmark context')
        req(meta.get('future_evidence_staged') is True,'prepared run must record staged future evidence')
        events=queue.get('events',[])
        req(queue.get('event_count')==len(selected) and len(events)==len(selected),f'candidate representative smoke queue count mismatch: {events}')
        req(all(x.get('kind')=='business_task' and str(x.get('event_id','')).startswith('TASK-') for x in events),f'candidate queue should contain opaque ordinary business tasks: {events}')
        hidden_keys={'contract_id','evaluation_id','competitive_profile','required_output','rubric_dimensions'}
        req(all(not (hidden_keys & set(x)) for x in events),f'candidate queue leaked evaluator target metadata: {events}')
        req(all('execute aura contract' not in str(x.get('task','')).lower() for x in events),'candidate task must not tell the model to execute a qualification contract')
        req(all(not any(cid.lower() in str(x.get('task','')).lower() for cid in selected) for x in events),'candidate task leaked selected contract id')
        evaluator_contracts={x.get('contract_id') for x in evaluator_queue.get('events',[])}
        req(evaluator_contracts==set(selected),f'evaluator queue lost the hidden target contracts: {evaluator_contracts}')
        req(evaluator_queue.get('contract_filter')==sorted(selected) and prep.get('contract_filter')==sorted(selected),'evaluator metadata must preserve exact representative contract filter')
        req('contract_filter' not in queue and 'contract_filter' not in meta,'candidate-visible queue/run metadata must not expose contract filter')

        # The candidate must see the runtime product, not the maintainer test laboratory.
        product=rd/'product'
        req(not (product/'tests').exists(),'developer tests leaked into staged candidate product')
        req(not (product/'qualification/fixtures').exists(),'raw benchmark fixtures leaked into staged candidate product')
        allowed_helpers={'common.py','checkpoint.py','release_fixture.py','resume_status.py','RECOVERY.md'}
        qroot=product/'qualification'
        qfiles={p.relative_to(qroot).as_posix() for p in qroot.rglob('*') if p.is_file()} if qroot.exists() else set()
        req(qfiles <= allowed_helpers,f'candidate product leaked maintainer qualification files: {sorted(qfiles-allowed_helpers)}')
        req({'common.py','checkpoint.py','release_fixture.py'} <= qfiles,f'candidate product is missing required qualification helpers: {sorted({"common.py","checkpoint.py","release_fixture.py"}-qfiles)}')
        req(not (product/'qualification/evaluate_run.py').exists() and not (product/'qualification/integrity.py').exists(),'evaluator implementation leaked into staged candidate product')

        catalog_pages=[product/'PLAYBOOK-INDEX.md',product/'PLAYBOOKS.md',*(product/'docs/playbooks').rglob('*.md')]
        for page in catalog_pages:
            page.read_text(encoding='utf-8')
        for fixture in ('atlasops-saas','harbor-hvac','northline-commerce'):
            src=rd/'workspace/attachments/qualification-inputs'/f'{fixture}.json'; req(src.exists(),f'{fixture}: sanitized candidate fixture missing')
            data=json.loads(src.read_text()); req('timeline' not in data,f'{fixture}: future timeline leaked into initial candidate fixture')
            req((rd/'workspace/runtime/qualification-bootstrap'/f'{fixture}-bootstrap-audit.json').exists(),f'{fixture}: canonical bootstrap audit missing')
        req((rd/'evaluator/hidden-fixtures/atlasops-saas-releases.json').exists(),'AtlasOps later-period release not staged')
        req((rd/'evaluator/hidden-fixtures/harbor-hvac-releases.json').exists(),'Harbor HVAC later-period release not staged')
        env=dict(os.environ); env['BUSINESSOS_WORKSPACE']=meta['workspace']; env['AURA_QUALIFICATION_RUN']=str(rd); env['PYTHONDONTWRITEBYTECODE']='1'
        create=subprocess.run([sys.executable,str(product/'scripts/create_run.py'),'qa-atlasops-saas','core.intelligence.ecosystem-radar','qualification object-form subcontract smoke'],cwd=product,env=env,capture_output=True,text=True)
        req(create.returncode==0,f'create_run object-form subcontract smoke failed: {create.stdout}\n{create.stderr}')
        rid=create.stdout.strip().splitlines()[-1]; manifest=rd/'workspace/runtime/runs/qa-atlasops-saas'/rid/'contract-execution.json'
        req(manifest.exists(),'create_run smoke did not persist contract-execution manifest')
        md=json.loads(manifest.read_text()); required=md.get('required_subcontracts') or []
        req(required and all(isinstance(x,str) for x in required),'create_run must normalize required subcontract metadata to contract-id strings')
        req('core.intelligence.ecosystem.source-discovery' in required,'object-form required subcontract id was not normalized into the Run manifest')
        release_event={'event_id':'SMOKE-RELEASE','kind':'business_task','business_id':'qa-atlasops-saas','fixture':'atlasops-saas','release_fixture':'later_period','task':'smoke timed release','receipt_path':'candidate-results/SMOKE-RELEASE.json'}
        queue_path.write_text(json.dumps({'format_version':'1.1','run_id':'smoke','event_count':1,'events':[release_event]},indent=2)+'\n')
        before=subprocess.run([sys.executable,str(product/'qualification/checkpoint.py'),'SMOKE-RELEASE','before','--business-id','qa-atlasops-saas'],cwd=product,env=env,capture_output=True,text=True)
        req(before.returncode==0,f'timed release before-checkpoint failed: {before.stdout}\n{before.stderr}')
        release=subprocess.run([sys.executable,str(product/'qualification/release_fixture.py'),'SMOKE-RELEASE'],cwd=product,env=env,capture_output=True,text=True)
        req(release.returncode==0,f'timed release helper failed: {release.stdout}\n{release.stderr}')
        released=rd/'workspace/attachments/qualification-inputs/atlasops-saas-later_period.json'; req(released.exists(),'timed release did not create candidate-visible evidence')
        rel=json.loads(released.read_text()); req(rel.get('release_fixture')=='later_period' and rel.get('evidence'),'timed release payload invalid')

def main():
    suite=build(); manifest=json.loads((ROOT/'SYSTEM-MANIFEST.json').read_text())
    expected=manifest.get('counts',{}).get('contract_count') or manifest.get('contract_count'); expected_caps=manifest.get('capability_count')
    req(suite['contract_count']==expected,f"qualification coverage {suite['contract_count']} != manifest {expected}")
    ids=[t['contract_id'] for t in suite['contract_tests']]; req(suite['capability_count']==expected_caps,f"qualification capability coverage {suite['capability_count']} != manifest {expected_caps}")
    req(len(suite['capability_coverage'])==expected_caps,'every declared capability needs a qualification mapping')
    req(len(ids)==len(set(ids)),'duplicate contract qualification tests')
    req(all(not t['unknown_required_subcontracts'] for t in suite['contract_tests']),'unknown required subcontracts in qualification suite')
    req(all(t['hard_gates'] and t['rubric_dimensions'] and t['candidate_task'] for t in suite['contract_tests']),'every contract needs gates, rubric, and candidate task')
    req(all('execute aura contract' not in t['candidate_task'].lower() and t['contract_id'].lower() not in t['candidate_task'].lower() for t in suite['contract_tests']),'contract acceptance requests must be production-like and hide target contract ids')
    ecosystem=next(t for t in suite['contract_tests'] if t['contract_id']=='core.intelligence.ecosystem-radar')
    req(ecosystem['required_subcontracts'] and all(isinstance(x,str) for x in ecosystem['required_subcontracts']),'qualification suite must normalize object-form subcontract metadata to ids')
    customer=[t for t in suite['contract_tests'] if t.get('artifact_role')=='customer_facing_production_root']
    req(customer,'expected customer-facing production contracts')
    req(all(t['output_policy']['artifact_required'] and 'actual_artifact_exists' in t['hard_gates'] for t in customer),'customer-facing roots must require actual artifacts')
    owners={m['owner_system'] for m in suite['domain_missions']}; required={'core','customer-intelligence','competitor-intelligence','industry-intelligence','seo-aeo','content-synthesis','marketing-synthesis','customer-optimization'}
    req(owners==required,f'domain mission coverage mismatch: {owners ^ required}')
    req(len(suite['cross_domain_missions'])>=5,'cross-domain mission coverage too small')
    req(len(suite['marathon_missions'])>=2,'marathon mission coverage too small')
    req(len(suite.get('concurrency_missions',[]))>=4,'concurrency mission coverage too small')
    live=[t for t in suite['contract_tests'] if t['competitive_profile']=='search_live_field']; req(live,'SEO/AEO live-field tests missing')
    ads=[t for t in suite['contract_tests'] if t['competitive_profile']=='paid_and_persuasion_field']; req(ads,'competitive marketing tests missing')
    fixture_paths=sorted((ROOT/'qualification/fixtures').glob('*.json')); req(fixture_paths,'qualification fixtures missing')
    for p in fixture_paths:
        f=json.loads(p.read_text()); req(isinstance(f.get('bootstrap_facts'),dict) and f['bootstrap_facts'],f'{p.name}: bootstrap_facts required')
    seed_source=inspect.getsource(init_business)
    req('bootstrap_explicit_context.py' in seed_source and '--require-context' in seed_source,'qualification preparation must ground fixture context canonically and validate required context before Level-2 testing')
    req("k!='timeline'" in seed_source and 'hidden-fixtures' in seed_source,'later-period fixture evidence must be withheld from initial candidate inputs')
    req((ROOT/'qualification/release_fixture.py').exists(),'timed fixture release helper missing')
    released=[m for m in suite['cross_domain_missions']+suite['marathon_missions'] if m.get('release_fixture')]
    req(len(released)>=2 and {'CROSS-MARKET-CHANGE-001','MARATHON-002'}.issubset({m['id'] for m in released}),'expected longitudinal evidence-release missions missing')
    smoke_prepare()
    print(f"qualification framework regressions passed: {suite['contract_count']} contract tests, {suite['capability_count']} capability mappings, {len(suite['domain_missions'])} domain missions, {len(suite['cross_domain_missions'])} cross-domain missions, {len(suite['marathon_missions'])} marathon missions, {len(suite.get('concurrency_missions',[]))} concurrency missions, {len(fixture_paths)} grounded fixtures, {len(released)} timed evidence releases, production-like preparation/release/run-creation smoke passed")
if __name__=='__main__': main()
