#!/usr/bin/env python3
"""Claim-manifest regressions preserve provenance without deterministic language semantics."""
from pathlib import Path
import json,shutil,sys
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'scripts';sys.path.insert(0,str(S))
from build_claim_manifest import scan_claims
from validate_business_claims import validate_manifest_entries,claim_errors
BID='claim-operational-promises';BASE=ROOT/'instances'/BID

def req(c,m):
    if not c:raise AssertionError(m)

def main():
    if BASE.exists():shutil.rmtree(BASE)
    try:
        (BASE/'context').mkdir(parents=True,exist_ok=True)
        (BASE/'context/business.json').write_text(json.dumps({'id':'biz_claim-operational-promises','object_type':'Business','schema_version':'1.0.0','business_id':BID,'created_at':'2026-08-25T00:00:00+00:00','updated_at':'2026-08-25T00:00:00+00:00','lineage':[],'name':'CrewBeacon'})+'\n')
        p=BASE/'assets/draft.md';p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text("""CrewBeacon brings supported connected lead sources together.
A 30-minute walkthrough with our team.
No setup required to see the demo.
""")

        # Candidate scanning remains an optional review aid; its output is not semantic authority.
        cands=scan_claims(BID,p)
        req(cands,'review helper should surface at least some candidate text')

        asset={'id':'ast_claim_fixture','object_type':'Asset','business_id':BID,'location_reference':str(p.relative_to(ROOT)),'extensions':{'businessos':{'customer_facing':True}}}
        req(not claim_errors(BID,[(asset,BASE/'assets/ast_claim_fixture.json')]),'customer-facing Asset must not require a claim manifest')

        idx={}
        errs=validate_manifest_entries([{'text':'Anything','classification':'approved_business_claim','support_refs':[]}],idx,'asset.json')
        req(any('requires support_refs' in e for e in errs),'approved manifest entry without provenance must fail')

        errs=validate_manifest_entries([{'text':'Anything','classification':'approved_business_claim','support_refs':['clm_missing']}],idx,'asset.json')
        req(any('missing/untrusted support refs' in e for e in errs),'missing support ref must fail')

        claim={
            'id':'clm_supported','object_type':'BusinessClaim','schema_version':'1.0.0','business_id':BID,
            'created_at':'2026-08-25T00:00:00+00:00','updated_at':'2026-08-25T00:00:00+00:00','lineage':['src_fixture'],
            'statement':'CrewBeacon provides written estimates.','claim_kind':'approved_business_claim','authority':'verified_first_party','status':'approved',
            'source_ref':'src_fixture','support_quote':'CrewBeacon provides written estimates.'
        }
        idx={'clm_supported':(claim,Path('claim.json'))}
        manifest=[{'text':'CrewBeacon provides written estimates.','classification':'approved_business_claim','support_refs':['clm_supported']}]
        req(not validate_manifest_entries(manifest,idx,'asset.json'),'trusted support refs should pass structural claim validation')

        # Semantic equivalence is intentionally not decided by deterministic validation.
        semantically_questionable=[{'text':'CrewBeacon guarantees every lead closes tomorrow.','classification':'approved_business_claim','support_refs':['clm_supported']}]
        req(not validate_manifest_entries(semantically_questionable,idx,'asset.json'),'deterministic validator must not police natural-language semantic equivalence')

        invalid=[{'text':'Anything','classification':'model_says_true','support_refs':['clm_supported']}]
        req(any('invalid classification' in e for e in validate_manifest_entries(invalid,idx,'asset.json')),'manifest vocabulary remains structurally bounded when used')

        asset['extensions']['businessos']['claim_manifest']=manifest
        req(not claim_errors(BID,[(asset,BASE/'assets/ast_claim_fixture.json')]),'optional structurally grounded manifest should pass')

        # Claim validation applies to the organization-owned Asset itself, independent of
        # whichever AURA operating-knowledge area or external method may have informed it.
        other=dict(asset);other['id']='ast_other_method';other['extensions']={'businessos':{'claim_manifest':[{'text':'Anything','classification':'approved_business_claim','support_refs':[]}]}}
        errs=claim_errors(BID,[(other,BASE/'assets/ast_other_method.json')])
        req(any('requires support_refs' in e for e in errs),'claim validation was incorrectly gated by AURA method/module context')

        print('claim provenance regressions passed with model-owned semantics and method-independent structural validation')
    finally:
        if BASE.exists():shutil.rmtree(BASE)
if __name__=='__main__':main()
