#!/usr/bin/env python3
"""Regression for evidence-based Workflow evolution and Innovation Exchange without semantic/runtime authority."""
from pathlib import Path
import json,re,shutil,sys,tempfile
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from persist_workflow_evolution import persist_proposal
from adopt_process_extension import adopt_extension
from process_extensions import resolve_effective,local_workflow_candidates
from prepare_innovation_package import prepare_package
from export_innovation_package import export_package
from innovation_common import validate_package,load_package,bounded_summary,innovation_entry_path
from import_innovation_package import import_package
from record_innovation_outcome import record_outcome
from list_innovation_exchange import list_entries
from configure_innovation_sharing import configure
from build_innovation_exchange_index import build_index
from browse_innovation_exchange_index import browse
from find_workflows import find_candidates
from resolve_contract import resolve_contract
A='test-evolution-a';B='test-evolution-b'
NEW_WORKFLOWS=['core/contracts/learning/workflow-evolution/CONTEXT.md','core/contracts/learning/adopt-process-extension/CONTEXT.md','core/contracts/intelligence/innovation-exchange/CONTEXT.md','core/contracts/intelligence/community-evidence-review/CONTEXT.md']
def fail(msg):raise AssertionError(msg)
def contains(text,*parts):
    low=text.lower();return all(str(p).lower() in low for p in parts)
def make_business(bid):
    base=ROOT/'instances'/bid;base.mkdir(parents=True,exist_ok=True);(base/'instance.json').write_text(json.dumps({'business_id':bid,'enabled_systems':['marketing-synthesis']},indent=2)+'\n');return base
def learning(base,bid):
    obj={'id':'lrn_evolution_test','object_type':'Learning','schema_version':'1.0.0','business_id':bid,'owner_scope':'business','owner_system':'marketing-synthesis','statement':'Proof-first landing structure improved qualified conversion in the tested context.','maturity':'validated','status':'active','applies_when':['Evidence-backed landing page work'],'does_not_apply_when':[],'evidence_refs':[],'confidence':0.9,'extensions':{}};path=base/'learning'/'lrn_evolution_test.json';path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(obj,indent=2)+'\n');return obj
def _check_workflow_shape(rel):
    text=(ROOT/rel).read_text();front=text.split('\n---\n',1)[0];body=text.split('\n---\n',1)[1] if '\n---\n' in text else text
    if 'type: workflow' not in front:fail(f'{rel} is not typed as Workflow')
    for heading in ['## Purpose','## Business Outcome','## Run When','## Process']:
        if heading not in body:fail(f'{rel} missing required section {heading}')
    process=re.search(r'## Process\n(.*?)(?=\n## |\Z)',body,re.S)
    if process is not None and not process.group(1).strip():fail(f'{rel} has an empty Process section')
