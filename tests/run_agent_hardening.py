#!/usr/bin/env python3
"""Protect AURA's agent-facing boundary without recreating an execution control plane.

This regression focuses on invariants AURA can actually own:
- explicit organization truth carries real source provenance;
- semantic normalization belongs to the capable model, not a keyword/stemming gate;
- outward business claims remain literally evidence-bounded;
- valid work does not require a Run or AURA playbook;
- the front door retrieves candidates without taking over execution;
- AURA domains remain bodies of operating knowledge rather than internal semantic services;
- process maps remain navigation/composition aids rather than execution graphs;
- flagship production and journey methods do not manufacture WorkRequest/Run/lifecycle ceremony;
- Marketing composition does not turn strategy/production steps into an internal job queue;
- retired semantic routing/orchestration/approval/event-control machinery stays physically absent.
"""
from pathlib import Path
import json,re,shutil,subprocess,sys

ROOT=Path(__file__).resolve().parents[1];SCRIPTS=ROOT/'scripts';sys.path.insert(0,str(SCRIPTS))
from _common import read_frontmatter,selector_type
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
        objects=build_objects(BID,industries=['residential HVAC'],markets=['Baltimore service area'],services=['installation','repair','maintenance'],objectives=['profitable growth'],source_text=SOURCE)
        for obj in objects:write_json(_path(BASE,obj),obj)

        errors,_,counts=validate_business(BID,True)
        require(not errors,f'provenanced organization context should validate: {errors}')
        require(counts.get('Business')==1 and counts.get('ProductService')==3,f'expected business/service context: {counts}')

        market=next((BASE/'context/markets').glob('*.json'));original=market.read_text();obj=json.loads(original)
        obj['extensions']['businessos']['source_ref']='src_missing_explicit_source';market.write_text(json.dumps(obj,indent=2)+'\n')
        errors,_,_=validate_business(BID,True)
        require(any('requires an existing SourceRecord source_ref' in e for e in errors),f'explicit context with missing provenance should fail: {errors}')
        market.write_text(original)

        srcp=next((BASE/'intelligence/sources').glob('src_*explicit*.json'));src=json.loads(srcp.read_text());srcid=src['id'];ts=src['created_at']
        claim={
            'id':f'clm_{BID}_written-estimates','object_type':'BusinessClaim','schema_version':'1.0.0','business_id':BID,
            'created_at':ts,'updated_at':ts,'lineage':[srcid],'statement':'We provide written estimates.',
            'claim_kind':'approved_business_claim','status':'approved','authority':'explicit_user','source_ref':srcid,
            'support_quote':'We provide written estimates.',
            'extensions':{'businessos':{'fact_status':'known','authority':'explicit_user','source_ref':srcid,'grounding_method':GROUNDING_METHOD,'grounding_version':'1.0'}}
        }
        cp=BASE/'context/claims'/f"{claim['id']}.json";write_json(cp,claim)

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
            ROOT/'core/contracts/intelligence/ecosystem/route-learning',ROOT/'core/contracts/intelligence/request-refresh',
            ROOT/'core/contracts/intelligence/evaluate-relevance',ROOT/'systems/marketing-synthesis/contracts/offer/context-proposal',
            ROOT/'core/contracts/learning/promote-learning',ROOT/'templates/manual-action.md',
        ]
        for path in retired:require(not path.exists(),f'retired control/router/orchestrator artifact reappeared: {path.relative_to(ROOT)}')
        for path in ROOT.glob('systems/*/contracts/intelligence/relevance-evaluation'):
            require(not path.exists(),f'domain semantic relevance dispatcher reappeared: {path.relative_to(ROOT)}')

        core_map=json.loads((ROOT/'core/process-map.json').read_text())
        entries={a.get('entry_contract') for a in core_map.get('activities',[])}
        for cid in ['core.routing.resolve-intent','core.coordination.multi-domain-request','core.intelligence.ecosystem.route-learning','core.intelligence.request-refresh','core.intelligence.evaluate-relevance','core.learning.promote-learning']:
            require(cid not in entries,f'Core process map reintroduced retired routing/orchestration/promotion entry: {cid}')

        # Process maps are browse/composition aids, not execution graphs.
        execution_graph_keys={'next','next_contract','depends_on','dependencies','sequence','order','routes_to','delegate_to','on_success','on_failure'}
        process_maps=[ROOT/'core/process-map.json',*ROOT.glob('systems/*/process-map.json')]
        for path in process_maps:
            data=json.loads(path.read_text(encoding='utf-8'))
            for activity in data.get('activities',[]):
                bad=execution_graph_keys & set(activity)
                require(not bad,f'{path.relative_to(ROOT)} reintroduced execution-graph metadata on {activity.get("id")}: {sorted(bad)}')

        # AURA domains are reusable bodies of expertise, not internal semantic services.
        domain_defaults=list(ROOT.glob('systems/*/DEFAULTS.md'))
        require(domain_defaults,'expected installed domain defaults')
        service_phrases=[
            'route them to the semantic owner','route to the correct owner',
            'route persuasion/content/sales/product work through the correct owner',
            'another domain already owns the opportunity and requests production',
            'route that interpretation to competitor intelligence','upstream semantic owners',
        ]
        for path in domain_defaults:
            text=path.read_text(encoding='utf-8');low=text.lower()
            require('## Knowledge Scope' in text,f'{path.relative_to(ROOT)} lost knowledge-scope framing')
            for phrase in service_phrases:require(phrase not in low,f'{path.relative_to(ROOT)} recreated internal domain-service routing: {phrase}')

        mandatory_run_phrases=('required run root','record_contract_completion.py','finalize_run.py','run contract-execution manifest','under the active run')

        # Flagship Marketing production roots produce the work itself. A WorkRequest may
        # be consumed as real continuity context, but it is not a mandatory internal output.
        marketing_roots=[]
        for path in ROOT.glob('systems/marketing-synthesis/contracts/assets/*/CONTEXT.md'):
            meta,body=read_frontmatter(path)
            if meta.get('artifact_role')!='customer_facing_production_root':continue
            marketing_roots.append(path);writes={selector_type(x) for x in meta.get('writes',[])}
            require('WorkRequest' not in writes,f'{path.relative_to(ROOT)} recreated mandatory internal WorkRequest production')
            for phrase in mandatory_run_phrases:require(phrase not in body.lower(),f'{path.relative_to(ROOT)} recreated mandatory Run/conformance machinery: {phrase}')
        require(marketing_roots,'expected flagship Marketing production roots')

        # Marketing strategy and ordinary composition leaves return reusable strategy/work,
        # not an internal AURA job queue. Direct canonical updates happen only when truth
        # is actually established; routine strategy must not create context-proposal flow.
        strategy_paths=list(ROOT.glob('systems/marketing-synthesis/contracts/strategy/*/CONTEXT.md'))
        require(strategy_paths,'expected Marketing strategy methods')
        positive_context_proposal=re.compile(r'\b(?:create|produce|persist|write)\s+(?:a\s+)?(?:core\s+)?(?:`)?context(?:update|\s+change)\s*proposal',re.I)
        for path in strategy_paths:
            meta,body=read_frontmatter(path);writes={selector_type(x) for x in meta.get('writes',[])}
            require('WorkRequest' not in writes,f'{path.relative_to(ROOT)} recreated internal WorkRequest strategy output')
            require(not positive_context_proposal.search(body),f'{path.relative_to(ROOT)} recreated routine ContextUpdateProposal workflow')

        direct_marketing_families=('ads','landing-page','webinar','email')
        for family in direct_marketing_families:
            for path in ROOT.glob(f'systems/marketing-synthesis/contracts/{family}/*/CONTEXT.md'):
                meta,body=read_frontmatter(path);writes={selector_type(x) for x in meta.get('writes',[])}
                require('WorkRequest' not in writes,f'{path.relative_to(ROOT)} recreated internal WorkRequest composition')
                for phrase in mandatory_run_phrases:require(phrase not in body.lower(),f'{path.relative_to(ROOT)} recreated mandatory Run/conformance machinery: {phrase}')

        prepublish=ROOT/'systems/content-synthesis/contracts/qa/pre-publish/CONTEXT.md'
        pmeta,pbody=read_frontmatter(prepublish);pwrites={selector_type(x) for x in pmeta.get('writes',[])}
        require('WorkRequest' not in pwrites,'Content pre-publish QA recreated internal WorkRequest production')
        for phrase in mandatory_run_phrases:require(phrase not in pbody.lower(),f'Content pre-publish QA recreated mandatory Run/conformance machinery: {phrase}')

        # Journey interventions may create durable meaning when it really occurs, but an
        # intervention is not automatically a five-object lifecycle.
        generic_intervention_lifecycle={'WorkRequest','ChangeEvent','Experiment','MetricObservation','OutcomeEvaluation'}
        internal_domain_delegate=re.compile(r'\b(?:route|delegate)\b.*\b(?:marketing|content|customer intelligence|competitor intelligence|industry intelligence|seo/aeo)\b',re.I)
        negative_delegate=('do not route','do not delegate','not route','not delegate','rather than route','rather than delegate')
        intervention_paths=list(ROOT.glob('systems/customer-optimization/contracts/intervention/*/CONTEXT.md'))
        require(intervention_paths,'expected Customer Optimization interventions')
        for path in intervention_paths:
            meta,body=read_frontmatter(path);writes={selector_type(x) for x in meta.get('writes',[])}
            require(not generic_intervention_lifecycle<=writes,f'{path.relative_to(ROOT)} recreated generic intervention lifecycle')
            for line in body.splitlines():
                low=line.lower()
                if internal_domain_delegate.search(line) and not any(marker in low for marker in negative_delegate):
                    require(False,f'{path.relative_to(ROOT)} recreated internal domain delegation: {line.strip()}')

        memory_contracts=[
            'core/contracts/intelligence/publish-observation/CONTEXT.md','core/contracts/intelligence/manage-insight/CONTEXT.md',
            'core/contracts/opportunity/qualify/CONTEXT.md','core/contracts/measurement/publish-metric/CONTEXT.md',
            'core/contracts/measurement/evaluate-outcome/CONTEXT.md',
        ]
        runtime_event_pattern=re.compile(r'\bemit\s+[a-z][a-z0-9_-]*\.[a-z][a-z0-9_.-]*',re.I)
        for rel in memory_contracts:
            text=(ROOT/rel).read_text(encoding='utf-8')
            require('Manual Action Packet' not in text,f'{rel} reintroduced retired manual-action fallback')
            require(runtime_event_pattern.search(text) is None,f'{rel} reintroduced named runtime event emission')

        forbidden_manual_fallbacks=['if a required capability is unavailable, create a human-executable manual action packet','or create a manual action packet']
        negative_emit_markers=('do not emit','does not emit','never emit','without emitting','not emit')
        for path in ROOT.rglob('CONTEXT.md'):
            if '/contracts/' not in path.as_posix():continue
            text=path.read_text(encoding='utf-8');low=text.lower()
            for phrase in forbidden_manual_fallbacks:require(phrase not in low,f'{path.relative_to(ROOT)} reintroduced retired Manual Action Packet fallback: {phrase}')
            for line in text.splitlines():
                line_low=line.lower()
                if re.search(r'\bemit(?:s|ted|ting)?\b',line_low) and not any(marker in line_low for marker in negative_emit_markers):
                    require(False,f'{path.relative_to(ROOT)} reintroduced positive runtime-event emission prose: {line.strip()}')

        errors,_,_=validate_business(BID,True);require(not errors,f'current architecture should finish with valid organization state: {errors}')
        print('agent hardening regressions passed: provenance and outward truth remain strong without semantic-routing/orchestration/event-control baggage')
    finally:
        if BASE.exists():shutil.rmtree(BASE)
        rbase=ROOT/'runtime/runs'/BID
        if rbase.exists():shutil.rmtree(rbase)

if __name__=='__main__':main()
