#!/usr/bin/env python3
from pathlib import Path
import argparse, base64, json, os, shutil, subprocess, sys, tempfile, uuid
from build_suite import build
from common import ROOT, now, product_snapshot, write_json

FIXTURES=ROOT/'qualification/fixtures'
RUBRICS=json.loads((ROOT/'qualification/rubrics/rubrics.json').read_text())


def fixture_data(fixture):
    return json.loads((FIXTURES/f'{fixture}.json').read_text())


def fixture_business_id(fixture):
    return fixture_data(fixture)['business_id']


def event_from_workflow(t):
    return {
        'event_id':t['test_id'],'kind':'workflow_acceptance','business_id':fixture_business_id(t['fixture']),
        'fixture':t['fixture'],'workflow_id':t['workflow_id'],'task':t['candidate_task']
    }


def mission_dimensions(m,kind):
    base=[x['id'] for x in RUBRICS['base']]
    if kind in {'composition_mission','cross_domain_mission'}: profile='cross_domain_system'
    elif kind=='marathon_mission': profile='marathon_system'
    else:
        owner=m.get('owner_system'); profile={'core':'organizational_memory','customer-intelligence':'customer_truth','competitor-intelligence':'competitive_intelligence','industry-intelligence':'ecosystem_truth','seo-aeo':'search_live_field','content-synthesis':'artifact_excellence','marketing-synthesis':'paid_and_persuasion_field','customer-optimization':'first_party_outcomes'}.get(owner,'cross_domain_system')
    return base + list(RUBRICS['profiles'].get(profile,[]))


def event_from_mission(m,kind):
    event={
        'event_id':m['id'],'kind':kind,'business_id':fixture_business_id(m['fixture']),'fixture':m['fixture'],
        'workflow_id':None,'task':m['task'],'rubric_dimensions':mission_dimensions(m,kind)
    }
    if m.get('release_fixture'): event['release_fixture']=m['release_fixture']
    return event


def select_events(suite,profile,domain=None,workflow_ids=None,mission_id=None):
    requested=set(workflow_ids or [])
    if requested and mission_id: raise SystemExit('--workflow and --mission cannot be used together')
    if requested and profile!='atomic': raise SystemExit('--workflow is supported only with --profile atomic so a representative workflow run cannot silently include missions')
    known={t['workflow_id'] for t in suite['workflow_tests']}; unknown=sorted(requested-known)
    if unknown: raise SystemExit('Unknown qualification workflow filter(s): '+', '.join(unknown))
    mission_groups=(
        ('composition','composition_missions','composition_mission'),
        ('domains','domain_missions','domain_mission'),
        ('cross-domain','cross_domain_missions','cross_domain_mission'),
        ('marathon','marathon_missions','marathon_mission'),
    )
    if mission_id:
        known_missions={m['id'] for _,key,_ in mission_groups for m in suite.get(key,[])}
        if mission_id not in known_missions: raise SystemExit(f'Unknown qualification mission filter: {mission_id}')
        matches=[(m,kind) for mission_profile,key,kind in mission_groups if profile in {mission_profile,'full'} for m in suite.get(key,[]) if m['id']==mission_id]
        if not matches: raise SystemExit(f'Qualification mission {mission_id} does not belong to --profile {profile}')
        mission,kind=matches[0]
        if profile=='domains' and domain and mission.get('owner_system')!=domain:
            raise SystemExit(f'Qualification mission {mission_id} does not belong to --domain {domain}')
        return [event_from_mission(mission,kind)]
    events=[]
    if profile in ('atomic','full'):
        for t in suite['workflow_tests']:
            if domain and t['owner_system']!=domain: continue
            if requested and t['workflow_id'] not in requested: continue
            events.append(event_from_workflow(t))
    if profile in ('composition','full'): events += [event_from_mission(m,'composition_mission') for m in suite.get('composition_missions',[])]
    if profile in ('domains','full'): events += [event_from_mission(m,'domain_mission') for m in suite['domain_missions'] if not domain or m['owner_system']==domain]
    if profile in ('cross-domain','full'): events += [event_from_mission(m,'cross_domain_mission') for m in suite['cross_domain_missions']]
    if profile in ('marathon','full'): events += [event_from_mission(m,'marathon_mission') for m in suite['marathon_missions']]
    if not events: raise SystemExit('Qualification filters selected no events')
    return events


def publicize_events(events):
    """Keep evaluator targets hidden while assigning stable opaque task IDs externally."""
    out=[]
    for i,event in enumerate(events,1):
        public_id=f'TASK-{i:04d}'; full=dict(event)
        full['evaluation_id']=event['event_id']; full['event_id']=public_id
        full['receipt_path']=f'evaluator/receipts/{public_id}.json'
        out.append(full)
    return out


