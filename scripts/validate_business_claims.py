#!/usr/bin/env python3
"""Validate structural provenance for optional customer-facing claim manifests.

AURA can verify that referenced organization truth exists and has an appropriate authority.
It must not use token overlap, stemming, regex phrase lists, or other home-grown NLP to
decide whether natural-language customer-facing copy is semantically supported. That
judgment belongs to the capable model/user applying the active-business truth policy.
"""
from _common import *

ALLOWED={'approved_business_claim','general_guidance','placeholder'}


def _trusted(obj):
    if obj.get('object_type')=='BusinessClaim':
        authority=obj.get('authority')
        trusted=bool(obj.get('status')=='approved' and obj.get('claim_kind')=='approved_business_claim' and authority in {'explicit_user','verified_first_party'})
        if authority=='verified_first_party':trusted=trusted and bool(obj.get('source_ref') and obj.get('support_quote'))
        return trusted
    ext=obj.get('extensions',{}) if isinstance(obj.get('extensions'),dict) else {}
    bos=ext.get('businessos',{}) if isinstance(ext.get('businessos'),dict) else {}
    return bos.get('authority') in {'explicit_user','verified_first_party'}


def validate_manifest_entries(manifest,idx,rel):
    errors=[]
    if manifest is None:return errors
    if not isinstance(manifest,list):return [f'{rel} extensions.businessos.claim_manifest must be a list when supplied']
    for i,item in enumerate(manifest):
        if not isinstance(item,dict):
            errors.append(f'{rel} claim_manifest[{i}] must be an object');continue
        cls=item.get('classification')
        if cls not in ALLOWED:
            errors.append(f'{rel} claim_manifest[{i}] has invalid classification {cls!r}');continue
        if cls!='approved_business_claim':continue
        refs=item.get('support_refs') or []
        if not isinstance(refs,list) or not refs:
            errors.append(f'{rel} claim_manifest[{i}] approved_business_claim requires support_refs');continue
        bad=[]
        for rid in refs:
            ent=idx.get(rid)
            if not ent or not _trusted(ent[0]):bad.append(rid)
        if bad:errors.append(f'{rel} claim_manifest[{i}] uses missing/untrusted support refs {bad}')
    return errors


def claim_errors(business_id,objects=None):
    """Validate only explicit claim-manifest provenance; omission is not an error."""
    errors=[];idx=object_index(business_id)
    if objects is None:objects=list(idx.values())
    else:objects=[(o,ROOT/p) if isinstance(p,str) else (o,p) for o,p in objects]
    for asset,path in objects:
        if asset.get('object_type')!='Asset' or asset.get('owner_system') not in {'content-synthesis','marketing-synthesis'}:continue
        bos=(asset.get('extensions') or {}).get('businessos',{}) if isinstance(asset.get('extensions'),dict) else {}
        rel=str(path.relative_to(ROOT)) if isinstance(path,Path) and path.is_absolute() else str(path)
        errors.extend(validate_manifest_entries(bos.get('claim_manifest'),idx,rel))
    return errors
