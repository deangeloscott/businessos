#!/usr/bin/env python3
"""RC15: scanner/validator catch invented timing, setup and absolute operational promises."""
from pathlib import Path
import json, shutil, sys
ROOT=Path(__file__).resolve().parents[1]; S=ROOT/'scripts'; sys.path.insert(0,str(S))
from build_claim_manifest import scan_claims
from validate_business_claims import validate_manifest_sentences
BID='claim-operational-promises'; BASE=ROOT/'instances'/BID

def req(c,m):
    if not c: raise AssertionError(m)

def claim(cid,text):
    return {'id':cid,'object_type':'BusinessClaim','schema_version':'1.0.0','business_id':BID,'created_at':'2026-08-25T00:00:00+00:00','updated_at':'2026-08-25T00:00:00+00:00','lineage':[],'statement':text,'claim_kind':'approved_business_claim','authority':'explicit_user','status':'approved'}

def main():
    if BASE.exists(): shutil.rmtree(BASE)
    try:
        (BASE/'context').mkdir(parents=True,exist_ok=True)
        (BASE/'context/business.json').write_text(json.dumps({'id':'biz_claim-operational-promises','object_type':'Business','schema_version':'1.0.0','business_id':BID,'created_at':'2026-08-25T00:00:00+00:00','updated_at':'2026-08-25T00:00:00+00:00','lineage':[],'name':'CrewBeacon'})+'\n')
        p=BASE/'assets/draft.md';p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text("""CrewBeacon brings supported connected lead sources together so nothing lives only in someone's inbox.\nA 30-minute walkthrough with our team, focused on how your office would prioritize leads.\nNo setup required to see the demo.\n""")
        cands=scan_claims(BID,p)
        req(any('30-minute walkthrough' in x for x in cands),'timing promise must be scanned')
        req(any('No setup required' in x for x in cands),'setup promise must be scanned')
        req(any('nothing lives only' in x for x in cands),'absolute benefit must be scanned')
        supports=[claim('clm_one-view','CrewBeacon can collect leads from supported connected lead sources into one operating view')]
        idx={o['id']:(o,Path('x')) for o in supports}
        manifest=[{'text':x,'classification':'approved_business_claim','support_refs':['clm_one-view']} for x in cands]
        errs=validate_manifest_sentences(manifest,cands,idx,'CrewBeacon','asset.json')
        req(any('30-minute walkthrough' in e for e in errs),'unsupported duration must fail')
        req(any('No setup required' in e for e in errs),'unsupported setup promise must fail')
        req(any('nothing lives only' in e for e in errs),'unsupported absolute benefit must fail')
        general=[{'text':x,'classification':'general_guidance','support_refs':[]} for x in cands]
        errs2=validate_manifest_sentences(general,cands,idx,'CrewBeacon','asset.json')
        req(all(any(x in e and 'general_guidance' in e for e in errs2) for x in cands),'scanner candidates must not escape as general guidance')
        minted=claim('clm_minted','CrewBeacon guarantees every lead receives a response')
        minted['authority']='verified_first_party';minted['lineage']=['src_fixture']
        sentence='CrewBeacon guarantees every lead receives a response.'
        errs3=validate_manifest_sentences([{'text':sentence,'classification':'approved_business_claim','support_refs':['clm_minted']}],[sentence],{'clm_minted':(minted,Path('minted.json'))},'CrewBeacon','asset.json')
        req(any('missing/untrusted support refs' in e for e in errs3),'self-stamped verified_first_party claim without source_ref/support_quote must not authorize customer-facing copy')
        print('claim operational-promise regressions passed')
    finally:
        if BASE.exists(): shutil.rmtree(BASE)
if __name__=='__main__': main()
