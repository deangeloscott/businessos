#!/usr/bin/env python3
"""Focused regressions for durable Asset truth, evidence origin, and optional receipts."""
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
    path.write_text(json.dumps(value,indent=2)+'\n' if isinstance(value,(dict,list)) else str(value),encoding='utf-8');return path

def init_business(workspace,business_id,env):
    run([S/'init_business.py',business_id,'--name',business_id.replace('-',' ').title()],env)
    run([S/'bootstrap_explicit_context.py',business_id,'--facts-json',json.dumps({'objectives':['Verify organizational state truth']}),'--source-text','The organization objective is to verify organizational state truth.'],env)
    return workspace/'instances'/business_id


def asset_truth_regression(workspace,env):
    """AURA remembers the Asset; it does not maintain a shadow production-readiness engine."""
    bid='asset-truth';base=init_business(workspace,bid,env)
    rid=run([S/'create_run.py',bid,'Prepare a truthful customer-facing landing-page draft','--workflow-id','marketing.assets.landing-page'],env).stdout.strip()
    artifact=write(base/'assets'/'landing-page.html','<html><body><p>We charge [CONFIRM ACTUAL FEE].</p><p>Start here: [CONFIRM CTA AND URL].</p></body></html>\n')
    business=json.loads((base/'context/business.json').read_text());aid=f'ast_{bid}_landing'
    asset={
        'id':aid,'object_type':'Asset','schema_version':'1.0.0','business_id':bid,'created_at':'2026-08-30T00:00:00+00:00','updated_at':'2026-08-30T00:00:00+00:00','lineage':[business['id']],
        'asset_type':'landing_page','business_role':'customer_facing_landing_page_draft','location_reference':f'instances/{bid}/assets/landing-page.html','version':'1','status':'draft',
        'extensions':{'businessos':{'customer_facing':True,'claim_manifest':[
            {'text':'We charge [CONFIRM ACTUAL FEE].','classification':'placeholder','support_refs':[],'launch_critical':True},
            {'text':'Start here: [CONFIRM CTA AND URL].','classification':'placeholder','support_refs':[],'launch_critical':True}]}}
    }
    asset_path=write(base/'assets'/f'{aid}.json',asset);before=asset_path.read_bytes()

    active=run([S/'validate_business.py',bid],env,check=False)
    req(active.returncode==0,f'active optional receipt invalidated truthful draft Asset: {active.stdout+active.stderr}')
    completed=run([S/'complete_run.py',bid,rid,'--result',asset_path.relative_to(workspace),'--result',artifact.relative_to(workspace),'--summary','Prepared a truthful landing-page draft with unresolved placeholders preserved.'],env)
    result=json.loads(completed.stdout);req(result.get('status')=='completed',f'receipt completion failed: {result}')
    req(asset_path.read_bytes()==before,'receipt completion mutated independent Asset truth')

    saved=json.loads(asset_path.read_text())
    req(saved.get('status')=='draft','receipt completion promoted Asset status')
    bos=saved.get('extensions',{}).get('businessos',{})
    req('production_readiness' not in bos,'Asset regained AURA-owned production_readiness state')
    retired={'run_ref','run_id','run_method_type','run_method_ref','run_contract_id','run_binding','run_history_refs','contract_chain'}
    req(not (retired & set(bos)),'Asset regained canonical Run backlinks')

    # Natural-language/local metadata may mention readiness, deployment, access, or review,
    # but AURA must not promote such labels into a canonical readiness ontology.
    bos['launch_ready']=True;bos['readiness_status']='ready_for_launch';bos['publishing_access']='missing'
    write(asset_path,saved)
    loose=run([S/'validate_business.py',bid],env,check=False)
    req(loose.returncode==0,f'loose readiness-like metadata gained deterministic semantic authority: {loose.stdout+loose.stderr}')

    # Protect the architecture itself: readiness is not a first-class AURA helper or
    # validator concern. Real publication/deployment changes and measured outcomes, when
    # worth remembering, belong in the durable objects that actually represent those facts.
    req(not (S/'artifact_readiness.py').exists(),'production-readiness control-plane helper reappeared')
    validator=(S/'validate_business.py').read_text(encoding='utf-8')
    req('artifact_readiness' not in validator and 'readiness_errors' not in validator,'business validation regained production-readiness semantics')
    change_schema=json.loads((ROOT/'core/schemas/action/change-event.schema.json').read_text())
    metric_schema=json.loads((ROOT/'core/schemas/measurement/metric-observation.schema.json').read_text())
    req(change_schema.get('title')=='ChangeEvent' and metric_schema.get('title')=='MetricObservation','natural durable owners for real changes/measurements are missing')


