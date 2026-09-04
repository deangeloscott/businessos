#!/usr/bin/env python3
"""Protect reusable organization-local Workflow knowledge and explicit sharing without runtime authority."""
from pathlib import Path
import json,os,shutil,sys,tempfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))

from init_business import init_business
from _common import now,iter_instance_objects,workflow_files,read_frontmatter
from persist_process_extension import persist_extension
from process_extensions import resolve_effective,local_workflow_candidates
from prepare_innovation_package import prepare_package
from export_innovation_package import export_package
from innovation_common import validate_package,load_package,bounded_summary,innovation_entry_path
from import_innovation_package import import_package
from configure_innovation_sharing import configure
from record_innovation_outcome import record_outcome
from list_innovation_exchange import list_entries

A='workflow-evolution-a'
B='workflow-evolution-b'


def req(condition,message):
    if not condition:raise AssertionError(message)


def seed_learning(business_id):
    base=ROOT/'instances'/business_id
    obj={
        'id':'lrn_workflow_evolution_test','object_type':'Learning','schema_version':'1.0.0','business_id':business_id,
        'created_at':now(),'updated_at':now(),'scope':'business',
        'statement':'Proof-first landing structure improved qualified conversion in the tested context.',
        'maturity':'validated','status':'active','applies_when':['Evidence-backed landing-page work'],
        'does_not_apply_when':[],'evidence_refs':[],'confidence':0.9,'extensions':{}
    }
    path=base/'learning'/'business'/f"{obj['id']}.json";path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(obj,indent=2)+'\n');return obj


def workflow_by_id(workflow_id):
    for path in workflow_files():
        meta,_=read_frontmatter(path)
        if meta.get('id')==workflow_id:return path,meta
    return None,None


