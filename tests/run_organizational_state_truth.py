#!/usr/bin/env python3
"""Focused regressions for readiness, evidence origin, and Run reconciliation truth."""
from pathlib import Path
import json,os,subprocess,sys,tempfile

ROOT=Path(__file__).resolve().parents[1];S=ROOT/'scripts'


def req(condition,message):
    if not condition:raise AssertionError(message)


def run(args,env,check=True):
    result=subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,env=env,capture_output=True,text=True)
    if check and result.returncode!=0:raise AssertionError(f'command failed: {args}\nstdout={result.stdout}\nstderr={result.stderr}')
    return result


def write(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    if isinstance(value,(dict,list)):path.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
    else:path.write_text(str(value),encoding='utf-8')
    return path


def init_business(workspace,business_id,env):
    run([S/'init_business.py',business_id,'--name',business_id.replace('-',' ').title()],env)
    run([S/'bootstrap_explicit_context.py',business_id,'--facts-json',json.dumps({'objectives':['Verify organizational state truth']}),'--source-text','The organization objective is to verify organizational state truth.','--initialization-only'],env)
    return workspace/'instances'/business_id


def readiness_regression(workspace,env):
    bid='readiness-truth';base=init_business(workspace,bid,env)
    rid=run([S/'create_run.py',bid,'marketing.assets.landing-page','Prepare a truthful customer-facing landing-page draft'],env).stdout.strip()
    rd=workspace/'runtime/runs'/bid/rid;manifest=json.loads((rd/'contract-execution.json').read_text())
    artifact=write(base/'assets'/'landing-page.html','<html><body><p>We charge [CONFIRM ACTUAL FEE].</p><p>Start here: [CONFIRM CTA AND URL].</p></body></html>\n')
    business=json.loads((base/'context/business.json').read_text())
    aid=f'ast_{bid}_landing'
    readiness={
        'status':'blocked','assessed_version':'1','unresolved_business_facts':['Actual customer fee and waiver policy are not established.','Final CTA destination is not established.'],
        'missing_authorization':['The current task has not authorized publication/deployment.'],'missing_capabilities':['The current harness does not have publishing access to the target surface.'],'other_blockers':[],
        'deployment_status':'not_performed','deployment_evidence_refs':[],'measurement_status':'pending','measurement_evidence_refs':[],
    }
    asset={
        'id':aid,'object_type':'Asset','schema_version':'1.0.0','business_id':bid,
        'created_at':'2026-08-30T00:00:00+00:00','updated_at':'2026-08-30T00:00:00+00:00','lineage':[business['id']],
        'asset_type':'landing_page','owner_system':'marketing-synthesis','business_role':'customer_facing_landing_page_draft',
        'location_reference':f'instances/{bid}/assets/landing-page.html','version':'1','status':'draft',
        'extensions':{'businessos':{
            'customer_facing':True,'run_ref':f'runtime/runs/{bid}/{rid}','run_id':rid,'run_contract_id':'marketing.assets.landing-page',
            'contract_chain':['marketing.assets.landing-page',*manifest['required_subcontracts']],
            'claim_manifest':[
                {'text':'We charge [CONFIRM ACTUAL FEE].','classification':'placeholder','support_refs':[],'launch_critical':True},
                {'text':'Start here: [CONFIRM CTA AND URL].','classification':'placeholder','support_refs':[],'launch_critical':True},
            ],
            'production_readiness':readiness,
        }}
    }
    asset_path=write(base/'assets'/f'{aid}.json',asset)
    qa=write(rd/'artifacts/landing-page-qa.json',{
        'contract_id':'marketing.landing-page.qa','status':'pass','tested_asset':aid,'tested_version':'1',
        'checks_performed':[
            {'check':'placeholder truth and claim calibration','status':'pass','method':'Inspected every customer-facing sentence and compared it with the claim manifest','finding':'Unknown fee and CTA facts remain visibly bracketed rather than stated as business facts.','target_component':'fee and CTA placeholder copy'},
            {'check':'draft structure and action clarity','status':'pass','method':'Inspected the saved HTML hierarchy and current draft action language','finding':'The current draft is structurally usable for business review while the unresolved CTA is visibly identified.','target_component':'saved landing-page draft'},
        ],
        'issues_found':[],'corrections_made':[],'limitations':['Production readiness was assessed separately and remains blocked.'],'blockers':[],
    })
    for cid in manifest['required_subcontracts']:
        refs=[asset_path]
        if cid=='marketing.landing-page.qa':refs=[qa,artifact]
        args=[S/'record_contract_completion.py',bid,rid,cid]
        for ref in refs:args.extend(['--evidence',f'{ref.relative_to(workspace).as_posix()}'])
        run(args,env)
    finalized=run([S/'finalize_run.py',bid,rid,'--workspace',workspace,'--skip-human-knowledge','--evidence',artifact.relative_to(workspace)],env)
    result=json.loads(finalized.stdout);scope=result.get('completion_scope',{})
    req(result.get('status')=='completed',f'valid blocked draft should complete its bounded work: {result}')
    req(scope.get('artifact_work')=='completed' and scope.get('production_readiness')=='blocked',f'artifact completion and readiness were conflated: {scope}')
    req(scope.get('qa') and scope['qa'][0].get('status')=='pass' and scope['qa'][0].get('artifact_qa_blockers')==[],f'current-version draft QA should pass independently: {scope}')
    row=scope['assets'][0]
    req(row.get('artifact_status')=='draft' and row.get('deployment_status')=='not_performed' and row.get('measurement_status')=='pending',f'draft/deployment/outcome state was not preserved: {row}')
    req(row.get('unresolved_business_facts') and row.get('missing_authorization') and row.get('missing_capabilities'),f'typed real-world readiness blockers were lost: {row}')

    qa_saved=json.loads(qa.read_text());qa_saved['production_ready']=True;write(qa,qa_saved)
    qa_bad=run([S/'validate_business.py',bid],env,check=False)
    req(qa_bad.returncode!=0 and 'QA record may pass artifact/version checks but cannot assert production/launch readiness' in qa_bad.stdout,f'artifact QA was allowed to impersonate global readiness: {qa_bad.stdout}')
    qa_saved.pop('production_ready');write(qa,qa_saved)

    # Neither typed real-world blockers nor launch-critical/unassessed placeholders may coexist with ready.
    saved=json.loads(asset_path.read_text());pr=saved['extensions']['businessos']['production_readiness'];pr['status']='ready'
    write(asset_path,saved);bad=run([S/'validate_business.py',bid],env,check=False)
    req(bad.returncode!=0 and 'cannot retain unresolved blockers' in bad.stdout,f'ready assertion retained typed blockers: {bad.stdout}')
    pr['status']='blocked';saved['extensions']['businessos']['no_blockers']=True;write(asset_path,saved)
    no_blockers_bad=run([S/'validate_business.py',bid],env,check=False)
    req(no_blockers_bad.returncode!=0 and 'no_blockers=true conflicts' in no_blockers_bad.stdout,f'global no-blockers assertion hid typed readiness blockers: {no_blockers_bad.stdout}')
    saved['extensions']['businessos'].pop('no_blockers');pr['status']='ready'
    for field in ('unresolved_business_facts','missing_authorization','missing_capabilities','other_blockers'):pr[field]=[]
    write(asset_path,saved);placeholder_bad=run([S/'validate_business.py',bid],env,check=False)
    req(placeholder_bad.returncode!=0 and 'placeholder claim entries remain launch-critical or unassessed' in placeholder_bad.stdout,f'launch-critical placeholders were allowed to assert ready: {placeholder_bad.stdout}')
    pr.update(readiness);write(asset_path,saved)
    req(run([S/'validate_business.py',bid],env).returncode==0,'truthful blocked draft should remain valid after contradiction checks')


def provenance_regression(workspace,env):
    bid='provenance-truth';base=init_business(workspace,bid,env)
    supplied=write(workspace/'attachments/customer-input.txt','A customer supplied this bounded internal evidence.\n')
    internal_bundle=write(workspace/'attachments/internal-bundle.json',{
        'contract_id':'competitor.analysis.customer-sentiment',
        'sources':[{'source_reference':'attachments/customer-input.txt','acquisition_method':'unknown','captured_text':supplied.read_text()}],
        'observations':[{'statement':'The supplied file contains one bounded internal evidence statement.','source_indexes':[0]}],
    })
    internal=run([S/'persist_research_bundle.py',bid,'--bundle-file',internal_bundle],env)
    internal_result=json.loads(internal.stdout);source_row=next(x for x in internal_result['objects_written'] if x['object_type']=='SourceRecord')
    source=json.loads((workspace/source_row['path']).read_text())
    req(source.get('source_type')=='organization_supplied_file' and source.get('origin')=='organization supplied' and source.get('access_scope')=='business_internal',f'organization-supplied source was misclassified: {source}')
    req(source.get('extensions',{}).get('businessos_evidence',{}).get('provenance_resolution')=='exact_workspace_reference',f'exact external-workspace provenance was not recorded: {source}')

    public_bundle=write(workspace/'attachments/public-bundle.json',{
        'contract_id':'competitor.analysis.customer-sentiment',
        'sources':[{'source_type':'review_platform','source_reference':'https://www.yelp.com/biz/aura-public-regression','acquisition_method':'user_provided','captured_text':'A bounded public review excerpt.'}],
    })
    public=json.loads(run([S/'persist_research_bundle.py',bid,'--bundle-file',public_bundle],env).stdout)
    public_row=next(x for x in public['objects_written'] if x['object_type']=='SourceRecord');public_source=json.loads((workspace/public_row['path']).read_text())
    req(public_source.get('origin')=='public web' and public_source.get('access_scope')=='public',f'genuine public-web source lost public provenance: {public_source}')

    ambiguous_bundle=write(workspace/'attachments/ambiguous-bundle.json',{
        'contract_id':'competitor.analysis.customer-sentiment',
        'sources':[{'source_reference':'provider-record-123','acquisition_method':'api_response','record_payload':{'statement':'bounded record'}}],
    })
    ambiguous=run([S/'persist_research_bundle.py',bid,'--bundle-file',ambiguous_bundle],env,check=False)
    req(ambiguous.returncode!=0 and 'cannot determine source provenance mechanically' in ambiguous.stderr and 'will not default ambiguous evidence to public web' in ambiguous.stderr,f'ambiguous provenance was guessed: {ambiguous.stdout+ambiguous.stderr}')
    req(not (ROOT/'instances'/bid).exists() and base.exists(),'external workspace provenance regression leaked organization state into product root')


def lifecycle_regression(workspace,env):
    bid='run-lifecycle-truth';init_business(workspace,bid,env)
    task='Inspect the exact indexing condition for this bounded interaction'
    old=run([S/'create_run.py',bid,'seo.diagnosis.detectors.indexing',task],env).stdout.strip()
    current=run([S/'create_run.py',bid,'seo.diagnosis.detectors.indexing',task,'--supersedes-run-id',old],env).stdout.strip()
    premature=json.loads(run([S/'reconcile_runs.py',bid,current,'--apply-safe-supersession'],env).stdout)
    req(premature.get('status')=='needs_judgment' and 'not exactly completed' in premature.get('reason',''),'active replacement was allowed to reconcile before successful completion')
    req(json.loads((workspace/'runtime/runs'/bid/old/'run.json').read_text()).get('status')=='active','pre-completion reconciliation mutated the prior Run')

    independent=run([S/'create_run.py',bid,'core.diagnosis.business-problem','Diagnose a separate still-active business question'],env).stdout.strip()
    ambiguous=run([S/'create_run.py',bid,'core.diagnosis.business-problem','Evaluate an unresolved support question','--parent-run-id',current],env).stdout.strip()

    current_dir=workspace/'runtime/runs'/bid/current
    evidence=write(current_dir/'artifacts/indexing-no-finding.json',{
        'contract_id':'seo.diagnosis.detectors.indexing','status':'completed','result':'no_finding',
        'checks_performed':[{'check':'bounded index-state inspection','status':'pass'}],
        'evidence_refs':[f'runtime/runs/{bid}/{current}/artifacts/inspection.txt'],
    })
    write(current_dir/'artifacts/inspection.txt','The bounded index-state inspection completed.\n')
    finalized=json.loads(run([S/'finalize_run.py',bid,current,'--workspace',workspace,'--skip-human-knowledge'],env).stdout)
    recon=finalized.get('run_reconciliation',{})
    req(finalized.get('status')=='completed',f'completed root Run should remain complete while reconciliation reports related receipts: {finalized}')
    req(any(x.get('run_id')==old for x in recon.get('mechanically_superseded_runs',[])),f'exact empty replacement was not safely superseded: {recon}')
    req(any(x.get('run_id')==independent for x in recon.get('legitimately_active_runs',[])),f'independent active Run was not preserved: {recon}')
    req(any(x.get('run_id')==ambiguous for x in recon.get('needs_judgment',[])) and recon.get('status')=='needs_judgment',f'ambiguous related Run did not request judgment: {recon}')
    req('blocked_or_waiting_runs' not in recon,f'Run reconciliation reintroduced an AURA-owned blocker queue: {recon}')
    statuses={rid:json.loads((workspace/'runtime/runs'/bid/rid/'run.json').read_text()).get('status') for rid in (old,current,independent,ambiguous)}
    req(statuses[old]=='superseded' and statuses[current]=='completed',f'exact Run completion/supersession state is wrong: {statuses}')
    req(statuses[independent]=='active' and statuses[ambiguous]=='active',f'independent/ambiguous Runs were auto-completed: {statuses}')
    req(evidence.exists(),'finalization removed completion evidence')

    # Completing one support Run must preserve its exact parent/root as meaningful composition work.
    parent=run([S/'create_run.py',bid,'core.diagnosis.business-problem','Coordinate a bounded composed diagnosis'],env).stdout.strip()
    child=run([S/'create_run.py',bid,'seo.diagnosis.detectors.indexing','Complete one bounded support inspection','--parent-run-id',parent],env).stdout.strip()
    child_dir=workspace/'runtime/runs'/bid/child
    write(child_dir/'artifacts/support-no-finding.json',{
        'contract_id':'seo.diagnosis.detectors.indexing','status':'completed','result':'no_finding',
        'checks_performed':[{'check':'bounded support inspection','status':'pass'}],
        'evidence_refs':[f'runtime/runs/{bid}/{child}/artifacts/support-inspection.txt'],
    })
    write(child_dir/'artifacts/support-inspection.txt','The bounded support inspection completed.\n')
    child_result=json.loads(run([S/'finalize_run.py',bid,child,'--workspace',workspace,'--skip-human-knowledge'],env).stdout)
    child_recon=child_result.get('run_reconciliation',{})
    req(child_recon.get('status')=='remaining_work' and any(x.get('run_id')==parent and x.get('relationship')=='exact_parent' for x in child_recon.get('legitimately_active_runs',[])),f'active parent/root composition work was treated as debris or ambiguity: {child_recon}')
    req(json.loads((workspace/'runtime/runs'/bid/parent/'run.json').read_text()).get('status')=='active','completed support Run auto-completed its exact parent')


def main():
    with tempfile.TemporaryDirectory(prefix='aura-organizational-state-truth-') as td:
        workspace=Path(td).resolve();env=os.environ.copy();env['BUSINESSOS_WORKSPACE']=str(workspace);env['PYTHONDONTWRITEBYTECODE']='1'
        readiness_regression(workspace,env)
        provenance_regression(workspace,env)
        lifecycle_regression(workspace,env)
    print('organizational state truth regressions passed: readiness, provenance, and Run reconciliation')


if __name__=='__main__':main()