def apply_fixture_override(events,fixture):
    """Use a maintainer-selected benchmark business for one representative event.

    This changes only hidden qualification setup; the candidate still sees an ordinary
    initialized business workspace and ordinary request.
    """
    if fixture is None:return events
    if len(events)!=1:raise ValueError('--fixture requires exactly one selected qualification event')
    path=FIXTURES/f'{fixture}.json'
    if not path.is_file():raise ValueError(f'Unknown qualification fixture: {fixture}')
    out=[dict(events[0])]
    out[0]['fixture']=fixture
    out[0]['business_id']=fixture_business_id(fixture)
    return out


def apply_candidate_request(events,request):
    """Allow one maintainer-authored ordinary request without exposing evaluator targets."""
    if request is None: return events
    if len(events)!=1: raise ValueError('--request requires exactly one selected qualification event')
    text=str(request).strip()
    if not text: raise ValueError('--request cannot be empty')
    hidden_targets=(('workflow',events[0].get('workflow_id')),('mission',events[0].get('evaluation_id')))
    for target_kind,target in hidden_targets:
        target=str(target or '').strip()
        if target and target.lower() in text.lower():
            raise ValueError(f'--request must not expose the hidden target {target_kind} id')
    lower=text.lower()
    if any(marker in lower for marker in ('qualification rubric','qualification score','qualification checkpoint','qualification receipt')):
        raise ValueError('--request must be an ordinary business request, not test-taking instructions')
    out=[dict(events[0])]; out[0]['task']=text
    return out


def candidate_surface(candidate_root=None):
    """Create a neutral candidate-visible filesystem surface outside evaluator state."""
    base=Path(candidate_root).expanduser().resolve() if candidate_root else (Path(tempfile.gettempdir())/'aura-workspaces').resolve()
    if any(marker in base.as_posix().lower() for marker in ('qualification','evaluator','checkpoint')):
        raise ValueError('--candidate-root must use a neutral path name that does not reveal qualification/evaluator machinery')
    base.mkdir(parents=True,exist_ok=True)
    return base/f'session-{uuid.uuid4().hex[:10]}'


def _ensure_separate(candidate_dir,run_dir):
    """Reject candidate surfaces nested with evaluator state in either direction."""
    candidate_dir=Path(candidate_dir).resolve(); run_dir=Path(run_dir).resolve()
    for child,parent in ((candidate_dir,run_dir),(run_dir,candidate_dir)):
        try:
            child.relative_to(parent)
            raise ValueError('candidate product/workspace and evaluator run state must be physically separate directory trees')
        except ValueError as e:
            if str(e).startswith('candidate product/workspace'): raise
    return True


def copy_product(src,dst):
    """Stage the same runtime product a normal user receives, with no qualification/test lab."""
    src=Path(src); dst=Path(dst)
    for p in src.rglob('*'):
        if not p.is_file(): continue
        rel=p.relative_to(src); parts=rel.parts
        if any(x in {'.git','__pycache__','.pytest_cache','.venv','venv'} for x in parts): continue
        if parts and parts[0] in {'generated','knowledge','attachments','aura-qualification-runs','tests','qualification'}: continue
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


def _stage_supplied_media(inputs,data):
    """Stage evaluator-owned fixture media as ordinary candidate-visible supplied files.

    Binary fixture bytes may be stored base64-encoded in the maintainer-only qualification
    tree so repository transport does not constrain the candidate-visible media format.
    Encoding details and evaluator source paths never appear in public business metadata.
    """
    staged=[]; public=[]
    for item in data.get('supplied_media',[]) or []:
        if isinstance(item,str):
            source=item; filename=Path(item).name; encoding='copy'; meta={'filename':filename}
        elif isinstance(item,dict):
            source=item.get('source'); filename=item.get('filename') or (Path(source).name if source else None); encoding=item.get('encoding') or 'copy'
            meta={k:v for k,v in item.items() if k not in {'source','encoding'}}
        else:raise SystemExit(f'Invalid supplied_media fixture entry: {item!r}')
        if not source or not filename:raise SystemExit(f'supplied_media entry requires source/filename: {item!r}')
        src=(FIXTURES/source).resolve()
        try:src.relative_to(FIXTURES.resolve())
        except ValueError:raise SystemExit(f'supplied_media source escapes qualification fixtures: {source}')
        if not src.is_file():raise SystemExit(f'supplied_media source missing: {source}')
        dest=(inputs/filename).resolve()
        try:dest.relative_to(inputs.resolve())
        except ValueError:raise SystemExit(f'supplied_media filename escapes supplied inputs: {filename}')
        dest.parent.mkdir(parents=True,exist_ok=True)
        if encoding=='copy':
            shutil.copy2(src,dest)
        elif encoding=='base64':
            try:
                encoded=''.join(src.read_text(encoding='ascii').split())
                dest.write_bytes(base64.b64decode(encoded,validate=True))
            except Exception as e:
                raise SystemExit(f'Invalid base64 supplied_media fixture {source}: {e}')
        else:
            raise SystemExit(f'Unsupported supplied_media encoding {encoding!r} for {source}')
        staged.append(str(dest)); public.append(meta)
    return staged,public


