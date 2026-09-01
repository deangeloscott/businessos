#!/usr/bin/env python3
"""Protect AURA's agent-facing boundary without recreating an execution control plane.

This regression focuses on invariants AURA can actually own:
- explicit organization truth carries real source provenance;
- semantic normalization belongs to the capable model, not a keyword/stemming gate;
- outward business claims remain literally evidence-bounded;
- valid work does not require a Run or AURA playbook;
- the front door retrieves candidates without taking over execution;
- retired semantic routing/orchestration/approval machinery stays physically absent.
"""
from pathlib import Path
import json,shutil,subprocess,sys

ROOT=Path(__file__).resolve().parents[1];SCRIPTS=ROOT/'scripts';sys.path.insert(0,str(SCRIPTS))
from bootstrap_explicit_context import build_objects,_path,GROUNDING_METHOD
from context_plan import build_plan
from enter import prepare_work
from validate_business import validate_business

BID='agent-hardening-regression';BASE=ROOT/'instances'/BID
SOURCE=(
    'My business is Northstar HVAC, a fictional residential HVAC company serving the Baltimore area. '
    'We install, repair, and maintain residential heating and cooling systems. '
    'Our main goal is profitable growth. We provide written estimates.'
)

def require(cond,msg):
    if not cond:raise AssertionError(msg)
def run(*args,check=True):return subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,capture_output=True,text=True,check=check)
def write_json(path,obj):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(obj,indent=2)+'\n')