def provenance_regression(workspace,env):
    bid='provenance-truth';base=init_business(workspace,bid,env)
    supplied=write(workspace/'attachments/customer-input.txt','A customer supplied this bounded internal evidence.\n')
    internal_bundle=write(workspace/'attachments/internal-bundle.json',{'sources':[{'source_reference':'attachments/customer-input.txt','acquisition_method':'unknown','captured_text':supplied.read_text()}],'observations':[{'statement':'The supplied file contains one bounded internal evidence statement.','source_indexes':[0]}]})
    internal_result=json.loads(run([S/'persist_research_bundle.py',bid,'--bundle-file',internal_bundle],env).stdout);source_row=next(x for x in internal_result['objects_written'] if x['object_type']=='SourceRecord');source=json.loads((workspace/source_row['path']).read_text())
    req(source.get('source_type')=='organization_supplied_file' and source.get('origin')=='organization supplied' and source.get('access_scope')=='business_internal',f'organization-supplied source was misclassified: {source}')
    req(source.get('extensions',{}).get('businessos_evidence',{}).get('provenance_resolution')=='exact_workspace_reference','exact external-workspace provenance was not recorded')
    public_bundle=write(workspace/'attachments/public-bundle.json',{'sources':[{'source_type':'review_platform','source_reference':'https://www.yelp.com/biz/aura-public-regression','acquisition_method':'user_provided','captured_text':'A bounded public review excerpt.'}]})
    public=json.loads(run([S/'persist_research_bundle.py',bid,'--bundle-file',public_bundle],env).stdout);public_row=next(x for x in public['objects_written'] if x['object_type']=='SourceRecord');public_source=json.loads((workspace/public_row['path']).read_text())
    req(public_source.get('origin')=='public web' and public_source.get('access_scope')=='public','genuine public-web source lost public provenance')
    ambiguous_bundle=write(workspace/'attachments/ambiguous-bundle.json',{'sources':[{'source_reference':'provider-record-123','acquisition_method':'api_response','record_payload':{'statement':'bounded record'}}]})
    ambiguous=run([S/'persist_research_bundle.py',bid,'--bundle-file',ambiguous_bundle],env,check=False)
    req(ambiguous.returncode!=0 and 'cannot determine source provenance mechanically' in ambiguous.stderr and 'will not default ambiguous evidence to public web' in ambiguous.stderr,'ambiguous provenance was guessed')
    req(not (ROOT/'instances'/bid).exists() and base.exists(),'external workspace provenance regression leaked organization state into product root')


def complete_receipt(workspace,env,bid,rid,label):
    evidence=write(workspace/'runtime/runs'/bid/rid/'artifacts'/f'{label}.txt',f'{label} completed.\n')
    return json.loads(run([S/'complete_run.py',bid,rid,'--evidence',evidence.relative_to(workspace),'--summary',f'Completed {label}.'],env).stdout)


def receipt_independence_regression(workspace,env):
    bid='run-receipt-truth';init_business(workspace,bid,env)
    first=run([S/'create_run.py',bid,'Inspect one bounded indexing condition','--workflow-id','seo.execution.indexing.index-troubleshooting'],env).stdout.strip()
    second=run([S/'create_run.py',bid,'Diagnose a separate business question','--workflow-id','core.diagnosis.business-problem'],env).stdout.strip()
    duplicate=run([S/'create_run.py',bid,'Inspect one bounded indexing condition','--workflow-id','seo.execution.indexing.index-troubleshooting'],env).stdout.strip()
    complete_receipt(workspace,env,bid,first,'bounded index-state inspection')
    states={rid:json.loads((workspace/'runtime/runs'/bid/rid/'run.json').read_text()) for rid in (first,second,duplicate)}
    req(states[first].get('status')=='completed','completed receipt did not close')
    req(states[second].get('status')=='active' and states[duplicate].get('status')=='active','completing one receipt mutated another receipt')
    retired_relationship_fields={'correlation_id','causation_id','root_run_id','parent_run_id','run_role','supersedes_run_id','superseded_by_run_id','lifecycle_reason'}
    for rid,row in states.items():
        leaked=retired_relationship_fields & set(row)
        req(not leaked,f'{rid} reintroduced receipt relationship graph: {sorted(leaked)}')
    schema=json.loads((ROOT/'core/schemas/runtime/run.schema.json').read_text())
    req(not (retired_relationship_fields & set(schema.get('properties',{}))),'Run schema reintroduced relationship lifecycle fields')
    req(not (S/'run_lifecycle.py').exists() and not (S/'reconcile_runs.py').exists(),'Run reconciliation subsystem reappeared')


def main():
    with tempfile.TemporaryDirectory(prefix='aura-organizational-state-truth-') as td:
        workspace=Path(td).resolve();env=os.environ.copy();env['BUSINESSOS_WORKSPACE']=str(workspace);env['PYTHONDONTWRITEBYTECODE']='1'
        asset_truth_regression(workspace,env);provenance_regression(workspace,env);receipt_independence_regression(workspace,env)
    print('organizational state truth regressions passed: Asset truth boundary, provenance, and independent optional receipts')


if __name__=='__main__':main()
