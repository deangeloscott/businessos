#!/usr/bin/env python3
"""Validate intra-organization canonical references from the canonical organization model."""
from _common import *
from canonical_store import INSTANCE_PATHS
import argparse,json,re


def canonical_reference_pattern():
    """Build the reference grammar from canonical organization-object ID schemas.

    Retired canonical prefixes disappear when their canonical types disappear; new canonical
    types become reference-valid automatically. Runtime/config/package interface schemas do
    not become canonical references merely because they also have ids. This derives directly
    from source schemas and does not require generated registries.
    """
    schema_by_title={}
    for path in schemas():
        try:data=json.loads(path.read_text())
        except Exception:continue
        title=data.get('title')
        if title in INSTANCE_PATHS:schema_by_title[title]=data
    prefixes=set()
    for title in INSTANCE_PATHS:
        data=schema_by_title.get(title) or {}
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
    index=object_index(business_id);errors=[];pat=canonical_reference_pattern()
    for oid,(obj,path) in index.items():
        for ref in pat.findall(json.dumps(obj)):
            if ref!=oid and ref not in index:errors.append(f'{path.relative_to(ROOT)} unresolved ref {ref}')
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
    return True,[],len(object_index(business_id))

def main():
    p=argparse.ArgumentParser();p.add_argument('business_id');a=p.parse_args();ok,errs,count=validate_references(a.business_id)
    if not ok:print('\n'.join(errs));raise SystemExit(1)
    print(f'references valid: {count} canonical objects')
if __name__=='__main__':main()
