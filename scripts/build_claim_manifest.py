#!/usr/bin/env python3
"""Surface possible customer-facing claim text as an optional review aid.

This helper uses lightweight lexical heuristics to reduce review effort. Its candidates are
not semantic classifications, truth judgments, permission decisions, or proof that omitted
text is safe. The capable model/user decides what actually constitutes a business claim,
whether it is supported, and what verification is appropriate.
"""
from _common import *
from claim_surface import CLAIM_SURFACE_FIELDS,TEXT_NATIVE_EXTS,load_claim_surface,native_text,units
import argparse,json,re


def business_name(business_id):
    p=ROOT/'instances'/business_id/'context/business.json'
    if p.exists():
        try:return json.loads(p.read_text()).get('name') or business_id
        except Exception:pass
    return business_id


def is_candidate(sentence,name):
    """Heuristically surface text that may deserve claim review; never classify semantics."""
    s=sentence.lower();n=(name or '').lower()
    if n and n in s:return True
    if re.search(r"\b(we|we'll|we’re|we're|our|ours|us)\b",s):return True
    if re.search(r'\byou\s+(get|receive|will receive|can expect|will get|are guaranteed)\b',s):return True
    if re.search(r'\b\d+\s*[- ]?(?:minute|hour|day|week|month|year)s?\b',s):return True
    if re.search(r'\b(?:no|zero)\s+(?:setup|cost|fee|fees|commitment|contract|obligation|downtime)\b',s):return True
    if re.search(r'\b(?:demo|walkthrough|onboarding|setup)\b',s) and re.search(r'\b(?:book|see|schedule|start|required?|takes?|within|minute|hour|day|week|no)\b',s):return True
    if re.search(r'\b(?:nothing|everything|always|never|ensure|ensures|ensured|make sure|makes sure|guarantee|guarantees|guaranteed)\b',s):return True
    return False


def _surface_units(surface):
    vals=[]
    for key in CLAIM_SURFACE_FIELDS:
        value=surface.get(key);values=[value] if isinstance(value,str) else value if isinstance(value,list) else []
        vals.extend(x.strip() for x in values if isinstance(x,str) and x.strip())
    return units('\n'.join(vals))


def scan_claims(business_id,asset_file,claim_surface_ref=None):
    name=business_name(business_id);p=Path(asset_file)
    if p.suffix.lower() in TEXT_NATIVE_EXTS:
        scanned=units(native_text(p))
        # SVG is usually compact enough that returning all audience-readable units is more
        # useful than heuristically filtering them. In every format these are review candidates.
        return scanned if p.suffix.lower()=='.svg' else [x for x in scanned if is_candidate(x,name)]
    if not claim_surface_ref:
        raise ValueError('opaque/rendered media needs --claim-surface only when this optional text-review helper is being used')
    surface,error=load_claim_surface(claim_surface_ref,p)
    if error:raise ValueError(error)
    return _surface_units(surface)


def main():
    ap=argparse.ArgumentParser(description='Optionally surface possible claim text for model/human review; this does not semantically classify or authorize wording.')
    ap.add_argument('business_id');ap.add_argument('asset_file')
    ap.add_argument('--claim-surface',help='Optional JSON sidecar containing visible_text, spoken_text, and material_visual_claims for opaque/rendered media')
    a=ap.parse_args();p=Path(a.asset_file)
    if not p.is_absolute():p=ROOT/p
    if not p.exists():raise SystemExit(f'Asset file not found: {p}')
    try:candidates=scan_claims(a.business_id,p,a.claim_surface)
    except ValueError as exc:raise SystemExit(str(exc))
    print(json.dumps({'business_id':a.business_id,'asset_file':storage_ref(p),'claim_surface':a.claim_surface,'candidates':candidates,'selection_authority':False,'semantic_authority':False,'reason':'Heuristic review candidates only; the active model/user decides what is actually a business claim and whether current organization truth supports it.'},indent=2))
if __name__=='__main__':main()
