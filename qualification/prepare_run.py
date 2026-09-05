#!/usr/bin/env python3
from pathlib import Path
import argparse, base64, json, os, shutil, subprocess, sys, tempfile, uuid
from common import ROOT, load_workflows, now, product_snapshot, write_json

FIXTURES=ROOT/'qualification/fixtures'
USE_CASE_ROOT=ROOT/'qualification/use-cases'
USE_CASE_LIBRARY=json.loads((USE_CASE_ROOT/'library.json').read_text())
RUBRICS=json.loads((ROOT/'qualification/rubrics/rubrics.json').read_text())

OWNER_PROFILES={
    'core':'organizational_memory',
    'customer-intelligence':'customer_truth',
    'competitor-intelligence':'competitive_intelligence',
    'industry-intelligence':'ecosystem_truth',
    'seo-aeo':'search_live_field',
    'content-synthesis':'artifact_excellence',
    'marketing-synthesis':'paid_and_persuasion_field',
    'customer-optimization':'first_party_outcomes',
}


def fixture_data(fixture):
    path=FIXTURES/f'{fixture}.json'
    if not path.is_file():raise SystemExit(f'Unknown qualification fixture: {fixture}')
    return json.loads(path.read_text())


def fixture_business_id(fixture):
    return fixture_data(fixture)['business_id']


def _use_case_file(rel):
    p=(USE_CASE_ROOT/rel).resolve()
    try:p.relative_to(USE_CASE_ROOT.resolve())
    except ValueError:raise SystemExit(f'Use-case path escapes library: {rel}')
    if not p.is_file():raise SystemExit(f'Use-case file missing: {rel}')
    return p


def _use_case(case_id):
    for case in USE_CASE_LIBRARY.get('cases',[]):
        if case.get('id')==case_id:return case
    known=', '.join(sorted(c.get('id','') for c in USE_CASE_LIBRARY.get('cases',[]) if c.get('id')))
    raise SystemExit(f'Unknown use case: {case_id}. Available: {known}')


def _workflow(workflow_id):
    for workflow in load_workflows():
        if workflow.get('type')=='workflow' and workflow.get('workflow_id')==workflow_id:return workflow
    raise SystemExit(f'Unknown Workflow diagnostic target: {workflow_id}')


def _dimensions(profile=None):
    base=[x['id'] for x in RUBRICS['base']]
    return base + list(RUBRICS['profiles'].get(profile,[]))


def use_case_dimensions(case):
    domains=case.get('domains') or []
    if case.get('kind')=='longitudinal':profile='marathon_system'
    elif len(domains)!=1:profile='cross_domain_system'
    else:profile=OWNER_PROFILES.get(domains[0],'cross_domain_system')
    return _dimensions(profile)


def workflow_dimensions(workflow):
    return _dimensions(OWNER_PROFILES.get(workflow.get('owner_system')))


def events_from_use_case(case_id):
    case=_use_case(case_id);fixture=case['fixture'];dims=use_case_dimensions(case);stages=case.get('stages') or []
    if stages:
        events=[]
        for i,stage in enumerate(stages,1):
            event={
                'event_id':f'USECASE-{case_id.upper()}-{i:02d}',
                'kind':'use_case','case_id':case_id,'business_id':fixture_business_id(fixture),
                'fixture':fixture,'workflow_id':None,
                'task':_use_case_file(stage['request']).read_text().strip(),
                'rubric_dimensions':dims,'judge_source':stage['judge'],
                'fresh_model_context':bool(stage.get('fresh_model_context')),
            }
            if stage.get('release_fixture'):event['release_fixture']=stage['release_fixture']
            events.append(event)
        return events
    return [{
        'event_id':f'USECASE-{case_id.upper()}','kind':'use_case','case_id':case_id,
        'business_id':fixture_business_id(fixture),'fixture':fixture,'workflow_id':None,
        'task':_use_case_file(case['request']).read_text().strip(),
        'rubric_dimensions':dims,'judge_source':case['judge'],
    }]


def _default_workflow_request(workflow):
    outcome=(workflow.get('business_outcome') or workflow.get('purpose') or workflow.get('title') or 'complete this business job').strip()
    return (
        f'For the active business, {outcome.rstrip(".")}. '
        'Do the real work using the organization context and the strongest appropriate tools available. '
        'Preserve durable organizational meaning only when it will materially help future work. '
        'Do not invent facts, sources, tool use, external actions, or outcomes.'
    )


