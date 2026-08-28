#!/usr/bin/env python3
from _common import *
from build_claim_manifest import business_name, is_candidate
from claim_surface import TEXT_NATIVE_EXTS, asset_claim_units
import re

ALLOWED={'approved_business_claim','general_guidance','placeholder'}
# Terms/phrases that often enlarge a promise. They are allowed only when present in supporting canonical text.
ESCALATION=[
    r'\bboth\b',r'\beach\b',r'\bevery\b',r'\balways\b',r'\bnever\b',r'\bguarantee(?:d|s)?\b',
    r'\bfree\b',r'\bdiscount\b',r'\bfinanc(?:e|ing)\b',r'\bwarrant(?:y|ies)\b',r'\blicensed\b',r'\bcertified\b',
    r'\bsame[- ]day\b',r'\b24/7\b',r'\bno[- ]pressure\b',r'\bpressure[- ]free\b',r'\bseparate\b',r'\btwo\b',
    r'\bon your timeline\b',r"\bwe won['’]?t\b",r'\b#?1\b',r'\bbest\b',r'\btop[- ]rated\b',
    r'\bany\s+time\b',r'\banytime\b',r'\bnothing\b',r'\beverything\b',
    r'\bno\s+setup\b',r'\bzero\s+setup\b',r'\b\d+\s*[- ]?(?:minute|hour|day|week|month|year)s?\b'
]

STOP={
    'a','an','and','are','as','at','be','been','being','but','by','can','could','did','do','does','for','from','had','has','have',
    'he','her','hers','him','his','i','if','in','into','is','it','its','may','might','my','of','on','or','our','ours','she','should',
    'so','than','that','the','their','theirs','them','then','there','these','they','this','those','to','us','was','we','were','what',
    'when','where','which','who','will','with','would','you','your','yours','about','re','ll','ve','m','s','t','d'
}
ACTION_VERBS={
    'provide','offer','explain','serve','install','repair','replace','guarantee','include','deliver','support','give','handle','specialize',
    'promise','ensure','finance','charge','price','respond','arrive','schedule','request','contact','walk','help','make','sell','buy','build',
    'create','perform','conduct','inspect','evaluate','assess','maintain','service','supply','ship','send','return','refund','cover','protect'
}
GENERIC_RECIPIENT={'customer','client','homeowner','buyer','seller','user','people','person','business','company','organization','resident','audience'}


def _norm(s):return re.sub(r'\s+',' ',re.sub(r'[^a-z0-9\[\]#]+',' ',(s or '').lower())).strip()

def _stem(tok):
    t=tok.lower().strip()
    if len(t)>5 and t.endswith('ies'): t=t[:-3]+'y'
    elif len(t)>5 and t.endswith('ing'): t=t[:-3]
    elif len(t)>4 and t.endswith('ed'): t=t[:-2]
    elif len(t)>4 and t.endswith('es'): t=t[:-2]
    elif len(t)>3 and t.endswith('s') and not t.endswith('ss'): t=t[:-1]
    if t in {'provid','provided'}: t='provide'
    if t in {'estimat'}: t='estimate'
    if t in {'serv','served','servic'}: t='serve'
    if t in {'replac'}: t='replace'
    if t in {'financ'}: t='finance'
    return t

def _tokens(text,name=''):
    name_tokens={_stem(x) for x in re.findall(r'[a-z0-9]+',(name or '').lower())}
    out=[]
    for raw in re.findall(r'[a-z0-9]+',(text or '').lower()):
        t=_stem(raw)
        if not t or t in STOP or t in name_tokens or len(t)<3: continue
        out.append(t)
    return out

def _core_clause(text):
    s=text or ''
    s=re.split(r'\s+[—–-]\s+|,\s+so\b|;\s*so\b|\s+so\s+(?:you|customers?|clients?|homeowners?|people)\b',s,maxsplit=1,flags=re.I)[0]
    return s.strip()

def _support_text(obj):
    typ=obj.get('object_type')
    if typ=='BusinessClaim':return obj.get('statement','')
    vals=[]
    if typ=='Business':vals=[obj.get('name','')]+obj.get('industries',[])+obj.get('business_models',[])
    elif typ=='Market':vals=[obj.get('name',''),obj.get('geography','')]
    elif typ=='ProductService':vals=[obj.get('name',''),obj.get('description','')]
    elif typ=='Objective':vals=[obj.get('name','')]
    return ' '.join(x for x in vals if x)

def _trusted(obj):
    if obj.get('object_type')=='BusinessClaim':
        authority=obj.get('authority')
        trusted=bool(obj.get('status')=='approved' and obj.get('claim_kind')=='approved_business_claim' and authority in {'explicit_user','verified_first_party'})
        if authority=='verified_first_party':trusted=trusted and bool(obj.get('source_ref') and obj.get('support_quote'))
        return trusted
    ext=obj.get('extensions',{}) if isinstance(obj.get('extensions'),dict) else {}
    bos=ext.get('businessos',{}) if isinstance(ext.get('businessos'),dict) else {}
    return bos.get('authority') in {'explicit_user','verified_first_party'}

