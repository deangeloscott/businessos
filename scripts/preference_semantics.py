#!/usr/bin/env python3
"""Semantic guardrails and legacy cleanup for PreferenceProfile payloads.

Preferences customize otherwise-valid choices. They must not become a durable
permission/approval store or silently convert a one-task action boundary into
reusable operator/business state.
"""
import copy
import hashlib
import json
import re

FORBIDDEN_KEY_FRAGMENTS={
    'authorization','authorisation','permission','permissions','approval','approvals','consent',
    'requires_approval','required_approval','approval_required','authorization_required','permission_required',
    'allowed_actions','prohibited_actions','authorized_actions','authorised_actions',
    'external_action_boundary','external_action_boundaries','production_action_boundary','production_action_boundaries',
    'approval_boundary','approval_boundaries','authorization_boundary','authorization_boundaries',
}
ACTION=r'(?:publish|publishing|deploy|deployment|ship|launch|spend|purchase|buy|contact|message|email|call|connect|link|modify|change|edit|run|execute|submit|send|post|release|activate)'
TEXT_PATTERNS=[
    re.compile(rf"\b(?:do\s+not|don['’]?t|never|must\s+not|may\s+not|cannot|can['’]?t)\s+{ACTION}\b",re.I),
    re.compile(rf"\b(?:must|need\s+to|needs\s+to|required\s+to|requires?\s+you\s+to)\s+(?:ask|obtain|get|have|receive)\b.{{0,60}}\b(?:approval|authorization|authorisation|permission|consent)\b",re.I),
    re.compile(r"\b(?:explicit\s+)?(?:approval|authorization|authorisation|permission|consent)\s+(?:is\s+|are\s+)?required\b",re.I),
    re.compile(rf"\b(?:authorized|authorised|approved|permitted)\s+to\s+{ACTION}\b",re.I),
    re.compile(r"\b(?:not\s+authorized|not\s+authorised|not\s+approved|not\s+permitted)\b",re.I),
    re.compile(r"\b(?:approval|authorization|authorisation|permission)\s+boundar(?:y|ies)\b",re.I),
    re.compile(r"\bwithout\s+(?:asking|approval|authorization|authorisation|permission|consent)\b",re.I),
]


def _norm_key(k):return re.sub(r'[^a-z0-9]+','_',str(k).lower()).strip('_')

def forbidden_preference_key(key):
    nk=_norm_key(key)
    return nk in FORBIDDEN_KEY_FRAGMENTS or any(frag in nk for frag in ('authorization','authorisation','permission','approval'))

def forbidden_preference_text(value):
    if not isinstance(value,str):return False
    text=' '.join(value.split());return any(pat.search(text) for pat in TEXT_PATTERNS)

def preference_semantic_errors(preferences,prefix='preferences'):
    errors=[]
    def walk(v,path):
        if isinstance(v,dict):
            for k,x in v.items():
                if forbidden_preference_key(k):errors.append(f'{path}.{k}: authorization/approval state is not a PreferenceProfile value')
                walk(x,f'{path}.{k}')
        elif isinstance(v,list):
            for i,x in enumerate(v):walk(x,f'{path}[{i}]')
        elif isinstance(v,str):
            text=' '.join(v.split())
            if forbidden_preference_text(text):errors.append(f'{path}: authorization/approval boundary must not be stored as a preference: {text!r}')
    if not isinstance(preferences,dict):return [f'{prefix}: preferences must be an object']
    walk(preferences,prefix);return errors

def _fingerprint(value):
    raw=json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode();return hashlib.sha256(raw).hexdigest()

def sanitize_legacy_preferences(preferences,prefix='preferences'):
    if not isinstance(preferences,dict):raise ValueError(f'{prefix}: preferences must be an object')
    DROP=object();removals=[]
    def record(path,reason,value):removals.append({'path':path,'reason':reason,'value_sha256':_fingerprint(value)})
    def clean(value,path):
        if isinstance(value,dict):
            out={};changed=False
            for key,item in value.items():
                child=f'{path}.{key}'
                if forbidden_preference_key(key):record(child,'authorization_key',item);changed=True;continue
                cleaned=clean(item,child)
                if cleaned is DROP:changed=True;continue
                out[key]=cleaned
                if cleaned!=item:changed=True
            if changed and not out and path!=prefix:return DROP
            return out
        if isinstance(value,list):
            out=[];changed=False
            for i,item in enumerate(value):
                cleaned=clean(item,f'{path}[{i}]')
                if cleaned is DROP:changed=True;continue
                out.append(cleaned)
                if cleaned!=item:changed=True
            if changed and not out:return DROP
            return out
        if isinstance(value,str) and forbidden_preference_text(value):record(path,'authorization_text',value);return DROP
        return copy.deepcopy(value)
    cleaned=clean(preferences,prefix)
    if cleaned is DROP:cleaned={}
    residual=preference_semantic_errors(cleaned,prefix)
    if residual:raise ValueError('Legacy preference cleanup left invalid action-boundary semantics: '+'; '.join(residual[:10]))
    return cleaned,removals

def validate_preference_semantics(preferences,prefix='preferences'):
    errors=preference_semantic_errors(preferences,prefix)
    if errors:
        raise ValueError('; '.join(errors[:10])+'. Keep reusable style/work-method choices in PreferenceProfile; keep current task/action constraints in the user request/work context. Persist a DecisionRecord only when a real organizational decision itself has future value. External account/legal/platform/organizational authorization remains external to AURA.')
    return preferences
