#!/usr/bin/env python3
"""Keep PreferenceProfile limited to reusable expression and work-method choices.

A PreferenceProfile is durable organizational/user customization, not a store for the
current task's action boundary or external permission state. Current-task constraints stay
with the request/work context. A real durable organizational decision may be remembered
as a DecisionRecord when that decision itself has future value.
"""
import re

# These key families describe permission/action-boundary state rather than preference.
FORBIDDEN_KEY_FRAGMENTS={
    'authorization','authorisation','permission','permissions','approval','approvals','consent',
    'allowed_actions','prohibited_actions','authorized_actions','authorised_actions',
    'external_action_boundary','external_action_boundaries','production_action_boundary','production_action_boundaries',
}
ACTION=r'(?:publish|publishing|deploy|deployment|ship|launch|spend|purchase|buy|contact|message|email|call|connect|link|modify|change|edit|run|execute|submit|send|post|release|activate)'
ACTION_BOUNDARY_PATTERNS=[
    re.compile(rf"\b(?:do\s+not|don['’]?t|never|must\s+not|may\s+not|cannot|can['’]?t)\s+{ACTION}\b",re.I),
    re.compile(rf"\b(?:must|need\s+to|needs\s+to|required\s+to|requires?\s+you\s+to)\s+(?:ask|obtain|get|have|receive)\b.{{0,60}}\b(?:approval|authorization|authorisation|permission|consent)\b",re.I),
    re.compile(r"\b(?:explicit\s+)?(?:approval|authorization|authorisation|permission|consent)\s+(?:is\s+|are\s+)?required\b",re.I),
    re.compile(rf"\b(?:authorized|authorised|approved|permitted)\s+to\s+{ACTION}\b",re.I),
    re.compile(r"\b(?:not\s+authorized|not\s+authorised|not\s+approved|not\s+permitted)\b",re.I),
    re.compile(r"\bwithout\s+(?:asking|approval|authorization|authorisation|permission|consent)\b",re.I),
]


def _norm_key(key):return re.sub(r'[^a-z0-9]+','_',str(key).lower()).strip('_')


def forbidden_preference_key(key):
    normalized=_norm_key(key)
    return normalized in FORBIDDEN_KEY_FRAGMENTS or any(
        fragment in normalized for fragment in ('authorization','authorisation','permission','approval')
    )


def forbidden_preference_text(value):
    if not isinstance(value,str):return False
    text=' '.join(value.split())
    return any(pattern.search(text) for pattern in ACTION_BOUNDARY_PATTERNS)


def preference_semantic_errors(preferences,prefix='preferences'):
    errors=[]
    def walk(value,path):
        if isinstance(value,dict):
            for key,item in value.items():
                if forbidden_preference_key(key):
                    errors.append(f'{path}.{key}: action/permission state is not a reusable PreferenceProfile value')
                walk(item,f'{path}.{key}')
        elif isinstance(value,list):
            for i,item in enumerate(value):walk(item,f'{path}[{i}]')
        elif isinstance(value,str) and forbidden_preference_text(value):
            errors.append(f'{path}: current action boundary is not a reusable PreferenceProfile value: {" ".join(value.split())!r}')
    if not isinstance(preferences,dict):return [f'{prefix}: preferences must be an object']
    walk(preferences,prefix)
    return errors


def validate_preference_semantics(preferences,prefix='preferences'):
    errors=preference_semantic_errors(preferences,prefix)
    if errors:
        raise ValueError(
            '; '.join(errors[:10])+
            '. Keep reusable style/work-method choices in PreferenceProfile; keep current task constraints in the request/work context. '
            'Persist a DecisionRecord only when a real durable organizational decision itself has future value. '
            'External account, legal, platform, and environment permission state remains outside PreferenceProfile.'
        )
    return preferences
