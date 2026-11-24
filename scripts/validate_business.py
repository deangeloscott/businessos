#!/usr/bin/env python3
from _common import *
from jsonschema import Draft202012Validator
from canonical_store import DATE_FORMATS
from validate_references import reference_errors
from validate_isolation import isolation_errors
from validate_research_evidence import evidence_errors
from validate_local_evidence import local_evidence_errors
from validate_business_claims import claim_errors
from validate_run_completion import run_completion_errors
from validate_opportunity_grounding import opportunity_grounding_errors
from validate_attention_lifecycle import lifecycle_errors
from preference_semantics import preference_semantic_errors
import argparse,json,collections,re,functools

@functools.lru_cache(maxsize=1)
def _schema_validators():
    """Schemas by title with one ready validator each. Product schemas are read once per process."""
    out={}
    for sp in schemas():
        try:
            sd=json.loads(sp.read_text(encoding='utf-8'));title=sd.get('title')
            if title:out[title]=(sd,sp,Draft202012Validator(sd,format_checker=DATE_FORMATS))
        except Exception:pass
    return out


ALLOWED_AUTHORITIES={'explicit_user','verified_first_party','external_evidence','derived_inference','candidate_strategy','unknown'}
EXPLICIT_CONTEXT_TYPES={'Business','Market','ProductService','Objective','BusinessClaim','Brand'}
STRATEGIC_TYPES={'Brand','AudienceSegment','Offer'}


def _businessos_ext(obj):
    ext=obj.get('extensions') if isinstance(obj.get('extensions'),dict) else {}
    return ext.get('businessos') if isinstance(ext.get('businessos'),dict) else {}


# Said where it is needed, so a model that hits one of these checks can fix it in one step.
STATED_FIX=(' To save what the person said, give remember.py their message as "said" and write each fact in their own words; '
            'AURA records the source. Wording that is yours rather than theirs belongs in ordinary context instead.')


def _source_authority(src):
    ext=src.get('extensions') if isinstance(src.get('extensions'),dict) else {}
    bos=ext.get('businessos') if isinstance(ext.get('businessos'),dict) else {}
    return bos.get('authority') or ext.get('authority')


def _source_text(src):
    ext=src.get('extensions') if isinstance(src.get('extensions'),dict) else {}
    bos=ext.get('businessos') if isinstance(ext.get('businessos'),dict) else {}
    evidence=ext.get('businessos_evidence') if isinstance(ext.get('businessos_evidence'),dict) else {}
    for value in (ext.get('verbatim_user_statement'),bos.get('verbatim_user_statement'),evidence.get('captured_text')):
        if isinstance(value,str) and value.strip():return value
    return None


def _provenance_errors(objects,sources):
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
            errors.append(f'{path} explicit_user authority requires an existing SourceRecord source_ref; got {srcid!r}.'+STATED_FIX)
            continue
        src=sources[srcid]
        if _source_authority(src)!='explicit_user':
            errors.append(f'{path} explicit_user source {srcid} is not marked explicit_user authority.'+STATED_FIX)
            continue
        if typ=='BusinessClaim':
            if obj.get('authority')!='explicit_user':
                errors.append(f'{path} explicit-user BusinessClaim must declare authority=explicit_user')
                continue
            quote=obj.get('support_quote');statement=_source_text(src)
            if not isinstance(quote,str) or not quote.strip():
                errors.append(f'{path} explicit-user BusinessClaim requires a non-empty support_quote.'+STATED_FIX)
                continue
            if not statement:
                errors.append(f'{path} explicit-user BusinessClaim source {srcid} lacks captured/verbatim text for literal support.'+STATED_FIX)
                continue
            normalized_quote=re.sub(r'\s+',' ',quote).strip().rstrip('.!').lower();normalized_source=re.sub(r'\s+',' ',statement).strip().lower()
            if normalized_quote not in normalized_source:
                errors.append(f'{path} explicit-user BusinessClaim support_quote is not a literal excerpt of source {srcid}.'+STATED_FIX)
    return errors


def validate_business(business_id,require_context=False):
    # Every check below reads the same records; they share one read instead of each re-reading the workspace.
    with index_snapshot():return _validate_business(business_id,require_context)


