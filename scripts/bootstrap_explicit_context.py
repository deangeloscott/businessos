#!/usr/bin/env python3
from _common import *
from jsonschema import Draft202012Validator
import argparse,json,datetime,sys,hashlib

SCHEMA_PATHS={
    'Business':'core/schemas/context/business.schema.json',
    'Market':'core/schemas/context/market.schema.json',
    'Objective':'core/schemas/context/objective.schema.json',
    'ProductService':'core/schemas/context/product-service.schema.json',
    'SourceRecord':'core/schemas/intelligence/source-record.schema.json',
    'BusinessClaim':'core/schemas/context/business-claim.schema.json',
    'Brand':'core/schemas/context/brand.schema.json',
}
GROUNDING_METHOD='bootstrap_explicit_context'
GROUNDING_VERSION='1.0'

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
    typ=obj.get('object_type'); sp=SCHEMA_PATHS.get(typ)
    if not sp: raise ValueError(f'Unsupported bootstrap object type: {typ}')
    schema=json.loads((ROOT/sp).read_text())
    errs=sorted(Draft202012Validator(schema).iter_errors(obj),key=lambda e:list(e.path))
    if errs: raise ValueError('; '.join(f'{list(e.path)} {e.message}' for e in errs))

def _stamp(): return now()
def _meta(src): return {'businessos':{'fact_status':'known','authority':'explicit_user','source_ref':src,'grounding_method':GROUNDING_METHOD,'grounding_version':GROUNDING_VERSION}}

def _fact_tokens(text):
    stop={'a','an','and','the','of','for','to','in','on','our','my','we','from','through','with','company','business'}
    toks=[]
    aliases={'maintenance':'maintain','maintaining':'maintain','installation':'install','installing':'install','repairs':'repair','repairing':'repair'}
    for raw in re.findall(r'[a-z0-9]+', (text or '').lower()):
        if raw in stop: continue
        if raw in aliases:
            toks.append(aliases[raw]); continue
        t=raw
        for suf,repl in [('ations',''),('ation',''),('ing',''),('ed',''),('ies','y'),('s','')]:
            if len(t)>len(suf)+2 and t.endswith(suf):
                t=t[:-len(suf)]+repl; break
        toks.append(t)
    return set(toks)

def _assert_grounded(values, source_text, label):
    if not source_text: return
    source=_fact_tokens(source_text)
    for value in values:
        missing=sorted(_fact_tokens(value)-source)
        if missing:
            raise ValueError(f'Unsupported {label} for explicit-user bootstrap: {value!r}; token(s) not grounded in source text: {", ".join(missing)}. Omit inferred expansion or store it as provisional evidence instead.')

def _list(v):
    if v is None: return []
    if isinstance(v,str): return [v]
    if isinstance(v,list): return [str(x) for x in v if x is not None]
    raise ValueError('Fact values must be a string or list of strings')

def _facts_from_mapping(raw):
    if not isinstance(raw,dict): raise ValueError('facts JSON must be an object')
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
    out={k:[] for k in ['industries','business_models','markets','services','objectives','lead_sources','approved_claims','claim_constraints']}
    out['brand']=None
    unknown=[]
    for k,v in raw.items():
        if k=='brand':
            if v is not None and not isinstance(v,dict): raise ValueError('brand must be a JSON object')
            out['brand']=v
            continue
        dest=aliases.get(k)
        if not dest: unknown.append(k); continue
        out[dest].extend(_list(v))
    if unknown: raise ValueError('Unknown facts JSON key(s): '+', '.join(sorted(unknown))+'. Allowed keys: '+', '.join(sorted(list(aliases)+['brand'])))
    return out

def _brand_strings(value,prefix='brand'):
    if value is None:
        return
    if isinstance(value,str):
        if value.strip(): yield value.strip(),prefix
    elif isinstance(value,list):
        for i,x in enumerate(value):
            yield from _brand_strings(x,f'{prefix}[{i}]')
    elif isinstance(value,dict):
        for k,v in value.items():
            yield from _brand_strings(v,f'{prefix}.{k}')
    elif isinstance(value,(int,float,bool)):
        yield str(value),prefix

