#!/usr/bin/env python3
"""Persist explicit organization context with source provenance, not semantic token policing.

The caller/model decides how to normalize supplied organization meaning. AURA preserves
the exact source and authority, validates structure/references/isolation, and requires
literal support for explicit BusinessClaim records because those may authorize outward
claims. General business context is not re-interpreted by a deterministic tokenizer.
"""
from _common import *
from jsonschema import Draft202012Validator
import argparse,json,sys,hashlib

SCHEMA_PATHS={
    'Business':'core/schemas/context/business.schema.json',
    'Market':'core/schemas/context/market.schema.json',
    'Objective':'core/schemas/context/objective.schema.json',
    'ProductService':'core/schemas/context/product-service.schema.json',
    'SourceRecord':'core/schemas/intelligence/source-record.schema.json',
    'BusinessClaim':'core/schemas/context/business-claim.schema.json',
    'Brand':'core/schemas/context/brand.schema.json',
}
# Stable provenance labels for explicit-context capture. They describe how state was
# persisted; they do not grant semantic authority beyond the underlying source provenance.
GROUNDING_METHOD='bootstrap_explicit_context'
GROUNDING_VERSION='2.0'

EXAMPLE_FACTS={
  'industries':['residential HVAC'],
  'markets':['Baltimore area'],
  'services':['installation','repair','maintenance'],
  'objectives':['profitable growth'],
  'lead_sources':['organic search','Google Ads','referrals','repeat customers'],
  'approved_claims':['we provide written estimates'],
  'claim_constraints':['we do not have response-time guarantees'],
  'brand':{
    'voice':{'tone':['plain English','calm','practical']},
    'prohibited_styles':['unsupported hype']
  }
}


def _validate(obj):
    typ=obj.get('object_type');sp=SCHEMA_PATHS.get(typ)
    if not sp:raise ValueError(f'Unsupported bootstrap object type: {typ}')
    schema=json.loads((ROOT/sp).read_text())
    errs=sorted(Draft202012Validator(schema).iter_errors(obj),key=lambda e:list(e.path))
    if errs:raise ValueError('; '.join(f'{list(e.path)} {e.message}' for e in errs))


def _stamp():return now()
def _meta(src):return {'businessos':{'fact_status':'known','authority':'explicit_user','source_ref':src,'grounding_method':GROUNDING_METHOD,'grounding_version':GROUNDING_VERSION}}


def _list(value):
    if value is None:return []
    if isinstance(value,str):return [value]
    if isinstance(value,list):return [str(x) for x in value if x is not None]
    raise ValueError('Fact values must be a string or list of strings')


def _facts_from_mapping(raw):
    if not isinstance(raw,dict):raise ValueError('facts JSON must be an object')
    aliases={
      'industry':'industries','industries':'industries',
      'business_model':'business_models','business_models':'business_models',
      'market':'markets','markets':'markets',
      'service':'services','services':'services',
      'objective':'objectives','objectives':'objectives',
      'lead_source':'lead_sources','lead_sources':'lead_sources',
      'approved_claim':'approved_claims','approved_claims':'approved_claims',
      'claim_constraint':'claim_constraints','claim_constraints':'claim_constraints',
    }
    out={k:[] for k in ['industries','business_models','markets','services','objectives','lead_sources','approved_claims','claim_constraints']};out['brand']=None;unknown=[]
    for key,value in raw.items():
        if key=='brand':
            if value is not None and not isinstance(value,dict):raise ValueError('brand must be a JSON object')
            out['brand']=value;continue
        dest=aliases.get(key)
        if not dest:unknown.append(key);continue
        out[dest].extend(_list(value))
    if unknown:raise ValueError('Unknown facts JSON key(s): '+', '.join(sorted(unknown))+'. Allowed keys: '+', '.join(sorted(list(aliases)+['brand'])))
    return out


def _normalize_brand(brand):
    if brand is None:return None
    claim_fields=sorted({'approved_claims','claims_to_avoid'}&set(brand))
    if claim_fields:raise ValueError('Brand profile claim field(s) '+', '.join(claim_fields)+' belong in BusinessClaim. Supply approved_claims or claim_constraints at the top level so AURA preserves one canonical owner for reusable claim truth.')
    allowed={'name','voice','positioning','visual_identity','content_style','channel_preferences','reference_assets','prohibited_styles','brand_rules'}
    unknown=sorted(set(brand)-allowed)
    if unknown:raise ValueError('Unknown brand key(s): '+', '.join(unknown)+'. Allowed keys: '+', '.join(sorted(allowed)))
    return {k:v for k,v in brand.items() if v not in (None,[],{})}


