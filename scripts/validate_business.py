#!/usr/bin/env python3
from _common import *
from jsonschema import Draft202012Validator
from validate_references import reference_errors
from validate_isolation import isolation_errors
from validate_research_evidence import evidence_errors
from validate_local_evidence import local_evidence_errors
from validate_business_claims import claim_errors
from validate_customer_facing_mutations import mutation_errors
from validate_run_completion import run_completion_errors
from validate_opportunity_grounding import opportunity_grounding_errors
from validate_attention_lifecycle import lifecycle_errors
from preference_semantics import preference_semantic_errors
from artifact_readiness import readiness_errors
import argparse,json,collections
from bootstrap_explicit_context import _fact_tokens, GROUNDING_METHOD

def _explicit_values(obj):
    typ=obj.get('object_type')
    vals=[]
    if typ=='Business':
        vals += [(x,'industry') for x in obj.get('industries',[]) if x]
        vals += [(x,'business model') for x in obj.get('business_models',[]) if x]
        ext=obj.get('extensions',{}) if isinstance(obj.get('extensions'),dict) else {}
        vals += [(x,'lead source') for x in ext.get('lead_sources',[]) if x]
    elif typ=='Market':
        if obj.get('name'): vals.append((obj['name'],'market'))
        if obj.get('geography') and obj.get('geography')!=obj.get('name'): vals.append((obj['geography'],'market geography'))
    elif typ=='ProductService':
        if obj.get('name'): vals.append((obj['name'],'service'))
    elif typ=='Objective':
        if obj.get('name'): vals.append((obj['name'],'objective'))
    elif typ=='BusinessClaim':
        if obj.get('statement'): vals.append((obj['statement'],'business claim'))
    elif typ=='Brand':
        def add(v,label):
            if isinstance(v,str) and v.strip(): vals.append((v.strip(),label))
            elif isinstance(v,list):
                for x in v:add(x,label)
            elif isinstance(v,dict):
                for k,x in v.items():add(x,f'{label}.{k}')
        if obj.get('name'): vals.append((obj['name'],'brand name'))
        for k in ['voice','positioning','visual_identity','content_style','channel_preferences','reference_assets','prohibited_styles','brand_rules','approved_claims','claims_to_avoid']:
            if k in obj:add(obj[k],f'brand {k}')
    return vals

def _provenance_errors(objects, sources):
    errors=[]
    explicit_types={'Business','Market','ProductService','Objective','BusinessClaim','Brand'}
    strategic_types={'Brand','AudienceSegment','Offer'}
    allowed_authorities={'explicit_user','verified_first_party','external_evidence','derived_inference','candidate_strategy','unknown'}
    for obj,path in objects:
        if obj.get('object_type')=='SourceRecord': continue
        typ=obj.get('object_type')
        ext=obj.get('extensions') if isinstance(obj.get('extensions'),dict) else {}
        bos=ext.get('businessos') if isinstance(ext.get('businessos'),dict) else {}
        authority=bos.get('authority') or (obj.get('authority') if typ=='BusinessClaim' else None)
        if typ in strategic_types:
            if not authority:
                errors.append(f'{path} {typ} requires extensions.businessos.authority; use derived_inference/candidate_strategy for agent-created strategy')
                continue
            if authority not in allowed_authorities:
                errors.append(f'{path} {typ} has unknown authority {authority!r}')
            if authority=='explicit_user':
                if not (typ=='Brand' and bos.get('grounding_method')==GROUNDING_METHOD and bos.get('explicit_brand_profile') is True):
                    errors.append(f'{path} {typ} may not self-assert explicit_user authority; persist explicit Brand instructions through bootstrap_explicit_context.py or preserve exact authorized claims as BusinessClaim and mark assembled strategy derived_inference/candidate_strategy')
                    continue
            if authority in {'derived_inference','candidate_strategy'}:
                basis=bos.get('basis_refs') or obj.get('lineage') or []
                if not basis: errors.append(f'{path} {typ} {authority} requires basis_refs/lineage')
        if authority!='explicit_user': continue
        if typ not in explicit_types:
            errors.append(f'{path} explicit_user authority is not allowed for {typ}; use the supported grounded context path')
            continue
        srcid=(obj.get('source_ref') if typ=='BusinessClaim' else None) or bos.get('source_ref')
        if not srcid or srcid not in sources:
            errors.append(f'{path} explicit_user authority requires an existing SourceRecord source_ref; got {srcid!r}')
            continue
        src=sources[srcid]
        sext=src.get('extensions') if isinstance(src.get('extensions'),dict) else {}
        statement=sext.get('verbatim_user_statement')
        # Only deterministic bootstrap-owned explicit objects may use this grounding method.
        if sext.get('grounding_method')!=GROUNDING_METHOD:
            errors.append(f'{path} explicit_user source {srcid} is not trusted: source was not persisted through {GROUNDING_METHOD}')
            continue
        if typ!='BusinessClaim' and bos.get('grounding_method')!=GROUNDING_METHOD:
            errors.append(f'{path} explicit_user authority is not trusted: canonical fact was not persisted through {GROUNDING_METHOD}')
            continue
        if typ=='BusinessClaim':
            if obj.get('authority')!='explicit_user' or bos.get('grounding_method')!=GROUNDING_METHOD:
                errors.append(f'{path} explicit-user BusinessClaim is not trusted: claim was not persisted through {GROUNDING_METHOD}')
                continue
        if not statement:
            errors.append(f'{path} explicit_user source {srcid} lacks verbatim_user_statement grounding')
            continue
        if typ=='BusinessClaim':
            quote=obj.get('support_quote')
            if not isinstance(quote,str) or not quote.strip():
                errors.append(f'{path} explicit-user BusinessClaim requires a non-empty support_quote')
                continue
            normalized_quote=re.sub(r'\s+',' ',quote).strip().lower()
            normalized_source=re.sub(r'\s+',' ',statement).strip().lower()
            if normalized_quote not in normalized_source:
                errors.append(f'{path} explicit-user BusinessClaim support_quote is not a literal excerpt of source {srcid}')
                continue
        stoks=_fact_tokens(statement)
        for value,label in _explicit_values(obj):
            missing=sorted(_fact_tokens(value)-stoks)
            if missing:
                errors.append(f'{path} explicit_user {label} {value!r} is not grounded in source {srcid}; unsupported token(s): {", ".join(missing)}')
    return errors