def _normalize_brand(brand):
    if brand is None:return None
    allowed={'name','voice','positioning','visual_identity','content_style','channel_preferences','reference_assets','prohibited_styles','brand_rules','approved_claims','claims_to_avoid'}
    unknown=sorted(set(brand)-allowed)
    if unknown: raise ValueError('Unknown brand key(s): '+', '.join(unknown)+'. Allowed keys: '+', '.join(sorted(allowed)))
    return {k:v for k,v in brand.items() if v not in (None,[],{})}


def _merge_brand_values(left,right,path='brand'):
    if left in (None,{},[]): return right
    if right in (None,{},[]): return left
    if isinstance(left,dict) and isinstance(right,dict):
        out=dict(left)
        for k,v in right.items():
            out[k]=_merge_brand_values(out.get(k),v,f'{path}.{k}') if k in out else v
        return out
    if isinstance(left,list) and isinstance(right,list):
        out=list(left)
        for v in right:
            if v not in out: out.append(v)
        return out
    if left==right:return left
    raise ValueError(f'Conflicting Brand values at {path}: {left!r} vs {right!r}. Resolve the explicit organization guidance instead of choosing silently.')


def _load_brand_profile_files(paths):
    brand=None
    loaded=[]
    for raw in paths or []:
        p=Path(raw);p=p if p.is_absolute() else ROOT/p
        if not p.exists() or not p.is_file(): raise ValueError(f'Could not read --brand-profile-file {raw!r}: file not found')
        try: spec=json.loads(p.read_text())
        except Exception as e: raise ValueError(f'Could not parse --brand-profile-file {raw!r}: {e}')
        if isinstance(spec,dict) and isinstance(spec.get('brand'),dict): spec=spec['brand']
        if not isinstance(spec,dict): raise ValueError(f'Brand profile manifest {raw!r} must be a JSON object or contain a brand object')
        spec=_normalize_brand(spec)
        if not spec: raise ValueError(f'Brand profile manifest {raw!r} contains no Brand fields')
        brand=_merge_brand_values(brand,spec)
        try: loaded.append(p.resolve().relative_to(ROOT.resolve()).as_posix())
        except Exception: loaded.append(str(p))
    return brand,loaded

def _source_member(reference,text,kind):
    return {'reference':reference,'text':text,'kind':kind,'content_hash':hashlib.sha256(text.encode()).hexdigest()}

def _load_source_members(source_texts=None,source_files=None):
    members=[]
    for i,txt in enumerate(source_texts or [],1):
        if txt is None: continue
        members.append(_source_member('current user statement' if i==1 else f'current user statement #{i}',str(txt),'inline_user_statement'))
    for raw in source_files or []:
        fp=Path(raw); fp=fp if fp.is_absolute() else ROOT/fp
        if not fp.exists() or not fp.is_file(): raise ValueError(f'Could not read --source-file {raw!r}: file not found')
        raw_bytes=fp.read_bytes();txt=raw_bytes.decode('utf-8')
        try: ref=fp.resolve().relative_to(ROOT.resolve()).as_posix()
        except Exception: ref=str(fp)
        member=_source_member(ref,txt,'user_supplied_file')
        member['content_hash']=hashlib.sha256(raw_bytes).hexdigest()
        members.append(member)
    if not members: raise ValueError('Explicit-user bootstrap requires at least one --source-text or --source-file grounding source.')
    return members