def _validate_business(business_id,require_context=False):
    errors=[];warnings=[];base=ROOT/'instances'/business_id
    if not base.exists() or not base.is_dir():return [f'Unknown business: {business_id}'],warnings,{}
    if base.resolve()!=workspace_root().resolve()/'instances'/business_id:return ['Linked record folder is outside this business.'],warnings,{}
    try:inst=json.loads((base/'instance.json').read_text(encoding='utf-8'))
    except Exception as e:return [f'invalid instance.json: {e}'],warnings,{}
    if inst.get('business_id')!=business_id:errors.append('instance.json business_id mismatch')
    unknown=set(inst.get('enabled_systems',[]))-(installed_modules()-{'core'})
    if unknown:errors.append('instance enables unavailable modules: '+', '.join(sorted(unknown)))
    schemas_by_title=_schema_validators()
    ids={};counts=collections.Counter();objects=[];sources={}
    # Locations are worked out as plain strings: the same results as before, without a path lookup per record.
    base_text=str(base);root_text=str(workspace_root()) if workspace_is_external() else str(PRODUCT_ROOT)
    for raw,stat_result,_ in walk_files(base):
        if not raw.endswith('.json'):continue
        rel=os.path.relpath(raw,root_text)
        try:data=json.loads(read_text_cached(raw,stat_result))
        except Exception as e:errors.append(f'{rel} invalid JSON: {e}');continue
        vals=data if isinstance(data,list) else [data]
        historical='history' in os.path.relpath(raw,base_text).split(os.sep)
        for obj in vals:
            if not isinstance(obj,dict) or not obj.get('object_type'):continue
            typ=obj.get('object_type');oid=obj.get('id')
            if typ not in schemas_by_title:errors.append(f'{rel} unknown object_type {typ}');continue
            schema,_,check=schemas_by_title[typ]
            for e in check.iter_errors(obj):errors.append(f'{rel} {list(e.path)}: {e.message}')
            if obj.get('business_id')!=business_id:errors.append(f'{rel} business_id mismatch')
            if oid:
                if oid in ids:errors.append(f'duplicate object id {oid}: {ids[oid]} and {rel}')
                ids[oid]=rel
            if not historical:counts[typ]+=1
            objects.append((obj,rel))
            if typ=='PreferenceProfile':errors.extend(f'{rel} {e}' for e in preference_semantic_errors(obj.get('preferences') or {}))
            if typ=='SourceRecord' and oid:sources[oid]=obj
    errors.extend(_provenance_errors(objects,sources))
    errors.extend(claim_errors(business_id,objects))
    errors.extend(run_completion_errors(business_id,objects))
    og_errors,og_warnings=opportunity_grounding_errors(business_id,objects);errors.extend(og_errors);warnings.extend(og_warnings)
    re_errors,re_warnings=evidence_errors(business_id);errors.extend(re_errors);warnings.extend(re_warnings)
    le_errors,le_warnings=local_evidence_errors(business_id);errors.extend(le_errors);warnings.extend(le_warnings)
    errors.extend(lifecycle_errors(business_id,objects))
    errors.extend(reference_errors(business_id))
    iso,_=isolation_errors(business_id);errors.extend(iso)
    notes=[p for p in (base/'context').rglob('*.md') if p.name!='README.md'] if (base/'context').exists() else []
    if notes:warnings.append('supplemental Markdown exists under context; it is non-canonical and does not satisfy object writes: '+', '.join(str(p.relative_to(base)) for p in notes))
    if require_context and counts['Business']<1:errors.append('required canonical Business context is missing; free-form notes do not satisfy bootstrap')
    return errors,warnings,dict(sorted(counts.items()))


def _put_back(files):
    for path,data in files.items():
        if data is None:path.unlink(missing_ok=True)
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)


def only_new_problems(errors,before,recheck):
    """Split `errors`, found after a change, into those the change introduced and those that were already there.

    `before` maps each changed file to its earlier bytes (None if it did not exist); `recheck` returns the errors for the
    current files. Only problems a change introduced should refuse it. Problems the business already had, such as records
    an older AURA accepted before a check was tightened, would otherwise block every later save and correction. When the
    change introduced a problem, its files are left as they were before it. The earlier state is checked only when
    something fails, so a clean save costs no more than before."""
    if not errors:return [],[]
    before={Path(path):data for path,data in before.items()}
    after={path:(path.read_bytes() if path.exists() else None) for path in before}
    _put_back(before)
    already=collections.Counter(recheck());introduced=[];existing=[]
    for e in errors:
        if already[e]:already[e]-=1;existing.append(e)
        else:introduced.append(e)
    if not introduced:_put_back(after)
    return introduced,existing


def validate_change(business_id,before,require_context=False):
    """Validate the business after a change to the files in `before`: (introduced, warnings, counts, existing)."""
    errors,warnings,counts=validate_business(business_id,require_context)
    introduced,existing=only_new_problems(errors,before,lambda:validate_business(business_id,require_context)[0])
    if not introduced:
        try:_note_older_problems(business_id,existing)
        except (OSError,ValueError,KeyError,TypeError):pass  # a notice must never cost the person their save
    return introduced,warnings,counts,existing


OLDER_PROBLEMS_KEY='aura-older-record-problems'


def _note_older_problems(business_id,existing):
    """Tell the person once, on Home, when saved records carry problems from before; settle it once a save finds none.
    It is noticed only when a save already ran the check, so opening a business costs nothing extra."""
    from upsert_attention import _id,_path,upsert
    path=_path(business_id,_id(business_id,OLDER_PROBLEMS_KEY))
    if not existing:
        if path.is_file():
            item=json.loads(path.read_text(encoding='utf-8'))
            if item.get('status') in {'open','acknowledged'}:
                from set_attention_status import set_status
                set_status(business_id,item['id'],'resolved',note='A later save found no problems in the saved records.')
        return
    files=sorted({e.split(' ',1)[0] for e in existing if e.startswith('instances')})
    title=('1 saved record needs fixing' if len(files)==1 else f'{len(files)} saved records need fixing') if files else 'Some saved records need fixing'
    upsert(business_id,OLDER_PROBLEMS_KEY,'data_quality','low',title,
           "These records don't pass AURA's checks, probably because an earlier version saved them. They don't block "
           "new saves, but they may be incomplete or out of date. First problem: "+existing[0][:300],
           recommended_action='Ask your AI to look at these records and fix or remove what is wrong.')


def existing_problems(existing):
    """How a write helper reports problems that were already there, so the next step is clear without blocking this one."""
    return {'count':len(existing),'first':existing[:3],
            'note':'These were in the business before this change and did not block it. Fixing them is separate work; '
                   'mention them to the person if they matter to what they asked.'}


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
