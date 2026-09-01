#!/usr/bin/env python3
"""Remove organization-owned memory only when doing so leaves canonical state sound.

For current truth corrections, prefer updating the existing object. Use this helper when
the object itself should no longer exist. If historical state is materially useful, keep
or retire it instead. AURA refuses deletion when another canonical object still refers
to the target; the capable model/user must resolve those semantics first rather than
having a deterministic helper rewrite meaning automatically.
"""
import argparse,json
from _common import *
from validate_business import validate_business
from validate_references import inbound_references


def forget(business_id,object_ref):
    resolved=resolve_business(business_id)
    if resolved.get('status')!='resolved':raise ValueError(resolved.get('reason') or 'Organization could not be resolved')
    bid=resolved['business_id'];idx=object_index(bid)
    if object_ref not in idx:raise ValueError(f'Unknown canonical object_ref for {bid}: {object_ref}')
    obj,path=idx[object_ref];typ=obj.get('object_type')
    if typ=='Business':raise ValueError('The canonical Business identity anchors the managed organization and may not be forgotten. Update its current fields or remove the organization workspace intentionally instead.')
    inbound=inbound_references(bid,object_ref)
    if inbound:
        refs=', '.join(f"{row['object_ref']} ({row['object_type']})" for row in inbound[:12])
        raise ValueError(f'Refusing to forget {object_ref}; canonical state still refers to it from: {refs}. Resolve/update those dependent meanings first.')
    path=Path(path);stored=json.loads(path.read_text())
    if not isinstance(stored,dict) or stored.get('id')!=object_ref:
        raise ValueError(f'{object_ref} is not stored as one independently removable canonical object')
    snapshot=path.read_bytes();path.unlink()
    try:
        errors,warnings,counts=validate_business(bid,require_context=True)
        if errors:raise ValueError('Post-removal validation failed: '+'; '.join(errors[:12]))
    except Exception:
        path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(snapshot);raise
    return {
        'status':'forgotten','business_id':bid,'object_ref':object_ref,'object_type':typ,
        'former_path':storage_ref(path),'validation':{'status':'clean','warnings':warnings[:5],'canonical_object_counts':counts},
        'rule':'The object was removed because no canonical state depended on it. AURA did not fabricate historical replacement state.'
    }


def main():
    p=argparse.ArgumentParser(description='Safely forget one unreferenced canonical AURA object. Update current truth instead when only its fields changed.')
    p.add_argument('business_id');p.add_argument('object_ref');a=p.parse_args()
    try:result=forget(a.business_id,a.object_ref)
    except (ValueError,OSError,json.JSONDecodeError) as exc:raise SystemExit(str(exc))
    print(json.dumps(result,indent=2,ensure_ascii=False))

if __name__=='__main__':main()