def _source_records(business_id,ts,token,members,source_reference=None):
    baseid=f'src_{business_id}_explicit_{token}'
    if len(members)==1:
        m=members[0]
        return [{
          'id':baseid,'object_type':'SourceRecord','schema_version':'1.0.0','business_id':business_id,
          'created_at':ts,'updated_at':ts,'lineage':[],'source_type':'user_statement' if m['kind']=='inline_user_statement' else 'user_supplied_file',
          'source_reference':source_reference or m['reference'],'origin':'active user conversation' if m['kind']=='inline_user_statement' else 'user-provided local file',
          'retrieved_at':ts,'published_at':None,'content_hash':m['content_hash'],'access_scope':'business-private',
          'extensions':{'authority':'explicit_user','grounding_method':GROUNDING_METHOD,'grounding_version':GROUNDING_VERSION,'verbatim_user_statement':m['text'],
                        'source_members':[{'reference':m['reference'],'content_hash':m['content_hash'],'kind':m['kind']}]}
        }],baseid,m['text']
    records=[]; member_ids=[]
    for i,m in enumerate(members,1):
        mid=f'{baseid}_{i}'
        member_ids.append(mid)
        records.append({
          'id':mid,'object_type':'SourceRecord','schema_version':'1.0.0','business_id':business_id,
          'created_at':ts,'updated_at':ts,'lineage':[],'source_type':'user_statement' if m['kind']=='inline_user_statement' else 'user_supplied_file',
          'source_reference':m['reference'],'origin':'active user conversation' if m['kind']=='inline_user_statement' else 'user-provided local file',
          'retrieved_at':ts,'published_at':None,'content_hash':m['content_hash'],'access_scope':'business-private',
          'extensions':{'authority':'explicit_user','grounding_method':GROUNDING_METHOD,'grounding_version':GROUNDING_VERSION,'verbatim_user_statement':m['text']}
        })
    combined='\n\n'.join(f'--- SOURCE: {m["reference"]} ---\n{m["text"]}' for m in members)
    records.append({
      'id':baseid,'object_type':'SourceRecord','schema_version':'1.0.0','business_id':business_id,
      'created_at':ts,'updated_at':ts,'lineage':member_ids,'source_type':'user_supplied_source_bundle',
      'source_reference':source_reference or f'{len(members)} user-supplied onboarding sources',
      'origin':'user-provided onboarding source bundle','retrieved_at':ts,'published_at':None,
      'content_hash':hashlib.sha256(combined.encode()).hexdigest(),'access_scope':'business-private',
      'extensions':{'authority':'explicit_user','grounding_method':GROUNDING_METHOD,'grounding_version':GROUNDING_VERSION,
                    'verbatim_user_statement':combined,
                    'source_members':[{'source_ref':rid,'reference':m['reference'],'content_hash':m['content_hash'],'kind':m['kind']} for rid,m in zip(member_ids,members)]}
    })
    return records,baseid,combined

def _load_facts(facts_json=None,facts_file=None,facts_stdin=False):
    sources=sum(bool(x) for x in [facts_json,facts_file,facts_stdin])
    if sources>1: raise ValueError('Use only one of --facts-json, --facts-file, or --facts-stdin')
    if not sources:
        out={k:[] for k in ['industries','business_models','markets','services','objectives','lead_sources','approved_claims','claim_constraints']};out['brand']=None;return out
    if facts_file:
        try: raw=json.loads(Path(facts_file).read_text())
        except Exception as e: raise ValueError(f'Could not read --facts-file {facts_file!r}: {e}')
    elif facts_stdin:
        try: raw=json.load(sys.stdin)
        except Exception as e: raise ValueError(f'Could not parse JSON from stdin: {e}')
    else:
        try: raw=json.loads(facts_json)
        except Exception as e: raise ValueError(f'Could not parse --facts-json: {e}')
    return _facts_from_mapping(raw)

