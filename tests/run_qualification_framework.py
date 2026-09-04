#!/usr/bin/env python3
"""Regression checks for the real-work qualification harness.

Protect evaluator isolation, truthful ordinary requests, real-world use-case privacy,
real result observation, optional continuity, and capable professional review. Do not infer
task semantics from Workflow ids or make execution ledgers/composition shapes part of correctness.
"""
from pathlib import Path
import inspect,json,os,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'qualification'))
from build_suite import build
from prepare_run import init_business,apply_candidate_request,candidate_surface,_ensure_separate
from checkpoint import capture_checkpoint
from release_fixture import release_event
from common import fixture_for
sys.path.insert(0,str(ROOT/'scripts'))
from _common import workflow_files


def req(c,m):
    if not c:raise AssertionError(m)


def smoke_prepare():
    selected=['content.intelligence.creator-monitoring','content.production.article']
    with tempfile.TemporaryDirectory(prefix='aura-qualification-smoke-') as td,tempfile.TemporaryDirectory(prefix='aura-workspaces-smoke-') as cd:
        cmd=[sys.executable,str(ROOT/'qualification/prepare_run.py'),'--profile','atomic','--domain','content-synthesis','--run-root',td,'--candidate-root',cd,'--run-id','smoke']
        for wid in selected:cmd+=['--workflow',wid]
        env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','PYTHONUTF8':'0'};p=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,env=env)
        req(p.returncode==0,f'qualification prepare smoke failed:\n{p.stdout}\n{p.stderr}')
        rd=Path(td)/'smoke';meta=json.loads((rd/'run.json').read_text());queue=json.loads((rd/'evaluator/queue.json').read_text());prep=json.loads((rd/'evaluator/preparation.json').read_text());product=Path(meta['product_root']);workspace=Path(meta['workspace']);surface=Path(meta['candidate_surface_root'])
        pointer=product/'.businessos/workspace.json';req(pointer.exists(),'staged product lost persistent workspace binding');req(Path(json.loads(pointer.read_text()).get('workspace_root','')).resolve()==workspace.resolve(),'staged workspace pointer mismatch')
        req(meta.get('candidate_blind') is True and prep.get('candidate_blind') is True,'blind-candidate mode not recorded');req(product.parent==surface and workspace.parent==surface,'candidate product/workspace should share only neutral candidate surface');req(rd not in product.parents and rd not in workspace.parents,'candidate and evaluator trees must be separate')
        req(not (surface/'evaluator').exists() and not (surface/'checkpoints').exists(),'evaluator state leaked into candidate surface');req('qualification' not in product.as_posix().lower() and 'qualification' not in workspace.as_posix().lower(),'candidate-visible paths reveal benchmark intent')
        events=queue.get('events',[]);req(len(events)==len(selected) and {x.get('workflow_id') for x in events}==set(selected),'representative Workflow targets were not preserved evaluator-side');req(all(str(x.get('event_id','')).startswith('TASK-') for x in events),'candidate task IDs should be opaque');req(all('competitive_profile' not in x and 'required_output' not in x for x in events),'evaluator events retained inferred semantic requirement fields')
        req(not (product/'tests').exists() and not (product/'qualification').exists(),'developer/evaluator machinery leaked into staged product');req((ROOT/'qualification/task_controller.py').exists(),'external blind task controller missing')
        for page in [product/'WORKFLOW-INDEX.md',product/'PLAYBOOKS.md',*(product/'docs/playbooks').rglob('*.md')]:req(page.exists(),f'generated candidate navigation missing: {page.name}');page.read_text(encoding='utf-8')
        supplied=workspace/'attachments/supplied/atlasops-saas.json';req(supplied.exists(),'selected AtlasOps supplied material missing');req('timeline' not in json.loads(supplied.read_text()),'future evidence leaked into initial candidate material');req((rd/'evaluator/hidden-fixtures/atlasops-saas-releases.json').exists(),'future evidence was not retained evaluator-side')
        start=subprocess.run([sys.executable,str(ROOT/'qualification/task_controller.py'),'start',str(rd)],cwd=ROOT,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'});req(start.returncode==0,f'blind controller start failed: {start.stdout}\n{start.stderr}');started=json.loads(start.stdout);msg=started.get('candidate_message','').lower();req(msg and not any(x in msg for x in ('qualification','checkpoint','receipt','scoring')),'candidate request contains test-taking language');req(all(wid.lower() not in msg for wid in selected),'candidate request leaked hidden Workflow ID')

        # Optional one-way Workflow receipt: provenance yes, execution ledger no.
        run_env=dict(os.environ);run_env.pop('BUSINESSOS_WORKSPACE',None);run_env.pop('BUSINESSOS_WORKSPACE_CONFIG',None);run_env['PYTHONDONTWRITEBYTECODE']='1'
        create=subprocess.run([sys.executable,str(product/'scripts/create_run.py'),'atlasops','core.intelligence.ecosystem-radar','external controller smoke'],cwd=product,env=run_env,capture_output=True,text=True);req(create.returncode==0,f'optional create_run smoke failed: {create.stdout}\n{create.stderr}');rid=create.stdout.strip().splitlines()[-1];run_path=workspace/'runtime/runs/atlasops'/rid/'run.json';state=json.loads(run_path.read_text());req(state.get('method_type')=='aura_workflow' and state.get('method_ref')=='core.intelligence.ecosystem-radar' and state.get('workflow_id')=='core.intelligence.ecosystem-radar','Workflow receipt lost truthful method provenance');req((state.get('continuity') or {}).get('purpose')=='organizational_work_receipt','receipt lost continuity purpose');req(not (run_path.parent/'contract-execution.json').exists(),'optional receipt recreated execution ledger')

        # Timed evidence remains evaluator-controlled and appears as ordinary supplied business evidence.
        synthetic={'event_id':'TASK-RELEASE','evaluation_id':'SMOKE-RELEASE','kind':'cross_domain_mission','business_id':'atlasops','fixture':'atlasops-saas','workflow_id':None,'task':'Use the new business update to reassess the situation.','release_fixture':'later_period','receipt_path':'evaluator/receipts/TASK-RELEASE.json'};queue['events']=[synthetic];queue['event_count']=1;(rd/'evaluator/queue.json').write_text(json.dumps(queue,indent=2)+'\n');capture_checkpoint(product,workspace,rd,'TASK-RELEASE','before','atlasops');released,_=release_event(rd,'TASK-RELEASE');rel=json.loads(released.read_text());req(rel.get('source_type')=='business_supplied_update' and rel.get('evidence'),'timed release did not appear as ordinary supplied evidence');req(not {'qualification_event_id','fixture','release_fixture'} & set(rel),'candidate-visible release leaked benchmark metadata')


def profile_smoke(profile,mission,kind):
    with tempfile.TemporaryDirectory(prefix='aura-profile-smoke-') as td,tempfile.TemporaryDirectory(prefix='aura-workspaces-profile-') as cd:
        cmd=[sys.executable,str(ROOT/'qualification/prepare_run.py'),'--profile',profile,'--run-root',td,'--candidate-root',cd,'--run-id','profile-smoke']
        if mission:cmd+=['--mission',mission]
        p=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'});req(p.returncode==0,f'{profile} preparation failed:\n{p.stdout}\n{p.stderr}');queue=json.loads((Path(td)/'profile-smoke/evaluator/queue.json').read_text());events=queue.get('events',[]);req(len(events)==1 and events[0].get('kind')==kind,f'{profile} selected wrong event');msg=str(events[0].get('task','')).lower();req(not any(x in msg for x in ('qualification','rubric','score')),'mission request leaked evaluator framing')


def judge_prompt_smoke():
    with tempfile.TemporaryDirectory(prefix='aura-judge-prompt-') as td:
        rd=Path(td);ev=rd/'evaluator';ev.mkdir();(ev/'review-packets.json').write_text(json.dumps([{'event_id':'TASK-0001','hard_pass':True,'rubric_dimensions':['accuracy']}])+'\n');p=subprocess.run([sys.executable,str(ROOT/'qualification/build_judge_prompt.py'),str(rd)],cwd=ROOT,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'});req(p.returncode==0,'judge prompt generation failed');instructions=(ev/'JUDGE-INSTRUCTIONS.md').read_text();req('Treat **5 as rare**' in instructions and 'Distinguish relevance from proof' in instructions,'professional judge calibration weakened');req('expected-outcome guidance' in instructions and 'candidate must never receive' in instructions.lower(),'judge prompt lost hidden use-case guidance boundary')


def use_case_smoke():
    lib_root=ROOT/'qualification/use-cases';library=json.loads((lib_root/'library.json').read_text());cases=library.get('cases',[]);ids=[c.get('id') for c in cases]
    req(cases and len(ids)==len(set(ids)),'real-world use-case library missing or has duplicate ids')
    for case in cases:
        refs=[]
        if case.get('stages'):
            for stage in case['stages']:refs += [stage.get('request'),stage.get('judge')]
        else:refs += [case.get('request'),case.get('judge')]
        req(all(refs),'use-case request/judge pairing incomplete')
        for ref in refs:
            p=(lib_root/ref).resolve();req(p.is_file(),f'use-case source missing: {ref}');req(lib_root.resolve() in p.parents,'use-case source escaped maintainer-only library')
    with tempfile.TemporaryDirectory(prefix='aura-usecase-evaluator-') as td,tempfile.TemporaryDirectory(prefix='aura-usecase-workspaces-') as cd:
        cmd=[sys.executable,str(ROOT/'qualification/prepare_run.py'),'--case','saas-positioning-page','--run-root',td,'--candidate-root',cd,'--run-id','usecase-smoke'];p=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'});req(p.returncode==0,f'use-case preparation failed:\n{p.stdout}\n{p.stderr}')
        rd=Path(td)/'usecase-smoke';run=json.loads((rd/'run.json').read_text());queue=json.loads((rd/'evaluator/queue.json').read_text());product=Path(run['product_root']);workspace=Path(run['workspace']);events=queue.get('events',[])
        req(run.get('profile')=='use-case' and queue.get('case_filter')=='saas-positioning-page','use-case identity not retained evaluator-side');req(len(events)==1 and events[0].get('kind')=='use_case','use-case event preparation failed');req(events[0].get('event_id')=='TASK-0001','candidate-facing task id is not opaque')
        judge=rd/'evaluator/judges/TASK-0001.md';req(judge.is_file() and 'Expected outcome' in judge.read_text(),'hidden use-case judge guidance was not staged evaluator-side')
        req(not (product/'qualification').exists() and not (product/'tests').exists(),'candidate product exposed qualification/test source');req(not (Path(run['candidate_surface_root'])/'evaluator').exists(),'candidate surface exposed evaluator tree');req('qualification' not in product.as_posix().lower() and 'evaluator' not in workspace.as_posix().lower(),'candidate-visible paths reveal testing/evaluator intent')
        start=subprocess.run([sys.executable,str(ROOT/'qualification/task_controller.py'),'start',str(rd)],cwd=ROOT,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'});req(start.returncode==0,f'use-case controller start failed: {start.stdout}\n{start.stderr}');msg=json.loads(start.stdout).get('candidate_message','').strip();expected=(lib_root/'requests/saas-positioning-page.md').read_text().strip();req(msg==expected,'candidate did not receive the ordinary request verbatim');req('saas-positioning-page' not in msg.lower() and 'expected outcome' not in msg.lower(),'candidate request leaked use-case/judge metadata')
    with tempfile.TemporaryDirectory(prefix='aura-longitudinal-evaluator-') as td,tempfile.TemporaryDirectory(prefix='aura-longitudinal-workspaces-') as cd:
        cmd=[sys.executable,str(ROOT/'qualification/prepare_run.py'),'--case','saas-memory-evolution','--run-root',td,'--candidate-root',cd,'--run-id','longitudinal-smoke'];p=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'});req(p.returncode==0,f'longitudinal use-case preparation failed:\n{p.stdout}\n{p.stderr}')
        rd=Path(td)/'longitudinal-smoke';queue=json.loads((rd/'evaluator/queue.json').read_text());events=queue.get('events',[]);req(len(events)==3,'longitudinal case did not produce three ordinary requests');req(len({e.get('business_id') for e in events})==1,'longitudinal stages lost shared organization workspace');req(events[1].get('fresh_model_context') is True and events[2].get('fresh_model_context') is True,'longitudinal fresh-context intent missing evaluator-side');req(events[2].get('release_fixture')=='later_period','longitudinal contradictory/new evidence release missing');req(all((rd/'evaluator/judges'/f"{e['event_id']}.md").is_file() for e in events),'longitudinal judge guidance not isolated per stage')


def main():
    principles=ROOT/'qualification/PRINCIPLES.md';ledger=ROOT/'qualification/ledger.jsonl';qreadme=ROOT/'qualification/README.md';req(principles.is_file() and ledger.is_file(),'qualification principles/ledger missing');req('PRINCIPLES.md' in qreadme.read_text(),'qualification README lost principles pointer')
    for i,line in enumerate(ledger.read_text().splitlines(),1):
        if line.strip():
            try:json.loads(line)
            except json.JSONDecodeError as e:raise AssertionError(f'qualification ledger line {i} invalid: {e}')

    target='seo.intelligence.organic-competition.page-analysis';ordinary='Analyze a strong current organic page for a valuable AtlasOps search intent and identify the material gaps for our business.';customized=apply_candidate_request([{'workflow_id':target,'task':'generic'}],ordinary);req(customized[0]['task']==ordinary,'ordinary candidate request was not preserved')
    try:apply_candidate_request([{'workflow_id':target,'task':'generic'}],f'Execute {target}')
    except ValueError:pass
    else:raise AssertionError('candidate request must not expose hidden Workflow ID')
    with tempfile.TemporaryDirectory(prefix='aura-workspaces-unit-') as cd,tempfile.TemporaryDirectory(prefix='aura-evaluator-unit-') as ed:
        surface=candidate_surface(cd);req('qualification' not in surface.as_posix().lower(),'neutral candidate surface leaked benchmark marker');req(_ensure_separate(surface,Path(ed)/'run') is True,'separate candidate/evaluator trees rejected')

    suite=build();expected=len(workflow_files());req(suite['workflow_count']==expected,f"qualification Workflow coverage {suite['workflow_count']} != authored Workflow inventory {expected}");tests=suite['workflow_tests'];ids=[t['workflow_id'] for t in tests];req(len(ids)==len(set(ids)),'duplicate Workflow qualification tests');req(all(t['hard_gates'] and t['rubric_dimensions'] and t['candidate_task'] for t in tests),'every Workflow needs universal gates, professional rubric, and ordinary task');req(all('capabilities' not in t for t in tests),'retired capability ontology leaked into qualification cases')
    universal={'workspace_valid','business_valid','material_result_observed','completion_claim_truthful'};req(all(set(t['hard_gates'])==universal for t in tests),'atomic Workflow suite regained task-specific deterministic semantic gates');req(all(not ({'artifact_role','competitive_profile','output_policy','authored_workflow_refs'} & set(t)) for t in tests),'atomic Workflow suite retained retired semantic/composition metadata')
    req(fixture_for('content.production.article','content-synthesis')=='atlasops-saas','fixture router misclassified production as ecommerce');req(fixture_for('seo-aeo.execution.product-page','seo-aeo')=='northline-commerce','explicit product work lost ecommerce fixture');req(fixture_for('seo-aeo.local.service-area','seo-aeo')=='harbor-hvac','local/service-area work lost HVAC fixture')
    owners={m['owner_system'] for m in suite['domain_missions']};required={'core','customer-intelligence','competitor-intelligence','industry-intelligence','seo-aeo','content-synthesis','marketing-synthesis','customer-optimization'};req(owners==required,f'domain mission coverage mismatch: {owners ^ required}');req({m['id'] for m in suite.get('composition_missions',[])}=={'COMPOSE-SEO-CONTENT-001'},'targeted composition mission missing');req(len(suite['cross_domain_missions'])>=5 and len(suite['marathon_missions'])>=2,'mission coverage too small')
    mission_text=' '.join(m.get('task','') for key in ('composition_missions','domain_missions','cross_domain_missions','marathon_missions') for m in suite.get(key,[])).lower();retired=('action package','execution receipt','complete its run','complete their run','authorized work through execution','authorization, action planning');req(not any(x in mission_text for x in retired),'candidate-visible mission text reintroduced execution-control architecture')
    seed_source=inspect.getsource(init_business);req('bootstrap_explicit_context.py' in seed_source and '--require-context' in seed_source,'qualification setup must ground fixture context canonically');req('hidden-fixtures' in seed_source and 'timeline' in seed_source,'longitudinal evidence path missing')
    evaluator=(ROOT/'qualification/evaluate_run.py').read_text();req('Infer substantive requirements from the ordinary request' in evaluator and 'Python does not infer those requirements from Workflow identifiers' in evaluator,'professional evaluator did not inherit semantic completeness responsibility')
    smoke_prepare();profile_smoke('composition',None,'composition_mission');profile_smoke('cross-domain','CROSS-MARKET-CHANGE-001','cross_domain_mission');judge_prompt_smoke();use_case_smoke()
    print(f"qualification framework regressions passed: {suite['workflow_count']} Workflow tests plus blind real-world use cases, semantic-neutral hard floor, isolated judge criteria, longitudinal releases, and capable professional review")

if __name__=='__main__':main()