def _merge_brand_values(left,right,path='brand'):
    if left in (None,{},[]):return right
    if right in (None,{},[]):return left
    if isinstance(left,dict) and isinstance(right,dict):
        out=dict(left)
        for key,value in right.items():out[key]=_merge_brand_values(out.get(key),value,f'{path}.{key}') if key in out else value
        return out
    if isinstance(left,list) and isinstance(right,list):
        out=list(left)
        for value in right:
            if value not in out:out.append(value)
        return out
    if left==right:return left
    raise ValueError(f'Conflicting Brand values at {path}: {left!r} vs {right!r}. Resolve the explicit organization guidance instead of choosing silently.')


def _load_brand_profile_files(paths):
    brand=None;loaded=[]
    for raw in paths or []:
        path=Path(raw);path=path if path.is_absolute() else ROOT/path
        if not path.exists() or not path.is_file():raise ValueError(f'Could not read --brand-profile-file {raw!r}: file not found')
        try:spec=json.loads(path.read_text())
        except Exception as exc:raise ValueError(f'Could not parse --brand-profile-file {raw!r}: {exc}')
        if isinstance(spec,dict) and isinstance(spec.get('brand'),dict):spec=spec['brand']
        if not isinstance(spec,dict):raise ValueError(f'Brand profile manifest {raw!r} must be a JSON object or contain a brand object')
        spec=_normalize_brand(spec)
        if not spec:raise ValueError(f'Brand profile manifest {raw!r} contains no Brand fields')
        brand=_merge_brand_values(brand,spec)
        try:loaded.append(path.resolve().relative_to(ROOT.resolve()).as_posix())
        except Exception:loaded.append(str(path))
    return brand,loaded


def _source_member(reference,text,kind):
    return {'reference':reference,'text':text,'kind':kind,'content_hash':hashlib.sha256(text.encode()).hexdigest()}


def _load_source_members(source_texts=None,source_files=None):
    members=[]
    for i,text in enumerate(source_texts or [],1):
        if text is None:continue
        members.append(_source_member('current user statement' if i==1 else f'current user statement #{i}',str(text),'inline_user_statement'))
    for raw in source_files or []:
        path=Path(raw);path=path if path.is_absolute() else ROOT/path
        if not path.exists() or not path.is_file():raise ValueError(f'Could not read --source-file {raw!r}: file not found')
        raw_bytes=path.read_bytes();text=raw_bytes.decode('utf-8')
        try:ref=path.resolve().relative_to(ROOT.resolve()).as_posix()
        except Exception:ref=str(path)
        member=_source_member(ref,text,'user_supplied_file');member['content_hash']=hashlib.sha256(raw_bytes).hexdigest();members.append(member)
    if not members:raise ValueError('Explicit-user context persistence requires at least one --source-text or --source-file source.')
    return members


def _source_records(business_id,ts,token,members,source_reference=None):
    baseid=f'src_{business_id}_explicit_{token}'
    if len(members)==1:
        member=members[0]
        return [{
          'id':baseid,'object_type':'SourceRecord','schema_version':'1.0.0','business_id':business_id,
          'created_at':ts,'updated_at':ts,'lineage':[],'source_type':'user_statement' if member['kind']=='inline_user_statement' else 'user_supplied_file',
          'source_reference':source_reference or member['reference'],'origin':'active user conversation' if member['kind']=='inline_user_statement' else 'user-provided local file',
          'retrieved_at':ts,'published_at':None,'content_hash':member['content_hash'],'access_scope':'business-private',
          'extensions':{'authority':'explicit_user','grounding_method':GROUNDING_METHOD,'grounding_version':GROUNDING_VERSION,'verbatim_user_statement':member['text'],
                        'source_members':[{'reference':member['reference'],'content_hash':member['content_hash'],'kind':member['kind']}]}
        }],baseid,member['text']
    records=[];member_ids=[]
    for i,member in enumerate(members,1):
        mid=f'{baseid}_{i}';member_ids.append(mid)
        records.append({
          'id':mid,'object_type':'SourceRecord','schema_version':'1.0.0','business_id':business_id,
          'created_at':ts,'updated_at':ts,'lineage':[],'source_type':'user_statement' if member['kind']=='inline_user_statement' else 'user_supplied_file',
          'source_reference':member['reference'],'origin':'active user conversation' if member['kind']=='inline_user_statement' else 'user-provided local file',
          'retrieved_at':ts,'published_at':None,'content_hash':member['content_hash'],'access_scope':'business-private',
          'extensions':{'authority':'explicit_user','grounding_method':GROUNDING_METHOD,'grounding_version':GROUNDING_VERSION,'verbatim_user_statement':member['text']}
        })
    combined='\n\n'.join(f'--- SOURCE: {member["reference"]} ---\n{member["text"]}' for member in members)
    records.append({
      'id':baseid,'object_type':'SourceRecord','schema_version':'1.0.0','business_id':business_id,
      'created_at':ts,'updated_at':ts,'lineage':member_ids,'source_type':'user_supplied_source_bundle',
      'source_reference':source_reference or f'{len(members)} user-supplied onboarding sources','origin':'user-provided onboarding source bundle',
      'retrieved_at':ts,'published_at':None,'content_hash':hashlib.sha256(combined.encode()).hexdigest(),'access_scope':'business-private',
      'extensions':{'authority':'explicit_user','grounding_method':GROUNDING_METHOD,'grounding_version':GROUNDING_VERSION,'verbatim_user_statement':combined,
                    'source_members':[{'source_ref':rid,'reference':member['reference'],'content_hash':member['content_hash'],'kind':member['kind']} for rid,member in zip(member_ids,members)]}
    })
    return records,baseid,combined


