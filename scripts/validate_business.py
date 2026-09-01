#!/usr/bin/env python3
from _common import *
from jsonschema import Draft202012Validator
from validate_references import reference_errors
from validate_isolation import isolation_errors
from validate_research_evidence import evidence_errors
from validate_local_evidence import local_evidence_errors
from validate_business_claims import claim_errors
from validate_run_completion import run_completion_errors
from validate_opportunity_grounding import opportunity_grounding_errors
from validate_attention_lifecycle import lifecycle_errors
from preference_semantics import preference_semantic_errors
from artifact_readiness import readiness_errors
import argparse,json,collections,re

ALLOWED_AUTHORITIES={'explicit_user','verified_first_party','external_evidence','derived_inference','candidate_strategy','unknown'}
EXPLICIT_CONTEXT_TYPES={'Business','Market','ProductService','Objective','BusinessClaim','Brand'}
STRATEGIC_TYPES={'Brand','AudienceSegment','Offer'}


def _businessos_ext(obj):
    ext=obj.get('extensions') if isinstance(obj.get('extensions'),dict) else {}
    return ext.get('businessos') if isinstance(ext.get('businessos'),dict) else {}


def _source_authority(src):
    ext=src.get('extensions') if isinstance(src.get('extensions'),dict) else {}
    bos=ext.get('businessos') if isinstance(ext.get('businessos'),dict) else {}
    return bos.get('authority') or ext.get('authority')


def _source_text(src):
    ext=src.get('extensions') if isinstance(src.get('extensions'),dict) else {}
    bos=ext.get('businessos') if isinstance(ext.get('businessos'),dict) else {}
    evidence=ext.get('businessos_evidence') if isinstance(ext.get('businessos_evidence'),dict) else {}
    for value in (
        ext.get('verbatim_user_statement'),bos.get('verbatim_user_statement'),
        evidence.get('captured_text'),
    ):
        if isinstance(value,str) and value.strip():return value
    return None


def _provenance_errors(objects,sources):
    """Validate source/authority mechanics while leaving semantic interpretation to the model.

    Deterministic AURA can prove that a source exists, belongs to the organization, and
    carries the claimed authority. It should not use a home-grown tokenizer/stemmer to
    decide whether a model's semantic normalization is equivalent to the source text.
    Exact literal support remains required for explicit outward BusinessClaim records.
    """
    errors=[]
    for obj,path in objects:
        if obj.get('object_type')=='SourceRecord':continue
        typ=obj.get('object_type');bos=_businessos_ext(obj)
        authority=bos.get('authority') or (obj.get('authority') if typ=='BusinessClaim' else None)

        if typ in STRATEGIC_TYPES:
            if not authority:
                errors.append(f'{path} {typ} requires extensions.businessos.authority; use explicit_user/verified_first_party for established organization guidance or derived_inference/candidate_strategy for model-created strategy')
                continue
            if authority not in ALLOWED_AUTHORITIES:errors.append(f'{path} {typ} has unknown authority {authority!r}')
            if authority in {'derived_inference','candidate_strategy'}:
                basis=bos.get('basis_refs') or obj.get('lineage') or []
                if not basis:errors.append(f'{path} {typ} {authority} requires basis_refs/lineage')

        if authority!='explicit_user':continue
        if typ not in EXPLICIT_CONTEXT_TYPES:
            errors.append(f'{path} explicit_user authority is not allowed for {typ}; preserve the appropriate evidence/decision/inference semantics instead')
            continue
        srcid=(obj.get('source_ref') if typ=='BusinessClaim' else None) or bos.get('source_ref')
        if not srcid or srcid not in sources:
            errors.append(f'{path} explicit_user authority requires an existing SourceRecord source_ref; got {srcid!r}')
            continue
        src=sources[srcid]
        if _source_authority(src)!='explicit_user':
            errors.append(f'{path} explicit_user source {srcid} is not marked explicit_user authority')
            continue

        # Exact authorized outward claims need exact evidence. General business context
        # may be semantically normalized by the capable model as long as its source and
        # authority are preserved; deterministic AURA does not re-interpret language.
        if typ=='BusinessClaim':
            if obj.get('authority')!='explicit_user':
                errors.append(f'{path} explicit-user BusinessClaim must declare authority=explicit_user')
                continue
            quote=obj.get('support_quote');statement=_source_text(src)
            if not isinstance(quote,str) or not quote.strip():
                errors.append(f'{path} explicit-user BusinessClaim requires a non-empty support_quote')
                continue
            if not statement:
                errors.append(f'{path} explicit-user BusinessClaim source {srcid} lacks captured/verbatim text for literal support')
                continue
            normalized_quote=re.sub(r'\s+',' ',quote).strip().lower();normalized_source=re.sub(r'\s+',' ',statement).strip().lower()
            if normalized_quote not in normalized_source:
                errors.append(f'{path} explicit-user BusinessClaim support_quote is not a literal excerpt of source {srcid}')
    return errors


