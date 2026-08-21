#!/usr/bin/env python3
from _common import *
import argparse, json
PERSONAL_FIELDS=('name','email','phone','location')
BUSINESS_FIELDS=('name','organization','email','phone','location','website')
def load_json(path, default): return json.loads(path.read_text()) if path.exists() else default
def resolve_profile(business_id):
    base=ROOT/'instances'/business_id
    if not base.exists(): raise ValueError('Unknown business')
    bp=base/'config/external-research-profile.json'
    if not bp.exists(): raise ValueError('Business research profile missing')
    business=load_json(bp,{})
    operator=load_json(ROOT/'deployment/operator-profile.json',{})
    effective={k:None for k in BUSINESS_FIELDS}; sources={k:None for k in BUSINESS_FIELDS}
    bident=business.get('identity') or {}
    for k in BUSINESS_FIELDS:
        v=bident.get(k)
        if v not in (None,''): effective[k]=v; sources[k]='business'
    if business.get('inherit_operator_profile',True):
        oident=operator.get('identity') or {}; reusable=set(operator.get('reuse_across_businesses') or [])
        for k in PERSONAL_FIELDS:
            if effective[k] in (None,'') and k in reusable:
                v=oident.get(k)
                if v not in (None,''): effective[k]=v; sources[k]='operator'
    return {'format_version':'1.0','business_id':business_id,'identity':effective,'sources':sources,'inherit_operator_profile':bool(business.get('inherit_operator_profile',True)),'allowed_without_additional_approval':business.get('allowed_without_additional_approval',[]),'requires_approval':business.get('requires_approval',[]),'prohibited':business.get('prohibited',[]),'notes':business.get('notes')}
def main():
    p=argparse.ArgumentParser(); p.add_argument('business_id'); a=p.parse_args()
    try: r=resolve_profile(a.business_id)
    except ValueError as e: raise SystemExit(str(e))
    print(json.dumps(r,indent=2))
if __name__=='__main__': main()
