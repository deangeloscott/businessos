#!/usr/bin/env python3
"""Protect reusable Workflow evolution and explicit sharing without runtime/tool authority."""
from pathlib import Path
import json,os,shutil,sys,tempfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))

from init_business import init_business
from _common import now,iter_instance_objects
from persist_workflow_evolution import persist_proposal
from adopt_process_extension import adopt_extension
from process_extensions import resolve_effective,local_workflow_candidates
from prepare_innovation_package import prepare_package
from export_innovation_package import export_package
from innovation_common import validate_package,load_package,bounded_summary,innovation_entry_path
from import_innovation_package import import_package
from configure_innovation_sharing import configure
from record_innovation_outcome import record_outcome
from list_innovation_exchange import list_entries
from resolve_contract import resolve_contract

A='workflow-evolution-a'
B='workflow-evolution-b'


def req(condition,message):
    if not condition:raise AssertionError(message)


def seed_learning(business_id):
    base=ROOT/'instances'/business_id
    obj={
        'id':'lrn_workflow_evolution_test','object_type':'Learning','schema_version':'1.0.0','business_id':business_id,
        'created_at':now(),'updated_at':now(),'owner_scope':'business','owner_system':'marketing-synthesis',
        'statement':'Proof-first landing structure improved qualified conversion in the tested context.',
        'maturity':'validated','status':'active','applies_when':['Evidence-backed landing-page work'],
        'does_not_apply_when':[],'evidence_refs':[],'confidence':0.9,'extensions':{}
    }
    path=base/'learning'/'business'/f"{obj['id']}.json";path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(obj,indent=2)+'\n');return obj