def validate_business(business_id,require_context=False,active_run_id=None):
    errors=[];warnings=[];base=ROOT/'instances'/business_id
    if not base.exists() or not base.is_dir():return [f'Unknown business: {business_id}'],warnings,{}
    try:inst=json.loads((base/'instance.json').read_text())
    except Exception as e:return [f'invalid instance.json: {e}'],warnings,{}
    if inst.get('business_id')!=business_id:errors.append('instance.json business_id mismatch')
    unknown=set(inst.get('enabled_systems',[]))-(installed_modules()-{'core'})
    if unknown:errors.append('instance enables unavailable modules: '+', '.join(sorted(unknown)))
    schemas_by_title={}
    for sp in schemas():
        try:
            sd=json.loads(sp.read_text());title=sd.get('title')
            if title:schemas_by_title[title]=(sd,sp)
        except Exception:pass
    ids={};counts=collections.Counter();objects=[];sources={}
    for p in sorted(base.rglob('*.json')):
        try:data=json.loads(p.read_text())
        except Exception as e:errors.append(f'{p.relative_to(ROOT)} invalid JSON: {e}');continue
        vals=data if isinstance(data,list) else [data]
        for obj in vals:
            if not isinstance(obj,dict) or not obj.get('object_type'):continue
            typ=obj.get('object_type');oid=obj.get('id');rel=str(p.relative_to(ROOT))
            if typ not in schemas_by_title:errors.append(f'{rel} unknown object_type {typ}');continue
            schema,_=schemas_by_title[typ]
            for e in Draft202012Validator(schema).iter_errors(obj):errors.append(f'{rel} {list(e.path)}: {e.message}')
            if obj.get('business_id')!=business_id:errors.append(f'{rel} business_id mismatch')
            if oid:
                if oid in ids:errors.append(f'duplicate object id {oid}: {ids[oid]} and {rel}')
                ids[oid]=rel
            counts[typ]+=1;objects.append((obj,rel))
            if typ=='PreferenceProfile':errors.extend(f'{rel} {e}' for e in preference_semantic_errors(obj.get('preferences') or {}))
            if typ=='SourceRecord' and oid:sources[oid]=obj
    errors.extend(_provenance_errors(objects,sources))
    errors.extend(claim_errors(business_id,objects))
    errors.extend(run_completion_errors(business_id,objects,active_run_id))
    errors.extend(readiness_errors(business_id,objects))
    og_errors,og_warnings=opportunity_grounding_errors(business_id,objects);errors.extend(og_errors);warnings.extend(og_warnings)
    re_errors,re_warnings=evidence_errors(business_id);errors.extend(re_errors);warnings.extend(re_warnings)
    le_errors,le_warnings=local_evidence_errors(business_id);errors.extend(le_errors);warnings.extend(le_warnings)
    errors.extend(lifecycle_errors(business_id,objects))
    errors.extend(reference_errors(business_id))
    iso,_=isolation_errors();errors.extend([e for e in iso if f'instances/{business_id}/' in e or f'-> {business_id}' in e])
    notes=[p for p in (base/'context').rglob('*.md') if p.name!='README.md'] if (base/'context').exists() else []
    if notes:warnings.append('supplemental Markdown exists under context; it is non-canonical and does not satisfy object writes: '+', '.join(str(p.relative_to(base)) for p in notes))
    if require_context and counts['Business']<1:errors.append('required canonical Business context is missing; free-form notes do not satisfy bootstrap')
    return errors,warnings,dict(sorted(counts.items()))


def main():
    ap=argparse.ArgumentParser(description='Validate one active AURA organization instance. This is not release/distribution validation.')
    ap.add_argument('business_id');ap.add_argument('--require-context',action='store_true');a=ap.parse_args()
    errors,warnings,counts=validate_business(a.business_id,a.require_context)
    print(f'business={a.business_id} canonical_objects={sum(counts.values())} types={json.dumps(counts,sort_keys=True)}')
    print(f'Errors: {len(errors)}; Warnings: {len(warnings)}')
    for w in warnings:print('WARNING',w)
    for e in errors:print('ERROR',e)
    if errors:raise SystemExit(1)
    print('active business validation passed')
if __name__=='__main__':main()