def _validate_ordinary_request(text,hidden_workflow_id=None):
    text=str(text or '').strip()
    if not text:raise ValueError('candidate request cannot be empty')
    if hidden_workflow_id and hidden_workflow_id.lower() in text.lower():
        raise ValueError('--request must not expose the hidden Workflow id')
    lower=text.lower()
    if any(marker in lower for marker in (
        'qualification rubric','qualification score','qualification checkpoint',
        'qualification receipt','judge criteria','target workflow',
    )):
        raise ValueError('--request must be an ordinary business request, not test-taking instructions')
    return text


def event_from_workflow(workflow_id,fixture,request=None):
    workflow=_workflow(workflow_id)
    task=_validate_ordinary_request(request or _default_workflow_request(workflow),workflow_id)
    return {
        'event_id':'WORKFLOW-DIAGNOSTIC-'+workflow_id.replace('.','-').upper(),
        'kind':'workflow_diagnostic',
        'business_id':fixture_business_id(fixture),
        'fixture':fixture,
        'workflow_id':workflow_id,
        'owner_system':workflow.get('owner_system'),
        'task':task,
        'rubric_dimensions':workflow_dimensions(workflow),
        'claim_under_test':{
            'title':workflow.get('title'),
            'purpose':workflow.get('purpose'),
            'business_outcome':workflow.get('business_outcome'),
            'completion_evidence':workflow.get('completion_evidence'),
        },
        'workflow_process_steps':workflow.get('process') or [],
    }


def publicize_events(events):
    """Keep evaluator targets hidden while assigning stable opaque task IDs externally."""
    out=[]
    for i,event in enumerate(events,1):
        public_id=f'TASK-{i:04d}';full=dict(event)
        full['evaluation_id']=event['event_id'];full['event_id']=public_id
        full['receipt_path']=f'evaluator/receipts/{public_id}.json'
        out.append(full)
    return out


def apply_candidate_request(events,request):
    """Replace one candidate-visible task with an ordinary maintainer-authored request."""
    if request is None:return events
    if len(events)!=1:raise ValueError('--request requires exactly one selected event')
    hidden=events[0].get('workflow_id')
    text=_validate_ordinary_request(request,hidden)
    out=[dict(events[0])];out[0]['task']=text
    return out


def candidate_surface(candidate_root=None):
    """Create a neutral candidate-visible filesystem surface outside evaluator state."""
    root=Path(candidate_root).expanduser().resolve() if candidate_root else (Path(tempfile.gettempdir())/'aura-workspaces').resolve()
    if any(marker in root.as_posix().lower() for marker in ('qualification','evaluator','checkpoint')):
        raise ValueError('--candidate-root must use a neutral path name that does not reveal qualification/evaluator machinery')
    root.mkdir(parents=True,exist_ok=True)
    return root/f'session-{uuid.uuid4().hex[:10]}'


def _ensure_separate(candidate_dir,run_dir):
    """Reject candidate surfaces nested with evaluator state in either direction."""
    candidate_dir=Path(candidate_dir).resolve();run_dir=Path(run_dir).resolve()
    for child,parent in ((candidate_dir,run_dir),(run_dir,candidate_dir)):
        try:
            child.relative_to(parent)
            raise ValueError('candidate product/workspace and evaluator run state must be physically separate directory trees')
        except ValueError as e:
            if str(e).startswith('candidate product/workspace'):raise
    return True


def copy_product(src,dst):
    """Stage the same runtime product a normal user receives, with no qualification/test lab."""
    src=Path(src);dst=Path(dst)
    for p in src.rglob('*'):
        if not p.is_file():continue
        rel=p.relative_to(src);parts=rel.parts
        if any(x in {'.git','__pycache__','.pytest_cache','.venv','venv'} for x in parts):continue
        if parts and parts[0] in {'generated','knowledge','attachments','aura-qualification-runs','tests','qualification'}:continue
        if parts and parts[0]=='instances' and (len(parts)<2 or parts[1] != '_template'):continue
        if parts and parts[0]=='runtime' and not (len(parts)==2 and parts[1]=='README.md'):continue
        if rel.as_posix()=='.businessos/workspace.json':continue
        if rel.suffix in {'.pyc','.zip'}:continue
        q=dst/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
    return dst


def _run(cmd,product_root,env):
    p=subprocess.run(cmd,cwd=product_root,env=env,capture_output=True,text=True)
    if p.returncode!=0:
        raise SystemExit(
            f"Qualification preparation command failed ({p.returncode}): {' '.join(map(str,cmd))}\n"
            f"STDOUT:\n{p.stdout}\nSTDERR:\n{p.stderr}"
        )
    return p


