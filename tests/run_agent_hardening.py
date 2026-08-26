#!/usr/bin/env python3
"""Focused regressions for agent-facing hardening. Safe: uses/removes one disposable instance and runtime file."""
from pathlib import Path
import json, shutil, subprocess, sys

ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/'scripts'
sys.path.insert(0,str(SCRIPTS))
from bootstrap_explicit_context import build_objects, GROUNDING_METHOD
from context_plan import build_plan
from route_task import route
from route_and_resolve import route_and_resolve
from validate_business import validate_business
from validate_research_evidence import evidence_errors
from validate_business_claims import claim_errors

BID='agent-hardening-regression'
BASE=ROOT/'instances'/BID
FACTS_PATH=ROOT/'runtime'/f'{BID}-facts.json'
SOURCE=(
    'My business is Northstar HVAC, a fictional residential HVAC company serving the Baltimore area. '
    'We make money installing, repairing, and maintaining residential heating and cooling systems. '
    'Our main goal is profitable growth. We currently get leads from organic search, Google Ads, referrals, and repeat customers. We provide written estimates. Do not use urgency or discounts.'
)
FACTS={
    'industries':['residential HVAC'],
    'markets':['Baltimore area'],
    'services':['installation','repair','maintenance'],
    'objectives':['profitable growth'],
    'lead_sources':['organic search','Google Ads','referrals','repeat customers'],
}

def require(cond,msg):
    if not cond: raise AssertionError(msg)

def run(*args,check=True):
    return subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,capture_output=True,text=True,check=check)