def main():
    # Reusable local knowledge is canonical; retired proposal/adoption/version ceremony stays gone.
    required=[
        'core/policies/workflow-evolution.md','core/schemas/learning/process-extension.schema.json',
        'scripts/persist_process_extension.py','scripts/process_extensions.py','INNOVATION-EXCHANGE.md'
    ]
    for rel in required:req((ROOT/rel).exists(),f'missing organization-local Workflow knowledge component: {rel}')
    retired=[
        'core/schemas/learning/workflow-evolution-proposal.schema.json','scripts/persist_workflow_evolution.py',
        'scripts/adopt_process_extension.py','core/capabilities/catalog.json','docs/adding-a-capability.md',
        'core/policies/playbook-evolution.md','core/schemas/learning/playbook-evolution-proposal.schema.json',
        'scripts/persist_playbook_evolution.py'
    ]
    for rel in retired:req(not (ROOT/rel).exists(),f'retired proposal/capability artifact still exists: {rel}')

    process_schema=json.loads((ROOT/'core/schemas/learning/process-extension.schema.json').read_text())
    req(process_schema.get('additionalProperties') is False,'ProcessExtension schema must remain strict')
    text=json.dumps(process_schema)
    for retired_name in ('required_capabilities','optional_capabilities','target_contract_id','local_contract_id','target_workflow_id','local_workflow_id','owner_system','reads','writes','compatibility','proposal_ref','approval'):
        req(retired_name not in text,f'ProcessExtension retained retired control/contract field {retired_name}')

    outcome_schema=json.loads((ROOT/'core/schemas/measurement/outcome-evaluation.schema.json').read_text())
    req('causal_confidence' not in outcome_schema.get('properties',{}),'OutcomeEvaluation regained forced numeric causal confidence')

    prior=os.environ.get('BUSINESSOS_WORKSPACE');tmp=Path(tempfile.mkdtemp(prefix='aura-workflow-learning-'));os.environ['BUSINESSOS_WORKSPACE']=str(tmp)
    try:
        init_business(A,'Workflow Learning A');init_business(B,'Workflow Learning B');seed_learning(A)

        augment={
            'mode':'augment_workflow','scope':'business','workflow_id':'marketing.assets.landing-page',
            'title':'Proof-first landing-page extension',
            'purpose':'Use the validated proof-first sequence when the evidence conditions match.',
            'source_kind':'learning_evolved','source_learning_refs':['lrn_workflow_evolution_test'],'source_refs':[],
            'evidence_refs':[],'applies_when':['Suitable proof exists'],'does_not_apply_when':['Proof is unavailable'],
            'discovery_terms':['proof first landing'],
            'instructions':['Lead the relevant persuasion sequence with the strongest supported proof before unsupported persuasion claims.'],
            'verification':['Confirm proof claims retain evidence and claim lineage.']
        }
        extension,_=persist_extension(A,augment)
        req(extension['object_type']=='ProcessExtension','local reusable knowledge used wrong canonical type')
        req(extension['source_kind']=='learning_evolved' and extension['source_learning_refs']==['lrn_workflow_evolution_test'],'Learning provenance was lost')
        req(extension['mode']=='augment_workflow' and extension['workflow_id']=='marketing.assets.landing-page','Workflow augmentation relation was not preserved')
        for retired_name in ('owner_system','reads','writes','compatibility','target_workflow_id','local_workflow_id'):
            req(retired_name not in extension,f'persisted ProcessExtension retained retired field {retired_name}')
        _,meta,content,extensions=resolve_effective('marketing.assets.landing-page',A)
        req(extension['id'] in [item['id'] for item in extensions],'organization extension not visible in effective knowledge')
        req('Proof-first landing-page extension' in content,'effective Workflow omitted organization extension')
        req('capabilities' not in meta,'retired capability ontology leaked into effective Workflow metadata')

        # Explicit organization-authored procedures require no fabricated Learning or source reference.
        local={
            'mode':'local_workflow','scope':'business','workflow_id':'custom.marketing.proof-first-landing',
            'title':'Proof First Landing Workflow','purpose':'Reusable organization-local procedure for proof-first landing-page work.',
            'source_kind':'organization_authored','source_refs':[],'evidence_refs':[],
            'applies_when':['The organization wants its proof-first landing approach'],'does_not_apply_when':[],
            'discovery_terms':['proof first landing'],
            'instructions':['Lead with the strongest supported proof, then adapt the persuasion sequence to the actual offer and audience.']
        }
        local_extension,_=persist_extension(A,local)
        req(local_extension['source_refs']==[] and local_extension['source_learning_refs']==[],'organization-authored procedure received fabricated provenance')
        req(local_extension['verification']==[],'verification became mandatory ceremony')
        candidates=local_workflow_candidates('Use our proof first landing workflow',A)
        req('custom.marketing.proof-first-landing' in [row.get('workflow_id') for row in candidates],'local Workflow discovery failed')
        req(all(row.get('selection_authority') is False for row in candidates),'local Workflow discovery claimed semantic authority')
        _,local_meta,local_content,_=resolve_effective('custom.marketing.proof-first-landing',A)
        req(local_meta.get('local_workflow') is True and 'Proof First Landing Workflow' in local_content,'local Workflow resolution failed')
        req('may adapt it or choose another sound method' in local_content,'local knowledge became mandatory execution authority')
        req('owner_system' not in local_meta,'organization-local Workflow invented a product-system owner')

        config,_=configure(A,'workflow_only','anonymous',True,['shared/innovation-index.json'],None)
        req('prompt_mode' not in config,'innovation config reintroduced pseudo prompting behavior')
        package,draft=prepare_package(A,local_extension['id'],detail='workflow_only',identity='anonymous')
        req(package['privacy']['user_approved_export'] is False,'prepared package must remain unapproved')
        package_text=json.dumps(package)
        for retired_name in ('capabilities','compatibility','aura_version','owner_system','reads','writes','target_workflow_id','local_workflow_id'):
            req(retired_name not in package_text,f'InnovationPackage retained retired field {retired_name}')
        req(package['process'].get('workflow_id')=='custom.marketing.proof-first-landing','shared process lost Workflow identity')
        zip_path=tmp/'innovation.zip';exported,_=export_package(draft,zip_path,approved=True)
        validate_package(load_package(zip_path),require_export_approval=True)
        req(exported['identity_level']=='anonymous' and exported['detail_level']=='workflow_only','sharing presets changed unexpectedly')
        try:bounded_summary({'api_key':'should-never-export'},'test')
        except ValueError:pass
        else:raise AssertionError('secret-like fields were not rejected')

        entry,source_record,stored=import_package(B,zip_path)
        req(entry['workflow_id']=='custom.marketing.proof-first-landing' and entry['mode']=='local_workflow','imported support lost process identity')
        req('compatibility_status' not in entry,'Innovation Exchange reintroduced product-version compatibility state')
        req(source_record.get('source_reference')==str(stored.relative_to(ROOT)),'imported SourceRecord does not point to stored package evidence')
        req(json.loads(innovation_entry_path(B,entry['id']).read_text()).get('object_type') is None,'Innovation Exchange support entry became canonical state')
        req(not any(obj.get('object_type')=='ProcessExtension' for obj,_ in iter_instance_objects(B)),'package import silently adopted foreign operating knowledge')
        req(not any(obj.get('object_type')=='Insight' for obj,_ in iter_instance_objects(B)),'package import manufactured semantic Insight')

        # Imported support may later gain local evidence without turning popularity into truth.
        evaluation={'id':'eval_exchange_test','object_type':'OutcomeEvaluation','schema_version':'1.0.0','business_id':B,'target_refs':[],'attribution_method':'controlled_test','conclusion':'The imported Workflow was supported in this bounded local test.','extensions':{}}
        ep=ROOT/'instances'/B/'measurement'/'outcome-evaluations'/'eval_exchange_test.json';ep.parent.mkdir(parents=True,exist_ok=True);ep.write_text(json.dumps(evaluation,indent=2)+'\n')
        record_outcome(B,entry['id'],'supported','eval_exchange_test');again=record_outcome(B,entry['id'],'supported','eval_exchange_test')
        req(again['local_evidence']['supported_count']==1,'duplicate local outcome was not idempotent')
        feed=list_entries(B);req(feed and feed[0]['local_supported']==1,'Innovation Exchange did not surface local outcome evidence')

        workflow_path,workflow_meta=workflow_by_id('core.learning.workflow-evolution')
        req(workflow_path and workflow_meta.get('type')=='workflow','Workflow learning procedure is not authored as reusable knowledge')
        exchange_path,exchange_meta=workflow_by_id('core.intelligence.innovation-exchange')
        req(exchange_path and exchange_meta.get('type')=='workflow','Innovation Exchange procedure is not authored as reusable knowledge')
        print('organization-local Workflow learning + Innovation Exchange regressions passed without proposal, capability, version, runtime authority')
    finally:
        if prior is None:os.environ.pop('BUSINESSOS_WORKSPACE',None)
        else:os.environ['BUSINESSOS_WORKSPACE']=prior
        shutil.rmtree(tmp,ignore_errors=True)


if __name__=='__main__':main()
