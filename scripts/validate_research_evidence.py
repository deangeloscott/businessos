#!/usr/bin/env python3
from _common import *
import argparse, json, hashlib

PUBLIC_NARRATIVE_TYPES={
    'review_platform','forum','social_platform','complaint_board','community','public_comment',
    'social_post','review','discussion','webpage','article','consumer_reports','industry_guide'
}

# acquisition_method records how the evidence was actually obtained. capture_method records
# what was preserved. Search/snippet discovery can be stored, but cannot support material claims.
DIRECT_ACQUISITION_METHODS={
    'direct_page_read','browser_read','browser_capture','api_response','downloaded_document',
    'uploaded_document','user_provided','first_party_export','authoritative_record'
}
DISCOVERY_ONLY_METHODS={
    'search_result','search_snippet','directory_preview','ai_summary','unvisited_url','unknown'
}
KNOWN_ACQUISITION_METHODS=DIRECT_ACQUISITION_METHODS|DISCOVERY_ONLY_METHODS
AUTHORITATIVE_POINTER_METHODS={'api_response','first_party_export','authoritative_record'}


def _evidence_ext(src):
    ext=src.get('extensions') if isinstance(src.get('extensions'),dict) else {}
    ev=ext.get('businessos_evidence') if isinstance(ext.get('businessos_evidence'),dict) else {}
    return ev


def _capture_quality(src):
    ev=_evidence_ext(src)
    status=ev.get('capture_status')
    acquisition=ev.get('acquisition_method') or 'unknown'
    captured_text=ev.get('captured_text')
    assets=ev.get('asset_refs') if isinstance(ev.get('asset_refs'),list) else []
    pointer=ev.get('evidence_pointer')
    payload=ev.get('record_payload')

    if acquisition not in KNOWN_ACQUISITION_METHODS:
        return False,f'{status or "missing"}/unrecognized_acquisition:{acquisition}'
    if acquisition in DISCOVERY_ONLY_METHODS:
        return False,f'{status or "missing"}/{acquisition}'
    if status=='captured' and acquisition in DIRECT_ACQUISITION_METHODS and (captured_text or assets or payload is not None):
        return True,f'captured/{acquisition}'
    if status=='external_pointer' and pointer and acquisition in AUTHORITATIVE_POINTER_METHODS:
        return True,f'external_pointer/{acquisition}'
    return False,f'{status or "missing"}/{acquisition}'


def evidence_errors(business_id):
    idx=object_index(business_id); errors=[]; warnings=[]
    sources={k:v[0] for k,v in idx.items() if v[0].get('object_type')=='SourceRecord'}
    observations={k:v[0] for k,v in idx.items() if v[0].get('object_type')=='Observation'}
    insights={k:v[0] for k,v in idx.items() if v[0].get('object_type')=='Insight'}

    for oid,obs in observations.items():
        refs=obs.get('source_refs') or []
        if not refs:
            errors.append(f'{oid} Observation has no source_refs')
            continue
        for ref in refs:
            src=sources.get(ref)
            if not src: continue  # reference validator reports missing refs
            public=src.get('access_scope')=='public' or src.get('source_type') in PUBLIC_NARRATIVE_TYPES or src.get('origin')=='public web'
            if not public: continue
            ok,mode=_capture_quality(src)
            if not ok:
                errors.append(f'{oid} relies on public source {ref} without directly acquired/reproducible evidence (evidence={mode}); search/snippet discovery or model-written text is not sufficient support')
            ev=_evidence_ext(src)
            txt=ev.get('captured_text')
            if txt and src.get('content_hash'):
                expected='sha256:'+hashlib.sha256(txt.encode('utf-8')).hexdigest()
                if src.get('content_hash')!=expected:
                    errors.append(f'{ref} content_hash does not match captured_text')

    for iid,ins in insights.items():
        if ins.get('status') not in {'supported','active'}: continue
        links=[x for x in (ins.get('evidence_links') or []) if isinstance(x,dict) and x.get('relationship') in {'supports','derived_from'}]
        if not links:
            errors.append(f'{iid} status={ins.get("status")} requires at least one supporting evidence link')
            continue
        supporting_obs=[]
        for link in links:
            ref=link.get('ref')
            if ref in observations: supporting_obs.append(ref)
            elif ref in sources:
                ok,mode=_capture_quality(sources[ref])
                if not ok: errors.append(f'{iid} directly relies on source {ref} without directly acquired/reproducible evidence (evidence={mode})')
            elif ref in insights:
                warnings.append(f'{iid} is supported by another Insight {ref}; ensure the upstream support chain remains valid')
        if not supporting_obs and not any(link.get('ref') in sources for link in links):
            errors.append(f'{iid} status={ins.get("status")} has no supporting Observation or SourceRecord link')

    return errors,warnings


def main():
    p=argparse.ArgumentParser(description='Validate semantic evidence support for researched SourceRecords, Observations, and supported/active Insights.')
    p.add_argument('business_id'); a=p.parse_args()
    errors,warnings=evidence_errors(a.business_id)
    print(f'business={a.business_id} research_evidence_errors={len(errors)} warnings={len(warnings)}')
    for w in warnings: print('WARNING',w)
    for e in errors: print('ERROR',e)
    if errors: raise SystemExit(1)
    print('research evidence validation passed')

if __name__=='__main__': main()