def build_objects(business_id, industries=None, business_models=None, markets=None, services=None, objectives=None, lead_sources=None, approved_claims=None, claim_constraints=None, brand=None, source_reference=None, source_text=None, source_members=None):
    base=ROOT/'instances'/business_id
    if not base.exists(): raise ValueError(f'Unknown business: {business_id}; initialize it first with: python3 scripts/init_business.py {business_id} --name "Business Name"')
    inst=json.loads((base/'instance.json').read_text()); name=inst.get('name') or business_id
    industries=[x.strip() for x in (industries or []) if str(x).strip()]; business_models=[x.strip() for x in (business_models or []) if str(x).strip()]
    markets=[x.strip() for x in (markets or []) if str(x).strip()]
    services=[part.strip() for x in (services or []) if x for part in str(x).split(',') if part.strip()]
    objectives=[x.strip() for x in (objectives or []) if str(x).strip()]
    lead_sources=[part.strip() for x in (lead_sources or []) if x for part in str(x).split(',') if part.strip()]
    approved_claims=[x.strip() for x in (approved_claims or []) if str(x).strip()]
    claim_constraints=[x.strip() for x in (claim_constraints or []) if str(x).strip()]
    brand=_normalize_brand(brand)
    if not any([industries,business_models,markets,services,objectives,lead_sources,approved_claims,claim_constraints,brand]):
        raise ValueError('No structured facts supplied. Use --facts-file/--facts-json/--facts-stdin or documented fact flags. Source text provides provenance; it does not auto-infer structured business facts. Run --help for an example.')
    ts=_stamp(); token=re.sub(r'[^0-9]','',ts)[:14]
    if source_members:
        source_records,srcid,grounding_text=_source_records(business_id,ts,token,source_members,source_reference)
    else:
        if not source_text:
            raise ValueError('Explicit-user bootstrap requires --source-text or --source-file with the verbatim/authoritative statement grounding the structured facts.')
        source_records,srcid,grounding_text=_source_records(business_id,ts,token,[_source_member(source_reference or 'current user statement',source_text,'inline_user_statement')],source_reference)
    for vals,label in [(industries,'industry'),(business_models,'business model'),(markets,'market'),(services,'service'),(objectives,'objective'),(lead_sources,'lead source'),(approved_claims,'approved claim'),(claim_constraints,'claim constraint')]: _assert_grounded(vals,grounding_text,label)
    if brand:
        for value,label in _brand_strings(brand):
            _assert_grounded([value],grounding_text,label)
    for src in source_records:
        if src['id']==srcid:
            src['extensions']['captured_fact_categories']=[k for k,v in [('industry',industries),('business_model',business_models),('market',markets),('service',services),('objective',objectives),('lead_source',lead_sources),('approved_claim',approved_claims),('claim_constraint',claim_constraints),('brand',brand)] if v]
    objs=list(source_records)
    biz={'id':f'biz_{business_id}','object_type':'Business','schema_version':'1.0.0','business_id':business_id,'created_at':ts,'updated_at':ts,'lineage':[srcid],'name':name}
    if business_models: biz['business_models']=business_models
    if industries: biz['industries']=industries
    ext=_meta(srcid)
    if lead_sources: ext['lead_sources']=lead_sources
    biz['extensions']=ext; objs.append(biz)
    if brand:
        b={'id':f'brd_{business_id}','object_type':'Brand','schema_version':'1.0.0','business_id':business_id,'created_at':ts,'updated_at':ts,
           'lineage':[srcid],'name':brand.get('name') or name}
        for k in ['voice','positioning','visual_identity','content_style','channel_preferences','reference_assets','prohibited_styles','brand_rules','approved_claims','claims_to_avoid']:
            if k in brand:b[k]=brand[k]
        b['extensions']={'businessos':{'fact_status':'known','authority':'explicit_user','source_ref':srcid,'grounding_method':GROUNDING_METHOD,'grounding_version':GROUNDING_VERSION,'explicit_brand_profile':True}}
        objs.append(b)
    for m in markets:
        sid=slug(m) or 'market'; objs.append({'id':f'mkt_{business_id}_{sid}','object_type':'Market','schema_version':'1.0.0','business_id':business_id,'created_at':ts,'updated_at':ts,'lineage':[srcid],'name':m,'geography':m,'extensions':_meta(srcid)})
    for svc in services:
        sid=slug(svc) or 'service'; objs.append({'id':f'prd_{business_id}_{sid}','object_type':'ProductService','schema_version':'1.0.0','business_id':business_id,'created_at':ts,'updated_at':ts,'lineage':[srcid],'name':svc,'kind':'service','description':svc,'extensions':_meta(srcid)})
    for i,objname in enumerate(objectives,1):
        sid=slug(objname) or f'objective-{i}'; objs.append({'id':f'obj_{business_id}_{sid}','object_type':'Objective','schema_version':'1.0.0','business_id':business_id,'created_at':ts,'updated_at':ts,'lineage':[srcid],'name':objname,'priority':i,'extensions':_meta(srcid)})
    for i,statement in enumerate(approved_claims,1):
        sid=slug(statement)[:48].rstrip('-_') or f'approved-{i}'
        objs.append({'id':f'clm_{business_id}_{sid}','object_type':'BusinessClaim','schema_version':'1.0.0','business_id':business_id,'created_at':ts,'updated_at':ts,'lineage':[srcid],'statement':statement,'claim_kind':'approved_business_claim','status':'approved','authority':'explicit_user','source_ref':srcid,'support_quote':statement,'extensions':_meta(srcid)})
    for i,statement in enumerate(claim_constraints,1):
        sid=slug(statement)[:48].rstrip('-_') or f'constraint-{i}'
        objs.append({'id':f'clm_{business_id}_constraint-{sid}','object_type':'BusinessClaim','schema_version':'1.0.0','business_id':business_id,'created_at':ts,'updated_at':ts,'lineage':[srcid],'statement':statement,'claim_kind':'constraint','status':'approved','authority':'explicit_user','source_ref':srcid,'support_quote':statement,'extensions':_meta(srcid)})
    for o in objs: _validate(o)
    return objs