def _stage_supplied_media(inputs,data):
    """Stage evaluator-owned fixture media as ordinary candidate-visible supplied files."""
    staged=[];public=[]
    for item in data.get('supplied_media',[]) or []:
        if isinstance(item,str):
            source=item;filename=Path(item).name;encoding='copy';meta={'filename':filename}
        elif isinstance(item,dict):
            source=item.get('source');filename=item.get('filename') or (Path(source).name if source else None);encoding=item.get('encoding') or 'copy'
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
        if encoding=='copy':shutil.copy2(src,dest)
        elif encoding=='base64':
            try:
                encoded=''.join(src.read_text(encoding='ascii').split())
                dest.write_bytes(base64.b64decode(encoded,validate=True))
            except Exception as e:raise SystemExit(f'Invalid base64 supplied_media fixture {source}: {e}')
        else:raise SystemExit(f'Unsupported supplied_media encoding {encoding!r} for {source}')
        staged.append(str(dest));public.append(meta)
    return staged,public


def init_business(product_root,workspace,fixture,evaluator_root=None):
    data=fixture_data(fixture);bid=data['business_id'];name=data['name'];bootstrap=data.get('bootstrap_facts')
    if not isinstance(bootstrap,dict) or not bootstrap:
        raise SystemExit(f'Qualification fixture {fixture} requires non-empty bootstrap_facts so tests begin from grounded canonical context')
    evaluator_root=Path(evaluator_root or workspace.parent/'evaluator');seed_dir=evaluator_root/'bootstrap';seed_dir.mkdir(parents=True,exist_ok=True)
    env=dict(os.environ);env['BUSINESSOS_WORKSPACE']=str(workspace);env['PYTHONDONTWRITEBYTECODE']='1';env['PYTHONUTF8']='1'
    _run([sys.executable,str(product_root/'scripts/init_business.py'),bid,'--name',name],product_root,env)
    inputs=workspace/'attachments'/'supplied';inputs.mkdir(parents=True,exist_ok=True)
    staged_media,public_media=_stage_supplied_media(inputs,data)
    initial={k:v for k,v in data.items() if k not in {'timeline','supplied_media'}}
    if public_media:initial['supplied_media']=public_media
    source_path=inputs/f'{fixture}.json';source_path.write_text(json.dumps(initial,indent=2)+'\n',encoding='utf-8')
    if data.get('timeline'):
        hidden=evaluator_root/'hidden-fixtures';hidden.mkdir(parents=True,exist_ok=True)
        write_json(hidden/f'{fixture}-releases.json',data['timeline'])
    facts_path=seed_dir/f'{fixture}-facts.json';facts_path.write_text(json.dumps(bootstrap,indent=2)+'\n',encoding='utf-8')
    boot=_run([
        sys.executable,str(product_root/'scripts/bootstrap_explicit_context.py'),bid,
        '--facts-file',str(facts_path),'--source-file',str(source_path),
        '--source-reference','supplied business material'
    ],product_root,env)
    validation=_run([sys.executable,str(product_root/'scripts/validate_business.py'),bid,'--require-context'],product_root,env)
    audit={
        'fixture':fixture,'business_id':bid,'source_path':str(source_path),
        'supplied_media_paths':staged_media,'facts_path':str(facts_path),
        'future_evidence_hidden':bool(data.get('timeline')),'bootstrapped_at':now(),
        'bootstrap_stdout':boot.stdout,'bootstrap_stderr':boot.stderr,
        'validation_stdout':validation.stdout,'validation_stderr':validation.stderr,
    }
    write_json(seed_dir/f'{fixture}-bootstrap-audit.json',audit)
    return bid