def _candidate_ids(rows):return [row.get('workflow_id') for row in rows if isinstance(row,dict)]
def main():
    for rel in ['core/policies/workflow-evolution.md','core/policies/process-extensions.md','core/policies/innovation-exchange.md',*NEW_WORKFLOWS,'core/schemas/learning/workflow-evolution-proposal.schema.json','core/schemas/learning/process-extension.schema.json','core/schemas/intelligence/innovation-package.schema.json','core/schemas/intelligence/innovation-exchange-entry.schema.json','core/schemas/config/innovation-sharing.schema.json','core/schemas/intelligence/innovation-exchange-index.schema.json']:
        if not (ROOT/rel).exists():fail(f'missing {rel}')
    for rel in NEW_WORKFLOWS:_check_workflow_shape(rel)
    for rel in ['core/capabilities/catalog.json','docs/adding-a-capability.md','core/schemas/learning/playbook-evolution-proposal.schema.json','scripts/persist_playbook_evolution.py','core/policies/playbook-evolution.md']:
        if (ROOT/rel).exists():fail(f'retired capability/flattened-playbook artifact remains: {rel}')
    for path in ['core/schemas/learning/workflow-evolution-proposal.schema.json','core/schemas/learning/process-extension.schema.json']:
        text=(ROOT/path).read_text()
        for retired in ['risk','autonomy_ceiling','approval_required','priority','extension_version','route_terms','required_capabilities','optional_capabilities','target_contract_id','local_contract_id','proposed_local_contract_id']:
            if f'"{retired}"' in text:fail(f'{path} still encodes retired process/tool/contract field {retired}')
    process_schema=json.loads((ROOT/'core/schemas/learning/process-extension.schema.json').read_text())
    if process_schema.get('additionalProperties') is not False:fail('ProcessExtension schema must be strict')
    if 'discovery_terms' not in process_schema.get('properties',{}):fail('ProcessExtension lost bounded local Workflow discovery terms')
    exchange_schema=json.loads((ROOT/'core/schemas/intelligence/innovation-exchange-entry.schema.json').read_text())
    if 'object_type' in exchange_schema.get('properties',{}):fail('InnovationExchangeEntry must remain non-canonical support state')
    if not {'target_workflow_id','local_workflow_id'} <= set(exchange_schema.get('properties',{})):fail('InnovationExchangeEntry lost Workflow identity')
    sharing_schema=json.loads((ROOT/'core/schemas/config/innovation-sharing.schema.json').read_text())
    if 'prompt_mode' in sharing_schema.get('properties',{}):fail('innovation sharing config reintroduced pseudo prompting/runtime behavior')
    policy=(ROOT/'core/policies/innovation-exchange.md').read_text()
    for phrase in ['No automatic sharing','workflow_only','anonymized_evidence','full_case_study','anonymous','pseudonymous','named','does **not** manufacture an `Insight`']:
        if phrase not in policy:fail(f'innovation policy missing {phrase}')
    if 'candidate Insight -> triangulation -> ignore/watch/investigate/test/adopt' in policy:fail('innovation policy restored synthetic semantic pipeline')

    source=(ROOT/'core/contracts/intelligence/ecosystem/source-discovery/CONTEXT.md').read_text();source_meta=source.split('\n---\n',1)[0]
    if '- InnovationExchangeEntry' in source_meta:fail('ecosystem discovery reintroduced exchange support data as canonical organization state')
    for concepts in [('exchange/index files','support data','canonical organization truth'),('innovation exchange contributions','discovery'),('discovery-only','support-grade evidence'),('popularity','repetition','independent evidence'),('semantic source identity','model/user')]:
        if not contains(source,*concepts):fail(f'ecosystem discovery lost innovation/evidence boundary: {concepts}')

    for bid in [A,B]:shutil.rmtree(ROOT/'instances'/bid,ignore_errors=True)
    shutil.rmtree(ROOT/'runtime'/'innovation'/A,ignore_errors=True);tmpdir=Path(tempfile.mkdtemp(prefix='aura-innovation-test-'))
    try:
        abase=make_business(A);bbase=make_business(B);learning(abase,A)
        proposal_payload={'owner_system':'marketing-synthesis','change_kind':'augment_existing','proposed_scope':'business','target_workflow_id':'marketing.assets.landing-page','proposed_local_workflow_id':None,'title':'Proof-first landing page extension','summary':'Add the validated proof-first sequence when evidence conditions match.','learning_refs':['lrn_evolution_test'],'evidence_refs':[],'applies_when':['Suitable proof exists'],'does_not_apply_when':['Proof is unavailable'],'discovery_terms':[],'reads':[],'writes':['DecisionRecord'],'instructions':['Lead the relevant persuasion sequence with the strongest supported proof before unsupported persuasion claims.'],'verification':['Confirm proof claims retain evidence/claim lineage.']}
        proposal,_=persist_proposal(A,proposal_payload);extension,_=adopt_extension(A,proposal['id']);_,meta,content,extensions=resolve_effective('marketing.assets.landing-page',A)
        if extension['id'] not in [item['id'] for item in extensions] or 'Proof-first landing page extension' not in content:fail('adopted extension not visible in effective Workflow')
        if 'DecisionRecord' not in meta.get('writes',[]):fail('extension durable-output metadata was incorrectly constrained by base Workflow writes')
        if any(key in meta for key in ['risk','autonomy_ceiling','version','capabilities']):fail('effective Workflow reintroduced retired authority/version/tool metadata')
        local_payload=dict(proposal_payload);local_payload.update({'change_kind':'new_local_workflow','target_workflow_id':None,'proposed_local_workflow_id':'custom.marketing.proof-first-landing','title':'Proof First Landing Workflow','summary':'A reusable local Workflow for proof-first landing-page planning.','discovery_terms':['proof first landing','proof-first workflow'],'writes':[]});local_proposal,_=persist_proposal(A,local_payload);local_extension,_=adopt_extension(A,local_proposal['id'])
        local_candidates=local_workflow_candidates('Use our proof first landing workflow',A)
        if 'custom.marketing.proof-first-landing' not in [row.get('workflow_id') for row in local_candidates]:fail('local Workflow candidate discovery failed')
        if any(row.get('selection_authority') is not False for row in local_candidates):fail('local Workflow candidates claimed semantic selection authority')
        _,local_meta,local_content,_=resolve_effective('custom.marketing.proof-first-landing',A)
        if not local_meta.get('local_workflow') or 'Proof First Landing Workflow' not in local_content:fail('explicit local Workflow resolution failed')

        config,_=configure(A,'workflow_only','anonymous',True,['shared/innovation-index.json'],None)
        if 'prompt_mode' in config:fail('innovation config retained pseudo prompting behavior')
        if not config['exchange_discovery_enabled'] or config['exchange_sources']!=['shared/innovation-index.json']:fail('innovation sharing/discovery config did not persist')
        package,draft=prepare_package(A,local_extension['id'],detail='workflow_only',identity='anonymous')
        if package['privacy']['user_approved_export']:fail('prepared package must remain unapproved draft')
        if 'aura_version' not in package or 'businessos_version' in package:fail('InnovationPackage retained legacy product-version naming')
        proc=package.get('process',{})
        if not {'target_workflow_id','local_workflow_id'} <= set(proc) or {'target_contract_id','local_contract_id','capabilities'} & set(proc):fail('InnovationPackage did not preserve clean Workflow semantics')
        zip_path=tmpdir/'innovation.zip';exported,_=export_package(draft,zip_path,approved=True);validate_package(load_package(zip_path),require_export_approval=True);index,index_path=build_index(tmpdir,'test-exchange');found=browse(index_path,'proof first')
        if len(index['entries'])!=1 or not found['entries'] or found['entries'][0]['package_id']!=exported['package_id']:fail('portable exchange index discovery failed')
        if exported['identity_level']!='anonymous' or exported['detail_level']!='workflow_only':fail('package sharing presets changed unexpectedly')
        try:bounded_summary({'api_key':'should-never-export'},'test')
        except ValueError:pass
        else:fail('secret-like fields were not rejected')

        entry,source_record,stored=import_package(B,zip_path)
        if entry['compatibility_status']!='compatible':fail(f"package unexpectedly incompatible: {entry['compatibility_status']}")
        if source_record.get('source_reference')!=str(stored.relative_to(ROOT)):fail('imported SourceRecord does not point to exact stored package evidence')
        support_entry=json.loads(innovation_entry_path(B,entry['id']).read_text())
        if support_entry.get('object_type') is not None:fail('exchange support entry became canonical organization state')
        if {'target_contract_id','local_contract_id'} & set(support_entry):fail('exchange support entry retained contract vocabulary')
        if any(obj.get('object_type')=='Insight' for obj,_ in __import__('_common').iter_instance_objects(B)):fail('package import manufactured a semantic Insight')
        entry2,_,_=import_package(B,zip_path)
        if entry2['reported_evidence']['contribution_count']!=1:fail('duplicate package import inflated contribution count')

        evaluation={'id':'eval_exchange_test','object_type':'OutcomeEvaluation','schema_version':'1.0.0','business_id':B,'owner_system':'marketing-synthesis','target_refs':[],'attribution_method':'controlled_test','causal_confidence':0.8,'conclusion':'The imported Workflow was supported in this bounded local test.','extensions':{}};evaluation_path=bbase/'measurement'/'eval_exchange_test.json';evaluation_path.parent.mkdir(parents=True,exist_ok=True);evaluation_path.write_text(json.dumps(evaluation,indent=2)+'\n');record_outcome(B,entry['id'],'supported','eval_exchange_test');entry4=record_outcome(B,entry['id'],'supported','eval_exchange_test')
        if entry4['local_evidence']['supported_count']!=1:fail('duplicate local outcome event was not idempotent')
        feed=list_entries(B,compatible_only=True)
        if not feed or feed[0]['id']!=entry['id'] or feed[0]['local_supported']!=1:fail('local innovation support view did not surface evidence')

        evolution_candidates=find_candidates('Improve this reusable workflow from what we learned',5)
        if 'core.learning.workflow-evolution' not in _candidate_ids(evolution_candidates):fail('Workflow evolution candidate missing')
        evolution_path,evolution_meta=resolve_contract('core.learning.workflow-evolution')
        if evolution_meta.get('id')!='core.learning.workflow-evolution' or not evolution_path.exists():fail('explicit Workflow evolution resolution failed')
        exchange_candidates=find_candidates('Share this workflow through the innovation exchange',5)
        if 'core.intelligence.innovation-exchange' not in _candidate_ids(exchange_candidates):fail('Innovation Exchange Workflow candidate missing')
        exchange_path,exchange_meta=resolve_contract('core.intelligence.innovation-exchange')
        if exchange_meta.get('id')!='core.intelligence.innovation-exchange' or not exchange_path.exists():fail('explicit Innovation Exchange Workflow resolution failed')
        print('Workflow evolution + Innovation Exchange regressions passed without capability ontology or semantic/runtime authority')
    finally:
        for bid in [A,B]:shutil.rmtree(ROOT/'instances'/bid,ignore_errors=True)
        shutil.rmtree(ROOT/'runtime'/'innovation'/A,ignore_errors=True);shutil.rmtree(tmpdir,ignore_errors=True)
if __name__=='__main__':main()
