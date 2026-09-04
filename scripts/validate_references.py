#!/usr/bin/env python3
"""Validate intra-organization canonical references from the canonical organization model."""
from _common import *
from canonical_store import INSTANCE_PATHS,schema_entry
import argparse,json,re


def canonical_reference_pattern():
    """Build the reference grammar from canonical organization-object ID schemas.

    Retired canonical prefixes disappear when their canonical types disappear; new canonical
    types become reference-valid automatically. Runtime/config/package interface schemas do
    not become canonical references merely because they also have ids.
    """
    prefixes=set()
    for title in INSTANCE_PATHS:
        try:_,data=schema_entry(title)
        except Exception:continue
        pattern=(((data.get('properties') or {}).get('id') or {}).get('pattern') or '')
        match=re.match(r'^\^([A-Za-z0-9]+)_',pattern)
        if match:prefixes.add(match.group(1))
    if not prefixes:raise ValueError('No canonical ID prefixes could be derived from the canonical organization model')
    joined='|'.join(sorted((re.escape(prefix) for prefix in prefixes),key=len,reverse=True))
    return re.compile(rf'(?<![A-Za-z0-9_-])(?:{joined})_[A-Za-z0-9_-]+(?![A-Za-z0-9_-])')


def references_in(value):
    return set(canonical_reference_pattern().findall(json.dumps(value)))


def reference_errors(business_id):
    base=ROOT/'instances'/business_id
    if not base.exists():return ['Unknown business']
    index={}
    for file in base.rglob('*.json'):
        try:data=json.loads(file.read_text())
        except Exception:continue
        vals=data if isinstance(data,list) else [data]
        for item in vals:
            if isinstance(item,dict) and item.get('id'):index[item['id']]=file
    errors=[];pat=canonical_reference_pattern()
    for oid,file in index.items():
        try:data=json.loads(file.read_text())
        except Exception:continue
        for ref in pat.findall(json.dumps(data)):
            if ref!=oid and ref not in index:errors.append(f'{file.relative_to(ROOT)} unresolved ref {ref}')
    return errors


def inbound_references(business_id,target_ref):
    """Return canonical objects that currently reference target_ref."""
    out=[];target=str(target_ref)
    for obj,path in iter_instance_objects(business_id):
        if obj.get('id')==target:continue
        if target in references_in(obj):out.append({'object_ref':obj.get('id'),'object_type':obj.get('object_type'),'path':storage_ref(path)})
    return out


def validate_references(business_id):
    errs=reference_errors(business_id)
    if errs:return False,errs,0
    base=ROOT/'instances'/business_id;count=sum(1 for file in base.rglob('*.json') if _has_id(file))
    return True,[],count

def _has_id(file):
    try:data=json.loads(file.read_text());return isinstance(data,dict) and bool(data.get('id'))
    except Exception:return False

def main():
    p=argparse.ArgumentParser();p.add_argument('business_id');a=p.parse_args();ok,errs,count=validate_references(a.business_id)
    if not ok:print('\n'.join(errs));raise SystemExit(1)
    print(f'references valid: {count} objects')
if __name__=='__main__':main()