def main():
    # The new semantic layer must be complete and the retired capability/playbook-evolution
    # ontology must be gone after the one-time migration.
    required=[
        'core/policies/workflow-evolution.md','core/schemas/learning/workflow-evolution-proposal.schema.json',
        'core/schemas/learning/process-extension.schema.json','scripts/persist_workflow_evolution.py',
        'scripts/persist_process_extension.py','scripts/process_extensions.py','INNOVATION-EXCHANGE.md'
    ]
    for rel in required:req((ROOT/rel).exists(),f'missing Workflow evolution component: {rel}')
    retired=[
        'core/capabilities/catalog.json','docs/adding-a-capability.md','core/policies/playbook-evolution.md',
        'core/schemas/learning/playbook-evolution-proposal.schema.json','scripts/persist_playbook_evolution.py'
    ]
    for rel in retired:req(not (ROOT/rel).exists(),f'retired capability/Playbook-evolution artifact still exists: {rel}')

    process_schema=json.loads((ROOT/'core/schemas/learning/process-extension.schema.json').read_text())
    proposal_schema=json.loads((ROOT/'core/schemas/learning/workflow-evolution-proposal.schema.json').read_text())
    for schema,name in ((process_schema,'ProcessExtension'),(proposal_schema,'WorkflowEvolutionProposal')):
        req(schema.get('additionalProperties') is False,f'{name} schema must remain strict')
        text=json.dumps(schema)
        for retired_name in ('required_capabilities','optional_capabilities','target_contract_id','local_contract_id','new_local_playbook'):
            req(retired_name not in text,f'{name} retained retired semantic field {retired_name}')

    prior=os.environ.get('BUSINESSOS_WORKSPACE');tmp=Path(tempfile.mkdtemp(prefix='aura-workflow-evolution-'));os.environ['BUSINESSOS_WORKSPACE']=str(tmp)
    try:
        init_business(A,'Workflow Evolution A');init_business(B,'Workflow Evolution B');seed_learning(A)

        augment={
            'owner_system':'marketing-synthesis','change_kind':'augment_existing','proposed_scope':'business',
            'target_workflow_id':'marketing.assets.landing-page','proposed_local_workflow_id':None,
            'title':'Proof-first landing-page extension','summary':'Use the validated proof-first sequence when the evidence conditions match.',
            'learning_refs':['lrn_workflow_evolution_test'],'evidence_refs':[],
            'applies_when':['Suitable proof exists'],'does_not_apply_when':['Proof is unavailable'],
            'discovery_terms':['proof first landing'],'reads':[],'writes':['DecisionRecord'],
            'instructions':['Lead the relevant persuasion sequence with the strongest supported proof before unsupported persuasion claims.'],
            'verification':['Confirm proof claims retain evidence and claim lineage.']
        }
        proposal,_=persist_proposal(A,augment);req(proposal['object_type']=='WorkflowEvolutionProposal','proposal used wrong canonical type');req(proposal['id'].startswith('wev_'),'Workflow evolution proposal used legacy id prefix')
        extension,_=adopt_extension(A,proposal['id']);req(extension['mode']=='augment_workflow','adopted augmentation used wrong mode');req(extension.get('target_workflow_id')=='marketing.assets.landing-page','adopted augmentation lost target Workflow')
        _,meta,content,extensions=resolve_effective('marketing.assets.landing-page',A)
        req(extension['id'] in [item['id'] for item in extensions],'adopted Workflow extension not visible in effective knowledge');req('Proof-first landing-page extension' in content,'effective Workflow omitted organization extension');req('DecisionRecord' in meta.get('writes',[]),'extension durable output metadata was lost');req('capabilities' not in meta,'retired capability ontology leaked into effective Workflow metadata')

        local=dict(augment)
        local.update({
            'change_kind':'new_local_workflow','target_workflow_id':None,
            'proposed_local_workflow_id':'custom.marketing.proof-first-landing','title':'Proof First Landing Workflow',
            'summary':'Reusable organization-local procedure for proof-first landing-page work.','writes':[]
        })
        local_proposal,_=persist_proposal(A,local);local_extension,_=adopt_extension(A,local_proposal['id'])
        candidates=local_workflow_candidates('Use our proof first landing workflow',A)
        req('custom.marketing.proof-first-landing' in [row.get('workflow_id') for row in candidates],'local Workflow discovery failed');req(all(row.get('selection_authority') is False for row in candidates),'local Workflow discovery claimed semantic authority')
        _,local_meta,local_content,_=resolve_effective('custom.marketing.proof-first-landing',A)
        req(local_meta.get('local_workflow') is True and 'Proof First Landing Workflow' in local_content,'local Workflow resolution failed')

        config,_=configure(A,'workflow_only','anonymous',True,['shared/innovation-index.json'],None);req('prompt_mode' not in config,'innovation config reintroduced pseudo prompting behavior')
        package,draft=prepare_package(A,local_extension['id'],detail='workflow_only',identity='anonymous');req(package['privacy']['user_approved_export'] is False,'prepared package must remain unapproved');req('capabilities' not in json.dumps(package),'InnovationPackage reintroduced capability ontology');req(package['process'].get('local_workflow_id')=='custom.marketing.proof-first-landing','shared process lost local Workflow identity')
        zip_path=tmp/'innovation.zip';exported,_=export_package(draft,zip_path,approved=True);validate_package(load_package(zip_path),require_export_approval=True);req(exported['identity_level']=='anonymous' and exported['detail_level']=='workflow_only','sharing presets changed unexpectedly')
        try:bounded_summary({'api_key':'should-never-export'},'test')
        except ValueError:pass
        else:raise AssertionError('secret-like fields were not rejected')

        entry,source_record,stored=import_package(B,zip_path);req(entry['compatibility_status']=='compatible','package unexpectedly incompatible');req(source_record.get('source_reference')==str(stored.relative_to(ROOT)),'imported SourceRecord does not point to stored package evidence');req(json.loads(innovation_entry_path(B,entry['id']).read_text()).get('object_type') is None,'Innovation Exchange support entry became canonical state');req(not any(obj.get('object_type')=='Insight' for obj,_ in iter_instance_objects(B)),'package import manufactured semantic Insight')

        # Imported support may later gain local evidence without turning popularity into truth.
        evaluation={'id':'eval_exchange_test','object_type':'OutcomeEvaluation','schema_version':'1.0.0','business_id':B,'owner_system':'marketing-synthesis','target_refs':[],'attribution_method':'controlled_test','causal_confidence':0.8,'conclusion':'The imported Workflow was supported in this bounded local test.','extensions':{}}
        ep=ROOT/'instances'/B/'measurement'/'outcome-evaluations'/'eval_exchange_test.json';ep.parent.mkdir(parents=True,exist_ok=True);ep.write_text(json.dumps(evaluation,indent=2)+'\n')
        record_outcome(B,entry['id'],'supported','eval_exchange_test');again=record_outcome(B,entry['id'],'supported','eval_exchange_test');req(again['local_evidence']['supported_count']==1,'duplicate local outcome was not idempotent');feed=list_entries(B,compatible_only=True);req(feed and feed[0]['local_supported']==1,'Innovation Exchange did not surface local outcome evidence')

        workflow_path,workflow_meta=resolve_contract('core.learning.workflow-evolution');req(workflow_path.exists() and workflow_meta.get('type')=='workflow','Workflow evolution procedure is not resolvable as a Workflow')
        exchange_path,exchange_meta=resolve_contract('core.intelligence.innovation-exchange');req(exchange_path.exists() and exchange_meta.get('type')=='workflow','Innovation Exchange procedure is not resolvable as a Workflow')
        print('Workflow evolution + Innovation Exchange regressions passed without capability/runtime authority')
    finally:
        if prior is None:os.environ.pop('BUSINESSOS_WORKSPACE',None)
        else:os.environ['BUSINESSOS_WORKSPACE']=prior
        shutil.rmtree(tmp,ignore_errors=True)

if __name__=='__main__':main()
