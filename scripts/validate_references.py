#!/usr/bin/env python3
from _common import *
import argparse,json,re
PAT=re.compile(r'(?<![A-Za-z0-9_-])(?:src|obs|ins|prf|opp|ini|act|wrk|apr|chg|ver|ast|mdef|mobs|exp|eval|lrn|inc|att|plc|clm|cup|cmp|plt|jrn|iev|ocs|odm|sas|aud|brd|biz|eco|mkt|obj|off|ofr|prd)_[A-Za-z0-9_-]+(?![A-Za-z0-9_-])')

def reference_errors(business_id):
    base=ROOT/'instances'/business_id
    if not base.exists():return ['Unknown business']
    index={}
    for f in base.rglob('*.json'):
        try:o=json.loads(f.read_text())
        except Exception:continue
        vals=o if isinstance(o,list) else [o]
        for item in vals:
            if isinstance(item,dict) and item.get('id'):index[item['id']]=f
    errors=[]
    for oid,f in index.items():
        try:o=json.loads(f.read_text())
        except Exception:continue
        for ref in PAT.findall(json.dumps(o)):
            if ref!=oid and ref not in index:errors.append(f'{f.relative_to(ROOT)} unresolved ref {ref}')
    return errors

def validate_references(business_id):
    errs=reference_errors(business_id)
    if errs:return False,errs,0
    base=ROOT/'instances'/business_id;count=sum(1 for f in base.rglob('*.json') if _has_id(f))
    return True,[],count

def _has_id(f):
    try:o=json.loads(f.read_text());return isinstance(o,dict) and bool(o.get('id'))
    except Exception:return False

def main():
    p=argparse.ArgumentParser();p.add_argument('business_id');a=p.parse_args();ok,errs,count=validate_references(a.business_id)
    if not ok:print('\n'.join(errs));raise SystemExit(1)
    print(f'references valid: {count} objects')
if __name__=='__main__':main()
