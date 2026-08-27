#!/usr/bin/env python3
from pathlib import Path
import inspect, json, os, subprocess, sys, tempfile
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'qualification'))
from build_suite import build
from prepare_run import init_business, copy_product
from checkpoint import capture_checkpoint
from release_fixture import release_event


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
        rd=Path(td)/'smoke'; meta=json.loads((rd/'run.json').read_text()); evaluator_queue=json.loads((rd/'evaluator/queue.json').read_text()); prep=json.loads((rd/'evaluator/preparation.json').read_text())
        req(meta.get('candidate_blind') is True and prep.get('candidate_blind') is True,'prepared qualification must explicitly record blind-candidate mode')
        req(meta.get('benchmark_context_seeded') is True,'prepared run must record grounded benchmark context')
        events=evaluator_queue.get('events',[]); req(evaluator_queue.get('event_count')==len(selected) and len(events)==len(selected),f'representative evaluator queue count mismatch: {events}')
        req(all(str(x.get('event_id','')).startswith('TASK-') for x in events),'evaluator tasks should use opaque external task IDs')
        req({x.get('contract_id') for x in events}==set(selected),'evaluator queue lost target contracts')
        req(evaluator_queue.get('contract_filter')==sorted(selected) and prep.get('contract_filter')==sorted(selected),'evaluator metadata must preserve exact representative contract filter')
        req('contract_filter' not in meta,'run metadata exposed exact contract filter unnecessarily')

        # The model receives the real runtime product, not any qualification/test tooling.
        product=rd/'product'
        req(not (product/'tests').exists(),'developer tests leaked into staged product')
        req(not (product/'qualification').exists(),'qualification machinery leaked into staged product')
        req(not (rd/'candidate').exists(),'candidate-visible qualification directory should not exist')
        req((ROOT/'qualification/task_controller.py').exists(),'external blind task controller missing')
        for page in [product/'PLAYBOOK-INDEX.md',product/'PLAYBOOKS.md',*(product/'docs/playbooks').rglob('*.md')]: page.read_text(encoding='utf-8')

        # Only fixtures required by selected work should be initialized, using normal-looking supplied-material paths.
        supplied=rd/'workspace/attachments/supplied/atlasops-saas.json'; req(supplied.exists(),'selected AtlasOps supplied material missing')
        data=json.loads(supplied.read_text()); req('timeline' not in data,'future timeline leaked into initial supplied material')
        req(not (rd/'workspace/attachments/qualification-inputs').exists(),'qualification-named input directory leaked into candidate workspace')
        req(not (rd/'workspace/runtime/qualification-bootstrap').exists(),'qualification bootstrap internals leaked into candidate workspace')
        req((rd/'evaluator/bootstrap/atlasops-saas-bootstrap-audit.json').exists(),'maintainer-side bootstrap audit missing')
        req(not (rd/'workspace/instances/harbor-hvac').exists() and not (rd/'workspace/instances/northline-coffee').exists(),'unrelated benchmark businesses were initialized for an AtlasOps-only representative run')
        req((rd/'evaluator/hidden-fixtures/atlasops-saas-releases.json').exists(),'selected AtlasOps future evidence was not staged evaluator-side')

        # Controller start takes the hidden before checkpoint and prints only an ordinary request for the candidate.
        start=subprocess.run([sys.executable,str(ROOT/'qualification/task_controller.py'),'start',str(rd)],cwd=ROOT,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
        req(start.returncode==0,f'blind controller start failed: {start.stdout}\n{start.stderr}')
        started=json.loads(start.stdout); msg=started.get('candidate_message','').lower()
        req(msg and 'qualification' not in msg and 'checkpoint' not in msg and 'receipt' not in msg and 'scoring' not in msg,'candidate request contains test-taking language')
        req(all(cid.lower() not in msg for cid in selected),'candidate request leaked selected contract ID')
        eid=events[0]['event_id']; req((rd/'checkpoints'/eid/'before.json').exists(),'controller did not take evaluator-side before checkpoint')

        # Ordinary product mechanics still work with only BUSINESSOS_WORKSPACE exposed to the runtime.
        env=dict(os.environ); env['BUSINESSOS_WORKSPACE']=meta['workspace']; env['PYTHONDONTWRITEBYTECODE']='1'
        create=subprocess.run([sys.executable,str(product/'scripts/create_run.py'),'atlasops','core.intelligence.ecosystem-radar','external controller smoke'],cwd=product,env=env,capture_output=True,text=True)
        req(create.returncode==0,f'create_run object-form subcontract smoke failed: {create.stdout}\n{create.stderr}')
        rid=create.stdout.strip().splitlines()[-1]; manifest=rd/'workspace/runtime/runs/atlasops'/rid/'contract-execution.json'; req(manifest.exists(),'create_run smoke did not persist contract-execution manifest')
        md=json.loads(manifest.read_text()); required=md.get('required_subcontracts') or []
        req(required and all(isinstance(x,str) for x in required),'create_run must normalize required subcontract metadata to contract-id strings')
        req('core.intelligence.ecosystem.source-discovery' in required,'object-form required subcontract id was not normalized into Run manifest')

        # Timed evidence is released by maintainer tooling after the external before checkpoint and appears as normal supplied business evidence.
        synthetic={'event_id':'TASK-RELEASE','evaluation_id':'SMOKE-RELEASE','kind':'cross_domain_mission','business_id':'atlasops','fixture':'atlasops-saas','contract_id':None,'task':'Use the new business update to reassess the situation.','release_fixture':'later_period','receipt_path':'evaluator/receipts/TASK-RELEASE.json'}
        evaluator_queue['events']=[synthetic]; evaluator_queue['event_count']=1; (rd/'evaluator/queue.json').write_text(json.dumps(evaluator_queue,indent=2)+'\n')
        capture_checkpoint(product,Path(meta['workspace']),rd,'TASK-RELEASE','before','atlasops')
        released,_=release_event(rd,'TASK-RELEASE'); req(released.exists(),'maintainer timed release did not create supplied evidence')
        rel=json.loads(released.read_text()); req(rel.get('source_type')=='business_supplied_update' and rel.get('evidence'),'timed release did not look like ordinary supplied business evidence')
        req('qualification_event_id' not in rel and 'fixture' not in rel and 'release_fixture' not in rel,'candidate-visible release payload leaked benchmark metadata')


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
    customer=[t for t in suite['contract_tests'] if t.get('artifact_role')=='customer_facing_production_root']; req(customer,'expected customer-facing production contracts')
    req(all(t['output_policy']['artifact_required'] and 'actual_artifact_exists' in t['hard_gates'] for t in customer),'customer-facing roots must require actual artifacts')
    owners={m['owner_system'] for m in suite['domain_missions']}; required={'core','customer-intelligence','competitor-intelligence','industry-intelligence','seo-aeo','content-synthesis','marketing-synthesis','customer-optimization'}; req(owners==required,f'domain mission coverage mismatch: {owners ^ required}')
    req(len(suite['cross_domain_missions'])>=5 and len(suite['marathon_missions'])>=2 and len(suite.get('concurrency_missions',[]))>=4,'mission coverage too small')
    req([t for t in suite['contract_tests'] if t['competitive_profile']=='search_live_field'],'SEO/AEO live-field tests missing')
    req([t for t in suite['contract_tests'] if t['competitive_profile']=='paid_and_persuasion_field'],'competitive marketing tests missing')
    fixture_paths=sorted((ROOT/'qualification/fixtures').glob('*.json')); req(fixture_paths,'qualification fixtures missing')
    for p in fixture_paths:
        f=json.loads(p.read_text()); req(isinstance(f.get('bootstrap_facts'),dict) and f['bootstrap_facts'],f'{p.name}: bootstrap_facts required'); req(not str(f.get('business_id','')).startswith('qa-'),f'{p.name}: candidate business id leaks qualification marker')
    seed_source=inspect.getsource(init_business)
    req('bootstrap_explicit_context.py' in seed_source and '--require-context' in seed_source,'qualification preparation must ground fixture context canonically and validate context')
    req("k!='timeline'" in seed_source and 'hidden-fixtures' in seed_source,'later-period evidence must be withheld from initial supplied inputs')
    req((ROOT/'qualification/release_fixture.py').exists() and (ROOT/'qualification/task_controller.py').exists(),'external qualification controller/release tooling missing')
    released=[m for m in suite['cross_domain_missions']+suite['marathon_missions'] if m.get('release_fixture')]
    req(len(released)>=2 and {'CROSS-MARKET-CHANGE-001','MARATHON-002'}.issubset({m['id'] for m in released}),'expected longitudinal evidence-release missions missing')
    smoke_prepare()
    print(f"qualification framework regressions passed: {suite['contract_count']} contract tests, {suite['capability_count']} capability mappings, blind candidate staging, external checkpoints/receipts/releases, selected-fixture preparation, and production-like run smoke passed")

if __name__=='__main__': main()
