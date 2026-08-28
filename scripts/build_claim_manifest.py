#!/usr/bin/env python3
from _common import *
from claim_surface import CLAIM_SURFACE_FIELDS, TEXT_NATIVE_EXTS, load_claim_surface, native_text, units
import argparse, json, re


def business_name(business_id):
    p=ROOT/'instances'/business_id/'context/business.json'
    if p.exists():
        try:return json.loads(p.read_text()).get('name') or business_id
        except Exception:pass
    return business_id


def is_candidate(sentence,name):
    """Return customer-facing statements that need explicit classification.

    In addition to named/first-person business claims, conservatively capture operational
    promises that models often invent without naming the business: timing/duration, setup,
    availability/absolutes, demos/walkthroughs, and assurance language. False positives are
    acceptable because genuinely non-business guidance can be classified as general guidance.
    """
    s=sentence.lower(); n=(name or '').lower()
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
        value=surface.get(key)
        values=[value] if isinstance(value,str) else value if isinstance(value,list) else []
        vals.extend(x.strip() for x in values if isinstance(x,str) and x.strip())
    return units('\n'.join(vals))


def scan_claims(business_id,asset_file,claim_surface_ref=None):
    name=business_name(business_id); p=Path(asset_file)
    if p.suffix.lower() in TEXT_NATIVE_EXTS:
        scanned=units(native_text(p))
        # Compact text-bearing visual media can classify every audience-readable unit;
        # general guidance remains allowed when it is not an active-business promise.
        return scanned if p.suffix.lower()=='.svg' else [x for x in scanned if is_candidate(x,name)]
    if not claim_surface_ref:
        raise ValueError('opaque/rendered media requires --claim-surface so claims can be audited without OCR')
    surface,error=load_claim_surface(claim_surface_ref,p)
    if error:raise ValueError(error)
    # A claim surface is intentionally compact, so classify every declared customer-facing
    # text/visual claim rather than guessing which binary-media statement matters.
    return _surface_units(surface)


def main():
    ap=argparse.ArgumentParser(description='Scan a customer-facing artifact or declared media claim surface for statements that need claim-manifest classification.')
    ap.add_argument('business_id');ap.add_argument('asset_file')
    ap.add_argument('--claim-surface',help='JSON sidecar containing visible_text, spoken_text, and material_visual_claims for opaque/rendered media')
    a=ap.parse_args();p=Path(a.asset_file)
    if not p.is_absolute():p=ROOT/p
    if not p.exists():raise SystemExit(f'Asset file not found: {p}')
    try:candidates=scan_claims(a.business_id,p,a.claim_surface)
    except ValueError as exc:raise SystemExit(str(exc))
    print(json.dumps({'business_id':a.business_id,'asset_file':str(p.relative_to(ROOT)),'claim_surface':a.claim_surface,'candidates':candidates},indent=2))
if __name__=='__main__':main()