def _load_facts(facts_json=None,facts_file=None,facts_stdin=False):
    sources=sum(bool(x) for x in [facts_json,facts_file,facts_stdin])
    if sources>1:raise ValueError('Use only one of --facts-json, --facts-file, or --facts-stdin')
    if not sources:
        out={k:[] for k in ['industries','business_models','markets','services','objectives','lead_sources','approved_claims','claim_constraints']};out['brand']=None;return out
    if facts_file:
        try:raw=json.loads(Path(facts_file).read_text())
        except Exception as exc:raise ValueError(f'Could not read --facts-file {facts_file!r}: {exc}')
    elif facts_stdin:
        try:raw=json.load(sys.stdin)
        except Exception as exc:raise ValueError(f'Could not parse JSON from stdin: {exc}')
    else:
        try:raw=json.loads(facts_json)
        except Exception as exc:raise ValueError(f'Could not parse --facts-json: {exc}')
    return _facts_from_mapping(raw)


def _literal_claim_quote(statement,source_text,label):
    normalized_statement=re.sub(r'\s+',' ',statement).strip().lower();normalized_source=re.sub(r'\s+',' ',source_text).strip().lower()
    if normalized_statement not in normalized_source:
        raise ValueError(f'Explicit {label} must be a literal source-supported statement because it can authorize outward business claims. Preserve the exact supported wording or store a non-claim interpretation through the appropriate context/evidence type: {statement!r}')
    return statement


