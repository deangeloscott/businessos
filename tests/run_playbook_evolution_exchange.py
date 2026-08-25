#!/usr/bin/env python3
"""End-to-end regression checks for playbook evolution, extensions, innovation packages, and community evidence."""
from pathlib import Path
import json,re,shutil,sys,tempfile
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))

from persist_playbook_evolution import persist_proposal
from adopt_process_extension import adopt_extension
from process_extensions import resolve_effective,effective_capabilities,route_local_playbook
from prepare_innovation_package import prepare_package
from export_innovation_package import export_package
from innovation_common import validate_package,load_package,bounded_summary
from import_innovation_package import import_package
from record_innovation_outcome import record_outcome
from list_innovation_exchange import list_entries
from configure_innovation_sharing import configure
from build_innovation_exchange_index import build_index
from browse_innovation_exchange_index import browse
from route_and_resolve import route_and_resolve

A='test-evolution-a';B='test-evolution-b'
NEW_CONTRACTS=[
    'core/contracts/learning/playbook-evolution/CONTEXT.md',
    'core/contracts/learning/adopt-process-extension/CONTEXT.md',
    'core/contracts/intelligence/innovation-exchange/CONTEXT.md',
    'core/contracts/intelligence/community-evidence-review/CONTEXT.md',
]

def fail(msg):raise AssertionError(msg)

def make_business(bid):
    base=ROOT/'instances'/bid;base.mkdir(parents=True,exist_ok=True);(base/'instance.json').write_text(json.dumps({'business_id':bid,'enabled_systems':['marketing-synthesis']},indent=2)+'\n');return base

def learning(base,bid):
    obj={'id':'lrn_evolution_test','object_type':'Learning','schema_version':'1.0.0','business_id':bid,'owner_scope':'business','owner_system':'marketing-synthesis','statement':'Proof-first landing structure improved qualified conversion in the tested context.','maturity':'validated','status':'active','applies_when':['Evidence-backed landing page work'],'does_not_apply_when':[],'evidence_refs':[],'confidence':0.9,'system_learning_eligible':False,'extensions':{}}
    p=base/'learning'/'lrn_evolution_test.json';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2)+'\n');return obj

def _check_contract_shape(rel):
    text=(ROOT/rel).read_text()
    body=text.split('\n---\n',1)[1] if '\n---\n' in text else text
    for heading in ['## Purpose','## Business Outcome','## Run When','## Process']:
        if heading not in body:fail(f'{rel} missing required section {heading}')
    proc=re.search(r'## Process\n(.*?)(?=\n## |\Z)',body,re.S)
    steps=re.findall(r'^\d+\.\s+',proc.group(1),re.M) if proc else []
    if len(steps)<5:fail(f'{rel} has fewer than 5 process steps')
    if not re.search(r'\[(AI|DETERMINISTIC|INTEGRATION|HUMAN|HYBRID)\]',proc.group(1) if proc else ''):fail(f'{rel} has no executor labels')