def validate_business(business_id,require_context=False,active_run_id=None):
    errors=[];warnings=[];base=ROOT/'instances'/business_id
    if not base.exists() or not base.is_dir(): return [f'Unknown business: {business_id}'],warnings,{}
    try: inst=json.loads((base/'instance.json').read_text())
    except Exception as e: return [f'invalid instance.json: {e}'],warnings,{}
    if inst.get('business_id')!=business_id: errors.append('instance.json business_id mismatch')
    unknown=set(inst.get('enabled_systems',[]))-(installed_modules()-{'core'})
    if unknown: errors.append('instance enables unavailable modules: '+', '.join(sorted(unknown)))
    schemas_by_title={}
    for sp in schemas():
        try:
            sd=json.loads(sp.read_text()); title=sd.get('title')
            if title: schemas_by_title[title]=(sd,sp)
        except Exception: pass
    ids={};counts=collections.Counter(); objects=[]; sources={}
    for p in sorted(base.rglob('*.json')):
        try:data=json.loads(p.read_text())
        except Exception as e: errors.append(f'{p.relative_to(ROOT)} invalid JSON: {e}');continue
        vals=data if isinstance(data,list) else [data]
        for obj in vals:
            if not isinstance(obj,dict) or not obj.get('object_type'): continue
            typ=obj.get('object_type'); oid=obj.get('id'); rel=str(p.relative_to(ROOT))
            if typ not in schemas_by_title: errors.append(f'{rel} unknown object_type {typ}');continue
            schema,_=schemas_by_title[typ]
            for e in Draft202012Validator(schema).iter_errors(obj): errors.append(f'{rel} {list(e.path)}: {e.message}')
            if obj.get('business_id')!=business_id: errors.append(f'{rel} business_id mismatch')
            if oid:
                if oid in ids: errors.append(f'duplicate object id {oid}: {ids[oid]} and {rel}')
                ids[oid]=rel
            counts[typ]+=1; objects.append((obj,rel))
            if typ=='PreferenceProfile':
                errors.extend(f'{rel} {e}' for e in preference_semantic_errors(obj.get('preferences') or {}))
            if typ=='SourceRecord' and oid: sources[oid]=obj
    errors.extend(_provenance_errors(objects,sources))
    errors.extend(claim_errors(business_id,objects))
    errors.extend(mutation_errors(business_id,objects))
    errors.extend(run_completion_errors(business_id,objects,active_run_id))
    errors.extend(readiness_errors(business_id,objects))
    og_errors,og_warnings=opportunity_grounding_errors(business_id,objects); errors.extend(og_errors); warnings.extend(og_warnings)
    re_errors,re_warnings=evidence_errors(business_id); errors.extend(re_errors); warnings.extend(re_warnings)
    le_errors,le_warnings=local_evidence_errors(business_id); errors.extend(le_errors); warnings.extend(le_warnings)
    errors.extend(lifecycle_errors(business_id,objects))
    errors.extend(reference_errors(business_id))
    iso,_=isolation_errors(); errors.extend([e for e in iso if f'instances/{business_id}/' in e or f'-> {business_id}' in e])
    notes=[p for p in (base/'context').rglob('*.md') if p.name!='README.md'] if (base/'context').exists() else []
    if notes: warnings.append('supplemental Markdown exists under context; it is non-canonical and does not satisfy object writes: '+', '.join(str(p.relative_to(base)) for p in notes))
    if require_context and counts['Business']<1: errors.append('required canonical Business context is missing; free-form notes do not satisfy bootstrap')
    return errors,warnings,dict(sorted(counts.items()))

def main():
    ap=argparse.ArgumentParser(description='Validate one active BusinessOS business instance. This is not release/distribution validation.')
    ap.add_argument('business_id'); ap.add_argument('--require-context',action='store_true'); a=ap.parse_args()
    errors,warnings,counts=validate_business(a.business_id,a.require_context)
    print(f'business={a.business_id} canonical_objects={sum(counts.values())} types={json.dumps(counts,sort_keys=True)}')
    print(f'Errors: {len(errors)}; Warnings: {len(warnings)}')
    for w in warnings: print('WARNING',w)
    for e in errors: print('ERROR',e)
    if errors: raise SystemExit(1)
    print('active business validation passed')
if __name__=='__main__': main()
