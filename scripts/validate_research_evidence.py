#!/usr/bin/env python3
from _common import *
from urllib.parse import urlparse
import argparse, json, hashlib

PUBLIC_NARRATIVE_TYPES={
    'review_platform','forum','social_platform','complaint_board','community','public_comment',
    'social_post','review','discussion','webpage','article','consumer_reports','industry_guide'
}

# acquisition_method records how the evidence was actually obtained. capture_method records
# what was preserved. Search/snippet discovery can be stored, but cannot support material claims.
DIRECT_ACQUISITION_METHODS={
    'direct_page_read','browser_read','browser_capture','api_response','downloaded_document',
    'uploaded_document','user_provided','first_party_export','authoritative_record',
    'image_inspection','audio_inspection','video_inspection','transcript_read','document_visual_inspection'
}
DISCOVERY_ONLY_METHODS={
    'search_result','search_snippet','directory_preview','ai_summary','unvisited_url','unknown'
}
KNOWN_ACQUISITION_METHODS=DIRECT_ACQUISITION_METHODS|DISCOVERY_ONLY_METHODS
AUTHORITATIVE_POINTER_METHODS={'api_response','first_party_export','authoritative_record'}
RESERVED_PUBLIC_HOSTS={'localhost','example.com','example.org','example.net'}


def _evidence_ext(src):
    ext=src.get('extensions') if isinstance(src.get('extensions'),dict) else {}
    ev=ext.get('businessos_evidence') if isinstance(ext.get('businessos_evidence'),dict) else {}
    return ev


def is_public_source(src):
    """Use declared provenance, not a narrative-looking type, for public-web safeguards."""
    return src.get('access_scope')=='public' or src.get('origin')=='public web'


def _subject_refs(obj):
    values=obj.get('subject_refs') if isinstance(obj,dict) else []
    if not isinstance(values,list): return set()
    return {str(x).strip() for x in values if isinstance(x,str) and x.strip()}


def _subject_mismatch(left,left_label,right,right_label):
    a=_subject_refs(left); b=_subject_refs(right)
    if not a or not b or a & b: return None
    return f'{left_label} subject_refs ({", ".join(sorted(a))}) do not overlap {right_label} subject_refs ({", ".join(sorted(b))}); evidence about one resolved subject cannot silently support another'


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


def public_source_locator_error(src):
    public=is_public_source(src)
    ref=str(src.get('source_reference') or '').strip()
    if not public or not ref.lower().startswith(('http://','https://')):return None
    host=(urlparse(ref).hostname or '').lower().rstrip('.')
    if not host or host in RESERVED_PUBLIC_HOSTS or host.endswith(('.invalid','.test','.localhost','.example')):
        return f'{src.get("id") or "public SourceRecord"} uses reserved/placeholder public source_reference {ref!r}; placeholder URLs cannot support current public evidence'
    return None


def evidence_errors(business_id):
    idx=object_index(business_id); errors=[]; warnings=[]
    sources={k:v[0] for k,v in idx.items() if v[0].get('object_type')=='SourceRecord'}
    observations={k:v[0] for k,v in idx.items() if v[0].get('object_type')=='Observation'}
    insights={k:v[0] for k,v in idx.items() if v[0].get('object_type')=='Insight'}

    for src in sources.values():
        locator_error=public_source_locator_error(src)
        if locator_error:errors.append(locator_error)

    for oid,obs in observations.items():
        refs=obs.get('source_refs') or []
        if not refs:
            errors.append(f'{oid} Observation has no source_refs')
            continue
        for ref in refs:
            src=sources.get(ref)
            if not src: continue  # reference validator reports missing refs
            mismatch=_subject_mismatch(obs,oid,src,ref)
            if mismatch: errors.append(mismatch)
            public=is_public_source(src)
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
            if ref in observations:
                supporting_obs.append(ref)
                mismatch=_subject_mismatch(ins,iid,observations[ref],ref)
                if mismatch: errors.append(mismatch)
            elif ref in sources:
                mismatch=_subject_mismatch(ins,iid,sources[ref],ref)
                if mismatch: errors.append(mismatch)
                ok,mode=_capture_quality(sources[ref])
                if not ok: errors.append(f'{iid} directly relies on source {ref} without directly acquired/reproducible evidence (evidence={mode})')
            elif ref in insights:
                warnings.append(f'{iid} is supported by another Insight {ref}; ensure the upstream support chain remains valid')
        if not supporting_obs and not any(link.get('ref') in sources for link in links):
            errors.append(f'{iid} status={ins.get("status")} has no supporting Observation or SourceRecord link')

    return errors,warnings


def main():
    p=argparse.ArgumentParser(description='Validate semantic evidence support for researched SourceRecords, Observations, and supported/active Insights across text, visual, audio, video, document, structured, and mixed-media evidence, including resolved-subject provenance when supplied.')
    p.add_argument('business_id'); a=p.parse_args()
    errors,warnings=evidence_errors(a.business_id)
    print(f'business={a.business_id} research_evidence_errors={len(errors)} warnings={len(warnings)}')
    for w in warnings: print('WARNING',w)
    for e in errors: print('ERROR',e)
    if errors: raise SystemExit(1)
    print('research evidence validation passed')

if __name__=='__main__': main()