def init_business(product_root,workspace,fixture,evaluator_root=None):
    data=fixture_data(fixture); bid=data['business_id']; name=data['name']; bootstrap=data.get('bootstrap_facts')
    if not isinstance(bootstrap,dict) or not bootstrap: raise SystemExit(f'Qualification fixture {fixture} requires non-empty bootstrap_facts so tests begin from grounded canonical context')
    evaluator_root=Path(evaluator_root or workspace.parent/'evaluator'); seed_dir=evaluator_root/'bootstrap'; seed_dir.mkdir(parents=True,exist_ok=True)
    env=dict(os.environ); env['BUSINESSOS_WORKSPACE']=str(workspace); env['PYTHONDONTWRITEBYTECODE']='1'; env['PYTHONUTF8']='1'
    _run([sys.executable,str(product_root/'scripts/init_business.py'),bid,'--name',name],product_root,env)
    inputs=workspace/'attachments'/'supplied'; inputs.mkdir(parents=True,exist_ok=True)
    staged_media,public_media=_stage_supplied_media(inputs,data)
    initial={k:v for k,v in data.items() if k not in {'timeline','supplied_media'}}
    if public_media:initial['supplied_media']=public_media
    source_path=inputs/f'{fixture}.json'; source_path.write_text(json.dumps(initial,indent=2)+'\n',encoding='utf-8')
    if data.get('timeline'):
        hidden=evaluator_root/'hidden-fixtures'; hidden.mkdir(parents=True,exist_ok=True)
        write_json(hidden/f'{fixture}-releases.json',data['timeline'])
    facts_path=seed_dir/f'{fixture}-facts.json'; facts_path.write_text(json.dumps(bootstrap,indent=2)+'\n',encoding='utf-8')
    boot=_run([sys.executable,str(product_root/'scripts/bootstrap_explicit_context.py'),bid,'--facts-file',str(facts_path),'--source-file',str(source_path),'--source-reference','supplied business material'],product_root,env)
    validation=_run([sys.executable,str(product_root/'scripts/validate_business.py'),bid,'--require-context'],product_root,env)
    audit={'fixture':fixture,'business_id':bid,'source_path':str(source_path),'supplied_media_paths':staged_media,'facts_path':str(facts_path),'future_evidence_hidden':bool(data.get('timeline')),'bootstrapped_at':now(),'bootstrap_stdout':boot.stdout,'bootstrap_stderr':boot.stderr,'validation_stdout':validation.stdout,'validation_stderr':validation.stderr}
    write_json(seed_dir/f'{fixture}-bootstrap-audit.json',audit)
    return bid


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--profile',choices=['atomic','composition','domains','cross-domain','marathon','full'],default='atomic'); ap.add_argument('--domain'); ap.add_argument('--workflow',action='append',default=[],help='Exact workflow ID to include in an atomic representative run; repeat for multiple workflows.'); ap.add_argument('--mission',help='Exact mission ID to include in a mission-based qualification profile.'); ap.add_argument('--fixture',help='Maintainer-only benchmark fixture override for exactly one selected qualification event.'); ap.add_argument('--request',help='Maintainer-authored ordinary business request for exactly one selected event. This replaces only the candidate-visible task text; evaluator target/rubric remain hidden.'); ap.add_argument('--run-root',help='Maintainer-only evaluator/checkpoint run root.'); ap.add_argument('--candidate-root',help='Neutral root for candidate-visible product/workspace. Must be physically separate from the evaluator run root.'); ap.add_argument('--run-id'); a=ap.parse_args()
    if a.profile=='atomic' and not a.domain and not a.workflow and not a.mission: raise SystemExit('Atomic qualification requires --workflow <exact-workflow-id> or --domain <installed-domain>; use --profile full explicitly only for an intentional broad endurance run')
    suite=build(); selected=select_events(suite,a.profile,a.domain,a.workflow,a.mission); evaluator_events=publicize_events(selected)
    try:
        evaluator_events=apply_fixture_override(evaluator_events,a.fixture)
        evaluator_events=apply_candidate_request(evaluator_events,a.request)
    except ValueError as e: raise SystemExit(str(e))
    run_id=a.run_id or ('aura-qualification-'+uuid.uuid4().hex[:10]); root=Path(a.run_root).expanduser().resolve() if a.run_root else Path(tempfile.gettempdir())/'aura-qualification-runs'; run_dir=root/run_id
    if run_dir.exists(): raise SystemExit(f'Run already exists: {run_dir}')
    try: run_dir.relative_to(ROOT.resolve()); raise SystemExit('Qualification run root must be outside the AURA product tree to prevent recursive staging or product contamination')
    except ValueError: pass
    try:
        candidate_dir=candidate_surface(a.candidate_root); _ensure_separate(candidate_dir,run_dir)
    except ValueError as e: raise SystemExit(str(e))
    if candidate_dir.exists(): raise SystemExit(f'Candidate surface already exists: {candidate_dir}')
    run_dir.mkdir(parents=True); (run_dir/'evaluator').mkdir(); (run_dir/'checkpoints').mkdir()
    product_root=copy_product(ROOT,candidate_dir/'product'); generation_env=dict(os.environ); generation_env['PYTHONDONTWRITEBYTECODE']='1'; generation_env['PYTHONUTF8']='1'; _run([sys.executable,str(product_root/'scripts/generate_registry.py')],product_root,generation_env)
    workspace=candidate_dir/'workspace'; workspace.mkdir(parents=True)

    # Persistently bind the staged runtime product to its neutral external
    # organization workspace. Candidate agents should not have to recreate the
    # maintainer's temporary BUSINESSOS_WORKSPACE environment variable in order
    # for normal AURA helpers to keep organization state outside product source.
    binding_env=dict(os.environ)
    binding_env.pop('BUSINESSOS_WORKSPACE',None)
    binding_env.pop('BUSINESSOS_WORKSPACE_CONFIG',None)
    binding_env['PYTHONDONTWRITEBYTECODE']='1'
    binding_env['PYTHONUTF8']='1'
    _run([
        sys.executable,
        str(product_root/'scripts/configure_workspace.py'),
        str(workspace),
        '--profile','power_user',
        '--json'
    ],product_root,binding_env)

    fixtures=sorted({event['fixture'] for event in evaluator_events})
    for fixture in fixtures: init_business(product_root,workspace,fixture,run_dir/'evaluator')
    baseline=product_snapshot(product_root); write_json(run_dir/'evaluator/product-snapshot.json',baseline)
    workflow_filter=sorted(set(a.workflow)); evaluator_queue={'format_version':'3.0','run_id':run_id,'profile':a.profile,'domain_filter':a.domain,'workflow_filter':workflow_filter,'mission_filter':a.mission,'event_count':len(evaluator_events),'events':evaluator_events}
    preparation={'profile':a.profile,'domain_filter':a.domain,'workflow_filter':workflow_filter,'mission_filter':a.mission,'fixture_override':a.fixture,'prepared_at':now(),'candidate_blind':True,'maintainer_authored_request':bool(a.request),'candidate_surface_root':str(candidate_dir)}
    write_json(run_dir/'evaluator/queue.json',evaluator_queue); write_json(run_dir/'evaluator/suite.json',suite); write_json(run_dir/'evaluator/preparation.json',preparation)
    future=any(fixture_data(f).get('timeline') for f in fixtures)
    write_json(run_dir/'run.json',{'run_id':run_id,'created_at':now(),'product_root':str(product_root),'workspace':str(workspace),'candidate_surface_root':str(candidate_dir),'profile':a.profile,'domain_filter':a.domain,'event_count':len(evaluator_events),'status':'prepared','execution_status':'prepared','qualification_status':'NOT_EVALUATED','product_snapshot_digest':baseline['digest'],'benchmark_context_seeded':True,'future_evidence_staged':future,'candidate_blind':True})
    print(json.dumps({'run_id':run_id,'run_dir':str(run_dir),'product_root':str(product_root),'workspace':str(workspace),'event_count':len(evaluator_events),'candidate_blind':True,'next_command':f'python3 qualification/task_controller.py start "{run_dir}"','candidate_exposure':'Give the model only the neutral staged product/workspace paths and the plain business request printed by task_controller.py start. Keep evaluator/checkpoint paths outside the candidate filesystem scope.'},indent=2))

if __name__=='__main__': main()