def main():
    ap=argparse.ArgumentParser(description='Prepare one blind real-work AURA qualification case or one on-demand Workflow diagnostic.')
    target=ap.add_mutually_exclusive_group(required=True)
    target.add_argument('--case',help='Real-world use-case id from qualification/use-cases/library.json.')
    target.add_argument('--workflow',help='Exact Workflow id for a focused diagnostic. This is not a generated all-Workflow test suite.')
    ap.add_argument('--fixture',help='Benchmark business fixture for --workflow. Required so the maintainer, not a heuristic router, chooses the relevant business context.')
    ap.add_argument('--request',help='Optional ordinary business request for --workflow. If omitted, a neutral request is derived from the authored Workflow outcome.')
    ap.add_argument('--run-root',help='Maintainer-only evaluator/checkpoint run root.')
    ap.add_argument('--candidate-root',help='Neutral root for candidate-visible product/workspace. Must be physically separate from the evaluator run root.')
    ap.add_argument('--run-id')
    a=ap.parse_args()

    if a.case and (a.fixture or a.request):
        raise SystemExit('--case uses its own hidden fixture/request pairing and cannot be combined with --fixture or --request')
    if a.workflow and not a.fixture:
        raise SystemExit('--workflow diagnostics require --fixture <benchmark-fixture>; choose the business context explicitly')

    if a.case:
        selected=events_from_use_case(a.case);effective_mode='use-case'
    else:
        selected=[event_from_workflow(a.workflow,a.fixture,a.request)];effective_mode='workflow-diagnostic'
    evaluator_events=publicize_events(selected)

    run_id=a.run_id or ('aura-qualification-'+uuid.uuid4().hex[:10])
    root=Path(a.run_root).expanduser().resolve() if a.run_root else Path(tempfile.gettempdir())/'aura-qualification-runs'
    run_dir=root/run_id
    if run_dir.exists():raise SystemExit(f'Run already exists: {run_dir}')
    try:
        run_dir.relative_to(ROOT.resolve())
        raise SystemExit('Qualification run root must be outside the AURA product tree to prevent recursive staging or product contamination')
    except ValueError:pass
    try:
        candidate_dir=candidate_surface(a.candidate_root);_ensure_separate(candidate_dir,run_dir)
    except ValueError as e:raise SystemExit(str(e))
    if candidate_dir.exists():raise SystemExit(f'Candidate surface already exists: {candidate_dir}')

    run_dir.mkdir(parents=True)
    (run_dir/'evaluator').mkdir()
    (run_dir/'checkpoints').mkdir()
    (run_dir/'evaluator/judges').mkdir()
    for event in evaluator_events:
        judge_source=event.pop('judge_source',None)
        if judge_source:
            (run_dir/'evaluator/judges'/f"{event['event_id']}.md").write_text(_use_case_file(judge_source).read_text(),encoding='utf-8')

    product_root=copy_product(ROOT,candidate_dir/'product')
    generation_env=dict(os.environ);generation_env['PYTHONDONTWRITEBYTECODE']='1';generation_env['PYTHONUTF8']='1'
    _run([sys.executable,str(product_root/'scripts/generate_registry.py')],product_root,generation_env)
    workspace=candidate_dir/'workspace';workspace.mkdir(parents=True)

    binding_env=dict(os.environ)
    binding_env.pop('BUSINESSOS_WORKSPACE',None)
    binding_env.pop('BUSINESSOS_WORKSPACE_CONFIG',None)
    binding_env['PYTHONDONTWRITEBYTECODE']='1';binding_env['PYTHONUTF8']='1'
    _run([
        sys.executable,str(product_root/'scripts/configure_workspace.py'),str(workspace),
        '--profile','power_user','--json'
    ],product_root,binding_env)

    fixtures=sorted({event['fixture'] for event in evaluator_events})
    for fixture in fixtures:init_business(product_root,workspace,fixture,run_dir/'evaluator')
    baseline=product_snapshot(product_root);write_json(run_dir/'evaluator/product-snapshot.json',baseline)

    workflow_filter=[a.workflow] if a.workflow else []
    evaluator_queue={
        'format_version':'4.0','run_id':run_id,'mode':effective_mode,
        'case_filter':a.case,'workflow_filter':workflow_filter,
        'event_count':len(evaluator_events),'events':evaluator_events,
    }
    preparation={
        'mode':effective_mode,'case_filter':a.case,'workflow_filter':workflow_filter,
        'fixture':a.fixture,'prepared_at':now(),'candidate_blind':True,
        'maintainer_authored_request':bool(a.request),'candidate_surface_root':str(candidate_dir),
    }
    write_json(run_dir/'evaluator/queue.json',evaluator_queue)
    write_json(run_dir/'evaluator/preparation.json',preparation)

    future=any(fixture_data(f).get('timeline') for f in fixtures)
    write_json(run_dir/'run.json',{
        'run_id':run_id,'created_at':now(),'product_root':str(product_root),
        'workspace':str(workspace),'candidate_surface_root':str(candidate_dir),
        'mode':effective_mode,'case_filter':a.case,'workflow_filter':workflow_filter,
        'event_count':len(evaluator_events),'status':'prepared','execution_status':'prepared',
        'qualification_status':'NOT_EVALUATED','product_snapshot_digest':baseline['digest'],
        'benchmark_context_seeded':True,'future_evidence_staged':future,'candidate_blind':True,
    })
    print(json.dumps({
        'run_id':run_id,'run_dir':str(run_dir),'product_root':str(product_root),
        'workspace':str(workspace),'event_count':len(evaluator_events),'candidate_blind':True,
        'next_command':f'python3 qualification/task_controller.py start "{run_dir}"',
        'candidate_exposure':'Give the model only the neutral staged product/workspace paths and the plain business request printed by task_controller.py start. Do not give the candidate access to the source checkout, evaluator tree, use-case library, judge files, checkpoints, or queue metadata.',
    },indent=2))


if __name__=='__main__':main()