def build_objects(business_id,industries=None,business_models=None,markets=None,services=None,objectives=None,lead_sources=None,approved_claims=None,claim_constraints=None,brand=None,source_reference=None,source_text=None,source_members=None):
    base=ROOT/'instances'/business_id
    if not base.exists():raise ValueError(f'Unknown business: {business_id}; initialize it first with: python3 scripts/init_business.py {business_id} --name "Business Name"')
    inst=json.loads((base/'instance.json').read_text());name=inst.get('name') or business_id
    industries=[str(x).strip() for x in (industries or []) if str(x).strip()];business_models=[str(x).strip() for x in (business_models or []) if str(x).strip()]
    markets=[str(x).strip() for x in (markets or []) if str(x).strip()]
    services=[part.strip() for x in (services or []) if x for part in str(x).split(',') if part.strip()]
    objectives=[str(x).strip() for x in (objectives or []) if str(x).strip()]
    lead_sources=[part.strip() for x in (lead_sources or []) if x for part in str(x).split(',') if part.strip()]
    approved_claims=[str(x).strip() for x in (approved_claims or []) if str(x).strip()]
    claim_constraints=[str(x).strip() for x in (claim_constraints or []) if str(x).strip()]
    brand=_normalize_brand(brand)
    if not any([industries,business_models,markets,services,objectives,lead_sources,approved_claims,claim_constraints,brand]):
        raise ValueError('No structured facts supplied. Source material provides provenance; the caller/model supplies the structured interpretation. Run --help for an example.')
    ts=_stamp();token=re.sub(r'[^0-9]','',ts)[:20]
    if source_members:source_records,srcid,source_text_full=_source_records(business_id,ts,token,source_members,source_reference)
    else:
        if not source_text:raise ValueError('Explicit-user context persistence requires --source-text or --source-file with the authoritative source material.')
        source_records,srcid,source_text_full=_source_records(business_id,ts,token,[_source_member(source_reference or 'current user statement',source_text,'inline_user_statement')],source_reference)

    # General context may be conservatively/semantically normalized by the capable model.
    # BusinessClaim is different: it may authorize outward language, so exact support stays literal.
    for statement in approved_claims:_literal_claim_quote(statement,source_text_full,'approved claim')
    for statement in claim_constraints:_literal_claim_quote(statement,source_text_full,'claim constraint')

    for src in source_records:
        if src['id']==srcid:
            src['extensions']['captured_fact_categories']=[key for key,value in [('industry',industries),('business_model',business_models),('market',markets),('service',services),('objective',objectives),('lead_source',lead_sources),('approved_claim',approved_claims),('claim_constraint',claim_constraints),('brand',brand)] if value]
    objs=list(source_records)
    biz={'id':f'biz_{business_id}','object_type':'Business','schema_version':'1.0.0','business_id':business_id,'created_at':ts,'updated_at':ts,'lineage':[srcid],'name':name}
    if business_models:biz['business_models']=business_models
    if industries:biz['industries']=industries
    ext=_meta(srcid)
    if lead_sources:ext['lead_sources']=lead_sources
    biz['extensions']=ext;objs.append(biz)
    if brand:
        b={'id':f'brd_{business_id}','object_type':'Brand','schema_version':'1.0.0','business_id':business_id,'created_at':ts,'updated_at':ts,'lineage':[srcid],'name':brand.get('name') or name}
        for key in ['voice','positioning','visual_identity','content_style','channel_preferences','reference_assets','prohibited_styles','brand_rules']:
            if key in brand:b[key]=brand[key]
        b['extensions']={'businessos':{'fact_status':'known','authority':'explicit_user','source_ref':srcid,'grounding_method':GROUNDING_METHOD,'grounding_version':GROUNDING_VERSION,'explicit_brand_profile':True}}
        objs.append(b)
    for market in markets:
        sid=slug(market) or 'market';objs.append({'id':f'mkt_{business_id}_{sid}','object_type':'Market','schema_version':'1.0.0','business_id':business_id,'created_at':ts,'updated_at':ts,'lineage':[srcid],'name':market,'geography':market,'extensions':_meta(srcid)})
    for service in services:
        sid=slug(service) or 'service';objs.append({'id':f'prd_{business_id}_{sid}','object_type':'ProductService','schema_version':'1.0.0','business_id':business_id,'created_at':ts,'updated_at':ts,'lineage':[srcid],'name':service,'kind':'service','description':service,'extensions':_meta(srcid)})
    for i,objective in enumerate(objectives,1):
        sid=slug(objective) or f'objective-{i}';objs.append({'id':f'obj_{business_id}_{sid}','object_type':'Objective','schema_version':'1.0.0','business_id':business_id,'created_at':ts,'updated_at':ts,'lineage':[srcid],'name':objective,'extensions':_meta(srcid)})
    for i,statement in enumerate(approved_claims,1):
        sid=slug(statement)[:48].rstrip('-_') or f'approved-{i}'
        objs.append({'id':f'clm_{business_id}_{sid}','object_type':'BusinessClaim','schema_version':'1.0.0','business_id':business_id,'created_at':ts,'updated_at':ts,'lineage':[srcid],'statement':statement,'claim_kind':'approved_business_claim','status':'approved','authority':'explicit_user','source_ref':srcid,'support_quote':statement,'extensions':_meta(srcid)})
    for i,statement in enumerate(claim_constraints,1):
        sid=slug(statement)[:48].rstrip('-_') or f'constraint-{i}'
        objs.append({'id':f'clm_{business_id}_constraint-{sid}','object_type':'BusinessClaim','schema_version':'1.0.0','business_id':business_id,'created_at':ts,'updated_at':ts,'lineage':[srcid],'statement':statement,'claim_kind':'constraint','status':'approved','authority':'explicit_user','source_ref':srcid,'support_quote':statement,'extensions':_meta(srcid)})
    for obj in objs:_validate(obj)
    return objs