def _path(base,obj):
    typ=obj['object_type']; oid=obj['id']
    if typ=='SourceRecord': return base/'intelligence/sources'/f'{oid}.json'
    if typ=='Business': return base/'context/business.json'
    if typ=='Market': return base/'context/markets'/f'{oid}.json'
    if typ=='ProductService': return base/'context/products'/f'{oid}.json'
    if typ=='Objective': return base/'context/objectives'/f'{oid}.json'
    if typ=='BusinessClaim': return base/'context/claims'/f'{oid}.json'
    if typ=='Brand': return base/'context/brand'/f'{oid}.json'
    raise ValueError(typ)

def persist_explicit_context(business_id, **kwargs):
    objs=build_objects(business_id,**kwargs); base=ROOT/'instances'/business_id
    paths=[_path(base,o) for o in objs]
    existing=[p.relative_to(ROOT).as_posix() for p in paths if p.exists()]
    if existing: raise FileExistsError('Refusing to overwrite existing canonical bootstrap object(s): '+', '.join(existing))
    for o,p in zip(objs,paths): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(o,indent=2)+'\n')
    return objs,paths

def _merge_lists(*groups):
    out=[]
    for g in groups:
        for x in (g or []):
            if x not in out: out.append(x)
    return out

def main():
    epilog='''Recommended conversational intake:
  1) Write a small facts JSON file in runtime/ or another temporary work path.
  2) Preserve the user's complete original request. If anything remains after setup, pass that remaining natural-language outcome with --residual-request.
  3) Run:
     python3 scripts/bootstrap_explicit_context.py northstar-hvac --facts-file runtime/northstar-facts.json --source-file supplied/business-overview.md --source-file supplied/brand-notes.md --brand-profile-file runtime/brand-profile.json --preference-profile-file runtime/operator-preferences.json --residual-request "determine what we should do next"

If the user requested initialization only, use --initialization-only instead of --residual-request.

Example facts JSON:
'''+json.dumps(EXAMPLE_FACTS,indent=2)+'''

The business ID is normally positional. --business-id is accepted as an agent-friendly alias. Repeat --source-file for multi-source onboarding instead of manually merging supplied source files; BusinessOS preserves each member reference/hash under the canonical source bundle. When supplied materials contain explicit organization-level brand/voice/style/audience instructions, persist them as first-class Brand state. Prefer `--brand-profile-file runtime/<brand>.json` for a small structured Brand manifest grounded in the original source files; a grounded `brand` object inside the facts JSON remains supported. Do not flatten brand voice/style/audience guidance into BusinessClaim constraints merely because it is convenient. Use --preference-profile-file when the user supplied reusable style/work-method preferences so they exist before residual work begins. Do not put task authorization/approval boundaries (for example, do not publish, ask before spending, or no customer contact without approval) into the preference manifest; those remain current request/Run/action-control requirements and formal approvals use the Approval lifecycle. Keep facts files relative to the workspace when practical (for example runtime/northstar-facts.json) to avoid shell/path quoting errors. Do not reverse-engineer or replace this helper if an invocation fails; run --help and correct the supported call.'''
    ap=argparse.ArgumentParser(description='Persist explicit user/first-party setup facts as grounded canonical BusinessOS objects. Unknowns remain unknown; unsupported expansion is rejected.',formatter_class=argparse.RawDescriptionHelpFormatter,epilog=epilog)
    ap.add_argument('business_id',nargs='?',help='Active business ID, e.g. northstar-hvac')
    ap.add_argument('--business-id',dest='business_id_alias',help='Alias for the positional business ID; provided for agent/tool-call robustness.')
    ap.add_argument('--facts-json',help='Inline JSON object containing industries/business_models/markets/services/objectives/lead_sources/approved_claims/claim_constraints.')
    ap.add_argument('--facts-file',help='Path to a JSON facts object. Prefer a temporary runtime/work file rather than product directories.')
    ap.add_argument('--facts-stdin',action='store_true',help='Read the JSON facts object from stdin.')
    ap.add_argument('--industry',action='append',default=[]); ap.add_argument('--business-model',action='append',default=[])
    ap.add_argument('--market',action='append',default=[]); ap.add_argument('--service',action='append',default=[],help='Repeat for each service; comma-separated values are also accepted.')
    ap.add_argument('--objective',action='append',default=[]); ap.add_argument('--lead-source',action='append',default=[],help='Repeat for each lead source; comma-separated values are also accepted.')
    ap.add_argument('--approved-claim',action='append',default=[],help='Repeat an explicitly authorized business/customer-facing claim or promise grounded in the source statement.')
    ap.add_argument('--claim-constraint',action='append',default=[],help='Repeat an explicit claim/marketing constraint, prohibition, or known-absence statement grounded in the source statement.')
    ap.add_argument('--source-reference',default=None,help='Optional override for the canonical grounding source/bundle label; original member refs are still preserved.')
    ap.add_argument('--source-text',action='append',default=[],help='Verbatim/authoritative statement grounding the structured facts. Repeat to combine multiple explicit user statements.')
    ap.add_argument('--source-file',action='append',default=[],help='User-supplied grounding source file. Repeat for multi-source onboarding; original file refs/hashes are preserved in canonical source provenance.')
    ap.add_argument('--brand-profile-file',action='append',default=[],help='Optional structured Brand manifest JSON grounded in the supplied source files. Repeat only when manifests are non-conflicting; values are merged deterministically. Accepts a Brand-shaped object or {"brand": {...}}.')
    ap.add_argument('--preference-profile-file',action='append',default=[],help='Optional PreferenceProfile manifest JSON to persist before residual routing. Repeat for multiple business/team/role/operator preference profiles.')
    ap.add_argument('--residual-request',help='Natural-language part of the original user request that remains after initialization, e.g. "determine what we should do next". When supplied, BusinessOS routes/resolves it automatically after bootstrap.')
    ap.add_argument('--initialization-only',action='store_true',help='Declare that the user requested initialization/persistence only and there is no remaining outcome to route. Do not use this when the original request also asked what to do next, diagnose, research, create, or otherwise continue.')
    a=ap.parse_args()
    business_id=a.business_id or a.business_id_alias
    if a.business_id and a.business_id_alias and a.business_id!=a.business_id_alias:
        ap.error('positional business_id and --business-id disagree')
    if not business_id: ap.error('business_id is required (positional or --business-id)')
    if a.residual_request and a.initialization_only: ap.error('use only one of --residual-request or --initialization-only')
    if not a.residual_request and not a.initialization_only:
        ap.error('completion scope is required: pass --residual-request "<remaining original user request>" when anything remains after setup, or --initialization-only only when setup/persistence was the entire request')
    try:
        source_members=_load_source_members(a.source_text,a.source_file)
        jf=_load_facts(a.facts_json,a.facts_file,a.facts_stdin)
        brand_manifest,brand_profile_files=_load_brand_profile_files(a.brand_profile_file)
        merged_brand=_merge_brand_values(jf.get('brand'),brand_manifest)
        facts={
          'industries':_merge_lists(jf['industries'],a.industry),
          'business_models':_merge_lists(jf['business_models'],a.business_model),
          'markets':_merge_lists(jf['markets'],a.market),
          'services':_merge_lists(jf['services'],a.service),
          'objectives':_merge_lists(jf['objectives'],a.objective),
          'lead_sources':_merge_lists(jf['lead_sources'],a.lead_source),
          'approved_claims':_merge_lists(jf['approved_claims'],a.approved_claim),
          'claim_constraints':_merge_lists(jf['claim_constraints'],a.claim_constraint),
          'brand':merged_brand,
        }
        objs,paths=persist_explicit_context(business_id,**facts,source_reference=a.source_reference,source_members=source_members)
    except (ValueError,FileExistsError) as e:
        raise SystemExit(str(e)+'\nSupported path: run `python3 scripts/bootstrap_explicit_context.py --help`; do not hand-author replacement canonical state.')
    preference_written=[]
    if a.preference_profile_file:
        from upsert_preference_profile import upsert as upsert_preference
        canonical_source=next((o['id'] for o in reversed(objs) if o.get('object_type')=='SourceRecord' and (o.get('extensions') or {}).get('captured_fact_categories') is not None),None)
        for raw in a.preference_profile_file:
            pp=Path(raw);pp=pp if pp.is_absolute() else ROOT/pp
            try: spec=json.loads(pp.read_text())
            except Exception as e: raise SystemExit(f'Could not read --preference-profile-file {raw!r}: {e}')
            if not isinstance(spec,dict) or not isinstance(spec.get('preferences'),dict):
                raise SystemExit(f'Preference profile manifest {raw!r} must be a JSON object with a preferences object')
            applies=spec.get('applies_to') or {}
            try:
                path,obj=upsert_preference(
                    business_id,spec.get('name') or 'Onboarding preferences',spec.get('scope') or 'operator',
                    spec.get('subject_ref'),spec['preferences'],spec.get('id'),int(spec.get('priority',0)),
                    spec.get('source_kind') or 'explicit_user',spec.get('source_refs') or ([canonical_source] if canonical_source else []),
                    applies.get('systems') or [],applies.get('contracts') or [],applies.get('output_types') or [],applies.get('channels') or [],spec.get('notes'))
            except Exception as e: raise SystemExit(f'Could not persist preference profile {raw!r}: {e}')
            preference_written.append({'id':obj['id'],'scope':obj['scope'],'subject_ref':obj['subject_ref'],'path':path.relative_to(ROOT).as_posix()})
    payload={
      'business_id':business_id,
      'objects_written':[{'id':o['id'],'object_type':o['object_type'],'path':p.relative_to(ROOT).as_posix()} for o,p in zip(objs,paths)],
      'preference_profiles_written':preference_written,
      'brand_profile_files_used':brand_profile_files,
      'truth_rule':'only grounded explicit facts were persisted; omitted fields remain unknown',
      'validation_required':f'python3 scripts/validate_business.py {business_id} --require-context',
    }
    if a.residual_request:
        from route_and_resolve import route_and_resolve
        try:
            residual=route_and_resolve(a.residual_request,business_id)
            payload.update({
              'completion_state':'initialization_complete_residual_routed',
              'residual_request':a.residual_request,
              'residual_route':residual,
              'required_next_action':'Validate active business state, then perform the resolved residual process before final response. Explicit Brand guidance supplied through the onboarding Brand path is already durable canonical context and must be included when the resolved contract requests Brand. Explicit reusable preferences supplied during onboarding are already persisted and must be resolved into downstream Runs using the applicable operator/team/role refs. Do not replace the residual outcome with a department/tactic menu. If broad_growth_precheck.status is baseline_required, the next-best work is the smallest first-party constraint baseline; do not substitute generic external research.',
            })
        except Exception as e:
            payload.update({
              'completion_state':'initialization_complete_residual_route_unresolved',
              'residual_request':a.residual_request,
              'residual_route_error':str(e),
              'required_next_action':f'Validate active business state, then route the residual request with: python3 scripts/route_and_resolve.py {json.dumps(a.residual_request)} --business-id {business_id} --show. Do not answer the broader request until that handoff is resolved.',
            })
    else:
        payload.update({
          'completion_state':'initialization_only_complete',
          'required_next_action':'Validate active business state. No residual business outcome was declared for this bootstrap call.',
        })
    print(json.dumps(payload,indent=2))
if __name__=='__main__': main()