def _is_general_business_claim(text,name):
    return is_candidate(text,name)

def _substantive_support(sent,support_objs,name):
    core=_core_clause(sent); stoks=_tokens(core,name)
    if not stoks:return True
    support_texts=[_support_text(o) for o in support_objs]; all_support=set(_tokens(' '.join(support_texts),name))
    if not all_support:return False
    if 'commitment' in stoks and any(o.get('object_type')=='BusinessClaim' for o in support_objs):return True
    action_pos=next((i for i,t in enumerate(stoks) if t in ACTION_VERBS),None)
    if action_pos is not None:
        action=stoks[action_pos]
        if action in {'contact','request','schedule'}:objs=[t for t in stoks[action_pos+1:] if t not in GENERIC_RECIPIENT]
        else:objs=[t for t in stoks[action_pos+1:] if t not in ACTION_VERBS and t not in GENERIC_RECIPIENT]
        overlap=[t for t in objs if t in all_support]
        if objs:
            ratio=len(overlap)/len(set(objs))
            if ratio < 0.60 and len(set(overlap)) < 2:return False
        if action not in all_support and len(set(overlap)) < 2:return False
        return True
    overlap=set(stoks)&all_support
    if len(overlap)>=2:return True
    if len(stoks)==1 and next(iter(set(stoks)),None) in all_support:return True
    return False

def validate_manifest_sentences(manifest,sentences,idx,name,rel):
    errors=[]
    if not isinstance(manifest,list):return [f'{rel} requires a claim manifest list; run the supported claim scanner and classify every candidate']
    bytext={_norm(x.get('text')):x for x in manifest if isinstance(x,dict) and x.get('text')}
    for sent in sentences:
        m=bytext.get(_norm(sent))
        if not m:
            errors.append(f'{rel} claim manifest missing artifact statement: {sent!r}');continue
        cls=m.get('classification')
        if cls not in ALLOWED:
            errors.append(f'{rel} claim {sent!r} has invalid classification {cls!r}');continue
        if cls=='placeholder':
            if '[' not in sent or ']' not in sent:errors.append(f'{rel} placeholder claim must be visibly placeholder-marked: {sent!r}')
            continue
        if cls=='general_guidance':
            if _is_general_business_claim(sent,name):errors.append(f'{rel} business-specific/promise-like statement cannot be classified as general_guidance: {sent!r}')
            continue
        refs=m.get('support_refs') or []
        if not refs:errors.append(f'{rel} approved business claim lacks support_refs: {sent!r}');continue
        support_objs=[];bad=[]
        for rid in refs:
            ent=idx.get(rid)
            if not ent or not _trusted(ent[0]):bad.append(rid);continue
            support_objs.append(ent[0])
        if bad:errors.append(f'{rel} approved business claim uses missing/untrusted support refs {bad}: {sent!r}')
        if support_objs and not _substantive_support(sent,support_objs,name):errors.append(f'{rel} approved business claim support_refs do not substantively authorize the customer-facing predicate: {sent!r}')
        corpus=' '.join(_support_text(o) for o in support_objs).lower()
        for pat in ESCALATION:
            hit=re.search(pat,sent.lower())
            if hit and not re.search(pat,corpus):errors.append(f'{rel} claim enlarges supported promise with unsupported term/phrase {hit.group(0)!r}: {sent!r}')
    return errors

def claim_errors(business_id,objects=None):
    errors=[]; idx=object_index(business_id); name=business_name(business_id)
    if objects is None:objects=list(idx.values())
    else:objects=[(o,ROOT/p) if isinstance(p,str) else (o,p) for o,p in objects]
    for asset,path in objects:
        if asset.get('object_type')!='Asset' or asset.get('owner_system') not in {'content-synthesis','marketing-synthesis'}:continue
        loc=asset.get('location_reference')
        if not loc:continue
        fp=Path(loc); fp=fp if fp.is_absolute() else ROOT/fp
        if not fp.exists():continue
        bos=(asset.get('extensions') or {}).get('businessos',{}) if isinstance(asset.get('extensions'),dict) else {}
        customer_facing=bos.get('customer_facing', True)
        if customer_facing is False:continue
        origin=str(bos.get('origin','')).lower(); produced=bool(bos.get('run_ref') or bos.get('run_id')) and origin not in {'imported','preexisting'}
        # Existing opaque imports are not retroactively forced through a sidecar until they
        # are mutated or newly produced. New rendered media may not bypass claim governance.
        if fp.suffix.lower() not in TEXT_NATIVE_EXTS and not produced:continue
        rel=str(path.relative_to(ROOT)) if isinstance(path,Path) and path.is_absolute() else str(path)
        candidates,surface_error=asset_claim_units(asset,fp)
        if surface_error:
            errors.append(f'{rel} {surface_error}');continue
        manifest=bos.get('claim_manifest')
        if not isinstance(manifest,list):
            errors.append(f'{rel} customer-facing {asset.get("owner_system")} Asset requires extensions.businessos.claim_manifest; run scripts/build_claim_manifest.py and classify every candidate')
            continue
        errors.extend(validate_manifest_sentences(manifest,candidates,idx,name,rel))
    return errors
