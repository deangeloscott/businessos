#!/usr/bin/env python3
from pathlib import Path
import inspect, json, os, subprocess, sys, tempfile
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'qualification'))
from build_suite import build
from prepare_run import init_business, copy_product, apply_candidate_request, candidate_surface, _ensure_separate, select_events
from checkpoint import capture_checkpoint
from release_fixture import release_event
from common import fixture_for


def req(c,m):
    if not c: raise AssertionError(m)


def smoke_prepare():
    with tempfile.TemporaryDirectory(prefix='aura-qualification-smoke-') as td, tempfile.TemporaryDirectory(prefix='aura-workspaces-smoke-') as cd:
        selected=['content.intelligence.creator-monitoring','content.production.article']
        cmd=[sys.executable,str(ROOT/'qualification/prepare_run.py'),'--profile','atomic','--domain','content-synthesis','--run-root',td,'--candidate-root',cd,'--run-id','smoke']
        for cid in selected: cmd += ['--contract',cid]
        prep_env=dict(os.environ); prep_env['PYTHONUTF8']='0'; prep_env['PYTHONDONTWRITEBYTECODE']='1'
        p=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,env=prep_env)
        req(p.returncode==0,f'qualification prepare smoke failed:\nSTDOUT:\n{p.stdout}\nSTDERR:\n{p.stderr}')
        rd=Path(td)/'smoke'; meta=json.loads((rd/'run.json').read_text()); evaluator_queue=json.loads((rd/'evaluator/queue.json').read_text()); prep=json.loads((rd/'evaluator/preparation.json').read_text())
        product=Path(meta['product_root']); workspace=Path(meta['workspace']); surface=Path(meta['candidate_surface_root'])
        pointer=product/'.businessos/workspace.json'
        req(pointer.exists(),'staged candidate product must be persistently bound to its external organization workspace')
        pointer_data=json.loads(pointer.read_text())
        req(Path(pointer_data.get('workspace_root','')).resolve()==workspace.resolve(),'staged candidate workspace pointer does not resolve to the prepared workspace')
        req(meta.get('candidate_blind') is True and prep.get('candidate_blind') is True,'prepared qualification must explicitly record blind-candidate mode')
        req(meta.get('benchmark_context_seeded') is True,'prepared run must record grounded benchmark context')
        req(product.parent==surface and workspace.parent==surface,'candidate product/workspace must share only the neutral candidate surface')
        req(rd not in product.parents and rd not in workspace.parents and surface not in rd.parents,'candidate surface and evaluator run tree must be physically separate')
        req(not (surface/'evaluator').exists() and not (surface/'checkpoints').exists(),'evaluator/checkpoint state leaked into candidate surface')
        req('qualification' not in product.as_posix().lower() and 'qualification' not in workspace.as_posix().lower(),'candidate-visible paths reveal qualification intent')
        events=evaluator_queue.get('events',[]); req(evaluator_queue.get('event_count')==len(selected) and len(events)==len(selected),f'representative evaluator queue count mismatch: {events}')
        req(all(str(x.get('event_id','')).startswith('TASK-') for x in events),'evaluator tasks should use opaque external task IDs')
        req({x.get('contract_id') for x in events}==set(selected),'evaluator queue lost target contracts')
        req(evaluator_queue.get('contract_filter')==sorted(selected) and prep.get('contract_filter')==sorted(selected),'evaluator metadata must preserve exact representative contract filter')
        req('contract_filter' not in meta,'run metadata exposed exact contract filter unnecessarily')

        # The model receives the real runtime product, not any qualification/test tooling.
        req(not (product/'tests').exists(),'developer tests leaked into staged product')
        req(not (product/'qualification').exists(),'qualification machinery leaked into staged product')
        req(not (rd/'candidate').exists(),'candidate-visible qualification directory should not exist')
        req((ROOT/'qualification/task_controller.py').exists(),'external blind task controller missing')
        for page in [product/'PLAYBOOK-INDEX.md',product/'PLAYBOOKS.md',*(product/'docs/playbooks').rglob('*.md')]: page.read_text(encoding='utf-8')

        # Only fixtures required by selected work should be initialized, using normal-looking supplied-material paths.
        supplied=workspace/'attachments/supplied/atlasops-saas.json'; req(supplied.exists(),'selected AtlasOps supplied material missing')
        data=json.loads(supplied.read_text()); req('timeline' not in data,'future timeline leaked into initial supplied material')
        req(not (workspace/'attachments/qualification-inputs').exists(),'qualification-named input directory leaked into candidate workspace')
        req(not (workspace/'runtime/qualification-bootstrap').exists(),'qualification bootstrap internals leaked into candidate workspace')
        req((rd/'evaluator/bootstrap/atlasops-saas-bootstrap-audit.json').exists(),'maintainer-side bootstrap audit missing')
        req(not (workspace/'instances/harbor-hvac').exists() and not (workspace/'instances/northline-coffee').exists(),'unrelated benchmark businesses were initialized for an AtlasOps-only representative run')
        req((rd/'evaluator/hidden-fixtures/atlasops-saas-releases.json').exists(),'selected AtlasOps future evidence was not staged evaluator-side')

        # Controller start takes the hidden before checkpoint and prints only an ordinary request for the candidate.
        start=subprocess.run([sys.executable,str(ROOT/'qualification/task_controller.py'),'start',str(rd)],cwd=ROOT,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
        req(start.returncode==0,f'blind controller start failed: {start.stdout}\n{start.stderr}')
        started=json.loads(start.stdout); msg=started.get('candidate_message','').lower()
        req(msg and 'qualification' not in msg and 'checkpoint' not in msg and 'receipt' not in msg and 'scoring' not in msg,'candidate request contains test-taking language')
        req(all(cid.lower() not in msg for cid in selected),'candidate request leaked selected contract ID')
        req(Path(started.get('product_root',''))==product and Path(started.get('workspace',''))==workspace,'controller changed candidate surface paths')
        eid=events[0]['event_id']; req((rd/'checkpoints'/eid/'before.json').exists(),'controller did not take evaluator-side before checkpoint')

        # Ordinary staged-product mechanics must resolve the prepared external
        # workspace without requiring the candidate to reconstruct maintainer-only
        # environment variables. A playbook-linked Run is an optional one-way work
        # receipt; it must not recreate a subcontract/execution manifest.
        env=dict(os.environ)
        env.pop('BUSINESSOS_WORKSPACE',None)
        env.pop('BUSINESSOS_WORKSPACE_CONFIG',None)
        env['PYTHONDONTWRITEBYTECODE']='1'
        create=subprocess.run([sys.executable,str(product/'scripts/create_run.py'),'atlasops','core.intelligence.ecosystem-radar','external controller smoke'],cwd=product,env=env,capture_output=True,text=True)
        req(create.returncode==0,f'optional create_run smoke failed: {create.stdout}\n{create.stderr}')
        rid=create.stdout.strip().splitlines()[-1]; run_path=workspace/'runtime/runs/atlasops'/rid/'run.json'; req(run_path.exists(),'create_run smoke did not persist optional work receipt')
        state=json.loads(run_path.read_text()); continuity=state.get('continuity') or []
        req(state.get('method_type')=='aura_playbook' and state.get('method_ref')=='core.intelligence.ecosystem-radar' and state.get('contract_id')=='core.intelligence.ecosystem-radar','playbook-linked receipt lost truthful method provenance')
        req((state.get('continuity') or {}).get('purpose')=='organizational_work_receipt','staged product receipt lost organizational continuity purpose')
        req(not (workspace/'runtime/runs/atlasops'/rid/'contract-execution.json').exists(),'optional receipt recreated retired contract-execution manifest')
        req('required_subcontracts' not in state,'optional receipt recreated subcontract execution ledger state')

        # Timed evidence is released by maintainer tooling after the external before checkpoint and appears as normal supplied business evidence.
        synthetic={'event_id':'TASK-RELEASE','evaluation_id':'SMOKE-RELEASE','kind':'cross_domain_mission','business_id':'atlasops','fixture':'atlasops-saas','contract_id':None,'task':'Use the new business update to reassess the situation.','release_fixture':'later_period','receipt_path':'evaluator/receipts/TASK-RELEASE.json'}
        evaluator_queue['events']=[synthetic]; evaluator_queue['event_count']=1; (rd/'evaluator/queue.json').write_text(json.dumps(evaluator_queue,indent=2)+'\n')
        capture_checkpoint(product,workspace,rd,'TASK-RELEASE','before','atlasops')
        released,_=release_event(rd,'TASK-RELEASE'); req(released.exists(),'maintainer timed release did not create supplied evidence')
        rel=json.loads(released.read_text()); req(rel.get('source_type')=='business_supplied_update' and rel.get('evidence'),'timed release did not look like ordinary supplied business evidence')
        req('qualification_event_id' not in rel and 'fixture' not in rel and 'release_fixture' not in rel,'candidate-visible release payload leaked benchmark metadata')


def composition_prepare_smoke():
    with tempfile.TemporaryDirectory(prefix='aura-composition-smoke-') as td, tempfile.TemporaryDirectory(prefix='aura-workspaces-compose-') as cd:
        p=subprocess.run([
            sys.executable,str(ROOT/'qualification/prepare_run.py'),'--profile','composition',
            '--run-root',td,'--candidate-root',cd,'--run-id','compose-smoke'
        ],cwd=ROOT,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
        req(p.returncode==0,f'composition qualification preparation failed:\nSTDOUT:\n{p.stdout}\nSTDERR:\n{p.stderr}')
        rd=Path(td)/'compose-smoke'; meta=json.loads((rd/'run.json').read_text()); queue=json.loads((rd/'evaluator/queue.json').read_text())
        events=queue.get('events',[])
        req(meta.get('profile')=='composition' and queue.get('profile')=='composition','composition profile was not preserved')
        req(len(events)==1 and events[0].get('kind')=='composition_mission','composition profile must prepare the targeted composition mission')
        req(events[0].get('evaluation_id')=='COMPOSE-SEO-CONTENT-001','unexpected composition mission selected')
        req(events[0].get('contract_id') is None,'composition mission must not masquerade as one atomic contract')
        req({'evidence_reuse','execution_completeness'} <= set(events[0].get('rubric_dimensions') or []),'composition mission must judge state/evidence compounding and real execution')
        msg=str(events[0].get('task','')).lower()
        req('qualification' not in msg and 'rubric' not in msg and 'score' not in msg,'composition candidate task leaked evaluator framing')


def mission_prepare_smoke():
    mission='CROSS-MARKET-CHANGE-001'
    with tempfile.TemporaryDirectory(prefix='aura-mission-smoke-') as td, tempfile.TemporaryDirectory(prefix='aura-workspaces-mission-') as cd:
        p=subprocess.run([
            sys.executable,str(ROOT/'qualification/prepare_run.py'),'--profile','cross-domain','--mission',mission,
            '--run-root',td,'--candidate-root',cd,'--run-id','mission-smoke'
        ],cwd=ROOT,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
        req(p.returncode==0,f'exact mission qualification preparation failed:\nSTDOUT:\n{p.stdout}\nSTDERR:\n{p.stderr}')
        result=json.loads(p.stdout); rd=Path(td)/'mission-smoke'; meta=json.loads((rd/'run.json').read_text()); queue=json.loads((rd/'evaluator/queue.json').read_text()); prep=json.loads((rd/'evaluator/preparation.json').read_text())
        events=queue.get('events',[])
        req(result.get('event_count')==1 and meta.get('event_count')==1 and queue.get('event_count')==1 and len(events)==1,'exact mission selector must prepare exactly one event')
        event=events[0]
        req(event.get('evaluation_id')==mission and event.get('event_id')=='TASK-0001','exact mission evaluator mapping must retain one hidden mission ID behind an opaque task ID')
        req(event.get('kind')=='cross_domain_mission' and event.get('contract_id') is None,'exact cross-domain mission selected the wrong event kind')
        req(queue.get('mission_filter')==mission and prep.get('mission_filter')==mission,'evaluator preparation metadata must preserve the exact mission filter')
        req('mission_filter' not in meta,'candidate-visible run metadata exposed the exact mission filter unnecessarily')
        req(mission.lower() not in str(event.get('task','')).lower(),'ordinary mission request leaked the hidden mission ID')

        start=subprocess.run([sys.executable,str(ROOT/'qualification/task_controller.py'),'start',str(rd)],cwd=ROOT,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
        req(start.returncode==0,f'exact mission controller start failed: {start.stdout}\n{start.stderr}')
        started=json.loads(start.stdout); visible=json.dumps(started).lower()
        req(started.get('candidate_message')==event.get('task'),'candidate must receive only the ordinary mission business request')
        req(mission.lower() not in visible and 'evaluation_id' not in visible and 'mission_filter' not in visible,'candidate controller payload leaked the hidden mission selector')


def judge_prompt_smoke():
    with tempfile.TemporaryDirectory(prefix='aura-judge-prompt-') as td:
        rd=Path(td); ev=rd/'evaluator'; ev.mkdir()
        (ev/'review-packets.json').write_text(json.dumps([{'event_id':'TASK-0001','hard_pass':True,'rubric_dimensions':['accuracy']}])+'\n')
        p=subprocess.run([sys.executable,str(ROOT/'qualification/build_judge_prompt.py'),str(rd)],cwd=ROOT,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
        req(p.returncode==0,f'judge prompt generation failed:\nSTDOUT:\n{p.stdout}\nSTDERR:\n{p.stderr}')
        instructions=(ev/'JUDGE-INSTRUCTIONS.md').read_text(encoding='utf-8')
        req('Treat **5 as rare**' in instructions,'judge prompt must calibrate exceptional scores as rare')
        req('Distinguish relevance from proof' in instructions,'judge prompt must prohibit upgrading relevance/proxies into stronger claims')
        req('direct page read' in instructions and 'top-ranking result' in instructions,'judge prompt must explicitly scrutinize unsupported observation/ranking claims')


def main():
    # Qualification philosophy and longitudinal record are durable maintainer state, not candidate content.
    principles=ROOT/'qualification/PRINCIPLES.md'; ledger=ROOT/'qualification/ledger.jsonl'; qreadme=ROOT/'qualification/README.md'
    req(principles.is_file() and ledger.is_file(),'qualification principles/ledger missing')
    req('PRINCIPLES.md' in qreadme.read_text(encoding='utf-8'),'qualification README must route maintainers to the authoritative principles')
    for i,line in enumerate(ledger.read_text(encoding='utf-8').splitlines(),1):
        if line.strip():
            try: json.loads(line)
            except json.JSONDecodeError as e: raise AssertionError(f'qualification ledger line {i} is not valid JSON: {e}')

    # Maintainers may supply a realistic ordinary request for one hidden target without exposing test machinery.
    target='seo.intelligence.organic-competition.page-analysis'; ordinary='Analyze a strong current organic page for a valuable AtlasOps search intent and identify the material gaps for our business.'
    customized=apply_candidate_request([{'contract_id':target,'task':'generic'}],ordinary)
    req(customized[0]['task']==ordinary,'maintainer-authored ordinary request was not preserved')
    try: apply_candidate_request([{'contract_id':target,'task':'a'},{'contract_id':'other','task':'b'}],ordinary)
    except ValueError: pass
    else: raise AssertionError('maintainer-authored request must require exactly one hidden event')
    try: apply_candidate_request([{'contract_id':target,'task':'a'}],f'Execute {target}')
    except ValueError: pass
    else: raise AssertionError('maintainer-authored request must not expose hidden target contract id')
    hidden_mission='CROSS-MARKET-CHANGE-001'
    mission_customized=apply_candidate_request([{'contract_id':None,'evaluation_id':hidden_mission,'task':'generic'}],ordinary)
    req(mission_customized[0]['task']==ordinary,'ordinary request for a hidden mission was not preserved')
    try: apply_candidate_request([{'contract_id':None,'evaluation_id':hidden_mission,'task':'generic'}],f'Execute {hidden_mission}')
    except ValueError as e: req('hidden target mission id' in str(e),'hidden mission request rejection was unclear')
    else: raise AssertionError('maintainer-authored request must not expose hidden target mission id')

    # Candidate-visible paths must be neutral and physically separate from evaluator state.
    with tempfile.TemporaryDirectory(prefix='aura-workspaces-unit-') as cd, tempfile.TemporaryDirectory(prefix='aura-evaluator-unit-') as ed:
        surface=candidate_surface(cd); req('qualification' not in surface.as_posix().lower(),'neutral candidate surface leaked qualification marker')
        req(_ensure_separate(surface,Path(ed)/'run') is True,'separate candidate/evaluator trees should be accepted')
        try: _ensure_separate(Path(ed)/'run'/'candidate',Path(ed)/'run')
        except ValueError: pass
        else: raise AssertionError('candidate surface nested under evaluator tree must be rejected')

    suite=build(); manifest=json.loads((ROOT/'SYSTEM-MANIFEST.json').read_text())
    expected=manifest.get('counts',{}).get('contract_count') or manifest.get('contract_count'); expected_caps=manifest.get('capability_count')
    req(suite['contract_count']==expected,f"qualification coverage {suite['contract_count']} != manifest {expected}")
    ids=[t['contract_id'] for t in suite['contract_tests']]; req(suite['capability_count']==expected_caps,f"qualification capability coverage {suite['capability_count']} != manifest {expected_caps}")
    req(len(suite['capability_coverage'])==expected_caps,'every declared capability needs a qualification mapping')
    req(len(ids)==len(set(ids)),'duplicate contract qualification tests')
    req(all(not t['unknown_required_subcontracts'] for t in suite['contract_tests']),'unknown required subcontracts in qualification suite')
    req(all(t['hard_gates'] and t['rubric_dimensions'] and t['candidate_task'] for t in suite['contract_tests']),'every contract needs gates, rubric, and candidate task')
    req(all('execute aura contract' not in t['candidate_task'].lower() and t['contract_id'].lower() not in t['candidate_task'].lower() for t in suite['contract_tests']),'contract acceptance requests must be production-like and hide target contract ids')
    req(fixture_for('content.production.article','content-synthesis')=='atlasops-saas','fixture router must not mistake production for ecommerce product work')
    req(fixture_for('seo-aeo.execution.product-page','seo-aeo')=='northline-commerce','fixture router must still map explicit product work to ecommerce')
    req(fixture_for('seo-aeo.local.service-area','seo-aeo')=='harbor-hvac','fixture router must still map explicit local/service-area work to HVAC')
    ecosystem=next(t for t in suite['contract_tests'] if t['contract_id']=='core.intelligence.ecosystem-radar')
    req(ecosystem['required_subcontracts'] and all(isinstance(x,str) for x in ecosystem['required_subcontracts']),'qualification suite must normalize object-form subcontract metadata to ids')
    customer=[t for t in suite['contract_tests'] if t.get('artifact_role')=='customer_facing_production_root']; req(customer,'expected customer-facing production contracts')
    req(all(t['output_policy']['artifact_required'] and 'actual_artifact_exists' in t['hard_gates'] for t in customer),'customer-facing roots must require actual artifacts')
    owners={m['owner_system'] for m in suite['domain_missions']}; required={'core','customer-intelligence','competitor-intelligence','industry-intelligence','seo-aeo','content-synthesis','marketing-synthesis','customer-optimization'}; req(owners==required,f'domain mission coverage mismatch: {owners ^ required}')
    composition=suite.get('composition_missions',[]); req(composition and {m['id'] for m in composition}=={'COMPOSE-SEO-CONTENT-001'},'targeted composition mission missing or ambiguous')
    compose_events=select_events(suite,'composition'); req(len(compose_events)==1 and compose_events[0]['kind']=='composition_mission','composition event selection failed')
    req({'evidence_reuse','execution_completeness'} <= set(compose_events[0].get('rubric_dimensions') or []),'composition rubric must evaluate compounding and execution')
    exact_missions=(
        ('composition','COMPOSE-SEO-CONTENT-001','composition_mission'),
        ('domains','DOMAIN-SEO-AEO-001','domain_mission'),
        ('cross-domain','CROSS-MARKET-CHANGE-001','cross_domain_mission'),
        ('marathon','MARATHON-002','marathon_mission'),
    )
    for profile,mission_id,kind in exact_missions:
        selected=select_events(suite,profile,mission_id=mission_id)
        req(len(selected)==1 and selected[0].get('event_id')==mission_id and selected[0].get('kind')==kind,f'exact mission selection failed for {profile}: {selected}')
    try: select_events(suite,'cross-domain',mission_id='CROSS-UNKNOWN-999')
    except SystemExit as e: req('Unknown qualification mission filter' in str(e),'unknown mission rejection was unclear')
    else: raise AssertionError('unknown mission selector must be rejected')
    try: select_events(suite,'marathon',mission_id='CROSS-MARKET-CHANGE-001')
    except SystemExit as e: req('does not belong to --profile marathon' in str(e),'mission/profile mismatch rejection was unclear')
    else: raise AssertionError('mission outside the selected profile must be rejected')
    try: select_events(suite,'cross-domain',contract_ids=[target],mission_id='CROSS-MARKET-CHANGE-001')
    except SystemExit as e: req('--contract and --mission cannot be used together' in str(e),'contract/mission ambiguity rejection was unclear')
    else: raise AssertionError('--contract and --mission must not be mixed')
    req(len(suite['cross_domain_missions'])>=5 and len(suite['marathon_missions'])>=2,'mission coverage too small')
    req('concurrency_missions' not in suite,'deferred concurrency qualification should not remain in the active suite')
    req(not (ROOT/'qualification/prepare_concurrency.py').exists() and not (ROOT/'qualification/launch_concurrent.py').exists(),'deferred concurrency mini-framework should not remain alongside the blind qualification path')
    mission_text=' '.join(m.get('task','') for key in ('composition_missions','domain_missions','cross_domain_missions','marathon_missions') for m in suite.get(key,[])).lower()
    retired_phrases=('action package','execution receipt','complete its run','complete their run','authorized work through execution','authorization, action planning')
    req(not any(x in mission_text for x in retired_phrases),'candidate-visible mission text reintroduced retired execution-control architecture')
    req([t for t in suite['contract_tests'] if t['competitive_profile']=='search_live_field'],'SEO/AEO live-field tests missing')
    req([t for t in suite['contract_tests'] if t['competitive_profile']=='paid_and_persuasion_field'],'competitive marketing tests missing')
    fixture_paths=sorted((ROOT/'qualification/fixtures').glob('*.json')); req(fixture_paths,'qualification fixtures missing')
    for p in fixture_paths:
        f=json.loads(p.read_text()); req(isinstance(f.get('bootstrap_facts'),dict) and f['bootstrap_facts'],f'{p.name}: bootstrap_facts required'); req(not str(f.get('business_id','')).startswith('qa-'),f'{p.name}: candidate business id leaks qualification marker')
    seed_source=inspect.getsource(init_business)
    req('bootstrap_explicit_context.py' in seed_source and '--require-context' in seed_source,'qualification preparation must ground fixture context canonically and validate context')
    # Actual withholding behavior is proven in smoke_prepare(): the candidate-visible supplied JSON has no timeline while evaluator hidden-fixtures retains it. Avoid asserting one exact Python-comprehension spelling here.
    req('hidden-fixtures' in seed_source and 'timeline' in seed_source,'qualification preparation must preserve a hidden later-period evidence path')
    req((ROOT/'qualification/release_fixture.py').exists() and (ROOT/'qualification/task_controller.py').exists(),'external qualification controller/release tooling missing')
    released=[m for m in suite['cross_domain_missions']+suite['marathon_missions'] if m.get('release_fixture')]
    req(len(released)>=2 and {'CROSS-MARKET-CHANGE-001','MARATHON-002'}.issubset({m['id'] for m in released}),'expected longitudinal evidence-release missions missing')
    smoke_prepare(); composition_prepare_smoke(); mission_prepare_smoke(); judge_prompt_smoke()
    print(f"qualification framework regressions passed: {suite['contract_count']} contract tests, {suite['capability_count']} capability mappings, durable principles/ledger, targeted composition profile, exact blind mission selection, calibrated professional judge, physically isolated blind candidate staging, external checkpoints/receipts/releases, selected-fixture preparation, and production-like optional receipt smoke passed")

if __name__=='__main__': main()