def main():
    if BASE.exists(): shutil.rmtree(BASE)
    FACTS_PATH.unlink(missing_ok=True)
    try:
        init=run(SCRIPTS/'init_business.py',BID,'--name','Northstar HVAC')
        require('bootstrap_explicit_context.py' in init.stdout and '--help' in init.stdout and '--residual-request' in init.stdout,'init_business should emit supported bootstrap + residual handoff')
        FACTS_PATH.parent.mkdir(parents=True,exist_ok=True); FACTS_PATH.write_text(json.dumps(FACTS))
        incomplete=run(SCRIPTS/'bootstrap_explicit_context.py','--business-id',BID,'--facts-file',FACTS_PATH,'--source-text',SOURCE,check=False)
        require(incomplete.returncode!=0 and 'completion scope is required' in incomplete.stderr,'conversational bootstrap must declare residual request or initialization-only scope before persistence')
        boot=run(SCRIPTS/'bootstrap_explicit_context.py','--business-id',BID,'--facts-file',FACTS_PATH,'--source-text',SOURCE,'--residual-request','determine what we should do next')
        payload=json.loads(boot.stdout)
        require(len(payload['objects_written'])==7,f'exact Northstar bootstrap should write 7 objects, got {payload}')
        require(payload.get('completion_state')=='initialization_complete_residual_routed',f'bootstrap should deterministically route declared residual intent, got {payload}')
        require(payload.get('residual_route',{}).get('contract_id')=='core.opportunity.discover-next-best-work',f'bootstrap residual route should select next-best-work, got {payload}')
        require(payload.get('residual_route',{}).get('broad_growth_precheck',{}).get('status')=='baseline_required',f'bootstrap residual route should carry fresh-business baseline gate, got {payload}')
        require('department/tactic menu' in payload.get('required_next_action',''),'bootstrap should make residual continuation non-optional')

        errors,warnings,counts=validate_business(BID,True)
        require(not errors,f'grounded bootstrap should validate, got {errors}')
        require(sum(counts.values())==7,f'expected 7 canonical objects, got {counts}')
        require(counts.get('ProductService')==3,f'expected three services, got {counts}')

        services=sorted(json.loads(p.read_text())['name'] for p in (BASE/'context/products').glob('*.json'))
        require(services==['installation','maintenance','repair'],f'discrete services expected, got {services}')
        biz=json.loads((BASE/'context/business.json').read_text())
        require(biz['extensions']['lead_sources']==['organic search','Google Ads','referrals','repeat customers'],'lead sources should be discrete')
        require(biz['extensions']['businessos']['grounding_method']==GROUNDING_METHOD,'grounding marker missing')

        # Source grounding rejects unsupported expansion before persistence.
        try:
            build_objects(BID,markets=['Baltimore area schools hotels'],source_text=SOURCE)
            raise AssertionError('unsupported market expansion should be rejected')
        except ValueError:
            pass

        # Plausible classifications are not explicit-user truth merely because they fit the business.
        for inferred_model in ['contracting','service business']:
            try:
                build_objects(BID,business_models=[inferred_model],source_text=SOURCE)
                raise AssertionError(f'unsupported inferred business model should be rejected: {inferred_model}')
            except ValueError:
                pass

        # Active-business validation must detect a forged/expanded explicit-user fact even if JSON remains schema-valid.
        mp=next((BASE/'context/markets').glob('*.json')); original=mp.read_text(); obj=json.loads(original)
        obj['name']='Maryland'; obj['geography']='Maryland'; mp.write_text(json.dumps(obj,indent=2)+'\n')
        errors,_,_=validate_business(BID,True)
        require(any('not grounded' in e and 'Maryland' in e for e in errors),f'provenance validator should reject unsupported explicit-user geography, got {errors}')
        mp.write_text(original)
        errors,_,_=validate_business(BID,True); require(not errors,f'restored state should validate, got {errors}')

        # Explicit-user trust cannot be self-asserted without the supported grounding marker.
        pp=next((BASE/'context/products').glob('*.json')); original=pp.read_text(); obj=json.loads(original)
        obj['extensions']['businessos'].pop('grounding_method',None); pp.write_text(json.dumps(obj,indent=2)+'\n')
        errors,_,_=validate_business(BID,True)
        require(any('not trusted' in e for e in errors),f'missing grounding method should invalidate explicit-user trust, got {errors}')
        pp.write_text(original)

        # Explicit reusable promises are first-class BusinessClaim objects; assembled strategy may not self-assert explicit_user.
        srcp=next((BASE/'intelligence/sources').glob('src_*explicit*.json')); src=json.loads(srcp.read_text()); srcid=src['id']; ts=src['created_at']
        claim={
            'id':f'clm_{BID}_written-estimates','object_type':'BusinessClaim','schema_version':'1.0.0','business_id':BID,
            'created_at':ts,'updated_at':ts,'lineage':[srcid],'statement':'We provide written estimates.',
            'claim_kind':'approved_business_claim','status':'approved','authority':'explicit_user','source_ref':srcid,'support_quote':'We provide written estimates.',
            'extensions':{'businessos':{'fact_status':'known','authority':'explicit_user','source_ref':srcid,'grounding_method':GROUNDING_METHOD,'grounding_version':'1.0'}}
        }
        cp=BASE/'context/claims'/f"{claim['id']}.json";cp.parent.mkdir(parents=True,exist_ok=True);cp.write_text(json.dumps(claim,indent=2)+'\n')
        brand={
            'id':f'brd_{BID}','object_type':'Brand','schema_version':'1.0.0','business_id':BID,'created_at':ts,'updated_at':ts,'lineage':[srcid],
            'name':'Northstar HVAC','voice':{'tone':['honest']},
            'extensions':{'businessos':{'authority':'explicit_user','source_ref':srcid,'grounding_method':GROUNDING_METHOD,'grounding_version':'1.0'}}
        }
        bp=BASE/'context/brand'/f"{brand['id']}.json";bp.parent.mkdir(parents=True,exist_ok=True);bp.write_text(json.dumps(brand,indent=2)+'\n')
        errors,_,_=validate_business(BID,True)
        require(any('may not self-assert explicit_user authority' in e for e in errors),f'agent-assembled Brand must not masquerade as explicit user truth, got {errors}')
        brand['extensions']['businessos']={'authority':'candidate_strategy','basis_refs':[srcid,claim['id']],'fact_status':'candidate'};bp.write_text(json.dumps(brand,indent=2)+'\n')
        errors,_,_=validate_business(BID,True);require(not errors,f'derived/candidate Brand with basis refs should validate, got {errors}')

        # Customer-facing marketing claims require a complete manifest and cannot enlarge the supported promise.
        html=BASE/'assets/claim-regression.html';html.parent.mkdir(parents=True,exist_ok=True);html.write_text('<html><body><p>Northstar HVAC guarantees same-day written estimates.</p></body></html>')
        asset={
            'id':f'ast_{BID}_claim-regression','object_type':'Asset','schema_version':'1.0.0','business_id':BID,'created_at':ts,'updated_at':ts,
            'lineage':[claim['id']],'asset_type':'landing-page','owner_system':'marketing-synthesis','business_role':'claim regression','location_reference':str(html.relative_to(ROOT)),'version':'1.0.0','status':'draft',
            'extensions':{'businessos':{'customer_facing':True,'origin':'imported','claim_manifest':[{'text':'Northstar HVAC guarantees same-day written estimates.','classification':'approved_business_claim','support_refs':[claim['id']]}]}}
        }
        apath=BASE/'assets'/f"{asset['id']}.json"
        saved_manifest=asset['extensions']['businessos'].pop('claim_manifest');apath.write_text(json.dumps(asset,indent=2)+'\n')
        errors,_,_=validate_business(BID,True)
        require(any('requires extensions.businessos.claim_manifest' in e for e in errors),f'customer-facing production must not omit claim manifest, got {errors}')
        asset['extensions']['businessos']['claim_manifest']=saved_manifest;apath.write_text(json.dumps(asset,indent=2)+'\n')
        errors,_,_=validate_business(BID,True)
        require(any('enlarges supported promise' in e for e in errors),f'unsupported guarantee/timing expansion should fail, got {errors}')
        html.write_text('<html><body><p>We put both repair and replacement options in writing.</p></body></html>')
        asset['extensions']['businessos']['claim_manifest']=[{'text':'We put both repair and replacement options in writing.','classification':'approved_business_claim','support_refs':[claim['id']]}];apath.write_text(json.dumps(asset,indent=2)+'\n')
        errors,_,_=validate_business(BID,True)
        require(any('enlarges supported promise' in e and "'both'" in e for e in errors),f'authorized written estimates must not expand into both-options promise, got {errors}')
        html.write_text('<html><body><p>We provide written estimates.</p></body></html>')
        asset['extensions']['businessos']['claim_manifest']=[{'text':'We provide written estimates.','classification':'approved_business_claim','support_refs':[claim['id']]}];apath.write_text(json.dumps(asset,indent=2)+'\n')
        errors,_,_=validate_business(BID,True);require(not errors,f'supported customer-facing claim should validate, got {errors}')

        # A trusted but unrelated explicit object is not a permission token for a new capability/promise.
        biz=json.loads((BASE/'context/business.json').read_text())
        html.write_text("<html><body><p>We're glad to provide written estimates and walk through repair-versus-replace options with you any time.</p></body></html>")
        asset['extensions']['businessos']['claim_manifest']=[{'text':"We're glad to provide written estimates and walk through repair-versus-replace options with you any time.",'classification':'approved_business_claim','support_refs':[biz['id']]}];apath.write_text(json.dumps(asset,indent=2)+'\n')
        errors,_,_=validate_business(BID,True)
        require(any('do not substantively authorize' in e for e in errors),f'unrelated trusted business identity must not authorize a new customer-facing capability, got {errors}')

        # Even a substantively related claim cannot silently add availability/timing breadth.
        html.write_text('<html><body><p>We provide written estimates any time.</p></body></html>')
        asset['extensions']['businessos']['claim_manifest']=[{'text':'We provide written estimates any time.','classification':'approved_business_claim','support_refs':[claim['id']]}];apath.write_text(json.dumps(asset,indent=2)+'\n')
        errors,_,_=validate_business(BID,True)
        require(any('enlarges supported promise' in e and 'any time' in e for e in errors),f'unsupported any-time availability expansion should fail, got {errors}')

        html.write_text('<html><body><p>We provide written estimates.</p></body></html>')
        asset['extensions']['businessos']['claim_manifest']=[{'text':'We provide written estimates.','classification':'approved_business_claim','support_refs':[claim['id']]}];apath.write_text(json.dumps(asset,indent=2)+'\n')

        # A strategy/helper Run cannot masquerade as the production provenance for a finished customer-facing Asset.
        asset['owner_system']='content-synthesis';apath.write_text(json.dumps(asset,indent=2)+'\n')
        sr=run(SCRIPTS/'create_run.py',BID,'content.strategy.format-platform','strategy-root must not prove production'); srid=sr.stdout.strip(); srdir=ROOT/'runtime/runs'/BID/srid
        # The strategy contract declares an Asset write, so use the canonical Asset object as
        # its structural completion evidence rather than unrelated loose prose.
        run(SCRIPTS/'complete_run.py',BID,srid,'--evidence',str(apath.relative_to(ROOT)))
        asset=json.loads(apath.read_text());asset['extensions']['businessos'].pop('origin',None);asset['extensions']['businessos']['run_ref']=srdir.relative_to(ROOT).as_posix();asset['extensions']['businessos']['contract_chain']=['content.strategy.format-platform'];apath.write_text(json.dumps(asset,indent=2)+'\n')
        errors,_,_=validate_business(BID,True)
        require(any('customer-facing Asset must reference a Run whose root contract is marked' in e for e in errors),f'strategy-only root contract must not validate as customer-facing production, got {errors}')
        shutil.rmtree(srdir)

        # A legitimate customer-facing production root must now reject unrelated root evidence before completion.
        asset['owner_system']='marketing-synthesis';apath.write_text(json.dumps(asset,indent=2)+'\n')
        def subcontract_evidence(run_dir,run_id,cid):
            if '.qa' in cid or cid.endswith('.qa'):
                q=run_dir/'artifacts'/f'{cid.replace(".","-")}-qa.json';q.parent.mkdir(parents=True,exist_ok=True)
                q.write_text(json.dumps({
                    'contract_id':cid,'status':'pass',
                    'checks':[{'check':'regression evidence linkage','status':'pass','result':'The named fixture Asset and exact version were inspected.'}],
                    'tested_asset':asset['id'],'tested_version':asset.get('version'),'blockers':[]
                },indent=2));return str(q.relative_to(ROOT))
            e=run_dir/'artifacts'/f'{cid.replace(".","-")}-evidence.json';e.parent.mkdir(parents=True,exist_ok=True)
            sub_asset={
                **asset,'id':f'ast_{BID}_{cid.replace(".","-")}_{run_id}','name':f'Regression evidence for {cid}',
                'description':f'Contract-specific regression evidence for {cid}','location_reference':str(html.relative_to(ROOT)),
                'extensions':{'businessos':{'customer_facing':False,'run_ref':run_dir.relative_to(ROOT).as_posix(),'run_id':run_id,'run_contract_id':cid,'contract_chain':[cid]}}
            }
            e.write_text(json.dumps(sub_asset,indent=2)+'\n');return str(e.relative_to(ROOT))
        qr=run(SCRIPTS/'create_run.py',BID,'marketing.assets.quiz-assessment','root evidence must include deliverable'); qrid=qr.stdout.strip(); qrdir=ROOT/'runtime/runs'/BID/qrid
        qmanifest=json.loads((qrdir/'contract-execution.json').read_text())
        qevidence=str(html.relative_to(ROOT))
        for cid in qmanifest.get('required_subcontracts',[]):
            ev=subcontract_evidence(qrdir,qrid,cid)
            run(SCRIPTS/'record_contract_completion.py',BID,qrid,cid,'--evidence',ev)
        asset['extensions']['businessos']['run_ref']=qrdir.relative_to(ROOT).as_posix();asset['extensions']['businessos']['contract_chain']=['marketing.assets.quiz-assessment']+qmanifest.get('required_subcontracts',[]);apath.write_text(json.dumps(asset,indent=2)+'\n')
        bad=run(SCRIPTS/'complete_run.py',BID,qrid,'--evidence',str((BASE/'context/business.json').relative_to(ROOT)),check=False)
        require(bad.returncode!=0 and 'Asset file must be supplied as root --evidence' in (bad.stderr+bad.stdout),f'production Run must reject unrelated root evidence before completion, got {bad.stderr+bad.stdout}')
        shutil.rmtree(qrdir)

        # Required subcontract/QA completion must be auditable for production Assets that reference a Run.
        rr=run(SCRIPTS/'create_run.py',BID,'marketing.assets.landing-page','claim/run completion regression'); rid=rr.stdout.strip(); rdir=ROOT/'runtime/runs'/BID/rid
        asset['extensions']['businessos'].pop('origin',None);asset['extensions']['businessos']['run_ref']=rdir.relative_to(ROOT).as_posix();asset['extensions']['businessos']['contract_chain']=['marketing.assets.landing-page'];apath.write_text(json.dumps(asset,indent=2)+'\n')
        errors,_,_=validate_business(BID,True)
        require(any('required subcontract not completed' in e for e in errors),f'production Asset must not pass with implied subcontracts, got {errors}')
        manifest=json.loads((rdir/'contract-execution.json').read_text());evidence=str(html.relative_to(ROOT))
        for cid in manifest['required_subcontracts']:
            ev=subcontract_evidence(rdir,rid,cid)
            run(SCRIPTS/'record_contract_completion.py',BID,rid,cid,'--evidence',ev)
        asset['extensions']['businessos']['contract_chain']=['marketing.assets.landing-page']+manifest['required_subcontracts'];apath.write_text(json.dumps(asset,indent=2)+'\n')
        run(SCRIPTS/'complete_run.py',BID,rid,'--evidence',evidence)
        errors,_,_=validate_business(BID,True);require(not errors,f'fully evidenced required-contract Run should validate, got {errors}')
        shutil.rmtree(rdir)
        apath.unlink(missing_ok=True);html.unlink(missing_ok=True);bp.unlink(missing_ok=True);cp.unlink(missing_ok=True)
        errors,_,_=validate_business(BID,True);require(not errors,f'cleanup should restore baseline validation, got {errors}')

        result=route('determine what we should do next')
        cid=result[0].get('contract_id') if isinstance(result,list) and result else None
        require(cid=='core.opportunity.discover-next-best-work',f'next-best-work routing expected, got {result}')
        rr=route_and_resolve('determine what we should do next',BID)
        require(rr.get('broad_growth_precheck',{}).get('status')=='baseline_required',f'fresh business should trigger baseline gate, got {rr}')

        plan=build_plan(BID,'core.opportunity.discover-next-best-work')
        require('core/policies/resource-aware-execution.md' in plan['files'],'resource-aware policy missing from next-best-work context plan')
        require('core/policies/active-business-truth.md' in plan['files'],'active-business truth policy missing from context plan')
        require('core/policies/operating-scope.md' in plan['files'],'operating-scope policy missing from context plan')

        truth=(ROOT/'core/policies/active-business-truth.md').read_text(encoding='utf-8')
        require('Unknown is not absent' in truth,'unknown-vs-absent rule missing')
        require('determine what to do next' in truth,'recommendation-vs-execution scope rule missing')
        agent=(ROOT/'core/policies/agent-execution.md').read_text(encoding='utf-8')
        require('clarification timeout' in agent,'clarification-timeout rule missing')
        require('BusinessOS system-integrity boundary' in agent,'system-integrity execution rule missing')
        require('Supplementary-artifact restraint' in agent,'supplementary-artifact restraint missing')
        require('--residual-request' in agent and 'required handoff' in agent,'post-bootstrap residual routing rule missing')

        scope=(ROOT/'core/policies/operating-scope.md').read_text(encoding='utf-8')
        require('protected infrastructure' in scope and 'scripts/' in scope and 'failed deterministic helper is not permission to bypass it' in scope,'operating-scope protection incomplete')
        require('Do not expose technical "modes"' in scope,'nontechnical-user scope inference rule missing')

        resource=(ROOT/'core/policies/resource-aware-execution.md').read_text(encoding='utf-8')
        require('user-effort duration' in resource and 'specific number of minutes/hours' in resource,'unsupported user-time estimate rule missing')
        require('Contextual questions are encouraged' in resource and 'decision-critical unknown' in resource,'contextual diagnostic question rule missing')

        nb=(ROOT/'core/contracts/opportunity/discover-next-best-work/CONTEXT.md').read_text(encoding='utf-8')
        require('growth_baseline_gate.py' in nb and 'hard first-pass gate' in nb,'deterministic profitable-growth baseline gate missing')
        require('one bounded discovery loop' in nb,'bounded discovery-loop rule missing')
        require('Do **not** implement' in nb,'next-best-work execution boundary missing')

        claim_policy=(ROOT/'core/policies/context-provenance-and-claims.md').read_text(encoding='utf-8')
        require('BusinessClaim' in claim_policy and 'claim_manifest' in claim_policy,'context provenance/claim policy missing core controls')
        mplan=build_plan(BID,'marketing.assets.landing-page')
        require('core/policies/context-provenance-and-claims.md' in mplan['files'],'marketing production context must load claim/provenance policy')
        require(any(x.get('type')=='BusinessClaim' for x in mplan.get('unresolved_selectors',[]) if isinstance(x,dict)),'marketing context plan should request reusable BusinessClaim context when none exists')
        agent=(ROOT/'core/policies/agent-execution.md').read_text(encoding='utf-8')
        require('Required-contract completion evidence' in agent and 'build_claim_manifest.py' in agent,'agent execution must enforce auditable production/claim controls')
        require((ROOT/'core/policies/completion-evidence.md').exists(),'contract-aware completion evidence policy missing')
        reg=json.loads((ROOT/'generated/contract-registry.json').read_text()); byid={c['id']:c for c in reg['contracts']}
        require(byid['content.production.article'].get('artifact_role')=='customer_facing_production_root','content production root role metadata missing')
        require(byid['marketing.assets.quiz-assessment'].get('artifact_role')=='customer_facing_production_root','marketing asset production root role metadata missing')
        require(byid['content.strategy.format-platform'].get('artifact_role') is None,'strategy contract must not be marked as a customer-facing production root')

        research_policy=(ROOT/'core/policies/research-evidence.md').read_text(encoding='utf-8')
        require('Search results are discovery, not evidence' in research_policy,'research evidence discovery-vs-support rule missing')
        require('persist_research_bundle.py' in research_policy,'research persistence helper missing from policy')
        require('Acquisition method vs. capture method' in research_policy,'research acquisition-vs-capture boundary missing')
        require('Business promise/change' in research_policy,'opportunity-vs-promise research boundary missing')

        cplan=build_plan(BID,'competitor.analysis.customer-sentiment')
        require('core/policies/research-evidence.md' in cplan['files'],'research-writing contracts must load research-evidence policy')
        cctx=(ROOT/'systems/competitor-intelligence/contracts/analysis/customer-sentiment/CONTEXT.md').read_text(encoding='utf-8')
        require('persist_research_bundle.py' in cctx and 'Search snippets' in cctx,'competitor sentiment should use shared evidence-preserving persistence path')

        # Discovery-only public sources may be indexed, but cannot support Observations -- even if text was copied from search results.
        bad_bundle=ROOT/'runtime'/f'{BID}-bad-research.json'
        bad_bundle.write_text(json.dumps({
            'contract_id':'competitor.analysis.customer-sentiment',
            'sources':[{'source_type':'review_platform','source_reference':'https://example.test/review','acquisition_method':'search_result','captured_text':'Search snippet says a reviewer complained about billing.'}],
            'observations':[{'statement':'A reviewer complained about billing.','source_indexes':[0]}]
        }))
        bad=run(SCRIPTS/'persist_research_bundle.py',BID,'--bundle-file',bad_bundle,check=False)
        require(bad.returncode!=0 and 'search/snippet discovery is not support' in bad.stderr,'search-result text must not masquerade as directly acquired evidence')
        bad_bundle.unlink(missing_ok=True)

        # Missing acquisition provenance is also insufficient for new material public evidence.
        no_acq_bundle=ROOT/'runtime'/f'{BID}-no-acquisition-research.json'
        no_acq_bundle.write_text(json.dumps({
            'contract_id':'competitor.analysis.customer-sentiment',
            'sources':[{'source_type':'review_platform','source_reference':'https://example.test/review/missing','captured_text':'A copied review excerpt.'}],
            'observations':[{'statement':'Reviewer described a billing issue.','source_indexes':[0]}]
        }))
        no_acq=run(SCRIPTS/'persist_research_bundle.py',BID,'--bundle-file',no_acq_bundle,check=False)
        require(no_acq.returncode!=0 and "acquired as 'unknown'" in no_acq.stderr,'captured text without acquisition provenance must not support an Observation')
        no_acq_bundle.unlink(missing_ok=True)

        # Broad superlative/frequency claims must be sample-scoped unless measured population evidence exists.
        broad_bundle=ROOT/'runtime'/f'{BID}-broad-frequency-research.json'
        broad_bundle.write_text(json.dumps({
            'contract_id':'competitor.analysis.customer-sentiment',
            'sources':[{'source_type':'review_platform','source_reference':'https://example.test/review/broad','acquisition_method':'direct_page_read','captured_text':'The technician explained the repair clearly and did not pressure me.'}],
            'observations':[{'statement':'Reviewer praised clear explanation and lack of sales pressure.','source_indexes':[0]}],
            'insights':[{'statement':'Clear explanation is the top driver of customer satisfaction.','observation_indexes':[0],'status':'supported'}]
        }))
        broad=run(SCRIPTS/'persist_research_bundle.py',BID,'--bundle-file',broad_bundle,check=False)
        require(broad.returncode!=0 and 'sample scope or measured frequency_basis' in broad.stderr,'unsupported market-wide superlative should be rejected')
        broad_bundle.unlink(missing_ok=True)

        good_bundle=ROOT/'runtime'/f'{BID}-good-research.json'
        good_bundle.write_text(json.dumps({
            'contract_id':'competitor.analysis.customer-sentiment',
            'sources':[{'source_type':'review_platform','source_reference':'https://example.test/review/1','acquisition_method':'direct_page_read','captured_text':'The technician explained the repair clearly and did not pressure me.','rating':5}],
            'observations':[{'statement':'Reviewer praised clear explanation and lack of sales pressure.','source_indexes':[0],'observation_type':'customer_praise'}],
            'insights':[{'statement':'Clear explanation and low-pressure service are positive signals in the sampled evidence.','observation_indexes':[0],'status':'supported','confidence':0.7}]
        }))
        good=run(SCRIPTS/'persist_research_bundle.py',BID,'--bundle-file',good_bundle)
        gp=json.loads(good.stdout); require(len(gp.get('objects_written',[]))==3,f'research helper should write source+observation+insight, got {gp}')
        re_errs,re_warn=evidence_errors(BID); require(not re_errs,f'captured research evidence should validate, got {re_errs}')
        errors,_,_=validate_business(BID,True); require(not errors,f'business validation should include and pass research evidence semantics, got {errors}')
        good_bundle.unlink(missing_ok=True)
        approval=(ROOT/'core/policies/approval.md').read_text(encoding='utf-8')
        require('Silence is not approval' in approval,'silence-not-approval rule missing')
        print('agent hardening regressions passed')
    finally:
        FACTS_PATH.unlink(missing_ok=True)
        if BASE.exists(): shutil.rmtree(BASE)
        rbase=ROOT/'runtime/runs'/BID
        if rbase.exists(): shutil.rmtree(rbase)

if __name__=='__main__': main()