def _path(base,obj):
    typ=obj['object_type'];oid=obj['id']
    if typ=='SourceRecord':return base/'intelligence/sources'/f'{oid}.json'
    if typ=='Business':return base/'context/business.json'
    if typ=='Market':return base/'context/markets'/f'{oid}.json'
    if typ=='ProductService':return base/'context/products'/f'{oid}.json'
    if typ=='Objective':return base/'context/objectives'/f'{oid}.json'
    if typ=='BusinessClaim':return base/'context/claims'/f'{oid}.json'
    if typ=='Brand':return base/'context/brand'/f'{oid}.json'
    raise ValueError(typ)


def _merge_existing_business(existing,incoming):
    if existing.get('object_type')!='Business' or existing.get('id')!=incoming.get('id') or existing.get('business_id')!=incoming.get('business_id'):
        raise ValueError('Existing canonical Business identity does not match the context target.')
    if existing.get('name')!=incoming.get('name'):
        raise ValueError(f"Existing Business name {existing.get('name')!r} conflicts with initialization name {incoming.get('name')!r}; resolve organization identity explicitly instead of overwriting it.")
    out=dict(existing);out['updated_at']=incoming['updated_at'];out['lineage']=list(dict.fromkeys([*(existing.get('lineage') or []),*(incoming.get('lineage') or [])]))
    for key in ('business_models','industries'):
        values=list(dict.fromkeys([*(existing.get(key) or []),*(incoming.get(key) or [])]))
        if values:out[key]=values
    ext=dict(existing.get('extensions') or {});incoming_ext=incoming.get('extensions') or {}
    for key,value in incoming_ext.items():
        if key=='businessos' and isinstance(value,dict):
            bos=dict(ext.get('businessos') or {});bos.update(value);ext['businessos']=bos
        elif key=='lead_sources':ext[key]=list(dict.fromkeys([*(ext.get(key) or []),*(value or [])]))
        else:ext[key]=value
    if ext:out['extensions']=ext
    _validate(out);return out


def persist_explicit_context(business_id,**kwargs):
    objs=build_objects(business_id,**kwargs);base=ROOT/'instances'/business_id;paths=[_path(base,obj) for obj in objs];blocked=[]
    for i,(obj,path) in enumerate(zip(objs,paths)):
        if not path.exists():continue
        if obj.get('object_type')=='Business':
            objs[i]=_merge_existing_business(json.loads(path.read_text()),obj);continue
        blocked.append(path.relative_to(ROOT).as_posix())
    if blocked:raise FileExistsError('Refusing to overwrite existing canonical context object(s): '+', '.join(blocked)+'. Update current context through its supported update path instead of silently replacing it.')
    for obj,path in zip(objs,paths):write_json_atomic(path,obj)
    return objs,paths


def _merge_lists(*groups):
    out=[]
    for group in groups:
        for item in group or []:
            if item not in out:out.append(item)
    return out


