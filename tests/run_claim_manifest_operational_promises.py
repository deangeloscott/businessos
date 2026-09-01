#!/usr/bin/env python3
"""Claim governance catches unsupported promises in text-native and opaque rendered media."""
from pathlib import Path
import json, shutil, sys
ROOT=Path(__file__).resolve().parents[1]; S=ROOT/'scripts'; sys.path.insert(0,str(S))
from build_claim_manifest import scan_claims
from validate_business_claims import validate_manifest_sentences, claim_errors
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
        p.write_text("""CrewBeacon brings supported connected lead sources together so nothing lives only in someone's inbox.
A 30-minute walkthrough with our team, focused on how your office would prioritize leads.
No setup required to see the demo.
""")
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

        # Text-bearing visual media enters the normal claim-governance path without OCR.
        svg=BASE/'assets/visual.svg'
        svg.write_text('''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="400">
  <title>CrewBeacon operating flow</title>
  <text x="20" y="60">CrewBeacon automatically reallocates every lead in real time.</text>
  <text x="20" y="110">Illustrative workflow: manager reviews the handoff before launch.</text>
</svg>\n''')
        svg_cands=scan_claims(BID,svg)
        req(any('automatically reallocates every lead' in x for x in svg_cands),'SVG product behavior must be extracted from audience-readable text')
        req(any('Illustrative workflow' in x for x in svg_cands),'SVG scan must cover visible guidance text, not raw XML markup')
        asset={
            'id':'ast_svg_claim_fixture','object_type':'Asset','business_id':BID,'owner_system':'content-synthesis',
            'location_reference':str(svg.relative_to(ROOT)),
            'extensions':{'businessos':{'customer_facing':True,'claim_manifest':[]}}
        }
        svg_errors=claim_errors(BID,[(asset,BASE/'assets/ast_svg_claim_fixture.json')])
        req(any('automatically reallocates every lead' in e for e in svg_errors),'customer-facing SVG cannot silently bypass claim manifest coverage')
        branded='CrewBeacon automatically reallocates every lead in real time.'
        branded_manifest=[{'text':x,'classification':('approved_business_claim' if x==branded else 'general_guidance'),'support_refs':(['clm_one-view'] if x==branded else [])} for x in svg_cands]
        svg_support_errors=validate_manifest_sentences(branded_manifest,svg_cands,idx,'CrewBeacon','asset.json')
        req(any('automatically reallocates every lead' in e for e in svg_support_errors),'generic trusted positioning must not authorize invented SVG product behavior')

        # Opaque media uses one format-independent claim-surface interface rather than an
        # extension-specific OCR/parser rule. PNG is representative of the opaque path; the
        # same sidecar contract applies to other raster, PDF/presentation, audio, and video media.
        # Claim governance must apply to a newly managed outward Asset even when no Run exists.
        png=BASE/'assets/visual.png';png.write_bytes(b'\x89PNG\r\n\x1a\nopaque-fixture')
        opaque_asset={
            'id':'ast_opaque_claim_fixture','object_type':'Asset','business_id':BID,'owner_system':'content-synthesis',
            'location_reference':str(png.relative_to(ROOT)),
            'extensions':{'businessos':{'customer_facing':True,'claim_manifest':[]}}
        }
        missing_surface=claim_errors(BID,[(opaque_asset,BASE/'assets/ast_opaque_claim_fixture.json')])
        req(any('claim_surface_ref' in e for e in missing_surface),'new opaque customer-facing media must expose an auditable claim surface without requiring a Run')
        sidecar=BASE/'assets/visual.claim-surface.json'
        sidecar.write_text(json.dumps({
            'format_version':'1.0','artifact_ref':str(png.relative_to(ROOT)),
            'visible_text':['CrewBeacon guarantees every lead is automatically routed in real time.'],
            'spoken_text':[],
            'material_visual_claims':['The graphic depicts an automated lead-routing workflow as product behavior.']
        })+'\n')
        opaque_asset['extensions']['businessos']['claim_surface_ref']=str(sidecar.relative_to(ROOT))
        opaque_errors=claim_errors(BID,[(opaque_asset,BASE/'assets/ast_opaque_claim_fixture.json')])
        req(any('guarantees every lead' in e for e in opaque_errors),'opaque claim surface must feed the same manifest coverage')

        print('claim operational-promise regressions passed without Run coupling')
    finally:
        if BASE.exists(): shutil.rmtree(BASE)
if __name__=='__main__': main()