def main():
    if BASE.exists():shutil.rmtree(BASE)
    try:
        run(SCRIPTS/'init_business.py',BID,'--name','Northstar HVAC')
        # These structured values are conservative model normalization of the supplied
        # source. AURA preserves provenance but does not re-interpret the English with a
        # hand-written semantic tokenizer.
        objects=build_objects(BID,industries=['residential HVAC'],markets=['Baltimore service area'],services=['installation','repair','maintenance'],objectives=['profitable growth'],source_text=SOURCE)
        for obj in objects:write_json(_path(BASE,obj),obj)

        errors,_,counts=validate_business(BID,True)
        require(not errors,f'provenanced organization context should validate: {errors}')
        require(counts.get('Business')==1 and counts.get('ProductService')==3,f'expected business/service context: {counts}')

        # What AURA can deterministically prove is provenance, not semantic equivalence.
        market=next((BASE/'context/markets').glob('*.json'));original=market.read_text();obj=json.loads(original)
        obj['extensions']['businessos']['source_ref']='src_missing_explicit_source';market.write_text(json.dumps(obj,indent=2)+'\n')
        errors,_,_=validate_business(BID,True)
        require(any('requires an existing SourceRecord source_ref' in e for e in errors),f'explicit context with missing provenance should fail: {errors}')
        market.write_text(original)

        # Persist one exact reusable business claim grounded to the original user source.
        srcp=next((BASE/'intelligence/sources').glob('src_*explicit*.json'));src=json.loads(srcp.read_text());srcid=src['id'];ts=src['created_at']
        claim={
            'id':f'clm_{BID}_written-estimates','object_type':'BusinessClaim','schema_version':'1.0.0','business_id':BID,
            'created_at':ts,'updated_at':ts,'lineage':[srcid],'statement':'We provide written estimates.',
            'claim_kind':'approved_business_claim','status':'approved','authority':'explicit_user','source_ref':srcid,
            'support_quote':'We provide written estimates.',
            'extensions':{'businessos':{'fact_status':'known','authority':'explicit_user','source_ref':srcid,'grounding_method':GROUNDING_METHOD,'grounding_version':'1.0'}}
        }
        cp=BASE/'context/claims'/f"{claim['id']}.json";write_json(cp,claim)

        # Literal evidence remains a real deterministic safeguard for outward claims.
        bad_claim=dict(claim);bad_claim['support_quote']='We guarantee same-day written estimates.'
        write_json(cp,bad_claim);errors,_,_=validate_business(BID,True)
        require(any('support_quote is not a literal excerpt' in e for e in errors),f'unsupported literal claim support should fail: {errors}')
        write_json(cp,claim)

        html=BASE/'assets/claim-regression.html';html.parent.mkdir(parents=True,exist_ok=True);html.write_text('<html><body><p>We provide written estimates.</p></body></html>')
        asset={
            'id':f'ast_{BID}_claim-regression','object_type':'Asset','schema_version':'1.0.0','business_id':BID,
            'created_at':ts,'updated_at':ts,'lineage':[claim['id']],'asset_type':'landing-page',
            'owner_system':'marketing-synthesis','business_role':'customer-facing draft',
            'location_reference':str(html.relative_to(ROOT)),'version':'1.0.0','status':'draft',
            'extensions':{'businessos':{'customer_facing':True,'claim_manifest':[{'text':'We provide written estimates.','classification':'approved_business_claim','support_refs':[claim['id']]}]}}
        }
        ap=BASE/'assets'/f"{asset['id']}.json";write_json(ap,asset)
        errors,_,_=validate_business(BID,True)
        require(not errors,f'valid customer-facing work must not require a Run: {errors}')
        require('run_ref' not in asset['extensions']['businessos'],'fixture accidentally depends on Run provenance')

        html.write_text('<html><body><p>We guarantee same-day written estimates.</p></body></html>')
        asset['extensions']['businessos']['claim_manifest']=[{'text':'We guarantee same-day written estimates.','classification':'approved_business_claim','support_refs':[claim['id']]}]
        write_json(ap,asset);errors,_,_=validate_business(BID,True)
        require(any('enlarges supported promise' in e for e in errors),f'unsupported outward promise expansion should fail: {errors}')
        html.write_text('<html><body><p>We provide written estimates.</p></body></html>');asset['extensions']['businessos']['claim_manifest']=[{'text':'We provide written estimates.','classification':'approved_business_claim','support_refs':[claim['id']]}];write_json(ap,asset)

        prepared=prepare_work('Draft a customer-facing landing page',business_id=BID,selected_contract_id='marketing.assets.landing-page')
        require(prepared.get('status')=='ready',f'front door should prepare bounded work context: {prepared}')
        require(prepared.get('run',{}).get('created') is False,f'front door must not create a Run merely to begin work: {prepared}')
        require({'aura_playbook','external_skill','model_created','ad_hoc'}<=set(prepared.get('method_options',[])),f'front door lost method freedom: {prepared}')
        require('not execution authority' in prepared.get('recommended_playbook',{}).get('rule',''),f'playbook selection became execution authority: {prepared}')

        plan=build_plan(BID,'marketing.assets.landing-page')
        require('core/policies/context-provenance-and-claims.md' in plan['files'],'outward marketing work should load reusable claim truth')
        require('core/policies/customer-facing-mutations.md' not in plan['files'],'deleted mutation gate returned to bounded context')
        require('core/DEFAULTS.md' not in plan['files'] and 'core/policies/agent-execution.md' not in plan['files'],'bounded context reintroduced redundant universal instructions')

        root_contract=(ROOT/'CONTEXT.md').read_text(encoding='utf-8')
        for phrase in ['not the model, semantic intent engine, universal orchestrator','The model/user decides semantic applicability.','Work normally.','A Run is an **optional bounded work receipt**']:
            require(phrase in root_contract,f'root agent contract lost first-principles boundary: {phrase}')

        agent=(ROOT/'core/policies/agent-execution.md').read_text(encoding='utf-8')
        require('AURA does not create generic `Approval` objects' in agent,'agent policy lost no-internal-approval boundary')
        require('Do not force work into an AURA contract merely to make it recordable' in agent,'agent policy lost method freedom')
        require('A bounded Run/work receipt is useful' in agent and 'not required before ordinary reasoning begins' in agent,'agent policy lost optional-Run boundary')

        claims=(ROOT/'core/policies/context-provenance-and-claims.md').read_text(encoding='utf-8')
        require('A valid customer-facing Asset does **not** require a Run' in claims,'claim policy lost optional-Run boundary')
        require('does **not** require a universal pre-edit snapshot' in claims,'claim policy reintroduced mutation ceremony')

        retired=[
            ROOT/'core/policies/approval.md',ROOT/'core/policies/operating-scope.md',ROOT/'core/policies/customer-facing-mutations.md',
            ROOT/'core/schemas/action/action-packet.schema.json',ROOT/'core/schemas/action/approval.schema.json',ROOT/'core/contracts/action-control',
            ROOT/'scripts/validate_customer_facing_mutations.py',ROOT/'scripts/capture_customer_facing_state.py',ROOT/'scripts/build_mutation_claim_manifest.py',
            ROOT/'core/contracts/routing/resolve-intent',ROOT/'core/contracts/coordination/multi-domain-request',
            ROOT/'core/contracts/intelligence/ecosystem/route-learning',
        ]
        for path in retired:require(not path.exists(),f'retired control/router/orchestrator artifact reappeared: {path.relative_to(ROOT)}')

        core_map=json.loads((ROOT/'core/process-map.json').read_text())
        entries={a.get('entry_contract') for a in core_map.get('activities',[])}
        for cid in ['core.routing.resolve-intent','core.coordination.multi-domain-request','core.intelligence.ecosystem.route-learning']:
            require(cid not in entries,f'Core process map reintroduced retired routing/orchestration entry: {cid}')

        errors,_,_=validate_business(BID,True);require(not errors,f'current architecture should finish with valid organization state: {errors}')
        print('agent hardening regressions passed: provenance and outward truth remain strong without semantic-routing/orchestration/execution-control baggage')
    finally:
        if BASE.exists():shutil.rmtree(BASE)
        rbase=ROOT/'runtime/runs'/BID
        if rbase.exists():shutil.rmtree(rbase)

if __name__=='__main__':main()