def main():
    epilog='''Recommended conversational intake:
  1) Initialize the organization once with `scripts/init_business.py`; the organization name alone is enough canonical context.
  2) Preserve exact user/first-party source material, then let the capable model structure only the meaning it can support. AURA validates provenance and structure; it does not use keyword overlap as semantic authority.
  3) Explicit outward BusinessClaim/constraint wording must remain literally supported by the supplied source.
  4) Continue the user's actual request normally after context persistence. Setup is not a routing gate.

Example facts JSON:
'''+json.dumps(EXAMPLE_FACTS,indent=2)+'''

Repeat --source-file for multi-source onboarding; AURA preserves each member reference/hash. Explicit organization-level brand/voice/style instructions belong in Brand state; reusable claims, promises, claim constraints, and prohibitions belong in BusinessClaim. Reusable work/output preferences belong in PreferenceProfile state. Current task/action boundaries remain part of the user's request and real harness/account/legal constraints; do not turn them into AURA approval machinery or reusable preferences unless the organization explicitly intends them to persist.'''
    ap=argparse.ArgumentParser(description='Persist explicit user/first-party organization context with exact source provenance. The model supplies semantic interpretation; AURA validates structure and literal outward claims.',formatter_class=argparse.RawDescriptionHelpFormatter,epilog=epilog)
    ap.add_argument('business_id',nargs='?');ap.add_argument('--business-id',dest='business_id_alias')
    ap.add_argument('--facts-json');ap.add_argument('--facts-file');ap.add_argument('--facts-stdin',action='store_true')
    ap.add_argument('--industry',action='append',default=[]);ap.add_argument('--business-model',action='append',default=[])
    ap.add_argument('--market',action='append',default=[]);ap.add_argument('--service',action='append',default=[])
    ap.add_argument('--objective',action='append',default=[]);ap.add_argument('--lead-source',action='append',default=[])
    ap.add_argument('--approved-claim',action='append',default=[]);ap.add_argument('--claim-constraint',action='append',default=[])
    ap.add_argument('--source-reference');ap.add_argument('--source-text',action='append',default=[]);ap.add_argument('--source-file',action='append',default=[])
    ap.add_argument('--brand-profile-file',action='append',default=[]);ap.add_argument('--preference-profile-file',action='append',default=[])
    a=ap.parse_args();business_id=a.business_id or a.business_id_alias
    if a.business_id and a.business_id_alias and a.business_id!=a.business_id_alias:ap.error('positional business_id and --business-id disagree')
    if not business_id:ap.error('business_id is required (positional or --business-id)')
    try:
        source_members=_load_source_members(a.source_text,a.source_file);jf=_load_facts(a.facts_json,a.facts_file,a.facts_stdin)
        brand_manifest,brand_profile_files=_load_brand_profile_files(a.brand_profile_file);merged_brand=_merge_brand_values(jf.get('brand'),brand_manifest)
        facts={
          'industries':_merge_lists(jf['industries'],a.industry),'business_models':_merge_lists(jf['business_models'],a.business_model),
          'markets':_merge_lists(jf['markets'],a.market),'services':_merge_lists(jf['services'],a.service),
          'objectives':_merge_lists(jf['objectives'],a.objective),'lead_sources':_merge_lists(jf['lead_sources'],a.lead_source),
          'approved_claims':_merge_lists(jf['approved_claims'],a.approved_claim),'claim_constraints':_merge_lists(jf['claim_constraints'],a.claim_constraint),
          'brand':merged_brand,
        }
        objs,paths=persist_explicit_context(business_id,**facts,source_reference=a.source_reference,source_members=source_members)
    except (ValueError,FileExistsError) as exc:raise SystemExit(str(exc)+'\nSupported path: run `python3 scripts/bootstrap_explicit_context.py --help`; do not hand-author replacement canonical state.')

    preference_written=[]
    if a.preference_profile_file:
        from upsert_preference_profile import upsert as upsert_preference
        canonical_source=next((obj['id'] for obj in reversed(objs) if obj.get('object_type')=='SourceRecord' and (obj.get('extensions') or {}).get('captured_fact_categories') is not None),None)
        for raw in a.preference_profile_file:
            path=Path(raw);path=path if path.is_absolute() else ROOT/path
            try:spec=json.loads(path.read_text())
            except Exception as exc:raise SystemExit(f'Could not read --preference-profile-file {raw!r}: {exc}')
            if not isinstance(spec,dict) or not isinstance(spec.get('preferences'),dict):raise SystemExit(f'Preference profile manifest {raw!r} must be a JSON object with a preferences object')
            applies=spec.get('applies_to') or {}
            try:
                p,obj=upsert_preference(business_id,spec.get('name') or 'Onboarding preferences',spec.get('scope') or 'operator',spec.get('subject_ref'),spec['preferences'],spec.get('id'),int(spec.get('priority',0)),spec.get('source_kind') or 'explicit_user',spec.get('source_refs') or ([canonical_source] if canonical_source else []),applies.get('systems') or [],applies.get('workflows') or [],applies.get('output_types') or [],applies.get('channels') or [],spec.get('notes'))
            except Exception as exc:raise SystemExit(f'Could not persist preference profile {raw!r}: {exc}')
            preference_written.append({'id':obj['id'],'scope':obj['scope'],'subject_ref':obj['subject_ref'],'path':p.relative_to(ROOT).as_posix()})

    payload={
      'business_id':business_id,'objects_written':[{'id':obj['id'],'object_type':obj['object_type'],'path':path.relative_to(ROOT).as_posix()} for obj,path in zip(objs,paths)],
      'preference_profiles_written':preference_written,'brand_profile_files_used':brand_profile_files,
      'truth_rule':'source provenance is preserved; semantic interpretation belongs to the capable model; explicit outward BusinessClaim wording remains literal-source-bounded',
      'validation_required':f'python3 scripts/validate_business.py {business_id} --require-context','completion_state':'context_persisted',
      'required_next_action':'Validate active organization state, then continue the user\'s actual request using model judgment and the host\'s real capabilities.'
    }
    print(json.dumps(payload,indent=2))


if __name__=='__main__':main()