def main():
    for rel in ['core/policies/playbook-evolution.md','core/policies/process-extensions.md','core/policies/innovation-exchange.md',*NEW_CONTRACTS,'core/schemas/learning/playbook-evolution-proposal.schema.json','core/schemas/learning/process-extension.schema.json','core/schemas/intelligence/innovation-package.schema.json','core/schemas/intelligence/innovation-exchange-entry.schema.json','core/schemas/config/innovation-sharing.schema.json','core/schemas/intelligence/innovation-exchange-index.schema.json']:
        if not (ROOT/rel).exists():fail(f'missing {rel}')
    for rel in NEW_CONTRACTS:_check_contract_shape(rel)
    policy=(ROOT/'core/policies/innovation-exchange.md').read_text()
    for phrase in ['No automatic sharing','workflow_only','anonymized_evidence','full_case_study','anonymous','pseudonymous','named']:
        if phrase not in policy:fail(f'innovation policy missing {phrase}')
    source=(ROOT/'core/contracts/intelligence/ecosystem/source-discovery/CONTEXT.md').read_text()
    if 'InnovationExchangeEntry' not in source or 'Innovation Exchange popularity/repetition is never counted as independent evidence' not in source:fail('ecosystem discovery is not wired to innovation exchange evidence boundary')
    process_schema=json.loads((ROOT/'core/schemas/learning/process-extension.schema.json').read_text())
    if process_schema.get('additionalProperties') is not False:fail('ProcessExtension schema must be strict')
    for bid in [A,B]:shutil.rmtree(ROOT/'instances'/bid,ignore_errors=True)
    shutil.rmtree(ROOT/'runtime'/'innovation'/A,ignore_errors=True);tmpdir=Path(tempfile.mkdtemp(prefix='businessos-innovation-test-'))
    try:
        abase=make_business(A);bbase=make_business(B);learning(abase,A)
        proposal_payload={'owner_system':'marketing-synthesis','change_kind':'augment_existing','proposed_scope':'business','target_contract_id':'marketing.assets.landing-page','proposed_local_contract_id':None,'title':'Proof-first landing page extension','summary':'Add the validated proof-first sequence when evidence conditions match.','learning_refs':['lrn_evolution_test'],'evidence_refs':[],'applies_when':['Suitable proof exists'],'does_not_apply_when':['Proof is unavailable'],'route_terms':[],'reads':[],'writes':[],'required_capabilities':['document.read'],'optional_capabilities':[],'risk':'medium','autonomy_ceiling':2,'instructions':['Lead the relevant persuasion sequence with the strongest approved proof before unsupported persuasion claims.'],'verification':['Confirm all proof claims retain approved evidence/claim lineage.']}
        bad_augment=dict(proposal_payload);bad_augment.update({'title':'Unsafe augment test','summary':'This test attempts to add a new undeclared canonical write type.','writes':['PlatformChange']});bad_prop,_=persist_proposal(A,bad_augment)
        try:adopt_extension(A,bad_prop['id'],approved=True)
        except ValueError as e:
            if 'may not introduce new canonical write types' not in str(e):raise
        else:fail('augmenting extension was allowed to introduce a new undeclared canonical write lifecycle')
        proposal,_=persist_proposal(A,proposal_payload);ext,_=adopt_extension(A,proposal['id'],approved=True);_,meta,content,exts=resolve_effective('marketing.assets.landing-page',A)
        if ext['id'] not in [x['id'] for x in exts] or 'Proof-first landing page extension' not in content:fail('adopted augmenting extension not visible in effective contract')
        if 'document.read' not in effective_capabilities('marketing.assets.landing-page',A)['required']:fail('extension required capability not visible to effective preflight metadata')
        if meta.get('autonomy_ceiling',4)>2:fail('extension did not tighten autonomy ceiling')
        local_payload=dict(proposal_payload);local_payload.update({'change_kind':'new_local_playbook','target_contract_id':None,'proposed_local_contract_id':'custom.marketing.proof-first-landing','title':'Proof First Landing Workflow','summary':'A reusable local workflow for proof-first landing-page planning.','route_terms':['proof first landing','proof-first workflow'],'required_capabilities':[]})
        local_prop,_=persist_proposal(A,local_payload);local_ext,_=adopt_extension(A,local_prop['id'],approved=True);routed=route_local_playbook('Use our proof first landing workflow',A)
        if not routed or routed['contract_id']!='custom.marketing.proof-first-landing':fail('local playbook routing failed')
        resolved=route_and_resolve('Use our proof first landing workflow',A)
        if not resolved.get('local_playbook'):fail('route_and_resolve did not resolve local playbook')
        _,local_meta,local_content,_=resolve_effective('custom.marketing.proof-first-landing',A)
        if not local_meta.get('local_playbook') or 'Proof First Landing Workflow' not in local_content:fail('local playbook effective resolution failed')
        cfg,_=configure(A,'ask_when_noteworthy','workflow_only','anonymous',True,['shared/innovation-index.json'],None)
        if not cfg['exchange_discovery_enabled'] or cfg['exchange_sources']!=['shared/innovation-index.json']:fail('innovation sharing/discovery configuration did not persist portable exchange source')
        pkg,draft=prepare_package(A,local_ext['id'],detail='workflow_only',identity='anonymous')
        if pkg['privacy']['user_approved_export']:fail('prepared package must remain unapproved draft')
        zip_path=tmpdir/'innovation.zip';exported,_=export_package(draft,zip_path,approved=True);validate_package(load_package(zip_path),require_export_approval=True);index,index_path=build_index(tmpdir,'test-exchange');found=browse(index_path,'proof first')
        if len(index['entries'])!=1 or not found['entries'] or found['entries'][0]['package_id']!=exported['package_id']:fail('portable exchange index/feed discovery failed')
        if exported['identity_level']!='anonymous' or exported['detail_level']!='workflow_only':fail('package sharing presets changed unexpectedly')
        try:bounded_summary({'api_key':'should-never-export'},'test')
        except ValueError:pass
        else:fail('secret-like fields were not rejected')
        entry,source_obj,insight,stored=import_package(B,zip_path)
        if entry['compatibility_status']!='compatible':fail(f"portable package unexpectedly incompatible: {entry['compatibility_status']}")
        entry2,_,_,_=import_package(B,zip_path)
        if entry2['reported_evidence']['contribution_count']!=1:fail('duplicate package import inflated contribution count')
        eval_obj={'id':'eval_exchange_test','object_type':'OutcomeEvaluation','schema_version':'1.0.0','business_id':B,'owner_system':'marketing-synthesis','target_refs':[],'attribution_method':'controlled_test','causal_confidence':0.8,'conclusion':'The imported workflow was supported in this bounded local test.','extensions':{}}
        ep=bbase/'measurement'/'eval_exchange_test.json';ep.parent.mkdir(parents=True,exist_ok=True);ep.write_text(json.dumps(eval_obj,indent=2)+'\n');entry3=record_outcome(B,entry['id'],'supported','eval_exchange_test');entry4=record_outcome(B,entry['id'],'supported','eval_exchange_test')
        if entry4['local_evidence']['supported_count']!=1:fail('duplicate local outcome event was not idempotent')
        feed=list_entries(B,compatible_only=True)
        if not feed or feed[0]['id']!=entry['id'] or feed[0]['local_supported']!=1:fail('local innovation feed did not surface recorded evidence')
        if route_and_resolve('Make this successful method a permanent BusinessOS playbook',A)['contract_id']!='core.learning.playbook-evolution':fail('playbook evolution natural-language route missing')
        if route_and_resolve('Share this workflow through the innovation exchange',A)['contract_id']!='core.intelligence.innovation-exchange':fail('innovation exchange natural-language route missing')
        print('playbook evolution + innovation exchange regressions passed end to end')
    finally:
        for bid in [A,B]:shutil.rmtree(ROOT/'instances'/bid,ignore_errors=True)
        shutil.rmtree(ROOT/'runtime'/'innovation'/A,ignore_errors=True);shutil.rmtree(tmpdir,ignore_errors=True)

if __name__=='__main__':main()
